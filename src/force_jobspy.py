
import logging
import sys
import os

# Setup paths
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scraper_jobspy_real import JobSpyRealScraper
from database import JobDatabase

# Logging config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ForceJobSpy")

def main():
    print("🚀 Iniciando busca forçada no JobSpy (LinkedIn/Indeed/Glassdoor)...")
    
    scraper = JobSpyRealScraper()
    # Termos de busca (pode vir de config, mas vou hardcode pra teste rapido)
    terms = ["Node.js", "Java", "Suporte TI", "Infraestrutura"] 
    
    all_jobs = []
    try:
        jobs = scraper.fetch_jobs(terms)
        all_jobs.extend(jobs)
        print(f"✅ JobSpy encontrou {len(jobs)} vagas!")
    except Exception as e:
        print(f"❌ Erro no JobSpy: {e}")

    if all_jobs:
        db = JobDatabase()
        count = db.add_jobs_batch(all_jobs)
        print(f"💾 {count} vagas salvas no banco de dados!")
    else:
        print("⚠️ Nenhuma vaga encontrada nesta tentativa.")

if __name__ == "__main__":
    main()
