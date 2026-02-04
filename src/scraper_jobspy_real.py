# -*- coding: utf-8 -*-
"""
Scraper usando JobSpy - LinkedIn + Indeed + ZipRecruiter + Glassdoor
Funciona apenas com Python 3.11 (não 3.13)
"""

from jobspy import scrape_jobs
from datetime import datetime
from typing import List, Dict
import pandas as pd

class JobSpyRealScraper:
    """Scraper multi-plataforma usando JobSpy library."""
    
    def __init__(self):
        self.platform = "JobSpy"
        self.sites = ["indeed", "linkedin", "zip_recruiter", "glassdoor"]
    
    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas em múltiplas plataformas."""
        all_jobs = []
        
        print(f"\n[*] Consultando JobSpy (LinkedIn + Indeed + ZipRecruiter)...")
        
        try:
            # Query otimizada para Brasil
            search_terms = [
                "desenvolvedor junior",
                "estagio ti",
                "trainee tecnologia"
            ]
            
            locations = [
                "São Paulo, SP", 
                "Rio de Janeiro, RJ", 
                "Remote, Brazil"
            ]
            
            for term in search_terms[:2]:  # Limitar a 2 para não demorar muito
                for loc in locations:
                    try:
                        print(f"  [*] Buscando '{term}' em '{loc}'...")
                        
                        # JobSpy scrape
                        jobs_df = scrape_jobs(
                            site_name=self.sites,
                            search_term=term,
                            location=loc,
                            results_wanted=15,
                            hours_old=168,
                            country_indeed='Brazil',
                            linkedin_fetch_description=False
                        )
                    
                        if jobs_df is None or len(jobs_df) == 0:
                            continue
                        
                        # Converter para nosso formato
                        for _, job in jobs_df.iterrows():
                            try:
                                site = job.get('site', 'unknown')
                                
                                # Ícone por plataforma
                                icon = {
                                    'linkedin': '🔵',
                                    'indeed': '🟢',
                                    'zip_recruiter': '🟣',
                                    'glassdoor': '🟡'
                                }.get(site, '⚪')
                                
                                job_data = {
                                    "titulo": f"{icon} {job.get('title', 'Vaga')}",
                                    "empresa": job.get('company', 'Empresa'),
                                    "localizacao": self._parse_location(job),
                                    "link": job.get('job_url', ''),
                                    "data_publicacao": job.get('date_posted', datetime.now().strftime("%Y-%m-%d")),
                                    "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "plataforma": f"JobSpy ({site.title()})"
                                }
                                
                                # Validação básica
                                if not job_data['link'] or 'None' in job_data['link']:
                                    continue
                                
                                all_jobs.append(job_data)
                                
                            except Exception as e:
                                continue
                
                    except Exception as e:
                        print(f"  [!] Erro no termo '{term}' em '{loc}': {e}")
                        continue
        
        except Exception as e:
            print(f"  [!] Erro geral JobSpy: {e}")
        
        print(f"  [+] {len(all_jobs)} vagas encontradas via JobSpy")
        return all_jobs
    
    def _parse_location(self, job) -> str:
        """Extrai localização do job."""
        try:
            # JobSpy retorna city, state (handling both dict and DataFrame row)
            city = job.get('city', '') if isinstance(job.get('city'), str) else (job.get('city', {}).get('name', '') if isinstance(job.get('city'), dict) else str(job.get('city', '')))
            state = job.get('state', '') if isinstance(job.get('state'), str) else (job.get('state', {}).get('name', '') if isinstance(job.get('state'), dict) else str(job.get('state', '')))
            
            if city and state:
                return f"{city}, {state}"
            elif city:
                return city
            elif state:
                return state
            
            # Fallback: location field
            location = job.get('location', '')
            if location:
                return location
            
            # Checar se é remoto
            if job.get('is_remote', False) or job.get('isRemote', False):
                return "🏠 REMOTO"
            
            return "Brasil"
        except:
            return "Brasil"
