# HandOff — OpenCode Agent

> Quick-start briefing for any new OpenCode agent (or a restarted session) working in this repo.
> Read this top-to-bottom before touching anything. It is the onboarding doc; the files it links
> are the deep references.

---

## 1. What this project is

A **Persian M.Sc. thesis** project on **OCEAN-personality Multi-Agent Reinforcement Learning (MARL)
for energy sharing in a smart neighborhood micro-grid**.

- 10 houses (agents) on a ring topology share surplus solar energy.
- Each agent has a fixed personality (selfish / individualist / prosocial / altruistic / innovator)
  mapped to Q-learning parameters.
- Reward = `w_self * own_comfort + w_fair * Jain's Fairness Index`.
- Studies emergent fairness/efficiency trade-offs, plus reproductions of **4 literature baselines**
  (Charbonnier marginal-IQL, Kusatake NSGA-II, Behrunani GNE, May & Huang PPO), an always-default
  control, and a battery-sensitivity scan.

**The deliverable is the thesis document**, not the code. Code exists to produce defensible,
reproducible results and figures for the thesis.

---

## 2. The single most important file

| File | Role |
|---|---|
| `0-Active Doc/Thesis_v9-3.md` | **THE LIVE THESIS.** The only document that matters. All other `.md` in that folder are history. **Never edit the older snapshots** (`thesis_v9-2 B.md`, etc.). |

Deep references (read these before making claims):
- `0-Active Doc/Important_considerations.md` — handoff guide for any agent: Farsi decimal pitfalls,
  ground-truth data sources, statistics conventions, fixed errors, retracted findings, open items.
- `0-Active Doc/AUDIT_REPORT_v9-2.md` — research-integrity audit.
- `0-Active Doc/AUDIT_PROGRESS.md` — progress checkpoint.
- `results/Result_Help.md` — the authoritative **figure/data registry** (every PNG, which script made
  it, whether the thesis uses it). Read before deleting/moving/regenerating anything in `results/`.
- `Visual_Guide_north-star.md` — which figures are canonical vs. superseded.
- `Code_Output_data_visuals_Map.md` — script → output mapping.

---

## 3. Repo layout (root = `/Users/hamidasgharian/Desktop/Thesis/sim`)

```
0-Active Doc/            Thesis + handoff/audit docs (ONLY live doc: Thesis_v9-3.md)
results/                 ALL outputs: figures/, qtable_heatmaps.png, baseline_*/ (each has results_plot.png, config.json, *_report.txt), analysis_support/qtab/*.npy, Result_Help.md
results/figures/         v01…v18 + v2_1  (canonical thesis figures, see §6)
generate_all_Visuals2.py  MAIN figure generator → all vNN figures + results/qtable_heatmaps.png
advanced_analysis.py      backward-compat: regenerates results/qtable_heatmaps.png from .npy
thesis_plot_style.py      THE canonical style module (palette C, style_* helpers, apply_rc, save_fig, fa())
offgrid_marl.py           main OCEAN-MARL experiment (also used by ocean_marl_endofday.py)
charbonnier_marginal_iql.py / may_huang_ppo.py / kusatake_evolutionary_moo.py / behrunani_gne_fairness.py
                          the 4 baseline reproductions
baseline_comparison.py    SOTA comparison chart → results/baseline_comparison.{png,csv,txt}
agent.py, environment.py, simulation.py   core sim
battery_sensitivity.py, gini_*.py, support_analysis.py, analyze_results.py, final_analysis.py
                          analysis/legacy helpers (many outputs superseded by v-figures)
requirements.txt          base deps
venv/                     THE Python env used for everything (see §5)
Traceability_Package.zip, Traceability_Package_From_Results/   packaging artifacts
```

---

## 4. Current status (as of 2026-08-16)

- **All work committed.** `git status` is clean. Latest commits: `249d0a7 new style`,
  `4042ddc Visuals`, `1f5897d Two method fixes`.
- **All 23 thesis figures exist and are freshly regenerated in one canonical style** (0 missing):
  - 18 in `results/figures/`: v01…v16, v18, v2_1
  - 1 heatmap: `results/qtable_heatmaps.png` (English, thesis شکل ۴-۷)
  - 4 baseline plots: `results/baseline_{charbonnier_validation,kusatake_timing,behrunani_sanity,may_huang_sanity}/results_plot.png`
- **Regeneration is deterministic** for all figure pipelines: baseline `final_metrics.csv` files are
  byte-identical across runs; only runtime-timing strings vary (e.g. `2.2s → 2.1s`).
- **Environment used for all scripts:** `venv/` (python 3.10; has `pymoo 0.6.2`,
  `matplotlib 3.7.1`, `arabic_reshaper`, `python-bidi`). It is the only env with the Farsi-text deps.
  Install commands (already done, for reference):
  `venv/bin/pip install pymoo arabic-reshaper python-bidi`

---

## 5. Workflow — how to regenerate figures

**Regenerate ALL main figures (v01–v18, v2_1, + `results/qtable_heatmaps.png`):**
```
venv/bin/python generate_all_Visuals2.py
```
- Writes both heatmaps: `results/figures/v17_qtable_heatmaps.png` (Persian variant — see §7) and
  `results/qtable_heatmaps.png` (English, thesis ۴-۷) from the same `.npy` data.
- `advanced_analysis.py` also writes `results/qtable_heatmaps.png` (backward-compat). Either is fine;
  running `generate_all_Visuals2.py` covers it.

**Regenerate the 4 baseline thesis figures** (each saves to
`results/baseline_<dir>/results_plot.png` + `config.json` + `*_report.txt` + `final_metrics.csv`):
```
venv/bin/python charbonnier_marginal_iql.py --validation   # results/baseline_charbonnier_validation/
venv/bin/python kusatake_evolutionary_moo.py --timing      # results/baseline_kusatake_timing/
venv/bin/python behrunani_gne_fairness.py --sanity         # results/baseline_behrunani_sanity/
venv/bin/python may_huang_ppo.py --sanity                  # results/baseline_may_huang_sanity/
```

**SOTA comparison chart:**
```
venv/bin/python baseline_comparison.py   # → results/baseline_comparison.png (superseded by v10) + .csv/.txt (KEEP: the .csv/.txt are the SOTA data the thesis cites)
```

> **After regenerating anything**, verify with `git status` that only intended outputs changed.
> Do NOT hand-edit `results/figures/*.png` — always change the generator script and re-run.

---

## 6. Canonical figure style (thesis_plot_style.py)

- Central style module: `thesis_plot_style.py` exposes `apply_rc()`, palette `C`, `save_fig()`,
  `style_data_axes()`, `style_legend()`, `style_bars()`, `label_bars()`, `fa()` (Farsi reshape), `FA_FONTS`.
- **All** thesis-facing scripts import and use it (`generate_all_Visuals2.py`, `advanced_analysis.py`,
  `offgrid_marl.py`, `baseline_comparison.py`, the 4 baseline scripts).
- Rule: **never introduce a new plot style.** New figures must use these helpers. Any script that
  hand-rolls colors/axes/legends is out of convention.

---

## 7. The open question (ask the user before proceeding)

**Figure language.** The thesis body is Persian; figure captions are Persian. But **every figure is
English except `v09` (Persian) and `v17` (Persian heatmap, NOT in thesis)**.

- Thesis شکل ۴-۷ currently uses the **English** `results/qtable_heatmaps.png`.
- `results/figures/v17_qtable_heatmaps.png` is the **Persian** version of the exact same heatmap
  (same data, same function, `persian=True/False` at `generate_all_Visuals2.py:800-801`). It was
  documented as "NOT a thesis figure" (`Important_considerations.md:186-188`) but that was a choice,
  not a requirement — for a Persian thesis, v17 is arguably more consistent.
- Decision to make: (a) switch شکل ۴-۷ to `v17` (1-line path change at `Thesis_v9-3.md:1336`), or
  (b) keep the English convention. And optionally (c) whether to make **all** figures Persian or
  keep all English, so `v09` doesn't stick out. **Do not decide unilaterally — ask the user.**

---

## 8. Farsi / editing pitfalls (these have caused real failures)

- **Farsi decimal convention:** Persian numerals + non-breaking decimal point. `0.8` renders as
  `۰/۸`. A recurring real error in this thesis — see `Important_considerations.md` §1.
- **ZWNJ (نیمفاصله, U+200C)** matters in Persian compounds (میآید ≠ میآید). The Edit tool has
  failed on Persian strings; copy exact text or use a Python-heredoc edit, then verify with `rg`.
- **Every figure needs a visible caption line** `شکل (X-Y): …`; markdown alt-text is invisible.
  Captions in «فهرست اشکال» must match the in-body captions exactly.
- **Figure numbering = order of appearance** per chapter. 23 figures, numbered ۱-۱ … ۴-۱۴.
- **If you need to check a figure's content**, this model cannot read images — verify via the
  generator script (titles/labels/`fa()` calls) instead of opening the PNG.

---

## 9. Numbers you must not break (keep tables ↔ prose ↔ figures ↔ abstracts in sync)

- Blackout rate harmonized at **۳/۸ (8.3%)** across Persian abstract ×2, RQ table, §4-9, Finding 4,
  and English abstract. Do NOT re-introduce the old 0.8 discrepancy.
- H1 test is **paired** t-test (آزمون t زوجی), not independent — line 1580 in thesis.
- p=0.14 is the 12.9%-waste claim; p=0.193 belongs ONLY to the 11.5% comparison (line 1235).
- Control waste 8.82 is 1.77–2.19× other methods — NOT ">2× for all".
- Behrunani comfort 0.9171 is the second-lowest (May & Huang lowest, 0.9058) — not "the lowest".
- **Never fabricate or inflate.** Reproductions report real controlled re-run results
  (Table 4-10), not the papers' published numbers.

---

## 10. If you are asked to change thesis claims/numbers

1. Find the ground-truth number in data files first (`results/*.csv`, `analysis_support/`,
   baseline `final_metrics.csv`, `statistical_tests.txt`), never in prose.
2. Know whether the comparison is paired or independent (see `Important_considerations.md` §3).
3. Check the claim is not an overstatement (`>`, `lowest`, `only`, `every`, `no study`).
4. Verify **tables ↔ prose ↔ English abstract ↔ figures** all agree on that number.
5. `rg`-verify no stale duplicate survives the edit.

---

## 11. First steps for a new agent

1. Read this file, `0-Active Doc/Important_considerations.md`, `results/Result_Help.md`.
2. Check `git status` is clean and the 23 thesis figure paths still exist (script in §4 of
   `Result_Help.md` lists them).
3. Confirm `venv/` works: `venv/bin/python -c "import pymoo, arabic_reshaper"`.
4. **Ask the user what they want next** — do not assume. The open items are: the figure-language
   decision (§7) and any thesis edits the user requests.
