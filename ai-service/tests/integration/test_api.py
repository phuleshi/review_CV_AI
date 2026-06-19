"""Integration tests for the Sprint 1 endpoints."""
from tests.fixtures.render import make_docx, make_pdf
from tests.fixtures.sample_cvs import SAMPLE_CVS


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok", "service": "ai-service"}


def test_parse_cv(client):
    res = client.post("/api/v1/parse-cv", json={"raw_text": "Jane Doe jane@mail.com"})
    assert res.status_code == 200
    body = res.json()
    assert "sections" in body
    assert body["sections"]["personal_info"]["email"] == "jane@mail.com"
    assert body["sections"]["education"] == []


def test_parse_cv_rejects_empty(client):
    res = client.post("/api/v1/parse-cv", json={"raw_text": ""})
    assert res.status_code == 422  # pydantic min_length


def test_parse_cv_file_pdf(client):
    pdf = make_pdf(SAMPLE_CVS["senior_backend"])
    res = client.post(
        "/api/v1/parse-cv-file",
        files={"file": ("cv.pdf", pdf, "application/pdf")},
    )
    assert res.status_code == 200
    sections = res.json()["sections"]
    assert sections["personal_info"]["name"] == "John Carter"
    assert "Python" in sections["skills"]
    assert sections["experience"]


def test_parse_cv_file_docx(client):
    docx = make_docx(SAMPLE_CVS["mid_frontend"])
    res = client.post(
        "/api/v1/parse-cv-file",
        files={"file": ("cv.docx", docx, "application/octet-stream")},
    )
    assert res.status_code == 200
    sections = res.json()["sections"]
    assert sections["personal_info"]["email"] == "maria.lopez@example.com"
    assert "React" in sections["skills"]


def test_parse_cv_file_rejects_unsupported_type(client):
    res = client.post(
        "/api/v1/parse-cv-file",
        files={"file": ("cv.txt", b"hello world", "text/plain")},
    )
    assert res.status_code == 422  # CVParsingError


def test_match_jd(client):
    res = client.post(
        "/api/v1/match-jd",
        json={
            "cv_text": SAMPLE_CVS["senior_backend"],
            "job_description": "Backend role: Python, FastAPI, PostgreSQL, Kubernetes, AWS",
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert set(body) == {
        "match_score",
        "matched_skills",
        "missing_skills",
        "recommendations",
    }
    assert 0 <= body["match_score"] <= 100
    assert "Python" in body["matched_skills"]


def test_match_jd_rejects_missing_jd(client):
    res = client.post("/api/v1/match-jd", json={"cv_text": "Python"})
    assert res.status_code == 422  # pydantic: job_description required


def test_review_cv(client):
    res = client.post("/api/v1/review-cv", json={"cv_text": "Some CV text"})
    assert res.status_code == 200
    body = res.json()
    assert body["schema_version"] == "1.0"
    assert set(body["category_scores"]) == {
        "structure", "skills", "experience", "projects", "ats",
    }
    # overall_score is the sum of the five categories (each 0-20 → 0-100).
    assert body["overall_score"] == sum(body["category_scores"].values())
    assert 0 <= body["overall_score"] <= 100
    assert isinstance(body["suggestions"], list)
    assert body["summary"]
    assert body["jd_match"] is None


def test_review_cv_accepts_backend_payload_aliases(client):
    res = client.post(
        "/api/v1/review-cv",
        json={
            "cvText": "  Frontend Developer with React, TypeScript and Next.js.  ",
            "jobDescription": "React TypeScript frontend role",
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert body["schema_version"] == "1.0"
    assert body["overall_score"] == sum(body["category_scores"].values())
    assert body["jd_match"] is not None


def test_review_cv_multiple_sample_cvs(client):
    for name, cv_text in SAMPLE_CVS.items():
        res = client.post("/api/v1/review-cv", json={"cv_text": cv_text})
        assert res.status_code == 200, name
        body = res.json()
        assert body["schema_version"] == "1.0"
        assert 0 <= body["overall_score"] <= 100
        assert body["overall_score"] == sum(body["category_scores"].values())
        assert body["summary"]
