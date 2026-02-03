# -*- coding: utf-8 -*-
"""
Scraper para Indeed Brasil (API Oficial)
Usa biblioteca indeed-python da Indeed Labs
"""

from indeed import IndeedClient
from datetime import datetime
from typing import List, Dict

class IndeedBrasilScraper:
    """Scraper Indeed usando API oficial."""
    
    def __init__(self):
        self.platform = "Indeed"
        self.client = IndeedClient(publisher_id='test')  # Publisher ID público para testes
        
    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas no Indeed Brasil."""
        all_jobs = []
        
        print(f"\n[*] Consultando Indeed Brasil (API)...")
        
        try:
            # Queries otimizadas para BR
            queries = [
                "desenvolvedor junior",
                "estagio ti",
                "trainee tecnologia"
            ]
            
            for query in queries[:2]:  # Limitar a 2
                try:
                    # Buscar vagas
                    params = {
                        'q': query,
                        'l': 'Brasil',
                        'co': 'br',  # Brasil
                        'limit': 25,
                        'fromage': 14,  # Últimos 14 dias
                        'jt': 'fulltime,internship',
                    }
                    
                    results = self.client.search(**params)
                    
                    if not results or 'results' not in results:
                        continue
                    
                    for job in results['results']:
                        try:
                            job_data = {
                                "titulo": f"🔵 {job.get('jobtitle', 'Vaga')}",
                                "empresa": job.get('company', 'Empresa'),
                                "localizacao": job.get('formattedLocation', 'Brasil'),
                                "link": job.get('url', ''),
                                "data_publicacao": job.get('date', datetime.now().strftime("%Y-%m-%d")),
                                "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "plataforma": self.platform
                            }
                            
                            # Filtro mínimo
                            if not job_data['link']:
                                continue
                            
                            all_jobs.append(job_data)
                            
                        except:
                            continue
                
                except Exception as e:
                    print(f"  [!] Erro query '{query}': {e}")
                    continue
                    
        except Exception as e:
            print(f"  [!] Erro geral Indeed: {e}")
        
        print(f"  [+] {len(all_jobs)} vagas encontradas no Indeed")
        return all_jobs
