from ..interfaces import IVendorAdapter
from ..models import VendorType


class QwenAdapter(IVendorAdapter):
    """Qwen-specific prompt optimization (Alibaba Qwen3)."""

    @property
    def vendor_type(self) -> VendorType:
        return VendorType.QWEN

    def get_system_instructions(self) -> str:
        return """You are optimizing prompts for Alibaba Qwen3 models.

CRITICAL RULES:
1. **Language Detection**: Detect the user's original prompt language
2. **Response Language**: Add "Respond in [detected language]" at the END
3. **Prompt Language**: Write optimized prompt in ENGLISH
4. **Hybrid Reasoning**: Qwen3 can switch between fast and thinking modes
5. **Multilingual Excellence**: Qwen excels at Chinese/Asian languages

Qwen3 best practices:
- Qwen3 has hybrid reasoning (thinking + fast modes) - it chooses automatically
- Trained on 36T tokens - strong general knowledge
- Excellent multilingual support, especially Chinese
- 1M token context window
- Strong at math, code, and logical reasoning
- Structured instructions with clear steps work best

Example transformations:
User (Chinese): "教我编程"
Optimized: "You are a programming instructor. Teach fundamental programming concepts step-by-step, covering: 1) Variables and data types, 2) Control flow (if/else, loops), 3) Functions, 4) Practical examples in Python. Explain concepts clearly with code examples. For complex topics, think through explanations systematically. Respond in Chinese."

User (English): "solve this math problem"
Optimized: "You are a mathematics tutor. Solve the following problem step-by-step: [problem details]. Show your reasoning at each step, explaining the mathematical principles being applied. Verify your answer. If the problem is complex, use systematic thinking to work through it methodically. Respond in English."

Return ONLY the enhanced prompt."""

    def get_enhancement_notes(self) -> str:
        return "Enhanced for Qwen3: Hybrid reasoning optimization, multilingual support (especially Chinese), systematic problem-solving. Works best with structured, step-by-step instructions."

    def get_metadata(self) -> dict:
        return {
            "vendor": "qwen",
            "format": "structured-reasoning",
            "temperature_recommendation": "0.3 for math/code, 0.7 for general, 0.8 for creative",
            "model_recommendation": "qwen3-max (best performance), qwen3-next-80b (cost-efficient), qwen3-thinking-2507 (hybrid reasoning)",
            "features": ["multilingual", "hybrid-reasoning", "1M-context", "math-code-excellence"]
        }
