"""Application service orchestrating CV parsing. Routers call this, not parsers.

Two entry points:
  * ``parse`` — normalize already-extracted plain text.
  * ``parse_file`` — extract text from PDF/DOCX bytes, then normalize.
Both return the same unified ``ParseCVResponse``.
"""
from pathlib import PurePath

from app.core.exceptions import CVParsingError
from app.core.logging import get_logger
from app.domain.interfaces.extractor import TextExtractor
from app.domain.interfaces.parser import CVParser
from app.schemas.cv_schema import ParseCVResponse
from app.services.cv_parsing.cv_normalizer import CVNormalizer
from app.services.cv_parsing.docx_parser import DOCXParser
from app.services.cv_parsing.pdf_parser import PDFParser

logger = get_logger(__name__)


class ParserService:
    def __init__(
        self,
        normalizer: CVParser | None = None,
        extractors: list[TextExtractor] | None = None,
    ) -> None:
        self._normalizer = normalizer or CVNormalizer()
        self._extractors = extractors or [PDFParser(), DOCXParser()]

    def parse(self, raw_text: str) -> ParseCVResponse:
        if not raw_text.strip():
            raise CVParsingError("raw_text must not be empty")
        logger.info("Normalizing CV (%d chars)", len(raw_text))
        sections = self._normalizer.parse(raw_text)
        return ParseCVResponse(sections=sections)

    def parse_file(
        self, content: bytes, filename: str, content_type: str | None = None
    ) -> ParseCVResponse:
        extractor = self._select_extractor(filename, content_type)
        text = extractor.extract(content)
        logger.info("Parsing CV file %r via %s", filename, type(extractor).__name__)
        return self.parse(text)

    def _select_extractor(
        self, filename: str, content_type: str | None
    ) -> TextExtractor:
        suffix = PurePath(filename or "").suffix.lower()
        for extractor in self._extractors:
            if suffix and suffix in extractor.suffixes:
                return extractor
            if content_type and content_type in extractor.content_types:
                return extractor
        supported = sorted({s for e in self._extractors for s in e.suffixes})
        raise CVParsingError(
            f"Unsupported file type {suffix or content_type!r}. "
            f"Supported: {', '.join(supported)}"
        )
