import numpy as np
import matplotlib.pyplot as plt
import os, json
from offgrid_marl import run_simulation, PERSONALITIES, DEMAND_PROFILES

# ========== 1. GINI COEFFICIENT FUNCTION ==========
def gini(x):
    """Compute Gini coefficient of an array of values."""
    x = np.array(x, dtype=float)
    if np.amin(x) < 0:
        x -= np.amin(x)   # shift to non-negative
    x += 1e-10   # avoid zero
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

    # Gini over last 1000 episodes
    last_comforts = history['agent_comforts']   # list of lists per agent
    last_1000 = slice(-1000, None)
    ginis = []
    for ep_comforts in zip(*[c[last_1000] for c in last_comforts]):
        ginis.append(gini(ep_comforts))
    mean_gini = np.mean(ginis)

    # Sharing frequency from Q-tables
    sharing_freqs = []
    for agent in agents:
        # Count state-action pairs where best action is index 1 or 2 (share 0.5 or 1.0)
        best_actions = np.argmax(agent.q, axis=2)   # shape (24, 4)
        share_count = np.sum(best_actions >= 1)     # action 1 or 2
        total_states = best_actions.size
        sharing_freqs.append(share_count / total_states)
    
    return mean_gini, np.array(sharing_freqs)

# ========== 3. RUN GINI & SHARING ANALYSIS ==========
scenarios = {
    'All Selfish': ['pure_selfish']*10,
    'All Prosocial': ['prosocial']*10,
    'Mixed': ['prosocial']*5 + ['pure_selfish']*5,
    'Varied Altruism': ['altruistic', 'prosocial', 'prosocial', 'prosocial', 'individualist', 'individualist', 'individualist', 'pure_selfish', 'pure_selfish', 'pure_selfish'],
    'Innovator Effect': ['high_openness_innovator'] + ['prosocial']*4 + ['individualist']*3 + ['pure_selfish']*2
}

gini_results = {}
sharing_results = {}

for name, mix in scenarios.items():
    print(f"Analyzing {name}...")
    mean_gini, sharing_freq = analyze_scenario_gini_and_sharing(name, mix)
    gini_results[name] = mean_gini
    sharing_results[name] = sharing_freq
    print(f"  Gini: {mean_gini:.4f}")
    print(f"  Sharing frequencies: {sharing_freq}")

# Plot Gini
plt.figure(figsize=(8,5))
bars = plt.bar(gini_results.keys(), gini_results.values(),
               color=['#e74c3c','#2ecc71','#3498db','#9b59b6','#f39c12'])
plt.ylabel('Gini Coefficient (comfort inequality)')
plt.title('Inequality Across Community Types')
plt.grid(axis='y', alpha=0.3)
for bar, val in zip(bars, gini_results.values()):
    plt.text(bar.get_x()+bar.get_width()/2., bar.get_height()+0.002,
             f'{val:.3f}', ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('results/gini_comparison.png', dpi=150)
plt.show()

# Plot Sharing Frequency per agent type
fig, ax = plt.subplots(figsize=(12,6))
# Group sharing frequencies: for mixed, varied, innovator separate prosocial vs selfish
labels = ['All Selfish','All Prosocial',
          'Mixed\n(Prosocial)','Mixed\n(Selfish)',
          'Varied\n(Prosocial)','Varied\n(Selfish)',
          'Innovator\n(Explorers)','Innovator\n(Selfish)']
freqs = [
    np.mean(sharing_results['All Selfish']),
    np.mean(sharing_results['All Prosocial']),
    np.mean(sharing_results['Mixed'][:5]),        # first 5 are prosocial
    np.mean(sharing_results['Mixed'][5:]),        # last 5 are selfish
    np.mean(sharing_results['Varied Altruism'][:4]),  # altruistic+3 prosocial
    np.mean(sharing_results['Varied Altruism'][4:]),  # 3 individualist+3 selfish
    np.mean(sharing_results['Innovator Effect'][:5]), # innovator+4 prosocial
    np.mean(sharing_results['Innovator Effect'][5:]), # 3 individualist+2 selfish
]
colors = ['#e74c3c','#2ecc71','#3498db','#e74c3c','#3498db','#e74c3c','#9b59b6','#e74c3c']
ax.bar(range(8), freqs, color=colors)
ax.set_xticks(range(8))
ax.set_xticklabels(labels, rotation=30, ha='right', fontsize=10)
ax.set_ylabel('Proportion of states where best action is Share')
ax.set_title('Learned Sharing Behaviour by Agent Type')
ax.grid(axis='y', alpha=0.3)
for i, v in enumerate(freqs):
    ax.text(i, v+0.01, f'{v:.3f}', ha='center')
plt.tight_layout()
plt.savefig('results/sharing_frequency.png', dpi=150)
plt.show()

# ========== 4. SENSITIVITY TO CLOUD PROBABILITY ==========
cloud_probs = [0.15, 0.25, 0.35]
seeds = [42, 123, 456]

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
ax.set_ylim(bottom=0.85, top=1.0)   # adjust based on your data
for bar, val in zip(bars1, pro_means):
    ax.text(bar.get_x()+bar.get_width()/2., bar.get_height()+0.002,
            f'{val:.3f}', ha='center', fontsize=9)
for bar, val in zip(bars2, self_means):
    ax.text(bar.get_x()+bar.get_width()/2., bar.get_height()+0.002,
            f'{val:.3f}', ha='center', fontsize=9)
plt.tight_layout()
plt.savefig('results/sensitivity_cloud.png', dpi=150)
plt.show()

print("\nAll advanced analyses complete. Plots saved in results/")