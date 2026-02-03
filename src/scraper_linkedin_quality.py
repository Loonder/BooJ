# -*- coding: utf-8 -*-
"""
Scraper LinkedIn de QUALIDADE
Usa linkedin-jobs-scraper para vagas reais
"""

from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters
from datetime import datetime
from typing import List, Dict
import time

class LinkedInQualityScraper:
    """LinkedIn scraper com vagas reais e verificadas."""
    
    def __init__(self):
        self.platform = "LinkedIn"
        self.jobs_collected = []
        
    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas no LinkedIn."""
        all_jobs = []
        
        print(f"\n[*] Consultando LinkedIn (Quality)...")
        
        try:
            # Event handlers
            def on_data(data: EventData):
                """Callback quando vaga é encontrada."""
                try:
                    # Filtro básico: deve ter pelo menos título e link
                    if not data.title or not data.link:
                        return
                    
                    # Filtro de qualidade: júnior/estágio
                    title_lower = data.title.lower()
                    relevant_keywords = ['junior', 'júnior', 'jr', 'estágio', 'estagio', 'trainee', 'entry']
                    
                    if not any(kw in title_lower for kw in relevant_keywords):
                        return
                    
                    job = {
                        "titulo": f"💼 {data.title}",
                        "empresa": data.company or "Empresa",
                        "localizacao": data.location or "Brasil",
                        "link": data.link,
                        "data_publicacao": data.date or datetime.now().strftime("%Y-%m-%d"),
                        "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "plataforma": self.platform
                    }
                    
                    self.jobs_collected.append(job)
                    
                except Exception as e:
                    pass
            
            def on_error(error):
                print(f"  [!] Erro LinkedIn: {error}")
            
            def on_end():
                print(f"  [+] LinkedIn finalizado")
            
            # Configurar scraper
            scraper = LinkedinScraper(
                chrome_options=None,  # Headless
                headless=True,
                max_workers=1,
                slow_mo=0.5,
            )
            
            # Registrar eventos
            scraper.on(Events.DATA, on_data)
            scraper.on(Events.ERROR, on_error)
            scraper.on(Events.END, on_end)
            
            # Queries otimizadas para BR
            queries = [
                Query(
                    query='desenvolvedor junior',
                    options=QueryOptions(
                        locations=['Brasil'],
                        apply_link=True,
                        limit=30,
                        filters=QueryFilters(
                            relevance=RelevanceFilters.RECENT,
                            time=TimeFilters.MONTH,
                            type=[TypeFilters.FULL_TIME, TypeFilters.INTERNSHIP],
                            experience=[ExperienceLevelFilters.ENTRY_LEVEL, ExperienceLevelFilters.INTERNSHIP]
                        )
                    )
                ),
                Query(
                    query='estagio ti',
                    options=QueryOptions(
                        locations=['São Paulo', 'Rio de Janeiro'],
                        apply_link=True,
                        limit=30,
                        filters=QueryFilters(
                            time=TimeFilters.MONTH,
                            type=[TypeFilters.INTERNSHIP],
                        )
                    )
                ),
                Query(
                    query='trainee tecnologia',
                    options=QueryOptions(
                        locations=['Brasil'],
                        apply_link=True,
                        limit=20,
                        filters=QueryFilters(
                            time=TimeFilters.MONTH,
                        )
                    )
                ),
            ]
            
            # Rodar scraper
            self.jobs_collected = []
            scraper.run(queries)
            
            all_jobs = self.jobs_collected
            
        except Exception as e:
            print(f"  [!] Erro geral LinkedIn: {e}")
            return []
        
        print(f"  [+] {len(all_jobs)} vagas encontradas no LinkedIn")
        return all_jobs
