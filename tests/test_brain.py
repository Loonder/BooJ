"""
Unit tests for intelligence module (job enhancement and scoring)
"""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestIntelligenceBasic:
    """Basic test suite for Intelligence module"""
    
    def test_intelligence_import(self):
        """Test intelligence module imports correctly"""
        try:
            from intelligence import Intelligence
            assert Intelligence is not None
        except ImportError as e:
            pytest.fail(f"Failed to import intelligence: {e}")
    
    def test_enhance_job_exists(self):
        """Test enhance_job_data method exists"""
        from intelligence import Intelligence
        
        brain = Intelligence()
        assert hasattr(brain, 'enhance_job_data')
        assert callable(brain.enhance_job_data)
    
    def test_enhance_job_data_works(self):
        """Test enhance_job_data adds score and tags"""
        from intelligence import Intelligence
        
        brain = Intelligence()
        job = {
            'titulo': 'Estágio Python Developer',
            'empresa': 'Tech Company',
            'link': 'https://example.com/job/1'
        }
        
        enhanced = brain.enhance_job_data(job)
        
        assert 'score' in enhanced
        assert 'is_relevant' in enhanced
        assert 'tags' in enhanced
        assert isinstance(enhanced['score'], int)
