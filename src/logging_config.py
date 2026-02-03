# -*- coding: utf-8 -*-
"""
Structured logging configuration using structlog
Outputs JSON logs for easy parsing and analysis
"""

import structlog
import logging
import sys
from pathlib import Path

def configure_logging(log_level: str = "INFO", log_file: str = "logs/hunter.log"):
    """
    Configure structured logging for the application
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Path to log file
    """
    
    # Ensure logs directory exists
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, log_level.upper()),
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    return structlog.get_logger()


def get_logger(name: str = None):
    """
    Get a configured structlog logger
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Configured structlog logger
    """
    if name:
        return structlog.get_logger(name)
    return structlog.get_logger()


# Example usage:
# from logging_config import get_logger
# logger = get_logger(__name__)
# logger.info("scraper_started", scraper="JobSpy", search_term="developer")
# logger.error("scraper_failed", scraper="Gupy", error=str(e), duration_ms=1500)
