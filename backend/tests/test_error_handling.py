"""Tests for error handling and edge cases."""
import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock
from src.application.services import OptimizationService
from src.domain.models import VendorType
from src.domain.exceptions import (
    VendorNotSupportedException,
    OptimizationFailedException,
    QuestionGenerationFailedException
)


@pytest.mark.asyncio
async def test_optimize_endpoint_vendor_not_supported_error(async_client: AsyncClient):
    """Test optimization endpoint handles VendorNotSupportedException."""
    from src.api.main import app
    from src.domain.registries import VendorRegistry

    # Temporarily clear registry to simulate unsupported vendor
    saved_adapters = VendorRegistry._adapters.copy()
    VendorRegistry.clear()

    try:
        response = await async_client.post(
            "/api/optimize",
            json={
                "prompt": "Test prompt",
                "vendor": "openai"
            }
        )

        # Should return 400 for vendor not supported
        assert response.status_code in [400, 500]
        data = response.json()
        assert "detail" in data
    finally:
        # Restore registry
        VendorRegistry._adapters = saved_adapters


@pytest.mark.asyncio
async def test_optimize_endpoint_value_error():
    """Test optimization endpoint handles ValueError."""
    mock_client = AsyncMock()
    mock_client.generate = AsyncMock(side_effect=ValueError("Invalid value"))

    service = OptimizationService(mock_client)

    from src.domain.models import OptimizationRequest

    with pytest.raises(ValueError):
        await service.optimize_prompt(
            OptimizationRequest(
                original_prompt="Test",
                target_vendor=VendorType.OPENAI
            )
        )


@pytest.mark.asyncio
async def test_generate_questions_endpoint_failure(async_client: AsyncClient):
    """Test question generation endpoint handles failures."""
    from src.api.main import app

    # Override mock to raise exception
    original_generate = app.container.llm_client().generate
    app.container.llm_client().generate = AsyncMock(
        side_effect=Exception("LLM generation failed")
    )

    try:
        response = await async_client.post(
            "/api/think/generate-questions",
            json={
                "prompt": "Test",
                "vendor": "openai",
                "num_questions": 5
            }
        )

        # Should return 500 for generation failure
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
    finally:
        # Restore original mock
        app.container.llm_client().generate = original_generate


@pytest.mark.asyncio
async def test_optimize_with_answers_endpoint_value_error(async_client: AsyncClient):
    """Test optimize with answers handles ValueError for mismatched Q&A."""
    response = await async_client.post(
        "/api/think/optimize-with-answers",
        json={
            "prompt": "Test",
            "vendor": "openai",
            "questions": ["Q1?", "Q2?"],
            "answers": ["A1"]  # Mismatch
        }
    )

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "match" in data["detail"].lower()


@pytest.mark.asyncio
async def test_optimize_with_answers_vendor_not_supported(async_client: AsyncClient):
    """Test optimize with answers handles unsupported vendor."""
    from src.api.main import app
    from src.domain.registries import VendorRegistry

    saved_adapters = VendorRegistry._adapters.copy()
    VendorRegistry.clear()

    try:
        response = await async_client.post(
            "/api/think/optimize-with-answers",
            json={
                "prompt": "Test",
                "vendor": "openai",
                "questions": ["Q1?"],
                "answers": ["A1"]
            }
        )

        # Should handle vendor not supported
        assert response.status_code in [400, 500]
    finally:
        VendorRegistry._adapters = saved_adapters


@pytest.mark.asyncio
async def test_optimization_service_llm_failure():
    """Test optimization service handles LLM client failures."""
    mock_client = AsyncMock()
    mock_client.generate = AsyncMock(side_effect=Exception("LLM connection failed"))

    service = OptimizationService(mock_client)

    from src.domain.models import OptimizationRequest

    with pytest.raises(Exception) as exc_info:
        await service.optimize_prompt(
            OptimizationRequest(
                original_prompt="Test",
                target_vendor=VendorType.OPENAI
            )
        )

    assert "LLM connection failed" in str(exc_info.value)


@pytest.mark.asyncio
async def test_generate_questions_llm_failure():
    """Test question generation handles LLM failures."""
    mock_client = AsyncMock()
    mock_client.generate = AsyncMock(side_effect=Exception("LLM unavailable"))

    service = OptimizationService(mock_client)

    with pytest.raises(Exception) as exc_info:
        await service.generate_questions(
            prompt="Test",
            vendor=VendorType.OPENAI,
            num_questions=5
        )

    assert "LLM unavailable" in str(exc_info.value)


@pytest.mark.asyncio
async def test_optimize_with_answers_llm_failure():
    """Test optimize with answers handles LLM failures."""
    mock_client = AsyncMock()
    mock_client.generate = AsyncMock(side_effect=Exception("LLM timeout"))

    service = OptimizationService(mock_client)

    with pytest.raises(Exception) as exc_info:
        await service.optimize_with_answers(
            prompt="Test",
            vendor=VendorType.OPENAI,
            questions=["Q1?"],
            answers=["A1"]
        )

    assert "LLM timeout" in str(exc_info.value)


@pytest.mark.asyncio
async def test_empty_prompt_validation(async_client: AsyncClient):
    """Test API rejects empty prompts."""
    response = await async_client.post(
        "/api/optimize",
        json={
            "prompt": "",
            "vendor": "openai"
        }
    )

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_invalid_num_questions(async_client: AsyncClient):
    """Test question generation with invalid num_questions."""
    # Test with 0
    response = await async_client.post(
        "/api/think/generate-questions",
        json={
            "prompt": "Test",
            "vendor": "openai",
            "num_questions": 0
        }
    )
    assert response.status_code == 422  # Validation error

    # Test with negative
    response = await async_client.post(
        "/api/think/generate-questions",
        json={
            "prompt": "Test",
            "vendor": "openai",
            "num_questions": -5
        }
    )
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_very_long_prompt(async_client: AsyncClient):
    """Test optimization with very long prompt."""
    long_prompt = "A" * 10000  # 10k characters

    response = await async_client.post(
        "/api/optimize",
        json={
            "prompt": long_prompt,
            "vendor": "openai"
        }
    )

    # Should handle long prompts
    assert response.status_code in [200, 400, 422]


@pytest.mark.asyncio
async def test_special_characters_in_prompt(async_client: AsyncClient):
    """Test prompts with special characters."""
    special_prompt = "Test with 特殊文字 and émojis 🚀 and symbols: @#$%^&*()"

    response = await async_client.post(
        "/api/optimize",
        json={
            "prompt": special_prompt,
            "vendor": "openai"
        }
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_concurrent_requests(async_client: AsyncClient):
    """Test handling multiple concurrent requests."""
    import asyncio

    async def make_request():
        return await async_client.post(
            "/api/optimize",
            json={
                "prompt": "Concurrent test",
                "vendor": "openai"
            }
        )

    # Make 10 concurrent requests
    responses = await asyncio.gather(*[make_request() for _ in range(10)])

    # All should succeed
    assert all(r.status_code == 200 for r in responses)


@pytest.mark.asyncio
async def test_max_length_constraint(async_client: AsyncClient):
    """Test optimization with max_length constraint."""
    response = await async_client.post(
        "/api/optimize",
        json={
            "prompt": "Short prompt",
            "vendor": "openai",
            "max_length": 100
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "optimized" in data
