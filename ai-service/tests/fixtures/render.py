"""Render plain CV text into real PDF / DOCX bytes for parser round-trip tests.

These produce genuine files (not stubs) so the extractors are exercised exactly
as they would be on an uploaded CV.
"""
import io

from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def make_pdf(text: str) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    _, height = letter
    y = height - 50
    for line in text.split("\n"):
        if y < 50:  # new page when we run out of vertical space
            c.showPage()
            y = height - 50
        c.drawString(50, y, line)
        y -= 14
    c.save()
    return buf.getvalue()


def make_docx(text: str) -> bytes:
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()
