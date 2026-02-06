"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Smartphone } from "lucide-react"

export function PWAInstallButton() {
    const [deferredPrompt, setDeferredPrompt] = useState<any>(null)
    const [isInstallable, setIsInstallable] = useState(false)

    useEffect(() => {
        const handler = (e: any) => {
            // Prevent the mini-infobar from appearing on mobile
            e.preventDefault()
            // Stash the event so it can be triggered later.
            setDeferredPrompt(e)
            setIsInstallable(true)
        }

        window.addEventListener("beforeinstallprompt", handler)

        // Check if app is already installed
        if (window.matchMedia('(display-mode: standalone)').matches) {
            setIsInstallable(false)
        }

        return () => window.removeEventListener("beforeinstallprompt", handler)
    }, [])

    const handleInstall = async () => {
        if (!deferredPrompt) return

        // Show the install prompt
        deferredPrompt.prompt()

        // Wait for the user to respond to the prompt
        const { outcome } = await deferredPrompt.userChoice

        if (outcome === 'accepted') {
            setDeferredPrompt(null)
            setIsInstallable(false)
        }
    }

    if (!isInstallable) return null

    return (
        <Button
            variant="outline"
            size="sm"
            className="gap-2 border-violet-500/50 text-violet-500 hover:bg-violet-500/10 animate-pulse font-semibold shadow-[0_0_10px_rgba(139,92,246,0.3)] hover:shadow-[0_0_15px_rgba(139,92,246,0.5)] transition-all"
            onClick={handleInstall}
        >
            <Smartphone className="w-4 h-4" />
            <span className="hidden sm:inline">Instalar App</span>
            <span className="sm:hidden">App</span>
        </Button>
    )
}
