# -*- coding: utf-8 -*-
"""
Scraper para RemoteOK API - Vagas remotas internacionais.
API pública e gratuita.
"""

import requests
from datetime import datetime
from typing import List, Dict

class RemoteOKScraper:
    """Coleta vagas remotas via RemoteOK API."""

    def __init__(self):
        self.api_url = "https://remoteok.com/api"
        self.platform = "RemoteOK"

    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas remotas no RemoteOK."""
        all_jobs = []
        
        print(f"\n[*] Consultando RemoteOK API...")

        try:
            response = requests.get(
                self.api_url,
                timeout=15,
                headers={"User-Agent": "Mozilla/5.0 JobBot/1.0"}
            )
            
            if response.status_code != 200:
                print(f"  [!] RemoteOK retornou {response.status_code}")
                return []
            
            data = response.json()
            
            # Primeiro item é metadata, pular
            jobs_list = data[1:] if len(data) > 1 else []
            
            for job in jobs_list[:50]:  # Limitar a 50 vagas
                title = job.get("position", "")
                title_lower = title.lower()
                
                # Filtrar junior/intern/entry
                is_relevant = any(term in title_lower for term in 
                    ["junior", "jr", "intern", "entry", "graduate", "trainee", "associate"])
                
                # Também aceitar se tiver tags relevantes
                tags = job.get("tags", [])
                if isinstance(tags, list):
                    tags_str = " ".join(tags).lower()
                    if any(t in tags_str for t in ["junior", "entry", "intern"]):
                        is_relevant = True
                
                if is_relevant:
                    job_data = {
                        "titulo": f"🌍 {title}",
                        "empresa": job.get("company", "Empresa"),
                        "localizacao": "🏠 Remote Worldwide",
                        "link": job.get("url", ""),
                        "data_publicacao": job.get("date", "N/A")[:10] if job.get("date") else "N/A",
                        "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "plataforma": self.platform
                    }
                    all_jobs.append(job_data)
                    
        except Exception as e:
            print(f"  [!] Erro RemoteOK: {e}")
            return []
        
        print(f"  [+] {len(all_jobs)} vagas junior/entry encontradas no RemoteOK")
        return all_jobs
