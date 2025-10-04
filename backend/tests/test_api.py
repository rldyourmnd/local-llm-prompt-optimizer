"""API endpoint integration tests."""
import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_optimize_endpoint_success(async_client: AsyncClient):
    """Test successful optimization request."""
    with patch("src.infrastructure.llm.LMStudioClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.generate = AsyncMock(return_value="Optimized prompt")
        mock_client_class.return_value = mock_client

        response = await async_client.post(
            "/api/optimize",
            json={
                "prompt": "Write a function",
                "vendor": "openai"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "original" in data
        assert "optimized" in data
        assert "vendor" in data
        assert "enhancement_notes" in data
        assert "metadata" in data
        assert data["vendor"] == "openai"


@pytest.mark.asyncio
async def test_optimize_endpoint_with_context(async_client: AsyncClient):
    """Test optimization with additional context."""
    with patch("src.infrastructure.llm.LMStudioClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.generate = AsyncMock(return_value="Optimized with context")
        mock_client_class.return_value = mock_client

        response = await async_client.post(
            "/api/optimize",
            json={
                "prompt": "Write a function",
                "vendor": "claude",
                "context": "For beginners"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["vendor"] == "claude"


@pytest.mark.asyncio
async def test_optimize_endpoint_invalid_vendor(async_client: AsyncClient):
    """Test optimization with invalid vendor."""
    response = await async_client.post(
        "/api/optimize",
        json={
            "prompt": "Write a function",
            "vendor": "invalid_vendor"
        }
    )

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_optimize_endpoint_missing_prompt(async_client: AsyncClient):
    """Test optimization without prompt."""
    response = await async_client.post(
        "/api/optimize",
        json={
            "vendor": "openai"
        }
    )

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_optimize_endpoint_empty_prompt(async_client: AsyncClient):
    """Test optimization with empty prompt."""
    response = await async_client.post(
        "/api/optimize",
        json={
            "prompt": "",
            "vendor": "openai"
        }
    )

    assert response.status_code == 422  # Validation error (min_length=1)


@pytest.mark.asyncio
@pytest.mark.parametrize("vendor", [
    "openai", "claude", "grok", "gemini", "qwen", "deepseek"
])
async def test_optimize_all_vendors_via_api(async_client: AsyncClient, vendor):
    """Test API optimization for all vendors."""
    with patch("src.infrastructure.llm.LMStudioClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client.generate = AsyncMock(return_value="Optimized")
        mock_client_class.return_value = mock_client

        response = await async_client.post(
            "/api/optimize",
            json={
                "prompt": "Test prompt",
                "vendor": vendor
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["vendor"] == vendor


@pytest.mark.asyncio
async def test_api_docs_available(async_client: AsyncClient):
    """Test that API documentation is available."""
    response = await async_client.get("/api/docs")
    assert response.status_code == 200
