"""Mock CV scorer for Sprint 1.

Returns fixed category scores (each on the canonical 0-20 scale). Later this
calls the LLM layer (via an injected LLMProvider) to produce real scores; the
interface and the output shape stay the same.
"""
from app.schemas.score_schema import CategoryScores


class CVScorer:
    def score(self, cv_text: str, job_description: str | None = None) -> CategoryScores:
        return CategoryScores(structure=16, skills=17, experience=15, projects=16, ats=15)

    @staticmethod
    def overall(scores: CategoryScores) -> int:
        # overall_score is the sum of categories (each /20) → 0-100.
        return scores.total()
