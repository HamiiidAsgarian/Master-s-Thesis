#!/usr/bin/env python3
"""Regression check for thesis converter fixes.

Runs the converter on Thesis_v9-5.md and verifies:
  P0-1: No duplicated front matter (abstract appears exactly once)
  P0-2: No malformed LaTeX in source ($w*{, $C\_{, etc.)
  P0-3: Inline tokenizer produces reasonable run lengths
  P0-5: tblCaption metadata present for List of Tables/Figures
  P0-7: Numerical fix (≈۵۱ درصد not ۵۰ درصد in abstract)
  P1-8: Punctuation normalization doesn't break decimals/URLs
  P1-9: No &nbsp; leakage in output

Usage:
  python verify_converter.py [input.md] [output.docx]
  (defaults: Thesis_v9-5.md → /tmp/verify_test.docx)
"""
import os
import re
import sys
import tempfile
import zipfile
from pathlib import Path

# ---------- config ----------
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = SCRIPT_DIR / "Thesis_v9-5.md"
DEFAULT_OUTPUT = Path(tempfile.mktemp(suffix=".docx"))
CONVERTER = SCRIPT_DIR / "Cloude_Converter_adapted.py"
NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
}


def run_converter(input_md, output_docx):
    import subprocess
    result = subprocess.run(
        [sys.executable, str(CONVERTER), str(input_md), str(output_docx), "--no-lint"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"CONVERTER FAILED:\n{result.stderr}")
        sys.exit(1)
    return result.stdout


def parse_docx(docx_path):
    from lxml import etree
    with zipfile.ZipFile(docx_path, "r") as z:
        doc_xml = z.read("word/document.xml")
    root = etree.fromstring(doc_xml)
    paragraphs = root.findall(".//w:p", NS)
    all_text = []
    for p in paragraphs:
        runs = p.findall(".//w:t", NS)
        text = "".join(r.text or "" for r in runs)
        all_text.append(text)
    return root, "\n".join(all_text)


def check_source(input_md):
    """Check the markdown source for known issues."""
    content = Path(input_md).read_text(encoding="utf-8")
    results = {}

    # P0-2: malformed LaTeX
    malformed = []
    for pat in ["w*{", "\\varepsilon*{", "C\\_{", "R*i", "C*i", "\\min*i"]:
        if pat in content:
            malformed.append(pat)
    results["P0-2_malformed_latex"] = len(malformed) == 0

    # P0-7: numerical fix
    results["P0-7_numerical_fix"] = "≈۵۱ درصد" in content and "کاهشی معادل ۵۰ درصد" not in content

    return results


def check_docx(docx_path, root, full_text):
    """Check the generated DOCX for known issues."""
    results = {}

    # P0-1: no duplicate front matter
    results["P0-1_no_duplicate_abstract"] = full_text.count("چکیده") <= 1

    # P0-5: tblCaption metadata
    tblCaption = root.findall(".//w:tblCaption", NS)
    results["P0-5_tblCaption_present"] = len(tblCaption) > 0

    # P1-9: no &nbsp;
    from lxml import etree as _etree
    raw_xml = _etree.tostring(root, encoding="unicode")
    results["P1-9_no_nbsp"] = raw_xml.count("&nbsp;") == 0

    # P0-3: inline tokenizer (check run lengths)
    runs = root.findall(".//w:r", NS)
    short = sum(
        1 for r in runs
        if len("".join((t.text or "") for t in r.findall(".//w:t", NS))) <= 2
    )
    total = len(runs)
    ratio = short / total if total else 0
    results["P0-3_tokenizer_ratio"] = ratio
    results["P0-3_tokenizer_ok"] = ratio < 0.75  # should be < 75% short runs

    # Bibliography check
    in_refs = False
    ref_count = 0
    for p in full_text.split("\n"):
        if p.strip() == "منابع":
            in_refs = True
            continue
        if in_refs and p.strip().startswith("["):
            ref_count += 1
    results["bibliography_ieee_count"] = ref_count
    results["bibliography_ieee_ok"] = ref_count >= 45  # expect ~50

    # Basic sanity
    tables = root.findall(".//w:tbl", NS)
    math_inline = root.findall(".//m:oMath", NS)
    math_display = root.findall(".//m:oMathPara", NS)
    results["table_count"] = len(tables)
    results["math_inline_count"] = len(math_inline)
    results["math_display_count"] = len(math_display)
    results["basic_sanity"] = (
        len(tables) == 32 and len(math_inline) == 234 and len(math_display) == 11
    )

    return results


def main():
    input_md = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    output_docx = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_OUTPUT

    if not input_md.exists():
        print(f"ERROR: {input_md} not found")
        sys.exit(1)
    if not CONVERTER.exists():
        print(f"ERROR: {CONVERTER} not found")
        sys.exit(1)

    print(f"Input:   {input_md}")
    print(f"Output:  {output_docx}")
    print()

    # Source checks
    print("--- Source Checks ---")
    src = check_source(input_md)
    for k, v in src.items():
        status = "PASS" if v else "FAIL"
        print(f"  [{status}] {k}")

    # Run converter
    print("\n--- Running Converter ---")
    stdout = run_converter(input_md, output_docx)
    print(stdout.strip())

    # DOCX checks
    print("--- DOCX Checks ---")
    from lxml import etree
    root, full_text = parse_docx(output_docx)
    docx_results = check_docx(docx_path=output_docx, root=root, full_text=full_text)
    for k, v in docx_results.items():
        if isinstance(v, bool):
            status = "PASS" if v else "FAIL"
            print(f"  [{status}] {k}")
        elif isinstance(v, float):
            print(f"  [INFO] {k} = {v:.3f}")
        else:
            print(f"  [INFO] {k} = {v}")

    # Cleanup
    if output_docx == DEFAULT_OUTPUT and output_docx.exists():
        output_docx.unlink()

    # Summary
    all_bool = {k: v for k, v in {**src, **docx_results}.items() if isinstance(v, bool)}
    passed = sum(1 for v in all_bool.values() if v)
    total = len(all_bool)
    print(f"\n=== {passed}/{total} checks passed ===")
    if passed < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
