# Translation Plan: English Academic Thesis → Farsi Academic Thesis (IAU Ardabil Standard)

> **Generated:** 2026-07-04
> **Source:** `ACADEMIC_v3_En.md` (1,375 lines, ~35K words)
> **Guide Documents:** `Cloude_Translation_Guide.md`, `Dictionary.md`, `AI-gen-flows.md`, `Rules-final.md`
> **Converter:** `Cloude_Converter.py` + Template DOCX

---

## 1. Source Document Overview

| Property | Value |
|----------|-------|
| **Source file** | `ACADEMIC_v3_En.md` |
| **Total lines** | 1,375 |
| **Estimated word count** | ~30,000–35,000 English words |
| **Chapters** | 5 (Introduction, Literature Review, Methodology, Results, Discussion) |
| **References** | ~55 entries |
| **Tables** | ~20 |
| **Figures** | ~6 |
| **Equations** | ~15 |

---

## 2. Translation Principles (from Cloude_Translation_Guide.md)

### 2.1 Non-Negotiable Rules
1. **SOV word order** — Verb always sentence-final in formal Persian. No English SVO calques.
2. **Ezafe constructions** — Break English noun stacks into properly connected Persian noun phrases using کسره اضافه.
3. **Impersonal register** — Default to passive/impersonal (سیستم ... پیاده‌سازی شد) unless supervisor explicitly approves first-person.
4. **Acronyms stay in Latin script** — CNN, MARL, OCEAN, etc. remain in Latin. Full Farsi term + English acronym in parentheses on first use **per chapter**.
5. **Author names stay in Latin script** — Only the surrounding sentence is translated.
6. **Equations, code, variable names, function names** — Never translated. Surrounding prose translated naturally.
7. **Solar Hijri dates** for Iranian context; **Gregorian dates** for international citations.
8. **Digits**: Persian digits (۰-۹) in body text; Western digits in equations, code, and tables.

### 2.2 Critical to Avoid
- **Translationese** — No literal calques of English syntax. Rebuild each paragraph in natural Farsi.
- **Forbidden AI vocabulary** — Never use Farsi equivalents of: *delve*, *moreover*, *furthermore*, *crucial*, *vital*, *robust* (as filler).
- **English punctuation in Persian text** — Use Persian punctuation (، ؟ ؛ « »).
- **Bolding key terms mid-sentence** — Bold only for headings and captions.

### 2.3 High-Risk Error Patterns

| # | Error Type | Fix |
|---|-----------|-----|
| 1 | Literal/calque translation | Ask: "would a Farsi-speaking CS professor write it this way?" |
| 2 | SVO word order (verb mid-sentence) | Move verb to end of clause |
| 3 | Active voice where impersonal expected | Default to passive (شد/می‌شود) |
| 4 | Tense over-translation | Simplify to tenses a Farsi writer would naturally use |
| 5 | English noun-stacking | Break into ezafe constructions |

---

## 3. Dictionary Usage (from Dictionary.md)

### 3.1 Term Classification

| Section | Type | Handling |
|---------|------|----------|
| Section 1 (~113 terms) | Confirmed Persian equivalents | Use Farsi directly |
| Section 2 (~28 terms) | Partial/contested equivalents | Farsi + English in parentheses on **first use per chapter** |
| Section 3 (~21 terms) | Transliterated terms | Farsi transliteration + English on first use |
| Section 4 (~135 terms) | Compound phrases | Translate as single unit; never decompose |
| Section 5 (5 terms) | Scenario names | Retain English name; translate only descriptive label |
| Section 6 (~40 acronyms) | Acronyms | Stay in Latin script; full Farsi on first use per chapter |
| Section 7 | Prohibited translations | Never use the listed wrong forms |

### 3.2 Workflow
1. **Before each chapter**: Scan Dictionary for all terms that appear.
2. **During translation**: For Section 2-3 terms, append English parenthetical on first occurrence per chapter.
3. **After each chapter**: Search Farsi text for every glossary term, confirm identical usage.
4. **Prohibited**: Never use مصرف‌تولیدکننده (use پروسومر), never use عدم ایستایی (use ناایستایی).

---

## 4. Structural Conversion

### 4.1 IAU 5-Chapter Structure

| Chapter | English Title | Farsi Title |
|---------|--------------|-------------|
| 1 | Introduction and Generalities | کلیات تحقیق |
| 2 | Literature Review | ادبیات و پیشینه تحقیق |
| 3 | Research Methodology | روش‌شناسی تحقیق |
| 4 | Data Analysis | تجزیه و تحلیل داده‌ها |
| 5 | Discussion and Conclusion | نتیجه‌گیری و پیشنهادات |

### 4.2 Numbering Convention (Ardabil: Hyphen-Based)

- Chapters: `1`, `2`, `3`, `4`, `5`
- Sections: `1-1`, `2-3`, `4-2`
- Sub-sections: `2-1-1`, `3-5-2`
- Equations: `(۳-۵)`, `(۴-۲)`
- Tables: `جدول ۳-۱`, `جدول ۴-۷`
- Figures: `شکل ۳-۱`, `شکل ۴-۳`

The English source already uses hyphen format — preserve as-is.

### 4.3 Markdown Artifacts to Strip
- Raw `#`, `##`, `**bold**`, `-`, `` ``` `` must become Word styles.
- Bullet-list arguments → convert to prose paragraphs.
- Bold mid-sentence key terms → remove.

---

## 5. Translation Pass Structure

Each chapter undergoes **3 passes**:

### Pass 1 — Rough Translation
- Read entire chapter first. Identify each paragraph's core claim.
- Rebuild in natural Farsi paragraph structure.
- Consult Dictionary for every technical term.
- Apply SOV word order, ezafe, impersonal register.

**Checklist:**
- [ ] Verb at end of clause?
- [ ] No English calques?
- [ ] Noun stacks broken into ezafe phrases?
- [ ] Dictionary terms used correctly?

### Pass 2 — Polish & Register
- Refine for formal academic Persian (فارسی نوشتاری رسمی).
- Sentence length: 15-25 words avg, max 35.
- Paragraph: one idea, ~100-200 words.
- Apply Persian punctuation (، ؟ ؛ « »).
- Remove any AI-vocabulary tells.

**Checklist:**
- [ ] Sentences 15-25 words avg, none over 35?
- [ ] No forbidden AI vocabulary?
- [ ] Persian punctuation used (not English)?

### Pass 3 — Terminology Audit & Cross-Reference
- Search Farsi text for every glossary term; confirm identical usage across all chapters so far.
- Verify equation/figure/table cross-references.
- Verify acronyms expanded on first use per chapter.
- Back-translation spot-check for 10 dense paragraphs.
- Read Farsi chapter without English original — does it read like native Farsi?

**Checklist:**
- [ ] Glossary term consistency audit passed?
- [ ] Cross-references intact?
- [ ] Acronyms expanded per chapter?
- [ ] Reads like native Farsi academic prose?

---

## 6. Phased Execution

### Phase 1 — Front Matter + Chapter 1 (~3,000 words Farsi)

**File:** `ACADEMIC_v3_Fa.md` (YAML + Ch.1)

**Sections to translate:**
- [ ] YAML front matter (title, author, supervisor, abstracts, keywords)
- [ ] Farsi abstract (چکیده: ~300 words, single paragraph, no citations)
- [ ] List of abbreviations (فهرست علائم و اختصارات)
- [ ] Section 1-1 (Statement of the Problem)
- [ ] Section 1-2 (Significance of the Study)
- [ ] Section 1-3 (Research Innovation)
- [ ] Section 1-4 (Research Objectives)
- [ ] Section 1-5 (Research Questions)
- [ ] Section 1-6 (Research Hypotheses)
- [ ] Section 1-7 (Operational Definitions)
- [ ] Section 1-8 (Thesis Outline)

**After completion:**
- [ ] Terminology consistency audit for Ch.1
- [ ] Pass 2 polish
- [ ] Pass 3 verification

---

### Phase 2 — Chapter 2 (~7,500 words Farsi)

**Sections to translate:**
- [ ] Section 2-1-1 (Prosumer Paradigm)
- [ ] Section 2-1-2 (P2P Market Structures)
- [ ] Section 2-1-3 (MARL for Distributed Control)
- [ ] Section 2-1-4 (Personality-Driven Decision Making)
- [ ] Section 2-2-1 (Efficiency-Focused MARL)
- [ ] Section 2-2-2 (Fairness-Aware MARL)
- [ ] Section 2-2-3 (Game-Theoretic Approaches)
- [ ] Section 2-2-4 (Alter-Exploration Problem)
- [ ] Section 2-3 (Qualitative Comparison Table)
- [ ] Section 2-4 (Conceptual Framework)

**Table handling:** Table 2-1 — translate Farsi row/column labels only.

**After completion:**
- [ ] Terminology audit for Ch.2 + Ch.1
- [ ] Pass 2 polish
- [ ] Pass 3 verification

---

### Phase 3 — Chapter 3 (~4,500 words Farsi)

**Sections to translate:**
- [ ] Section 3-1 through 3-13 (entire Methodology)

**Table handling:** Tables 3-1 to 3-11 — translate headers/labels only.
**Equation handling:** Keep all LaTeX as-is. Translate surrounding prose.
**Code/algorithm:** Keep as LTR code blocks (not translated).

**After completion:**
- [ ] Terminology audit for all chapters so far
- [ ] Pass 2 polish
- [ ] Pass 3 verification

---

### Phase 4 — Chapter 4 (~6,000 words Farsi)

**Sections to translate:**
- [ ] Section 4-1 through 4-11 (entire Results)

**Table handling:** Tables 4-1 to 4-9 — translate headers/labels; keep numeric values.

**After completion:**
- [ ] Terminology audit for all chapters
- [ ] Pass 2 polish
- [ ] Pass 3 verification

---

### Phase 5 — Chapter 5 + References + English Abstract (~3,000 words Farsi)

**Sections to translate:**
- [ ] Sections 5-2 to 5-7 (Discussion and Conclusion)
- [ ] Section 5-5-1 (Threats to Validity)

**Reference list:**
- [ ] Split into: (1) Farsi/Persian sources, (2) Non-Farsi sources
- [ ] Author names stay Latin; journal names, DOIs, publishers not translated
- [ ] Each list alphabetized by author's last name

**English abstract:**
- [ ] Faithful translation of Farsi abstract (same content)
- [ ] One paragraph, ~300 words, keywords at bottom

**English title page:**
- [ ] Full English mirror of Farsi title page (for end of document)

**After completion:**
- [ ] Full-document terminology consistency audit
- [ ] Pass 2 polish
- [ ] Pass 3 verification

---

### Phase 6 — DOCX Generation

**Tasks:**
- [ ] Finalize YAML front matter with all metadata
- [ ] Verify headings use correct format (1-, 1-1, 2-1-1)
- [ ] Verify Table/Figure captions use `Table:` / `![caption](path)` format
- [ ] Run converter:

```bash
pip install python-docx pyyaml --break-system-packages

python3 Cloude_Converter.py ACADEMIC_v3_Fa.md ACADEMIC_v3_Fa.docx \
    --branch ardabil \
    --template "فرمت پایان نامه - تحصیلات TEMPLATE.docx"
```

- [ ] Open in Word, Ctrl+A → F9 to refresh TOC/LoF/LoT
- [ ] Verify: margins (top 3, bottom 3, right 3, left 2 cm), fonts (Lotus), RTL/LTR, page numbering
- [ ] Print one sample page for supervisor confirmation

---

## 7. Progress Tracking Table

```
Phase   | Chapter     | Pass 1 | Pass 2 | Pass 3 | Glossary Audit | Status
--------|-------------|--------|--------|--------|----------------|---------
Phase 1 | YAML + Meta |   —    |   —    |   —    |       —        | PENDING
Phase 1 | 1-1 to 1-8  |   —    |   —    |   —    |       —        | PENDING
Phase 2 | 2-1 to 2-4  |   —    |   —    |   —    |       —        | PENDING
Phase 3 | 3-1 to 3-13 |   —    |   —    |   —    |       —        | PENDING
Phase 4 | 4-1 to 4-11 |   —    |   —    |   —    |       —        | PENDING
Phase 5 | 5-2 to 5-7  |   —    |   —    |   —    |       —        | PENDING
Phase 5 | References  |   —    |   —    |   —    |       —        | PENDING
Phase 6 | DOCX Gen    |   —    |   —    |   —    |       —        | PENDING
```

After each section: replace `—` with `✅` or `❌`.

---

## 8. Open Decisions (Require Supervisor Input)

| # | Decision | Default | [VERIFY] |
|---|----------|---------|----------|
| 1 | Digit convention (Persian vs Western digits in body) | Persian digits (۰-۹) for body; Western for equations/tables | YES — CS/SE may prefer Western |
| 2 | Register (impersonal passive vs first-person plural) | Impersonal passive | YES |
| 3 | Farsi thesis title | From OCEAN-to-RL mapping | Needs supervisor sign-off |
| 4 | Figures with English text (axis labels) | Must be regenerated in Farsi | Flag as open item |
| 5 | Citation style (Author-Date vs IEEE) | Author-Date (Ardabil standard) | YES |
| 6 | Abstract sequencing | Finalize Farsi first, then translate to English | YES |
| 7 | Term handling (English parenthetical) | Farsi + English on first use per chapter | YES |
| 8 | Reference list order | Persian sources first, non-Persian second | YES |
| 9 | Page numbering format (front matter) | Persian abjad (الف، ب، ج...) | YES |
| 10 | Line spacing | Exactly 28 pt | YES |
| 11 | Font: Lotus vs Nazanin vs Zar | Lotus (Ardabil profile) | YES |

---

## 9. Quick Reference: Key Farsi Translations

| English | Farsi Equivalent | Section |
|---------|-----------------|---------|
| Reinforcement Learning (RL) | یادگیری تقویتی | §1 |
| Multi-Agent RL (MARL) | یادگیری تقویتی چندعاملی | §1 |
| Independent Q-Learning (IQL) | یادگیری Q مستقل | §1 |
| Markov Decision Process (MDP) | فرآیند تصمیم‌گیری مارکوف | §1 |
| Prosumer | پروسومر (Prosumer) | §3 |
| Peer-to-Peer (P2P) | نظیربه‌نظیر | §1 |
| Smart Neighbourhood | محله هوشمند | §1 |
| Microgrid | ریزشبکه | §1 |
| Jain's Fairness Index | شاخص انصاف جین | §1 |
| Gini Coefficient | ضریب جینی | §1 |
| Agreeableness | توافق‌پذیری | §1 |
| Openness to Experience | گشودگی به تجربه | §1 |
| Extraversion | برون‌گرایی | §1 |
| Conscientiousness | وظیفه‌شناسی | §1 |
| Neuroticism | روان‌رنجوری | §1 |
| Reward Shaping | شکل‌دهی پاداش (Reward Shaping) | §2 |
| Non-stationarity | ناایستایی (Non-stationarity) | §2 |
| Innovator Effect | اثر نوآور | §5 |
| Emergent Reciprocity | جبران پیدایشی (Emergent Reciprocity) | §2 |
| Prosocial Advantage | مزیت نوعدوستانه (Prosocial Advantage) | §2 |
| Alter-Exploration Problem | مسئله اکتشاف متغیر (Alter-Exploration Problem) | §2 |
| State-of-the-Art | وضع موجود فناوری | §1 |
| Demand Response (DR) | پاسخ‌گویی بار | §1 |
| Smart Grid | شبکه هوشمند | §1 |
| Battery Energy Storage System (BESS) | سامانه ذخیره‌ساز انرژی باتری | §1 |
| Centralised Training Decentralised Execution (CTDE) | آموزش متمرکز با اجرای غیرمتمرکز (CTDE) | §2 |
| Tragedy of the Commons | تراژدی منابع مشترک | §1 |
| Nash Equilibrium | تعادل نش | §1 |
| OCEAN-to-RL Mapping | نگاشت OCEAN به یادگیری تقویتی | §4 |
| Personality-Modulated Reward Weights | وزن‌های پاداش تعدیل‌شده توسط شخصیت | §4 |
| Fairness-Aware MARL | یادگیری تقویتی چندعاملی آگاه به عدالت | §4 |
| Exploration Floor | کف اکتشاف | §4 |
| Prosocial Orientation | گرایش نوعدوستانه | §4 |
| Blackout Day Rate | نرخ روزهای قطعی | §1 |
| Energy Waste | اتلاف انرژی | §1 |
| Mean Community Comfort | میانگین راحتی جامعه | §1 |
| Sharing Frequency | فراوانی اشتراک‌گذاری | §1 |

---

## 10. File Organization

```
HamidOutput/
├── ACADEMIC_v3_En.md              ← Source (English)
├── ACADEMIC_v3_Fa.md              ← Target (Farsi) — to be created
├── Translate_Plan.md              ← This file
├── Writing-Rules/
│   ├── Cloude_Translation_Guide.md
│   ├── Dictionary.md
│   ├── AI-gen-flows.md
│   └── Rules-final.md
└── DocX Converter/
    ├── Cloude_Converter.py
    └── فرمت پایان نامه - تحصیلات TEMPLATE.docx
```

---

## 11. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Terminology drift across chapters | Medium | High | Glossary audit after each chapter |
| Translationese / calque errors | High | Medium | 3-pass structure + native-fluency read-through |
| Cross-reference breaks from renumbering | Low | High | Verify all refs after each chapter |
| Forbidden AI vocabulary in Farsi | Medium | Medium | Pass 2 explicitly checks for this |
| Converter script issues (fonts, RTL) | Medium | High | Test on a small sample first |
| Missing YAML front matter fields | Low | Medium | Final checklist before Phase 6 |

---

*End of Translate_Plan.md*
