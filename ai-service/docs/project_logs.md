# Project Logs — AI CV Review Platform

Append-only work log. Newest entries at the top. Format is fixed (see Working Rules).

---

## [2026-06-05 10:30]

Task:
Frontend Integration (FE ↔ BE ↔ AI Service)

Status:
DONE

Files:
* backend/src/review/review.types.ts
* backend/src/review/dto/review-cv.dto.ts
* backend/src/review/review.service.ts
* backend/src/review/review.controller.ts
* backend/src/review/review.module.ts
* backend/src/app.module.ts
* backend/.env.example
* backend/.env
* frontend/app/types.ts
* frontend/app/api.ts
* frontend/app/page.tsx
* frontend/app/globals.css

Summary:
Wired the full chain. Backend: new ReviewModule exposing POST /api/review-cv —
validates the body (class-validator DTO, snake_case to match the contract) and proxies
to the AI service (POST /api/v1/review-cv) with the X-Internal-Api-Key header, reading
AI_SERVICE_URL/INTERNAL_API_KEY from config; forwards AI errors and returns 502 if the
AI service is unreachable. Frontend: removed the old local mock scoring; the page now
calls the backend and renders the canonical schema — overall_score /100, five category
bars (each /20), and strengths/weaknesses/suggestions/summary, with loading + error
states. Shared the canonical schema as typed interfaces on both ends.

Verification:
* `nest build` → exit 0; `next build` → exit 0; frontend `tsc --noEmit` → clean.
* AI service started on :8000; real HTTP smoke test of the exact BE→AI proxy request
  returned the canonical schema (overall 80, all 5 categories, jd_match null).
* Note: a live NestJS boot needs Postgres (TypeORM connects on startup), which is not
  available in this environment, so the backend was verified by build + the HTTP proxy
  contract rather than a live boot.

Next Task:
Deployment (priority #8) — Docker Compose for ai-service + backend + frontend + Postgres,
and CI/CD. Optionally: enforce X-Internal-Api-Key in the AI service; PDF/DOCX parsing.

---

## [2026-06-04 13:30]

Task:
API Contract Alignment

Status:
DONE

Files:
* docs/api_contract.md

Summary:
Documented the shared FE ↔ BE ↔ AI Service data contract: POST /api/v1/review-cv
request/response (canonical schema, all field types/ranges, overall == sum invariant),
the jd_match block (Sprint 2), parse-cv + health endpoints, error envelope/status
codes, the engine fallback guarantee (always returns valid 200), versioning rules, and
per-layer contract ownership.

Next Task:
Frontend Integration (priority #7) — wire the Next.js UI to render the canonical
schema via the NestJS backend.

---

## [2026-06-04 13:05]

Task:
AI Review Engine

Status:
DONE

Files:
* ai-service/app/services/ai_review/review_service.py
* ai-service/app/services/ai_review/prompt_manager.py
* ai-service/app/services/ai_review/output_parser.py
* ai-service/app/llm/heuristic_provider.py
* ai-service/app/llm/factory.py
* ai-service/app/core/config.py
* ai-service/app/api/v1/routes/review.py
* ai-service/.env.example
* ai-service/README.md
* ai-service/tests/fixtures/sample_cvs.py
* ai-service/tests/unit/test_review_engine.py

Summary:
Built the end-to-end engine: CV → PromptManager builds the V1 prompt → LLMProvider
returns raw text → output_parser extracts/validates/clamps JSON and recomputes
overall_score → ReviewCVResponse. Added a grounded "heuristic" LLM provider (Sprint 1
default, no API key, no hallucination — scores derive from CV signals) and a graceful
fallback to the mock review on any parse/validation failure. Made the review flow
async. Tested 5 varied CVs (senior 90, mid/fullstack 88, junior 80, weak 44) plus
fallback, determinism, grounding, and parser edge cases (code fences, clamping, JD
match, garbage). Installed pytest-asyncio. 18/18 tests pass.

Next Task:
API Contract Alignment → docs/api_contract.md

---

## [2026-06-04 12:20]

Task:
Review Prompt V1

Status:
DONE

Files:
* prompts/review_prompt_v1.md

Summary:
Authored the V1 review prompt: system prompt (strict, anti-hallucination,
seniority-aware, JSON-only) + user template with the rubric, feedback guidelines,
optional JD block, RAG-context placeholder (Sprint 2), and the exact JSON output shape.
Documented engine post-processing (JSON extraction, clamp, recompute overall, force
jd_match) and prompt/schema lockstep versioning. Mirrored in code by PromptManager.

Next Task:
AI Review Engine → wire CV → prompt → LLM → validated JSON

---

## [2026-06-04 11:15]

Task:
Knowledge Base V1

Status:
DONE

Files:
* kb/ats_rules.md
* kb/common_cv_mistakes.md
* kb/feedback_templates.md
* kb/frontend_skillmap.md
* kb/backend_skillmap.md
* kb/fullstack_skillmap.md

Summary:
Hand-written knowledge base (no crawling, no Pinecone). ATS rules with do/don't +
checklist; a 24-item catalogue of common CV mistakes mapped to scoring categories;
feedback phrasing templates for consistent tone; and three seniority-aware skill maps
(frontend, backend, full-stack) for the skills category and JD keyword matching.
Together with scoring_rubric.md this completes the 7-file kb/ V1.

Next Task:
Review Prompt V1 → prompts/review_prompt_v1.md

---

## [2026-06-04 10:40]

Task:
CV Scoring Rubric

Status:
DONE

Files:
* kb/scoring_rubric.md

Summary:
Defined the scoring rubric matching the output schema: 5 categories (structure,
skills, experience, projects, ats) each 0-20, summing to overall_score 0-100. Each
category has a band guide, scoring description, explicit deduct/add rules, calibration
anchors by seniority, and rules for the scorer (no hallucination, consistency,
seniority-aware weighting, JD-aware skills/ats).

Next Task:
Knowledge Base V1 → kb/*.md

---

## [2026-06-04 10:00]

Task:
AI Output Schema (canonical)

Status:
DONE

Files:
* ai-service/app/schemas/score_schema.py
* ai-service/app/schemas/review_schema.py
* ai-service/app/services/ai_review/cv_scorer.py
* ai-service/tests/integration/test_api.py

Summary:
Defined the canonical AI output JSON schema for the whole system. Five categories
(structure, skills, experience, projects, ats), each 0-20, summing to a 0-100
overall_score. Added schema_version ("1.0") and an optional jd_match block as the
extension point for JD Matching in Sprint 2 (null until a JD is provided). Aligned
the Pydantic models, the mock scorer (overall = sum of categories), and updated the
integration tests. All 4 tests pass.

Next Task:
CV Scoring Rubric → kb/scoring_rubric.md

---
