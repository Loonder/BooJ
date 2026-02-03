"""
Test configuration and fixtures
"""
import pytest
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def sample_job():
    """Sample job data for testing"""
    return {
        "titulo": "Desenvolvedor Python Junior",
        "empresa": "Tech Company",
        "localizacao": "São Paulo, SP",
        "link": "https://example.com/job/123",
        "data_publicacao": "2026-02-01",
        "data_coleta": "2026-02-03 10:00:00",
        "plataforma": "JobSpy (Linkedin)"
    }


@pytest.fixture
def sample_jobs_list():
    """List of sample jobs for testing"""
    return [
        {
            "titulo": "Estagiário Backend",
            "empresa": "Startup XYZ",
            "localizacao": "Remoto",
            "link": "https://example.com/job/1",
            "data_publicacao": "2026-02-02",
            "data_coleta": "2026-02-03 10:00:00",
            "plataforma": "Gupy"
        },
        {
            "titulo": "Desenvolvedor Full Stack Jr",
            "empresa": "Big Tech",
            "localizacao": "São Paulo, SP",
            "link": "https://example.com/job/2",
            "data_publicacao": "2026-02-01",
            "data_coleta": "2026-02-03 10:00:00",
            "plataforma": "Catho"
        },
        {
            "titulo": "Trainee TI",
            "empresa": "Corporation Inc",
            "localizacao": "Rio de Janeiro, RJ",
            "link": "https://example.com/job/3",
            "data_publicacao": "2026-01-30",
            "data_coleta": "2026-02-03 10:00:00",
            "plataforma": "JobSpy (Indeed)"
        }
    ]
