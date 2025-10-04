from ..interfaces import IVendorAdapter
from ..models import VendorType


class GrokAdapter(IVendorAdapter):
    """Grok-specific prompt optimization (xAI Grok 4)."""

    @property
    def vendor_type(self) -> VendorType:
        return VendorType.GROK

    def get_system_instructions(self) -> str:
        return """You are optimizing prompts for xAI Grok 4 models.

CRITICAL RULES:
1. **Language Detection**: Detect the user's original prompt language
2. **Response Language**: Add "Respond in [detected language]" at the END
3. **Prompt Language**: Write optimized prompt in ENGLISH
4. **Real-Time Focus**: Grok has web/X search - use it for current events
5. **Conversational Tone**: Grok responds well to direct, conversational prompts

Grok 4 best practices:
- Grok has 2M token context (grok-4-fast) or 128K (grok-4)
- Native real-time web and X (Twitter) search integration
- Great for current events, trending topics, and real-time information
- Conversational and engaging tone works best
- Can use tools natively - specify if you need web search
- Direct instructions work better than complex formatting

Example transformations:
User (Spanish): "noticias sobre IA"
Optimized: "You are a tech journalist. Search the web for the latest AI news from today. Summarize the top \
5 most significant developments, including: what happened, why it matters, and key players involved. Prioritize \
breaking news and major announcements. Respond in Spanish."

User (English): "explain cryptocurrency trends"
Optimized: "You are a financial analyst with access to real-time market data. Explain current cryptocurrency \
market trends. Include: 1) Recent price movements of major coins, 2) Market sentiment analysis, 3) Key factors \
driving current trends. Use web search to get the latest data. Keep explanations clear and data-driven. Respond \
in English."

Return ONLY the enhanced prompt."""

    def get_enhancement_notes(self) -> str:
        return (
            "Enhanced for Grok 4: Real-time information focus, web/X search integration, conversational tone. "
            "Optimized for current events and trending topics."
        )

    def get_metadata(self) -> dict:
        return {
            "vendor": "grok",
            "format": "conversational",
            "temperature_recommendation": (
                "0.8 for balanced, 1.0+ for creative/engaging content"
            ),
            "model_recommendation": (
                "grok-4 (best intelligence, 128K), grok-4-fast (40% efficient, 2M context), "
                "grok-4-heavy (SuperGrok tier)"
            ),
            "features": ["real-time-search", "X-integration", "2M-context", "native-tool-use"]
        }
