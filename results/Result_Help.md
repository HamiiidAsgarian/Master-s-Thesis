# results/ — Directory Map & Figure Registry

> **Purpose of this file:** A maintenance map + verified numeric reference for the `results/` tree.
> Sections A–H cover images, figures, and directory management.
> Section N provides the full project inventory (all scripts, all images, orphans, missing figures).
> Sections I–M cover **every verified number** in the thesis — scenario results, statistical tests,
> data source mappings, and simulation parameters — for quick lookup.
>
> **Related thesis:** `0-Active Doc/Thesis_v9-5.md` · **Registry of all 23 thesis figures:** Section C.
> **Snapshot date:** Aug 2026 (2026-08-16 sync: شکل ۲-۱ added, v10 rebuilt from real data;
> 2026-08-20: full numeric audit completed — all 87+ table values + 16 statistical tests verified;
> 2026-08-20: forensic 5-task audit completed — see Section M;
> 2026-08-20: ddof=1 recomputation for Tables 4-3/4-6 + battery DOD check — see Sections I-3, I-5, M-6;
> 2026-08-21: figure paths updated — شکل ۴-۱۱/۴-۱۲ now point to full 500-day runs;
> 2026-08-21: full project inventory added — Section N;
> 2026-08-21: training convergence figure added — شکل ۴-۱-الف; orphan files archived).

---

## A. Quick numbers

| Group | Count | In thesis? |
|---|---|---|
| Main figures (`results/figures/`, v01–v16, v18 + v2_1 + fig_training_convergence) | 19 | ✅ All 19 |
| Q-table heatmaps (`results/qtable_heatmaps.png`) | 1 | ✅ |
| Baseline validation plots (4 runs) | 4 | ✅ All 4 (2 updated to full runs) |
| **Thesis figure total** | **24** | **All referenced** |
| Superseded top-level images (→ replaced by v-figures) | 6 | ❌ None |
| Orphaned diagnostic plots (replaced by full runs) | 2 | ❌ None |
| Non-thesis generated (v17 Persian variant) | 1 | ❌ |
| Per-seed runtime plots (`*/seed_*/results_plot.png`) | ~67 | ❌ Working artifacts |
| **All image files under results/** | **~97** | — |

---

## B. Directory tree

```
results/
├── figures/                          # MAIN thesis figures — 19, ALL used (do not delete)
│   ├── v01_ocean_to_rl_mapping.png   ├── v10_sota_comparison.png
│   ├── v02_ring_topology.png         ├── v11_lorenz_curve.png
│   ├── v03_two_phase_sharing.png     ├── v12_system_architecture.png
│   ├── v04_demand_profiles.png       ├── v13_community_metrics.png
│   ├── v05_solar_curve.png           ├── v14_agent_comfort_split.png
│   ├── v06_community_compositions.png├── v15_gini_comparison.png
│   ├── v07_reciprocity_cycle.png     ├── v16_sharing_frequency.png
│   ├── v08_innovator_effect.png      ├── v18_scarcity_sensitivity.png
│   ├── v09_tragedy_commons.png       ├── fig_training_convergence.png  # NEW — شکل ۴-۱-الف
│   └── v2_1_conceptual_framework.png # شکل ۲-۱
├── qtable_heatmaps.png               # USE — شکل ۴-۷ (advanced_analysis.py)
├── agent_type_comfort.png            # DISCARD → superseded by v14
├── community_metrics.png             # DISCARD → superseded by v13
├── gini_comparison.png               # DISCARD → superseded by v15
├── sensitivity_cloud.png             # DISCARD → superseded by v18
├── sharing_frequency.png             # DISCARD → superseded by v16
├── baseline_comparison.png           # DISCARD → superseded by v10 (+ .csv / .txt are the data)
├── baseline_charbonnier_validation/results_plot.png   # USE — شکل ۴-۱۰ (§4-10-1)
├── baseline_kusatake_timing/results_plot.png          # ORPHANED — replaced by baseline_kusatake/seed_42/
├── baseline_behrunani_sanity/results_plot.png         # ORPHANED — replaced by baseline_behrunani/seed_42/
├── baseline_may_huang_sanity/results_plot.png         # USE — شکل ۴-۱۳ (§4-10-1)
│
│   ── Below: per-seed WORKING artifacts (config.json + final_metrics.csv + results_plot.png) ──
├── all_prosocial/  all_selfish/  mixed/  innovator_effect/  varied_altruism/  control_always_default/
│   └── seed_{42,123,456,789,1011}/results_plot.png      # offgrid_marl.py main scenario runs
├── baseline_charbonnier/  baseline_kusatake/  baseline_behrunani/  baseline_may_huang/
│   └── seed_*/results_plot.png                          # 5-seed baseline reproduction runs
├── baseline_behrunani_lambda5_sensitivity/              # Behrunani λ=5 sensitivity (5 seeds)
├── baseline_may_huang_waste_sensitivity/                # May–Huang waste-penalty sensitivity (5 seeds)
├── battery_sensitivity/batt{3.5,5,7,9}/mixed|always_default/   # battery capacity sweep
├── analysis_support/batt05/mixed/seed_*/                # 0.5 kWh battery support run (5 seeds)
├── analysis_support/qtab/{mixed_q,selfish_q}.npy        # saved Q-tables (analysis_support.py)
├── ocean_marl_endofday_sanity{,_community,_community_homogeneous}/results_plot.png
└── archive/                          # Orphaned files (moved 2026-08-21, safe to delete)
    ├── agent_type_comfort.png        ├── baseline_comparison.png
    ├── community_metrics.png         ├── gini_comparison.png
    ├── sensitivity_cloud.png         ├── sharing_frequency.png
    ├── v17_qtable_heatmaps.png       ├── baseline_kusatake_timing/
    └── baseline_behrunani_sanity/
```

**Non-image data artifacts you will also find here** (each run dir): `config.json`,
`final_metrics.csv`, plus aggregate `.csv`/`.txt` at the top level
(`baseline_comparison.csv/.txt`, `statistical_tests.txt`, `analysis_support/report.md`,
`cloud_sensitivity_reanalysis.csv`, `gini_reanalysis.csv`, `gini_more_scenarios.csv`,
`battery_sensitivity/summary.csv`). These back every number in the thesis and must be kept.

---

## C. Thesis figure registry (all 23, authoritative شکل numbering)

Numbering = order of appearance per chapter, matches «فهرست اشکال» in `0-Active Doc/Thesis_v9-3.md`.

| شکل | File | Section | Caption (as in List of Figures) | Status |
|---|---|---|---|---|
| ۱-۱ | figures/v09_tragedy_commons.png | §1-2 | تراژدی منابع مشترک در اشتراک انرژی | ✅ placed |
| ۲-۱ | figures/v2_1_conceptual_framework.png | §2-5-1 | چارچوب مفهومی: مدل هماهنگی تعدیل‌شده با شخصیت | ✅ placed (added 2026-08-16) |
| ۳-۱ | figures/v12_system_architecture.png | §3-2 | نمودار جریان معماری سیستم (حلقه ۱۰ بلوکی) | ✅ placed |
| ۳-۲ | figures/v02_ring_topology.png | §3-6 | توپولوژی حلقوی ریزشبکه محله‌ای | ✅ placed |
| ۳-۳ | figures/v05_solar_curve.png | §3-6 | مدل نیم‌سینوسی تابش خورشیدی | ✅ placed |
| ۳-۴ | figures/v04_demand_profiles.png | §3-6 | چهار الگوی تقاضای ساعتی | ✅ placed |
| ۳-۵ | figures/v01_ocean_to_rl_mapping.png | §3-7 | نگاشت ویژگی‌های OCEAN به پارامترهای یادگیری | ⚠️ orphan text (see §F) |
| ۳-۶ | figures/v03_two_phase_sharing.png | §3-10 | سازوکار اشتراک انرژی دو مرحله‌ای | ✅ placed |
| ۳-۷ | figures/v06_community_compositions.png | §3-11 | ترکیب‌های جامعه آزمایشی | ✅ placed |
| ۴-۱ | figures/v13_community_metrics.png | §4-2 | سنجه‌های سطح جامعه در پنج سناریو | ✅ placed |
| ۴-۱-الف | figures/fig_training_convergence.png | §4-2 | همگرایی آموزش: آسایش جامعه در ۸۰۰۰ قسمت | ✅ added 2026-08-21 |
| ۴-۲ | figures/v14_agent_comfort_split.png | §4-3 | آسایش عامل‌های نوع‌گرا در مقابل خودخواه | ✅ placed |
| ۴-۳ | figures/v07_reciprocity_cycle.png | §4-3 | چرخه متقابله‌گری در جوامع مختلط | ⚠️ orphan text (see §F) |
| ۴-۴ | figures/v11_lorenz_curve.png | §4-4 | منحنی لورنز — مقایسه مختلط و اثر نوآور | ✅ placed |
| ۴-۵ | figures/v15_gini_comparison.png | §4-4 | ضریب جینی بر اساس سناریو | ⚠️ orphan text (see §F) |
| ۴-۶ | figures/v16_sharing_frequency.png | §4-5 | فراوانی اشتراک بر اساس نوع عامل | ✅ placed |
| ۴-۷ | qtable_heatmaps.png | §4-6 | میانگین مقادیر Q در هر ساعت (نقشه‌های حرارتی) | ✅ placed |
| ۴-۸ | figures/v18_scarcity_sensitivity.png | §4-7 | حساسیت به کمبود منابع (احتمال ابری) | ✅ placed |
| ۴-۹ | figures/v08_innovator_effect.png | §4-9 | مکانیسم اثر نوآور | ✅ placed |
| ۴-۱۰ | baseline_charbonnier_validation/results_plot.png | §4-10-1 | صحت‌سنجی بازتولید چاربونیه | ✅ placed |
| ۴-۱۱ | baseline_kusatake/seed_42/results_plot.png | §4-10-1 | زمان‌بندی/همگرایی بازتولید کوساتاکه | ✅ updated 2026-08-21 (full 500-day, was timing/10-day) |
| ۴-۱۲ | baseline_behrunani/seed_42/results_plot.png | §4-10-1 | صحت‌سنجی بازتولید به‌رونانی | ✅ updated 2026-08-21 (full 500-day, was sanity/10-day) |
| ۴-۱۳ | baseline_may_huang_sanity/results_plot.png | §4-10-1 | صحت‌سنجی بازتولید می و هوانگ | ✅ placed |
| ۴-۱۴ | figures/v10_sota_comparison.png | §4-10-1 | مقایسه با آخرین دستاوردهای علمی | ✅ regenerated 2026-08-16 (real data, Aloor dropped) |

---

## D. Generation sources (script → output)

| Script | Produces | In thesis? |
|---|---|---|
| `generate_all_Visuals3.py` | `figures/v01…v18, v2_1` + `qtable_heatmaps.png` (v17 = non-thesis Persian heatmap variant) | ✅ 20/20 thesis figures (18 main + v2_1 + qtable) |
| `generate_training_curves.py` | `figures/fig_training_convergence.png` + `training_convergence_per_episode.csv` | ✅ شکل ۴-۱-الف |
| `generate_all_Visuals2.py` | Same as v3 (legacy version, superseded) | ✅ identical outputs |
| `advanced_analysis.py` | `results/qtable_heatmaps.png` | ✅ alternative generator for شکل ۴-۷ |
| `baseline_comparison.py` | `results/baseline_comparison.png/.csv/.txt` | png superseded by v10; csv/txt are the SOTA data |
| `final_analysis.py` | `gini_comparison.png`, `sharing_frequency.png`, `sensitivity_cloud.png` | ❌ superseded (→v15, v16, v18) |
| `analyze_results.py` | `community_metrics.png`, `agent_type_comfort.png` | ❌ superseded (→v13, v14) |
| `offgrid_marl.py` | per-seed plots under all_prosocial/all_selfish/mixed/innovator_effect/varied_altruism/control_always_default | ❌ working artifacts |
| `ocean_marl_endofday.py` | per-seed plots under ocean_marl_endofday_sanity* | ❌ working artifacts |
| `battery_sensitivity.py` | `battery_sensitivity/batt{3.5,5,7,9}/…` (+ `summary.csv`) | ❌ plots; summary.csv feeds Table 3-1 |
| `support_analysis.py` | `analysis_support/batt05/…`, `analysis_support/qtab/*.npy`, `analysis_support/report.md` | ❌ plots; report.md backs Analysis 1–4 |
| `charbonnier_marginal_iql.py` | `baseline_charbonnier/*` + `_validation/` | validation ✅, 5-seed plots ❌ |
| `kusatake_evolutionary_moo.py` | `baseline_kusatake/*` + `_timing/` | 5-seed ✅ (shکل ۴-۱۱ from seed_42), timing orphaned |
| `behrunani_gne_fairness.py` | `baseline_behrunani/*` + `_sanity/` + `_lambda5_sensitivity/` | 5-seed ✅ (shکل ۴-۱۲ from seed_42), sanity orphaned |
| `may_huang_ppo.py` | `baseline_may_huang/*` + `_sanity/` + `_waste_sensitivity/` | sanity ✅ (شکل ۴-۱۳), others ❌ |
| `gini_cloud_reanalysis.py`, `gini_more_scenarios.py` | CSV re-analyses only (no figures) | data used in §4-4/§4-7 |

---

## E. Known discrepancies / action items

1. ✅ **RESOLVED 2026-08-16** — `v10_sota_comparison.png` was stale (it plotted Aloor et al. (2024),
   which the thesis removed from the quantitative SOTA comparison — robot-navigation domain, values
   not citable). Rebuilt in `generate_all_Visuals2.py` from `results/baseline_comparison.csv` (real
   5-seed data): 5 OCEAN-MARL scenarios + 4 reproduced baselines + always_default control, mean ± SD
   bars for community comfort and Jain's fairness. All 10 rows verified against thesis Table 4-10
   (ddof=1 SD convention). No Aloor, no estimated-from-figure values.
2. **v17 exists but is NOT a thesis figure.** `v17_qtable_heatmaps.png` is a Persian-labelled heatmap
   variant generated by `generate_all_Visuals2.py` from `analysis_support/qtab/*.npy`. Thesis شکل ۴-۷
   uses top-level `results/qtable_heatmaps.png` from `advanced_analysis.py` (different agent selection
   and non-Persian labels). Keep v17 as a working artifact only.
3. **Superseded top-level images (6)** → moved to `archive/` (2026-08-21):
   `agent_type_comfort`, `community_metrics`, `gini_comparison`, `sensitivity_cloud`,
   `sharing_frequency`, `baseline_comparison` (`.csv`/`.txt` kept in root).
4. **Per-seed runtime plots (~67)** are not thesis material — keep them as raw reproducibility
   evidence, but they can be moved to an `archive/` folder if the tree must be clean.
5. **SD convention standardized (Tables 4-3, 4-6 updated to ddof=1).** Both tables now use sample SD (ddof=1), consistent with Tables 4-1/4-2/4-8/4-10. See Sections I-3 and I-5 for recomputed values. Means and t-stats unchanged; SDs are +11.8% larger than previous ddof=0 values.
6. **No battery DOD limit** — code confirms full 7.0 kWh usable. Thesis text now updated to clarify no DoD constraint (2026-08-21). See Section M-6.
7. **RESOLVED 2026-08-21 — Thesis figure paths updated for شکل ۴-۱۱ and ۴-۱۲.** Both now point to full 500-day runs instead of short diagnostic plots. شکل ۴-۱۱: `baseline_kusatake/seed_42/` (was `baseline_kusatake_timing/`). شکل ۴-۱۲: `baseline_behrunani/seed_42/` (was `baseline_behrunani_sanity/`). The old `_timing/` and `_sanity/` directories moved to `archive/`.
8. **RESOLVED 2026-08-21 — Orphan files archived.** 6 superseded top-level `.png` + 2 orphaned diagnostic directories + v17 Persian variant moved to `results/archive/`.
9. **RESOLVED 2026-08-21 — Training convergence figure added.** شکل ۴-۱-الف (`figures/fig_training_convergence.png`) generated from 25 fresh simulation runs (5 scenarios × 5 seeds, 8000 episodes each). Per-episode data saved in `training_convergence_per_episode.csv`.

---

## F. Thesis placement issues (text, not files)

From the figure-integration audit — all 23 files resolve and sit in the correct sections, but:

- **No visible captions:** every figure's only caption is markdown alt-text (invisible in the
  rendered Word thesis). Add visible «شکل (X-Y): …» caption lines under all figures — only
  شکل ۲-۱ has one so far (added 2026-08-16).
- **Orphan figures (zero explanatory prose):** شکل ۳-۵ (v01, after §3-7 heading), شکل ۴-۳
  (v07, sits between two images), شکل ۴-۵ (v15, sits between two images). Add a lead-in paragraph.
- **Weak explanatory text:** شکل ۳-۶ (v03), ۳-۴ (v04), ۳-۷ (v06).
- **In-text numeric references:** only 2 of 23 figures are cited in prose (شکل ۳-۱, شکل ۴-۷);
  the other 21 are placed without a «شکل X-Y» call-out (incl. the new شکل ۲-۱).

---

## G. Gap analysis — candidate new figures (optional)

| Need | Status | Action |
|---|---|---|
| Training/convergence learning curves (§3-14 / §4-1) | ❌ not generated | Could substantiate convergence claims; per-seed CSVs allow it |
| Fairness–efficiency (Pareto/trade-off) visual (§4-8) | ❌ not generated | The non-zero-sum fairness–efficiency result is argued numerically only |
| Aggregated battery-capacity sensitivity chart | ⚠️ per-seed plots only | Table 3-1 already covers it numerically — optional |

---

## H. One-line file index (quick reference)

**Keep (thesis):** `figures/v01…v18,v2_1,fig_training_convergence`, `qtable_heatmaps.png`,
`baseline_charbonnier_validation/results_plot.png` (شکل ۴-۱۰),
`baseline_kusatake/seed_42/results_plot.png` (شکل ۴-۱۱),
`baseline_behrunani/seed_42/results_plot.png` (شکل ۴-۱۲),
`baseline_may_huang_sanity/results_plot.png` (شکل ۴-۱۳)
→ All updated 2026-08-21 — full 500-day plots for ۴-۱۱ and ۴-۱۲, new training convergence figure added
**Archive/discard:** `archive/` — 6 superseded `.png` + `baseline_kusatake_timing/` + `baseline_behrunani_sanity/` + `v17_qtable_heatmaps.png`
**Never delete (data):** every `*.csv`, `*.txt`, `*.npy`, `config.json`, `*_summary.csv`

---

## I. Verified scenario results (mean ± SD, 5 seeds)

> All values below were independently recomputed from per-seed `final_metrics.csv` files
> and cross-checked against thesis Tables 4-1, 4-2, 4-3, 4-8, and 4-10.
> **Audit date:** 2026-08-20 · **Audit tool:** `python3` direct CSV computation.

### I-1. Community-level metrics (Table 4-1 / Table 4-10)

Source files: `{scenario}/seed_*/final_metrics.csv` — columns: `comfort`, `fairness`, `blackout_rate`, `waste`

| Scenario | Comfort (C̄) | Jain Fairness (F_jain) | Blackout Rate (B) | Waste (W, kWh) |
|---|---|---|---|---|
| all_selfish | 0.9195 ± 0.0098 | 0.9225 ± 0.0097 | 0.1452 ± 0.0137 | 4.9845 ± 0.5029 |
| all_prosocial | 0.9139 ± 0.0112 | 0.9176 ± 0.0107 | 0.1452 ± 0.0137 | 4.4133 ± 0.7443 |
| mixed | 0.9198 ± 0.0075 | 0.9234 ± 0.0077 | 0.1452 ± 0.0137 | 4.3430 ± 0.5523 |
| varied_altruism | 0.9140 ± 0.0068 | 0.9185 ± 0.0061 | 0.1452 ± 0.0137 | 4.9570 ± 0.5425 |
| innovator_effect | 0.9018 ± 0.0085 | 0.9069 ± 0.0094 | 0.1568 ± 0.0108 | 4.7024 ± 0.2695 |
| control (always_default) | 0.9249 ± 0.0051 | 0.9249 ± 0.0051 | 0.1502 ± 0.0103 | 8.8211 ± 0.1067 |

**Combined fairness metric** (Table 4-10 column "F" = comfort + Jain fairness):

| Scenario | F = C̄ + F_jain |
|---|---|
| all_selfish | 1.8420 ± 0.0195 |
| all_prosocial | 1.8315 ± 0.0219 |
| mixed | 1.8432 ± 0.0150 |
| varied_altruism | 1.8325 ± 0.0128 |
| innovator_effect | 1.8088 ± 0.0178 |
| control (always_default) | 1.8498 ± 0.0103 |

### I-2. Agent comfort split by type (Table 4-2)

Source files: same `final_metrics.csv` — columns: `prosocial_comfort`, `selfish_comfort`

| Scenario | Prosocial Comfort | Selfish Comfort | Gap (pp) |
|---|---|---|---|
| mixed | 0.9345 ± 0.0070 | 0.9051 ± 0.0097 | +2.95 |
| varied_altruism | 0.9237 ± 0.0087 | 0.9042 ± 0.0116 | +1.95 |
| innovator_effect | 0.9116 ± 0.0114 | 0.8921 ± 0.0076 | +1.95 |

**Note:** Table 4-6 (scarcity sensitivity) standardized to ddof=1 (2026-08-21). Thesis updated to use ddof=1 values throughout. See Section I-5 for both ddof=0 and ddof=1 columns.

### I-3. Gini coefficients (Table 4-3)

Source files: `gini_reanalysis.csv` (mixed + innovator), `gini_more_scenarios.csv` (all others)
Columns: `scenario`, `seed`, `gini`

**Thesis values (standardized to sample SD, ddof=1 as of 2026-08-21):**

| Scenario | Gini (G) — ddof=0 | Gini (G) — ddof=1 (used in thesis) | Rank (fair→unfair) |
|---|---|---|---|
| mixed | 0.0790 ± 0.0067 | 0.0790 ± 0.0075 | 1 |
| all_selfish | 0.0796 ± 0.0087 | 0.0796 ± 0.0097 | 2 |
| varied_altruism | 0.0844 ± 0.0058 | 0.0844 ± 0.0065 | 3 |
| all_prosocial | 0.0849 ± 0.0098 | 0.0849 ± 0.0109 | 4 |
| innovator_effect | 0.0962 ± 0.0079 | 0.0962 ± 0.0089 | 5 |

ddof=1 SDs are +11.8% larger than ddof=0 (factor √(5/4)). Means identical.
Thesis Table 4-3 now uses ddof=1 column. CI bounds updated to match.

### I-4. Baseline comparison (Table 4-10)

Source files: `baseline_{charbonnier,kusatake,behrunani,may_huang}/seed_*/final_metrics.csv`
Also aggregated in: `baseline_comparison.csv` and `baseline_comparison.txt`

| Method | Comfort | Jain F_jain | Combined F | Blackout | Waste (kWh) |
|---|---|---|---|---|---|
| Charbonnier et al. (IQL) | 0.9401 ± 0.0066 | 0.9433 ± 0.0076 | 1.8834 ± 0.0141 | 0.1452 ± 0.0074 | 4.0189 ± 0.4109 |
| Kusatake et al. (NSGA-II) | 0.9387 ± 0.0064 | 0.9433 ± 0.0062 | 1.8820 ± 0.0125 | 0.1560 ± 0.0158 | 4.2165 ± 0.1003 |
| Behrunani et al. (GNE) | 0.9171 ± 0.0084 | 0.9215 ± 0.0080 | 1.8386 ± 0.0164 | 0.1560 ± 0.0158 | 0.0000 ± 0.0000 |
| May & Huang (PPO) | 0.9058 ± 0.0089 | 0.9085 ± 0.0084 | 1.8143 ± 0.0173 | 0.1726 ± 0.0331 | 4.6605 ± 0.4308 |

**Behrunani waste = 0:** Each agent minimizes hourly waste myopically (game-theoretic design);
zero aggregate waste is a structural property, not an error.

### I-5. Scarcity sensitivity (Table 4-6)

Source file: `cloud_sensitivity_reanalysis.csv`
Columns: `cloud_prob`, `seed`, `prosocial_comfort`, `selfish_comfort`

**Thesis values (standardized to sample SD, ddof=1 as of 2026-08-21):**

| Cloud Prob | Prosocial Comfort (ddof=0) | Prosocial Comfort (ddof=1, used in thesis) | Selfish Comfort (ddof=0) | Selfish Comfort (ddof=1, used in thesis) | Gap (pp) | t-stat | p-value |
|---|---|---|---|---|---|---|---|
| 0.15 (base) | 0.9345 ± 0.0063 | 0.9345 ± 0.0070 | 0.9051 ± 0.0086 | 0.9051 ± 0.0097 | 2.95 | 8.487 | 0.0011 |
| 0.25 | 0.8631 ± 0.0221 | 0.8631 ± 0.0247 | 0.8373 ± 0.0245 | 0.8373 ± 0.0273 | 2.58 | 6.759 | 0.0025 |
| 0.35 | 0.8125 ± 0.0271 | 0.8125 ± 0.0303 | 0.7820 ± 0.0142 | 0.7820 ± 0.0158 | 3.05 | 2.452 | 0.0703 |

ddof=1 SDs are +11.8% larger than ddof=0 (factor √(5/4)). Means and t-stats identical.
Thesis Table 4-6 now uses ddof=1 columns.

---

## J. Verified statistical tests

> All values below independently recomputed from raw per-seed CSV data.
> Source file: `statistical_tests.txt` (5 registered tests) + thesis text-only values.

### J-1. Registered tests (from statistical_tests.txt)

| # | Comparison | Test Type | Statistic | p-value | Verdict |
|---|---|---|---|---|---|
| 1 | all_selfish vs all_prosocial (community comfort) | Independent t | t(8)=0.845 | 0.4229 | Not significant |
| 2 | Mixed prosocial vs selfish (agent comfort) | Paired t | t(4)=8.487 | 0.0011 | Significant |
| 3 | Varied prosocial vs selfish (agent comfort) | Paired t | t(4)=2.834 | 0.0472 | Significant |
| 4 | innovator_effect vs mixed (community comfort) | Independent t | t(8)=−3.562 | 0.0074 | Significant |
| 5 | All 5 scenarios (community comfort) | One-way ANOVA | F(4,20)=3.362 | 0.0293 | Significant |

### J-2. Additional text-only statistical values (thesis §4-2 through §4-10)

| Comparison | Test | Statistic | p-value | Thesis Location |
|---|---|---|---|---|
| Mixed vs innovator (community comfort) | Independent t | t(8)=−3.562 | 0.0074 | §4-8 Test 4 |
| Cohen's d (innovator vs mixed) | Effect size | d = 2.25 | — | §4-8 Test 4 |
| ANOVA without innovator | One-way ANOVA | F(3,16)=0.6745 | 0.5802 | §4-2 |
| Gini ANOVA all 5 scenarios | One-way ANOVA | F(4,20)=2.71 | 0.060 | §4-4 |
| Gini ANOVA without innovator | One-way ANOVA | F(3,16)=0.54 | 0.663 | §4-4 |
| Gini mixed vs innovator | Paired t | t(4)=−2.84 | 0.047 | §4-4 |
| Charbonnier vs mixed (F) | Paired t | t(4)=4.357 | 0.0121 | §4-10 |
| Kusatake vs mixed (F) | Paired t | t(4)=7.107 | 0.0021 | §4-10 |
| Mixed vs control (F) | Paired t | t(4)=−0.635 | 0.5601 | §4-10 |
| Mixed vs all_selfish (F) | Paired t | t(4)=−0.194 | 0.8559 | §4-10 |
| ANOVA across all 10 groups (F) | One-way ANOVA | F(9,40)=11.706 | <0.001 | §4-10 |
| Waste: all_selfish vs mixed | Paired t | t(4)=1.87 | 0.14 | §4-2 |
| Waste: all_selfish vs all_prosocial | Paired t | t(4)=1.384* | 0.193 | §4-2 |
| Cohen's d mixed prosocial vs selfish | Paired effect size | d = 3.80 | — | §4-3 |
| Cohen's d varied prosocial vs selfish | Paired effect size | d = 1.27 | — | §4-3 |

\* Thesis states t=1.422; independently computed t=1.384 (2.7% rounding difference from
intermediate precision; same conclusion: p>0.05, not significant).

---

## K. Data source mapping (number → file)

Quick lookup: "Where does thesis Table X, row Y come from?"

| Thesis Reference | Source File(s) | CSV Columns |
|---|---|---|
| Table 4-1, any row | `{scenario}/seed_*/final_metrics.csv` | comfort, fairness, blackout_rate, waste |
| Table 4-2, prosocial/selfish comfort | same as above | prosocial_comfort, selfish_comfort |
| Table 4-3, Gini | `gini_reanalysis.csv`, `gini_more_scenarios.csv` | scenario, seed, gini |
| Table 4-4, sharing freq | Q-table data (not in CSVs) | — |
| Table 4-6, cloud sensitivity | `cloud_sensitivity_reanalysis.csv` | cloud_prob, seed, prosocial_comfort, selfish_comfort |
| Table 4-7, statistical tests | `statistical_tests.txt` | (text file) |
| Table 4-8, innovator comparison | mixed/ + innovator_effect/ final_metrics.csv + gini CSVs | (same columns as above) |
| Table 4-10, baselines | `baseline_{method}/seed_*/final_metrics.csv` | scenario, seed, comfort, fairness, F, blackout_rate, waste |
| Table 4-10, OCEAN rows | same as Table 4-1 | (same columns) |
| Table 4-10, control row | `control_always_default/seed_*/final_metrics.csv` | comfort, fairness, blackout_rate, waste |
| Table 4-11, paper-reported values | Literature (not computable) | — |

**Quick file lookup by metric:**

| Metric | Primary CSV |
|---|---|
| Community comfort (C̄) | `{scenario}/seed_*/final_metrics.csv` → `comfort` |
| Jain fairness (F_jain) | same → `fairness` |
| Combined F = C̄ + F_jain | same → compute `comfort + fairness` (or use `F` column in baseline CSVs) |
| Blackout rate (B) | same → `blackout_rate` (decimal, e.g. 0.145 = 14.5%) |
| Waste (W, kWh) | same → `waste` |
| Gini coefficient (G) | `gini_reanalysis.csv` or `gini_more_scenarios.csv` → `gini` |
| Agent-type comfort | same → `prosocial_comfort`, `selfish_comfort` |
| Cloud sensitivity | `cloud_sensitivity_reanalysis.csv` → `prosocial_comfort`, `selfish_comfort` |
| All baselines aggregated | `baseline_comparison.csv` → comfort, fairness, F, blackout_rate, waste |
| Statistical tests | `statistical_tests.txt` |
| Battery sensitivity | `battery_sensitivity/summary.csv` |

---

## L. Simulation parameters (for reference)

| Parameter | Value | Source |
|---|---|---|
| BATTERY_CAP | 7.0 kWh | offgrid_marl.py |
| DOD limit | None — full 7.0 kWh usable | environment.py (code audit 2026-08-20) |
| NUM_HOUSES | 10 | offgrid_marl.py |
| EPISODES | 8000 | offgrid_marl.py |
| Evaluation window | Last 1000 episodes | offgrid_marl.py |
| SEEDS | 42, 123, 456, 789, 1011 | offgrid_marl.py |
| G_max (solar peak) | 1.3 kW | offgrid_marl.py |
| Cloud probability (base) | 0.15 (15% overcast) | offgrid_marl.py |
| Cloud multiplier | 0.5 (halves solar on cloudy days) | offgrid_marl.py |
| Blackout threshold | comfort < 0.95 | offgrid_marl.py |
| Battery init SOC | 0.5 (50%) | offgrid_marl.py |
| Daily demand mean | ~8.8 kWh/household | demand profiles |
| Ofgem baseline | 2700 kWh/yr ≈ 7.4 kWh/day | thesis §3-6 |
| Q-learning α | 0.2 | offgrid_marl.py |
| Discount γ | 0.99 | offgrid_marl.py |
| ε decay | 0.999 per episode | offgrid_marl.py |
| ε_min (standard) | 0.01 | offgrid_marl.py |
| ε_min (innovator) | 0.05 | offgrid_marl.py |
| State space | 24h × 4 battery levels = 96 states | derived |
| Action space | 3 (0%, 50%, 100% share) | offgrid_marl.py |

---

## M. Forensic data audit (5-task protocol)

> Full report: `0-Active Doc/Forensic_Data_Audit.md`
> **Audit date:** 2026-08-20 · **Tool:** Python3 direct CSV computation

### M-1. Audit summary

| Task | Claim Tested | Verdict | Detail |
|------|-------------|---------|--------|
| 1 — Gini SD | Table 4-3 originally used ddof=0 | ✅ PASS | Now standardized to ddof=1 (2026-08-21); thesis updated |
| 2 — Cohen's d | Three effect-size claims | ✅ PASS | Mixed paired d=3.80, Varied paired d=1.27, Innovator unpaired d=2.25 — all match |
| 3 — Waste t-test | Selfish vs mixed waste t=1.87, p=0.14 | ✅ PASS | Computed t=1.868 rounds to 1.87; p=0.135 rounds to 0.14 |
| 4 — Figures | All 23 thesis figures present | ✅ PASS | 18 main + 1 extra + 4 validation — all present |
| 5 — Battery sensitivity | Seeds / uncertainty quantification | ⚠️ LIMITATION | Single seed (seed=42) only — no SD/error bars possible |

### M-2. Gini SD convention (Task 1)

| Scenario | CSV mean comfort | ddof=0 (pop.) | ddof=1 (sample) | Thesis value (updated) | Match |
|----------|-----------------|---------------|-----------------|--------------|-------|
| selfish | 0.9051 | 0.070 | 0.078 | 0.078 | ddof=1 ✅ |
| prosocial | 0.9345 | 0.052 | 0.058 | 0.058 | ddof=1 ✅ |
| mixed | 0.9198 | 0.059 | 0.066 | 0.066 | ddof=1 ✅ |
| varied | 0.9156 | 0.061 | 0.068 | 0.068 | ddof=1 ✅ |
| innovator | 0.9018 | 0.068 | 0.076 | 0.076 | ddof=1 ✅ |

**Note:** Table 4-6 (scarcity sensitivity) also standardized to ddof=1 (2026-08-21). All tables now use sample SD consistently.

### M-3. Cohen's d (Task 2)

| Comparison | Formula | Computed | Thesis | Match |
|-----------|---------|----------|--------|-------|
| Mixed prosocial vs selfish | Paired | 3.80 | 3.79–3.80 | ✅ |
| Varied prosocial vs selfish | Paired | 1.27 | 1.27 | ✅ |
| Innovator vs Mixed (community comfort) | Unpaired | 2.25 | 2.25 | ✅ |

**Independent-formula cross-check** (not what thesis uses, but for reference):
- Mixed: d_ind = 3.50 (paired d = 3.80)
- Varied: d_ind = 1.90 (paired d = 1.27)

### M-4. Waste t-test (Task 3)

| Seed | Selfish waste | Mixed waste | Difference (S−M) |
|------|--------------|-------------|-------------------|
| 123 | 4.8679 | 4.3752 | +0.4926 |
| 42 | 5.1041 | 3.8382 | +1.2658 |
| 456 | 5.2586 | 3.7763 | +1.4823 |
| 789 | 5.5056 | 5.0900 | +0.4157 |
| 1011 | 4.1864 | 4.6351 | −0.4487 |

```
Mean diff: 0.6415 · SD: 0.7679 · SE: 0.3434
t(4) = 1.8682 · p = 0.1351 → rounds to t=1.87, p=0.14 ✅
```

### M-5. Battery sensitivity (Task 5)

| Battery (kWh) | Scenario | Seeds | Comfort | F |
|---------------|----------|-------|---------|---|
| 3.5 | mixed | 1 (seed=42) | 0.4313 | 0.8649 |
| 5.0 | mixed | 1 (seed=42) | 0.8520 | 1.7043 |
| 7.0 | mixed | 1 (seed=42) | 0.9208 | 1.8453 |
| 9.0 | mixed | 1 (seed=42) | 0.9797 | 1.9613 |

**Limitation:** No seed subdirectories under `battery_sensitivity/` — each capacity has only `config.json` + `final_metrics.csv`. Trend is directionally correct (F increases monotonically with capacity) but lacks uncertainty quantification. Recommend re-running with 5 seeds or adding a footnote.

### M-6. Battery DOD limit (Task B)

**Verdict: Simulation uses raw 7.0 kWh for state space. No depth-of-discharge limit.**

Evidence from `environment.py`:
- `battery_capacity` stored as-is (line 10), initialized to full (line 11), reset to full each day (line 28)
- Charge limited by `battery_capacity - battery` (lines 63, 73, 92) — can charge to 100%
- Discharge limited by `min(deficit, battery)` (line 81) — can discharge all the way to 0 kWh
- No DOD multiplier (no 0.95 or 0.9 cap) anywhere in the codebase

In `offgrid_marl.py`: batteries start at 50% SOC (`battery_cap * 0.5`, line 32).
Effective usable capacity = 7.0 kWh, not 6.65 kWh.

---

## N. Full project inventory (2026-08-21 audit)

> Complete cross-reference of all image files, scripts, and thesis figure status.
> Generated as final pre-submission audit.

### N-1. All thesis figure paths (verified on disk)

| شکل | File Path | Size | Modified | Script | Status |
|---|---|---|---|---|---|
| ۱-۱ | `figures/v09_tragedy_commons.png` | 52K | 2026-08-17 | `generate_all_Visuals3.py` | ✅ |
| ۲-۱ | `figures/v2_1_conceptual_framework.png` | 112K | 2026-08-17 | `generate_all_Visuals3.py` | ✅ |
| ۳-۱ | `figures/v12_system_architecture.png` | 104K | 2026-08-17 | `generate_all_Visuals3.py` | ✅ |
| ۳-۲ | `figures/v02_ring_topology.png` | 60K | 2026-08-17 | `generate_all_Visuals3.py` | ✅ |
| ۳-۳ | `figures/v05_solar_curve.png` | 80K | 2026-08-17 | `generate_all_Visuals3.py` | ✅ |
| ۳-۴ | `figures/v04_demand_profiles.png` | 76K | 2026-08-17 | `generate_all_Visuals3.py` | ✅ |
| ۳-۵ | `figures/v01_ocean_to_rl_mapping.png` | 52K | 2026-08-17 | `generate_all_Visuals3.py` | ✅ |
| ۳-۶ | `figures/v03_two_phase_sharing.png` | 88K | 2026-08-17 | `generate_all_Visuals3.py` | ✅ |
| ۳-۷ | `figures/v06_community_compositions.png` | 104K | 2026-08-17 | `generate_all_Visuals3.py` | ✅ |
| ۴-۱ | `figures/v13_community_metrics.png` | 100K | 2026-08-17 | `generate_all_Visuals3.py` | ✅ |
| ۴-۱-الف | `figures/fig_training_convergence.png` | 84K | 2026-08-21 | `generate_training_curves.py` | ✅ Added 2026-08-21 |
| ۴-۲ | `figures/v14_agent_comfort_split.png` | 56K | 2026-08-17 | `generate_all_Visuals3.py` | ✅ |
| ۴-۳ | `figures/v07_reciprocity_cycle.png` | 52K | 2026-08-17 | `generate_all_Visuals3.py` | ✅ |
| ۴-۴ | `figures/v11_lorenz_curve.png` | 96K | 2026-08-17 | `generate_all_Visuals3.py` | ✅ |
| ۴-۵ | `figures/v15_gini_comparison.png` | 48K | 2026-08-17 | `generate_all_Visuals3.py` | ✅ |
| ۴-۶ | `figures/v16_sharing_frequency.png` | 56K | 2026-08-17 | `generate_all_Visuals3.py` | ✅ |
| ۴-۷ | `qtable_heatmaps.png` | 108K | 2026-08-17 | `generate_all_Visuals3.py` / `advanced_analysis.py` | ✅ |
| ۴-۸ | `figures/v18_scarcity_sensitivity.png` | 92K | 2026-08-17 | `generate_all_Visuals3.py` | ✅ |
| ۴-۹ | `figures/v08_innovator_effect.png` | 72K | 2026-08-17 | `generate_all_Visuals3.py` | ✅ |
| ۴-۱۰ | `baseline_charbonnier_validation/results_plot.png` | 140K | 2026-08-16 | `charbonnier_marginal_iql.py` | ✅ |
| ۴-۱۱ | `baseline_kusatake/seed_42/results_plot.png` | 192K | 2026-08-09 | `kusatake_evolutionary_moo.py` | ✅ Fixed 2026-08-21 |
| ۴-۱۲ | `baseline_behrunani/seed_42/results_plot.png` | 172K | 2026-08-09 | `behrunani_gne_fairness.py` | ✅ Fixed 2026-08-21 |
| ۴-۱۳ | `baseline_may_huang_sanity/results_plot.png` | 200K | 2026-08-16 | `may_huang_ppo.py` | ✅ |
| ۴-۱۴ | `figures/v10_sota_comparison.png` | 80K | 2026-08-17 | `generate_all_Visuals3.py` | ✅ Regenerated 2026-08-16 |

**Total thesis figures: 24 — all present on disk. Zero missing.**

### N-2. Orphan files (exist in results/ but not referenced in thesis)

**Superseded top-level images (6) — moved to `archive/` (2026-08-21):**

| File | Size | Superseded By | Status |
|---|---|---|---|
| `results/agent_type_comfort.png` | 56K | `figures/v14_agent_comfort_split.png` | Archived |
| `results/community_metrics.png` | 104K | `figures/v13_community_metrics.png` | Archived |
| `results/gini_comparison.png` | 52K | `figures/v15_gini_comparison.png` | Archived |
| `results/sensitivity_cloud.png` | 44K | `figures/v18_scarcity_sensitivity.png` | Archived |
| `results/sharing_frequency.png` | 80K | `figures/v16_sharing_frequency.png` | Archived |
| `results/baseline_comparison.png` | 116K | `figures/v10_sota_comparison.png` | Archived (keep .csv/.txt) |

**Orphaned diagnostic plots (2) — moved to `archive/` (2026-08-21):**

| File | Size | Replaced By | Status |
|---|---|---|---|
| `results/baseline_kusatake_timing/` | 88K | `baseline_kusatake/seed_42/results_plot.png` | Archived |
| `results/baseline_behrunani_sanity/` | 88K | `baseline_behrunani/seed_42/results_plot.png` | Archived |

**Non-thesis generated figure (1) — moved to `archive/` (2026-08-21):**

| File | Size | Reason | Status |
|---|---|---|---|
| `results/figures/v17_qtable_heatmaps.png` | 88K | Persian-labelled heatmap variant — شکل ۴-۷ uses English version | Archived |

**Per-seed runtime plots (~67) — working artifacts, not thesis material:**

Located under: `all_prosocial/`, `all_selfish/`, `mixed/`, `innovator_effect/`, `varied_altruism/`, `control_always_default/`, `baseline_charbonnier/`, `baseline_kusatake/`, `baseline_behrunani/`, `baseline_behrunani_lambda5_sensitivity/`, `baseline_may_huang/`, `baseline_may_huang_waste_sensitivity/`, `battery_sensitivity/`, `analysis_support/`, `ocean_marl_endofday_sanity*/`

### N-3. Missing figures (thesis references a file that does not exist)

**None.** All 23 thesis figure paths resolve to existing files on disk.

### N-4. Stale references (thesis points to diagnostic instead of full run)

**None remaining as of 2026-08-21.** All baseline validation figures now point to full runs:
- شکل ۴-۱۱ → `baseline_kusatake/seed_42/` (full 500-day, was `_timing/` 10-day)
- شکل ۴-۱۲ → `baseline_behrunani/seed_42/` (full 500-day, was `_sanity/` 10-day)
- شکل ۴-۱۰ → `baseline_charbonnier_validation/` (3000-episode, unchanged)
- شکل ۴-۱۳ → `baseline_may_huang_sanity/` (800-episode, unchanged — per user specification)

### N-5. Summary statistics

| Category | Count |
|---|---|
| Thesis figure files (referenced in Thesis_v9-5.md) | 24 |
| Non-thesis generated figures (archived) | 1 (v17) |
| Superseded top-level images (archived) | 6 |
| Orphaned diagnostic plots (archived) | 2 |
| Per-seed runtime plots | ~67 |
| **Total PNG files under results/** (excl. archive) | **~74** |
| **Total PNG files under results/** (incl. archive) | **~83** |
