# Forensic report: your actual thesis + current converter

I audited the **actual `Thesis_v9-5.md` and `Cloude_Converter_adapted.py`**, and I also executed the converter against the thesis and inspected the generated DOCX XML.

## Verdict

**Do not use the current converter to produce the final thesis.**

It is a useful prototype and several parts are good, but in its current form I would rate it:

| Area                       | Current status                          | Confidence |
| -------------------------- | --------------------------------------- | ---------: |
| Basic Markdown → DOCX      | Works                                   |        95% |
| Persian paragraph RTL      | Reasonable foundation                   |        88% |
| RTL tables                 | Good foundation, still needs visual QA  |        90% |
| Display equations          | Promising                               |        90% |
| Inline equations           | **Unsafe**                              |        99% |
| Mixed Persian/English runs | **Unsafe**                              |        99% |
| Front matter               | **Incorrect / duplicated**              |        99% |
| Images                     | **Cannot complete with supplied files** |       100% |
| TOC                        | Potentially usable                      |        85% |
| List of Tables/Figures     | **Not structurally correct**            |        95% |
| Numerical fidelity         | **Needs source-level repair first**     |        99% |
| Final thesis readiness     | **Not ready**                           |        99% |

The important point is that I found **real, specific failures**, not merely theoretical risks.

---

# 1. The biggest problem: your Markdown already contains the front matter that the converter also generates

Your YAML contains the title, author, abstract, acknowledgements, dedication, abbreviations, etc., **and the body of the same Markdown file separately contains the title pages, acknowledgements, dedication, abstract, TOC, lists, etc.** 

The converter then explicitly generates those pages again whenever YAML front matter exists, before converting the body. 

So the current architecture is effectively:

```text
YAML front matter
    ↓
generate title / abstract / TOC / etc.
    ↓
convert body
    ↓
body contains title / abstract / TOC / etc. again
```

I confirmed this in the generated DOCX: the converted file contains duplicate occurrences of the title material, TOC, abstract, etc.

### Severity

**Critical — 99%**

### Fix

We must choose exactly one source of truth:

**Recommended:** YAML controls front matter; the body begins at Chapter 1.

That means the manually duplicated title pages / abstract / TOC / lists must either be removed from the Markdown body or explicitly skipped by the converter.

---

# 2. Your current inline-math parser is a serious problem

The converter uses this regex for inline Markdown:

```python
(?P<latin>(?:[\(\[\{]\s*)?[a-zA-Z](?:[a-zA-Z0-9\.\-&:@/ _]*?[a-zA-Z0-9\)\]\}\.])?)
```

and then turns every match into a separate LTR run. 

This is far too permissive.

I tested it against actual thesis text. For example:

```text
Charbonnier
```

gets fragmented into pieces such as:

```text
(Ch)
ar
bo
nn
ie
r
```

and ordinary English prose is broken into huge numbers of tiny runs.

The generated DOCX consequently contains thousands of runs; in my test there were roughly **9,600 runs**, with **6,764 runs of length ≤2 characters**.

That is undesirable for a 150-page thesis because bidi behavior is partly determined at run boundaries.

### Severity

**Critical — 99%**

### Why it matters

A sentence like:

```text
این روش با Charbonnier et al. (2022) مقایسه شد.
```

should have a small number of semantically meaningful directional runs.

The current parser produces many artificial boundaries.

### Fix

Do **not** use a character-pattern regex to identify generic English runs.

Use Unicode bidi classification to identify logical spans, and explicitly classify:

* Persian/Arabic text
* Latin words
* numbers
* mathematical expressions
* URLs
* citations
* punctuation
* identifiers/code

The run segmentation must be semantic, not “starts with a Latin letter”.

---

# 3. I found actual malformed LaTeX in the thesis source

This is separate from the converter.

Your thesis contains expressions such as:

```text
$w*{\text{self}}$
$w*{\text{fair}}$
```

instead of:

```latex
$w_{\text{self}}$
$w_{\text{fair}}$
```

and:

```text
$C\_{i,t}$
```

instead of:

```latex
$C_{i,t}$
```

The source contains multiple examples of both forms.  

I tested what Pandoc does with these.

For example:

```latex
C\_{i,t}
```

becomes OMML representing:

```text
C _ i , t
```

rather than a proper subscript.

Likewise:

```latex
w*{\text{self}}
```

becomes essentially:

```text
w * self
```

not `w_self`.

This is extremely important because **Pandoc can successfully generate a DOCX while still representing the malformed mathematical syntax literally**.

### Severity

**Critical — 100%**

### Fix

Before conversion we need a **math-source audit and correction pass**.

I would not blindly auto-correct all LaTeX. We should detect suspicious patterns and produce a review list.

Examples that should be flagged automatically:

```text
\_{...}
\_{...}
*{...}
A*{...}
C*i
R*i
w*{\text{...}}
```

Then correct them deliberately.

---

# 4. The thesis has 234 mathematical spans

My source audit found approximately:

* **223 inline math expressions**
* **11 display equations**

The converter successfully produced OMML for the 11 tested display equations, which is encouraging.

The converter's design explicitly uses Pandoc to generate native OMML. 

That part is fundamentally the right direction.

### But

The inline path and source math syntax need to be repaired before we can call the math conversion reliable.

**Display math confidence: 90%**

**Inline math confidence in current pipeline: 60%**

---

# 5. Display-equation labels are currently just text, not real equation numbering

Your source uses:

```latex
\qquad \text{(معادله ۳-۲)}
```

The converter deliberately strips that out of the OMML and adds it back as an ordinary Word text run. 

That means:

```text
Equation body
```

and

```text
(معادله ۳-۲)
```

are separate visual objects.

This can work visually, but it is **not a real Word equation-number/reference system**.

Therefore:

* changing equation order will not renumber automatically;
* cross-references are not genuine Word cross-reference fields;
* there is no structural relationship between equation 3-2 and references to “معادله ۳-۲”.

### Severity

**High — 94%**

For a thesis under active revision, I would strongly prefer equation identifiers to be structural.

---

# 6. The generated inline OMML needs stricter structural validation

The current code inserts inline `m:oMath` into a Word run:

```python
run = paragraph.add_run()
run._r.append(copy.deepcopy(omml))
```

The generated XML therefore contains patterns like:

```xml
<w:r>
    <m:oMath>...</m:oMath>
</w:r>
```

Modern OOXML examples commonly represent inline `m:oMath` as a paragraph-level inline object alongside ordinary `w:r` elements. Microsoft documents `oMath` as an inline math zone, and examples show it occurring in the paragraph flow. ([Microsoft Learn][1])

I would therefore **not keep the current insertion method without schema/Word round-trip validation**.

### Severity

**High — 90%**

This is exactly the kind of XML detail that can behave differently between Word, LibreOffice, and validators.

---

# 7. Your table implementation is better than the math implementation

The converter correctly attempts both:

```python
table.table_direction = WD_TABLE_DIRECTION.RTL
```

and OOXML:

```xml
<w:bidiVisual w:val="1"/>
```

which is good. 

That directly addresses the table-direction problem I described in the previous report.

I tested the output and found:

* 32 tables generated from the 32 table blocks;
* RTL table metadata present.

So this part is promising.

### But there are still problems

The parser does:

```python
cells = tl.strip().strip("|").split("|")
```



That means escaped/embedded pipe characters are not supported.

For example:

```latex
\mid
```

is safe because it is two characters `\mid`, but a literal `|` inside future table content would break the table structure.

### Severity

**Medium/High — 88%**

---

# 8. Table equations will not inherit table font sizing correctly

The table code adds inline equations first and afterwards executes:

```python
for run in p.runs:
    run.font.size = Pt(12)
```



That changes Word run formatting, but OMML math has its own internal math runs/properties.

Therefore an equation inside a table may remain at a different effective math size than surrounding 12pt text.

Your thesis has formulas inside tables, e.g. the OCEAN/reward tables. 

### Severity

**Medium/High — 90%**

We should apply math formatting explicitly inside OMML rather than relying on `w:r` font size.

---

# 9. Your List of Tables / List of Figures is not a proper Word caption system

The converter creates:

```text
جدول ۳-۲: ...
شکل ۳-۴: ...
```

as ordinary text in the `Caption` style.

It then creates fields such as:

```text
TOC \h \z \c "Table"
TOC \h \z \c "Figure"
```

However, the generated DOCX contains **no `SEQ Table` / `SEQ Figure` fields**.

That means I would **not trust Word's List of Tables / List of Figures to populate correctly** after F9.

This is a structural issue, not just formatting.

### Severity

**Critical for thesis navigation — 95%**

### Fix

Use genuine Word caption structures:

```text
SEQ Table
SEQ Figure
```

or an equivalent controlled caption/bookmark system, then generate the lists from those real structural captions.

---

# 10. `&nbsp;` is actually leaking into the generated DOCX

Your Markdown contains HTML entities in the manual TOC:

```text
&nbsp;&nbsp;۲-۲-۱ ...
```

The current parser does not decode HTML entities.

The generated DOCX therefore contains literal:

```text
&nbsp;
```

text.

I confirmed this in the generated document.

### Severity

**High — 99%**

This is a direct conversion defect.

### Fix

Either:

1. remove the HTML indentation from source, or
2. decode HTML entities before Markdown parsing.

Prefer the first option for this thesis.

---

# 11. Your images are currently unavailable

The Markdown references 25 images, including:

```text
media/image1.jpeg
media/image2.wmf
../results/figures/...
```

The uploaded workspace does **not** contain those files.

The converter explicitly writes:

```text
[missing image: ...]
```

when a referenced image cannot be found. 

The generated DOCX therefore contains missing-image placeholders and **zero embedded media**.

The source itself confirms the image references.  

### Severity

**Blocking — 100%**

We cannot certify the final thesis visually without the real images.

---

# 12. WMF is especially risky

The logo:

```text
media/image2.wmf
```

is a Windows Metafile.

Even after supplying it, this is not an asset format I would want to leave to an uncontrolled Python image pipeline.

### Recommendation

Convert legacy WMF assets to a modern format such as:

* PNG for raster artwork
* SVG where Word compatibility permits
* EMF for vector Word-oriented artwork

before final assembly.

**Confidence: 95%.**

---

# 13. The current parser does not understand full Markdown; it understands a custom subset

This is not inherently bad, but it must be explicit.

The converter supports:

* headings
* emphasis
* code
* inline math
* footnotes
* images
* pipe tables
* bullets
* numbered lists
* block quotes
* horizontal rules

as shown in the parser.  

Your current thesis happens to use mostly those constructs.

However, the parser is **not a general Markdown parser**, so we should stop treating `.md` as generic Markdown and instead define a controlled thesis Markdown grammar.

That will make the conversion far safer.

---

# 14. Footnotes are not currently an issue in this particular source

I found no actual `[^...]` references/definitions in the thesis source.

The converter nevertheless has a custom OOXML footnote-injection implementation. 

So this is not currently a blocker, but it should be tested independently before claiming generic footnote support.

---

# 15. Your ZWNJ usage is extensive and must be preserved

The source contains approximately **6,777 zero-width non-joiner (`U+200C`) characters**.

That is entirely plausible for Persian typography.

The converter must **preserve them**, not normalize them away.

This is especially important because your text visibly depends on constructions such as:

```text
ریزشبکه‌ی
به‌عنوان
پایان‌نامه
می‌انگین
```

and many similar words. The source contains these throughout. 

### Severity

**Critical to Persian quality — 97%.**

---

# 16. The punctuation normalizer is dangerous

The converter says it is trying to be careful, but it performs:

```python
re.sub(r"\s+([،؛؟:.])", ...)
re.sub(r"([،؛؟:])(?!\s|$)", ...)
```



This is too broad for a technical thesis containing:

* URLs
* abbreviations
* decimal numbers
* equations
* citations
* file paths
* code
* English punctuation

The safe strategy is not "normalize every punctuation character inside an RTL paragraph".

It should operate on **typed text spans**.

### Severity

**High — 96%.**

---

# 17. Mixed Persian/English handling is not yet semantically correct

The converter uses:

```python
is_persian(text)
```

and if any Arabic-script character is present, the whole paragraph becomes RTL. 

Paragraph-level RTL is fine as a foundation.

But the actual content contains hundreds of mixed lines, for example:

```text
... MARL ...
... OCEAN ...
... Charbonnier et al. ...
... p = 0.0011 ...
... G(h) ...
```

The correct solution is:

```text
RTL paragraph
   ├── Persian run
   ├── LTR Latin run
   ├── numeric run
   ├── punctuation
   ├── math zone
   └── Persian run
```

not:

```text
RTL paragraph
   ├── 2-character Latin run
   ├── 2-character Latin run
   ├── 2-character Latin run
   ...
```

This is the core bidi issue.

---

# 18. Your source contains inconsistent numerical notation

The thesis uses Persian decimal notation such as:

```text
۹/۹
۳/۱
۰/۷
```

while equations and English sections use:

```text
1.3
0.5
0.95
```

This may be intentional academic typography, but the conversion pipeline must treat the two consistently according to the university's required style.

It must **not automatically convert `/` to `.` or vice versa**.

Your thesis has many examples of this mixed numeric representation. 

---

# 19. I found content inconsistencies that have nothing to do with DOCX

These must be fixed before conversion because otherwise I cannot guarantee a numerically accurate final document.

### A. Innovator blackout increase

Persian abstract:

> افزایش **۳/۸ درصدی** نرخ خاموشی

English abstract:

> raised blackout rates by **8.3%**

Those are different results. 

**Confidence: 100% that the source texts disagree.**

---

### B. 82.8 → 34.4 is not a 50% reduction

The Persian abstract says:

```text
۸۲/۸ → ۳۴/۴
کاهشی معادل ۵۰ درصد
```

Mathematically:

[
\frac{82.8-34.4}{82.8}=58.45%
]

So “50%” does not match those two values.

This is a **source-content error**, not a DOCX conversion problem.

**Confidence: 99%.**

---

### C. Defense year mismatch

The YAML metadata states:

```text
defense_date: ۱۴۰۵
defense_date_en: 2025
```



Those dates should be reconciled before finalization.

**Confidence: 99%.**

---

# 20. Your current thesis has 7 H1 headings, and one is `منابع`

The source contains:

* English title
* Chapter 1
* Chapter 2
* Chapter 3
* Chapter 4
* Chapter 5
* References

The converter increments the chapter counter for every H1 except the English title. 

Therefore `منابع` is treated internally as another chapter state.

This probably won't visibly damage the current document because there are no later captions, but it is the wrong document model.

### Fix

Only actual thesis chapters should increment the chapter counter.

---

# 21. The current source has 4 heading levels

The converter supports H1–H4.

Your source actually uses all four levels.

That is good technically, but the converter's own lint logic says H4 is an exception. The thesis clearly uses H4 for real subsections, so the style rules need to explicitly account for that rather than treating it as an anomaly.

---

# 22. The generated DOCX itself passed basic XML parsing

This is worth noting.

The test file:

* opens as a DOCX package,
* has well-formed XML parts,
* contains the expected number of tables,
* contains OMML,
* contains RTL/table direction metadata.

So the converter is **not fundamentally broken**.

The problem is that:

> **valid DOCX XML ≠ correct thesis**

This distinction is crucial.

---

# 23. What I would keep from the current converter

Several parts are genuinely useful:

### Keep

* branch profiles
* reference-document/style architecture
* page dimensions/margins
* ZWNJ preservation
* RTL paragraph foundation
* RTL table metadata
* repeated table header
* no row splitting
* Pandoc as the LaTeX → OMML engine
* OOXML post-processing
* real Word footnote infrastructure

The current source already implements these ideas.  

### Replace

* custom Latin regex
* ad-hoc punctuation normalization
* naive inline math handling
* manual caption text
* duplicated front-matter model
* simplistic Markdown parser
* lack of source/math audit

---

# 24. Recommended final architecture

I would change the pipeline to:

```text
THESIS SOURCE
     │
     ├── source audit
     │     ├── Markdown structures
     │     ├── Unicode / ZWNJ
     │     ├── numbers
     │     ├── URLs
     │     ├── citations
     │     └── math syntax
     │
     ▼
CANONICAL INTERMEDIATE REPRESENTATION
     │
     ├── paragraph RTL/LTR
     ├── semantic text spans
     ├── math nodes
     ├── captions
     ├── tables
     ├── references
     └── figures
     │
     ▼
DOCX
     │
     ├── native Word styles
     ├── native OMML
     ├── real SEQ captions
     ├── real TOC/list fields
     ├── RTL OOXML
     └── RTL tables
     │
     ▼
OOXML QA
     │
     ├── XML validity
     ├── structure checks
     ├── equation count
     ├── table count
     ├── caption count
     ├── number comparison
     └── missing asset detection
     │
     ▼
VISUAL QA
     │
     ├── mixed bidi pages
     ├── equations
     ├── tables
     ├── captions
     ├── bibliography
     └── front/back matter
```

---

# 25. The QA system I recommend for this thesis

Before declaring the DOCX final, automatically compare:

| Check                             | Required result |
| --------------------------------- | --------------: |
| Source equations → DOCX equations |            100% |
| Source tables → DOCX tables       |            100% |
| Source figures → DOCX figures     |            100% |
| Source headings → Word headings   |            100% |
| Numeric tokens preserved          |            100% |
| Equation labels preserved         |            100% |
| Missing assets                    |               0 |
| Raw LaTeX outside math            |               0 |
| `&nbsp;` leakage                  |               0 |
| Broken footnote refs              |               0 |
| Broken hyperlinks                 |               0 |
| Caption fields missing            |               0 |
| Known bidi test failures          |               0 |

And then a second **visual QA corpus** specifically containing:

```text
فارسی + English
فارسی + 15.25
فارسی + (15.25)
فارسی + R² = 0.982
فارسی + p < 0.001
فارسی + URL
فارسی + citation
فارسی + equation
Persian table + numeric columns
Persian table + formula cells
```

---

# 26. Final priority list

### P0 — must fix before conversion

**1. Remove duplicated front matter model.**
**2. Repair malformed LaTeX in the source.**
**3. Replace the inline Latin/bidi tokenizer.**
**4. Build semantic math spans and native OMML correctly.**
**5. Implement real Word captions/SEQ numbering.**
**6. Supply all figure assets.**
**7. Fix source numerical/content inconsistencies.**

### P1 — must fix before final QA

**8. Replace global punctuation normalization with span-aware normalization.**
**9. Decode/remove `&nbsp;`.**
**10. Make equation numbering/cross-references structural.**
**11. Validate RTL tables visually and structurally.**
**12. Add automated numeric-equivalence testing.**

### P2 — quality improvements

**13. Better bibliography/reference structure.**
**14. Better page-number/section logic.**
**15. Better font fallback detection.**
**16. Rendered-page regression tests.**

---

# Bottom line

Your current converter is **a good prototype, not a production thesis converter**.

The most important discovery is not actually the RTL table code. It is this combination:

> **malformed mathematical source + fragile inline tokenizer + duplicated front matter + nonstructural captions**

That combination makes the current output unsuitable for submission-level use.

The good news is that the architecture is salvageable. I would **not throw the project away**; I would rebuild the parsing/conversion core while preserving much of its OOXML/style infrastructure.

**Overall assessment: 99% confidence.**

The next technically correct step is to build a **source audit + corrected conversion engine**, using this exact thesis as the test corpus, rather than trying to patch visible Word formatting errors after conversion.

Also, Microsoft’s OOXML documentation confirms that Office Math has distinct inline and display math structures, and current Word/OOXML guidance supports using native OMML rather than flattening equations to ordinary text. ([Microsoft Learn][1])

[1]: https://learn.microsoft.com/en-us/openspecs/office_standards/ms-oe376/1d77457b-2884-4749-9b4a-c150ca13cc19?utm_source=chatgpt.com "[MS-OE376]: Part 4 Section 7.1.2.77, oMath (Office Math) | Microsoft Learn"
