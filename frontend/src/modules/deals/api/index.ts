import { api } from "@/core/api/client"
import type {
    Company,
    Deal,
    DealCreatePayload,
    DealMovePayload,
    KanbanBoard,
    Pipeline,
} from "../types"

export const dealsApi = {
    async kanban(pipelineId: string): Promise<KanbanBoard> {
        const { data } = await api.get<KanbanBoard>("/deals/kanban/", {
            params: { pipeline: pipelineId },
        })
        return data
    },

    async retrieve(id: string): Promise<Deal> {
        const { data } = await api.get<Deal>(`/deals/${id}/`)
        return data
    },

    async create(payload: DealCreatePayload): Promise<Deal> {
        const { data } = await api.post<Deal>("/deals/", payload)
        return data
    },

    async move(id: string, payload: DealMovePayload): Promise<Deal> {
        const { data } = await api.patch<Deal>(`/deals/${id}/move/`, payload)
        return data
    },
}

export const pipelinesApi = {
    async list(): Promise<Pipeline[]> {
        const { data } = await api.get<Pipeline[]>("/pipelines/")
        return data
    },

    async ensureDefault(): Promise<Pipeline> {
        const { data } = await api.post<Pipeline>("/pipelines/ensure-default/")
        return data
    },
}

export const companiesApi = {
    async list(): Promise<Company[]> {
        const { data } = await api.get<Company[]>("/companies/", {
            params: { page_size: 100 },
        })
        return data
    },

    async create(payload: { name: string; industry?: string }): Promise<Company> {
        const { data } = await api.post<Company>("/companies/", payload)
        return data
    },
}