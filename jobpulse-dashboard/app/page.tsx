"use client"

import { useState, useEffect } from "react"
import { JobList } from "@/components/JobList"
import type { Job } from "@/types/job"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { ThemeToggle } from "@/components/theme-toggle"
import { PWAInstallButton } from "@/components/pwa-install-button"
import {
  Search, Filter, SortAsc, X, MapPin, Globe, Flame, Calendar, Building2,
  Github, Linkedin, Coffee, Copy, Check, TrendingUp, ExternalLink
} from "lucide-react"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001"

// Filtros de localização com ICONES
const LOCATION_FILTERS = [
  { id: "remoto", label: "Remoto", icon: Globe, pattern: "remot|home|remote" },
  { id: "sp", label: "São Paulo", icon: MapPin, pattern: "SP|São Paulo|Sao Paulo" },
  { id: "rj", label: "Rio de Janeiro", icon: MapPin, pattern: "RJ|Rio de Janeiro" },
  { id: "mg", label: "Minas Gerais", icon: MapPin, pattern: "MG|Minas Gerais|Belo Horizonte" },
  { id: "sul", label: "Sul", icon: MapPin, pattern: "PR|SC|RS|Curitiba|Florian|Porto Alegre|Paraná|Santa Catarina" },
  { id: "nordeste", label: "Nordeste", icon: MapPin, pattern: "BA|PE|CE|Recife|Salvador|Fortaleza|Bahia|Pernambuco|Ceará" },
  { id: "brasil", label: "Brasil", icon: MapPin, pattern: "Brasil|Brazil|BR" },
]

// BLACKLIST: Termos que, se presentes no título, escondem a vaga automaticamente (salvo se usuário buscar explicitamente)
const BLACKLIST_TERMS = [
  "pedreiro", "servente", "motorista", "limpeza", "vigilante", "porteiro", "recepcionista",
  "vendedor de loja", "atendente", "frentista", "operador de caixa", "segurança patrimonial",
  "advogado", "juridico", "direito", "financeiro", "contabil", "facilities", "serviços gerais"
]

// Filtros de CATEGORIA (Novos)
const CATEGORY_FILTERS = [
  { id: "estagio", label: "🎓 Estágio", pattern: "estagio|estágio|intern|trainée|trainee" },
  { id: "junior", label: "👶 Junior", pattern: "junior|jr|iniciante|assoc" },
  { id: "vendas", label: "💰 Vendas/SDR", pattern: "sdr|vendas|sales|comercial|closer|bdr|account exec" },
  { id: "dev", label: "💻 Dev", pattern: "dev|desenvolvedor|programador|front|back|full|software|engenheiro" },
  { id: "dados", label: "📊 Dados", pattern: "dados|data|analytics|bi|ciencia" },
  { id: "design", label: "🎨 Design/UX", pattern: "design|ux|ui|designer|visual|criativo" },
  { id: "produto", label: "🚀 Produto", pattern: "produto|product|po|pm|agile|scrum" },
  { id: "qa", label: "🧪 QA/Testes", pattern: "qa|teste|quality|test|tester" },
  { id: "mobile", label: "📱 Mobile", pattern: "mobile|ios|android|flutter|react native|kotlin|swift" },
  { id: "devops", label: "☁️ DevOps", pattern: "devops|cloud|aws|azure|docker|kubernetes|sre|infra" },
  { id: "suporte", label: "🛠️ Suporte", pattern: "suporte|help desk|infra|tech support" },
  { id: "seguranca", label: "🔐 Segurança", pattern: "cyber|security|segurança|pentest|hacker|defensive|offensive|red team|blue team" },
  { id: "analista", label: "📈 Analista", pattern: "analista|analyst" },
]

export default function Home() {
  const [searchTerm, setSearchTerm] = useState("")
  const [jobs, setJobs] = useState<Job[]>([])
  const [loading, setLoading] = useState(true)
  const [sortBy, setSortBy] = useState("score")
  const [stats, setStats] = useState({ total: 0, today: 0, avgScore: 0 })

  // Filtros
  const [showFilters, setShowFilters] = useState(false)
  const [selectedLocations, setSelectedLocations] = useState<string[]>([])
  const [selectedCategories, setSelectedCategories] = useState<string[]>([])
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([])

  // Clipboard state
  const [copied, setCopied] = useState(false)

  // Fetch jobs from API
  useEffect(() => {
    fetchJobs()
    fetchStats()
  }, [])

  // Helper to clean platform names (extract base platform)
  const cleanPlatformName = (plataforma: string): string => {
    // Match patterns like "JobSpy (Indeed) Remoto" → "Indeed"
    const match = plataforma.match(/JobSpy\s*\(([^)]+)\)/)
    if (match) return match[1].trim()
    // Remove any remaining parentheses
    return plataforma.replace(/[()]/g, '').trim()
  }

  // Deduplicate jobs by title + company (case insensitive)
  const deduplicateJobs = (jobList: Job[]): Job[] => {
    const seen = new Set<string>()
    return jobList.filter(job => {
      const key = `${job.titulo.toLowerCase().trim()}|${job.empresa.toLowerCase().trim()}`
      if (seen.has(key)) return false
      seen.add(key)
      return true
    })
  }

  const fetchJobs = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${API_URL}/api/v1/jobs?limit=500`)
      const data = await response.json()
      setJobs(data.jobs || [])
      // Calculate average score from jobs
      const jobList = data.jobs || []
      const avgScore = jobList.length > 0
        ? (jobList.reduce((acc: number, j: Job) => acc + (j.score || 0), 0) / jobList.length).toFixed(1)
        : 0
      setStats(prev => ({ ...prev, total: data.total || 0, today: 0, avgScore: parseFloat(String(avgScore)) }))
    } catch (error) {
      console.error("Erro ao buscar vagas:", error)
      setJobs([])
    } finally {
      setLoading(false)
    }
  }

  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_URL}/api/v1/stats`)
      const data = await response.json()
      setStats(prev => ({
        ...prev,
        total: data.total_jobs || 0,
        today: data.jobs_today || 0
      }))
    } catch (error) {
      console.error("Erro ao buscar stats:", error)
    }
  }

  // Get unique platforms (clean names)
  const platforms = Array.from(new Set(
    jobs.map(j => cleanPlatformName(j.plataforma))
  )).filter(p => p)

  // Filter and sort jobs
  const filteredAndSortedJobs = jobs
    .filter(job => {
      // 🚫 BLACKLIST: Remove vagas irrelevantes (pedreiro, motorista, etc)
      // Só mostra se o usuário DIGITAR explicitamente algo na busca que coincida (ex: quer ver se tem pedreiro)
      const isBlacklisted = BLACKLIST_TERMS.some(term => job.titulo.toLowerCase().includes(term))
      if (isBlacklisted && searchTerm === "") return false

      // Search filter
      const matchesSearch = searchTerm === "" ||
        job.titulo.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.empresa.toLowerCase().includes(searchTerm.toLowerCase())

      // Check if job is remote
      const isRemote = /remot|home|remote/i.test(job.localizacao) ||
        /🏠/i.test(job.titulo) ||
        /remoto/i.test(job.titulo)

      // Location filter - Show ALL jobs by default, filter only if location selected
      const matchesLocation = selectedLocations.length === 0 ||
        selectedLocations.some(locId => {
          if (locId === "remoto") return isRemote
          const location = LOCATION_FILTERS.find(l => l.id === locId)
          if (!location) return false
          const regex = new RegExp(location.pattern, 'i')
          return regex.test(job.localizacao)
        })

      // Category filter
      const matchesCategory = selectedCategories.length === 0 ||
        selectedCategories.some(catId => {
          const category = CATEGORY_FILTERS.find(c => c.id === catId)
          if (!category) return false
          const regex = new RegExp(category.pattern, 'i')
          return regex.test(job.titulo) || regex.test(job.descricao || "")
        })

      // Platform filter (use cleaned name)
      const jobPlatformClean = cleanPlatformName(job.plataforma)
      const matchesPlatform = selectedPlatforms.length === 0 ||
        selectedPlatforms.includes(jobPlatformClean)

      return matchesSearch && matchesLocation && matchesPlatform && matchesCategory
    })
    .sort((a, b) => {
      // Primary sort: prioritize Brazilian jobs (SP, RJ first)
      const priorityOrder = ['SP', 'São Paulo', 'RJ', 'Rio de Janeiro', 'MG', 'Belo Horizonte']
      const aIsPriority = priorityOrder.some(loc => a.localizacao?.includes(loc))
      const bIsPriority = priorityOrder.some(loc => b.localizacao?.includes(loc))

      if (aIsPriority && !bIsPriority) return -1
      if (!aIsPriority && bIsPriority) return 1

      // Secondary sort by user selection
      switch (sortBy) {
        case "score":
          return (b.score || 0) - (a.score || 0)
        case "date":
          return new Date(b.data_publicacao).getTime() - new Date(a.data_publicacao).getTime()
        case "company":
          return a.empresa.localeCompare(b.empresa)
        default:
          return 0
      }
    })

  const toggleLocation = (locationId: string) => {
    setSelectedLocations(prev =>
      prev.includes(locationId)
        ? prev.filter(l => l !== locationId)
        : [...prev, locationId]
    )
  }

  const toggleCategory = (catId: string) => {
    setSelectedCategories(prev =>
      prev.includes(catId)
        ? prev.filter(c => c !== catId)
        : [...prev, catId]
    )
  }

  const togglePlatform = (platform: string) => {
    setSelectedPlatforms(prev =>
      prev.includes(platform)
        ? prev.filter(p => p !== platform)
        : [...prev, platform]
    )
  }

  const clearFilters = () => {
    setSelectedLocations([])
    setSelectedCategories([])
    setSelectedPlatforms([])
    setSearchTerm("")
  }

  // Bookmarks persistence
  const [bookmarkedIds, setBookmarkedIds] = useState<number[]>([])

  useEffect(() => {
    const saved = localStorage.getItem('bookmarkedJobs')
    if (saved) {
      setBookmarkedIds(JSON.parse(saved))
    }
  }, [])

  const toggleBookmark = (id: number) => {
    setBookmarkedIds(prev => {
      const newBookmarks = prev.includes(id)
        ? prev.filter(b => b !== id)
        : [...prev, id]

      localStorage.setItem('bookmarkedJobs', JSON.stringify(newBookmarks))
      return newBookmarks
    })
  }

  const activeFiltersCount = selectedLocations.length + selectedPlatforms.length + selectedCategories.length

  const handleCopyPix = () => {
    navigator.clipboard.writeText("11941068987")
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
    alert("Chave Pix copiada para a área de transferência!")
  }

  return (
    <div className="min-h-screen bg-background relative overflow-hidden selection:bg-primary/20">
      {/* Background Gradients */}
      <div className="fixed inset-0 -z-10 h-full w-full bg-background bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.3),rgba(255,255,255,0))] dark:bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(60,50,150,0.3),rgba(0,0,0,0))]"></div>

      {/* Header Minimalista (Sticky) */}
      <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/80 backdrop-blur-xl supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3 group cursor-pointer" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
            <div className="relative">
              <img src="/boo_ghost_clean.png" alt="Boo" className="w-8 h-8 object-contain group-hover:rotate-12 transition-transform" />
            </div>
            <span className="font-bold text-xl tracking-tight">BooJ</span>
          </div>

          <div className="flex items-center gap-4">
            <div className="hidden md:flex items-center gap-4 text-sm text-muted-foreground border-r border-border/50 pr-4">
              <span className="flex items-center gap-1.5">
                <TrendingUp className="w-4 h-4 text-emerald-500" />
                <span className="font-medium text-foreground">{stats.today}</span>
                <span className="text-xs">novas</span>
              </span>
            </div>
            <PWAInstallButton />
            <ThemeToggle />
          </div>
        </div>
      </header>

      {/* HERO SECTION GIGANTE - BOO KING SIZE */}
      <section className="relative py-12 md:py-24 overflow-visible">
        <div className="container mx-auto px-4 flex flex-col items-center text-center relative z-10">

          {/* O GHOST */}
          <div className="mb-8 relative animate-float">
            <div className="absolute -inset-10 bg-violet-500/20 blur-[100px] rounded-full animate-pulse"></div>
            <img
              src="/boo_ghost_clean.png"
              alt="Boo Giant"
              className="w-64 h-64 md:w-80 md:h-80 object-contain drop-shadow-[0_20px_50px_rgba(124,58,237,0.3)] transition-transform hover:scale-105 duration-700"
            />
          </div>

          <h1 className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight mb-6 pb-4 pt-2 bg-clip-text text-transparent bg-gradient-to-b from-foreground to-foreground/60 drop-shadow-sm select-none leading-normal">
            Caçador de Vagas
          </h1>

          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-8 font-medium leading-relaxed">
            O Boo varre a internet 24/7 encontrando as melhores oportunidades de estágio para você não perder tempo.
          </p>

          <div className="flex gap-4">
            <Button size="lg" className="bg-violet-600 hover:bg-violet-700 text-white shadow-lg shadow-violet-500/20 font-bold px-8 h-12 rounded-full transform transition hover:scale-105" onClick={() => document.getElementById('jobs')?.scrollIntoView({ behavior: 'smooth' })}>
              <Flame className="w-5 h-5 mr-2" /> Ver Vagas
            </Button>
            <Button variant="outline" size="lg" className="rounded-full h-12 px-8 border-border/50 hover:bg-muted font-medium" asChild>
              <a href="https://paulomoraes.cloud" target="_blank">
                <span className="mr-2">🚀</span> Meu Portfolio
              </a>
            </Button>
          </div>
        </div>
      </section >

      {/* Info Cards Section */}
      < section className="container mx-auto px-4 pb-12" >
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Developer Card */}
          <Card className="bg-card/50 backdrop-blur border-border/50 hover:border-violet-500/30 transition-colors group">
            <CardHeader className="flex flex-row items-center gap-4 pb-2">
              <img src="https://github.com/Loonder.png" alt="Paulo" className="w-12 h-12 rounded-full border-2 border-violet-500/50 group-hover:border-violet-500 transition-colors" />
              <div>
                <CardTitle className="text-base">Paulo Moraes</CardTitle>
                <a href="https://paulomoraes.cloud" target="_blank" className="text-xs text-violet-500 hover:underline flex items-center gap-1">
                  paulomoraes.cloud <ExternalLink className="w-2.5 h-2.5" />
                </a>
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex gap-2">
                <Button variant="outline" size="sm" className="flex-1 h-8 text-xs" asChild>
                  <a href="https://linkedin.com/in/paulomoraesdev" target="_blank">
                    <Linkedin className="w-3.5 h-3.5 mr-2" /> LinkedIn
                  </a>
                </Button>
                <Button variant="outline" size="sm" className="flex-1 h-8 text-xs" asChild>
                  <a href="https://github.com/Loonder" target="_blank">
                    <Github className="w-3.5 h-3.5 mr-2" /> GitHub
                  </a>
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Statistics Card */}
          <Card className="bg-card/50 backdrop-blur border-border/50 hover:border-violet-500/30 transition-colors">
            <CardHeader className="pb-2">
              <CardTitle className="text-base flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-violet-500" /> Métricas
              </CardTitle>
            </CardHeader>
            <CardContent className="flex justify-between items-center px-6">
              <div className="text-center">
                <p className="text-2xl font-bold text-foreground">{stats.total}</p>
                <p className="text-[10px] uppercase tracking-wider text-muted-foreground">Total</p>
              </div>
              <div className="h-8 w-[1px] bg-border"></div>
              <div className="text-center">
                <p className="text-2xl font-bold text-emerald-500">+{stats.today}</p>
                <p className="text-[10px] uppercase tracking-wider text-muted-foreground">Novas</p>
              </div>
              <div className="h-8 w-[1px] bg-border"></div>
              <div className="text-center">
                <p className="text-2xl font-bold text-amber-500">{stats.avgScore || 0}</p>
                <p className="text-[10px] uppercase tracking-wider text-muted-foreground">Score</p>
              </div>
            </CardContent>
          </Card>

          {/* Pix / Support Card */}
          <Card className="bg-gradient-to-br from-emerald-500/5 to-teal-500/5 border-emerald-500/20 backdrop-blur relative overflow-hidden hover:border-emerald-500/40 transition-colors">
            <CardHeader className="pb-2">
              <CardTitle className="text-base flex items-center gap-2">
                <Coffee className="w-4 h-4 text-emerald-500" /> Apoie o Projeto
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs text-muted-foreground mb-3">
                Servidores custam caro. Ajude a manter o Boo vivo! 👻
              </p>
              <div className="flex items-center gap-2 bg-background/50 p-1.5 rounded border border-emerald-500/20">
                <div className="bg-emerald-500/10 p-1 rounded">
                  <div className="w-5 h-5 flex items-center justify-center text-emerald-500">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="w-4 h-4"
                    >
                      <path d="M16 8.2A11 11 0 0 0 8.2 16" />
                      <path d="M12 2A10 10 0 1 1 2 12" />
                      <path d="m14 14-4-4" />
                      <path d="m10 14 4-4" />
                    </svg>
                  </div>
                </div>
                <code className="text-xs font-mono flex-1 text-center font-bold text-foreground truncate">11941068987</code>
                <Button size="icon" variant="ghost" className="h-6 w-6 hover:text-emerald-500" onClick={handleCopyPix}>
                  {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </section >

      {/* Main Jobs Section */}
      < main className="container mx-auto px-4 pb-20 space-y-8" id="jobs" >

        {/* Search & Filters Bar */}
        < div className="sticky top-20 z-40 bg-background/90 backdrop-blur-md rounded-xl border border-border/50 shadow-sm p-2 md:p-4 transition-all duration-300" >
          <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
            <div className="w-full md:w-auto flex-1 relative group">
              <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground group-focus-within:text-violet-500 transition-colors" />
              <Input
                placeholder="Busque por cargo, empresa ou tecnologia..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-9 border-border/50 focus-visible:ring-violet-500/30 bg-background"
              />
              {searchTerm && (
                <Button variant="ghost" size="sm" onClick={() => setSearchTerm("")} className="absolute right-2 top-2 h-6 w-6 p-0 hover:bg-muted">
                  <X className="h-3 w-3" />
                </Button>
              )}
            </div>

            <div className="flex gap-2 w-full md:w-auto overflow-x-auto pb-1 md:pb-0">
              <Select value={sortBy} onValueChange={setSortBy}>
                <SelectTrigger className="w-[140px] bg-background border-border/50">
                  <SortAsc className="h-4 w-4 mr-2 text-muted-foreground" />
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="score"><span className="flex items-center gap-2"><Flame className="w-3 h-3 text-orange-500" /> Score</span></SelectItem>
                  <SelectItem value="date"><span className="flex items-center gap-2"><Calendar className="w-3 h-3 text-blue-500" /> Recentes</span></SelectItem>
                  <SelectItem value="company"><span className="flex items-center gap-2"><Building2 className="w-3 h-3 text-slate-500" /> Empresa</span></SelectItem>
                </SelectContent>
              </Select>

              <Button
                variant={showFilters ? "default" : "outline"}
                onClick={() => setShowFilters(!showFilters)}
                className={`gap-2 ${showFilters ? 'bg-violet-600 hover:bg-violet-700 text-white' : 'border-border/50 hover:bg-muted'}`}
              >
                <Filter className="h-4 w-4" />
                Filtros
                {activeFiltersCount > 0 && <Badge variant="secondary" className="ml-1 px-1 h-5 text-[10px]">{activeFiltersCount}</Badge>}
              </Button>
            </div>
          </div>

          {/* Filters Panel (Collapsible) */}
          {
            showFilters && (
              <div className="mt-4 pt-4 border-t border-border/50 animate-in fade-in slide-in-from-top-2 duration-200">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="font-semibold text-sm flex items-center gap-2 text-foreground">
                    <Filter className="h-4 w-4 text-violet-500" /> Filtros Ativos
                  </h3>
                  <Button variant="ghost" size="sm" onClick={clearFilters} className="h-7 text-xs text-muted-foreground hover:text-destructive">
                    Limpar tudo
                  </Button>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="text-xs font-semibold mb-2 text-muted-foreground uppercase tracking-wider">Localização</h4>
                    <div className="flex flex-wrap gap-2">
                      {LOCATION_FILTERS.map(loc => {
                        const Icon = loc.icon
                        return (
                          <div
                            key={loc.id}
                            className={`
                                 cursor-pointer rounded-full border px-3 py-1.5 flex items-center gap-2 transition-all duration-200 text-sm
                                 ${selectedLocations.includes(loc.id)
                                ? 'bg-violet-500/10 border-violet-500/50 text-violet-600 dark:text-violet-300 font-medium'
                                : 'hover:bg-muted border-border bg-background text-muted-foreground'}
                               `}
                            onClick={() => toggleLocation(loc.id)}
                          >
                            <Icon className="w-3.5 h-3.5" />
                            <span>{loc.label}</span>
                          </div>
                        )
                      })}
                    </div>
                  </div>

                  <div>
                    <h4 className="text-xs font-semibold mb-2 text-muted-foreground uppercase tracking-wider">Categoria</h4>
                    <div className="flex flex-wrap gap-2">
                      {CATEGORY_FILTERS.map(cat => (
                        <Badge
                          key={cat.id}
                          variant={selectedCategories.includes(cat.id) ? "default" : "outline"}
                          className={`
                                   cursor-pointer px-3 py-1.5 text-sm transition-all font-normal
                                   ${selectedCategories.includes(cat.id)
                              ? 'bg-violet-600 hover:bg-violet-700 text-white'
                              : 'hover:border-violet-400 text-muted-foreground bg-background'}
                                 `}
                          onClick={() => toggleCategory(cat.id)}
                        >
                          {cat.label}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  {platforms.length > 0 && (
                    <div>
                      <h4 className="text-xs font-semibold mb-2 text-muted-foreground uppercase tracking-wider">Plataformas</h4>
                      <div className="flex flex-wrap gap-2">
                        {platforms.map(platform => (
                          <Badge
                            key={platform}
                            variant={selectedPlatforms.includes(platform) ? "default" : "outline"}
                            className={`
                                     cursor-pointer px-3 py-1.5 text-sm transition-all font-normal
                                     ${selectedPlatforms.includes(platform) ? 'bg-violet-600 hover:bg-violet-700 text-white' : 'hover:border-violet-400 text-muted-foreground bg-background'}
                                   `}
                            onClick={() => togglePlatform(platform)}
                          >
                            {platform}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )
          }
        </div >

        {/* Content */}
        {
          loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <div key={i} className="h-64 rounded-xl border bg-card/50 animate-pulse" />
              ))}
            </div>
          ) : (
            <div className="animate-in fade-in duration-500">
              {deduplicateJobs(filteredAndSortedJobs).length === 0 ? (
                <div className="flex flex-col items-center justify-center py-20 text-center">
                  <div className="relative mb-6">
                    <img src="/boo_ghost_clean.png" alt="Boo triste" className="w-32 h-32 object-contain opacity-50 grayscale" />
                  </div>
                  <h3 className="text-xl font-semibold text-foreground mb-2">Ops, nada por aqui</h3>
                  <p className="text-muted-foreground text-sm max-w-md mb-4">
                    Nenhuma vaga encontrada com esses filtros. Tente limpar a busca!
                  </p>
                  <Button variant="outline" onClick={clearFilters} className="gap-2">
                    <X className="w-4 h-4" /> Limpar Filtros
                  </Button>
                </div>
              ) : (
                <JobList
                  jobs={deduplicateJobs(filteredAndSortedJobs)}
                  onBookmark={toggleBookmark}
                  bookmarkedIds={bookmarkedIds}
                />
              )}
            </div>
          )
        }
      </main >

      {/* Footer */}
      < footer className="border-t border-border/40 bg-background/50 backdrop-blur-lg mt-20" >
        <div className="container mx-auto px-4 py-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="relative">
                <img src="/boo.png" className="w-6 h-6 object-contain" alt="Boo" />
              </div>
              <span className="font-bold">BooJ</span>
            </div>

            <p className="text-xs text-muted-foreground">
              Feito com 💜 por <a href="https://paulomoraes.cloud" target="_blank" className="hover:text-violet-500 transition-colors">Paulo Moraes</a>
            </p>

            <div className="flex gap-4">
              <a href="https://paulomoraes.cloud" target="_blank" className="text-xs text-muted-foreground hover:text-foreground transition-colors flex items-center gap-1">
                <Globe className="w-3 h-3" /> Portfolio
              </a>
              <a href="https://github.com/Loonder" className="text-xs text-muted-foreground hover:text-foreground transition-colors flex items-center gap-1">
                <Github className="w-3 h-3" /> GitHub
              </a>
            </div>
          </div>
        </div>
      </footer >
    </div >
  )
}
