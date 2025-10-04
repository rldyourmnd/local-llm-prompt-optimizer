from fastapi import APIRouter, Depends
from ...application.services import OptimizationService
from ...infrastructure.di import Container
from ...domain.registries import VendorRegistry
from ..schemas import HealthResponse

router = APIRouter(tags=["health"])

container = Container()


def get_optimization_service() -> OptimizationService:
    """Dependency injection for optimization service."""
    return container.optimization_service()


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
        vendor_adapters=VendorRegistry.count()
    )
