export type DealStatus = "open" | "won" | "lost"

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

export interface PipelineBrief {
    id: string
    name: string
}

export interface StageBrief {
    id: string
    name: string
    color: string
}

export interface UserBrief {
    id: string
    email: string
    first_name: string
    last_name: string
}

export interface Deal {
    id: string
    title: string
    amount: string
    currency: string
    expected_close_date: string | null
    probability: number
    status: DealStatus
    order: number
    company: CompanyBrief
    contact: ContactBrief | null
    pipeline: PipelineBrief
    stage: StageBrief
    owner: UserBrief | null
    created_at: string
    updated_at: string
}

export interface Stage {
    id: string
    name: string
    order: number
    color: string
    is_won: boolean
    is_lost: boolean
    deals: Deal[]
}

export interface KanbanBoard {
    pipeline: PipelineBrief
    stages: Stage[]
}

export interface Pipeline {
    id: string
    name: string
    is_default: boolean
    stages: StageBrief[]
}

export interface Company {
    id: string
    name: string
    industry?: string
}

export interface DealCreatePayload {
    title: string
    company_id: string
    pipeline_id: string
    stage_id?: string | null
    contact_id?: string | null
    amount?: string
    currency?: string
    expected_close_date?: string | null
    probability?: number
}

export interface DealMovePayload {
    stage_id: string
    order?: number
}