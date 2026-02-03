# -*- coding: utf-8 -*-
"""
Scraper para Vagas no GitHub (Issues).
Foca em repositórios da comunidade brasileira.
"""

import requests
import time
from datetime import datetime
from typing import List, Dict

from config import REQUEST_HEADERS, REQUEST_TIMEOUT, SEARCH_TERMS

# Repositórios mais ativos (reduzido para evitar rate limit)
# GitHub Search API: 10 req/min sem auth, 30 req/min com token
GITHUB_REPOS = [
    # Top 6 mais ativos (priorizados)
    "backend-br/vagas",
    "react-brasil/vagas",
    "vuejs-br/vagas",
    "pythonbrasil/vagas",
    "devopsbr/vagas",
    "datascience-br/vagas",
]

class GithubScraper:
    """Coleta vagas de Issues no GitHub."""

    def __init__(self):
        self.platform_base = "GitHub"
        self.api_url = "https://api.github.com/search/issues"
        self._request_count = 0
        self._last_request = 0

    def _rate_limit_wait(self):
        """Espera adequada para não bater rate limit (10 req/min sem auth)."""
        self._request_count += 1
        
        # A cada 8 requests, pausa mais longa
        if self._request_count >= 8:
            print(f"      [~] Pausa preventiva de rate limit (40s)...")
            time.sleep(40)
            self._request_count = 0
        else:
            # Delay base: 7s entre requests (10 req/min = 6s, +1s margem)
            elapsed = time.time() - self._last_request
            if elapsed < 7:
                time.sleep(7 - elapsed)
        
        self._last_request = time.time()

    def fetch_jobs(self) -> List[Dict]:
        """
        Busca issues abertas com termos de estágio nos repositórios selecionados.
        Usa a API de Search do GitHub para otimizar requisições.
        """
        all_jobs = []
        print(f"\n[*] Consultando GitHub Vagas (Brasil)...")

        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": REQUEST_HEADERS["User-Agent"]
        }

        target_labels = ["estagio", "estágio", "junior", "júnior", "trainee", "intern"]
        
        for repo in GITHUB_REPOS:
            print(f"  [>] Verificando {repo}...")
            
            # Query simplificada SEM aspas e SEM acentos (evita 422)
            # Busca issues abertas no repo com termos simples
            query = f'repo:{repo} state:open type:issue estagio OR junior OR trainee'
            
            params = {
                "q": query,
                "sort": "created",
                "order": "desc",
                "per_page": 15  # Reduzido para ser mais rápido
            }
            
            try:
                self._rate_limit_wait()
                
                response = requests.get(
                    self.api_url, 
                    params=params, 
                    headers=headers, 
                    timeout=REQUEST_TIMEOUT
                )
                
                if response.status_code == 403 or response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 60))
                    print(f"      [!] Rate limit (403/429). Esperando {retry_after}s...")
                    time.sleep(retry_after)
                    continue
                
                if response.status_code == 422:
                    # Tenta query ainda mais simples
                    simple_query = f'repo:{repo} state:open estagio'
                    params["q"] = simple_query
                    response = requests.get(
                        self.api_url, 
                        params=params, 
                        headers=headers, 
                        timeout=REQUEST_TIMEOUT
                    )
                    if response.status_code != 200:
                        print(f"      [!] Repo {repo} indisponível, pulando...")
                        continue

                response.raise_for_status()
                data = response.json()
                
                items = data.get("items", [])
                
                count = 0
                for item in items:
                    title = item.get("title", "").strip()
                    body = (item.get("body") or "").strip()
                    html_url = item.get("html_url")
                    created_at = item.get("created_at", "")
                    
                    # Verificação de validade
                    text_content = (title + " " + body).lower()
                    
                    is_valid = any(term in text_content for term in target_labels)
                    
                    if is_valid:
                        local = "Não informado"
                        # Extração de local entre colchetes [Local]
                        if "[" in title and "]" in title:
                            try:
                                start = title.find("[")
                                end = title.find("]")
                                if end > start:
                                    local = title[start+1:end]
                            except:
                                pass

                        job = {
                            "titulo": title,
                            "empresa": f"Via {repo}",
                            "localizacao": local,
                            "link": html_url,
                            "data_publicacao": created_at[:10],
                            "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "plataforma": f"GitHub ({repo.split('/')[0]})",
                        }
                        
                        all_jobs.append(job)
                        count += 1
                
                if count > 0:
                    print(f"      [+] {count} vagas encontradas")
                else:
                    print(f"      [.] Nenhuma vaga recente")

            except requests.exceptions.RequestException as e:
                print(f"      [!] Erro em {repo}: {type(e).__name__}")
            except Exception as e:
                print(f"      [!] Erro genérico: {e}")

        print(f"  [*] GitHub finalizado: {len(all_jobs)} vagas coletadas")
        return all_jobs

