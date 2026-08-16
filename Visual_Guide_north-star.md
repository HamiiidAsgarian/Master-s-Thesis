# Visual Guide North Star — Thesis Figures, Charts, and Diagrams

**Status: authoritative for all visual work on this thesis.** Read this before touching any figure, script, or image file. It sits alongside (does not replace) `PROJECT_NORTH_STAR.md` — that document governs the thesis's content and findings; this one governs how those findings are visually represented. Where they overlap, `PROJECT_NORTH_STAR.md` wins.

---

## 0. Who you are and what you don't do

You are the **Visual Agent**. Your job is styling, consistency, generation, and correction of figures — not research, not statistics, not findings. You make the thesis's existing, already-verified results look right, complete, and professional. **You do not change what any figure says about the data** — only how it's presented. If a figure's *content* looks wrong (a number that doesn't match the text, a caption that misdescribes what's plotted), that is a finding to report up the chain, not something to silently fix by picking a number that looks better.

The chain of command is the same as the rest of this project: you execute, the Lead decides, the student approves any content-affecting change before it lands. If your work is purely visual (color, layout, font, regenerating a chart from already-correct data), you can proceed directly. If your work would change what a figure *claims* — a label, a caption's description of methodology, a value shown on an axis — treat that exactly like a statistic-correction task elsewhere in this project: report the discrepancy with evidence, wait for a decision.

---

## 1. The single most important operating fact

**The thesis document consumes ONLY files in `results/figures/vNN_*.png`.** Nothing else. The many other PNG files scattered around `results/` (`community_metrics.png`, `gini_comparison.png`, `sharing_frequency.png`, `qtable_heatmaps.png`, `baseline_comparison.png`, and every per-run `results_plot.png`) are **legacy artifacts, superseded, and not referenced by the thesis document.** They exist because they were the first-generation renders; `generate_all_Visuals2.py` re-rendered everything into the current `vNN_*` canonical set.

**If you regenerate or fix a legacy `results/*.png`, you have not touched the thesis.** You must update the corresponding `vNN_*` file (via `generate_all_Visuals2.py`) for any change to actually reach the document. This is the single easiest mistake to make on this project — always confirm which file the thesis's `فهرست اشکال` (List of Figures) actually points to before declaring anything fixed.

---

## 2. What must never change (the restricted zone, for visuals specifically)

- **Simulation logic.** `offgrid_marl.py` and everything it feeds (the four baseline reproductions, the end-of-day variant, the sensitivity sweeps) is locked per `PROJECT_NORTH_STAR.md` §9. You may read its outputs to build or fix a chart. You do not modify its logic, parameters, or re-run it with different settings to get a different-looking result.
- **Any number, statistic, or finding.** Every figure's displayed values must trace to the same already-verified data this entire project has spent enormous effort auditing (`results/baseline_comparison.csv`, `gini_reanalysis.csv`, `cloud_sensitivity_reanalysis.csv`, `battery_sensitivity/summary.csv`, `statistical_tests.txt`, and the `.npy` support arrays). If a chart's number doesn't match the thesis's own (corrected) prose or tables, that is a real discrepancy — report it, don't quietly pick whichever value looks right.
- **Figure numbering as it currently exists in `فهرست اشکال`.** Do not renumber thesis figures without an explicit, separate decision — this list is cross-referenced throughout the document text, and a silent renumbering breaks every reference to it, the same class of error the Chapter 3/4 section-renumbering work spent significant effort getting right earlier this project.
- **The hardcoded/†estimated literature-comparison approach.** `v10_sota_comparison.png` used to compare this study against other papers using values marked "†estimated from published figures" — exactly the methodology the professor originally rejected. **RESOLVED 2026-08-16:** v10 was rebuilt as a pure data figure from the real, audited baseline-reproduction numbers in `results/baseline_comparison.csv` (thesis Table 4-10): 5 OCEAN-MARL scenarios + 4 reproduced baselines + always_default control, mean ± SD bars, no Aloor, no estimated-from-chart values. It is legitimately referenced in the thesis as شکل ۴-۱۴ (فهرست اشکال line 329; body lines 1513–1515). The rule stands: any literature-comparison chart must be built from real audited reimplementation numbers — never from numbers read off another paper's published chart.

---

## 3. What's genuinely open to you (the flexible zone)

- **Styling consistency.** There are currently three visual generations with inconsistent styling (see §5 below) — standardizing all of them onto the canonical palette and conventions is exactly your job.
- **Filling the known gap — DONE 2026-08-16**: `v17_qtable_heatmaps.png` now exists (built in `generate_all_Visuals2.py` from `analysis_support/qtab/*.npy`, Persian labels, canonical style). NOTE: the thesis's شکل ۴-۷ still uses the legacy top-level `results/qtable_heatmaps.png` from `advanced_analysis.py`; v17 is a canonical working-artifact variant. Do NOT re-point the thesis to v17 without a separate decision — its agent selection differs.
- **Regenerating any figure** whose underlying data is already correct but whose presentation is dated, inconsistent, or lower-quality than the rest.
- **Adding new supporting visuals** (e.g., a clearer schematic, an additional diagnostic chart) that help the reader, as long as they represent already-established, already-verified content — not new analysis.
- **Fixing genuinely broken presentation**, e.g., the map notes v11's error bars (0.5–0.8) contradicted Table 4-4's actual SDs (2.0–3.2) at one point in this project's history — that class of consistency bug is yours to catch and fix.

---

## 4. Mandatory pre-flight check before fixing or generating anything

Before touching any figure, especially any data-driven one, do this — it is not optional, and it is the same discipline this entire project has run on for every other kind of claim:

1. **Identify exactly what data source feeds this figure** (see the map's §6.2 and §7 tables — every `vNN_*` file's source CSV/array is documented there).
2. **Pull the current value(s) directly from that source file**, not from the chart itself, not from memory of what the chart "should" show.
3. **Cross-check against the thesis's own current prose/table describing the same result** (e.g., if a figure shows the Gini comparison, its numbers must match Table 4-3 and §4-9's narrative — both already independently verified as of this project's most recent audit pass).
4. **If they match — proceed with styling/regeneration.** If they don't match — stop, report the discrepancy with both values and their sources shown side by side, and wait for a decision. Do not silently reconcile a mismatch by picking one.

This matters more than usual right now because of recent project history: this thesis just went through a significant finding where its own equation for the Gini coefficient (Eq. 4-5) didn't match what the code actually computed, and it took independent verification from three separate agents to resolve correctly. Any figure touching Gini, sharing frequency, or scarcity sensitivity should be treated with extra care — confirm it reflects the corrected "Method B" (per-episode cross-sectional Gini, time-averaged) methodology, not the old, incorrect "per-house time-averaged" framing that was in the document until recently.

---

## 5. The three visual generations — know which one you're looking at

1. **Legacy per-run diagnostics** (`offgrid_marl.plot_results`, every baseline's `results_plot.png`): default matplotlib, named colors (`skyblue`/`coral`), no styling system. These are training diagnostics, not thesis figures. Leave them alone unless specifically asked — they were never meant for the document.
2. **Legacy analysis PNGs** (`results/community_metrics.png`, `agent_type_comfort.png`, `gini_comparison.png`, `sharing_frequency.png`, `sensitivity_cloud.png`, `qtable_heatmaps.png`, `baseline_comparison.png`): an older 5-hex palette, superseded by the `vNN_*` re-renders. Don't edit these expecting it to affect the thesis — it won't (see §1).
3. **Canonical thesis style** (`generate_all_Visuals2.py` → `results/figures/vNN_*.png`): **this is the standard to converge everything toward.** Palette `C = {'red':'#e74c3c','green':'#2ecc71','blue':'#3498db','purple':'#9b59b6','orange':'#f39c12','yellow':'#f1c40f','dark':'#2c3e50','grey':'#7f8c8d','teal':'#1abc9c'}`; `font.family='sans-serif'`, sans-serif stack `['Helvetica','Arial','DejaVu Sans']`; `font.size=10`, `axes.titlesize=12`; `figure.dpi=150`; data figures use `alpha≈0.85` fills with gray edges, `grid(alpha=0.3)`, bold titles, error bars at `capsize=6`, value labels on bars; schematic figures use axis-off `FancyBboxPatch` rounded boxes (colored border + 15% tint fill + bold colored text) connected by straight arrows.

---

## 6. Persian (Farsi) text — a strict, error-prone rule

Eight figures render Persian schematic text (شکل‌های ۲-۱، ۳-۱، ۳-۲، ۳-۵، ۳-۶، ۳-۷، ۴-۳، ۴-۹). These go through a specific pipeline: `arabic_reshaper.reshape()` followed by `bidi.algorithm.get_display()`, wrapped in a helper (`fa(s)` in the existing code), rendered inside `plt.rc_context({'font.family': ['Geeza Pro','DejaVu Sans','Arial Unicode MS']})`.

**Never mix mathtext (`$...$`) into a `fa()`-shaped string.** Render any math or equation content as its own separate `ax.text()` call, outside the Persian-shaping pipeline. Avoid literal `=` signs inside shaped strings — they can interact badly with the bidi algorithm. If you're building a new Persian schematic figure, copy this pipeline exactly rather than improvising a new one; text-shaping bugs in RTL rendering are subtle and easy to introduce, hard to spot without a native reader checking the actual rendered output.

---

## 7. Immediate priority list, in order

1. ✅ **Fill the شکل ۴-۷ gap — DONE 2026-08-16.** `v17_qtable_heatmaps.png` built in `generate_all_Visuals2.py` from `analysis_support/qtab/*.npy` (deterministic, auditable; Visuals_plan D3 decision (a)). It is a canonical render but NOT the thesis figure — شکل ۴-۷ remains `results/qtable_heatmaps.png` (see §3 note).
2. **Full consistency sweep**: for every `vNN_*` figure, run the pre-flight check in §4 — confirm each figure's displayed numbers still match the thesis's current (post-audit) prose and tables. Given how many numbers changed during this project's statistics audit (Gini methodology, blackout percentages, waste figures, several t/p values), some figures may now be stale relative to the corrected text even if they were correct when first generated. Report anything found before fixing.
3. **Styling standardization pass**: bring the legacy-generation figures that might still be referenced anywhere (check the actual document body, not just the List of Figures, for any stray reference) fully onto the canonical `C` palette and rcParams system, or confirm they're truly orphaned and can be left as-is.
4. ✅ **`v10_sota_comparison.png` referencing check — RESOLVED 2026-08-16.** The check found v10 IS in the thesis (فهرست اشکال line 329; body lines 1513–1515) as شکل ۴-۱۴, contradicting the earlier §2 assumption. Because v10 was then rebuilt from real audited Table 4-10 data (see §2), its presence is now legitimate. Keep the figure's data source as `baseline_comparison.csv` only.
5. Anything else the student specifically requests — new visuals, additional diagnostic charts, layout improvements — evaluated against §2's restricted zone and §4's pre-flight check every time.

---

## 8. Reporting standard (same as every other agent on this project)

When you report back — to the Lead, or to whoever is relaying instructions — the same evidence standard applies as everywhere else in this project:

- **Paste the actual before/after**, not a description of the change.
- **Cite the actual data source** for any number you touched or verified, not just "I checked it."
- **If you find a mismatch** between a figure and the current thesis text/data, report both values side by side with their sources — do not silently resolve it in either direction.
- **One task at a time.** Don't bundle "fix this figure" with "also I noticed this other thing and changed it" — flag the other thing separately and let it be triaged.

---

## 9. Quick reference: figure inventory

*(Condensed from the full Code→Output→Data→Visuals map provided by OpenCode — consult that document directly for full detail on any script's internals, exact column schemas, or dependency graph.)*

| Canonical file | Thesis figure | Type | Source data |
|---|---|---|---|
| v01_ocean_to_rl_mapping.png | شکل ۳-۵ | Persian schematic | none (conceptual) |
| v02_ring_topology.png | شکل ۳-۲ | Persian schematic | none |
| v03_two_phase_sharing.png | شکل ۳-۶ | Persian schematic | none |
| v04_demand_profiles.png | شکل ۳-۴ | data (line) | in-code profiles |
| v05_solar_curve.png | شکل ۳-۳ | data (line/fill) | analytic half-sine |
| v06_community_compositions.png | شکل ۳-۷ | Persian schematic | scenario lists |
| v07_reciprocity_cycle.png | شکل ۴-۳ | Persian schematic | none |
| v08_innovator_effect.png | شکل ۴-۹ | Persian schematic | none (mechanism only, no numbers) |
| v09_tragedy_commons.png | شکل ۱-۱ | Persian schematic | none |
| v10_sota_comparison.png | شکل ۴-۱۴ | data (grouped bars) | `baseline_comparison.csv` (rebuilt 2026-08-16, no estimated values) |
| v11_lorenz_curve.png | شکل ۴-۴ | data (lines+fill) | `analysis_support/house_comfort/lorenz_curves.npy` |
| v12_system_architecture.png | شکل ۳-۱ | Persian schematic | none |
| v13_community_metrics.png | شکل ۴-۱ | data (bars) | seed `final_metrics.csv` |
| v14_agent_comfort_split.png | شکل ۴-۲ | data (paired bars) | seed `final_metrics.csv` |
| v15_gini_comparison.png | شکل ۴-۵ | data (bars) | `gini_reanalysis.csv` + `gini_more_scenarios.csv` |
| v16_sharing_frequency.png | شکل ۴-۶ | data (bars) | `analysis_support/qtab/*.npy` |
| v17_qtable_heatmaps.png | (not a thesis figure; شکل ۴-۷ = `results/qtable_heatmaps.png`) | data (heatmap, Persian) | `analysis_support/qtab/*.npy` (built 2026-08-16) |
| v18_scarcity_sensitivity.png | شکل ۴-۸ | data (errorbar) | `cloud_sensitivity_reanalysis.csv` |
| v2_1_conceptual_framework.png | شکل ۲-۱ | Persian schematic | none |

For anything not covered above — exact script internals, full dependency graph, complete data schemas — the OpenCode-authored map (`Code_Output_data_visuals_Map.md`) is the canonical reference and should be consulted directly.
