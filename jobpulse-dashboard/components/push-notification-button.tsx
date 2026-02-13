
"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Bell, BellOff, Loader2 } from "lucide-react"
import { useToast } from "./ui/use-toast"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001"
const VAPID_PUBLIC_KEY = process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY

function urlBase64ToUint8Array(base64String: string) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}

export function PushNotificationButton() {
    const [isSubscribed, setIsSubscribed] = useState(false)
    const [loading, setLoading] = useState(false)
    const [supported, setSupported] = useState(false)

    // Simple toast fallback if not available
    const toast = typeof window !== 'undefined' ? (window as any).toast || console.log : console.log

    useEffect(() => {
        if ('serviceWorker' in navigator && 'PushManager' in window) {
            setSupported(true)
            registerServiceWorker()
        }
    }, [])

    const registerServiceWorker = async () => {
        try {
            const registration = await navigator.serviceWorker.register('/sw.js')
            const subscription = await registration.pushManager.getSubscription()
            setIsSubscribed(!!subscription)
        } catch (error) {
            console.error("Service Worker registration failed:", error)
        }
    }

    const subscribeParams = async (registration: ServiceWorkerRegistration) => {
        if (!VAPID_PUBLIC_KEY) {
            console.error("VAPID Public Key key not found")
            return
        }

        try {
            const subscription = await registration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY)
            })
            return subscription
        } catch (err) {
            console.error("Failed to subscribe the user: ", err);
            return null
        }
    }

    const handleSubscribe = async () => {
        setLoading(true)
        try {
            const registration = await navigator.serviceWorker.ready
            const subscription = await subscribeParams(registration)

            if (subscription) {
                // Send to backend
                await fetch(`${API_URL}/api/v1/subscribe`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(subscription),
                })

                setIsSubscribed(true)
                alert("Notificações ativadas com sucesso! 🔔")
            }
        } catch (error) {
            console.error("Subscription failed:", error)
            alert("Erro ao ativar notificações. Verifique se você permitiu no navegador.")
        } finally {
            setLoading(false)
        }
    }

    const handleUnsubscribe = async () => {
        // For now we just unsubscribe locally, backend handles 410 Gone automatically
        setLoading(true)
        try {
            const registration = await navigator.serviceWorker.ready
            const subscription = await registration.pushManager.getSubscription()
            if (subscription) {
                await subscription.unsubscribe()
                setIsSubscribed(false)
                alert("Notificações desativadas.")
            }
        } catch (error) {
            console.error("Error unsubscribing", error)
        } finally {
            setLoading(false)
        }
    }

    if (!supported) return null

    return (
        <Button
            variant={isSubscribed ? "outline" : "default"}
            size="sm"
            onClick={isSubscribed ? handleUnsubscribe : handleSubscribe}
            disabled={loading}
            className={isSubscribed ? "border-violet-500/50 text-violet-500" : "bg-violet-600 hover:bg-violet-700 text-white"}
        >
            {loading ? (
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
            ) : isSubscribed ? (
                <BellOff className="h-4 w-4 mr-2" />
            ) : (
                <Bell className="h-4 w-4 mr-2" />
            )}
            {isSubscribed ? "Desativar Alertas" : "Ativar Alertas"}
        </Button>
    )
}
