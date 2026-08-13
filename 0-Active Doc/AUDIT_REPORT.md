# Research Integrity Audit Report

**Document audited:** `0-Active Doc/thesis_v8.md` (Persian M.Sc. thesis, 1561 lines)
**Data sources:** `results/baseline_comparison.csv|.txt`, `results/statistical_tests.txt`,
`results/analysis_support/report.md`, `results/cloud_sensitivity_reanalysis.csv`,
`results/gini_reanalysis.csv`, `results/gini_more_scenarios.csv`,
`results/battery_sensitivity/summary.csv`, scripts `final_analysis.py`, `advanced_analysis.py`,
`gini_cloud_reanalysis.py`, `gini_more_scenarios.py`, `results/figures/`
**Date:** session-complete

---

## Summary verdict

Every quantitative claim in the thesis that is checkable from the saved artifacts is **accurate**.
The two discrepancies flagged early in the audit (Gini-vs-fairness ANOVA; paired-vs-unpaired waste
t-test) were both **resolved as correct on the document's side** (doc used the Jain fairness index
and an independent t-test, respectively). A small number of **presentation-level inconsistencies**
remain (listed below), most minor; none overturns any headline finding.

---

## Section A — Numerical claims (VERIFIED)

| Claim | Status |
|---|---|
| 2.9pp prosocial advantage (mixed) | ✓ 2.95pp computed |
| p = 0.0011 (t = 8.487) | ✓ |
| 2% community-comfort drop (innovator) | ✓ 1.96% |
| 22% Gini increase (innovator) | ✓ 21.8% |
| 8.3% blackout increase (innovator) | ✓ |
| 12.9% waste (mixed vs all-selfish) | ✓ 12.87% |
| 50% waste (mixed vs no-sharing) | ✓ 50.8% |
| p = 0.14 (waste reduction) | ✓ t = −1.87, p = 0.135 |
| 43% (all-selfish vs no-sharing) | ✓ 43.5% |
| 37.5% surplus / 18.2% sharing | ✓ (Analysis 3) |
| 6.9% Q-policy divergence | ✓ (Analysis 2) |
| Q-values 3.9344 / 3.8066 / 3.8637 | ✓ (Analysis 2) |
| r = 0.284, p = 0.170 (fairness–waste) | ✓ (Analysis 4) |
| cloud gap 2.58pp (25%) / 3.05pp (35%) | ✓ |
| blackout 14.5% / 15.7% | ✓ |
| Cohen's d 3.79 / 2.25 / 1.27 | ✓ |
| ANOVA 5 scenarios F = 3.362, p = 0.0293 | ✓ |
| ANOVA excl. innovator F = 0.6745, p = 0.5802 | ✓ (0.67/0.580) |
| Jain fairness ANOVA F = 2.7087, p = 0.0595; excl. innovator F = 0.5385, p = 0.6627 | ✓ |
| innovator-gini paired t vs mixed t(4) = −2.84, p = 0.047 | ✓ |
| Gini +21.77% vs mixed; +13.32% vs next-worst (prosocial) | ✓ (13% in doc) |
| Table 4-3 SDs (population SD) | ✓ .0067/.0087/.0058/.0098/.0079 |
| Table 4-6 cloud SDs + ratios (4.3x / 1.7x), abs drop .122/.123 | ✓ |
| 15/15 seed–cloud direction consistency | ✓ |
| Power analysis ≈18 seeds | ✓ (20 conservative / 13 pooled) |
| Table 4-8 relative changes | ✓ comfort −2.0%, fairness −1.7%, blackout +1.2pp/+8.3%, gini +22%, waste +8.3% |
| Battery sensitivity slopes 0.56 / 0.07 / 0.06 F·kWh⁻¹ | ✓ (summary.csv) |
| 9.0 kWh gap +2.74pp; 7.0 kWh gap ≈ 0 | ✓ |
| γ = 0.99 → effective horizon ≈ 100 steps | ✓ |
| Varied-altruism comfort 0.914 / waste 4.96 | ✓ |
| Ch.5 battery sensitivity (waste SIG at 0.5 & 0.7 kWh; comfort ns both) | ✓ |

## Section B — Comparisons (VERIFIED)
- Table 4-10 SOTA: all 10 rows match `baseline_comparison.txt` (comfort/fairness/F/blackout/waste). ✓
- SOTA stats: Charbonnier vs mixed t = +4.357, p = 0.0121 ✓; Kusatake t = +7.107, p = 0.0021 ✓;
  mixed vs control t = −0.635, p = 0.5601 ✓; mixed vs all-selfish t = −0.194, p = 0.8559 ✓;
  10-group ANOVA F = 11.706, p < 0.001 ✓; Kusatake 411/500 sunny days (82%) ✓.
- Table 4-12 2×2: A = 1.8453, B = 1.8361, C = 1.9057 (+0.0207), D = 1.8359 — all match. ✓
- Behrunani λ=5 sensitivity (F = 1.8324 ± 0.0648, ~4x SD) and May–Huang waste-penalty variant
  (F = 1.7985 ± 0.0130) internally consistent with script output. ✓

## Section C — Tables (VERIFIED present)
Tables 2-1, 3-1…3-12, 4-1…4-12 all present (33 tables). `جدول ۳-X` placeholder caption was
renumbered to `جدول ۳-۱` (battery/capacity table) and all subsequent chapter-3 tables shifted
3-1…3-11 → 3-2…3-12; captions and in-text references verified monotonic (residual `X` = none).

## Section D — Figures (VERIFIED)
All 17 files in `results/figures/` + `results/qtable_heatmaps.png` + 4 baseline `results_plot.png`
exist; every reference resolves; no orphans.

## Section E — Explanations (VERIFIED)
All mechanism narratives (reciprocity cycle, no-sharing baseline, sparse action/state space,
one-richest-house Gini model, γ-horizon credit assignment) are consistent with the verified data.
Explanations in 5-1-1-1 are grounded in the quantitative results rather than speculation.

## Section F/G/H — Hypotheses, research questions, objectives (RESOLVED)
New subsection **۵-۱-۱-۲- آزمون فرضیههای پژوهش** (end of §5-1-1) now labels all four hypotheses
with explicit accept/reject verdicts: H1 waste (12.9% reduction, ns p = 0.14) **not fully
supported**; H2 comfort (2.9pp, p = 0.0011) **supported**; H3 scarcity persistence
(2.58pp p = 0.0025 / 3.05pp p = 0.0703) **partially supported**; H4 innovator (22% gini,
p = 0.0074, d = 2.25) **supported**. Research questions and objectives remain mapped by findings 1–5.

---

## Open discrepancies to fix before submission

> **All 10 items below were EXECUTED** (see verification notes after each). Re-verified against
> `thesis_v8.md` after edits; only item 10 is a data-persistence note (no thesis text change).

1. **Cloud-25% significance inconsistency (§4-12 line 1349 vs Table 4-6 / §4-7).** §4-12 reports
   p = 0.159 / p = 0.078 for cloud 25%/35% — these are **independent-t** values; the paired t used in
   Table 4-6 gives p = 0.0025 (significant) for 25%. §4-7 additionally claims "significance only at
   base 15%", which the data contradict. **Fix:** harmonize on paired t → 25% IS significant.
   ✅ **EXECUTED:** §4-12 (line 1349) now reports p = 0.0025 (25%, significant) and p = 0.0703 (35%,
   ns); §4-7 (line 1205) restated likewise; no stale 0.159/0.078 values remain.
2. **§4-4 top-decile formula error (line 1122).** Formula «(1+G)/2 × 10%» yields ~5.4%, not the stated
   17.9%/19.2%. Correct relation (one-richest-house): **S = G + 0.1** → mixed 17.90% ✓, innovator
   19.62% (doc's 19.2% understated). Fix formula and innovator number.
   ✅ **EXECUTED:** formula replaced with $S \approx G + 0.1$; innovator value corrected to ۶۲/۱۹٪
   (19.62); mixed ۹۰/۱۷٪ (17.90) retained.
3. **§4-4 seed-consistency phrasing (line 1124).** "Innovator high in 4/5 seeds, only 456 within
   non-innov range" — per-seed comparison confirms 4/5 (fails only seed 1011), but the **range clause
   is inverted**: seeds 123, 456, 789, 1011 all fall inside [0.0715, 0.1026]; only seed 42 (0.111)
   exceeds. Fix the clause.
   ✅ **EXECUTED:** reworded — innovator gini exceeds its seed's non-innov mean in 4/5 seeds; only
   seed 42 (0.111) lies markedly above the rest. Claims at lines 1473/1485 (4/5 consistency) remain valid.
4. **§4-4 / §4-7 CI overstatement.** "Innovator gini exceeded the upper 95% CI of all other scenarios"
   is false for all-prosocial (innovator mean 0.0962 < prosocial upper 0.0971); it exceeds mixed
   (0.0873), all-selfish (0.0904), varied (0.0916). Also "above mixed CI in 4/5 seeds" should be 5/5.
   Restate precisely.
   ✅ **EXECUTED:** §4-4 restated — innovator (0.0962) exceeds CIs of mixed/selfish/varied but
   overlaps all-prosocial; §4-7 line 1247 claim ("4/5 seeds above mixed CI") is correct under the
   sample-SD CI (0.0884) and left unchanged.
5. **§4-2 fairness drop (line 1076) vs Table 4-8.** "1.6%" vs "−1.7%"; computed 1.79% relative /
   1.65pp absolute. Harmonize to 1.8%.
   ✅ **EXECUTED:** §4-2 now states "۸/۱ درصد پایینتر" (1.8%); no 1.6% claim remains.
6. **§5-1-4 horizon mislabel (line 1451).** "افق ۷۴/۲ سالهی شبیهسازی" — 2.74 years is the 1000-day
   *evaluation window* (line 1054 correct); the full simulation is 8000 days ≈ 21.9 years. Adjust wording.
   ✅ **EXECUTED:** §5-1-4 now says "پنجرهی ارزیابی ۱۰۰۰ روزه" and identifies 8000 days ≈ 21.9 years
   as the full simulation horizon.
7. **§4-2 base ambiguity (line 1080).** "هدررفت ۹/۱۲٪ بالاتر نسبت به سناریوی مختلط" — 12.9% is only
   valid with all-selfish as base; with mixed as base it is 14.8%.
   ✅ **EXECUTED:** §4-2 now states "حدود ۸/۱۴ درصد بیشتر بود (معادل ۶۴/۰ کیلوواتساعت در روز)" —
   mixed as base (0.64/4.34 = 14.7% ≈ 14.8%). The 12.9% figure elsewhere (abstract, §4-12, H1) refers
   to the mixed-vs-all-selfish *reduction* and is correct in those contexts.
8. **Ch.5 hypothesis labeling (F).** No explicit «فرضیه» references or accept/reject statements.
   ✅ **EXECUTED:** new subsection ۵-۱-۱-۲- آزمون فرضیههای پژوهش added at end of §5-1-1 (before
   §5-1-2) with explicit H1–H4 verdicts (see Section F/G/H above).
9. **«جدول ۳-X» placeholder** (~lines 560/562) still unnumbered.
   ✅ **EXECUTED:** renumbered to جدول ۳-۱; tables 3-1…3-11 shifted to 3-2…3-12 with captions and
   all in-text references updated (monotonic; no residual X).
10. **Sharing t(8) = 0.684 (§4-5 line 1151)** — plausible (means 0.1392 vs 0.1304, +0.88pp) but not
    independently reproducible from saved artifacts (per-seed sharing data not persisted to CSV).
    ✅ **NOTE (data persistence, no text change):** per-seed sharing-frequency data is only printed by
    the script and is not saved as CSV; for reproducibility, future work should persist it. The
    t(8) = 0.684 value is internally consistent with the stated means and passes sanity checks, so it
    is retained as-is in the thesis text.

## Non-audit template items still open
- References (line 1507+) are APA bullets; template requires a numbered IEEE-style list.

---

## Overall verdict

**The empirical content of the thesis is trustworthy, and the document now matches the audit
requirements.** All ten discrepancies identified by the audit have been corrected and re-verified
against `thesis_v8.md` (all checkable numbers, statistics, tables, figures, and explanations match
the saved simulation artifacts). All headline findings (prosocial comfort advantage, scarcity
persistence, non-zero-sum fairness–efficiency, innovator destabilization) are unchanged and are
consistent with the data. Two residuals remain as *documented notes*, not errors: (1) §4-5 sharing
t(8) = 0.684 is retained because it is internally consistent, though its per-seed input data is not
persisted to CSV (future-work reproducibility note); (2) the References list is still APA-style
bullets, which the template requires converted to a numbered IEEE-style list.
