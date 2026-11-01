export const dealKeys = {
    all: ["deals"] as const,
    detail: (id: string) => [...dealKeys.all, "detail", id] as const,
    kanban: (pipelineId: string) => [...dealKeys.all, "kanban", pipelineId] as const,
}

export const pipelineKeys = {
    all: ["pipelines"] as const,
}

export const companyKeys = {
    all: ["companies"] as const,
}