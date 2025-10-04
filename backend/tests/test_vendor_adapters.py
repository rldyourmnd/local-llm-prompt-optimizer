"""Tests for vendor-specific adapters."""
import pytest
from src.domain.models import VendorType, OptimizationRequest, OptimizedPrompt
from src.domain.vendors import (
    OpenAIAdapter,
    ClaudeAdapter,
    GrokAdapter,
    GeminiAdapter,
    QwenAdapter,
    DeepSeekAdapter
)


@pytest.mark.parametrize("adapter_class,expected_vendor", [
    (OpenAIAdapter, VendorType.OPENAI),
    (ClaudeAdapter, VendorType.CLAUDE),
    (GrokAdapter, VendorType.GROK),
    (GeminiAdapter, VendorType.GEMINI),
    (QwenAdapter, VendorType.QWEN),
    (DeepSeekAdapter, VendorType.DEEPSEEK),
])
def test_adapter_vendor_type(adapter_class, expected_vendor):
    """Test that each adapter returns correct vendor type."""
    adapter = adapter_class()
    assert adapter.vendor_type == expected_vendor


@pytest.mark.parametrize("adapter_class", [
    OpenAIAdapter,
    ClaudeAdapter,
    GrokAdapter,
    GeminiAdapter,
    QwenAdapter,
    DeepSeekAdapter,
])
def test_adapter_system_instructions(adapter_class):
    """Test that each adapter provides system instructions."""
    adapter = adapter_class()
    instructions = adapter.get_system_instructions()
    assert isinstance(instructions, str)
    assert len(instructions) > 0
    assert "best practices" in instructions.lower() or "characteristics" in instructions.lower()


# NOTE: Tests for adapter.optimize() method removed in v1.1.0
# In the new SOLID/DDD architecture, adapters no longer have optimize() methods.
# They only provide:
#   - system_instructions: Instructions for the LLM on how to optimize
#   - metadata: Vendor-specific metadata
#   - enhancement_notes: Notes about the optimization
#
# The actual optimization is handled by OptimizationService using VendorRegistry.
# See test_optimization_service.py for integration tests.
