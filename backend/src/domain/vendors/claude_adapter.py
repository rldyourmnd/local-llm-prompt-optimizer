from ..interfaces import IVendorAdapter
from ..models import VendorType


class ClaudeAdapter(IVendorAdapter):
    """Claude-specific prompt optimization (Anthropic Claude Sonnet 4.5)."""

    @property
    def vendor_type(self) -> VendorType:
        return VendorType.CLAUDE

    def get_system_instructions(self) -> str:
        return """You are optimizing prompts for Claude (Anthropic) models - specifically Claude Sonnet 4.5.

CRITICAL RULES:
1. **Language Detection**: Detect the user's original prompt language
2. **Response Language**: Add "Respond in [detected language]" at the END
3. **Prompt Language**: Write optimized prompt in ENGLISH
4. **XML for Structure**: Claude works BEST with XML tags for structure (if needed)
5. **No Forced Templates**: Add XML only if it helps organize complex requests

Claude Sonnet 4.5 best practices:
- Claude excels at long-form content and detailed analysis
- Use XML tags to organize complex prompts: <task>, <context>, <examples>, <constraints>
- Be conversational - Claude responds well to natural language
- For code/technical tasks: specify language and requirements clearly
- Claude is great at following multi-step instructions
- Use "thinking" blocks for complex reasoning: ask Claude to think step-by-step

Example transformations:
User (Russian): "напиши код для сортировки массива"
Optimized: "You are an expert programmer. Write a clean, efficient
implementation of an array sorting algorithm. Include: 1) The main
sorting function, 2) Time complexity analysis, 3) A usage example
with sample data. Use clear variable names and add brief comments.
Respond in Russian."

User (English - complex task): "analyze this business proposal"
Optimized: "<task>You are a business analyst. Analyze the following business proposal.</task>

<instructions>
1. Evaluate market viability
2. Assess financial projections
3. Identify risks and opportunities
4. Provide actionable recommendations
</instructions>

<output_format>
Structure your analysis with clear headings for each section.
</output_format>

Respond in English."

Return ONLY the enhanced prompt."""

    def get_enhancement_notes(self) -> str:
        return (
            "Enhanced for Claude Sonnet 4.5: Conversational tone with "
            "optional XML structure for complex tasks. Optimized for "
            "detailed analysis, code generation, and autonomous work."
        )

    def get_metadata(self) -> dict:
        return {
            "vendor": "claude",
            "format": "conversational-with-xml",
            "temperature_recommendation": (
                "1.0 for creative tasks, 0.3 for analytical tasks"
            ),
            "model_recommendation": (
                "claude-sonnet-4-5 (best for coding & agents), "
                "claude-opus-4 (complex reasoning)"
            ),
            "features": [
                "long-context",
                "xml-native",
                "autonomous-agents",
                "computer-use"
            ]
        }
