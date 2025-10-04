"""Health check endpoint tests."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint_returns_200(async_client: AsyncClient):
    """Test that health endpoint returns 200."""
    response = await async_client.get("/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_response_structure(async_client: AsyncClient):
    """Test that health endpoint returns correct structure."""
    response = await async_client.get("/health")
    data = response.json()

    assert "status" in data
    assert "lm_studio_available" in data
    assert "vendor_adapters" in data
    assert data["status"] == "healthy"
    assert isinstance(data["lm_studio_available"], bool)
    assert data["vendor_adapters"] == 6


@pytest.mark.asyncio
async def test_root_endpoint(async_client: AsyncClient):
    """Test root endpoint returns correct information."""
    response = await async_client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "credits" in data
    assert data["credits"]["author"] == "Danil Silantyev"
    assert data["credits"]["company"] == "NDDev OpenNetwork"
