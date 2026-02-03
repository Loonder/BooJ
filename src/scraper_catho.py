# -*- coding: utf-8 -*-
"""
Scraper para Catho.com.br
Site brasileiro de empregos - BeautifulSoup
"""

import requests
from bs4 import BeautifulSoup  
from datetime import datetime
from typing import List, Dict

class CathoScraper:
    """Scraper para Catho.com.br - vagas BR."""
    
    def __init__(self):
        self.base_url = "https://www.catho.com.br/vagas"
        self.platform = "Catho"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas no Catho."""
        all_jobs = []
        
        print(f"\n[*] Consultando Catho...")
        
        # Termos otimizados
        search_terms = ["desenvolvedor-junior", "estagio-ti", "trainee-tecnologia"]
        
        for term in search_terms[:2]:  # Limitar a 2
            try:
                url = f"{self.base_url}/{term}/"
                response = requests.get(url, headers=self.headers, timeout=15)
                
                if response.status_code != 200:
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Catho usa cards de vaga
                # Seletores podem variar, tentar múltiplos
                job_cards = soup.select('article.sc-job-card, div.job-item, li.job')
                
                if not job_cards:
                    # Fallback: procurar links com /vaga/
                    job_links = soup.select('a[href*="/vaga/"]')
                    
                    for link in job_links[:20]:
                        try:
                            href = link.get('href', '')
                            if not href.startswith('http'):
                                href = f"https://www.catho.com.br{href}"
                            
                            title = link.get_text(strip=True)
                            if len(title) < 10:
                                continue
                            
                            # Filtro palavras-chave
                            if not any(kw in title.lower() for kw in ['junior', 'júnior', 'estagio', 'trainee', 'jr']):
                                continue
                            
                            job = {
                                "titulo": f"🟢 {title[:80]}",
                                "empresa": "Via Catho",
                                "localizacao": "Brasil",
                                "link": href,
                                "data_publicacao": datetime.now().strftime("%Y-%m-%d"),
                                "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "plataforma": self.platform
                            }
                            
                            all_jobs.append(job)
                            
                        except:
                            continue
                else:
                    # Parse job cards
                    for card in job_cards[:20]:
                        try:
                            title_elem = card.select_one('h2, h3, .job-title')
                            if not title_elem:
                                continue
                            
                            title = title_elem.get_text(strip=True)
                            
                            link_elem = card.select_one('a')
                            if not link_elem:
                                continue
                            
                            href = link_elem.get('href', '')
                            if not href.startswith('http'):
                                href = f"https://www.catho.com.br{href}"
                            
                            # Empresa
                            company_elem = card.select_one('.company, .empresa')
                            company = company_elem.get_text(strip=True) if company_elem else "Empresa"
                            
                            # Local
                            location_elem = card.select_one('.location, .local')
                            location = location_elem.get_text(strip=True) if location_elem else "Brasil"
                            
                            job = {
                                "titulo": f"🟢 {title[:80]}",
                                "empresa": company,
                                "localizacao": location,
                                "link": href,
                                "data_publicacao": datetime.now().strftime("%Y-%m-%d"),
                                "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "plataforma": self.platform
                            }
                            
                            all_jobs.append(job)
                            
                        except:
                            continue
            
            except Exception as e:
                print(f"  [!] Erro Catho: {e}")
                continue
        
        print(f"  [+] {len(all_jobs)} vagas encontradas no Catho")
        return all_jobs
