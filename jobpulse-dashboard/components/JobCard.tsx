import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ExternalLink, Bookmark, MapPin, Building2, CalendarDays, Code2, Terminal, Cpu, Database, Cloud, Share2 } from "lucide-react"
import type { Job } from "@/types/job"

interface JobCardProps {
    job: Job
    onBookmark?: (id: number) => void
    isBookmarked?: boolean
}

export function JobCard({ job, onBookmark, isBookmarked = false }: JobCardProps) {
    const isRemote = job.localizacao.toLowerCase().includes('remoto') ||
        job.localizacao.includes('🏠')

    // Clean platform name
    const cleanPlatform = job.plataforma
        .replace(/JobSpy\s*\(/i, '')
        .replace(/\)$/, '')
        .trim()

    // Format date
    const formatDate = (dateString: string) => {
        try {
            const date = new Date(dateString)
            return new Intl.DateTimeFormat('pt-BR', { day: '2-digit', month: 'short' }).format(date)
        } catch {
            return dateString
        }
    }

    // Determine Icon based on title
    const getJobIcon = (title: string) => {
        const t = title.toLowerCase()
        if (t.includes('python') || t.includes('django') || t.includes('flask')) return Terminal
        if (t.includes('react') || t.includes('frontend') || t.includes('js') || t.includes('node')) return Code2
        if (t.includes('data') || t.includes('dados') || t.includes('sql')) return Database
        if (t.includes('cloud') || t.includes('aws') || t.includes('azure')) return Cloud
        if (t.includes('machine') || t.includes('ia') || t.includes('ai')) return Cpu
        return Code2 // Default
    }

    const Icon = getJobIcon(job.titulo)
    const title = job.titulo.replace(/^[🔵🟢🟣🟡⚪]\s/, '') // Remove emojis if still present

    const handleShare = async () => {
        if (navigator.share) {
            try {
                await navigator.share({
                    title: `Vaga: ${title}`,
                    text: `Olha essa vaga de ${title} na ${job.empresa}! Encontrei no BooJ.`,
                    url: job.link
                })
            } catch (error) {
                console.log('Error sharing:', error)
            }
        } else {
            // Fallback: copy to clipboard
            navigator.clipboard.writeText(`${title} - ${job.link}`)
            alert("Link copiado para a área de transferência!")
        }
    }

    return (
        <Card className="group relative overflow-hidden border-border/50 bg-card/60 backdrop-blur-md transition-all duration-300 hover:shadow-xl hover:border-violet-500/30 hover:-translate-y-1 dark:bg-card/40">
            {/* Gradient Glow on Hover */}
            <div className="absolute inset-0 -z-10 bg-gradient-to-br from-violet-500/5 via-fuchsia-500/5 to-transparent opacity-0 transition-opacity duration-500 group-hover:opacity-100"></div>

            {/* Top Border Gradient */}
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-violet-500/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

            <CardHeader className="pb-3 pt-5">
                <div className="flex items-start justify-between gap-3">
                    <div className="space-y-1.5">
                        <h3 className="font-bold text-lg leading-tight text-foreground group-hover:text-violet-600 dark:group-hover:text-violet-400 transition-colors flex items-center gap-2">
                            <div className="p-1.5 rounded-md bg-violet-500/10 text-violet-500 group-hover:bg-violet-500 group-hover:text-white transition-colors">
                                <Icon className="w-5 h-5" />
                            </div>
                            <span className="line-clamp-2">{title}</span>
                        </h3>
                        <div className="flex items-center gap-2 text-sm text-muted-foreground/80 font-medium">
                            <Building2 className="h-3.5 w-3.5" />
                            {job.empresa}
                        </div>
                    </div>

                    {job.score && (
                        <div className={`
                            flex flex-col items-center justify-center w-12 h-12 rounded-xl border backdrop-blur-sm
                            ${job.score >= 80
                                ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-500'
                                : job.score >= 50
                                    ? 'bg-amber-500/10 border-amber-500/20 text-amber-500'
                                    : 'bg-muted/50 border-white/5 text-muted-foreground'}
                        `}>
                            <span className="text-xs font-bold">{job.score}</span>
                            <span className="text-[9px] uppercase opacity-70">Score</span>
                        </div>
                    )}
                </div>
            </CardHeader>

            <CardContent className="pb-3 space-y-4">
                <div className="flex flex-wrap gap-2">
                    <Badge variant="secondary" className={`
                        font-normal transition-colors
                        ${isRemote ? 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20' : 'bg-slate-500/10 text-slate-400'}
                    `}>
                        <MapPin className="h-3 w-3 mr-1" />
                        {isRemote ? 'Remoto' : job.localizacao}
                    </Badge>

                    <Badge variant="outline" className="font-mono text-xs opacity-70">
                        {cleanPlatform}
                    </Badge>

                    <Badge variant="outline" className="font-mono text-xs opacity-70 flex items-center gap-1">
                        <CalendarDays className="h-3 w-3" />
                        {formatDate(job.data_publicacao)}
                    </Badge>
                </div>
            </CardContent>

            <CardFooter className="flex gap-2 pt-3 border-t border-border/50 bg-muted/20 mt-auto">
                <Button
                    asChild
                    className="flex-1 bg-violet-600 hover:bg-violet-700 text-white border-0 shadow-lg shadow-violet-500/20"
                    size="sm"
                >
                    <a
                        href={job.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center justify-center gap-2"
                    >
                        Quero essa vaga
                        <ExternalLink className="h-3.5 w-3.5" />
                    </a>
                </Button>

                <Button
                    variant="outline"
                    size="sm"
                    onClick={handleShare}
                    className="border-border hover:bg-violet-50 hover:text-violet-500 hover:border-violet-500/50 transition-all dark:hover:bg-violet-950/30 text-muted-foreground"
                    title="Compartilhar"
                >
                    <Share2 className="h-4 w-4" />
                </Button>

                {onBookmark && (
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => onBookmark(job.id)}
                        className={`
                            border-border hover:bg-pink-50 hover:text-pink-500 hover:border-pink-500/50 transition-all dark:hover:bg-pink-950/30
                            ${isBookmarked ? 'text-pink-600 border-pink-500/50 bg-pink-50 dark:bg-pink-900/20 dark:text-pink-400' : 'text-muted-foreground'}
                        `}
                    >
                        <Bookmark className={`h-4 w-4 ${isBookmarked ? 'fill-current' : ''}`} />
                    </Button>
                )}
            </CardFooter>
        </Card>
    )
}
