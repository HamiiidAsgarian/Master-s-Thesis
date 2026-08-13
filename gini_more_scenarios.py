import csv
import os
import numpy as np

from offgrid_marl import run_simulation

SEEDS = [42, 123, 456, 789, 1011]
EPISODES = 8000
LAST_N = 1000
BATTERY_CAP = 7.0
SOLAR_MAX = 1.3

SCENARIOS = {
    'all_selfish': ['pure_selfish'] * 10,
    'all_prosocial': ['prosocial'] * 10,
    'varied_altruism': ['altruistic'] + ['prosocial'] * 3
                       + ['individualist'] * 3 + ['pure_selfish'] * 3,
}


def gini(x):
    x = np.array(x, dtype=float)
    if np.amin(x) < 0:
        x -= np.amin(x)
    x += 1e-10
    x = np.sort(x)
    n = len(x)
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * x) / (n * np.sum(x)) - (n + 1) / n)


def validate(scenario, seed, hist):
    path = os.path.join('results', scenario, f'seed_{seed}', 'final_metrics.csv')
    if not os.path.exists(path):
        print(f"    [validation] no saved file at {path} — skipping")
        return
    with open(path) as f:
        saved = next(csv.DictReader(f))
    last = slice(-LAST_N, None)
    comfort = np.mean(hist['comfort_mean'][last])
    fairness = np.mean(hist['fairness'][last])
    blackout = np.mean(hist['blackout_days'][last])
    waste = np.mean(hist['total_waste'][last])
    pro = np.mean([np.mean(hist['agent_comforts'][i][last]) for i in range(5)])
    self = np.mean([np.mean(hist['agent_comforts'][i][last]) for i in range(5, 10)])
    diffs = {
        'comfort': abs(comfort - float(saved['comfort'])),
        'fairness': abs(fairness - float(saved['fairness'])),
        'blackout_rate': abs(blackout - float(saved['blackout_rate'])),
        'waste': abs(waste - float(saved['waste'])),
        'prosocial_comfort': abs(pro - float(saved['prosocial_comfort'])),
        'selfish_comfort': abs(self - float(saved['selfish_comfort'])),
    }
    worst = max(diffs.values())
    print(f"    [validation] {scenario}/seed_{seed}: max |re-run - saved| = {worst:.3e}"
          + ("  (reproduction OK)" if worst < 1e-9 else "  (MISMATCH)"))


rows = []
for scenario, mix in SCENARIOS.items():
    print(f"\n--- GINI: {scenario} ---")
    for seed in SEEDS:
        _, _, history = run_simulation(
            num_houses=10, episodes=EPISODES, battery_cap=BATTERY_CAP,
            solar_max=SOLAR_MAX, personality_mix=mix, seed=seed,
            verbose=False)
        validate(scenario, seed, history)
        per_ep = [gini([history['agent_comforts'][i][e] for i in range(10)])
                  for e in range(EPISODES - LAST_N, EPISODES)]
        g = float(np.mean(per_ep))
        rows.append({'scenario': scenario, 'seed': seed, 'gini': g})
        print(f"    seed {seed}: gini = {g:.6f}")

with open('results/gini_more_scenarios.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['scenario', 'seed', 'gini'])
    writer.writeheader()
    writer.writerows(rows)
print("\nsaved results/gini_more_scenarios.csv")

for scenario in SCENARIOS:
    vals = [r['gini'] for r in rows if r['scenario'] == scenario]
    print(f"\n{scenario}: gini mean = {np.mean(vals):.6f} ± {np.std(vals, ddof=0):.6f} (pop) "
          f"± {np.std(vals, ddof=1):.6f} (sample), values = {[round(v, 6) for v in vals]}")
