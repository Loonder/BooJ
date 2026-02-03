# -*- coding: utf-8 -*-
"""
Módulo de Notificações para o Hunter Bot.
Envia alertas para Discord via Webhook com rate limiting inteligente.
"""

import requests
import json
import logging
import time
from typing import Dict, List
from config import DISCORD_WEBHOOK_URL, GOLD_KEYWORDS

logger = logging.getLogger("HunterNotifier")

# Rate limiting state
_last_request_time = 0
_consecutive_429s = 0

def calculate_score(job: Dict) -> int:
    """Calcula pontuação da vaga baseado em keywords."""
    score = 0
    title = job.get("titulo", "").lower()
    desc = job.get("descricao", "").lower() # Futuro: se tiver descrição completa
    content = f"{title} {desc}"
    
    for kw in GOLD_KEYWORDS:
        if kw.lower() in content:
            score += 10
            
    return score

def _wait_for_rate_limit():
    """Espera tempo adequado baseado no histórico de rate limits."""
    global _last_request_time, _consecutive_429s
    
    # Base delay: 2 segundos (Discord permite ~30 requests/min)
    base_delay = 2.0
    
    # Se teve 429s recentes, aumenta o delay exponencialmente
    if _consecutive_429s > 0:
        delay = base_delay * (2 ** min(_consecutive_429s, 5))  # Max 64 segundos
    else:
        delay = base_delay
    
    elapsed = time.time() - _last_request_time
    if elapsed < delay:
        sleep_time = delay - elapsed
        logger.debug(f"Rate limit: aguardando {sleep_time:.1f}s...")
        time.sleep(sleep_time)

def send_discord_alert(job: Dict, new_job: bool = True, max_retries: int = 3):
    """
    Envia alerta rico para o Discord com retry e backoff exponencial.
    """
    global _last_request_time, _consecutive_429s
    
    if not DISCORD_WEBHOOK_URL:
        logger.warning("Discord Webhook não configurado.")
        return False

    score = calculate_score(job)
    is_gold = score > 0
    
    # Cores: Dourado (Gold) ou Azul (Normal)
    color = 16766720 if is_gold else 3447003
    
    emoji = "🔥" if is_gold else "🆕"
    title_prefix = "[VAGA PERFEITA]" if is_gold else "[Nova Vaga]"
    
    embed = {
        "title": f"{emoji} {title_prefix} {job['titulo']}",
        "url": job['link'],
        "color": color,
        "fields": [
            {
                "name": "🏢 Empresa",
                "value": job['empresa'],
                "inline": True
            },
            {
                "name": "📍 Local",
                "value": job['localizacao'],
                "inline": True
            },
            {
                "name": "📌 Fonte",
                "value": job['plataforma'],
                "inline": True
            },
            {
                "name": "🕐 Publicado",
                "value": job.get("data_publicacao", "N/A"),
                "inline": True
            }
        ],
        "footer": {
            "text": f"Hunter Bot • Score: {score} • {job['data_coleta']}"
        }
    }
    
    payload = {
        "username": "JobPulse Hunter",
        "avatar_url": "https://i.imgur.com/4M34hi2.png",
        "embeds": [embed]
    }
    
    for attempt in range(max_retries):
        try:
            # Aguarda rate limit antes de enviar
            _wait_for_rate_limit()
            
            response = requests.post(
                DISCORD_WEBHOOK_URL,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            _last_request_time = time.time()
            
            # Handle rate limit response
            if response.status_code == 429:
                _consecutive_429s += 1
                retry_after = response.json().get('retry_after', 5)
                logger.warning(f"Rate limited! Aguardando {retry_after}s (tentativa {attempt + 1}/{max_retries})")
                time.sleep(retry_after)
                continue
            
            response.raise_for_status()
            
            # Reset 429 counter on success
            _consecutive_429s = max(0, _consecutive_429s - 1)
            
            logger.info(f"Notificação enviada: {job.get('localizacao', '🇧🇷 BR')[:5]} {job['titulo'][:50]}")
            return True
            
        except requests.exceptions.RequestException as e:
            if "429" in str(e):
                _consecutive_429s += 1
                wait_time = 5 * (attempt + 1)
                logger.warning(f"Rate limit (429). Aguardando {wait_time}s...")
                time.sleep(wait_time)
            else:
                logger.error(f"Erro ao enviar notificação: {e}")
                return False
    
    logger.error(f"Falha após {max_retries} tentativas: {job['titulo'][:30]}")
    return False

