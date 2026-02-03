# -*- coding: utf-8 -*-
"""
Scraper para canais públicos do Telegram - Vagas BR.
Usa Telethon para ler mensagens de canais públicos.
"""

import os
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict

# Telethon é instalado via requirements.txt
try:
    from telethon import TelegramClient
    from telethon.tl.functions.messages import GetHistoryRequest
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False

class TelegramScraper:
    """Coleta vagas de canais públicos do Telegram."""

    def __init__(self):
        self.platform = "Telegram"
        self.api_id = os.getenv("TELEGRAM_API_ID", "")
        self.api_hash = os.getenv("TELEGRAM_API_HASH", "")
        
        # Canais brasileiros de vagas (públicos)
        self.channels = [
            "vagasTI",
            "VagasBrasil_TI",
            "vagastecnologia",
            "estagiosbr",
            "vagasremotobr",
            "DevJobs_BR",
        ]
        
        self.session_file = "data/telegram_session"

    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas nos canais do Telegram."""
        if not TELETHON_AVAILABLE:
            print(f"\n[*] Telegram: Telethon não instalado. Pulando...")
            return []
            
        if not self.api_id or not self.api_hash:
            print(f"\n[*] Telegram: Credenciais não configuradas. Pulando...")
            return []
        
        # Rodar async
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self._fetch_async())

    async def _fetch_async(self) -> List[Dict]:
        """Busca assíncrona nos canais."""
        all_jobs = []
        seen_ids = set()
        
        print(f"\n[*] Consultando Telegram ({len(self.channels)} canais)...")
        
        # Garantir diretório
        os.makedirs("data", exist_ok=True)
        
        client = TelegramClient(self.session_file, int(self.api_id), self.api_hash)
        
        try:
            await client.start()
            
            # Data limite (últimos 7 dias)
            date_limit = datetime.now() - timedelta(days=7)
            
            for channel_name in self.channels:
                try:
                    # Tentar resolver o canal primeiro com tratamento de erro específico
                    try:
                        channel = await client.get_entity(channel_name)
                    except ValueError:
                        print(f"  [!] Canal não encontrado (ValueError): {channel_name}")
                        continue
                    except Exception as e:
                        # RpcError ou outros erros de resolução
                        print(f"  [!] Erro ao resolver canal {channel_name}: {e}")
                        continue
                    
                    # Pegar últimas 50 mensagens
                    history = await client(GetHistoryRequest(
                        peer=channel,
                        limit=50,
                        offset_date=None,
                        offset_id=0,
                        max_id=0,
                        min_id=0,
                        add_offset=0,
                        hash=0
                    ))
                    
                    for msg in history.messages:
                        if not msg.message:
                            continue
                        
                        # Verificar data
                        if msg.date.replace(tzinfo=None) < date_limit:
                            continue
                        
                        msg_id = f"{channel_name}_{msg.id}"
                        if msg_id in seen_ids:
                            continue
                        seen_ids.add(msg_id)
                        
                        text = msg.message
                        text_lower = text.lower()
                        
                        # Filtrar por termos de estágio/junior
                        is_relevant = any(term in text_lower for term in 
                            ["estágio", "estagio", "junior", "jr", "trainee", 
                             "vaga", "contratando", "oportunidade", "hiring"])
                        
                        if is_relevant and len(text) > 50:
                            # Extrair título (primeira linha)
                            lines = text.split('\n')
                            title = lines[0][:100] if lines else text[:100]
                            
                            # Detectar localização
                            loc = "Brasil"
                            if any(x in text_lower for x in ["remoto", "remote", "home office"]):
                                loc = "🏠 Remoto"
                            elif "são paulo" in text_lower or " sp" in text_lower:
                                loc = "📍 SP"
                            elif "rio de janeiro" in text_lower or " rj" in text_lower:
                                loc = "📍 RJ"
                            
                            job_data = {
                                "titulo": f"💬 {title}",
                                "empresa": f"@{channel_name}",
                                "localizacao": loc,
                                "link": f"https://t.me/{channel_name}/{msg.id}",
                                "data_publicacao": msg.date.strftime("%Y-%m-%d"),
                                "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "plataforma": f"Telegram ({channel_name})"
                            }
                            all_jobs.append(job_data)
                            
                except Exception as e:
                    print(f"  [!] Erro genérico no loop do canal {channel_name}: {e}")
                    continue
                    
        except Exception as e:
            print(f"  [!] Erro Telegram: {e}")
            return []
        finally:
            await client.disconnect()
        
        print(f"  [+] {len(all_jobs)} vagas encontradas no Telegram")
        return all_jobs
