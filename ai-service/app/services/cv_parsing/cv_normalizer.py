"""Mock CV normalizer for Sprint 1.

Turns raw text into the CVSections shape. Real section extraction (NLP / LLM)
replaces this later; the public `parse` signature stays the same.
"""
import re

from app.domain.interfaces.parser import CVParser
from app.schemas.cv_schema import CVSections

_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_PHONE_RE = re.compile(r"(?:\+?\d[\d\s().-]{7,}\d)")


class CVNormalizer(CVParser):
    def parse(self, raw_text: str) -> CVSections:
        text = raw_text.strip()
        personal_info: dict[str, str] = {}

        email = _EMAIL_RE.search(text)
        if email:
            personal_info["email"] = email.group(0)

        phone = _PHONE_RE.search(text)
        if phone:
            personal_info["phone"] = phone.group(0).strip()

        # Mock: real parsing of education/experience/etc. comes later.
        return CVSections(personal_info=personal_info)
