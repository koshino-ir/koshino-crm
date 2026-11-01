export interface CompanyBrief {
    id: string
    name: string
}

export interface Contact {
    id: string
    first_name: string
    last_name: string
    full_name: string
    email: string
    phone: string
    position: string
    is_primary: boolean
    company: CompanyBrief | null
    created_at: string
    updated_at: string
}

export interface ContactWritePayload {
    first_name: string
    last_name?: string
    email?: string
    phone?: string
    position?: string
    is_primary?: boolean
    company_id?: string | null
}