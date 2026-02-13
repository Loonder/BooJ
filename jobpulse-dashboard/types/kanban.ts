
// Types for Kanban
export type KanbanColumnType = "Interesse" | "Aplicado" | "Entrevista" | "Proposta" | "Rejeitado"

export interface KanbanJob {
    id: string
    title: string
    company: string
    status: KanbanColumnType
    dateAdded: string
    link?: string
}
