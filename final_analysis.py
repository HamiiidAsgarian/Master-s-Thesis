import numpy as np
import matplotlib.pyplot as plt
import os, json
from offgrid_marl import run_simulation, PERSONALITIES, DEMAND_PROFILES

# ========== 1. GINI COEFFICIENT FUNCTION ==========
def gini(x):
    """Compute Gini coefficient of an array of values."""
    x = np.array(x, dtype=float)
    if np.amin(x) < 0:
        x -= np.amin(x)
    x += 1e-10
    x = np.sort(x)
    n = len(x)
    index = np.arange(1, n+1)
    return (2 * np.sum(index * x) / (n * np.sum(x)) - (n+1)/n)

# ========== 2. COLLECT GINI & SHARING DATA ==========
def analyze_scenario_gini_and_sharing(scenario_name, mix, seed=42):
    """
    Run one simulation, return:
    - gini_last_1000: average Gini coefficient across houses over last 1000 episodes
    - sharing_freq: array of sharing frequency per agent (proportion of Q-table states where best action is share)
    """
    agents, community, history = run_simulation(
        num_houses=10, episodes=8000, battery_cap=7.0, solar_max=1.3,
        personality_mix=mix, seed=seed, verbose=False
    )

    last_comforts = history['agent_comforts']
    last_1000 = slice(-1000, None)
    ginis = []
    for ep_comforts in zip(*[c[last_1000] for c in last_comforts]):
        ginis.append(gini(ep_comforts))
    mean_gini = np.mean(ginis)

    sharing_freqs = []
    for agent in agents:
        best_actions = np.argmax(agent.q, axis=2)
        share_count = np.sum(best_actions >= 1)
        total_states = best_actions.size
        sharing_freqs.append(share_count / total_states)

    return mean_gini, np.array(sharing_freqs)

# ========== 3. RUN GINI & SHARING ANALYSIS (All 5 Seeds) ==========
scenarios = {
    'All Selfish': ['pure_selfish']*10,
    'All Prosocial': ['prosocial']*10,
    'Mixed': ['prosocial']*5 + ['pure_selfish']*5,
    'Varied Altruism': ['altruistic', 'prosocial', 'prosocial', 'prosocial', 'individualist', 'individualist', 'individualist', 'pure_selfish', 'pure_selfish', 'pure_selfish'],
    'Innovator Effect': ['high_openness_innovator'] + ['prosocial']*4 + ['individualist']*3 + ['pure_selfish']*2
}

all_seeds = [42, 123, 456, 789, 1011]

gini_results = {name: [] for name in scenarios}
sharing_results = {name: [] for name in scenarios}

for name, mix in scenarios.items():
    print(f"Analyzing {name} across {len(all_seeds)} seeds...")
    for seed in all_seeds:
        mean_gini, sharing_freq = analyze_scenario_gini_and_sharing(name, mix, seed)
        gini_results[name].append(mean_gini)
        sharing_results[name].append(sharing_freq)
        print(f"  seed {seed}: Gini={mean_gini:.4f}")

# ========== 4. GINI RESULTS ==========
print("\n" + "=" * 60)
print("GINI COEFFICIENT RESULTS (Mean ± Std across 5 seeds)")
print("=" * 60)
gini_means = {}
gini_stds = {}
for name in scenarios:
    vals = gini_results[name]
    m, s = np.mean(vals), np.std(vals)
    gini_means[name] = m
    gini_stds[name] = s
    print(f"  {name:20s}: {m:.4f} ± {s:.4f}")

# Plot Gini with error bars
plt.figure(figsize=(8,5))
names = list(scenarios.keys())
means = [gini_means[n] for n in names]
stds = [gini_stds[n] for n in names]
bars = plt.bar(names, means, yerr=stds, capsize=6,
               color=['#e74c3c','#2ecc71','#3498db','#9b59b6','#f39c12'])
plt.ylabel('Gini Coefficient (comfort inequality)')
plt.title('Inequality Across Community Types (Mean ± Std, 5 seeds)')
plt.grid(axis='y', alpha=0.3)
for bar, val, std in zip(bars, means, stds):
    plt.text(bar.get_x()+bar.get_width()/2., bar.get_height()+std+0.002,
             f'{val:.4f} ± {std:.4f}', ha='center', fontweight='bold', fontsize=8)
plt.tight_layout()
plt.savefig('results/gini_comparison.png', dpi=150)
plt.close()

# ========== 5. SHARING FREQUENCY RESULTS ==========
print("\n" + "=" * 60)
print("SHARING FREQUENCY RESULTS (Mean ± Std across 5 seeds)")
print("=" * 60)

# Define agent group indices for each scenario
group_defs = {
    'All Selfish': [('All Agents', range(0, 10))],
    'All Prosocial': [('All Agents', range(0, 10))],
    'Mixed': [('Prosocial', range(0, 5)), ('Selfish', range(5, 10))],
    'Varied Altruism': [('Prosocial Group', range(0, 4)), ('Selfish Group', range(4, 10))],
    'Innovator Effect': [('Explorers', range(0, 5)), ('Selfish', range(5, 10))],
}

for name in scenarios:
    print(f"\n  {name}:")
    all_sharing = np.array(sharing_results[name])  # shape (5 seeds, 10 agents)
    for group_label, idx_range in group_defs[name]:
        group_vals = all_sharing[:, list(idx_range)]
        overall_mean = np.mean(group_vals)
        overall_std = np.std(group_vals)
        print(f"    {group_label:20s}: {overall_mean:.4f} ± {overall_std:.4f}")

# Plot Sharing Frequency per agent group with error bars
fig, ax = plt.subplots(figsize=(12, 6))
labels = [
    'All Selfish', 'All Prosocial',
    'Mixed\n(Prosocial)', 'Mixed\n(Selfish)',
    'Varied\n(Prosocial)', 'Varied\n(Selfish)',
    'Innovator\n(Explorers)', 'Innovator\n(Selfish)'
]

# Compute per-group mean and std across seeds for the plot
all_sharing_arr = {name: np.array(sharing_results[name]) for name in scenarios}  # (5, 10)

def group_stats(scenario, idx_range):
    vals = all_sharing_arr[scenario][:, idx_range]
    return np.mean(vals), np.std(vals)

freq_means = [
    group_stats('All Selfish', range(0, 10))[0],
    group_stats('All Prosocial', range(0, 10))[0],
    group_stats('Mixed', range(0, 5))[0],
    group_stats('Mixed', range(5, 10))[0],
    group_stats('Varied Altruism', range(0, 4))[0],
    group_stats('Varied Altruism', range(4, 10))[0],
    group_stats('Innovator Effect', range(0, 5))[0],
    group_stats('Innovator Effect', range(5, 10))[0],
]
freq_stds = [
    group_stats('All Selfish', range(0, 10))[1],
    group_stats('All Prosocial', range(0, 10))[1],
    group_stats('Mixed', range(0, 5))[1],
    group_stats('Mixed', range(5, 10))[1],
    group_stats('Varied Altruism', range(0, 4))[1],
    group_stats('Varied Altruism', range(4, 10))[1],
    group_stats('Innovator Effect', range(0, 5))[1],
    group_stats('Innovator Effect', range(5, 10))[1],
]

colors = ['#e74c3c', '#2ecc71', '#3498db', '#e74c3c', '#3498db', '#e74c3c', '#9b59b6', '#e74c3c']
ax.bar(range(8), freq_means, yerr=freq_stds, capsize=6, color=colors)
ax.set_xticks(range(8))
ax.set_xticklabels(labels, rotation=30, ha='right', fontsize=10)
ax.set_ylabel('Proportion of states where best action is Share')
ax.set_title('Learned Sharing Behaviour by Agent Type (Mean ± Std, 5 seeds)')
ax.grid(axis='y', alpha=0.3)
for i, (m, s) in enumerate(zip(freq_means, freq_stds)):
    ax.text(i, m + s + 0.005, f'{m:.3f} ± {s:.3f}', ha='center', fontsize=8)
plt.tight_layout()
plt.savefig('results/sharing_frequency.png', dpi=150)
plt.close()

# ========== 4. SENSITIVITY TO CLOUD PROBABILITY ==========
cloud_probs = [0.15, 0.25, 0.35]
seeds = [42, 123, 456, 789, 1011]

sensitivity_data = {cp: {'prosocial':[], 'selfish':[]} for cp in cloud_probs}

for cp in cloud_probs:
    for seed in seeds:
        print(f"Running mixed scenario with cloud_prob={cp}, seed={seed}...")
        agents, _, history = run_simulation(
            num_houses=10, episodes=8000, battery_cap=7.0, solar_max=1.3,
            personality_mix=['prosocial']*5+['pure_selfish']*5,
            seed=seed, verbose=False,
            weather_cloud_prob=cp)
        last_n = 1000
        pro_comf = np.mean([np.mean(history['agent_comforts'][i][-last_n:]) for i in range(5)])
        self_comf = np.mean([np.mean(history['agent_comforts'][i][-last_n:]) for i in range(5,10)])
        sensitivity_data[cp]['prosocial'].append(pro_comf)
        sensitivity_data[cp]['selfish'].append(self_comf)

# Compute means and stds
cp_labels = [f'{int(cp*100)}%' for cp in cloud_probs]
pro_means = [np.mean(sensitivity_data[cp]['prosocial']) for cp in cloud_probs]
self_means = [np.mean(sensitivity_data[cp]['selfish']) for cp in cloud_probs]
pro_stds = [np.std(sensitivity_data[cp]['prosocial']) for cp in cloud_probs]
self_stds = [np.std(sensitivity_data[cp]['selfish']) for cp in cloud_probs]

x = np.arange(len(cloud_probs))
width = 0.35

fig, ax = plt.subplots(figsize=(8,5))
bars1 = ax.bar(x - width/2, pro_means, width, yerr=pro_stds,
               label='Prosocial', color='#3498db', capsize=6)
bars2 = ax.bar(x + width/2, self_means, width, yerr=self_stds,
               label='Selfish', color='#e74c3c', capsize=6)

ax.set_xticks(x)
ax.set_xticklabels(cp_labels)
ax.set_xlabel('Cloudy Day Probability')
ax.set_ylabel('Final Comfort')
ax.set_title('Personality Gap Grows with Scarcity')
ax.legend()
ax.grid(axis='y', alpha=0.3)
ax.set_ylim(0.7, 1.0)
for bar, val, std in zip(bars1, pro_means, pro_stds):
    ax.text(bar.get_x()+bar.get_width()/2., bar.get_height()+std+0.005,
            f'{val:.3f}', ha='center', fontsize=9)
for bar, val, std in zip(bars2, self_means, self_stds):
    ax.text(bar.get_x()+bar.get_width()/2., bar.get_height()+std+0.005,
            f'{val:.3f}', ha='center', fontsize=9)
plt.tight_layout()
plt.savefig('results/sensitivity_cloud.png', dpi=150)
plt.close()

print("\nAll advanced analyses complete. Plots saved in results/")