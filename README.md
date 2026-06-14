# Smart Neighborhood Energy Sharing MARL Simulation — V3

## What It Is

A **Multi-Agent Reinforcement Learning (MARL)** simulation where houses in a smart neighborhood micro-grid decide whether to share surplus solar energy with neighbours. Each house has a **personality** (selfish → altruistic) that determines how much it values personal comfort vs. community fairness in its reward function. The project studies emergent sharing behaviour, fairness-efficiency trade-offs, and the impact of personality diversity under resource scarcity.

---

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

---

## Project Structure

```
sim/
├── offgrid_marl.py          # MAIN: full simulation (House, Community, QLAgent, run_simulation, plotting)
├── run_experiments.py.py    # Batch runner: 5 scenarios × 5 seeds, saves results/
├── analyze_results.py       # Loads CSVs → community_metrics.png + agent_type_comfort.png + summary table
├── advanced_analysis.py     # Q-table heatmaps + statistical tests (t-tests, ANOVA)
├── final_analysis.py        # Gini coefficient, sharing frequency, sensitivity analysis (cloud probability)
├── agent.py                 # Alternate/legacy Q-learning agent (unused, superseded by offgrid_marl.py)
├── environment.py           # Alternate/legacy House + EnergyCommunity (unused, superseded by offgrid_marl.py)
├── simulation.py            # Alternate/legacy simulation runner (incomplete, unused)
├── t.py                     # Quick dependency test script
├── requirements.txt         # numpy, matplotlib, pandas, scipy, seaborn, jupyter
├── results/                 # All outputs (CSVs, plots, configs)
│   ├── all_selfish/         #   seed_42, seed_123, seed_456, seed_789, seed_1011
│   ├── all_prosocial/       #   (same seeds)
│   ├── mixed/               #   (same seeds)
│   ├── varied_altruism/     #   (same seeds)
│   ├── innovator_effect/    #   (same seeds)
│   ├── community_metrics.png
│   ├── agent_type_comfort.png
│   ├── qtable_heatmaps.png
│   ├── gini_comparison.png
│   ├── sharing_frequency.png
│   ├── sensitivity_cloud.png
│   └── statistical_tests.txt
├── README.md                # This file — project overview
├── TECHNICAL.md             # Technical documentation (setup, modules, how to run)
├── ACADEMIC.md              # Academic write‑up (thesis-style paper with results)
├── REVIEW.md                # Review feedback from advisor (identifies OCEAN gap)
├── THESIS_ADVISOR_BRIEF.md  # Brief for academic assistant guiding student's thesis
└── TASK_v4.md               # Archived implementation instructions (v4 changes)
```

## How to Run

```bash
pip install -r requirements.txt
python offgrid_marl.py                  # single test run (mixed, saves to results/mixed/seed_42/)
python run_experiments.py.py            # full batch (25 runs, ~25-35 min)
python analyze_results.py               # plots from saved CSVs
python advanced_analysis.py             # Q-table heatmaps + stats (~15-20 min)
python final_analysis.py                # Gini + sharing freq + sensitivity (~10-15 min)
```
