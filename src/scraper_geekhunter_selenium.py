# -*- coding: utf-8 -*-
"""
Scraper SELENIUM para GeekHunter
Usa Selenium para lidar com JavaScript
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from typing import List, Dict
import time

class GeekHunterSeleniumScraper:
    def __init__(self):
        self.base_url = "https://www.geekhunter.com.br/vagas"
        self.platform = "GeekHunter"
        self.driver = None
    
    def _init_driver(self):
        """Inicializa driver Selenium headless."""
        options = Options()
        options.add_argument('--headless')  # Rodar sem abrir janela
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        self.driver = webdriver.Chrome(options=options)
    
    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas no GeekHunter via Selenium."""
        all_jobs = []
        
        print(f"\n[*] Consultando GeekHunter (Selenium)...")
        
        try:
            self._init_driver()
            
            # Buscar vagas júnior/estágio
            search_terms = ["junior", "estagio"]
            
            for term in search_terms[:1]:  # Apenas 1 busca para não demorar
                try:
                    url = f"{self.base_url}?q={term}"
                    self.driver.get(url)
                    
                    # Aguardar vagas carregarem
                    time.sleep(3)
                    
                    # Scroll para carregar mais vagas (lazy loading)
                    for _ in range(2):
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1)
                    
                    # Buscar cards de vagas (ajustar seletores conforme site real)
                    job_cards = self.driver.find_elements(By.CSS_SELECTOR, 
                        ".job-card, .vaga-card, [data-testid='job-card'], article")
                    
                    if not job_cards:
                        # Fallback: tentar outros seletores
                        job_cards = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/vaga/']")
                    
                    for card in job_cards[:15]:  # Limitar a 15
                        try:
                            # Extrair dados
                            title = card.find_element(By.CSS_SELECTOR, "h2, h3, .title").text
                            
                            # Link
                            link_elem = card.find_element(By.TAG_NAME, "a")
                            link = link_elem.get_attribute("href")
                            
                            if not link or "geekhunter.com.br" not in link:
                                continue
                            
                            # Empresa (opcional, pode não ter)
                            try:
                                company = card.find_element(By.CSS_SELECTOR, ".company, .empresa").text
                            except:
                                company = "Empresa via GeekHunter"
                            
                            # Localização
                            try:
                                location = card.find_element(By.CSS_SELECTOR, ".location, .local").text
                            except:
                                location = "Brasil"
                            
                            job = {
                                "titulo": f"🎯 {title[:100]}",
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
                    print(f"  [!] Erro na busca '{term}': {e}")
                    continue
        
        except Exception as e:
            print(f"  [!] Erro GeekHunter Selenium: {e}")
        finally:
            if self.driver:
                self.driver.quit()
        
        print(f"  [+] {len(all_jobs)} vagas encontradas no GeekHunter")
        return all_jobs
