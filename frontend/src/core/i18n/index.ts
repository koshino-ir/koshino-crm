import { createI18n } from "vue-i18n"

import ar from "./locales/ar.json"
import en from "./locales/en.json"
import fa from "./locales/fa.json"

export type AppLocale = "fa" | "en" | "ar"

const STORAGE_KEY = "koshino:locale"

const RTL_LOCALES: AppLocale[] = ["fa", "ar"]

export function isRtl(locale: AppLocale): boolean {
    return RTL_LOCALES.includes(locale)
}

function detectInitialLocale(): AppLocale {
    const stored = localStorage.getItem(STORAGE_KEY) as AppLocale | null
    if (stored && ["fa", "en", "ar"].includes(stored)) return stored
    const browser = navigator.language.toLowerCase()
    if (browser.startsWith("fa")) return "fa"
    if (browser.startsWith("ar")) return "ar"
    return "en"
}

export const i18n = createI18n({
    legacy: false,
    locale: detectInitialLocale(),
    fallbackLocale: "en",
    messages: { fa, en, ar },
})

export function applyDocumentLocale(locale: AppLocale) {
    document.documentElement.lang = locale
    document.documentElement.dir = isRtl(locale) ? "rtl" : "ltr"
}

export function setLocale(locale: AppLocale) {
    i18n.global.locale.value = locale
    localStorage.setItem(STORAGE_KEY, locale)
    applyDocumentLocale(locale)
}

// Apply once on module load so initial render is correct
applyDocumentLocale(i18n.global.locale.value as AppLocale)