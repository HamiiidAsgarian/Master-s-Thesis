# Handoff Briefing — Master's Thesis Project (Personality-Driven MARL Energy Sharing)

## Your role
You are the **lead research advisor** for this thesis. The student (Hamid Asgharian, Islamic Azad University, Ardabil) relies on you to make all judgment calls on content, claims, citations, and structure. Two other agents assist and execute under your direction:
- **NotebookLM** — holds the actual source PDFs (~28 files). Use it only for *literal extraction* (exact title/author/venue from a source's own first page) — never trust its summaries or judgment calls, and always specify "from the source file itself, not from any thesis document" since it has previously pulled corrupted data from the thesis by mistake.
- **OpenCode** — a local coding agent with access to the student's actual project folder, `results/` (simulation outputs, images, CSVs), and the real thesis build pipeline. It executes what you specify; it does not make content or framing decisions. **Do not trust its "done"/"verified" claims at face value — multiple times this session it reported a fix as applied when the file showed otherwise.** Always ask for the actual pasted text/data as proof, not a summary of what it did.

You (the new lead) work only with the **thesis MD file** (attached: `thesis_full.md`, the current canonical version) using your own file-editing tools. OpenCode owns images, the `results/` data, and DOCX generation.

## The goal
Original state: a 114-page thesis with a Chapter 4 comparison section that used numbers copied from other papers' published figures ("estimated from published figures," marked †), which the student's professor flagged as unacceptable — insisting comparisons must be based on the student's own reimplementation of 4–5 other methods, run under matched conditions, with real statistics.

Target: a thesis with a genuinely rigorous Chapter 4, real reproduced baselines, a fully verified reference list, and structural compliance with the university's template — **page count is explicitly not a constraint** (student confirmed quality matters more than hitting 80-90 pages).

## What has been done (in order)

### 1. Baseline reimplementation (the core methodological fix)
Reimplemented 4 comparison methods **inside the student's own simulation environment** (10 houses, 1.3kW PV peak, 7kWh battery, 15% cloud probability), same 5 seeds (42, 123, 456, 789, 1011) as the main runs, so comparisons are apples-to-apples instead of literature-estimated:
- **Charbonnier et al. (2022)** — marginal/counterfactual IQL with hysteretic asymmetric updates. First attempt (same-hour counterfactual) gave a structurally zero reward signal — environment-specific finding, documented, not hidden. Fixed with end-of-day counterfactual; this version works and beats the no-sharing control.
- **Kusatake et al. (2023)** — NSGA-II evolutionary multi-objective optimizer (no learning loop). Found: comfort/fairness saturate on 85%+ of "sunny" days (battery covers all demand regardless of policy), so the GA's choice is arbitrary there; only the ~15-18% "cloudy" days show genuine optimization. This is documented as an authentic limitation of Kusatake's formulation, not a bug.
- **Behrunani et al. (2023)** — decentralized generalized Nash equilibrium (GNE) game, projected-gradient best-response. Original "cost reduction" is a monetary quantity in the source paper; adapted to an energy-unit analog (kWh unmet + wasted) since there's no price mechanism in this environment — this was a genuine mistranslation we caught and fixed (comfort-based version was structurally dead, energy-based version works). Achieves zero waste (myopic per-hour optimization) but the lowest comfort of the four baselines (no cross-hour battery coordination).
- **May & Huang (2023)** — single-level PPO (dropped their bi-level price-planner, no price mechanism exists in this env). Reward=comfort+fairness gives PPO nothing to learn from; documented honestly as a finding, not glossed over.
- Built an **`always_default` (no-sharing) control** that never existed before. Critical finding: **the thesis's main OCEAN-MARL scenarios do not beat this control on absolute comfort/fairness** — they only beat it on waste reduction (~45-50%). This is now the corrected, honest framing throughout (abstract, Ch4, Ch5).

### 2. Mechanistic isolation (why some methods work and others don't)
Ran a controlled 2×2 experiment (objective type: personality-weighted vs. community/role-free × reward horizon: per-step vs. end-of-day-counterfactual) to find the causal factor. **Result: neither variable alone explains it.** The actual cause is the **Q-learning update rule** — optimistic initialization + symmetric updates never resolves near-zero-magnitude reward signals (ties stay unbroken, policy collapses to default); Charbonnier's asymmetric/hysteretic low-α updates escape this. This is now written into a new §4-11 in the thesis as a genuine mechanistic finding, framed as a methodological insight (not a flaw), with a matching future-work note in Ch5.

### 3. Bibliography audit (ongoing, high-value, not finished)
**Confirmed pattern: real papers cited with fabricated/wrong author names, titles, or venues.** Fixed so far:
- Charbonnier, Kusatake, Behrunani, Jadhav, Aloor, Ma et al., Ali et al., Zhang et al. — all real papers, all had wrong metadata, all corrected in Ch6 to verified real data.
- Fehr & Schmidt (1999) — wrong middle initial, fixed.
- Aloor's paper is about **multi-agent navigation fairness, not energy** — removed as a quantitative energy comparator (it fabricated "community comfort" numbers for a paper that never measures that), kept only as a general MARL-fairness citation.

**Unresolved — likely fully fabricated (not just wrong metadata, no matching paper found at all):**
- Alshehri, J., & Gaunt, C. (2020) — **this is serious**: cited repeatedly as the physical justification for the thesis's battery capacity (7kWh) and demand-pattern parameters in Chapter 3. Needs either a real replacement citation or the claim reworded to rely only on the citations that did verify (Charbonnier, Bui et al., Kusatake, Ofgem).
- Karimi, Zhang & Li (2024)
- Zhou & Sun (2023)

**Confirmed real/clean:** Jain (1984), Hardin (1968), Fehr & Schmidt (1999, after fix).

**Not yet checked** (~14 references, confirmed NOT in NotebookLM's source files, so need direct web verification): Fehr & Gächter (2000), Fischbacher & Gächter (2010), Gersani et al. (2001) — *this one especially looks suspicious, an odd journal ("Evolutionary Ecology") for prosumer-sharing content* —, Moon et al. (2022), Le/Nguyen/Nguyen (2022), Li & Zhang (2022), Rathnayaka et al. (2014), Qiu/Wang/Strbac (2021), Moret & Pinson (2019/2020), Skoplaki & Palyvos (2009), Hernandez-Leal et al. (2017), Binz & Schulz (2023), Leng (2025).

**Not checked but very low risk** (canonical/famous works, essentially safe without spending search budget): Sutton & Barto (2018), Watkins & Dayan (1992), Tan (1993), Rashid et al. QMIX (2018), Lowe et al. MADDPG (2017), Oliehoek & Amato (2016), Ostrom (1990), Gini (1912).

**Student's instruction: full accuracy required, even if the final reference list shrinks to only 20-30 verified entries.** Any reference/claim that can't be verified should be removed or replaced, not left in place.

### 4. Thesis content updates already applied to `thesis_full.md`
- Table 4-9 replaced with real reproduced numbers (was: literature-estimated "†" values); old table demoted to context-only with caveat, Aloor row removed.
- New §4-10-1 "Baseline Reproduction Methodology" — table + prose explaining exactly what was implemented/adapted/hyperparameterized for each of the 4 baselines (this directly answers the professor's original question: "did you reimplement or copy from their papers?").
- New §4-11 with the 2×2 mechanistic isolation table and explanation.
- 4 new baseline validation figures added (learning curves / convergence checks).
- Abstract reframed: removed the false "improves comfort without reducing efficiency" claim, replaced with the accurate waste-reduction + distributional-dynamics framing.
- Kusatake sunny/cloudy saturation and Behrunani zero-waste-mechanism caveats added to prose.
- New battery-capacity sensitivity subsection in §3 (real data: F rises monotonically 3.5→9kWh but with sharply diminishing returns per added kWh after 5kWh; at 7kWh the mixed-vs-control comfort gap is ~zero, consistent with the §4-11 finding; at 9kWh the gap unexpectedly reappears — flagged as an open question, not explained away).
- p-value bug fixed (§4-7 scarcity table had a stale t/p-value for the 15% baseline row that didn't match the same data reported correctly in §4-3 — now consistent).
- λ=5 Behrunani sensitivity and May & Huang waste-augmented sensitivity — both run, both reported honestly (neither meaningfully changes the primary finding).
- Kusatake's weather-split numbers corrected (was 85%/0.614, now accurately 82.2%/0.607).
- Blackout-rate consistency fixed (14.4%→14.5% to match the authoritative `baseline_comparison.txt`).
- Removed a leaked raw-YAML text artifact that was showing up as literal visible text under the title.
- All 8 bibliography corrections listed above are applied in Ch6.

## What remains — prioritized

1. **Finish the bibliography audit** (in progress when this handoff was written). Specifically:
   - Resolve Alshehri & Gaunt — this is load-bearing for Ch3's parameter justification, needs a real replacement or reworded claim, not just removal.
   - Check/resolve Karimi et al. and Zhou & Sun — likely remove, find real replacements only if a claim depends on them.
   - Check the ~14 remaining references via web search (list above).
   - **Also audit in-text claims, not just bibliography entries** — the student explicitly wants every claim cited in the body text checked against what its source actually says, not just correct author names. This has not been systematically done yet except for the baseline papers (which were checked via NotebookLM's technical-spec extraction).
   - Once resolved, the reference list will likely shrink from ~53 to ~20-30 entries — this is expected and acceptable per the student.

2. **Chapter renaming** — rename the 5 main chapters to match the university's exact template titles: کلیات / مبانی نظری و پیشینه تحقیق / روش پیشنهادی / تجزیه و تحلیل نتایج / نتیجه‌گیری (currently: مقدمه و کلیات / مرور پیشینه‌ی پژوهش / روش‌شناسی پژوهش / تحلیل داده‌ها / بحث و نتیجه‌گیری). Not started.

3. **IEEE reference conversion** — convert the bibliography from APA style to numbered IEEE style, and correspondingly convert every in-text `(Author, Year)` citation throughout the document to `[N]` numbered form. Not started. **Do this after the bibliography audit is fully closed**, not before — don't convert citations that are about to be corrected or removed.

4. **Light readability pass** — remove genuine redundancy (there was a duplicate Jain's index definition concern raised earlier, checked and found to be a false alarm — Ch2 has the conceptual definition, Ch3 the formal equation, that's correct as-is, not duplication). No aggressive page-cutting needed given the relaxed page constraint.

5. **DOCX generation** — deliberately deferred to the very end, after all content is finalized. OpenCode has access to the real images and should generate via `pandoc thesis_full.md -o output.docx --reference-doc="template.docx"` (using the university's actual template file as the reference-doc so styles/margins/fonts inherit automatically) — this approach was validated to work structurally, just needs to be run where the real images resolve.

6. **English doc parity** (`ACADEMIC_v3_En.md`) — fully deferred, do this last, after the Persian version is 100% final. Don't sync incrementally, it'll just mean redoing it.

## Important process lessons from this session — please follow these

- **Never accept "done"/"fixed"/"verified" from OpenCode without direct evidence.** This happened at least 3 times: a claimed p-value fix that wasn't applied, a claimed process step that was silently skipped, and a claimed data delivery that never actually arrived in chat. Always ask for the actual pasted content/grep output, not a summary.
- **Don't let OpenCode or NotebookLM make content/framing decisions.** They execute and extract; you (the lead) decide what claims go in the thesis, what gets cut, what gets rewritten.
- **When an experiment produces a "negative" or unexpected result (a baseline fails, a claim doesn't hold up), the instinct should be to document it honestly as a finding, not to retune parameters until it looks better.** This happened repeatedly (Charbonnier's dead reward, the always-default control revealing the main results don't beat doing-nothing, Kusatake's saturation) and every time, the honest documented version made the thesis stronger and more defensible, not weaker.
- **Verify citations against the source's own first page, never against another document's citation of it** — this exact failure mode (pulling wrong data from the thesis's own prior draft instead of the real source) happened at least once with NotebookLM.
- The student has been a good-faith, engaged collaborator throughout and has explicitly prioritized correctness over speed or page count — lean into that, don't rush fixes without verification to "finish" faster.

## Attached
- `thesis_full.md` — current canonical thesis file, reflects everything in section 4 above. This supersedes any copy OpenCode or the student's local `Sections/*.md` may have — as of this handoff, **only this file is up to date**; the local build pipeline has not been resynced (flag this to OpenCode as the first thing to resolve if further edits need to go through it).
