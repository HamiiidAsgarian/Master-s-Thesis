# Islamic Azad University, Ardabil Branch — M.Sc. Computer Science / Software Engineering

# Single Source of Truth: Complete Thesis Formatting & Submission Rules

> **⚠️ AUTHORITATIVE NOTICE**
> This document is the single source of truth, reconciling `Cloude_Final_Rules.md`, `Rules.md`, `Rules2.md`, and a third-party gap analysis. All known contradictions are resolved with `[VERIFY]` flags where department confirmation is needed. Confirm every flagged item with your supervisor and the Ardabil Thesis Affairs Office (امور پایان نامه) before final printing.

---

## 1. DOCUMENT STRUCTURE — Full Page Order

Your thesis **must** follow this sequence precisely. Preliminary pages use Persian alphabet labels (الف، ب، ج...).

| #   | Section                                          | Label    | Notes                                                                 |
| --- | ------------------------------------------------ | -------- | --------------------------------------------------------------------- |
| –   | Hardcover front cover (جلد)                      | —        | Dark blue, silver/gold embossing **[VERIFY]**                          |
| –   | Blank buffer page (آستر بدرقه)                   | —        | No visible number                                                     |
| 1   | Bismillah page (بسم الله الرحمن الرحیم)          | الف      | Centered, counted but no printed number                               |
| 2   | **Thesis Defense Approval Page (صفحه تأییدیه)**  | —        | **Critical** — signed by supervisor, advisor, examiners, dept head    |
| 3   | Declaration of originality (تعهدنامه اصالت اثر)  | —        | Increasingly mandatory university-wide **[VERIFY]**                   |
| 4   | Persian title page (copy of cover)               | ب        | Exact duplicate of cover text                                         |
| 5   | English title page                               | ج        | Full English translation of cover                                     |
| 6   | Acknowledgements (سپاسگزاری) — optional           | د        | Max 1 page                                                            |
| 7   | Dedication (تقدیم به) — optional                 | ﻫ        | Max 1 page                                                            |
| 8   | Table of Contents (فهرست مطالب)                  | —        | **Auto-generated** from Word Heading styles — never manual            |
| 9   | List of Tables (فهرست جداول)                     | —        | Auto-generated from caption tool, dot leaders to page numbers         |
| 10  | List of Figures (فهرست اشکال/نمودارها)           | —        | Auto-generated from caption tool, dot leaders to page numbers         |
| 11  | List of Abbreviations/Symbols (فهرست علائم)      | —        | Required if >5 abbreviations used (recommended for CS/SE)             |
| 12  | Persian Abstract (چکیده فارسی)                   | —        | 250–300 words (max 1–2 pages), one paragraph, no citations, 3–5 keywords |
| 13  | **Chapter 1 – Introduction**                     | ۱، ۲...  | Arabic numeral pagination starts here                                 |
| 14  | **Chapter 2 – Literature Review / Related Work** |          |                                                                       |
| 15  | **Chapter 3 – Methodology / Proposed Method**    |          | For SE: system design, architecture, algorithms                       |
| 16  | **Chapter 4 – Implementation & Results**         |          | For SE: implementation, testing, evaluation metrics                   |
| 17  | **Chapter 5 – Discussion & Conclusion**          |          |                                                                       |
| 18  | Responsibility Disclaimer (صفحه مسئولیت)         | —        | "مسئولیت محتوای این پایان‌نامه بر عهده نویسنده است" **[VERIFY]**      |
| 19  | Appendices (پیوست‌ها)**                          | —        | Named with Persian letters (پیوست الف، ب...). Source code, UML, raw data |
| 20  | References (فهرست منابع)                         | —        | Persian sources first, then non-Persian, each alphabetized separately |
| 21  | Index (فهرست نام‌ها) — optional                  | —        | Optional                                                              |
| 22  | English Abstract (چکیده انگلیسی)                 | —        | Faithful translation of Persian abstract, one paragraph, with keywords |
| 23  | English Title Page                               | —        | Full English translation of cover                                     |
| –   | Back cover (جلد پشتی)                            | —        | English title in matching embossing                                   |

> **Note on order of items 18–20:** Sources disagree on whether Appendices or References come first. **[VERIFY] which order your department requires.**

---

## 2. SOFTWARE ENGINEERING–SPECIFIC CONTENT ADDITIONS

Unlike a generic CS thesis, an SE thesis typically requires these embedded elements (check with supervisor which are mandatory for your specific track):

- **Requirements specification** (functional & non-functional) — usually in Chapter 3
- **System architecture diagrams** (UML: use-case, class, sequence, activity, deployment diagrams) — numbered/captioned like any figure
- **Design rationale / design patterns used**, if applicable
- **Evaluation methodology**: metrics used (accuracy, precision/recall, performance benchmarks, complexity analysis, usability testing, etc.) — must be explicit and reproducible
- **Testing chapter or section**: unit/integration/system testing approach and results, if the thesis involves a built system
- **Threats to validity** subsection (common in SE research; sometimes required in Chapter 5 alongside Limitations)

---

## 3. PHYSICAL COVER & BINDING (جلد)

### 3.1 Cover Specifications

| Element                     | Specification                                                      |
| --------------------------- | ------------------------------------------------------------------ |
| **Cover Color (Master's)**  | **Dark blue (آبی تیره / سرمه‌ای)** — not black, not light blue     |
| **Stamping/Embossing**      | **Silver (نقره‌کوب) or gold (زرکوب)** — **[VERIFY] which**         |
| **Binding Type**            | **Hardcover (گالینگور)**                                           |
| **University Logo**         | **[VERIFY]** Top-center (common IAU) or top-left 4×3 cm (claimed)  |
| **Spine (عطف)**             | Thesis title + author name embossed. **[VERIFY] text direction**   |
| **Printing Sides**          | **[VERIFY]** One-sided (traditional) or double-sided (claimed)     |

### 3.2 Cover Text Arrangement

The cover typically follows this top-to-bottom layout:

1. **University name** (top-center): دانشگاه آزاد اسلامی
2. **Branch name**: واحد اردبیل
3. **Faculty name**: دانشکده فنی و مهندسی / گروه کامپیوتر
4. **Label**: پایان‌نامه کارشناسی ارشد (M.Sc. Thesis)
5. **Thesis title** (largest text, centered)
6. **Supervisor**: استاد راهنما: — Name
7. **Advisor**: استاد مشاور: — Name (if any)
8. **Student name**: نام و نام خانوادگی
9. **Academic year**: سال تحصیلی ۱۴۰۴-۱۴۰۵ **[VERIFY] format**
10. **Thesis Registration Number** from Pazhooheshyar system

> **[VERIFY] exact cover layout** by examining a recent approved SE/CS thesis from Ardabil.

---

## 4. PAGE SETUP & MARGINS (Word Layout)

| Setting             | **Ardabil Branch** | General IAU (Standard) |
| ------------------- | ------------------ | ---------------------- |
| **Paper Size**      | A4 (21 × 29.7 cm)  | A4 (21 × 29.7 cm)      |
| **Top Margin**      | **3 cm**           | 2.5 cm                 |
| **Bottom Margin**   | **3 cm**           | 2.5 cm                 |
| **Right Margin**    | **3 cm**           | 2.5 cm                 |
| **Left Margin**     | **2 cm**           | 3.5 cm (for binding)   |
| **Headers/Footers** | 1.5 cm from edge   | 1.5 cm from edge       |
| **Line Length**     | 16 cm              | _(implicit)_           |

> **[VERIFY] margins** — Ardabil-specific values differ from General IAU. Print one sample page and confirm with supervisor.

**Key Rules:**
- Margins **absolutely consistent** throughout (including appendices)
- No decorative borders, frames, or running heads
- Line length of 16 cm = 21 cm width − 3 cm right − 2 cm left

---

## 5. FONTS & TYPOGRAPHY (فونت‌ها)

### 5.1 Farsi (Persian) Text — Ardabil Branch

| Element                       | Font                              | Size   | Style           |
| ----------------------------- | --------------------------------- | ------ | --------------- |
| **Main Body Text**            | **Lotus Thin (لوتوس نازک)**       | **14** | Normal          |
| **Chapter Titles**            | **Lotus Bold (لوتوس پررنگ)**      | **25** | Bold (New Page) |
| **Section Headings (1st)**    | **Lotus Bold**                    | **14** | Bold            |
| **Sub-headings (2nd)**        | **Lotus Bold**                    | **12** | Bold            |
| **Sub-sub-headings (3rd)**    | **Lotus Bold**                    | **12** | Bold/Italic     |
| **Figure/Table Captions**     | **Lotus Bold**                    | **11** | Bold            |
| **Footnotes**                 | **Lotus**                         | **12** | Normal          |

> **[VERIFY] font family** — Lotus vs. Nazanin vs. Zar vs. Titr is the single most-cited inconsistency across IAU branch documents. Lotus 25 for chapter titles seems unusually large — some sources say 16 is safer. **Ask your department for the official `.dotx` Word template if one exists.**

### 5.2 Farsi (Persian) Text — General IAU Standard (if not Ardabil)

| Element                          | Font                 | Size  | Style  |
| -------------------------------- | -------------------- | :---- | :----- |
| University/Branch names          | Zarr (زر)            | 18    | Bold   |
| Thesis Title                     | Titr (تيتر)          | 18    | Bold   |
| "Title/Supervisor/Author" labels | Nazanin (نازنين)     | 18    | Bold   |
| Body Text                        | B Nazanin or B Mitra | 14    | Normal |
| Section Headings                 | Nazanin or B Mitra   | 14–16 | Bold   |

### 5.3 English Text (All Branches)

| Element                       | Font                    | Size   | Style  |
| ----------------------------- | ----------------------- | ------ | ------ |
| **Body Text (English)**       | **Times New Roman**     | **12** | Normal |
| **Chapter Titles (English)**  | **Times New Roman**     | **25** | Bold   |
| **English Headings**          | **Times New Roman**     | **14** | Bold   |
| **Code/Programming listings** | Courier New or Consolas | 10–11  | Normal |
| **English Captions**          | Times New Roman         | 10–11  | Bold   |

### 5.4 Non-Negotiable Rules

- Never mix Persian font families within the same text level
- Any English word inside a Persian sentence → switch to Times New Roman inline
- **No underlining anywhere** — use bold or italic instead
- Bold + Italic combined only for the deepest sub-heading level, if at all
- Code/algorithms → monospace, left-aligned, LTR, even inside an RTL document
- Consistency across the entire document is mandatory

---

## 6. LINE SPACING & PARAGRAPH FORMATTING (فاصله خطوط و پاراگراف)

| Element                  | Specification (Ardabil)         | Word Setting                                                                  |
| ------------------------ | -------------------------------- | ----------------------------------------------------------------------------- |
| **Line Spacing (Body)**  | **1–1.5 cm between lines**       | **[VERIFY]** Exactly 28 pt or Multiple 1.5                                    |
| **Line Spacing (Abstract)** | Tighter single spacing         |                                                                               |
| **Paragraph Indent**     | **~1 cm** (first line only)     | Special → First line → 1 cm                                                   |
| **Paragraph Spacing**    | One blank line between paragraphs | Set Before: 0 pt, After: 0 pt press Enter once between paragraphs           |
| **Alignment (Body)**     | **Justified (تراز شده)**         | Ctrl + J                                                                      |
| **Lines per Page**       | 22–27 lines                     | Sanity-check after font/spacing finalised                                     |
| **Widow/Orphan Control** | ON                               | Format → Paragraph → Line & Page Breaks → Widow/Orphan control = ON           |

**Key Rules:**
- Do NOT indent the first paragraph after a heading
- Every body paragraph must be fully justified
- Paragraphs: 5–10 sentences (~100–200 words), one main idea
- Heading must have at least 2 lines of text below it before a page break

---

## 7. TEXT DIRECTION & ALIGNMENT (جهت و تراز)

| Language         | Direction           | Alignment |
| ---------------- | ------------------- | --------- |
| **Persian Text** | Right-to-Left (RTL) | Justified |
| **English Text** | Left-to-Right (LTR) | Justified |
| **Mixed Text**   | Unicode BiDi        | Justified |

- Set Word's default paragraph direction to **RTL** for the main Persian thesis
- Switch to **LTR** for English abstracts, code blocks, or large English excerpts
- Never use Left-Align or Right-Align for body text — only **Justify**

---

## 8. NUMBERING SYSTEM (شماره‌گذاری سطوح)

> **Ardabil Branch uses a HYPHEN-based system (not decimal dots).**

| Level               | Format                    | Example   | Meaning                            |
| ------------------- | ------------------------- | --------- | ---------------------------------- |
| **Chapter**         | Single number             | `2`       | Chapter 2                          |
| **Section**         | `Chapter-Section`         | `2-4`     | Chapter 2, Section 4               |
| **Sub-section**     | `Chapter-Section-Sub`     | `2-4-3`   | Chapter 2, Sec 4, Sub-sec 3        |
| **Sub-sub-section** | `Chapter-Section-Sub-Sub` | `2-4-3-1` | Chapter 2, Sec 4, Sub 3, Sub-sub 1 |
| **Equations**       | `Chapter-Number`          | `6-8`     | 8th equation in Chapter 6          |

- Maximum depth: 3–4 levels. Beyond that, use `(الف)`, `(ب)` instead
- Implement via Word's **Multilevel List** linked to Heading 1/2/3 — never type manually
- In Persian: chapter number on the **right**, section on the **left** visually (e.g., `4-2`)

---

## 9. PAGE NUMBERING (شماره صفحات)

| Section                              | Numbering Format                | Position      | Notes                     |
| ------------------------------------ | ------------------------------- | ------------- | ------------------------- |
| **Preliminary Pages** (→ Abstract)   | Persian alphabet (الف، ب، پ...) | Bottom-center | 1.5 cm from edge          |
| **Main Body** (Ch.1 → End)           | Arabic numerals (۱، ۲، ۳...)    | Bottom-center | Restarts at "۱" Chapter 1 |
| **Cover / Title Pages**              | **No visible number**           | —             |                           |
| **Blank Pages**                      | **No visible number**           | —             | Counted but not displayed |

- Use **Section Breaks (Next Page)** in Word to separate Prelim from Main Body — this is the #1 technical mistake
- Never type page numbers manually — use Word's Page Number field

---

## 10. HEADINGS & SUBHEADINGS (عنوان‌ها)

| Level                     | Formatting Style                       | Alignment    | Example                       |
| ------------------------- | -------------------------------------- | ------------ | ----------------------------- |
| **Chapter**               | Bold, 25 Lotus / 25 TNR                | Centered     | **فصل دوم: ادبیات تحقیق**     |
| **Section (1st)**         | Bold, 14 pt                            | Left-aligned | **۲-۱- مبانی نظری**           |
| **Sub-section (2nd)**     | Bold, 12–13 pt                         | Left-aligned | **۲-۱-۱- تعریف متغیرها**      |
| **Sub-sub-section (3rd)** | Bold/Italic, 12 pt                     | Left-aligned | **_۲-۱-۱-۱- شاخص‌های کلیدی_** |

- No orphan headings — a heading must have ≥2 lines of body text after it on the same page
- Do not use more than 3 heading levels

---

## 11. BOLD, ITALIC, UNDERLINE (پررنگ، کج، زیرخط)

| Element           | Usage Rule                                                          |
| ----------------- | ------------------------------------------------------------------- |
| **Bold**          | Chapter titles, headings, key terms on first mention only           |
| _Italic_          | Book/journal titles in references, foreign words, equation variables |
| Underline         | **AVOID COMPLETELY** — use bold or italic instead                   |
| **Bold + Italic** | Only for sub-sub-headings (level 3), nowhere else                   |

---

## 12. PUNCTUATION — Persian Text (نشانه‌گذاری)

| Symbol  | Name             | Usage                                           |
| ------- | ---------------- | ----------------------------------------------- |
| **،**   | Comma (ویرگول)   | Separates items, clauses                        |
| **.**   | Full stop (نقطه) | Ends sentences (Persian dot, not English period) |
| **؟**   | Question mark    | Ends questions                                  |
| **!**   | Exclamation      | Rare; avoid unless quoting                      |
| **؛**   | Semicolon        | Separates related independent clauses            |
| **:**   | Colon            | Introduces lists, explanations, block quotes    |
| **« »** | Guillemets (گیومه) | Direct quotes and titles                       |
| **( )** | Parentheses      | Additional info, citations, acronyms            |

**Critical:**
- Place a **space after** punctuation marks (, . ؟ :), not before
- Do not use English punctuation (`.`, `,`, `?`) inside Persian text — RTL rendering issues

---

## 13. SENTENCE STRUCTURE & LENGTH (جملات)

| Element            | Recommendation                                                 |
| ------------------ | -------------------------------------------------------------- |
| **Average length** | 15–25 words per sentence                                       |
| **Maximum length** | 30–35 words (hard ceiling ~35)                                 |
| **Voice**          | Prefer active voice; passive acceptable in scientific writing  |
| **First Person**   | Acceptable ("I propose", "We observe") — check with supervisor |
| **Tone**           | Formal, academic, objective. No colloquialisms, no slang       |
| **Terminology**    | Use precise CS/SE terminology (MARL, RL, UML, etc.)            |

---

## 14. BULLET POINTS & NUMBERED LISTS

| List Type                | Usage                                | Symbol                     |
| ------------------------ | ------------------------------------ | -------------------------- |
| **Bulleted (Unordered)** | No sequence/priority                 | Use `•` or `—` consistently |
| **Numbered (Ordered)**   | Sequential steps, rankings           | Use `1.`, `2.` or `(۱)`    |

- Introduce lists with a colon (`:`)
- Complete sentences → capitalize + period; fragments → no period
- Maintain parallel structure
- Reserve lists for genuinely enumerable content — not for arguments or literature synthesis (use prose)
- Nested lists: outer `•`, inner `◦`

---

## 15. FORMULAS & EQUATIONS (فرمول‌ها)

| Element               | Specification                                                |
| --------------------- | ------------------------------------------------------------ |
| **Editor**            | Microsoft Word Equation Editor (or MathType)                 |
| **Font**              | Times New Roman or Cambria Math                              |
| **Variables**         | **Italicized** (_x_, _y_, _E_, _P_)                         |
| **Constants/Numbers** | Roman (not italic) — π, e, 1.3                               |
| **Display**           | Centered on separate line for major equations                |
| **Numbering**         | Right-aligned in parentheses, chapter-based: `(3-5)`         |
| **In-text ref**       | "همانطور که در معادله (۳-۵) نشان داده شده است..."              |

**Critical:**
- Define every symbol the first time it appears (parameter table if >5 symbols)
- Equations in Persian text must be **LTR** — ensure equation box direction is LTR
- Number **all** equations you refer back to

---

## 16. CODE & ALGORITHM FORMATTING (CS/SE-Specific)

| Element            | Specification                                                   |
| ------------------ | --------------------------------------------------------------- |
| **Code Font**      | Courier New or Consolas, 10–11 pt                               |
| **Code Alignment** | Left-aligned (LTR), even inside an RTL Persian document         |
| **Code Spacing**   | Single-spaced                                                   |
| **Line Numbers**   | Optional but recommended for long listings                      |
| **Code Caption**   | Below code block: "**کد ۳-۱:** پیاده‌سازی الگوریتم..."           |
| **Pseudocode**     | Consistent algorithmic style. Label: "الگوریتم ۳-۱"             |
| **In-text Ref**    | "همانطور که در کد ۳-۱ مشاهده می‌شود..."                           |

- Language-specific syntax highlighting is permitted but must remain readable in print
- Use Word text boxes or dedicated LTR paragraphs for multi-line code blocks

---

## 17. FIGURES, TABLES & CAPTIONS (تصاویر، جداول و عنوان‌ها)

| Element                    | Rule                                                         |
| -------------------------- | ------------------------------------------------------------ |
| **Caption Placement**      | **Table captions → ABOVE** the table. **Figure captions → BELOW** the figure. |
| **Caption Font (Farsi)**   | Lotus Bold 11 / B Nazanin 11                                 |
| **Caption Font (English)** | Times New Roman 11 Bold                                      |
| **Numbering**              | By chapter: `شکل ۳-۴` or `جدول ۲-۱`                          |
| **Figure Resolution**      | Minimum **300 DPI**                                           |
| **Table Formatting**       | No vertical lines. Horizontal lines only (top, bottom, header separator) |

**Key Rules:**
- **Reference every figure/table/equation in the text** before it appears — never insert a visual with no textual pointer
- Place figures/tables as close as possible to their first reference
- Do not split tables across pages if avoidable. Use "Keep with next" or "Repeat header rows"
- Use Word's **Insert Caption** feature for auto-generated List of Figures/Tables
- List of Figures / List of Tables: dot leaders connecting number to page number

---

## 18. CITATIONS & REFERENCES (ارجاع‌دهی و منابع)

### 18.1 In-Text Citation Style (Ardabil Standard)

> **Rule:** The **first and last name** and the **year of publication** should be mentioned.

- (مردوخی، احمد، ۱۳۷۵)
- (Rahimian, Ali, 2021)

### 18.2 Alternative Styles (If Supervisor Requires)

- **APA Style:** (Author, Year) — e.g., (رحیمیان، ۱۴۰۰) or (Rahimian, 2021)
- **IEEE Style:** Numerical brackets `[1]` — common in CS/SE. **[VERIFY] which your department mandates**

### 18.3 Reference List Order

| Order      | Type                          | Sorting                             |
| ---------- | ----------------------------- | ----------------------------------- |
| **First**  | **Farsi/Persian sources**     | Alphabetical by author's last name  |
| **Second** | **Non-Farsi (English, etc.)** | Alphabetical by author's last name  |

### 18.4 Critical Rules

- **Pick ONE citation style** and use it for 100% of the thesis — mixing APA and IEEE is a red flag
- Every claim must be cited unless common knowledge
- Direct quotes must include page numbers and be in `« »` (Persian guillemets)
- Short quotes (<40 words): inline with guillemets. Long quotes (≥40 words): indented block, single-spaced, no quotation marks
- No plagiarism — paraphrase properly and cite

---

## 19. ACRONYMS & ABBREVIATIONS (مخفف‌ها)

| Rule           | Example                                                                      |
| -------------- | ---------------------------------------------------------------------------- |
| **First use**  | Write full term + abbreviation in parentheses: "شبکه عصبی کانولوشنی (CNN)..." |
| **Thereafter** | Use abbreviation only                                                        |
| **List**       | Include "List of Abbreviations" before Chapter 1 if >5 used                  |

**Format:** Two columns — Abbreviation (left) → Full Term (right), alphabetically sorted, dot leaders.

---

## 20. FRONT MATTER FORMATTING DETAILS

| Element              | Formatting Rule                                                               |
| -------------------- | ----------------------------------------------------------------------------- |
| **Approval Page**    | "صفحه تأییدیه" centered. Signature lines: supervisor, advisor, internal examiner, external examiner, dept head. Obtain after defense. |
| **Declaration of Originality** | "تعهدنامه اصالت اثر" — increasingly required. **[VERIFY]**                     |
| **Acknowledgements** | "سپاسگزاری" (20 pt Bold). Body: justified, 14 pt. Max 1 page. Optional.       |
| **Dedication**       | "تقدیم" (20 pt Bold). Body: centered, 14 pt. Max 1 page. Optional.           |
| **Persian Abstract** | "چکیده" (20 pt Bold). Body: justified, 14 pt. Max 1–2 pages. 250–300 words, one paragraph, no citations. Keywords at bottom: "واژگان کلیدی: ..." |
| **English Abstract** | "Abstract" (20 pt TNR Bold). Body: justified, 12 pt TNR. Max 2 pages. Faithful translation of Farsi abstract. Keywords at bottom. |
| **Keywords**         | 3–5 keywords, comma-separated, immediately after abstract on same page        |

---

## 21. CHAPTER-SPECIFIC CONTENT REQUIREMENTS

| Chapter                  | Must Include                                                                                          | Must NOT Include                              |
| ------------------------ | ----------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| **1: Introduction**      | Problem statement, Significance, Objectives (main & secondary), Hypotheses/Questions, Operational Definitions, Scope & Limitations (قلمرو و محدودیت‌ها) | Detailed lit review, Data, Results            |
| **2: Literature Review** | Theoretical framework, Domestic & International studies, **critical synthesis** (contrasting methods, contradictory findings), Research gap | New research, Methodology, Results |
| **3: Methodology**       | Research design, Population, Sample, Tools (validity/reliability), Algorithm design, Statistical/ML methods, Ethics statement (if applicable) | Results, Discussion, Lit review               |
| **4: Results**           | **Objective** presentation of findings. Tables, charts, statistical outputs. **No interpretation**    | Interpretation, discussion, recommendations    |
| **5: Discussion**        | Interpretation, Comparison with Ch.2 studies, **specific limitations**, Future suggestions             | New data, New literature (refer back only)   |

- **SE-specific:** Requirements spec, system architecture (UML), design rationale, evaluation methodology, testing, threats to validity

### 21.1 Word and Page Count Guidelines

> These are approximate ranges for a typical 100–150 page thesis. Data-heavy CS/SE theses may extend to 200 pages with appendices. **Confirm expectations with your supervisor.**

| Chapter | Title | Typical Pages | Approx. Words (Farsi) |
| :------ | :---- | :------------ | :-------------------- |
| **1**   | Introduction and Generalities (کلیات تحقیق) | 10–20 | 3,000–6,000 |
| **2**   | Literature Review and Background (ادبیات و پیشینه تحقیق) | 25–40 | 7,500–12,000 |
| **3**   | Research Methodology (روش‌شناسی تحقیق) | 15–25 | 4,500–7,500 |
| **4**   | Data Analysis and Findings (تجزیه و تحلیل داده‌ها) | 20–35 | 6,000–10,500 |
| **5**   | Conclusion and Suggestions (نتیجه‌گیری و پیشنهادات) | 10–15 | 3,000–4,500 |

### 21.2 Detailed Chapter Breakdown

#### Chapter 1 — Introduction and Generalities (کلیات تحقیق)

**Must Include:**
1. **Introduction (مقدمه)**: Broad overview of the topic to engage the reader and set context
2. **Problem Statement (بیان مسئله)**: Clear, precise definition of the research problem or gap
3. **Significance and Necessity (اهمیت و ضرورت تحقیق)**: Why this research matters — scientific and practical value
4. **Research Objectives (اهداف تحقیق)**: Main goal + specific sub-objectives
5. **Research Questions (سوالات تحقیق)**: Primary and secondary questions
6. **Research Hypotheses (فرضیه‌های تحقیق)**: Testable predictions (if applicable)
7. **Research Methodology (روش تحقیق)**: Brief introduction of methods (simulation, algorithm design, data analysis)
8. **Scope and Limitations (قلمرو و محدودیت‌های تحقیق)**: Boundaries of the study (time, place, subject matter)
9. **Operational Definitions (تعریف مفاهیم و اصطلاحات)**: Specialised terms used in the thesis

**Must NOT Include:** Overly long historical background (belongs in Ch.2), data, results, or conclusions.

#### Chapter 2 — Literature Review and Background (ادبیات و پیشینه تحقیق)

**Must Include:**
1. **Theoretical Foundations (مبانی نظری)**: Comprehensive review of theories, concepts, and models
2. **Review of Related Literature (پیشینه تحقیق)**: Critical review of prior studies — both Iranian and international, organised thematically or chronologically. Highlight contradictions and the research gap
3. **Conceptual Framework (چارچوب مفهومی)**: The model or framework guiding the research (if applicable)

**Must NOT Include:** New research, methodology details, results. Do **not** present a list of summaries without critical analysis.

#### Chapter 3 — Research Methodology (روش‌شناسی تحقیق)

**Must Include:**
1. **Research Design and Approach (طرح و روش تحقیق)**: Type (applied, developmental) and approach (quantitative, qualitative, mixed)
2. **Data Collection Methods (روش‌های گردآوری داده‌ها)**: Sources — datasets, simulation logs, survey instruments
3. **Tools and Instruments (ابزارهای تحقیق)**: Software, libraries, hardware, APIs (e.g., Python, NumPy, NS-3, MATLAB)
4. **Population, Sample, and Sampling Method (جامعه، نمونه و روش نمونه‌گیری)**: Target population and sampling strategy
5. **Data Analysis Methods (روش‌های تجزیه و تحلیل داده‌ها)**: Statistical or analytical techniques (regression, algorithm comparison, performance metrics)
6. **Ethics Statement**: If human data is involved

**Must NOT Include:** Results, discussion, literature review. This chapter is a clear step-by-step recipe for replication.

#### Chapter 4 — Data Analysis and Findings (تجزیه و تحلیل داده‌ها)

**Must Include:**
1. **Descriptive Analysis (توصیف و تحلیل داده‌ها)**: General characteristics of the data (if applicable)
2. **Hypothesis Testing / Findings (آزمون فرضیه‌ها / یافته‌های تحقیق)**: Results of experiments, simulations, or analysis
3. **Data Visualisation**: Tables, charts, graphs — all numbered and captioned (§17)
4. **Objective Explanation**: What the results mean without drawing final conclusions

**Must NOT Include:** Interpretation beyond what the data shows. No recommendations or conclusions — reserve those for Chapter 5.

#### Chapter 5 — Discussion and Conclusion (نتیجه‌گیری و پیشنهادات)

**Must Include:**
1. **Summary of Findings (خلاصه یافته‌ها)**: Brief recap of the most important results
2. **Conclusion (نتیجه‌گیری)**: Answer the research questions, confirm/reject hypotheses
3. **Research Contributions (دستاوردهای تحقیق)**: Explicit statement of the thesis's contribution
4. **Research Limitations (محدودیت‌های تحقیق)**: Acknowledge study-specific constraints
5. **Suggestions for Future Research (پیشنهادات برای پژوهش‌های آتی)**: Specific directions based on findings and limitations
6. **Practical Suggestions (پیشنهادات کاربردی)**: How findings apply in industry or practice (if applicable)

**Must NOT Include:** New data, new arguments, new literature not previously discussed.

---

## 22. AI-TEXT & LANGUAGE QUALITY CHECKLIST

> Examiners increasingly screen for these specific tells. Run this checklist before final submission.

### 22.1 Sentence & Paragraph Mechanics

- [ ] Average sentence length 15–25 words; hard ceiling ~35 words
- [ ] Each paragraph covers **one idea**, ~100–200 words (5–10 sentences)
- [ ] No repeated formulaic paragraph shape (topic sentence → 3 points → summary sentence) repeated identically

### 22.2 Formatting Discipline — Markdown Leakage

- [ ] **Zero raw Markdown syntax** in final Word document — no stray `**`, `##`, `-`, `*` from AI drafts (this is the #1 giveaway)
- [ ] Bullet/numbered lists only for sequential/enumerable content — not for arguments or literature synthesis
- [ ] No AI-typical bolding of "key terms" mid-sentence — bold only for headings/captions

### 22.3 Vocabulary & Tone

- [ ] Avoid overused AI-vocabulary: _delve, moreover, furthermore, underscores, pivotal, robust, multifaceted, tapestry, landscape, in today's world, it is important to note_
- [ ] No generic hedging clichés ("further research is needed" with no specifics)
- [ ] Formal, objective register — no marketing phrasing ("showcases," "plays a crucial role," "highlights the importance")

### 22.4 Argumentative Substance

- [ ] Chapter 2 **critically compares and synthesizes** sources — not a list of summaries
- [ ] Research gap is **narrow and specific**, tied to concrete limitations of prior work
- [ ] Chapter 4 strictly descriptive — no interpretation leaking in (Chapter 5 only)
- [ ] Chapter 5 has **specific, study-tied limitations** — not generic boilerplate
- [ ] All citations correspond to **real, checkable sources** — fabricated citations are a known AI failure mode

### 22.5 Final Pre-Submission Pass

- [ ] Read the entire thesis aloud — catches uniform AI rhythm
- [ ] Run plagiarism/similarity check (Turnitin, iThenticate, or Samim Noor) — **[VERIFY] which tool Ardabil mandates**
- [ ] Verify every acronym expanded on first use
- [ ] Verify every figure/table/equation is referenced
- [ ] Verify every reference entry corresponds to an in-text citation (and vice versa)

---

## 23. WORD PROCESSING & FINAL SUBMISSION

| Requirement           | Specification                                                         |
| --------------------- | --------------------------------------------------------------------- |
| **Software**          | **Microsoft Word** (DOCX)                                             |
| **Final Formats**     | Submit **BOTH** Word (`.docx`) and **PDF**                            |
| **Submission Media**  | **2 CDs or USB drives**[VERIFY]                                       |
| **Bound Copies**      | **4 bound copies** (Ardabil) — General IAU sometimes asks for 5 [VERIFY] |
| **Article Proof**     | Proof of article publication/acceptance or supervisor confirmation     |
| **Digital Upload**    | Upload to `ganj.irandoc.ac.ir` or Ardabil portal **[VERIFY]**         |

**CD/USB Folder Structure:**
- CD1: Full thesis (Word + PDF)
- CD2: Full thesis (Word + PDF) + Database samples (Forms A2 & B2) + Abstract forms

**CD/USB Label Content:**
- Student name | Thesis title | Registration number | Academic year | Supervisor name

**Responsibility Disclaimer:**
> مسئولیت محتوای این پایان‌نامه بر عهده نویسنده است و دانشگاه آزاد اسلامی واحد اردبیل هیچ‌گونه مسئولیتی در قبال آن ندارد.

**[VERIFY] if Ardabil requires this page and its exact wording.**

---

## 24. SUBMISSION & DEFENSE PROCEDURES

| Item                              | Details                                                                  |
| --------------------------------- | ------------------------------------------------------------------------ |
| **Thesis Registration**           | Register topic in **سامانه پژوهشیار (Pazhooheshyar)** before starting     |
| **Registration Number**           | Appears on title page. Obtain from Pazhooheshyar                         |
| **Pre-Defense Submission**        | Submit copies to committee N days before defense **[VERIFY]**             |
| **Defense Presentation**          | Typically 15–20 slides, 20–30 min + Q&A **[VERIFY] format**               |
| **Defense Committee**             | Supervisor + Advisor + Internal Examiner + External Examiner + Dept Head  |
| **Plagiarism Check**              | Required. Acceptable similarity: < 25–30% **[VERIFY] tool & threshold**   |
| **Post-Defense Corrections**      | Typically 2–4 weeks **[VERIFY] deadline**                                 |
| **Fees**                          | Binding, CD preparation, submission fees **[VERIFY] amounts**             |
| **Final Bound Copies**            | 4: department, supervisor, library, student                               |

---

## 25. WORD TEMPLATE SETUP — Practical Steps

| Task                              | How to Do It in Word                                                  |
| --------------------------------- | --------------------------------------------------------------------- |
| **Set Margins**                   | Layout → Margins → Custom Margins → Enter values                      |
| **Set Line Spacing**              | Home → Paragraph → Line Spacing → Exactly → 28 pt                    |
| **Set Paragraph Indent**          | Home → Paragraph → Indentation → Special → First line → 1 cm          |
| **Create Multi-Level Numbering**  | Home → Multilevel List → Define New List Style → Link to Heading Styles |
| **Insert Captions**               | References → Insert Caption → Label: "شکل" or "جدول" → Chapter-based  |
| **Insert Page Numbers (Prelim)**  | Insert → Page Number → Bottom Center → Format: "الف، ب، ..."           |
| **Insert Page Numbers (Body)**    | Insert → Page Number → Bottom Center → Format: "۱، ۲، ..."             |
| **Section Breaks**                | Layout → Breaks → Next Page (separate Prelim from Body)               |
| **Widow/Orphan Control**          | Format → Paragraph → Line and Page Breaks → ON                         |
| **Auto-generate TOC**             | References → Table of Contents → Custom Table of Contents              |

---

## 26. COMPLETE FINAL CHECKLIST (Pre-Submission)

**Cover & Binding:**
- [ ] Dark blue hardcover
- [ ] Silver/gold stamping — **[VERIFY]**
- [ ] University logo placed correctly — **[VERIFY]**
- [ ] Spine: title + author name
- [ ] Cover text follows standard layout (§3.2)

**Page Setup:**
- [ ] Paper: A4 (21 × 29.7 cm)
- [ ] Margins (Ardabil): Top 3, Bottom 3, Right 3, Left 2 cm — **[VERIFY]**
- [ ] Line length: 16 cm
- [ ] Double-sided or one-sided — **[VERIFY]**
- [ ] No decorative borders/headers

**Typography:**
- [ ] Farsi Body: Lotus Thin 14 / B Nazanin 14 — **[VERIFY]**
- [ ] English Body: Times New Roman 12
- [ ] Chapter Titles: Lotus Bold 25 (Ardabil)
- [ ] No underlining; bold/italic used correctly
- [ ] No font mixing within same text level

**Paragraphs & Text:**
- [ ] Fully Justified (Ctrl+J)
- [ ] First line indent: ~1 cm
- [ ] Line spacing: ~1 cm / Exactly 28 pt — **[VERIFY]**
- [ ] One blank line between paragraphs
- [ ] Sentences: 15–25 words avg, max 35
- [ ] RTL for Persian, LTR for English
- [ ] Zero Markdown syntax in final docx
- [ ] No AI-vocabulary tells (delve, moreover, etc.)

**Numbering:**
- [ ] Hyphen-based system (`۲-۴-۳`)
- [ ] Prelim pages: Persian letters (الف، ب...)
- [ ] Body pages: Arabic numerals (۱، ۲...)

**Equations, Figures, Code:**
- [ ] Equations numbered by chapter, variables italicized
- [ ] Table captions ABOVE; Figure captions BELOW
- [ ] Code listings: LTR, Courier New/Consolas 10–11
- [ ] All figures/tables/equations/code referenced in text

**Citations & References:**
- [ ] Single citation style used 100% — **[VERIFY] Author-Date vs IEEE**
- [ ] Farsi references first, then Non-Farsi
- [ ] Every claim cited; all sources real
- [ ] Reference list fully cross-matched with in-text citations

**Front & Back Matter:**
- [ ] Approval page signed
- [ ] Declaration of originality included — **[VERIFY]**
- [ ] Persian abstract + keywords
- [ ] English abstract + keywords
- [ ] English title page (exact translation)
- [ ] Responsibility disclaimer — **[VERIFY]**
- [ ] TOC, List of Tables, List of Figures auto-generated

**Procedural:**
- [ ] Thesis registered in Pazhooheshyar (number on title page)
- [ ] Plagiarism report attached (similarity < threshold) — **[VERIFY]**
- [ ] Article publication/acceptance proof or supervisor confirmation
- [ ] Defense scheduled and confirmed
- [ ] 4 bound copies ready — **[VERIFY] exact count**
- [ ] 2 CDs/USBs ready (Word + PDF), correctly labelled
- [ ] All fees paid
- [ ] Digital submission to Irandoc / Ardabil portal completed

---

## 27. MASTER [VERIFY] CHECKLIST

| #  | Item to Verify                                                         | Who to Ask                     |
| -- | ---------------------------------------------------------------------- | ------------------------------ |
| 1  | **Stamp color:** Silver or gold?                                       | Thesis Affairs Office          |
| 2  | **Cover text:** Exact wording, font, and layout?                       | Thesis Affairs / Supervisor    |
| 3  | **Logo placement:** Top-center (common) or top-left 4×3 (claimed)?     | Thesis Affairs Office          |
| 4  | **Printing sides:** One-sided (traditional) or double-sided?           | Thesis Affairs Office          |
| 5  | **Margins:** Ardabil (R:3, L:2) or General IAU (R:2.5, L:3.5)?       | Supervisor + Thesis Affairs    |
| 6  | **Font family:** Lotus or B Nazanin/Zarr/Titr?                         | Supervisor / Recent theses     |
| 7  | **Chapter title font size:** 25 or smaller (e.g., 16)?                 | Supervisor / Official template |
| 8  | **Body line spacing:** Exactly 28 pt or Multiple 1.5?                  | Supervisor / Template          |
| 9  | **Citation style:** Author-Date (Ardabil) or IEEE (CS/SE standard)?   | Supervisor                     |
| 10 | **Back-matter order:** Appendices before References, or vice versa?    | Supervisor                     |
| 11 | **Bound copies:** 4 or 5?                                              | Thesis Affairs Office          |
| 12 | **Submission media:** CDs or USB drives?                               | Thesis Affairs Office          |
| 13 | **Spine text direction:** Bottom→top (RTL) or top→bottom (LTR)?        | Thesis Affairs Office          |
| 14 | **Declaration of originality:** Required?                              | Thesis Affairs / Supervisor    |
| 15 | **Research ethics statement:** Required for your data type?            | Supervisor                     |
| 16 | **Plagiarism check:** Required? Acceptable similarity %?               | Thesis Affairs Office          |
| 17 | **Plagiarism tool:** Turnitin, iThenticate, or Samim Noor?            | Thesis Affairs Office          |
| 18 | **Defense presentation:** Slides? Time limit? Handouts?                | Supervisor                     |
| 19 | **Defense committee:** Who are the internal/external examiners?        | Department Head                |
| 20 | **Pre-defense submission:** How many days before?                      | Thesis Affairs Office          |
| 21 | **Post-defense corrections:** How many days allowed?                   | Thesis Affairs Office          |
| 22 | **Registration number:** Where exactly on title page?                  | Thesis Affairs Office          |
| 23 | **Academic year:** Shamsi or Gregorian format?                         | Thesis Affairs Office          |
| 24 | **Responsibility disclaimer:** Required? Exact wording?               | Thesis Affairs Office          |
| 25 | **Digital submission portal:** Irandoc or Ardabil-specific?            | Thesis Affairs Office          |
| 26 | **Article requirement:** Acceptance letter format and deadline?        | Supervisor / Research Dept     |
| 27 | **Fees:** Exact amounts for binding, CDs, submission?                  | Thesis Affairs Office          |

---

## 💎 Final Recommendations

1. **Consult Your Supervisor** — This is the single most important step.
2. **Check the Official Portal** — `ardabil.iau.ir` for any posted regulations or forms.
3. **Use the Pazhooheshyar System** — Register thesis topic and proposals through **سامانه پژوهشیار**.
4. **Download a Template** — Look for pre-formatted Word templates for IAU Ardabil branch online.
5. **Examine Recent Theses** — Find 2–3 approved CS/SE theses from Ardabil (last 2–3 years) and use them as a visual reference.
6. **Print a Sample Page** — Before writing 80+ pages, set up your template and print **one sample page** to have your supervisor confirm margins, font, and spacing.
7. **Create a Submission Plan** — Track key dates, forms (Pazhooheshyar, Thesis Affairs), and fees.

---

## ⚠️ BRANCH DISCLAIMER

> **This document is the reconciled single source of truth, merging `Cloude_Final_Rules.md`, `Rules.md`, `Rules2.md`, and a third-party gap analysis.**
>
> If you are at **Tehran Central**, **Science & Research**, **Karaj**, **Dubai**, or any other branch:
>
> - Fonts may differ (Zarr/Nazanin/Titr instead of Lotus)
> - Margins may differ (e.g., Left 3.5 cm)
> - Citation styles may differ (strict APA or IEEE)
>
> **You MUST verify all rules with your specific branch's Office of Graduate Studies and your supervisor before final printing.** Department-specific requirements for Computer Science / Software Engineering may also apply (e.g., mandatory IEEE format for references).

---

_This document is the authoritative single source of truth. All 27 [VERIFY] items must be closed with your department before final printing. When in doubt, prioritize your branch's official printed manual._
