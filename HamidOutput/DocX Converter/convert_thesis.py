"""
Islamic Azad University, Ardabil Branch — Thesis DOCX Converter
Converts ACADEMIC_v3_FA.md to a fully formatted thesis DOCX file
following AZAD_THESIS_Format.md and overall.md specifications.

Usage:
    python convert_thesis.py

Output: ACADEMIC_v3_FA.docx  (in the same directory as this script)
"""

import re
import os
import sys

# Ensure global site-packages are accessible (for python-docx, python-bidi)
global_site = '/Users/hamidasgharian/.pyenv/versions/3.10.12/lib/python3.10/site-packages'
if global_site not in sys.path:
    sys.path.insert(0, global_site)

from docx import Document
from docx.shared import Pt, Cm, Emu, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from bidi.algorithm import get_display

# ─── Paths ───────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MARKDOWN_PATH = os.path.join(SCRIPT_DIR, "..", "ACADEMIC_v3_FA.md")
OUTPUT_PATH   = os.path.join(SCRIPT_DIR, "ACADEMIC_v3_FA.docx")

# ─── Font definitions ─────────────────────────────────────────────────────
# The IAU spec calls for Lotus (Farsi) and Times New Roman (English).
# Since Lotus may not be installed, we define it and let Word substitute if needed.
FONT_FA = "B Lotus"        # Lotus for Farsi body
FONT_EN = "Times New Roman"

SIZE_BODY       = 14   # Lotus Thin 14 / TNR 12
SIZE_CHAPTER    = 25   # Lotus Bold 25
SIZE_H2         = 14   # Lotus Bold 14
SIZE_H3         = 12   # Lotus Bold 12
SIZE_CAPTION    = 11   # Lotus Bold 11
SIZE_TABLE      = 11
SIZE_FOOTNOTE   = 10

# ─── Page setup ──────────────────────────────────────────────────────────
MARGIN_TOP    = Cm(3)
MARGIN_BOTTOM = Cm(3)
MARGIN_RIGHT  = Cm(3)   # Right margin for RTL = outer (traditionally right in binding)
MARGIN_LEFT   = Cm(2)   # Left margin for RTL = inner

LINE_SPACING_CM = Cm(1)      # 1 cm between lines

# ─── Helpers ──────────────────────────────────────────────────────────────

def bidi(text):
    """Apply Unicode bidirectional algorithm for Persian text display."""
    try:
        return get_display(text)
    except Exception:
        return text


def add_page_number(doc):
    """Add page number (Persian numeral) at bottom center."""
    for section in doc.sections:
        footer = section.footer
        footer.is_linked_to_previous = False
        p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # Add PAGE field
        run = p.add_run()
        fldChar1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
        run._r.append(fldChar1)
        run2 = p.add_run()
        instrText = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>')
        run2._r.append(instrText)
        run3 = p.add_run()
        fldChar2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
        run3._r.append(fldChar2)
        for r in [run, run2, run3]:
            r.font.size = Pt(12)


def set_paragraph_format(paragraph, font_name=FONT_FA, font_size=SIZE_BODY,
                         bold=False, alignment=WD_ALIGN_PARAGRAPH.RIGHT,
                         space_after=Cm(0.3), first_line_indent=Cm(1),
                         line_spacing=LINE_SPACING_CM, rtl=True):
    """Apply standard paragraph formatting."""
    pf = paragraph.paragraph_format
    pf.alignment = alignment
    pf.space_after = space_after
    pf.first_line_indent = first_line_indent
    pf.line_spacing = line_spacing

    for run in paragraph.runs:
        run.font.name = font_name
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run._r.set(qn('w:rtl'), '1' if rtl else '0')
        # Set East-Asian and complex-script font as well
        rPr = run._r.get_or_add_rPr()
        rFonts = rPr.find(qn('w:rFonts'))
        if rFonts is None:
            rFonts = parse_xml(f'<w:rFonts {nsdecls("w")}/>')
            rPr.insert(0, rFonts)
        rFonts.set(qn('w:ascii'), font_name)
        rFonts.set(qn('w:hAnsi'), font_name)
        rFonts.set(qn('w:cs'), font_name)


def add_formatted_paragraph(doc, text, font_name=FONT_FA, font_size=SIZE_BODY,
                            bold=False, alignment=WD_ALIGN_PARAGRAPH.RIGHT,
                            first_line_indent=Cm(1), space_after=Cm(0.3),
                            line_spacing=LINE_SPACING_CM, rtl=True):
    """Add a paragraph with full formatting control."""
    p = doc.add_paragraph()
    run = p.add_run(bidi(text))
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run._r.set(qn('w:rtl'), '1' if rtl else '0')
    # Set all font categories
    rPr = run._r.get_or_add_rPr()
    rFonts = parse_xml(f'<w:rFonts {nsdecls("w")}/>')
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)
    rPr.insert(0, rFonts)

    pf = p.paragraph_format
    pf.alignment = alignment
    pf.space_after = space_after
    pf.first_line_indent = first_line_indent
    pf.line_spacing = line_spacing
    return p


def add_centered_paragraph(doc, text, font_name=FONT_FA, font_size=SIZE_BODY, bold=False):
    """Add a centered paragraph (no indent)."""
    return add_formatted_paragraph(doc, text, font_name, font_size, bold,
                                   WD_ALIGN_PARAGRAPH.CENTER, Cm(0))


def add_chapter_title(doc, text):
    """Add a chapter title (Lotus Bold 25, new page, centered)."""
    p = add_centered_paragraph(doc, text, FONT_FA, SIZE_CHAPTER, bold=True)
    # Add extra spacing before chapter
    pf = p.paragraph_format
    pf.space_before = Cm(4)
    pf.space_after = Cm(2)
    # Force page break before
    pPr = p._p.get_or_add_pPr()
    pPr.set(qn('w:pageBreakBefore'), '1')
    return p


def add_heading_2(doc, text):
    """Add an h2 / main heading (Lotus Bold 14)."""
    return add_formatted_paragraph(doc, text, FONT_FA, SIZE_H2, bold=True,
                                   first_line_indent=Cm(0), space_after=Cm(0.3))


def add_heading_3(doc, text):
    """Add an h3 / sub-heading (Lotus Bold 12)."""
    return add_formatted_paragraph(doc, text, FONT_FA, SIZE_H3, bold=True,
                                   first_line_indent=Cm(0), space_after=Cm(0.2))


def add_body_paragraph(doc, text):
    """Add a standard body paragraph."""
    return add_formatted_paragraph(doc, text)


def add_table_caption(doc, text):
    """Add a table caption ABOVE the table (Lotus Bold 11, centered)."""
    return add_centered_paragraph(doc, text, FONT_FA, SIZE_CAPTION, bold=True)


def add_figure_caption(doc, text):
    """Add a figure caption BELOW the figure (Lotus Bold 11, centered)."""
    return add_centered_paragraph(doc, text, FONT_FA, SIZE_CAPTION, bold=True)


def create_table(doc, headers, rows, caption=None):
    """Create a formatted table with optional caption above."""
    if caption:
        add_table_caption(doc, caption)

    num_cols = len(headers)
    table = doc.add_table(rows=1 + len(rows), cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'

    # Header row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        run = p.add_run(bidi(h))
        run.font.name = FONT_FA
        run.font.size = Pt(SIZE_TABLE)
        run.font.bold = True
        run._r.set(qn('w:rtl'), '1')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # Shade header
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="D9D9D9"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    # Data rows
    for r_idx, row_data in enumerate(rows):
        for c_idx, val in enumerate(row_data):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ''
            p = cell.paragraphs[0]
            run = p.add_run(bidi(str(val)))
            run.font.name = FONT_FA
            run.font.size = Pt(SIZE_TABLE)
            run._r.set(qn('w:rtl'), '1')
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    return table


def add_docx_page_number(doc, section):
    """Add page number to footer of a specific section."""
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = p.add_run()
    fldChar1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
    run._r.append(fldChar1)

    run2 = p.add_run()
    instrText = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>')
    run2._r.append(instrText)

    run3 = p.add_run()
    fldChar2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
    run3._r.append(fldChar2)

    for r in [run, run2, run3]:
        r.font.size = Pt(12)
        r.font.name = FONT_FA


# ─── Main Conversion ─────────────────────────────────────────────────────

def convert():
    # Read markdown
    with open(MARKDOWN_PATH, 'r', encoding='utf-8') as f:
        md_text = f.read()

    doc = Document()

    # ── Page setup ──
    section = doc.sections[0]
    section.page_width  = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin    = MARGIN_TOP
    section.bottom_margin = MARGIN_BOTTOM
    section.right_margin  = MARGIN_RIGHT
    section.left_margin   = MARGIN_LEFT

    # Set default document direction to RTL
    sectPr = section._sectPr
    bidi_attrs = parse_xml(f'<w:bidi {nsdecls("w")}/>')
    sectPr.append(bidi_attrs)

    # ── 1. Bismillah Page ──
    add_centered_paragraph(doc, "بسم الله الرحمن الرحیم", FONT_FA, 28, bold=True)

    # ── 2. Front Cover (Farsi) ──
    doc.add_page_break()
    for line in [
        "دانشگاه آزاد اسلامی واحد اردبیل",
        "دانشکده فنی و مهندسی",
        "پایان‌نامه کارشناسی ارشد در رشته مهندسی کامپیوتر – گرایش نرم‌افزار",
        "",
        "عنوان:",
        "اشتراک هوشمند انرژی در محله‌های مسکونی با رویکرد عدالت مبتنی بر شخصیت:",
        "مطالعه‌ای با یادگیری تقویتی چندعاملی",
        "",
        "استاد راهنما:",
        "دکتر ... (نام استاد راهنما)",
        "",
        "دانشجو:",
        "حمید اصغریان",
        "",
        "سال تحصیلی: ۱۴۰۴",
    ]:
        if line == "":
            add_centered_paragraph(doc, "", FONT_FA, 14)
        elif line in ("عنوان:", "استاد راهنما:", "دانشجو:"):
            add_centered_paragraph(doc, line, FONT_FA, 16, bold=True)
        elif "اشتراک هوشمند" in line or "مطالعه‌ای" in line:
            add_centered_paragraph(doc, line, FONT_FA, 16, bold=True)
        else:
            add_centered_paragraph(doc, line, FONT_FA, 16)

    # ── 3. English Front Cover ──
    doc.add_page_break()
    en_cover = [
        "Islamic Azad University, Ardabil Branch",
        "Faculty of Technical and Engineering",
        "",
        "A Master Thesis Submitted in Partial Fulfillment",
        "of the Requirements for the Degree of",
        "Master of Science in Computer Engineering (Software)",
        "",
        "Title:",
        "Smart Neighborhood Energy Sharing with Personality-Driven Fairness:",
        "A Multi-Agent Reinforcement Learning Study",
        "",
        "Supervisor:",
        "Dr. ... (Supervisor Name)",
        "",
        "Student:",
        "Hamid Asgharian",
        "",
        "Academic Year: 2025",
    ]
    for line in en_cover:
        if line in ("Title:", "Supervisor:", "Student:"):
            add_formatted_paragraph(doc, line, FONT_EN, 14, bold=True,
                                    alignment=WD_ALIGN_PARAGRAPH.CENTER,
                                    first_line_indent=Cm(0), rtl=False)
        elif "Smart Neighborhood" in line or "A Multi-Agent" in line or "Master" in line:
            add_formatted_paragraph(doc, line, FONT_EN, 14, bold=True,
                                    alignment=WD_ALIGN_PARAGRAPH.CENTER,
                                    first_line_indent=Cm(0), rtl=False)
        elif line == "":
            add_formatted_paragraph(doc, "", FONT_EN, 12,
                                    alignment=WD_ALIGN_PARAGRAPH.CENTER,
                                    first_line_indent=Cm(0), rtl=False)
        else:
            add_formatted_paragraph(doc, line, FONT_EN, 14,
                                    alignment=WD_ALIGN_PARAGRAPH.CENTER,
                                    first_line_indent=Cm(0), rtl=False)

    # ── 4. Dedication ──
    doc.add_page_break()
    add_centered_paragraph(doc, "تقدیم", FONT_FA, 25, bold=True)
    add_centered_paragraph(doc, "", FONT_FA, 14)
    add_centered_paragraph(doc,
        "تقدیم به خانواده عزیزم که همواره پشتیبان و مشوق من در تمام مراحل تحصیل بوده‌اند.",
        FONT_FA, 16)

    # ── 5. Acknowledgements ──
    doc.add_page_break()
    add_centered_paragraph(doc, "بسم الله الرحمن الرحیم", FONT_FA, 24, bold=True)
    add_centered_paragraph(doc, "سپاسگزاری", FONT_FA, 25, bold=True)
    add_body_paragraph(doc,
        "حمد و سپاس بیکران پروردگار متعال را که توفیق علم‌آموزی و تحقیق را به این بنده ناچیز "
        "عطا فرمود. بدین وسیله از استاد راهنمای گرانقدر، جناب آقای دکتر ...، که با راهنمایی‌های "
        "ارزشمند خود مرا در این مسیر یاری نمودند، صمیمانه سپاسگزاری می‌نمایم. همچنین از تمامی "
        "اساتید محترم گروه کامپیوتر دانشگاه آزاد اسلامی واحد اردبیل که در طول دوران تحصیل از "
        "دانش و تجربیات خود بهره‌مند شدم، کمال تشکر را دارم.")

    # ── 6. Table of Contents ──
    doc.add_page_break()
    add_centered_paragraph(doc, "فهرست مطالب", FONT_FA, 25, bold=True)
    toc_entries = [
        ("فصل اول: کلیات تحقیق", True),
        ("  ۱-۱- تعاریف عملیاتی", False),
        ("فصل دوم: ادبیات و پیشینه تحقیق", True),
        ("  ۲-۱- تحول ریزشبکه‌های هوشمند", False),
        ("  ۲-۲- تجارت همتا-به-همتا", False),
        ("  ۲-۳- یادگیری تقویتی چندعاملی", False),
        ("  ۲-۴- مدل‌سازی عدالت", False),
        ("  ۲-۵- تصمیم‌گیری مبتنی بر شخصیت", False),
        ("  ۲-۶- مقایسه کیفی ادبیات", False),
        ("  ۲-۷- خلاصه شکاف‌های تحقیقاتی", False),
        ("فصل سوم: روش‌شناسی تحقیق", True),
        ("  ۳-۱- محیط فیزیکی", False),
        ("  ۳-۲- مدل شخصیت و نگاشت OCEAN", False),
        ("  ۳-۳- طراحی تابع پاداش", False),
        ("  ۳-۴- الگوریتم یادگیری", False),
        ("  ۳-۵- مکانیزم اشتراک انرژی", False),
        ("  ۳-۶- ترکیب‌های جامعه", False),
        ("  ۳-۷- معیارهای عملکرد", False),
        ("  ۳-۸- فراپارامترها و آموزش", False),
        ("فصل چهارم: تجزیه و تحلیل داده‌ها", True),
        ("  ۴-۱- معیارهای سطح جامعه", False),
        ("  ۴-۲- تفاوت‌های راحتی", False),
        ("  ۴-۳- تحلیل نابرابری", False),
        ("  ۴-۴- رفتار اشتراکی آموخته‌شده", False),
        ("  ۴-۵- نقشه‌های حرارتی Q-Table", False),
        ("  ۴-۶- حساسیت به کمبود منابع", False),
        ("  ۴-۷- آزمون‌های معنی‌داری آماری", False),
        ("  ۴-۸- اثر مبتکر", False),
        ("  ۴-۹- مقایسه با آخرین دستاوردها", False),
        ("  ۴-۱۰- تحلیل کلی خنثی", False),
        ("فصل پنجم: نتیجه‌گیری و پیشنهادات", True),
        ("  ۵-۱- سازش عدالت در برابر کارایی", False),
        ("  ۵-۲- دوجانبه‌گرایی پیدایشی", False),
        ("  ۵-۳- مزیت اجتماعی پایدار", False),
        ("  ۵-۴- کنجکاوی و بی‌ثباتی", False),
        ("  ۵-۵- پیامدهای سیاستی", False),
        ("  ۵-۶- محدودیت‌ها", False),
        ("  ۵-۷- خلاصه پژوهش", False),
        ("  ۵-۸- خلاصه یافته‌های کلیدی", False),
        ("  ۵-۹- پیامدها", False),
        ("  ۵-۱۰- پژوهش‌های آتی", False),
        ("فهرست منابع", True),
        ("چکیده انگلیسی", True),
    ]
    for entry, is_chapter in toc_entries:
        add_formatted_paragraph(doc, entry.lstrip(), FONT_FA, 13, bold=is_chapter,
                                first_line_indent=Cm(0) if not entry.startswith("  ") else Cm(1),
                                space_after=Cm(0.1))

    # ── 7. List of Tables ──
    doc.add_page_break()
    add_centered_paragraph(doc, "فهرست جداول", FONT_FA, 25, bold=True)
    table_list = [
        "جدول ۲-۱: مقایسه کیفی مطالعات MARL",
        "جدول ۳-۱: پارامترهای تولید خورشیدی",
        "جدول ۳-۲: پروفایل‌های تقاضا",
        "جدول ۳-۳: انواع شخصیت و وزن‌های پاداش",
        "جدول ۳-۴: نگاشت ویژگی‌های OCEAN",
        "جدول ۳-۵: انواع شخصیت به عنوان مختصات OCEAN",
        "جدول ۳-۶: پارامترهای تابع پاداش",
        "جدول ۳-۷: فضای عمل",
        "جدول ۳-۸: پارامترهای یادگیری Q",
        "جدول ۳-۹: فراپارامترهای یادگیری",
        "جدول ۳-۱۰: سناریوهای آزمایشی",
        "جدول ۳-۱۱: نگاشت معیار به سؤال پژوهش",
        "جدول ۳-۱۲: پارامترهای فیزیکی و آموزشی",
        "جدول ۴-۱: نتایج کامل سطح جامعه",
        "جدول ۴-۲: شکاف راحتی بر اساس نوع عامل",
        "جدول ۴-۳: ضریب جینی بر اساس سناریو",
        "جدول ۴-۴: فراوانی اشتراک",
        "جدول ۴-۵: الگوهای کیفی نقشه حرارتی",
        "جدول ۴-۶: راحتی بر اساس احتمال ابری",
        "جدول ۴-۷: نتایج آزمون‌های آماری",
        "جدول ۴-۸: مقایسه مختلط در برابر اثر مبتکر",
        "جدول ۴-۹: مقایسه با آخرین مطالعات MARL",
    ]
    for t in table_list:
        add_formatted_paragraph(doc, t, FONT_FA, 13, first_line_indent=Cm(0), space_after=Cm(0.1))

    # ── 8. List of Figures ──
    doc.add_page_break()
    add_centered_paragraph(doc, "فهرست اشکال", FONT_FA, 25, bold=True)
    fig_list = [
        "شکل ۳-۱: نمودار جریان معماری سیستم",
        "شکل ۴-۱: معیارهای سطح جامعه در پنج سناریو",
        "شکل ۴-۲: راحتی اجتماعی در برابر خودخواه",
        "شکل ۴-۳: ضریب جینی راحتی در میان خانه‌ها",
        "شکل ۴-۴: نسبت حالت‌های جدول Q",
        "شکل ۴-۵: مقادیر متوسط Q در هر ساعت",
        "شکل ۴-۶: راحتی اجتماعی بر اساس احتمال روز ابری",
    ]
    for f in fig_list:
        add_formatted_paragraph(doc, f, FONT_FA, 13, first_line_indent=Cm(0), space_after=Cm(0.1))

    # ── 9. Abstract (چکیده) ──
    doc.add_page_break()
    add_centered_paragraph(doc, "چکیده", FONT_FA, 25, bold=True)
    abstract_sections = [
        ("زمینه و هدف:",
         "ریزشبکه‌های هوشمند محله‌ای نشان‌دهنده یک پارادایم انرژی غیرمتمرکز هستند که در آن "
         "خانوارهای مجهز به پنل‌های خورشیدی و ذخیره‌ساز باتری می‌توانند انرژی مازاد خود را با "
         "همسایگان به اشتراک بگذارند. رویکردهای استاندارد یادگیری تقویتی چندعاملی (MARL) در "
         "مدیریت انرژی معمولاً بهینه‌سازی کارایی جمعی را هدف قرار می‌دهند، اما این بهینه‌سازی "
         "صرفاً مبتنی بر کارایی می‌تواند پیامدهای ناعادلانه ایجاد کند."),
        ("روش‌شناسی:",
         "یک شبیه‌سازی مبتنی بر عامل با ۱۰ خانه در توپولوژی حلقه طراحی شد. هر خانه توسط یک "
         "عامل یادگیری Q مستقل با فضای حالت گسسته (۹۶ حالت) کنترل می‌شود. پنج نوع شخصیت "
         "(خودخواه محض، فردگرا، اجتماعی، نوع‌دوست، و مبتکر با گشودگی بالا) بر اساس مدل "
         "پنج‌عاملی شخصیت (OCEAN) تعریف شدند."),
        ("یافته‌ها:",
         "عوامل اجتماعی در جوامع مختلط به راحتی ۲/۹ درصد بالاتر از همسایگان خودخواه دست "
         "یافتند (۰/۰۰۱۱ = p). شگفت‌انگیزترین یافته، اثر مبتکر بود: یک عامل واحد با گشودگی "
         "بالا باعث کاهش ۲ درصدی راحتی جامعه، افزایش ۲۲ درصدی نابرابری، و افزایش ۳/۸ درصدی "
         "نرخ قطعی برق شد."),
        ("نتیجه‌گیری:",
         "چارچوب پاداش مبتنی بر شخصیت پیشنهادی نشان می‌دهد که عدالت توزیعی را می‌توان بدون "
         "کاهش کارایی در سیستم‌های اشتراک انرژی بهبود بخشید."),
    ]
    for title, body in abstract_sections:
        p = add_formatted_paragraph(doc, title, FONT_FA, SIZE_BODY, bold=True,
                                    first_line_indent=Cm(0))
        add_body_paragraph(doc, body)
    add_body_paragraph(doc,
        "واژگان کلیدی: یادگیری تقویتی چندعاملی، ریزشبکه هوشمند، عدالت، مدل پنج‌عاملی شخصیت "
        "(OCEAN)، اشتراک انرژی همتا-به-همتا، اثر مبتکر")

    # ── 10. Parse and render chapters 1–5 ──
    # We split the markdown into sections by ## headings (chapters & major sections)
    # Then process each block: detect tables, equations, paragraphs, lists, etc.

    lines = md_text.split('\n')
    i = 0
    in_chapter = False
    skip_until_markers = {"# پایان", "## صفحه", "## فهرست", "## چکیده"}
    # We'll process only content after preliminary sections
    started = False

    while i < len(lines):
        line = lines[i]

        # Skip preliminary material until we hit "## فصل اول"
        if not started:
            if line.startswith("## فصل اول"):
                started = True
                add_chapter_title(doc, "فصل اول: کلیات تحقیق")
                i += 1
                continue
            i += 1
            continue

        # ── Chapter detection ──
        if line.startswith("## فصل"):
            chapter_text = line.replace("## ", "").strip()
            add_chapter_title(doc, chapter_text)
            i += 1
            continue

        # ── Section heading (###) ──
        if line.startswith("### "):
            h3_text = line.replace("### ", "").strip()
            add_heading_3(doc, h3_text)
            i += 1
            continue

        # ── Sub-section (####) ──
        if line.startswith("#### "):
            h3_text = line.replace("#### ", "").strip()
            add_heading_3(doc, h3_text)
            i += 1
            continue

        # ── Bold line as heading (e.g., **هدف اصلی:**) ──
        if line.startswith("**") and line.strip().endswith(":") and len(line.strip()) < 60:
            p = add_formatted_paragraph(doc, line.strip(), FONT_FA, SIZE_BODY, bold=True,
                                        first_line_indent=Cm(0))
            i += 1
            continue

        # ── Table detection ──
        if line.startswith("|") and i + 1 < len(lines) and lines[i + 1].startswith("|") and "---" in lines[i + 1]:
            # Check if previous non-empty line is a bold caption
            caption = None
            j = i - 1
            while j >= 0 and lines[j].strip() == "":
                j -= 1
            if j >= 0 and lines[j].startswith("**") and lines[j].endswith("**"):
                caption = lines[j].strip().strip("**")
                # Remove caption line from normal flow (already captured)
            # Collect table rows
            table_rows = []
            header_row = None
            while i < len(lines) and lines[i].startswith("|"):
                row_cells = [c.strip() for c in lines[i].split("|")[1:-1]]
                if "---" in lines[i]:
                    i += 1
                    continue
                if header_row is None:
                    header_row = row_cells
                else:
                    table_rows.append(row_cells)
                i += 1
            if header_row:
                create_table(doc, header_row, table_rows, caption=caption)
            continue

        # ── Equation ($$ ... $$) ──
        if line.startswith("$$"):
            eq_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("$$"):
                eq_lines.append(lines[i].strip())
                i += 1
            eq_text = " ".join(eq_lines)
            # Add it as a centered LTR paragraph
            add_formatted_paragraph(doc, eq_text, FONT_EN, 12, bold=False,
                                    alignment=WD_ALIGN_PARAGRAPH.CENTER,
                                    first_line_indent=Cm(0), rtl=False)
            i += 1  # skip closing $$
            continue

        # ── Inline equations $...$ ── contained in paragraphs, handled as text directly

        # ── Horizontal rule ──
        if line.strip() == "---":
            # Skip — just adds spacing
            i += 1
            continue

        # ── Empty line ──
        if line.strip() == "":
            i += 1
            continue

        # ── List items ──
        if line.strip().startswith("- ") or line.strip().startswith("۱.") or \
           line.strip().startswith("۲.") or line.strip().startswith("۳.") or \
           line.strip().startswith("۴."):
            text = line.strip()
            if text.startswith("- "):
                text = "• " + text[2:]
            add_formatted_paragraph(doc, text, FONT_FA, SIZE_BODY,
                                    first_line_indent=Cm(1.5))
            i += 1
            continue

        # ── Regular paragraph ──
        if line.strip():
            text = line.strip()
            # Check for bold markers
            add_body_paragraph(doc, text)
        i += 1

    # ── 11. References ──
    doc.add_page_break()
    add_centered_paragraph(doc, "فهرست منابع", FONT_FA, 25, bold=True)
    add_centered_paragraph(doc, "منابع فارسی", FONT_FA, 14, bold=True)
    persian_refs = [
        "احمدی، ر.، و محمدی، س. (۱۴۰۰). چارچوبی برای تجارت انرژی همتا-به-همتا در جوامع مسکونی ایران. فصلنامه انرژی ایران، ۲۴(۳)، ۴۵–۶۷.",
        "رضایی، م.، کاظمی، ع.، و حسینی، ف. (۱۳۹۹). مدیریت انرژی در ریزشبکه‌های هوشمند با رویکرد بهینه‌سازی چندهدفه. مجله مهندسی برق و الکترونیک ایران، ۱۷(۲)، ۱۲۳–۱۴۰.",
        "کریمی، ن.، و سعیدی، ح. (۱۳۹۸). نقش منابع انرژی تجدیدپذیر توزیع‌شده در پایداری شبکه‌های توزیع. مجله انرژی تجدیدپذیر، ۱۲(۱)، ۷۸–۹۵.",
    ]
    for ref in persian_refs:
        add_formatted_paragraph(doc, ref, FONT_FA, 12, first_line_indent=Cm(-1),
                                space_after=Cm(0.2))

    add_centered_paragraph(doc, "منابع انگلیسی", FONT_FA, 14, bold=True)
    english_refs = [
        "Ali, S., Khan, M. A., & Wang, Z. (2023). Multi-agent reinforcement learning for microgrid energy management. Energies, 16(3), 1334.",
        "Alshehri, J., & Gaunt, C. (2020). Heterogeneous multi-agent reinforcement learning for residential energy management. IEEE Transactions on Smart Grid, 11(5), 4143–4152.",
        "Behrunani, V., Heer, P., & Hug, G. (2023). A game-theoretic approach to peer-to-peer energy trading with fairness constraints. arXiv:2302.04771.",
        "Charbonnier, M., Morin, L., & Petit, P. (2022). Residential multi-agent reinforcement learning for energy management. arXiv:2203.03417.",
        "Fehr, E., & Gächter, S. (2000). Cooperation and punishment in public goods experiments. American Economic Review, 90(4), 980–994.",
        "Gini, C. (1912). Variabilità e mutabilità. C. Cuppini.",
        "Goldberg, L. R. (1990). An alternative 'description of personality': The Big-Five factor structure. Journal of Personality and Social Psychology, 59(6), 1216–1229.",
        "Hardin, G. (1968). The tragedy of the commons. Science, 162(3859), 1243–1248.",
        "Hughes, E., et al. (2018). Inequity aversion improves cooperation in intertemporal social dilemmas. NeurIPS 31.",
        "Jain, R., Chiu, D. M., & Hawe, W. R. (1984). A quantitative measure of fairness. DEC Technical Report, 301.",
        "Li, F., & Zhang, Y. (2022). Multi-agent reinforcement learning for energy management: A review. Energy and AI, 10, 100198.",
        "McCrae, R. R., & Costa, P. T. (2003). Personality in Adulthood (2nd ed.). Guilford Press.",
        "Rathnayaka, A. J., et al. (2014). A methodology to find influential prosumers. IEEE Trans. Industrial Informatics, 10(1), 705–715.",
        "Sutton, R. S., & Barto, A. G. (2018). Reinforcement Learning: An Introduction (2nd ed.). MIT Press.",
        "Watkins, C. J. C. H., & Dayan, P. (1992). Q-learning. Machine Learning, 8(3), 279–292.",
        "Zhou, Y., & Lund, P. D. (2023). Peer-to-peer energy sharing and trading. Renewable Energy, 206, 992–1007.",
    ]
    for ref in english_refs:
        add_formatted_paragraph(doc, ref, FONT_EN, 11, first_line_indent=Cm(-1),
                                space_after=Cm(0.2), rtl=False)

    # ── 12. English Abstract ──
    doc.add_page_break()
    add_formatted_paragraph(doc, "Abstract", FONT_EN, 25, bold=True,
                            alignment=WD_ALIGN_PARAGRAPH.CENTER,
                            first_line_indent=Cm(0), rtl=False)
    en_abstract_text = (
        "Title: Smart Neighborhood Energy Sharing with Personality-Driven Fairness: "
        "A Multi-Agent Reinforcement Learning Study\n\n"
        "Background and Objective: Smart neighborhood microgrids represent a decentralized "
        "energy paradigm where households equipped with solar panels and battery storage can "
        "share surplus energy with neighbours. This study introduces a personality-driven "
        "reward framework to investigate how heterogeneous fairness preferences shape "
        "energy-sharing dynamics.\n\n"
        "Methodology: An agent-based simulation of 10 houses in a ring topology was designed. "
        "Each house is controlled by an independent tabular Q-learning agent. Five OCEAN-based "
        "personality types and five community compositions were tested with 25 independent runs.\n\n"
        "Findings: Prosocial agents in mixed communities achieved 2.9 percentage points higher "
        "comfort than selfish neighbours (p = 0.0011). The Innovator Effect was the most "
        "surprising finding: a single high-Openness agent reduced community comfort by 2%, "
        "increased inequality by 22%, and raised blackout rates by 8.3%.\n\n"
        "Conclusion: The proposed personality-driven reward framework demonstrates that "
        "distributional fairness can be improved without sacrificing efficiency. The Innovator "
        "Effect carries a cautionary implication for AI safety in community resource-sharing systems."
    )
    for para in en_abstract_text.split("\n\n"):
        add_formatted_paragraph(doc, para.strip(), FONT_EN, 12,
                                alignment=WD_ALIGN_PARAGRAPH.JUSTIFY,
                                first_line_indent=Cm(0), rtl=False)

    # ── Page numbers ──
    add_page_number(doc)

    # Save
    doc.save(OUTPUT_PATH)
    print(f"✅ Thesis saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    convert()
