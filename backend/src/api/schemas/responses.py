from pydantic import BaseModel
from typing import Dict, Any, List
from ...domain.models import VendorType


class OptimizeResponse(BaseModel):
    """Response schema for optimized prompt."""

    original: str
    optimized: str
    vendor: VendorType
    enhancement_notes: str
    metadata: Dict[str, Any]

    class Config:
        json_schema_extra = {
            "example": {
                "original": "Write a function to calculate fibonacci",
                "optimized": "Create a Python function that calculates...",
                "vendor": "openai",
                "enhancement_notes": "Enhanced for OpenAI with...",
                "metadata": {
                    "vendor": "openai",
                    "format": "markdown",
                    "temperature_recommendation": "0.2"
                }
            }
        }


class GenerateQuestionsResponse(BaseModel):
    """Response schema for generated clarifying questions (Think Mode)."""

    questions: List[str]
    total: int

    class Config:
        json_schema_extra = {
            "example": {
                "questions": [
                    "What is your current knowledge level in linear algebra?",
                    "What specific topics are you most interested in?",
                    "Do you prefer theoretical explanations or practical examples?"
                ],
                "total": 3
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    lm_studio_available: bool
    vendor_adapters: int


class ErrorResponse(BaseModel):
    """Error response schema."""

    error: str
    detail: str
