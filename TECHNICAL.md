# Smart Neighborhood Energy Sharing MARL Simulation – Technical Documentation

## Overview

This project implements a **multi‑agent reinforcement learning (MARL)** simulation of a smart neighborhood micro-grid where houses (agents) decide whether to share surplus solar energy with neighbours. Each agent follows a fixed personality profile (selfish, prosocial, altruistic) that shapes its reward function, enabling the study of emergent fairness and efficiency trade‑offs.

## File Structure

```
offgrid-energy-marl/
├── offgrid_marl.py          # Core simulation environment, agents, and learning loop
├── run_experiments.py       # Batch runner for multiple scenarios and seeds
├── analyze_results.py       # Statistical analysis and main comparison plots
├── advanced_analysis.py     # Q‑table heatmaps and t‑tests / ANOVA
├── final_analysis.py        # Gini coefficient, sharing frequency, sensitivity analysis
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
├── README.md                # Project overview
├── TECHNICAL.md             # Technical documentation (this file)
├── ACADEMIC.md              # Academic write-up
├── REVIEW.md                # Review feedback
├── THESIS_ADVISOR_BRIEF.md  # Academic assistant brief
└── TASK_v4.md               # Archived implementation instructions
```

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

1. **Setup**: `pip install -r requirements.txt`
2. **Single test run**: `python offgrid_marl.py` (runs mixed community, saves plots+CSV in `results/mixed/seed_42/`)
3. **Full experiments**: `python run_experiments.py` (runs all scenarios × seeds, 25 combinations, takes ~25‑35 minutes)
4. **Analysis**:
   - `python analyze_results.py` → community‑level metrics and comparison plots.
   - `python advanced_analysis.py` → Q‑table heatmaps and statistical tests (may take ~15‑20 min because it retrains agents).
   - `python final_analysis.py` → Gini, sharing frequency, sensitivity (also retrains multiple times, ~10‑15 min).

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
