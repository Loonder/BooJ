# -*- coding: utf-8 -*-
"""
Scraper para BuscoJobs (https://br.buscojobs.com/)
Site de vagas da América Latina
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
import time

class BuscoJobsScraper:
    def __init__(self):
        self.base_url = "https://br.buscojobs.com"
        self.platform = "BuscoJobs"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    
    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas no BuscoJobs baseado em termos de busca."""
        all_jobs = []
        print(f"\n[*] Consultando BuscoJobs...")
        
        # Termos padrão se não fornecidos
        if not terms:
            terms = ["estagio ti", "desenvolvedor junior", "programador junior"]
        
        try:
            for term in terms[:2]:  # Limitar a 2 termos para não sobrecarregar
                search_url = f"{self.base_url}/pesquisa?q={term.replace(' ', '+')}"
                
                try:
                    response = requests.get(search_url, headers=self.headers, timeout=15)
                    
                    if response.status_code != 200:
                        continue
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # BuscoJobs geralmente usa cards com class "job-card" ou similar
                    # Vamos procurar links de vagas (ajustar seletores conforme estrutura real)
                    job_cards = soup.select('article.job-item, div.job-card, a[href*="/trabalho/"]')
                    
                    for card in job_cards[:20]:  # Limitar primeiras 20 por busca
                        try:
                            # Tentar extrair título
                            title_elem = card.select_one('h2, h3, .job-title, .titulo')
                            if not title_elem:
                                title_elem = card.find('a') if card.name == 'div' else card
                            
                            title = title_elem.get_text(strip=True) if title_elem else "Vaga TI"
                            
                            # Extrair link
                            link_elem = card if card.name == 'a' else card.find('a')
                            if not link_elem or not link_elem.get('href'):
                                continue
                                
                            link = link_elem['href']
                            if not link.startswith('http'):
                                link = self.base_url + link
                            
                            # Empresa
                            company_elem = card.select_one('.company, .empresa, .company-name')
                            company = company_elem.get_text(strip=True) if company_elem else "Empresa via BuscoJobs"
                            
                            # Localização
                            location_elem = card.select_one('.location, .local, .cidade')
                            location = location_elem.get_text(strip=True) if location_elem else "América Latina"
                            
                            # Filtro básico para evitar duplicatas
                            if any(job['link'] == link for job in all_jobs):
                                continue
                            
                            job = {
                                "titulo": f"🌎 {title[:100]}",
                                "empresa": company,
                                "localizacao": location,
                                "link": link,
                                "data_publicacao": datetime.now().strftime("%Y-%m-%d"),
                                "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "plataforma": self.platform
                            }
                            
                            all_jobs.append(job)
                            
                        except Exception as e:
                            continue
                    
                    time.sleep(2)  # Delay entre buscas
                    
                except Exception as e:
                    print(f"  [!] Erro ao buscar '{term}': {e}")
                    continue
        
        except Exception as e:
            print(f"  [!] Erro BuscoJobs: {e}")
            return []
        
        print(f"  [+] {len(all_jobs)} vagas encontradas no BuscoJobs")
        return all_jobs
