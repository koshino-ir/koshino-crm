import axios, {
    AxiosError,
    type AxiosInstance,
    type InternalAxiosRequestConfig,
} from "axios"

import { appConfig } from "@/core/config"

// --- Types ---

export interface ApiEnvelope<T = unknown> {
    success: boolean
    data: T
    message: string
    errors: unknown
    meta: unknown
}

export interface PaginationMeta {
    count: number
    page: number
    page_size: number
    total_pages: number
}

export class ApiError extends Error {
    status: number
    errors: unknown

    constructor(message: string, status: number, errors: unknown) {
        super(message)
        this.name = "ApiError"
        this.status = status
        this.errors = errors
    }

    /**
     * Normalize the backend's `errors` payload into `{ field: string[] }`.
     * Handles DRF's shapes:
     *   { "password": ["..."] }
     *   { "email": "..." }
     *   { "detail": "..." }
     *   ["..."]
     */
    fieldErrors(): Record<string, string[]> {
        const e = this.errors
        if (!e) return {}

        const result: Record<string, string[]> = {}

        if (Array.isArray(e)) {
            result.non_field_errors = e.map(String)
            return result
        }

        if (typeof e === "object") {
            for (const [key, value] of Object.entries(e as Record<string, unknown>)) {
                if (Array.isArray(value)) {
                    result[key] = value.map((v) => String(v))
                } else if (typeof value === "string") {
                    result[key] = [value]
                } else if (value && typeof value === "object") {
                    const flat: string[] = []
                    for (const v of Object.values(value as Record<string, unknown>)) {
                        if (Array.isArray(v)) flat.push(...v.map(String))
                        else if (typeof v === "string") flat.push(v)
                    }
                    if (flat.length > 0) result[key] = flat
                }
            }
        }

        return result
    }

    /** Short label for the first error (useful as a toast or summary). */
    firstError(): string {
        const fields = this.fieldErrors()
        for (const messages of Object.values(fields)) {
            if (messages.length > 0) return messages[0]
        }
        return this.message || "Request failed"
    }
}

// --- CSRF helpers ---

function getCookie(name: string): string | null {
    const match = document.cookie.match(
        new RegExp("(^|;\\s*)" + name + "=([^;]*)"),
    )
    return match ? decodeURIComponent(match[2]) : null
}

const UNSAFE_METHODS = new Set(["post", "put", "patch", "delete"])

// --- Axios instance ---

export const api: AxiosInstance = axios.create({
    baseURL: appConfig.apiBaseUrl,
    withCredentials: true,
    headers: { "Content-Type": "application/json" },
    timeout: 15000,
})

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
    const method = (config.method || "get").toLowerCase()
    if (UNSAFE_METHODS.has(method)) {
        const token = getCookie("csrftoken")
        if (token) {
            config.headers.set("X-CSRFToken", token)
        }
    }

    // Multi-tenancy: current org
    const orgId = localStorage.getItem(appConfig.storageKeys.orgId)
    if (orgId) {
        config.headers.set("X-Organization-Id", orgId)
    }

    return config
})

// --- Refresh coordination (single-flight) ---

let refreshPromise: Promise<void> | null = null

async function refreshSession(): Promise<void> {
    if (!refreshPromise) {
        refreshPromise = api
            .post("/auth/token/refresh/")
            .then(() => undefined)
            .finally(() => {
                refreshPromise = null
            })
    }
    return refreshPromise
}

const AUTH_ENDPOINTS = ["/auth/login/", "/auth/register/", "/auth/token/refresh/"]

function isAuthEndpoint(url?: string): boolean {
    if (!url) return false
    return AUTH_ENDPOINTS.some((e) => url.includes(e))
}

// --- Response handling ---

api.interceptors.response.use(
    (response) => {
        // Unwrap envelope → views get pure data
        const envelope = response.data as ApiEnvelope
        if (envelope && typeof envelope === "object" && "success" in envelope) {
            if (!envelope.success) {
                throw new ApiError(envelope.message || "Request failed", 400, envelope.errors)
            }
            response.data = envelope.data
            if (envelope.meta) {
                ; (response as unknown as { meta: unknown }).meta = envelope.meta
            }
        }
        return response
    },
    async (error: AxiosError) => {
        const original = error.config as InternalAxiosRequestConfig & { _retried?: boolean }
        const status = error.response?.status

        // Refresh on 401 (unless it's an auth endpoint or we already retried)
        if (status === 401 && original && !original._retried && !isAuthEndpoint(original.url)) {
            original._retried = true
            try {
                await refreshSession()
                return api(original)
            } catch {
                window.dispatchEvent(new CustomEvent("auth:expired"))
            }
        }

        const envelope = error.response?.data as ApiEnvelope | undefined
        const message =
            envelope?.message || error.message || "Network error"
        throw new ApiError(message, status ?? 0, envelope?.errors)
    },
)

/**
 * Ensures a CSRF cookie exists before the first unsafe request.
 * The backend exposes GET /auth/csrf/ returning the token and setting the cookie.
 */
export async function ensureCsrfCookie(): Promise<void> {
    if (getCookie("csrftoken")) return
    try {
        await api.get("/auth/csrf/")
    } catch {
        // Non-fatal — the login endpoint tolerates missing CSRF.
    }
}