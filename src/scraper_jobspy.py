# -*- coding: utf-8 -*-
"""
Scraper usando JobSpy
Integra LinkedIn, Indeed, ZipRecruiter com seletores mantidos
"""

from jobspy import scrape_jobs
from datetime import datetime
from typing import List, Dict
import pandas as pd

class JobSpyScraper:
    def __init__(self):
        self.platform = "JobSpy"
        self.sites = ["linkedin", "indeed", "zip_recruiter"]
    
    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas usando JobSpy em múltiplos sites."""
        all_jobs = []
        
        print(f"\n[*] Consultando JobSpy ({', '.join(self.sites)})...")
        
        # Termos otimizados para BR
        search_terms = [
            "desenvolvedor junior",
            "estagio ti",
            "trainee tecnologia"
        ]
        
        for term in search_terms[:2]:  # Limitar a 2 para não demorar
            try:
                print(f"  Buscando: '{term}'...")
                
                # Scrape jobs
                jobs_df = scrape_jobs(
                    site_name=self.sites,
                    search_term=term,
                    location="Brasil",
                    results_wanted=30,  # 30 por site = até 90 total
                    hours_old=72,  # Últimas 72h
                    country_indeed='Brazil'  # Indeed BR
                )
                
                if jobs_df is None or len(jobs_df) == 0:
                    continue
                
                # Converter DataFrame para nosso formato
                for _, row in jobs_df.iterrows():
                    # Filtro de qualidade
                    title = str(row.get('title', '')).lower()
                    if not any(kw in title for kw in ['junior', 'jr', 'estagio', 'trainee', 'entry']):
                        continue
                    
                    # Determinar localização
                    location = row.get('location', 'Brasil')
                    if pd.isna(location):
                        location = 'Brasil'
                    
                    # Remoto?
                    is_remote = row.get('is_remote', False)
                    if is_remote:
                        location = '🏠 REMOTO'
                    
                    # Plataforma original
                    site = row.get('site', 'JobSpy')
                    
                    job = {
                        "titulo": f"🌐 {row.get('title', 'Vaga')}",
                        "empresa": row.get('company', 'Empresa'),
                        "localizacao": location,
                        "link": row.get('job_url', ''),
                        "data_publicacao": datetime.now().strftime("%Y-%m-%d"),
                        "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "plataforma": f"{site.title()}"
                    }
                    
                    all_jobs.append(job)
                
            except Exception as e:
                print(f"  [!] Erro com termo '{term}': {e}")
                continue
        
        # Remover duplicatas por link
        seen_links = set()
        unique_jobs = []
        for job in all_jobs:
            link = job['link']
            if link not in seen_links:
                seen_links.add(link)
                unique_jobs.append(job)
        
        print(f"  [+] {len(unique_jobs)} vagas únicas encontradas via JobSpy")
        return unique_jobs
