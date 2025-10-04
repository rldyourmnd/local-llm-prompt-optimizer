from ...domain.models import VendorType, OptimizationRequest, OptimizedPrompt
from ...domain.interfaces import ILLMClient, IVendorAdapter
from ...domain.registries import VendorRegistry


class OptimizationService:
    """Application service for prompt optimization."""

    def __init__(self, llm_client: ILLMClient):
        self.llm_client = llm_client

    async def optimize_prompt(self, request: OptimizationRequest) -> OptimizedPrompt:
        """Optimize a prompt for a specific vendor."""

        # Get vendor adapter from registry
        adapter = VendorRegistry.get(request.target_vendor)

        # Generate optimized prompt using LLM with vendor-specific guidance
        optimized_prompt = await self._generate_base_optimization(request, adapter)

        # Return result with metadata (no additional structure added)
        return OptimizedPrompt(
            original=request.original_prompt,
            optimized=optimized_prompt,
            vendor=request.target_vendor,
            enhancement_notes=adapter.get_enhancement_notes(),
            metadata=adapter.get_metadata()
        )

    async def _generate_base_optimization(
        self,
        request: OptimizationRequest,
        adapter: IVendorAdapter
    ) -> str:
        """Generate base optimization using LLM."""

        system_message = f"""You are an expert prompt engineer. \
Your task is to improve user prompts for LLM interactions.

{adapter.get_system_instructions()}

Key principles:
- Make prompts clear and unambiguous
- Add necessary context and constraints
- Structure information logically
- Optimize for the target LLM vendor's strengths
- Preserve the user's intent while enhancing effectiveness"""

        user_message = f"""Original prompt to optimize:
{request.original_prompt}

Target vendor: {request.target_vendor.value}
{f"Additional context: {request.context}" if request.context else ""}
{f"Max length constraint: {request.max_length} characters" if request.max_length else ""}

Provide an improved version of this prompt optimized for {request.target_vendor.value}."""

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        result = await self.llm_client.generate(
            messages=messages,
            temperature=0.3,  # Lower temperature for more consistent optimization
            max_tokens=2048
        )

        return result.strip()

    async def health_check(self) -> bool:
        """Check if the optimization service is healthy."""
        return await self.llm_client.health_check()

    async def generate_questions(
        self,
        prompt: str,
        vendor: VendorType,
        num_questions: int
    ) -> list[str]:
        """Generate clarifying questions for Think Mode."""

        system_message = (
            f"You are an expert prompt engineer. Generate exactly {num_questions} clarifying questions to "
            f"better understand the user's intent and create the perfect prompt.\n"
            "\n"
            "CRITICAL RULES:\n"
            "- DETECT the language of the user's original prompt\n"
            "- Generate questions in THE SAME LANGUAGE as the user's prompt\n"
            "- Ask questions that will significantly improve the final prompt\n"
            "- Focus on: user's knowledge level, specific goals, preferred format, depth of detail, context\n"
            "- Questions should be concise and specific\n"
            f"- Return ONLY the questions, numbered 1-{num_questions}\n"
            "- Each question on a new line\n"
            "- No additional text or explanations\n"
            "\n"
            "Example:\n"
            'If user\'s prompt is in Russian: "расскажи про физику"\n'
            'Generate questions in Russian: "1. Какой у вас текущий уровень знаний физики?"\n'
            "\n"
            'If user\'s prompt is in English: "tell me about physics"\n'
            'Generate questions in English: "1. What is your current knowledge level in physics?"\n'
        )

        user_message = f"""User's original prompt: "{prompt}"
Target vendor: {vendor.value}

Generate {num_questions} essential questions to optimize this prompt perfectly."""

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        result = await self.llm_client.generate(
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )

        # Parse questions from numbered list
        questions = []
        for line in result.strip().split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                # Remove numbering and clean up
                question = line.lstrip('0123456789.-• \t')
                if question:
                    questions.append(question)

        return questions[:num_questions]  # Ensure we return exactly the requested number

    async def optimize_with_answers(
        self,
        prompt: str,
        vendor: VendorType,
        questions: list[str],
        answers: list[str],
        context: str | None = None
    ) -> OptimizedPrompt:
        """Optimize prompt with user's answers to clarifying questions."""

        # Get vendor adapter from registry
        adapter = VendorRegistry.get(vendor)

        # Build Q&A context
        qa_context = "\n".join([
            f"Q: {q}\nA: {a}"
            for q, a in zip(questions, answers)
        ])

        system_message = (
            f"You are an expert prompt engineer. Create the PERFECT optimized prompt using the user's "
            f"answers to clarifying questions.\n"
            f"\n"
            f"{adapter.get_system_instructions()}\n"
            f"\n"
            f"Use the Q&A to deeply understand what the user wants and create an ideal prompt."
        )

        user_message = f"""Original prompt: "{prompt}"
Target vendor: {vendor.value}

Clarifying Q&A:
{qa_context}

{f"Additional context: {context}" if context else ""}

Create the PERFECT optimized prompt for {vendor.value} based on all this information."""

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        optimized_prompt = await self.llm_client.generate(
            messages=messages,
            temperature=0.3,
            max_tokens=2048
        )

        return OptimizedPrompt(
            original=prompt,
            optimized=optimized_prompt.strip(),
            vendor=vendor,
            enhancement_notes=(
                f"{adapter.get_enhancement_notes()} Enhanced with {len(questions)} clarifying questions "
                f"for precision."
            ),
            metadata=adapter.get_metadata()
        )
