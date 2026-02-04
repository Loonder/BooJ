import { JobCard } from "./JobCard"
import { ScrollArea } from "@/components/ui/scroll-area"
import type { Job } from "@/types/job"

interface JobListProps {
    jobs: Job[]
    onBookmark?: (id: number) => void
    bookmarkedIds?: number[]
}

export function JobList({ jobs, onBookmark, bookmarkedIds = [] }: JobListProps) {
    if (jobs.length === 0) {
        return (
            <div className="text-center py-20 bg-muted/10 rounded-3xl border border-dashed border-muted-foreground/20">
                <div className="inline-flex h-16 w-16 items-center justify-center rounded-full bg-muted/20 mb-4 animate-bounce-soft">
                    <span className="text-2xl">👻</span>
                </div>
                <h3 className="text-xl font-bold mb-2">Ops, nada por aqui</h3>
                <p className="text-muted-foreground">
                    Nenhuma vaga encontrada com esses filtros. Tente limpar a busca!
                </p>
            </div>
        )
    }

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-in slide-in-from-bottom-4 duration-700 fade-in">
            {jobs.map((job) => (
                <JobCard
                    key={job.id}
                    job={job}
                    onBookmark={onBookmark}
                    isBookmarked={bookmarkedIds.includes(job.id)}
                />
            ))}
        </div>
    )
}
