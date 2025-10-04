from pydantic import BaseModel, Field
from typing import Optional, List
from ...domain.models import VendorType


class OptimizeRequest(BaseModel):
    """Request schema for prompt optimization."""

    prompt: str = Field(..., min_length=1, description="The original prompt to optimize")
    vendor: VendorType = Field(..., description="Target LLM vendor")
    context: Optional[str] = Field(None, description="Additional context for optimization")
    max_length: Optional[int] = Field(None, gt=0, description="Maximum length constraint")

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Write a function to calculate fibonacci",
                "vendor": "openai",
                "context": "This is for a Python tutorial",
                "max_length": 500
            }
        }


class GenerateQuestionsRequest(BaseModel):
    """Request schema for generating clarifying questions (Think Mode)."""

    prompt: str = Field(..., min_length=1, description="The original user prompt")
    vendor: VendorType = Field(..., description="Target LLM vendor")
    num_questions: int = Field(..., ge=5, le=25, description="Number of questions to generate (5, 10, or 25)")

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "расскажи мне про линейную алгебру",
                "vendor": "openai",
                "num_questions": 10
            }
        }


class OptimizeWithAnswersRequest(BaseModel):
    """Request schema for optimization with user answers to clarifying questions."""

    prompt: str = Field(..., min_length=1, description="The original user prompt")
    vendor: VendorType = Field(..., description="Target LLM vendor")
    questions: List[str] = Field(..., min_items=1, description="List of questions that were asked")
    answers: List[str] = Field(..., min_items=1, description="User's answers to the questions")
    context: Optional[str] = Field(None, description="Additional context")

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "расскажи мне про линейную алгебру",
                "vendor": "openai",
                "questions": ["What is your current level?", "What topics do you want to focus on?"],
                "answers": ["Beginner", "Vectors and matrices"]
            }
        }
