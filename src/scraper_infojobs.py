# -*- coding: utf-8 -*-
"""
Scraper para InfoJobs Brasil (API)
Requer API key gratuita de https://developer.infojobs.net/
"""

import requests
from datetime import datetime
from typing import List, Dict
import os

class InfoJobsScraper:
    """Scraper InfoJobs via API oficial."""
    
    def __init__(self):
        self.platform = "InfoJobs"
        self.api_url = "https://api.infojobs.com.br/v1"
        # API Key é opcional - pode pegar de .env
        self.api_key = os.getenv("INFOJOBS_API_KEY", "")
        self.headers = {
            "User-Agent": "Mozilla/5.0",
        }
        
        # Se tiver API key, adicionar no header
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
    
    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas no InfoJobs."""
        all_jobs = []
        
        print(f"\n[*] Consultando InfoJobs...")
        
        if not self.api_key:
            print(f"  [!] API Key não configurada (opcional)")
            print(f"  [!] Para usar InfoJobs, adicione INFOJOBS_API_KEY no .env")
            print(f"  [!] Registre em: https://developer.infojobs.net/")
            return []
        
        try:
            # Queries otimizadas
            queries = ["desenvolvedor junior", "estagio ti"]
            
            for query in queries[:1]:
                try:
                    params = {
                        "q": query,
                        "province": "SP",  # São Paulo
                        "page": 1,
                        "pageSize": 50
                    }
                    
                    response = requests.get(
                        f"{self.api_url}/vacancies",
                        headers=self.headers,
                        params=params,
                        timeout=10
                    )
                    
                    if response.status_code != 200:
                        print(f"  [!] InfoJobs retornou {response.status_code}")
                        continue
                    
                    data = response.json()
                    vacancies = data.get('items', data.get('vacancies', []))
                    
                    for vac in vacancies:
                        try:
                            title = vac.get('title', 'Vaga')
                            company = vac.get('author', {}).get('name', 'Empresa')
                            location = vac.get('province', {}).get('value', 'Brasil')
                            link = vac.get('link', vac.get('url', ''))
                            
                            if not link:
                                continue
                            
                            job = {
                                "titulo": f"🔵 {title}",
                                "empresa": company,
                                "localizacao": location,
                                "link": link,
                                "data_publicacao": datetime.now().strftime("%Y-%m-%d"),
                                "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "plataforma": self.platform
                            }
                            
                            all_jobs.append(job)
                            
                        except:
                            continue
                
                except Exception as e:
                    print(f"  [!] Erro query '{query}': {e}")
                    continue
        
        except Exception as e:
            print(f"  [!] Erro InfoJobs: {e}")
        
        print(f"  [+] {len(all_jobs)} vagas encontradas no InfoJobs")
        return all_jobs
