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

**Request normalization**

The canonical Backend → AI payload is snake_case (`cv_text`, `job_description`).
For compatibility during integration, the AI Service also accepts these aliases
and normalizes them internally before review:

| Canonical field | Accepted aliases |
|-----------------|------------------|
| `cv_text` | `cvText`, `cv`, `raw_text`, `rawText` |
| `job_description` | `jobDescription`, `jd`, `job_desc`, `jobDesc` |

Whitespace is trimmed server-side. Responses are always returned in the canonical
snake_case schema below.

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
| `jd_match` | object \| null | `null` unless a JD was provided (see below). |

**`jd_match` object**

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
| `notes` | string | Short rationale and/or recommendations. |

When the LLM omits `jd_match`, the AI Service fills this block using the
deterministic JD Matching engine so Backend and Frontend can rely on the field
being populated whenever `job_description` is non-empty.

---

## 2. Parse a CV

Two entry points produce the **same** unified `sections` shape: one for raw text,
one for an uploaded PDF/DOCX file.

### `POST /api/v1/parse-cv`  (raw text)

**Request**

```json
{ "raw_text": "string — required, non-empty" }
```

### `POST /api/v1/parse-cv-file`  (file upload)

`multipart/form-data` with a single `file` field (`.pdf` or `.docx`). The service
extracts text (pypdf / python-docx, routed by extension or MIME type) then runs
the same normalizer.

**Response `200` (both endpoints) — unified CV JSON**

```json
{
  "sections": {
    "personal_info": {
      "name": "string",
      "email": "string",
      "phone": "string",
      "links": ["string"]
    },
    "education": [
      { "degree": "string|null", "institution": "string|null", "period": "string|null" }
    ],
    "experience": [
      {
        "title": "string|null",
        "company": "string|null",
        "period": "string|null",
        "highlights": ["string"]
      }
    ],
    "projects": [
      { "name": "string|null", "description": "string|null", "tech": ["string"] }
    ],
    "skills": ["string"],
    "certifications": ["string"]
  }
}
```

| Field | Type | Notes |
|-------|------|-------|
| `personal_info` | object | Keys present only when detected (`name`, `email`, `phone`, `links`). |
| `education` | object[] | Degree / institution / period per entry. |
| `experience` | object[] | Role header parsed into title/company/period + bullet `highlights`. |
| `projects` | object[] | `tech` extracted from parenthesised tech lists. |
| `skills` | string[] | De-duplicated token list (compound tokens like `CI/CD` preserved). |
| `certifications` | string[] | One entry per listed certification. |

> Parsing is deterministic and rule-based (no LLM): fast, free, reproducible.
> A scanned/image-only PDF (no extractable text) returns `422`.

---

## 3. Match a CV against a JD

### `POST /api/v1/match-jd`  (AI Service)

Deterministic skill matching: **Skill Extraction → Gap Analysis → Match Score**.
Standalone counterpart to the review engine's qualitative `jd_match` block.

**Request**

```json
{
  "cv_text": "string — required, non-empty",
  "job_description": "string — required, non-empty"
}
```

**Response `200`**

```json
{
  "match_score": 78,
  "matched_skills": ["string"],
  "missing_skills": ["string"],
  "recommendations": ["string"]
}
```

| Field | Type | Notes |
|-------|------|-------|
| `match_score` | int 0–100 | Share of JD-required skills the CV demonstrates. |
| `matched_skills` | string[] | Canonical skills found in both CV and JD. |
| `missing_skills` | string[] | JD skills absent from the CV. |
| `recommendations` | string[] | Actionable guidance derived from the gaps. |

> Skill resolution is alias-aware (`JS`→JavaScript, `k8s`→Kubernetes,
> `postgres`→PostgreSQL). Source of truth: `app/services/jd_matching/skill_taxonomy.py`.

---

## 4. Health

### `GET /health`  (AI Service)

```json
{ "status": "ok", "service": "ai-service" }
```

---

## 5. Errors

All handled service errors use a consistent envelope (mapped from `AIServiceError`).

```json
{
  "error": "human-readable message",
  "type": "ReviewError"
}
```

| Status | When |
|--------|------|
| `422` | Validation error (e.g. empty `cv_text`/`raw_text`). |
| `502` | AI service dependency error that cannot be recovered. |
| `500` | Unexpected server error. |

> Resilience note: if the LLM returns malformed output or does not respond, the AI Review Engine
> **falls back** to a deterministic mock review and still returns `200` with a valid
> body — clients never receive a partial or invalid schema.

---

## 6. Versioning rules

1. Additive, backward-compatible changes (new optional field) → keep `schema_version` `"1.0"`.
2. Breaking changes (rename/remove field, change score ranges) → bump to `"2.0"` and
   `prompts/review_prompt_v2.md`; keep schema and prompt versions in lockstep.
3. FE/BE should read `schema_version` and degrade gracefully on unknown versions.

## 7. Contract ownership

| Layer | Responsibility |
|-------|----------------|
| AI Service | Produces the canonical response; enforces ranges, sum, and fallback. |
| Backend | Validates request, injects `X-Internal-Api-Key`, may persist results, proxies to FE. |
| Frontend | Renders `category_scores` (each /20), `overall_score` (/100), and the lists. |
