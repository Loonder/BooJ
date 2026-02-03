# -*- coding: utf-8 -*-
"""
Hunter Bot - O Caçador de Vagas 24/7.
Executa ciclo contínuo de busca e notifica no Discord e Telegram.
"""

import sys
import os
import time
import random
import logging
from datetime import datetime

# Setup paths
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import SEARCH_TERMS, HUNTER_SLEEP_MIN, HUNTER_SLEEP_MAX, LOG_FILE

# Working scrapers (API/RSS based - NO BROWSER NEEDED!)
from scraper_rss import RssScraper
from scraper_github import GithubScraper
from scraper_adzuna import AdzunaScraper
from scraper_remoteok import RemoteOKScraper
from scraper_reddit import RedditScraper
from scraper_hackernews import HackerNewsScraper
from scraper_telegram import TelegramScraper
from scraper_br import BRScraper
from scraper_tabnews import TabNewsScraper
from scraper_apinfo import ApinfoScraper

from notifier import send_discord_alert
from notifier_telegram import TelegramNotifier
from filters import apply_all_filters
from database import JobDatabase
from intelligence import Intelligence

# Garantir diretório de logs
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("HunterBot")

# Inicializar Inteligência e Notificadores
brain = Intelligence()
telegram = TelegramNotifier()


def run_cycle():
    """Executa um ciclo de busca em TODAS as fontes gratuitas."""
    logger.info("--- Iniciando Ciclo de Caça (8 fontes) ---")
    
    raw_jobs = []
    
    # 1. GitHub (API)
    try:
        logger.info("🐙 Caçando no GitHub...")
        gh = GithubScraper()
        raw_jobs.extend(gh.fetch_jobs())
    except Exception as e: logger.error(f"Erro GitHub: {e}")

    # 2. RSS Feeds
    try:
        logger.info("📡 Caçando RSS...")
        rss = RssScraper()
        raw_jobs.extend(rss.fetch_all(SEARCH_TERMS))
    except Exception as e: logger.error(f"Erro RSS: {e}")

    # 3. Adzuna API (Principal - Brasil)
    try:
        logger.info("🌐 Caçando no Adzuna Brasil...")
        adzuna = AdzunaScraper()
        raw_jobs.extend(adzuna.fetch_jobs(SEARCH_TERMS))
    except Exception as e: logger.error(f"Erro Adzuna: {e}")

    # 4. RemoteOK (Remotas internacionais)
    try:
        logger.info("🌍 Caçando no RemoteOK...")
        remoteok = RemoteOKScraper()
        raw_jobs.extend(remoteok.fetch_jobs(SEARCH_TERMS))
    except Exception as e: logger.error(f"Erro RemoteOK: {e}")

    # 5. Reddit (Subreddits de vagas)
    try:
        logger.info("📱 Caçando no Reddit...")
        reddit = RedditScraper()
        raw_jobs.extend(reddit.fetch_jobs(SEARCH_TERMS))
    except Exception as e: logger.error(f"Erro Reddit: {e}")

    # 6. Hacker News (Jobs)
    try:
        logger.info("🔶 Caçando no Hacker News...")
        hn = HackerNewsScraper()
        raw_jobs.extend(hn.fetch_jobs(SEARCH_TERMS))
    except Exception as e: logger.error(f"Erro HN: {e}")

    # 7. Telegram (Canais BR de vagas)
    try:
        logger.info("💬 Caçando no Telegram...")
        tg_scraper = TelegramScraper()
        raw_jobs.extend(tg_scraper.fetch_jobs(SEARCH_TERMS))
    except Exception as e: logger.error(f"Erro Telegram: {e}")

    # 8. Sites BR (Programathor)
    try:
        logger.info("🇧🇷 Caçando no Programathor...")
        br_scraper = BRScraper()
        raw_jobs.extend(br_scraper.fetch_jobs(SEARCH_TERMS))
    except Exception as e: logger.error(f"Erro Sites BR: {e}")

    # 9. TabNews (API)
    try:
        logger.info("📑 Caçando no TabNews...")
        tabnews = TabNewsScraper()
        raw_jobs.extend(tabnews.fetch_jobs())
    except Exception as e: logger.error(f"Erro TabNews: {e}")

    # 10. Apinfo (Legacy)
    try:
        logger.info("💾 Caçando no Apinfo...")
        apinfo = ApinfoScraper()
        raw_jobs.extend(apinfo.fetch_jobs())
    except Exception as e: logger.error(f"Erro Apinfo: {e}")

    # --- DISABLED / BROKEN ---
    # EmpregosScraper -> Removed due to quality issues.

    return raw_jobs

def main_loop():
    """Loop principal do Hunter Bot."""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                 👻 BOOJ SYSTEM - CAÇADOR PRO 👻           ║
    ║        Monitorando vagas 24/7 com Inteligência + SQLite   ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Initialize SQLite database (memory-efficient!)
    db = JobDatabase()
    job_count = db.count_jobs()
    logger.info(f"💾 SQLite inicializado com {job_count} vagas no banco.")

    while True:
        try:
            start_time = datetime.now()
            
            # 1. Coletar
            jobs = run_cycle()
            
            # 2. Filtrar vagas antigas (apenas últimos 30 dias, exclui 2023 e antes)
            recent_jobs = apply_all_filters(jobs, max_days=30)
            
            # 3. Processamento Inteligente (Score + Dedupe via SQL)
            processed_jobs = []
            logger.info("🧠 Aplicando Inteligência (Match 0-100)...")
            
            for job in recent_jobs:
                # Deduplicação via SQLite (O(1) lookup, não carrega tudo na RAM!)
                if db.is_fuzzy_duplicate(job):
                    continue
                
                # Calcular Score
                job = brain.enhance_job_data(job)
                
                # Descartar lixo (score < 0)
                if job['score'] < 0:
                    continue
                    
                processed_jobs.append(job)
            
            # 4. Salvar no SQLite (batch insert)
            if processed_jobs:
                inserted = db.add_jobs_batch(processed_jobs)
                logger.info(f"💾 {inserted} vagas novas salvas no SQLite.")
            
            # 5. Notificar
            new_count = 0
            for job in processed_jobs:
                link = job['link']
                
                # Verifica se já foi enviado (via SQL)
                if db.is_sent(link):
                    continue
                
                # Discord (Todas as relevantes) - notifier já tem rate limiting interno
                send_discord_alert(job)
                
                # Telegram (Apenas as Melhores - Score > 40)
                if job['score'] >= 40:
                    try: 
                        telegram.send_job_alert(job)
                        db.mark_sent_telegram(link)
                    except: pass
                
                db.mark_sent_discord(link)
                new_count += 1
                # Rate limiting agora é feito pelo notifier.py

            
            # Enviar Resumo Diário no Telegram se houve novidades
            if new_count > 0:
                telegram.send_daily_summary(processed_jobs)

            logger.info(f"Ciclo finalizado. {new_count} novos alertas enviados.")
            
            # Dormência
            minutes = random.randint(HUNTER_SLEEP_MIN, HUNTER_SLEEP_MAX)
            seconds = minutes * 60
            next_run = datetime.now().timestamp() + seconds
            next_run_str = datetime.fromtimestamp(next_run).strftime("%H:%M:%S")
            logger.info(f"Dormindo por {minutes} min. Volta às {next_run_str}...")
            time.sleep(seconds)

        except KeyboardInterrupt:
            logger.info("Hunter Bot desativado pelo usuário.")
            sys.exit(0)
        except Exception as e:
            logger.error(f"ERRO CRÍTICO NO LOOP: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main_loop()

