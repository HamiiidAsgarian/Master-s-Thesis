# Comprehensive Review Plan — ACADEMIC_v3_En.md

## Objective
Review the thesis manuscript against **two independent rule sets**:
1. **Rules.md** — IAU Ardabil formatting standards (English portion)
2. **AI-gen-flows.md** — Indicators and remediation of AI-generated academic text

---

## Phase A: Structural & Formatting Compliance (Rules.md)

### A1. Document Structure & Pagination
- [ ] Verify the sequence matches the IAU requirements (as relevant for an English thesis): Title page → Abstract → ToC → List of Tables → List of Figures → Chapters → References → Appendices → English Abstract.
- [ ] Ensure no raw Markdown syntax (`##`, `**bold**`, `- bullet`) survives in the final deliverable — convert to proper Word heading styles / LaTeX sectioning.
- [ ] Check page numbering: preliminary pages (lowercase Roman or Persian letters), body (Arabic numerals), bottom center.

### A2. English Typography (Rules.md §4.3)
- [ ] Body text: **Times New Roman 12pt**, justified.
- [ ] Chapter titles: **Times New Roman 25pt, Bold**, centred.
- [ ] Section headings: **Times New Roman 14pt, Bold**, left-aligned.
- [ ] Sub-section headings: **Times New Roman 12–13pt, Bold/Italic**.
- [ ] Code/programming snippets: **Courier New or Consolas 10–11pt**.
- [ ] English captions (tables & figures): **Times New Roman 11pt, Bold**.

### A3. Line Spacing & Paragraphs (Rules.md §5)
- [ ] Line spacing: **1.5× multiple** (or Exactly 28pt).
- [ ] Paragraph indent: **1 cm** first line (except first paragraph after a heading).
- [ ] Alignment: **Fully Justified** throughout.
- [ ] Paragraph length: 5–10 sentences (~100–200 words), one main idea per paragraph.
- [ ] Widow/orphan control enabled.

### A4. Numbering System (Rules.md §7 — Hyphen-Based)
- [ ] Confirm all headings follow `Chapter-Section-Sub` format (e.g., `3-2`, `4-1-3`). *The thesis already uses this convention — verify consistency.*
- [ ] Equation numbering: `(Chapter-Number)` format, right-aligned.
- [ ] Table/Figure numbering: `Chapter-Number` format (e.g., Table 4-1, Figure 4-2).

### A5. Figures, Tables & Captions (Rules.md §15)
- [ ] Table captions → **above** the table; Figure captions → **below** the figure.
- [ ] No vertical lines in tables; horizontal lines only (top, bottom, header separator).
- [ ] Every figure/table referenced in text *before* it appears.

### A6. Citations & References (Rules.md §16)
- [ ] Citation style: **Author-Date (Name, Year)** per Ardabil standard.
- [ ] All citations in the reference list must be cited in text and vice versa.
- [ ] Reference list: alphabetical by author surname.
- [ ] Every claim that is not common knowledge must be cited.

### A7. Chapter Content Requirements (Rules.md §19)
- [ ] **Ch. 1 (Introduction)**: Problem statement, significance, objectives, questions/hypotheses, operational definitions. *Verify no detailed literature review or results leak in.*
- [ ] **Ch. 2 (Literature Review)**: Theoretical framework, prior studies, research gaps. *Verify no methodology details or results appear.*
- [ ] **Ch. 3 (Methodology)**: Design, tools, parameters, procedure. *Verify no results or discussion here.*
- [ ] **Ch. 4 (Data Analysis)**: Objective presentation of findings with tables/charts. *Verify no interpretation or discussion creeps in — this should be purely descriptive.*
- [ ] **Ch. 5 (Discussion)**: Interpretation, comparison with prior work (Ch. 2), limitations, future work. *Verify no new data or new literature introduced.*

---

## Phase B: AI-Text Remediation (AI-gen-flows.md)

### B1. Structural Tells (Highest Priority)
- [ ] **Excessive heading levels**: Convert nested `###` / `####` sections into flowing prose where the content between headings is too short or fragmented. Aim for 2–3 section breaks per chapter maximum where prose naturally groups.
- [ ] **Bullet/list overuse**: Convert every bullet list into connected argument paragraphs, unless the list format is genuinely appropriate (research questions, inclusion criteria, a short enumeration of findings). Currently, §4-1, §4-2, §4-3, §4-4, §5-1 etc. contain bullet lists — each must be judged for necessity.
- [ ] **Bold of key terms mid-sentence**: Search for `**word**` patterns inside body paragraphs and remove nearly all instances. Use italics or natural emphasis via sentence structure instead.
- [ ] **Template-like section rhythm**: Check for repeated "framing sentence → bullet points → summary" pattern. Rewrite for varied paragraph structure.

### B2. Sentence & Paragraph Rhythm
- [ ] **Uniform sentence length**: Flag sections with repetitive short-medium-short cadence. Introduce longer subordinate-clause sentences and occasional short emphatic sentences naturally.
- [ ] **Formulaic paragraph shape**: Look for the "topic sentence → 3 supporting points → wrap-up sentence" pattern. Vary paragraph architecture — some paragraphs should build cumulative arguments, others compare/contrast, others analyse causality.
- [ ] **Short declarative "punchy" sentences**: Identify and rewrite blog-like emphatic fragments into denser academic prose (e.g., replace "The answer is unambiguous:" with integrated argumentation).

### B3. Lexical Red Flags
- [ ] Search and replace AI-style overused phrases:
  - `delve`, `furthermore`, `moreover`, `underscores`, `boasts`, `pivotal`, `robust` (when used vaguely), `tapestry`, `landscape`, `multifaceted`, `in today's world`, `it is important to note`, `plays a crucial role`, `showcases`.
- [ ] **Excessive hedging**: Check repeated phrases like `it could be argued that`, `this suggests that`, `further research is needed`. Anchor each to a specific finding, study, or limitation — never use as filler.
- [ ] **False balance**: Replace generic `On one hand… on the other hand…` with specific references to opposing studies or concrete methodological trade-offs.

### B4. Argumentative Depth & Originality
- [ ] **Literature synthesis depth**: In Ch. 2, verify that sources are critically *compared* (methodology, sample size, limitations, contradictory findings) rather than just summarised side-by-side. The current text has good coverage — check each paragraph for genuine synthesis vs. descriptive listing.
- [ ] **Research gap precision**: The gap statements in §2-7 are three enumerated items. Ensure each is a *precise, narrow, defensible gap* rather than a broad generalisation.
- [ ] **Authorial position**: Throughout Ch. 5, verify that the thesis stakes a clear, committed claim defended across sections, rather than staying neutrally descriptive. The current draft has strong positions (e.g., §5-4 on Innovator Effect) — ensure weaker sections follow suit.
- [ ] **Conclusion quality**: §5-7 and §5-8 must synthesise new insight from the analysis, not merely restate the introduction.

### B5. Citation & Evidence Rigour
- [ ] **Citation precision**: Every in-text citation should reference a *specific finding, methodology, or number* from the source — not just the source's general topic.
- [ ] **Methodological specificity**: Ch. 3 should include precise procedural detail (sample sizes, parameter choices, implementation specifics). Currently strong — verify no vague methods remain.
- [ ] **Reference list audit**: Cross-check every in-text citation against the reference list for consistency. Flag any source referenced vaguely without a clear match.

### B6. Repetition & Redundancy
- [ ] **Cross-chapter redundancy**: Search for concepts defined/explained multiple times (e.g., Jain's index defined in §3-3 and again in §3-7, OCEAN explained in §1-1 and §3-2). Consolidate: define once, refer back.
- [ ] **Intra-chapter restatement**: Identify paragraphs that make the same point with slightly different wording within the same section. Merge.
- [ ] **Obvious restatement**: Remove re-definitions of basic terms the reader already knows (e.g., explaining what Q-learning is each time it appears).

### B7. Tone & Voice
- [ ] **Overconfident/promotional tone**: Flag words like `showcases`, `highlights the importance`, `plays a crucial role`, `robust` (unsupported). Replace with measured academic language.
- [ ] **Limitations specificity**: §5-6 currently has detailed, specific limitations in four focused paragraphs — this is good. Verify no generic boilerplate (`time constraints`, `small sample size`) without context.
- [ ] **Genuine uncertainty**: In results interpretation (§4-10, §5-1), ensure statistical non-significance is acknowledged frankly and not papered over with directional language. The current text does this well — check for any lapses.

### B8. Markdown Conversion Preparation
- [ ] Convert entire document from `.md` to **Word (.docx)** or **LaTeX** as required.
- [ ] Replace all `#` heading markers with Word Heading 1/2/3 styles or LaTeX `\section{}` / `\subsection{}`.
- [ ] Convert all remaining raw Markdown formatting (`**bold**`, `*italic*`, `` `code` ``) to proper Word/LaTeX equivalents.
- [ ] Replace inline image links (`![...](../results/...)`) with embedded high-resolution (300+ DPI) figures.
- [ ] Convert all inline math (`$...$`) and display math (`$$...$$`) to the target editor's equation format.

---

## Execution Order

| Priority | Phase | Estimated Effort |
|----------|-------|------------------|
| 1 | **B1 — Structural tells** (most obvious to examiners) | High |
| 2 | **B2 + B3 — Sentence rhythm + Lexical fixes** | High |
| 3 | **A6 + B5 — Citations & references** | Medium |
| 4 | **B4 — Argumentative depth** (especially Ch. 2 & Ch. 5) | High |
| 5 | **A1–A5, A7 — Formatting compliance** | Medium |
| 6 | **B6 — Repetition removal** | Medium |
| 7 | **B7 — Tone adjustment** | Low |
| 8 | **B8 — Markdown → Word/LaTeX conversion** | Medium |

**Note**: Phase B (AI-text remediation) is prioritised over Phase A (formatting) because content quality carries more weight in thesis review. Formatting fixes are mechanical and can be applied later in batch.

---

## Verification

After all changes:
- [ ] Re-read the thesis end-to-end for flow and argument coherence.
- [ ] Run a final check of every citation against the reference list.
- [ ] Confirm all figures/tables are referenced in text and numbered correctly.
- [ ] Verify spelling and grammar (UK English throughout, consistent).
- [ ] Check that no raw Markdown syntax remains.
