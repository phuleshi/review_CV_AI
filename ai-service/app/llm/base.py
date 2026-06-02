"""Mock LLM provider used in Sprint 1 to keep the contract exercised end-to-end."""
from app.domain.interfaces.llm_provider import LLMProvider


class MockLLMProvider(LLMProvider):
    async def complete(self, prompt: str, *, temperature: float = 0.2) -> str:
        return "[mock-llm-response]"
