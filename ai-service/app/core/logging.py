"""Basic logging configuration for the AI service."""
import logging
import sys

from app.core.config import get_settings

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def setup_logging() -> None:
    """Configure root logger once at app startup."""
    settings = get_settings()
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logging.basicConfig(level=level, format=_LOG_FORMAT, stream=sys.stdout)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
