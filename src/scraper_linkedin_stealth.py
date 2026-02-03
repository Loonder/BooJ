# -*- coding: utf-8 -*-
"""
Scraper STEALTH para LinkedIn
Usa undetected-chromedriver para evitar detecção
"""

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from typing import List, Dict
import time
import os

class LinkedInStealthScraper:
    def __init__(self):
        self.email = os.getenv("LINKEDIN_EMAIL", "")
        self.password = os.getenv("LINKEDIN_PASSWORD", "")
        self.platform = "LinkedIn"
        self.driver = None
    
    def _init_driver(self):
        """Inicializa driver stealth."""
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        
        # Headless optional (mais stealth sem headless)
        # options.add_argument('--headless')
        
        self.driver = uc.Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    def _login(self):
        """Login no LinkedIn."""
        try:
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(2)
            
            # Email
            email_field = self.driver.find_element(By.ID, "username")
            email_field.send_keys(self.email)
            
            # Password
            pass_field = self.driver.find_element(By.ID, "password")
            pass_field.send_keys(self.password)
            
            # Submit
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_btn.click()
            
            time.sleep(5)  # Aguardar login
            
            # Verificar se logou
            if "feed" in self.driver.current_url or "jobs" in self.driver.current_url:
                print("  [+] Login no LinkedIn OK!")
                return True
            else:
                print("  [!] Login falhou - pode precisar de verificação manual")
                return False
                
        except Exception as e:
            print(f"  [!] Erro no login: {e}")
            return False
    
    def fetch_jobs(self, terms: List[str] = None) -> List[Dict]:
        """Busca vagas no LinkedIn."""
        
        if not self.email or not self.password:
            print(f"\n[*] LinkedIn: Credenciais não configuradas no .env")
            return []
        
        all_jobs = []
        
        print(f"\n[*] Consultando LinkedIn (STEALTH MODE)...")
        
        try:
            self._init_driver()
            
            # Login
            if not self._login():
                return []
            
            # Buscar vagas
            search_terms = [
                "estágio tecnologia",
                "desenvolvedor júnior",
                "estagiário programação"
            ]
            
            for query in search_terms[:2]:  # Limitar a 2 buscas
                try:
                    # URL de busca de vagas
                    search_url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location=Brasil&f_TPR=r86400&f_E=2"  # r86400 = últimas 24h, f_E=2 = Entry level
                    
                    self.driver.get(search_url)
                    time.sleep(3)
                    
                    # Scroll para carregar vagas
                    for _ in range(3):
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1)
                    
                    # Pegar cards de vagas
                    job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".job-search-card")
                    
                    for card in job_cards[:20]:  # Limitar a 20 por busca
                        try:
                            title = card.find_element(By.CSS_SELECTOR, ".job-search-card__title").text
                            company = card.find_element(By.CSS_SELECTOR, ".job-search-card__company-name").text
                            location = card.find_element(By.CSS_SELECTOR, ".job-search-card__location").text
                            link = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                            
                            # Limpar link (remover tracking)
                            if "?" in link:
                                link = link.split("?")[0]
                            
                            job = {
                                "titulo": f"🔗 {title}",
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
                    
                    time.sleep(2)  # Delay entre buscas
                    
                except Exception as e:
                    print(f"  [!] Erro na busca '{query}': {e}")
                    continue
            
        except Exception as e:
            print(f"  [!] Erro LinkedIn: {e}")
        finally:
            if self.driver:
                self.driver.quit()
        
        print(f"  [+] {len(all_jobs)} vagas encontradas no LinkedIn")
        return all_jobs
