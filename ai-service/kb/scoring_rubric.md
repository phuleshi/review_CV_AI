# CV Scoring Rubric — V1

Source of truth for how the AI scores a CV. The JSON output schema
(`category_scores`) mirrors this file exactly. Keep them in sync.

## Scale

- 5 categories, each scored **0–20**.
- `overall_score` = sum of all categories = **0–100**.
- Scores are integers only.

| Category    | Max | What it measures                                   |
|-------------|-----|----------------------------------------------------|
| structure   | 20  | Layout, sections, length, readability, consistency |
| skills      | 20  | Relevance, depth, and organization of skills       |
| experience  | 20  | Impact, clarity, and progression of work history   |
| projects    | 20  | Quality, relevance, and depth of projects          |
| ats         | 20  | ATS / keyword compatibility & machine-readability  |
| **Total**   |**100**|                                                  |

## Band guide (applies to each category, scaled to /20)

| Band        | /20 range | Meaning                                            |
|-------------|-----------|----------------------------------------------------|
| Excellent   | 18–20     | Best practice, almost nothing to improve           |
| Good        | 14–17     | Solid, minor gaps                                  |
| Average     | 10–13     | Acceptable but several clear weaknesses            |
| Weak        | 5–9       | Major gaps, needs significant rework               |
| Missing/Poor| 0–4       | Section absent or unusable                          |

---

## 1. Structure (max 20)

How well the CV is organized and presented.

**Scoring**
- Start from 20 and deduct.
- 18–20: Clear sections (Summary, Skills, Experience, Projects, Education), consistent formatting, 1–2 pages, scannable in <30s.
- 14–17: Good order; minor inconsistency (spacing, bullet style) or slightly long.
- 10–13: Sections present but cluttered, inconsistent tense, or >2 pages without reason.
- 5–9: Missing key sections or hard to scan (walls of text, no bullets).
- 0–4: No discernible structure.

**Deduct points**
- −2 No professional summary / headline.
- −2 Inconsistent date formats or tense.
- −2 Over 2 pages for <8 years experience.
- −2 Dense paragraphs instead of bullets.
- −1 Missing or wrong section ordering.

**Add points (within cap)**
- +1 Clean, consistent typographic hierarchy.
- +1 Reverse-chronological order used correctly.

## 2. Skills (max 20)

Relevance and credibility of listed skills.

**Scoring**
- 18–20: Skills grouped (languages / frameworks / tools), relevant to target role, evidenced elsewhere in CV.
- 14–17: Relevant skills listed but flat (one long list) or partly unsupported.
- 10–13: Generic skills, some irrelevant, little grouping.
- 5–9: Vague ("good communication"), mostly soft skills, no technical depth.
- 0–4: No usable skills section.

**Deduct points**
- −2 Skills listed but never backed by experience/projects.
- −2 Self-rated bars/percentages (e.g. "Python 90%") with no basis.
- −2 Outdated or irrelevant tech dominating the list.
- −1 No grouping/categorization.

**Add points (within cap)**
- +2 Skills clearly map to the target role (or JD when provided).
- +1 Distinguishes core vs familiar tech honestly.

## 3. Experience (max 20)

Quality of the work-history section.

**Scoring**
- 18–20: Each role has impact-focused bullets with quantified outcomes (%, $, time, scale); clear progression.
- 14–17: Good responsibilities, some quantification, mostly action-led.
- 10–13: Duty-listing ("responsible for…") with little measurable impact.
- 5–9: Vague, no metrics, gaps unexplained.
- 0–4: Missing or unusable (titles only).

**Deduct points**
- −3 No quantified achievements anywhere.
- −2 Passive/duty phrasing instead of action verbs.
- −2 Unexplained gaps > 6 months.
- −1 Missing dates, titles, or company context.

**Add points (within cap)**
- +2 Strong metrics on most bullets.
- +1 Clear upward progression / increasing scope.
- +1 Action verbs + result pattern ("Did X using Y, achieving Z").

> Note: A junior/new-grad CV with little experience is scored relative to seniority —
> a thin experience section is expected and should lean on projects, not be punished twice.

## 4. Projects (max 20)

Especially important for juniors / career switchers.

**Scoring**
- 18–20: Relevant projects with problem → role → tech → outcome, links (repo/demo), clear ownership.
- 14–17: Good projects, decent description, some missing outcomes or links.
- 10–13: Projects listed but shallow ("built a todo app", no detail).
- 5–9: Tutorial clones only, no description of contribution.
- 0–4: No projects (heavier penalty for juniors, lighter for seniors with strong experience).

**Deduct points**
- −2 No description of personal contribution / role.
- −2 No tech stack mentioned.
- −2 No outcome, scale, or link.
- −1 Only generic tutorial projects.

**Add points (within cap)**
- +2 Live demo or source link provided.
- +1 Demonstrates depth (architecture, trade-offs, scale).

## 5. ATS Compatibility (max 20)

Will an Applicant Tracking System parse it correctly? See `kb/ats_rules.md` for detail.

**Scoring**
- 18–20: Single-column, standard fonts, standard section headers, text-based (not image), relevant keywords present.
- 14–17: Mostly ATS-safe, minor issues (icons, a graphic element).
- 10–13: Some risky elements (tables, columns) but parseable.
- 5–9: Multi-column/graphics-heavy, keywords sparse.
- 0–4: Image-based PDF, unreadable by ATS.

**Deduct points**
- −3 Multi-column layout that breaks parsing order.
- −3 Text embedded in images / scanned PDF.
- −2 Non-standard section headings (ATS can't categorize).
- −2 Tables/text boxes for core content.
- −2 Missing role-relevant keywords (esp. vs JD when provided).
- −1 Unusual fonts or special characters.

**Add points (within cap)**
- +2 Keyword coverage matches the target role / JD.
- +1 Standard headings + clean single-column layout.

---

## Calibration anchors

- **Strong senior CV** ≈ 85–95 overall.
- **Solid mid-level CV** ≈ 70–84.
- **Average junior CV** ≈ 55–69.
- **Needs major work** ≈ < 55.

## Rules for the scorer

1. Score only what's in the CV — never invent experience (see anti-hallucination in the prompt).
2. Be consistent: the same CV should get the same score (low temperature).
3. Always justify low categories in `weaknesses` and the fix in `suggestions`.
4. Seniority-aware: weight projects more for juniors, experience more for seniors.
5. When a JD is provided, skills + ats are judged against the JD's keywords.
