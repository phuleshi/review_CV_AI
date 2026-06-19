"""Heuristic CV normalizer: plain text -> unified CVSections.

The strategy is deterministic and dependency-free:
  1. Pull contact details + name from the header block (lines above the first
     recognized section heading).
  2. Slice the body into sections by matching heading lines against a known set
     of aliases.
  3. Parse each section into its typed shape (experience/education/projects) or
     a token list (skills/certifications).

It is intentionally rule-based rather than LLM-driven so parsing stays fast,
free, and reproducible; an LLM normalizer can later implement the same
``CVParser`` port without touching callers.
"""
import re

from app.domain.interfaces.parser import CVParser
from app.schemas.cv_schema import (
    CVSections,
    EducationItem,
    ExperienceItem,
    ProjectItem,
)

_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_PHONE_RE = re.compile(r"(?:\+?\d[\d\s().-]{7,}\d)")
_URL_RE = re.compile(r"\b((?:https?://|www\.)\S+|(?:github|linkedin|gitlab)\.com/\S+)", re.I)
_BULLET_RE = re.compile(r"^\s*(?:[-•*▪◦·–—]|\d+[.)])\s+")
_PAREN_RE = re.compile(r"\(([^)]*)\)")

# Period like "2020 - Present", "Jan 2020 – Dec 2021", "2016 - 2020".
_PERIOD_RE = re.compile(
    r"(?:[A-Za-z]{3,9}\.?\s+)?(?:19|20)\d{2}"
    r"\s*(?:-|–|—|to)\s*"
    r"(?:(?:[A-Za-z]{3,9}\.?\s+)?(?:19|20)\d{2}|present|current|now|ongoing)",
    re.I,
)
_YEAR_RE = re.compile(r"\b(?:19|20)\d{2}\b")

# Heading alias -> canonical section. "summary" is recognized (so it ends the
# header block) but produces no output field.
_SECTION_ALIASES: dict[str, str] = {
    "summary": "summary",
    "profile": "summary",
    "objective": "summary",
    "about": "summary",
    "about me": "summary",
    "skills": "skills",
    "technical skills": "skills",
    "core skills": "skills",
    "key skills": "skills",
    "technologies": "skills",
    "tech stack": "skills",
    "competencies": "skills",
    "experience": "experience",
    "work": "experience",
    "work experience": "experience",
    "working experience": "experience",
    "professional experience": "experience",
    "employment": "experience",
    "employment history": "experience",
    "work history": "experience",
    "education": "education",
    "academic background": "education",
    "academic": "education",
    "qualifications": "education",
    "projects": "projects",
    "personal projects": "projects",
    "side projects": "projects",
    "selected projects": "projects",
    "notable projects": "projects",
    "certifications": "certifications",
    "certification": "certifications",
    "certificates": "certifications",
    "licenses": "certifications",
    "licenses & certifications": "certifications",
    "courses": "certifications",
    "awards": "certifications",
}


def _heading_for(line: str) -> str | None:
    """Return the canonical section if ``line`` is a known heading, else None."""
    key = line.strip().lower().rstrip(":").strip(" *_-#")
    return _SECTION_ALIASES.get(key)


def _strip_bullet(line: str) -> str:
    return _BULLET_RE.sub("", line).strip()


def _is_bullet(line: str) -> bool:
    return bool(_BULLET_RE.match(line))


def _split_tokens(text: str) -> list[str]:
    # Split on commas / pipes / semicolons / bullets / newlines — never on "/"
    # so "CI/CD" and "TCP/IP" survive intact.
    return [t.strip(" .-•*\t") for t in re.split(r"[,\|;\n•]+", text)]


class CVNormalizer(CVParser):
    def parse(self, raw_text: str) -> CVSections:
        lines = [ln.rstrip() for ln in raw_text.replace("\r\n", "\n").split("\n")]

        header_lines, sections = self._split_sections(lines)

        return CVSections(
            personal_info=self._personal_info(header_lines, raw_text),
            education=self._parse_education(sections.get("education", [])),
            experience=self._parse_experience(sections.get("experience", [])),
            projects=self._parse_projects(sections.get("projects", [])),
            skills=self._parse_skills(sections.get("skills", [])),
            certifications=self._parse_certifications(sections.get("certifications", [])),
        )

    # -- sectioning ---------------------------------------------------------
    def _split_sections(
        self, lines: list[str]
    ) -> tuple[list[str], dict[str, list[str]]]:
        header_lines: list[str] = []
        sections: dict[str, list[str]] = {}
        current: str | None = None
        seen_heading = False

        for line in lines:
            heading = _heading_for(line)
            if heading is not None:
                current = heading
                seen_heading = True
                sections.setdefault(current, [])
                continue
            if not line.strip():
                continue
            if not seen_heading:
                header_lines.append(line)
            elif current is not None:
                sections[current].append(line)
        return header_lines, sections

    # -- personal info ------------------------------------------------------
    def _personal_info(self, header_lines: list[str], raw_text: str) -> dict[str, object]:
        info: dict[str, object] = {}

        email = _EMAIL_RE.search(raw_text)
        if email:
            info["email"] = email.group(0)
        phone = _PHONE_RE.search(raw_text)
        if phone:
            info["phone"] = phone.group(0).strip()

        links: list[str] = []
        for ln in header_lines:
            for m in _URL_RE.finditer(ln):
                url = m.group(0).rstrip(".,)")
                if url not in links:
                    links.append(url)
        if links:
            info["links"] = links

        name = self._guess_name(header_lines)
        if name:
            info["name"] = name
        return info

    @staticmethod
    def _guess_name(header_lines: list[str]) -> str | None:
        for ln in header_lines:
            candidate = ln.strip()
            if not candidate or _EMAIL_RE.search(candidate) or _URL_RE.search(candidate):
                continue
            if _PHONE_RE.search(candidate) or "@" in candidate:
                continue
            words = candidate.split()
            if 1 <= len(words) <= 5 and all(w[0].isupper() for w in words if w[:1].isalpha()):
                return candidate
        return None

    # -- experience ---------------------------------------------------------
    def _parse_experience(self, body: list[str]) -> list[ExperienceItem]:
        items: list[ExperienceItem] = []
        current: ExperienceItem | None = None

        for line in body:
            if _is_bullet(line):
                if current is None:
                    current = ExperienceItem()
                    items.append(current)
                current.highlights.append(_strip_bullet(line))
            elif self._looks_like_entry_header(line):
                current = self._parse_role_header(line)
                items.append(current)
            else:
                if current is None:
                    current = ExperienceItem()
                    items.append(current)
                current.highlights.append(line.strip())
        return items

    @staticmethod
    def _looks_like_entry_header(line: str) -> bool:
        if _PERIOD_RE.search(line):
            return True
        words = line.split()
        if len(words) <= 8 and not line.strip().endswith("."):
            return True
        return False

    @staticmethod
    def _parse_role_header(line: str) -> ExperienceItem:
        period = None
        m = _PERIOD_RE.search(line)
        if m:
            period = m.group(0).strip()
            line = line.replace(m.group(0), "")
        line = line.replace("(", " ").replace(")", " ").strip(" -–—,")

        title: str | None = None
        company: str | None = None
        # Separator may be a comma (often no leading space), a dash, "@" or "at".
        parts = re.split(r"\s*,\s+|\s+[–—@-]\s+|\s+at\s+", line, maxsplit=1)
        if parts:
            title = parts[0].strip() or None
        if len(parts) > 1:
            company = parts[1].strip() or None
        return ExperienceItem(title=title, company=company, period=period)

    # -- education ----------------------------------------------------------
    def _parse_education(self, body: list[str]) -> list[EducationItem]:
        items: list[EducationItem] = []
        for raw in body:
            line = _strip_bullet(raw)
            if not line:
                continue
            period = None
            pm = _PERIOD_RE.search(line) or _YEAR_RE.search(line)
            if pm:
                period = pm.group(0).strip()
                line = line.replace(pm.group(0), "")
            line = line.strip(" -–—,()")
            degree: str | None = None
            institution: str | None = None
            parts = re.split(r"\s*(?:,|–|—| - | at )\s*", line, maxsplit=1)
            if parts:
                degree = parts[0].strip() or None
            if len(parts) > 1:
                institution = parts[1].strip(" ,") or None
            items.append(EducationItem(degree=degree, institution=institution, period=period))
        return items

    # -- projects -----------------------------------------------------------
    def _parse_projects(self, body: list[str]) -> list[ProjectItem]:
        items: list[ProjectItem] = []
        for raw in body:
            line = _strip_bullet(raw)
            if not line:
                continue
            tech: list[str] = []
            pm = _PAREN_RE.search(line)
            if pm:
                tech = [t for t in _split_tokens(pm.group(1)) if t]
                line = _PAREN_RE.sub("", line).strip()

            name: str | None = None
            description: str | None = None
            parts = re.split(r"\s+(?:-|–|—|:)\s+", line, maxsplit=1)
            name = parts[0].strip(" -–—:") or None
            if len(parts) > 1:
                description = parts[1].strip() or None
            items.append(ProjectItem(name=name, description=description, tech=tech))
        return items

    # -- skills -------------------------------------------------------------
    def _parse_skills(self, body: list[str]) -> list[str]:
        skills: list[str] = []
        seen: set[str] = set()
        for raw in body:
            line = _strip_bullet(raw)
            if ":" in line:  # "Languages: Python, Go" -> keep the values only
                line = line.split(":", 1)[1]
            for token in _split_tokens(line):
                if not token or len(token) > 50 or len(token.split()) > 6:
                    continue
                key = token.lower()
                if key not in seen:
                    seen.add(key)
                    skills.append(token)
        return skills

    # -- certifications -----------------------------------------------------
    def _parse_certifications(self, body: list[str]) -> list[str]:
        certs: list[str] = []
        for raw in body:
            line = _strip_bullet(raw)
            if line:
                certs.append(line)
        return certs
