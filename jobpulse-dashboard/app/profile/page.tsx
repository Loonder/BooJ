"use client"

import { useState, useEffect } from "react"
import { useSession, signIn, signOut } from "next-auth/react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { ArrowLeft, Save, LogOut, User, Instagram, Image as ImageIcon, Loader2 } from "lucide-react"

export default function ProfilePage() {
    const { data: session, status } = useSession()
    const router = useRouter()
    const [loading, setLoading] = useState(false)

    // Form states
    const [name, setName] = useState("")
    const [instagram, setInstagram] = useState("")
    const [photoUrl, setPhotoUrl] = useState("")

    useEffect(() => {
        if (session?.user) {
            setName(session.user.name || "")
            setPhotoUrl(session.user.image || "")
            // Simulating fetching extra fields (instagram) from DB or local storage for now
            const storedInsta = localStorage.getItem("user_instagram")
            if (storedInsta) setInstagram(storedInsta)
        }
    }, [session])

    if (status === "loading") {
        return (
            <div className="flex h-screen items-center justify-center bg-background">
                <Loader2 className="h-10 w-10 animate-spin text-primary" />
            </div>
        )
    }

    if (status === "unauthenticated") {
        return (
            <div className="flex h-screen items-center justify-center bg-background p-4">
                <Card className="w-full max-w-md border-primary/20 bg-background/50 backdrop-blur-md">
                    <CardHeader className="text-center">
                        <CardTitle className="text-3xl font-bold text-foreground">Acesso Restrito 🔒</CardTitle>
                        <CardDescription>Faça login para editar seu perfil e ganhar XP.</CardDescription>
                    </CardHeader>
                    <CardContent className="flex flex-col gap-4">
                        <Button size="lg" className="w-full gap-2" onClick={() => signIn("google")}>
                            <svg className="h-5 w-5" viewBox="0 0 24 24">
                                <path
                                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                                    fill="#4285F4"
                                />
                                <path
                                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                                    fill="#34A853"
                                />
                                <path
                                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                                    fill="#FBBC05"
                                />
                                <path
                                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                                    fill="#EA4335"
                                />
                            </svg>
                            Entrar com Google
                        </Button>

                        <Button variant="outline" size="lg" className="w-full gap-2" onClick={() => signIn("github")}>
                            <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                            </svg>
                            Entrar com GitHub
                        </Button>

                        <Button variant="ghost" className="mt-4" onClick={() => router.push("/")}>
                            <ArrowLeft className="mr-2 h-4 w-4" /> Voltar para Vagas
                        </Button>
                    </CardContent>
                </Card>
            </div>
        )
    }

    const handleSave = async () => {
        setLoading(true)
        // Here we would sync with the Database. For now using localStorage as a mock persistence layer for extra fields
        localStorage.setItem("user_instagram", instagram)

        // Simulate API call
        setTimeout(() => {
            setLoading(false)
            // Here usually user update session logic happens
            alert("Perfil atualizado com sucesso! (Simulado)")
        }, 1000)
    }

    return (
        <div className="min-h-screen bg-background p-4 md:p-8 flex items-center justify-center">
            <Card className="w-full max-w-2xl border-primary/20 shadow-2xl bg-background/60 backdrop-blur-xl">
                <CardHeader className="relative overflow-hidden rounded-t-lg bg-gradient-to-r from-purple-500/20 to-blue-500/20 pb-8 pt-8">
                    <div className="absolute top-4 left-4">
                        <Button variant="ghost" size="sm" onClick={() => router.push("/")}>
                            <ArrowLeft className="mr-2 h-4 w-4" /> Voltar
                        </Button>
                    </div>
                    <div className="flex flex-col items-center justify-center gap-4">
                        <Avatar className="h-24 w-24 border-4 border-background shadow-lg cursor-pointer hover:opacity-80 transition">
                            <AvatarImage src={photoUrl || session?.user?.image || ""} alt={name} />
                            <AvatarFallback className="text-2xl font-bold bg-primary/20 text-primary">
                                {name?.charAt(0) || "U"}
                            </AvatarFallback>
                        </Avatar>
                        <div className="text-center">
                            <CardTitle className="text-2xl font-bold">{name || "Usuário"}</CardTitle>
                            <CardDescription className="text-primary font-medium">Nível 1 • Novato</CardDescription>
                        </div>
                    </div>
                </CardHeader>

                <CardContent className="space-y-6 pt-8">
                    <div className="grid gap-6 md:grid-cols-2">
                        <div className="space-y-2">
                            <Label htmlFor="name" className="flex items-center gap-2">
                                <User className="h-4 w-4 text-muted-foreground" /> Nome de Exibição
                            </Label>
                            <Input
                                id="name"
                                placeholder="Seu nome"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                            />
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="instagram" className="flex items-center gap-2">
                                <Instagram className="h-4 w-4 text-muted-foreground" /> Instagram
                            </Label>
                            <Input
                                id="instagram"
                                placeholder="@seu.insta"
                                value={instagram}
                                onChange={(e) => setInstagram(e.target.value)}
                            />
                        </div>

                        <div className="space-y-2 md:col-span-2">
                            <Label htmlFor="photo" className="flex items-center gap-2">
                                <ImageIcon className="h-4 w-4 text-muted-foreground" /> Link da Foto (URL)
                            </Label>
                            <Input
                                id="photo"
                                placeholder="https://exemplo.com/sua-foto.jpg"
                                value={photoUrl}
                                onChange={(e) => setPhotoUrl(e.target.value)}
                            />
                            <p className="text-xs text-muted-foreground">Cole o link de uma imagem pública (ex: GitHub, LinkedIn)</p>
                        </div>
                    </div>
                </CardContent>

                <CardFooter className="flex justify-between border-t p-6 bg-muted/20">
                    <Button variant="ghost" onClick={() => signOut()}>
                        <LogOut className="mr-2 h-4 w-4" /> Sair
                    </Button>
                    <Button onClick={handleSave} disabled={loading} className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700">
                        {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Save className="mr-2 h-4 w-4" />}
                        Salvar Alterações
                    </Button>
                </CardFooter>
            </Card>
        </div>
    )
}
