## Action Plan — Path to "Standard and Complete"

Ordered by dependency (later phases assume earlier ones are closed). Each item tags the responsible agent: **Lead** (me, content/framing/judgment + direct edits to `thesis_full.md`), **NotebookLM** (literal extraction from source PDFs only), **OpenCode** (local build, `results/` data, images, DOCX pipeline), **Student** (approvals/decisions only I can't make for him).

### Phase 1 — Close the Bibliography Audit
*(blocks Phase 4; partially blocks Phase 2)*

1. **Resolve Alshehri & Gaunt (2020)** — highest priority, load-bearing for Ch3 battery/demand-pattern justification.
   - **Lead**: web-verify whether any real paper matches; if not, decide replacement citation or reword the Ch3 claim to lean only on already-verified sources (Charbonnier, Bui et al., Kusatake, Ofgem).
   - **Student**: sign off if the Ch3 claim needs to be weakened/reworded rather than replaced.
2. **Resolve Karimi, Zhang & Li (2024) and Zhou & Sun (2023)** — likely remove.
   - **Lead**: web-verify; find real replacements only if a specific claim depends on them, otherwise cut.
3. **Verify the ~14 remaining unchecked references** (Fehr & Gächter 2000, Fischbacher & Gächter 2010, Gersani et al. 2001 — flagged as most suspicious, Moon et al. 2022, Le/Nguyen/Nguyen 2022, Li & Zhang 2022, Rathnayaka et al. 2014, Qiu/Wang/Strbac 2021, Moret & Pinson 2019/2020, Skoplaki & Palyvos 2009, Hernandez-Leal et al., Binz & Schulz 2023, Leng 2025).
   - **Lead**: web search each; confirm real vs. fabricated/wrong metadata; fix or cut.
4. **Spot-check the "low risk" canonical works** (Sutton & Barto, Watkins & Dayan, Tan, QMIX, MADDPG, Oliehoek & Amato, Ostrom, Gini) — light touch only, not full budget.
   - **Lead**: quick confirmation pass, no deep verification needed.
5. **Update Ch6 reference list** to final verified set (expect ~20–30 entries).
   - **Lead**: direct edit to `thesis_full.md`.

### Phase 2 — In-Text Claim Audit
*(the student's explicit ask, not yet done systematically beyond baseline papers)*

6. **Check every in-text claim against what its cited source actually says**, not just correct metadata — sentence-by-sentence pass through Ch1–Ch5 wherever a citation supports a factual/quantitative claim.
   - **NotebookLM**: pull the literal claim/finding from each source's own text (never from thesis or another citation of it) — for sources it holds.
   - **Lead**: judge whether the thesis's claim accurately represents the source; rewrite or cite differently where it doesn't; verify against web for the ~14 sources not in NotebookLM.
7. **Any claim that still can't be verified** → remove or reword, per student's standing instruction (accuracy over reference-list size).
   - **Lead**: execute the edit.

### Phase 3 — Structural / Template Compliance

8. **Rename the 5 main chapters** to the university's exact template titles (کلیات / مبانی نظری و پیشینه تحقیق / روش پیشنهادی / تجزیه و تحلیل نتایج / نتیجه‌گیری).
   - **Lead**: direct edit to headers; check whether renaming implies any restructuring of subsections to match template expectations, not just title swaps.
9. **Confirm no other template-required elements are missing** (e.g., required front-matter, abstract-in-Persian placement, appendix conventions) — not explicitly flagged yet, worth a deliberate check rather than assuming only chapter titles are outstanding.
   - **Lead**: review against university template; **Student**: confirm template document/requirements if ambiguous.

### Phase 4 — Citation Style Conversion (APA → IEEE)
*(explicitly sequenced after Phase 1 closes — don't convert citations about to change)*

10. **Convert reference list to numbered IEEE style.**
    - **Lead**: direct edit, Ch6.
11. **Convert every in-text `(Author, Year)` to `[N]`** throughout the document, keeping numbering consistent with final reference order.
    - **Lead**: direct edit; this is mechanical but high-error-risk (numbers must match), so worth a verification pass (grep every `[N]` back against Ch6) before calling it done.

### Phase 5 — Readability Pass

12. **Light redundancy check** across the document (already ruled out one false alarm on Jain's index — Ch2 conceptual vs. Ch3 formal definition is correct, not duplicated).
    - **Lead**: read-through, cut genuine redundancy only; no aggressive page-cutting given relaxed page constraint.

### Phase 6 — Image & Results Verification
*(not explicitly listed in "what remains" but implied — worth confirming before DOCX)*

13. **Confirm the 4 new baseline validation figures and any updated figures actually exist in `results/` and match what the text describes** (numbers, captions, axis labels).
    - **OpenCode**: paste actual file listing + image metadata as proof — not a "done" summary.
    - **Lead**: verify pasted evidence against thesis text before sign-off.
14. **Resync OpenCode's local `Sections/*.md` and build pipeline** with the canonical `thesis_full.md` (flagged in handoff as out of sync).
    - **OpenCode**: perform sync.
    - **Lead**: verify via diff/grep output, not a claim of "synced."

### Phase 7 — DOCX Generation
*(deliberately last, after all content is final)*

15. **Run `pandoc thesis_full.md -o output.docx --reference-doc="template.docx"`** using the university's real template.
    - **OpenCode**: execute where real images resolve.
    - **Lead**: request the actual generated file / a rendered screenshot as proof, check headings, TOC, figure numbering, citation formatting survived the conversion.

### Phase 8 — English Document Parity
*(fully deferred, done only once Persian version is 100% final)*

16. **Update `ACADEMIC_v3_En.md`** to match the finalized Persian thesis, once and only once — no incremental syncing.
    - **Lead**: content/translation-consistency decisions.
    - **OpenCode**: file handling if needed.

### Phase 9 — Final Sign-off

17. **Final read-through against professor's original objection** (comparisons must be reimplemented, not literature-estimated) — confirm §4-10-1/§4-11 fully answer it.
    - **Lead**.
18. **Student final review and approval** before submission.
    - **Student**.

---

Given the dependency chain, I'd suggest we start at **Phase 1, item 1 (Alshehri & Gaunt)** since it's both highest-risk and blocking. Want me to start there now?
