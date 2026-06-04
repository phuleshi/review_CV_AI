# API Contract — V1

Shared data contract for **Frontend (Next.js) ↔ Backend (NestJS) ↔ AI Service (FastAPI)**.
All three layers use the same JSON shapes described here.

```
FE (Next.js)  →  BE (NestJS)  →  AI Service (FastAPI)  →  LLM
   renders         validates &        scores + feedback
   the result      proxies/persists   (canonical JSON)
```

- `schema_version` is `"1.0"`. Bumping the schema bumps this version + the prompt version.
- Source of truth in code: `app/schemas/review_schema.py`, `score_schema.py`.
- Scoring semantics: [kb/scoring_rubric.md](../kb/scoring_rubric.md).

---

## 1. Review a CV

### `POST /api/v1/review-cv`  (AI Service)

The Backend calls this; the Frontend calls the Backend's equivalent route, which
forwards the same body and returns the same response.

**Headers (internal BE → AI call)**

| Header | Value |
|--------|-------|
| `Content-Type` | `application/json` |
| `X-Internal-Api-Key` | shared secret (`INTERNAL_API_KEY`) |

**Request body**

```json
{
  "cv_text": "string — required, non-empty (raw CV text)",
  "job_description": "string | null — optional; enables JD matching"
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `cv_text` | string | yes | Min length 1. Plain text extracted from the CV. |
| `job_description` | string \| null | no | When present, `skills`/`ats` are judged against it and `jd_match` is populated (Sprint 2). |

**Response `200` — canonical AI Output Schema**

```json
{
  "schema_version": "1.0",
  "overall_score": 82,
  "category_scores": {
    "structure": 18,
    "skills": 17,
    "experience": 15,
    "projects": 16,
    "ats": 16
  },
  "strengths": ["string", "..."],
  "weaknesses": ["string", "..."],
  "suggestions": ["string", "..."],
  "summary": "string",
  "jd_match": null
}
```

| Field | Type | Notes |
|-------|------|-------|
| `schema_version` | string | Always `"1.0"` for this contract. |
| `overall_score` | int 0–100 | **Always equals the sum of `category_scores`** (enforced server-side). |
| `category_scores.structure` | int 0–20 | Layout, sections, readability. |
| `category_scores.skills` | int 0–20 | Relevance & depth of skills. |
| `category_scores.experience` | int 0–20 | Impact & clarity of work history. |
| `category_scores.projects` | int 0–20 | Quality & relevance of projects. |
| `category_scores.ats` | int 0–20 | ATS / keyword compatibility. |
| `strengths` | string[] | Evidence-based positives (may be empty). |
| `weaknesses` | string[] | Concrete issues, each tied to a category. |
| `suggestions` | string[] | Actionable fixes, ordered by impact. |
| `summary` | string | 2–3 sentence overall verdict. |
| `jd_match` | object \| null | `null` unless a JD was provided (see below). Sprint 2. |

**`jd_match` object (Sprint 2 — JD Matching)**

```json
{
  "match_score": 0,
  "matched_skills": ["string"],
  "missing_skills": ["string"],
  "notes": "string"
}
```

| Field | Type | Notes |
|-------|------|-------|
| `match_score` | int 0–100 | Overall CV↔JD fit. |
| `matched_skills` | string[] | JD skills found in the CV. |
| `missing_skills` | string[] | JD skills absent from the CV. |
| `notes` | string | Short rationale. |

---

## 2. Parse a CV (supporting endpoint)

### `POST /api/v1/parse-cv`  (AI Service)

**Request**

```json
{ "raw_text": "string — required, non-empty" }
```

**Response `200`**

```json
{
  "sections": {
    "personal_info": {},
    "education": [],
    "experience": [],
    "skills": [],
    "projects": [],
    "certifications": []
  }
}
```

> Sprint 1: parsing is mocked (loosely-typed lists). Section list shape is stable;
> item shapes will be tightened in a later sprint.

---

## 3. Health

### `GET /health`  (AI Service)

```json
{ "status": "ok", "service": "ai-service" }
```

---

## 4. Errors

All errors use a consistent envelope (mapped from `AIServiceError`).

```json
{ "detail": "human-readable message" }
```

| Status | When |
|--------|------|
| `422` | Validation error (e.g. empty `cv_text`/`raw_text`). |
| `502` | Upstream LLM error the engine could not recover from. |
| `500` | Unexpected server error. |

> Resilience note: if the LLM returns malformed output, the AI Review Engine
> **falls back** to a deterministic mock review and still returns `200` with a valid
> body — clients never receive a partial or invalid schema.

---

## 5. Versioning rules

1. Additive, backward-compatible changes (new optional field) → keep `schema_version` `"1.0"`.
2. Breaking changes (rename/remove field, change score ranges) → bump to `"2.0"` and
   `prompts/review_prompt_v2.md`; keep schema and prompt versions in lockstep.
3. FE/BE should read `schema_version` and degrade gracefully on unknown versions.

## 6. Contract ownership

| Layer | Responsibility |
|-------|----------------|
| AI Service | Produces the canonical response; enforces ranges, sum, and fallback. |
| Backend | Validates request, injects `X-Internal-Api-Key`, may persist results, proxies to FE. |
| Frontend | Renders `category_scores` (each /20), `overall_score` (/100), and the lists. |
