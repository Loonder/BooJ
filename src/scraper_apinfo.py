# -*- coding: utf-8 -*-
"""
Scraper para Apinfo.com (HTML Legado) - ATUALIZADO
Site antigo de vagas de TI no Brasil.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict

class ApinfoScraper:
    """Coleta vagas do Apinfo (Layout Tabela Antiga)."""

    def __init__(self):
        self.url = "https://www.apinfo.com/apinfo/inc/list4.cfm"
        self.platform = "Apinfo"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Lê o listão do Apinfo e tenta extrair vagas relevantes."""
        all_jobs = []
        print(f"\n[*] Consultando Apinfo...")

        try:
            response = requests.get(self.url, headers=self.headers, timeout=20)
            response.encoding = 'latin-1' 
            
            if response.status_code != 200:
                print(f"  [!] Apinfo retornou {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # NOVA ABORDAGEM: Pegar TODOS os links e filtrar por conteúdo
            all_links = soup.find_all('a')
            
            seen_urls = set()
            
            for link_elem in all_links:
                try:
                    href = link_elem.get("href", "")
                    if not href:
                        continue
                    
                    # Garantir URL completa
                    if href.startswith('/'):
                        full_link = f"https://www.apinfo.com{href}"
                    elif href.startswith('http'):
                        full_link = href
                    else:
                        full_link = f"https://www.apinfo.com/apinfo/inc/{href}"
                    
                    # Dedupe
                    if full_link in seen_urls:
                        continue
                    
                    # Pegar texto do link
                    link_text = link_elem.get_text(strip=True)
                    
                    # Se texto muito curto, pegar contexto do pai
                    parent_text = ""
                    if len(link_text) < 10 and link_elem.parent:
                        parent_text = link_elem.parent.get_text(" ", strip=True)
                    
                    full_text = f"{link_text} {parent_text}".lower()
                    
                    # FILTROS: Deve conter pelo menos uma keyword relevante
                    relevant_keywords = [
                        "estágio", "estagio", "trainee", "junior", "júnior", 
                        "jr", "iniciante", "vaga", "oportunidade"
                    ]
                    
                    tech_keywords = [
                        "python", "javascript", "java", "php", "c#", ".net", 
                        "react", "node", "sql", "desenvolvedor", "programador",
                        "ti", "tecnologia", "suporte", "analista"
                    ]
                    
                    is_relevant = any(kw in full_text for kw in relevant_keywords)
                    is_tech = any(kw in full_text for kw in tech_keywords)
                    
                    # Filtrar links que não sejam de vagas (ex: navegação)
                    skip_keywords = ["home", "login", "cadastro", "sobre", "contato", "menu"]
                    should_skip = any(kw in full_text for kw in skip_keywords) and len(full_text) < 50
                    
                    if (is_relevant or is_tech) and not should_skip and len(full_text) > 15:
                        seen_urls.add(full_link)
                        
                        # Extrair localização
                        local = "Brasil"
                        if "sp" in full_text or "paulo" in full_text:
                            local = "📍 SP"
                        elif "remoto" in full_text or "home office" in full_text:
                            local = "🏠 REMOTO"
                        elif "rj" in full_text or "rio de janeiro" in full_text:
                            local = "📍 RJ"
                        
                        # Título
                        title = link_text if len(link_text) > 10 else parent_text
                        title = title[:100]  # Truncar
                        
                        if not title or len(title) < 5:
                            continue
                        
                        job = {
                            "titulo": f"💾 {title}",
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
