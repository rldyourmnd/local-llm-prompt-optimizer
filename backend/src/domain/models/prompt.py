from dataclasses import dataclass
from enum import Enum
from typing import Optional


class VendorType(str, Enum):
    """Supported LLM vendors."""
    OPENAI = "openai"
    CLAUDE = "claude"
    GROK = "grok"
    GEMINI = "gemini"
    QWEN = "qwen"
    DEEPSEEK = "deepseek"


@dataclass
class OptimizationRequest:
    """Request to optimize a prompt."""
    original_prompt: str
    target_vendor: VendorType
    context: Optional[str] = None
    max_length: Optional[int] = None


@dataclass
class OptimizedPrompt:
    """Optimized prompt result."""
    original: str
    optimized: str
    vendor: VendorType
    enhancement_notes: str
    metadata: dict


@dataclass
class PromptScore:
    """Scoring metrics for a prompt."""
    clarity: float
    specificity: float
    structure: float
    vendor_compliance: float
    overall: float
