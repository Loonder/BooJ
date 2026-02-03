# -*- coding: utf-8 -*-
"""
Scraper AVANÇADO para Telegram Channels
Lê canais BR de vagas em tempo real
"""

from telethon.sync import TelegramClient
from datetime import datetime, timedelta
from typing import List, Dict
import re
import os

class TelegramJobScraper:
    def __init__(self):
        self.api_id = os.getenv("TELEGRAM_API_ID", "")
        self.api_hash = os.getenv("TELEGRAM_API_HASH", "")
        self.phone = os.getenv("TELEGRAM_PHONE", "")
        self.platform = "Telegram"
        
        # Canais BR de vagas tech
        self.channels = [
            "@vagasdeti",
            "@devsjob", 
            "@estagiostech",
            "@remotasbr",
            "@vagastecnologia",
            "@vagasdevbr"
        ]
    
    def _extract_job_from_message(self, text: str) -> Dict:
        """Extrai informações de vaga de uma mensagem."""
        # Regex patterns para extrair dados
        title_patterns = [
            r"(?:vaga|oportunidade|hiring)[\s:]+(.+?)(?:\n|$)",
            r"(?:^|\n)(.+?)(?:júnior|junior|pleno|sênior|senior)",
            r"\*\*(.+?)\*\*"  # Texto em negrito
        ]
        
        company_patterns = [
            r"(?:empresa|company)[\s:]+(.+?)(?:\n|$)",
            r"(?:@|em|na)\s+([A-Z][a-zA-Z\s]+)",
        ]
        
        location_patterns = [
            r"(?:local|localização|location)[\s:]+(.+?)(?:\n|$)",
            r"(remoto|remote|home\s*office)",
            r"(?:SP|São Paulo|RJ|Rio de Janeiro)"
        ]
        
        link_patterns = [
            r"(https?://[^\s]+)",
            r"(?:link|apply|candidatar)[\s:]+(.+?)(?:\n|$)"
        ]
        
        # Extrair título
        title = "Vaga Tech"
        for pattern in title_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                title = match.group(1).strip()[:100]
                break
        
        # Extrair empresa
        company = "Empresa"
        for pattern in company_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                company = match.group(1).strip()[:50]
                break
        
        # Extrair localização
        location = "Brasil"
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                loc = match.group(1).strip() if len(match.groups()) > 0 else match.group(0)
                if 'remoto' in loc.lower() or 'remote' in loc.lower():
                    location = "🏠 REMOTO"
                else:
                    location = loc[:50]
                break
        
        # Extrair link
        link = ""
        for pattern in link_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                link = match.group(1).strip()
                break
        
        return {
            "titulo": f"📱 {title}",
            "empresa": company,
            "localizacao": location,
            "link": link if link else "https://t.me/vagasdeti"
        }
    
    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas dos canais do Telegram."""
        
        # Verificar credenciais
        if not self.api_id or not self.api_hash:
            print(f"\n[*] Telegram: Credenciais não configuradas (API_ID/API_HASH).")
            print("    Obtenha em: https://my.telegram.org/apps")
            return []
        
        all_jobs = []
        
        print(f"\n[*] Consultando {len(self.channels)} canais do Telegram...")
        
        try:
            # Criar cliente
            client = TelegramClient('session_jobs', int(self.api_id), self.api_hash)
            client.start(phone=self.phone)
            
            # Data limite (últimas 48h)
            date_limit = datetime.now() - timedelta(hours=48)
            
            for channel in self.channels:
                try:
                    # Buscar mensagens recentes
                    messages = client.get_messages(channel, limit=50)
                    
                    for msg in messages:
                        # Filtrar por data
                        if msg.date < date_limit:
                            continue
                        
                        text = msg.message
                        if not text:
                            continue
                        
                        # Filtrar por keywords relevantes
                        text_lower = text.lower()
                        keywords = ['vaga', 'estágio', 'estagio', 'júnior', 'junior', 
                                    'desenvolvedor', 'programador', 'tech', 'ti']
                        
                        if not any(kw in text_lower for kw in keywords):
                            continue
                        
                        # Extrair informações
                        job_data = self._extract_job_from_message(text)
                        
                        job = {
                            **job_data,
                            "data_publicacao": msg.date.strftime("%Y-%m-%d"),
                            "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "plataforma": f"{self.platform} ({channel})"
                        }
                        
                        all_jobs.append(job)
                    
                except Exception as e:
                    print(f"  [!] Erro no canal {channel}: {e}")
                    continue
            
            client.disconnect()
            
        except Exception as e:
            print(f"  [!] Erro Telegram: {e}")
            return []
        
        print(f"  [+] {len(all_jobs)} vagas encontradas no Telegram")
        return all_jobs
