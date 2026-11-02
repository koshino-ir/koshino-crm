import { api, type PaginationMeta } from "@/core/api/client"
import type { Task, TaskWritePayload } from "./types"

export const taskKeys = {
    all: ["tasks"] as const,
    list: (params: Record<string, unknown>) => [...taskKeys.all, "list", params] as const,
}

interface ListParams {
    page?: number
    page_size?: number
    search?: string
    status?: string
    priority?: string
}

export const tasksApi = {
    async list(params: ListParams = {}): Promise<{ items: Task[]; meta: PaginationMeta }> {
        const res = await api.get<Task[]>("/tasks/", { params })
        const meta = (res as unknown as { meta?: PaginationMeta }).meta ?? {
            count: res.data.length,
            page: 1,
            page_size: res.data.length,
            total_pages: 1,
        }
        return { items: res.data, meta }
    },
    async create(p: TaskWritePayload): Promise<Task> {
        const { data } = await api.post<Task>("/tasks/", p)
        return data
    },
    async update(id: string, p: Partial<TaskWritePayload>): Promise<Task> {
        const { data } = await api.patch<Task>(`/tasks/${id}/`, p)
        return data
    },
    async delete(id: string): Promise<void> {
        await api.delete(`/tasks/${id}/`)
    },
    async complete(id: string): Promise<Task> {
        const { data } = await api.post<Task>(`/tasks/${id}/complete/`)
        return data
    },
    async reopen(id: string): Promise<Task> {
        const { data } = await api.post<Task>(`/tasks/${id}/reopen/`)
        return data
    },
}