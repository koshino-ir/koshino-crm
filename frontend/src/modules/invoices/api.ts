import { api, type PaginationMeta } from "@/core/api/client"
import type { Invoice, InvoiceWritePayload } from "./types"

export const invoiceKeys = {
    all: ["invoices"] as const,
    list: (params: Record<string, unknown>) => [...invoiceKeys.all, "list", params] as const,
}

interface ListParams {
    page?: number
    page_size?: number
    search?: string
    status?: string
}

export const invoicesApi = {
    async list(params: ListParams = {}): Promise<{ items: Invoice[]; meta: PaginationMeta }> {
        const res = await api.get<Invoice[]>("/invoices/", { params })
        const meta = (res as unknown as { meta?: PaginationMeta }).meta ?? {
            count: res.data.length,
            page: 1,
            page_size: res.data.length,
            total_pages: 1,
        }
        return { items: res.data, meta }
    },
    async create(p: InvoiceWritePayload): Promise<Invoice> {
        const { data } = await api.post<Invoice>("/invoices/", p)
        return data
    },
    async update(id: string, p: Partial<InvoiceWritePayload>): Promise<Invoice> {
        const { data } = await api.patch<Invoice>(`/invoices/${id}/`, p)
        return data
    },
    async delete(id: string): Promise<void> {
        await api.delete(`/invoices/${id}/`)
    },
    async markPaid(id: string): Promise<Invoice> {
        const { data } = await api.post<Invoice>(`/invoices/${id}/mark-paid/`)
        return data
    },
}