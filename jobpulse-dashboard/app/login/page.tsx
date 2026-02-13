"use client"

import { signIn } from "next-auth/react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Github, ArrowLeft } from "lucide-react"
import Link from "next/link"

export default function LoginPage() {
    const handleLogin = (provider: string) => {
        // Callback URL ensures user goes back to home after login
        signIn(provider, { callbackUrl: "/" })
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-background relative overflow-hidden">
            {/* Background Gradients */}
            <div className="fixed inset-0 -z-10 h-full w-full bg-background bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.3),rgba(255,255,255,0))] dark:bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(60,50,150,0.3),rgba(0,0,0,0))]"></div>

            <div className="absolute top-8 left-8">
                <Button variant="ghost" asChild>
                    <Link href="/" className="flex items-center gap-2">
                        <ArrowLeft className="w-4 h-4" /> Voltar
                    </Link>
                </Button>
            </div>

            <Card className="w-full max-w-md border-border/50 bg-card/60 backdrop-blur-xl shadow-2xl">
                <CardHeader className="text-center flex flex-col items-center">
                    <div className="w-20 h-20 mb-4 relative animate-float">
                        <img src="/boo_ghost_clean.png" alt="Boo" className="w-full h-full object-contain" />
                    </div>
                    <CardTitle className="text-2xl font-bold">Bem-vindo de volta!</CardTitle>
                    <CardDescription>
                        Entre para salvar vagas, ver métricas e mais.
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <Button
                        variant="outline"
                        className="w-full h-12 text-base relative hover:bg-white/10 hover:border-white/20 transition-all border-border/50"
                        onClick={() => handleLogin('google')}
                    >
                        <div className="absolute left-4">
                            <svg viewBox="0 0 24 24" className="w-5 h-5" xmlns="http://www.w3.org/2000/svg">
                                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
                                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
                                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
                                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
                            </svg>
                        </div>
                        Entrar com Google
                    </Button>

                    <Button
                        variant="outline"
                        className="w-full h-12 text-base relative hover:bg-white/10 hover:border-white/20 transition-all border-border/50"
                        onClick={() => handleLogin('github')}
                    >
                        <div className="absolute left-4">
                            <Github className="w-5 h-5" />
                        </div>
                        Entrar com GitHub
                    </Button>

                    <div className="text-center text-xs text-muted-foreground mt-4">
                        Ao entrar, você concorda com nossos termos de serviço.
                        <br />
                        (Fique tranquilo, nós só queremos te ajudar a achar vaga)
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
