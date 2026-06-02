"""CV parsing route: POST /api/v1/parse-cv."""
from fastapi import APIRouter, Depends

from app.api.deps import get_parser_service
from app.schemas.cv_schema import ParseCVRequest, ParseCVResponse
from app.services.cv_parsing.parser_service import ParserService

router = APIRouter()


@router.post("/parse-cv", response_model=ParseCVResponse, tags=["cv"])
async def parse_cv(
    payload: ParseCVRequest,
    service: ParserService = Depends(get_parser_service),
) -> ParseCVResponse:
    return service.parse(payload.raw_text)
