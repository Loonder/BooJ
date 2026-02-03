# -*- coding: utf-8 -*-
"""
Configurações globais do JobPulse.
"""

# Termos de busca para vagas de estágio em TI
SEARCH_TERMS = [
    # Dev
    "estágio ti",
    "estágio desenvolvimento",
    "estágio programador",
    "estágio software engineer",
    "estágio front-end",
    "estágio back-end",
    "estágio fullstack",
    "estágio mobile",
    
    # Dados & IA
    "estágio dados",
    "estágio data science",
    "estágio machine learning",
    "estágio inteligência artificial",
    "estágio bi",
    "estágio analytics",

    # Infra/Cloud/Segurança
    "estágio suporte",
    "estágio infraestrutura",
    "estágio cloud",
    "estágio devops",
    "estágio cyber security",
    "estágio segurança da informação",
    "estágio pentest",
    "estágio redes",

    # Qualidade
    "estágio qa",
    "estágio testes",

    # Produto & Design
    "estágio produto",
    "estágio product owner",
    "estágio ux ui",
    "estágio design",
]

import os
from dotenv import load_dotenv

load_dotenv()

# Localização padrão para busca
DEFAULT_LOCATION = "São Paulo, SP"

# Credenciais LinkedIn (Do .env)
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

# Headers para requisições HTTP (simular navegador)
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

# Configurações de scraping responsável
REQUEST_DELAY_SECONDS = 2  # Delay entre requisições
MAX_PAGES_PER_SEARCH = 3   # Máximo de páginas por termo de busca
REQUEST_TIMEOUT = 10       # Timeout em segundos

# Filtros de tempo
HOURS_FILTER = 720  # Últimos 30 dias (garantir volume)

# Diretório para exportação de dados
DATA_DIR = "data"

# Nome do arquivo CSV de saída
# Nome do arquivo CSV de saída
OUTPUT_FILENAME = "vagas_estagio_ti.csv"
CSV_PATH = os.path.join(DATA_DIR, OUTPUT_FILENAME)

# SQLite Database Path (Memory-efficient storage)
DB_PATH = os.path.join(DATA_DIR, "jobs.db")



# URL base do Indeed Brasil
INDEED_BASE_URL = "https://br.indeed.com"

# --- NOVAS FONTES (Fase 4 e 2) ---

# RemoteOK API
REMOTEOK_API_URL = "https://remoteok.com/api"

# RSS Feeds que funcionam (internacionais)
RSS_FEEDS = {
    # WeWorkRemotely - Funciona bem
    "WeWorkRemotely_Dev": "https://weworkremotely.com/categories/remote-programming-jobs.rss",
    "WeWorkRemotely_All": "https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss",
    
    # Remotive - Tech remoto
    "Remotive_Dev": "https://remotive.com/remote-jobs/feed/software-dev",
}

# --- HUNTER BOT CONFIG ---

# Discord Webhook (Notificações) - From environment variable
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

# Keywords de "Vaga Perfeita" (Prioridade Alta)
GOLD_KEYWORDS = [
    'python',
    'cybersecurity',
    'segurança',
    'pentest',
    'redes',
    'linux'
]

# Intervalo de loop (minutos)
HUNTER_SLEEP_MIN = 5
HUNTER_SLEEP_MAX = 10

# Persistência
SENT_JOBS_FILE = "data/sent_jobs.txt"
LOG_FILE = "logs/hunter.log"

# Configurações Telegram (Phase 9/22)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Diretórios
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Reddit Subreddits Expandidos
REDDIT_SUBREDDITS_EXPANDED = ['vagasTI', 'empregosBrasil', 'devbr', 'brdev', 'forhire', 'jobbit', 'remotejs', 'remotepython', 'techjobs', 'cscareerquestions']

# Telegram Channels Expandidos
TELEGRAM_CHANNELS_EXPANDED = ['@VagasBrasil_TI', '@vagastecnologia', '@vagasti', '@vagasdev', '@vagas_ti_br', '@oportunidadesti', '@empregosBR', '@startupjobsbr', '@devjobs_br', '@pythonvagas']
