# Cloude_Converter.py — Ideal Output Guide

## Prerequisites

| Dependency    | Install                                                  |
| ------------- | -------------------------------------------------------- |
| `python-docx` | `pip install python-docx`                                |
| `pyyaml`      | `pip install pyyaml`                                     |
| **pandoc**    | `brew install pandoc` (path: `/opt/homebrew/bin/pandoc`) |

Use the **pyenv** Python at `/Users/hamidasgharian/.pyenv/versions/3.10.12/bin/python3` — it has all deps installed.

## Exact Command (Ardabil branch)

```bash
/Users/hamidasgharian/.pyenv/versions/3.10.12/bin/python3 \
  "/Users/hamidasgharian/Desktop/sim/HamidOutput/DocX Converter/Cloude_Converter.py" \
  "/Users/hamidasgharian/Desktop/sim/HamidOutput/ACADEMIC_v3_Fa_restructured.md" \
  "/Users/hamidasgharian/Desktop/sim/HamidOutput/Thesis_Output.docx" \
  --branch ardabil
```

To regenerate, just re-run this exact command. For the English file, replace the input with `ACADEMIC_v3_En.md`.

## Input File Requirements

- **YAML front matter** (`---` delimited) must be at the top of the `.md` file with keys: `title_fa`, `title_en`, `author`, `supervisor`, `university`, `branch`, `faculty`, `degree`, `field`, `abstract_fa`, `abstract_en`, `keywords_fa`, `keywords_en`, `acknowledgements`, `dedication`. See `ACADEMIC_v3_Fa_restructured.md` for a complete example.
- **Display math** uses `$$ ... $$`. Equation labels like `\qquad \text{(معادله ۳-۱)}` at the end are automatically split off and rendered as LTR text runs (fixes mirrored parentheses in Word).
- **Inline math** uses `$ ... $` or `\( ... \)` (LaTeX syntax) — both are normalized to native OMML via pandoc.
- **Headings**: `#` = chapter (centered, new page), `##` = section, `###` = sub-section, `####` = sub-sub-section. Number them manually in the text (e.g. `## 2-4 عنوان بخش`).
- **Tables**: pipe (`|`) tables. `Table: caption text` on the line immediately before the table.
- **Images**: `![caption](path/to/image.png)`. Caption auto-numbered below the image.
- **Footnotes**: `text[^1]` with `[^1]: definition` anywhere in the file.
- **Blockquotes**: `>` lines — rendered as 1cm-indented, single-spaced quote style.

## What the Script Does

- Applies IAU Ardabil formatting: 3cm margins, Lotus fonts, 28pt line spacing, 1cm first-line indent, justified RTL text.
- Generates all front/back matter pages in the correct IAU order.
- Converts display math to native Word equations (OMML) via pandoc.
- Equation labels with parentheses around Persian text are split off from the OMML element and rendered as separate LTR text runs to prevent Word from mirroring the parentheses.
- Tables get horizontal-only borders, repeating header rows, and auto-numbered Persian captions above.
- Figures get auto-numbered Persian captions below.
- Punctuation normalization (ASCII `,;?` → Persian `،؛؟`) for Persian text.
- Genuine Word footnotes (not endnotes).
- Abjad page numbering for front matter, Arabic numerals for body.
- TOC / List of Tables / List of Figures as updateable Word fields.

## After Generation

1. Open `Thesis_Output.docx` in Microsoft Word (not Google Docs / LibreOffice).
2. Press **Ctrl+A** then **F9** to refresh all TOC / List of Tables / List of Figures fields.
3. Verify equation labels display correctly (parentheses should NOT be mirrored).

## Magic Fixes Applied

| Problem                                       | Fix Location                                                                                        |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Reversed parentheses in `\text{(معادله ۳-۱)}` | Line 864: `TEXT_LABEL_RE` splits label off before pandoc; lines 1054–1059 render it as LTR text run |
| Body text needs RTL + indentation             | `set_paragraph_rtl(p, True)` + `first_line_indent=Cm(1)`                                            |
| Equations must be LTR                         | `set_paragraph_rtl(p, False)` + `set_run_rtl(r, False)` on display math paragraphs                  |
| Inline math in RTL paragraphs                 | `set_run_rtl(r, False)` on the OMML math element                                                    |
| LaTeX `\(...\)` inline math not rendering     | `_process_inline()` normalizes `\(...\)` → `$...$` before regex matching; both delimiters work now  |

## Common Issues

- **`ModuleNotFoundError: No module named 'docx'`**: You used the wrong Python. Use the pyenv path above.
- **`input file not found`**: Use absolute paths (the script's CWD may not be what you expect).
- **Missing Lotus fonts**: The docx will reference them but they won't render on a machine without them. Font embedding is not handled by the script.
- **Pandoc not found**: Hardcoded at `/opt/homebrew/bin/pandoc`. Install via `brew install pandoc` or update the path in `latex_to_omml()`.
- **Formulas show raw `\(...\)` text**: The source uses LaTeX `\(...\)` delimiters. The script now auto-normalizes these to `$...$`, but if you see raw text, you may be using an older version — update the script or run a global find-replace: `\(` → `$`, `\)` → `$`.
