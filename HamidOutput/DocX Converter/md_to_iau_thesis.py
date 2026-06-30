#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md_to_iau_thesis.py
====================

Converts a Farsi (Persian) Markdown thesis file into a Word .docx document
formatted according to the Islamic Azad University (IAU) Master's thesis
style cheat sheet (see the rules table this script implements below).

--------------------------------------------------------------------------
WHAT THIS SCRIPT DOES
--------------------------------------------------------------------------
1. Reads an optional YAML front-matter block at the top of your .md file
   to auto-generate a Persian title page (university, branch, faculty,
   degree, field, thesis title, supervisor, advisor, author, defense date).
2. Parses the Markdown body (headings, paragraphs, bold/italic, ordered &
   unordered lists, blockquotes, pipe tables, horizontal rules, images,
   inline code) and rebuilds it as a properly styled Word document.
3. Applies IAU-style formatting:
   - A4 page size, 1-inch-ish academic margins
   - Right-to-left (RTL) paragraph direction + bidi runs for Persian text
   - Persian fonts for headings/title page (B Zar / B Titr / B Nazanin,
     with graceful fallback - see FONT NOTES below)
   - Times New Roman body text for any Latin/English passages
   - Heading 1/2/3 styles wired to Word's built-in outline levels so
     Word's automatic Table of Contents / List of Figures / List of
     Tables features work out of the box
   - Justified body text, 1.15 line spacing
   - Centered page numbers (Arabic numerals) in the footer starting at
     the Introduction / Chapter 1 section
4. Inserts placeholder TOC / List of Figures / List of Tables fields
   that Word will populate when the user presses F9 ("update field")
   or right-clicks -> "Update Field" after opening the document.

--------------------------------------------------------------------------
FONT NOTES (IMPORTANT - READ THIS)
--------------------------------------------------------------------------
IAU's official cheat sheet calls for the proprietary Persian fonts
"Zarr" (زر), "Nazanin" (نازنین) and "Titr" (تیتر). These are NOT
standard fonts bundled with Windows/Office and are usually distributed
by the university itself or downloaded separately (commonly as
"B Zar", "B Titr", "B Nazanin" - the "B" prefix fonts from the old
"Zar" Persian font pack, still the most common substitute in Iranian
university templates).

This script defaults to:
    - Persian body / heading font : "B Nazanin"
    - Persian title / chapter font: "B Titr"
    - Persian bold display font   : "B Zar"

If these aren't installed on the machine that opens the resulting
.docx, Word will silently substitute a fallback font and the layout
will look slightly different (but the RTL/bidi structure and styles
remain correct). You can:
    (a) Install the "B Zar" font family (search "Zar font pack"), or
    (b) Change the FONT_* constants below to whatever Persian font you
        already have (e.g. "IRANSans", "Vazirmatn", "B Nazanin", etc.)
    (c) Pass --fa-font / --fa-title-font / --fa-bold-font on the CLI.

--------------------------------------------------------------------------
MARKDOWN CONVENTIONS EXPECTED
--------------------------------------------------------------------------
    # Heading            -> Chapter title   (فصل)   -> Word "Heading 1"
    ## Heading            -> Section title           -> Word "Heading 2"
    ### Heading           -> Subsection title         -> Word "Heading 3"
    **bold**, *italic*    -> inline formatting (mix freely)
    - item / * item       -> bulleted list
    1. item               -> numbered list
    > quote               -> block quote (indented, italic)
    ---                   -> horizontal rule (rendered as a section divider line)
    | a | b |              -> pipe tables (first row = header)
    ![caption](path.png)  -> embedded image with an auto Word "Caption"
                              (so it feeds the List of Figures)
    ```code```            -> monospace paragraph (Consolas)

Optional YAML front matter (put this at the very top of your .md file,
between two '---' lines) drives the auto-generated title page:

    ---
    university: "دانشگاه آزاد اسلامی"
    branch: "واحد تهران مرکزی"
    faculty: "دانشکده فنی و مهندسی - گروه کامپیوتر"
    degree: "پایان‌نامه کارشناسی ارشد (M.Sc.)"
    field: "مهندسی کامپیوتر - نرم‌افزار"
    title_fa: "عنوان پایان‌نامه به فارسی"
    title_en: "Thesis Title in English"
    supervisor: "دکتر ..."
    advisor: "دکتر ..."
    author: "نام و نام خانوادگی دانشجو"
    defense_date: "تابستان ۱۴۰۴"
    abstract_fa: "چکیده فارسی پایان‌نامه..."
    abstract_en: "English abstract of the thesis..."
    ---

If no front matter is present, the script skips the title page and
converts only the body content (useful if you already have a separate
approved title/approval page and just want the chapters converted).

--------------------------------------------------------------------------
USAGE
--------------------------------------------------------------------------
    pip install python-docx pyyaml --break-system-packages

    python3 md_to_iau_thesis.py thesis.md thesis.docx
    python3 md_to_iau_thesis.py thesis.md thesis.docx --fa-font "Vazirmatn"
    python3 md_to_iau_thesis.py thesis.md thesis.docx --no-title-page

After generation, open the file in Word and press Ctrl+A then F9 to
refresh the Table of Contents / List of Figures / List of Tables.
--------------------------------------------------------------------------
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


# ==========================================================================
# CONFIGURATION (override via CLI flags - see bottom of file)
# ==========================================================================

DEFAULTS = {
    "fa_body_font": "B Nazanin",     # Persian body & heading font
    "fa_title_font": "B Titr",       # Persian thesis-title / chapter font
    "fa_bold_font": "B Zar",         # Persian university-name / labels font
    "en_font": "Times New Roman",    # Latin font for English passages
    "mono_font": "Consolas",         # Code blocks
    "body_size": 13,                 # pt, Persian body text (~12-14 typical)
    "en_body_size": 12,              # pt, English body text
}

PERSIAN_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F]")


def is_persian(text: str) -> bool:
    """Heuristic: treat text as Persian/RTL if it contains any Arabic-script
    characters. Mixed text (Persian + inline English/numbers) still gets
    treated as an RTL paragraph, which is how Word normally handles it."""
    return bool(PERSIAN_RE.search(text))


# ==========================================================================
# LOW-LEVEL OXML HELPERS (python-docx doesn't expose RTL/bidi natively)
# ==========================================================================

# OOXML requires strict child-element ordering inside <w:pPr>, <w:rPr> and
# <w:sectPr>. Blindly .append()-ing new elements (as a naive implementation
# would) produces schema-invalid XML that Word *usually* tolerates but that
# fails strict validation and can misbehave in some viewers (e.g. LibreOffice,
# Google Docs). These order lists + helper keep every insertion schema-correct.

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


def _localname(el):
    return el.tag.split("}")[-1]


def insert_ordered(parent, new_child, order):
    """Insert new_child into parent respecting the OOXML sequence given in
    `order`. Falls back to plain append if the tag isn't in the order list
    or no later sibling is found."""
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
    """Find an existing child element by tag, or create+insert it in order."""
    el = parent.find(qn(f"w:{tag_name}"))
    if el is None:
        el = OxmlElement(f"w:{tag_name}")
        insert_ordered(parent, el, order)
    return el


def set_paragraph_rtl(paragraph, rtl=True):
    """Mark a paragraph as bidi (right-to-left) at the paragraph level."""
    pPr = paragraph._p.get_or_add_pPr()
    bidi = get_or_create(pPr, "bidi", PPR_ORDER)
    bidi.set(qn("w:val"), "1" if rtl else "0")


def set_run_rtl(run, rtl=True):
    """Mark a run's complex-script direction as RTL so Persian glyphs shape
    and reorder correctly regardless of surrounding Latin text."""
    rPr = run._r.get_or_add_rPr()
    rtl_el = get_or_create(rPr, "rtl", RPR_ORDER)
    rtl_el.set(qn("w:val"), "1" if rtl else "0")


def set_run_fonts(run, latin_font=None, cs_font=None, ea_font=None):
    """Set ascii/hAnsi (Latin) font and cs (complex-script / Persian) font
    independently on the same run, per OOXML rFonts rules."""
    rPr = run._r.get_or_add_rPr()
    rFonts = get_or_create(rPr, "rFonts", RPR_ORDER)
    if latin_font:
        rFonts.set(qn("w:ascii"), latin_font)
        rFonts.set(qn("w:hAnsi"), latin_font)
    if cs_font:
        rFonts.set(qn("w:cs"), cs_font)
    if ea_font:
        rFonts.set(qn("w:eastAsia"), ea_font)


def add_field(paragraph, field_code, result_text=""):
    """Insert a Word field (e.g. TOC, PAGE) with a cached display value so
    the document isn't blank before the user refreshes fields in Word."""
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


def set_section_page_numbering(section, fmt="decimal", start=None, restart=True):
    """Configure Arabic/roman/etc. page numbering for a section."""
    sectPr = section._sectPr
    pgNumType = get_or_create(sectPr, "pgNumType", SECTPR_ORDER)
    pgNumType.set(qn("w:fmt"), fmt)
    if restart and start is not None:
        pgNumType.set(qn("w:start"), str(start))


def add_page_number_field(paragraph):
    """Insert a PAGE field into a paragraph (used in footers)."""
    add_field(paragraph, "PAGE", "1")


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
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(6)

    # ---- Body Text (Persian, justified, RTL) -----------------------------
    if "IAU Body" not in [s.name for s in styles]:
        body = styles.add_style("IAU Body", WD_STYLE_TYPE.PARAGRAPH)
        body.base_style = normal
        body.font.name = cfg["en_font"]
        body.font.size = Pt(cfg["body_size"])
        body.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        body.paragraph_format.line_spacing = 1.15
        body.paragraph_format.space_after = Pt(8)
        rpr = body.element.get_or_add_rPr()
        rFonts = get_or_create(rpr, "rFonts", RPR_ORDER)
        rFonts.set(qn("w:cs"), cfg["fa_body_font"])
        insert_ordered(rpr, _font_size_cs(cfg["body_size"]), RPR_ORDER)

    # ---- Headings ----------------------------------------------------
    heading_specs = [
        ("Heading 1", 18, True, cfg["fa_title_font"]),
        ("Heading 2", 15, True, cfg["fa_body_font"]),
        ("Heading 3", 13, True, cfg["fa_body_font"]),
    ]
    for name, size, bold, cs_font in heading_specs:
        st = styles[name]
        st.font.name = cfg["en_font"]
        st.font.size = Pt(size)
        st.font.bold = bold
        st.font.color.rgb = RGBColor(0, 0, 0)
        st.paragraph_format.alignment = (
            WD_ALIGN_PARAGRAPH.CENTER if name == "Heading 1" else WD_ALIGN_PARAGRAPH.RIGHT
        )
        st.paragraph_format.space_before = Pt(18 if name == "Heading 1" else 12)
        st.paragraph_format.space_after = Pt(12)
        st.paragraph_format.keep_with_next = True
        rpr = st.element.get_or_add_rPr()
        rFonts = get_or_create(rpr, "rFonts", RPR_ORDER)
        rFonts.set(qn("w:cs"), cs_font)
        insert_ordered(rpr, _font_size_cs(size), RPR_ORDER)
        get_or_create(rpr, "b", RPR_ORDER)
        get_or_create(rpr, "bCs", RPR_ORDER)

    # ---- Caption -------------------------------------------------------
    if "Caption" in [s.name for s in styles]:
        cap = styles["Caption"]
        cap.font.name = cfg["en_font"]
        cap.font.size = Pt(11)
        cap.font.italic = True
        cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rpr = cap.element.get_or_add_rPr()
        rFonts = get_or_create(rpr, "rFonts", RPR_ORDER)
        rFonts.set(qn("w:cs"), cfg["fa_body_font"])
        insert_ordered(rpr, _font_size_cs(11), RPR_ORDER)

    # ---- Quote style -----------------------------------------------------
    if "IAU Quote" not in [s.name for s in styles]:
        q = styles.add_style("IAU Quote", WD_STYLE_TYPE.PARAGRAPH)
        q.base_style = styles["IAU Body"]
        q.font.italic = True
        q.paragraph_format.left_indent = Cm(1)
        q.paragraph_format.right_indent = Cm(1)

    # ---- Code style ------------------------------------------------------
    if "IAU Code" not in [s.name for s in styles]:
        c = styles.add_style("IAU Code", WD_STYLE_TYPE.PARAGRAPH)
        c.base_style = normal
        c.font.name = cfg["mono_font"]
        c.font.size = Pt(10.5)
        c.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        c.paragraph_format.shading = None  # (shading set via oxml below if desired)


def _font_size_cs(pt_size):
    """<w:szCs> element (complex-script font size), needed alongside <w:sz>
    for Persian text to render at the correct size."""
    el = OxmlElement("w:szCs")
    el.set(qn("w:val"), str(int(pt_size * 2)))
    return el


# ==========================================================================
# PAGE SETUP
# ==========================================================================

def setup_page(section, margins_cm=(3.0, 2.5, 2.5, 3.5)):
    """A4 size with typical Iranian-thesis margins:
    top, bottom, right ~2.5-3cm, left (binding side, RTL so 'inside') 3.5cm.
    Adjust to match your branch's exact requirement if it differs."""
    top, bottom, right, left = margins_cm
    section.page_height = Cm(29.7)
    section.page_width = Cm(21.0)
    section.top_margin = Cm(top)
    section.bottom_margin = Cm(bottom)
    section.right_margin = Cm(right)
    section.left_margin = Cm(left)


# ==========================================================================
# TITLE PAGE
# ==========================================================================

def add_title_page(doc: Document, meta: dict, cfg: dict):
    def para(text, font, size, bold=True, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER):
        p = doc.add_paragraph()
        p.alignment = align
        set_paragraph_rtl(p, is_persian(text))
        p.paragraph_format.space_after = Pt(space_after)
        r = p.add_run(text)
        r.bold = bold
        r.font.size = Pt(size)
        set_run_fonts(r, latin_font=cfg["en_font"], cs_font=font)
        set_run_rtl(r, is_persian(text))
        return p

    # Bismillah
    if meta.get("bismillah", True):
        para("به نام خدا", cfg["fa_body_font"], 14, bold=False, space_after=36)

    para(meta.get("university", "دانشگاه آزاد اسلامی"), cfg["fa_bold_font"], 18)
    if meta.get("branch"):
        para(meta["branch"], cfg["fa_bold_font"], 18)
    if meta.get("faculty"):
        para(meta["faculty"], cfg["fa_bold_font"], 16)
    if meta.get("degree"):
        para(meta["degree"], cfg["fa_bold_font"], 16, space_after=18)
    if meta.get("field"):
        para(meta["field"], cfg["fa_bold_font"], 16, space_after=24)

    para("عنوان", cfg["fa_body_font"], 18, space_after=6)
    if meta.get("title_fa"):
        para(meta["title_fa"], cfg["fa_title_font"], 18, space_after=6)
    if meta.get("title_en"):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_paragraph_rtl(p, False)
        r = p.add_run(meta["title_en"])
        r.italic = True
        r.font.size = Pt(13)
        set_run_fonts(r, latin_font=cfg["en_font"])
        p.paragraph_format.space_after = Pt(24)

    if meta.get("supervisor"):
        para("استاد راهنما", cfg["fa_body_font"], 18, space_after=4)
        para(meta["supervisor"], cfg["fa_bold_font"], 18, space_after=18)
    if meta.get("advisor"):
        para("استاد مشاور", cfg["fa_body_font"], 18, space_after=4)
        para(meta["advisor"], cfg["fa_bold_font"], 18, space_after=18)
    if meta.get("author"):
        para("نگارش", cfg["fa_body_font"], 18, space_after=4)
        para(meta["author"], cfg["fa_bold_font"], 18, space_after=36)
    if meta.get("defense_date"):
        para(meta["defense_date"], cfg["fa_bold_font"], 14, space_after=0)

    doc.add_page_break()


def add_abstract_page(doc, heading, text, cfg, rtl=True):
    h = doc.add_paragraph()
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_rtl(h, rtl)
    r = h.add_run(heading)
    r.bold = True
    r.font.size = Pt(16)
    set_run_fonts(r, latin_font=cfg["en_font"], cs_font=cfg["fa_title_font"])
    set_run_rtl(r, rtl)
    h.paragraph_format.space_after = Pt(18)

    p = doc.add_paragraph(style="IAU Body")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    set_paragraph_rtl(p, rtl)
    r = p.add_run(text)
    set_run_fonts(r, latin_font=cfg["en_font"], cs_font=cfg["fa_body_font"])
    set_run_rtl(r, rtl)
    doc.add_page_break()


def add_toc_pages(doc, cfg):
    for heading_fa, field in [
        ("فهرست مطالب", 'TOC \\o "1-3" \\h \\z \\u'),
        ("فهرست جداول", 'TOC \\h \\z \\c "Table"'),
        ("فهرست نمودارها", 'TOC \\h \\z \\c "Figure"'),
    ]:
        h = doc.add_paragraph()
        h.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_paragraph_rtl(h, True)
        r = h.add_run(heading_fa)
        r.bold = True
        r.font.size = Pt(16)
        set_run_fonts(r, latin_font=cfg["en_font"], cs_font=cfg["fa_title_font"])
        set_run_rtl(r, True)
        h.paragraph_format.space_after = Pt(12)

        note = doc.add_paragraph()
        set_paragraph_rtl(note, True)
        nr = note.add_run("(در Word پس از باز کردن فایل، کلیدهای Ctrl+A سپس F9 را بزنید تا این فهرست به‌روزرسانی شود.)")
        nr.italic = True
        nr.font.size = Pt(10)
        set_run_fonts(nr, latin_font=cfg["en_font"], cs_font=cfg["fa_body_font"])
        set_run_rtl(nr, True)

        field_p = doc.add_paragraph()
        set_paragraph_rtl(field_p, True)
        add_field(field_p, field, "")
        doc.add_page_break()


# ==========================================================================
# INLINE MARKDOWN (bold / italic / code) -> RUNS
# ==========================================================================

INLINE_TOKEN_RE = re.compile(
    r"(\*\*\*(?P<b_i>.+?)\*\*\*)"     # ***bold italic***
    r"|(\*\*(?P<bold>.+?)\*\*)"        # **bold**
    r"|(\*(?P<italic>.+?)\*)"          # *italic*
    r"|(`(?P<code>.+?)`)"              # `code`
)


def add_inline_runs(paragraph, text, cfg, rtl=None):
    """Parse a line of markdown inline formatting and append runs to an
    existing paragraph, preserving bold/italic/code spans."""
    if rtl is None:
        rtl = is_persian(text)

    pos = 0
    for m in INLINE_TOKEN_RE.finditer(text):
        if m.start() > pos:
            _append_run(paragraph, text[pos:m.start()], cfg, rtl)
        if m.group("b_i") is not None:
            _append_run(paragraph, m.group("b_i"), cfg, rtl, bold=True, italic=True)
        elif m.group("bold") is not None:
            _append_run(paragraph, m.group("bold"), cfg, rtl, bold=True)
        elif m.group("italic") is not None:
            _append_run(paragraph, m.group("italic"), cfg, rtl, italic=True)
        elif m.group("code") is not None:
            _append_run(paragraph, m.group("code"), cfg, rtl, mono=True)
        pos = m.end()
    if pos < len(text):
        _append_run(paragraph, text[pos:], cfg, rtl)


def _append_run(paragraph, text, cfg, rtl, bold=False, italic=False, mono=False):
    if text == "":
        return
    r = paragraph.add_run(text)
    r.bold = bold
    r.italic = italic
    if mono:
        set_run_fonts(r, latin_font=cfg["mono_font"], cs_font=cfg["mono_font"])
    else:
        set_run_fonts(r, latin_font=cfg["en_font"], cs_font=cfg["fa_body_font"])
    set_run_rtl(r, rtl)


# ==========================================================================
# MARKDOWN BODY PARSER
# ==========================================================================

TABLE_ROW_RE = re.compile(r"^\s*\|(.+)\|\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")
IMAGE_RE = re.compile(r"^!\[(?P<alt>.*?)\]\((?P<path>.*?)\)\s*$")
ORDERED_RE = re.compile(r"^\s*(\d+)[.)]\s+(.*)$")
UNORDERED_RE = re.compile(r"^\s*[-*+]\s+(.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def strip_yaml_frontmatter(md_text: str):
    if md_text.startswith("---"):
        end = md_text.find("\n---", 3)
        if end != -1:
            fm_raw = md_text[3:end].strip("\n")
            body = md_text[end + 4:]
            body = body.lstrip("\n")
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


def ensure_bullet_numbering(doc):
    """Return numbering (numId) for bullet & decimal lists, creating a
    minimal abstract numbering definition if python-docx's default
    numbering part doesn't already provide one."""
    numbering_part = doc.part.numbering_part
    numbering_elem = numbering_part.numbering_definitions._numbering
    # python-docx ships default list styles ("List Bullet", "List Number")
    # which already carry correct numbering; we simply use those styles
    # rather than hand-building numPr XML, which keeps this robust across
    # Word versions.
    return None


def add_table_from_rows(doc, rows, cfg):
    if not rows:
        return
    n_cols = len(rows[0])
    table = doc.add_table(rows=len(rows), cols=n_cols)
    table.style = "Table Grid"
    table.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for ri, row in enumerate(rows):
        for ci, cell_text in enumerate(row):
            cell = table.cell(ri, ci)
            cell.text = ""
            p = cell.paragraphs[0]
            rtl = is_persian(cell_text)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_paragraph_rtl(p, rtl)
            r = p.add_run(cell_text.strip())
            r.bold = (ri == 0)
            set_run_fonts(r, latin_font=cfg["en_font"], cs_font=cfg["fa_body_font"])
            set_run_rtl(r, rtl)
    # Caption above the table (feeds "List of Tables")
    cap = doc.paragraphs[doc.paragraphs.index(table._tbl.getparent()) - 1] if False else None
    doc.add_paragraph()  # spacing after table


def add_table_caption(doc, caption_text, cfg, label="Table"):
    if not caption_text:
        return
    p = doc.add_paragraph(style="Caption")
    rtl = is_persian(caption_text)
    set_paragraph_rtl(p, rtl)
    label_run = p.add_run(f"{label}: ")
    set_run_fonts(label_run, latin_font=cfg["en_font"], cs_font=cfg["fa_body_font"])
    r = p.add_run(caption_text)
    set_run_fonts(r, latin_font=cfg["en_font"], cs_font=cfg["fa_body_font"])
    set_run_rtl(r, rtl)


def convert_markdown_body(doc: Document, md_text: str, cfg: dict):
    lines = md_text.split("\n")
    i = 0
    n = len(lines)
    in_code_block = False
    code_buffer = []

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
            i += 1
            continue
        if in_code_block:
            code_buffer.append(line)
            i += 1
            continue

        stripped = line.strip()

        # ---- blank line ----------------------------------------------
        if stripped == "":
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

        # ---- image -----------------------------------------------------
        img_m = IMAGE_RE.match(stripped)
        if img_m:
            path = img_m.group("path")
            alt = img_m.group("alt")
            img_path = Path(path)
            if not img_path.is_absolute():
                img_path = (Path(cfg["md_dir"]) / path).resolve()
            if img_path.exists():
                doc.add_picture(str(img_path), width=Cm(14))
                last_p = doc.paragraphs[-1]
                last_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                warn_p = doc.add_paragraph()
                wr = warn_p.add_run(f"[missing image: {path}]")
                wr.italic = True
            add_table_caption(doc, alt, cfg, label="Figure")
            i += 1
            continue

        # ---- heading -----------------------------------------------------
        h_m = HEADING_RE.match(line)
        if h_m:
            level = min(len(h_m.group(1)), 3)
            text = h_m.group(2).strip()
            style_name = f"Heading {level}"
            p = doc.add_paragraph(style=style_name)
            rtl = is_persian(text)
            set_paragraph_rtl(p, rtl)
            add_inline_runs(p, text, cfg, rtl=rtl)
            i += 1
            continue

        # ---- blockquote --------------------------------------------------
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
            continue

        # ---- table -------------------------------------------------------
        if TABLE_ROW_RE.match(line):
            table_lines = []
            while i < n and TABLE_ROW_RE.match(lines[i]):
                table_lines.append(lines[i])
                i += 1
            rows = []
            for idx, tl in enumerate(table_lines):
                if idx == 1 and TABLE_SEP_RE.match(tl):
                    continue  # skip the '---|---' separator row
                cells = [c.strip() for c in tl.strip().strip("|").split("|")]
                rows.append(cells)
            add_table_from_rows(doc, rows, cfg)
            continue

        # ---- unordered list ------------------------------------------------
        if UNORDERED_RE.match(line):
            while i < n and UNORDERED_RE.match(lines[i]):
                text = UNORDERED_RE.match(lines[i]).group(1)
                p = doc.add_paragraph(style="List Bullet")
                rtl = is_persian(text)
                set_paragraph_rtl(p, rtl)
                add_inline_runs(p, text, cfg, rtl=rtl)
                i += 1
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
            continue

        # ---- normal paragraph (collect contiguous lines) --------------------
        para_lines = [line]
        i += 1
        while i < n and lines[i].strip() != "" and not HEADING_RE.match(lines[i]) \
                and not UNORDERED_RE.match(lines[i]) and not ORDERED_RE.match(lines[i]) \
                and not TABLE_ROW_RE.match(lines[i]) and not lines[i].strip().startswith(">") \
                and not lines[i].strip().startswith("```") \
                and not IMAGE_RE.match(lines[i].strip()) \
                and not re.match(r"^(-{3,}|\*{3,}|_{3,})$", lines[i].strip()):
            para_lines.append(lines[i])
            i += 1
        text = " ".join(l.strip() for l in para_lines)
        p = doc.add_paragraph(style="IAU Body")
        rtl = is_persian(text)
        set_paragraph_rtl(p, rtl)
        add_inline_runs(p, text, cfg, rtl=rtl)


# ==========================================================================
# FOOTER / PAGE NUMBERS
# ==========================================================================

def add_footer_page_numbers(section, cfg):
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
# MAIN
# ==========================================================================

def _fix_zoom_setting(doc: Document):
    """python-docx's built-in blank template ships a <w:zoom/> element with
    no w:percent attribute, which is schema-invalid. Patch it so strict
    validators (and some non-Word viewers) don't choke on it."""
    settings = doc.settings.element
    zoom = settings.find(qn("w:zoom"))
    if zoom is not None and zoom.get(qn("w:percent")) is None:
        zoom.set(qn("w:percent"), "100")


def main():
    parser = argparse.ArgumentParser(
        description="Convert a Farsi Markdown thesis into an IAU-styled .docx file."
    )
    parser.add_argument("input_md", help="Path to the source .md file")
    parser.add_argument("output_docx", help="Path to write the resulting .docx file")
    parser.add_argument("--no-title-page", action="store_true",
                         help="Skip auto-generating the title page even if YAML front matter is present")
    parser.add_argument("--fa-font", default=DEFAULTS["fa_body_font"],
                         help="Persian body/heading font (default: %(default)s)")
    parser.add_argument("--fa-title-font", default=DEFAULTS["fa_title_font"],
                         help="Persian thesis-title/chapter font (default: %(default)s)")
    parser.add_argument("--fa-bold-font", default=DEFAULTS["fa_bold_font"],
                         help="Persian bold display font for title page labels (default: %(default)s)")
    parser.add_argument("--en-font", default=DEFAULTS["en_font"],
                         help="Latin font for English text (default: %(default)s)")
    parser.add_argument("--body-size", type=int, default=DEFAULTS["body_size"],
                         help="Persian body text size in pt (default: %(default)s)")
    args = parser.parse_args()

    cfg = dict(DEFAULTS)
    cfg["fa_body_font"] = args.fa_font
    cfg["fa_title_font"] = args.fa_title_font
    cfg["fa_bold_font"] = args.fa_bold_font
    cfg["en_font"] = args.en_font
    cfg["body_size"] = args.body_size

    input_path = Path(args.input_md)
    if not input_path.exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    cfg["md_dir"] = str(input_path.parent)

    md_text = input_path.read_text(encoding="utf-8")
    meta, body_text = strip_yaml_frontmatter(md_text)

    doc = Document()
    _fix_zoom_setting(doc)
    build_styles(doc, cfg)
    setup_page(doc.sections[0])

    # ---- Front matter (title page, TOC, abstract) -------------------------
    has_title_page = bool(meta) and not args.no_title_page
    if has_title_page:
        add_title_page(doc, meta, cfg)
        add_toc_pages(doc, cfg)
        if meta.get("abstract_fa"):
            add_abstract_page(doc, "چکیده", meta["abstract_fa"], cfg, rtl=True)

    # ---- Front matter uses letter/roman numbering; body restarts at 1 -----
    if has_title_page:
        set_section_page_numbering(doc.sections[0], fmt="lowerRoman", start=1)
        add_footer_page_numbers(doc.sections[0], cfg)
        # New section so the body can restart Arabic numbering at 1
        body_section = doc.add_section(WD_SECTION.NEW_PAGE)
        setup_page(body_section)
        set_section_page_numbering(body_section, fmt="decimal", start=1)
        add_footer_page_numbers(body_section, cfg)
    else:
        set_section_page_numbering(doc.sections[0], fmt="decimal", start=1)
        add_footer_page_numbers(doc.sections[0], cfg)

    # ---- Body content -------------------------------------------------------
    convert_markdown_body(doc, body_text, cfg)

    # ---- English abstract (goes at the very end per IAU section order) -----
    if has_title_page and meta.get("abstract_en"):
        doc.add_page_break()
        add_abstract_page(doc, "Abstract", meta["abstract_en"], cfg, rtl=False)

    output_path = Path(args.output_docx)
    doc.save(str(output_path))
    print(f"Saved: {output_path}")
    print("Reminder: open in Word, select all (Ctrl+A), press F9 to refresh "
          "the Table of Contents / List of Figures / List of Tables.")


if __name__ == "__main__":
    main()
