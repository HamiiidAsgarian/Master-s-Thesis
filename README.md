# Smart Neighborhood Energy Sharing MARL Simulation

## What It Is

A **Multi-Agent Reinforcement Learning (MARL)** simulation of a smart neighborhood micro-grid where houses (agents) decide whether to share surplus solar energy with neighbours. Each agent follows a fixed personality profile (selfish, prosocial, altruistic) that shapes its reward function, enabling the study of emergent fairness and efficiency trade‑offs under resource scarcity.

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
- **Personality types**: `pure_selfish` (1.0, 0.0), `individualist` (0.8, 0.2), `prosocial` (0.5, 0.5), `altruistic` (0.2, 0.8).
- **OCEAN mapping**: personalities correspond to Big Five coordinates — see OCEAN mapping table in `ACADEMIC.md` §2.2.
- **Learning**: ε-greedy (ε decays 1.0→0.01), α=0.2, γ=0.99, optimistic Q-init.

### Community Layer

- **Energy flow**: generation → own demand → battery storage → surplus export to neighbour.
- **Fairness metric**: Jain's fairness index of demand-met fractions across houses.
- **Tracking**: comfort, blackout rate, waste, Gini coefficient, sharing frequency from learned Q-tables.

### Experiments

5 scenarios × 5 seeds:

| Scenario         | Composition                                                 |
| ---------------- | ----------------------------------------------------------- |
| All Selfish      | 10 × pure_selfish                                           |
| All Prosocial    | 10 × prosocial                                              |
| Mixed            | 5 prosocial + 5 selfish                                     |
| Varied Altruism  | 1 altruistic, 3 prosocial, 3 individualist, 3 selfish       |
| Innovator Effect | 1 high-O innovator, 4 prosocial, 3 individualist, 2 selfish |

### Key Findings

- All communities achieve ~0.91 comfort, ~0.92 fairness, ~14% blackout rate (no significant ANOVA difference at community level).
- Prosocial agents outperform selfish by **2.4 pp** in mixed communities (p < 0.05, paired t-test).
- Mixed communities show highest **inequality** (Gini = 0.105).
- **Sharing frequency** from Q-tables: prosocial ~14–16%, selfish ~9–10%.
- Comfort gap **widens under scarcity** (higher cloud probability), showing personality matters most when resources are tight.
- Scenario 5 (Innovator Effect) pending results: tests whether a single high-Openness exploratory agent stabilizes or disrupts mixed community energy sharing.

## Module Descriptions

### `offgrid_marl.py`
The heart of the simulation. Contains:
- **Personality profiles** (`PERSONALITIES` dict): weights for self‑interest vs. fairness.
- **Demand profiles** (`DEMAND_PROFILES`): hourly electricity demand for different house types.
- **`House` class**: models solar generation (half‑sine curve), battery storage, demand, and sharing logic. Energy flows: generation → own demand → battery → surplus → possible sharing.
- **`Community` class**: coordinates multiple houses, manages sharing pairs (ring topology), computes Jain's fairness index.
- **`QLAgent` class**: independent tabular Q‑learner with state (hour, discretised battery level), actions (share 0%, 50%, 100% of net generation), and personality‑weighted reward (own comfort + fairness).
- **`run_simulation()`**: main loop, configurable with house count, battery capacity, solar peak, personality mix, cloud probability, saving options.

### `run_experiments.py`
Defines five scenarios (all‑selfish, all‑prosocial, mixed, varied‑altruism, innovator_effect) and loops over five random seeds. Calls `run_simulation()` for each combination and saves metrics in `results/<scenario>/seed_<N>/`.

### `analyze_results.py`
Loads all `final_metrics.csv` files, computes means and standard deviations, and produces:
- `community_metrics.png`: bar charts of comfort, fairness, blackout rate across scenarios.
- `agent_type_comfort.png`: grouped bar chart comparing prosocial vs selfish comfort in mixed communities.
Prints a summary table to console.

### `advanced_analysis.py`
- Retrains a set of agents for each scenario to extract Q‑tables.
- Generates `qtable_heatmaps.png`: average Q‑values per hour for representative agents.
- Runs statistical tests (independent t‑test, paired t‑test, one‑way ANOVA) and saves results in `statistical_tests.txt`.

### `final_analysis.py`
- Computes **Gini coefficient** of comfort across houses for one seed per scenario → `gini_comparison.png`.
- Extracts **sharing frequency** from Q‑tables (fraction of states where best action is share) → `sharing_frequency.png`.
- **Sensitivity analysis**: runs the mixed community with cloud probabilities 15%, 25%, 35% and plots the prosocial‑selfish comfort gap → `sensitivity_cloud.png`.

## Key Parameters

- `solar_max = 1.3` kW → daily generation ~9.9 kWh (clear)
- `battery_cap = 7.0` kWh (starts at 50%)
- `weather_cloud_prob = 0.15` (15% chance of cloudy day with 50% solar)
- Demand profiles total ~8.8 kWh/day
- Episodes = 8000, ε‑greedy decay from 1.0 to 0.01, α = 0.2, γ = 0.99

## Output Data per Experiment Seed

- `final_metrics.csv`: comfort, fairness, blackout rate, waste, prosocial/selfish comfort
- `config.json`: record of parameters used
- `results_plot.png`: learning curves and final comfort bar chart

## Dependencies

Install from `requirements.txt`:

```
numpy==1.24.3
matplotlib==3.7.1
pandas==2.0.3
scipy==1.10.1
```

Use Python 3.8 or newer.

## How to Run

```bash
pip install -r requirements.txt
python offgrid_marl.py                  # single test run (mixed, saves to results/mixed/seed_42/)
python run_experiments.py               # full batch (5 scenarios × 5 seeds, ~25-35 min)
python analyze_results.py               # community-level plots from saved CSVs
python advanced_analysis.py             # Q-table heatmaps + statistical tests (~15-20 min)
python final_analysis.py                # Gini + sharing freq + sensitivity (~10-15 min)
```

## Project Structure

```
offgrid-energy-marl/
├── offgrid_marl.py          # Core simulation environment, agents, and learning loop
├── run_experiments.py       # Batch runner for multiple scenarios and seeds
├── analyze_results.py       # Statistical analysis and main comparison plots
├── advanced_analysis.py     # Q‑table heatmaps and t‑tests / ANOVA
├── final_analysis.py        # Gini coefficient, sharing frequency, sensitivity analysis
├── agent.py                 # Alternate/legacy Q-learning agent (unused)
├── environment.py           # Alternate/legacy House + EnergyCommunity (unused)
├── simulation.py            # Alternate/legacy simulation runner (incomplete)
├── t.py                     # Quick dependency test script
├── requirements.txt         # Python dependencies
├── results/                 # Output directory (generated)
│   ├── all_selfish/
│   ├── all_prosocial/
│   ├── mixed/
│   ├── varied_altruism/
│   ├── innovator_effect/
│   ├── community_metrics.png
│   ├── agent_type_comfort.png
│   ├── qtable_heatmaps.png
│   ├── gini_comparison.png
│   ├── sharing_frequency.png
│   ├── sensitivity_cloud.png
│   └── statistical_tests.txt
├── README.md                # Project overview, technical reference, and usage (this file)
├── ACADEMIC.md              # Academic write‑up (thesis-style paper with results)
├── REVIEW.md                # Review feedback from advisor
├── THESIS_ADVISOR_BRIEF.md  # Internal brief for academic assistant guiding the thesis
└── TASK_v4.md               # Archived implementation instructions
```

## Related Documents

- **`ACADEMIC.md`** — Full academic write‑up formatted as a thesis chapter, including OCEAN mapping table, ethics framing, and detailed results discussion.
- **`THESIS_ADVISOR_BRIEF.md`** — Internal operational document for the AI academic assistant (student profile, pacing plan, communication strategy). Not part of the public project documentation.
- **`REVIEW.md`** — Advisor review feedback and action items.
- **`Final_state.md`** — Working audit log tracking professor feedback items and revision status (thesis-writing process only).
