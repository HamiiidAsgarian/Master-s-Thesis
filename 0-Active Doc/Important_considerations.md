# Important Considerations — Handoff Guide for Any Future Agent

**Scope:** Persian M.Sc. thesis project on OCEAN-personality MARL energy sharing in smart neighborhoods.
**Repo root:** `/Users/hamidasgharian/Desktop/Thesis/sim`
**Active thesis file:** `0-Active Doc/Thesis_v9-3.md` (this is the ONLY live document — `thesis_v9-2 B.md` and older snapshots are historical).
**Read first (authoritative):** `0-Active Doc/AUDIT_REPORT_v9-2.md` (research-integrity audit), `0-Active Doc/AUDIT_PROGRESS.md` (progress checkpoint), `results/Result_Help.md` (figure/data registry).
**Last updated:** 2026-08-16 (figures regenerated in `generate_all_Visuals2.py`; new **شکل ۲-۱** conceptual-framework figure added to §2-5-1 and فهرست اشکال as `results/figures/v2_1_conceptual_framework.png`).

This file exists so any agent (new or resumed, with or without history) can work without
re-discovering the same pitfalls, mis-reading the same conventions, or re-introducing errors
that were already fixed. Read it before editing the thesis, writing new claims, regenerating
figures, or running statistical comparisons.

---

## 1. THE #1 PITFALL: The Farsi decimal convention (memorize this)

The thesis uses a **non-standard decimal notation**: numbers are written as
`[fractional digits]/[integer part]`, which reads as **`integer.fraction`**.

| Written | Means | NOT |
|---|---|---|
| `۰/۸` | **8.0** | 0.8 ❌ |
| `۳/۸` | **8.3** | 3.8 ❌ |
| `۹/۱۲` | **12.9** | 9.12 ❌ |
| `۰/۲` | **2.0** | 0.2 ❌ |
| `۰/۷` | **7.0** (LG Chem battery total) | 0.7 ❌ |
| `۵/۳` | **3.5** (half of 7.0 kWh) | 5.3 ❌ |
| `۴/۷` | **7.4** (Ofgem 2700/365 kWh/day) | 4.7 ❌ |
| `۳/۱` | **1.3** (PV peak kWp) | 3.1 ❌ |
| `۰/۱` | **1.0** (Behrunani λ baseline) | 0.1 ❌ |
| `۷/۱%-` | **1.7%** (Table 4-8 Jain change) | 7.1 ❌ |

**Ground-truth confirmations** (external specs): LG Chem RESU7H total 7.0 kWh / usable 6.6 kWh;
50% charge = 3.5 kWh; Ofgem 2,700 kWh/yr = 7.4 kWh/day; MCS 3–4×400 W panels = 1.3 kWp.

**Consequences of getting this wrong:** An entire audit batch (C2, C7, C8, C9) was *retracted*
because a reviewer mis-read leading-zero fractions (`۰/۸` as 0.8 instead of 8.0). Do NOT re-flag
correct numbers as "errors". Do NOT "fix" `۰/۸` → `۸/۰` thinking it's reversed — the convention
is already consistent document-wide.

**Always cross-check:** any numeric claim you touch against `results/baseline_comparison.txt`
or the underlying CSV/`config.json` in **decimal form**, then convert to the thesis notation
only as a final formatting step.

---

## 2. Where the ground-truth data lives (never trust prose; trust these)

All thesis numbers must be reproducible from saved artifacts. Read the raw files, not the text.

| Claim / table | Source of truth |
|---|---|
| Table 4-1, 4-10 (all 10 SOTA rows: comfort/Jain/F/blackout/waste) | `results/baseline_comparison.txt` (5-seed means ± SD) |
| Statistical tests (t, ANOVA, p, CI, Cohen's d) | `results/statistical_tests.txt` |
| Prosocial/selfish per-agent comfort, Q-tables, sharing freq | `results/analysis_support/report.md`, `results/analysis_support/qtab/*.npy` |
| Cloud sensitivity 15/25/35% | `results/cloud_sensitivity_reanalysis.csv` |
| Gini analyses | `results/gini_reanalysis.csv`, `results/gini_more_scenarios.csv` |
| Battery capacity sweep (Table 3-1) | `results/battery_sensitivity/summary.csv` |
| Baseline reproductions (per-seed) | `results/baseline_{charbonnier,kusatake,behrunani,may_huang}/seed_*/final_metrics.csv` |
| Kusatake sunny/cloudy day split | `results/baseline_kusatake/seed_42/weather_split_metrics.csv` (NOT the timing_report.txt — that is a 10-day sanity check only) |
| Behrunani λ sensitivity / May–Huang waste penalty | `results/baseline_behrunani_lambda5_sensitivity/`, `results/baseline_may_huang_waste_sensitivity/` (recomputed from `final_metrics.csv`) |
| 2×2 isolation (Table 4-12) | `results/baseline_comparison.txt` "ISOLATION 2×2" block |
| Main scenario seeds | `results/{all_prosocial,all_selfish,mixed,innovator_effect,varied_altruism,control_always_default}/seed_*/` |

**Per-seed runtime plots (~67)** are working artifacts, not thesis material. Every
`*.csv`, `*.txt`, `*.npy`, `config.json` is data evidence — **never delete**.

---

## 3. Statistical test conventions (paired vs independent — a real error source)

- **Seed-matched comparisons = PAIRED (`آزمون t زوجی`).** Any comparison between scenarios that
  used the same 5 seeds (same weather sequences) is paired: mixed vs all-selfish waste (t=−1.87,
  p=0.135), gini mixed→innovator (paired t(4)=−2.84, p=0.047), cloud-sensitivity tests, etc.
- **Independent (`آزمون t مستقل`) is used only for between-group comparisons** with different
  units: all-prosocial vs all-selfish comfort (t=0.845, p=0.4229), innovator vs mixed comfort
  (t(8)=−3.562), sharing-freq prosocial-in-mixed vs all-selfish baseline (t(8)=0.684).
- **THE p-values that go with each:** 12.9% waste reduction (mixed vs all-selfish) → **p=0.14**
  (paired). 11.5% waste reduction (all-prosocial vs all-selfish) → **p=0.193** (independent).
  Do not attach 0.193 to the 12.9% claim (this exact misattachment was a real audit finding, C4).
- ANOVA: comfort F(4,20)=3.362 p=0.0293; excl. innovator F(3,16)=0.6745 p=0.5802. Jain
  F(4,20)=2.71 p=0.060; excl. innovator F(3,16)=0.54 p=0.663. 10-group SOTA F=11.706 p<0.001.

---

## 4. Real errors already fixed — do NOT re-introduce (from AUDIT_REPORT_v9-2 §C)

| # | Fix applied (in thesis_v9-2) |
|---|---|
| C1 | Blackout prose harmonized `۰/۸`→`۳/۸` (8.3%) in abstract×2, RQ table (1144), §4-9 (1420), Finding 4 (1558). Now consistent with Table 4-8 and English abstract. |
| C3 | H1 test label: `آزمون t مستقل` → `آزمون t زوجی` (line 1580). |
| C4 | Line 1672 validity-threats paragraph: p=0.193 → **p=0.14** (12.9% claim). Keep p=0.193 ONLY on the 11.5% comparison at line 1235. |
| C5 | Line 1486: removed "بیش از دو برابر هر روش یادگیریمحور" → "بیشتر از هر روش (از ۸/۱ تا ۲/۲ برابر)". Control waste 8.82 is 1.77–2.19× different methods — NOT >2× for all. |
| C6 | Line 1490: Behrunani comfort 0.9171 is NOT lowest of the four reproductions → now "نسبتاً پایین، دومین پایینترین پس از می و هوانگ با ۹۰۵۸/۰". |
| C10 | Table 4-12: now **two-column F** — F column = training-F for all cells (A=1.8453, B=1.8361, C=1.8714, D/D2=1.8359); added "F (حریصانه)" column (A=— not computed, B=1.8850, C=1.9057, D=1.8850). The improvement column (+0.0000/+0.0207/+0.0000) is now directly derivable as greedy-F − control greedy-F (1.8850). Intro sentence explains the two eval regimes and why A has no greedy-F (reference scenario, reported in Table 4-10). |

Earlier batch (in thesis_v8, carried forward): cloud p-values 25% sig p=0.0025 / 35% ns
p=0.0703; top-decile formula S≈G+0.1; seed 42 (not 456) is the outlier; CI-overlap restatement;
fairness drop 1.6→1.8%; horizon 1000-day eval window; waste-base 14.8%; H1–H4 verdicts added;
ch3 table renumbering; abstract waste percentages (≈50% vs no-share, 12.9% p=0.14).

---

## 5. Retracted findings — do NOT re-flag these as errors

These were **verified as CORRECT** after the decimal-convention challenge. If you re-check them,
confirm against the raw data and do not "correct" them:

- C2 (orig.): innovator comfort reduction **2.0%** is correct everywhere (`۰/۲` = 2.0).
- C7 (orig.): sharing frequency "۱۲–۱۴٪ از وضعیتها" is reproducible from `qtab/*.npy`
  (`(greedy>=1).mean()`: mixed prosocial 13.92±2.00, mixed selfish 13.08±2.77, all-selfish 13.04).
- C8 (orig.): Kusatake 411/500 sunny days (82.2%), 89 cloudy (17.8%), cloudy comfort 0.607 vs
  0.500 no-share (+21.4%) — all confirmed in `weather_split_metrics.csv`.
- C9 (orig.): Behrunani λ = `۰/۱` = 1.0 (baseline), NOT a typo.
- The earlier "54.5%" sharing figure was an **audit recomputation error**, never in the thesis.

---

## 6. Open / unfinished items (known risk areas — resolve before submission)

1. **Zhang et al. (2025)** — heaviest Ch3 citation load; 2 of 5 claims (ε-decay=0.999,
   optimistic init Q=1.0) were NEVER confirmed against the source. Verify or soften.
2. **Behrunani "Swiss historical irradiation data"** (Ch4 table) — confirm or flag.
3. **Kusatake "21% Markov-chain cloud probability"** (Ch4 table) — confirm or flag.
4. **Fig 4-4 error bars (0.5–0.8)** look inconsistent with Table 4-4 SDs (2.0–3.2) — figure-vs-table check.
5. **Table 4-8 Jain 1.7% vs §4-2 1.8%** — one-directional rounding inconsistency (computed 1.79%).
6. **Table 4-2 sample SD vs Table 4-6 population SD** for same 5-seed data — pick one convention.
7. **§5-1-1 Finding 5 sharing windows** (8am–6pm altruistic vs 10am–4pm prosocial) — not checkable from artifacts.
8. **Lines 1560 `۱۲–۱۴٪` vs 1566 `۱۸/۲٪`** are TWO DIFFERENT sharing metrics (states vs time-steps) — never conflate in text.
9. **Chapter 5 prose** never received the same sentence-level scrutiny as Ch2–4.
10. ✅ **RESOLVED 2026-08-16** — `v10_sota_comparison.png` was stale (plotted Aloor et al. 2024,
    which the thesis removed from the quantitative comparison). Regenerated from real
    `results/baseline_comparison.csv` data (5 OCEAN-MARL scenarios + 4 reproduced baselines +
    control); all 10 rows verified against Table 4-10. See Result_Help §E.
11. **Full cross-consistency sweep** of tables 2-1, 3-2, 3-4, 4-9, 4-10, 4-11 after many edits — never re-run.
12. **Orphaned residue check** — captions/footnotes/cross-refs still pointing at removed content (fabricated papers) were never grepped exhaustively.
13. **References list** is APA-style bullets; template requires numbered IEEE-style list (deferred phase).

---

## 7. Academic integrity (non-negotiable)

- **NEVER fabricate or hallucinate references.** History: 8 fabricated papers (Zhou & Sun,
  Gersani, Moon, Le/Nguyen/Nguyen, Li & Zhang, Moret/Tacher/Pinson, Qiu/Wang/Strbac, Leng) were
  purged. Any new citation must be real, correctly attributed (authors/year/venue/title), and its
  specific claims verified against an actual source.
- Do not invent numbers, mechanisms, or attributions for a paper. If a claim cannot be verified,
  **soften it or mark it open** (see §6 items 1–3).
- Every numeric claim in the thesis must trace to a saved artifact (§2). If data was never
  persisted (e.g., per-seed sharing rates), say so honestly rather than back-filling.
- The "did you reimplement or copy?" question (§4-10-1, §4-11) is the professor's core mandate —
  re-run this check whenever Ch4 content changes.

---

## 8. Big-picture / methodology reminders (don't lose the forest)

- **Four headline findings** (all verified): (1) prosocial comfort advantage 2.9pp p=0.0011;
  (2) scarcity persistence 2.58–3.05pp across 15 seed–cloud combos; (3) fairness–efficiency
  NON-zero-sum (Jain improved, waste directionally lower); (4) innovator destabilization
  (gini +22%, t(8)=−3.562, d=2.25). Corrections are localized text/mechanical errors — none
  overturn these. Keep fixes proportional: don't over-edit correct content.
- **Contributions are honest-negative:** no absolute community-comfort win over no-sharing
  control (all ns); the contribution is (a) directional waste reduction (12.9%, ns), (b)
  distributive dynamics (prosocial advantage, innovator effect). Do not let any edit turn this
  into an over-claimed result.
- **Environment constraints are structural:** 10 houses, PV 1.3 kW, battery 7.0 kWh, Bernoulli
  cloud 15%; solar-only noon surplus window; agents share in only 12–14% of states. Claims must
  respect these limits (e.g., the ">2×" and "lowest comfort" errors came from over-generalizing).
- **Two metrics must never be conflated:** sharing frequency as % of states vs % of time-steps;
  also sample-SD vs population-SD conventions across tables.

---

## 9. Farsi / RTL / formatting pitfalls

- **ZWNJ (نیمفاصله, U+200C) is critical** in Persian compound words (میآید → میآید). The Edit
  tool has failed on Persian strings before; use exact-copy oldString, or Python-heredoc edits as
  a fallback, and verify with `rg` after any edit.
- After any edit, **verify by grep** (e.g., `rg -n "old text"`) that no stray/partial occurrence
  remains and that `replaceAll` did not clobber other locations.
- **Every figure needs a visible caption line** `شکل (X-Y): …` — markdown alt-text is invisible
  in the DOCX. In-text figure call-outs (`شکل X-Y را ببینید`) exist for only 2 of 22 figures;
  add the rest.
- **Figure numbering:** order-of-appearance per chapter. `v17_qtable_heatmaps.png` now exists
  (Persian variant generated by `generate_all_Visuals2.py`) but is NOT a thesis figure — شکل ۴-۷
  uses top-level `results/qtable_heatmaps.png` from `advanced_analysis.py`. **23** thesis figures in
  the v9-3 فهرست اشکال (شکل ۲-۱ added 2026-08-16 as `v2_1_conceptual_framework.png`); Result_Help §C
  is synced (23 rows).
- **Tables/figures captions** must match «فهرست جداول» / «فهرست اشکال» exactly.
- English abstract must stay numerically in sync with the Persian abstract and body (e.g., 8.3%
  blackout, 12.9% waste p=0.14, 2.9pp comfort).

---

## 10. Process / workflow rules

- **Single source of truth for edits:** `0-Active Doc/thesis_v9-2.md`. The stale split files
  (`thesis_full.md`, `Sections/*.md`) are a known risk for the DOCX pipeline — do not edit them
  as if they were live, and flag if they drift.
- **Update `AUDIT_PROGRESS.md`** after completing any correction batch (it is the resume
  checkpoint if context is lost). Keep `AUDIT_REPORT_v9-2.md` authoritative for what was checked.
- **Run with the venv** (`venv/`; requirements pinned: numpy 1.24.3, scipy 1.15.3, etc.) if you
  re-run experiments or regenerate figures.
- **Regeneration discipline:** a figure is only trustworthy if the regenerating script and its
  data inputs are consistent with the thesis claims. Before regenerating, diff the script's
  outputs against the numbers currently in the thesis.
- Do not delete: results `.csv/.txt/.npy/config.json`, `Result_Help.md`, audit docs, this file.

---

## 11. Quick sanity checklist before calling a number/claim "done"

1. Read the raw value from the artifact (decimal form), not from prose.
2. Convert to thesis notation only for display (`۰/۸` = 8.0, etc.).
3. Attach the correct p-value to the correct comparison; know if it's paired or independent.
4. Check the claim is not an overstatement (>, lowest, only, every, "no study").
5. Verify tables ↔ prose ↔ English abstract ↔ figures all agree for that number.
6. `rg`-verify no stale duplicates remain after editing.

---

## 12. results/ quick reference (authoritative: `results/Result_Help.md`)

Summary of the risk-relevant parts of the figure/data registry. Full detail is in
`results/Result_Help.md` (sections A–H) — read it before deleting, moving, or regenerating files.

**Script → output map (regeneration):**
- `generate_all_Visuals2.py` → `figures/v01…v18, v2_1` (the 18 thesis vNN figures; `v17_…` is a
  redundant Persian heatmap variant — thesis شکل ۴-۷ uses `advanced_analysis.py`'s top-level
  `qtable_heatmaps.png`). New `v2_1` = شکل ۲-۱ conceptual framework (added 2026-08-16).
- `advanced_analysis.py` → `qtable_heatmaps.png` (شکل ۴-۷)
- `baseline_comparison.py` → `baseline_comparison.{png,csv,txt}` (png superseded by v10; **csv/txt are the SOTA data**)
- `final_analysis.py` → superseded pngs (→v15/v16/v18); `analyze_results.py` → superseded pngs (→v13/v14)
- `offgrid_marl.py` / `ocean_marl_endofday.py` → per-seed plots (working artifacts)
- `battery_sensitivity.py` → `battery_sensitivity/batt{3.5,5,7,9}/…` + `summary.csv` (feeds Table 3-1)
- `support_analysis.py` → `analysis_support/qtab/*.npy` + `report.md` (backs Analysis 1–4)
- `charbonnier_marginal_iql.py` / `kusatake_evolutionary_moo.py` / `behrunani_gne_fairness.py` /
  `may_huang_ppo.py` → baseline reproduction dirs (only `_validation/`, `_timing/`, `_sanity/` pngs are in the thesis)
- `gini_cloud_reanalysis.py`, `gini_more_scenarios.py` → CSV re-analyses only (no figures)

**Superseded top-level images (6) — NOT thesis figures:** `agent_type_comfort.png`,
`community_metrics.png`, `gini_comparison.png`, `sensitivity_cloud.png`,
`sharing_frequency.png`, `baseline_comparison.png`. Do not mistake them for thesis figures;
if archiving, **keep the `.csv`/`.txt` beside `baseline_comparison.png`**.

**Thesis figure placement issues (open presentation work):**
- Every figure currently has only markdown alt-text (invisible in DOCX) — add visible
  «شکل (X-Y): …» caption lines under all 22 figures.
- Orphan figures with zero explanatory prose: شکل ۳-۵ (v01), شکل ۴-۳ (v07), شکل ۴-۵ (v15);
  weak explanatory text: شکل ۳-۶ (v03), ۳-۴ (v04), ۳-۷ (v06).
- Only 2 of 22 figures are cited in prose (شکل ۳-۱, شکل ۴-۷) — add «شکل X-Y را ببینید» call-outs.
- Candidate optional figures (not generated): training/convergence learning curves,
  fairness–efficiency trade-off visual, aggregated battery-capacity chart.
