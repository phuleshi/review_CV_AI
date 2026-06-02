"""Port for LLM providers. Implementations live in app/llm.

Sprint 1 does not call any real provider — this contract exists so the review
service can later depend on an abstraction instead of a concrete vendor SDK.
"""
from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    async def complete(self, prompt: str, *, temperature: float = 0.2) -> str:
        """Return the model's text completion for a prompt."""
        raise NotImplementedError
