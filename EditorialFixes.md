# EditorialFixes — ACADEMIC_v3.md vs Rules.md

## 1. Sub-Sectioning (Rule 9 — max 3 heading levels)

**Issue:** 4th-level headings (`####`) used in Chapter 4 for Quantitative Summary, Key Observations, Key Findings, Analysis, Quantitative Results, Interpretation, Key Finding, and Metric-to-Research-Question Mapping.

**Fix:** Remove all `####`. Turn them into bold lead-in sentences or absorb into the parent paragraph. Example:
- `#### Key Findings` → `**Key Findings:**` as first sentence of the paragraph.

---

## 2. Unnumbered Sub-Heading Labels (Rule 7 — hyphen-based numbering)

**Issue:** Labels like "Quantitative Summary", "Key Observations", "Key Findings", "Analysis", "Interpretation" under numbered sections have no hyphen-based number (e.g., `4-1-1`).

**Fix:** Since 4th heading levels are banned (see #1), integrate these as bold text leads — no numbering needed.

---

## 3. Chapter Title Format (Rule 9 — colon separator)

**Issue:** `## 1- Introduction and Generalities` uses a hyphen after the chapter number. Rule 9 example shows `فصل دوم: ادبیات تحقیق` (colon, not hyphen).

**Fix:** Change to `## Chapter 1: Introduction and Generalities` (and similarly for chapters 2–5).

---

## 4. Equation Numbering (Rule 14 — no "Eq." prefix)

**Issue:** All equations use `(Eq. 3-1)` instead of just `(3-1)`. Rule 14 shows format as `(Chapter-Number)`, e.g., `(6-8)`.

**Fix:** Remove "Eq." from all equation labels. `(Eq. 3-1)` → `(3-1)`. Affected lines: 135, 177, 238, 250, 291, 446, 452, 458, 464, 479, 491.

---

## 5. Bullet Points / Lists (Rule 13)

**Issue a — Missing colon before lists:** Several lists lack a preceding colon. E.g., line 66 lists sub-questions with no colon before the numbered list.

**Fix:** Ensure every list is introduced with a colon (`:`).

**Issue b — Fragment vs sentence inconsistency:** Line 75–78 definition list uses fragments without periods (correct), but some bullet lists mix full sentences and fragments.

**Fix:** Verify each list: full sentences = capitalize + period; fragments = no period. Keep parallel structure.

**Issue c — Overuse of bullets for 1-2 items:** Some lists have only 2 items (e.g., Phase 1 and Phase 2 in 3-5). Rule says reserve bullets for 3+.

**Fix:** Convert 1–2 item lists into plain text paragraphs.

---

## 6. Sentence Length (Rule 12 — max 35 words)

**Issue:** Some sentences exceed 35 words. Examples:
- Line 84 (~40 words): "In this emerging paradigm, residential households have transitioned from passive consumers into prosumers who generate renewable energy through solar photovoltaics (PV), manage local demand, and store energy in battery energy storage systems (BESS) (Rathnayaka et al., 2014)."
- Line 123 (~60 words): First sentence of 2-7 Research Gaps.
- Line 852 (~85 words): First sentence of Limitations.
- Line 856 (~85 words): Network scope paragraph.
- Line 258 (~45 words).

**Fix:** Split sentences over 35 words into two or more shorter sentences.

---

## 7. Paragraph Structure (Rule 5 — 5–10 sentences, 100–200 words)

**Issue:** Many paragraphs are very long (10+ sentences, 250+ words). Examples:
- Line 84 (2-1): single paragraph covering entire section.
- Line 557–559: one paragraph with 8+ sentences and ~200 words.
- Line 852–860: Limitations section has paragraphs of 80–85 words per sentence, extremely dense.

**Fix:** Break paragraphs longer than ~200 words / 10 sentences into smaller units, each covering one idea.

---

## 8. Bold Overuse (Rule 10 — bold only for headings and first-use key terms)

**Issue:** `**Finding 1:**` through `**Finding 5:**` in Section 5-8 use bold for emphasis in body text. Also `**Key Findings:**`, `**Quantitative Summary:**`, etc. (but those will be fixed by issue #1).

**Fix:** Remove bold from Finding labels in 5-8 — use plain text or italic.

---

## 9. Citation Format (Rule 16.1 — Ardabil standard)

**Issue:** Current uses APA `(Author, Year)` e.g., `(Rathnayaka et al., 2014)`. Ardabil standard requires first AND last name: `(Rathnayaka, J., 2014)`.

**Fix:** Either switch to `(Last, First, Year)` format, or confirm with supervisor that APA is approved as an alternative (Rule 16.2).

---

## 10. Reference Order (Rule 16.3 — Farsi first)

**Issue:** References list has only English sources. If the full thesis includes Persian sources, they must come first.

**Fix:** Either add a "Persian References" section before "Non-Persian References", or note that ACADEMIC_v3.md is the English-only portion and Persian refs will be added in the Persian version.

---

## 11. Image Paths (Practical issue)

**Issue:** All images reference `../results/*.png` — these files do not exist in the repository.

**Fix:** Either place images at the expected path, or update paths to the actual locations.

---

## 12. Table Captions (Rule 15 — placement)

**Issue:** Some table captions use bold markdown `**Table X-Y:**` which is fine, but verify that in the final Word rendering, table captions are placed ABOVE the table (currently correct in markdown).

**Fix:** No change needed in markdown, but verify in final Word output.
