# Persian/Farsi Academic Markdown → DOCX: A Full Diagnostic Report

This report is split into two halves, because the failures come from two different places:

1. **The Markdown source file itself** — how Farsi text, math, citations, tables, and structure are *written* in the .md file.
2. **The Pandoc conversion pipeline** — how Pandoc (and the DOCX/OOXML format itself) handles RTL, bidi text, and complex scripts.

At the end there's a recommended "ideal setup" workflow.

---

## PART 1 — Problems Originating in the Markdown Source

### 1.1 Character-level and encoding issues
- **Arabic vs. Persian glyph confusion**: Persian keyboards/OCR tools often insert Arabic-variant characters instead of Persian ones — Arabic ي (U+064A) instead of Persian ی (U+06CC), Arabic ك (U+0643) instead of Persian ک (U+06A9), Arabic ة vs Persian ه. These render differently, break search/find-replace, break spellcheck, and can break alphabetical sorting in bibliographies.
- **Missing Zero-Width Non-Joiner (ZWNJ, U+200C)**: Persian compound words (می‌روم, کتاب‌ها, نمی‌شود) require ZWNJ for correct "half-space" rendering. If typed as a real space or omitted entirely, words either break onto two lines wrongly or fuse into one visually joined word. Many Persian MD files have inconsistent ZWNJ usage (some from Word, some from web copy-paste, some missing).
- **Zero-Width Joiner (ZWJ) and stray control characters**: Copy-pasted text from PDFs or websites often carries invisible characters (ZWJ, LRM U+200E, RLM U+200F, BOM) that silently corrupt rendering or Markdown parsing (e.g., breaking `**bold**` markers because a hidden character sits between asterisks and text).
- **Unicode normalization mismatch (NFC vs NFD)**: Text from different sources (Word, InDesign, web) may not be normalized consistently, causing "identical-looking" text to fail exact matches (important for automated citation or glossary matching).
- **Persian vs. Arabic-Indic vs. Latin digits**: ۰۱۲۳۴۵۶۷۸۹ (Persian), ٠١٢٣٤٥٦٧٨٩ (Arabic-Indic), 0123456789 (Latin) look similar but are different code points. Mixed use within one document (common when pasting from different sources) causes visual inconsistency and breaks numeric sorting/parsing.

### 1.2 Bidirectional (RTL/LTR) text mixing
- **Directional runs without markers**: A Farsi sentence containing an English term, a citation key, a variable name, or a number needs correct bidi handling. Plain UTF-8 text without embedded directional marks (LRM/RLM, or `\u2066…\u2069` isolates) can render with words in the wrong order, especially around punctuation and parentheses.
- **Parentheses/brackets flipping**: In RTL context, `(text)` should visually mirror — but mixed LTR content inside parentheses within an RTL sentence is one of the most common visual bugs: numbers, citation years, or English abbreviations inside `()` frequently show the wrong bracket orientation or content order after rendering.
- **Mixed-language sentences**: A sentence like `این روش در (Smith, 2020) بررسی شده و دقت آن ۹۵٪ است` mixes Farsi, Latin citation, and Persian percent sign — each segment has its own directionality, and Markdown itself carries **no bidi metadata at all**, so correctness depends entirely on how the renderer (Pandoc/Word) infers direction from the Unicode Bidi Algorithm — which frequently guesses wrong on short mixed runs.
- **Punctuation and symbol directionality**: Persian uses its own comma (،), semicolon (؛), and question mark (؟). Using Latin `,` `;` `?` instead is common (from English-layout typing) and causes both cosmetic inconsistency and, in RTL rendering, sometimes causes the punctuation to visually detach or reorder.
- **Quotation marks**: «guillemets» are the traditional Persian style vs. curly “ ” (English) vs straight `" "`. Mixed usage looks unprofessional and some render engines mirror the wrong direction for `“ ”` in RTL runs.

### 1.3 Persian-specific spacing rules
- **Half-space (ZWNJ) vs. full space vs. no space** — three different spacing states exist in Persian orthography for compound words, prefixes (می, نمی), and plural ها/ات suffixes. Markdown editors that auto-"clean" whitespace (trimming multiple spaces, converting tabs) frequently strip ZWNJ or replace it with a normal space.
- **Space before Persian punctuation**: Standard Persian typography puts *no* space before ؟ ، ؛ but a Latin-typing habit often adds one — inconsistent across a large document, which is visually distracting in a formal academic file.
- **Non-breaking spaces around numbers/units**: e.g., ۵ متر — if a normal space is used, "5" and "متر" can end up on separate lines at a line break.

### 1.4 LaTeX / math formulas
- **Bidi collision inside math mode**: `$x_1 + y_2 = ۵$` — mixing Persian digits or Farsi text inside a LaTeX math span is a serious source of breakage. Math is inherently LTR; embedding it inside an RTL paragraph without isolation frequently causes the *whole formula* to visually reverse (e.g., `a - b` rendering as `b - a`), or causes text captions/labels for equations to detach from the formula's flow.
- **Farsi variable names or text-in-math**: `$\text{سرعت} = \text{مسافت}/\text{زمان}$` — `\text{}` runs inside math environments are one of the most fragile spots; Pandoc's math-to-OMML (Office Math) converter has inconsistent RTL support for embedded text runs, and equation numbering `(1)`, `(2)` at the right/left margin often ends up on the wrong side for RTL academic convention (Persian theses conventionally put equation numbers on the **left**, opposite of English convention on the right — this is rarely handled automatically).
- **Inline vs. display math delimiters**: `$...$` vs `$$...$$` vs `\(...\)` vs `\[...\]` — Pandoc requires consistent delimiter conventions and a `math` extension enabled; mixed delimiter styles from copy-pasted content silently fail to render as math and appear as literal dollar-sign text.
- **Numbering/cross-referencing formulas**: Markdown alone has no native equation-numbering/cross-ref mechanism; without a filter (e.g., `pandoc-crossref`), equation numbers must be typed manually and are not consistent with the direction of the surrounding Farsi text.

### 1.5 References / citations
- **Bibliography style and sorting**: Pandoc-citeproc/citeproc sorts references alphabetically by default using Unicode collation, which does **not** correctly alphabetize Persian entries by Persian alphabetical order unless a Farsi-aware CSL locale (`fa-IR`) and a Farsi CSL style are explicitly used. Many CSL styles are English-only, so Persian names/titles sort incorrectly or citation labels format in the wrong (Latin) convention.
- **Mixed-language bibliography**: A reference list mixing Farsi-titled and English-titled sources is common in Persian theses; without careful CSL configuration, the two get inconsistent punctuation, name-order (family/given), and directionality (Farsi entries may not correctly right-align while English ones stay left-aligned).
- **In-text citation style**: Persian academic convention often uses author-year in Farsi numerals or a bracketed numeric system `[۱]`; Pandoc's default citation processor outputs Latin numerals/format unless explicitly configured, creating inconsistency with surrounding Farsi digits.
- **BibTeX/CSL-JSON encoding**: `.bib` files with Farsi entries need correct UTF-8 handling and often break if fields contain unescaped Farsi punctuation or ZWNJ characters inside titles.

### 1.6 Tables
- **Column order and alignment**: Markdown pipe-tables (`| col1 | col2 |`) are inherently defined left-to-right in the source syntax regardless of content language. Pandoc does not automatically reverse column order for RTL tables, so a table meant to be read right-to-left (per Persian convention) is often still rendered with the first Markdown column on the *left* in the DOCX, contradicting a Farsi reader's expectation of "first column on the right."
- **Text alignment inside cells**: Markdown table syntax only supports left/center/right column alignment markers (`:---`, `:---:`, `---:`); this maps to LTR-relative alignment, not RTL-relative — so "right-aligned" in Markdown may not equal "reading start" alignment in an RTL cell.
- **Mixed content per cell**: Numbers, Farsi text, and English abbreviations inside the same cell face the same bidi problems as inline text (see 1.2), often worse because table cells are narrow and wrap more.
- **Long tables spanning pages**: Markdown has no native "repeat header row" instruction; this must be set manually in the DOCX afterward, or it's lost.

### 1.7 Table of Contents / List of Figures / List of Tables
- **No native RTL TOC support in Markdown**: A Markdown-generated TOC (`toc: true` in YAML) is inserted by Pandoc as a flat, LTR-ordered field. Persian academic ToCs conventionally have page numbers on the **left** with dot-leaders running right-to-left toward them, and are read top-to-bottom but each line right-aligned — Pandoc's default TOC/field code does not replicate this without manual Word-side reformatting.
- **Page numbers in Farsi numerals**: Persian formal documents often use Persian digits for the body page numbers and sometimes Latin/lowercase-roman for front matter (مقدمه, فهرست) — Markdown/Pandoc have no built-in mechanism for automatic Persian-numeral page numbering; this must be done manually in Word after conversion (via section breaks and number-format settings).
- **List of Figures / List of Tables**: These typically rely on Word's caption/cross-reference fields, which Pandoc does not generate natively from Markdown image captions — they must be added post-conversion or via `pandoc-crossref` with careful configuration, and even then the resulting Word fields are LTR by default.
- **Heading numbering (١.٢.٣ vs 1.2.3)**: If the outline numbering is expected in Farsi digits, Pandoc's default heading/TOC numbering uses Latin digits; there's no built-in flag to force Persian numerals in the auto-numbering.

### 1.8 Lists (bulleted/numbered) and other block structures
- **List markers on the wrong side**: Ordered/unordered list bullets and numbers are LTR-positioned by default (marker on the left, text flowing right in the DOCX list style) — for correct Farsi lists, the number/bullet should sit on the **right**. Markdown gives no control over this; it's purely a DOCX list-style/paragraph-direction issue downstream.
- **Nested lists with mixed-language items**: compound the bidi problems of 1.2 at increasing indentation levels.
- **Footnotes**: Markdown footnote markers `[^1]` are rendered as superscript Latin numerals by Pandoc; Persian formal documents sometimes expect Persian-numeral or symbol-based footnote marks — not configurable from Markdown alone.
- **Blockquotes and code blocks**: Code blocks (needed for e.g. algorithm listings) are always LTR by definition (correct), but if they're placed inside an RTL document without an explicit direction override, Word can misapply paragraph-level RTL formatting to the code block itself, breaking monospace alignment.

### 1.9 Symbols and typography
- **Percent, currency, and unit symbols**: ٪ (Persian percent, symbol before the number) vs % (Latin, after the number) — placement convention differs; mixed usage is extremely common in translated/adapted academic content.
- **Em-dash / en-dash usage**: Persian text conventionally uses different dash and ellipsis conventions than English; Markdown's autoconversion of `--`/`---` to en/em-dash assumes an LTR context and can look wrong when the dash sits inside a heavily RTL sentence.
- **Mathematical/logical symbols (≤, ≥, →, ∑, √) inside prose (not math mode)**: These are LTR by Unicode default and can pull surrounding RTL text out of order if not isolated.

---

## PART 2 — Problems from the Pandoc → DOCX Conversion Process

### 2.1 DOCX/OOXML's fundamental RTL model
- Word's OOXML format encodes directionality **per paragraph and per run** (`<w:bidi/>`, `<w:rtl/>` properties), not as a document-wide "RTL mode." Pandoc, when converting from Markdown, generally does **not** emit these bidi/RTL paragraph properties automatically — it produces plain LTR paragraphs even if the visible text is Persian. The document *looks* correct only because Word applies its Unicode Bidi Algorithm at render time per character run — but paragraph alignment, list markers, and table direction stay LTR-styled underneath, causing:
  - Bullet/number lists sitting on the left instead of the right.
  - Paragraph alignment defaulting to left instead of right (unless explicitly set in the reference DOCX).
  - Tables anchored/direction as LTR (column 1 leftmost) instead of RTL (column 1 rightmost).

### 2.2 The reference.docx template problem
- Pandoc styles all output using a `reference.docx` template (default or user-supplied). If this template's built-in styles (Normal, Heading 1–6, List Paragraph, Table Grid, Caption, TOC styles, Footnote) are **not** explicitly set to RTL/bidi + a Farsi-friendly font (e.g., B Nazanin, Vazirmatn, IRANSans, XB Zar), the resulting DOCX will:
  - Use LTR paragraph direction sitewide even though it holds Farsi text.
  - Use a font stack that doesn't include appropriate Persian glyph shaping, causing tofu boxes, wrong glyph joining, or missing ZWNJ rendering.
  - Have header/footer, TOC and heading styles all LTR-templated.
- **This is the single biggest fixable/preventable cause of "broken-looking" Farsi DOCX output** — but it requires manually building/configuring a proper RTL reference.docx, which most users skip.

### 2.3 Math conversion (LaTeX → OMML)
- Pandoc converts `$...$`/`$$...$$` LaTeX into Word's native OMML (Office Math Markup Language) by default. OMML equation objects are internally LTR containers; Word does have RTL math support (`m:rPr` with bidi), but Pandoc's LaTeX→OMML converter (via `texmath`) has incomplete/inconsistent handling of RTL contexts and Farsi `\text{}` runs — commonly resulting in:
  - Correct math symbols but wrong overall equation direction/alignment.
  - Farsi text inside `\text{}` rendering with disconnected letters (because Word's math run doesn't apply Arabic-script shaping the same way body text does).
  - Equation numbers ending up on the Word-default (right) side instead of the Persian-convention (left) side.
- Alternative: converting math to embedded images (via `--webtex` or MathML-to-image) sidesteps OMML RTL bugs entirely but loses editability and can look visually inconsistent with body text size/baseline.

### 2.4 Citation processing (citeproc)
- Pandoc's citeproc engine needs `csl` (style) + `bibliography` + correct `lang: fa-IR` in YAML metadata to produce correctly localized citation punctuation, name order, and sorting. Missing `lang` metadata is one of the most common oversights — citeproc then defaults to English locale rules even for Farsi-titled references.
- Even with correct locale, many public CSL styles simply lack full `fa-IR` term translations (words like "and", "edition", "volume", "in:" for embedded citations) — leading to a document that's *mostly* Farsi but has a scattering of untranslated English connector words in the bibliography.
- The generated bibliography paragraph style comes from the reference.docx `Bibliography`/`CSL-...` style — if that's not RTL-configured, entries will be left-aligned/LTR even if the reference text itself is Persian.

### 2.5 Table of Contents / cross-reference fields
- Pandoc's `--toc` inserts a static list of links (or, with `--toc` + certain writer settings, a Word TOC field). Either way, it's generated with LTR paragraph/tab-leader settings by default. Word's *native* RTL TOC (dot leaders running right-to-left, page number on the left) requires the TOC field's paragraph style to carry `bidi` — again dependent on the reference.docx, not something Pandoc sets automatically.
- `pandoc-crossref` (for List of Figures/Tables/Equations) generates plain sequential fields (`SEQ Figure`) that are numeral-based only — no automatic Persian-numeral formatting, and the caption paragraph direction again depends on the template.

### 2.6 Font handling and fallback
- Pandoc does not embed fonts; it just references font names in styles. If the reference.docx specifies a Farsi font not installed on the machine opening the file, Word silently substitutes a fallback font — this can silently break ZWNJ rendering, digit shapes, or overall glyph shaping quality, and is invisible until opened on a different machine.
- Persian requires **Arabic-script-aware OpenType fonts** with proper `mark`/`mkmk`/`init`/`medi`/`fina` GSUB features for correct letter joining; generic "Unicode" fonts without full Arabic shaping tables can render disconnected or malformed Persian letterforms even though the Unicode text is correct.

### 2.7 Numerals
- Pandoc performs no digit transliteration. All numerals typed as Latin digits stay Latin; all typed as Persian digits stay Persian; there is no post-conversion "make all page numbers/citations Persian numerals" step — that's either handled at the Markdown-authoring stage (consistently typing Persian digits) or via manual Word field-formatting after conversion (`\* ARABIC` vs custom number format `۰۱۲۳...`).

### 2.8 Header/footer, section breaks, and page setup
- Markdown has no concept of headers/footers, section breaks, or page-number-format changes (e.g., roman numerals for front matter, Persian numerals for body) — 100% of this must be done manually in Word post-conversion, and it's easy to introduce direction bugs at each section break (each section has its own bidi/LTR context flag).

### 2.9 Miscellaneous conversion quirks
- **Nested emphasis/bold with Farsi text**: `**متن پررنگ**` sometimes breaks if invisible characters (ZWNJ, LRM) sit adjacent to the `**` markers — Pandoc's Markdown parser is strict about marker adjacency to "word characters," and some Persian-specific invisible characters aren't classified as expected, silently disabling the bold/italic.
- **Smart punctuation (`--smart` / default in Pandoc ≥2.x)**: automatic curly-quote and dash conversion is tuned for English typography and can produce wrong-direction curly quotes or unwanted em-dash conversions in Farsi text; usually should be disabled (`--no-smart` or set in defaults file) for Farsi documents and quotes typed explicitly as « » where needed.
- **YAML metadata block encoding**: if `lang`, `dir`, or title metadata fields contain Farsi text, encoding mismatches (non-UTF-8 saved files) show up as mojibake in the title page/metadata — always ensure the .md file itself is saved as UTF-8 (without BOM causing issues) before conversion.

---

## PART 3 — Recommended "Ideal Setup" Workflow

**A. In the Markdown source**
1. Save the file as UTF-8. Standardize on Persian (not Arabic) letterforms (ی ک ه) — run a find/replace pass or a normalization script.
2. Use ZWNJ (`\u200C`) consistently for compound words — ideally normalize this programmatically (e.g., a Python script with `virastar`/`hazm`-style Persian text cleanup) rather than relying on manual typing.
3. Standardize on one numeral system per context deliberately (e.g., Persian digits in prose, Latin digits inside code/math) and be consistent.
4. Use Persian punctuation (، ؛ ؟ «»​) explicitly rather than Latin equivalents.
5. For math: keep formulas numerically/symbolically clean; avoid embedding Farsi words inside `\text{}` where possible — if unavoidable, test render early and expect manual fixing.
6. For citations: set YAML `lang: fa-IR`, use a CSL style with confirmed `fa-IR` locale terms (test with a few entries before committing to a 100-source bibliography), and keep bibliography entries in a clean CSL-JSON or BibTeX file with escaped/normalized Farsi.
7. For tables, remember Markdown table syntax is always authored left-to-right positionally — decide up front whether you'll reverse column order manually in the source to match RTL reading order, or fix it in Word afterward.
8. Disable Pandoc's smart typography (`--no-smart`) to avoid unwanted curly-quote/dash conversions.

**B. In the Pandoc conversion step**
1. Build (once) a proper `reference.docx`: set `Normal`, all `Heading` styles, `List Paragraph`, `Table Grid`, `Caption`, `TOC 1–3`, `Bibliography`/CSL styles, `Footnote Text`, and header/footer styles to right-to-left paragraph direction and a proper Persian OpenType font (e.g., Vazirmatn, IRANSans, XB Zar, B Nazanin). Set default table direction to RTL. Reuse this template for every conversion.
2. Convert with explicit metadata: `lang: fa-IR`, `dir: rtl` in YAML (Pandoc does pass `dir` through in some writers/contexts and it helps downstream tools), and specify `--csl=your-farsi-style.csl --bibliography=refs.bib`.
3. Consider `--webtex` or MathML-to-image rendering for math instead of native OMML if you hit persistent RTL/equation-direction bugs — trade editability for reliability.
4. Use `pandoc-crossref` for figure/table/equation numbering, but plan for a manual pass afterward to fix numeral system and paragraph direction on generated captions/TOC/LoF/LoT fields.
5. **Always plan for a manual Word finishing pass**: page-number formatting (Persian numerals, section-based front/body matter), TOC dot-leader direction, list bullet-side correction, and spot-checking every formula and table — DOCX's per-paragraph bidi model means Pandoc cannot fully automate a publication-ready RTL academic document from Markdown alone today.

**C. Alternative pipeline worth considering**
For heavily mathematical, heavily-cited Persian theses, many academic users get more reliable, more "typographically correct" results going **Markdown → LaTeX (using `xepersian`/`bidi` packages) → PDF**, rather than → DOCX, since XeLaTeX/`xepersian` has mature, purpose-built Persian RTL, digit, and math-direction handling that DOCX/OOXML + Pandoc's writer does not yet fully match. If a DOCX is still required as a deliverable (e.g., for a Word-based journal template), converting PDF→DOCX or doing the DOCX pass only for a mostly-text version (with math/tables handled separately) is sometimes more robust than trying to get one Pandoc DOCX pass to be publication-ready.

---

**Bottom line**: Markdown itself carries no directionality, spacing, or script-shaping metadata — every RTL-specific behavior in the final DOCX depends on (a) disciplined, normalized Farsi text in the source file, and (b) an RTL-correctly-configured `reference.docx` plus explicit CSL/locale/math settings at conversion time. Skipping either side is what produces the classic symptoms: bullets on the wrong side, equations facing the wrong way, tables reading left-to-right, mixed numerals, and a bibliography that's alphabetized as if it were English.