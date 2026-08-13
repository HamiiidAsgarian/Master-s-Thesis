# Support Analyses — Baseline-Performance Issue (Discussion)

All runs: 10 houses, PV 1.3 kWp, cloud p=0.15, 5 seeds {42,123,456,789,1011},
8000 episodes, last-1000 eval window. `0.5 kWh` = battery_cap 5.0, `0.7 kWh` = 7.0.

## Analysis 1 — Battery Capacity Sensitivity (0.5 vs 0.7 kWh)

| Metric | 0.5 kWh Mixed (mean ± SD) | 0.5 kWh No-Sharing | 0.7 kWh Mixed (Table 4-1) | 0.7 kWh No-Sharing |
|---|---|---|---|---|
| Mean Community Comfort | 0.8568 ± 0.0149 | 0.8498 ± 0.0103 | 0.9198 ± 0.0075 | 0.9249 ± 0.0051 |
| Jain's Fairness | 0.8580 ± 0.0157 | 0.8498 ± 0.0103 | 0.9234 ± 0.0077 | 0.9249 ± 0.0051 |
| Energy Waste (kWh/day) | 8.72 ± 1.14 | 17.32 ± 0.21 | 4.34 ± 0.55 | 8.82 ± 0.11 |
| Blackout Rate (%) | 14.58 ± 1.29 | 15.02 ± 1.03 | 14.52 ± 1.37 | 15.02 ± 1.03 |

Paired t-test, mixed vs no-sharing (seed-matched):

| Battery | Metric | t | p | sig |
|---|---|---|---|---|
| 0.5 kWh | comfort | +0.693 | 0.5265 | ns |
| 0.5 kWh | waste | −16.18 | 0.0001 | SIG |
| 0.7 kWh | comfort | −0.988 | 0.3790 | ns |
| 0.7 kWh | waste | −18.68 | <0.0001 | SIG |

**Interpretation:** The hypothesized "0.5 kWh shows improvement, 0.7 kWh does not"
pattern is NOT supported for comfort — the comfort gain over the no-sharing baseline
is non-significant at BOTH battery sizes (0.5 kWh: +0.007, p=0.53; 0.7 kWh: −0.005,
p=0.38). Waste reduction over no-sharing, by contrast, is large and significant at
BOTH sizes (roughly halved). So the baseline-performance issue (sharing does not
raise comfort significantly) is robust to battery capacity, while waste reduction is
robust across capacities.

## Analysis 2 — Q-Value Distribution (mixed vs all-selfish proxy for no-sharing)

| Agent group | Mean Q | Q variance | States where greedy = share (%) |
|---|---|---|---|
| Mixed (prosocial agents) | 3.9344 | 23.057 | 54.5 |
| Mixed (selfish agents) | 3.8066 | 22.760 | 54.0 |
| All-selfish baseline | 3.8637 | 22.894 | 52.0 |

States where greedy action differs vs all-selfish baseline:
- mixed-prosocial vs baseline: **6.9%**
- mixed-selfish vs baseline: **5.4%**

**Interpretation:** Despite the personality difference, prosocial and selfish agents
learn nearly identical Q-distributions (mean Q ~3.9, variance ~23 in all groups) and
diverge from the no-sharing proxy policy in only ~5–7% of the 96 states. This is the
mechanistic reason for the baseline-performance issue: the per-step reward signal
produces little policy differentiation, so the mixed community behaves almost like a
selfish/no-sharing one.

## Analysis 3 — Share-Action Frequency (mixed vs baselines)

| Metric | Mixed | All-selfish | No-sharing (0%) |
|---|---|---|---|
| Greedy action = share (states, %) | 54.5 | 52.0 | 0.0 |
| Actual sharing occurred (time steps, %) | 18.2 | 18.0 | 0.0 |
| Exportable surplus available (time steps, %) | 37.5 | 37.5 | 37.5 |

**Interpretation:** Although the greedy policy prefers sharing in over half of the
states, actual sharing is realized in only ~18% of agent time-steps (about half of the
37.5% of steps with exportable surplus). Mixed and all-selfish show virtually
identical sharing behavior (18.2% vs 18.0%), again consistent with the flat
Q-differentiation finding — sharing is frequent enough to halve waste, but not enough
to move community comfort significantly.

## Analysis 4 — Correlation: w̄_fair vs Waste Reduction

| Scenario | w̄_fair | Mean waste red. (kWh/day) | Per-seed red. |
|---|---|---|---|
| all_selfish | 0.000 | 3.837 | 3.63, 3.85, 3.61, 3.31, 4.79 |
| all_prosocial | 0.500 | 4.408 | 3.49, 3.93, 4.18, 5.46, 4.98 |
| mixed | 0.250 | 4.478 | 4.89, 4.34, 5.09, 3.72, 4.34 |
| varied_altruism | 0.290 | 3.864 | 4.09, 3.58, 4.15, 4.35, 3.16 |
| innovator_effect | 0.310 | 4.119 | 3.75, 3.75, 4.18, 4.43, 4.48 |

- Scenario-level (n=5): Pearson **r = 0.6114, p = 0.2732**
- Per-seed pooled (n=25): Pearson **r = 0.2836, p = 0.1695**

**Interpretation:** w̄_fair and waste reduction are positively but NOT significantly
correlated at scenario level (r=0.61, p=0.27, n=5) or per-seed (r=0.28, p=0.17, n=25).
The direction is consistent with the thesis (more prosocial weight → lower waste) but
is not statistically significant; even the all-selfish community halves waste, so
waste reduction is only weakly personality-driven.

---
Artifacts: `results/analysis_support/` — `batt05/` (5-seed 0.5 kWh mixed + no-sharing
metrics), `qtab/mixed_q.npy`, `qtab/selfish_q.npy`, `wfair_waste_scatter.csv`.
