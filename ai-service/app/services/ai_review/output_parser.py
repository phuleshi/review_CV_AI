"""Parse + sanitize raw LLM output into a valid ReviewCVResponse.

The model is instructed to return pure JSON, but we never trust it: we extract the
JSON object, coerce/clamp values, recompute overall_score so it is always internally
consistent, and validate against the Pydantic schema. Any failure raises
ReviewParseError so the caller can fall back.
"""
import json
import re

from pydantic import ValidationError

from app.schemas.review_schema import JDMatch, ReviewCVResponse
from app.schemas.score_schema import CATEGORY_MAX, CATEGORY_NAMES


class ReviewParseError(Exception):
    """Raised when raw LLM output cannot be turned into a valid review."""


def _extract_json_object(raw: str) -> dict:
    """Pull the first balanced ``{...}`` object out of arbitrary model text.

    Tolerates ```json fences, leading prose, and trailing commentary.
    """
    if not raw or not raw.strip():
        raise ReviewParseError("empty LLM output")

    # Fast path: the whole thing is JSON.
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Strip code fences then scan for the first balanced object.
    text = re.sub(r"```(?:json)?", "", raw)
    start = text.find("{")
    if start == -1:
        raise ReviewParseError("no JSON object found in LLM output")

    depth = 0
    for i in range(start, len(text)):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                candidate = text[start : i + 1]
                try:
                    return json.loads(candidate)
                except json.JSONDecodeError as exc:
                    raise ReviewParseError(f"malformed JSON object: {exc}") from exc
    raise ReviewParseError("unbalanced JSON object in LLM output")


def _clamp(value: object, lo: int, hi: int) -> int:
    try:
        return max(lo, min(hi, int(round(float(value)))))  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return lo


def _first(data: dict, *keys: str, default: object = None) -> object:
    for key in keys:
        if key in data:
            return data[key]
    return default


def _normalize_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def _coerce_str_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        # Some providers return newline or comma separated prose instead of arrays.
        parts = re.split(r"\n|;|,", value)
        return [part.strip(" -\t") for part in parts if part.strip(" -\t")]
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _normalize_scores(data: dict) -> dict[str, int]:
    score_aliases = (
        "category_scores",
        "categoryScores",
        "scores",
        "score_breakdown",
        "scoreBreakdown",
    )
    raw_scores = _first(data, *score_aliases, default={})
    if not isinstance(raw_scores, dict):
        raise ReviewParseError("category_scores missing or not an object")

    score_key_map = {_normalize_key(key): key for key in raw_scores}
    aliases = {
        "structure": ("structure", "format", "formatting", "layout", "readability"),
        "skills": ("skills", "technicalskills", "skillmatch"),
        "experience": ("experience", "workexperience", "employment", "impact"),
        "projects": ("projects", "project", "portfolio"),
        "ats": ("ats", "atscompatibility", "keywords", "keywordmatch"),
    }

    scores: dict[str, int] = {}
    for canonical in CATEGORY_NAMES:
        value = raw_scores.get(canonical)
        if value is None:
            for alias in aliases[canonical]:
                actual_key = score_key_map.get(_normalize_key(alias))
                if actual_key is not None:
                    value = raw_scores[actual_key]
                    break
        scores[canonical] = _clamp(value, 0, CATEGORY_MAX)
    return scores


def _normalize_jd_match(data: dict) -> JDMatch | None:
    raw = _first(data, "jd_match", "jdMatch", "job_match", "jobMatch", "match", default=None)
    if not isinstance(raw, dict):
        return None

    return JDMatch(
        match_score=_clamp(_first(raw, "match_score", "matchScore", "score"), 0, 100),
        matched_skills=_coerce_str_list(_first(raw, "matched_skills", "matchedSkills")),
        missing_skills=_coerce_str_list(_first(raw, "missing_skills", "missingSkills")),
        notes=str(_first(raw, "notes", "summary", "rationale", default="") or "").strip(),
    )


def parse_review_output(raw: str, *, jd_provided: bool) -> ReviewCVResponse:
    """Turn raw LLM text into a validated, internally-consistent ReviewCVResponse."""
    data = _extract_json_object(raw)
    if not isinstance(data, dict):
        raise ReviewParseError("LLM output is not a JSON object")

    # Clamp each category to 0-CATEGORY_MAX; recompute overall as the sum so the
    # total is always consistent regardless of the model's arithmetic.
    scores = _normalize_scores(data)
    overall = sum(scores.values())

    jd_match = _normalize_jd_match(data) if jd_provided else None

    try:
        return ReviewCVResponse(
            overall_score=overall,
            category_scores=scores,  # type: ignore[arg-type]
            strengths=_coerce_str_list(_first(data, "strengths", "pros")),
            weaknesses=_coerce_str_list(_first(data, "weaknesses", "cons", "issues")),
            suggestions=_coerce_str_list(_first(data, "suggestions", "recommendations", "actions")),
            summary=str(_first(data, "summary", "overall_summary", "overallSummary") or "").strip()
            or "No summary provided.",
            jd_match=jd_match,
        )
    except ValidationError as exc:
        raise ReviewParseError(f"schema validation failed: {exc}") from exc
