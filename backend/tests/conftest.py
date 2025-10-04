"""Pytest configuration and fixtures."""
import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from src.api.main import app
from src.infrastructure.llm import LMStudioClient
from src.application.services import OptimizationService
from src.infrastructure.di.container import Container


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
    """Fixture for async HTTP client with mocked LLM client."""
    # Create a mock LLM client
    mock_llm_client = AsyncMock()
    mock_llm_client.generate = AsyncMock(return_value="Optimized test prompt")
    mock_llm_client.health_check = AsyncMock(return_value=True)

    # Override DI container's llm_client
    with patch.object(Container, 'llm_client', return_value=mock_llm_client):
        # Reinitialize the app's container with mocked client
        app.container.llm_client.override(mock_llm_client)

        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client

        # Reset override after test
        app.container.llm_client.reset_override()
