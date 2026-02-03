# -*- coding: utf-8 -*-
"""
Scraper para Reddit - Vagas de subreddits de emprego.
100% grátis - usa endpoint .json público.
"""

import requests
from datetime import datetime
from typing import List, Dict

class RedditScraper:
    """Coleta vagas de subreddits de emprego."""

    def __init__(self):
        self.platform = "Reddit"
        self.subreddits = [
            "forhire",          # Freelance/jobs
            "remotejs",         # Remote JS jobs
            "remotepython",     # Remote Python
            "techjobs",         # Tech jobs
            "jobopenings",      # General openings
        ]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (BooJ JobBot/1.0)"
        }

    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas em subreddits."""
        all_jobs = []
        seen_ids = set()
        
        print(f"\n[*] Consultando Reddit ({len(self.subreddits)} subreddits)...")

        for sub in self.subreddits:
            try:
                # Reddit expõe JSON público sem auth
                url = f"https://www.reddit.com/r/{sub}/new.json?limit=25"
                
                response = requests.get(url, headers=self.headers, timeout=15)
                
                if response.status_code != 200:
                    continue
                
                data = response.json()
                posts = data.get("data", {}).get("children", [])
                
                for post in posts:
                    post_data = post.get("data", {})
                    post_id = post_data.get("id")
                    
                    if post_id in seen_ids:
                        continue
                    seen_ids.add(post_id)
                    
                    title = post_data.get("title", "")
                    title_lower = title.lower()
                    selftext = post_data.get("selftext", "").lower()
                    
                    # Filtrar por termos de estágio/junior
                    search_text = f"{title_lower} {selftext}"
                    is_relevant = any(term in search_text for term in 
                        ["junior", "jr", "intern", "entry", "graduate", "trainee", 
                         "estágio", "estagio", "entry-level", "beginner"])
                    
                    # Também aceitar se mencionar hiring/remote
                    is_hiring = "[hiring]" in title_lower or "looking for" in title_lower
                    
                    if is_relevant or is_hiring:
                        # Extrair flair como localização
                        flair = post_data.get("link_flair_text", "Remote")
                        
                        job_data = {
                            "titulo": f"📱 {title[:100]}",
                            "empresa": f"r/{sub}",
                            "localizacao": flair if flair else "Remote",
                            "link": f"https://reddit.com{post_data.get('permalink', '')}",
                            "data_publicacao": datetime.fromtimestamp(
                                post_data.get("created_utc", 0)
                            ).strftime("%Y-%m-%d"),
                            "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "plataforma": f"Reddit ({sub})"
                        }
                        all_jobs.append(job_data)
                        
            except Exception as e:
                continue
        
        print(f"  [+] {len(all_jobs)} vagas encontradas no Reddit")
        return all_jobs
