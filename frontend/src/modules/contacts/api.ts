import { api, type PaginationMeta } from "@/core/api/client"
import type { Contact, ContactWritePayload } from "./types"

export const contactKeys = {
    all: ["contacts"] as const,
    list: (params: Record<string, unknown>) => [...contactKeys.all, "list", params] as const,
}

interface ListParams {
    page?: number
    page_size?: number
    search?: string
    company?: string
}

export const contactsApi = {
    async list(params: ListParams = {}): Promise<{ items: Contact[]; meta: PaginationMeta }> {
        const res = await api.get<Contact[]>("/contacts/", { params })
        const meta = (res as unknown as { meta?: PaginationMeta }).meta ?? {
            count: res.data.length,
            page: 1,
            page_size: res.data.length,
            total_pages: 1,
        }
        return { items: res.data, meta }
    },
    async create(p: ContactWritePayload): Promise<Contact> {
        const { data } = await api.post<Contact>("/contacts/", p)
        return data
    },
    async update(id: string, p: Partial<ContactWritePayload>): Promise<Contact> {
        const { data } = await api.patch<Contact>(`/contacts/${id}/`, p)
        return data
    },
    async delete(id: string): Promise<void> {
        await api.delete(`/contacts/${id}/`)
    },
}