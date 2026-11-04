import { createRouter, createWebHistory } from "vue-router"

import { useAuthStore } from "@/core/stores/auth"


const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: "/", name: "landing", component: () => import("@/modules/landing/LandingPage.vue"), meta: { public: true } },

        { path: "/dashboard", name: "dashboard", component: () => import("@/modules/dashboard/DashboardPage.vue"), meta: { requiresAuth: true } },

        // --- Auth ---
        { path: "/login", name: "login", component: () => import("@/modules/auth/pages/LoginPage.vue"), meta: { guestOnly: true, layout: "auth" } },
        { path: "/register", name: "register", component: () => import("@/modules/auth/pages/RegisterPage.vue"), meta: { guestOnly: true, layout: "auth" } },
        { path: "/auth/callback", name: "auth-callback", component: () => import("@/modules/auth/pages/AuthCallbackPage.vue"), meta: { layout: "auth" } },

        // --- App ---

        { path: "/deals", name: "deals", component: () => import("@/modules/deals/pages/DealsPage.vue"), meta: { requiresAuth: true, titleKey: "nav.deals" } },
        { path: "/deals/:id", name: "deal-detail", component: () => import("@/modules/deals/pages/DealDetailPage.vue"), meta: { requiresAuth: true, titleKey: "nav.deals" } },

        { path: "/companies", name: "companies", component: () => import("@/modules/companies/CompaniesPage.vue"), meta: { requiresAuth: true } },
        { path: "/contacts", name: "contacts", component: () => import("@/modules/contacts/ContactsPage.vue"), meta: { requiresAuth: true } },
        { path: "/leads", name: "leads", component: () => import("@/modules/leads/LeadsPage.vue"), meta: { requiresAuth: true } },

        { path: "/tasks", name: "tasks", component: () => import("@/modules/tasks/TasksPage.vue"), meta: { requiresAuth: true } },
        { path: "/activities", name: "activities", component: () => import("@/modules/activities/ActivitiesPage.vue"), meta: { requiresAuth: true } },
        { path: "/projects", name: "projects", component: () => import("@/modules/projects/ProjectsPage.vue"), meta: { requiresAuth: true } },
        { path: "/invoices", name: "invoices", component: () => import("@/modules/invoices/InvoicesPage.vue"), meta: { requiresAuth: true } },
        { path: "/settings", name: "settings", component: () => import("@/modules/settings/SettingsPage.vue"), meta: { requiresAuth: true } },

        // --- 404 ---
        { path: "/:pathMatch(.*)*", name: "not-found", component: () => import("@/modules/dashboard/pages/NotFoundPage.vue"), meta: { requiresAuth: true } },
    ],
    scrollBehavior: () => ({ top: 0 }),
})

router.beforeEach(async (to) => {
    const auth = useAuthStore()
    if (!auth.initialized) await auth.init()

    // Public pages — always accessible
    if (to.meta.public) return

    // Auth-required pages
    if (to.meta.requiresAuth && !auth.isAuthenticated) {
        return { name: "login", query: { redirect: to.fullPath } }
    }

    // Guest-only pages — redirect logged-in users
    if (to.meta.guestOnly && auth.isAuthenticated) {
        return { name: "dashboard" }
    }
})

export default router