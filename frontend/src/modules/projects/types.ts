export type ProjectStatus = "planning" | "active" | "on_hold" | "completed" | "cancelled"

export interface Project {
    id: string
    name: string
    description: string
    status: ProjectStatus
    start_date: string | null
    end_date: string | null
    budget: string
    client_company: { id: string; name: string }
    owner: { id: string; email: string; first_name: string; last_name: string } | null
    invoices_count: number
    created_at: string
    updated_at: string
}

export interface ProjectWritePayload {
    name: string
    description?: string
    status?: ProjectStatus
    start_date?: string | null
    end_date?: string | null
    budget?: string
    client_company_id: string
}