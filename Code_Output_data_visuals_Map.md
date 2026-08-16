# Code → Output → Data → Visuals Map (OCEAN-MARL Thesis Project)

> **Purpose of this file:** a structural map of every Python script in this repository.
> For each script it documents: (1) what it does for the research, (2) what data files
> it writes/reads, (3) what visual files it produces and their titles, (4) the styling
> system it uses, and (5) where its output is consumed (thesis figure numbers, tables,
> downstream scripts). A future coding agent should use this map to understand the
> codebase before **styling / refactoring / updating visuals** — without changing the
> simulation **logic**, so the thesis document (v9-3) stays consistent.
>
> **Golden rule when editing visuals:** the thesis document
> `0-Active Doc/Thesis_v9-3.md` consumes ONLY the files in `results/figures/vNN_*.png`.
> The older `results/*.png` files produced by analysis scripts are NOT referenced by the
> thesis anymore — they were superseded by the re-renders in `generate_all_Visuals2.py`.
> If you update a figure, update the corresponding `vNN_*` re-render in
> `generate_all_Visuals2.py`, NOT the legacy `results/*.png`.

---

## 1. Repository layout (root = `/Users/hamidasgharian/Desktop/Thesis/sim`)

```
sim/
├── agent.py  environment.py  simulation.py      # earliest core (agent.py & environment.py used; simulation.py is a STUB)
├── offgrid_marl.py                              # ⭐ THE real simulation engine (imported by almost everything)
├── run_experiments.py.py                        # batch driver: 5 scenarios × 5 seeds → results/<scenario>/seed_<seed>/
├── analyze_results.py                           # result aggregator → ۴-۱, ۴-۲ (legacy results/*.png)
├── final_analysis.py                            # Gini / sharing-freq / scarcity → ۴-۵, ۴-۶, ۴-۸ (legacy)
├── advanced_analysis.py                         # Q-table heatmaps + statistical tests → ۴-۷, statistical_tests.txt
├── support_analysis.py                          # discussion/support analyses → analysis_support/ (no plots)
├── charbonnier_marginal_iql.py                  # baseline: Charbonnier 2022 (marginal IQL)
├── may_huang_ppo.py                             # baseline: May & Huang 2023 (independent PPO)
├── kusatake_evolutionary_moo.py                 # baseline: Kusatake 2023 (NSGA-II MOO)
├── behrunani_gne_fairness.py                    # baseline: Behrunani 2023 (GNE game)
├── ocean_marl_endofday.py                       # variant: end-of-day reward OCEAN-MARL (2×2 isolation design)
├── battery_sensitivity.py                       # battery-cap sensitivity sweep
├── baseline_comparison.py                       # unified baseline table/plot + stats
├── gini_cloud_reanalysis.py                     # gini + cloud-sensitivity reanalysis CSVs
├── gini_more_scenarios.py                       # gini for 3 extra scenarios
├── generate_all_Visuals2.py                     # ⭐⭐ THESIS FIGURE GENERATOR (all results/figures/vNN_*.png)
├── t.py                                         # dependency smoke test (junk)
├── results/                                     # all generated data + figures (see §7)
├── Traceability_Package_From_Results/scripts/   # IDENTICAL copies of 5 scripts (advanced_analysis, baseline_comparison,
│                                               #   gini_cloud_reanalysis, gini_more_scenarios, ocean_marl_endofday)
└── 0-Active Doc/Thesis_v9-3.md                  # the thesis document (consumes results/figures/*)
```

**Dependency graph (imports):**

```
run_experiments.py.py ──► offgrid_marl.run_simulation
analyze_results.py     ──► (reads) results/*/seed_*/final_metrics.csv
final_analysis.py      ──► offgrid_marl (run_simulation, PERSONALITIES, DEMAND_PROFILES)
advanced_analysis.py   ──► offgrid_marl + reads final_metrics.csv
support_analysis.py    ──► offgrid_marl (House, Community, QLAgent, run_simulation)
charbonnier / may_huang / kusatake / behrunani ──► offgrid_marl (DEMAND_PROFILES, House, Community)
ocean_marl_endofday.py ──► offgrid_marl + reads results/<scenario>/seed_42/..., baseline_charbonnier_validation/
baseline_comparison.py ──► (reads) all baseline + scenario seed CSVs + sanity reports
gini_cloud_reanalysis / gini_more_scenarios ──► offgrid_marl.run_simulation + validate against saved CSVs
generate_all_Visuals2.py ──► (reads) results/gini_*.csv, cloud_sensitivity_reanalysis.csv,
                             results/analysis_support/{house_comfort/lorenz_curves.npy, qtab/*_q.npy}, seed final_metrics.csv
```

---

## 2. Simulation CORE (the logic that MUST NOT change)

### 2.1 `offgrid_marl.py` — ⭐ THE main simulation engine
- **Role:** everything imports this. Defines personalities, demand profiles, the physical
  environment (house + ring-topology community), the tabular Q-learning agent, the training
  loop, and a 2×2 diagnostic plot.
- **Key constants / classes:**
  - `PERSONALITIES`: `pure_selfish` (w_self=1.0,w_fair=0.0), `individualist` (0.8/0.2),
    `prosocial` (0.5/0.5), `altruistic` (0.2/0.8), `high_openness_innovator` (0.5/0.5, min_eps=0.05).
  - `DEMAND_PROFILES`: `morning`, `evening`, `flat`, `night_owl` (24-h lists).
  - `House` (battery, half-sine solar max 1.3 kW, hourly step, waste/blackout tracking),
    `Community` (ring `{i: [(i+1)%N]}`, `jain_fairness()`), `QLAgent` (state=(hour,battery-bin
    from `state_bins=[0.25,0.5,0.75]`), 3 actions `{0.0,0.5,1.0}`, alpha=0.2, gamma=0.99,
    eps_decay=0.999, min_eps=0.01), reward `w_self·comfort + w_fair·fairness`.
  - `run_simulation(...)`: 10 houses, 8000 episodes, battery 7.0 kWh (start 50%), solar 1.3 kW,
    weather cloud prob 0.15 (cloudy → W=0.5 halves solar).
- **Writes (only when `save_path` given):** `final_metrics.csv`, `config.json`, `results_plot.png`.
- **Styling:** NO `rcParams`. Default matplotlib; named colors `skyblue` (prosocial),
  `coral` (selfish); grid `alpha=0.3`. Figure `(14,10)` 2×2, suptitle `Scenario: {mix}`.

### 2.2 `agent.py` + `environment.py` — earliest core (superseded)
- Clean OOP version of the same ideas: `QLearningAgent` (agent.py) and `House` /
  `EnergyCommunity` (environment.py). Self-contained, no I/O, no plotting.
- **Note:** NOT imported by anything current (offgrid_marl has its own parallel
  `QLAgent`/`House`/`Community`). Keep in sync if you touch them, or mark for deletion.

### 2.3 `simulation.py` — ⚠️ INCOMPLETE STUB (dead code)
- `run_simulation(...)` signature exists but the body is `pass` with comments.
- No I/O, no plotting. Safe to delete or complete — nothing imports it.

### 2.4 `run_experiments.py.py` — batch driver
- Runs `offgrid_marl.run_simulation` for 5 scenarios × 5 seeds `[42,123,456,789,1011]` →
  `results/<scenario>/seed_<seed>/{final_metrics.csv, config.json, results_plot.png}`.
- Scenarios (10 houses each): `all_selfish` (10×pure_selfish), `all_prosocial` (10×prosocial),
  `mixed` (5 pro + 5 self), `varied_altruism` (1 altruistic +3 pro +3 individualist +3 self),
  `innovator_effect` (1 high_openness_innovator +4 pro +3 individualist +2 self).

### 2.5 `t.py` — junk smoke test (prints numpy/pandas versions). Ignore/delete.

---

## 3. Main experiment analysis (thesis Ch. 4 results)

### 3.1 `analyze_results.py` — شکل ۴-۱ & ۴-۲ (LEGACY render)
- **Role:** aggregates the per-seed `final_metrics.csv` → mean±std bar charts + console table.
- **Inputs:** `results/{5 scenarios}/seed_*/final_metrics.csv` (cols comfort, fairness,
  blackout_rate, waste, prosocial_comfort, selfish_comfort).
- **Outputs (legacy):**
  - `results/community_metrics.png` — figsize (16,6), 3 panels, suptitle
    "Community-Level Metrics Across Scenarios" (panels: Community Comfort / Community
    Fairness / Blackout Frequency by Scenario) → thesis **شکل ۴-۱**.
  - `results/agent_type_comfort.png` — (10,6), "Comfort by Personality Type (Mixed
    Communities)" → thesis **شکل ۴-۲**.
- **Styling:** no rcParams; hardcoded hex palette
  `['#e74c3c','#2ecc71','#3498db','#9b59b6','#f39c12']` (red/green/blue/purple/orange) for
  scenario bars; prosocial `#3498db`, selfish `#e74c3c`; alpha 0.8–0.85, gray edges,
  capsize 6–8.
- **Thesis consumption:** superseded by `v13_community_metrics.png` / `v14_agent_comfort_split.png`.

### 3.2 `final_analysis.py` — شکل ۴-۵, ۴-۶, ۴-۸ (LEGACY render)
- **Role:** re-runs sims in-process (no file I/O) to compute (1) per-episode Gini of comfort,
  (2) learned sharing frequency from Q-tables, (3) cloud-probability (scarcity) sensitivity.
- **Outputs (legacy):** `results/gini_comparison.png` (thesis شکل **۴-۵**), `results/sharing_frequency.png`
  (thesis شکل **۴-۶**), `results/sensitivity_cloud.png` (thesis شکل **۴-۸**).
- **Styling:** no rcParams; same 5-hex scenario palette; 8-bar sharing-freq palette
  `[red,green,blue,red,blue,red,purple,red]`; titles listed in §7.
- **Key function:** `gini(x)` — canonical Gini implementation (replicated in the gini re-analysis scripts).

### 3.3 `advanced_analysis.py` — شکل ۴-۷ + statistical tests
- **Role:** part 1 trains agents per scenario (seed 42) and plots average Q-value heatmaps
  (hour × action); part 2 loads all seed `final_metrics.csv` and runs 5 tests.
- **Outputs:**
  - `results/qtable_heatmaps.png` — (24,10), 2×5 grid, `cmap='YlOrRd'`, suptitle
    "Q-table Heatmaps: Average Action Values by Hour" → thesis **شکل ۴-۷**. NOTE: since
    2026-08-16 `generate_all_Visuals2.py` also emits `results/figures/v17_qtable_heatmaps.png`
    (Persian-labelled variant, different agent selection) — it is NOT a thesis figure.
  - `results/statistical_tests.txt` — text report of the 5 tests.
- **Statistical tests (exact):** independent t-test all-selfish vs all-prosocial comfort
  (t=0.845, p=0.4229 ns); paired t-test mixed prosocial vs selfish (t=8.487, p=0.0011 SIG);
  paired t-test varied-altruism pro vs self (t=2.834, p=0.0472 SIG); independent t-test
  innovator vs mixed community (t=-3.562, p=0.0074 SIG); one-way ANOVA on comfort across
  5 scenarios (F=3.362, p=0.0293 SIG).

### 3.4 `support_analysis.py` — Discussion/support artifacts (no plots)
- **Role:** diagnoses the "sharing does not significantly raise comfort" baseline issue for
  the Ch.4 Discussion: battery-capacity sensitivity (0.5 vs 0.7 kWh), Q-value distribution,
  share-action frequency, w̄_fair–waste correlation.
- **Outputs (data only):**
  - `results/analysis_support/batt05/mixed/seed_*/{final_metrics.csv, config.json, results_plot.png}`
    (battery_cap=5.0 mixed runs).
  - `results/analysis_support/qtab/mixed_q.npy`, `qtab/selfish_q.npy` — shape
    (5 seeds, 10 agents, 24 h, 4 bins, 3 actions).
  - `results/analysis_support/wfair_waste_scatter.csv` — cols `scenario, seed, wbar_fair, waste_reduction_kwh` (25 rows).
  - Console tables + `report.md`; paired t-tests (mixed vs no-sharing: 0.5 kWh comfort
    t=0.693 p=0.5265 ns; waste t=-16.18 p=0.0001 SIG; 0.7 kWh comfort t=-0.988 p=0.379 ns;
    waste t=-18.68 p<0.0001 SIG); Pearson w̄_fair–waste (scenario n=5 r=0.6114 p=0.2732;
    pooled n=25 r=0.2836 p=0.1695).

---

## 4. Published-baseline reproductions (all: no rcParams, default styling, dpi=150)

All four share an **identical `final_metrics.csv` schema** for drop-in ANOVA compatibility:
`scenario, seed, comfort, fairness, F, blackout_rate, waste, prosocial_comfort, selfish_comfort`
(prosocial/selfish both = overall mean — agents are role-free/neutral). All write
`config.json` + a per-seed `results_plot.png`. None read any CSV.

| File | Baseline (paper) | Method | Output dirs | Extra files | results_plot.png |
|---|---|---|---|---|---|
| `charbonnier_marginal_iql.py` | Charbonnier 2022 | role-free **marginal Independent Q-Learning**, end-of-day counterfactual reward `F_end − F_end^default`, hysteretic update | `results/baseline_charbonnier/seed_{s}/` + `results/baseline_charbonnier_validation/` (--validation) | `validation_report.txt` | figsize (15,4) 1×3: Community Performance / Blackout Rate (500-ep) / Mean Agent Reward (200-ep); suptitle `Baseline Charbonnier Marginal IQL (seed {s})` |
| `may_huang_ppo.py` | May & Huang 2023 | **independent PPO** per house (2×32 MLP, GAE-λ, clip ε=0.2, 4 epochs, entropy 0.01); rewards `cf` or `cf_waste`; `--sanity` mode | `results/baseline_may_huang/seed_{s}/` (+`_sanity`, `_waste_sensitivity`) | `sanity_report.txt` | (13,9) 2×2: Community Performance / Blackout Rate / PPO Losses / Entropy & KL (dashed ln(3) ref) |
| `kusatake_evolutionary_moo.py` | Kusatake 2023 | **NSGA-II (pymoo)** per day, 240-var action plan, obj F1=mean comfort, F2=std comfort; sunny-day saturation caveat | `results/baseline_kusatake/seed_{s}/` + `_timing` | `weather_split_metrics.csv` (cols `weather, days, comfort, fairness, F, blackout_rate, waste, share_frac`), `timing_report.txt` | (15,4) 1×3: Community Performance / Daily Waste & Blackout / Chosen Sharing & Front Size |
| `behrunani_gne_fairness.py` | Behrunani 2023 | **GNE** per-hour best-response game (projected gradient, central finite-diff), `L_i=unmet+wasted`, penalty `λ(ΔL_i−meanΔL)²`; `--sanity` λ=1 vs λ=0 | `results/baseline_behrunani/seed_{s}/` (+`_sanity`, `_lambda5_sensitivity`) | `sanity_report.txt` | (15,4) 1×3: Community Performance / Daily Waste & Chosen Sharing / Game Convergence & Signal |

---

## 5. Re-analysis / sanity / sensitivity scripts

### 5.1 `ocean_marl_endofday.py` — end-of-day reward variant (2×2 isolation design)
- **Role:** main experiment with **end-of-day counterfactual reward** (re-run hours t..23 with
  agent i forced to 0%), completing the objective×horizon 2×2 design. Objectives:
  `'personality'` (w_self·C + w_fair·F) vs `'community'` (Charbonnier's mean(C)+F);
  `--homogeneous` gives a role-free mirror env. Cells: A (per-step personality), B (per-step
  community), C (Charbonnier), D (end-of-day personality), D2 (end-of-day community homogeneous).
- **Outputs:** flat sanity dirs `results/ocean_marl_endofday_sanity{, _community, _community_homogeneous}/
  {final_metrics.csv, config.json, sanity_report.txt, results_plot.png}`; full runs
  `results/<scenario>_endofday/seed_<s>/...`.
- **`final_metrics.csv` cols:** `scenario, seed, comfort, fairness, F, blackout_rate, waste,
  prosocial_comfort, selfish_comfort` (pro/self = overall mean).
- **Inputs read:** main + control + Charbonnier seed_42 CSVs, `baseline_charbonnier_validation/validation_report.txt`.
- **Styling:** via `offgrid_marl.plot_results` (2×2, skyblue/coral); suptitle `OCEAN-MARL end-of-day ({scenario}, seed {seed})`.

### 5.2 `battery_sensitivity.py` — battery-cap sweep
- **Role:** battery sizes `[3.5,5.0,7.0,9.0]` kWh × (always-default control + mixed Q-learning), seed 42.
- **Outputs:** `results/battery_sensitivity/summary.csv` (cols `battery_cap, run, comfort,
  fairness, F, blackout_rate, waste`), per-run `batt<size>/{always_default,mixed}/final_metrics.csv` + config.json.
- **Note:** the control writes `scenario, battery_cap, ...`; the mixed run (via offgrid_marl) does NOT
  have a `scenario` column — reconciled only in `summary.csv`.

### 5.3 `baseline_comparison.py` — unified comparison + stats
- **Role:** aggregates 5 main scenarios + 4 baselines + always-default control across 5 seeds;
  builds the 2×2 isolation block from sanity reports; ANOVA + paired t-tests; writes CSV/TXT/PNG.
- **Outputs:** `results/baseline_comparison.csv` (cols `method, seed, comfort, fairness, F,
  blackout_rate, waste`), `baseline_comparison.txt`, `baseline_comparison.png` (figsize (17,5.5),
  1×3 panels Composite F / Community comfort / Energy waste).
- **Styling:** no rcParams; **hex palette `#2ecc71` (green = baselines+control), `#3498db`
  (blue = main OCEAN-MARL)**; error bars capsize 5, alpha 0.85, gray edges, xticks rotated 30°.
- **Stats:** one-way ANOVA on F/comfort/waste; paired t-tests (seed-matched) of each method vs
  always-default (F, comfort); headline paired t-tests vs OCEAN-MARL mixed (F).

### 5.4 `gini_cloud_reanalysis.py` — `--task {gini,cloud}`
- **Role:** (gini) re-runs mixed + innovator_effect (5 seeds) and recomputes per-episode Gini
  (last 1000 eps), validating each run against saved `final_metrics.csv`; (cloud) mixed at cloud
  probs 0.15/0.25/0.35 × 5 seeds.
- **Outputs:** `results/gini_reanalysis.csv` (cols `scenario, seed, gini`),
  `results/cloud_sensitivity_reanalysis.csv` (cols `cloud_prob, seed, prosocial_comfort, selfish_comfort`).
- **Stats (console only):** paired t-test + Cohen's d (gini); Welch + Student t-tests per cloud prob.
- **Feeds:** `generate_all_Visuals2.py` v15 (gini) and v18 (scarcity).

### 5.5 `gini_more_scenarios.py` — gini for the other 3 scenarios
- **Role:** same as above but for `all_selfish`, `all_prosocial`, `varied_altruism` (15 rows total).
- **Outputs:** `results/gini_more_scenarios.csv` (cols `scenario, seed, gini`). Feeds v15.

---

## 6. ⭐⭐ `generate_all_Visuals2.py` — THE THESIS FIGURE GENERATOR

The single most important file for visuals. It re-renders **every** thesis figure into
`results/figures/vNN_*.png` (150 dpi, white background). It has two families:

### 6.1 Shared styling system (CANONICAL — replicate this)
- **Palette** `C = {'red':'#e74c3c','green':'#2ecc71','blue':'#3498db','purple':'#9b59b6',
  'orange':'#f39c12','yellow':'#f1c40f','dark':'#2c3e50','grey':'#7f8c8d','teal':'#1abc9c'}`
- **Global defaults:** `font.family='sans-serif'`, `font.sans-serif=['Helvetica','Arial','DejaVu Sans']`,
  `font.size=10`, `axes.titlesize=12`, `figure.dpi=150`.
- **Helpers:** `_box(cx,cy,w,h,text,color,fs,fc)` → FancyBboxPatch round box (fc='tint' = colored
  border + 15% tint fill + colored bold text); `_arrow(x1,y1,x2,y2,color,lw)` → straight arrow;
  `_load_data()` → dict of DataFrames from all `results/<scenario>/seed_*/final_metrics.csv`.
- **Persian (Farsi) text pipeline (only for figures ۲-۱, ۳-۱, ۳-۲, ۳-۵, ۳-۶, ۳-۷, ۴-۳, ۴-۹):**
  `arabic_reshaper.reshape()` + `bidi.algorithm.get_display()` inside helper `fa(s)`, with
  `plt.rc_context({'font.family': ['Geeza Pro','DejaVu Sans','Arial Unicode MS']})`.
  **Rule:** never mix mathtext `$...$` into a `fa()`-shaped string — render math in its own
  `ax.text()` run; avoid `=` inside mathtext.
- **Data-driven figures** (v04, v05, v10, v11, v13–v16, v18) use the `C` palette, `alpha≈0.85`,
  gray edges, `grid(alpha=0.3)`, bold titles, error bars `capsize=6`, value labels on bars.
  Highlighted bars (e.g., innovator) get `edgecolor=C['dark']` + thicker linewidth.

### 6.2 Per-figure table (vNN → thesis figure → style family → data source)

| File | Thesis fig | Type | Content / title | Data source |
|---|---|---|---|---|
| `v01_ocean_to_rl_mapping.png` | شکل ۳-۵ | schematic (Persian) | OCEAN traits → RL params (Openness→ε_min, Agreeableness→w_fair; others held at mean) | none |
| `v02_ring_topology.png` | شکل ۳-۲ | schematic (Persian) | 10-house ring, 2 neighbors each | none |
| `v03_two_phase_sharing.png` | شکل ۳-۶ | schematic (Persian) | Phase-1 local / Phase-2 sharing flow | none |
| `v04_demand_profiles.png` | شکل ۳-۴ | data (line) | "The Four Hourly Demand Profile Types" (Morning/Evening/Flat/Night Owl) | in-code profile lists |
| `v05_solar_curve.png` | شکل ۳-۳ | data (line/fill) | "Half-Sine Solar Irradiance Model", Eq. 3-1, clear vs cloudy | analytic half-sine |
| `v06_community_compositions.png` | شکل ۳-۷ | schematic (Persian) | 5 scenario compositions (color dots) | scenario lists |
| `v07_reciprocity_cycle.png` | شکل ۴-۳ | schematic (Persian) | 4-node reciprocity cycle + virtuous/vicious labels | none |
| `v08_innovator_effect.png` | شکل ۴-۹ | schematic (Persian) | Innovator mechanism = **unpredictability** (not reduced sharing); no numbers | none |
| `v09_tragedy_commons.png` | شکل ۱-۱ | schematic (Persian) | Tragedy-of-commons ↔ energy-sharing analogy (Hardin 1968) | none |
| `v10_sota_comparison.png` | شکل ۴-۱۴ | data (grouped bars) | "Comparison with State-of-the-Art Energy MARL Studies" (Comfort + Jain) | `baseline_comparison.csv` (real 5-seed data; rebuilt 2026-08-16) |
| `v11_lorenz_curve.png` | شکل ۴-۴ | data (lines+fill) | "Lorenz Curves — Mixed vs. Innovator Effect" | `analysis_support/house_comfort/lorenz_curves.npy` |
| `v12_system_architecture.png` | شکل ۳-۱ | schematic (Persian) | 10-block simulation loop (env + learning columns, h<23 loop, next-episode loop) | none |
| `v13_community_metrics.png` | شکل ۴-۱ | data (2×2 bars) | Community-Level Metrics (Comfort, Jain, Blackout %, Waste) across 5 scenarios | seed `final_metrics.csv` |
| `v14_agent_comfort_split.png` | شکل ۴-۲ | data (paired bars) | Prosocial vs Selfish comfort in mixed-type communities | seed `final_metrics.csv` |
| `v15_gini_comparison.png` | شکل ۴-۵ | data (bars) | "Gini Coefficient by Scenario" (+p annotation) | `gini_reanalysis.csv` + `gini_more_scenarios.csv` |
| `v16_sharing_frequency.png` | شکل ۴-۶ | data (bars) | Proportion of Q-table states where greedy=share (8 groups, mean ~13.1%) | `analysis_support/qtab/*_q.npy` |
| `v18_scarcity_sensitivity.png` | شکل ۴-۸ | data (errorbar) | Prosocial vs Selfish comfort vs cloudy-day probability | `cloud_sensitivity_reanalysis.csv` |
| `v2_1_conceptual_framework.png` | **شکل ۲-۱ (NEW)** | schematic (Persian) | 3-level personality-adjusted coordination model | none |

> Figure numbering above is taken verbatim from the CURRENT `فهرست اشکال` in
> `0-Active Doc/Thesis_v9-3.md` (lines ~305–327). The Q-table heatmap maps to **شکل ۴-۷**
> (`results/qtable_heatmaps.png` from `advanced_analysis.py`). Since 2026-08-16
> `generate_all_Visuals2.py` also renders `results/figures/v17_qtable_heatmaps.png`
> (Persian-labelled variant, different agent selection) — a working artifact, NOT the thesis figure.

---

## 7. Data inventory (`results/`)

### 7.1 `final_metrics.csv` — the canonical per-run metric file
Written by `offgrid_marl.run_simulation` (main), `ocean_marl_endofday`, `battery_sensitivity`
(control variant), and all 4 baseline scripts.
- **Main/offgrid schema:** `seed, comfort, fairness, blackout_rate, waste, prosocial_comfort, selfish_comfort`
- **Baselines/endofday schema:** `scenario, seed, comfort, fairness, F, blackout_rate, waste, prosocial_comfort, selfish_comfort`
- All = mean of the **last 1,000 episodes**; `prosocial/selfish_comfort` = first/last half of
  houses (main) or overall mean (baselines, role-free).

### 7.2 `config.json` (per run)
Main: `personality_mix, num_houses, episodes, battery_cap, solar_max, seed`.
Endofday: `scenario, algorithm, objective, personality_mix, reward, update, num_houses, episodes, battery_cap, solar_max, weather_cloud_prob, seed`.

### 7.3 Aggregated CSVs (inputs to `generate_all_Visuals2.py`)
| File | Columns | Produced by |
|---|---|---|
| `results/gini_reanalysis.csv` | scenario, seed, gini | gini_cloud_reanalysis.py |
| `results/gini_more_scenarios.csv` | scenario, seed, gini | gini_more_scenarios.py |
| `results/cloud_sensitivity_reanalysis.csv` | cloud_prob, seed, prosocial_comfort, selfish_comfort | gini_cloud_reanalysis.py |
| `results/baseline_comparison.csv` | method, seed, comfort, fairness, F, blackout_rate, waste | baseline_comparison.py |
| `results/analysis_support/wfair_waste_scatter.csv` | scenario, seed, wbar_fair, waste_reduction_kwh | support_analysis.py |
| `results/battery_sensitivity/summary.csv` | battery_cap, run, comfort, fairness, F, blackout_rate, waste | battery_sensitivity.py |
| `results/baseline_kusatake/seed_*/weather_split_metrics.csv` | weather, days, comfort, fairness, F, blackout_rate, waste, share_frac | kusatake_evolutionary_moo.py |

### 7.4 .npy support arrays
- `results/analysis_support/qtab/{all_selfish,all_prosocial,mixed,varied_altruism,innovator_effect,selfish}_q.npy` — (5 seeds, 10 agents, 24 h, 4 bins, 3 actions)
- `results/analysis_support/house_comfort/lorenz_curves.npy` — dict with `mixed`, `innovator_effect` curves

### 7.5 Text reports
`results/statistical_tests.txt`, `results/baseline_comparison.txt`, `results/analysis_support/report.md`,
`results/baseline_charbonnier_validation/validation_report.txt`,
`results/baseline_may_huang_sanity/sanity_report.txt`, `results/baseline_kusatake_timing/timing_report.txt`,
`results/baseline_behrunani_sanity/sanity_report.txt`,
`results/ocean_marl_endofday_sanity*/sanity_report.txt`.

### 7.6 Output directory tree (key folders)
```
results/
├── all_selfish | all_prosocial | mixed | varied_altruism | innovator_effect   /seed_{42,123,456,789,1011}/
├── control_always_default/seed_{s}/          (0% sharing control, 0.7 kWh)
├── baseline_charbonnier{,_validation}/
├── baseline_may_huang{,_sanity,_waste_sensitivity}/
├── baseline_kusatake{,_timing}/
├── baseline_behrunani{,_sanity,_lambda5_sensitivity}/
├── ocean_marl_endofday_sanity{, _community, _community_homogeneous}/
├── battery_sensitivity/batt{3.5,5,7,9}/{always_default,mixed}/
├── analysis_support/{batt05,qtab,house_comfort,report.md,wfair_waste_scatter.csv}
├── figures/v01…v18 + v2_1 (THE thesis figures)        ← ← consumer: Thesis_v9-3.md
├── gini_reanalysis.csv  gini_more_scenarios.csv  cloud_sensitivity_reanalysis.csv
├── baseline_comparison.csv/.txt/.png  statistical_tests.txt  qtable_heatmaps.png
├── community_metrics.png  agent_type_comfort.png  gini_comparison.png
├── sharing_frequency.png  sensitivity_cloud.png  Result_Help.md
```

---

## 8. Visual style families (for systematic styling)

There are effectively **three visual generations**, with inconsistent styling:

1. **Legacy per-run diagnostics** (`offgrid_marl.plot_results`, baseline `results_plot.png`,
   endofday `results_plot.png`): default matplotlib, named colors `skyblue`/`coral`, NO rcParams,
   NO palette. These are training diagnostics only — NOT thesis figures.
2. **Legacy analysis PNGs** (`results/community_metrics.png`, `agent_type_comfort.png`,
   `gini_comparison.png`, `sharing_frequency.png`, `sensitivity_cloud.png`,
   `qtable_heatmaps.png`, `baseline_comparison.png`): hardcoded 5-hex palette
   (`#e74c3c,#2ecc71,#3498db,#9b59b6,#f39c12`), no rcParams. **Superseded** by vNN re-renders.
3. **⭐ Canonical thesis style** (`generate_all_Visuals2.py` → `results/figures/vNN_*.png`):
   the `C` palette above, `rcParams` defaults, round FancyBboxPatch schematic boxes,
   `alpha≈0.85` bars with gray edges, grid `alpha=0.3`, bold titles, dpi 150, and (for the
   8 Persian figures) the `fa()` shaping pipeline with `Geeza Pro/DejaVu Sans`.

**Optimization guidance for a styling agent:**
- Standardize on the `C` palette + rcParams block everywhere (target: all three generations).
- Keep schematic vs data styles distinct (schematic = axis-off FancyBboxPatch + arrows;
  data = standard axes, grid, error bars).
- Persian figures must always go through `fa()` + `rc_context(FA_FONTS)`; never combine
  `$...$` math inside shaped strings.
- If you regenerate a legacy `results/*.png`, also update its `vNN_*` twin so the thesis stays consistent.
- Do NOT renumber thesis figures without checking `فهرست اشکال` in `Thesis_v9-3.md`.

---

## 9. Quick reference — script → thesis figure / output

| Script | Writes (data) | Writes (visuals) | Thesis fig(s) | Inputs |
|---|---|---|---|---|
| offgrid_marl.py | final_metrics.csv, config.json | results_plot.png (diag) | (feeds all) | — |
| run_experiments.py.py | (via offgrid_marl) | — | — | — |
| analyze_results.py | — | community_metrics.png, agent_type_comfort.png | ۴-۱, ۴-۲ (legacy) | seed CSVs |
| final_analysis.py | — | gini_comparison.png, sharing_frequency.png, sensitivity_cloud.png | ۴-۵, ۴-۶, ۴-۸ (legacy) | re-runs sims |
| advanced_analysis.py | statistical_tests.txt | qtable_heatmaps.png | ۴-۷ (v17_* variant is a non-thesis working artifact) | seed CSVs |
| support_analysis.py | batt05 CSVs, qtab/*.npy, wfair_waste_scatter.csv | — | (Discussion) | seed CSVs |
| charbonnier_marginal_iql.py | baseline_charbonnier seed CSVs | results_plot.png | (Ch.4 validation) | — |
| may_huang_ppo.py | baseline_may_huang seed CSVs | results_plot.png | (Ch.4 validation) | — |
| kusatake_evolutionary_moo.py | baseline_kusatake seed CSVs + weather_split | results_plot.png | (Ch.4 validation) | — |
| behrunani_gne_fairness.py | baseline_behrunani seed CSVs | results_plot.png | (Ch.4 validation) | — |
| ocean_marl_endofday.py | *_endofday CSVs, sanity reports | results_plot.png | (2×2 isolation) | main/control/Charb CSVs |
| battery_sensitivity.py | battery_sensitivity/*.csv | — | (robustness) | batt mixed CSVs |
| baseline_comparison.py | baseline_comparison.csv/.txt | baseline_comparison.png | (Ch.4 summary) | all seed CSVs + sanity reports |
| gini_cloud_reanalysis.py | gini_reanalysis.csv, cloud_sensitivity_reanalysis.csv | — | feeds v15/v18 | seed CSVs (validate) |
| gini_more_scenarios.py | gini_more_scenarios.csv | — | feeds v15 | seed CSVs (validate) |
| **generate_all_Visuals2.py** | — | **figures/v01…v18, v2_1** | **ALL thesis figures** | gini/cloud CSVs, qtab/*.npy, lorenz_curves.npy, seed CSVs |

---

## 10. Files NOT part of the simulation pipeline
- `t.py` — dependency smoke test (junk).
- `HamidOutput/DocX Converter/*.py` — Markdown→DOCX thesis converters (irrelevant to sim).
- `Traceability_Package_From_Results/scripts/` — verified **byte-identical copies** of the 5 root
  scripts (advanced_analysis, baseline_comparison, gini_cloud_reanalysis, gini_more_scenarios,
  ocean_marl_endofday). If you edit the root ones, decide whether to mirror or mark stale.
- `simulation.py` — incomplete stub (dead code).
- `agent.py` / `environment.py` — superseded clean-OOP versions; nothing imports them.

---

*Last updated: 2026-08-16. Generated from direct source inspection. All CSV column names,
figure titles, and hex colors verified against the actual scripts and on-disk outputs.*
