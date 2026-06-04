"""Request/response schemas for CV review.

This is the canonical AI Output Schema for the platform. FE renders it, BE
validates it, the AI Service produces it. Versioned via ``schema_version`` so
clients can evolve safely. The optional ``jd_match`` block is the extension point
for JD Matching (Sprint 2) and stays ``null`` until a job description is provided.
"""
from pydantic import BaseModel, Field

from app.schemas.score_schema import CategoryScores

SCHEMA_VERSION = "1.0"


class ReviewCVRequest(BaseModel):
    cv_text: str = Field(..., min_length=1, description="CV content to review")
    job_description: str | None = Field(
        default=None, description="Optional JD to tailor the review against"
    )


class JDMatch(BaseModel):
    """JD Matching result. Populated only when a job description is supplied.
    Reserved/extensible for Sprint 2 (RAG + Pinecone)."""

    match_score: int = Field(..., ge=0, le=100, description="Overall CV↔JD fit (0-100)")
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    notes: str = ""


class ReviewCVResponse(BaseModel):
    schema_version: str = Field(default=SCHEMA_VERSION, description="Output schema version")
    overall_score: int = Field(..., ge=0, le=100, description="Sum of category_scores")
    category_scores: CategoryScores
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    summary: str = Field(..., description="Short overall verdict for the candidate")
    jd_match: JDMatch | None = Field(
        default=None, description="JD Matching result; null when no JD provided"
    )
