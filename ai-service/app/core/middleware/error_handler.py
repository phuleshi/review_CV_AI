"""Central exception handlers so routers never build error responses themselves."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AIServiceError
from app.core.logging import get_logger

logger = get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AIServiceError)
    async def _handle_service_error(_: Request, exc: AIServiceError) -> JSONResponse:
        logger.warning("Service error (%s): %s", exc.status_code, exc.message)
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.message, "type": exc.__class__.__name__},
        )

    @app.exception_handler(Exception)
    async def _handle_unexpected(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled error")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "type": "InternalError"},
        )
