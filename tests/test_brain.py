"""
Simplified unit tests for brain module
"""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestBrainBasic:
    """Basic test suite for AI brain module"""
    
    def test_brain_import(self):
        """Test brain module imports correctly"""
        try:
            from brain import enhance_job_data
            assert enhance_job_data is not None
        except ImportError as e:
            pytest.fail(f"Failed to import brain: {e}")
    
    def test_enhance_job_exists(self):
        """Test enhance_job_data function exists"""
        from brain import enhance_job_data
        
        assert enhance_job_data is not None
        assert callable(enhance_job_data)
