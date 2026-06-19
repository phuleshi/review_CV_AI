"""Request/response schemas for CV parsing.

The normalized CV is the single, unified shape every downstream consumer
(review engine, future JD matcher) reads. Lists are typed so callers can rely
on a stable structure regardless of the source format (PDF / DOCX / raw text).
"""
from typing import Any

from pydantic import BaseModel, Field


class ParseCVRequest(BaseModel):
    raw_text: str = Field(..., min_length=1, description="Raw CV text to parse")


class ExperienceItem(BaseModel):
    title: str | None = None
    company: str | None = None
    period: str | None = None
    highlights: list[str] = Field(default_factory=list)


class EducationItem(BaseModel):
    degree: str | None = None
    institution: str | None = None
    period: str | None = None


class ProjectItem(BaseModel):
    name: str | None = None
    description: str | None = None
    tech: list[str] = Field(default_factory=list)


class CVSections(BaseModel):
    """Normalized, source-agnostic CV structure."""

    personal_info: dict[str, Any] = Field(default_factory=dict)
    education: list[EducationItem] = Field(default_factory=list)
    experience: list[ExperienceItem] = Field(default_factory=list)
    projects: list[ProjectItem] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)


class ParseCVResponse(BaseModel):
    sections: CVSections
