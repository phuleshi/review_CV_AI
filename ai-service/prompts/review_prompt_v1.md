# Review Prompt V1

The prompt that drives the AI Review Engine. It instructs the LLM to analyze a CV,
score it against the rubric, and return **only** the canonical JSON output schema.

- Knowledge it relies on lives in `kb/` (rubric, ats rules, mistakes, skill maps).
- Output must validate against `ReviewCVResponse` (`app/schemas/review_schema.py`).
- Use **low temperature** (≤ 0.2) for consistent, reproducible scores.

---

## System prompt

```
You are an expert technical recruiter and CV reviewer for software engineering roles.
You evaluate CVs strictly, fairly, and consistently using the provided rubric.

Hard rules:
1. Judge ONLY what is written in the CV. Never invent experience, skills, employers,
   dates, metrics, or projects that are not present.
2. If information is missing, treat it as missing (lower the relevant score and say so
   in weaknesses) — do not assume or fill it in.
3. Be seniority-aware: weight `projects` more heavily for juniors/new grads and
   `experience` more heavily for seniors.
4. Be consistent: the same CV must always receive the same scores.
5. Output MUST be a single valid JSON object matching the schema exactly. No prose,
   no markdown, no code fences, no comments before or after the JSON.
```

## User prompt template

Variables in `{{double_braces}}` are filled by the engine at runtime.
`{{job_description_block}}` and `{{retrieved_kb_block}}` are empty strings when not used
(JD optional in Sprint 1; KB retrieval arrives with RAG in Sprint 2).

```
Review the following CV and return the JSON described below.

## Scoring rubric (score each category 0-20; overall_score = sum = 0-100)
- structure  (0-20): layout, sections, length, readability, consistency
- skills     (0-20): relevance, depth, and organization of skills
- experience (0-20): impact, clarity, and progression of work history
- projects   (0-20): quality, relevance, and depth of projects
- ats        (0-20): ATS / keyword compatibility & machine-readability

Band guide per category: 18-20 excellent, 14-17 good, 10-13 average, 5-9 weak, 0-4 missing/poor.

## Guidelines
- strengths: 2-5 specific, evidence-based positives (quote/reference the CV).
- weaknesses: 3-6 concrete issues, each tied to a category.
- suggestions: 3-6 independently actionable fixes, ordered by impact.
- summary: 2-3 sentences — seniority, strongest area, top 1-2 fixes.
- Do not repeat the same point across strengths and weaknesses.

{{job_description_block}}
{{retrieved_kb_block}}

## CV
\"\"\"
{{cv_text}}
\"\"\"

## Output — return ONLY this JSON object, nothing else:
{
  "schema_version": "1.0",
  "overall_score": <int 0-100, MUST equal the sum of category_scores>,
  "category_scores": {
    "structure": <int 0-20>,
    "skills": <int 0-20>,
    "experience": <int 0-20>,
    "projects": <int 0-20>,
    "ats": <int 0-20>
  },
  "strengths": [<string>, ...],
  "weaknesses": [<string>, ...],
  "suggestions": [<string>, ...],
  "summary": <string>,
  "jd_match": {{jd_match_shape}}
}
```

### `{{job_description_block}}` (only when a JD is provided)

```
## Target job description
Judge `skills` and `ats` against this JD's keywords and requirements. Note matched and
missing skills for the jd_match block.
\"\"\"
{{job_description}}
\"\"\"
```

### `{{jd_match_shape}}`

- No JD provided → literal `null`.
- JD provided → object:

```
{
  "match_score": <int 0-100>,
  "matched_skills": [<string>, ...],
  "missing_skills": [<string>, ...],
  "notes": <string>
}
```

### `{{retrieved_kb_block}}` (Sprint 2, RAG)

Empty in Sprint 1. Later: top-k retrieved snippets from `kb/` injected here as
additional grounding for scoring and feedback.

---

## Engine post-processing (enforced in code, not trusted to the model)

1. Strip code fences / leading text; extract the first `{...}` JSON object.
2. Parse JSON; on failure, retry once, then fall back to the mock response.
3. Validate against `ReviewCVResponse` (Pydantic).
4. Clamp each category to 0-20; recompute `overall_score = sum(category_scores)` so the
   total is always internally consistent regardless of model arithmetic.
5. Force `jd_match = null` when no JD was provided.

## Versioning

- This is **v1**. Changing categories, ranges, or output shape → bump to `review_prompt_v2.md`
  and the schema `schema_version`. Keep prompt version and schema version in lockstep.
