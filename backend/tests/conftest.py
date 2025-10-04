"""Pytest configuration and fixtures."""
import pytest
from httpx import AsyncClient
from src.api.main import app
from src.infrastructure.llm import LMStudioClient
from src.application.services import OptimizationService


@pytest.fixture
def llm_client():
    """Fixture for LLM client."""
    return LMStudioClient()


@pytest.fixture
def optimization_service(llm_client):
    """Fixture for optimization service."""
    return OptimizationService(llm_client)


@pytest.fixture
async def async_client():
    """Fixture for async HTTP client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
