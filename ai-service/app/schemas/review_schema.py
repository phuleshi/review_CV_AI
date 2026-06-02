"""Request/response schemas for CV review."""
from pydantic import BaseModel, Field

from app.schemas.score_schema import CategoryScores


class ReviewCVRequest(BaseModel):
    cv_text: str = Field(..., min_length=1, description="CV content to review")
    job_description: str | None = Field(
        default=None, description="Optional JD to tailor the review against"
    )


class ReviewCVResponse(BaseModel):
    overall_score: int = Field(..., ge=0, le=100)
    category_scores: CategoryScores
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    summary: str
