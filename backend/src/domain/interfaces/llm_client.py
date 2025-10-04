from abc import ABC, abstractmethod
from typing import List, Dict


class ILLMClient(ABC):
    """Interface for LLM client implementations."""

    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """Generate text from messages."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if LLM service is available."""
        pass
