"""Health-check route (mounted at root: GET /health)."""
from fastapi import APIRouter

from app.schemas.health_schema import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["health"])
async def health() -> HealthResponse:
    return HealthResponse(status="ok", service="ai-service")
