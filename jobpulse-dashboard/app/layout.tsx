import type { Metadata, Viewport } from "next";

import { Geist, Geist_Mono } from "next/font/google";
import { ThemeProvider } from "@/components/theme-provider";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const viewport: Viewport = {
  themeColor: "#7c3aed",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
};

export const metadata: Metadata = {
  title: {
    default: "BooJ 👻 | Caçador de Vagas TI & Vendas",
    template: "%s | BooJ"
  },
  description: "Encontre seu Estágio em TI, vaga Junior ou oportunidade como SDR/Vendas sem esforço. O Boo varre a internet 24/7 para você não perder tempo. 🚀",
  manifest: "/manifest.json",
  icons: {
    icon: [
      { url: "/favicon.ico", sizes: "any" },
      { url: "/favicon-32x32.png", sizes: "32x32", type: "image/png" },
      { url: "/favicon-16x16.png", sizes: "16x16", type: "image/png" },
    ],
    apple: [
      { url: "/apple-touch-icon.png", sizes: "180x180", type: "image/png" },
    ],
    other: [
      { rel: "icon", url: "/favicon-32x32.png" },
    ]
  },
  openGraph: {
    type: "website",
    locale: "pt_BR",
    url: "https://boo.paulomoraes.cloud",
    title: "BooJ 👻 | O Caçador de Vagas",
    description: "Pare de procurar, deixe o fantasma trabalhar! Agregador de vagas para TI (Estágio/Jr) e Comercial (SDR/Vendas) com filtros inteligentes.",
    siteName: "BooJ",
    images: [
      {
        url: "/boo_ghost_clean.png",
        width: 512,
        height: 512,
        alt: "BooJ Mascot",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "BooJ 👻 | Caçador de Vagas",
    description: "Estágios TI, Vagas Junior e SDR. Tudo em um só lugar.",
    images: ["/boo_ghost_clean.png"],
    creator: "@paulomoraesdev",
  },
  authors: [{ name: "Paulo Moraes", url: "https://paulomoraes.cloud" }],
  appleWebApp: {
    capable: true,
    statusBarStyle: "default",
    title: "BooJ",
  },
};

import { Providers } from "@/components/providers"

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR" suppressHydrationWarning>
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased selection:bg-primary/20 bg-background text-foreground`}>
        <Providers>
          <ThemeProvider
            defaultTheme="system"
            storageKey="booj-theme"
          >
            {children}
          </ThemeProvider>
        </Providers>
      </body>
    </html>
  );
}
