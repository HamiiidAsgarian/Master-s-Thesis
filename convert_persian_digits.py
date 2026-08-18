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


def main():
    filepath = sys.argv[1] if len(sys.argv) > 1 else '0-Active Doc/Thesis_v9-5.md'

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

    # Safety: check for corruption in lines 1-178
    for i, (old, new) in enumerate(zip(orig_lines, new_lines)):
        if old != new and i < 178:
            if any(c in new for c in '۰۱۲۳۴۵۶۷۸۹'):
                print(f'\n!!! CORRUPTION at L{i+1}: {new[:100]}')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(converted)
    print(f'\nWritten: {filepath}')


if __name__ == '__main__':
    main()
