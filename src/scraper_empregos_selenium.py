# -*- coding: utf-8 -*-
"""
Scraper SELENIUM para Empregos.com.br
Usa Selenium para lidar com JavaScript
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from typing import List, Dict
import time

class EmpregosSeleniumScraper:
    def __init__(self):
        self.base_url = "https://www.empregos.com.br"
        self.platform = "Empregos.com.br"
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
        """Busca vagas no Empregos.com.br via Selenium."""
        all_jobs = []
        
        print(f"\n[*] Consultando Empregos.com.br (Selenium)...")
        
        try:
            self._init_driver()
            
            # Buscar estágios
            search_urls = [
                f"{self.base_url}/vagas/estagio-ti",
                f"{self.base_url}/vagas/junior-desenvolvedor"
            ]
            
            for url in search_urls[:2]:
                try:
                    self.driver.get(url)
                    time.sleep(3)
                    
                    # Scroll
                    for _ in range(3):
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1)
                    
                    # Buscar vagas
                    job_cards = self.driver.find_elements(By.CSS_SELECTOR,
                        ".vaga, .job-item, .opportunity")
                    
                    if not job_cards:
                        job_cards = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/vaga/']")
                    
                    for card in job_cards[:30]:  # Mais vagas, site grande
                        try:
                            title = card.find_element(By.CSS_SELECTOR, "h3, h4, .title, .job-title").text
                            
                            link_elem = card.find_element(By.TAG_NAME, "a")
                            link = link_elem.get_attribute("href")
                            
                            if not link:
                                continue
                            
                            if not link.startswith("http"):
                                link = self.base_url + link
                            
                            try:
                                company = card.find_element(By.CSS_SELECTOR, ".company, .empresa").text
                            except:
                                company = "Empresa"
                            
                            try:
                                location = card.find_element(By.CSS_SELECTOR, ".location, .local").text
                            except:
                                location = "Brasil"
                            
                            job = {
                                "titulo": f"💼 {title[:100]}",
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
                    
                    time.sleep(2)  # Delay entre URLs
                    
                except Exception as e:
                    print(f"  [!] Erro: {e}")
                    continue
        
        except Exception as e:
            print(f"  [!] Erro Empregos Selenium: {e}")
        finally:
            if self.driver:
                self.driver.quit()
        
        print(f"  [+] {len(all_jobs)} vagas encontradas no Empregos.com.br")
        return all_jobs
