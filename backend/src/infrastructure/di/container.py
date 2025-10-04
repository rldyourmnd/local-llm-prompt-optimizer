"""Dependency Injection Container."""

from dependency_injector import containers, providers
from ...domain.vendors import (
    OpenAIAdapter, ClaudeAdapter, GrokAdapter,
    GeminiAdapter, QwenAdapter, DeepSeekAdapter
)
from ...domain.registries import VendorRegistry
from ..llm import LMStudioClient
from ...application.services import OptimizationService


class Container(containers.DeclarativeContainer):
    """Application Dependency Injection Container."""

    config = providers.Configuration()

    llm_client = providers.Singleton(LMStudioClient)

    openai_adapter = providers.Singleton(OpenAIAdapter)
    claude_adapter = providers.Singleton(ClaudeAdapter)
    grok_adapter = providers.Singleton(GrokAdapter)
    gemini_adapter = providers.Singleton(GeminiAdapter)
    qwen_adapter = providers.Singleton(QwenAdapter)
    deepseek_adapter = providers.Singleton(DeepSeekAdapter)

    optimization_service = providers.Factory(
        OptimizationService,
        llm_client=llm_client
    )

    @classmethod
    def initialize_vendor_registry(cls):
        """Initialize vendor registry with all adapters."""
        VendorRegistry.register(OpenAIAdapter)
        VendorRegistry.register(ClaudeAdapter)
        VendorRegistry.register(GrokAdapter)
        VendorRegistry.register(GeminiAdapter)
        VendorRegistry.register(QwenAdapter)
        VendorRegistry.register(DeepSeekAdapter)
