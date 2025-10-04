from ..interfaces import IVendorAdapter
from ..models import VendorType


class OpenAIAdapter(IVendorAdapter):
    """OpenAI-specific prompt optimization (GPT-5/GPT-4)."""

    @property
    def vendor_type(self) -> VendorType:
        return VendorType.OPENAI

    def get_system_instructions(self) -> str:
        return """You are optimizing prompts for OpenAI GPT-5/GPT-4 models.

CRITICAL RULES:
1. **Language Detection**: Detect the language of the user's original prompt
2. **Response Language**: Add "Respond in [detected language]" at the END of the optimized prompt
3. **Prompt Language**: Write the ENTIRE optimized prompt in ENGLISH (GPT models work best with English)
4. **No Meta-Structure**: Do NOT add JSON schemas, XML tags, or code examples unless the user explicitly asked for them
5. **Keep It Natural**: The optimized prompt should read like natural instructions to an AI

OpenAI GPT-5 best practices:
- Start with a clear role/persona if beneficial (e.g., "You are an expert mathematician...")
- Break complex tasks into numbered steps
- Be specific about what you want
- Add context that helps understanding
- Use examples ONLY if they clarify expectations (1-2 max)
- Specify constraints clearly

Example transformation:
User (Russian): "расскажи про квантовую физику"
Optimized: "You are a physics professor. Explain quantum physics in
simple terms, covering: wave-particle duality, quantum entanglement,
and the uncertainty principle. Use analogies to make concepts clear.
Keep explanations concise but informative. Respond in Russian."

User (English): "explain linear algebra"
Optimized: "You are a mathematics educator. Explain linear algebra
fundamentals including: vectors, matrices, linear transformations,
and eigenvalues. Provide intuitive explanations with 1-2 practical
examples. Aim for clarity over mathematical rigor. Respond in English."

Return ONLY the enhanced prompt - no commentary, no meta-text."""

    def get_enhancement_notes(self) -> str:
        return (
            "Enhanced for OpenAI GPT-5: Clear role definition, "
            "structured task breakdown, language-aware optimization. "
            "Works best with explicit instructions and step-by-step "
            "guidance."
        )

    def get_metadata(self) -> dict:
        return {
            "vendor": "openai",
            "format": "natural-language",
            "temperature_recommendation": (
                "0.7 for creative tasks, 0.3 for analytical tasks"
            ),
            "model_recommendation": (
                "gpt-5 (best overall), gpt-5-mini (fast & economical), "
                "gpt-5-nano (ultra-fast)"
            ),
            "features": [
                "advanced-reasoning",
                "web-search",
                "multimodal",
                "function-calling"
            ]
        }
