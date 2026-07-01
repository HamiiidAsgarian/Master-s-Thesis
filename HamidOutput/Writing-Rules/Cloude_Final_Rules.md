# Islamic Azad University, Ardabil Branch — M.Sc. Software Engineering

# Comprehensive Thesis Rulebook (Reconciled Draft)

> **⚠️ VERIFICATION NOTICE — READ FIRST**
> This document reconciles two sources: (1) web research aggregated from multiple IAU branches' published regulations, and (2) an AI-agent-produced file claiming Ardabil-specific detail. **Neither source could be confirmed against the current live Ardabil branch PDF** (site access was blocked during research). Wherever the two sources conflicted, both values are shown with a **[VERIFY]** flag. Before binding your final copy, confirm every flagged item with:
>
> - Your supervisor (استاد راهنما)
> - The Ardabil Graduate Studies Office (اداره تحصیلات تکمیلی، دانشگاه آزاد اردبیل)
> - The current official شیوه‌نامه (style guide) PDF on `ardabil.iau.ir`
>
> Software Engineering theses at IAU commonly follow the general Computer Engineering/CS format **plus** department-specific content chapters (requirements specs, architecture, UML) — confirm with your SE department head whether a supplementary SE-specific annex exists.

---

## PART A — DOCUMENT STRUCTURE

### A.1 Full Page Order

| #   | Section                                          | Persian                           | Page Label | Notes                                                                                     |
| --- | ------------------------------------------------ | --------------------------------- | ---------- | ----------------------------------------------------------------------------------------- |
| –   | Hardcover front cover                            | جلد                               | —          | See Part B                                                                                |
| –   | Blank buffer page                                | —                                 | —          | No visible number                                                                         |
| 1   | Bismillah page                                   | بسم‌الله الرحمن الرحیم            | الف        | Centered, no visible number but counted                                                   |
| 2   | Persian title page (copy of cover)               | صفحه عنوان فارسی                  | ب          | Exact duplicate of cover text                                                             |
| 3   | Board/defense approval page                      | صورتجلسه دفاع                     | ج/د        | Signed by committee — obtain after defense                                                |
| 4   | Declaration of originality                       | تعهدنامه اصالت اثر                | —          | Increasingly mandatory university-wide; confirm requirement                               |
| 5   | Dedication (optional)                            | تقدیم‌نامه                        | —          | Max 1 page                                                                                |
| 6   | Acknowledgements (optional)                      | سپاسگزاری                         | —          | Max 1 page                                                                                |
| 7   | Table of Contents                                | فهرست مطالب                       | —          | **Auto-generated** from Word Heading styles — never typed manually                        |
| 8   | List of Tables                                   | فهرست جداول                       | —          | Auto-generated from caption tool                                                          |
| 9   | List of Figures                                  | فهرست اشکال/نمودارها              | —          | Auto-generated from caption tool                                                          |
| 10  | List of Abbreviations/Symbols                    | فهرست علائم و اختصارات            | —          | Required if >5 abbreviations used (common in SE due to technical acronyms)                |
| 11  | Persian Abstract                                 | چکیده فارسی                       | —          | 250–300 words (some sources say max 1–2 pages); one paragraph, no citations, 3–5 keywords |
| 12  | **Chapter 1 – Introduction**                     | فصل اول: کلیات تحقیق              | ۱, ۲...    | Arabic numeral pagination starts here                                                     |
| 13  | **Chapter 2 – Literature Review / Related Work** | فصل دوم: ادبیات و پیشینه تحقیق    |            |                                                                                           |
| 14  | **Chapter 3 – Methodology / Proposed Method**    | فصل سوم: روش تحقیق / روش پیشنهادی |            | For SE: system design, architecture, algorithms                                           |
| 15  | **Chapter 4 – Implementation & Results**         | فصل چهارم: پیاده‌سازی و نتایج     |            | For SE: implementation details, testing, evaluation metrics                               |
| 16  | **Chapter 5 – Discussion & Conclusion**          | فصل پنجم: بحث و نتیجه‌گیری        |            |                                                                                           |
| 17  | References                                       | فهرست منابع                       | —          | Persian sources first, then non-Persian, each alphabetized separately                     |
| 18  | Appendices                                       | پیوست‌ها                          | —          | Source code excerpts, questionnaires, raw data, UML diagrams if not in-body               |
| 19  | English Abstract                                 | Abstract                          | —          | Faithful translation of Persian abstract, one paragraph, with keywords                    |
| 20  | English Title Page                               | English Title Page                | —          | Full English translation of cover                                                         |
| –   | Back cover                                       | جلد پشتی                          | —          | English title in matching embossing                                                       |

### A.2 Software Engineering–Specific Content Additions

Unlike a generic CS thesis, an SE thesis typically requires these embedded elements (check with supervisor which are mandatory for your specific track — data mining, software architecture, testing, AI/ML applications in SE, etc.):

- **Requirements specification** (functional & non-functional) — usually in Chapter 3
- **System architecture diagrams** (UML: use-case, class, sequence, activity, deployment diagrams) — properly numbered/captioned like any figure
- **Design rationale / design patterns used**, if applicable
- **Evaluation methodology**: metrics used (accuracy, precision/recall, performance benchmarks, complexity analysis, usability testing, etc.) — must be explicit and reproducible
- **Testing chapter or section**: unit/integration/system testing approach and results, if the thesis involves a built system
- **Threats to validity** subsection (common in SE research, sometimes required in Chapter 5 alongside Limitations)

---

## PART B — PHYSICAL BINDING & COVER

| Element                   | Specification                                                                                                           | Confidence                                                                                                                                                      |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Cover color (Master's)    | Dark navy/blue (سرمه‌ای / آبی تیره)                                                                                     | Both sources agree — high confidence                                                                                                                            |
| Stamping color            | **[VERIFY]** — one source says silver (نقره‌کوب), general IAU convention is often gold (زرکوب) for gallingor covers     | Conflicting — confirm with binder/print shop that handles IAU Ardabil theses regularly, they'll know current convention                                         |
| Binding type              | Hardcover (گالینگور)                                                                                                    | Agreed                                                                                                                                                          |
| University logo placement | Top-center is the more common IAU-wide convention; one source claims top-left 4×3cm                                     | **[VERIFY]**                                                                                                                                                    |
| Spine (عطف)               | Title + author name embossed                                                                                            | Agreed                                                                                                                                                          |
| Printing sides            | **[VERIFY]** — one-sided is the more traditional/common IAU requirement; one source claims double-sided                 | Confirm — this affects your whole print job, check before printing                                                                                              |
| Bound copies required     | Typically 3–5 copies (department, supervisor, library, co-supervisor, student) — exact number varies by year/department | **[VERIFY exact count with department]**                                                                                                                        |
| Digital submission        | Word (.docx) + PDF, often via IAU's Irandoc/thesis portal upload as well as physical CD                                 | **[VERIFY current submission method — many IAU branches have moved to online-only portal submission (ganj.irandoc.ac.ir or similar) rather than physical CDs]** |

---

## PART C — PAGE SETUP

| Setting                | Value A (general IAU, multi-branch sourced) | Value B (claimed Ardabil-specific) | Action                                                       |
| ---------------------- | ------------------------------------------- | ---------------------------------- | ------------------------------------------------------------ |
| Paper size             | A4 (21 × 29.7 cm)                           | A4                                 | ✅ Agreed                                                    |
| Top margin             | 3.5 cm                                      | 3 cm                               | **[VERIFY]**                                                 |
| Bottom margin          | 3–3.5 cm                                    | 3 cm                               | **[VERIFY]**                                                 |
| Right margin           | 3.5 cm                                      | 3 cm                               | **[VERIFY]**                                                 |
| Left margin            | 2.5 cm (extra room reserved for binding)    | 2 cm                               | **[VERIFY]** — binding-side margin matters most, don't guess |
| Header/footer distance | 1.5 cm from edge                            | 1.5 cm from edge                   | ✅ Agreed                                                    |
| Lines per page         | ~22 lines                                   | Not specified                      | Use as a sanity check once your font/spacing is finalized    |

**Practical fix:** Set up your Word template with placeholder margins, then before you commit to writing 80+ pages, print **one sample page** and have your supervisor confirm it visually matches a previously-approved Ardabil SE thesis. This is more reliable than any web-sourced number.

---

## PART D — FONTS & TYPOGRAPHY

### D.1 Persian Text

| Element                      | Font (best available guess)                          | Size                                                                                  | Style          |
| ---------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------- | -------------- |
| Chapter titles               | B Lotus Bold or B Titr                               | 16–25 (sources disagree — likely 16 is safer/more standard; 25 seems unusually large) | Bold, new page |
| Section headings (1st level) | B Lotus Bold or B Nazanin Bold                       | 14                                                                                    | Bold           |
| Sub-headings (2nd level)     | B Lotus Bold or B Nazanin Bold                       | 12–13                                                                                 | Bold           |
| Sub-sub-headings (3rd level) | Same family                                          | 12                                                                                    | Bold/Italic    |
| Body text                    | **B Lotus or B Nazanin** (pick ONE, stay consistent) | 14                                                                                    | Normal         |
| Figure/table captions        | Same as body, bold                                   | 11–12                                                                                 | Bold           |
| Footnotes                    | Same family                                          | 10–12                                                                                 | Normal         |

**[VERIFY] font family** — Lotus vs. Nazanin vs. Zar vs. Titr — this is the single most-cited inconsistency across all IAU branch documents found in research. **Do not guess: ask your department for the exact `.dotx` Word template file if one exists — almost every IAU department has one and it removes all font ambiguity instantly.**

### D.2 English Text

| Element                        | Font                    | Size                             | Style              |
| ------------------------------ | ----------------------- | -------------------------------- | ------------------ |
| Body text                      | Times New Roman         | 12                               | Normal             |
| Chapter titles (English pages) | Times New Roman         | Match Persian chapter title size | Bold               |
| Headings                       | Times New Roman         | 12–14                            | Bold               |
| Code/programming listings      | Courier New or Consolas | 10–11                            | Normal, monospaced |
| Captions                       | Times New Roman         | 10–11                            | Bold               |

### D.3 Non-Negotiable Rules

- Never mix Persian font families within the same text level (e.g., don't use Lotus for one heading and Nazanin for another).
- Any English word/term inside a Persian sentence switches font to Times New Roman inline.
- No underlining anywhere — use bold or italic instead.
- Bold + Italic combined only for the deepest sub-heading level, if at all.
- Code snippets/algorithms in monospace font, left-aligned, LTR, even inside an otherwise-RTL document.

---

## PART E — SPACING, ALIGNMENT & PARAGRAPHS

| Element                      | Rule                                                                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Line spacing (body)          | Single spacing, roughly equivalent to 1–1.5 cm between lines — **[VERIFY exact Word "Line Spacing" value with your template]** |
| Line spacing (abstract)      | Tighter single spacing                                                                                                         |
| Paragraph first-line indent  | ~1 cm (some styles use Tab instead — check template)                                                                           |
| Space between paragraphs     | Either one blank line OR paragraph "space after" setting — pick one method and use consistently, don't do both                 |
| Alignment                    | **Justified** for all body text (Ctrl+J), both Persian and English                                                             |
| Text direction               | RTL for Persian, LTR for English — set via Word's paragraph direction, not manual spacing tricks                               |
| Widow/orphan control         | ON — prevents a single line from being stranded at top/bottom of a page                                                        |
| Heading-then-text page break | A heading must have at least 2 lines of body text below it before a page break — no orphaned headings                          |

---

## PART F — NUMBERING SYSTEMS

### F.1 Section/Chapter Numbering

- Chapter-Section-Subsection format: `2-4-3` = Chapter 2, Section 4, Subsection 3.
- Maximum recommended depth: 3–4 levels. Beyond that, use lettered lists `(الف)`, `(ب)` instead of further numeric nesting.
- Implement via Word's **Multilevel List** linked to Heading 1/2/3 styles — never type section numbers manually (this breaks the moment you reorder sections, and is a dead giveaway of rushed/AI-assisted work if numbers end up inconsistent).

### F.2 Page Numbering

| Section                                  | Format                                                       | Position      |
| ---------------------------------------- | ------------------------------------------------------------ | ------------- |
| Preliminary pages (Bismillah → Abstract) | Persian abjad letters (الف، ب، پ...)                         | Bottom-center |
| Main body (Ch.1 → References)            | Arabic numerals (۱، ۲، ۳...), restarting at 1 from Chapter 1 | Bottom-center |
| Cover/title pages                        | No visible number                                            | —             |

Use Word **Section Breaks (Next Page)** to switch numbering formats between the preliminary and main sections — this is the #1 technical mistake students make (numbers either don't reset or carry the wrong format).

### F.3 Figures, Tables, Equations

- All numbered **by chapter**, not continuously through the whole thesis: `Figure 3-2` = 2nd figure in Chapter 3.
- **Table captions go ABOVE the table.**
- **Figure captions go BELOW the figure.**
- Equations numbered in parentheses, chapter-based: `(3-5)` = 5th equation in Chapter 3, typically right-aligned in Persian text but the equation itself often stays LTR.
- Every figure, table, and equation **must be referenced in the surrounding text** — never insert a visual with no textual pointer to it.

---

## PART G — CITATIONS & REFERENCES

| Element                                  | Rule                                                                                                                                                                                              |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Primary in-text style**                | Author-Year, e.g., (Rahimi, 2023) or (رحیمی، ۱۴۰۲) — this is the IAU-wide default                                                                                                                 |
| **Alternative (if supervisor requires)** | IEEE numeric `[1]` — common in CS/SE internationally; **confirm which your specific SE department mandates, as this varies more by department than by branch**                                    |
| Reference list order                     | Persian/Arabic sources first (alphabetical by surname), then non-Persian sources (alphabetical by surname), listed separately                                                                     |
| Direct quotes                            | Must include page number; short quotes (<40 words) use « » guillemets inline; long quotes (≥40 words) become an indented block, single-spaced, no quotation marks                                 |
| Every claim                              | Must be cited unless common knowledge — uncited claims are one of the most common reasons for revision requests                                                                                   |
| Consistency                              | **Pick ONE citation style and use it for 100% of the thesis** — mixing APA and IEEE mid-document is an immediate red flag to examiners and a common tell of stitched-together AI-assisted writing |

---

## PART H — LANGUAGE, SENTENCE & AI-TEXT MISTAKE CHECKLIST

This is the part most directly relevant to using AI tools for drafting — the formatting rules above are necessary but not sufficient. Examiners increasingly screen for these specific tells:

### H.1 Sentence & Paragraph Mechanics

- [ ] Average sentence length 15–25 words; hard ceiling ~35 words — AI drafts often oscillate between very short punchy sentences and one very long one; human academic writing has more natural, less bimodal variation.
- [ ] Each paragraph covers **one idea**, roughly 100–200 words (5–10 sentences) — avoid AI's tendency toward short, choppy 2–3 sentence paragraphs that read like blog posts.
- [ ] No repeated formulaic paragraph shape (topic sentence → 3 points → summary sentence) repeated identically across every section.

### H.2 Formatting Discipline (Markdown Leakage)

- [ ] **Zero raw Markdown syntax** in the final Word document — no stray `**`, `##`, `-`, or `*` characters left over from AI-generated drafts. This is the single most common giveaway of unedited AI-assisted writing and instantly signals to an examiner that the text wasn't manually typeset.
- [ ] Bullet/numbered lists reserved for genuinely sequential or enumerable content (requirements lists, algorithm steps, inclusion criteria) — not for arguments, literature synthesis, or discussion, which should be continuous prose.
- [ ] No AI-typical bolding of "key terms" mid-sentence for emphasis — bold is reserved strictly for headings/captions per Part D.

### H.3 Vocabulary & Tone

- [ ] Avoid overused AI-vocabulary: _delve, moreover, furthermore, underscores, pivotal, robust, multifaceted, tapestry, landscape, in today's world, it is important to note._
- [ ] No generic hedging clichés repeated verbatim without being anchored to a specific study or dataset ("further research is needed" with no specifics).
- [ ] Formal, objective register throughout — no colloquialisms, no promotional/marketing-style phrasing ("showcases," "plays a crucial role," "highlights the importance").

### H.4 Argumentative Substance (What Examiners Actually Check)

- [ ] Chapter 2 (Literature Review) **critically compares and synthesizes** sources — contrasting methodologies, sample sizes, contradictory findings — rather than listing summaries side-by-side. This is the single biggest quality gap between AI-drafted and genuine graduate-level lit reviews.
- [ ] Research gap is stated **narrowly and specifically**, tied to concrete limitations of prior SE work you reviewed — not a generic "more research is needed in this area."
- [ ] Chapter 4 (Results) is strictly descriptive/objective — no interpretation or discussion leaking in (that belongs in Chapter 5 only).
- [ ] Chapter 5 includes **specific, study-tied limitations** (e.g., "our dataset was limited to X samples from Y domain, limiting generalizability to Z") rather than generic boilerplate limitations.
- [ ] All citations correspond to real, checkable sources with correct years/authors — fabricated or approximate citations (a known AI failure mode) are grounds for serious academic integrity concerns, not just a formatting deduction.

### H.5 Final Pre-Submission Pass

- [ ] Read the entire thesis aloud (or have someone else read it) — AI-drafted text often "sounds" subtly uniform in rhythm even when grammatically correct; a read-aloud pass catches this quickly.
- [ ] Run a plagiarism/similarity check (required by most IAU branches, often via Samim Noor or Irandoc systems) — confirm which tool Ardabil currently mandates.
- [ ] Verify every acronym is expanded on first use, every figure/table/equation is referenced, and every reference list entry corresponds to an actual in-text citation (and vice versa) — these cross-reference mismatches are extremely common when text has been AI-assisted and lightly edited.

---

## PART I — FINAL SUBMISSION CHECKLIST

- [ ] Confirm cover color, stamping color, binding type, and number of physical copies with department **[VERIFY — flagged as conflicting above]**
- [ ] Confirm exact margins against official template or sample approved thesis **[VERIFY]**
- [ ] Confirm font family (Lotus vs. Nazanin vs. Zar) — ideally obtain the department's official `.dotx` template
- [ ] Confirm current digital submission method (CD vs. portal upload) **[VERIFY — likely to have changed to online-only]**
- [ ] Confirm citation style mandated specifically by your SE supervisor/department (APA vs. IEEE)
- [ ] Confirm plagiarism-check tool and required similarity threshold
- [ ] All preliminary pages present and correctly ordered (Part A.1)
- [ ] All figures/tables/equations numbered by chapter, captioned correctly, and referenced in text
- [ ] Reference list fully cross-matched with in-text citations
- [ ] No leftover Markdown syntax or AI-vocabulary tells (Part H)
- [ ] Table of Contents, List of Figures, List of Tables all auto-generated (not manually typed) and refreshed as the final step before printing

---

_This document is a reconciled research aid, not an official university publication. The [VERIFY] flags are not optional — treat them as open questions to close with your department before final printing, not minor details._
