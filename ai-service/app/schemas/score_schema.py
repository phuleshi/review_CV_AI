"""Score schemas shared by the review response."""
from pydantic import BaseModel, Field


class CategoryScores(BaseModel):
    format: int = Field(..., ge=0, le=100)
    ats: int = Field(..., ge=0, le=100)
    skills: int = Field(..., ge=0, le=100)
    projects: int = Field(..., ge=0, le=100)
    experience: int = Field(..., ge=0, le=100)
