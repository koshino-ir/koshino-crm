export type LeadStatus = "new" | "contacted" | "qualified" | "unqualified"
export type LeadSource = "web" | "referral" | "social" | "event" | "cold_call" | "other"

export interface CompanyBrief {
    id: string
    name: string
}

export interface ContactBrief {
    id: string
    first_name: string
    last_name: string
    email: string
}

export interface Lead {
    id: string
    title: string
    source: LeadSource
    status: LeadStatus
    notes: string
    company: CompanyBrief | null
    contact: ContactBrief | null
    created_at: string
    updated_at: string
}

export interface LeadWritePayload {
    title: string
    source?: LeadSource
    status?: LeadStatus
    notes?: string
    company_id?: string | null
    contact_id?: string | null
}