# -*- coding: utf-8 -*-
"""
Scraper para Adzuna API.
Adzuna é um agregador de vagas com API gratuita.
Registre em: https://developer.adzuna.com/
"""

import requests
from datetime import datetime
from typing import List, Dict
import os

class AdzunaScraper:
    """Coleta vagas via API do Adzuna - Prioriza SP e Remoto."""

    def __init__(self):
        self.app_id = os.getenv("ADZUNA_APP_ID", "")
        self.app_key = os.getenv("ADZUNA_APP_KEY", "")
        self.base_url = "https://api.adzuna.com/v1/api/jobs/br/search"
        self.platform = "Adzuna"
        
        # Priorizar SP e Remoto, depois nacional
        self.search_queries = [
            # PRIORIDADE 1: São Paulo
            ("estágio TI", "São Paulo"),
            ("estágio desenvolvedor", "São Paulo"),
            ("estagiário programação", "São Paulo"),
            # PRIORIDADE 2: Remoto
            ("estágio remoto", None),
            ("estágio home office", None),
            ("desenvolvedor remoto junior", None),
            # PRIORIDADE 3: Nacional
            ("estágio tecnologia", None),
            ("trainee tecnologia", None),
            ("junior desenvolvedor", None),
        ]
    
    def _get_location_tag(self, location: str) -> str:
        """Retorna tag de localização baseado no texto."""
        loc_lower = location.lower() if location else ""
        
        if any(x in loc_lower for x in ["remoto", "remote", "home office", "anywhere"]):
            return "🏠 REMOTO"
        elif any(x in loc_lower for x in ["são paulo", "sao paulo", "sp"]):
            return "📍 SP"
        elif any(x in loc_lower for x in ["rio de janeiro", "rj"]):
            return "📍 RJ"
        else:
            return "🇧🇷 BR"

    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas no Adzuna Brasil - Prioriza SP e Remoto."""
        if not self.app_id or not self.app_key:
            print(f"\n[*] Adzuna: Credenciais não configuradas. Pulando...")
            return []

        all_jobs = []
        seen_links = set()
        
        print(f"\n[*] Consultando API Adzuna ({len(self.search_queries)} buscas - SP/Remoto primeiro)...")
        
        for query_tuple in self.search_queries:
            query = query_tuple[0]
            location = query_tuple[1] if len(query_tuple) > 1 else None
            
            try:
                # Paginação: Páginas 1, 2 e 3
                for page in range(1, 4):
                    params = {
                        "app_id": self.app_id,
                        "app_key": self.app_key,
                        "results_per_page": 50,
                        "what": query,
                        "max_days_old": 30,
                        "sort_by": "date"
                    }
                    
                    # Adicionar filtro de localização se especificado
                    if location:
                        params["where"] = location
                    
                    try:
                        response = requests.get(
                            f"{self.base_url}/{page}",
                            params=params,
                            timeout=15
                        )
                        
                        if response.status_code != 200:
                            # Se der erro numa página, passa para a próxima ou encerra a query?
                            # Geralmente 400/404 indica fim.
                            continue
                        
                        data = response.json()
                        results = data.get("results", [])
                        
                        if not results:
                            # Se página vier vazia, para de iterar essa query
                            break
                        
                        for item in results:
                            link = item.get("redirect_url", "")
                            
                            # FILTRO: Rejeitar domínios ruins ANTES de adicionar
                            link_lower = link.lower()
                            blacklisted_domains = ['emprego.pt', 'net-empregos', 'empregos.pt']
                            if any(domain in link_lower for domain in blacklisted_domains):
                                continue  # Pular esta vaga
                            
                            if link in seen_links:
                                continue
                            seen_links.add(link)
                            
                            title = item.get("title", "")
                            title_lower = title.lower()
                            description = item.get("description", "").lower()
                            search_text = f"{title_lower} {description}"
                            
                            is_relevant = any(term in search_text for term in 
                                ["estágio", "estagio", "intern", "junior", "trainee", "jr", "entry"])
                            
                            if is_relevant:
                                job_location = item.get("location", {}).get("display_name", "Brasil")
                                location_tag = self._get_location_tag(job_location)
                                
                                # Adicionar tag ao título
                                tagged_title = f"{location_tag} {title}"
                                
                                job = {
                                    "titulo": tagged_title,
                                    "empresa": item.get("company", {}).get("display_name", "Empresa"),
                                    "localizacao": job_location,
                                    "link": link,
                                    "data_publicacao": item.get("created", "N/A")[:10],
                                    "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "plataforma": self.platform
                                }
                                all_jobs.append(job)
                                
                    except Exception as pg_err:
                        print(f"      [!] Erro na página {page} da query '{query}': {pg_err}")
                        continue
                        
            except Exception as e:
                print(f"  [!] Erro na query '{query}': {e}")
                continue
        
        print(f"  [+] {len(all_jobs)} vagas únicas encontradas no Adzuna")
        return all_jobs
