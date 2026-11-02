export type InvoiceStatus = "draft" | "sent" | "paid" | "overdue" | "cancelled"

export interface Invoice {
    id: string
    number: string
    amount: string
    tax: string
    total: string
    status: InvoiceStatus
    issue_date: string
    due_date: string
    paid_at: string | null
    notes: string
    created_at: string
    updated_at: string
}

export interface InvoiceWritePayload {
    project_id: string
    number?: string
    amount: string
    tax?: string
    issue_date: string
    due_date: string
    notes?: string
}