#!/usr/bin/env python3
"""Convert Latin digits in Persian text to Persian numerals (۰-۹).

Preserves: YAML front matter, English title page, English abstract,
bibliography, citations, math, image paths, code blocks,
English author-year refs, table version labels.
"""
import re
import sys

DIGIT_MAP = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')


def convert_persian_digits(text):
    lines = text.split('\n')
    result = []
    in_english_abstract = False
    in_code_block = False
    in_yaml_or_title = True
    in_bibliography = False

    for line in lines:
        # Skip YAML front matter + English title page
        if in_yaml_or_title:
            result.append(line)
            if re.match(r'^##\s+(?!Abstract\b)', line.strip()) and any(
                ord(c) > 0x0600 for c in line.strip()
            ):
                in_yaml_or_title = False
            continue

        # Track bibliography (## منابع فارسی / ## منابع غیرفارسی)
        if re.match(r'^##\s+منابع', line.strip()):
            in_bibliography = True
        if in_bibliography:
            result.append(line)
            continue

        # Track English abstract
        if re.match(r'^##\s+Abstract\s*$', line.strip()):
            in_english_abstract = True
        if in_english_abstract and line.strip() == '---':
            in_english_abstract = False
            result.append(line)
            continue

        # Track code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if in_english_abstract or in_code_block:
            result.append(line)
            continue

        result.append(convert_line(line))

    return '\n'.join(result)


def convert_line(line):
    originals = []

    def save(text):
        idx = len(originals)
        originals.append(text)
        return chr(0xE000 + idx)

    protected = line

    # Display math $$...$$
    protected = re.sub(r'\$\$.*?\$\$', lambda m: save(m.group(0)), protected, flags=re.DOTALL)
    # Inline math $...$
    protected = re.sub(r'\$[^$\n]+\$', lambda m: save(m.group(0)), protected)
    # Image paths
    protected = re.sub(r'!\[.*?\]\(.*?\)', lambda m: save(m.group(0)), protected)
    # Inline code
    protected = re.sub(r'`[^`\n]+`', lambda m: save(m.group(0)), protected)
    # Citations [n], [n,m], [n]-[m]
    protected = re.sub(r'\[[\d,\s–\-]+\]', lambda m: save(m.group(0)), protected)
    # English author-year refs in tables: "Author et al. (YYYY)" or "Author & Author (YYYY)"
    protected = re.sub(r'[A-Z][a-z]+(?:\s+(?:et al\.?|&\s*[A-Z][a-z]+))?\s*\(\d{4}\)', lambda m: save(m.group(0)), protected)
    # "Author, Author & Author, YYYY" or "Author, Author, YYYY"
    protected = re.sub(r'[A-Z][a-z]+(?:[,\s]+(?:&\s*)?[A-Z][a-z]+)+\s*,\s*\d{4}', lambda m: save(m.group(0)), protected)
    # Standalone "et al., YYYY" or "et al. (YYYY)"
    protected = re.sub(r'et al\.?,?\s*\(?\d{4}\)?', lambda m: save(m.group(0)), protected)
    # ArXiv IDs
    protected = re.sub(r'arXiv:\d{4}\.\d+', lambda m: save(m.group(0)), protected)
    # English abbreviations with digits
    for abbr in ['P2P', 'A3C', 'LG Chem RESU7H', 'RESU7H', 'RESU 7H',
                 'Python 3.x', 'Python 3', 'n-1', 'Apple M1',
                 'M1 Pro', 'D / D2', 'D2', 'Q≈']:
        protected = re.sub(re.escape(abbr), lambda m: save(m.group(0)), protected)

    # Convert all remaining digits to Persian
    converted = protected.translate(DIGIT_MAP)

    # Restore all protected spans (reverse order)
    for idx in range(len(originals) - 1, -1, -1):
        marker = chr(0xE000 + idx)
        converted = converted.replace(marker, originals[idx])

    return converted


def _fmt(pattern):
    """Human-readable label for a regex, tolerant of zero-width chars."""
    return pattern.replace('‌', '<ZWNJ>').replace('‑', '<U+2011>')


# (label, compiled regex, severity) — ERROR blocks a final build.
ZWNJ = '‌'
LINT_RULES = [
    # NB: a bare "می‌" + verb (می‌دهد، می‌تواند، می‌رود) is CORRECT Persian, so
    # only the specific mis-ZWNJ'd compounds are listed here.
    ('ZWNJ: می‌انگین / می‌انی / می‌انه',
     re.compile(r'می‌(?:انگین|انی|انه)'), 'error'),
    ('ZWNJ: می‌لیون / می‌نیمال / می‌وپیک',
     re.compile(r'می‌(?:لیون|نیمال|وپیک)'), 'error'),
    ('ZWNJ: شب‌که',            re.compile(r'شب‌که'), 'error'),
    ('ZWNJ: در‌برخی',           re.compile(r'در‌برخی'), 'error'),
    ('space: پایان نامه',           re.compile(r'پایان نامه'), 'error'),
    ('ZWNJ: double',                 re.compile(ZWNJ * 2), 'error'),
    ('ZWNJ: ریزشبکه‌های‌هوشمند',
     re.compile('ریزشبکه‌های' + ZWNJ + 'هوشمند'), 'error'),

    ('stats: reversed "value = p/t/n/r/F"',
     re.compile(r'[۰-۹][۰-۹.,٫]*\s*=\s*(?:p|t|n|r|F)(?![\w])'), 'error'),
    ('stats: Latin digit + درصد',   re.compile(r'[0-9]+\s*درصد'), 'error'),
    # Retired suffix-minus style (۳٫۵۶۲-). A decimal separator is required (so
    # section numbering like ۱-۴- نوآوری is not flagged), and a following word
    # character is excluded so hyphenated names (GPT-۳٫۵-turbo) are not flagged.
    ('stats: suffix minus on a decimal value',
     re.compile(r'[۰-۹]+[٫.][۰-۹]+-(?![‌\w])'
                r'|[0-9]+\.[0-9]+-(?![‌\w])'), 'error'),
    ('stats: ASCII hyphen used as minus (want U+2212)',
     re.compile(r'(?<=[=,\[(\s])-(?=[۰-۹]+[٫.][۰-۹]'
                r'|[0-9]+\.[0-9])'), 'error'),
    ('stats: Western dot in Persian digits',
     re.compile(r'[۰-۹]\.[۰-۹]'), 'error'),

    ('terminology: انصاف',     re.compile('انصاف'), 'error'),
    ('terminology: رفاه',      re.compile('رفاه'), 'error'),
    ('terminology: هدررفت',    re.compile('هدررفت'), 'error'),
    ('terminology: زمین‌گذاری',re.compile('زمین' + ZWNJ + 'گذاری'), 'error'),
    ('terminology: زمین‌فیزیکی', re.compile('زمین' + ZWNJ + 'فیزیکی'), 'error'),
    ('terminology: عدالت‌آگاه', re.compile('عدالت' + ZWNJ + 'آگاه'), 'error'),
    ('terminology: نوع‌گرایانه', re.compile('نوع' + ZWNJ + 'گرایانه'), 'error'),
    ('terminology: منصفانه',      re.compile('منصفانه'), 'error'),
    ('terminology: متقابل‌گرا',  re.compile('متقابل' + ZWNJ + 'گرا'), 'error'),
    ('terminology: متقابله‌گری', re.compile('متقابله' + ZWNJ + 'گری'), 'error'),

    ('chars: Arabic yeh ي',         re.compile('ي'), 'error'),
    ('chars: Arabic kaf ك',         re.compile('ك'), 'error'),
    ('frontmatter: advisor key',    re.compile(r'^advisor(_en)?:', re.M), 'error'),
    ('frontmatter: Not assigned',   re.compile('Not assigned'), 'error'),

    ('report-only: آزمایش (calque of شبیه‌سازی)',
     re.compile('آزمایش'), 'warn'),
    ('report-only: OCEAN‑MARL (U+2011 hyphen, intentional)',
     re.compile('OCEAN' + '‑' + 'MARL'), 'warn'),
]


def lint(filepath):
    """Read-only style check. Returns process exit code (0 = clean)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    lines = text.split('\n')

    errors = warns = 0
    for label, rx, sev in LINT_RULES:
        hits = []
        for i, line in enumerate(lines, 1):
            for m in rx.finditer(line):
                hits.append((i, m.group(0)))
        if not hits:
            continue
        if sev == 'error':
            errors += len(hits)
        else:
            warns += len(hits)
        print(f'[{sev.upper():4s}] {label}: {len(hits)}')
        for i, frag in hits[:6]:
            print(f'         L{i}: {frag[:60]!r}')
        if len(hits) > 6:
            print(f'         ... and {len(hits) - 6} more')

    # Abstract numeric parity (Persian vs English) — best-effort, needs PyYAML.
    try:
        import yaml
        m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
        if m:
            fm = yaml.safe_load(m.group(1)) or {}
            fa = str(fm.get('abstract_fa', ''))
            en = str(fm.get('abstract_en', ''))
            tr = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
            fa_n = {x.replace('٫', '.')
                    for x in re.findall(r'[\d۰-۹]+(?:[٫.][\d۰-۹]+)?', fa.translate(tr))}
            en_n = {x.replace(',', '')
                    for x in re.findall(r'\d+(?:,\d{3})*(?:\.\d+)?', en)}
            only_fa = sorted(fa_n - en_n)
            only_en = sorted(en_n - fa_n)
            if only_fa or only_en:
                errors += 1
                print(f'[ERROR] abstract parity: only-FA={only_fa} only-EN={only_en}')
            else:
                print('[ OK  ] abstract numeric parity')
    except ImportError:
        print('[SKIP  ] abstract parity (PyYAML not installed)')

    print(f'\nLint summary: {errors} error(s), {warns} warning(s)')
    return 1 if errors else 0


def main():
    args = sys.argv[1:]
    check_only = '--check' in args
    args = [a for a in args if not a.startswith('--')]

    if check_only:
        if not args:
            print('usage: convert_persian_digits.py --check <file.md>')
            return 2
        return lint(args[0])

    if not args:
        print('usage: convert_persian_digits.py [--check] <file.md>')
        return 2
    filepath = args[0]

    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    persian_before = len(re.findall(r'[۰-۹]', text))
    latin_before = len(re.findall(r'\d', text))

    converted = convert_persian_digits(text)

    persian_after = len(re.findall(r'[۰-۹]', converted))
    latin_after = len(re.findall(r'\d', converted))

    print(f'Before: {persian_before} Persian, {latin_before} Latin')
    print(f'After:  {persian_after} Persian, {latin_after} Latin')
    print(f'Net: +{persian_after - persian_before} Persian, {latin_after - latin_before} Latin')

    orig_lines = text.split('\n')
    new_lines = converted.split('\n')
    changes = 0
    for i, (old, new) in enumerate(zip(orig_lines, new_lines)):
        if old != new:
            changes += 1
            if changes <= 40:
                print(f'\nL{i+1}:')
                print(f'  OLD: {old[:170]}')
                print(f'  NEW: {new[:170]}')
    print(f'\nTotal lines changed: {changes}')

    # Safety: flag any line that still contains Persian digits after conversion
    for i, (old, new) in enumerate(zip(orig_lines, new_lines)):
        if old != new and any(c in new for c in '۰۱۲۳۴۵۶۷۸۹'):
            print(f'\n!!! REVIEW at L{i+1}: {new[:100]}')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(converted)
    print(f'\nWritten: {filepath}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
