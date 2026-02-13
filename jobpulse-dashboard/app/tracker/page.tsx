
import { KanbanBoard } from "@/components/kanban/KanbanBoard"
import { Metadata } from 'next'

export const metadata: Metadata = {
    title: 'Meus Processos | BooJ',
    description: 'Acompanhe suas candidaturas de estágio em TI.',
}

export default function TrackerPage() {
    return (
        <div className="container mx-auto py-8">
            <div className="mb-8 pl-4">
                <h1 className="text-3xl font-bold tracking-tight mb-2">Meus Processos</h1>
                <p className="text-muted-foreground">
                    Gerencie suas candidaturas. Arraste os cards para atualizar o status.
                    Os dados ficam salvos no seu navegador. 💾
                </p>
            </div>

            <KanbanBoard />
        </div>
    )
}
