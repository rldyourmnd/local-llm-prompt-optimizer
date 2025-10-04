from abc import ABC, abstractmethod
from ..models import VendorType


class IVendorAdapter(ABC):
    """Interface for vendor-specific prompt optimization guidance."""

    @property
    @abstractmethod
    def vendor_type(self) -> VendorType:
        """Get the vendor type this adapter handles."""
        pass

    @abstractmethod
    def get_system_instructions(self) -> str:
        """
        Get vendor-specific system instructions for the LLM optimizer.

        These instructions guide the LLM on how to optimize prompts for this vendor.
        Should include:
        - Best practices for the vendor
        - Language detection and response language handling
        - Formatting preferences
        - What to avoid
        """
        pass

    @abstractmethod
    def get_enhancement_notes(self) -> str:
        """
        Get human-readable notes about what enhancements were applied.

        Returns a description of optimizations specific to this vendor.
        """
        pass

    @abstractmethod
    def get_metadata(self) -> dict:
        """
        Get vendor-specific metadata and recommendations.

        Returns a dictionary with:
        - vendor: str
        - format: str
        - temperature_recommendation: str
        - model_recommendation: str
        - features: list[str]
        """
        pass
