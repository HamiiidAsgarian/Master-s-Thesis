#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md_to_iau_thesis.py
====================

Converts a Farsi (Persian) Markdown thesis into a Word .docx file that
follows the IAU "Complete & Comprehensive Thesis Formatting Bible"
(general IAU rules + explicit Ardabil branch rules).

--------------------------------------------------------------------------
WHAT'S NEW IN THIS VERSION (strict rule-following pass)
--------------------------------------------------------------------------
- Branch profiles: --branch ardabil (default) or --branch general, each
  with its own margins and fonts, matching the rules document exactly.
- 4 heading levels (chapter / section / sub-section / sub-sub-section),
  chapter centered + starts on a new page, sections/sub-sections
  left-aligned per the rules.
- Body paragraphs: exact 28pt line spacing, 1cm first-line indent
  (skipped on the paragraph immediately after a heading), 0pt
  before/after spacing, full justification, widow/orphan control on.
- Tables: horizontal-only borders (no vertical rules), header row
  repeats on every page, rows won't split across a page break.
- Captions: table captions ABOVE the table, figure captions BELOW the
  figure, auto-numbered per chapter using Persian digits
  ("جدول ۲-۱", "شکل ۳-۴").
- Block quotes rendered as the "long quote" style (1cm indent both
  sides, single spacing, no quotation marks) per the quotation rules.
- Inline `$...$` math spans forced to Times New Roman + left-to-right,
  matching "equations are written LTR even inside Persian text."
- Real Word footnotes: `text[^1]` + `[^1]: definition text` anywhere in
  the markdown produces genuine Word footnotes (not endnotes / not fake
  superscript text), font-matched to the branch's footnote spec.
- Automatic Persian punctuation normalization (، ؟ ؛ with correct
  spacing) applied to Persian paragraph/heading/list/quote text.
- Full front/back matter order per the rules: Bismillah -> Farsi title
  page copy -> English title page -> Acknowledgements -> Dedication ->
  TOC -> List of Tables -> List of Figures -> Persian abstract (with
  keywords) -> [body, Arabic numerals restart at 1] -> English abstract
  -> English title page.
- Front-matter pages use Persian abjad-letter page numbering
  (و،لف، ب، ج ...) via OOXML's arabicAbjad number format; the Bismillah
  page's footer is suppressed (counts as page "الف" but shows nothing),
  matching the rule.
- A style/content lint report (word counts per paragraph, sentence
  length, heading depth) is printed after conversion so you can see
  where your draft breaks the 15-25 word/sentence and 100-250
  word/paragraph guidance -- this is advisory only, nothing is rewritten.

--------------------------------------------------------------------------
THINGS THIS SCRIPT DELIBERATELY DOES **NOT** AUTOMATE (and why)
--------------------------------------------------------------------------
- Native Word multi-level list numbering (2-4-3 style) tied live to
  heading levels: OOXML numbering fields don't have a reliable
  "Persian digit" numFmt that behaves consistently across Word
  versions, and a live numbering scheme would silently renumber if you
  reorder chapters later, which is riskier than it sounds for a thesis
  under active revision. Instead: type your chapter/section numbers
  directly into the Markdown heading text exactly as the rules show
  (e.g. `## 2-4 عنوان بخش`) and the script preserves them exactly,
  verbatim, with correct RTL shaping.
- Native Word equation objects (OMML). `$x^2$` gets styled (TNR, LTR)
  but isn't a real Word equation you can double-click to edit. For
  complex formulas, insert them via Word's Equation Editor after
  conversion.
- Reference-list reordering (Farsi sources first, then non-Farsi).
  Put them in that order in your Markdown; auto-sorting bibliographic
  entries reliably is riskier than it's worth.
- Anything physical: cover color/binding/embossing, CD burning, bound
  copy count. Those aren't docx-file properties.

--------------------------------------------------------------------------
MARKDOWN CONVENTIONS
--------------------------------------------------------------------------
    # Heading           -> Chapter        -> Heading 1 (centered, new page)
    ## Heading           -> Section        -> Heading 2 (left-aligned)
    ### Heading          -> Sub-section    -> Heading 3 (left-aligned)
    #### Heading         -> Sub-sub-sect.  -> Heading 4 (bold italic, left)
    **bold**, *italic*, ***both***, `code`
    $E = mc^2$            -> inline equation span (TNR, forced LTR)
    text[^1]               -> footnote reference
    [^1]: definition text  -> footnote definition (can appear anywhere;
                               stripped from the visible body automatically)
    - item / * item        -> bulleted list
    1. item                -> numbered list
    > long quotation       -> block-quote style (1cm indent, no marks)
    ---                    -> horizontal rule
    ![caption](img.png)    -> figure, caption BELOW, auto-numbered
    Table: caption text    -> (line immediately before a pipe table)
    | a | b |               caption ABOVE the table, auto-numbered
    | - | - |
    | 1 | 2 |
    ```lang
    code block
    ```

Optional YAML front matter (top of file, between `---` lines) drives the
title pages / abstract pages -- see README block at the bottom of
--help output, or the example `sample_thesis.md`.

--------------------------------------------------------------------------
USAGE
--------------------------------------------------------------------------
    pip install python-docx pyyaml --break-system-packages

    python3 md_to_iau_thesis.py thesis.md thesis.docx
    python3 md_to_iau_thesis.py thesis.md thesis.docx --branch general
    python3 md_to_iau_thesis.py thesis.md thesis.docx --no-title-page
    python3 md_to_iau_thesis.py thesis.md thesis.docx --no-lint

After generation: open in Word, Ctrl+A then F9 to refresh the
Table of Contents / List of Tables / List of Figures fields.
--------------------------------------------------------------------------
"""

import argparse
import copy
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_DIRECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement, parse_xml


# ==========================================================================
# BRANCH PROFILES (margins + fonts), per the rules document
# ==========================================================================

BRANCH_PROFILES = {
    "ardabil": {
        "margins_cm": {"top": 3.0, "bottom": 3.0, "right": 3.0, "left": 2.0},
        "fa_body_font": "LMU Lotus",
        "fa_chapter_font": "B Lotus",
        "fa_heading_font": "B Lotus",
        "fa_caption_font": "B Lotus",
        "fa_footnote_font": "LMU Lotus",
        "fa_bold_font": "B Lotus",
        "fa_title_font": "B Lotus",
        "body_size": 14,
        "chapter_size": 25,
        "h2_size": 14,
        "h3_size": 12,
        "h4_size": 12,
        "caption_size": 13,
        "footnote_size": 12,
    },
    "general": {
        "margins_cm": {"top": 2.5, "bottom": 2.5, "right": 2.5, "left": 3.5},
        "fa_body_font": "B Nazanin",
        "fa_chapter_font": "B Titr",
        "fa_heading_font": "B Nazanin",
        "fa_caption_font": "B Nazanin",
        "fa_footnote_font": "B Nazanin",
        "fa_bold_font": "B Zar",
        "fa_title_font": "B Titr",
        "body_size": 14,
        "chapter_size": 18,
        "h2_size": 16,
        "h3_size": 13,
        "h4_size": 12,
        "caption_size": 13,
        "footnote_size": 12,
    },
}

COMMON_DEFAULTS = {
    "en_font": "Times New Roman",
    "mono_font": "Consolas",
    "en_body_size": 12,
    "en_chapter_size": 25,
    "en_heading_size": 14,
    "en_caption_size": 11,
}

PERSIAN_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F]")


def is_persian(text: str) -> bool:
    """Heuristic: treat text as Persian/RTL if it contains any Arabic-script
    characters. Mixed text (Persian + inline English/numbers) still gets
    treated as an RTL paragraph, which is how Word normally handles it."""
    return bool(PERSIAN_RE.search(text))


PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"


def to_persian_digits(n) -> str:
    return "".join(PERSIAN_DIGITS[int(c)] if c.isdigit() else c for c in str(n))


# ==========================================================================
# PERSIAN PUNCTUATION NORMALIZATION
# --------------------------------------------------------------------------
# Only applied to text detected as Persian (is_persian == True), and never
# to code spans / code blocks / table of raw values, so URLs, code, and
# numeric data are left untouched.
# ==========================================================================

_PUNCT_MAP = {",": "،", ";": "؛", "?": "؟"}

# Pattern: ASCII punctuation surrounded by Persian characters (don't touch
# punctuation inside English/Latin runs like citations: "Jadhav et al., 2025a")
_PERSIAN_CONTEXT_RE = {
    ",": re.compile(r"([\u0600-\u06FF\u0750-\u077F])\s*,\s*([\u0600-\u06FF\u0750-\u077F])"),
    ";": re.compile(r"([\u0600-\u06FF\u0750-\u077F])\s*;\s*([\u0600-\u06FF\u0750-\u077F])"),
    "?": re.compile(r"([\u0600-\u06FF\u0750-\u077F])\s*\?\s*([\u0600-\u06FF\u0750-\u077F])"),
}

_SAFE_PUNCT_RE = re.compile(
    r"(?:"
    r"(?P<seg_persian>[\u0600-\u06FF\u0750-\u077F\u200C\s،؛؟:.]+)"  # Persian chars + punct
    r"|(?P<seg_other>[^$\u0600-\u06FF\u0750-\u077F]+)"                 # everything else (Latin, digits, URLs, math)
    r"|\$(?P<seg_math>[^$]+)\$"                                         # inline math
    r"|\x60(?P<seg_code>[^\x60]+)\x60"                                  # code span
    r")"
)

def normalize_persian_punctuation(text: str) -> str:
    if not is_persian(text):
        return text
    # Step A: replace ASCII punctuation when flanked by Persian characters
    for ascii_p, fa_p in _PUNCT_MAP.items():
        pattern = _PERSIAN_CONTEXT_RE[ascii_p]
        text = pattern.sub(r"\1" + fa_p + r"\2", text)
    # Steps B+C: span-aware — only operate on Persian prose segments,
    # skip decimals, URLs, citations, math, code
    parts = []
    last = 0
    for m in _SAFE_PUNCT_RE.finditer(text):
        if m.start() > last:
            # gap text — leave untouched
            parts.append(text[last:m.start()])
        if m.group("seg_persian"):
            seg = m.group("seg_persian")
            # Step B: remove space(s) before Persian punctuation
            seg = re.sub(r"\s+([،؛؟:.])", r"\1", seg)
            # Step C: force space after punctuation (not period)
            seg = re.sub(r"([،؛؟:])(?!\s|$)", r"\1 ", seg)
            parts.append(seg)
        elif m.group("seg_math") is not None:
            parts.append("$" + m.group("seg_math") + "$")
        elif m.group("seg_code") is not None:
            parts.append("`" + m.group("seg_code") + "`")
        else:
            parts.append(m.group("seg_other"))
        last = m.end()
    if last < len(text):
        parts.append(text[last:])
    return "".join(parts)


# ==========================================================================
# PRE-CONVERSION VALIDATION
# ==========================================================================

def validate_markdown(md_text: str) -> list:
    """Scan the Markdown source for issues that would cause DOCX rendering
    problems.  Returns a list of (severity, line_number, message) tuples.
    Severity is 'error' (will break rendering) or 'warn' (may cause issues).

    Checks (per Collective-md-to-docx-standards §XVI):
    - Arabic ي / ك instead of Persian ی / ک
    - Incorrect ZWNJ usage (space where ZWNJ expected)
    - Repeated spaces
    - English comma/semicolon/question-mark in Persian context
    - Unclosed math delimiters
    - Malformed tables
    - Duplicate heading IDs
    """
    issues = []
    lines = md_text.split("\n")
    heading_ids = {}

    # Precompiled patterns
    arabic_yeh_re = re.compile(r'[\u064A]')      # Arabic ي
    arabic_kaf_re = re.compile(r'[\u0643]')       # Arabic ك
    repeated_space_re = re.compile(r'  +')        # 2+ spaces
    eng_comma_fa_re = re.compile(r'[\u0600-\u06FF]\s*,\s*[\u0600-\u06FF]')
    eng_semicolon_fa_re = re.compile(r'[\u0600-\u06FF]\s*;\s*[\u0600-\u06FF]')
    eng_qmark_fa_re = re.compile(r'[\u0600-\u06FF]\s*\?\s*[\u0600-\u06FF]')
    heading_re = re.compile(r'^(#{1,4})\s+(.*)$')
    table_row_re = re.compile(r'^\s*\|(.+)\|\s*$')

    in_code_block = False
    unclosed_math = False
    math_start_line = 0
    table_col_counts = []

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Track code blocks (skip validation inside)
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Skip YAML front matter
        if i <= 2 and stripped == "---":
            continue

        # --- Arabic character detection ---
        for m in arabic_yeh_re.finditer(line):
            issues.append(('warn', i, f"Arabic ي (U+064A) at col {m.start()+1}; use Persian ی (U+06CC)"))
        for m in arabic_kaf_re.finditer(line):
            issues.append(('warn', i, f"Arabic ك (U+0643) at col {m.start()+1}; use Persian ک (U+06A9)"))

        # --- Repeated spaces (skip table rows and images) ---
        if not table_row_re.match(line) and not stripped.startswith("!") and not stripped.startswith("|"):
            for m in repeated_space_re.finditer(line):
                issues.append(('warn', i, f"Repeated spaces at col {m.start()+1}"))

        # --- English punctuation in Persian context ---
        if eng_comma_fa_re.search(line):
            issues.append(('warn', i, "English comma ',' between Persian characters; use '،'"))
        if eng_semicolon_fa_re.search(line):
            issues.append(('warn', i, "English semicolon ';' between Persian characters; use '؛'"))
        if eng_qmark_fa_re.search(line):
            issues.append(('warn', i, "English question mark '?' between Persian characters; use '؟'"))

        # --- Unclosed math delimiters ---
        dollar_count = line.count("$") - line.count("\\$")
        if dollar_count % 2 != 0:
            if unclosed_math:
                unclosed_math = False
            else:
                unclosed_math = True
                math_start_line = i

        # --- Heading ID tracking ---
        hm = heading_re.match(line)
        if hm:
            import hashlib
            h_text = hm.group(2).strip()
            h_id = hashlib.md5(h_text.encode()).hexdigest()[:8]
            if h_id in heading_ids:
                issues.append(('warn', i, f"Duplicate heading ID with line {heading_ids[h_id]}: '{h_text[:50]}'"))
            else:
                heading_ids[h_id] = i

    if unclosed_math:
        issues.append(('error', math_start_line, "Unclosed math delimiter '$'"))

    return issues


def print_validation_report(issues: list):
    """Print validation results. Called before conversion."""
    if not issues:
        print("[validation] No issues found.")
        return
    errors = [i for i in issues if i[0] == 'error']
    warnings = [i for i in issues if i[0] == 'warn']
    print(f"\n--- Pre-conversion validation ({len(errors)} error(s), {len(warnings)} warning(s)) ---")
    for severity, line_no, msg in errors[:20]:
        print(f"  [ERROR]   L{line_no}: {msg}")
    for severity, line_no, msg in warnings[:30]:
        print(f"  [WARN]    L{line_no}: {msg}")
    if len(warnings) > 30:
        print(f"  ... and {len(warnings) - 30} more warnings")
    print("--- end validation ---\n")


# ==========================================================================
# LOW-LEVEL OXML HELPERS (python-docx doesn't expose RTL/bidi/footnotes)
# ==========================================================================

# OOXML requires strict child-element ordering inside <w:pPr>, <w:rPr> and
# <w:sectPr>. A naive .append() produces schema-invalid XML that Word often
# tolerates but that fails strict validation / other viewers. These order
# lists + helper keep every insertion schema-correct.

PPR_ORDER = [
    "pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr", "widowControl",
    "numPr", "suppressLineNumbers", "pBdr", "shd", "tabs", "suppressAutoHyphens",
    "kinsoku", "wordWrap", "overflowPunct", "topLinePunct", "autoSpaceDE",
    "autoSpaceDN", "bidi", "adjustRightInd", "snapToGrid", "spacing", "ind",
    "contextualSpacing", "mirrorIndents", "suppressOverlap", "jc", "textDirection",
    "textAlignment", "textboxTightWrap", "outlineLvl", "divId", "cnfStyle", "rPr",
    "sectPr", "pPrChange",
]

RPR_ORDER = [
    "rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps", "strike",
    "dstrike", "outline", "shadow", "emboss", "imprint", "noProof", "snapToGrid",
    "vanish", "webHidden", "color", "spacing", "w", "kern", "position", "sz",
    "szCs", "highlight", "u", "effect", "bdr", "shd", "fitText", "vertAlign",
    "rtl", "cs", "em", "lang", "eastAsianLayout", "specVanish", "oMath",
]

SECTPR_ORDER = [
    "headerReference", "footerReference", "footnotePr", "endnotePr", "type",
    "pgSz", "pgMar", "paperSrc", "pgBorders", "lnNumType", "pgNumType", "cols",
    "formProt", "vAlign", "noEndnote", "titlePg", "textDirection", "bidi",
    "rtlGutter", "docGrid", "printerSettings", "sectPrChange",
]

TBLPR_ORDER = [
    "tblStyle", "tblpPr", "tblOverlap", "bidiVisual", "tblStyleRowBandSize",
    "tblStyleColBandSize", "tblW", "jc", "tblCellSpacing", "tblInd",
    "tblBorders", "shd", "tblLayout", "tblCellMar", "tblLook", "tblCaption",
    "tblDescription",
]


def _localname(el):
    return el.tag.split("}")[-1]


def insert_ordered(parent, new_child, order):
    tag = _localname(new_child)
    if tag not in order:
        parent.append(new_child)
        return new_child
    idx = order.index(tag)
    for sibling in parent:
        sib_tag = _localname(sibling)
        if sib_tag in order and order.index(sib_tag) > idx:
            sibling.addprevious(new_child)
            return new_child
    parent.append(new_child)
    return new_child


def get_or_create(parent, tag_name, order):
    el = parent.find(qn(f"w:{tag_name}"))
    if el is None:
        el = OxmlElement(f"w:{tag_name}")
        insert_ordered(parent, el, order)
    return el


def set_paragraph_rtl(paragraph, rtl=True):
    pPr = paragraph._p.get_or_add_pPr()
    bidi = get_or_create(pPr, "bidi", PPR_ORDER)
    bidi.set(qn("w:val"), "1" if rtl else "0")


def set_run_rtl(run, rtl=True):
    rPr = run._r.get_or_add_rPr()
    rtl_el = get_or_create(rPr, "rtl", RPR_ORDER)
    rtl_el.set(qn("w:val"), "1" if rtl else "0")


def set_run_fonts(run, latin_font=None, cs_font=None, ea_font=None):
    rPr = run._r.get_or_add_rPr()
    rFonts = get_or_create(rPr, "rFonts", RPR_ORDER)
    if latin_font:
        rFonts.set(qn("w:ascii"), latin_font)
        rFonts.set(qn("w:hAnsi"), latin_font)
    if cs_font:
        rFonts.set(qn("w:cs"), cs_font)
    if ea_font:
        rFonts.set(qn("w:eastAsia"), ea_font)


def _font_size_cs(pt_size):
    el = OxmlElement("w:szCs")
    el.set(qn("w:val"), str(int(pt_size * 2)))
    return el


def set_run_superscript(run):
    rPr = run._r.get_or_add_rPr()
    va = get_or_create(rPr, "vertAlign", RPR_ORDER)
    va.set(qn("w:val"), "superscript")


def add_field(paragraph, field_code, result_text=""):
    run = paragraph.add_run()
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = field_code
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    fld_text = OxmlElement("w:t")
    fld_text.text = result_text
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    r = run._r
    r.append(fld_begin)
    r.append(instr)
    r.append(fld_sep)
    r.append(fld_text)
    r.append(fld_end)
    return run


def set_section_page_numbering(section, fmt="decimal", start=None):
    sectPr = section._sectPr
    pgNumType = get_or_create(sectPr, "pgNumType", SECTPR_ORDER)
    pgNumType.set(qn("w:fmt"), fmt)
    if start is not None:
        pgNumType.set(qn("w:start"), str(start))


def add_page_number_field(paragraph):
    add_field(paragraph, "PAGE", "1")


def add_footnote_reference_run(paragraph, footnote_id: int):
    """Insert a real <w:footnoteReference> into the paragraph (superscripted,
    auto-numbered by Word). Requires the footnotes part to be injected into
    the saved .docx afterward -- see inject_footnotes_part()."""
    run = paragraph.add_run()
    set_run_superscript(run)
    ref = OxmlElement("w:footnoteReference")
    ref.set(qn("w:id"), str(footnote_id))
    run._r.append(ref)
    return run


# ==========================================================================
# LATEX → OMML CONVERSION (via pandoc)
# ==========================================================================

_OMML_CACHE: dict = {}

def _normalize_latex(latex_str: str) -> str:
    """Fix common LaTeX escaping issues before passing to pandoc/OMML.

    - ``\\_`` → ``_``: escaped underscores are invalid in LaTeX math mode
      and cause pandoc conversion failures.
    - ``\\{`` / ``\\}`` → ``{`` / ``}``: escaped braces (rare but possible).
    """
    s = latex_str
    s = s.replace("\\_", "_")
    s = s.replace("\\{", "{")
    s = s.replace("\\}", "}")
    s = s.replace("\\^", "^")
    return s


def latex_to_omml(latex_str: str, display: bool = False):
    """Convert a LaTeX string to a native Word equation element using pandoc.

    Returns an ``OxmlElement`` for ``m:oMath`` (inline) or ``m:oMathPara``
    (display).  Returns ``None`` when pandoc is unavailable or the conversion
    fails; the caller should fall back to plain-text rendering.
    """
    latex_str = _normalize_latex(latex_str)
    cache_key = (latex_str, display)
    if cache_key in _OMML_CACHE:
        return _OMML_CACHE[cache_key]

    # Wrap LaTeX in a minimal document so pandoc produces proper OMML
    if display:
        doc = (r"\documentclass{article}\usepackage{amsmath}\begin{document}$$"
               + latex_str + r"$$\end{document}")
    else:
        doc = (r"\documentclass{article}\usepackage{amsmath}\begin{document}$"
               + latex_str + r"$\end{document}")

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tex_path = Path(tmpdir) / "eq.tex"
            docx_path = Path(tmpdir) / "eq.docx"
            tex_path.write_text(doc, encoding="utf-8")
            pandoc_cmd = shutil.which("pandoc") or "pandoc"
            result = subprocess.run(
                [pandoc_cmd, str(tex_path), "-o", str(docx_path)],
                capture_output=True, timeout=30,
            )
            if result.returncode != 0:
                _OMML_CACHE[cache_key] = None
                return None
            with zipfile.ZipFile(docx_path, "r") as zf:
                xml_bytes = zf.read("word/document.xml")
    except Exception:
        _OMML_CACHE[cache_key] = None
        return None

    import xml.etree.ElementTree as ET

    ET.register_namespace("m", "http://schemas.openxmlformats.org/officeDocument/2006/math")
    root = ET.fromstring(xml_bytes)
    ns = {"m": "http://schemas.openxmlformats.org/officeDocument/2006/math"}

    target_tag = "m:oMathPara" if display else "m:oMath"
    el = root.find(f".//{target_tag}", ns)
    if el is None:
        _OMML_CACHE[cache_key] = None
        return None

    omml_xml = ET.tostring(el, encoding="unicode")
    parsed = parse_xml(omml_xml)
    _OMML_CACHE[cache_key] = parsed
    return parsed


# ==========================================================================
# STYLE SETUP
# ==========================================================================

def build_styles(doc: Document, cfg: dict):
    styles = doc.styles

    # ---- Normal (base) style --------------------------------------------
    normal = styles["Normal"]
    normal.font.name = cfg["en_font"]
    normal.font.size = Pt(cfg["en_body_size"])
    normal_rpr = normal.element.get_or_add_rPr()
    rFonts = get_or_create(normal_rpr, "rFonts", RPR_ORDER)
    rFonts.set(qn("w:cs"), cfg["fa_body_font"])
    insert_ordered(normal_rpr, _font_size_cs(cfg["body_size"]), RPR_ORDER)
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.space_before = Pt(0)

    # ---- IAU Body: justified, RTL, exact 28pt line spacing, 1cm indent ---
    def make_body_style(name, first_line_indent_cm):
        if name in [s.name for s in styles]:
            return styles[name]
        st = styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        st.base_style = normal
        st.font.name = cfg["en_font"]
        st.font.size = Pt(cfg["body_size"])
        pf = st.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.widow_control = True
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pf.line_spacing = Pt(28)
        if first_line_indent_cm:
            pf.first_line_indent = Cm(first_line_indent_cm)
        rpr = st.element.get_or_add_rPr()
        rFonts = get_or_create(rpr, "rFonts", RPR_ORDER)
        rFonts.set(qn("w:cs"), cfg["fa_body_font"])
        insert_ordered(rpr, _font_size_cs(cfg["body_size"]), RPR_ORDER)
        return st

    make_body_style("IAU Body", first_line_indent_cm=1.0)
    make_body_style("IAU Body First", first_line_indent_cm=0.0)  # no indent right after a heading

    # ---- Headings: Chapter (H1) / Section (H2) / Sub (H3) / Sub-sub (H4)
    heading_specs = [
        ("Heading 1", cfg["chapter_size"], True, False, cfg["fa_chapter_font"], WD_ALIGN_PARAGRAPH.CENTER, True),
        ("Heading 2", cfg["h2_size"], True, False, cfg["fa_heading_font"], WD_ALIGN_PARAGRAPH.LEFT, False),
        ("Heading 3", cfg["h3_size"], True, False, cfg["fa_heading_font"], WD_ALIGN_PARAGRAPH.LEFT, False),
        ("Heading 4", cfg["h4_size"], True, True, cfg["fa_heading_font"], WD_ALIGN_PARAGRAPH.LEFT, False),
    ]
    for name, size, bold, italic, cs_font, align, new_page in heading_specs:
        st = styles[name]
        st.font.name = cfg["en_font"]
        st.font.size = Pt(size)
        st.font.bold = bold
        st.font.italic = italic
        st.font.color.rgb = RGBColor(0, 0, 0)
        st.font.underline = False
        pf = st.paragraph_format
        pf.alignment = align
        pf.space_before = Pt(24 if new_page else 12)
        pf.space_after = Pt(12)
        pf.keep_with_next = True
        pf.widow_control = True
        pf.page_break_before = new_page
        rpr = st.element.get_or_add_rPr()
        rFonts = get_or_create(rpr, "rFonts", RPR_ORDER)
        rFonts.set(qn("w:cs"), cs_font)
        insert_ordered(rpr, _font_size_cs(size), RPR_ORDER)
        get_or_create(rpr, "b", RPR_ORDER)
        get_or_create(rpr, "bCs", RPR_ORDER)
        if italic:
            get_or_create(rpr, "i", RPR_ORDER)
            get_or_create(rpr, "iCs", RPR_ORDER)

    # ---- Caption (used for both table & figure captions) -----------------
    if "Caption" in [s.name for s in styles]:
        cap = styles["Caption"]
        cap.font.name = cfg["en_font"]
        cap.font.size = Pt(cfg["caption_size"])
        cap.font.bold = True
        cap.font.italic = True
        cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.paragraph_format.space_before = Pt(4)
        cap.paragraph_format.space_after = Pt(4)
        rpr = cap.element.get_or_add_rPr()
        rFonts = get_or_create(rpr, "rFonts", RPR_ORDER)
        rFonts.set(qn("w:cs"), cfg["fa_caption_font"])
        insert_ordered(rpr, _font_size_cs(cfg["caption_size"]), RPR_ORDER)
        get_or_create(rpr, "b", RPR_ORDER)

    # ---- Long block-quote style: 1cm indent both sides, single-spaced,
    # no italics, no quotation marks added by the script -------------------
    if "IAU Quote" not in [s.name for s in styles]:
        q = styles.add_style("IAU Quote", WD_STYLE_TYPE.PARAGRAPH)
        q.base_style = styles["IAU Body"]
        q.paragraph_format.left_indent = Cm(1)
        q.paragraph_format.right_indent = Cm(1)
        q.paragraph_format.first_line_indent = Cm(0)
        q.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        q.paragraph_format.line_spacing = 1.0

    # ---- Code style --------------------------------------------------------
    if "IAU Code" not in [s.name for s in styles]:
        c = styles.add_style("IAU Code", WD_STYLE_TYPE.PARAGRAPH)
        c.base_style = normal
        c.font.name = cfg["mono_font"]
        c.font.size = Pt(10.5)
        c.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        c.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE

    # ---- List styles (may be missing in custom templates) ------------------
    for list_style, base_name in [("List Bullet", "Normal"), ("List Number", "Normal")]:
        try:
            _ = styles[list_style]
        except KeyError:
            ls = styles.add_style(list_style, WD_STYLE_TYPE.PARAGRAPH)
            ls.base_style = styles[base_name]
            ls.font.name = cfg["en_font"]
            ls.font.size = Pt(cfg["body_size"])
            ls.paragraph_format.space_before = Pt(0)
            ls.paragraph_format.space_after = Pt(2)
            ls.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            rpr = ls.element.get_or_add_rPr()
            rFonts = get_or_create(rpr, "rFonts", RPR_ORDER)
            rFonts.set(qn("w:cs"), cfg["fa_body_font"])
            insert_ordered(rpr, _font_size_cs(cfg["body_size"]), RPR_ORDER)


# ==========================================================================
# PAGE SETUP
# ==========================================================================

def setup_page(section, margins_cm: dict):
    section.page_height = Cm(29.7)
    section.page_width = Cm(21.0)
    section.top_margin = Cm(margins_cm["top"])
    section.bottom_margin = Cm(margins_cm["bottom"])
    section.right_margin = Cm(margins_cm["right"])
    section.left_margin = Cm(margins_cm["left"])
    section.header_distance = Cm(1.5)
    section.footer_distance = Cm(1.5)

    sectPr = section._sectPr
    rtl_gutter = get_or_create(sectPr, "rtlGutter", SECTPR_ORDER)
    rtl_gutter.set(qn("w:val"), "1")


# ==========================================================================
# TITLE / FRONT MATTER PAGES
# ==========================================================================

def _para(doc, text, cs_font, en_font, size, bold=True, italic=False,
          space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER, force_rtl=None):
    p = doc.add_paragraph()
    p.alignment = align
    rtl = is_persian(text) if force_rtl is None else force_rtl
    set_paragraph_rtl(p, rtl)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    r.font.size = Pt(size)
    set_run_fonts(r, latin_font=en_font, cs_font=cs_font)
    set_run_rtl(r, rtl)
    return p


def add_bismillah_page(doc, cfg):
    _para(doc, "به نام خدا", cfg["fa_body_font"], cfg["en_font"], 14, bold=False, space_after=0)
    doc.add_page_break()


def add_farsi_title_page(doc, meta, cfg):
    p = _para
    if meta.get("university"):
        p(doc, meta["university"], cfg["fa_bold_font"], cfg["en_font"], 18)
    if meta.get("branch"):
        p(doc, meta["branch"], cfg["fa_bold_font"], cfg["en_font"], 18)
    if meta.get("faculty"):
        p(doc, meta["faculty"], cfg["fa_bold_font"], cfg["en_font"], 16)
    if meta.get("degree"):
        p(doc, meta["degree"], cfg["fa_bold_font"], cfg["en_font"], 16, space_after=18)
    if meta.get("field"):
        p(doc, meta["field"], cfg["fa_bold_font"], cfg["en_font"], 16, space_after=24)

    p(doc, "عنوان", cfg["fa_body_font"], cfg["en_font"], 18, space_after=6)
    if meta.get("title_fa"):
        p(doc, meta["title_fa"], cfg["fa_title_font"], cfg["en_font"], 18, space_after=24)

    if meta.get("supervisor"):
        p(doc, "استاد راهنما", cfg["fa_body_font"], cfg["en_font"], 18, space_after=4)
        p(doc, meta["supervisor"], cfg["fa_bold_font"], cfg["en_font"], 18, space_after=18)
    if meta.get("advisor"):
        p(doc, "استاد مشاور", cfg["fa_body_font"], cfg["en_font"], 18, space_after=4)
        p(doc, meta["advisor"], cfg["fa_bold_font"], cfg["en_font"], 18, space_after=18)
    if meta.get("author"):
        p(doc, "نگارش", cfg["fa_body_font"], cfg["en_font"], 18, space_after=4)
        p(doc, meta["author"], cfg["fa_bold_font"], cfg["en_font"], 18, space_after=36)
    if meta.get("defense_date"):
        p(doc, meta["defense_date"], cfg["fa_bold_font"], cfg["en_font"], 14, space_after=0)
    doc.add_page_break()


def add_english_title_page(doc, meta, cfg):
    p = _para
    lines = [
        (meta.get("university_en", "Islamic Azad University"), 18, True),
        (meta.get("branch_en"), 18, True),
        (meta.get("faculty_en"), 16, True),
        (meta.get("degree_en", "A Thesis Submitted in Partial Fulfillment of the Requirements for the Degree of Master of Science (M.Sc.)"), 14, False),
        (meta.get("field_en"), 16, True),
    ]
    for text, size, bold in lines:
        if text:
            p(doc, text, None, cfg["en_font"], size, bold=bold, space_after=14, force_rtl=False)

    if meta.get("title_en"):
        p(doc, "Title", None, cfg["en_font"], 16, space_after=6, force_rtl=False)
        p(doc, meta["title_en"], None, cfg["en_font"], 16, italic=True, space_after=24, force_rtl=False)

    if meta.get("supervisor_en"):
        p(doc, "Supervisor", None, cfg["en_font"], 14, space_after=4, force_rtl=False)
        p(doc, meta["supervisor_en"], None, cfg["en_font"], 14, space_after=18, force_rtl=False)
    if meta.get("advisor_en"):
        p(doc, "Advisor", None, cfg["en_font"], 14, space_after=4, force_rtl=False)
        p(doc, meta["advisor_en"], None, cfg["en_font"], 14, space_after=18, force_rtl=False)
    if meta.get("author_en"):
        p(doc, "By", None, cfg["en_font"], 14, space_after=4, force_rtl=False)
        p(doc, meta["author_en"], None, cfg["en_font"], 14, space_after=36, force_rtl=False)
    if meta.get("defense_date_en"):
        p(doc, meta["defense_date_en"], None, cfg["en_font"], 12, bold=False, space_after=0, force_rtl=False)


def add_simple_fa_page(doc, heading_fa, body_text, cfg):
    if not body_text:
        return
    h = _para(doc, heading_fa, cfg["fa_chapter_font"], cfg["en_font"], 16, space_after=18)
    p = doc.add_paragraph(style="IAU Body")
    rtl = is_persian(body_text)
    set_paragraph_rtl(p, rtl)
    r = p.add_run(normalize_persian_punctuation(body_text))
    set_run_fonts(r, latin_font=cfg["en_font"], cs_font=cfg["fa_body_font"])
    set_run_rtl(r, rtl)
    doc.add_page_break()


def add_toc_pages(doc, cfg):
    for heading_fa, field in [
        ("فهرست مطالب", 'TOC \\o "1-4" \\h \\z \\u'),
        ("فهرست جداول", 'TOC \\h \\z \\c "Table"'),
        ("فهرست نمودارها و تصاویر", 'TOC \\h \\z \\c "Figure"'),
    ]:
        _para(doc, heading_fa, cfg["fa_chapter_font"], cfg["en_font"], 16, space_after=12)
        note = doc.add_paragraph()
        set_paragraph_rtl(note, True)
        nr = note.add_run("(در Word پس از باز کردن فایل، Ctrl+A سپس F9 را بزنید تا این فهرست به‌روزرسانی شود.)")
        nr.italic = True
        nr.font.size = Pt(10)
        set_run_fonts(nr, latin_font=cfg["en_font"], cs_font=cfg["fa_body_font"])
        set_run_rtl(nr, True)
        field_p = doc.add_paragraph()
        set_paragraph_rtl(field_p, True)
        add_field(field_p, field, "")
        doc.add_page_break()


def add_abstract_page(doc, heading, text, keywords, cfg, rtl=True):
    _para(doc, heading, cfg["fa_chapter_font"] if rtl else None, cfg["en_font"], 16,
          space_after=18, force_rtl=rtl)
    p = doc.add_paragraph(style="IAU Body")
    set_paragraph_rtl(p, rtl)
    display_text = normalize_persian_punctuation(text) if rtl else text
    r = p.add_run(display_text)
    set_run_fonts(r, latin_font=cfg["en_font"], cs_font=cfg["fa_body_font"])
    set_run_rtl(r, rtl)
    if keywords:
        kw_label = "کلیدواژه‌ها: " if rtl else "Keywords: "
        kw_text = keywords if isinstance(keywords, str) else "، ".join(keywords) if rtl else ", ".join(keywords)
        kp = doc.add_paragraph(style="IAU Body")
        set_paragraph_rtl(kp, rtl)
        kp.paragraph_format.space_before = Pt(12)
        kr = kp.add_run(kw_label)
        kr.bold = True
        set_run_fonts(kr, latin_font=cfg["en_font"], cs_font=cfg["fa_body_font"])
        set_run_rtl(kr, rtl)
        kr2 = kp.add_run(kw_text)
        set_run_fonts(kr2, latin_font=cfg["en_font"], cs_font=cfg["fa_body_font"])
        set_run_rtl(kr2, rtl)


def add_abbreviations_page(doc, abbreviations, cfg):
    if not abbreviations:
        return
    _para(doc, "فهرست علائم و اختصارات", cfg["fa_chapter_font"], cfg["en_font"], 16, space_after=18)
    for item in abbreviations:
        if isinstance(item, dict):
            term = item.get("term", "")
            definition = item.get("definition", "")
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            term, definition = item
        else:
            term, definition = str(item), ""
        p = doc.add_paragraph(style="IAU Body")
        rtl = is_persian(str(term)) or is_persian(str(definition))
        set_paragraph_rtl(p, rtl)
        r1 = p.add_run(f"{term} — ")
        r1.bold = True
        set_run_fonts(r1, latin_font=cfg["en_font"], cs_font=cfg["fa_body_font"])
        set_run_rtl(r1, rtl)
        r2 = p.add_run(str(definition))
        set_run_fonts(r2, latin_font=cfg["en_font"], cs_font=cfg["fa_body_font"])
        set_run_rtl(r2, rtl)
    doc.add_page_break()


# ==========================================================================
# INLINE MARKDOWN (bold / italic / code / equation / footnote) -> RUNS
# ==========================================================================

# Also matches \(...\) LaTeX inline math — normalized to $...$ first.
INLINE_TOKEN_RE = re.compile(
    r"(\*\*\*(?P<b_i>.+?)\*\*\*)"        # ***bold italic***
    r"|(\*\*(?P<bold>.+?)\*\*)"           # **bold**
    r"|(\*(?P<italic>.+?)\*)"             # *italic*
    r"|(`(?P<code>.+?)`)"                 # `code`
    r"|(\$(?P<eq>[^$]+)\$)"               # $equation$  (or \(...\) normalized to $...$)
    r"|(\[\^(?P<fnref>[^\]]+)\])"         # [^footnote-id]
)


def _bidi_class(ch):
    """Return 'RTL', 'LTR', 'NUM', 'PUNCT', or 'WS' for a character."""
    cp = ord(ch)
    if 0x0600 <= cp <= 0x06FF or 0x0750 <= cp <= 0x077F or 0xFB50 <= cp <= 0xFDFF or 0xFE70 <= cp <= 0xFEFF:
        return 'RTL'
    if ch in '\u200C\u200D\u200E\u200F\u2066\u2067\u2068\u2069':
        return 'WS'
    if ch.isascii() and ch.isalpha():
        return 'LTR'
    if ch.isdigit():
        return 'NUM'
    if ch.isspace():
        return 'WS'
    return 'PUNCT'


_BRACKET_PAIRS = {'(': ')', '[': ']'}
_BRACKET_CLOSERS = {v: k for k, v in _BRACKET_PAIRS.items()}


def _resolve_bracket_classes(text, classes, base_rtl):
    """Mutate *classes* in place so each matched bracket pair shares one
    direction, chosen from the dominant direction of its enclosed content
    (falling back to the paragraph's base direction when the content is
    directionally neutral). This mirrors the Unicode bidi algorithm's rule
    for resolving "neutral" mirrored characters like parentheses/brackets,
    instead of letting each paren be classified alone as PUNCT."""
    stack = []
    for i, ch in enumerate(text):
        if ch in _BRACKET_PAIRS:
            stack.append(i)
        elif ch in _BRACKET_CLOSERS:
            for j in range(len(stack) - 1, -1, -1):
                if text[stack[j]] == _BRACKET_CLOSERS[ch]:
                    open_i = stack.pop(j)
                    del stack[j:]
                    rtl_count = 0
                    ltr_count = 0
                    for k in range(open_i + 1, i):
                        if classes[k] == 'RTL':
                            rtl_count += 1
                        elif classes[k] == 'LTR':
                            ltr_count += 1
                    if rtl_count > ltr_count:
                        pair_cls = 'RTL'
                    elif ltr_count > rtl_count:
                        pair_cls = 'LTR'
                    else:
                        pair_cls = 'RTL' if base_rtl else 'LTR'
                    classes[open_i] = pair_cls
                    classes[i] = pair_cls
                    break


def _tokenize_bidi_spans(text, base_rtl=False):
    """Split text into (substring, direction) pairs.

    *base_rtl* is the paragraph's overall direction; it's used as the
    tie-breaker for directionally-neutral bracket pairs (e.g. a
    parenthesis around a number) so bracket runs don't get stranded as
    their own isolated LTR span in the middle of RTL text.
    """
    if not text:
        return []
    classes = [_bidi_class(ch) for ch in text]
    _resolve_bracket_classes(text, classes, base_rtl)
    spans = []
    current_class = classes[0]
    current = text[0]
    for idx in range(1, len(text)):
        ch = text[idx]
        cls = classes[idx]
        # Keep a decimal/thousands separator glued to a surrounding NUM run
        # (e.g. "3.14" or "1,000") instead of splitting off its own PUNCT span.
        if (cls == 'PUNCT' and ch in '.,' and current_class == 'NUM'
                and idx + 1 < len(text) and classes[idx + 1] == 'NUM'):
            cls = 'NUM'
        if cls == current_class or (cls == 'WS' and current_class != 'WS'):
            current += ch
            if cls != 'WS':
                current_class = cls
        else:
            spans.append((current, current_class))
            current = ch
            current_class = cls
    spans.append((current, current_class))
    return spans


def add_inline_runs(paragraph, text, cfg, rtl=None, normalize_punct=True):
    """Parse inline Markdown formatting and append runs to *paragraph*.
    Delegates to the recursive :func:`_process_inline` so that nested
    formatting (e.g., ``**bold $equation$ bold**``) is handled correctly."""
    if rtl is None:
        rtl = is_persian(text)
    _process_inline(paragraph, text, cfg, rtl, normalize_punct,
                    default_bold=False, default_italic=False)


def _process_inline(paragraph, text, cfg, rtl, normalize_punct,
                    default_bold, default_italic):
    """Recursive inline processor.

    *default_bold* / *default_italic* are inherited from parent formatting
    contexts (e.g. inside ``**…**``) and applied to plain-text segments.
    """
    # Normalize \(...\) to $...$ so both LaTeX and Markdown math delimiters work.
    # Use regex to match \(...\) as a unit, avoiding corruption of text like
    # "something \(is\) a test" where backslash-paren is not math.
    text = re.sub(r'\\\((.+?)\\\)', r'$\1$', text)
    pos = 0
    for m in INLINE_TOKEN_RE.finditer(text):
        if m.start() > pos:
            segment = text[pos:m.start()]
            if normalize_punct and rtl:
                segment = normalize_persian_punctuation(segment)
            for span_text, span_cls in _tokenize_bidi_spans(segment, base_rtl=rtl):
                span_rtl = (span_cls == 'RTL')
                _append_run(paragraph, span_text, cfg, span_rtl,
                            bold=default_bold, italic=default_italic)
        if m.group("b_i") is not None:
            _process_inline(paragraph, m.group("b_i"), cfg, rtl, normalize_punct,
                            default_bold=True, default_italic=True)
        elif m.group("bold") is not None:
            _process_inline(paragraph, m.group("bold"), cfg, rtl, normalize_punct,
                            default_bold=True, default_italic=default_italic)
        elif m.group("italic") is not None:
            _process_inline(paragraph, m.group("italic"), cfg, rtl, normalize_punct,
                            default_bold=default_bold, default_italic=True)
        elif m.group("code") is not None:
            _append_run(paragraph, m.group("code"), cfg, rtl, mono=True)
        elif m.group("eq") is not None:
            eq_text = m.group("eq")
            omml = latex_to_omml(eq_text, display=False)
            if omml is not None:
                run = paragraph.add_run()
                run._r.append(copy.deepcopy(omml))
            else:
                _append_run(paragraph, eq_text, cfg, False, equation=True)
        elif m.group("fnref") is not None:
            label = m.group("fnref")
            fn_registry = cfg["_footnotes"]
            if label in fn_registry["defs"]:
                if label not in fn_registry["assigned"]:
                    fn_registry["next_id"] += 1
                    fn_registry["assigned"][label] = fn_registry["next_id"]
                    fn_registry["order"].append(label)
                add_footnote_reference_run(paragraph, fn_registry["assigned"][label])
            else:
                print(f"[warn] footnote reference [^{label}] has no matching "
                      f"definition; left as plain text.", file=sys.stderr)
                _append_run(paragraph, f"[^{label}]", cfg, rtl)
        pos = m.end()
    if pos < len(text):
        segment = text[pos:]
        if normalize_punct and rtl:
            segment = normalize_persian_punctuation(segment)
        for span_text, span_cls in _tokenize_bidi_spans(segment, base_rtl=rtl):
            span_rtl = (span_cls == 'RTL')
            _append_run(paragraph, span_text, cfg, span_rtl,
                        bold=default_bold, italic=default_italic)


def _append_run(paragraph, text, cfg, rtl, bold=False, italic=False, mono=False, equation=False):
    if text == "":
        return
    r = paragraph.add_run(text)
    r.bold = bold
    r.italic = italic

    rpr = r._r.get_or_add_rPr()
    if bold:
        get_or_create(rpr, "bCs", RPR_ORDER)
    if italic:
        get_or_create(rpr, "iCs", RPR_ORDER)
    if rtl:
        lang = get_or_create(rpr, "lang", RPR_ORDER)
        lang.set(qn("w:val"), "en-US")
        lang.set(qn("w:bidi"), "fa-IR")

    if mono:
        set_run_fonts(r, latin_font=cfg["mono_font"], cs_font=cfg["mono_font"])
    elif equation:
        set_run_fonts(r, latin_font=cfg["en_font"], cs_font=cfg["en_font"])
        r.font.size = Pt(10)
    else:
        set_run_fonts(r, latin_font=cfg["en_font"], cs_font=cfg["fa_body_font"])
    set_run_rtl(r, rtl)


# ==========================================================================
# MARKDOWN BODY PARSER
# ==========================================================================

TABLE_ROW_RE = re.compile(r"^\s*\|(.+)\|\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")
IMAGE_RE = re.compile(r"^!\[(?P<alt>.*?)\]\((?P<path>.*?)\)\s*$")
TABLE_CAPTION_RE = re.compile(
    r"^\s*\*?\*?(?:Table|جدول)\s*\([\d۰-۹]+-[\d۰-۹]+\)\s*[:：]?\s*\*?\*?\s*(.+?)(?:\*\*)?\s*$",
    re.IGNORECASE,
)
ORDERED_RE = re.compile(r"^\s*(\d+)[.)]\s+(.*)$")
UNORDERED_RE = re.compile(r"^\s*[-*+]\s+(.*)$")
IEEE_REF_RE = re.compile(r"^\s*\[(\d+)\]\s+(.*)$")
HEADING_RE = re.compile(r"^(#{1,4})\s+(.*)$")
FOOTNOTE_DEF_RE = re.compile(r"^\[\^([^\]]+)\]:\s*(.*)$")
DISPLAY_MATH_RE = re.compile(r"^\$\$(.+)\$\$\s*$")
# Matches \qquad \text{(...)} label at end of display math (to split off from OMML)
TEXT_LABEL_RE = re.compile(r"^(.*?)\\qquad\s*\\text\{([^}]*)\}\s*$")


def strip_yaml_frontmatter(md_text: str):
    if md_text.startswith("---"):
        end = md_text.find("\n---", 3)
        if end != -1:
            fm_raw = md_text[3:end].strip("\n")
            body = md_text[end + 4:].lstrip("\n")
            meta = {}
            if yaml is not None:
                try:
                    meta = yaml.safe_load(fm_raw) or {}
                except Exception as e:
                    print(f"[warn] could not parse YAML front matter: {e}", file=sys.stderr)
            else:
                print("[warn] pyyaml not installed; skipping front matter parsing "
                      "(pip install pyyaml --break-system-packages)", file=sys.stderr)
            return meta, body
    return {}, md_text


def _strip_body_front_matter(body_text: str) -> str:
    """When YAML front matter already generated title/abstract/TOC pages,
    strip the hand-written duplicates from the markdown body.

    Removes everything before the first '# فصل' (Chapter) heading.
    If no such heading is found, returns the body unchanged (safe fallback).
    """
    import re as _re
    chapter_re = _re.compile(r"^#\s+فصل\s+", _re.MULTILINE)
    m = chapter_re.search(body_text)
    if m:
        return body_text[m.start():]
    return body_text


def extract_footnote_definitions(lines):
    """Pull out `[^id]: text` lines anywhere in the doc, returning the
    remaining lines plus a {label: text} dict."""
    defs = {}
    kept = []
    for line in lines:
        m = FOOTNOTE_DEF_RE.match(line.strip())
        if m:
            defs[m.group(1)] = m.group(2).strip()
        else:
            kept.append(line)
    return kept, defs


def set_table_borders_horizontal_only(table):
    """No vertical rules; horizontal top/bottom border on the table plus a
    separator line under the header row, per the caption/table rule."""
    tbl = table._tbl
    tblPr = tbl.tblPr
    # RTL table direction
    bidi_el = get_or_create(tblPr, "bidiVisual", TBLPR_ORDER)
    bidi_el.set(qn("w:val"), "1")
    borders = OxmlElement("w:tblBorders")
    border_specs = {
        "top": "single", "left": "nil", "bottom": "single",
        "right": "nil", "insideH": "single", "insideV": "nil",
    }
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), border_specs[edge])
        if border_specs[edge] == "single":
            el.set(qn("w:sz"), "6")
            el.set(qn("w:space"), "0")
            el.set(qn("w:color"), "000000")
        borders.append(el)
    insert_ordered(tblPr, borders, TBLPR_ORDER)

    # remove any per-cell borders inherited from a table style, and make the
    # header row repeat + disallow row splitting across a page break
    for ri, row in enumerate(table.rows):
        tr = row._tr
        trPr = tr.get_or_add_trPr()
        if ri == 0:
            hdr = OxmlElement("w:tblHeader")
            hdr.set(qn("w:val"), "true")
            trPr.append(hdr)
        cant_split = OxmlElement("w:cantSplit")
        cant_split.set(qn("w:val"), "true")
        trPr.append(cant_split)
        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = OxmlElement("w:tcBorders")
            for edge in ("left", "right"):
                el = OxmlElement(f"w:{edge}")
                el.set(qn("w:val"), "nil")
                tcBorders.append(el)
            tcPr.append(tcBorders)


def add_table_from_rows(doc, rows, cfg):
    if not rows:
        return None
    n_cols = len(rows[0])
    table = doc.add_table(rows=len(rows), cols=n_cols)
    table.table_direction = WD_TABLE_DIRECTION.RTL
    table.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for ri, row in enumerate(rows):
        for ci, cell_text in enumerate(row):
            cell = table.cell(ri, ci)
            cell.text = ""
            p = cell.paragraphs[0]
            rtl = is_persian(cell_text)
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if rtl else WD_ALIGN_PARAGRAPH.CENTER
            set_paragraph_rtl(p, rtl)
            add_inline_runs(p, cell_text.strip(), cfg, rtl=rtl, normalize_punct=rtl)
            # Set cell text to 12pt (per IAU academic standard)
            for run in p.runs:
                run.font.size = Pt(12)
            if ri == 0:
                for run in p.runs:
                    run.bold = True
    set_table_borders_horizontal_only(table)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    return table


def add_caption(doc, kind, caption_text, cfg, state, position="above"):
    """kind: 'table' or 'figure'. Auto-numbers per current chapter using
    Persian digits, e.g. جدول ۲-۱ / شکل ۳-۴."""
    chapter = max(state["chapter"], 1)
    if kind == "table":
        state["table"] += 1
        num = state["table"]
        label = f"جدول {to_persian_digits(chapter)}-{to_persian_digits(num)}"
    else:
        state["figure"] += 1
        num = state["figure"]
        label = f"شکل {to_persian_digits(chapter)}-{to_persian_digits(num)}"

    p = doc.add_paragraph(style="Caption")
    set_paragraph_rtl(p, True)
    pPr = p._p.get_or_add_pPr()
    tblCaption = OxmlElement('w:tblCaption')
    tblCaption.set(qn('w:val'), 'Table' if kind == "table" else 'Figure')
    pPr.append(tblCaption)
    label_run = p.add_run(label)
    label_run.bold = True
    label_run.italic = True
    set_run_fonts(label_run, latin_font=cfg["en_font"], cs_font=cfg["fa_caption_font"])
    set_run_rtl(label_run, True)
    if caption_text:
        sep_run = p.add_run(": ")
        set_run_fonts(sep_run, latin_font=cfg["en_font"], cs_font=cfg["fa_caption_font"])
        set_run_rtl(sep_run, True)
        text_run = p.add_run(normalize_persian_punctuation(caption_text))
        text_run.bold = False
        text_run.italic = True
        set_run_fonts(text_run, latin_font=cfg["en_font"], cs_font=cfg["fa_caption_font"])
        set_run_rtl(text_run, True)
    return p


def convert_markdown_body(doc: Document, md_text: str, cfg: dict, state: dict, lint: dict):
    lines = md_text.split("\n")
    lines = [html.unescape(line) for line in lines]
    lines, footnote_defs = extract_footnote_definitions(lines)
    cfg["_footnotes"]["defs"].update(footnote_defs)

    n = len(lines)
    i = 0
    in_code_block = False
    code_buffer = []
    just_after_heading = False
    pending_table_caption = None

    while i < n:
        line = lines[i]

        # ---- fenced code blocks ------------------------------------
        if line.strip().startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_buffer = []
            else:
                in_code_block = False
                p = doc.add_paragraph(style="IAU Code")
                set_paragraph_rtl(p, False)
                r = p.add_run("\n".join(code_buffer))
                set_run_fonts(r, latin_font=cfg["mono_font"], cs_font=cfg["mono_font"])
                set_run_rtl(r, False)
                just_after_heading = False
            i += 1
            continue
        if in_code_block:
            code_buffer.append(line)
            i += 1
            continue

        stripped = line.strip()

        if stripped == "":
            i += 1
            continue

        # ---- display math ($$...$$) — centered LTR paragraph (native OMML) ---
        dm_m = DISPLAY_MATH_RE.match(stripped)
        if dm_m:
            eq_text = dm_m.group(1).strip()
            # Split off \qquad \text{(label)} so it renders as a regular LTR
            # text run outside the OMML zone, avoiding mirrored parentheses.
            label_text = None
            label_match = TEXT_LABEL_RE.match(eq_text)
            if label_match:
                eq_text = label_match.group(1).strip()
                label_text = label_match.group(2)
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_paragraph_rtl(p, False)
            omp = latex_to_omml(eq_text, display=True)
            if omp is not None:
                p._p.append(copy.deepcopy(omp))
                if label_text:
                    r = p.add_run(f"  {label_text}")
                    r.font.name = cfg["en_font"]
                    r.font.size = Pt(cfg["en_body_size"])
                    set_run_fonts(r, latin_font=cfg["en_font"], cs_font=cfg["en_font"])
                    set_run_rtl(r, False)
            else:
                set_paragraph_rtl(p, False)
                full_text = eq_text
                if label_text:
                    full_text += f"  {label_text}"
                r = p.add_run(full_text)
                r.font.name = cfg["en_font"]
                r.font.size = Pt(cfg["en_body_size"])
                set_run_fonts(r, latin_font=cfg["en_font"], cs_font=cfg["en_font"])
                set_run_rtl(r, False)
            just_after_heading = False
            i += 1
            continue

        # ---- table caption marker (consumed, applied to the table below) --
        cap_m = TABLE_CAPTION_RE.match(stripped)
        if cap_m:
            # Look ahead past blank lines for a table row
            j2 = i + 1
            while j2 < n and lines[j2].strip() == "":
                j2 += 1
            if j2 < n and TABLE_ROW_RE.match(lines[j2]):
                pending_table_caption = cap_m.group(1).strip()
                i += 1
                continue

        # ---- horizontal rule -------------------------------------------
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", stripped):
            p = doc.add_paragraph()
            pPr = p._p.get_or_add_pPr()
            pBdr = get_or_create(pPr, "pBdr", PPR_ORDER)
            bottom = OxmlElement("w:bottom")
            bottom.set(qn("w:val"), "single")
            bottom.set(qn("w:sz"), "6")
            bottom.set(qn("w:space"), "1")
            bottom.set(qn("w:color"), "999999")
            pBdr.append(bottom)
            i += 1
            continue

        # ---- image (figure) — caption BELOW, auto-numbered -----------------
        img_m = IMAGE_RE.match(stripped)
        if img_m:
            path = img_m.group("path")
            alt = img_m.group("alt")
            img_path = Path(path)
            if not img_path.is_absolute():
                img_path = (Path(cfg["md_dir"]) / path).resolve()
            if img_path.exists():
                try:
                    doc.add_picture(str(img_path), width=Cm(14))
                    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
                except Exception:
                    warn_p = doc.add_paragraph()
                    wr = warn_p.add_run(f"[unsupported image format: {path}]")
                    wr.italic = True
            else:
                warn_p = doc.add_paragraph()
                wr = warn_p.add_run(f"[missing image: {path}]")
                wr.italic = True
            # Peek ahead: if the next non-empty line is a manual caption like
            # **شکل (X-Y):** text or شکل (X-Y): text, use it as the caption
            # text and skip auto-numbering.
            caption_text = alt
            j = i + 1
            while j < n and lines[j].strip() == "":
                j += 1
            CAPTION_RE = re.compile(
                r"^\s*\*?\*?شکل\s*\([\d۰-۹]+-[\d۰-۹]+\)\s*[:：]?\s*\*?\*?\s*(.+)$"
            )
            if j < n:
                cap_m2 = CAPTION_RE.match(lines[j].strip())
                if cap_m2:
                    caption_text = cap_m2.group(1).strip()
                    i = j + 1  # skip the caption line
                else:
                    i += 1
            else:
                i += 1
            # Skip auto-numbered captions for images before the first chapter
            if state["chapter"] > 0:
                add_caption(doc, "figure", caption_text, cfg, state, position="below")
            else:
                # Front-matter image: add caption as plain centered text
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(caption_text)
                r.italic = True
                r.font.size = Pt(10)
                set_run_fonts(r, latin_font=cfg["en_font"], cs_font=cfg["fa_caption_font"])
                set_run_rtl(r, True)
            just_after_heading = False
            continue

        # ---- heading -----------------------------------------------------
        h_m = HEADING_RE.match(line)
        if h_m:
            level = len(h_m.group(1))
            text = h_m.group(2).strip()
            if level == 1:
                # Skip the English title page heading (not a real chapter)
                en_title = cfg.get("_meta_title_en", "")
                if en_title and text.strip() == en_title.strip():
                    pass  # don't increment chapter counter
                else:
                    state["chapter"] += 1
                    state["table"] = 0
                    state["figure"] = 0
            # Detect references section for IEEE numbering (H1 or H2)
            _ref_headings = {"منابع", "منابع فارسی", "منابع غیرفارسی"}
            if text.strip() in _ref_headings:
                state["in_references"] = True
                state["ref_counter"] = 0
            style_name = f"Heading {level}"
            p = doc.add_paragraph(style=style_name)
            rtl = is_persian(text)
            set_paragraph_rtl(p, rtl)
            add_inline_runs(p, text, cfg, rtl=rtl)
            lint["heading_levels"].add(level)
            just_after_heading = True
            i += 1
            continue

        # ---- blockquote (long quote: 1cm indent, no marks, single-spaced) --
        if stripped.startswith(">"):
            quote_lines = []
            while i < n and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip().lstrip(">").strip())
                i += 1
            text = " ".join(quote_lines)
            p = doc.add_paragraph(style="IAU Quote")
            rtl = is_persian(text)
            set_paragraph_rtl(p, rtl)
            add_inline_runs(p, text, cfg, rtl=rtl)
            just_after_heading = False
            continue

        # ---- table (caption ABOVE, auto-numbered) --------------------------
        if TABLE_ROW_RE.match(line):
            table_lines = []
            while i < n and TABLE_ROW_RE.match(lines[i]):
                table_lines.append(lines[i])
                i += 1
            rows = []
            for idx, tl in enumerate(table_lines):
                if idx == 1 and TABLE_SEP_RE.match(tl):
                    continue
                cells = [c.strip() for c in tl.strip().strip("|").split("|")]
                rows.append(cells)
            add_caption(doc, "table", pending_table_caption, cfg, state, position="above")
            pending_table_caption = None
            add_table_from_rows(doc, rows, cfg)
            just_after_heading = False
            continue

        # ---- IEEE [N] reference entry (inside or outside references section) -
        ref_m = IEEE_REF_RE.match(line)
        if ref_m:
            ref_num = ref_m.group(1)
            ref_text = ref_m.group(2)
            p = doc.add_paragraph()
            rtl = is_persian(ref_text)
            set_paragraph_rtl(p, rtl)
            # Add [N] label as bold run
            label_run = p.add_run(f"[{ref_num}] ")
            label_run.bold = True
            set_run_fonts(label_run, latin_font=cfg["en_font"], cs_font=cfg["fa_body_font"])
            set_run_rtl(label_run, False)
            # Add the rest of the reference text
            add_inline_runs(p, ref_text, cfg, rtl=rtl)
            just_after_heading = False
            i += 1
            continue

        # ---- unordered list ------------------------------------------------
        if UNORDERED_RE.match(line):
            while i < n and UNORDERED_RE.match(lines[i]):
                text = UNORDERED_RE.match(lines[i]).group(1)
                if state["in_references"]:
                    # IEEE numbered reference: [1] Author. (Year). ...
                    state["ref_counter"] += 1
                    label = "[{}]".format(state["ref_counter"])
                    p = doc.add_paragraph(style="List Number")
                    rtl = is_persian(text)
                    set_paragraph_rtl(p, rtl)
                    # Add the [N] label as a separate run, then the rest
                    label_run = p.add_run(label + " ")
                    label_run.bold = True
                    set_run_fonts(label_run, latin_font=cfg["en_font"], cs_font=cfg["fa_body_font"])
                    set_run_rtl(label_run, False)
                    add_inline_runs(p, text, cfg, rtl=rtl)
                else:
                    p = doc.add_paragraph(style="List Bullet")
                    rtl = is_persian(text)
                    set_paragraph_rtl(p, rtl)
                    add_inline_runs(p, text, cfg, rtl=rtl)
                i += 1
            just_after_heading = False
            continue

        # ---- ordered list --------------------------------------------------
        if ORDERED_RE.match(line):
            while i < n and ORDERED_RE.match(lines[i]):
                text = ORDERED_RE.match(lines[i]).group(2)
                p = doc.add_paragraph(style="List Number")
                rtl = is_persian(text)
                set_paragraph_rtl(p, rtl)
                add_inline_runs(p, text, cfg, rtl=rtl)
                i += 1
            just_after_heading = False
            continue

        # ---- normal paragraph (collect contiguous lines) --------------------
        para_lines = [line]
        i += 1
        while i < n and lines[i].strip() != "" and not HEADING_RE.match(lines[i]) \
                and not UNORDERED_RE.match(lines[i]) and not ORDERED_RE.match(lines[i]) \
                and not TABLE_ROW_RE.match(lines[i]) and not lines[i].strip().startswith(">") \
                and not lines[i].strip().startswith("```") \
                and not IMAGE_RE.match(lines[i].strip()) \
                and not TABLE_CAPTION_RE.match(lines[i].strip()) \
                and not DISPLAY_MATH_RE.match(lines[i].strip()) \
                and not re.match(r"^(-{3,}|\*{3,}|_{3,})$", lines[i].strip()):
            para_lines.append(lines[i])
            i += 1
        text = " ".join(l.strip() for l in para_lines)
        style_name = "IAU Body First" if just_after_heading else "IAU Body"
        p = doc.add_paragraph(style=style_name)
        rtl = is_persian(text)
        set_paragraph_rtl(p, rtl)
        add_inline_runs(p, text, cfg, rtl=rtl)
        _lint_paragraph(text, lint)
        just_after_heading = False


# ==========================================================================
# LINT REPORT (advisory only — does not alter the document)
# ==========================================================================

SENTENCE_SPLIT_RE = re.compile(r"[.!؟]+\s*")


def _word_count(text):
    return len(re.findall(r"\S+", text))


def _lint_paragraph(text, lint):
    wc = _word_count(text)
    if wc < 30:
        lint["short_paragraphs"].append((wc, text[:60]))
    elif wc > 250:
        lint["long_paragraphs"].append((wc, text[:60]))
    for sentence in SENTENCE_SPLIT_RE.split(text):
        sc = _word_count(sentence)
        if sc > 35:
            lint["long_sentences"].append((sc, sentence[:60]))
    # Typography checks (Collective standards §XVI)
    # Check for inconsistent percent signs
    if "%" in text and "٪" in text:
        lint["mixed_percent"].append(text[:60])
    # Check for inconsistent decimal separators (Arabic ٫ mixed with English .)
    if "٫" in text and re.search(r'\d+\.\d+', text):
        lint["mixed_decimals"].append(text[:60])


def print_lint_report(lint):
    print("\n--- Style guidance report (advisory only; nothing was rewritten) ---")
    if lint["heading_levels"] - {1, 2, 3}:
        print(f"[info] Heading levels used beyond H3: {sorted(lint['heading_levels'])} "
              f"(rules recommend max 3 levels except where a 4th sub-sub-section is needed).")
    if lint["short_paragraphs"]:
        print(f"[info] {len(lint['short_paragraphs'])} paragraph(s) under ~30 words "
              f"(guidance: 100-250 words / 5-10 sentences per paragraph). First few:")
        for wc, snippet in lint["short_paragraphs"][:5]:
            print(f"    ({wc} words) {snippet}...")
    if lint["long_paragraphs"]:
        print(f"[info] {len(lint['long_paragraphs'])} paragraph(s) over ~250 words. First few:")
        for wc, snippet in lint["long_paragraphs"][:5]:
            print(f"    ({wc} words) {snippet}...")
    if lint["long_sentences"]:
        print(f"[info] {len(lint['long_sentences'])} sentence(s) over 35 words "
              f"(guidance: 15-25 words average, 35 max). First few:")
        for sc, snippet in lint["long_sentences"][:5]:
            print(f"    ({sc} words) {snippet}...")
    # Typography checks
    if lint.get("mixed_percent"):
        print(f"[warn] {len(lint['mixed_percent'])} paragraph(s) mix '%' and '٪' (Arabic percent). "
              f"Use one consistently. First few:")
        for snippet in lint["mixed_percent"][:3]:
            print(f"    {snippet}...")
    if lint.get("mixed_decimals"):
        print(f"[warn] {len(lint['mixed_decimals'])} paragraph(s) mix '.' and '٫' (Arabic decimal separator). "
              f"Use one consistently. First few:")
        for snippet in lint["mixed_decimals"][:3]:
            print(f"    {snippet}...")
    if not any([lint["short_paragraphs"], lint["long_paragraphs"], lint["long_sentences"],
                lint.get("mixed_percent", []), lint.get("mixed_decimals", [])]):
        print("[ok] No paragraph/sentence-length or typography issues detected.")
    print("--- end report ---\n")


# ==========================================================================
# FOOTER / PAGE NUMBERS
# ==========================================================================

def add_footer_page_numbers(section, cfg, suppress_first_page=False):
    if suppress_first_page:
        section.different_first_page_header_footer = True
        # first-page footer stays blank (no field added)
        _ = section.first_page_footer
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_rtl(p, False)
    p.text = ""
    add_page_number_field(p)
    for r in p.runs:
        r.font.size = Pt(10)
        set_run_fonts(r, latin_font=cfg["en_font"])


# ==========================================================================
# FOOTNOTES PART INJECTION (post-processing the saved .docx)
# ==========================================================================

FOOTNOTES_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"
FOOTNOTES_REL_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes"


def build_footnotes_xml(footnote_registry, cfg) -> bytes:
    w_ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    parts = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        f'<w:footnotes xmlns:w="{w_ns}">',
        '<w:footnote w:type="separator" w:id="-1"><w:p><w:pPr><w:bidi w:val="1"/><w:jc w:val="right"/><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:separator/></w:r></w:p></w:footnote>',
        '<w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:pPr><w:bidi w:val="1"/><w:jc w:val="right"/><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:continuationSeparator/></w:r></w:p></w:footnote>',
    ]
    import xml.sax.saxutils as sax

    for label in footnote_registry["order"]:
        fid = footnote_registry["assigned"][label]
        text = footnote_registry["defs"].get(label, "")
        rtl = is_persian(text)
        text = normalize_persian_punctuation(text) if rtl else text
        esc = sax.escape(text)
        bidi = '<w:bidi w:val="1"/>' if rtl else ""
        jc = '<w:jc w:val="right"/>' if rtl else ""
        cs_font = cfg["fa_footnote_font"]
        sz = int(cfg["footnote_size"] * 2)
        rtl_run = '<w:rtl w:val="1"/>' if rtl else ""
        parts.append(
            f'<w:footnote w:id="{fid}">'
            f'<w:p><w:pPr>{bidi}<w:spacing w:after="0"/>{jc}</w:pPr>'
            f'<w:r><w:rPr><w:vertAlign w:val="superscript"/></w:rPr><w:footnoteRef/></w:r>'
            f'<w:r><w:rPr><w:rFonts w:ascii="{cfg["en_font"]}" w:hAnsi="{cfg["en_font"]}" w:cs="{cs_font}"/>'
            f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>{rtl_run}</w:rPr>'
            f'<w:t xml:space="preserve"> {esc}</w:t></w:r></w:p></w:footnote>'
        )
    parts.append("</w:footnotes>")
    return "".join(parts).encode("utf-8")


def inject_footnotes_part(docx_path: Path, footnotes_xml: bytes):
    """Post-process the saved .docx zip to add word/footnotes.xml, the
    matching relationship, and the content-type override. This is done as
    a zip-level patch because python-docx has no footnotes API."""
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".docx")
    os.close(tmp_fd)
    Path(tmp_path).unlink()  # we just want a free filename
    tmp_path = Path(tmp_path)

    with zipfile.ZipFile(docx_path, "r") as zin:
        names = zin.namelist()
        content_types = zin.read("[Content_Types].xml").decode("utf-8")
        rels = zin.read("word/_rels/document.xml.rels").decode("utf-8")

        # Ensure content-type override exists
        if FOOTNOTES_CONTENT_TYPE not in content_types:
            content_types = content_types.replace(
                "</Types>",
                f'<Override PartName="/word/footnotes.xml" ContentType="{FOOTNOTES_CONTENT_TYPE}"/></Types>',
            )

        # Ensure relationship exists; re-use existing one if present
        existing_footnote_rel = re.search(r'Target="footnotes\.xml"', rels)
        if existing_footnote_rel:
            # relationship already exists (from template); keep the same Id
            new_id = None  # signal: don't add another relationship
        else:
            existing_ids = [int(m) for m in re.findall(r'Id="rId(\d+)"', rels)]
            new_id = f"rId{(max(existing_ids) + 1) if existing_ids else 1000}"
            rels = rels.replace(
                "</Relationships>",
                f'<Relationship Id="{new_id}" Type="{FOOTNOTES_REL_TYPE}" Target="footnotes.xml"/></Relationships>',
            )

        with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == "[Content_Types].xml":
                    zout.writestr(item, content_types)
                elif item.filename == "word/_rels/document.xml.rels":
                    zout.writestr(item, rels)
                elif item.filename == "word/footnotes.xml":
                    continue  # skip template's footnotes; we write our own
                else:
                    zout.writestr(item, zin.read(item.filename))
            zout.writestr("word/footnotes.xml", footnotes_xml)

    shutil.move(str(tmp_path), str(docx_path))


def _fix_zoom_setting(doc: Document):
    """python-docx's built-in blank template ships a <w:zoom/> element with
    no w:percent attribute, which is schema-invalid. Patch it."""
    settings = doc.settings.element
    zoom = settings.find(qn("w:zoom"))
    if zoom is not None and zoom.get(qn("w:percent")) is None:
        zoom.set(qn("w:percent"), "100")


# ==========================================================================
# MAIN
# ==========================================================================

def _open_doc(template_path=None):
    """Create a new document, optionally inheriting styles from *template_path*.

    When a template is given, its style definitions and section properties are
    carried over, but all body content (paragraphs, tables) is stripped so the
    document starts clean.
    """
    if template_path:
        doc = Document(template_path)
        body = doc.element.body
        # Keep only <w:sectPr>, remove everything else
        sectPr = body.find(qn("w:sectPr"))
        for child in list(body):
            if child.tag != qn("w:sectPr"):
                body.remove(child)
        if sectPr is not None and sectPr not in body:
            body.append(sectPr)
        return doc
    return Document()


def _register_caption_labels(doc):
    """Register 'Table' and 'Figure' caption labels in the numbering part
    so Word's TOC \\c \"Table\" / \\c \"Figure\" fields can find them."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn as _qn

    numbering_part = doc.part.numbering_part
    if numbering_part is None:
        return

    numbering = numbering_part.numbering_definitions._numbering

    # Check if caption labels already exist
    existing_labels = set()
    for num in numbering.findall(_qn("w:num")):
        for child in num:
            if child.tag == _qn("w:caption"):
                existing_labels.add(child.get(_qn("w:name")))

    if "Table" in existing_labels and "Figure" in existing_labels:
        return

    # Find the highest abstractNumId and numId in use
    max_abstract = -1
    max_num = -1
    for an in numbering.findall(_qn("w:abstractNum")):
        val = an.get(_qn("w:abstractNumId"))
        if val is not None:
            max_abstract = max(max_abstract, int(val))
    for num in numbering.findall(_qn("w:num")):
        val = num.get(_qn("w:numId"))
        if val is not None:
            max_num = max(max_num, int(val))

    # Add abstractNum entries for Table and Figure caption labels
    for label_name, start_val in [("Table", 1), ("Figure", 1)]:
        max_abstract += 1
        max_num += 1

        abstract_num = OxmlElement("w:abstractNum")
        abstract_num.set(_qn("w:abstractNumId"), str(max_abstract))
        lvl = OxmlElement("w:lvl")
        lvl.set(_qn("w:ilvl"), "0")
        num_fmt = OxmlElement("w:numFmt")
        num_fmt.set(_qn("w:val"), "decimal")
        lvl.append(num_fmt)
        lvl_text = OxmlElement("w:lvlText")
        lvl_text.set(_qn("w:val"), "%1")
        lvl.append(lvl_text)
        start = OxmlElement("w:start")
        start.set(_qn("w:val"), str(start_val))
        lvl.append(start)
        abstract_num.append(lvl)
        # Place abstractNum before any num elements
        first_num = numbering.find(_qn("w:num"))
        if first_num is not None:
            numbering.insert(list(numbering).index(first_num), abstract_num)
        else:
            numbering.append(abstract_num)

        num_el = OxmlElement("w:num")
        num_el.set(_qn("w:numId"), str(max_num))
        abs_ref = OxmlElement("w:abstractNumId")
        abs_ref.set(_qn("w:val"), str(max_abstract))
        num_el.append(abs_ref)
        caption = OxmlElement("w:caption")
        caption.set(_qn("w:name"), label_name)
        caption.set(_qn("w:pos"), "afterText")
        caption.set(_qn("w:sep"), ":")
        num_el.append(caption)
        numbering.append(num_el)


def _fix_toc_fields_rtl(doc):
    """Make all TOC field paragraphs RTL so the list renders correctly for
    a Persian thesis (page numbers on the left, text on the right)."""
    from docx.oxml.ns import qn as _qn
    ns_w = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

    for p in doc.paragraphs:
        # Check if this paragraph contains a TOC field
        p_elem = p._p
        instr_texts = p_elem.findall(".//" + _qn("w:instrText"))
        has_toc = False
        for it in instr_texts:
            if it.text and "TOC" in it.text:
                has_toc = True
                break
        if not has_toc:
            continue

        # Make this paragraph RTL
        pPr = p_elem.get_or_add_pPr()
        bidi = pPr.find(_qn("w:bidi"))
        if bidi is None:
            bidi = OxmlElement("w:bidi")
            pPr.append(bidi)
        bidi.set(_qn("w:val"), "1")

        # Set paragraph alignment to right (for RTL visual)
        jc = pPr.find(_qn("w:jc"))
        if jc is None:
            jc = OxmlElement("w:jc")
            pPr.append(jc)
        jc.set(_qn("w:val"), "right")


def main():
    parser = argparse.ArgumentParser(
        description="Convert a Farsi Markdown thesis into an IAU-styled .docx file "
                     "following the strict Ardabil/General rules document.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input_md", help="Path to the source .md file")
    parser.add_argument("output_docx", help="Path to write the resulting .docx file")
    parser.add_argument("--branch", choices=["ardabil", "general"], default="ardabil",
                         help="Font/margin profile to use (default: ardabil)")
    parser.add_argument("--no-title-page", action="store_true",
                         help="Skip auto-generating front/back matter even if YAML front matter is present")
    parser.add_argument("--no-lint", action="store_true",
                         help="Skip the paragraph/sentence-length style report")
    parser.add_argument("--fa-font", default=None, help="Override Persian body font")
    parser.add_argument("--fa-chapter-font", default=None, help="Override Persian chapter-title font")
    parser.add_argument("--en-font", default=None, help="Override Latin font")
    parser.add_argument("--body-size", type=int, default=None, help="Override Persian body text size (pt)")
    parser.add_argument("--template", default=None,
                        help="Path to a .docx template file; its styles are used as the base while "
                             "branch-specific fonts/margins still override where needed")
    args = parser.parse_args()

    cfg = dict(BRANCH_PROFILES[args.branch])
    cfg.update(COMMON_DEFAULTS)
    if args.fa_font:
        cfg["fa_body_font"] = args.fa_font
        cfg["fa_heading_font"] = args.fa_font
        cfg["fa_caption_font"] = args.fa_font
        cfg["fa_footnote_font"] = args.fa_font
    if args.fa_chapter_font:
        cfg["fa_chapter_font"] = args.fa_chapter_font
        cfg["fa_title_font"] = args.fa_chapter_font
    if args.en_font:
        cfg["en_font"] = args.en_font
    if args.body_size:
        cfg["body_size"] = args.body_size
    cfg["_footnotes"] = {"defs": {}, "assigned": {}, "order": [], "next_id": 0}

    input_path = Path(args.input_md)
    if not input_path.exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    cfg["md_dir"] = str(input_path.parent)

    md_text = input_path.read_text(encoding="utf-8")
    meta, body_text = strip_yaml_frontmatter(md_text)
    cfg["_meta_title_en"] = meta.get("title_en", "")

    doc = _open_doc(args.template)
    _fix_zoom_setting(doc)
    build_styles(doc, cfg)
    margins = BRANCH_PROFILES[args.branch]["margins_cm"]
    setup_page(doc.sections[0], margins)

    has_front_matter = bool(meta) and not args.no_title_page

    if has_front_matter:
        add_bismillah_page(doc, cfg)                              # page الف (hidden number)
        add_farsi_title_page(doc, meta, cfg)                      # page ب
        add_english_title_page(doc, meta, cfg)                    # page ج
        add_simple_fa_page(doc, "سپاسگزاری", meta.get("acknowledgements"), cfg)   # page د
        add_simple_fa_page(doc, "تقدیم", meta.get("dedication"), cfg)             # page ه
        add_toc_pages(doc, cfg)
        add_abbreviations_page(doc, meta.get("abbreviations"), cfg)
        if meta.get("abstract_fa"):
            add_abstract_page(doc, "چکیده", meta["abstract_fa"], meta.get("abstract_fa_keywords"), cfg, rtl=True)

        set_section_page_numbering(doc.sections[0], fmt="arabicAbjad", start=1)
        add_footer_page_numbers(doc.sections[0], cfg, suppress_first_page=True)

        body_section = doc.add_section(WD_SECTION.NEW_PAGE)
        setup_page(body_section, margins)
        set_section_page_numbering(body_section, fmt="decimal", start=1)
        add_footer_page_numbers(body_section, cfg)
    else:
        set_section_page_numbering(doc.sections[0], fmt="decimal", start=1)
        add_footer_page_numbers(doc.sections[0], cfg)

    if has_front_matter:
        body_text = _strip_body_front_matter(body_text)

    state = {"chapter": 0, "table": 0, "figure": 0, "in_references": False, "ref_counter": 0}
    lint = {"short_paragraphs": [], "long_paragraphs": [], "long_sentences": [], "heading_levels": set(),
            "mixed_percent": [], "mixed_decimals": []}

    # Pre-conversion validation (Collective standards §XVI)
    validation_issues = validate_markdown(body_text)
    print_validation_report(validation_issues)

    convert_markdown_body(doc, body_text, cfg, state, lint)

    if has_front_matter and meta.get("abstract_en"):
        doc.add_page_break()
        add_abstract_page(doc, "Abstract", meta["abstract_en"], meta.get("abstract_en_keywords"), cfg, rtl=False)
        doc.add_page_break()
        add_english_title_page(doc, meta, cfg)

    _register_caption_labels(doc)
    _fix_toc_fields_rtl(doc)

    output_path = Path(args.output_docx)
    doc.save(str(output_path))

    if cfg["_footnotes"]["order"]:
        footnotes_xml = build_footnotes_xml(cfg["_footnotes"], cfg)
        inject_footnotes_part(output_path, footnotes_xml)
        print(f"Injected {len(cfg['_footnotes']['order'])} footnote(s).")

    print(f"Saved: {output_path}")
    print("Reminder: open in Word, select all (Ctrl+A), press F9 to refresh "
          "the Table of Contents / List of Tables / List of Figures.")

    if not args.no_lint:
        print_lint_report(lint)


if __name__ == "__main__":
    main()
