
import { useSortable } from "@dnd-kit/sortable"
import { CSS } from "@dnd-kit/utilities"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Calendar, ExternalLink, GripVertical } from "lucide-react"
import { KanbanJob } from "@/types/kanban"

interface JobCardProps {
    job: KanbanJob
}

export function JobCard({ job }: JobCardProps) {
    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging,
    } = useSortable({
        id: job.id,
        data: {
            type: "Job",
            job,
        },
    })

    const style = {
        transform: CSS.Transform.toString(transform),
        transition,
    }

    if (isDragging) {
        return (
            <div
                ref={setNodeRef}
                style={style}
                className="opacity-30 bg-violet-500/10 border-2 border-violet-500 rounded-lg h-[100px]"
            />
        )
    }

    return (
        <div ref={setNodeRef} style={style} {...attributes} {...listeners} className="touch-none">
            <Card className="hover:border-violet-500/50 transition-colors cursor-grab active:cursor-grabbing bg-card/80 backdrop-blur-sm">
                <CardHeader className="p-3 pb-0 space-y-0">
                    <div className="flex justify-between items-start">
                        <CardTitle className="text-sm font-medium leading-tight line-clamp-2">
                            {job.title}
                        </CardTitle>
                        <GripVertical className="h-4 w-4 text-muted-foreground/50 flex-shrink-0 ml-2" />
                    </div>
                </CardHeader>
                <CardContent className="p-3">
                    <div className="text-xs text-muted-foreground font-medium mb-2 truncate">
                        {job.company}
                    </div>
                    <div className="flex items-center justify-between text-[10px] text-muted-foreground">
                        <span className="flex items-center gap-1">
                            <Calendar className="h-3 w-3" />
                            {new Date(job.dateAdded).toLocaleDateString('pt-BR')}
                        </span>
                        {job.link && (
                            <a
                                href={job.link}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="hover:text-violet-500 transition-colors"
                                onClick={(e) => e.stopPropagation()}
                                onPointerDown={(e) => e.stopPropagation()}
                            >
                                <ExternalLink className="h-3 w-3" />
                            </a>
                        )}
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
