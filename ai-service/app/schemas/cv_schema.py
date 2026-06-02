"""Request/response schemas for CV parsing."""
from typing import Any

from pydantic import BaseModel, Field


class ParseCVRequest(BaseModel):
    raw_text: str = Field(..., min_length=1, description="Raw CV text to parse")


class CVSections(BaseModel):
    """Normalized CV structure. Lists stay loosely typed in Sprint 1 and will be
    tightened (e.g. Education/Experience models) once real parsing lands."""

    personal_info: dict[str, Any] = Field(default_factory=dict)
    education: list[Any] = Field(default_factory=list)
    experience: list[Any] = Field(default_factory=list)
    skills: list[Any] = Field(default_factory=list)
    projects: list[Any] = Field(default_factory=list)
    certifications: list[Any] = Field(default_factory=list)


class ParseCVResponse(BaseModel):
    sections: CVSections
