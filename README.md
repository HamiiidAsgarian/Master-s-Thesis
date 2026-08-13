# Smart Neighborhood Energy Sharing MARL Simulation

## What It Is

A **Multi-Agent Reinforcement Learning (MARL)** simulation of a smart neighborhood micro-grid where houses (agents) decide whether to share surplus solar energy with neighbours. Each agent follows a fixed personality profile (selfish, prosocial, altruistic, ...) that shapes its reward function, enabling the study of emergent fairness and efficiency trade‑offs under resource scarcity.

The project also implements **four literature baselines** (Charbonnier marginal-IQL, Kusatake NSGA-II, Behrunani GNE, May & Huang PPO), an **always-default control**, a **battery-capacity sensitivity scan**, and an **end-of-day counterfactual reward variant** used to isolate *why* the main approach underperforms doing-nothing on comfort/fairness while still delivering large waste reductions.

## How It Works

### Physical Layer

- **10 houses** on a ring topology, each can share surplus with one designated neighbour.
- **Solar generation**: half-sine curve from 6 AM–6 PM, peak 1.3 kW (clear day); cloudy days (15% probability) halve output.
- **Demand profiles**: 4 types (morning, evening, flat, night-owl), ~8.8 kWh/day total.
- **Battery**: 7.0 kWh capacity, starts at 50% each day.

### Agent Layer (Independent Tabular Q-Learning)

- **State**: (hour 0–23, discretised battery level 0–3).
- **Actions**: share 0%, 50%, or 100% of net surplus.
- **Reward**: `w_self * own_comfort + w_fair * Jain's Fairness Index`.
- **Personality types**: `pure_selfish` (1.0, 0.0), `individualist` (0.8, 0.2), `prosocial` (0.5, 0.5), `altruistic` (0.2, 0.8), `high_openness_innovator` (0.5, 0.5, min-eps 0.05). The weights correspond to Big Five coordinates (high/low agreeableness, openness, etc.).
- **Learning**: ε-greedy (ε decays 1.0→0.01), α=0.2, γ=0.99, optimistic Q-init.

### Community Layer

- **Energy flow**: generation → own demand → battery storage → surplus export to neighbour.
- **Fairness metric**: Jain's fairness index of demand-met fractions across houses.
- **Tracking**: comfort, blackout rate, waste, Gini coefficient, sharing frequency from learned Q-tables.

## Experiments

### Main scenarios (5 × 5 seeds, 8000 episodes)

| Scenario         | Composition                                                 |
| ---------------- | ----------------------------------------------------------- |
| All Selfish      | 10 × pure_selfish                                           |
| All Prosocial    | 10 × prosocial                                              |
| Mixed            | 5 prosocial + 5 selfish                                     |
| Varied Altruism  | 1 altruistic, 3 prosocial, 3 individualist, 3 selfish       |
| Innovator Effect | 1 high-O innovator, 4 prosocial, 3 individualist, 2 selfish |

### Baselines, control, and sensitivity (identical environment, matched seeds)

- **Control (always-default)**: every house shares 0% — the "do nothing" benchmark (`results/control_always_default/`).
- **Charbonnier marginal-IQL** (`charbonnier_marginal_iql.py`): role-free `F = mean comfort + Jain fairness`, end-of-day counterfactual reward, hysteretic low-alpha learning.
- **Kusatake NSGA-II** (`kusatake_evolutionary_moo.py`): evolutionary multi-objective optimisation over comfort/fairness.
- **Behrunani GNE** (`behrunani_gne_fairness.py`): game-theoretic Nash/GNE fairness price mechanism.
- **May & Huang PPO** (`may_huang_ppo.py`): deep PPO baseline with `comfort + fairness` reward (+ waste-augmented sensitivity variant).
- **Battery-capacity scan** (`battery_sensitivity.py`): comfort/waste vs battery size 3.5–9 kWh.
- **End-of-day counterfactual isolation** (`ocean_marl_endofday.py`): swaps the per-step reward for a true end-of-day counterfactual, with a `--sanity` mode producing the 2×2 isolation (objective × reward horizon) that pins the mechanism on the learning rule.
- **Re-analysis / reproduction** (`gini_cloud_reanalysis.py`, `gini_more_scenarios.py`): re-run the main scenarios with the identical seeds and validate each run against the saved `final_metrics.csv` (max re-run vs saved error < 1e-9), then recompute Gini inequality and cloud-scarcity gaps.

## Key Findings

### Main community-level results (5-seed means)

- Main scenarios cluster near comfort ≈ 0.90–0.93, fairness ≈ 0.90–0.93, F = comfort + fairness ≈ 1.81–1.86, blackout ≈ 14–16%. One-way ANOVA across the five scenarios is now significant (F = 3.362, p = 0.0293), driven by the innovator-effect community, which underperforms mixed on comfort (t = −3.562, p = 0.0074).
- **Prosocial agents outperform selfish by ~2.9 pp** in mixed communities (p = 0.0011, paired t-test).
- Comfort gap **widens under scarcity** (higher cloud probability): at cloud 0.15 the prosocial–selfish gap is 2.95 pp, at cloud 0.35 it is 3.05 pp — personality matters most when resources are tight.

### Control and baselines (identical env, 5 seeds) — F = comfort + fairness

| Method                     | F       | comfort | waste (kWh) | vs control |
| -------------------------- | ------- | ------- | ----------- | ---------- |
| Charbonnier marginal-IQL   | 1.8834  | 0.9401  | 4.02        | **+0.0336, p=0.0016 (SIG)** |
| Kusatake NSGA-II           | 1.8820  | 0.9387  | 4.22        | **+0.0322, p=0.0126 (SIG)** |
| Always-default (control)   | 1.8498  | 0.9249  | 8.82        | —          |
| OCEAN-MARL all-selfish     | 1.8420  | 0.9195  | 4.98        | −0.0078 (ns) |
| OCEAN-MARL mixed           | 1.8432  | 0.9198  | 4.34        | −0.0066 (ns) |
| Behrunani GNE              | 1.8386  | 0.9171  | 0.00        | −0.0112 (ns) |
| OCEAN-MARL all-prosocial   | 1.8315  | 0.9139  | 4.41        | −0.0183 (ns) |
| OCEAN-MARL varied-altruism | 1.8325  | 0.9140  | 4.96        | −0.0173 (ns) |
| May & Huang PPO            | 1.8143  | 0.9058  | 4.66        | −0.0355, p=0.0008 (worse) |
| OCEAN-MARL innovator       | 1.8088  | 0.9018  | 4.70        | −0.0410, p=0.0017 (worse) |

Take-aways:
- **No learned method beats doing-nothing on comfort/fairness except the two working baselines** (Charbonnier, Kusatake).
- **Every learning method cuts waste ~45–50% vs the 8.82 kWh control** (Behrunani 0.00 by design) — ANOVA on waste F=119, p<0.0001. This waste-reduction framing is the thesis's core efficiency contribution.

### Gini inequality re-analysis

- Re-run with validation (max error < 1e-9 vs saved runs) gives Gini (comfort inequality, last 1000 eps): mixed 0.0790 vs innovator 0.0962 — the innovator composition adds ~21.8% inequality (paired t = −2.84, p = 0.047, `results/gini_reanalysis.csv`).
- Gini across `all_selfish` / `all_prosocial` / `varied_altruism` is tightly clustered (~0.07–0.10, `results/gini_more_scenarios.csv`).
- Cloud-scarcity re-run: prosocial–selfish comfort gap 2.95 pp (cloud 0.15) → 3.05 pp (cloud 0.35) (`results/cloud_sensitivity_reanalysis.csv`).

### Mechanism isolation: 2×2 (objective × reward horizon), seed 42, greedy F vs default 1.8850

| Cell | Objective × Horizon × Learner            | train F | greedy F | gain |
| ---- | ---------------------------------------- | ------- | -------- | ---- |
| A    | personality × per-step × OCEAN-MARL      | 1.8453  | ~default | ~0   |
| B    | personality × end-of-day × OCEAN-MARL    | 1.8361  | 1.8850   | +0.0000 |
| C    | community × end-of-day × Charbonnier-IQL | 1.8714  | 1.9057   | +0.0207 (76.4% sharing) |
| D    | community × end-of-day × OCEAN-MARL (mixed env) | 1.8359 | 1.8850 | +0.0000 |
| D2   | community × end-of-day × OCEAN-MARL (homogeneous env) | 1.8359 | 1.8850 | +0.0000 |

**Isolation verdict:** the objective and the reward horizon are *ruled out* as causal; the working cell C differs from D2 only in the **learning rule**. OCEAN-MARL's symmetric α=0.2 with optimistic Q-init (Q≈1.0) leaves near-zero end-of-day marginals unresolved → arbitrary ~45% sharing → greedy collapses to doing-nothing. Charbonnier's hysteretic low-alpha IQL escapes the tie and learns a real sharing policy. D2 ≡ D confirms env personality composition is irrelevant under a role-free objective.

### Battery-capacity sensitivity

- Comfort saturates for battery sizes ≈ 5–7 kWh; at 7 kWh mixed-community waste drops 8.73 → 3.84 kWh (−56%) vs default; only at 9 kWh does sharing lift comfort (0.980 vs 0.952 default).

## Module Descriptions

### Core
- **`offgrid_marl.py`** — The heart of the simulation. Personality profiles (`PERSONALITIES`), demand profiles (`DEMAND_PROFILES`), `House` (solar generation, battery, sharing), `Community` (ring topology, Jain fairness), `QLAgent` (tabular Q-learner), `run_simulation()`.

### Main runs & analysis
- **`run_experiments.py.py`** — Batch runner: five scenarios × five seeds → `results/<scenario>/seed_<N>/`.
- **`analyze_results.py`** — Loads `final_metrics.csv`, means/stds, `community_metrics.png`, `agent_type_comfort.png`.
- **`advanced_analysis.py`** — Q-table heatmaps, t-tests, one-way ANOVA → `statistical_tests.txt`.
- **`final_analysis.py`** — Gini coefficient, sharing frequency, cloud-scarcity sensitivity (→ `gini_comparison.png`, `sharing_frequency.png`, `sensitivity_cloud.png`).

### Re-analysis / reproduction
- **`gini_cloud_reanalysis.py`** — Re-runs `mixed` and `innovator_effect` (all 5 seeds), validates each run against the saved `final_metrics.csv` (max |re-run − saved| < 1e-9), writes `results/gini_reanalysis.csv`, and runs a paired t-test on Gini (`--task gini`). Also re-runs the cloud-scarcity scan (cloud 0.15/0.25/0.35) with Welch/Student t-tests → `results/cloud_sensitivity_reanalysis.csv` (`--task cloud`).
- **`gini_more_scenarios.py`** — Same validated re-run for `all_selfish`, `all_prosocial`, `varied_altruism` → `results/gini_more_scenarios.csv`.

### Baselines & controls
- **`charbonnier_marginal_iql.py`** — Baseline #1: role-free end-of-day counterfactual reward, hysteretic low-alpha IQL (`results/baseline_charbonnier/`, validation report in `results/baseline_charbonnier_validation/`).
- **`kusatake_evolutionary_moo.py`** — Baseline #2: evolutionary multi-objective optimisation (`results/baseline_kusatake/`).
- **`behrunani_gne_fairness.py`** — Baseline #3: GNE fairness price mechanism (`results/baseline_behrunani/`, λ=5 sensitivity in `results/baseline_behrunani_lambda5_sensitivity/`).
- **`may_huang_ppo.py`** — Baseline #4: deep PPO, `comfort + fairness` reward, supports `--reward cf_waste` and `--sanity` (`results/baseline_may_huang/`, waste-augmented sensitivity in `results/baseline_may_huang_waste_sensitivity/`).

### Isolation, sensitivity, comparison
- **`ocean_marl_endofday.py`** — End-of-day counterfactual variant of the main Q-learning (switchable `--objective personality|community`, `--homogeneous`). Sanity runs in `results/ocean_marl_endofday_sanity/`, `..._community/`, `..._community_homogeneous/`.
- **`battery_sensitivity.py`** — Battery-capacity scan (control + mixed) → `results/battery_sensitivity/`.
- **`baseline_comparison.py`** — The Chapter-4 comparison pipeline: aggregates main scenarios + 4 baselines + control into `results/baseline_comparison.{csv,txt,png}`, runs ANOVA and seed-matched t-tests, and appends the isolation 2×2 table.

### Control
- **`results/control_always_default/`** — pre-computed always-share-0% control for all five seeds, mirroring `run_simulation` exactly (`seed_<N>/`).

## Key Parameters

- `solar_max = 1.3` kW → daily generation ~9.9 kWh (clear)
- `battery_cap = 7.0` kWh (starts at 50%)
- `weather_cloud_prob = 0.15` (15% chance of cloudy day with 50% solar)
- Demand profiles total ~8.8 kWh/day
- Episodes = 8000 (baselines/sanity 3000), ε-greedy decay from 1.0 to 0.01, α = 0.2, γ = 0.99

## Output Data per Experiment Seed

- `final_metrics.csv`: scenario, seed, comfort, fairness, F, blackout rate, waste, prosocial/selfish comfort
- `config.json`: record of parameters used (includes the honest `personality_mix` for isolation runs)
- `results_plot.png`: learning curves and final comfort bar chart

## Dependencies

Install from `requirements.txt`:

```
numpy==1.24.3
matplotlib==3.7.1
pandas==2.0.3
scipy==1.10.1
torch   # required only for may_huang_ppo.py (PPO baseline)
```

Use Python 3.8 or newer. A local venv at the project root is recommended (`venv/bin/python`).

## How to Run

```bash
pip install -r requirements.txt
python offgrid_marl.py                     # single test run (mixed, saves to results/mixed/seed_42/)
python run_experiments.py.py               # full batch (5 scenarios × 5 seeds, ~25-35 min)
python charbonnier_marginal_iql.py         # baseline #1 (faithful run)
python kusatake_evolutionary_moo.py        # baseline #2
python behrunani_gne_fairness.py           # baseline #3
python may_huang_ppo.py                    # baseline #4 (PPO, needs torch)
python ocean_marl_endofday.py --sanity --objective community --homogeneous   # isolation cell D2
python battery_sensitivity.py              # battery-capacity scan
python baseline_comparison.py              # Chapter-4 comparison pipeline (CSV/TXT/PNG)
python analyze_results.py                  # community-level plots from saved CSVs
python advanced_analysis.py                # Q-table heatmaps + statistical tests (~15-20 min)
python final_analysis.py                   # Gini + sharing freq + sensitivity (~10-15 min)
python gini_cloud_reanalysis.py --task gini    # validated Gini re-run (mixed vs innovator)
python gini_cloud_reanalysis.py --task cloud   # cloud-scarcity re-run (0.15/0.25/0.35)
python gini_more_scenarios.py              # validated Gini for 3 more scenarios
```

The always-default control is pre-computed under `results/control_always_default/seed_<N>/` (computed via `run_simulation` with sharing forced to 0%).

## Project Structure

```
offgrid-energy-marl/
├── offgrid_marl.py               # Core simulation environment, agents, and learning loop
├── run_experiments.py.py         # Batch runner for main scenarios and seeds
├── analyze_results.py            # Community-level plots and stats from saved CSVs
├── advanced_analysis.py          # Q-table heatmaps and t-tests / ANOVA
├── final_analysis.py             # Gini coefficient, sharing frequency, scarcity sensitivity
├── gini_cloud_reanalysis.py      # Validated re-run: Gini (mixed vs innovator) + cloud scan
├── gini_more_scenarios.py        # Validated Gini: all_selfish / all_prosocial / varied_altruism
├── charbonnier_marginal_iql.py   # Baseline #1: role-free end-of-day marginal IQL
├── kusatake_evolutionary_moo.py  # Baseline #2: evolutionary multi-objective optimisation
├── behrunani_gne_fairness.py     # Baseline #3: GNE fairness price mechanism
├── may_huang_ppo.py              # Baseline #4: deep PPO
├── ocean_marl_endofday.py        # End-of-day counterfactual variant + isolation sanity runs
├── battery_sensitivity.py        # Battery-capacity scan
├── baseline_comparison.py        # Chapter-4 comparison pipeline (main + baselines + control)
├── agent.py, environment.py, simulation.py, t.py   # legacy/alternate code (unused)
├── requirements.txt              # Python dependencies
├── README.md                     # Project overview, technical reference, and usage (this file)
├── 0-Active Doc/                 # Main thesis documents (see below)
└── results/                      # Output directory (generated)
    ├── all_selfish/  all_prosocial/  mixed/
    ├── varied_altruism/  innovator_effect/     # 5 seeds each: seed_<N>/{final_metrics.csv, config.json, results_plot.png}
    ├── control_always_default/                 # always-share-0% control (5 seeds)
    ├── baseline_charbonnier/ + baseline_charbonnier_validation/
    ├── baseline_kusatake/ + baseline_kusatake_timing/
    ├── baseline_behrunani/ + ..._lambda5_sensitivity/ + ..._sanity/
    ├── baseline_may_huang/ + ..._waste_sensitivity/ + ..._sanity/
    ├── ocean_marl_endofday_sanity/ + ..._community/ + ..._community_homogeneous/
    ├── battery_sensitivity/                    # batt3.5/  batt5/  batt7/  batt9/  summary.csv
    ├── baseline_comparison.{csv,txt,png}       # Chapter-4 comparison + stats + isolation 2×2
    ├── gini_reanalysis.csv  gini_more_scenarios.csv  cloud_sensitivity_reanalysis.csv
    ├── community_metrics.png  agent_type_comfort.png
    ├── qtable_heatmaps.png  gini_comparison.png
    ├── sharing_frequency.png  sensitivity_cloud.png
    ├── statistical_tests.txt
    └── figures/                                # thesis figures (v01–v18, e.g. ring topology, solar curve, Lorenz curve)
```

## Related Documents

- **`0-Active Doc/`** — The **main documents for the Thesis**: `thesis_v8.md` (full active thesis draft) and `check list.md` (tracking/revision checklist).

