"""Integration tests for the Sprint 1 endpoints."""


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
