"""Request/response schemas for CV review.

This is the canonical AI Output Schema for the platform. FE renders it, BE
validates it, the AI Service produces it. Versioned via ``schema_version`` so
clients can evolve safely. The optional ``jd_match`` block is the extension point
for JD Matching (Sprint 2) and stays ``null`` until a job description is provided.
"""
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from app.schemas.score_schema import CategoryScores

SCHEMA_VERSION = "1.0"


class ReviewCVRequest(BaseModel):
    cv_text: str = Field(..., min_length=1, description="CV content to review")
    job_description: str | None = Field(
        default=None, description="Optional JD to tailor the review against"
    )

    @model_validator(mode="before")
    @classmethod
    def normalize_backend_payload(cls, data: Any) -> Any:
        """Accept common BE/FE variants while keeping one internal contract."""
        if not isinstance(data, dict):
            return data

        normalized = dict(data)
        aliases = {
            "cv_text": ("cvText", "cv", "raw_text", "rawText"),
            "job_description": ("jobDescription", "jd", "job_desc", "jobDesc"),
        }
        for canonical, candidates in aliases.items():
            if canonical in normalized:
                continue
            for candidate in candidates:
                if candidate in normalized:
                    normalized[canonical] = normalized[candidate]
                    break
        return normalized

    @field_validator("cv_text", "job_description", mode="before")
    @classmethod
    def strip_text_fields(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.strip()
        return value


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
