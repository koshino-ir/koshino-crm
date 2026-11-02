import { api, type PaginationMeta } from "@/core/api/client"
import type { Project, ProjectWritePayload } from "./types"

export const projectKeys = {
    all: ["projects"] as const,
    list: (params: Record<string, unknown>) => [...projectKeys.all, "list", params] as const,
}

interface ListParams {
    page?: number
    page_size?: number
    search?: string
    status?: string
}

export const projectsApi = {
    async list(params: ListParams = {}): Promise<{ items: Project[]; meta: PaginationMeta }> {
        const res = await api.get<Project[]>("/projects/", { params })
        const meta = (res as unknown as { meta?: PaginationMeta }).meta ?? {
            count: res.data.length,
            page: 1,
            page_size: res.data.length,
            total_pages: 1,
        }
        return { items: res.data, meta }
    },
    async create(p: ProjectWritePayload): Promise<Project> {
        const { data } = await api.post<Project>("/projects/", p)
        return data
    },
    async update(id: string, p: Partial<ProjectWritePayload>): Promise<Project> {
        const { data } = await api.patch<Project>(`/projects/${id}/`, p)
        return data
    },
    async delete(id: string): Promise<void> {
        await api.delete(`/projects/${id}/`)
    },
}