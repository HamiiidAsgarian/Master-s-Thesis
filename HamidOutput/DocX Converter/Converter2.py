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

# Ensure global site-packages are accessible (for python-docx, python-bidi, arabic_reshaper)
global_site = '/Users/hamidasgharian/.pyenv/versions/3.10.12/lib/python3.10/site-packages'
if global_site not in sys.path:
    sys.path.insert(0, global_site)

from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from bidi.algorithm import get_display
import arabic_reshaper

# ─── Font fallback ────────────────────────────────────────────────────────
def get_available_font():
    import platform
    if platform.system() == "Windows":
        return "B Lotus", "Times New Roman"
    else:
        # Mac/Linux: Tahoma is a safe, universally available Farsi-friendly font.
        return "Tahoma", "Times New Roman"

FONT_FA, FONT_EN = get_available_font()

SIZE_BODY       = 14
SIZE_CHAPTER    = 25
SIZE_H2         = 14
SIZE_H3         = 12
SIZE_CAPTION    = 11
SIZE_TABLE      = 11

# ─── Page setup ──────────────────────────────────────────────────────────
MARGIN_TOP    = Cm(3)
MARGIN_BOTTOM = Cm(3)
MARGIN_RIGHT  = Cm(3)
MARGIN_LEFT   = Cm(2)
LINE_SPACING_CM = Cm(1)

# ─── FIX: The "No-Hang" XML Font Applier ──────────────────────────────────
def apply_run_style(run, font_name, font_size, bold=False, italic=False, rtl=True):
    """
    Apply font, size, bold, italic, and RTL directly via XML.
    This completely bypasses the buggy python-docx property setters
    that cause infinite loops (KeyboardInterrupt).
    """
    r = run._r
    rPr = r.get_or_add_rPr()

    # 1. Font Name (remove any existing duplicates)
    for elem in rPr.findall(qn('w:rFonts')):
        rPr.remove(elem)
    rFonts = parse_xml(
        f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" '
        f'w:hAnsi="{font_name}" w:cs="{font_name}"/>'
    )
    rPr.insert(0, rFonts)

    # 2. Font Size (in half-points: 14pt = 28)
    sz = rPr.find(qn('w:sz'))
    if sz is None:
        sz = parse_xml(f'<w:sz {nsdecls("w")} w:val="{font_size * 2}"/>')
        rPr.append(sz)
    else:
        sz.set(qn('w:val'), str(font_size * 2))

    # 3. Bold
    b = rPr.find(qn('w:b'))
    if bold:
        if b is None:
            b = parse_xml(f'<w:b {nsdecls("w")} w:val="1"/>')
            rPr.append(b)
        else:
            b.set(qn('w:val'), '1')
    else:
        if b is not None:
            b.set(qn('w:val'), '0')

    # 4. Italic
    i = rPr.find(qn('w:i'))
    if italic:
        if i is None:
            i = parse_xml(f'<w:i {nsdecls("w")} w:val="1"/>')
            rPr.append(i)
        else:
            i.set(qn('w:val'), '1')
    else:
        if i is not None:
            i.set(qn('w:val'), '0')

    # 5. RTL direction
    if rtl:
        r.set(qn('w:rtl'), '1')
    else:
        if qn('w:rtl') in r.attrib:
            del r.attrib[qn('w:rtl')]


# ─── Helpers ──────────────────────────────────────────────────────────────

def bidi(text):
    """Apply Unicode bidirectional + reshape for Farsi script."""
    try:
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except Exception:
        return text


def process_inline_formatting(paragraph, raw_text, font_name, font_size,
                              bold=False, rtl=True):
    """
    Parse **bold** and *italic* from markdown and apply them safely
    using the XML-based apply_run_style (no hanging).
    """
    parts = re.split(r'(\*\*.*?\*\*|\*.*?\*)', raw_text)
    for part in parts:
        if not part:
            continue
        is_bold = False
        is_italic = False
        clean_text = part

        if part.startswith('**') and part.endswith('**'):
            is_bold = True
            clean_text = part[2:-2]
        elif part.startswith('*') and part.endswith('*'):
            is_italic = True
            clean_text = part[1:-1]

        run = paragraph.add_run(bidi(clean_text))
        apply_run_style(run, font_name, font_size,
                        bold=bold or is_bold,
                        italic=is_italic,
                        rtl=rtl)
    return paragraph


def add_formatted_paragraph(doc, text, font_name=FONT_FA, font_size=SIZE_BODY,
                            bold=False, alignment=WD_ALIGN_PARAGRAPH.RIGHT,
                            first_line_indent=Cm(1), space_after=Cm(0.3),
                            line_spacing=LINE_SPACING_CM, rtl=True):
    p = doc.add_paragraph()
    process_inline_formatting(p, text, font_name, font_size, bold, rtl)

    pf = p.paragraph_format
    pf.alignment = alignment
    pf.space_after = space_after
    pf.first_line_indent = first_line_indent
    pf.line_spacing = line_spacing
    return p


def add_centered_paragraph(doc, text, font_name=FONT_FA, font_size=SIZE_BODY, bold=False):
    return add_formatted_paragraph(doc, text, font_name, font_size, bold,
                                   WD_ALIGN_PARAGRAPH.CENTER, Cm(0))


def add_chapter_title(doc, text):
    p = add_centered_paragraph(doc, text, FONT_FA, SIZE_CHAPTER, bold=True)
    pf = p.paragraph_format
    pf.space_before = Cm(4)
    pf.space_after = Cm(2)
    pPr = p._p.get_or_add_pPr()
    pPr.set(qn('w:pageBreakBefore'), '1')
    return p


def add_heading_2(doc, text):
    return add_formatted_paragraph(doc, text, FONT_FA, SIZE_H2, bold=True,
                                   first_line_indent=Cm(0), space_after=Cm(0.3))


def add_heading_3(doc, text):
    return add_formatted_paragraph(doc, text, FONT_FA, SIZE_H3, bold=True,
                                   first_line_indent=Cm(0), space_after=Cm(0.2))


def add_body_paragraph(doc, text):
    return add_formatted_paragraph(doc, text)


def add_table_caption(doc, text):
    return add_centered_paragraph(doc, text, FONT_FA, SIZE_CAPTION, bold=True)


def create_table(doc, headers, rows, caption=None):
    """Create a table using the safe XML font applier."""
    if caption:
        add_table_caption(doc, caption)

    num_cols = len(headers)
    table = doc.add_table(rows=1 + len(rows), cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'

    # Header row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ''  # Clear default
        p = cell.paragraphs[0]
        process_inline_formatting(p, h, FONT_FA, SIZE_TABLE, bold=True, rtl=True)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # Gray background
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="D9D9D9"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    # Data rows
    for r_idx, row_data in enumerate(rows):
        for c_idx, val in enumerate(row_data):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ''
            p = cell.paragraphs[0]
            process_inline_formatting(p, str(val), FONT_FA, SIZE_TABLE,
                                      bold=False, rtl=True)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    return table


def add_page_number(doc):
    for section in doc.sections:
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
            apply_run_style(r, FONT_FA, 12, bold=False, rtl=True)


# ─── Main Conversion ─────────────────────────────────────────────────────

def convert():
    # 1. Read markdown
    with open(MARKDOWN_PATH, 'r', encoding='utf-8') as f:
        md_text = f.read()

    doc = Document()

    # ── Page setup ──
    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = MARGIN_TOP
    section.bottom_margin = MARGIN_BOTTOM
    section.right_margin = MARGIN_RIGHT
    section.left_margin = MARGIN_LEFT

    sectPr = section._sectPr
    bidi_attrs = parse_xml(f'<w:bidi {nsdecls("w")}/>')
    sectPr.append(bidi_attrs)

    # ── 1. Bismillah ──
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

    # ── 3. English Cover ──
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

    # ── 9. Abstract ──
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

    # ── 10. Parse Markdown Body (Chapters 1–5) ──
    lines = md_text.split('\n')
    i = 0
    started = False

    def collect_paragraph(start_idx):
        """Merge soft-wrapped lines into a single paragraph."""
        collected = []
        j = start_idx
        while j < len(lines) and lines[j].strip() != "":
            collected.append(lines[j].strip())
            j += 1
        return " ".join(collected), j

    while i < len(lines):
        line = lines[i].strip()

        if not started:
            if line.startswith("## فصل اول"):
                started = True
                add_chapter_title(doc, "فصل اول: کلیات تحقیق")
                i += 1
                continue
            i += 1
            continue

        # ── Chapter ──
        if line.startswith("## فصل"):
            chapter_text = line.replace("## ", "").strip()
            add_chapter_title(doc, chapter_text)
            i += 1
            continue

        # ── Sub-headings (### / ####) ──
        if line.startswith("### ") or line.startswith("#### "):
            h3_text = re.sub(r'^#+\s*', '', line).strip()
            add_heading_3(doc, h3_text)
            i += 1
            continue

        # ── Bold label (e.g., **هدف اصلی:**) ──
        if line.startswith("**") and ":**" in line and len(line) < 80:
            add_formatted_paragraph(doc, line, FONT_FA, SIZE_BODY, bold=True,
                                    first_line_indent=Cm(0))
            i += 1
            continue

        # ── Table ──
        if line.startswith("|") and i + 1 < len(lines) and "---" in lines[i + 1]:
            caption = None
            for k in range(i - 1, max(0, i - 3), -1):
                if lines[k].strip() and lines[k].strip().startswith("**"):
                    caption = lines[k].strip().strip('**')
                    break

            header_row = None
            table_rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
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

        # ── Equation ──
        if line.startswith("$$"):
            eq_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("$$"):
                eq_lines.append(lines[i].strip())
                i += 1
            eq_text = " ".join(eq_lines)
            add_formatted_paragraph(doc, eq_text, FONT_EN, 12, bold=False,
                                    alignment=WD_ALIGN_PARAGRAPH.CENTER,
                                    first_line_indent=Cm(0), rtl=False)
            i += 1
            continue

        # ── Horizontal rule ──
        if line == "---":
            i += 1
            continue

        # ── List items ──
        if line.startswith("- ") or re.match(r'^[۱-۴]\.', line):
            text = line
            if text.startswith("- "):
                text = "• " + text[2:]
            add_formatted_paragraph(doc, text, FONT_FA, SIZE_BODY,
                                    first_line_indent=Cm(1.5))
            i += 1
            continue

        # ── Regular paragraph ──
        if line:
            full_text, next_i = collect_paragraph(i)
            if full_text and full_text != "*":
                add_body_paragraph(doc, full_text)
            i = next_i
        else:
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