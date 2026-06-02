"""CV review route: POST /api/v1/review-cv."""
from fastapi import APIRouter, Depends

from app.api.deps import get_review_service
from app.schemas.review_schema import ReviewCVRequest, ReviewCVResponse
from app.services.ai_review.review_service import ReviewService

router = APIRouter()


@router.post("/review-cv", response_model=ReviewCVResponse, tags=["review"])
async def review_cv(
    payload: ReviewCVRequest,
    service: ReviewService = Depends(get_review_service),
) -> ReviewCVResponse:
    return service.review(payload)
