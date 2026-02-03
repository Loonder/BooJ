# -*- coding: utf-8 -*-
"""
Scraper para TabNews.com.br (Via API)
Comunidade de TI com vagas de alta qualidade.
"""

import requests
from datetime import datetime
from typing import List, Dict

class TabNewsScraper:
    def __init__(self):
        self.url = "https://www.tabnews.com.br/api/v1/contents"
        self.platform = "TabNews"
    
    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Consulta API do TabNews buscando posts recentes sobre vagas."""
        all_jobs = []
        print(f"\n[*] Consultando TabNews...")
        
        # Estratégia: Buscar nas 'relevantes' ou 'new' e filtrar por palavras-chave
        # A API permite paginação. Vamos pegar as primeiras 2 páginas (aprox 60 items)
        
        try:
            for page in range(1, 3):
                params = {"strategy": "new", "page": page, "per_page": 50}
                response = requests.get(self.url, params=params, timeout=10)
                
                if response.status_code != 200:
                    continue
                    
                posts = response.json()
                
                for post in posts:
                    title = post.get("title", "")
                    body = post.get("body", "") # As vezes vazio na listagem
                    slug = post.get("slug", "")
                    owner = post.get("owner_username", "")
                    
                    full_text = (title + " " + slug).lower()
                    
                    # Keywords para identificar vagas
                    is_job = any(k in full_text for k in ["vaga", "oportunidade", "contratando", "remoto", "estágio", "estagio", "junior", "jr", "trainee"])
                    
                    # Se não tiver cara de vaga, pula
                    if not is_job:
                        continue
                        
                    # Filtrar por termos de TI (opcional, pois TabNews já é TI)
                    # Mas garante que não é "Dúvida sobre vaga"
                    
                    link = f"https://www.tabnews.com.br/{owner}/{slug}"
                    
                    # Tentar inferir local
                    local = "Brasil/Remoto"
                    if "remoto" in full_text: local = "🏠 Remoto"
                    elif "sp" in full_text or "paulo" in full_text: local = "📍 SP"
                    
                    job = {
                        "titulo": f"📑 {title}",
                        "empresa": f"TabNews ({owner})",
                        "localizacao": local,
                        "link": link,
                        "data_publicacao": datetime.now().strftime("%Y-%m-%d"),
                        "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "plataforma": self.platform
                    }
                    
                    all_jobs.append(job)
        
        except Exception as e:
            print(f"  [!] Erro TabNews: {e}")
            return []

        print(f"  [+] {len(all_jobs)} vagas encontradas no TabNews")
        return all_jobs
