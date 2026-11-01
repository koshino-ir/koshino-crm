import { VueQueryPlugin } from "@tanstack/vue-query"
import { createPinia } from "pinia"
import { createApp } from "vue"

import App from "./App.vue"
import { i18n } from "@/core/i18n"
import router from "@/core/router"
import "@/assets/styles/main.css"

const app = createApp(App)

app.use(createPinia())
app.use(i18n)
app.use(router)
app.use(VueQueryPlugin)

app.mount("#app")