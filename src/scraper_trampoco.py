# -*- coding: utf-8 -*-
"""
Scraper para Trampo.co
Site BR de vagas para startups e tech
"""

import requests
from datetime import datetime
from typing import List, Dict

class TrampoCoScraper:
    """Scraper para Trampo.co."""
    
    def __init__(self):
        self.base_url = "https://trampo.co"
        self.platform = "Trampo.co"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas no Trampo.co."""
        all_jobs = []
        
        print(f"\n[*] Consultando Trampo.co...")
        
        try:
            # Trampo.co pode ter API ou endpoint JSON
            # Tentar endpoint de API primeiro
            api_url = f"{self.base_url}/api/opportunities"
            
            params = {
                "query": "junior",
                "location": "remoto",
                "page": 1
            }
            
            try:
                response = requests.get(api_url, headers=self.headers, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Processar JSON
                    opportunities = data.get('opportunities', data.get('data', []))
                    
                    for opp in opportunities[:30]:
                        try:
                            job = {
                                "titulo": f"🚀 {opp.get('title', 'Vaga')}",
                                "empresa": opp.get('company', {}).get('name', 'Startup'),
                                "localizacao": opp.get('location', 'Brasil'),
                                "link": f"{self.base_url}/oportunidades/{opp.get('slug', opp.get('id'))}",
                                "data_publicacao": datetime.now().strftime("%Y-%m-%d"),
                                "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "plataforma": self.platform
                            }
                            
                            all_jobs.append(job)
                        except:
                            continue
                    
                else:
                    # Fallback: Web scraping
                    print(f"  [!] API não disponível, tentando web scraping...")
                    return self._fallback_web_scraping()
                    
            except Exception:
                return self._fallback_web_scraping()
        
        except Exception as e:
            print(f"  [!] Erro Trampo.co: {e}")
        
        print(f"  [+] {len(all_jobs)} vagas encontradas no Trampo.co")
        return all_jobs
    
    def _fallback_web_scraping(self) -> List[Dict]:
        """Fallback usando requests + BeautifulSoup."""
        from bs4 import BeautifulSoup
        
        jobs = []
        
        try:
            url = f"{self.base_url}/oportunidades?q=junior"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Procurar links de vagas
            job_links = soup.select('a[href*="/oportunidade/"]')
            
            for link in job_links[:20]:
                try:
                    href = link.get('href', '')
                    if not href.startswith('http'):
                        href = f"{self.base_url}{href}"
                    
                    title = link.get_text(strip=True)
                    
                    if len(title) < 10:
                        continue
                    
                    job = {
                        "titulo": f"🚀 {title[:80]}",
                        "empresa": "Startup",
                        "localizacao": "Brasil",
                        "link": href,
                        "data_publicacao": datetime.now().strftime("%Y-%m-%d"),
                        "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "plataforma": self.platform
                    }
                    
                    jobs.append(job)
                except:
                    continue
        
        except Exception as e:
            print(f"  [!] Fallback error: {e}")
        
        return jobs
