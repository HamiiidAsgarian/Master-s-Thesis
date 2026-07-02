# Instructions for Translating an English Markdown Thesis into a Farsi Academic Thesis (IAU Standard)

> **Purpose:** This is a working checklist for an AI agent (or human translator) converting a completed English-language Markdown thesis into a publication-ready Farsi academic thesis matching Islamic Azad University conventions. Formatting rules (margins, fonts, numbering) are covered in the companion Rulebook — this document focuses specifically on **translation accuracy, academic register, and structural conversion risks**.
>
> **Terminology:** A complete locked glossary of 260+ terms with verified Farsi equivalents is in `Dictionary.md`. Consult it before translating any chapter — inconsistent term translation is the single most visible error to examiners.

---

## PART 1 — BEFORE TRANSLATING: SETUP RISKS

### 1.1 Never translate sentence-by-sentence in isolation

- [ ] Read and understand the **entire chapter** before translating any of it. Persian academic prose restructures at the paragraph level, not the sentence level — a mechanical sentence-by-sentence pass produces grammatically correct but stylistically foreign-sounding Farsi (a strong "translated" tell to any Farsi-speaking examiner).
- [ ] Identify the core claim of each paragraph first, then rebuild it in natural Farsi paragraph structure — don't preserve English sentence boundaries as a default.

### 1.2 Build a terminology glossary FIRST, before translating a single chapter

- [ ] A comprehensive glossary of 260+ terms already exists in `Dictionary.md` — **read it in full before translating**. It covers all RL/MARL, energy, psychology, statistics, and thesis-specific terms with locked Farsi equivalents.
- [ ] **Lock the glossary before translating** — this is the single biggest cause of inconsistency in AI-assisted translations: the same English term getting translated 3 different ways across 5 chapters (e.g., "framework" → چارچوب in Chapter 2, ساختار in Chapter 3, فریم‌ورک in Chapter 4).
- [ ] For terms with no clean Farsi equivalent (common in CS/SE — "microservice," "API," "container"), decide once whether to: (a) keep the English term italicized in Latin script, (b) transliterate into Farsi script, or (c) use the Farsi equivalent with the English term in parentheses on first use. Apply that decision uniformly.
- [ ] After translating each chapter, run a **terminology consistency audit**: search the Farsi text for every glossary term and confirm it was used identically everywhere.

### 1.3 Decide the register up front

- [ ] Confirm this is **formal written Persian (فارسی نوشتاری رسمی)** — not conversational Persian, not the Persian used in casual technical blogs/tutorials. This affects verb forms, sentence connectors, and vocabulary choice throughout.
- [ ] Confirm whether the department wants first-person plural ("ما بررسی می‌کنیم" / "we examine") or passive/impersonal constructions ("بررسی می‌شود" / "it is examined") — Persian academic writing leans passive/impersonal more than modern English CS writing does. Default to impersonal unless supervisor explicitly allows first person.

---

## PART 2 — HIGH-RISK TRANSLATION ERRORS (Priority Order)

### 2.1 Literal/Calque Translation (Highest-Frequency Error)

- English syntax directly mapped into Farsi word order produces "translationese" — grammatically parseable but immediately recognizable as machine-translated, not authored in Farsi.
- **Symptom to watch for:** long strings of prepositional phrases stacked in English order, relative clauses translated word-for-word, or English idioms translated literally (e.g., "on the other hand" → literal calque instead of the natural Farsi equivalent «از سوی دیگر»/«از طرفی»).
- **Fix:** After translating a paragraph, ask "would a Farsi-speaking Software Engineering professor write it this way?" — if not, restructure rather than patch.

### 2.2 Word Order (SOV vs SVO)

- English is Subject-Verb-Object; Persian is fundamentally Subject-Object-Verb, with the verb almost always sentence-final in formal writing.
- A direct translation that leaves the verb mid-sentence (mimicking English structure) is a very strong "translated, not written" signal.
- **Fix:** Actively move the verb to the end of the clause during translation — don't just substitute words in place.

### 2.3 Passive Voice & Impersonal Constructions

- Persian academic writing uses impersonal/passive constructions more heavily than contemporary English CS writing (which increasingly favors active "we propose," "we implement").
- Translating "we implemented the system using..." literally into first-person Farsi can read as informal if the department expects impersonal register.
- **Fix:** Default to impersonal passive (سیستم با استفاده از ... پیاده‌سازی شد) unless the supervisor has approved first-person Farsi.

### 2.4 Tense and Aspect Mismatches

- English's rich tense system (present perfect, past perfect, conditional) doesn't map 1:1 onto Persian tenses.
- Common error: over-literal rendering of "has been shown that..." or "would have resulted in..." produces awkward, non-native tense stacking in Farsi.
- **Fix:** Simplify to the tense a Farsi academic writer would naturally use for that logical relationship (usually simple past or present perfect در حالت ساده), not a mechanical tense-for-tense substitution.

### 2.5 Compound/Technical Noun Phrases

- English stacks nouns freely ("machine learning model performance evaluation metrics") — Persian cannot stack nouns the same way and requires **ezafe constructions** (کسره اضافه) or restructuring into phrases.
- **Fix:** Break these into properly connected Persian noun phrases (e.g., "معیارهای ارزیابی عملکرد مدل یادگیری ماشین") rather than mechanically translating word order.

### 2.6 Numbers, Digits, and Dates

- [ ] Decide whether the thesis uses **Persian digits (۰-۹)** or **Arabic/Western digits (0-9)** — IAU convention typically uses Persian digits in body text but this varies by department; **[VERIFY]**.
- [ ] Be consistent — don't mix Persian and Western digits within the same document, and definitely not within the same table.
- [ ] Convert all dates: the English thesis's Gregorian dates must be converted to **Solar Hijri (Jalali) calendar** dates for any Persian-context references (submission date, historical references to Iranian events, etc.) — but **keep Gregorian dates for international publication dates and citations** (e.g., a 2023 journal article citation stays 2023, not ۱۴۰۲).
- [ ] Watch for silent unit/number-format errors: decimal separators, thousand separators, and percentage formatting differ by convention — verify each converted number rather than assuming a 1:1 copy is safe.

### 2.7 Acronyms and Abbreviations

- English acronyms (CNN, API, IEEE, RMSE) generally **stay in Latin script** even inside Farsi text — do not transliterate acronyms into Farsi letters.
- On first use, provide the full Farsi term followed by the English acronym in parentheses: «شبکه عصبی کانولوشنی (CNN)».
- After first use, the acronym alone is used — but confirm it's the same acronym form used consistently in your glossary (Part 1.2).

### 2.8 Citations and In-Text References

- **Do not translate author names or reference titles.** Author names stay in Latin script exactly as published; only the surrounding Farsi sentence is translated.
- In-text citation format must match whichever style (Author-Year vs IEEE numeric) the Rulebook specifies — verify the English thesis's citation style doesn't get silently altered during translation.
- Reference list: Persian sources and non-Persian (English) sources must be **split into two separate alphabetized lists** in the final Farsi thesis — this is a structural change from a typical single-list English references section, not just a translation task.
- **Do not "translate" journal names, publisher names, or DOIs** — these remain in their original language/form always.

### 2.9 Equations, Code, Variables

- Equations, source code, variable names, and function names are **never translated** — they remain exactly as in the English original.
- However, the **surrounding explanatory prose** referencing them must read naturally in Farsi, and equation/figure/table numbering must be converted to the chapter-based numbering scheme required by the Farsi thesis structure (see companion Rulebook Part F), which may differ from the English original's numbering.
- Code blocks/algorithms remain LTR and in monospace font even inside the RTL document — verify Word's bidi (bi-directional text) settings don't corrupt code formatting during conversion.

### 2.10 Figure and Table Text

- Any text baked into images (chart axis labels, diagram labels) ideally should be regenerated in Farsi, not left in English, if it's meant to be a "Farsi thesis" — flag this explicitly to the user, since it requires regenerating the visual assets, not just translating surrounding text. If regenerating isn't feasible, at minimum note this as an open item rather than silently leaving all figures in English.

---

## PART 3 — STRUCTURAL CONVERSION (Markdown → Farsi Thesis Document)

### 3.1 Markdown Artifacts Must Not Survive

- [ ] Strip all raw Markdown syntax (`#`, `##`, `**`, `-`, `*`, ` ``` `) during conversion — these must become actual Word heading styles, bold formatting, and list formatting, not literal characters left in the Farsi text.
- [ ] Markdown's typical heavy use of bullet points and headers (common in English MD drafts, including AI-assisted ones) should be **converted into continuous Farsi academic prose** wherever the content is argumentative (literature review, discussion) — see the companion document on AI-text tells. Do not just translate bullet points into Farsi bullet points if the original bulleting was itself already a symptom of under-developed prose.

### 3.2 Chapter/Section Structure May Not Map 1:1

- English theses (especially ones drafted informally in Markdown) often don't follow the rigid 5-chapter IAU structure. Before translating, **reorganize the English content into the required Farsi structure first** (see companion Rulebook Part A.1: Introduction → Literature Review → Methodology → Results → Discussion), rather than translating chapter-by-chapter and hoping the structures happen to align.
- Flag to the user any content that doesn't cleanly map (e.g., an English thesis with a combined "Results and Discussion" chapter must be split to match IAU's separate Chapter 4/Chapter 5 requirement — this is a content reorganization task, not a translation task).

### 3.3 Abstract Requires Independent (Not Mechanical) Translation

- The Farsi abstract (چکیده) has its own word-count and single-paragraph constraints (typically 250–300 words) — a direct translation of an English abstract may run long or short.
- **Write the Farsi abstract as a fresh, self-contained academic summary**, not a mechanical translation, then verify it against the English abstract for factual/scope consistency (they must say the same thing, but don't need to be sentence-for-sentence parallel).
- The English abstract at the end of the document should match the _content_ of the Farsi one exactly — if you revise the Farsi abstract during editing, the English abstract must be updated too, and vice versa. This bidirectional sync is a common point of silent drift.

### 3.4 Title Page Translation

- Thesis title translation deserves special care — a literal translation of an English academic title often sounds awkward in Farsi. Farsi academic titles frequently restructure using ezafe constructions and different word order than a literal rendering would produce. Get supervisor sign-off on the Farsi title specifically, since it appears on the cover and is hard to revise post-binding.

---

## PART 4 — QUALITY CONTROL / VERIFICATION PASS

### 4.1 Back-Translation Spot Check

- [ ] For a sample of ~10 dense technical paragraphs (especially Methodology and Results), mentally back-translate the Farsi into English and compare against the original — if meaning has drifted, flag it. This catches silent semantic errors that read fluently in Farsi but no longer say the same thing as the source.

### 4.2 Native-Fluency Read-Through

- [ ] Read the Farsi thesis **without reference to the English original** — does it read as though it was originally written in Farsi by a Software Engineering graduate student, or does it still "feel" translated (unnatural word order, calques, inconsistent terminology)?
- [ ] This read-through should be done by (or reviewed by) a native Farsi-speaking academic in the field where possible — an AI-only translation pass, however careful, should not be treated as final without this human check, given the stakes of a formal academic submission.

### 4.3 Terminology Consistency Audit

- [ ] Search the completed Farsi document for every glossary term (Part 1.2) and confirm it was used identically everywhere — this is mechanically checkable and should not be skipped.

### 4.4 Cross-Reference Integrity After Renumbering

- [ ] Since figure/table/equation numbering will likely change format during conversion (Part 2.9), verify every in-text reference ("as shown in Figure 3-2") still points to the correct renumbered figure — renumbering is a common source of silent broken cross-references.

### 4.5 Formatting Re-Verification

- [ ] After translation, re-run the full formatting checklist from the companion Rulebook (margins, fonts, RTL/LTR settings, page numbering) — translation into Farsi (RTL) from English (LTR) source Markdown very often corrupts paragraph direction, indentation, and list formatting in Word; do not assume the conversion preserved these correctly.

### 4.6 Plagiarism/Similarity Re-Check

- [ ] Run the Farsi thesis through whatever plagiarism-detection tool the university mandates (e.g., Samim Noor/Irandoc) — a translated document should still be checked, since translation doesn't guarantee originality-detection systems will treat it identically to the source, and duplicate submission policies may apply if the English version was also submitted/published elsewhere.

---

## PART 5 — WHAT TO EXPLICITLY FLAG TO THE HUMAN REVIEWER

An agent performing this translation should surface these as open decisions rather than silently resolving them:

1. Any term with no clean single Farsi equivalent (ambiguous glossary decisions)
2. Any content reorganization needed to fit the mandatory 5-chapter IAU structure
3. Any figures/diagrams containing English text baked into the image
4. The final Farsi thesis title (needs explicit supervisor approval)
5. Digit convention (Persian vs. Western) if not already specified
6. First-person vs. impersonal register choice if not already specified
7. Any paragraph where back-translation (Part 4.1) revealed a meaning drift
8. Any citation style mismatch between the English source and Farsi target requirement

---

## Summary — Top 5 Priorities If Time-Constrained

If only partial review time is available, prioritize in this order:

1. **Terminology consistency** (Part 1.2, 4.3) — inconsistent term translation is the most visible and most damaging error to examiners.
2. **Native-fluency read-through without the English source** (Part 4.2) — catches "translationese" that a grammar check will miss entirely.
3. **Citation/reference integrity** (Part 2.8) — author names, reference splitting, and citation style must survive translation unchanged.
4. **Structural conformance to the 5-chapter IAU format** (Part 3.2) — a fluent translation of a wrongly-structured thesis still fails formatting review.
5. **Markdown artifact removal** (Part 3.1) — the fastest thing an examiner notices, and the easiest to fix if caught early.
