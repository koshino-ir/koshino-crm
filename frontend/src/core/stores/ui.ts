import { defineStore } from "pinia"
import { computed, ref } from "vue"

import { appConfig } from "@/core/config"

type Theme = "light" | "dark"

export const useUiStore = defineStore("ui", () => {
    const theme = ref<Theme>(
        (localStorage.getItem(appConfig.storageKeys.theme) as Theme) || "light",
    )
    const sidebarCollapsed = ref(false)

    const isDark = computed(() => theme.value === "dark")

    function applyTheme(): void {
        document.documentElement.classList.toggle("dark", isDark.value)
    }

    function toggleTheme(): void {
        theme.value = isDark.value ? "light" : "dark"
        localStorage.setItem(appConfig.storageKeys.theme, theme.value)
        applyTheme()
    }

    function toggleSidebar(): void {
        sidebarCollapsed.value = !sidebarCollapsed.value
    }

    // Apply once on store init
    applyTheme()

    return { theme, isDark, sidebarCollapsed, toggleTheme, toggleSidebar }
})