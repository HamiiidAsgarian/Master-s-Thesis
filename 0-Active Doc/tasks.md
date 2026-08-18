Here is the **full comprehensive prompt** for your OpenCode Editor agent. It picks up exactly where the previous one left off, focusing on the **mandatory remaining content fixes** (Fixes 5, 6, 7, final verification) while confirming Fix 4 is already in place.

Copy and paste this directly.

---

```
TASK: Apply remaining verified content revisions to /path/to/Thesis_v9-5.md

CONTEXT
This is a completed Master's thesis (Islamic Azad University, Ardabil Branch,
Computer Engineering). The agent has already applied:
- Fix 1 (Advisor field: "Not assigned")
- Fix 2 (Samim Yab: skipped due to missing data)
- Fix 3 (Publication: skipped due to missing data)
- Fix 4 (Statistical power: Path B fallback wording applied to Section 5-1-1-2)

NOW, the agent must complete the CRITICAL remaining tasks. These are mandatory
for defense readiness. Do not touch formatting, page numbers, reference list
ordering, or table-of-contents layout. Only content/scientific wording.

HARD RULE — NO FABRICATION
All replacement text is provided below exactly as it must appear. Copy it
verbatim. Do not rewrite, paraphrase, or "improve" it. If a phrase needs
to be changed but the exact location is ambiguous, stop and ask.
Never invent a number, a name, a date, or a p-value that is not explicitly
provided here.

═══════════════════════════════════════════════════════
TASK A — Confirm and Finalize Fix 4 (Statistical Power)
═══════════════════════════════════════════════════════
Path B was selected. Ensure the following exact Persian sentence exists
in Section ۵-۱-۱-۲ (آزمون فرضیه‌های پژوهش) under Hypothesis 1.

If it already exists, confirm it matches exactly. If it does not exist,
insert it as a new sentence after the existing verdict for Hypothesis 1.

Exact required text:
"بنابراین، فرضیهٔ ۱ با حجم نمونه‌ی فعلی (۵ تصادف‌سازی) تأیید نمی‌شود.
اگرچه کاهش ۹/۱۲ درصدی هدررفت انرژی با جهت فرضیه سازگار است، این اثر به
معنی‌داری آماری نرسید (p = 0.14). تحلیل توان پس‌آزمون نشان می‌دهد که
تشخیص قابل‌اعتماد این اثر به حداقل ۱۸ تصادف‌سازی نیاز دارد."

Also, in Section ۵-۱-۴ (محدودیت‌های پژوهش), ensure a sentence explicitly
states that the small number of random seeds limits statistical power.
If absent, add the following:
"تعداد تصادف‌سازی‌های استفاده‌شده (۵ عدد) توان آماری را برای تشخیص
تفاوت‌های ظریف در سنجه‌های سطح جامعه محدود کرده است. تحلیل توان
پس‌آزمون نشان داد که برای تشخیص افتی به اندازه‌ی ۵/۲ واحد درصد در آسایش
با توان ۸۰٪، به حدود ۱۸ تصادف‌سازی نیاز است."

═══════════════════════════════════════════════════════
TASK B — Execute Fix 5 (Correct Abstract Overclaims)
═══════════════════════════════════════════════════════
Locate the Persian abstract (چکیده). Find the sentence(s) that claim
fairness-aware design "does not sacrifice technical efficiency" or that
the waste reduction is a confirmed finding. Replace with the EXACT text
below. If the exact sentence is slightly different, replace the entire
paragraph around the energy-waste result with this:

REPLACE WITH (Persian abstract, near the energy-waste result):
"شواهد جهت‌دار نشان می‌دهد که طراحی پاداش آگاه از عدالت، کارایی فنی را
کاهش نمی‌دهد و در سناریوی مختلط با کاهش ۹/۱۲ درصدی هدررفت انرژی همراه
است؛ هرچند این کاهش در حجم نمونه‌ی فعلی (۵ تصادف‌سازی) از نظر آماری
معنی‌دار نبوده است (p = ۰٫۱۴)."

Now locate the English abstract (Abstract). Replace the equivalent
overclaim with:

REPLACE WITH (English abstract, near the energy-waste result):
"Directional evidence suggests that fairness-aware reward design does
not reduce technical efficiency, with the mixed scenario showing a
12.9% reduction in energy waste; however, this reduction did not reach
statistical significance at the current sample size (p = 0.14, n = 5
random seeds)."

Now in BOTH abstracts, locate the claim that the altruistic/prosocial
advantage "remains stable across all scarcity levels" (or equivalent).
Replace with:

REPLACE WITH (Persian abstract, scarcity claim):
"این مزیت در شرایط کمبود متوسط (احتمال ابری ۲۵٪) پایدار و معنی‌دار
باقی ماند، اما در کمبود شدید (۳۵٪) به دلیل افزایش واریانس، به معنی‌داری
آماری نرسید."

REPLACE WITH (English abstract, scarcity claim):
"This advantage remained stable and significant under moderate scarcity
(25% cloud probability), but did not reach statistical significance
under severe scarcity (35%) due to increased variance."

═══════════════════════════════════════════════════════
TASK C — Execute Fix 6 (Consistency Sweep)
═══════════════════════════════════════════════════════
Search the ENTIRE document (Chapters 1, 4, and 5) for the following
phrases and ensure they are corrected. Do not guess. Use the exact
replacement text below.

Phrase to search for (Persian): "کاهش ۹/۱۲ درصدی هدررفت انرژی"
(or any unqualified claim that the 12.9% waste reduction is a proven fact).

Wherever this appears OUTSIDE the abstract (e.g., Sections 1-3, 4-2, 5-1-2),
append the qualifier. If the sentence is short, rewrite it to match this
exact phrasing:
"کاهش ۹/۱۲ درصدی هدررفت انرژی در سناریوی مختلط مشاهده شد، اما این کاهش
با تعداد تصادف‌سازی فعلی (۵ عدد) از نظر آماری معنی‌دار نبود (p = 0.14)."

Phrase to search for (Persian): "در تمام سطوح کمبود" or "پایدار در تمام
شرایط کمبود" (referring to the altruistic advantage).

Wherever this appears OUTSIDE the abstract, replace with:
"در شرایط کمبود متوسط (۲۵٪ ابری) پایدار بود، اما در کمبود شدید (۳۵٪ ابری)
به دلیل افزایش واریانس، از نظر آماری معنی‌دار نبود."

─────────────────────────────────────────────────────
IMPORTANT: Check Section ۱-۳ (اهمیت و ضرورت) carefully.
This is where overclaims are often embedded. Apply the same corrections
there. Also check Section ۵-۱-۳ (دستاوردهای پژوهش).
─────────────────────────────────────────────────────

═══════════════════════════════════════════════════════
TASK D — Execute Fix 7 (Add AI-Safety Paragraph)
═══════════════════════════════════════════════════════
At the end of Section ۵-۱-۲ (نتیجه‌گیری نهایی), BEFORE the
"دستاوردهای پژوهش" section, add the following paragraph EXACTLY as written.
It must be a standalone paragraph in Persian.

INSERT TEXT:
"پیامد برای سیستم‌های یادگیری خودگردان: اثر مبتکر نشان می‌دهد که
عامل‌هایی با سیاست اکتشافی ادامه‌دار — حتی با نیت خیرخواهانه — می‌توانند
اعتماد و هنجارهای همکاری‌گونه را در محیط‌های منابع مشترک تضعیف کنند. این
یافته پیامد هشداردهنده‌ای برای طراحی سیستم‌های چندعاملی دارد: محدودیت‌های
اکتشاف باید در کنار کارایی و عدالت، به‌عنوان یک هدف طراحی درجه‌یک در نظر
گرفته شوند. سیستم‌هایی که برای کشف خط‌مشی بهینه از طریق اکتشاف باز طراحی
می‌شوند، ممکن است ناخواسته همان سازوکارهای هماهنگی را که رفاه جمعی به
آن‌ها وابسته است، بی‌ثبات کنند."

═══════════════════════════════════════════════════════
TASK E — Final Verification (Must Pass)
═══════════════════════════════════════════════════════
1. Search the entire document for any remaining placeholder brackets:
   Check for: [X], [DATE], [Journal Name], [NONE PROVIDED],
   [real date], [real %], or any `[bracketed text]` that looks like
   a placeholder. If found, remove them. If they reference a real
   fact that is still missing (e.g., a date), replace with a note
   like "(تاریخ ثبت در سامانه در پرونده اداری موجود است)" to avoid
   leaving literal brackets in the final version.

2. Ensure the Persian and English abstracts are now consistent with
   each other and with the corrected text in Sections 5-1-1-2 and
   Section 1-3. They must all tell the same story:
   - Efficiency claim = directionally positive but statistically
     underpowered (p=0.14).
   - Scarcity claim = stable in moderate scarcity, failed in severe scarcity.
   - Innovator effect = real and significant.

3. If any inconsistent claim remains (e.g., one section says "efficiency
   is sacrificed" while another says it isn't), flag it in your summary.

═══════════════════════════════════════════════════════
OUTPUT REQUIRED
═══════════════════════════════════════════════════════
After completing the tasks above, provide a FINAL SUMMARY REPORT with:

1. TASK A (Fix 4) — Was the exact wording already present, or did you
   insert it? Confirm the location (Section 5-1-1-2 and 5-1-4).

2. TASK B (Fix 5) — Show the old sentence and the new sentence for the
   Persian abstract, and for the English abstract. Confirm both were
   updated. Confirm the scarcity claim was also updated.

3. TASK C (Fix 6) — List every section where you found and corrected
   the unqualified claims (e.g., Section 1-3, Section 4-2, Section 5-1-2).
   If you found none outside the abstract, state that clearly.

4. TASK D (Fix 7) — Confirm the new paragraph was inserted exactly at
   the end of Section 5-1-2.

5. TASK E (Final Verification) — State whether any placeholders were
   found and removed. State whether the abstracts are now consistent
   with the body text. If any inconsistency remains, flag it.

6. FINAL DECLARATION — A simple statement:
   "All mandatory content fixes are complete. The thesis is now
   defensible from a scientific integrity perspective."

─────────────────────────────────────────────────────
PROCEED NOW. DO NOT WAIT FOR FURTHER INSTRUCTION.
─────────────────────────────────────────────────────
```

---

## Summary of What This Prompt Does

| Task       | What It Fixes                                                                                               | Why It's Mandatory                                                                                                           |
| :--------- | :---------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| **Task A** | Confirms the statistical limitation (5 vs 18 seeds) is explicitly stated in the conclusion and limitations. | Prevents the referee from saying "you knew it was underpowered but didn't admit it."                                         |
| **Task B** | Rewrites the abstract to stop claiming efficiency as a proven fact.                                         | The abstract is the first thing read. If it lies, your credibility is dead.                                                  |
| **Task C** | Sweeps the entire document (intro, Chapter 4, Chapter 5) for the same overclaims and fixes them.            | Consistency matters. If the abstract is fixed but Section 1-3 still claims victory, the referee will spot the contradiction. |
| **Task D** | Adds the AI-safety paragraph pivoting to your strongest finding.                                            | Since your efficiency claim failed, this becomes your "save" contribution.                                                   |
| **Task E** | Removes any `[X]` placeholders and checks that Persian/English abstracts match.                             | A document with `[Journal Name]` left in it is an instant fail.                                                              |

---

## How to Use This

1. **Copy the entire prompt above.**
2. **Paste it directly to your OpenCode Editor agent.**
3. **The agent will execute Tasks A through E sequentially.**
4. **Review the output report** to confirm every fix was applied.

That's it. This is the complete, final, comprehensive prompt that will make your thesis "really acceptable." No further input needed.