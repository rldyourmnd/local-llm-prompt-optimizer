import httpx
from typing import List, Dict, Optional
from ...domain.interfaces import ILLMClient
from ..config import settings


class LMStudioClient(ILLMClient):
    """OpenAI-compatible LM Studio client."""

    def __init__(self):
        self.base_url = settings.lm_studio_base_url
        self.api_key = settings.lm_studio_api_key
        self.model = settings.lm_studio_model
        self.timeout = settings.request_timeout_seconds

    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """Generate text using LM Studio."""
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": settings.lm_studio_top_p
        }

        if self.model:
            payload["model"] = self.model

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def health_check(self) -> bool:
        """Check if LM Studio is available."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url.rsplit('/v1', 1)[0]}/v1/models")
                return response.status_code == 200
        except Exception:
            return False
