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
- **Personality types**: `pure_selfish` (1.0, 0.0), `individualist` (0.8, 0.2), `prosocial` (0.5, 0.5), `altruistic` (0.2, 0.8), `high_openness_innovator` (0.5, 0.5, min-eps 0.05).
- **OCEAN mapping**: personalities correspond to Big Five coordinates — see OCEAN mapping table in `ACADEMIC.md` §2.2.
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

## Key Findings

### Main community-level results (5-seed means)

- All main scenarios cluster near comfort ≈ 0.92, fairness ≈ 0.92, F = comfort + fairness ≈ 1.83–1.84, blackout ≈ 14–16% (no significant ANOVA difference at community level).
- **Prosocial agents outperform selfish by 2.9 pp** in mixed communities (p = 0.0011, paired t-test).
- Comfort gap **widens under scarcity** (higher cloud probability), showing personality matters most when resources are tight.

### Control and baselines (identical env, 5 seeds) — F = comfort + fairness

| Method                     | F       | comfort | waste (kWh) | vs control |
| -------------------------- | ------- | ------- | ----------- | ---------- |
| Charbonnier marginal-IQL   | 1.8834  | 0.9401  | 4.02        | **+0.0336, p=0.002 (SIG)** |
| Kusatake NSGA-II           | 1.8820  | 0.9387  | 4.22        | **+0.0322, p=0.013 (SIG)** |
| Always-default (control)   | 1.8498  | 0.9249  | 8.82        | —          |
| OCEAN-MARL mixed           | 1.8432  | 0.9198  | 4.34        | −0.0066 (ns) |
| Behrunani GNE              | 1.8386  | 0.9171  | 0.00        | −0.0112 (ns) |
| May & Huang PPO            | 1.8143  | 0.9058  | 4.66        | −0.0355, p=0.001 (worse) |
| OCEAN-MARL innovator       | 1.8088  | 0.9018  | 4.70        | −0.0410, p=0.002 (worse) |

Take-aways:
- **No learned method beats doing-nothing on comfort/fairness except the two working baselines** (Charbonnier, Kusatake).
- **Every learning method cuts waste ~45–50% vs the 8.82 kWh control** (Behrunani 0.00 by design) — ANOVA on waste F=119, p<0.0001. This waste-reduction framing is the thesis's core efficiency contribution.

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
- **`final_analysis.py`** — Gini coefficient, sharing frequency, scarcity sensitivity.

### Baselines & controls
- **`charbonnier_marginal_iql.py`** — Baseline #1: role-free end-of-day counterfactual reward, hysteretic low-alpha IQL (`results/baseline_charbonnier/`, validation report in `results/baseline_charbonnier_validation/`).
- **`kusatake_evolutionary_moo.py`** — Baseline #2: evolutionary multi-objective optimisation (`results/baseline_kusatake/`).
- **`behrunani_gne_fairness.py`** — Baseline #3: GNE fairness price mechanism (`results/baseline_behrunani/`, λ=5 sensitivity in `results/baseline_behrunani_lambda5_sensitivity/`).
- **`may_huang_ppo.py`** — Baseline #4: deep PPO, `comfort + fairness` reward, supports `--reward cf_waste` and `--sanity` (`results/baseline_may_huang/`, waste-augmented sensitivity in `results/baseline_may_huang_waste_sensitivity/`).

### Isolation, sensitivity, comparison
- **`ocean_marl_endofday.py`** — End-of-day counterfactual variant of the main Q-learning (switchable `--objective personality|community`, `--homogeneous`). Sanity runs in `results/ocean_marl_endofday_sanity/`, `..._community/`, `..._community_homogeneous/`.
- **`battery_sensitivity.py`** — Battery-capacity scan (control + mixed) → `results/battery_sensitivity/`.
- **`baseline_comparison.py`** — The Chapter-4 comparison pipeline: aggregates main scenarios + 4 baselines + control into `results/baseline_comparison.{csv,txt,png}`, runs ANOVA and seed-matched t-tests, and appends the isolation 2×2 table.

### Control runner
- **`control_always_default/`** — pre-computed always-share-0% control for all five seeds, mirroring `run_simulation` exactly (results in `results/control_always_default/seed_<N>/`).

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
python control_always_default/...           # control computed via run_simulation (see notes)
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
```

## Project Structure

```
offgrid-energy-marl/
├── offgrid_marl.py               # Core simulation environment, agents, and learning loop
├── run_experiments.py.py         # Batch runner for main scenarios and seeds
├── analyze_results.py            # Statistical analysis and main comparison plots
├── advanced_analysis.py          # Q-table heatmaps and t-tests / ANOVA
├── final_analysis.py             # Gini coefficient, sharing frequency, sensitivity analysis
├── charbonnier_marginal_iql.py   # Baseline #1: role-free end-of-day marginal IQL
├── kusatake_evolutionary_moo.py  # Baseline #2: evolutionary multi-objective optimisation
├── behrunani_gne_fairness.py     # Baseline #3: GNE fairness price mechanism
├── may_huang_ppo.py              # Baseline #4: deep PPO
├── ocean_marl_endofday.py        # End-of-day counterfactual variant + isolation sanity runs
├── battery_sensitivity.py        # Battery-capacity scan
├── baseline_comparison.py        # Chapter-4 comparison pipeline (main + baselines + control)
├── agent.py, environment.py, simulation.py, t.py   # legacy/alternate code (unused)
├── requirements.txt              # Python dependencies
├── results/                      # Output directory (generated)
│   ├── all_selfish/  all_prosocial/  mixed/
│   ├── varied_altruism/  innovator_effect/
│   ├── control_always_default/        # always-share-0% control (5 seeds)
│   ├── baseline_charbonnier/          # + baseline_charbonnier_validation/
│   ├── baseline_kusatake/             # + baseline_kusatake_timing/
│   ├── baseline_behrunani/            # + ..._lambda5_sensitivity/ + ..._sanity/
│   ├── baseline_may_huang/            # + ..._waste_sensitivity/ + ..._sanity/
│   ├── ocean_marl_endofday_sanity/    # + ..._community/ + ..._community_homogeneous/
│   ├── battery_sensitivity/
│   ├── baseline_comparison.{csv,txt,png}
│   ├── community_metrics.png  agent_type_comfort.png
│   ├── qtable_heatmaps.png  gini_comparison.png
│   ├── sharing_frequency.png  sensitivity_cloud.png
│   ├── statistical_tests.txt
│   └── figures/
├── README.md                   # Project overview, technical reference, and usage (this file)
├── ACADEMIC.md                 # Academic write-up (thesis-style paper with results)
├── HamidOutput/                # Thesis drafts (fa/En): thesis_full.md, ACADEMIC_v3_En.md
└── instructions-nuri-2.md      # Baseline specs + wiring instructions
```

## Related Documents

- **`ACADEMIC.md`** — Full academic write-up formatted as a thesis chapter, including OCEAN mapping table, ethics framing, and detailed results discussion.
- **`HamidOutput/thesis_full.md`** — Full Persian thesis draft (front matter, ch. 1–5, references).
- **`HamidOutput/ACADEMIC_v3_En.md`** — English thesis draft (academic v3, structured TOC, tables/figures lists).
- **`REVIEW.md`** — Advisor review feedback and action items.
- **`Final_state.md`** — Working audit log tracking professor feedback items and revision status (thesis-writing process only).
- **`instructions-nuri-2.md`** — Baseline specifications and wiring instructions for the ANOVA/post-hoc pipeline.
