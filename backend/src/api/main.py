from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routes import optimization_router, health_router
from ..infrastructure.config import settings
import logging

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Local LLM Prompt Optimizer",
    description="Optimize prompts for different LLM vendors using local LM Studio",
    version="1.0.2",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(optimization_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Local LLM Prompt Optimizer API",
        "version": "1.0.2",
        "docs": "/api/docs",
        "health": "/health",
        "credits": {
            "author": "Danil Silantyev",
            "telegram": "@Danil_Silantyev",
            "company": "NDDev OpenNetwork",
            "website": "https://nddev.tech"
        }
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc) if settings.app_env == "development" else "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_env == "development"
    )
