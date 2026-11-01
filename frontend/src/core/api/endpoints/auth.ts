import { api, ensureCsrfCookie } from "@/core/api/client"

export interface ApiUser {
    id: string
    email: string
    first_name: string
    last_name: string
    avatar: string | null
    language: "fa" | "en" | "ar"
    organizations: Array<{
        id: string
        name: string
        slug: string
        role: "owner" | "admin" | "member"
    }>
}

export interface LoginPayload {
    email: string
    password: string
}

export interface RegisterPayload {
    email: string
    password: string
    first_name?: string
    last_name?: string
    organization_name: string
}

export const authApi = {
    async login(payload: LoginPayload): Promise<ApiUser> {
        await ensureCsrfCookie()
        const { data } = await api.post<ApiUser>("/auth/login/", payload)
        return data
    },

    async register(payload: RegisterPayload): Promise<ApiUser> {
        await ensureCsrfCookie()
        const { data } = await api.post<ApiUser>("/auth/register/", payload)
        return data
    },

    async logout(): Promise<void> {
        await api.post("/auth/logout/")
    },

    async me(): Promise<ApiUser> {
        const { data } = await api.get<ApiUser>("/auth/me/")
        return data
    },

    async googleUrl(redirect: string): Promise<string> {
        const { data } = await api.get<{ url: string }>("/auth/google/", {
            params: { redirect },
        })
        return data.url
    },
}