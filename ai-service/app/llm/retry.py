"""Retry helper for LLM calls. Not wired into the mock flow yet — provided so the
real OpenAIProvider can decorate its network calls in a later sprint.
"""
from app.core.config import get_settings


def llm_retry():
    """Return a tenacity retry decorator configured from settings.

    Imported lazily so `tenacity` is only needed when retries are actually used.
    """
    from tenacity import retry, stop_after_attempt, wait_exponential

    settings = get_settings()
    return retry(
        stop=stop_after_attempt(settings.llm_max_retries),
        wait=wait_exponential(multiplier=1, max=10),
        reraise=True,
    )
