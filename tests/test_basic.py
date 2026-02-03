"""
Working basic tests for JobPulse
"""
import pytest


class TestBasicFunctionality:
    """Basic smoke tests to verify testing works"""
    
    def test_python_version(self):
        """Test we're running Python 3.11"""
        import sys
        assert sys.version_info.major == 3
        assert sys.version_info.minor == 11
    
    def test_pytest_works(self):
        """Basic test that pytest is working"""
        assert 1 + 1 == 2
    
    def test_list_operations(self):
        """Test basic Python operations"""
        test_list = [1, 2, 3]
        test_list.append(4)
        assert len(test_list) == 4
        assert 4 in test_list


class TestJobSpyScraperSimple:
    """Simple tests for JobSpy scraper without mocking"""
    
    def test_jobspy_scraper_exists(self):
        """Test JobSpy scraper can be imported"""
        import sys
        from pathlib import Path
        
        # Add src to path
        src_path = Path(__file__).parent.parent / "src"
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))
        
        from scraper_jobspy_real import JobSpyRealScraper
        assert JobSpyRealScraper is not None
    
    def test_jobspy_initialization(self):
        """Test JobSpy scraper initializes"""
        import sys
        from pathlib import Path
        
        src_path = Path(__file__).parent.parent / "src"
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))
        
        from scraper_jobspy_real import JobSpyRealScraper
        
        scraper = JobSpyRealScraper()
        assert scraper.platform == "JobSpy"
        assert isinstance(scraper.sites, list)
        assert len(scraper.sites) > 0
