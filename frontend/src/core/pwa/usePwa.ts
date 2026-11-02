import { ref } from "vue"

interface BeforeInstallPromptEvent extends Event {
    prompt: () => Promise<void>
    userChoice: Promise<{ outcome: "accepted" | "dismissed" }>
}

const deferredPrompt = ref<BeforeInstallPromptEvent | null>(null)
const isInstalled = ref(false)
const isOffline = ref(!navigator.onLine)
const updateAvailable = ref(false)

let swRegistration: ServiceWorkerRegistration | undefined
let initialized = false

export function initPwa(): void {
    if (initialized) return
    initialized = true

    // Detect if already running as installed PWA
    isInstalled.value = window.matchMedia("(display-mode: standalone)").matches

    // Listen for install prompt
    window.addEventListener("beforeinstallprompt", (e) => {
        e.preventDefault()
        deferredPrompt.value = e as BeforeInstallPromptEvent
    })

    window.addEventListener("appinstalled", () => {
        isInstalled.value = true
        deferredPrompt.value = null
    })

    // Online/offline
    window.addEventListener("online", () => (isOffline.value = false))
    window.addEventListener("offline", () => (isOffline.value = true))

    // Service worker registration (dynamic import so SSR-safe)
    import("virtual:pwa-register").then(({ registerSW }) => {
        registerSW({
            immediate: true,
            onRegisteredSW(_swUrl, registration) {
                swRegistration = registration
            },
            onNeedRefresh() {
                updateAvailable.value = true
            },
            onOfflineReady() {
                // eslint-disable-next-line no-console
                console.info("[PWA] App ready to work offline")
            },
        })
    })
}

export function usePwa() {
    async function install(): Promise<boolean> {
        if (!deferredPrompt.value) return false
        await deferredPrompt.value.prompt()
        const choice = await deferredPrompt.value.userChoice
        deferredPrompt.value = null
        return choice.outcome === "accepted"
    }

    async function applyUpdate(): Promise<void> {
        if (!swRegistration) {
            window.location.reload()
            return
        }
        try {
            await swRegistration.update()
        } catch {
            // If SW update fails (e.g. offline), reload anyway
        }
        window.location.reload()
    }

    function dismissUpdate(): void {
        updateAvailable.value = false
    }

    return {
        canInstall: deferredPrompt,
        isInstalled,
        isOffline,
        updateAvailable,
        install,
        applyUpdate,
        dismissUpdate,
    }
}