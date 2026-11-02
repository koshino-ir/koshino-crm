import { api, type PaginationMeta } from "@/core/api/client"
import type { Activity, ActivityWritePayload } from "./types"

export const activityKeys = {
    all: ["activities"] as const,
    list: (params: Record<string, unknown>) => [...activityKeys.all, "list", params] as const,
}

interface ListParams {
    page?: number
    page_size?: number
    search?: string
    type?: string
}

export const activitiesApi = {
    async list(params: ListParams = {}): Promise<{ items: Activity[]; meta: PaginationMeta }> {
        const res = await api.get<Activity[]>("/activities/", { params })
        const meta = (res as unknown as { meta?: PaginationMeta }).meta ?? {
            count: res.data.length,
            page: 1,
            page_size: res.data.length,
            total_pages: 1,
        }
        return { items: res.data, meta }
    },
    async create(p: ActivityWritePayload): Promise<Activity> {
        const { data } = await api.post<Activity>("/activities/", p)
        return data
    },
    async delete(id: string): Promise<void> {
        await api.delete(`/activities/${id}/`)
    },
}