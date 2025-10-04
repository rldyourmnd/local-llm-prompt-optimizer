"""Tests for optimization service."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from src.application.services import OptimizationService
from src.domain.models import VendorType, OptimizationRequest, OptimizedPrompt


@pytest.mark.asyncio
async def test_optimization_service_initialization():
    """Test optimization service initializes correctly."""
    from src.domain.registries import VendorRegistry

    mock_client = AsyncMock()
    service = OptimizationService(mock_client)

    assert service.llm_client == mock_client
    # In v1.1.0, adapters are managed by VendorRegistry, not OptimizationService
    assert VendorRegistry.is_registered(VendorType.OPENAI)
    assert VendorRegistry.is_registered(VendorType.CLAUDE)
    assert VendorRegistry.is_registered(VendorType.GROK)
    assert VendorRegistry.is_registered(VendorType.GEMINI)
    assert VendorRegistry.is_registered(VendorType.QWEN)
    assert VendorRegistry.is_registered(VendorType.DEEPSEEK)


@pytest.mark.asyncio
async def test_optimize_prompt_success():
    """Test successful prompt optimization."""
    mock_client = AsyncMock()
    mock_client.generate = AsyncMock(return_value="Optimized prompt content")

    service = OptimizationService(mock_client)
    request = OptimizationRequest(
        original_prompt="Write a function",
        target_vendor=VendorType.OPENAI
    )

    result = await service.optimize_prompt(request)

    assert isinstance(result, OptimizedPrompt)
    assert result.vendor == VendorType.OPENAI
    assert result.original == "Write a function"
    assert len(result.optimized) > 0
    mock_client.generate.assert_called_once()


@pytest.mark.asyncio
async def test_optimize_prompt_with_context():
    """Test prompt optimization with additional context."""
    mock_client = AsyncMock()
    mock_client.generate = AsyncMock(return_value="Optimized with context")

    service = OptimizationService(mock_client)
    request = OptimizationRequest(
        original_prompt="Write a function",
        target_vendor=VendorType.CLAUDE,
        context="For Python tutorial"
    )

    result = await service.optimize_prompt(request)

    assert isinstance(result, OptimizedPrompt)
    assert result.vendor == VendorType.CLAUDE
    # Verify that generate was called with messages containing the context
    call_args = mock_client.generate.call_args
    messages = call_args[1]["messages"]
    user_message = messages[1]["content"]
    assert "For Python tutorial" in user_message


@pytest.mark.asyncio
async def test_optimize_prompt_unsupported_vendor():
    """Test optimization with unsupported vendor raises error."""
    from src.domain.registries import VendorRegistry
    from src.domain.exceptions import VendorNotSupportedException

    mock_client = AsyncMock()
    service = OptimizationService(mock_client)

    # In v1.1.0, we need to clear the VendorRegistry to simulate unsupported vendor
    # Save current state and restore after test
    saved_adapters = VendorRegistry._adapters.copy()
    VendorRegistry.clear()

    try:
        request = OptimizationRequest(
            original_prompt="Test",
            target_vendor=VendorType.OPENAI
        )

        with pytest.raises(VendorNotSupportedException):
            await service.optimize_prompt(request)
    finally:
        # Restore registry state
        VendorRegistry._adapters = saved_adapters


@pytest.mark.asyncio
async def test_optimize_prompt_calls_llm():
    """Test that optimization calls LLM client with correct parameters."""
    mock_client = AsyncMock()
    mock_client.generate = AsyncMock(return_value="Generated response")

    service = OptimizationService(mock_client)
    request = OptimizationRequest(
        original_prompt="Calculate fibonacci",
        target_vendor=VendorType.DEEPSEEK,
        max_length=1000
    )

    await service.optimize_prompt(request)

    # Verify LLM was called
    mock_client.generate.assert_called_once()

    # Verify parameters
    call_kwargs = mock_client.generate.call_args[1]
    assert call_kwargs["temperature"] == 0.3  # Lower for consistency
    assert call_kwargs["max_tokens"] == 2048
    assert "messages" in call_kwargs
    assert len(call_kwargs["messages"]) == 2
    assert call_kwargs["messages"][0]["role"] == "system"
    assert call_kwargs["messages"][1]["role"] == "user"


@pytest.mark.asyncio
async def test_health_check_success():
    """Test health check when LLM is available."""
    mock_client = AsyncMock()
    mock_client.health_check = AsyncMock(return_value=True)

    service = OptimizationService(mock_client)
    result = await service.health_check()

    assert result is True
    mock_client.health_check.assert_called_once()


@pytest.mark.asyncio
async def test_health_check_failure():
    """Test health check when LLM is unavailable."""
    mock_client = AsyncMock()
    mock_client.health_check = AsyncMock(return_value=False)

    service = OptimizationService(mock_client)
    result = await service.health_check()

    assert result is False
    mock_client.health_check.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize("vendor", [
    VendorType.OPENAI,
    VendorType.CLAUDE,
    VendorType.GROK,
    VendorType.GEMINI,
    VendorType.QWEN,
    VendorType.DEEPSEEK,
])
async def test_optimize_all_vendors(vendor):
    """Test optimization works for all supported vendors."""
    mock_client = AsyncMock()
    mock_client.generate = AsyncMock(return_value="Optimized content")

    service = OptimizationService(mock_client)
    request = OptimizationRequest(
        original_prompt="Test prompt",
        target_vendor=vendor
    )

    result = await service.optimize_prompt(request)

    assert result.vendor == vendor
    assert isinstance(result, OptimizedPrompt)
    assert result.original == "Test prompt"
