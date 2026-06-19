"""Unit tests for the JD Matching Engine: skill extraction, gap analysis, score."""
import pytest

from app.core.exceptions import AIServiceError
from app.services.jd_matching.jd_matching_service import JDMatchingService
from app.services.jd_matching.skill_extractor import extract_skills
from tests.fixtures.sample_cvs import SAMPLE_CVS


# -- skill extraction ------------------------------------------------------
def test_extracts_canonical_skills():
    skills = extract_skills("Built services in Python and FastAPI on PostgreSQL.")
    assert set(skills) == {"Python", "FastAPI", "PostgreSQL"}


def test_resolves_aliases_to_canonical_form():
    skills = extract_skills("Strong in JS, TS, k8s, postgres and reactjs.")
    assert set(skills) == {"JavaScript", "TypeScript", "Kubernetes", "PostgreSQL", "React"}


def test_longest_alias_wins_no_spurious_react():
    # "React Native" must not also yield bare "React".
    assert extract_skills("Experience with React Native") == ["React Native"]


def test_does_not_match_substrings():
    # "java" inside "javascript" must not produce Java.
    assert extract_skills("Senior JavaScript developer") == ["JavaScript"]


def test_handles_punctuation_and_compound_tokens():
    skills = extract_skills("Stack: C++, C#, Node.js, CI/CD, gRPC.")
    assert set(skills) == {"C++", "C#", "Node.js", "CI/CD", "gRPC"}


def test_empty_text_yields_no_skills():
    assert extract_skills("") == []
    assert extract_skills("   ") == []


def test_extraction_is_deterministic_and_sorted():
    text = "Kubernetes, AWS, Docker, Python"
    assert extract_skills(text) == extract_skills(text)
    assert extract_skills(text) == sorted(extract_skills(text), key=str.lower)


# -- matching pipeline -----------------------------------------------------
def _match(cv: str, jd: str):
    return JDMatchingService().match(cv, jd)


def test_match_computes_score_matched_and_missing():
    cv = "Skills: Python, FastAPI, PostgreSQL, Docker"
    jd = "Looking for Python, FastAPI, PostgreSQL, Kubernetes, AWS"
    res = _match(cv, jd)
    assert res.matched_skills == ["FastAPI", "PostgreSQL", "Python"]
    assert res.missing_skills == ["AWS", "Kubernetes"]
    # 3 of 5 JD skills matched -> 60.
    assert res.match_score == 60


def test_perfect_match_scores_100():
    cv = "Python, Django, PostgreSQL"
    jd = "We need Python, Django, PostgreSQL"
    res = _match(cv, jd)
    assert res.match_score == 100
    assert res.missing_skills == []


def test_no_overlap_scores_zero():
    res = _match("Java, Spring", "React, TypeScript, CSS")
    assert res.match_score == 0
    assert set(res.missing_skills) == {"React", "TypeScript", "CSS"}


def test_recommendations_mention_missing_skills():
    res = _match("Python", "Python, Kubernetes, Terraform")
    joined = " ".join(res.recommendations)
    assert "Kubernetes" in joined
    assert "Terraform" in joined


def test_jd_with_no_recognized_skills_is_handled():
    res = _match("Python developer", "We want a passionate team player who loves coffee")
    assert res.match_score == 0
    assert res.matched_skills == []
    assert res.recommendations  # explains the limitation


def test_real_cv_against_relevant_jd_scores_high():
    jd = "Senior Backend Engineer: Python, FastAPI, PostgreSQL, Docker, Kubernetes, AWS"
    res = _match(SAMPLE_CVS["senior_backend"], jd)
    assert res.match_score >= 80
    assert "Python" in res.matched_skills


def test_real_cv_against_irrelevant_jd_scores_low():
    jd = "Android Engineer: Kotlin, Jetpack Compose, Flutter, Swift, iOS"
    res = _match(SAMPLE_CVS["senior_backend"], jd)
    assert res.match_score < 50


def test_empty_inputs_rejected():
    with pytest.raises(AIServiceError):
        _match("   ", "Python")
    with pytest.raises(AIServiceError):
        _match("Python", "   ")
