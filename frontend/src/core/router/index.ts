import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router"

import { useAuthStore } from "@/core/stores/auth"

const Placeholder = () => import("@/modules/dashboard/pages/PlaceholderPage.vue")

const placeholderRoutes: RouteRecordRaw[] = [
    { path: "/tasks", name: "tasks", component: Placeholder, meta: { requiresAuth: true, titleKey: "nav.tasks" } },
    { path: "/projects", name: "projects", component: Placeholder, meta: { requiresAuth: true, titleKey: "nav.projects" } },
    { path: "/invoices", name: "invoices", component: Placeholder, meta: { requiresAuth: true, titleKey: "nav.invoices" } },
    { path: "/settings", name: "settings", component: Placeholder, meta: { requiresAuth: true, titleKey: "nav.settings" } },
]

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: "/", redirect: "/dashboard" },

        // --- Auth ---
        { path: "/login", name: "login", component: () => import("@/modules/auth/pages/LoginPage.vue"), meta: { guestOnly: true, layout: "auth" } },
        { path: "/register", name: "register", component: () => import("@/modules/auth/pages/RegisterPage.vue"), meta: { guestOnly: true, layout: "auth" } },
        { path: "/auth/callback", name: "auth-callback", component: () => import("@/modules/auth/pages/AuthCallbackPage.vue"), meta: { layout: "auth" } },

        // --- App ---
        { path: "/dashboard", name: "dashboard", component: () => import("@/modules/dashboard/pages/DashboardPage.vue"), meta: { requiresAuth: true } },
        ...placeholderRoutes,

        { path: "/deals", name: "deals", component: () => import("@/modules/deals/pages/DealsPage.vue"), meta: { requiresAuth: true, titleKey: "nav.deals" } },
        { path: "/deals/:id", name: "deal-detail", component: () => import("@/modules/deals/pages/DealDetailPage.vue"), meta: { requiresAuth: true, titleKey: "nav.deals" } },

        { path: "/companies", name: "companies", component: () => import("@/modules/companies/CompaniesPage.vue"), meta: { requiresAuth: true } },
        { path: "/contacts", name: "contacts", component: () => import("@/modules/contacts/ContactsPage.vue"), meta: { requiresAuth: true } },
        { path: "/leads", name: "leads", component: () => import("@/modules/leads/LeadsPage.vue"), meta: { requiresAuth: true } },

        // --- 404 ---
        { path: "/:pathMatch(.*)*", name: "not-found", component: () => import("@/modules/dashboard/pages/NotFoundPage.vue"), meta: { requiresAuth: true } },
    ],
    scrollBehavior: () => ({ top: 0 }),
})

router.beforeEach(async (to) => {
    const auth = useAuthStore()
    if (!auth.initialized) {
        await auth.init()
    }
    if (to.meta.requiresAuth && !auth.isAuthenticated) {
        return { name: "login", query: { redirect: to.fullPath } }
    }
    if (to.meta.guestOnly && auth.isAuthenticated) {
        return { name: "dashboard" }
    }
})

export default router