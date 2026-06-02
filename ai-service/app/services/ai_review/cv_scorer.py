"""Mock CV scorer for Sprint 1.

Returns fixed category scores. Later this calls the LLM layer (via an injected
LLMProvider) to produce real scores; the interface stays the same.
"""
from app.schemas.score_schema import CategoryScores


class CVScorer:
    def score(self, cv_text: str, job_description: str | None = None) -> CategoryScores:
        return CategoryScores(format=80, ats=75, skills=85, projects=80, experience=78)

    @staticmethod
    def overall(scores: CategoryScores) -> int:
        values = list(scores.model_dump().values())
        return round(sum(values) / len(values))
