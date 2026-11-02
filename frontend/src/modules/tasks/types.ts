export type TaskPriority = "low" | "medium" | "high" | "urgent"
export type TaskStatus = "todo" | "in_progress" | "done"

export interface Task {
    id: string
    title: string
    description: string
    due_date: string | null
    priority: TaskPriority
    status: TaskStatus
    completed_at: string | null
    assigned_to: { id: string; email: string; first_name: string; last_name: string } | null
    created_at: string
    updated_at: string
}

export interface TaskWritePayload {
    title: string
    description?: string
    due_date?: string | null
    priority?: TaskPriority
    status?: TaskStatus
}