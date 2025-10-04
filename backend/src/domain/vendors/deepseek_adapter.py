from ..interfaces import IVendorAdapter
from ..models import VendorType


class DeepSeekAdapter(IVendorAdapter):
    """DeepSeek-specific prompt optimization (DeepSeek V3.2-Exp).

    Latest models:
    - DeepSeek-V3.2-Exp (Sep 29, 2025): Non-thinking and thinking modes
    - DeepSeek-R1-0528 (May 28, 2025): Advanced reasoning
    """

    @property
    def vendor_type(self) -> VendorType:
        return VendorType.DEEPSEEK

    def get_system_instructions(self) -> str:
        return """You are optimizing prompts for DeepSeek V3.2-Exp models (Sep 29, 2025).

CRITICAL RULES:
1. **Language Detection**: Detect the user's original prompt language
2. **Response Language**: Add "Respond in [detected language]" at the END
3. **Prompt Language**: Write optimized prompt in ENGLISH
4. **Technical Focus**: DeepSeek excels at code and technical tasks
5. **Dual Modes**: V3.2-Exp has thinking and non-thinking modes

DeepSeek V3.2-Exp best practices:
- DeepSeek-V3.2-Exp (Sep 29, 2025): Latest with dual thinking/non-thinking modes
- DeepSeek-R1-0528 (May 28, 2025): Specialized advanced reasoning model
- BEST at code generation and technical tasks
- Thinking mode: For complex reasoning, system design, architectural decisions
- Non-thinking mode: For direct code generation, quick technical answers
- 128K context window with DSA sparse attention (very efficient)
- Strong at: code, math, system design, technical analysis
- Precise technical specifications work best
- For code: specify language, requirements, edge cases

Example transformations:
User (Korean): "알고리즘 최적화"
Optimized: "You are a senior software engineer specializing in algorithm optimization. Analyze the given \
algorithm and optimize it for: 1) Time complexity, 2) Space complexity, 3) Code readability. Provide the \
optimized implementation with detailed comments explaining improvements. Include complexity analysis (Big-O \
notation). For complex optimizations, think through trade-offs systematically. Respond in Korean."

User (English): "design a database schema"
Optimized: "You are a database architect. Design a normalized database schema for [use case]. Include: \
1) Entity-relationship diagram description, 2) Table definitions with primary/foreign keys, 3) Indexing \
strategy, 4) Justification for design decisions. Consider scalability and query performance. Think through \
normalization trade-offs. Respond in English."

Return ONLY the enhanced prompt."""

    def get_enhancement_notes(self) -> str:
        return (
            "Enhanced for DeepSeek V3.2-Exp (Sep 29, 2025): Latest model with dual thinking/non-thinking modes. "
            "Technical precision, code optimization focus. DeepSeek-R1-0528 (May 28, 2025) available for "
            "advanced reasoning. Best for programming, algorithms, and system design."
        )

    def get_metadata(self) -> dict:
        return {
            "vendor": "deepseek",
            "format": "technical-structured",
            "temperature_recommendation": (
                "0.1-0.3 for code, 0.5 for technical writing, 0.7 for general"
            ),
            "model_recommendation": (
                "deepseek-v3.2-exp (Sep 29, 2025, thinking/non-thinking modes), "
                "deepseek-r1-0528 (May 28, 2025, advanced reasoning)"
            ),
            "features": ["code-generation", "math-excellence", "DSA-sparse-attention", "128K-context", "MIT-licensed"]
        }
