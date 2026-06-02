"""Schema for the health-check endpoint."""
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "ai-service"
