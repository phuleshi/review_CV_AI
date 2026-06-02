"""Select an LLM provider based on configuration (multi-LLM extension point)."""
from app.core.config import get_settings
from app.domain.interfaces.llm_provider import LLMProvider
from app.llm.base import MockLLMProvider


def get_llm_provider() -> LLMProvider:
    provider = get_settings().llm_provider.lower()

    if provider == "openai":
        # Imported lazily so the SDK is only required when actually selected.
        from app.llm.openai_provider import OpenAIProvider

        return OpenAIProvider()

    # Default (Sprint 1): mock.
    return MockLLMProvider()
