export interface KpiStats {
    open_deals_count: number
    open_deals_value: string
    won_deals_count: number
    won_deals_value: string
    companies_count: number
    leads_count: number
    tasks_open_count: number
    tasks_overdue_count: number
}

export interface FunnelRow {
    stage_id: string
    name: string
    color: string
    count: number
    total: string
}

export interface RevenueRow {
    month: string | null
    total: string
    count: number
}

export interface RecentActivity {
    id: string
    type: "call" | "email" | "meeting" | "note"
    subject: string
    description: string
    occurred_at: string
    created_by: { id: string; email: string; first_name: string; last_name: string } | null
}