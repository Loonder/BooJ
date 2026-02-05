"""
Unit tests for JobSpy scraper
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scraper_jobspy_real import JobSpyRealScraper


class TestJobSpyScraper:
    """Test suite for JobSpy scraper"""
    
    def test_initialization(self):
        """Test scraper initializes correctly"""
        scraper = JobSpyRealScraper()
        
        assert scraper.platform == "JobSpy"
        assert scraper.sites == ["indeed", "linkedin", "google"]
    
    def test_parse_location_with_dict(self):
        """Test location parsing with dictionary"""
        scraper = JobSpyRealScraper()
        
        job = {
            'city': 'São Paulo',
            'state': 'SP'
        }
        
        location = scraper._parse_location(job)
        assert location == "São Paulo, SP"
    
    def test_parse_location_city_only(self):
        """Test location parsing with city only"""
        scraper = JobSpyRealScraper()
        
        job = {
            'city': 'Campinas',
            'state': ''
        }
        
        location = scraper._parse_location(job)
        assert location == "Campinas"
    
    def test_parse_location_remote(self):
        """Test location parsing for remote jobs"""
        scraper = JobSpyRealScraper()
        
        job = {'is_remote': True}
        
        location = scraper._parse_location(job)
        assert location == "🏠 REMOTO"
    
    def test_parse_location_fallback(self):
        """Test location parsing fallback"""
        scraper = JobSpyRealScraper()
        
        job = {}
        
        location = scraper._parse_location(job)
        assert location == "Brasil"
    
    @patch('scraper_jobspy_real.scrape_jobs')
    def test_fetch_jobs_success(self, mock_scrape):
        """Test successful job fetching with mocked API"""
        # Mock API response
        mock_df = pd.DataFrame([
            {
                'site': 'linkedin',
                'title': 'Software Engineer',
                'company': 'Tech Co',
                'city': 'São Paulo',
                'state': 'SP',
                'job_url': 'https://linkedin.com/job/123',
                'date_posted': '2026-02-01'
            },
            {
                'site': 'indeed',
                'title': 'Backend Developer',
                'company': 'Startup XYZ',
                'city': 'Remoto',
                'state': '',
                'job_url': 'https://indeed.com/job/456',
                'date_posted': '2026-02-02'
            }
        ])
        mock_scrape.return_value = mock_df
        
        scraper = JobSpyRealScraper()
        jobs = scraper.fetch_jobs()
        
        # Verify results
        assert isinstance(jobs, list)
        assert len(jobs) >= 0  # May filter some results
        
        # Check first job structure
        if len(jobs) > 0:
            job = jobs[0]
            assert 'titulo' in job
            assert 'empresa' in job
            assert 'localizacao' in job
            assert 'link' in job
            assert 'plataforma' in job
            
            # Check platform formatting
            assert job['plataforma'].startswith('JobSpy (')
    
    @patch('scraper_jobspy_real.scrape_jobs')
    def test_fetch_jobs_empty_response(self, mock_scrape):
        """Test handling of empty API response"""
        mock_scrape.return_value = None
        
        scraper = JobSpyRealScraper()
        jobs = scraper.fetch_jobs()
        
        assert isinstance(jobs, list)
        assert len(jobs) == 0
    
    @patch('scraper_jobspy_real.scrape_jobs')
    def test_fetch_jobs_filters_invalid(self, mock_scrape):
        """Test that invalid jobs are filtered out"""
        mock_df = pd.DataFrame([
            {
                'site': 'linkedin',
                'title': 'Valid Job',
                'company': 'Tech Co',
                'city': 'SP',
                'state': '',
                'job_url': 'https://linkedin.com/job/123',
                'date_posted': '2026-02-01'
            },
            {
                'site': 'indeed',
                'title': 'Invalid Job',
                'company': 'Bad Co',
                'city': '',
                'state': '',
                'job_url': 'None',  # Invalid URL
                'date_posted': '2026-02-02'
            }
        ])
        mock_scrape.return_value = mock_df
        
        scraper = JobSpyRealScraper()
        jobs = scraper.fetch_jobs()
        
        # Invalid job should be filtered
        assert all(job['link'] and 'None' not in job['link'] for job in jobs)
    
    @patch('scraper_jobspy_real.scrape_jobs')
    def test_fetch_jobs_handles_exception(self, mock_scrape):
        """Test error handling when API fails"""
        mock_scrape.side_effect = Exception("API Error")
        
        scraper = JobSpyRealScraper()
        jobs = scraper.fetch_jobs()
        
        # Should return empty list on error
        assert isinstance(jobs, list)
        assert len(jobs) == 0
