"""
Simplified unit tests for database module
"""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestDatabaseBasic:
    """Basic test suite for JobDatabase"""
    
    def test_database_import(self):
        """Test database module imports correctly"""
        try:
            from database import JobDatabase
            assert JobDatabase is not None
        except ImportError as e:
            pytest.fail(f"Failed to import database: {e}")
    
    def test_job_database_exists(self):
        """Test JobDatabase class exists"""
        from database import JobDatabase
        
        # Just verify the class exists and can be referenced
        assert JobDatabase is not None
        assert callable(JobDatabase)
