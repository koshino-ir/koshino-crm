import { onBeforeUnmount, watchEffect } from "vue"

export interface SeoOptions {
    title: string
    description?: string
    image?: string
    url?: string
    type?: "website" | "article"
    noindex?: boolean
}

const DEFAULT_TITLE = "Koshino CRM"
const DEFAULT_DESCRIPTION =
    "Customer Relationship Management for modern teams. Track deals, manage pipelines, and grow revenue."
const DEFAULT_IMAGE = "/pwa-512x512.png"
const SITE_URL =
    typeof window !== "undefined" ? window.location.origin : ""

function setMeta(attr: "name" | "property", key: string, content: string): void {
    let el = document.head.querySelector<HTMLMetaElement>(
        `meta[${attr}="${key}"]`,
    )
    if (!el) {
        el = document.createElement("meta")
        el.setAttribute(attr, key)
        document.head.appendChild(el)
    }
    el.setAttribute("content", content)
}

function removeMeta(attr: "name" | "property", key: string): void {
    document.head
        .querySelector<HTMLMetaElement>(`meta[${attr}="${key}"]`)
        ?.remove()
}

function setLink(rel: string, href: string): void {
    let el = document.head.querySelector<HTMLLinkElement>(`link[rel="${rel}"]`)
    if (!el) {
        el = document.createElement("link")
        el.setAttribute("rel", rel)
        document.head.appendChild(el)
    }
    el.setAttribute("href", href)
}

export function useSeo(options: SeoOptions): void {
    const original = document.title

    watchEffect(() => {
        const title = options.title ? `${options.title} · ${DEFAULT_TITLE}` : DEFAULT_TITLE
        const description = options.description ?? DEFAULT_DESCRIPTION
        const image = options.image
            ? options.image.startsWith("http")
                ? options.image
                : `${SITE_URL}${options.image}`
            : `${SITE_URL}${DEFAULT_IMAGE}`
        const url = options.url
            ? `${SITE_URL}${options.url}`
            : `${SITE_URL}${window.location.pathname}`

        document.title = title
        setMeta("name", "description", description)

        if (options.noindex) {
            setMeta("name", "robots", "noindex, nofollow")
        } else {
            removeMeta("name", "robots")
        }

        setMeta("property", "og:title", title)
        setMeta("property", "og:description", description)
        setMeta("property", "og:image", image)
        setMeta("property", "og:url", url)
        setMeta("property", "og:type", options.type ?? "website")
        setMeta("property", "og:site_name", DEFAULT_TITLE)

        setMeta("name", "twitter:card", "summary_large_image")
        setMeta("name", "twitter:title", title)
        setMeta("name", "twitter:description", description)
        setMeta("name", "twitter:image", image)

        setLink("canonical", url)
    })

    onBeforeUnmount(() => {
        document.title = original
    })
}