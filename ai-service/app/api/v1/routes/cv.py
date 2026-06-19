"""CV parsing routes.

  * POST /api/v1/parse-cv       — normalize raw text (JSON body).
  * POST /api/v1/parse-cv-file  — upload a PDF/DOCX and get the unified CV JSON.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile

from app.api.deps import get_parser_service
from app.core.exceptions import CVParsingError
from app.schemas.cv_schema import ParseCVRequest, ParseCVResponse
from app.services.cv_parsing.parser_service import ParserService

router = APIRouter()


@router.post("/parse-cv", response_model=ParseCVResponse, tags=["cv"])
async def parse_cv(
    payload: ParseCVRequest,
    service: Annotated[ParserService, Depends(get_parser_service)],
) -> ParseCVResponse:
    return service.parse(payload.raw_text)


@router.post("/parse-cv-file", response_model=ParseCVResponse, tags=["cv"])
async def parse_cv_file(
    file: Annotated[UploadFile, File(...)],
    service: Annotated[ParserService, Depends(get_parser_service)],
) -> ParseCVResponse:
    content = await file.read()
    if not content:
        raise CVParsingError("Uploaded file is empty")
    return service.parse_file(content, file.filename or "", file.content_type)
