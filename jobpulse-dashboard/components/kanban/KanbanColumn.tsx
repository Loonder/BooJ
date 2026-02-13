
import { SortableContext, useSortable, verticalListSortingStrategy } from "@dnd-kit/sortable"
import { CSS } from "@dnd-kit/utilities"
import { useMemo } from "react"
import type { KanbanJob, KanbanColumnType } from "@/types/kanban"
import { JobCard } from "./JobCard"

interface Props {
    column: {
        id: KanbanColumnType
        title: string
    }
    jobs: KanbanJob[]
}

export function KanbanColumn({ column, jobs }: Props) {
    const jobsIds = useMemo(() => {
        return jobs.map((job) => job.id)
    }, [jobs])

    const { setNodeRef, isOver } = useSortable({
        id: column.id,
        data: {
            type: "Column",
            column,
        },
    })

    return (
        <div
            ref={setNodeRef}
            className={`
        bg-accent/30 w-[350px] max-w-full rounded-xl flex flex-col gap-4 p-4
        border-2 transition-colors
        ${isOver ? "border-violet-500 bg-violet-500/10" : "border-transparent"}
      `}
        >
            <div className="flex items-center justify-between">
                <h3 className="font-bold text-foreground flex items-center gap-2">
                    {column.title}
                </h3>
                <span className="bg-muted text-muted-foreground px-2 py-0.5 rounded text-xs font-medium">
                    {jobs.length}
                </span>
            </div>

            <div className="flex flex-grow flex-col gap-3 min-h-[500px]">
                <SortableContext items={jobsIds} strategy={verticalListSortingStrategy}>
                    {jobs.map((job) => (
                        <JobCard key={job.id} job={job} />
                    ))}
                </SortableContext>
                {jobs.length === 0 && (
                    <div className="h-full flex items-center justify-center text-muted-foreground/30 text-sm border-2 border-dashed border-muted-foreground/10 rounded-lg">
                        Solte aqui
                    </div>
                )}
            </div>
        </div>
    )
}
