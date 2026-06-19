"""Extract canonical skills from free text (a CV or a JD).

Alias-aware and longest-match-first: "React Native" resolves to *React Native*
without also spuriously matching *React*, because longer aliases are matched and
masked out before shorter ones are tried. Output is the set of canonical skill
names, sorted for deterministic results.
"""
import re

from app.services.jd_matching.skill_taxonomy import SKILL_TAXONOMY

# Boundaries that treat +, # and *internal* dots as part of a token so "c++",
# "c#" and "node.js" match exactly and "java" never matches inside "javascript".
# A trailing dot is only protected when it is followed by a word char (an
# internal dot like node.js), so a sentence-ending "gRPC." still matches.
_BOUNDARY_L = r"(?<![\w+#.])"
_BOUNDARY_R = r"(?![\w+#]|\.\w)"


def _compile(alias: str) -> re.Pattern[str]:
    return re.compile(_BOUNDARY_L + re.escape(alias) + _BOUNDARY_R, re.IGNORECASE)


# (alias, canonical, pattern) sorted longest-alias-first for match precedence.
_ALIASES: list[tuple[str, str, re.Pattern[str]]] = sorted(
    (
        (alias, canonical, _compile(alias))
        for canonical, aliases in SKILL_TAXONOMY.items()
        for alias in aliases
    ),
    key=lambda item: len(item[0]),
    reverse=True,
)


def extract_skills(text: str) -> list[str]:
    """Return the sorted set of canonical skills mentioned in ``text``."""
    if not text or not text.strip():
        return []
    work = f" {text.lower()} "
    found: set[str] = set()
    for _alias, canonical, pattern in _ALIASES:
        masked, hits = pattern.subn(" ", work)
        if hits:
            found.add(canonical)
            work = masked  # consume so shorter overlapping aliases don't re-match
    return sorted(found, key=str.lower)
