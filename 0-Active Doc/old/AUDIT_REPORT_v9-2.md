# Research Integrity Audit Report — thesis_v9-2

**Document audited:** `0-Active Doc/thesis_v9-2.md` (Persian M.Sc. thesis, 1761 lines)
**Audited against:** `thesis_v9.md` diff — v9-2 is the newer revision (correctly added
`t(4)=-2.84, p=0.047` and `t(8)=-3.562, d=2.25` to the innovator claims that v9 mis-attributed).
**Data sources:** `results/baseline_comparison.txt`, `results/statistical_tests.txt`,
`results/cloud_sensitivity_reanalysis.csv`, `results/gini_reanalysis.csv`,
`results/gini_more_scenarios.csv`, `results/battery_sensitivity/summary.csv`,
`results/analysis_support/report.md`, `results/analysis_support/qtab/*.npy`,
`results/baseline_*_sensitivity/seed_*/final_metrics.csv`,
`results/{scenario}/seed_*/final_metrics.csv`,
scripts `final_analysis.py`, `support_analysis.py`, `generate_all_Visuals2.py`, `offgrid_marl.py`
**Date:** 2026-08-15
**Decimal-convention resolution:** Re-verified after a reviewer challenge. The document's convention
is `[fractional digits]/[integer part]` → `integer.fraction` (e.g. `۹/۱۲` = 12.9, `۳/۸` = 8.3,
`۰/۷` = 7.0). Confirmed by external ground truth: LG Chem RESU7H battery — `۰/۷` total = 7.0 kWh and
`۶/۶` usable = 6.6 kWh (real spec 7.0/6.6), 50% charge written `۵/۳` = 3.5 kWh (= half of 7.0),
Ofgem 2,700 kWh/yr `۴/۷` = 7.4 kWh/day (= 2700/365), MCS installs `۵/۳ تا ۰/۴` = 3.5–4.0 kWp,
3–4×400W panels ↔ `۳/۱` = 1.3 kW peak. **C1, C2 and C9 in the original audit were based on a
mis-reading of leading-zero fractions (`۰/۸` as 0.8 instead of 8.0, etc.). C2 and C9 are fully
retracted; C1 is downgraded to a minor harmonization note. C7 and C8 are also retracted after
re-verification (reproduced exactly from saved artifacts — see below).** C3–C6, C10 are unaffected
(verified against `baseline_comparison.txt` / results files, no leading-zero ambiguity).

---

## Summary verdict

The empirical content is overwhelmingly accurate: **every headline statistic is reproducible**
from the saved artifacts (Section A/B), and v9-2 fixed the v9 innovator t-stat mis-attributions.
Note: items C1, C2, C7, C8, C9 of the original draft were **re-verified and corrected after a
reviewer challenge on the document's decimal convention** — C2, C7, C8, C9 are fully retracted
(sharing-frequency and Kusatake figures reproduce exactly from saved artifacts), C1 downgraded
to a minor harmonization note (details below). The remaining **real errors** are: the H1 waste
test labelled "independent" when the reported p = 0.14 is only the paired-test value; p = 0.193
attached to the wrong comparison; and two factual overstatements in §4-10. None of these
overturn the four headline findings, but they should be corrected before submission.

---

## Section A — Numerical claims (VERIFIED, reproducible)

| Claim | Verification |
|---|---|
| Table 4-1 (5 scenarios × comfort/Jain/blackout/waste, ±SD) | ✓ matches `baseline_comparison.txt` row-for-row |
| 2.9pp prosocial comfort advantage (mixed, p = 0.0011) | ✓ t = 8.487 (2.95pp) |
| All-selfish vs all-prosocial comfort t = 0.845, p = 0.423 | ✓ independent t |
| Varied-altruism prosocial-vs-selfish t(4) = 2.834, p = 0.0472, CI [0.0004, 0.040] | ✓ `statistical_tests.txt` |
| Innovator vs mixed comfort t(8) = -3.562, p = 0.0074, d = 2.25, CI [-0.030, -0.006] | ✓ |
| ANOVA comfort F(4,20) = 3.362, p = 0.0293; excl. innovator F(3,16) = 0.6745, p = 0.5802 | ✓ |
| Jain ANOVA F = 2.71, p = 0.060; excl. innovator F = 0.54, p = 0.663 | ✓ |
| Gini mixed 0.0790 → innovator 0.0962, +22% (21.8%), paired t(4) = -2.84, p = 0.047 | ✓ |
| Innovator gini above mixed 95% CI in 4/5 seeds (sample-SD CI upper = 0.0883) | ✓ (seed 1011 = 0.0880 < 0.0883) |
| Table 4-8: comfort -0.018, Jain -1.7pp, blackout +1.2pp/+8.3%, gini +0.0172/+22%, waste 4.34→4.70 (+8.3%) | ✓ |
| Cloud 15/25/35%: gaps 2.95/2.58/3.05pp; t = 8.487/6.759/2.452; p = 0.0011/0.0025/0.0703; prosocial & selfish each lose ~13% of base comfort | ✓ |
| 15/15 seed–cloud direction consistency | ✓ (recomputed: prosocial > selfish in all 15) |
| Waste mixed vs all-selfish: 12.87% reduction, PAIRED t = -1.87, p = 0.135 | ✓ (independent p = 0.091) |
| Waste all-prosocial vs all-selfish: 11.46% reduction, independent t = -1.422, p = 0.193 | ✓ |
| Waste mixed vs no-sharing 50% (8.82 → 4.34); all-selfish 43% (8.82 → 4.98) | ✓ |
| Q means 3.934/3.807/3.864; 6.9% Q-policy divergence; 18.2% actual sharing; 37.5% surplus; r = 0.284, p = 0.170 | ✓ `analysis_support/report.md` |
| Sharing frequency 12.60–13.92% of states: mixed prosocial 13.92±2.00, mixed selfish 13.08±2.77, all-selfish 13.04 | ✓ recomputed `(greedy>=1).mean()` from `qtab/*.npy` matches exactly |
| Battery sensitivity: 0.5 & 0.7 kWh waste SIG (t = -16.18 / -18.68), comfort ns both | ✓ |
| Battery slopes 0.56/0.07/0.06 F·kWh⁻¹; 9.0 kWh +2.74pp; 7.0 kWh ≈ 0 | ✓ |
| Innovator effect consistent in 4/5 seeds | ✓ (gini fails only seed 1011) |
| §4-10 λ sensitivity: Behrunani λ=5 → F = 1.8324 ± 0.0648 vs 1.8386 ± 0.0164 (~3.95× SD) | ✓ recomputed from `final_metrics.csv` |
| §4-10 May & Huang waste-penalty variant: F = 1.7985 ± 0.0130 vs 1.8143 ± 0.0173 | ✓ recomputed |
| §5-1-4: all-prosocial waste SD 0.74 kWh; power analysis ≈ 18 seeds | ✓ (SD; power plausible) |

## Section B — Comparisons (VERIFIED)

- Table 4-10 SOTA: **all 10 rows** match `baseline_comparison.txt` (comfort/fairness/F/blackout/waste). ✓
- Kusatake 411/500 sunny days (82.2%), 89 cloudy (17.8%); cloudy-day comfort 0.607 vs 0.500 no-share
  reference (+21.4%) — **confirmed** in `results/baseline_kusatake/seed_42/weather_split_metrics.csv`. ✓
- Charbonnier vs mixed t = +4.357, p = 0.0121; Kusatake t = +7.107, p = 0.0021 ✓
- Mixed vs control t = -0.635, p = 0.5601; mixed vs all-selfish t = -0.194, p = 0.8559 ✓
- 10-group ANOVA on F: F = 11.706, p < 0.001 ✓
- Behrunani zero waste (0.00 ± 0.00) ✓
- Table 4-12 2×2: A = 1.8453, B = 1.8361, C = 1.9057 (+0.0207), D/D2 = 1.8359 (+0.0000) ✓

---

## Section C — Findings (re-verified after decimal-convention correction)

1. **Blackout increase prose "۰/۸" reads 8.0% (not 0.8%) — MINOR harmonization, NOT a 0.8→8.3 error.**
   Under the confirmed convention `۰/۸` = 8.0. Lines **33** (abstract_fa), **1144** (RQ table),
   **1420** (§4-9), **1558** (Finding 4) therefore say 8.0%, while Table 4-8 (line 1416: `۳/۸%+`
   = 8.3%) and the English abstract (line 43: 8.3%) report the computed value 8.28%. The prose
   figure is a slight understatement (8.0 vs 8.28). → optional harmonization: change prose
   `۰/۸` → `۳/۸` (8.3) for internal consistency; not a factual error.

2. **RETRACTED — Innovator comfort reduction is CORRECT (2%) everywhere.** `۰/۲` reads 2.0 under the
   confirmed convention. Lines **1414** (Table 4-8 `۰/۲%-` = -2.0%), **1420**, **1538**, **1610**
   all correctly state 2.0%; lines **33**, **1558**, **1586** state ۲ (2%) directly. Computed
   1.96%. No change needed. (Original flag resulted from mis-reading `۰/۲` as 0.2.)

3. **H1 test-type mislabel (§5-1-1-2, line 1580).** The mixed-vs-all-selfish waste test is
   labelled «آزمون t مستقل» (independent) with p = 0.14. p = 0.14 only holds for the **paired**
   test (t = -1.87, p = 0.135; independent gives p = 0.091). §4-2 (line 1235) labels the same test
   correctly as «آزمون t زوجی». → change مستقل → زوجی in H1.

4. **p = 0.193 wrong attachment (line 1672).** The validity-threats paragraph cites
   «عدم معنیداری آماری برای کاهش هدررفت انرژی (p = 0.193)» in the context of the headline
   12.9% reduction. p = 0.193 belongs to the **all-prosocial vs all-selfish** comparison (11.5%,
   line 1235); the headline 12.9% reduction has p = 0.14. → replace p = 0.193 with p = 0.14
   (or reword the comparison).

5. **«اتلافی بیش از دو برابر هر روش یادگیریمحور» overstatement (line 1486).** Control waste
   8.82 is >2× only vs Charbonnier (4.02), Kusatake (4.22), mixed (4.34), all-prosocial (4.41);
   it is ~1.8–1.9× vs all-selfish (4.98), varied (4.96), innovator (4.70), May & Huang (4.66).
   → soften to «نزدیک به دو برابر / بیشتر از هر روش یادگیریمحور».

6. **«پایینترین آسایش جامعه در میان چهار روش بازتولیدشده (۹۱۷۱/۰)» false (line 1490).**
   Behrunani comfort 0.9171 is NOT the lowest of the four reproduced methods: May & Huang PPO
   = 0.9058 is lower. → restate (e.g., Behrunani trades waste minimization for a low
   community comfort, second-lowest of the four).

7. **RETRACTED — Sharing frequency "۱۲–۱۴٪ از وضعیتها" is REPRODUCIBLE (not hardcoded).**
   Recomputing `(greedy >= 1).mean()` over all Q-states from the saved Q-tables
   (`results/analysis_support/qtab/`) reproduces the exact thesis values: mixed prosocial
   13.92 ± 2.00 (thesis ۱۳/۹۲ ± ۲/۰۰ ✓), mixed selfish 13.08 ± 2.77 (thesis ۱۳/۰۸ ± ۲/۷۷ ✓),
   overall 13.5% (mixed) / 13.04% (selfish). The values in `generate_all_Visuals2.py` line 668
   are consistent with these computations. The earlier audit's "54.5%" figure was an error in the
   audit recomputation, not in the thesis. NOTE: Fig 4-4 error bars (0.5–0.8) still appear
   inconsistent with Table 4-4 SDs (2.0–3.2) — minor figure-vs-table check remains open.

8. **RETRACTED — Kusatake "411/500 days, 82% sunny, 0.607 vs 0.500, +21%" is fully supported.**
   `results/baseline_kusatake/seed_42/weather_split_metrics.csv` shows: sunny 411 days (82.2%),
   cloudy 89 days (17.8%), cloudy-day comfort 0.607 vs 0.500 (no-sharing reference), +21.4%.
   These match the thesis claims exactly. The earlier audit only checked the 10-day
   `timing_report.txt`, which is a sanity check and does not contain these numbers — but the
   per-seed weather-split CSVs do. No artifact gap.

9. **RETRACTED — Table 4-9 Behrunani λ = ۰/۱ reads 1.0, matching the stated baseline. NOT a typo.**
   Under the confirmed convention `۰/۱` = 1.0 (integer 1, fraction 0); §4-10 line 1465 baseline
   λ=۱ and all `config.json` values (λ = 1.0) are consistent. No change needed.

10. **Table 4-12 mixes F conventions (lines 1517–1522).** Cells A (1.8453), B (1.8361), D/D2
    (1.8359) report training-F, but cell C reports greedy-F (1.9057); training-F for C is 1.8714.
    The improvement column is greedy-based for all. → either use greedy-F throughout or label the
    column per row.

### Minor notes (presentation-level)

- Table 4-8 Jain relative change «۷/۱٪-» reads 1.7% under the confirmed convention; computed
  (0.9234−0.9069)/0.9234 = 1.79% → rounds to 1.8%. §4-2 (line 1231) correctly says ۸/۱ (1.8%).
  Minor one-directional rounding inconsistency (Table 4-8 1.7% vs §4-2 1.8%).
- Table 4-2 reports **sample** SD (mixed comfort 0.007) while Table 4-6 reports **population** SD
  (0.0063) for the same underlying 5-seed data. Pick one convention.
- §4-12 / §5-1-4 power analysis "≈18 seeds" is plausible but not recomputed here (no SDs persisted
  for the 35% condition in CSV form; the figure hardcodes SD 0.0271/0.0142).
- §5-1-1 Finding 5 sharing windows (8am–6pm altruistic vs 10am–4pm prosocial) not directly
  checkable from saved artifacts.
- Line 1560's «۱۲–۱۴٪» and line 1566's «۱۸/۲٪» are two different sharing metrics (states vs time
  steps); ensure the text never conflates them.

---

## Overall verdict

**The four headline findings are all confirmed and reproducible** (prosocial comfort advantage
2.9pp/p=0.0011; scarcity persistence 2.58–3.05pp; non-zero-sum fairness-efficiency; innovator
destabilization 22% gini / t(8)=-3.562). The errors in Section C are real but **localized and
mechanical**: two are test-type/attachment labels (C3, C4), two are §4-10 wording overstatements
(C5, C6), one is a table-cell F-convention mix (C10). C1 is a minor harmonization note (8.0% prose
vs 8.3% table/abstract, computed 8.28%). C2, C7, C8 and C9 were **retracted** after re-verification
(decimal-convention misreading and audit recomputation errors — the document reproduces correctly
in all four cases). Fixing C1 and C3–C6, C10 is a straightforward text edit; no experiment needs
re-running.
