# -*- coding: utf-8 -*-
"""
Scraper para Hacker News - "Who is Hiring" threads mensais.
100% grátis - usa API pública do HN.
"""

import requests
from datetime import datetime
from typing import List, Dict

class HackerNewsScraper:
    """Coleta vagas dos threads 'Who is Hiring' do HN."""

    def __init__(self):
        self.platform = "HackerNews"
        self.api_base = "https://hacker-news.firebaseio.com/v0"

    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas no HN Jobs e Who is Hiring."""
        all_jobs = []
        
        print(f"\n[*] Consultando Hacker News Jobs...")

        try:
            # HN tem endpoint de jobs direto
            response = requests.get(
                f"{self.api_base}/jobstories.json",
                timeout=15
            )
            
            if response.status_code != 200:
                print(f"  [!] HN retornou {response.status_code}")
                return []
            
            job_ids = response.json()[:30]  # Pegar 30 mais recentes
            
            for job_id in job_ids:
                try:
                    # Buscar detalhes de cada job
                    item_resp = requests.get(
                        f"{self.api_base}/item/{job_id}.json",
                        timeout=10
                    )
                    
                    if item_resp.status_code != 200:
                        continue
                    
                    item = item_resp.json()
                    if not item:
                        continue
                    
                    title = item.get("title", "")
                    title_lower = title.lower()
                    text = item.get("text", "").lower() if item.get("text") else ""
                    
                    # Filtrar junior/intern/remote
                    search_text = f"{title_lower} {text}"
                    is_relevant = any(term in search_text for term in 
                        ["junior", "jr", "intern", "entry", "remote", "trainee", 
                         "graduate", "early career", "new grad"])
                    
                    if is_relevant:
                        # Extrair empresa do título (formato: "Company is hiring...")
                        company = title.split(" is ")[0] if " is " in title else "Startup"
                        company = company.split(" (")[0]  # Remover parênteses
                        
                        job_data = {
                            "titulo": f"🔶 {title[:100]}",
                            "empresa": company[:50],
                            "localizacao": "🌍 Remote/Global" if "remote" in search_text else "USA",
                            "link": item.get("url", f"https://news.ycombinator.com/item?id={job_id}"),
                            "data_publicacao": datetime.fromtimestamp(
                                item.get("time", 0)
                            ).strftime("%Y-%m-%d"),
                            "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "plataforma": self.platform
                        }
                        all_jobs.append(job_data)
                        
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"  [!] Erro HN: {e}")
            return []
        
        print(f"  [+] {len(all_jobs)} vagas junior/remote encontradas no HN")
        return all_jobs
