# results/ — Directory Map & Figure Registry

> **Purpose of this file:** A maintenance map that explains every image (and key data artifact) in
> the `results/` tree — what it is, which script generated it, whether the thesis uses it, and what
> to do with it. Read this before deleting, moving, or regenerating anything here.
>
> **Related thesis:** `0-Active Doc/Thesis_v9-3.md` · **Registry of all 23 thesis figures:** Section C.
> **Snapshot date:** Aug 2026 (post figure-integration audit; 2026-08-16 sync: شکل ۲-۱ added,
> v10 rebuilt from real `baseline_comparison.csv` data with Aloor dropped, v14 innovator p-value
> removed to match Table 4-2).

---

## A. Quick numbers

| Group | Count | In thesis? |
|---|---|---|
| Main figures (`results/figures/`, v01–v16, v18 + v2_1) | 18 | ✅ All 18 |
| Q-table heatmaps (`results/qtable_heatmaps.png`) | 1 | ✅ |
| Baseline validation plots (4 sanity/timing runs) | 4 | ✅ All 4 |
| **Thesis figure total** | **23** | **All referenced** |
| Superseded top-level images (→ replaced by v-figures) | 6 | ❌ None |
| Per-seed runtime plots (`*/seed_*/results_plot.png`) | ~67 | ❌ Working artifacts |
| **All image files under results/** | **~95** | — |

---

## B. Directory tree

```
results/
├── figures/                          # MAIN thesis figures — 18, ALL used (do not delete)
│   ├── v01_ocean_to_rl_mapping.png   ├── v10_sota_comparison.png
│   ├── v02_ring_topology.png         ├── v11_lorenz_curve.png
│   ├── v03_two_phase_sharing.png     ├── v12_system_architecture.png
│   ├── v04_demand_profiles.png       ├── v13_community_metrics.png
│   ├── v05_solar_curve.png           ├── v14_agent_comfort_split.png
│   ├── v06_community_compositions.png├── v15_gini_comparison.png
│   ├── v07_reciprocity_cycle.png     ├── v16_sharing_frequency.png
│   ├── v08_innovator_effect.png      ├── v18_scarcity_sensitivity.png
│   ├── v09_tragedy_commons.png       └── v2_1_conceptual_framework.png   # NEW — شکل ۲-۱
│   └── v17_qtable_heatmaps.png        # Persian heatmap variant — NOT a thesis figure
│                                      # (شکل ۴-۷ = top-level results/qtable_heatmaps.png)
├── qtable_heatmaps.png               # USE — شکل ۴-۷ (advanced_analysis.py)
├── agent_type_comfort.png            # DISCARD → superseded by v14
├── community_metrics.png             # DISCARD → superseded by v13
├── gini_comparison.png               # DISCARD → superseded by v15
├── sensitivity_cloud.png             # DISCARD → superseded by v18
├── sharing_frequency.png             # DISCARD → superseded by v16
├── baseline_comparison.png           # DISCARD → superseded by v10 (+ .csv / .txt are the data)
├── baseline_charbonnier_validation/results_plot.png   # USE — شکل ۴-۱۰ (§4-10-1)
├── baseline_kusatake_timing/results_plot.png          # USE — شکل ۴-۱۱ (§4-10-1)
├── baseline_behrunani_sanity/results_plot.png         # USE — شکل ۴-۱۲ (§4-10-1)
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
└── ocean_marl_endofday_sanity{,_community,_community_homogeneous}/results_plot.png
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
| ۴-۲ | figures/v14_agent_comfort_split.png | §4-3 | آسایش عامل‌های نوع‌گرا در مقابل خودخواه | ✅ placed |
| ۴-۳ | figures/v07_reciprocity_cycle.png | §4-3 | چرخه متقابله‌گری در جوامع مختلط | ⚠️ orphan text (see §F) |
| ۴-۴ | figures/v11_lorenz_curve.png | §4-4 | منحنی لورنز — مقایسه مختلط و اثر نوآور | ✅ placed |
| ۴-۵ | figures/v15_gini_comparison.png | §4-4 | ضریب جینی بر اساس سناریو | ⚠️ orphan text (see §F) |
| ۴-۶ | figures/v16_sharing_frequency.png | §4-5 | فراوانی اشتراک بر اساس نوع عامل | ✅ placed |
| ۴-۷ | qtable_heatmaps.png | §4-6 | میانگین مقادیر Q در هر ساعت (نقشه‌های حرارتی) | ✅ placed |
| ۴-۸ | figures/v18_scarcity_sensitivity.png | §4-7 | حساسیت به کمبود منابع (احتمال ابری) | ✅ placed |
| ۴-۹ | figures/v08_innovator_effect.png | §4-9 | مکانیسم اثر نوآور | ✅ placed |
| ۴-۱۰ | baseline_charbonnier_validation/results_plot.png | §4-10-1 | صحت‌سنجی بازتولید چاربونیه | ✅ placed |
| ۴-۱۱ | baseline_kusatake_timing/results_plot.png | §4-10-1 | زمان‌بندی/همگرایی بازتولید کوساتاکه | ✅ placed |
| ۴-۱۲ | baseline_behrunani_sanity/results_plot.png | §4-10-1 | صحت‌سنجی بازتولید به‌رونانی | ✅ placed |
| ۴-۱۳ | baseline_may_huang_sanity/results_plot.png | §4-10-1 | صحت‌سنجی بازتولید می و هوانگ | ✅ placed |
| ۴-۱۴ | figures/v10_sota_comparison.png | §4-10-1 | مقایسه با آخرین دستاوردهای علمی | ✅ regenerated 2026-08-16 (real data, Aloor dropped) |

---

## D. Generation sources (script → output)

| Script | Produces | In thesis? |
|---|---|---|
| `generate_all_Visuals2.py` | `figures/v01…v18, v2_1` (v17 = non-thesis Persian heatmap variant) | ✅ 18/18 thesis figures |
| `advanced_analysis.py` | `results/qtable_heatmaps.png` | ✅ |
| `baseline_comparison.py` | `results/baseline_comparison.png/.csv/.txt` | png superseded by v10; csv/txt are the SOTA data |
| `final_analysis.py` | `gini_comparison.png`, `sharing_frequency.png`, `sensitivity_cloud.png` | ❌ superseded (→v15, v16, v18) |
| `analyze_results.py` | `community_metrics.png`, `agent_type_comfort.png` | ❌ superseded (→v13, v14) |
| `offgrid_marl.py` | per-seed plots under all_prosocial/all_selfish/mixed/innovator_effect/varied_altruism/control_always_default | ❌ working artifacts |
| `ocean_marl_endofday.py` | per-seed plots under ocean_marl_endofday_sanity* | ❌ working artifacts |
| `battery_sensitivity.py` | `battery_sensitivity/batt{3.5,5,7,9}/…` (+ `summary.csv`) | ❌ plots; summary.csv feeds Table 3-1 |
| `support_analysis.py` | `analysis_support/batt05/…`, `analysis_support/qtab/*.npy`, `analysis_support/report.md` | ❌ plots; report.md backs Analysis 1–4 |
| `charbonnier_marginal_iql.py` | `baseline_charbonnier/*` + `_validation/` | validation ✅, 5-seed plots ❌ |
| `kusatake_evolutionary_moo.py` | `baseline_kusatake/*` + `_timing/` | timing ✅, 5-seed plots ❌ |
| `behrunani_gne_fairness.py` | `baseline_behrunani/*` + `_sanity/` + `_lambda5_sensitivity/` | sanity ✅, others ❌ |
| `may_huang_ppo.py` | `baseline_may_huang/*` + `_sanity/` + `_waste_sensitivity/` | sanity ✅, others ❌ |
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
3. **Superseded top-level images (6)** can be archived/deleted without touching the thesis:
   `agent_type_comfort`, `community_metrics`, `gini_comparison`, `sensitivity_cloud`,
   `sharing_frequency`, `baseline_comparison` (keep the `.csv`/`.txt` alongside the last one).
4. **Per-seed runtime plots (~67)** are not thesis material — keep them as raw reproducibility
   evidence, but they can be moved to an `archive/` folder if the tree must be clean.

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

**Keep (thesis):** `figures/v01…v18,v2_1`, `qtable_heatmaps.png`,
`baseline_{charbonnier_validation,kusatake_timing,behrunani_sanity,may_huang_sanity}/results_plot.png`
→ v10 already regenerated 2026-08-16 — **no stale figures remain**
**Archive/discard:** 6 top-level superseded `.png`; all `*/seed_*/results_plot.png`
**Never delete (data):** every `*.csv`, `*.txt`, `*.npy`, `config.json`, `*_summary.csv`
