"""Tests for domain models."""
from src.domain.models import (
    VendorType,
    OptimizationRequest,
    OptimizedPrompt,
    PromptScore
)


def test_vendor_type_enum():
    """Test VendorType enum values."""
    assert VendorType.OPENAI == "openai"
    assert VendorType.CLAUDE == "claude"
    assert VendorType.GROK == "grok"
    assert VendorType.GEMINI == "gemini"
    assert VendorType.QWEN == "qwen"
    assert VendorType.DEEPSEEK == "deepseek"


def test_optimization_request_creation():
    """Test OptimizationRequest dataclass creation."""
    request = OptimizationRequest(
        original_prompt="Test prompt",
        target_vendor=VendorType.OPENAI,
        context="Test context",
        max_length=500
    )

    assert request.original_prompt == "Test prompt"
    assert request.target_vendor == VendorType.OPENAI
    assert request.context == "Test context"
    assert request.max_length == 500


def test_optimization_request_without_optional_fields():
    """Test OptimizationRequest without optional fields."""
    request = OptimizationRequest(
        original_prompt="Test prompt",
        target_vendor=VendorType.CLAUDE
    )

    assert request.original_prompt == "Test prompt"
    assert request.target_vendor == VendorType.CLAUDE
    assert request.context is None
    assert request.max_length is None


def test_optimized_prompt_creation():
    """Test OptimizedPrompt dataclass creation."""
    result = OptimizedPrompt(
        original="Original prompt",
        optimized="Improved prompt",
        vendor=VendorType.OPENAI,
        enhancement_notes="Added structure",
        metadata={"format": "markdown"}
    )

    assert result.original == "Original prompt"
    assert result.optimized == "Improved prompt"
    assert result.vendor == VendorType.OPENAI
    assert result.enhancement_notes == "Added structure"
    assert result.metadata["format"] == "markdown"


def test_prompt_score_creation():
    """Test PromptScore dataclass creation."""
    score = PromptScore(
        clarity=0.9,
        specificity=0.85,
        structure=0.95,
        vendor_compliance=0.88,
        overall=0.89
    )

    assert score.clarity == 0.9
    assert score.specificity == 0.85
    assert score.structure == 0.95
    assert score.vendor_compliance == 0.88
    assert score.overall == 0.89
