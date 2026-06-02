"""FastAPI dependency providers — the single place services get constructed."""
from app.services.ai_review.review_service import ReviewService
from app.services.cv_parsing.parser_service import ParserService


def get_parser_service() -> ParserService:
    return ParserService()


def get_review_service() -> ReviewService:
    return ReviewService()
