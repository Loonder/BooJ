# -*- coding: utf-8 -*-
"""
Scraper usando JobSpy - OTIMIZADO para máximo volume BRASIL
LinkedIn + Indeed + Google (SEM Glassdoor - muito lento)
Meta: 150+ vagas por ciclo
"""

from jobspy import scrape_jobs
from datetime import datetime
from typing import List, Dict
import pandas as pd

class JobSpyRealScraper:
    """Scraper multi-plataforma usando JobSpy - TURBO BRASIL."""
    
    def __init__(self):
        self.platform = "JobSpy"
        # Removido glassdoor (muito lento e erros de location)
        self.sites = ["indeed", "linkedin", "google"]
    
    def _safe_str(self, value, default: str = "") -> str:
        """Converte valor para string, tratando NaN e None."""
        if value is None:
            return default
        if pd.isna(value):
            return default
        return str(value).strip()
    
    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas em múltiplas plataformas - VOLUME MÁXIMO BRASIL."""
        all_jobs = []
        
        print(f"\n[*] 🚀 JobSpy TURBO BRASIL (Indeed + LinkedIn + Google)...")
        
        try:
            # Termos EXPANDIDOS para cobertura nacional
            search_terms = [
                # Desenvolvimento
                "desenvolvedor junior",
                "desenvolvedor trainee",
                "programador junior",
                "desenvolvedor web junior",
                "front end junior",
                "back end junior",
                "full stack junior",
                # Estágio TI
                "estagio ti",
                "estagio tecnologia",
                "estagio programacao",
                "estagio desenvolvimento",
                "estagio sistemas",
                "estagio informatica",
                # Trainee
                "trainee tecnologia",
                "trainee ti",
                # Análise
                "analista junior ti",
                "analista sistemas junior",
                "suporte tecnico junior",
                # Dados
                "analista dados junior",
                "estagio dados",
                "estagio ciencia dados",
                # SDR / Vendas / Comercial
                "sdr junior",
                "sdr estagio",
                "sales development representative",
                "pre vendas junior",
                "closer junior",
                "inside sales junior",
                "estagio vendas",
                "estagio comercial",
                "vendedor junior",
                "analista comercial junior",
                "bdr junior"
            ]
            
            # Todas as capitais brasileiras + regiões importantes
            locations = [
                # Sudeste (maior mercado)
                "São Paulo, Brazil",
                "Rio de Janeiro, Brazil",
                "Belo Horizonte, Brazil",
                "Campinas, Brazil",
                "Vitória, Brazil",
                # Sul
                "Curitiba, Brazil",
                "Porto Alegre, Brazil",
                "Florianópolis, Brazil",
                # Centro-Oeste
                "Brasília, Brazil",
                "Goiânia, Brazil",
                "Campo Grande, Brazil",
                # Nordeste
                "Salvador, Brazil",
                "Recife, Brazil",
                "Fortaleza, Brazil",
                "Natal, Brazil",
                # Norte
                "Manaus, Brazil",
                "Belém, Brazil",
                # Genérico
                "Brazil",
                "Remote"
            ]
            
            # Randomizar e aumentar range de busca para garantir variedade (Junior, Sdr, Estágio)
            import random
            random.shuffle(search_terms)
            terms_to_use = search_terms[:5] # Reduzido para 5 para ciclos mais rápidos e evitar travar
            locs_to_use = locations[:4] # Reduz locations para focar nos termos
            
            for term in terms_to_use:
                for loc in locs_to_use:
                    try:
                        print(f"  [*] '{term}' em '{loc}'...")
                        
                        jobs_df = scrape_jobs(
                            site_name=self.sites,
                            search_term=term,
                            location=loc,
                            results_wanted=30,  # 30 por combinação
                            hours_old=72,  # Últimos 3 dias
                            country_indeed='Brazil',
                            linkedin_fetch_description=False,
                            verbose=0
                        )
                    
                        if jobs_df is None or len(jobs_df) == 0:
                            continue
                        
                        print(f"      [+] {len(jobs_df)} encontradas")
                        
                        for _, job in jobs_df.iterrows():
                            try:
                                site = job.get('site', 'unknown')
                                icon = {
                                    'linkedin': '🔵',
                                    'indeed': '🟢',
                                    'google': '�',
                                    'zip_recruiter': '�'
                                }.get(site, '⚪')
                                
                                job_data = {
                                    "titulo": f"{icon} {self._safe_str(job.get('title'), 'Vaga')}",
                                    "empresa": self._safe_str(job.get('company'), 'Empresa'),
                                    "localizacao": self._parse_location(job),
                                    "link": self._safe_str(job.get('job_url')),
                                    "data_publicacao": self._safe_str(job.get('date_posted'), datetime.now().strftime("%Y-%m-%d")),
                                    "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "plataforma": f"JobSpy ({self._safe_str(site, 'unknown').title()})"
                                }
                                
                                if not job_data['link'] or 'None' in str(job_data['link']):
                                    continue
                                
                                all_jobs.append(job_data)
                                
                            except Exception:
                                continue
                
                    except Exception as e:
                        # Continua silenciosamente para não travar
                        continue
            
            # Busca EXTRA: Estágios com filtro job_type
            print(f"  [*] 🎓 Buscando estágios (filtro especial)...")
            try:
                internship_df = scrape_jobs(
                    site_name=["indeed", "linkedin"],
                    search_term="estagio",
                    location="Brazil",
                    job_type="internship",
                    results_wanted=100,
                    country_indeed='Brazil',
                    verbose=0
                )
                
                if internship_df is not None and len(internship_df) > 0:
                    print(f"      [+] {len(internship_df)} estágios")
                    for _, job in internship_df.iterrows():
                        try:
                            site = job.get('site', 'unknown')
                            job_data = {
                                "titulo": f"🎓 {self._safe_str(job.get('title'), 'Estágio')}",
                                "empresa": self._safe_str(job.get('company'), 'Empresa'),
                                "localizacao": self._parse_location(job),
                                "link": self._safe_str(job.get('job_url')),
                                "data_publicacao": self._safe_str(job.get('date_posted'), datetime.now().strftime("%Y-%m-%d")),
                                "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "plataforma": f"JobSpy ({self._safe_str(site, 'unknown').title()}) Estágio"
                            }
                            if job_data['link'] and 'None' not in str(job_data['link']):
                                all_jobs.append(job_data)
                        except:
                            continue
            except Exception as e:
                print(f"  [!] Erro estágios: {e}")
            
            # Busca EXTRA: Remotas
            print(f"  [*] 🏠 Buscando vagas remotas...")
            try:
                remote_df = scrape_jobs(
                    site_name=["indeed", "linkedin"],
                    search_term="desenvolvedor",
                    is_remote=True,
                    results_wanted=50,
                    country_indeed='Brazil',
                    verbose=0
                )
                
                if remote_df is not None and len(remote_df) > 0:
                    print(f"      [+] {len(remote_df)} remotas")
                    for _, job in remote_df.iterrows():
                        try:
                            site = job.get('site', 'unknown')
                            job_data = {
                                "titulo": f"🏠 {self._safe_str(job.get('title'), 'Remoto')}",
                                "empresa": self._safe_str(job.get('company'), 'Empresa'),
                                "localizacao": "🏠 REMOTO",
                                "link": self._safe_str(job.get('job_url')),
                                "data_publicacao": self._safe_str(job.get('date_posted'), datetime.now().strftime("%Y-%m-%d")),
                                "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "plataforma": f"JobSpy ({self._safe_str(site, 'unknown').title()}) Remoto"
                            }
                            if job_data['link'] and 'None' not in str(job_data['link']):
                                all_jobs.append(job_data)
                        except:
                            continue
            except Exception as e:
                print(f"  [!] Erro remotas: {e}")
        
        except Exception as e:
            print(f"  [!] Erro geral JobSpy: {e}")
        
        # Dedupe por link
        seen = set()
        unique_jobs = []
        for job in all_jobs:
            if job['link'] not in seen:
                seen.add(job['link'])
                unique_jobs.append(job)
        
        print(f"  [+] ✅ {len(unique_jobs)} vagas ÚNICAS via JobSpy (de {len(all_jobs)} total)")
        return unique_jobs
    
    def _parse_location(self, job) -> str:
        """Extrai localização do job."""
        try:
            city = str(job.get('city', '') or '')
            state = str(job.get('state', '') or '')
            
            if city and city != 'nan' and state and state != 'nan':
                return f"{city}, {state}"
            elif city and city != 'nan':
                return city
            elif state and state != 'nan':
                return state
            
            location = str(job.get('location', '') or '')
            if location and location != 'nan':
                return location
            
            if job.get('is_remote', False):
                return "🏠 REMOTO"
            
            return "Brasil"
        except:
            return "Brasil"
