"""Heuristic LLM stand-in for Sprint 1.

Implements the LLMProvider port but instead of calling a real model it derives a
*grounded* review from signals actually present in the CV (section headers, metrics,
known tech keywords, links). This keeps the full engine pipeline exercised
end-to-end (prompt → provider → JSON string → parse → validate) without an API key,
and guarantees no hallucination: every score and comment traces to detected text.

Swap `LLM_PROVIDER=openai` to replace this with a real model — the engine, schema,
and parser are unchanged.
"""
import json
import re

from app.domain.interfaces.llm_provider import LLMProvider

# Small keyword set drawn from kb/*_skillmap.md — enough to differentiate CVs in
# Sprint 1. The real model uses the full knowledge base.
_TECH_KEYWORDS = {
    "javascript", "typescript", "react", "next.js", "nextjs", "vue", "angular",
    "html", "css", "tailwind", "redux", "node", "node.js", "express", "nestjs",
    "python", "fastapi", "django", "flask", "java", "spring", "go", "golang",
    "c#", ".net", "sql", "postgresql", "mysql", "mongodb", "redis", "graphql",
    "docker", "kubernetes", "aws", "gcp", "azure", "git", "ci/cd", "rest",
    "kafka", "rabbitmq", "terraform", "prisma", "typeorm", "sqlalchemy",
}
_SECTION_HEADERS = ("summary", "experience", "skills", "education", "projects", "certification")
_ACTION_VERBS = (
    "led", "built", "designed", "implemented", "developed", "created", "improved",
    "reduced", "increased", "launched", "migrated", "optimized", "shipped", "owned",
)


def _extract_cv(prompt: str) -> str:
    """Pull the CV body out of the built prompt (between the ## CV markers)."""
    m = re.search(r"## CV\s*\"\"\"(.*?)\"\"\"", prompt, re.DOTALL)
    return (m.group(1) if m else prompt).strip()


def _found(text: str, items) -> list[str]:
    return [k for k in items if k in text]


class HeuristicLLMProvider(LLMProvider):
    async def complete(self, prompt: str, *, temperature: float = 0.2) -> str:
        cv = _extract_cv(prompt)
        text = cv.lower()

        headers = _found(text, _SECTION_HEADERS)
        techs = _found(text, _TECH_KEYWORDS)
        verbs = _found(text, _ACTION_VERBS)
        metrics = re.findall(r"\b\d+%|\$\d|\b\d{2,}\b", cv)
        has_links = bool(re.search(r"github\.com|https?://|gitlab\.com", text))
        has_email = bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", cv))
        has_bullets = bool(re.search(r"(^|\n)\s*[-•*]", cv))
        word_count = len(cv.split())

        # ---- category scores (each 0-20), grounded in the signals above ----
        structure = 8
        structure += 4 if len(headers) >= 4 else len(headers)
        structure += 2 if has_bullets else 0
        structure += 2 if 150 <= word_count <= 900 else 0
        structure = min(20, structure)

        skills = 6 + min(12, len(techs) * 2)
        skills += 2 if "skills" in headers else 0
        skills = min(20, skills)

        experience = 6
        experience += 4 if "experience" in headers else 0
        experience += min(6, len(verbs) * 2)
        experience += min(4, len(metrics) * 2)
        experience = min(20, experience)

        projects = 5
        projects += 5 if "projects" in headers else 0
        projects += 4 if has_links else 0
        projects += 2 if len(techs) >= 4 else 0
        projects = min(20, projects)

        ats = 10
        ats += 3 if len(headers) >= 4 else 0
        ats += 2 if has_email else 0
        ats += min(5, len(techs))
        ats = min(20, ats)

        scores = {
            "structure": structure,
            "skills": skills,
            "experience": experience,
            "projects": projects,
            "ats": ats,
        }
        overall = sum(scores.values())

        # ---- grounded feedback ----
        strengths, weaknesses, suggestions = [], [], []

        if len(techs) >= 4:
            strengths.append(f"Relevant technical stack detected ({', '.join(techs[:6])}).")
        if metrics and verbs:
            strengths.append("Experience includes action verbs and quantified results.")
        if has_links:
            strengths.append("Projects include links, making the work verifiable.")
        if len(headers) >= 4:
            strengths.append("Clear section structure that is easy to scan.")

        if not metrics:
            weaknesses.append("No quantified achievements — impact is hard to gauge.")
            suggestions.append("Add metrics to experience bullets (%, $, users, time saved).")
        if not verbs:
            weaknesses.append("Experience reads as duties rather than achievements.")
            suggestions.append("Rewrite bullets as 'action verb + result + metric'.")
        if not has_links and "projects" in headers:
            weaknesses.append("Projects lack repo/demo links.")
            suggestions.append("Add a GitHub repo or live demo link to each project.")
        if "summary" not in headers:
            weaknesses.append("No professional summary at the top.")
            suggestions.append("Add a 2-3 line summary tailored to the target role.")
        if len(techs) < 4:
            weaknesses.append("Skills section is thin or not clearly listed.")
            suggestions.append("Group concrete skills into languages / frameworks / tools.")
        if not has_bullets:
            suggestions.append("Use concise bullet points instead of paragraphs.")

        # Guarantee the minimums the schema/guidelines expect.
        strengths = strengths or ["CV content was readable and parseable."]
        weaknesses = weaknesses or ["Minor polish opportunities only."]
        suggestions = suggestions or ["Tailor keywords to each target role/JD."]

        band = (
            "strong" if overall >= 85 else
            "solid" if overall >= 70 else
            "average" if overall >= 55 else
            "early-stage"
        )
        top = max(scores, key=scores.get)
        summary = (
            f"A {band} CV scoring {overall}/100, strongest in {top}. "
            f"Biggest wins: {suggestions[0].lower()}"
        )

        return json.dumps(
            {
                "schema_version": "1.0",
                "overall_score": overall,
                "category_scores": scores,
                "strengths": strengths,
                "weaknesses": weaknesses,
                "suggestions": suggestions,
                "summary": summary,
                "jd_match": None,
            }
        )
