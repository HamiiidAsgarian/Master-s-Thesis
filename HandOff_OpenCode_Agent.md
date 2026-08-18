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
| `0-Active Doc/Thesis_v9-5.md` | **THE LIVE THESIS.** The only document that matters. All other `.md` in that folder are history. **Never edit the older snapshots** (`thesis_v9-2 B.md`, `Thesis_v9-3.md`, etc.). |

Deep references (read these before making claims):
- `0-Active Doc/Important_considerations.md` — handoff guide for any agent: Farsi decimal pitfalls,
  ground-truth data sources, statistics conventions, fixed errors, retracted findings, open items.
- `0-Active Doc/Forensic_Data_Audit.md` — full forensic audit of every number in the thesis (87+ values verified).
- `results/Result_Help.md` — the authoritative **figure/data registry** (every PNG, which script made
  it, whether the thesis uses it). Read before deleting/moving/regenerating anything in `results/`.
- `Visual_Guide_north-star.md` — which figures are canonical vs. superseded.
- `Code_Output_data_visuals_Map.md` — script → output mapping.
- `0-Active Doc/Cloude_Converter_adapted.py` — the MD→DOCX converter (Persian RTL, BiDi, citations).

---

## 3. Repo layout (root = `/Users/hamidasgharian/Desktop/Thesis/sim`)

```
0-Active Doc/            Thesis + handoff/audit docs (ONLY live doc: Thesis_v9-5.md)
                         Cloude_Converter_adapted.py = MD→DOCX converter (Persian RTL, BiDi, citations)
                         postprocess_docx.py = post-processing for generated DOCX
                         Important_considerations.md = handoff guide
                         Forensic_Data_Audit.md = full number audit
                         check list.md = tracking/revision checklist
results/                 ALL outputs: figures/, qtable_heatmaps.png, baseline_*/ (each has results_plot.png, config.json, *_report.txt), analysis_support/qtab/*.npy, Result_Help.md
results/figures/         v01…v18 + v2_1 + fig_training_convergence.png + fig_training_early.png (canonical thesis figures)
generate_all_Visuals2.py  MAIN figure generator → all vNN figures + results/qtable_heatmaps.png
generate_training_curves.py  Training convergence figures (smoothed + early-training standalone)
convert_persian_digits.py    Latin→Persian digit converter for thesis text
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

## 4. Current status (as of 2026-08-22)

### Completed work

**All major thesis tasks are complete.** The thesis is in its final form.

#### Thesis text fixes (all 10 original issues resolved)
1. Tables 4-3/4-6 standardized to sample SD (ddof=1) with statistical justification in §3-13 and abstract.
2. Battery capacity corrected from 0.7→7.0 kWh across all 12 locations.
3. DOD (depth-of-discharge) explanation added — full 7.0 kWh usable.
4. Statistical justification paragraph inserted in Section 3-13.
5. PV stress-test justification added.
6. W=0.1→1.0 corrected (W=1.0 sunny, W=0.5 cloudy).
7. Table 3-1 footnote added.
8. فهرست اختصارات section inserted (20 rows: MARL through IEA).
9. Persian abstract statistical convention sentence added.
10. Figure 4-7 path verified (`../results/qtable_heatmaps.png`).

#### Number formatting (fully standardized)
- **998 slash-decimal patterns converted** (e.g., `۰/۸` → `۰٫۸`).
- **All tables use sample SD (ddof=1)** — standardized across thesis.
- **Persian decimal convention:** `٫` (U+066D) for Persian text, `.` for English.
- **All numbers in Persian body text use Persian-Indic digits** (۰–۹).
- **Persian digit conversion script:** `convert_persian_digits.py` — converts Latin digits in Persian text while protecting code, math, bibliography, citations, English author-year refs, abbreviations (P2P, A3C, n-1, etc.).

#### Figures (24 total in thesis)
- **19 v-figures** in `results/figures/`: v01–v16, v18, v2_1 (produced by `generate_all_Visuals2.py`)
- **1 heatmap**: `results/qtable_heatmaps.png` (English, thesis شکل ۴-۷)
- **4 baseline plots**: `results/baseline_{charbonnier_validation,kusatake_timing,behrunani_sanity,may_huang_sanity}/results_plot.png`
- **2 training convergence figures** (NEW):
  - `results/figures/fig_training_convergence.png` — main convergence (smoothed mean ± SD, y 0.80–1.0)
  - `results/figures/fig_training_early.png` — standalone early-training raw behavior (eps 0–1000, y 0.0–1.0)

#### Forensic data audit (complete)
- 87+ values verified against source CSVs/outputs.
- All statistical tests verified (16/19 computable, all PASS).
- Full audit documented in `0-Active Doc/Forensic_Data_Audit.md`.

#### Training convergence figures
- **Two separate figures** (not an inset):
  - Main convergence: smoothed bands (window=200), two-pass rendering (bands first, then lines), y 0.80–1.0
  - Early training: raw unsmoothed mean lines, episodes 0–1000, y 0.0–1.0
- Generated by `generate_training_curves.py` from `results/training_convergence_per_episode.csv`.

#### F metric definition (clarified)
- Table 4-10: F = comfort + Jain fairness (~1.8x range)
- Table 4-1 / فهرست جداول: "عدالت جین (F)" = Jain's fairness index only (~0.9x range)
- These are different metrics using the same letter in different contexts — this is correct.

### Key numbers to keep in sync
- BATTERY_CAP = 7.0 kWh (code and all thesis references)
- Blackout rate: ۳/۸ (8.3%) across Persian abstract ×2, RQ table, §4-9, Finding 4, English abstract
- H1 test: paired t-test (آزمون t زوجی), not independent
- p=0.14: 12.9%-waste claim; p=0.193: ONLY for 11.5% comparison (line 1235)
- Control waste: 8.82 kWh (1.77–2.19× other methods, NOT ">2× for all")
- Behrunani comfort 0.9171: second-lowest (May & Huang lowest at 0.9058)

---

## 5. Workflow — how to regenerate figures

**Regenerate ALL main figures (v01–v18, v2_1, + `results/qtable_heatmaps.png`):**
```
venv/bin/python generate_all_Visuals2.py
```

**Regenerate training convergence figures:**
```
venv/bin/python generate_training_curves.py
```
- Outputs: `results/figures/fig_training_convergence.png` + `fig_training_early.png`
- Reads from `results/training_convergence_per_episode.csv` (already exists, no re-simulation needed)

**Regenerate the 4 baseline thesis figures:**
```
venv/bin/python charbonnier_marginal_iql.py --validation   # results/baseline_charbonnier_validation/
venv/bin/python kusatake_evolutionary_moo.py --timing      # results/baseline_kusatake_timing/
venv/bin/python behrunani_gne_fairness.py --sanity         # results/baseline_behrunani_sanity/
venv/bin/python may_huang_ppo.py --sanity                  # results/baseline_may_huang_sanity/
```

**Convert Latin digits in thesis to Persian:**
```
venv/bin/python convert_persian_digits.py "0-Active Doc/Thesis_v9-5.md"
```
- Protects: code blocks, math, bibliography, citations, English author-year refs, abbreviations.

**SOTA comparison chart:**
```
venv/bin/python baseline_comparison.py
```

> **After regenerating anything**, verify with `git status` that only intended outputs changed.
> Do NOT hand-edit `results/figures/*.png` — always change the generator script and re-run.

---

## 6. Canonical figure style (thesis_plot_style.py)

- Central style module: `thesis_plot_style.py` exposes `apply_rc()`, palette `C`, `save_fig()`,
  `style_data_axes()`, `style_legend()`, `style_bars()`, `label_bars()`, `fa()` (Farsi reshape), `FA_FONTS`.
- **All** thesis-facing scripts import and use it.
- Rule: **never introduce a new plot style.** New figures must use these helpers.

---

## 7. The open question (ask the user before proceeding)

**Figure language.** The thesis body is Persian; figure captions are Persian. But **every figure is
English except `v09` (Persian) and `v17` (Persian heatmap, NOT in thesis)**.

- Thesis شکل ۴-۷ currently uses the **English** `results/qtable_heatmaps.png`.
- `results/figures/v17_qtable_heatmaps.png` is the **Persian** version of the exact same heatmap.
- Decision to make: (a) switch شکل ۴-۷ to `v17`, or (b) keep the English convention. **Do not decide unilaterally — ask the user.**

---

## 8. Major challenges & struggles (learned the hard way)

### Persian/Arabic text editing
- **ZWNJ (نیمفاصله, U+200C)** matters in Persian compounds. The Edit tool has failed on Persian strings; copy exact text or use Python-heredoc edits, then verify with `rg`.
- **Farsi decimal convention:** `٫` (U+066D) for Persian, `.` for English. Mixing them is a recurring error. The `convert_persian_digits.py` script handles this, but manual review is sometimes needed.
- **Unicode normalization:** invisible differences between characters (e.g., different Hamza forms) cause silent mismatches. Always verify edits with `repr()` or hex inspection.

### Statistical correctness
- **ddof=0 vs ddof=1:** Code uses `np.std(ddof=1)` (sample SD). Tables must match. This was a major fix — 998 patterns converted, tables re-standardized.
- **Paired vs independent t-tests:** Easy to mix up. H1 is paired (same houses, same seeds). H4 is independent (different scenarios). Getting this wrong invalidates p-values.
- **F-metric ambiguity:** F means different things in different tables (comfort+Jain vs Jain alone). Always check the column header.

### Data integrity
- **Never trust prose numbers.** Always verify against source CSVs (`results/*.csv`, `final_metrics.csv`).
- **Reproducibility:** Baseline `final_metrics.csv` files are byte-identical across runs; only runtime strings vary.
- **BATTERY_CAP was wrong** in thesis (0.7 vs 7.0 kWh in code). Found during audit. Fixed everywhere.

### Figure management
- **23+ figures** with complex naming conventions (v01–v18, v2_1, baseline plots, training curves).
- **Thesis references specific paths** — changing a figure name requires updating the thesis AND `Result_Help.md` AND `Code_Output_data_visuals_Map.md`.
- **Persian figure generation** uses `fa()` pipeline (`arabic_reshaper` + `bidi` + `Geeza Pro`/`DejaVu Sans`). Fragile; font availability varies.

---

## 9. Key considerations for future work

1. **The thesis is in its final form.** Unless the user requests changes, treat it as complete.
2. **Never fabricate or inflate numbers.** The forensic audit is complete — maintain integrity.
3. **When editing thesis text:** always check tables ↔ prose ↔ English abstract ↔ figures all agree on any changed number.
4. **Persian text edits:** use `convert_persian_digits.py` after manual edits to ensure digit consistency.
5. **New figures:** must use `thesis_plot_style.py` helpers. No hand-rolled styles.
6. **The `venv/` environment** is the only one with all deps (pymoo, arabic_reshaper, python-bidi). Use it for all scripts.

---

## 10. First steps for a new agent

1. Read this file, `0-Active Doc/Important_considerations.md`, `results/Result_Help.md`.
2. Check `git status` is clean.
3. Confirm `venv/` works: `venv/bin/python -c "import pymoo, arabic_reshaper"`.
4. **Ask the user what they want next** — do not assume.
