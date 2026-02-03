# -*- coding: utf-8 -*-
"""
Scraper para Gupy API (Maior Plataforma de Recrutamento do Brasil)
Gupy powers Catho, Vagas.com, and hundreds of corporate career pages
"""

import requests
from datetime import datetime
from typing import List, Dict

class GupyScraper:
    """Scraper para Gupy API - A MAIOR do Brasil."""
    
    def __init__(self):
        self.platform = "Gupy"
        self.api_base = "https://portal.gupy.io/api"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas no Gupy (API pública)."""
        all_jobs = []
        
        print(f"\n[*] Consultando Gupy (Maior Plataforma BR)...")
        
        try:
            # Gupy API endpoint público
            # Buscar em career pages populares
            search_queries = [
                "desenvolvedor junior",
                "estagio ti",
                "trainee tecnologia"
            ]
            
            for query in search_queries[:2]:
                try:
                    # Endpoint de jobs públicos
                    url = f"{self.api_base}/v1/jobs"
                    params = {
                        'query': query,
                        'limit': 50,
                        'offset': 0
                    }
                    
                    response = requests.get(url, headers=self.headers, params=params, timeout=10)
                    
                    if response.status_code != 200:
                        # Fallback: Tentar através de career pages conhecidas
                        self._scrape_career_pages(all_jobs)
                        continue
                    
                    data = response.json()
                    jobs = data.get('data', data.get('jobs', []))
                    
                    for job in jobs:
                        try:
                            job_data = {
                                "titulo": f"🔵 {job.get('name', 'Vaga')}",
                                "empresa": job.get('companyName', job.get('careerPageName', 'Empresa')),
                                "localizacao": self._parse_location(job),
                                "link": f"https://portal.gupy.io/job/{job.get('id', '')}",
                                "data_publicacao": job.get('publishedDate', datetime.now().strftime("%Y-%m-%d")),
                                "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "plataforma": self.platform
                            }
                            
                            if not job_data['link'] or 'None' in job_data['link']:
                                continue
                            
                            all_jobs.append(job_data)
                            
                        except:
                            continue
                
                except Exception as e:
                    print(f"  [!] Erro query '{query}': {e}")
                    continue
        
        except Exception as e:
            print(f"  [!] Erro geral Gupy: {e}")
        
        print(f"  [+] {len(all_jobs)} vagas encontradas no Gupy")
        return all_jobs
    
    def _parse_location(self, job: Dict) -> str:
        """Extrai localização do job."""
        try:
            if 'city' in job and job['city']:
                city = job['city'].get('name', '')
                state = job['city'].get('state', {}).get('name', '')
                if city and state:
                    return f"{city}, {state}"
                return city or state or "Brasil"
            
            if 'location' in job:
                return job['location']
            
            if 'isRemote' in job and job['isRemote']:
                return "🏠 REMOTO"
            
            return "Brasil"
        except:
            return "Brasil"
    
    def _scrape_career_pages(self, all_jobs: List[Dict]):
        """Fallback: Scrapear career pages populares."""
        # Top companies using Gupy
        career_slugs = [
            "ambev", "nubank", "magazine-luiza", 
            "stone", "mercadolivre", "ifood"
        ]
        
        for slug in career_slugs[:3]:
            try:
                url = f"https://portal.gupy.io/api/v1/companies/{slug}/jobs"
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    jobs = data.get('data', [])
                    
                    for job in jobs[:10]:
                        try:
                            # Filtrar junior/estagio
                            title = job.get('name', '').lower()
                            if not any(kw in title for kw in ['junior', 'júnior', 'estagio', 'trainee', 'jr']):
                                continue
                            
                            job_data = {
                                "titulo": f"🔵 {job.get('name', '')}",
                                "empresa": slug.replace('-', ' ').title(),
                                "localizacao": self._parse_location(job),
                                "link": f"https://portal.gupy.io/job/{job.get('id', '')}",
                                "data_publicacao": datetime.now().strftime("%Y-%m-%d"),
                                "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "plataforma": self.platform
                            }
                            
                            all_jobs.append(job_data)
                        except:
                            continue
            except:
                continue
