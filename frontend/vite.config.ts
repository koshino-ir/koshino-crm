import { fileURLToPath, URL } from "node:url"

import tailwindcss from "@tailwindcss/vite"
import vue from "@vitejs/plugin-vue"
import { defineConfig } from "vite"
import { VitePWA } from "vite-plugin-pwa"

export default defineConfig({
    plugins: [
        vue(),
        tailwindcss(),
        VitePWA({
            registerType: "prompt",
            injectRegister: false,
            includeAssets: ["favicon.svg", "apple-touch-icon.png", "robots.txt"],
            manifest: false, // we provide our own manifest.webmanifest
            workbox: {
                globPatterns: ["**/*.{js,css,html,svg,png,ico,woff2}"],
                navigateFallback: "/offline.html",
                navigateFallbackDenylist: [/^\/api\//, /^\/admin\//],
                runtimeCaching: [
                    {
                        // API: network-first, fall back to cached response
                        urlPattern: ({ url }) => url.pathname.startsWith("/api/"),
                        handler: "NetworkFirst",
                        options: {
                            cacheName: "koshino-api",
                            networkTimeoutSeconds: 5,
                            expiration: {
                                maxEntries: 100,
                                maxAgeSeconds: 60 * 60 * 24, // 1 day
                            },
                            cacheableResponse: { statuses: [0, 200] },
                        },
                    },
                    {
                        // Google Fonts / fontsource
                        urlPattern: /\.(woff2?|ttf|otf)$/,
                        handler: "CacheFirst",
                        options: {
                            cacheName: "koshino-fonts",
                            expiration: { maxEntries: 20, maxAgeSeconds: 60 * 60 * 24 * 365 },
                        },
                    },
                    {
                        // Images
                        urlPattern: /\.(?:png|jpg|jpeg|svg|gif|webp|ico)$/,
                        handler: "CacheFirst",
                        options: {
                            cacheName: "koshino-images",
                            expiration: { maxEntries: 60, maxAgeSeconds: 60 * 60 * 24 * 30 },
                        },
                    },
                ],
            },
            devOptions: {
                enabled: false, // enable manually when testing (see step 9)
                type: "module",
            },
        }),
    ],
    resolve: {
        alias: {
            "@": fileURLToPath(new URL("./src", import.meta.url)),
        },
    },
    server: {
        port: 5173,
        host: "0.0.0.0",
        proxy: {
            "/api": {
                target: "http://localhost:8000",
                changeOrigin: true,
            },
        },
    },
})