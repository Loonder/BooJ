# -*- coding: utf-8 -*-
"""
Scraper para Remotive.com (Via API Pública)
Remote jobs de alta qualidade
"""

import requests
from datetime import datetime
from typing import List, Dict

class RemotiveScraper:
    def __init__(self):
        self.api_url = "https://remotive.com/api/remote-jobs"
        self.platform = "Remotive"
    
    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas remotas via API pública do Remotive."""
        all_jobs = []
        print(f"\n[*] Consultando Remotive API...")
        
        try:
            # A API retorna vagas recentes, podemos filtrar por categoria se necessário
            params = {
                "limit": 50,  # Limitar a 50 vagas mais recentes
                # "category": "software-dev" # Opcional: filtrar categoria
            }
            
            response = requests.get(self.api_url, params=params, timeout=10)
            
            if response.status_code != 200:
                print(f"  [!] Remotive API retornou {response.status_code}")
                return []
            
            data = response.json()
            
            # API retorna formato: {"jobs": [...]}
            jobs_data = data.get("jobs", [])
            
            for job_data in jobs_data:
                try:
                    title = job_data.get("title", "")
                    company = job_data.get("company_name", "Unknown Company")
                    location = job_data.get("candidate_required_location", "Remote")
                    link = job_data.get("url", "")
                    published = job_data.get("publication_date", datetime.now().strftime("%Y-%m-%d"))
                    category = job_data.get("category", "")
                    
                    if not title or not link:
                        continue
                    
                    # Filtro opcional por categoria relevante
                    relevant_categories = ["software", "dev", "engineer", "data", "tech"]
                    if category and not any(cat in category.lower() for cat in relevant_categories):
                        continue
                    
                    # Filtro por palavras-chave no título se terms fornecidos
                    if terms:
                        title_lower = title.lower()
                        if not any(term.lower() in title_lower for term in terms):
                            continue
                    
                    job = {
                        "titulo": f"🌍 {title}",
                        "empresa": company,
                        "localizacao": location if location else "🏠 Remote",
                        "link": link,
                        "data_publicacao": published,
                        "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "plataforma": self.platform
                    }
                    
                    all_jobs.append(job)
                    
                except Exception:
                    continue
            
        except Exception as e:
            print(f"  [!] Erro Remotive API: {e}")
            return []
        
        print(f"  [+] {len(all_jobs)} vagas encontradas no Remotive")
        return all_jobs
