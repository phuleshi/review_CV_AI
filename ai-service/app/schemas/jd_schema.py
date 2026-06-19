"""Request/response schemas for JD (job description) matching."""
from pydantic import BaseModel, Field


class MatchJDRequest(BaseModel):
    cv_text: str = Field(..., min_length=1, description="CV content")
    job_description: str = Field(..., min_length=1, description="Target job description")


class MatchJDResponse(BaseModel):
    match_score: int = Field(..., ge=0, le=100, description="CV↔JD skill fit (0-100)")
    matched_skills: list[str] = Field(
        default_factory=list, description="JD skills also found in the CV"
    )
    missing_skills: list[str] = Field(
        default_factory=list, description="JD skills not found in the CV"
    )
    recommendations: list[str] = Field(default_factory=list)
