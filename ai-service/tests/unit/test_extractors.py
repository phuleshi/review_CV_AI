"""Unit tests for the PDF/DOCX text extractors and the file parsing pipeline."""
import io

import pytest
from docx import Document

from app.core.exceptions import CVParsingError
from app.services.cv_parsing.docx_parser import DOCXParser
from app.services.cv_parsing.parser_service import ParserService
from app.services.cv_parsing.pdf_parser import PDFParser
from tests.fixtures.render import make_docx, make_pdf
from tests.fixtures.sample_cvs import SAMPLE_CVS

_CV = SAMPLE_CVS["senior_backend"]


# -- PDF -------------------------------------------------------------------
def test_pdf_extractor_recovers_text():
    text = PDFParser().extract(make_pdf(_CV))
    assert "John Carter" in text
    assert "Senior Backend Engineer" in text


def test_pdf_extractor_rejects_empty_bytes():
    with pytest.raises(CVParsingError):
        PDFParser().extract(b"")


def test_pdf_extractor_rejects_non_pdf():
    with pytest.raises(CVParsingError):
        PDFParser().extract(b"this is not a pdf")


# -- DOCX ------------------------------------------------------------------
def test_docx_extractor_recovers_text():
    text = DOCXParser().extract(make_docx(_CV))
    assert "John Carter" in text
    assert "PostgreSQL" in text


def test_docx_extractor_reads_table_cells():
    doc = Document()
    table = doc.add_table(rows=1, cols=2)
    table.rows[0].cells[0].text = "Email"
    table.rows[0].cells[1].text = "jane@example.com"
    buf = io.BytesIO()
    doc.save(buf)

    text = DOCXParser().extract(buf.getvalue())
    assert "jane@example.com" in text


def test_docx_extractor_rejects_garbage():
    with pytest.raises(CVParsingError):
        DOCXParser().extract(b"not a docx file")


# -- full file -> CV JSON pipeline -----------------------------------------
def test_parse_file_pdf_end_to_end():
    resp = ParserService().parse_file(make_pdf(_CV), "cv.pdf", "application/pdf")
    assert resp.sections.personal_info["name"] == "John Carter"
    assert resp.sections.experience
    assert "Python" in resp.sections.skills


def test_parse_file_docx_end_to_end():
    resp = ParserService().parse_file(make_docx(_CV), "cv.docx")
    assert resp.sections.personal_info["email"] == "john.carter@example.com"
    assert resp.sections.skills


def test_parse_file_routes_by_extension_when_no_content_type():
    resp = ParserService().parse_file(make_docx(_CV), "resume.DOCX", None)
    assert resp.sections.personal_info["name"] == "John Carter"


def test_parse_file_rejects_unsupported_type():
    with pytest.raises(CVParsingError):
        ParserService().parse_file(b"hello", "cv.txt", "text/plain")
