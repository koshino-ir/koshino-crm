import { defineStore } from "pinia"
import { computed, ref } from "vue"

import { ApiError } from "@/core/api/client"
import {
    authApi,
    type ApiUser,
    type LoginPayload,
    type RegisterPayload,
} from "@/core/api/endpoints/auth"

export const useAuthStore = defineStore("auth", () => {
    const user = ref<ApiUser | null>(null)
    const initialized = ref(false)
    const loading = ref(false)

    const isAuthenticated = computed(() => user.value !== null)

    async function init(): Promise<void> {
        if (initialized.value) return
        try {
            user.value = await authApi.me()
        } catch (err) {
            if (err instanceof ApiError && err.status === 401) {
                user.value = null
            } else {
                throw err
            }
        } finally {
            initialized.value = true
        }
    }

    async function login(payload: LoginPayload): Promise<void> {
        loading.value = true
        try {
            user.value = await authApi.login(payload)
            initialized.value = true
        } finally {
            loading.value = false
        }
    }

    async function register(payload: RegisterPayload): Promise<void> {
        loading.value = true
        try {
            user.value = await authApi.register(payload)
            initialized.value = true
        } finally {
            loading.value = false
        }
    }

    async function logout(): Promise<void> {
        try {
            await authApi.logout()
        } finally {
            user.value = null
        }
    }

    // Auto-logout when refresh fails
    if (typeof window !== "undefined") {
        window.addEventListener("auth:expired", () => {
            user.value = null
        })
    }

    return {
        user,
        initialized,
        loading,
        isAuthenticated,
        init,
        login,
        register,
        logout,
    }
})