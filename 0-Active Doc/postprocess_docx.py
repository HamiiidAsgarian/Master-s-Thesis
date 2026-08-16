#!/usr/bin/env python3
"""
Post-process pandoc-generated DOCX for Farsi RTL thesis.
Pandoc already handles: heading styles, math (OMML), images, bold/italic.
This script adds: RTL, B Nazanin font, centering, page breaks, title page.
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

INPUT = '0-Active Doc/Thesis_v9-5_raw.docx'
OUTPUT = '0-Active Doc/Thesis_v9-5_clean.docx'


def set_rtl_paragraph(para):
    """Add w:bidi to paragraph properties."""
    pPr = para._p.get_or_add_pPr()
    if pPr.find(qn('w:bidi')) is None:
        pPr.append(parse_xml(f'<w:bidi {nsdecls("w")} w:val="1"/>'))


def set_run_font(run, font='B Nazanin', size=None):
    """Set font on a run (ascii, hAnsi, eastAsia, cs)."""
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")}/>')
        rPr.insert(0, rFonts)
    for attr in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        rFonts.set(qn(attr), font)
    if size:
        run.font.size = size


def set_table_rtl(table):
    tblPr = table._tbl.find(qn('w:tblPr'))
    if tblPr is None:
        tblPr = parse_xml(f'<w:tblPr {nsdecls("w")}/>')
        table._tbl.insert(0, tblPr)
    if tblPr.find(qn('w:bidi')) is None:
        tblPr.append(parse_xml(f'<w:bidi {nsdecls("w")} w:val="1"/>'))


def set_cell_rtl(cell):
    tcPr = cell._tc.find(qn('w:tcPr'))
    if tcPr is None:
        tcPr = parse_xml(f'<w:tcPr {nsdecls("w")}/>')
        cell._tc.insert(0, tcPr)
    if tcPr.find(qn('w:bidi')) is None:
        tcPr.append(parse_xml(f'<w:bidi {nsdecls("w")} w:val="1"/>'))


def add_page_break_before(para):
    """Insert a page break at the start of a paragraph."""
    pPr = para._p.get_or_add_pPr()
    # Remove existing page breaks first
    for pb in pPr.findall(qn('w:pageBreakBefore')):
        pPr.remove(pb)
    pPr.append(parse_xml(f'<w:pageBreakBefore {nsdecls("w")} w:val="1"/>'))


def has_display_math(para):
    """Check if paragraph contains oMathPara (display math)."""
    return len(para._p.findall('.//' + qn('m:oMathPara'))) > 0


def has_image(para):
    """Check if paragraph contains a drawing/image."""
    return len(para._p.findall('.//' + qn('w:drawing'))) > 0


# ── Main ─────────────────────────────────────────────────────────────────

print("Loading raw DOCX...")
doc = Document(INPUT)

# ── 1. Styles ────────────────────────────────────────────────────────────
print("Configuring styles...")
styles_to_fix = {
    'Heading 1': ('B Nazanin', Pt(16), True),
    'Heading 2': ('B Nazanin', Pt(14), True),
    'Heading 3': ('B Nazanin', Pt(13), True),
    'Heading 4': ('B Nazanin', Pt(12), True),
    'Normal':     ('B Nazanin', Pt(12), False),
    'Body Text':  ('B Nazanin', Pt(12), False),
}
for sname, (fname, fsize, fbold) in styles_to_fix.items():
    try:
        s = doc.styles[sname]
        s.font.name = fname
        s.font.size = fsize
        s.font.bold = fbold
        rPr = s.element.find(qn('w:rPr'))
        if rPr is None:
            rPr = parse_xml(f'<w:rPr {nsdecls("w")}/>')
            s.element.append(rPr)
        rFonts = rPr.find(qn('w:rFonts'))
        if rFonts is None:
            rFonts = parse_xml(f'<w:rFonts {nsdecls("w")}/>')
            rPr.insert(0, rFonts)
        rFonts.set(qn('w:eastAsia'), fname)
        rFonts.set(qn('w:ascii'), fname)
        rFonts.set(qn('w:hAnsi'), fname)
        rFonts.set(qn('w:cs'), fname)
    except KeyError:
        pass

# ── 2. Document defaults ─────────────────────────────────────────────────
print("Setting document defaults (language, font)...")
docDefaults = doc.styles.element.find(qn('w:docDefaults'))
if docDefaults is not None:
    rPrDef = docDefaults.find(qn('w:rPrDefault'))
    if rPrDef is not None:
        rPr = rPrDef.find(qn('w:rPr'))
        if rPr is not None:
            rFonts = rPr.find(qn('w:rFonts'))
            if rFonts is not None:
                rFonts.set(qn('w:eastAsia'), 'B Nazanin')
                rFonts.set(qn('w:ascii'), 'B Nazanin')
                rFonts.set(qn('w:hAnsi'), 'B Nazanin')
            lang = rPr.find(qn('w:lang'))
            if lang is None:
                lang = parse_xml(f'<w:lang {nsdecls("w")} w:val="fa-IR" w:eastAsia="fa-IR"/>')
                rPr.append(lang)
            else:
                lang.set(qn('w:val'), 'fa-IR')
                lang.set(qn('w:eastAsia'), 'fa-IR')

# ── 3. Page layout ───────────────────────────────────────────────────────
print("Setting page layout...")
for section in doc.sections:
    section.top_margin = Cm(3.5)
    section.bottom_margin = Cm(3.0)
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(2.5)
    sectPr = section._sectPr
    if sectPr.find(qn('w:bidi')) is None:
        sectPr.append(parse_xml(f'<w:bidi {nsdecls("w")} w:val="1"/>'))

# ── 4. Process paragraphs ───────────────────────────────────────────────
print("Processing paragraphs (RTL + font + centering + page breaks)...")
n = len(doc.paragraphs)
center_titles = {'فهرست مطالب', 'فهرست جداول', 'فهرست اشکال', 'سپاسگزاری',
                 'تقدیم به', 'چکیده', 'Abstract'}

for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()

    # RTL on every paragraph
    set_rtl_paragraph(para)

    # Font on every run (skip field code runs)
    for run in para.runs:
        r = run._r
        if r.find(qn('w:fldChar')) is not None or r.find(qn('w:instrText')) is not None:
            continue
        if r.find(qn('m:oMath')) is not None or r.find(qn('m:oMathPara')) is not None:
            continue  # don't touch math runs
        set_run_font(run, 'B Nazanin')

    # Title page: center paragraphs 0-23 (both Farsi and English title pages)
    if i <= 23:
        if text:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Section titles: center
    if text in center_titles:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Figure/table captions: center, smaller font
    if text.startswith('شکل (') or text.startswith('جدول ('):
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in para.runs:
            if not (run._r.find(qn('m:oMath')) is not None):
                run.font.size = Pt(10)

    # Bold captions (after pandoc strips **)
    # pandoc already handles this - bold runs exist

    # Display math: center
    if has_display_math(para):
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Images: center
    if has_image(para) and not text:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Page breaks before chapter headings (Heading 1)
    if para.style.name == 'Heading 1':
        add_page_break_before(para)

    if (i + 1) % 200 == 0:
        print(f"  {i+1}/{n}")

print(f"  {n}/{n}")

# ── 5. Tables ────────────────────────────────────────────────────────────
print("Processing tables (RTL + font)...")
for t_idx, table in enumerate(doc.tables):
    set_table_rtl(table)
    for row in table.rows:
        for cell in row.cells:
            set_cell_rtl(cell)
            for para in cell.paragraphs:
                set_rtl_paragraph(para)
                for run in para.runs:
                    set_run_font(run, 'B Nazanin', Pt(10))

# ── 6. Save ──────────────────────────────────────────────────────────────
print(f"Saving to {OUTPUT}...")
doc.save(OUTPUT)

# ── Summary ──────────────────────────────────────────────────────────────
doc2 = Document(OUTPUT)
math_count = len(doc2.element.findall('.//' + qn('m:oMath')))
math_para = len(doc2.element.findall('.//' + qn('m:oMathPara')))
img_count = sum(1 for p in doc2.paragraphs if has_image(p))
h1 = sum(1 for p in doc2.paragraphs if p.style.name == 'Heading 1')
h2 = sum(1 for p in doc2.paragraphs if p.style.name == 'Heading 2')
h3 = sum(1 for p in doc2.paragraphs if p.style.name == 'Heading 3')
print(f"\n=== DONE ===")
print(f"Output: {OUTPUT}")
print(f"Math: {math_para} display + {math_count} inline")
print(f"Images: {img_count}")
print(f"Headings: H1={h1}, H2={h2}, H3={h3}")
print(f"RTL: all paragraphs")
print(f"Font: B Nazanin (all runs)")
