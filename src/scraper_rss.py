# -*- coding: utf-8 -*-
"""
Scraper para Feeds RSS.
"""

import feedparser
from datetime import datetime
from typing import List, Dict

from config import RSS_FEEDS


class RssScraper:
    """Coleta vagas via RSS Feeds."""

    def __init__(self):
        self.feeds = RSS_FEEDS

    def fetch_all(self, terms: List[str] = None) -> List[Dict]:
        """
        Busca em todos os feeds configurados.
        """
        all_jobs = []
        print(f"\n[*] Consultando Feeds RSS...")

        for name, url in self.feeds.items():
            print(f"  [>] Lendo feed: {name}...")
            try:
                feed = feedparser.parse(url)
                
                if feed.bozo:
                    print(f"      [!] Aviso: XML do feed pode estar mal formatado.")
                
                count = 0
                for entry in feed.entries:
                    title = entry.get("title", "").strip()
                    summary = entry.get("summary", "").lower()
                    
                    # Filtragem simples
                    is_match = False
                    if not terms:
                        is_match = True
                    else:
                        # Termos extendidos para inglês (comum em RSS tech)
                        extended_terms = terms + ["intern", "internship", "estágio", "junior"]
                        search_text = f"{title.lower()} {summary}"
                        
                        for term in extended_terms:
                            if term.lower() in search_text:
                                is_match = True
                                break
                    
                    if is_match:
                        # Tentar extrair empresa do título (comum "Cargo @ Empresa")
                        company = "RSS Source"
                        if " @ " in title:
                            parts = title.split(" @ ")
                            title = parts[0]
                            company = parts[-1]
                        elif " at " in title:
                             parts = title.split(" at ")
                             title = parts[0]
                             company = parts[-1]

                        published = "N/A"
                        if hasattr(entry, "published"):
                            published = entry.published
                        elif hasattr(entry, "updated"):
                            published = entry.updated

                        job = {
                            "titulo": title,
                            "empresa": company,
                            "localizacao": "Remoto/RSS",
                            "link": entry.get("link"),
                            "data_publicacao": published,
                            "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "plataforma": f"RSS ({name})",
                        }
                        
                        all_jobs.append(job)
                        count += 1
                
                print(f"      [+] {count} vagas encontradas")

            except Exception as e:
                print(f"      [!] Erro ao ler feed {name}: {e}")

        return all_jobs
