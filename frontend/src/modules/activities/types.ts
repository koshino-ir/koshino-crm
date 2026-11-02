export type ActivityType = "call" | "email" | "meeting" | "note"

export interface Activity {
    id: string
    type: ActivityType
    subject: string
    description: string
    occurred_at: string
    created_by: { id: string; email: string; first_name: string; last_name: string } | null
    created_at: string
    updated_at: string
}

export interface ActivityWritePayload {
    type: ActivityType
    subject: string
    description?: string
    occurred_at: string
    deal_id?: string | null
    lead_id?: string | null
    contact_id?: string | null
    company_id?: string | null
}