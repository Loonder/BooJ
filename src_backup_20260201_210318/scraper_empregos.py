# -*- coding: utf-8 -*-
"""
Scraper para Empregos.com.br
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
from config import REQUEST_HEADERS

class EmpregosScraper:
    """Coleta vagas do Empregos.com.br"""

    def __init__(self):
        self.base_url = "https://www.empregos.com.br/vagas/estagio"
        self.domain = "https://www.empregos.com.br"
        self.platform = "Empregos.com.br"

    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas de estágio"""
        all_jobs = []
        print(f"\n[*] Consultando Empregos.com.br...")

        # URL de busca: https://www.empregos.com.br/vagas/estagio-em-tecnologia-da-informacao/sao-paulo/sp
        # Vamos usar uma busca mais genérica: 'estagio ti' na busca de texto se possível, ou categorias.
        # A URL de busca textual é: https://www.empregos.com.br/vagas?vaga=estagio+ti
        
        search_urls = [
            "https://www.empregos.com.br/vagas?vaga=estagio+tecnologia",
            "https://www.empregos.com.br/vagas?vaga=estagio+programacao",
            "https://www.empregos.com.br/vagas?vaga=estagio+ti"
        ]

        seen_links = set()

        for url in search_urls:
            try:
                response = requests.get(url, headers=REQUEST_HEADERS, timeout=15)
                if response.status_code != 200:
                    print(f"      [!] Erro {response.status_code} em {url}")
                    continue

                soup = BeautifulSoup(response.text, "html.parser")
                
                # Seletores podem variar, tentando o padrão comum
                # Geralmente lista de vagas é <ul> com <li> ou divs com class 'vaga'
                
                # Tentativa 1: Procurar cards de vaga
                cards = soup.find_all("div", class_="vaga")  # Exemplo genérico
                if not cards:
                    cards = soup.find_all("li", class_="vaga") # Outro comum
                
                # Se não achar por classe vaga, tentar estrutura de listagem
                if not cards:
                    # Tentar encontrar links de vagas
                    # Geralmente href contém '/vaga/'
                    pass

                # Empregos.com.br costuma usar <div class="item-vaga"> ou similar
                # Vamos tentar ser mais abrangentes: Listar elementos que parecem vagas
                possible_cards = soup.select(".vaga, .item-vaga, .box-vaga")
                
                count = 0
                for card in possible_cards:
                    try:
                        title_elem = card.select_one("h2, h3, .titulo-vaga")
                        if not title_elem:
                            continue
                        
                        title = title_elem.get_text(strip=True)
                        
                        link_elem = card.select_one("a")
                        if not link_elem:
                            continue
                            
                        link = link_elem.get("href")
                        if not link.startswith("http"):
                            link = self.domain + link
                            
                        if link in seen_links:
                            continue
                        seen_links.add(link)

                        company_elem = card.select_one(".nome-empresa, .empresa")
                        company = company_elem.get_text(strip=True) if company_elem else "Confidencial"
                        
                        loc_elem = card.select_one(".cidade-estado, .local")
                        location = loc_elem.get_text(strip=True) if loc_elem else "Brasil"
                        
                        # Data muitas vezes não está explícita ou é "Há x dias"
                        date_elem = card.select_one(".publicado, .data")
                        date_text = date_elem.get_text(strip=True) if date_elem else "Recente"

                        job = {
                            "titulo": title,
                            "empresa": company,
                            "localizacao": location,
                            "link": link,
                            "data_publicacao": date_text, # Pode precisar de tratamento
                            "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "plataforma": self.platform
                        }
                        
                        # Filtrar relevancia
                        if any(x in title.lower() for x in ["estágio", "estagio", "trainee", "junior", "jr"]):
                             all_jobs.append(job)
                             count += 1
                             
                    except Exception as e:
                        continue

                # Fallback se não achou nada com seletores de classe:
                # Buscar todos Links que contem 'vaga' e tentar extrair info
                if count == 0:
                     # Fallback logic could go here, but kept simple for now
                     pass

            except Exception as e:
                print(f"      [!] Erro ao processar Empregos.com.br: {e}")
                
        print(f"  [+] {len(all_jobs)} vagas únicas encontradas no Empregos.com.br")
        return all_jobs
