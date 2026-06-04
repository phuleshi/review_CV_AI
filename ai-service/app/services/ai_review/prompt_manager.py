"""Build the review prompt sent to the LLM.

Mirrors prompts/review_prompt_v1.md in code so the engine has a single, testable
source for the prompt string. When RAG lands (Sprint 2), retrieved kb/ snippets are
injected via ``kb_context`` without changing the engine or the schema.
"""

PROMPT_VERSION = "v1"

SYSTEM_PROMPT = (
    "You are an expert technical recruiter and CV reviewer for software engineering "
    "roles. You evaluate CVs strictly, fairly, and consistently using the provided "
    "rubric. Judge ONLY what is written in the CV; never invent experience, skills, "
    "employers, dates, metrics, or projects. If information is missing, treat it as "
    "missing and lower the relevant score. Be seniority-aware. Output MUST be a single "
    "valid JSON object matching the schema exactly — no prose, no markdown, no fences."
)

_RUBRIC = (
    "## Scoring rubric (score each category 0-20; overall_score = sum = 0-100)\n"
    "- structure  (0-20): layout, sections, length, readability, consistency\n"
    "- skills     (0-20): relevance, depth, and organization of skills\n"
    "- experience (0-20): impact, clarity, and progression of work history\n"
    "- projects   (0-20): quality, relevance, and depth of projects\n"
    "- ats        (0-20): ATS / keyword compatibility & machine-readability\n"
    "Band per category: 18-20 excellent, 14-17 good, 10-13 average, 5-9 weak, 0-4 poor."
)

_GUIDELINES = (
    "## Guidelines\n"
    "- strengths: 2-5 specific, evidence-based positives.\n"
    "- weaknesses: 3-6 concrete issues, each tied to a category.\n"
    "- suggestions: 3-6 independently actionable fixes, ordered by impact.\n"
    "- summary: 2-3 sentences (seniority, strongest area, top 1-2 fixes)."
)

_OUTPUT_NO_JD = (
    "## Output — return ONLY this JSON object:\n"
    '{"schema_version":"1.0","overall_score":<int 0-100 == sum of category_scores>,'
    '"category_scores":{"structure":<0-20>,"skills":<0-20>,"experience":<0-20>,'
    '"projects":<0-20>,"ats":<0-20>},"strengths":[<string>],"weaknesses":[<string>],'
    '"suggestions":[<string>],"summary":<string>,"jd_match":null}'
)

_OUTPUT_JD = (
    "## Output — return ONLY this JSON object:\n"
    '{"schema_version":"1.0","overall_score":<int 0-100 == sum of category_scores>,'
    '"category_scores":{"structure":<0-20>,"skills":<0-20>,"experience":<0-20>,'
    '"projects":<0-20>,"ats":<0-20>},"strengths":[<string>],"weaknesses":[<string>],'
    '"suggestions":[<string>],"summary":<string>,'
    '"jd_match":{"match_score":<0-100>,"matched_skills":[<string>],'
    '"missing_skills":[<string>],"notes":<string>}}'
)


class PromptManager:
    def build_review_prompt(
        self,
        cv_text: str,
        job_description: str | None = None,
        kb_context: str | None = None,
    ) -> str:
        parts = [
            SYSTEM_PROMPT,
            "",
            "Review the following CV and return the JSON described below.",
            "",
            _RUBRIC,
            "",
            _GUIDELINES,
        ]

        if job_description:
            parts += [
                "",
                "## Target job description",
                "Judge `skills` and `ats` against this JD's keywords. Note matched and "
                "missing skills for the jd_match block.",
                '"""',
                job_description.strip(),
                '"""',
            ]

        if kb_context:  # Sprint 2 (RAG) — empty in Sprint 1.
            parts += ["", "## Reference knowledge", kb_context.strip()]

        parts += [
            "",
            "## CV",
            '"""',
            cv_text.strip(),
            '"""',
            "",
            _OUTPUT_JD if job_description else _OUTPUT_NO_JD,
        ]
        return "\n".join(parts)
