"""PDF text extraction using pypdf."""
import io

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from app.core.exceptions import CVParsingError
from app.core.logging import get_logger
from app.domain.interfaces.extractor import TextExtractor

logger = get_logger(__name__)


class PDFParser(TextExtractor):
    suffixes = (".pdf",)
    content_types = ("application/pdf",)

    def extract(self, content: bytes) -> str:
        if not content:
            raise CVParsingError("PDF file is empty")
        try:
            reader = PdfReader(io.BytesIO(content))
            pages = [page.extract_text() or "" for page in reader.pages]
        except (PdfReadError, ValueError, OSError) as exc:
            raise CVParsingError(f"Could not read PDF: {exc}") from exc

        text = "\n".join(pages).strip()
        if not text:
            raise CVParsingError(
                "No extractable text in PDF (it may be a scanned image)"
            )
        logger.info("Extracted %d chars from %d-page PDF", len(text), len(pages))
        return text
