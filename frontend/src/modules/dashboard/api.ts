import { api } from "@/core/api/client"
import type { FunnelRow, KpiStats, RecentActivity, RevenueRow } from "./types"

export const dashboardKeys = {
    stats: ["dashboard", "stats"] as const,
    funnel: ["dashboard", "funnel"] as const,
    revenue: (months: number) => ["dashboard", "revenue", months] as const,
    recent: ["dashboard", "recent"] as const,
}

export const dashboardApi = {
    async stats(): Promise<KpiStats> {
        const { data } = await api.get<KpiStats>("/dashboard/stats/")
        return data
    },
    async funnel(): Promise<FunnelRow[]> {
        const { data } = await api.get<FunnelRow[]>("/dashboard/funnel/")
        return data
    },
    async revenue(months = 6): Promise<RevenueRow[]> {
        const { data } = await api.get<RevenueRow[]>("/dashboard/revenue/", {
            params: { months },
        })
        return data
    },
    async recentActivities(): Promise<RecentActivity[]> {
        const { data } = await api.get<RecentActivity[]>("/dashboard/recent-activities/")
        return data
    },
}