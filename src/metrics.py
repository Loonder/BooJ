# -*- coding: utf-8 -*-
"""
Prometheus metrics for monitoring JobPulse performance
"""

from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Metrics definitions

# Jobs scraped counter (by source)
jobs_scraped_total = Counter(
    'jobs_scraped_total',
    'Total number of jobs scraped',
    ['source']
)

# Scraping duration histogram (by source)
scrape_duration_seconds = Histogram(
    'scrape_duration_seconds',
    'Time spent scraping jobs from a source',
    ['source'],
    buckets=(0.5, 1, 2.5, 5, 10, 30, 60, 120, 300)
)

# Scraping errors counter (by source)
scrape_errors_total = Counter(
    'scrape_errors_total',
    'Total number of scraping errors',
    ['source', 'error_type']
)

# Active jobs in database
active_jobs_gauge = Gauge(
    'active_jobs_total',
    'Current number of jobs in database'
)

# Jobs filtered out
jobs_filtered_total = Counter(
    'jobs_filtered_total',
    'Total jobs filtered out',
    ['reason']
)

# Cycle duration
cycle_duration_seconds = Histogram(
    'cycle_duration_seconds',
    'Total time to complete one scraping cycle',
    buckets=(60, 120, 300, 600, 900, 1800)
)

# New jobs added per cycle
new_jobs_per_cycle = Histogram(
    'new_jobs_per_cycle',
    'Number of new (non-duplicate) jobs added per cycle',
    buckets=(0, 10, 50, 100, 200, 500, 1000)
)


class MetricsTracker:
    """Helper class to track metrics with context manager"""
    
    def __init__(self, source: str):
        self.source = source
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        scrape_duration_seconds.labels(source=self.source).observe(duration)
        
        if exc_type is not None:
            # Record error
            error_type = exc_type.__name__
            scrape_errors_total.labels(
                source=self.source,
                error_type=error_type
            ).inc()
        
        return False  # Don't suppress exceptions


def start_metrics_server(port: int = 8000):
    """
    Start Prometheus metrics HTTP server
    
    Args:
        port: Port to expose metrics on (default: 8000)
    """
    start_http_server(port)
    print(f"📊 Metrics server started on http://localhost:{port}/metrics")


# Example usage:
# from metrics import MetricsTracker, jobs_scraped_total
# 
# with MetricsTracker("JobSpy"):
#     jobs = scraper.fetch_jobs()
#     jobs_scraped_total.labels(source="JobSpy").inc(len(jobs))
