"""JD Matching Engine.

Pipeline:  CV + JD  ->  Skill Extraction  ->  Gap Analysis  ->  Match Score.

Deterministic and explainable: the score is the share of JD-required skills the
CV demonstrates, gap analysis is a straight set difference, and recommendations
are derived from the gaps. No LLM call — fast, free, reproducible. (The review
engine's ``jd_match`` block remains the LLM-flavoured, qualitative counterpart.)
"""
from app.core.exceptions import AIServiceError
from app.core.logging import get_logger
from app.schemas.jd_schema import MatchJDResponse
from app.services.jd_matching.skill_extractor import extract_skills

logger = get_logger(__name__)

# Cap how many missing skills we turn into individual recommendations.
_MAX_MISSING_RECS = 5


class JDMatchError(AIServiceError):
    status_code = 422


class JDMatchingService:
    def match(self, cv_text: str, job_description: str) -> MatchJDResponse:
        if not cv_text.strip() or not job_description.strip():
            raise JDMatchError("cv_text and job_description must not be empty")

        cv_skills = set(extract_skills(cv_text))
        jd_skills = extract_skills(job_description)  # ordered list

        matched = [s for s in jd_skills if s in cv_skills]
        missing = [s for s in jd_skills if s not in cv_skills]
        score = self._score(matched, jd_skills)

        logger.info(
            "JD match: %d/%d skills matched (score=%d)",
            len(matched),
            len(jd_skills),
            score,
        )
        return MatchJDResponse(
            match_score=score,
            matched_skills=matched,
            missing_skills=missing,
            recommendations=self._recommendations(matched, missing, jd_skills, score),
        )

    @staticmethod
    def _score(matched: list[str], jd_skills: list[str]) -> int:
        if not jd_skills:
            return 0
        return round(100 * len(matched) / len(jd_skills))

    @staticmethod
    def _recommendations(
        matched: list[str],
        missing: list[str],
        jd_skills: list[str],
        score: int,
    ) -> list[str]:
        recs: list[str] = []

        if not jd_skills:
            recs.append(
                "No recognized skills were found in the job description; "
                "matching is limited. Provide a more detailed JD."
            )
            return recs

        for skill in missing[:_MAX_MISSING_RECS]:
            recs.append(
                f"Add or highlight '{skill}' — it is required by the JD but not "
                f"found in your CV."
            )

        if len(missing) > _MAX_MISSING_RECS:
            extra = len(missing) - _MAX_MISSING_RECS
            recs.append(f"Address {extra} more missing skill(s) from the JD.")

        if matched:
            top = ", ".join(matched[:3])
            recs.append(
                f"Emphasize your matching strengths ({top}) prominently near the top."
            )

        if score >= 80:
            recs.append("Strong overall fit — tailor your summary to mirror the JD wording.")
        elif score < 50:
            recs.append(
                "Significant skill gap — consider upskilling or targeting roles "
                "closer to your current profile."
            )

        return recs
