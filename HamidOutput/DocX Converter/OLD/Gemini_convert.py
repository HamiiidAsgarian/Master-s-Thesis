#!/usr/bin/env python3
"""
Gemini_convert.py — Hybrid IAU Thesis Converter

Stage 1: Pre-processing  (Python)    — YAML front matter → Markdown front pages,
                                       Persian punctuation normalization
Stage 2: Compilation     (Pandoc)    — Markdown → .docx with native OMML equations
Stage 3: Post-processing (docx)      — Ardabil fonts, 28pt spacing, table RTL, margins

Usage:
    python Gemini_convert.py <input.md> <template.docx> <output.docx>
"""

import os
import re
import sys
import subprocess

from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

try:
    import yaml
except ImportError:
    yaml = None


# ==========================================================================
# Persian helpers
# ==========================================================================

PERSIAN_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F]")

def is_persian(text: str) -> bool:
    return bool(PERSIAN_RE.search(text))

_PUNCT_MAP = {",": "،", ";": "؛", "?": "؟"}

def normalize_persian_punctuation(text: str) -> str:
    """Replace ASCII punct with Persian equivalents in Persian text only.
    Never touches content inside $...$ or $$...$$."""
    # Protect math segments
    parts = re.split(r"(\$\$[^$]*\$\$|\$[^$]*\$)", text)
    result = []
    for p in parts:
        if p.startswith("$"):
            result.append(p)
        elif is_persian(p):
            for ascii_p, fa_p in _PUNCT_MAP.items():
                p = p.replace(ascii_p, fa_p)
            p = re.sub(r"\s+([،؛؟:.])", r"\1", p)
            p = re.sub(r"([،؛؟:])(?!\s|$)", r"\1 ", p)
            result.append(p)
        else:
            result.append(p)
    return "".join(result)


# ==========================================================================
# YAML front matter
# ==========================================================================

def parse_yaml_frontmatter(md_text: str):
    """Extract YAML front matter and return (meta_dict, body_text)."""
    meta = {}
    body = md_text
    if md_text.startswith("---"):
        end = md_text.find("\n---", 3)
        if end != -1:
            raw = md_text[3:end].strip()
            body = md_text[end + 4:].lstrip()
            if yaml:
                try:
                    meta = yaml.safe_load(raw) or {}
                except Exception:
                    pass
    return meta, body


# ==========================================================================
# Stage 1 — Pre-processing: generate front matter as Markdown
# ==========================================================================

def generate_front_matter_md(meta: dict) -> str:
    """Generate Farsi title page, Bismillah, etc. from YAML metadata."""
    parts = []

    # Bismillah
    parts.append("# به نام خدا\n\n---\n\n")

    # Farsi title page
    parts.append("# صفحه عنوان\n")
    for key in ("university", "branch", "faculty", "degree", "field"):
        val = meta.get(key)
        if val:
            parts.append(f"{val}\n")
    parts.append("\n**عنوان**\n\n")
    if meta.get("title_fa"):
        parts.append(f"{meta['title_fa']}\n\n")
    if meta.get("supervisor"):
        parts.append(f"**استاد راهنما**\n\n{meta['supervisor']}\n\n")
    if meta.get("advisor"):
        parts.append(f"**استاد مشاور**\n\n{meta['advisor']}\n\n")
    if meta.get("author"):
        parts.append(f"**نگارش**\n\n{meta['author']}\n\n")
    if meta.get("defense_date"):
        parts.append(f"{meta['defense_date']}\n")

    parts.append("\n---\n\n")
    return "\n".join(parts)


# ==========================================================================
# Stage 1 — Punctuation normalization on full body
# ==========================================================================

def normalize_body_punctuation(text: str) -> str:
    lines = text.split("\n")
    result = []
    for line in lines:
        stripped = line.strip()
        # Skip code blocks, math blocks, table separators
        if stripped.startswith("```") or stripped.startswith("$$") or re.match(r"^\|[\s:|-]+\|$", stripped):
            result.append(line)
        else:
            result.append(normalize_persian_punctuation(line))
    return "\n".join(result)


# ==========================================================================
# Stage 2 — Pandoc compilation
# ==========================================================================

def compile_with_pandoc(markdown_text: str, template_docx: str, output_path: str):
    """Pass enriched markdown via stdin to pandoc."""
    cmd = [
        "pandoc",
        "-o", output_path,
        f"--reference-doc={template_docx}",
        "--metadata", "dir=rtl",
        "--metadata", "lang=fa",
        "--from=markdown",
    ]
    try:
        subprocess.run(cmd, input=markdown_text, capture_output=True,
                       text=True, check=True, encoding="utf-8")
    except subprocess.CalledProcessError as e:
        print(f"Pandoc failed:\n{e.stderr}", file=sys.stderr)
        sys.exit(1)


# ==========================================================================
# Stage 3 — Post-processing (python-docx formatting)
# ==========================================================================

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

TBLPR_ORDER = [
    "tblCnfStyle", "tblStyle", "tblpPr", "tblBorders", "shd",
    "tblLayout", "tblCellMar", "tblLook", "bidiVisual",
]


def _localname(el):
    return el.tag.split("}")[-1]


def insert_ordered(parent, new_child, order):
    tag = _localname(new_child)
    if tag not in order:
        parent.append(new_child)
        return
    idx = order.index(tag)
    for sibling in parent:
        sib_tag = _localname(sibling)
        if sib_tag in order and order.index(sib_tag) > idx:
            sibling.addprevious(new_child)
            return
    parent.append(new_child)


def get_or_create(parent, tag_name, order):
    el = parent.find(qn(f"w:{tag_name}"))
    if el is None:
        el = OxmlElement(f"w:{tag_name}")
        insert_ordered(parent, el, order)
    return el


def set_run_properties(run, fa_font, en_font, size_pt, bold_flag=None):
    rPr = run._r.get_or_add_rPr()
    rFonts = get_or_create(rPr, "rFonts", RPR_ORDER)
    rFonts.set(qn("w:ascii"), en_font)
    rFonts.set(qn("w:hAnsi"), en_font)
    rFonts.set(qn("w:cs"), fa_font)
    if size_pt is not None:
        run.font.size = Pt(size_pt)
        sz = get_or_create(rPr, "sz", RPR_ORDER)
        sz.set(qn("w:val"), str(int(size_pt * 2)))
        szCs = get_or_create(rPr, "szCs", RPR_ORDER)
        szCs.set(qn("w:val"), str(int(size_pt * 2)))
    if bold_flag is not None:
        run.bold = bold_flag
        bCs = get_or_create(rPr, "bCs", RPR_ORDER)
        bCs.set(qn("w:val"), "1" if bold_flag else "0")


def set_paragraph_rtl(p, rtl=True):
    pPr = p._p.get_or_add_pPr()
    bidi = get_or_create(pPr, "bidi", PPR_ORDER)
    bidi.set(qn("w:val"), "1" if rtl else "0")


def apply_ardabil_formatting(doc: Document):
    # Page setup — Ardabil: 3/3/3/2 cm on A4, applied to ALL sections
    for section in doc.sections:
        section.page_width = Cm(21)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(3)
        section.bottom_margin = Cm(3)
        section.right_margin = Cm(3)
        section.left_margin = Cm(2)
        section.header_distance = Cm(1.5)
        section.footer_distance = Cm(1.5)

    for para in doc.paragraphs:
        style_name = para.style.name.lower()

        para.paragraph_format.space_before = Pt(0)
        para.paragraph_format.space_after = Pt(0)
        para.paragraph_format.widow_control = True
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        set_paragraph_rtl(para, True)

        if 'heading 1' in style_name or 'title' in style_name:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            para.paragraph_format.line_spacing = Pt(32)
            para.paragraph_format.page_break_before = True
            for run in para.runs:
                set_run_properties(run, "Lotus Bold", "Times New Roman", 25, bold_flag=True)

        elif 'heading 2' in style_name:
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT
            para.paragraph_format.line_spacing = Pt(28)
            for run in para.runs:
                set_run_properties(run, "Lotus Bold", "Times New Roman", 14, bold_flag=True)

        elif 'heading 3' in style_name:
            para.alignment = WD_ALIGN_PARAGRAPH.LEFT
            para.paragraph_format.line_spacing = Pt(24)
            for run in para.runs:
                set_run_properties(run, "Lotus Bold", "Times New Roman", 12, bold_flag=True)

        elif 'caption' in style_name:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in para.runs:
                set_run_properties(run, "Lotus Bold", "Times New Roman", 11, bold_flag=True)

        else:
            para.paragraph_format.line_spacing = Pt(28)
            para.paragraph_format.first_line_indent = Cm(1)
            for run in para.runs:
                set_run_properties(run, "Lotus Thin", "Times New Roman", 14, bold_flag=False)

    # Caption detection — convert جدول/شکل bold paragraphs to Word Caption style
    _caption_pat = re.compile(r"^(شکل|جدول)\s+\d+-\d+:")
    try:
        cap_style = doc.styles["Caption"]
    except KeyError:
        cap_style = None
    for para in doc.paragraphs:
        text = para.text.strip()
        if _caption_pat.match(text):
            if cap_style is not None:
                para.style = cap_style
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            para.paragraph_format.line_spacing = Pt(20)
            para.paragraph_format.first_line_indent = Cm(0)
            for run in para.runs:
                set_run_properties(run, "Lotus Bold", "Times New Roman", 11, bold_flag=True)

    # Table RTL
    for table in doc.tables:
        get_or_create(table._tbl.tblPr, "bidiVisual", TBLPR_ORDER)
        for row in table.rows:
            trPr = row._tr.get_or_add_trPr()
            cantSplit = OxmlElement("w:cantSplit")
            trPr.append(cantSplit)

    # Footnotes — apply Ardabil font to all runs in the footnotes part
    try:
        footnotes_part = doc.part.package.part_related_by(
            "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes"
        )
        from lxml import etree
        fn_tree = etree.parse(footnotes_part.blob)
        NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        for fn in fn_tree.findall(".//w:footnote", NS):
            fn_id = fn.get(qn("w:id"))
            if fn_id in ("0", "-1"):
                continue
            for r in fn.findall(".//w:r", NS):
                rPr = r.find("w:rPr", NS)
                if rPr is None:
                    rPr = etree.SubElement(r, qn("w:rPr"))
                rFonts = rPr.find("w:rFonts", NS)
                if rFonts is None:
                    rFonts = etree.SubElement(rPr, qn("w:rFonts"))
                rFonts.set(qn("w:ascii"), "Times New Roman")
                rFonts.set(qn("w:hAnsi"), "Times New Roman")
                rFonts.set(qn("w:cs"), "Lotus")
                sz = rPr.find("w:sz", NS)
                if sz is None:
                    sz = etree.SubElement(rPr, qn("w:sz"))
                sz.set(qn("w:val"), "22")  # 11pt in half-points
                szCs = rPr.find("w:szCs", NS)
                if szCs is None:
                    szCs = etree.SubElement(rPr, qn("w:szCs"))
                szCs.set(qn("w:val"), "22")
        footnotes_part._blob = etree.tostring(fn_tree, xml_declaration=True, encoding="UTF-8", standalone=True)
    except Exception:
        pass  # no footnotes part = no footnotes to format


# ==========================================================================
# Pipeline
# ==========================================================================

def run_pipeline(markdown_in, template_docx, output_docx):
    with open(markdown_in, "r", encoding="utf-8") as f:
        raw_md = f.read()

    # ---- Stage 1: Pre-processing ---------------------------------------
    print("Stage 1: Pre-processing (YAML → Markdown front matter)...")
    meta, body = parse_yaml_frontmatter(raw_md)
    front_matter = generate_front_matter_md(meta)
    body = normalize_body_punctuation(body)
    enriched_md = front_matter + "\n\n" + body

    # ---- Stage 2: Pandoc compilation -----------------------------------
    print("Stage 2: Pandoc compilation...")
    intermediate = "temp_intermediate.docx"
    compile_with_pandoc(enriched_md, template_docx, intermediate)

    # ---- Stage 3: Post-processing --------------------------------------
    print("Stage 3: Applying Ardabil formatting rules...")
    doc = Document(intermediate)
    apply_ardabil_formatting(doc)
    doc.save(output_docx)
    os.remove(intermediate)

    print(f"Done: {output_docx}")
    print("Note: Open in Word, press Ctrl+A then F9 to refresh TOC / List of Tables / List of Figures. Captions are auto-styled for Word's Table of Figures.")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python Gemini_convert.py <input.md> <template.docx> <output.docx>")
        sys.exit(1)
    run_pipeline(sys.argv[1], sys.argv[2], sys.argv[3])
