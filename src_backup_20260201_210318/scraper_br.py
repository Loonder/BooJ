# -*- coding: utf-8 -*-
"""
Scraper para sites brasileiros de vagas em TI.
Usa BeautifulSoup para parsing leve (sem Selenium).
Fontes: Programathor, APINFO.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict

class BRScraper:
    """Coleta vagas do Programathor e APINFO."""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca em todas as fontes BR suportadas."""
        jobs = []
        jobs.extend(self._fetch_programathor())
        # APINFO é mais complexo devido ao layout antigo, focando no Programathor primeiro
        return jobs

    def _fetch_programathor(self) -> List[Dict]:
        """Busca vagas de estágio no Programathor."""
        print("\n[*] Consultando Programathor...")
        jobs = []
        url = "https://programathor.com.br/jobs-city/estagio"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                print(f"  [!] Programathor retornou {response.status_code}")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            # Vagas estão em divs com class 'cell-list'
            job_cards = soup.find_all("div", class_="cell-list")
            
            for card in job_cards:
                try:
                    title_elem = card.find("h3")
                    if not title_elem: continue
                    
                    title = title_elem.get_text(strip=True)
                    link = "https://programathor.com.br" + card.find("a")["href"]
                    
                    # Detalhes (Empresa, Local)
                    details = card.find_all("span")
                    company = "Confidencial"
                    location = "Brasil"
                    
                    if len(details) > 0:
                        company = details[0].get_text(strip=True)
                    if len(details) > 1:
                        location = details[1].get_text(strip=True)
                        
                    # Tags de tech
                    tags = []
                    tag_elems = card.find_all("span", class_="tag")
                    for t in tag_elems:
                        tags.append(t.get_text(strip=True))
                    
                    tech_stack = ", ".join(tags)
                    full_title = f"{title} [{tech_stack}]"
                    
                    # Padronizar local
                    loc_std = "🇧🇷 Brasil"
                    loc_lower = location.lower()
                    if "remoto" in loc_lower: loc_std = "🏠 Remoto"
                    elif "paulo" in loc_lower: loc_std = "📍 SP"
                    elif "rio" in loc_lower: loc_std = "📍 RJ"
                    
                    jobs.append({
                        "titulo": f"🚀 {full_title[:100]}",
                        "empresa": company,
                        "localizacao": loc_std,
                        "link": link,
                        "data_publicacao": datetime.now().strftime("%Y-%m-%d"), # Site não mostra data fácil
                        "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "plataforma": "Programathor"
                    })
                    
                except Exception:
                    continue
                    
            print(f"  [+] {len(jobs)} vagas encontradas no Programathor")
            
        except Exception as e:
            print(f"  [!] Erro Programathor: {e}")
            
        return jobs
