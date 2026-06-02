"""Mock feedback generator for Sprint 1.

Returns canned strengths/weaknesses/suggestions/summary. Later this is backed by
the LLM layer + prompt templates in app/services/prompts.
"""


class FeedbackGenerator:
    def generate(self, cv_text: str, job_description: str | None = None) -> dict:
        return {
            "strengths": [
                "Clear, well-structured layout",
                "Relevant technical skills listed",
            ],
            "weaknesses": [
                "Work experience lacks measurable impact",
                "No tailored summary for the target role",
            ],
            "suggestions": [
                "Quantify achievements with numbers and outcomes",
                "Add a short professional summary at the top",
                "Align keywords with the job description for better ATS matching",
            ],
            "summary": (
                "A solid CV with strong fundamentals. Focus on quantifying impact "
                "and tailoring content to the target role to stand out further."
            ),
        }
