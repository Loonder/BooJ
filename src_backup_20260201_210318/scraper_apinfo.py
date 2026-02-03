# -*- coding: utf-8 -*-
"""
Scraper para Apinfo.com (HTML Legado)
Site antigo de vagas de TI no Brasil.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
import re

class ApinfoScraper:
    """Coleta vagas do Apinfo (Layout Tabela Antiga)."""

    def __init__(self):
        self.url = "https://www.apinfo.com/apinfo/inc/list.cfm"
        self.platform = "Apinfo"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Lê o listão do Apinfo e tenta extrair vagas relevantes."""
        all_jobs = []
        print(f"\n[*] Consultando Apinfo...")

        try:
            # Apinfo aceita POST com filtros, mas list.cfm geralmente mostra as últimas.
            # Vamos pegar a home da lista que traz tudo recente.
            response = requests.get(self.url, headers=self.headers, timeout=20)
            response.encoding = 'latin-1' # Site antigo costuma ser latin-1 ou ISO-8859-1
            
            if response.status_code != 200:
                print(f"  [!] Apinfo retornou {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # O layout do Apinfo é baseado em tabelas.
            # Geralmente as vagas estão dentro de um 'div class=box-vagas' ou tabela direta.
            # Estratégia: Procurar links que contêm 'click.cfm' ou 'detalhe'
            
            # Os links das vagas costumam ser: https://www.apinfo.com/apinfo/inc/u.cfm?id=...
            
            # Vamos buscar todos os blocos de texto que pareçam vagas
            # Geralmente estão em <div class="ch"> (cabeçalho?) ou <div class="d"> (descrição)
            # Mas mudou recentemente. Vamos buscar links diretos de vaga.
            
            # Link pattern: u.cfm?id=XXXX
            job_links = soup.select("a[href*='u.cfm?id=']")
            
            seen_ids = set()
            
            for link_elem in job_links:
                try:
                    url_suffix = link_elem.get("href")
                    if not url_suffix: continue
                    
                    full_link = f"https://www.apinfo.com/apinfo/inc/{url_suffix}"
                    
                    # Dedupe por URL
                    if full_link in seen_ids: continue
                    seen_ids.add(full_link)
                    
                    # O Texto do link geralmente é o cargo/skill
                    cargo = link_elem.get_text(strip=True)
                    
                    # Às vezes o texto é curto, e a descrição está no parent ou sibling
                    # Estrutura típica: Cod. X - Cargo - Empresa - Local
                    
                    # Filtro de keywords
                    full_text_lower = cargo.lower()
                    
                    # Se o texto do link for muito curto (ex: "SP"), pegar o texto da linha inteira pai
                    parent_text = link_elem.parent.get_text(" ", strip=True) if link_elem.parent else ""
                    if len(cargo) < 5:
                        full_text_lower = parent_text.lower()
                        cargo = parent_text[:100] # Truncar título
                    
                    # Keywords
                    is_relevant = any(k in full_text_lower for k in ["estágio", "estagio", "trainee", "junior", "jr", "iniciante"])
                    
                    # Tech keywords (opcional, para não pegar vaga de senior se não tiver junior explicito)
                    # Apinfo tem muita vaga senior.
                    is_tech = any(k in full_text_lower for k in ["python", "javascript", "node", "java", "php", "c#", ".net", "react", "sql", "suporte"])
                    
                    if is_relevant and is_tech:
                        # Extrair local
                        local = "Brasil"
                        if "sp" in full_text_lower or "paulo" in full_text_lower: local = "📍 SP"
                        elif "remoto" in full_text_lower or "home" in full_text_lower: local = "🏠 Remoto"
                        
                        # Empresa geralmente não está clara no link listagem, assume Confidencial ou extrai do texto
                        # Ex: "Empresa XPTO contrata Estagiário..."
                        
                        job = {
                            "titulo": f"💾 {cargo}",
                            "empresa": "Apinfo User",
                            "localizacao": local,
                            "link": full_link,
                            "data_publicacao": datetime.now().strftime("%Y-%m-%d"),
                            "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "plataforma": self.platform
                        }
                        
                        all_jobs.append(job)
                        
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"  [!] Erro Apinfo: {e}")
            return []
            
        print(f"  [+] {len(all_jobs)} vagas encontradas no Apinfo")
        return all_jobs
