"""Application service orchestrating CV parsing. Routers call this, not parsers."""
from app.core.exceptions import CVParsingError
from app.core.logging import get_logger
from app.domain.interfaces.parser import CVParser
from app.schemas.cv_schema import ParseCVResponse
from app.services.cv_parsing.cv_normalizer import CVNormalizer

logger = get_logger(__name__)


class ParserService:
    def __init__(self, parser: CVParser | None = None) -> None:
        # Default to the mock normalizer; swap for PDF/DOCX parsers later.
        self._parser = parser or CVNormalizer()

    def parse(self, raw_text: str) -> ParseCVResponse:
        if not raw_text.strip():
            raise CVParsingError("raw_text must not be empty")
        logger.info("Parsing CV (%d chars)", len(raw_text))
        sections = self._parser.parse(raw_text)
        return ParseCVResponse(sections=sections)
