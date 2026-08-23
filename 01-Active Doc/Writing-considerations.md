# Farsi Thesis Markdown — Authoring & Cleanup Standards

Instructions for whoever (or whatever agent) edits `thesis.md` before it goes
through `Cloude_Converter_adapted.py`. Follow these so the converter's
automatic fixes (bidi-aware parentheses, punctuation, TOC/List fields) have
clean input to work with. The converter now handles bracket-direction and
spacing automatically — **do not hand-edit parenthesis direction**; just keep
the rules below and let the script do that part.

## 1. Character-level correctness (fix these first, by find-and-replace)

| Wrong                                                            | Right                                                                                           | Why                                                                                                                                                                                                     |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ي` (Arabic yeh, U+064A)                                         | `ی` (Persian yeh, U+06CC)                                                                       | Arabic and Persian yeh look alike but are different code points; mixing them breaks search, sorting, and some fonts' final-form rendering.                                                              |
| `ك` (Arabic kaf, U+0643)                                         | `ک` (Persian kaf, U+06A9)                                                                       | Same issue as above.                                                                                                                                                                                    |
| Arabic-Indic digits `٠١٢٣٤٥٦٧٨٩`                                 | Persian digits `۰۱۲۳۴۵۶۷۸۹` (in Farsi prose) or plain ASCII `0-9` (in equations/citations/code) | Three digit systems exist; pick one per context and don't mix silently.                                                                                                                                 |
| A plain space where a compound word needs joining, e.g. `می روم` | ZWNJ (U+200C, "half-space"): `می‌روم`                                                            | A full space visually splits what should read as one word. Common spots: `می‌`, `نمی‌`, `‌ها` (plural), `‌تر` / `‌ترین` (comparative/superlative), `‌ای`                                                      |
| A normal space glued to `‌ها` plural suffix, e.g. `کتاب ها`       | `کتاب‌ها` (ZWNJ)                                                                                 | Same rule, most common single source of "extra space" complaints in Farsi Word docs.                                                                                                                    |
| ASCII `,` `;` `?` sitting between two Farsi words                | `،` `؛` `؟`                                                                                     | The converter auto-corrects this when ASCII punctuation is flanked by Farsi characters on both sides — but it can't catch every case (e.g. at line breaks), so fix it at the source when you notice it. |
| Two+ consecutive spaces                                          | One space                                                                                       | Silently produces uneven-looking justified text and can move captions off by a character in Word's TOC.                                                                                                 |

Do **not** try to manually reverse or "pre-flip" parentheses/brackets to
compensate for how they might render — the converter now resolves each
`(...)`/`[...]` pair by its content and renders it correctly. Manually
flipping them in the source will just make it wrong again.

## 2. Parentheses & brackets — just keep them literal and balanced

- Always type `(` before the parenthetical content and `)` after it, in
  logical reading order — regardless of whether the content inside is Farsi,
  English, or a number. The converter figures out direction from context.
- Keep every `(` matched with a `)`, and every `[` matched with a `]`, **on
  the same logical unit** (nesting is fine, but don't leave one hanging —
  the converter's pre-flight validator will warn about unbalanced brackets,
  and unbalanced brackets are the one case it can't safely auto-direction).
- One space before an opening bracket, no space just inside it; no space
  just before a closing bracket, one space just after it — you don't have
  to enforce this by hand, the converter normalizes it, but keeping it
  reasonably clean at the source makes any manual line-editing easier.
- Square brackets `[12]` used as an inline citation marker: keep the number
  immediately inside, e.g. `روشی که در [12] ارائه شد`, not `[ 12 ]`.
- Avoid using square brackets for anything except: (a) citation markers, or
  (b) Markdown link/image/footnote syntax (`[text](url)`, `[^note]`). Mixing
  other uses in a bidi-heavy paragraph is a common source of confusion.

## 3. Numbers, decimals, equations

- In Farsi prose, write numbers as Persian digits (`۳٫۱۴`, using `٫` as the
  Persian decimal separator) unless the number is inside an equation or a
  citation, where plain ASCII (`3.14`) is standard and expected.
- Don't mix digit systems inside the *same* number (e.g. `3۴` or `۱2`).
- Equation numbering: label a display equation like this so the converter
  turns it into a proper "List of Formulas" entry:
  ```
  $$ E = mc^2 \qquad \text{(1-1)} $$
  ```
  The `(chapter-number)` label goes through `\qquad \text{...}`, not as
  plain trailing text — this keeps it out of the OMML math zone so it
  renders as ordinary LTR text instead of getting mixed into the equation.
- Inline math uses single `$...$`; the converter also accepts `\(...\)` and
  normalizes it to `$...$` automatically. Keep inline math on one line;
  don't let a `$...$` span span a paragraph break.

## 4. Structural conventions the converter expects

| Content                                 | Markdown pattern                                                                                                                                                                                                                    |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Chapter                                 | `# عنوان فصل` (starts new page, centered, auto-numbers chapters)                                                                                                                                                                    |
| Section / sub-section / sub-sub-section | `##`, `###`, `####` — type the `2-4` style numbering directly into the heading text yourself, e.g. `## 2-4 عنوان بخش` (the converter does **not** auto-number sections — only chapter/table/figure/equation counters are automatic) |
| Table caption                           | A line `Table: <caption text>` (or `جدول: <caption text>`) immediately before the pipe table — caption renders **above** the table, auto-numbered `جدول ۲-۱`                                                                        |
| Figure                                  | `![<caption text>](path/to/image.png)` — caption renders **below** the figure, auto-numbered `شکل ۲-۱`                                                                                                                              |
| Labeled equation                        | `$$ ... \qquad \text{(2-3)} $$` — feeds "فهرست فرمول‌ها" (List of Formulas)                                                                                                                                                          |
| Footnote                                | `text[^1]` at point of use, `[^1]: definition` anywhere else in the file                                                                                                                                                            |
| Block quote                             | `> quoted text` (renders as the indented "long quote" style, no quotation marks added)                                                                                                                                              |
| Bold / italic / bold-italic             | `**bold**`, `*italic*`, `***both***`                                                                                                                                                                                                |
| References section heading              | Exactly `منابع`, `منابع فارسی`, or `منابع غیرفارسی` (triggers IEEE-style `[1]`, `[2]`... numbering) — put Farsi sources first, then non-Farsi, in that order in the file (the converter does not reorder them)                      |

## 5. Pre-flight checklist (run before every conversion)

The converter's built-in `validate_markdown()` pass checks most of this
automatically and prints warnings — but if you're editing by hand or via an
agent, check for these explicitly before handing the file back:

1. No Arabic ي / ك anywhere (`ی` / `ک` only).
2. No Arabic-Indic digits (٠-٩) — Persian ۰-۹ in prose, ASCII in
   equations/code/citations.
3. No literal double spaces.
4. No ASCII `,` `;` `?` stranded between two Farsi words.
5. Every `(`/`[` has a matching `)`/`]` on the same logical line or block.
6. Every `$` and `$$` math delimiter is closed.
7. No duplicate heading text used twice in a way that would collide (the
   validator flags exact duplicate heading text — rename or add context if
   two headings are identical, since Word's bookmark/hyperlink generation
   for TOC entries needs unique anchors).
8. Table captions use the `Table:`/`جدول:` line immediately before the pipe
   table — not after, not two lines before.
9. Figure alt-text is the caption you actually want printed — it's not just
   accessibility text here, it becomes the visible caption.
10. Reference list order: Farsi sources first, then non-Farsi.

## 6. What the converter fixes automatically (don't hand-fix these)

- Parenthesis/bracket **direction** in mixed Farsi/English runs — resolved
  per bracket pair from its content, not per character.
- Spacing immediately inside/outside `()`/`[]`.
- Space before Persian punctuation (removed) and after it (enforced).
- ASCII `,`/`;`/`?` → `،`/`؛`/`؟` when flanked by Farsi characters.
- Decimal points/commas between digits (kept as one number, not split).
- RTL/LTR run splitting for headings, body text, table cells, and captions
  (each gets the correct per-character-run direction, not a single
  forced-RTL blob).

## 7. What still requires a manual pass in Word after conversion

- Ctrl+A, then F9, to actually populate/refresh فهرست مطالب / فهرست جداول /
  فهرست اشکال / فهرست فرمول‌ها (Word fields don't self-populate on file open).
- Double-clicking any equation that fell back to plain LTR text (i.e.
  LaTeX the converter's `latex_to_omml()` couldn't parse) to rebuild it in
  Word's Equation Editor.
- Visually spot-checking any parenthetical that mixes Farsi *and* English
  *and* a citation number all in one unit — the converter picks one
  dominant direction per bracket pair, but a genuinely three-way-mixed
  parenthetical is a judgment call no automated rule gets right 100% of
  the time.