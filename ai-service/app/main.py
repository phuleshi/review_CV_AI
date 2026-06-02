"""FastAPI application entrypoint.

Run locally:  uvicorn app.main:app --reload
"""
from fastapi import FastAPI

from app.api.router import api_v1_router, root_router
from app.core.config import get_settings
from app.core.logging import get_logger, setup_logging
from app.core.middleware.error_handler import register_exception_handlers

setup_logging()
logger = get_logger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="AI CV Reviewer — AI Service",
        version="0.1.0",
        description="FastAPI microservice for CV parsing and AI review.",
    )

    register_exception_handlers(app)
    app.include_router(root_router)
    app.include_router(api_v1_router)

    logger.info("AI Service initialized (env=%s, llm=%s)", settings.app_env, settings.llm_provider)
    return app


app = create_app()
