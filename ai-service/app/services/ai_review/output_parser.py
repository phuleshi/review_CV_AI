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


def parse_review_output(raw: str, *, jd_provided: bool) -> ReviewCVResponse:
    """Turn raw LLM text into a validated, internally-consistent ReviewCVResponse."""
    data = _extract_json_object(raw)
    if not isinstance(data, dict):
        raise ReviewParseError("LLM output is not a JSON object")

    raw_scores = data.get("category_scores") or {}
    if not isinstance(raw_scores, dict):
        raise ReviewParseError("category_scores missing or not an object")

    # Clamp each category to 0-CATEGORY_MAX; recompute overall as the sum so the
    # total is always consistent regardless of the model's arithmetic.
    scores = {name: _clamp(raw_scores.get(name), 0, CATEGORY_MAX) for name in CATEGORY_NAMES}
    overall = sum(scores.values())

    def _str_list(key: str) -> list[str]:
        items = data.get(key) or []
        if not isinstance(items, list):
            return []
        return [str(x).strip() for x in items if str(x).strip()]

    jd_match = None
    if jd_provided and isinstance(data.get("jd_match"), dict):
        jm = data["jd_match"]
        jd_match = JDMatch(
            match_score=_clamp(jm.get("match_score"), 0, 100),
            matched_skills=[str(x) for x in (jm.get("matched_skills") or []) if str(x).strip()],
            missing_skills=[str(x) for x in (jm.get("missing_skills") or []) if str(x).strip()],
            notes=str(jm.get("notes") or ""),
        )

    try:
        return ReviewCVResponse(
            overall_score=overall,
            category_scores=scores,  # type: ignore[arg-type]
            strengths=_str_list("strengths"),
            weaknesses=_str_list("weaknesses"),
            suggestions=_str_list("suggestions"),
            summary=str(data.get("summary") or "").strip() or "No summary provided.",
            jd_match=jd_match,
        )
    except ValidationError as exc:
        raise ReviewParseError(f"schema validation failed: {exc}") from exc
