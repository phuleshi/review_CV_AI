"""Application service orchestrating CV review (scoring + feedback)."""
from app.core.exceptions import ReviewError
from app.core.logging import get_logger
from app.schemas.review_schema import ReviewCVRequest, ReviewCVResponse
from app.services.ai_review.cv_scorer import CVScorer
from app.services.ai_review.feedback_generator import FeedbackGenerator

logger = get_logger(__name__)


class ReviewService:
    def __init__(
        self,
        scorer: CVScorer | None = None,
        feedback: FeedbackGenerator | None = None,
    ) -> None:
        self._scorer = scorer or CVScorer()
        self._feedback = feedback or FeedbackGenerator()

    def review(self, request: ReviewCVRequest) -> ReviewCVResponse:
        if not request.cv_text.strip():
            raise ReviewError("cv_text must not be empty", status_code=422)

        logger.info("Reviewing CV (jd_provided=%s)", request.job_description is not None)
        scores = self._scorer.score(request.cv_text, request.job_description)
        feedback = self._feedback.generate(request.cv_text, request.job_description)

        return ReviewCVResponse(
            overall_score=self._scorer.overall(scores),
            category_scores=scores,
            **feedback,
        )
