# ATS Rules — V1

Reference for the `ats` scoring category. ATS = Applicant Tracking System: software
that parses a CV into structured fields before a human ever sees it. A CV that looks
great to a human can score 0 in an ATS if it can't be parsed.

## How ATS reads a CV

1. Extracts raw text from the file (PDF text layer or DOCX).
2. Splits it into sections using **standard headings**.
3. Pulls out fields: name, contact, skills, experience, education, dates.
4. Matches keywords against the job posting.

If any step fails, the candidate is filtered out automatically.

## DO (ATS-safe)

- **Single-column** layout. ATS reads left-to-right, top-to-bottom.
- **Standard section headings**: `Summary`, `Skills`, `Experience` / `Work Experience`,
  `Projects`, `Education`, `Certifications`.
- **Standard fonts**: Arial, Calibri, Helvetica, Times New Roman, Georgia.
- **Real, selectable text** — export as a text-based PDF, never a scan/screenshot.
- **Simple bullets** (`•` or `-`).
- **Consistent dates**: `MMM YYYY – MMM YYYY` (e.g. `Jan 2022 – Present`).
- **Standard file types**: `.pdf` (text layer) or `.docx`.
- **Spell out then abbreviate**: `Continuous Integration (CI)` so both match.
- **Relevant keywords** taken from the target role / JD, used naturally.

## DON'T (breaks parsing)

- ❌ Multi-column / newspaper layouts — text order gets scrambled.
- ❌ Tables or text boxes for core content (skills, experience).
- ❌ Images, icons, logos carrying information; photos.
- ❌ Text inside images / fully scanned PDFs.
- ❌ Headers/footers holding contact info (often ignored by parsers).
- ❌ Fancy/decorative or non-embedded fonts.
- ❌ Special characters/emoji as bullets or separators.
- ❌ Creative section names ("My Journey", "What I Bring") — ATS can't categorize them.
- ❌ Graphics-heavy templates from design tools exported as flat images.

## Keyword matching

- Mirror the exact terminology of the job posting (e.g. "React.js" vs "ReactJS" — use what the JD uses, or both).
- Include both the acronym and full form once: `AWS (Amazon Web Services)`.
- Put core skills in a dedicated `Skills` section **and** demonstrate them in experience/projects.
- Avoid keyword stuffing — repetition without context reads as spam to modern ATS + recruiters.

## Quick ATS checklist (maps to the `ats` rubric category)

- [ ] Single column
- [ ] Standard headings
- [ ] Selectable text (not an image)
- [ ] Standard font
- [ ] Contact info in the body (not only header/footer)
- [ ] No tables/text boxes for core content
- [ ] Consistent date format
- [ ] Role/JD keywords present and contextual
- [ ] Exported as text PDF or DOCX
