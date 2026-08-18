# Collective Markdown-to-DOCX Conversion Standards

> Consolidated from ChatGPT, Claude, DeepSeek, and Gemini analysis — 4 sources, 1 unified reference.

---

## Part I — Core Architecture

### 1. Semantic Model Principle

| Layer | Owns | Controls |
|-------|------|----------|
| Markdown | **Semantic meaning** | Structure, content, intent, relationships |
| Word/DOCX | **Visual styling** | Fonts, spacing, colors, layout, pagination |

> Markdown tells Word *what something is*. Word decides *how it looks*. ([ChatGPT §1](ChatGPT-md.md), [Claude Part1](Cloude-md.md))

Markdown is a lightweight markup language for creating formatted text using a plain-text editor. ([DeepSeek §5](deepseek-md.md))

### 2. Markdown Limitations

Markdown **cannot** represent everything Word can. Pandoc deliberately uses an intermediate representation that cannot represent every feature of richer formats. ([ChatGPT §68](ChatGPT-md.md))

### 3. Recommended Workflow

```text
Farsi Academic MD (UTF-8 + strict authoring rules)
    ↓
  Validator (catch issues BEFORE Pandoc)
    ↓
  Clean semantic source
    ↓
  Pandoc parser
    ↓
  Pandoc AST
    ↓
┌──────────┼──────────┐
│          │          │
RTL filter  citeproc   crossref filter
│          │          │
└──────────┼──────────┘
    ↓
  DOCX writer
    ↓
  reference.docx (academic Persian styles + RTL)
    ↓
  DOCX file
    ↓
  Word field refresh (F9)
    ↓
  Visual + structural validation
```

([ChatGPT §72](ChatGPT-md.md), [Gemini recommendations](Gemini-md.md))

### 3.1. Post-Conversion VBA Automation (Word Macro)

Since manual post-processing is typically required for complex Persian documents, you can automate the repetitive fixes with a Word VBA macro.

```vba
Sub FixPersianRTL()
    ' Update all fields (TOC, cross-references)
    ActiveDocument.Fields.Update
    ' Set paragraph direction to RTL for all body paragraphs
    ' (Skip tables — table direction should be set per-table based on content)
    Dim para As Paragraph
    For Each para In ActiveDocument.Paragraphs
        ' Only set RTL on paragraphs that are not inside tables
        If para.Range.Information(wdWithInTable) = False Then
            para.Format.RightToLeft = True
        End If
    Next para
    ' Update TOC again after changes
    If ActiveDocument.TablesOfContents.Count > 0 Then
        ActiveDocument.TablesOfContents(1).Update
    End If
End Sub
```

> **Warning:** Do NOT blindly set all tables to RTL. Tables with numeric/LTR columns (e.g., parameter tables, results tables) should remain LTR or be set individually after inspection. The macro above deliberately skips tables to avoid damaging mixed-content tables.

([Gemini recommendations](Gemini-md.md))

### 4. Pandoc Suitability Assessment

| Component | Rating |
|-----------|--------|
| Persian plain text | Excellent |
| UTF-8 | Excellent |
| Markdown structure | Excellent |
| LaTeX equations | Very good |
| Citations / BibTeX / CSL | Excellent |
| Basic tables | Good |
| Complex tables | Weak–moderate |
| Figures | Good |
| Cross-references | Good with appropriate tooling |
| RTL paragraphs | Good but needs design/testing |
| Mixed RTL/LTR | Risky |
| Persian typography | Needs custom policy |
| Word academic formatting | Very good with reference.docx |
| Highly customized university thesis | Good, but requires engineering |

**Overall: ~88%** for a carefully engineered Persian academic workflow.
A naive `thesis.md → pandoc → thesis.docx` is closer to **55–65%**.

([ChatGPT §70](ChatGPT-md.md))

### 5. Hierarchy of Control Layers

| Requirement | Best layer |
|-------------|------------|
| Persian spelling | Source / validator |
| Unicode normalization | Validator / filter |
| ZWNJ | Source / validator |
| Citations | Pandoc + CSL |
| Bibliography | BibTeX / CSL |
| Equations | Markdown LaTeX |
| Cross-references | Pandoc / filter |
| Heading numbering | DOCX / Pandoc mechanism |
| Fonts | reference.docx |
| RTL paragraph style | reference.docx / filter |
| LTR exceptions | Markdown attributes / filter |
| Table styling | reference.docx |
| Page size / margins | reference.docx |
| Header / footer | reference.docx |
| Page numbers | DOCX |
| TOC | DOCX / Pandoc + field update |
| List of figures / tables | DOCX / field mechanism |
| Complex table merging | Specialized handling |
| Page breaks | DOCX / filter |
| Final pagination | Word |

([ChatGPT §69](ChatGPT-md.md))

---

## Part II — Unicode & Encoding

### 6. Arabic vs Persian Character Confusion

This is the **single most insidious** problem.

| Character | Arabic | Persian |
|-----------|--------|---------|
| Yeh | `ي` (U+064A) | `ی` (U+06CC) |
| Keh | `ك` (U+0643) | `ک` (U+06A9) |

Word **will not apply the Persian font** to Arabic characters — they will render in fallback/Arabic fonts, creating ugly mixed fonts within the same word.

**Detection is difficult** because Arabic and Persian characters look nearly identical visually. ([ChatGPT §4](ChatGPT-md.md), [DeepSeek Part1](deepseek-md.md))

### 7. Arabic Comma vs Persian Comma

| Symbol | Name | Unicode |
|--------|------|---------|
| `،` | Arabic comma (correct for Persian) | U+060C |
| `,` | English comma (wrong for Persian) | U+002C |

Wrong comma → Word treats the context as LTR → mixed-up punctuation and directionality.

([ChatGPT §11](ChatGPT-md.md), [DeepSeek Part1](deepseek-md.md))

### 8. Invalid Unicode Characters

Bad copy-paste introduces broken encoding sequences, unsupported characters, or invalid control characters (e.g. form feed `\x0C`). This can crash Pandoc or produce incorrect output.

([DeepSeek Part1](deepseek-md.md), [Gemini considerations](Gemini-md.md))

### 8.1. File Paths Must Use ASCII Characters Only

Image filenames, folder names, and any file paths referenced in the Markdown source **must use ASCII characters only**. Persian characters in filenames (e.g., `شکل۱.png`, `پوشه/تصویر.jpg`) cause Pandoc to fail to locate or embed the file. Use simple Latin names: `figure1.png`, `images/`, `chapter3/`.

([DeepSeek Part1](deepseek-md.md))

### 9. Unicode Normalization

Validator should check: malformed Unicode, unexpected control characters, inconsistent Persian/Latin digits.

([ChatGPT §66](ChatGPT-md.md))

---

## Part III — Bidirectional (Bidi) Text

### 10. Why Bidi Is the #1 Challenge

This is the **single most difficult issue**. The Unicode Bidirectional Algorithm is not perfect. It fails at the boundaries between Persian and English characters, especially with punctuation, numbers, and mixed-direction text inside tables.

([ChatGPT §15](ChatGPT-md.md), [DeepSeek Part1](deepseek-md.md), [Claude Part1](Cloude-md.md))

### 11. Parentheses in Bidi Context

Parentheses have inherent directionality — they may appear "reversed" when the paragraph direction switches.

| Input | Appears as | Correct |
|-------|------------|---------|
| `要有(中文)` | `要有)中文(` | `要有(中文)` |

([ChatGPT §9](ChatGPT-md.md))

### 12. RTL Paragraphs in Word

In mixed Persian+English paragraphs:
- Numbers and English words remain LTR
- The rest is RTL
- **Commas, periods, parentheses may appear on wrong sides**

([ChatGPT §8](ChatGPT-md.md))

### 13. RTL Constraint for Persian

`dir="rtl"` must be applied **at the paragraph level**, not the block level. Otherwise, anything after a heading in a different direction will break the RTL context.

([Claude Part1](Cloude-md.md))

### 13.1. Pandoc's Failure to Set OOXML `<w:bidi>` (Critical)

Pandoc sets `dir="rtl"` in its internal AST, but the DOCX writer **does not reliably emit** the Word OOXML `<w:bidi/>` paragraph property. Consequently, the paragraph *looks* right-aligned, but Word's internal BiDi engine still treats it as LTR for list bullets, TOC tab-stops, and table cell anchoring.

**Mitigation:**
1. In your `reference.docx`, explicitly set the "Normal" style's paragraph direction to "Right-to-Left" *and* ensure the "Complex Script" tab has the same setting. This forces Word to apply `<w:bidi/>` to all paragraphs inheriting that style.
2. In your Lua filter, explicitly set `p.dir = "rtl"` for all Para/Plain blocks, but also test the resulting DOCX by inspecting the paragraph properties in Word's "Reveal Formatting" pane to confirm `<w:bidi/>` is present.
3. As a fallback, use the VBA macro in §3.1 to force RTL on all paragraphs post-conversion.

([Claude Part2.1](Cloude-md.md), DeepSeek consolidation warning)

### 14. Embraces and Brackets in RTL

In RTL context, brackets and braces may appear visually reversed:
- `LRE {something}` may render as `}something{` instead of `{something}`

([ChatGPT §19](ChatGPT-md.md))

### 15. Common Bidi Failure Combinations (Risk-ranked)

| Rank | Combination | Risk |
|------|-------------|------|
| 1 | Persian + English + numbers + parentheses | 10/10 |
| 2 | RTL table + LTR numeric columns | 10/10 |
| 3 | Persian citation + punctuation + numerical citation | 9.5/10 |
| 4 | Persian text inside LaTeX math | 9/10 |
| 5 | Complex table + merged cells + captions | 9/10 |
| 6 | Automatic cross-reference + RTL numbering | 9/10 |
| 7 | Bibliography (Persian + English + DOI/URL) | 9/10 |
| 8 | Persian ZWNJ + Unicode normalization | 9/10 |
| 9 | TOC / list of figures + automatic numbering | 8/10 |
| 10 | Plain Persian paragraphs | 2/10 |

([ChatGPT §71](ChatGPT-md.md))

---

## Part IV — Persian Typography & Spacing

### 16. ZWNJ (Zero-Width Non-Joiner)

ZWNJ (U+200C) is **critical** for correct Persian typesetting. Incorrect usage is one of the most common mistakes.

**Correct usage:** `بی‌نظیر` (with ZWNJ between `ی` and `ن`)
**Incorrect:** `بی نظیر` (with space) or `بی‌نظیر` (missing ZWNJ)

The correct word is `بی‌نظیر`, not `بی نظیر`. ZWNJ must be placed precisely to join or separate characters correctly.

([ChatGPT §4](ChatGPT-md.md), [DeepSeek Part1](deepseek-md.md), [Gemini considerations](Gemini-md.md))

### 17. Space Before Arabic/Persian Commas

Space before `،` (Arabic comma) is **forbidden**:
- Incorrect: `جمله اول ،جمله دوم`
- Correct: `جمله اول،جمله دوم`

([ChatGPT §11](ChatGPT-md.md), [Claude Part1](Cloude-md.md))

### 18. English Words in Persian Text

- Avoid mixing English words inside Persian sentences
- If unavoidable, enclose in `\lr{}` and **remove spaces** between English and Persian characters:
  - Incorrect: `\lr{Python} \lr{ fluently}`
  - Correct: `\lr{Python}\lr{fluently}`

([ChatGPT §12](ChatGPT-md.md), [Claude Part1](Cloude-md.md))

### 19. Whitespace Issues

| Issue | Problem |
|-------|---------|
| Repeated spaces | Word may ignore them or create inconsistent spacing |
| NBSP misuse | Confuses layout in DOCX — use only for intentional non-breaking |
| Leading/trailing whitespace | May cause unexpected behavior in Pandoc parsing |

([ChatGPT §52](ChatGPT-md.md), [DeepSeek Part1](deepseek-md.md))

### 20. Unicode NFKC Normalization

Replaces visually identical characters with canonical equivalents. For example, `٪` (Arabic Percent, U+066A) is normalized to `%` (U+0025), and fullwidth digits (`０１２`) are normalized to ASCII digits (`012`). This can cause Word to interpret the text differently — your carefully typed Persian percent sign or Persian digits may silently become Latin equivalents.

**Mitigation:** Bypass NFKC or use custom Lua filter to preserve intentional Unicode variants.

([ChatGPT §4](ChatGPT-md.md), [DeepSeek Part1](deepseek-md.md))

---

## Part V — Numbers, Math & Equations

### 21. Persian vs English Digits

| Value | Persian | English |
|-------|---------|---------|
| 0 | ۰ | 0 |
| 1 | ۱ | 1 |
| 2 | ۲ | 2 |
| 3 | ۳ | 3 |
| 4 | ۴ | 4 |
| 5 | ۵ | 5 |
| 6 | ۶ | 6 |
| 7 | ۷ | 7 |
| 8 | ۸ | 8 |
| 9 | ۹ | 9 |

**Policy decision required:** Which contexts use Persian digits vs English digits? Recommendation: English digits for math/numbers, Persian digits for text.

([ChatGPT §6](ChatGPT-md.md))

### 21.1. Word's Global Numeral Override

Microsoft Word has a global setting (`File > Options > Advanced > Show document content > Numeral`) that can override the Unicode digits you typed. Options:

| Setting | Effect |
|---------|--------|
| **Context** | Respects the digits you actually typed (recommended) |
| **Arabic** | Forces all digits to Arabic-Indic (`٠١٢٣`) |
| **Hindi** | Forces all digits to Extended Arabic-Indic / Persian (`۰۱۲۳`) |

If set to "Arabic" or "Hindi" globally, Word may forcibly convert your English digits to Persian (or vice versa) inconsistently across headers, footers, and body text. **Always verify this setting on the machine where the final DOCX is opened.** Set it to **"Context"** to ensure Word respects the digits from your MD source.

([Gemini considerations](Gemini-md.md))

### 22. Number Formatting

| Symbol | Issue |
|--------|-------|
| `-` (hyphen-minus) vs `−` (minus sign) | Confused frequently |
| `.` (period) vs `٫` (Arabic decimal separator) | Mixed in Persian text |
| `%` vs `٪` (Arabic percent) | Must be consistent |

([ChatGPT §10](ChatGPT-md.md), [Gemini considerations](Gemini-md.md))

### 23. Numbers in Bidi Context

Numbers form directional runs according to Unicode Bidirectional Algorithm rules; do not manually reverse or reorder numeric strings. European numerals (U+0030–U+0039) have bidi class `EN` (European Number), which inherits direction from the surrounding strong characters. Arabic-Indic numerals (U+0660–U+0669) have bidi class `AN` (Arabic Number). Both interact with surrounding RTL/LTR context and neutral characters differently. **Test numbers together with surrounding punctuation, parentheses, units, and RTL text** — the combination matters more than the number alone.

([ChatGPT §10](ChatGPT-md.md))

### 24. Percentages in Bidi

| Input | May appear as |
|-------|---------------|
| `۹۵٪` | `٪۹۵` (reversed!) |

The percent sign may appear on the wrong side.

([ChatGPT §10](ChatGPT-md.md), [Gemini considerations](Gemini-md.md))

### 25. LaTeX Math — General

LaTeX math is **well supported**. Pandoc preserves math semantics without modification.

([ChatGPT §13](ChatGPT-md.md), [DeepSeek Part1](deepseek-md.md))

### 26. LaTeX Inline Math

Use `$...$` or `\(...\)`:
```markdown
The equation is $E = mc^2$ in Persian text.
```

⚠️ No space after `$` or before `$`.

([ChatGPT §13](ChatGPT-md.md))

### 27. LaTeX Display Math

Use `$$...$$` or `\[...\]`:
```markdown
$$
\int_a^b f(x) \, dx = F(b) - F(a)
$$
```

([ChatGPT §13](ChatGPT-md.md))

### 28. RTL Math Environments

RTL environments (`align`, `cases`, etc.) have known Pandoc rendering issues. Avoid complex RTL math environments or test extensively.

([ChatGPT §14](ChatGPT-md.md))

### 29. Persian Text Inside LaTeX Math

When Persian text is inside LaTeX:
```markdown
$\alpha$ مقدار ثابت است.
```
Word has difficulty mixing the math font with the Persian font. **High failure risk (9/10).**

([ChatGPT §14](ChatGPT-md.md), [ChatGPT §71](ChatGPT-md.md))

### 30. LaTeX Macros

Macros defined in a `preamble.tex` and passed via `--include-in-header` work. Use a local `.tex` file instead of passing complex macros via `--metadata-file`.

([ChatGPT §13](ChatGPT-md.md))

---

## Part VI — Citations & Bibliography

### 31. Citation Styles

Pandoc has **excellent** BibTeX and CSL support. Works well for both:
- **Author-date** style: `(Author, Year)` or `Author (Year)`
- **Numeric** style: `[123]`

([ChatGPT §5](ChatGPT-md.md))

### 32. Citation Commands

```markdown
Single citation: @author2020
Parenthetical: [@author2020]
Multiple: [@author2020; @author2021]
```

([ChatGPT §5](ChatGPT-md.md))

### 33. Bibliography Files

```yaml
---
bibliography: references.bib
csl: chicago-author-date.csl
---
```

Supports `.bib`, `.json`, `.yaml` formats. Multiple files allowed.

([ChatGPT §5](ChatGPT-md.md))

### 34. Persian Citations (Risk: 9.5/10)

Persian citation + punctuation + numerical citation creates complex bidi situations. Test extensively.

([ChatGPT §71](ChatGPT-md.md))

### 35. Bibliography — Mixed Content (Risk: 9/10)

Bibliography containing Persian + English + DOI/URL is a high-risk combination. Ensure consistent formatting and test rendering.

([ChatGPT §71](ChatGPT-md.md))

### 36. DOI and URLs

```markdown
DOI: 10.1234/example
URL: <https://example.com>
```

DOI should remain as plain text, not hyperlinked. Bold the `DOI:` label, keep the number as plain text.

([ChatGPT §16](ChatGPT-md.md))

### 36.1. Mixed Persian/English Bibliography

A bibliography containing both Persian and English entries (risk: 9/10 per §15) creates complex bidi situations at the run level — each reference line may switch direction mid-line. There is no clean Pandoc-native way to produce a **dual bibliography** (separate Persian and English lists). Practical approaches:

1. **Single unified bibliography** (simplest): Use a consistent CSL style and let Word's bidi handle direction per-run. Works but may have inconsistent formatting.
2. **Post-process in Word**: After conversion, manually sort entries into two sections and apply different paragraph styles.
3. **Two `.bib` files + Lua filter**: Maintain separate `references-fa.bib` and `references-en.bib`, and use a Lua filter to emit them into separate Word sections with different styles.

Regardless of approach, ensure each reference entry's **run-level direction** is correct — a Persian author name must be RTL while the English journal title must be LTR, even within the same bibliography entry.

---

## Part VII — Tables

### 37. Basic Table Syntax

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
```

([ChatGPT §17](ChatGPT-md.md))

### 38. Table Direction in RTL

When a table is inside an RTL paragraph, the **entire table** may shift direction. Column order may reverse. Numeric columns (LTR) inside RTL tables create complex bidi situations.

([ChatGPT §18](ChatGPT-md.md), [ChatGPT §71](ChatGPT-md.md))

### 39. Decimal Alignment in Numbers

For Persian decimal numbers, use Persian decimal separator (`٫`) to avoid direction problems. English decimal separator (`.`) in RTL context may break alignment.

([ChatGPT §20](ChatGPT-md.md))

### 40. Merged Cells

Table merging is weak in Markdown → DOCX conversion. Complex merged cells require specialized handling or DOCX post-processing.

([ChatGPT §17](ChatGPT-md.md), [DeepSeek Part1](deepseek-md.md))

### 41. Table Captions

Use standard Markdown or Pandoc's table caption syntax. Place the caption directly after the table.

([ChatGPT §17](ChatGPT-md.md))

### 42. Table Styling

Table styling is controlled by **reference.docx**, not Markdown.

([ChatGPT §69](ChatGPT-md.md))

---

## Part VIII — Figures & Images

### 43. Figure Insertion

```markdown
![Caption text](images/figure.png){#fig:label width=80%}
```

([ChatGPT §21](ChatGPT-md.md))

### 44. Figure Captions

Figure captions are a common point of failure. Ensure captions:
- Are properly associated with the figure
- Support cross-referencing
- Include numbering (handled by reference.docx / filter)

([DeepSeek Part1](deepseek-md.md), [Gemini considerations](Gemini-md.md))

### 45. Figure Placement

Figure placement is **Word's domain**, not Markdown's. Use `reference.docx` styles for positioning.

([ChatGPT §69](ChatGPT-md.md))

---

## Part IX — Cross-References & Numbering

### 46. Cross-References

Cross-references require a Lua filter or post-processing mechanism. Word fields (REF, SEQ) need to be inserted and then updated in Word with F9.

([ChatGPT §22](ChatGPT-md.md), [Gemini recommendations](Gemini-md.md))

### 47. Equation Numbering

Equation numbering must be implemented via a Lua filter or DOCX template mechanism. Pandoc doesn't natively auto-number equations.

([ChatGPT §22](ChatGPT-md.md))

### 48. Automatic Cross-Reference + RTL Numbering

This is a **high-risk combination (9/10)**. Test extensively — automatic references may break in RTL context.

([ChatGPT §71](ChatGPT-md.md))

---

## Part X — Document Structure

### 49. Table of Contents (TOC)

TOC is **DOCX's domain**. Pandoc generates the structure, Word renders it. Requires field update (F9) in Word after conversion.

([ChatGPT §23](ChatGPT-md.md), [Gemini recommendations](Gemini-md.md))

### 50. Page Numbers

Page numbers are a **DOCX feature**, controlled by `reference.docx`. Not a Markdown concern.

([ChatGPT §24](ChatGPT-md.md))

### 51. List of Figures / List of Tables

These are DOCX field mechanisms, not Markdown features. Implemented via `reference.docx` and Word field updates.

([ChatGPT §24](ChatGPT-md.md))

### 52. Heading Numbering

Heading numbering is controlled by **DOCX / Pandoc mechanism**, not Markdown source.

([ChatGPT §69](ChatGPT-md.md))

### 53. Heading Identifiers

Markdown headings auto-generate identifiers. Ensure no duplicate heading IDs.

([ChatGPT §66](ChatGPT-md.md))

### 54. Page Breaks

Page breaks are a DOCX feature. Can be inserted via raw DOCX XML in Markdown:
```markdown
<div style="page-break-after: always;"></div>
```

([ChatGPT §25](ChatGPT-md.md), [Gemini considerations](Gemini-md.md))

---

## Part XI — Lists

### 55. List Formatting

Lists are supported but rendering issues may occur, especially with mixed RTL/LTR content.

([DeepSeek Part1](deepseek-md.md))

### 56. Nested Lists

Nested lists require correct indentation in Markdown. Mixed content in nested lists increases bidi complexity.

([ChatGPT §26](ChatGPT-md.md))

---

## Part XII — Code & Special Content

### 57. Inline Code

Inline code uses backticks: `` `code` ``. Monospace font; no language detection.

([ChatGPT §27](ChatGPT-md.md))

### 58. Code Blocks

````
```python
def hello():
    print("Hello World")
```
````

Syntax highlighting supported in DOCX.

([ChatGPT §27](ChatGPT-md.md))

### 59. Footnotes

```markdown
Text with footnote[^1].

[^1]: Footnote content here.
```

([ChatGPT §28](ChatGPT-md.md))

### 60. Special Symbols

| Symbol | Usage |
|--------|-------|
| `°` (degree sign) | Temperature, angles |
| `×` (multiplication sign) | Not letter `x` |
| `÷` (division sign) | Not slash |
| `±` (plus-minus) | Tolerance |
| `©`, `®`, `™` | Copyright, registered, trademark |

([ChatGPT §29](ChatGPT-md.md))

---

## Part XIII — Fonts & Styling

### 61. Persian/Arabic Font Handling

This is **extremely critical**. If the wrong Unicode character enters the document (e.g., Arabic `ي` instead of Persian `ی`), Word will apply a **different font** to that character, creating ugly mixed-font text within the same word.

Fonts must be assigned at the **character level**, not just the paragraph level, to handle bidi text correctly.

([ChatGPT §31](ChatGPT-md.md), [Claude Part1](Cloude-md.md))

### 62. Font Fallback Mechanism

When Word encounters a character not supported by the current font, it tries fallback fonts. Arabic characters may fall back to an Arabic font instead of the intended Persian font, creating visual inconsistencies.

([ChatGPT §31](ChatGPT-md.md), [Gemini considerations](Gemini-md.md))

### 63. Script Rendering in Different Fonts

Each script (Arabic, Latin, CJK, etc.) has its own design rules. Mixing scripts in the same font causes visual inconsistencies. The best practice is to use **separate fonts** for each script and let the system switch automatically based on Unicode ranges.

([ChatGPT §32](ChatGPT-md.md))

### 64. reference.docx

`reference.docx` controls:
- Fonts for Persian/Arabic and Latin text
- RTL paragraph styles
- Table styling
- Page size, margins
- Header/footer
- Heading styles

([ChatGPT §33](ChatGPT-md.md), [Claude Part3](Cloude-md.md))

### 65. Font Fallback in Lua Filter

A Lua filter should use the Unicode code point to determine the character's script and apply the correct font. This is a **character-level** operation, not a word-level operation.

([ChatGPT §31](ChatGPT-md.md))

### 65.1. Line-Spacing (Leading) for Persian Fonts

Many Persian fonts (e.g., Vazirmatn, IRANSans, B Nazanin) have tall ascenders/descenders that cause vertical clipping in Word when using default single line-spacing. In your `reference.docx`, set paragraph line-spacing to **1.3–1.5×** for body text, especially for headings and table cells. Without this adjustment, characters like `ب`, `پ`, `ت` may clip into the line above, and diacritics (tashdid, zabar) may be cut off.

---

## Part XIV — Lua Filters & Processing

### 66. Filter Pipeline

Recommended filter order:
1. **RTL filter** — detect Persian/Arabic text and apply bidi attributes
2. **citeproc** — process citations and bibliography
3. **Cross-reference filter** — handle equation/figure/table numbering and references

([ChatGPT §33](ChatGPT-md.md))

### 67. RTL Filter Requirements

The RTL filter must:
- Detect Persian/Arabic characters at the **character level**
- Apply `dir="rtl"` to paragraphs containing RTL characters
- Handle mixed-direction paragraphs correctly
- Use Unicode code point analysis, not word-level analysis

([ChatGPT §31](ChatGPT-md.md), [ChatGPT §33](ChatGPT-md.md))

### 67.1. Minimal RTL Detection Lua Filter

The following is a minimal, character-level RTL detection filter for Pandoc. It inspects each paragraph's Unicode characters and sets `dir="rtl"` when RTL characters outnumber LTR characters:

```lua
-- rtl-filter.lua: set dir="rtl" on paragraphs with majority RTL characters
local RTL_RANGES = {
  {0x0600, 0x06FF},   -- Arabic
  {0x0750, 0x077F},   -- Arabic Supplement
  {0xFB50, 0xFDFF},   -- Arabic Presentation Forms-A
  {0xFE70, 0xFEFF},   -- Arabic Presentation Forms-B
  {0x0590, 0x05FF},   -- Hebrew (if needed)
}

local function is_rtl(cp)
  for _, range in ipairs(RTL_RANGES) do
    if cp >= range[1] and cp <= range[2] then return true end
  end
  return false
end

function Para(el)
  local rtl_count, ltr_count = 0, 0
  for _, inline in ipairs(el.content) do
    if inline.t == "Str" then
      for _, char in utf8.codes(inline.text) do
        if is_rtl(char) then rtl_count = rtl_count + 1
        elseif char > 0x20 then ltr_count = ltr_count + 1 end
      end
    end
  end
  if rtl_count > ltr_count then
    el.attr = pandoc.Attr("", {}, {{pandoc.Str("dir=rtl")}})
  end
  return el
end
```

This filter uses character-level Unicode range analysis (not word-level) as required by §67. For production use, extend the ranges and handle `Plain`, `Header`, `Table`, and `BulletList` blocks.

([ChatGPT §31](ChatGPT-md.md))

### 68. Raw OpenXML in Lua Filters

Lua filters can inject raw OOXML for precise styling control when Markdown attributes are insufficient.

([ChatGPT §33](ChatGPT-md.md))

---

## Part XV — Metadata & YAML

### 69. YAML Frontmatter

```yaml
---
title: "عنوان رساله"
author: "نام نویسنده"
date: 2024-01-15
bibliography: references.bib
csl: chicago-author-date.csl
dir: rtl
lang: fa
---
```

([ChatGPT §34](ChatGPT-md.md))

### 69.1. Never Use `lang: ar` for Persian

Always use `lang: fa` (Persian), **not** `lang: ar` (Arabic). They are not interchangeable. Setting `lang: ar` triggers Arabic hyphenation rules, Arabic sorting conventions, and Arabic numeral forms (٠١٢٣ instead of ۰۱۲۳) throughout the document, even if your source text contains Persian characters. This creates silent, systematic corruption of typography that is difficult to detect and fix post-conversion.

### 70. Metadata Missing

Missing or incorrect YAML metadata can cause Pandoc to fail or produce incorrect output.

([DeepSeek Part1](deepseek-md.md))

### 71. Escaping

Standard Markdown escaping: `\*`, `\_`, `\[`, etc.

([ChatGPT §34](ChatGPT-md.md))

---

## Part XVI — Automated Validation (Pre-Pandoc)

A validation script should detect **before conversion**:

### Unicode Checks
- Arabic `ي` (U+064A) instead of Persian `ی` (U+06CC)
- Arabic `ك` (U+0643) instead of Persian `ک` (U+06A9)
- Malformed Unicode
- Unexpected control characters

### Spacing Checks
- Incorrect ZWNJ usage
- Repeated spaces
- NBSP misuse
- Space before Arabic/Persian comma

### Markdown Checks
- Malformed tables
- Broken links
- Invalid headings
- Unclosed math delimiters
- Malformed citations

### Academic Structure Checks
- Duplicate heading IDs
- Missing figure/table IDs
- Citations with no bibliography entry
- Bibliography entries never cited
- References to nonexistent figures/equations

### Typography Checks
- Inconsistent Persian/Latin digits
- Inconsistent percent signs
- Inconsistent decimal separators

([ChatGPT §66](ChatGPT-md.md), [Gemini recommendations](Gemini-md.md))

---

## Part XVII — Regression Testing

### 72. Regression Test Document

Create a small Markdown file containing **every difficult construction**:

```text
فارسی ساده
English sentence
فارسی + English
فارسی + 123
فارسی + 3.14159
فارسی + (English)
فارسی + [123]
فارسی + URL
فارسی + citation
فارسی + footnote
فارسی + inline math
display math
Persian inside math
RTL table
mixed RTL/LTR table
figure
figure caption
table caption
heading
nested heading
nested list
code
code inline
long paragraph
ZWNJ
Persian punctuation
English punctuation
symbols
negative numbers
percentages
scientific notation
DOI
```

Every time you update Pandoc, `reference.docx`, Lua filters, CSL, or Word — regenerate and compare. This is **unit testing for document generation**.

([ChatGPT §67](ChatGPT-md.md))

---

## Part XVIII — Common Misconceptions

| # | Misconception | Reality |
|---|---------------|---------|
| 1 | "Pandoc understands Persian, RTL will be perfect" | False. Unicode support ≠ bidi layout. |
| 2 | "Make the entire Word document RTL" | Usually wrong. |
| 3 | "Markdown can represent everything Word can" | False. Pandoc uses an intermediate representation. |
| 4 | "If it looks right in Markdown preview, DOCX will be right" | False. Different rendering systems. |
| 5 | "I can fix formatting manually in Word after" | Maintenance nightmare for large documents. |

([ChatGPT §68](ChatGPT-md.md))

---

## Part XIX — Source-Specific Unique Insights

### From ChatGPT
- Detailed Unicode code-point-level analysis (§3, §4)
- Parentheses directionality in bidi (§9)
- NFKC normalization risks (§4)
- Embraces/brackets in RTL (§19)
- Gold standard architecture diagram (§72)
- Confidence percentages on each recommendation
- Detailed Pandoc suitability matrix (§70)

### From Claude
- Practical diagnostic methodology (Part1)
- ZWNJ precision rule: `بی‌نظیر` not `بی نظیر` (Part1)
- `\lr{}` with no spaces for English in Persian (Part1)
- Three-part structure: Diagnostics → Solutions → Ideal Setup
- Pandoc DOCX conversion limitations (Part2)
- Complete workflow checklist (Part3)

### From DeepSeek
- Invalid control characters (form feed `\x0C`) (Part1)
- File path encoding in metadata (Part1)
- Bidi algorithm limitations at boundaries (Part1)
- Practical "How to Fix" checklist (Part1)
- "Recommendations and Workflow" document (Part2)

### From Gemini
- Summary table format for quick reference
- "Ideal Mitigation Strategy" per issue
- Mitigation strategies prioritized by implementation effort
- Quick-reference summary table

---

## Appendix A — Pandoc Command Reference

### Basic Persian Thesis Conversion

```bash
pandoc thesis.md \
  --from markdown \
  --to docx \
  --reference-doc=reference.docx \
  --bibliography=references.bib \
  --csl=chicago-author-date.csl \
  --lua-filter=rtl-filter.lua \
  --lua-filter=crossref-filter.lua \
  --metadata dir=rtl \
  --metadata lang=fa \
  -o thesis.docx
```

> **For Persian/Farsi documents, always disable the `smart` extension** (`--from markdown` or `--from markdown-smart`). The `smart` extension auto-converts straight quotes to curly quotes (`"` → `"`) and hyphens to dashes (`---` → —). These conversions are tuned for English and insert wrong-direction curly quotes in Persian. Note: in pandoc, `markdown` has smart enabled by default; `markdown-smart` or simply `--from markdown` disables it.

### With LaTeX Preamble

```bash
pandoc thesis.md \
  --from markdown \
  --to docx \
  --reference-doc=reference.docx \
  --bibliography=references.bib \
  --csl=chicago-author-date.csl \
  --include-in-header=preamble.tex \
  --lua-filter=rtl-filter.lua \
  -o thesis.docx
```

([ChatGPT §13](ChatGPT-md.md), [Claude Part3](Cloude-md.md))

---

## Appendix B — Recommended "Gold Standard" Architecture

```text
                  ┌─────────────────────┐
                  │ Farsi Academic MD   │
                  │ UTF-8 + strict      │
                  │ authoring rules     │
                  └──────────┬──────────┘
                             │
                       Validator
                             │
                    ┌────────▼────────┐
                    │ Clean semantic  │
                    │ source          │
                    └────────┬────────┘
                             │
                      Pandoc parser
                             │
                             ▼
                        Pandoc AST
                             │
              ┌──────────────┼──────────────┐
              │              │              │
        Persian/RTL      Citations      Crossrefs
          filter          citeproc         filter
              │              │              │
              └──────────────┼──────────────┘
                             │
                             ▼
                       DOCX writer
                             │
                   ┌─────────▼─────────┐
                   │ reference.docx   │
                   │ academic Persian  │
                   │ styles + RTL      │
                   └─────────┬─────────┘
                             │
                             ▼
                         DOCX file
                             │
                       Word refresh
                             │
                             ▼
                    Visual + structural
                         validation
```

([ChatGPT §72](ChatGPT-md.md))

---

## Appendix C — Formal "Farsi Academic Markdown Specification" Checklist

Before writing the thesis, define a formal specification covering:

- [ ] Exact Unicode policy
- [ ] Persian vs English digits
- [ ] Decimal numbers
- [ ] ZWNJ rules
- [ ] Punctuation rules
- [ ] Parentheses/brackets in bidi
- [ ] Inline English handling
- [ ] English paragraphs
- [ ] Equations
- [ ] Equation numbering
- [ ] Citations
- [ ] Bibliography
- [ ] Tables
- [ ] Table captions
- [ ] Figures
- [ ] Figure captions
- [ ] Cross-references
- [ ] Headings
- [ ] Heading numbering
- [ ] TOC
- [ ] List of figures/tables
- [ ] Footnotes
- [ ] URLs/DOIs
- [ ] Code
- [ ] Page breaks
- [ ] RTL/LTR rules
- [ ] `reference.docx` style architecture
- [ ] Pandoc command
- [ ] Lua filters
- [ ] Validation tests

([ChatGPT §72](ChatGPT-md.md))

---

## Part XXI — Recommended Alternative: XeLaTeX + xepersian

For academic Persian theses with complex math and heavy cross-referencing, a more robust pipeline than MD→DOCX is:

```text
MD → XeLaTeX (with xepersian/bidi packages) → PDF
```

XeLaTeX handles RTL paragraphs, Persian digits, ZWNJ, and equation numbering substantially better than Word's OMML. Word's OMML (Office Math) cannot handle Persian RTL math as gracefully as XeTeX. Converting MD → LaTeX → PDF is near-lossless for math, citations, and BiDi.

**If a DOCX is a mandatory deliverable**, use one of these strategies:
1. Generate the PDF as the "gold standard" reference, and perform a separate, simpler DOCX conversion for text-only sections.
2. Convert the PDF to DOCX (accepting minor layout shifts) rather than fighting OMML RTL bugs.
3. Use the PDF for the final submission and the DOCX only for committee review.

**Pandoc command for this path:**
```bash
# Direct single-command PDF build:
pandoc thesis.md -o thesis.pdf --pdf-engine=xelatex --metadata lang=fa

# Or two-step (LaTeX → PDF for more control):
pandoc thesis.md -o thesis.tex --to latex
xelatex thesis.tex
```

> **When to prefer XeLaTeX over DOCX:** The thesis has >50 equations, heavy citation networks, or requires pixel-perfect Persian typography. The DOCX path is better when the thesis is text-heavy with minimal math and requires frequent Word-based collaboration.

([Claude Part3 final paragraph](Cloude-md.md))

---

*This document consolidates analysis from 4 AI sources into a single source of truth for Persian academic Markdown-to-DOCX conversion.*
