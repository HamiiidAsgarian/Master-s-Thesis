import argparse
import os
import sys
import csv
import numpy as np
from scipy import stats

from offgrid_marl import run_simulation

SEEDS = [42, 123, 456, 789, 1011]
EPISODES = 8000
LAST_N = 1000
BATTERY_CAP = 7.0
SOLAR_MAX = 1.3

SCENARIOS = {
    'mixed': ['prosocial'] * 5 + ['pure_selfish'] * 5,
    'innovator_effect': ['high_openness_innovator'] + ['prosocial'] * 4
                        + ['individualist'] * 3 + ['pure_selfish'] * 2,
}


def gini(x):
    """Identical implementation to final_analysis.py:gini()"""
    x = np.array(x, dtype=float)
    if np.amin(x) < 0:
        x -= np.amin(x)
    x += 1e-10
    x = np.sort(x)
    n = len(x)
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * x) / (n * np.sum(x)) - (n + 1) / n)


def summarize(history):
    """Community-level metrics exactly as in offgrid_marl.py:338-359."""
    last = slice(-LAST_N, None)
    comfort = np.mean(history['comfort_mean'][last])
    fairness = np.mean(history['fairness'][last])
    blackout = np.mean(history['blackout_days'][last])
    waste = np.mean(history['total_waste'][last])
    pro = np.mean([np.mean(history['agent_comforts'][i][last]) for i in range(5)])
    self = np.mean([np.mean(history['agent_comforts'][i][last]) for i in range(5, 10)])
    return comfort, fairness, blackout, waste, pro, self


def validate(scenario, seed, hist):
    """Compare re-run summary against the originally saved final_metrics.csv."""
    path = os.path.join('results', scenario, f'seed_{seed}', 'final_metrics.csv')
    if not os.path.exists(path):
        print(f"    [validation] no saved file at {path} — skipping")
        return
    with open(path) as f:
        saved = next(csv.DictReader(f))
    comfort, fairness, blackout, waste, pro, self = summarize(hist)
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


def task_gini():
    rows = []
    mixed_ginis = []
    innov_ginis = []
    for scenario, mix in SCENARIOS.items():
        print(f"\n--- GINI: {scenario} ---")
        for seed in SEEDS:
            agents, _, history = run_simulation(
                num_houses=10, episodes=EPISODES, battery_cap=BATTERY_CAP,
                solar_max=SOLAR_MAX, personality_mix=mix, seed=seed,
                verbose=False)
            validate(scenario, seed, history)
            per_ep = [gini([history['agent_comforts'][i][e] for i in range(10)])
                      for e in range(EPISODES - LAST_N, EPISODES)]
            g = float(np.mean(per_ep))
            rows.append({'scenario': scenario, 'seed': seed, 'gini': g})
            if scenario == 'mixed':
                mixed_ginis.append(g)
            else:
                innov_ginis.append(g)
            print(f"    seed {seed}: gini = {g:.6f}")

    with open('results/gini_reanalysis.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['scenario', 'seed', 'gini'])
        writer.writeheader()
        writer.writerows(rows)
    print("\nsaved results/gini_reanalysis.csv")

    print("\n=== PAIRED t-TEST: mixed gini vs innovator_effect gini ===")
    print(f"  mixed     gini values: {[round(v,6) for v in mixed_ginis]}")
    print(f"  innovator gini values: {[round(v,6) for v in innov_ginis]}")
    print("  scipy.stats.ttest_rel(mixed_ginis, innov_ginis)")
    t_stat, p_val = stats.ttest_rel(mixed_ginis, innov_ginis)
    print(f"  t = {t_stat:.6f}   p = {p_val:.6f}")
    d = np.array(mixed_ginis) - np.array(innov_ginis)
    print(f"  diffs (mixed-innov): {[round(v,6) for v in d]}")
    print(f"  mean diff = {np.mean(d):.6f}")
    print(f"  Cohen's d (mean/std, ddof=1) = {np.mean(d)/np.std(d, ddof=1):.3f}")
    pct = (np.mean(innov_ginis) - np.mean(mixed_ginis)) / np.mean(mixed_ginis) * 100
    print(f"  innovator gini is +{pct:.2f}% vs mixed "
          f"(mean mixed={np.mean(mixed_ginis):.6f}, mean innov={np.mean(innov_ginis):.6f})")


def task_cloud():
    rows = []
    results = {}
    for cp in [0.15, 0.25, 0.35]:
        print(f"\n--- CLOUD SENSITIVITY: cloud_prob={cp} ---")
        pro_vals = []
        self_vals = []
        for seed in SEEDS:
            _, _, history = run_simulation(
                num_houses=10, episodes=EPISODES, battery_cap=BATTERY_CAP,
                solar_max=SOLAR_MAX,
                personality_mix=['prosocial'] * 5 + ['pure_selfish'] * 5,
                seed=seed, verbose=False, weather_cloud_prob=cp)
            if cp == 0.15:
                validate('mixed', seed, history)
            last = slice(-LAST_N, None)
            pro = float(np.mean([np.mean(history['agent_comforts'][i][last])
                                 for i in range(5)]))
            self = float(np.mean([np.mean(history['agent_comforts'][i][last])
                                  for i in range(5, 10)]))
            pro_vals.append(pro)
            self_vals.append(self)
            rows.append({'cloud_prob': cp, 'seed': seed,
                         'prosocial_comfort': pro, 'selfish_comfort': self})
            print(f"    seed {seed}: prosocial={pro:.6f}  selfish={self:.6f}")
        results[cp] = (pro_vals, self_vals)

    with open('results/cloud_sensitivity_reanalysis.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f,
                                fieldnames=['cloud_prob', 'seed',
                                            'prosocial_comfort', 'selfish_comfort'])
        writer.writeheader()
        writer.writerows(rows)
    print("\nsaved results/cloud_sensitivity_reanalysis.csv")

    for cp in [0.15, 0.25, 0.35]:
        pro_vals, self_vals = results[cp]
        gap_pp = (np.mean(pro_vals) - np.mean(self_vals)) * 100
        print(f"\n=== cloud_prob={cp}: prosocial vs selfish (independent t-test) ===")
        print(f"  prosocial values: {[round(v,6) for v in pro_vals]}")
        print(f"  selfish   values: {[round(v,6) for v in self_vals]}")
        print(f"  prosocial mean={np.mean(pro_vals):.4f} ± {np.std(pro_vals,ddof=0):.4f} (pop), "
              f"{np.std(pro_vals,ddof=1):.4f} (sample)")
        print(f"  selfish   mean={np.mean(self_vals):.4f} ± {np.std(self_vals,ddof=0):.4f} (pop), "
              f"{np.std(self_vals,ddof=1):.4f} (sample)")
        print(f"  gap = {gap_pp:.2f} percentage points")
        t_w, p_w = stats.ttest_ind(pro_vals, self_vals, equal_var=False)
        t_s, p_s = stats.ttest_ind(pro_vals, self_vals, equal_var=True)
        print(f"  scipy.stats.ttest_ind(pro, self, equal_var=False): t = {t_w:.4f}  p = {p_w:.4f}  (Welch)")
        print(f"  scipy.stats.ttest_ind(pro, self, equal_var=True) : t = {t_s:.4f}  p = {p_s:.4f}  (Student)")


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--task', choices=['gini', 'cloud'], required=True)
    args = ap.parse_args()
    if args.task == 'gini':
        task_gini()
    else:
        task_cloud()
