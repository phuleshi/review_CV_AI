"""Score schemas shared by the review response.

Canonical scoring contract for the whole system (FE / BE / AI). Each of the five
categories is scored out of 20 so they sum to a 0-100 ``overall_score``. Keep the
field set and the max-per-category in sync with ``kb/scoring_rubric.md`` and
``docs/api_contract.md``.
"""
from pydantic import BaseModel, Field

# Max points per category. They sum to 100 (the overall_score scale).
CATEGORY_MAX = 20
CATEGORY_NAMES = ("structure", "skills", "experience", "projects", "ats")


class CategoryScores(BaseModel):
    """Per-category breakdown. Every category is on the same 0-20 scale so the FE
    can render them uniformly and the sum equals ``overall_score``."""

    structure: int = Field(..., ge=0, le=CATEGORY_MAX, description="Layout, sections, readability")
    skills: int = Field(..., ge=0, le=CATEGORY_MAX, description="Relevance & depth of skills")
    experience: int = Field(
        ...,
        ge=0,
        le=CATEGORY_MAX,
        description="Impact & clarity of work history",
    )
    projects: int = Field(..., ge=0, le=CATEGORY_MAX, description="Quality & relevance of projects")
    ats: int = Field(..., ge=0, le=CATEGORY_MAX, description="ATS / keyword compatibility")

    def total(self) -> int:
        """Sum of all categories == overall_score (0-100)."""
        return sum(self.model_dump().values())
