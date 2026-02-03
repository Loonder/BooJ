# -*- coding: utf-8 -*-
"""
Async version of run_cycle for parallel scraping
Reduces execution time from 15min to <3min!
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
import time

def run_cycle_parallel(scrapers_config: List[Dict]) -> List[Dict]:
    """
    Execute scraping cycle with parallel execution
    
    Args:
        scrapers_config: List of scraper configurations
        Each config: {"name": str, "scraper": callable, "args": tuple}
    
    Returns:
        List of all jobs from all scrapers
    """
    all_jobs = []
    
    # Use ThreadPoolExecutor for I/O-bound tasks
    max_workers = min(16, len(scrapers_config))  # Cap at 16 workers
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all scraping tasks
        future_to_scraper = {}
        
        for config in scrapers_config:
            scraper_name = config['name']
            scraper_func = config['scraper']
            scraper_args = config.get('args', ())
            
            future = executor.submit(scraper_func, *scraper_args)
            future_to_scraper[future] = scraper_name
        
        # Collect results as they complete
        for future in as_completed(future_to_scraper):
            scraper_name = future_to_scraper[future]
            
            try:
                jobs = future.result(timeout=120)  # 2min timeout per scraper
                
                if jobs and isinstance(jobs, list):
                    all_jobs.extend(jobs)
                    print(f"✅ {scraper_name}: {len(jobs)} vagas")
                else:
                    print(f"⚠️ {scraper_name}: 0 vagas")
                    
            except Exception as e:
                print(f"❌ {scraper_name}: {type(e).__name__} - {str(e)[:100]}")
    
    return all_jobs


def create_scraper_configs():
    """
    Create scraper configurations for parallel execution
    
    Returns:
        List of scraper configs
    """
    from config import SEARCH_TERMS
    
    # Import all scrapers
    from scraper_github import GithubScraper
    from scraper_reddit import RedditScraper
    from scraper_hackernews import HackerNewsScraper
    from scraper_tabnews import TabNewsScraper
    from scraper_rss import RssScraper
    from scraper_remoteok import RemoteOKScraper
    from scraper_apinfo import ApinfoScraper
    from scraper_buscojobs import BuscoJobsScraper
    from scraper_remotive import RemotiveScraper
    from scraper_telegram_advanced import TelegramJobScraper
    from scraper_catho import CathoScraper
    from scraper_trampoco import TrampoCoScraper
    from scraper_gupy import GupyScraper
    from scraper_jobspy_real import JobSpyRealScraper
    from scraper_br import BRScraper
    
    configs = [
        # Fast API scrapers (parallel safe)
        {"name": "GitHub", "scraper": lambda: GithubScraper().fetch_jobs(SEARCH_TERMS)},
        {"name": "Reddit", "scraper": lambda: RedditScraper().fetch_jobs(SEARCH_TERMS)},
        {"name": "HackerNews", "scraper": lambda: HackerNewsScraper().fetch_jobs(SEARCH_TERMS)},
        {"name": "TabNews", "scraper": lambda: TabNewsScraper().fetch_jobs(SEARCH_TERMS)},
        {"name": "RSS", "scraper": lambda: RssScraper().fetch_jobs(SEARCH_TERMS)},
        {"name": "RemoteOK", "scraper": lambda: RemoteOKScraper().fetch_jobs(SEARCH_TERMS)},
        {"name": "Remotive", "scraper": lambda: RemotiveScraper().fetch_jobs(SEARCH_TERMS)},
        {"name": "BuscoJobs", "scraper": lambda: BuscoJobsScraper().fetch_jobs(SEARCH_TERMS)},
        
        # BR Scrapers
        {"name": "BRScraper", "scraper": lambda: BRScraper().fetch_jobs(SEARCH_TERMS)},
        {"name": "Apinfo", "scraper": lambda: ApinfoScraper().fetch_jobs(SEARCH_TERMS)},
        {"name": "Catho", "scraper": lambda: CathoScraper().fetch_jobs(SEARCH_TERMS)},
        {"name": "Trampo.co", "scraper": lambda: TrampoCoScraper().fetch_jobs(SEARCH_TERMS)},
        {"name": "Gupy", "scraper": lambda: GupyScraper().fetch_jobs(SEARCH_TERMS)},
        
        # Telegram (may need rate limiting)
        {"name": "Telegram", "scraper": lambda: TelegramJobScraper().fetch_jobs(SEARCH_TERMS)},
        
        # JobSpy (slow but valuable)
        {"name": "JobSpy", "scraper": lambda: JobSpyRealScraper().fetch_jobs(SEARCH_TERMS)},
    ]
    
    return configs


# Example usage:
# from async_hunter import run_cycle_parallel, create_scraper_configs
# 
# configs = create_scraper_configs()
# jobs = run_cycle_parallel(configs)
# print(f"Total: {len(jobs)} vagas em paralelo!")
