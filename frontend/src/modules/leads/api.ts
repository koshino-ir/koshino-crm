import { api, type PaginationMeta } from "@/core/api/client"
import type { Lead, LeadWritePayload } from "./types"

export const leadKeys = {
    all: ["leads"] as const,
    list: (params: Record<string, unknown>) => [...leadKeys.all, "list", params] as const,
}

interface ListParams {
    page?: number
    page_size?: number
    search?: string
    status?: string
}

export const leadsApi = {
    async list(params: ListParams = {}): Promise<{ items: Lead[]; meta: PaginationMeta }> {
        const res = await api.get<Lead[]>("/leads/", { params })
        const meta = (res as unknown as { meta?: PaginationMeta }).meta ?? {
            count: res.data.length,
            page: 1,
            page_size: res.data.length,
            total_pages: 1,
        }
        return { items: res.data, meta }
    },
    async create(p: LeadWritePayload): Promise<Lead> {
        const { data } = await api.post<Lead>("/leads/", p)
        return data
    },
    async update(id: string, p: Partial<LeadWritePayload>): Promise<Lead> {
        const { data } = await api.patch<Lead>(`/leads/${id}/`, p)
        return data
    },
    async delete(id: string): Promise<void> {
        await api.delete(`/leads/${id}/`)
    },
    async convert(id: string, pipelineId: string, stageId?: string | null): Promise<unknown> {
        const { data } = await api.post(`/leads/${id}/convert/`, {
            pipeline_id: pipelineId,
            stage_id: stageId ?? null,
        })
        return data
    },
}