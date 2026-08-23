Yes. For a **Persian/Farsi academic Markdown → DOCX workflow**, the difficult part is not Markdown itself. The real problem is the interaction between:

1. **Markdown's limited document model**
2. **Pandoc's intermediate AST**
3. **Word/DOCX's bidirectional-text and layout model**
4. **Farsi typography**
5. **LaTeX math**
6. **citation/reference processing**
7. **automatic numbering/cross-references**
8. **tables and mixed RTL/LTR content**
9. **Word styles and page-layout requirements**

Pandoc is structurally very good at this workflow, but it is **not a lossless Farsi typesetting system**. Pandoc explicitly notes that its intermediate representation cannot represent every feature of richer document formats. ([Pandoc][1])

Below is the comprehensive risk map I would use before designing the Markdown format.

---

# 1. The most important principle

**Do not treat the `.md` file as a visually formatted document.**

Treat it as a **semantic source document** from which DOCX is generated.

That means your Markdown should primarily encode:

* headings
* paragraphs
* emphasis
* lists
* equations
* tables
* figures
* captions
* citations
* cross-references
* metadata
* identifiers

while the DOCX `reference.docx` controls:

* Persian font
* English font
* paragraph direction
* heading appearance
* margins
* line spacing
* indentation
* page size
* headers/footers
* page numbering
* table style
* caption style
* TOC appearance

Pandoc explicitly recommends using a customized `reference.docx` for DOCX production. ([Pandoc][2])

**Confidence: 98%**

---

# 2. Overall risk map

| Area                                |          Risk | Typical severity |
| ----------------------------------- | ------------: | ---------------- |
| UTF-8 / Unicode                     |        Medium | High             |
| Farsi RTL paragraphs                |          High | Critical         |
| Mixed Persian/English               | **Very high** | **Critical**     |
| Numbers inside Persian              | **Very high** | **Critical**     |
| Parentheses/brackets                | **Very high** | **Critical**     |
| Mathematical expressions            |          High | High             |
| LaTeX equations                     |   Medium–High | High             |
| Citation direction                  | **Very high** | High             |
| Bibliography                        | **Very high** | High             |
| Tables                              | **Very high** | Critical         |
| Table cell RTL/LTR                  | **Very high** | Critical         |
| Figures/captions                    |   Medium–High | High             |
| Cross-references                    |          High | High             |
| TOC                                 |   Medium–High | High             |
| List of figures                     |          High | High             |
| Page numbers                        |        Medium | Medium           |
| Heading numbering                   |   Medium–High | High             |
| Farsi spacing                       | **Very high** | High             |
| ZWNJ                                | **Very high** | High             |
| Arabic vs Persian Unicode           | **Very high** | Critical         |
| Arabic numerals vs Persian numerals |          High | High             |
| Fonts                               |          High | Critical         |
| Word compatibility                  |   Medium–High | High             |
| Manual formatting                   | **Very high** | Critical         |
| Raw OpenXML                         |          High | Very high        |
| Post-conversion editing             |          High | High             |

These risks are not independent. **RTL + mixed LTR + numbers + punctuation + math + citations** is the combination that produces the nastiest failures.

---

# 3. Problems originating in the Markdown source

## 3.1 Markdown has no native concept of "Persian paragraph"

This is fundamental.

Markdown knows that something is a paragraph, but ordinary Markdown does not inherently mean:

> "This paragraph is a Persian RTL paragraph using font X, with Persian punctuation and Persian numerals."

Pandoc does have `dir` attributes and supports RTL/LTR overrides through native spans/divs. ([Pandoc][3])

For example, conceptually:

```markdown
::: {dir=rtl}
این یک پاراگراف فارسی است.
:::
```

But you don't necessarily want to manually wrap **every paragraph** this way.

A better architecture is usually:

**Document-level RTL default + explicit LTR exceptions.**

**Risk: 9/10**

---

# 4. Unicode problems

This is one of the biggest hidden sources of errors.

Persian text can contain visually identical but technically different characters.

For example:

```text
ی
ي
```

and:

```text
ک
ك
```

The first pair is Persian `ی` vs Arabic `ي`.

The second is Persian `ک` vs Arabic `ك`.

They look similar but are different Unicode code points.

You can therefore have:

```text
می‌روم
```

versus text with incorrectly encoded characters.

### Recommended normalization

Your source should establish a Unicode policy:

* UTF-8
* Persian `ی` U+06CC
* Persian `ک` U+06A9
* Persian digits if required
* Arabic/Persian punctuation consistently
* ZWNJ U+200C where required
* no accidental Arabic presentation forms
* no unnecessary invisible characters

**Risk: 10/10**

---

# 5. ZWNJ / نیم‌فاصله

This deserves its own category.

Examples:

```text
می‌روم
خانه‌ها
داده‌های
به‌کارگیری
```

versus:

```text
می روم
خانه ها
داده های
به کارگیری
```

These are not merely visual differences.

A Markdown processing pipeline can accidentally:

* remove ZWNJ
* normalize it incorrectly
* break search
* break spellchecking
* alter line breaking
* interact unexpectedly with Word's font/rendering
* produce visually different output

You should therefore define ZWNJ as part of the **source-text specification**, rather than attempting to repair it after DOCX generation.

**Risk: 9/10**

---

# 6. Farsi punctuation

Persian academic text can contain:

```text
، ؛ ؟
```

rather than:

```text
, ; ?
```

But mixed-language sentences may legitimately contain English punctuation.

For example:

```text
روش پیشنهادی (Proposed Method) در شکل (3) نشان داده شده است.
```

The punctuation's visual position is determined by the Unicode bidirectional algorithm, not simply by the order in the Markdown source.

This is why:

```text
(3)
```

can sometimes visually appear in an unexpected location inside RTL text.

**Risk: 10/10**

---

# 7. Parentheses are particularly dangerous

Consider:

```text
روش پیشنهادی (CNN) در شکل (3) ارائه شده است.
```

The source order is straightforward.

The visual order is determined by bidi processing.

Problems become worse with:

```text
روش پیشنهادی (CNN-v2.1) در سال 2025 ارائه شد.
```

and even worse:

```text
مدل (ResNet-50، 2025) در شکل (3-b) ...
```

because now you have:

* RTL text
* LTR Latin
* hyphen
* digits
* punctuation
* parentheses

all inside one logical sentence.

**Risk: 10/10**

---

# 8. Mixed Persian + English is the central RTL problem

This:

```text
این روش با استفاده از Transformer architecture در Python 3.12 پیاده‌سازی شد.
```

is much more complicated than a purely Persian paragraph.

The document contains:

```text
RTL Persian
+
LTR English
+
LTR code
+
numbers
+
punctuation
```

The correct approach is **not** to reverse strings manually.

Never do things such as:

```text
نوشتن متن انگلیسی به صورت برعکس
```

or manually reorder numbers.

You want logically ordered Unicode text and let the bidi engine handle presentation.

Pandoc itself supports language and direction metadata, including `lang` and `dir` attributes and local overrides. ([Pandoc][3])

**Risk: 10/10**

---

# 9. Numbers

You need to decide whether your academic document uses:

### Persian digits

```text
۱۲۳۴۵۶۷۸۹۰
```

or:

### Latin digits

```text
1234567890
```

or a mixed policy.

For example:

```text
در سال 2025، مدل 3.14 با دقت 97.5٪ عمل کرد.
```

The source is logically clear but the rendering is bidi-sensitive.

### Decimal numbers

These are especially problematic:

```text
3.14159
0.95
-0.25
1,234.56
```

inside RTL paragraphs.

The decimal separator, minus sign, commas and surrounding parentheses can create surprising visual arrangements.

**Recommendation:** keep numeric tokens internally consistent and do not attempt to "fix" their visual direction by reversing characters.

**Risk: 9.5/10**

---

# 10. Percentages

These are a classic mixed-direction case:

```text
95%
```

versus:

```text
۹۵٪
```

and:

```text
دقت مدل برابر با 95.3% است.
```

The percent sign can interact with bidi ordering.

If your university requires Persian digits and Persian percent signs, define this globally.

**Risk: 8/10**

---

# 11. Minus sign vs hyphen

Do not casually use these interchangeably:

```text
-
−
–
—
```

They mean different things:

| Character | Typical meaning                 |
| --------- | ------------------------------- |
| `-`       | hyphen/minus in simple contexts |
| `−`       | mathematical minus              |
| `–`       | en dash                         |
| `—`       | em dash                         |

For academic equations, especially:

```text
x − y
```

you should use actual mathematical notation rather than relying on ASCII hyphens.

**Risk: 7/10**

---

# 12. LaTeX mathematics

Pandoc has strong support for LaTeX mathematics and can convert mathematical expressions to native Word equation objects in DOCX. ([Pandoc][4])

So this is one of the **stronger parts of the pipeline**.

For example:

```markdown
The loss function is

$$
L(\theta)=\frac{1}{N}\sum_{i=1}^{N}(y_i-\hat{y}_i)^2
$$
```

can work well.

But there are important limitations.

---

# 13. LaTeX macros

Simple LaTeX:

```latex
\frac
\sum
\alpha
\mathbf
```

usually has a good chance of conversion.

Custom macros such as:

```latex
\newcommand{\R}{\mathbb{R}}
```

require more care.

Pandoc has a `latex_macros` extension that can parse macro definitions and apply them to mathematics and raw LaTeX. ([Pandoc][5])

But not every arbitrary LaTeX package command has an equivalent in Word's equation model.

For example, a complicated LaTeX construction involving package-specific commands may not translate faithfully.

**Risk: 7/10 for ordinary math; 9/10 for advanced/custom LaTeX.**

---

# 14. Mathematical RTL is substantially harder

This is an important distinction:

### Ordinary Persian text containing an equation

```text
تابع هزینه به صورت زیر تعریف می‌شود:

$$
L(\theta)=...
$$
```

is relatively manageable.

### Persian inside mathematics

```latex
f(x)=\text{تابع هزینه}
```

is much more problematic.

### Persian variable descriptions mixed into equations

```latex
x_{\text{ورودی}}
```

can also create font/direction issues.

**Recommendation:**

Keep mathematical notation mathematically neutral whenever possible:

```latex
x_{\mathrm{input}}
```

and explain it in surrounding Persian text.

**Risk: 9/10**

---

# 15. Inline equations

This:

```markdown
مقدار $x_i$ برای هر نمونه محاسبه می‌شود.
```

is usually fine.

But combinations such as:

```markdown
مقدار $x_{i+1}$ در رابطه (3-2) محاسبه می‌شود.
```

combine:

* Persian
* inline math
* subscripts
* numbers
* parentheses
* hyphens

This is exactly the type of expression that should be part of your conversion test suite.

**Risk: 8/10**

---

# 16. Citations

Pandoc's citation architecture is actually strong.

You can use citation syntax such as:

```markdown
[@smith2024]
```

and process it with `--citeproc`.

Pandoc supports bibliography data in BibTeX, BibLaTeX, CSL JSON and CSL YAML, and CSL controls the citation style. ([Pandoc][4])

The danger is **not primarily Pandoc's citation engine**.

The danger is:

> citation rendering + Persian RTL + punctuation + numerical citation styles.

---

# 17. Author-date citations

Example:

```text
(محمدی، ۱۴۰۲)
```

or:

```text
(Mohammadi, 2023)
```

or:

```text
(محمدی و احمدی، ۱۴۰۲)
```

These require careful bidi handling.

Especially:

```text
(Mohammadi & Ahmadi, 2023)
```

inside Persian text.

**Risk: 9/10**

---

# 18. Numeric citations

IEEE-like citations:

```text
[1]
[2, 5]
[3–7]
```

inside RTL text can be surprisingly problematic.

For example:

```text
مطابق مطالعات پیشین [3–7]، ...
```

The brackets and numeric sequence are bidi-sensitive.

**Risk: 9/10**

---

# 19. Bibliography

The bibliography is another major issue.

A Persian bibliography may contain:

```text
محمدی، علی. (۱۴۰۲). عنوان مقاله...
```

followed by English references:

```text
Smith, J. (2024). Title of article...
```

This creates mixed:

* RTL bibliography entries
* LTR bibliography entries
* DOI
* URLs
* volume/issue
* page ranges
* punctuation
* author names
* Latin abbreviations

A single global RTL setting is therefore **not necessarily correct for the bibliography**.

**Risk: 9/10**

---

# 20. DOI and URLs

Examples:

```text
https://doi.org/10.1016/j.example.2025.123456
```

inside Persian text are LTR.

Do not manually reverse them.

URLs are particularly dangerous when placed next to:

```text
)
،
؛
.
```

because bidi rendering can make punctuation appear visually misplaced.

**Risk: 9/10**

---

# 21. Tables are one of the highest-risk components

Simple Markdown tables:

```markdown
| متغیر | مقدار | واحد |
| ----- | ----: | ---- |
| دما   |  25.4 | °C   |
| دقت   |  97.5 | %    |
```

are structurally supported.

But academic tables can require:

* RTL table direction
* RTL header
* LTR numerical columns
* decimal alignment
* merged cells
* multi-row headers
* footnotes
* captions
* table numbering
* cell-specific alignment
* Persian/English mixed cells

Markdown's table model is much less expressive than Word tables.

Pandoc itself warns that complex tables may not fit its simple document model. ([Pandoc][1])

**Risk: 10/10 for complex academic tables.**

---

# 22. Table direction ≠ paragraph direction

This distinction is often missed.

You can have:

```text
Table = RTL
```

but:

```text
Column 1 = Persian RTL
Column 2 = English LTR
Column 3 = numbers LTR
```

So the table needs multiple layers of direction.

A naive "make the entire document RTL" approach can therefore make numeric and English columns worse.

**Risk: 10/10**

---

# 23. Decimal alignment in tables

Academic tables often need:

```text
0.123
0.456
0.789
```

aligned on the decimal point.

Markdown doesn't provide a robust semantic model for decimal-tabular alignment.

Word can do sophisticated table alignment, but Pandoc's Markdown representation doesn't necessarily preserve every Word-specific table layout requirement.

**Risk: 8/10**

---

# 24. Merged cells

Markdown generally does not naturally express:

```text
┌───────────────┐
│   Group A     │
├───────┬───────┤
│ X     │ Y     │
```

with arbitrary rowspan/colspan semantics.

You can use HTML or more specialized mechanisms, but this complicates the Pandoc pipeline.

**Recommendation:** if the academic document contains many merged/complex tables, Markdown → DOCX may be the wrong authoring representation for those tables.

**Risk: 9/10**

---

# 25. Table captions

You need to distinguish:

```text
جدول ۳-۲. نتایج آزمایش
```

from simply:

```text
| ... |
```

Pandoc can represent captions, but the final Word numbering and positioning depend heavily on the chosen workflow/reference document/filtering.

For serious academic work, I would explicitly test:

* table number
* caption direction
* caption position
* numbering hierarchy
* cross-reference
* TOC/list-of-tables behavior

**Risk: 8/10**

---

# 26. Figures

Similar issues occur with:

```markdown
![شکل معماری مدل](figures/model.png)
```

You need to control:

* image size
* alignment
* caption
* caption direction
* figure numbering
* cross-reference
* placement
* page breaks
* list of figures

Pandoc supports images well structurally, but Word layout is inherently more complicated than Markdown.

**Risk: 7/10**

---

# 27. Figure numbering

You might want:

```text
شکل ۳-۴
```

rather than:

```text
Figure 4
```

and perhaps chapter-based numbering:

```text
Figure 3-4
Table 3-2
Equation 3-7
```

This is beyond ordinary Markdown.

Pandoc's ecosystem has filters such as `pandoc-crossref` and `pandoc-xnos` for numbering/cross-referencing figures, equations, tables and sections. ([Pandoc][6])

**Risk: 8/10**

---

# 28. Equation numbering

This:

```latex
$$
E=mc^2
$$
```

is easy.

This:

```text
(3-12)
```

with automatic references:

```text
مطابق رابطه (3-12)، ...
```

is a different problem.

You need a deliberate numbering/cross-reference system.

Otherwise you end up manually maintaining numbers—which is fragile.

**Risk: 8/10**

---

# 29. Cross-references

You may need:

```text
مطابق شکل ۴-۲ ...
```

```text
مطابق جدول ۳-۱ ...
```

```text
رابطه (۲-۷) ...
```

```text
بخش ۵-۲ ...
```

The ideal source representation should use **semantic identifiers**, not hardcoded numbers.

For example conceptually:

```markdown
{#fig:architecture}
```

and references to:

```text
@fig:architecture
```

rather than writing:

```text
شکل ۳-۴
```

yourself.

This prevents numbering from becoming inconsistent when chapters are added or removed.

**Risk: 9/10**

---

# 30. Table of Contents

There are two fundamentally different things:

### A. TOC generated by Pandoc

```bash
--toc
```

### B. Word's dynamic TOC field

The second is generally preferable for a final academic DOCX because Word can update it.

But it introduces a crucial issue:

> The TOC may not contain final page numbers until Word updates fields.

Pandoc's cross-reference documentation also notes that some numbering/cross-reference results become visible only after fields are refreshed in the final document. ([Pandoc][3])

**Risk: 7/10**

---

# 31. Page numbers

Markdown has essentially no concept of:

```text
Page 37
```

because pages don't exist until layout occurs.

Page numbering belongs to DOCX.

Therefore:

**Never put page numbers into Markdown content.**

Use Word headers/footers through the reference document/template.

**Risk: 3/10 if designed correctly; 9/10 if attempted in Markdown.**

---

# 32. List of Figures

Same principle as TOC.

A Markdown source can identify figures semantically.

The actual:

```text
فهرست شکل‌ها
```

should ideally be generated in the DOCX layer.

Otherwise you are duplicating information manually.

**Risk: 8/10**

---

# 33. List of Tables

Same issue.

You want:

```text
فهرست جداول
```

generated from actual table captions, not manually typed.

**Risk: 8/10**

---

# 34. Heading numbering

You should avoid writing:

```markdown
## 3.2 روش پیشنهادی
```

if the number is supposed to be automatic.

Prefer:

```markdown
## روش پیشنهادی
```

and let the numbering system generate:

```text
۳-۲ روش پیشنهادی
```

or whatever the university requires.

Otherwise adding one section forces manual renumbering.

**Risk: 8/10**

---

# 35. Markdown heading identifiers

For Persian headings:

```markdown
## روش پیشنهادی
```

automatic identifiers can become undesirable or unstable depending on the parser/settings.

For academic cross-referencing, explicit IDs are safer:

```markdown
## روش پیشنهادی {#sec:method}
```

Then reference the semantic ID.

**Risk: 7/10**

---

# 36. Lists

Persian numbered lists can create problems:

```markdown
1. مورد اول
2. مورد دوم
3. مورد سوم
```

Word may display the numbering according to its own locale/style settings.

The actual list number is not necessarily simply a Persian Unicode character stored in Markdown.

You should distinguish:

* semantic list numbering
* displayed numeral style
* paragraph direction
* indentation

**Risk: 7/10**

---

# 37. Nested lists

Mixed RTL/LTR nested lists are worse:

```text
۱. روش‌های پیشنهادی
   a. CNN
   b. Transformer
```

The indentation and numbering direction may not look as expected.

**Risk: 8/10**

---

# 38. Footnotes

Footnotes can contain:

* Persian
* English
* URLs
* citations
* equations

which creates another bidi context.

Pandoc supports footnotes structurally, but the Word rendering depends on Word's footnote behavior and styles.

**Risk: 7/10**

---

# 39. Inline code

Example:

```markdown
در Python از تابع `train_model()` استفاده شد.
```

This is a mixed-direction situation.

The code itself should remain LTR.

You therefore want something like:

```text
RTL paragraph
    LTR code span
RTL continuation
```

rather than attempting to make the entire paragraph LTR.

**Risk: 8/10**

---

# 40. Code blocks

Code blocks should be LTR:

```python
model.fit(X_train, y_train)
```

A global RTL document style can accidentally produce ugly code presentation if not explicitly styled.

Your reference DOCX should therefore have a dedicated `Source Code` style. Pandoc's reference document supports a Source Code paragraph style. ([Pandoc][2])

**Risk: 7/10**

---

# 41. Special symbols

Academic documents may contain:

```text
±
≤
≥
≈
≠
→
←
↔
×
÷
∈
∑
√
∞
α β γ
μ σ
°
℃
Ω
```

The main problem isn't necessarily Pandoc.

It is:

* font support
* Unicode normalization
* bidi behavior
* equation-vs-text semantics
* Word rendering

Some symbols should be represented as mathematical notation rather than ordinary Unicode text.

**Risk: 6/10**

---

# 42. Degree symbols and units

For example:

```text
25 °C
```

versus:

```text
25°C
```

and:

```text
25 درجه سانتی‌گراد
```

Academic formatting may require a specific convention.

Markdown cannot enforce all of this.

A style/filter layer may be needed if consistency is critical.

**Risk: 6/10**

---

# 43. Font problems

This is a **major DOCX issue**.

You might have:

* Persian body font
* English body font
* mathematical font
* Latin symbols
* Arabic/Persian glyphs
* code font

A single font setting does not necessarily solve everything.

For example:

```text
فارسی English 123 α β
```

may involve several font fallback decisions.

Your `reference.docx` should define the appropriate fonts for:

* Normal
* Body Text
* Heading 1–9
* Caption
* Table Caption
* Figure
* Source Code
* Footnote Text
* mathematical content

Pandoc's reference DOCX mechanism is explicitly intended for this kind of style customization. ([Pandoc][2])

**Risk: 10/10**

---

# 44. Word font fallback

Even if the DOCX specifies a Persian font, Word may use fallback fonts for characters that aren't contained in that font.

This can create:

* visually different glyphs
* different character widths
* different line breaks
* different pagination

which can then change the page numbers in the TOC.

This is why **pagination should only be validated on the target Word environment**.

**Risk: 8/10**

---

# 45. Line spacing

Persian academic documents often have strict requirements:

```text
1.15
1.5
double
exactly 18 pt
```

Markdown doesn't encode this.

It belongs in the Word styles.

**Risk: 2/10 if reference.docx is properly designed.**

---

# 46. Paragraph indentation

Same issue.

Requirements such as:

```text
first-line indent = 0.5 cm
```

should be a Word style property, not manually encoded in Markdown.

**Risk: 2/10 with a proper reference document.**

---

# 47. Page margins

Same.

Use:

* A4
* margins
* gutter
* header distance
* footer distance

in the reference DOCX.

Do not attempt to encode these in Markdown.

Pandoc's documentation explicitly describes the reference DOCX as controlling margins, page size, headers and footers. ([Pandoc][2])

---

# 48. RTL does not mean everything should be RTL

This is perhaps the most important correction to a common design assumption.

You do **not** want:

> "Make the entire DOCX RTL."

You want:

```text
Document base direction: RTL

Persian paragraph: RTL
English paragraph: LTR
Code block: LTR
Equation: mathematical/LTR-like
English citation: context-sensitive
URL: LTR
English table column: LTR
Numeric column: controlled
Persian table column: RTL
```

RTL is **hierarchical and contextual**, not a single global switch.

**Confidence: 99%.**

---

# 49. Markdown's whitespace

Markdown itself is sensitive to:

* blank lines
* indentation
* list indentation
* code-block indentation
* fence placement

For Persian prose, people sometimes insert spaces for visual formatting.

That is dangerous.

Do not use spaces to simulate:

* indentation
* alignment
* tables
* centering
* RTL positioning

Use semantic Markdown structures.

**Risk: 7/10**

---

# 50. Multiple spaces

Markdown generally collapses or interprets whitespace structurally.

Therefore:

```text
کلمه        کلمه
```

should not be used for layout.

Use tables, styles, or actual document structures.

**Risk: 5/10**

---

# 51. Non-breaking spaces

Academic Persian sometimes needs controlled spacing:

```text
۲۰۲۶
```

or between numerical/value components.

But NBSP and ZWNJ have different purposes.

Do not indiscriminately replace ordinary spaces with non-breaking spaces.

It can affect:

* wrapping
* justification
* line breaks
* Word behavior

**Risk: 7/10**

---

# 52. Markdown escaping

Characters such as:

```text
*
_
[
]
(
)
#
+
-
.
```

have Markdown meaning.

This can be especially annoying in mathematical or technical text.

For example:

```markdown
(3-2)
```

is harmless, but:

```markdown
-0.25
```

at the beginning of a line can potentially be interpreted as a list.

Likewise:

```markdown
[ABC]
```

may become part of link syntax depending on context.

**Risk: 6/10**

---

# 53. YAML metadata

A serious academic Markdown document may start with:

```yaml
---
title: ...
author: ...
lang: fa
dir: rtl
bibliography: references.bib
csl: ...
---
```

This is useful, but YAML itself has syntax rules.

Persian strings containing:

```text
:
#
-
"
'
```

can cause metadata parsing problems if not quoted correctly.

**Risk: 5/10**

---

# 54. Metadata language

You should explicitly establish:

```yaml
lang: fa
dir: rtl
```

rather than relying entirely on automatic detection.

Pandoc documents both `lang` and `dir` metadata and supports local language/direction overrides. ([Pandoc][3])

**Risk: 8/10 if omitted; 2/10 if correctly configured.**

---

# 55. Persian vs Arabic language tags

There is an important distinction between:

```text
fa
```

and:

```text
ar
```

They are not interchangeable.

For Persian academic documents, the base language should normally be Persian:

```yaml
lang: fa
```

while English segments can be explicitly marked:

```text
lang=en
```

where useful.

**Risk: 6/10**

---

# 56. Raw OpenXML

Pandoc supports raw OpenXML, which can be inserted into Markdown for DOCX-specific features. ([Pandoc][7])

For example, a raw OpenXML block can insert a page break.

This is powerful but dangerous.

You are then coupling your Markdown source to:

```text
Markdown → Pandoc → DOCX/OpenXML
```

instead of maintaining a format-independent source.

Use raw OpenXML only for things that genuinely cannot be expressed through:

* Markdown
* metadata
* reference.docx
* filters

**Risk: 9/10 if heavily used.**

---

# 57. Reference.docx is critical

For your particular project, I would consider the `reference.docx` almost as important as the Markdown specification.

You should create a dedicated academic Persian reference document containing styles such as:

```text
Normal
Body Text
Title
Subtitle
Heading 1
Heading 2
Heading 3
...
Caption
Table Caption
Figure
Source Code
Footnote Text
Bibliography
TOC Heading
```

These are among the styles Pandoc expects/uses in its reference DOCX architecture. ([Pandoc][2])

**Confidence: 99%.**

---

# 58. Reference.docx should establish RTL styles

For example:

| Style        | Direction  | Font          | Purpose        |
| ------------ | ---------- | ------------- | -------------- |
| Normal       | RTL        | Persian font  | normal Persian |
| Body Text    | RTL        | Persian font  | body           |
| Heading 1    | RTL        | Persian font  | chapter        |
| Heading 2    | RTL        | Persian font  | section        |
| Caption      | RTL        | Persian font  | captions       |
| Bibliography | controlled | Persian/Latin | references     |
| Source Code  | LTR        | monospace     | code           |
| Table        | controlled | mixed         | tables         |

But the exact styles depend on your university's requirements.

---

# 59. A major architectural recommendation

I would **not** build the workflow as:

```text
Farsi Markdown
       ↓
Pandoc
       ↓
DOCX
       ↓
manually fix everything in Word
```

That will become painful very quickly.

Instead:

```text
                    ┌───────────────┐
                    │ Academic MD   │
                    │ semantic      │
                    │ source        │
                    └───────┬───────┘
                            │
                     Pandoc parsing
                            │
                            ▼
                     Pandoc AST
                            │
              ┌─────────────┼──────────────┐
              │             │              │
          Lua filters    citeproc      crossref
              │             │              │
              └─────────────┼──────────────┘
                            ▼
                    DOCX writer
                            │
                            ▼
                    reference.docx
                            │
                            ▼
                     final DOCX
                            │
                            ▼
                  Word field refresh
                            │
                            ▼
                     QA / validation
```

This is much more robust.

---

# 60. Filters are probably necessary

For your requirements, I would seriously consider a Lua-filter layer.

Possible responsibilities:

* normalize Persian characters
* enforce language attributes
* add direction attributes
* handle special classes
* manipulate captions
* normalize tables
* control specific mixed-direction spans
* implement custom academic conventions
* prepare cross-references

Pandoc explicitly supports filters and Lua filters as part of its customization architecture. ([Pandoc][8])

**Confidence: 90%**

---

# 61. Do not put typography rules into the prose

Bad:

```markdown
<div align="right">
...
</div>
```

everywhere.

Bad:

```markdown
&nbsp;
```

for spacing.

Bad:

```text
                    متن
```

for centering.

Bad:

```markdown
#### 3-2 روش پیشنهادی
```

when numbering should be automatic.

Good:

```markdown
## روش پیشنهادی {#sec:method}
```

and let the document-generation layer determine:

* numbering
* direction
* spacing
* font
* layout

---

# 62. Recommended Markdown conventions

For a project like yours, I would establish a formal **Farsi Academic Markdown Profile**.

Something like:

```yaml
---
title: "..."
author: "..."
lang: fa
dir: rtl
bibliography: references.bib
csl: university.csl
---
```

Then define rules such as:

### Rule 1

All source files are UTF-8.

### Rule 2

Persian `ی` and `ک` are mandatory.

### Rule 3

ZWNJ is U+200C.

### Rule 4

No manual heading numbers.

### Rule 5

No manual figure/table numbers.

### Rule 6

No page numbers in Markdown.

### Rule 7

No visual spacing with repeated spaces.

### Rule 8

Equations are LaTeX math.

### Rule 9

Citations use Pandoc citation syntax.

### Rule 10

Cross-references use identifiers.

### Rule 11

English/code/URLs receive LTR treatment where necessary.

### Rule 12

Complex tables follow a defined convention.

### Rule 13

All typography is controlled by `reference.docx`.

---

# 63. What I would NOT put into Markdown

I would avoid putting these into the source unless absolutely necessary:

* page numbers
* page breaks
* Word-specific indentation
* Word-specific fonts
* manual table numbering
* manual figure numbering
* manual heading numbering
* manual TOC
* manual list of figures
* manual list of tables
* repeated spaces
* manually reversed RTL strings
* HTML formatting everywhere
* raw OpenXML everywhere

---

# 64. What I WOULD put into Markdown

I would encode:

* semantic headings
* paragraphs
* lists
* equations
* images
* captions
* citations
* references
* cross-reference IDs
* tables
* footnotes
* emphasis
* code
* metadata
* language/direction where semantically necessary

---

# 65. The conversion pipeline I recommend

For a serious thesis/dissertation:

```text
01_source/
    thesis.md
    references.bib
    figures/
    data/

02_config/
    reference.docx
    university.csl
    filters/
        normalize-persian.lua
        rtl.lua
        crossref.lua

03_build/
    ...

04_output/
    thesis.docx

05_validation/
    ...
```

Then:

```text
Markdown
   ↓
validation
   ↓
Unicode normalization
   ↓
Pandoc
   ↓
Lua filters
   ↓
citeproc
   ↓
cross-reference processing
   ↓
DOCX
   ↓
Word field update
   ↓
visual QA
```

---

# 66. Automated validation should happen BEFORE Pandoc

This is extremely valuable.

A validation script should detect:

### Unicode

* Arabic `ي`
* Arabic `ك`
* malformed Unicode
* unexpected control characters

### Spacing

* incorrect ZWNJ
* repeated spaces
* NBSP misuse

### Markdown

* malformed tables
* broken links
* invalid headings
* unclosed math delimiters
* malformed citations

### Academic structure

* duplicate heading IDs
* missing figure IDs
* missing table IDs
* citations with no bibliography entry
* bibliography entries never cited
* references to nonexistent figures
* references to nonexistent equations

### Typography

* inconsistent Persian/Latin digits
* inconsistent percent signs
* inconsistent decimal separators

This catches problems **before Word enters the picture**.

**Confidence: 97%.**

---

# 67. You need a regression test document

This is perhaps the single most useful practical recommendation.

Create a small Markdown file containing every difficult construction:

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

Then every time you update:

* Pandoc
* reference.docx
* Lua filters
* CSL
* Word

you regenerate the document and compare it.

This is essentially **unit testing for document generation**.

**Confidence: 99%.**

---

# 68. The biggest misconceptions to avoid

### Misconception 1

> "If Pandoc understands Persian, RTL will automatically be perfect."

**False.**

Persian Unicode support and complex bidi layout are different problems.

**Confidence: 99%.**

### Misconception 2

> "Make the entire Word document RTL."

Usually wrong.

**Confidence: 99%.**

### Misconception 3

> "Markdown can represent everything Word can."

False.

Pandoc deliberately uses an intermediate representation that cannot represent every feature of richer formats. ([Pandoc][1])

**Confidence: 99%.**

### Misconception 4

> "If the text looks right in Markdown preview, DOCX will look right."

False.

Markdown preview and Word use different layout/rendering systems.

**Confidence: 99%.**

### Misconception 5

> "I can fix formatting manually in Word after conversion."

For a large thesis, this becomes a maintenance nightmare.

**Confidence: 95%.**

---

# 69. The hierarchy of what should control what

I recommend this division:

| Requirement           | Best layer                 |
| --------------------- | -------------------------- |
| Persian spelling      | Source/validator           |
| Unicode normalization | Validator/filter           |
| ZWNJ                  | Source/validator           |
| Citations             | Pandoc + CSL               |
| Bibliography          | BibTeX/CSL                 |
| Equations             | Markdown LaTeX             |
| Cross-references      | Pandoc/filter              |
| Heading numbering     | DOCX/Pandoc mechanism      |
| Fonts                 | reference.docx             |
| RTL paragraph style   | reference.docx/filter      |
| LTR exceptions        | Markdown attributes/filter |
| Table styling         | reference.docx             |
| Page size             | reference.docx             |
| Margins               | reference.docx             |
| Header/footer         | reference.docx             |
| Page numbers          | DOCX                       |
| TOC                   | DOCX/Pandoc + field update |
| List of figures       | DOCX/field mechanism       |
| List of tables        | DOCX/field mechanism       |
| Complex table merging | specialized handling       |
| Page breaks           | DOCX/filter                |
| Final pagination      | Word                       |

---

# 70. My assessment of Pandoc for your use case

| Component                           | Assessment                         |
| ----------------------------------- | ---------------------------------- |
| Persian plain text                  | **Excellent**                      |
| UTF-8                               | **Excellent**                      |
| Markdown structure                  | **Excellent**                      |
| LaTeX equations                     | **Very good**                      |
| Citations                           | **Excellent**                      |
| BibTeX                              | **Excellent**                      |
| CSL                                 | **Excellent**                      |
| Basic tables                        | **Good**                           |
| Complex tables                      | **Weak–moderate**                  |
| Figures                             | **Good**                           |
| Cross references                    | **Good with appropriate tooling**  |
| RTL paragraphs                      | **Good but needs design/testing**  |
| Mixed RTL/LTR                       | **Risky**                          |
| Persian typography                  | **Needs custom policy**            |
| Word academic formatting            | **Very good with reference.docx**  |
| Automatic page-level layout         | **Word's domain, not Markdown's**  |
| Highly customized university thesis | **Good, but requires engineering** |

**Overall suitability: ~88%** for a carefully engineered Persian academic workflow.

A naive:

```text
thesis.md → pandoc → thesis.docx
```

workflow is closer to **55–65%** suitability for a demanding thesis.

---

# 71. The most dangerous combinations

If I had to rank the failure-prone combinations:

### 1. Persian + English + numbers + parentheses

**10/10 risk**

### 2. RTL table + LTR numeric columns

**10/10**

### 3. Persian citation + punctuation + numerical citation

**9.5/10**

### 4. Persian text inside LaTeX math

**9/10**

### 5. Complex table + merged cells + captions

**9/10**

### 6. Automatic cross-reference + RTL numbering

**9/10**

### 7. Bibliography containing Persian + English + DOI/URL

**9/10**

### 8. Persian ZWNJ + Unicode normalization

**9/10**

### 9. TOC/list of figures + automatic numbering

**8/10**

### 10. Plain Persian paragraphs

**2/10**

This tells you where to spend your engineering/testing effort.

---

# 72. Recommended "gold standard" architecture

For your specific requirements, I would aim for:

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

That is the architecture I would trust for a thesis.

---

## One important next step

If this is for an actual thesis/dissertation rather than a theoretical investigation, **the next thing I would do is define a formal "Farsi Academic Markdown Specification" before writing the thesis**.

It should specify, down to individual examples:

* exact Unicode policy
* Persian vs English digits
* decimal numbers
* ZWNJ
* punctuation
* parentheses/brackets
* inline English
* English paragraphs
* equations
* equation numbering
* citations
* bibliography
* tables
* table captions
* figures
* figure captions
* cross-references
* headings
* heading numbering
* TOC
* list of figures/tables
* footnotes
* URLs/DOIs
* code
* page breaks
* RTL/LTR rules
* `reference.docx` style architecture
* Pandoc command
* Lua filters
* validation tests

That specification would turn this from a fragile "Markdown-to-Word conversion" into a **reproducible document-generation system**.

Pandoc itself is designed for this kind of extensible workflow through custom styles, metadata, citations, filters and reference documents. ([Pandoc][2])

**Confidence in this overall architecture: 96%.**

If you want, I can next produce the **actual Farsi Academic Markdown Specification**, including a concrete `.md` template, `reference.docx` style plan, Pandoc command, Lua-filter architecture, Unicode rules, and a **100+ case RTL regression-test document**.

[1]: https://pandoc.org/CONTRIBUTING.html?utm_source=chatgpt.com "Pandoc - CONTRIBUTING"
[2]: https://www.pandoc.org/demo/example2.html?utm_source=chatgpt.com "Pandoc User’s Guide"
[3]: https://pandoc.org/demo/example2.html?utm_source=chatgpt.com "Pandoc User’s Guide"
[4]: https://pandoc.org/?utm_source=chatgpt.com "Pandoc - index"
[5]: https://pandoc.org/demo/example33/8.15-latex-macros.html?utm_source=chatgpt.com "LaTeX macros"
[6]: https://pandoc.org/extras.html?utm_source=chatgpt.com "Pandoc - Pandoc Extras"
[7]: https://pandoc.org/MANUAL.pdf?utm_source=chatgpt.com "Pandoc User’s Guide"
[8]: https://pandoc.org/demo/example33/3.5-citation-rendering.html?utm_source=chatgpt.com "Citation rendering"
