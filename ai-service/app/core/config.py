"""Application settings loaded from environment variables / .env file."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "INFO"

    # Security: shared secret the NestJS backend sends on internal calls.
    internal_api_key: str = "change-me"

    # LLM (Sprint 1 uses "mock" — no real provider call yet)
    llm_provider: str = "mock"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    llm_timeout_seconds: int = 60
    llm_max_retries: int = 3


@lru_cache
def get_settings() -> Settings:
    """Cached singleton so env is parsed once per process."""
    return Settings()
