# -*- coding: utf-8 -*-
"""
Scraper SELENIUM para Trampos.co
Usa Selenium para lidar com JavaScript
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from typing import List, Dict
import time

class TramposSeleniumScraper:
    def __init__(self):
        self.base_url = "https://trampos.co/oportunidades"
        self.platform = "Trampos.co"
        self.driver = None
    
    def _init_driver(self):
        """Inicializa driver Selenium headless."""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        self.driver = webdriver.Chrome(options=options)
    
    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas no Trampos.co via Selenium."""
        all_jobs = []
        
        print(f"\n[*] Consultando Trampos.co (Selenium)...")
        
        try:
            self._init_driver()
            
            # Buscar por categoria tecnologia
            urls = [
                f"{self.base_url}?category=tecnologia",
                f"{self.base_url}?q=desenvolvedor+junior"
            ]
            
            for url in urls[:1]:  # Apenas 1 URL
                try:
                    self.driver.get(url)
                    time.sleep(3)
                    
                    # Scroll
                    for _ in range(2):
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1)
                    
                    # Buscar vagas
                    job_cards = self.driver.find_elements(By.CSS_SELECTOR,
                        ".opportunity-card, .job-card, article")
                    
                    if not job_cards:
                        job_cards = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/oportunidade/']")
                    
                    for card in job_cards[:20]:
                        try:
                            title = card.find_element(By.CSS_SELECTOR, "h2, h3, .title").text
                            
                            link_elem = card.find_element(By.TAG_NAME, "a")
                            link = link_elem.get_attribute("href")
                            
                            if not link or "trampos.co" not in link:
                                continue
                            
                            # Filtro tech
                            title_lower = title.lower()
                            tech_keywords = ['dev', 'programador', 'tech', 'ti', 'software', 
                                           'júnior', 'junior', 'estágio', 'estagio']
                            
                            if not any(kw in title_lower for kw in tech_keywords):
                                continue
                            
                            try:
                                company = card.find_element(By.CSS_SELECTOR, ".company").text
                            except:
                                company = "Startup"
                            
                            try:
                                location = card.find_element(By.CSS_SELECTOR, ".location").text
                            except:
                                location = "Brasil"
                            
                            job = {
                                "titulo": f"🚀 {title[:100]}",
                                "empresa": company,
                                "localizacao": location,
                                "link": link,
                                "data_publicacao": datetime.now().strftime("%Y-%m-%d"),
                                "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "plataforma": self.platform
                            }
                            
                            all_jobs.append(job)
                            
                        except Exception:
                            continue
                
                except Exception as e:
                    print(f"  [!] Erro: {e}")
                    continue
        
        except Exception as e:
            print(f"  [!] Erro Trampos Selenium: {e}")
        finally:
            if self.driver:
                self.driver.quit()
        
        print(f"  [+] {len(all_jobs)} vagas encontradas no Trampos.co")
        return all_jobs
