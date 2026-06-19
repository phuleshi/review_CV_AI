        """Unit tests for the heuristic CVNormalizer (text -> unified CV JSON)."""
import pytest

from app.schemas.cv_schema import CVSections
from app.services.cv_parsing.cv_normalizer import CVNormalizer
from tests.fixtures.sample_cvs import SAMPLE_CVS


def _normalize(text: str) -> CVSections:
    return CVNormalizer().parse(text)


@pytest.mark.parametrize("name", list(SAMPLE_CVS))
def test_normalizer_returns_unified_shape(name):
    cv = _normalize(SAMPLE_CVS[name])
    # Every CV yields the full unified structure regardless of content.
    assert set(cv.model_dump()) == {
        "personal_info",
        "education",
        "experience",
        "projects",
        "skills",
        "certifications",
    }


# Every CV except the deliberately-weak one lists a Skills section.
_WITH_SKILLS = [n for n in SAMPLE_CVS if n != "weak_no_metrics"]
# The junior CV leans on projects and has no Experience section.
_WITH_EXPERIENCE = [n for n in _WITH_SKILLS if n != "junior_projects"]


@pytest.mark.parametrize("name", _WITH_SKILLS)
def test_well_formed_cvs_have_skills(name):
    assert _normalize(SAMPLE_CVS[name]).skills, "expected skills to be extracted"


@pytest.mark.parametrize("name", _WITH_EXPERIENCE)
def test_well_formed_cvs_have_experience(name):
    assert _normalize(SAMPLE_CVS[name]).experience, "expected experience entries"


def test_extracts_contact_info():
    cv = _normalize(SAMPLE_CVS["data_scientist"])
    assert cv.personal_info["name"] == "Daniel Kim"
    assert cv.personal_info["email"] == "daniel.kim@example.com"
    assert "phone" in cv.personal_info
    assert any("linkedin.com" in link for link in cv.personal_info["links"])


def test_parses_experience_with_title_company_period_and_highlights():
    cv = _normalize(SAMPLE_CVS["senior_backend"])
    assert len(cv.experience) == 2
    first = cv.experience[0]
    assert first.title == "Senior Backend Engineer"
    assert first.company == "Acme"
    assert "2020" in first.period and "Present" in first.period
    assert len(first.highlights) == 3
    assert any("latency" in h for h in first.highlights)


def test_parses_skills_as_token_list_preserving_compound_tokens():
    cv = _normalize(SAMPLE_CVS["devops_engineer"])
    assert "Kubernetes" in cv.skills
    assert "Terraform" in cv.skills
    # "CI/CD" must not be split on the slash.
    assert "CI/CD" in cv.skills


def test_parses_projects_with_name_and_tech():
    cv = _normalize(SAMPLE_CVS["senior_backend"])
    assert len(cv.projects) == 1
    proj = cv.projects[0]
    assert proj.name == "Distributed rate limiter"
    assert proj.tech == ["Go", "Redis"]


def test_parses_education_degree_and_period():
    cv = _normalize(SAMPLE_CVS["data_scientist"])
    assert cv.education
    edu = cv.education[0]
    assert "M.Sc" in (edu.degree or "")
    assert edu.period == "2019"


def test_parses_certifications():
    cv = _normalize(SAMPLE_CVS["data_scientist"])
    assert "AWS Certified Machine Learning - Specialty" in cv.certifications
    assert len(cv.certifications) == 2


def test_skills_are_deduplicated_case_insensitively():
    cv = _normalize("Skills\nPython, python, PYTHON, Go\n")
    lowered = [s.lower() for s in cv.skills]
    assert lowered.count("python") == 1
    assert "Go" in cv.skills


def test_weak_cv_still_normalizes_without_crashing():
    cv = _normalize(SAMPLE_CVS["weak_no_metrics"])
    assert cv.personal_info.get("name") == "Sam Taylor"
    # No real skills section -> empty list, not an error.
    assert cv.skills == []
