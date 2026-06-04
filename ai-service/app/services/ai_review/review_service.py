"""AI Review Engine — orchestrates the CV → Prompt → LLM → JSON flow.

    cv_text (+ optional JD)
        → PromptManager builds the review prompt
        → LLMProvider.complete() returns raw text
        → output_parser validates + sanitizes into ReviewCVResponse

If the LLM output can't be parsed/validated, the engine falls back to the mock
scorer + feedback so the API always returns a valid response (MVP-first). The LLM
provider is injected, so swapping the heuristic stand-in for OpenAI (or adding RAG
context to the prompt) needs no change here.
"""
from app.core.exceptions import ReviewError
from app.core.logging import get_logger
from app.domain.interfaces.llm_provider import LLMProvider
from app.llm.factory import get_llm_provider
from app.schemas.review_schema import ReviewCVRequest, ReviewCVResponse
from app.services.ai_review.cv_scorer import CVScorer
from app.services.ai_review.feedback_generator import FeedbackGenerator
from app.services.ai_review.output_parser import ReviewParseError, parse_review_output
from app.services.ai_review.prompt_manager import PromptManager

logger = get_logger(__name__)


class ReviewService:
    def __init__(
        self,
        llm: LLMProvider | None = None,
        prompt_manager: PromptManager | None = None,
        scorer: CVScorer | None = None,
        feedback: FeedbackGenerator | None = None,
    ) -> None:
        self._llm = llm or get_llm_provider()
        self._prompts = prompt_manager or PromptManager()
        self._scorer = scorer or CVScorer()
        self._feedback = feedback or FeedbackGenerator()

    async def review(self, request: ReviewCVRequest) -> ReviewCVResponse:
        if not request.cv_text.strip():
            raise ReviewError("cv_text must not be empty", status_code=422)

        jd_provided = bool(request.job_description and request.job_description.strip())
        logger.info("Reviewing CV (jd_provided=%s)", jd_provided)

        prompt = self._prompts.build_review_prompt(request.cv_text, request.job_description)
        try:
            raw = await self._llm.complete(prompt, temperature=0.2)
            return parse_review_output(raw, jd_provided=jd_provided)
        except ReviewParseError as exc:
            logger.warning("LLM output unusable (%s); falling back to mock review", exc)
            return self._fallback(request)

    def _fallback(self, request: ReviewCVRequest) -> ReviewCVResponse:
        """Deterministic mock review — keeps the API contract intact on LLM failure."""
        scores = self._scorer.score(request.cv_text, request.job_description)
        feedback = self._feedback.generate(request.cv_text, request.job_description)
        return ReviewCVResponse(
            overall_score=self._scorer.overall(scores),
            category_scores=scores,
            **feedback,
        )
