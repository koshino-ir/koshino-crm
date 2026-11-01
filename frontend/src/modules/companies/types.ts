export interface UserBrief {
    id: string
    email: string
    first_name: string
    last_name: string
}

export interface Company {
    id: string
    name: string
    industry: string
    website: string
    phone: string
    email: string
    address: string
    city: string
    country: string
    notes: string
    owner: UserBrief | null
    contacts_count: number
    created_at: string
    updated_at: string
}

export interface CompanyWritePayload {
    name: string
    industry?: string
    website?: string
    phone?: string
    email?: string
    address?: string
    city?: string
    country?: string
    notes?: string
}