
"use client"

import { useMemo, useState, useEffect } from "react"
import { createPortal } from "react-dom"
import { KanbanColumn } from "./KanbanColumn"
import { DndContext, DragOverlay, DragStartEvent, DragEndEvent, DragOverEvent, useSensor, useSensors, PointerSensor, TouchSensor } from "@dnd-kit/core"
import { arrayMove } from "@dnd-kit/sortable"
import type { KanbanColumnType, KanbanJob } from "@/types/kanban"
import { JobCard } from "./JobCard"

export function KanbanBoard() {
    const [jobs, setJobs] = useState<KanbanJob[]>([])
    const [activeJob, setActiveJob] = useState<KanbanJob | null>(null)

    // Persistence
    useEffect(() => {
        const saved = localStorage.getItem("kanban-jobs")
        if (saved) {
            try {
                setJobs(JSON.parse(saved))
            } catch (e) {
                console.error("Failed to load kanban jobs", e)
            }
        } else {
            // Sample data
            setJobs([
                { id: "1", title: "Estágio Python", company: "Google", status: "Interesse", dateAdded: new Date().toISOString() },
                { id: "2", title: "Dev React Jr", company: "Meta", status: "Aplicado", dateAdded: new Date().toISOString() },
            ])
        }
    }, [])

    useEffect(() => {
        localStorage.setItem("kanban-jobs", JSON.stringify(jobs))
    }, [jobs])

    const columns: { id: KanbanColumnType; title: string }[] = [
        { id: "Interesse", title: "👀 Interesse" },
        { id: "Aplicado", title: "🚀 Aplicado" },
        { id: "Entrevista", title: "🎤 Entrevista" },
        { id: "Proposta", title: "🎉 Proposta" },
        { id: "Rejeitado", title: "❌ Rejeitado" },
    ]

    const sensors = useSensors(
        useSensor(PointerSensor, {
            activationConstraint: {
                distance: 3, // 3px movement required before drag starts
            },
        }),
        useSensor(TouchSensor)
    )

    function onDragStart(event: DragStartEvent) {
        if (event.active.data.current?.type === "Job") {
            setActiveJob(event.active.data.current.job)
        }
    }

    function onDragEnd(event: DragEndEvent) {
        setActiveJob(null)
        const { active, over } = event
        if (!over) return

        const activeId = active.id
        const overId = over.id

        const activeJob = jobs.find((j) => j.id === activeId)
        const overJob = jobs.find((j) => j.id === overId)

        if (!activeJob) return

        // Dropping on a column (empty area)
        if (!overJob) {
            // Check if overId is a columnId
            const isColumn = columns.some(c => c.id === overId)
            if (isColumn && activeJob.status !== overId) {
                setJobs((prev) => {
                    const activeIndex = prev.findIndex((j) => j.id === activeId)
                    const newJobs = [...prev]
                    newJobs[activeIndex] = { ...prev[activeIndex], status: overId as KanbanColumnType }
                    return newJobs
                })
            }
            return
        }

        // Dropping on another job
        if (activeId !== overId) {
            // Logic handled in DragOver mainly for different columns
            // For reordering in same column:
            const activeIndex = jobs.findIndex((j) => j.id === activeId)
            const overIndex = jobs.findIndex((j) => j.id === overId)

            if (jobs[activeIndex].status === jobs[overIndex].status) {
                setJobs((jobs) => arrayMove(jobs, activeIndex, overIndex))
            }
        }
    }

    function onDragOver(event: DragOverEvent) {
        const { active, over } = event
        if (!over) return

        const activeId = active.id
        const overId = over.id

        if (activeId === overId) return

        const isActiveJob = active.data.current?.type === "Job"
        const isOverJob = over.data.current?.type === "Job"

        if (!isActiveJob) return

        // Dropping check
        if (isActiveJob && isOverJob) {
            setJobs((jobs) => {
                const activeIndex = jobs.findIndex((j) => j.id === activeId)
                const overIndex = jobs.findIndex((j) => j.id === overId)

                if (jobs[activeIndex].status !== jobs[overIndex].status) {
                    const newJobs = [...jobs]
                    newJobs[activeIndex].status = jobs[overIndex].status
                    return arrayMove(newJobs, activeIndex, overIndex - 1)
                }

                return arrayMove(jobs, activeIndex, overIndex)
            })
        }

        const isOverColumn = over.data.current?.type === "Column"

        if (isActiveJob && isOverColumn) {
            setJobs((jobs) => {
                const activeIndex = jobs.findIndex((j) => j.id === activeId)
                const newJobs = [...jobs]
                newJobs[activeIndex].status = over.id as KanbanColumnType
                return arrayMove(newJobs, activeIndex, activeIndex) // Trigger update
            })
        }
    }

    return (
        <div className="flex gap-4 overflow-x-auto pb-4 h-full min-h-[70vh]">
            <DndContext
                sensors={sensors}
                onDragStart={onDragStart}
                onDragEnd={onDragEnd}
                onDragOver={onDragOver}
            >
                <div className="flex gap-4 m-auto">
                    {columns.map((col) => (
                        <KanbanColumn
                            key={col.id}
                            column={col}
                            jobs={jobs.filter((row) => row.status === col.id)}
                        />
                    ))}
                </div>

                {typeof document !== 'undefined' && createPortal(
                    <DragOverlay>
                        {activeJob && <JobCard job={activeJob} />}
                    </DragOverlay>,
                    document.body
                )}
            </DndContext>
        </div>
    )
}
