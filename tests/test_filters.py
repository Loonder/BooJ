"""
Simple unit tests for filters module
"""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestFiltersBasic:
    """Basic test suite for job filtering functions"""
    
    def test_imports_work(self):
        """Test that filter module imports correctly"""
        try:
            from filters import parse_relative_date
            assert parse_relative_date is not None
        except ImportError as e:
            pytest.fail(f"Failed to import filters: {e}")
    
    def test_parse_relative_date_recent(self):
        """Test parsing recent dates"""
        from filters import parse_relative_date
        
        # Test "agora" / "now"
        result = parse_relative_date("agora")
        assert result == 0
        
    def test_parse_relative_date_hours(self):
        """Test parsing hours"""
        from filters import parse_relative_date
        
        result = parse_relative_date("Há 2 horas")
        assert result == 120  # 2 hours = 120 minutes
    
    def test_parse_relative_date_days(self):
        """Test parsing days"""
        from filters import parse_relative_date
        
        result = parse_relative_date("Há 1 dia")
        assert result == 1440  # 1 day = 1440 minutes
    
    def test_parse_relative_date_unknown(self):
        """Test unknown date format"""
        from filters import parse_relative_date
        
        result = parse_relative_date("")
        assert result == 999999  # Unknown dates get low priority
