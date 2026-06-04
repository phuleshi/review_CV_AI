"""AI Review Engine tests — runs the full CV → Prompt → LLM → JSON pipeline.

Covers the Sprint-1 requirement: at least 5 CVs through the engine, all producing
valid, internally-consistent, grounded output; plus the fallback and JSON-parsing
edge cases.
"""
import pytest

from app.llm.base import MockLLMProvider
from app.llm.heuristic_provider import HeuristicLLMProvider
from app.schemas.review_schema import ReviewCVRequest, ReviewCVResponse
from app.services.ai_review.output_parser import ReviewParseError, parse_review_output
from app.services.ai_review.review_service import ReviewService
from tests.fixtures.sample_cvs import SAMPLE_CVS


def _engine() -> ReviewService:
    # Explicit heuristic provider so the test is independent of env config.
    return ReviewService(llm=HeuristicLLMProvider())


def _assert_valid(resp: ReviewCVResponse) -> None:
    assert resp.schema_version == "1.0"
    cats = resp.category_scores.model_dump()
    assert set(cats) == {"structure", "skills", "experience", "projects", "ats"}
    for v in cats.values():
        assert 0 <= v <= 20
    # overall_score is always the sum of categories.
    assert resp.overall_score == sum(cats.values())
    assert 0 <= resp.overall_score <= 100
    assert resp.summary
    assert resp.strengths and resp.weaknesses and resp.suggestions


@pytest.mark.parametrize("name", list(SAMPLE_CVS))
async def test_engine_produces_valid_output_for_each_cv(name):
    resp = await _engine().review(ReviewCVRequest(cv_text=SAMPLE_CVS[name]))
    _assert_valid(resp)


async def test_engine_differentiates_strong_vs_weak():
    eng = _engine()
    strong = await eng.review(ReviewCVRequest(cv_text=SAMPLE_CVS["senior_backend"]))
    weak = await eng.review(ReviewCVRequest(cv_text=SAMPLE_CVS["weak_no_metrics"]))
    assert strong.overall_score > weak.overall_score


async def test_scores_are_grounded_in_cv_content():
    eng = _engine()
    # CV with quantified metrics should out-score one with none on experience.
    with_metrics = await eng.review(ReviewCVRequest(cv_text=SAMPLE_CVS["senior_backend"]))
    no_metrics = await eng.review(ReviewCVRequest(cv_text=SAMPLE_CVS["weak_no_metrics"]))
    assert with_metrics.category_scores.experience > no_metrics.category_scores.experience
    # Junior CV with repo links should score projects highly.
    junior = await eng.review(ReviewCVRequest(cv_text=SAMPLE_CVS["junior_projects"]))
    assert junior.category_scores.projects >= 12


async def test_deterministic_same_cv_same_score():
    eng = _engine()
    cv = SAMPLE_CVS["mid_frontend"]
    a = await eng.review(ReviewCVRequest(cv_text=cv))
    b = await eng.review(ReviewCVRequest(cv_text=cv))
    assert a.model_dump() == b.model_dump()


async def test_engine_falls_back_on_bad_llm_output():
    # MockLLMProvider returns "[mock-llm-response]" — not JSON → fallback path.
    eng = ReviewService(llm=MockLLMProvider())
    resp = await eng.review(ReviewCVRequest(cv_text=SAMPLE_CVS["mid_frontend"]))
    _assert_valid(resp)  # still a valid response despite unusable LLM output


async def test_empty_cv_rejected():
    from app.core.exceptions import ReviewError

    with pytest.raises(ReviewError):
        await _engine().review(ReviewCVRequest.model_construct(cv_text="   "))


# ---- output_parser edge cases ----

def test_parser_extracts_json_from_code_fence():
    raw = '```json\n{"category_scores":{"structure":18,"skills":17,"experience":15,' \
          '"projects":16,"ats":16},"strengths":["a"],"weaknesses":["b"],' \
          '"suggestions":["c"],"summary":"ok"}\n```'
    resp = parse_review_output(raw, jd_provided=False)
    assert resp.overall_score == 18 + 17 + 15 + 16 + 16
    assert resp.jd_match is None


def test_parser_recomputes_and_clamps_overall():
    # Model lies about overall and over-ranges a category; parser fixes both.
    raw = '{"overall_score":999,"category_scores":{"structure":25,"skills":17,' \
          '"experience":15,"projects":16,"ats":16},"summary":"x"}'
    resp = parse_review_output(raw, jd_provided=False)
    assert resp.category_scores.structure == 20  # clamped from 25
    assert resp.overall_score == 20 + 17 + 15 + 16 + 16


def test_parser_populates_jd_match_when_provided():
    raw = '{"category_scores":{"structure":18,"skills":17,"experience":15,' \
          '"projects":16,"ats":16},"summary":"x","jd_match":{"match_score":80,' \
          '"matched_skills":["python"],"missing_skills":["go"],"notes":"good fit"}}'
    resp = parse_review_output(raw, jd_provided=True)
    assert resp.jd_match is not None
    assert resp.jd_match.match_score == 80
    assert resp.jd_match.matched_skills == ["python"]


def test_parser_raises_on_garbage():
    with pytest.raises(ReviewParseError):
        parse_review_output("no json here at all", jd_provided=False)
