import { api, type PaginationMeta } from "@/core/api/client"
import type { Company, CompanyWritePayload } from "./types"

export const companyKeys = {
    all: ["companies"] as const,
    list: (params: Record<string, unknown>) => [...companyKeys.all, "list", params] as const,
}

interface ListParams {
    page?: number
    page_size?: number
    search?: string
}

export const companiesApi = {
    async list(params: ListParams = {}): Promise<{ items: Company[]; meta: PaginationMeta }> {
        const res = await api.get<Company[]>("/companies/", { params })
        const meta =
            (res as unknown as { meta?: PaginationMeta }).meta ?? {
                count: res.data.length,
                page: 1,
                page_size: res.data.length,
                total_pages: 1,
            }
        return { items: res.data, meta }
    },
    async create(payload: CompanyWritePayload): Promise<Company> {
        const { data } = await api.post<Company>("/companies/", payload)
        return data
    },
    async update(id: string, payload: Partial<CompanyWritePayload>): Promise<Company> {
        const { data } = await api.patch<Company>(`/companies/${id}/`, payload)
        return data
    },
    async delete(id: string): Promise<void> {
        await api.delete(`/companies/${id}/`)
    },
}