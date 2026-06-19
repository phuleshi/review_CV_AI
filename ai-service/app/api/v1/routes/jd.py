"""JD matching route: POST /api/v1/match-jd."""
from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_jd_matching_service
from app.schemas.jd_schema import MatchJDRequest, MatchJDResponse
from app.services.jd_matching.jd_matching_service import JDMatchingService

router = APIRouter()


@router.post("/match-jd", response_model=MatchJDResponse, tags=["jd"])
async def match_jd(
    payload: MatchJDRequest,
    service: Annotated[JDMatchingService, Depends(get_jd_matching_service)],
) -> MatchJDResponse:
    return service.match(payload.cv_text, payload.job_description)
