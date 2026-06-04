# AI Service — AI CV Reviewer

Independent **Python FastAPI** microservice. Called by the NestJS backend over HTTP.

```
FE (Next.js) → BE (NestJS) → AI Service (FastAPI) → LLM / RAG
```

Designed with **Clean Architecture**: dependencies point inward
(`api → services → domain`). Outer layers (FastAPI, OpenAI, Pinecone) depend on
abstractions defined in `domain/interfaces`, never the other way around.

## Layer map

| Layer | Folder | Responsibility |
|-------|--------|----------------|
| Interface | `app/api` | HTTP transport: routers, request/response validation, DI wiring |
| Application | `app/services` | Use cases: CV parsing, scoring, feedback orchestration |
| Domain | `app/domain` | Pure entities + ports (interfaces). No framework imports |
| LLM | `app/llm` | Provider abstraction, OpenAI impl, retry/error handling |
| RAG | `app/rag` | Embeddings, retrieval, Pinecone client (future) |
| Schemas | `app/schemas` | Pydantic DTOs crossing the API boundary |
| Infra | `app/core` | Config, logging, DI container, middleware, exceptions |

See the repo design notes for the full folder explanation and sprint plan.

> **Sprint 1 status:** the **AI Review Engine** is live end-to-end
> (`CV → prompt → LLM → validated JSON`). The default `LLM_PROVIDER=heuristic` is a
> *grounded local stand-in* — it derives scores/feedback from signals actually in the
> CV, so no OpenAI key is needed and nothing is hallucinated. Set `LLM_PROVIDER=openai`
> to swap in a real model (engine, schema, and parser unchanged). PDF/DOCX parsing and
> Pinecone/RAG remain mocked/deferred. Output is the canonical schema in
> [docs/api_contract.md](docs/api_contract.md); scoring follows
> [kb/scoring_rubric.md](kb/scoring_rubric.md); prompt is
> [prompts/review_prompt_v1.md](prompts/review_prompt_v1.md).

## Run (local)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env        # defaults work for Sprint 1 (LLM_PROVIDER=mock)
uvicorn app.main:app --reload
```

Interactive docs: http://localhost:8000/docs

## Endpoints (Sprint 1)

| Method | Path | Description |
|--------|------|-------------|
| GET  | `/health`          | Liveness check |
| POST | `/api/v1/parse-cv` | Parse raw CV text → normalized sections (mock) |
| POST | `/api/v1/review-cv`| Score + feedback for a CV (mock) |

```bash
curl localhost:8000/health

curl -X POST localhost:8000/api/v1/parse-cv \
  -H 'Content-Type: application/json' \
  -d '{"raw_text": "Jane Doe — jane@mail.com — Python, FastAPI"}'

curl -X POST localhost:8000/api/v1/review-cv \
  -H 'Content-Type: application/json' \
  -d '{"cv_text": "Senior engineer...", "job_description": "Backend role"}'
```

## Test

```bash
pytest
```
