import { defineStore } from "pinia"
import { computed, ref, watchEffect } from "vue"

import { appConfig } from "@/core/config"
import { useAuthStore } from "@/core/stores/auth"

export interface OrgMembership {
    id: string
    name: string
    slug: string
    role: "owner" | "admin" | "member"
}

export const useOrganizationStore = defineStore("organization", () => {
    const currentId = ref<string | null>(null)

    // Sync with auth + localStorage
    watchEffect(() => {
        const auth = useAuthStore()
        const orgs = auth.user?.organizations ?? []
        if (orgs.length === 0) {
            currentId.value = null
            return
        }
        const stored = localStorage.getItem(appConfig.storageKeys.orgId)
        const valid = stored && orgs.some((o) => o.id === stored)
        currentId.value = valid ? stored : orgs[0].id
        if (!valid && currentId.value) {
            localStorage.setItem(appConfig.storageKeys.orgId, currentId.value)
        }
    })

    function setCurrent(orgs: OrgMembership[], id?: string): void {
        const chosen = id ?? orgs[0]?.id ?? null
        if (chosen) {
            currentId.value = chosen
            localStorage.setItem(appConfig.storageKeys.orgId, chosen)
        } else {
            clear()
        }
    }

    function clear(): void {
        currentId.value = null
        localStorage.removeItem(appConfig.storageKeys.orgId)
    }

    return { currentId, setCurrent, clear }
})

export function useCurrentOrg() {
    const auth = useAuthStore()
    const orgStore = useOrganizationStore()

    return computed<OrgMembership | null>(() => {
        const orgs = auth.user?.organizations ?? []
        return orgs.find((o) => o.id === orgStore.currentId) ?? orgs[0] ?? null
    })
}