# ──────────────────────────────────────────────
# Combined thesis generation from translated chapters
# ──────────────────────────────────────────────
# Steps below assume we are in the repo root (~/Desktop/sim).

# 1. Combine chapters (order: intro, lit rev, method, results, discussion, refs)
#    Uses the `-fa-d.md` (final) versions. Remove translation-header noise from
#    chapter 1 and fix heading levels (## → # for chapter, ### → ## for sections).

# 2. Install dependencies (one-time)

pip install python-docx pyyaml
brew install pandoc              # or download from pandoc.org

# 3. Run the converter (use absolute paths + pyenv Python)

/Users/hamidasgharian/.pyenv/versions/3.10.12/bin/python3 \
  "/Users/hamidasgharian/Desktop/sim/HamidOutput/DocX Converter/Cloude_Converter.py" \
  "/Users/hamidasgharian/Desktop/sim/HamidOutput/thesis_full.md" \
  "/Users/hamidasgharian/Desktop/sim/HamidOutput/Thesis_Output.docx" \
  --branch ardabil

# 4. Open Thesis_Output.docx in Word, Ctrl+A, F9 to refresh fields.

# ──────────────────────────────────────────────
# Appendix: exact step used last time
# ──────────────────────────────────────────────
# This Python one-liner builds thesis_full.md from YAML + chapters:

python3 -c "
import re
d = '/Users/hamidasgharian/Desktop/sim/HamidOutput/Sections'
# YAML
y = open(f'{d}/0.yaml').read()
# Ch1 — strip 7-line header, fix headings
c1 = open(f'{d}/1-fa-d.md').read()
c1 = '\n'.join(c1.split('\n')[7:])
c1 = re.sub(r'^## ', '# ', c1, flags=re.MULTILINE)
c1 = re.sub(r'^### ', '## ', c1, flags=re.MULTILINE)
c1 = re.sub(r'^#### ', '### ', c1, flags=re.MULTILINE)
c1 = c1.replace('**[پایان محتوای فایل]**', '')
# Ch2–6 as-is
rest = '\n'.join(open(f'{d}/{i}-fa-d.md').read() for i in range(2,7))
open('/Users/hamidasgharian/Desktop/sim/HamidOutput/thesis_full.md','w').write(y + '\n' + c1 + '\n' + rest)
"

# ──────────────────────────────────────────────
# Checklist Before Running the Converter
# ──────────────────────────────────────────────
# ✅    Combined all chapters (1-fa-d.md – 6-fa-d.md) into thesis_full.md
# ✅    Prepended 0.yaml front matter (already delimited with ---)
# ✅    Excluded 0-fa-d.md content (TOC, Lists) — the script auto-generates them
# ✅    Installed python-docx, pyyaml, and pandoc
# ✅    Checked pandoc path is /opt/homebrew/bin/pandoc (update in script if needed)
# ✅    Verified Persian fonts (Lotus Thin, Lotus Bold) are installed, or use --fa-font
# ⚠    1-fa-d.md may have a translation-header block — strip it before combining
# ⚠    Heading levels in 1-fa-d.md may need fixing (##→#, ###→##, ####→###)
# ⚠    Chapter 5 may skip from ۵-۲ directly (no ۵-۱ section) — this is normal
