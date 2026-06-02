"""OpenAI implementation of the LLMProvider port.

Stub for Sprint 1 — wiring the real SDK call (with retry from app.llm.retry)
happens in a later sprint. Intentionally does not import the openai SDK yet so
module import stays cheap and side-effect free.
"""
from app.core.config import get_settings
from app.domain.interfaces.llm_provider import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self) -> None:
        settings = get_settings()
        self._api_key = settings.openai_api_key
        self._model = settings.openai_model

    async def complete(self, prompt: str, *, temperature: float = 0.2) -> str:
        raise NotImplementedError("OpenAI integration arrives in a later sprint")
