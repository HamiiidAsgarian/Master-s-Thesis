Absolutely. Here is the **fully English** version of the comprehensive report, with all Persian script examples replaced by descriptive placeholders, ensuring the entire document is purely in English while retaining all technical depth.

---

# Comprehensive Report: Common Problems Converting Persian/Farsi Academic Markdown to DOCX

Converting Persian (Farsi) academic Markdown to DOCX presents a unique set of challenges. Because Persian is a **Right-to-Left (RTL)** complex script, and both Markdown and Pandoc were originally designed for **Left-to-Right (LTR)** English-centric workflows, issues can arise at every stage—from the structure of your source file to the final rendering in Word.

This report is divided into two main parts: **MD Source File Structure Issues** (authoring phase) and **Pandoc Conversion Process Issues** (rendering phase), followed by an ideal workflow.

---

## Part 1: MD Source File Structure Issues (Authoring Phase)

If the Markdown source is not written with RTL and Persian typography in mind, subsequent conversions are almost guaranteed to fail.

### 1. Missing or Incorrect Metadata (YAML Front Matter)
This is the single most critical step. If the file header does not declare the language and text direction, Pandoc will default to LTR.

- **Symptoms**: The generated document is left-aligned. Persian characters may render as boxes, garbled text, or disjointed isolated letters (breaking the cursive connection).
- **Solution**: Every Persian MD file **must** start with the following YAML Front Matter:
  ```yaml
  ---
  lang: fa          # 'ar' (Arabic) also works for Persian scripts
  dir: rtl
  title: "Persian Document Title"
  author: "Author Name"
  date: "Date in Persian Calendar"
  ---
  ```

### 2. Incorrect Handling of the Zero-Width Non-Joiner (ZWNJ)
In Persian orthography, the ZWNJ (U+200C) is essential for correct spelling (e.g., it prevents incorrect letter connections in compound words).

- **Symptoms**: Using a regular space instead of a ZWNJ forces adjacent letters to connect incorrectly, altering the meaning and appearance of words. Conversely, the ZWNJ character may be stripped or corrupted during editing.
- **Solution**: Always use the correct ZWNJ character (often mapped to Shift+Space on Persian keyboards). Run a pre-processing script (e.g., `persian_cleanup.py`) to automatically standardize these characters before conversion.

### 3. Use of Incorrect Persian/Arabic Unicode Characters
- **Symptoms**: Using the Arabic forms of `ي` and `ك` instead of the Persian-specific `ی` and `ک`; using English punctuation (`,`, `?`, `;`) instead of Persian punctuation (`،`, `؟`, `؛`).
- **Solution**: Ensure the source file uses the correct Persian Unicode code points. Use automated text normalization tools to standardize the entire document.

### 4. Mixed Text Direction (Persian ↔ English/Numbers)
Academic papers inevitably mix RTL Persian, LTR English, and numerical data within a single paragraph.

- **Symptoms**: Punctuation (brackets, parentheses, periods) appears on the wrong side of the sentence. Numbers may jump to the left margin or be placed out of logical order. The bidirectional (bidi) algorithm often gets confused.
- **Solution**: For LaTeX/PDF outputs, wrap RTL content in `\RL{...}` or `\begin{RTL}...\end{RTL}`. For DOCX, Pandoc's support is limited; explicitly use HTML `<span dir="ltr">...</span>` tags around English terms in the MD file.

### 5. Complex Table Structures
Academic tables often have Persian headers, English data, and numerical values.

- **Symptoms**: The table remains LTR (first column on the left) instead of RTL (first column on the right). Cell content alignment is inconsistent. Markdown's native pipe tables fail to inherit the correct width or RTL styling.
- **Solution**: Pre-define a RTL table style in a `reference-docx` template. If using scripting, ensure `table.table_direction = WD_TABLE_DIRECTION.RTL`.

### 6. Lists (Ordered/Unordered) Numbering and Bullets
- **Symptoms**: Ordered list numbers (e.g., "1.") appear on the right side of the text instead of the left. Bullet point indentation is reversed or misaligned in the RTL context.
- **Solution**: Pre-define RTL list styles in the `reference-docx` template. Keep Markdown list syntax simple; avoid deeply nested RTL/LTR mixing.

### 7. Figure and Table Captions
- **Symptoms**: Captions like "Figure 1: Description" render with incorrect alignment or have the label and number placed on the wrong side.
- **Solution**: Use standard Markdown `![caption](image.png)` syntax, but define the "Caption" style explicitly as RTL in the Word template.

---

## Part 2: Pandoc Conversion Process Issues (Rendering Phase)

Even with a perfect Markdown source, the Pandoc conversion pipeline introduces specific technical failures.

### 1. Font and Glyph Rendering (Most Frequent)
Pandoc and Word use default fallback fonts that often lack Persian glyphs.

- **Symptoms**: Persian text appears as blank squares, question marks, or disjointed letters (not connected).
- **Solution**:
  - **Crucial**: Always use the `--reference-docx` flag pointing to a template where all paragraph styles have a Persian-compatible font (e.g., `Vazirmatn`, `BNazanin`, `Tahoma`).
  - For PDF via `xelatex`, specify `-V mainfont='Vazirmatn'`.

### 2. Failure to Enforce RTL Direction
- **Symptoms**: The entire document remains left-aligned, ignoring the metadata directive.
- **Solution**: Explicitly add `-V lang=ar` to the Pandoc command, or ensure the `dir: rtl` key is correctly placed in the YAML header. Note that Pandoc sometimes requires the `lang` variable to trigger Word's RTL paragraph properties.

### 3. Loss of Complex Script Formatting
Word handles "Complex Script" (e.g., Arabic, Persian) with specific formatting attributes (e.g., `w:bCs` for bold, `w:iCs` for italic).

- **Symptoms**: Bold, italic, and underline formatting applied to Persian text in Markdown are completely lost in the DOCX output.
- **Solution**: Pandoc's internal docx reader/writer does not fully support the `w:bCs` and `w:iCs` attributes. The most reliable workaround is to pre-define "Strong" and "Emphasis" styles as RTL-compatible in the `reference-docx` template.

### 4. Bidi Algorithm Collapse (Mixed Content)
- **Symptoms**: In a paragraph mixing Persian, English, and mathematical symbols, the directional order collapses. Brackets `()` or `[]` wrapping English text may appear on the far right, and the logical reading order is destroyed.
- **Solution**: Wrap LTR content explicitly using `<span dir="ltr">[English text]</span>` in the MD file. After conversion, manual correction in Word is often unavoidable for highly mixed paragraphs.

### 5. Table Direction Ignored
- **Symptoms**: Tables are generated strictly LTR, meaning the first column is on the far left, which is undesirable in a RTL document.
- **Solution**: Pandoc does not currently support a native flag to set table direction to RTL. You **must** use a `reference-docx` template where the Table Grid style has "Right-to-Left" table direction enabled. Alternatively, fix this manually in Word after conversion.

### 6. LaTeX Math Formula Conversion
- **Symptoms**: Complex formulas may not translate perfectly into Word's Equation Editor. Numbered equations may lose their tags, and inline math may be misaligned vertically relative to Persian text.
- **Solution**: Pandoc generally converts LaTeX math to Word OMML (Office MathML) adequately. Use the `--filter pandoc-crossref` to handle equation numbering. Ensure the font used for equations supports mathematical symbols.

### 7. Table of Contents (TOC) Rendering Issues
- **Symptoms**: Page numbers appear on the left side of the TOC entries instead of the right. Indentation for sub-sections is reversed.
- **Solution**: Generate the TOC using `--toc`. Afterwards, you must apply an RTL-aware TOC style via `reference-docx` or manually update the TOC in Word and change its paragraph direction to RTL.

### 8. Citation and Reference List Formatting
- **Symptoms**: Citation markers (e.g., `[Author, 2020]`) appear in the wrong place within the Persian sentence. The bibliography/reference list retains LTR numbering and indentation, breaking the page layout.
- **Solution**: Process citations with `--citeproc`. Use a CSL style that supports RTL. Crucially, define the "Bibliography" paragraph style in your `reference-docx` template as RTL-aligned with appropriate hanging indents.

### 9. Page Breaks and Widow/Orphan Control
- **Symptoms**: Headings appear isolated at the bottom of a page (orphans), or tables break across pages without carrying header rows.
- **Solution**: Pre-configure the heading styles in the `reference-docx` template with "Keep with next" and "Keep lines together" enabled. Pandoc does not inject these properties natively.

### 10. Invalid OOXML Control Characters
- **Symptoms**: The conversion fails entirely with XML parsing errors.
- **Solution**: Ensure the MD file is strictly UTF-8 encoded and contains no invalid Unicode surrogates or invisible OOXML control characters (often introduced by copy-pasting from PDFs).

### 11. File Paths Containing Non-ASCII Characters
- **Symptoms**: Images fail to embed, or Pandoc throws a "file not found" error despite the file existing.
- **Solution**: Only use ASCII characters for image filenames (e.g., use `figure1.png`, never `شکل۱.png`).

---

## Part 3: The Ideal Workflow and Authoring Checklist

To mitigate the issues above, follow this strict protocol:

### The Ideal MD File Structure (Fully English Placeholders)
```markdown
---
lang: fa
dir: rtl
title: "Persian Academic Paper Title"
author: "Author Full Name"
date: "1405/05/28"
---

# Introduction (Persian text)

This is a paragraph with a mix of Persian text [Persian script] and English terms like `Algorithm`. 
Numbers like `123` must be handled carefully.

## Mathematical Formulation

$$ E = mc^2 $$

### Table Example

| Right Column (Persian Header) | Left Column (English Header) |
| ----------------------------- | ---------------------------- |
| Value 1 (Persian)             | Value 2 (English/Number)     |

### List Example

- First Persian item
- Second Persian item

```

### The Recommended Pandoc Conversion Command
```bash
pandoc input.md -o output.docx \
  --reference-docx=persian-rtl-template.docx \
  --toc \
  --citeproc \
  --filter pandoc-crossref
```

### Critical Operational Recommendations
1.  **Metadata is non-negotiable**: Always declare `lang: fa` and `dir: rtl`.
2.  **Build a Rock-Solid `reference-docx` Template**:
    - Generate the default template: `pandoc -o reference.docx --print-default-data-file reference.docx`.
    - Open it in Word. Set **every** style (Normal, Heading 1-6, Table, Caption, Bibliography, TOC) to:
      - *Font*: A Persian-compatible font (e.g., Vazirmatn, Tahoma).
      - *Paragraph Direction*: Right-to-Left.
      - *Alignment*: Justify (or Right).
      - *Complex Script* formatting for bold/italic.
    - Save this file and always use it.
3.  **Source Encoding**: Always save your Markdown file as **UTF-8 without BOM**.
4.  **Pre-clean your text**: Run a script to normalize ZWNJ, Persian characters (`ی` vs `ي`), and punctuation before conversion.
5.  **Post-conversion proofreading is mandatory**: Despite all automation, Word's rendering of Bidi text and complex tables often requires final manual adjustments. Do not skip this step.

---

## References (Community Insights)

- Pandoc User Manual – General usage
- Pandoc GitHub Issues: #2191 (RTL support), #5558 (Complex Script formatting), #1502 (Table direction)
- Community projects: `persian-writing` GitHub utilities
- Delnatech Farsi Exporter documentation