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


@pytest.mark.asyncio
@pytest.mark.parametrize("adapter_class,vendor_type", [
    (OpenAIAdapter, VendorType.OPENAI),
    (ClaudeAdapter, VendorType.CLAUDE),
    (GrokAdapter, VendorType.GROK),
    (GeminiAdapter, VendorType.GEMINI),
    (QwenAdapter, VendorType.QWEN),
    (DeepSeekAdapter, VendorType.DEEPSEEK),
])
async def test_adapter_optimize(adapter_class, vendor_type):
    """Test that each adapter can optimize a prompt."""
    adapter = adapter_class()
    request = OptimizationRequest(
        original_prompt="Write a function to calculate fibonacci numbers",
        target_vendor=vendor_type
    )
    base_optimized = "Create a Python function that efficiently calculates fibonacci numbers"

    result = await adapter.optimize(request, base_optimized)

    assert isinstance(result, OptimizedPrompt)
    assert result.vendor == vendor_type
    assert result.original == request.original_prompt
    assert len(result.optimized) > len(base_optimized)
    assert isinstance(result.enhancement_notes, str)
    assert isinstance(result.metadata, dict)
    assert "vendor" in result.metadata
    assert "format" in result.metadata


@pytest.mark.asyncio
async def test_claude_adapter_xml_structure():
    """Test that Claude adapter adds XML structure."""
    adapter = ClaudeAdapter()
    request = OptimizationRequest(
        original_prompt="Test task",
        target_vendor=VendorType.CLAUDE
    )
    base_optimized = "Perform the test task"

    result = await adapter.optimize(request, base_optimized)

    assert "<task>" in result.optimized
    assert "</task>" in result.optimized
    assert result.metadata["format"] == "xml"


@pytest.mark.asyncio
async def test_openai_adapter_markdown_structure():
    """Test that OpenAI adapter uses markdown structure."""
    adapter = OpenAIAdapter()
    request = OptimizationRequest(
        original_prompt="Test task",
        target_vendor=VendorType.OPENAI
    )
    base_optimized = "Perform the test task"

    result = await adapter.optimize(request, base_optimized)

    assert "**Task:**" in result.optimized or "**" in result.optimized
    assert result.metadata["format"] == "markdown"


@pytest.mark.asyncio
async def test_gemini_adapter_structured_format():
    """Test that Gemini adapter uses structured format."""
    adapter = GeminiAdapter()
    request = OptimizationRequest(
        original_prompt="Test task",
        target_vendor=VendorType.GEMINI
    )
    base_optimized = "Perform the test task"

    result = await adapter.optimize(request, base_optimized)

    assert "##" in result.optimized
    assert result.metadata["format"] == "structured"


@pytest.mark.asyncio
async def test_deepseek_adapter_technical_structure():
    """Test that DeepSeek adapter adds technical structure."""
    adapter = DeepSeekAdapter()
    request = OptimizationRequest(
        original_prompt="Write code",
        target_vendor=VendorType.DEEPSEEK
    )
    base_optimized = "Write clean code"

    result = await adapter.optimize(request, base_optimized)

    assert "## Objective" in result.optimized or "Objective" in result.optimized
    assert result.metadata["format"] == "technical_structured"
    assert "code generation" in result.metadata["strengths"]


@pytest.mark.asyncio
async def test_adapter_with_context():
    """Test adapter optimization with additional context."""
    adapter = OpenAIAdapter()
    request = OptimizationRequest(
        original_prompt="Test task",
        target_vendor=VendorType.OPENAI,
        context="This is for a tutorial"
    )
    base_optimized = "Perform the test task"

    result = await adapter.optimize(request, base_optimized)

    assert "tutorial" in result.optimized.lower() or "context" in result.optimized.lower()
