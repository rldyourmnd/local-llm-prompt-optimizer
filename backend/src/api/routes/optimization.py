from fastapi import APIRouter, HTTPException, Depends
from ...application.services import OptimizationService
from ...domain.models import OptimizationRequest as DomainOptimizationRequest
from ...domain.exceptions import (
    VendorNotSupportedException,
    OptimizationFailedException,
    QuestionGenerationFailedException
)
from ..schemas import (
    OptimizeRequest,
    OptimizeResponse,
    GenerateQuestionsRequest,
    GenerateQuestionsResponse,
    OptimizeWithAnswersRequest
)

router = APIRouter(prefix="/api", tags=["optimization"])


def get_optimization_service() -> OptimizationService:
    """Dependency injection for optimization service."""
    from ..main import container
    return container.optimization_service()


@router.post("/optimize", response_model=OptimizeResponse)
async def optimize_prompt(
    request: OptimizeRequest,
    service: OptimizationService = Depends(get_optimization_service)
):
    """
    Optimize a prompt for a specific LLM vendor.

    This endpoint takes a user prompt and optimizes it according to best practices
    for the specified vendor (OpenAI, Claude, Grok, Gemini, Qwen, or DeepSeek).
    """
    try:
        # Convert API request to domain model
        domain_request = DomainOptimizationRequest(
            original_prompt=request.prompt,
            target_vendor=request.vendor,
            context=request.context,
            max_length=request.max_length
        )

        # Optimize the prompt
        result = await service.optimize_prompt(domain_request)

        # Convert domain model to API response
        return OptimizeResponse(
            original=result.original,
            optimized=result.optimized,
            vendor=result.vendor,
            enhancement_notes=result.enhancement_notes,
            metadata=result.metadata
        )

    except VendorNotSupportedException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except OptimizationFailedException as e:
        raise HTTPException(status_code=500, detail=e.message)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")


@router.post("/think/generate-questions", response_model=GenerateQuestionsResponse)
async def generate_questions(
    request: GenerateQuestionsRequest,
    service: OptimizationService = Depends(get_optimization_service)
):
    """
    Generate clarifying questions for Think Mode.

    This endpoint generates 5, 10, or 25 clarifying questions to better understand
    the user's intent and create the perfect optimized prompt.
    """
    try:
        questions = await service.generate_questions(
            prompt=request.prompt,
            vendor=request.vendor,
            num_questions=request.num_questions
        )

        return GenerateQuestionsResponse(
            questions=questions,
            total=len(questions)
        )

    except QuestionGenerationFailedException as e:
        raise HTTPException(status_code=500, detail=e.message)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Question generation failed: {str(e)}")


@router.post("/think/optimize-with-answers", response_model=OptimizeResponse)
async def optimize_with_answers(
    request: OptimizeWithAnswersRequest,
    service: OptimizationService = Depends(get_optimization_service)
):
    """
    Optimize a prompt using user's answers to clarifying questions (Think Mode).

    This endpoint takes the original prompt, the questions that were asked,
    and the user's answers to generate a perfectly optimized prompt.
    """
    try:
        # Validate that questions and answers have the same length
        if len(request.questions) != len(request.answers):
            raise ValueError("Number of questions and answers must match")

        # Optimize with answers
        result = await service.optimize_with_answers(
            prompt=request.prompt,
            vendor=request.vendor,
            questions=request.questions,
            answers=request.answers,
            context=request.context
        )

        # Convert domain model to API response
        return OptimizeResponse(
            original=result.original,
            optimized=result.optimized,
            vendor=result.vendor,
            enhancement_notes=result.enhancement_notes,
            metadata=result.metadata
        )

    except VendorNotSupportedException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except OptimizationFailedException as e:
        raise HTTPException(status_code=500, detail=e.message)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization with answers failed: {str(e)}")
