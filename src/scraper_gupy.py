# -*- coding: utf-8 -*-
"""
Scraper para Gupy (Maior Plataforma de Recrutamento do Brasil)
Usa busca pública via HTML parsing (API é Enterprise-only)
"""

import requests
from datetime import datetime
from typing import List, Dict
from bs4 import BeautifulSoup
import re

class GupyScraper:
    """Scraper para Gupy - A MAIOR do Brasil."""
    
    def __init__(self):
        self.platform = "Gupy"
        self.search_url = "https://portal.gupy.io/job-search/term="
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    
    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas no Gupy via busca pública."""
        all_jobs = []
        
        print(f"\n[*] Consultando Gupy (Maior Plataforma BR)...")
        
        search_terms = terms or ["estagio ti", "desenvolvedor junior"]
        
        # Scrape career pages de empresas populares que usam Gupy
        career_pages = [
            "https://nubank.gupy.io",
            "https://ambev.gupy.io",
            "https://magazineluiza.gupy.io",
            "https://stone.gupy.io",
            "https://ifood.gupy.io",
            "https://mercadolivre.gupy.io",
            "https://itau.gupy.io",
            "https://bradesco.gupy.io",
            "https://santander.gupy.io",
            "https://totvs.gupy.io",
            "https://accenture.gupy.io",
            "https://sebrae.gupy.io"
        ]
        
        for page_url in career_pages:
            try:
                company = page_url.split("//")[1].split(".")[0].title()
                print(f"  [>] Consultando {company}...")
                
                response = requests.get(page_url, headers=self.headers, timeout=10)
                
                if response.status_code != 200:
                    continue
                
                # Parse JSON embedded in page (Gupy uses React with JSON state)
                html = response.text
                
                # Look for job data in script tags
                jobs_found = self._extract_jobs_from_html(html, company, page_url)
                all_jobs.extend(jobs_found)
                
            except Exception as e:
                print(f"  [!] Erro em {page_url}: {e}")
                continue
        
        # Dedupe by link
        seen_links = set()
        unique_jobs = []
        for job in all_jobs:
            if job['link'] not in seen_links:
                seen_links.add(job['link'])
                unique_jobs.append(job)
        
        print(f"  [+] {len(unique_jobs)} vagas encontradas no Gupy")
        return unique_jobs
    
    def _extract_jobs_from_html(self, html: str, company: str, base_url: str) -> List[Dict]:
        """Extrai vagas do HTML da página."""
        jobs = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Gupy uses data attributes with job info
            job_links = soup.find_all('a', href=True)
            
            for link in job_links:
                href = link.get('href', '')
                
                # Job links pattern: /job/12345 or full URL
                if '/job/' not in href:
                    continue
                
                # Get title from link text or aria-label
                title = link.get_text(strip=True)
                if not title or len(title) < 5:
                    title = link.get('aria-label', '')
                
                if not title or len(title) < 5:
                    continue
                
                # Filter for junior/estagio
                title_lower = title.lower()
                if not any(kw in title_lower for kw in ['junior', 'júnior', 'jr', 'estagio', 'estágio', 'trainee', 'aprendiz', 'iniciante']):
                    continue
                
                # Build full URL
                if href.startswith('/'):
                    job_url = base_url.rstrip('/') + href
                elif href.startswith('http'):
                    job_url = href
                else:
                    job_url = base_url.rstrip('/') + '/' + href
                
                job_data = {
                    "titulo": f"🟣 {title}",
                    "empresa": company,
                    "localizacao": "Brasil",
                    "link": job_url,
                    "data_publicacao": datetime.now().strftime("%Y-%m-%d"),
                    "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "plataforma": self.platform
                }
                
                jobs.append(job_data)
                
        except Exception as e:
            print(f"  [!] Erro parsing HTML: {e}")
        
        return jobs
