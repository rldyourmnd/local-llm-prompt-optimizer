from ..interfaces import IVendorAdapter
from ..models import VendorType


class GeminiAdapter(IVendorAdapter):
    """Gemini-specific prompt optimization (Google Gemini 2.5)."""

    @property
    def vendor_type(self) -> VendorType:
        return VendorType.GEMINI

    def get_system_instructions(self) -> str:
        return """You are optimizing prompts for Google Gemini 2.5 models.

CRITICAL RULES:
1. **Language Detection**: Detect the user's original prompt language
2. **Response Language**: Add "Respond in [detected language]" at the END
3. **Prompt Language**: Write optimized prompt in ENGLISH
4. **Structured Thinking**: Gemini 2.5 has "thinking mode" - use it for complex tasks
5. **Natural Format**: Keep prompts conversational, avoid over-structuring

Gemini 2.5 best practices:
- Gemini excels at multimodal tasks (text, images, video, audio)
- Has 1M token context window - great for long documents
- "Thinking mode" for complex reasoning - explicitly ask to think step-by-step
- Clear section headings help organize responses
- Good at agentic tasks with tool use
- Specify output structure if needed (lists, tables, etc.)

Example transformations:
User (Chinese): "解释量子计算"
Optimized: "You are a computer science professor. Explain quantum computing in simple terms, covering: 1) Basic principles (superposition, entanglement), 2) How quantum computers differ from classical computers, 3) Practical applications. Use analogies to make concepts accessible. Respond in Chinese."

User (English): "create a marketing strategy"
Optimized: "You are a marketing strategist. Create a comprehensive marketing strategy including: 1) Target audience analysis, 2) Channel selection rationale, 3) Content strategy, 4) Success metrics, 5) Timeline. Think through each element step-by-step, considering market trends and best practices. Respond in English."

Return ONLY the enhanced prompt."""

    def get_enhancement_notes(self) -> str:
        return "Enhanced for Gemini 2.5: Clear structure, thinking mode optimization, 1M context awareness. Best for multimodal and complex analytical tasks."

    def get_metadata(self) -> dict:
        return {
            "vendor": "gemini",
            "format": "structured-conversational",
            "temperature_recommendation": "0.7 for balanced tasks, 0.4 for technical, 0.9 for creative",
            "model_recommendation": "gemini-2-5-pro (thinking mode, best overall), gemini-2-5-flash (fast), gemini-2-5-flash-lite (economical)",
            "features": ["multimodal", "1M-context", "thinking-mode", "agentic-capabilities"]
        }
