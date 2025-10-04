"""Vendor Registry for dynamic adapter management."""

from typing import Dict, Type
from ..interfaces import IVendorAdapter
from ..models import VendorType
from ..exceptions import VendorNotSupportedException


class VendorRegistry:
    """Registry for vendor adapters following Registry pattern."""

    _adapters: Dict[VendorType, IVendorAdapter] = {}

    @classmethod
    def register(cls, adapter_class: Type[IVendorAdapter]) -> None:
        """Register a vendor adapter."""
        if not issubclass(adapter_class, IVendorAdapter):
            raise TypeError(f"{adapter_class.__name__} must implement IVendorAdapter")

        adapter = adapter_class()
        cls._adapters[adapter.vendor_type] = adapter

    @classmethod
    def get(cls, vendor: VendorType) -> IVendorAdapter:
        """Get adapter for vendor."""
        if vendor not in cls._adapters:
            raise VendorNotSupportedException(f"No adapter registered for vendor: {vendor.value}")
        return cls._adapters[vendor]

    @classmethod
    def all(cls) -> Dict[VendorType, IVendorAdapter]:
        """Get all registered adapters."""
        return cls._adapters.copy()

    @classmethod
    def is_registered(cls, vendor: VendorType) -> bool:
        """Check if vendor is registered."""
        return vendor in cls._adapters

    @classmethod
    def count(cls) -> int:
        """Get count of registered adapters."""
        return len(cls._adapters)

    @classmethod
    def clear(cls) -> None:
        """Clear all registered adapters (for testing)."""
        cls._adapters.clear()
