from fastapi import APIRouter, Depends
from ...application.services import OptimizationService
from ...infrastructure.llm import LMStudioClient
from ..schemas import HealthResponse

router = APIRouter(tags=["health"])


def get_optimization_service() -> OptimizationService:
    """Dependency injection for optimization service."""
    llm_client = LMStudioClient()
    return OptimizationService(llm_client)


@router.get("/health", response_model=HealthResponse)
async def health_check(
    service: OptimizationService = Depends(get_optimization_service)
):
    """
    Health check endpoint.

    Returns the service status and LM Studio availability.
    """
    lm_studio_available = await service.health_check()

    return HealthResponse(
        status="healthy",
        lm_studio_available=lm_studio_available,
        vendor_adapters=6  # OpenAI, Claude, Grok, Gemini, Qwen, DeepSeek
    )
