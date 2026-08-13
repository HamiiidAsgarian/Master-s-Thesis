import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, json, csv
from scipy import stats

# ========== CONFIGURATION ==========
scenarios = ['all_selfish', 'all_prosocial', 'mixed', 'varied_altruism', 'innovator_effect']
base_dir = 'results'

# Re‑run a single simulation with verbose=False to get the final agents
# We'll load one seed per scenario and plot the first agent's Q‑table.

from offgrid_marl import run_simulation

def get_agents_for_scenario(scenario_name, mix, seed=42):
    """Run a short simulation and return the trained agents."""
    agents, community, history = run_simulation(
        num_houses=10, episodes=8000, battery_cap=7.0, solar_max=1.3,
        personality_mix=mix, seed=seed, verbose=False
    )
    return agents

# ========== 1. Q‑TABLE HEATMAPS ==========
mixes = {
    'all_selfish': ['pure_selfish']*10,
    'all_prosocial': ['prosocial']*10,
    'mixed': ['prosocial']*5 + ['pure_selfish']*5,
    'varied_altruism': ['altruistic', 'prosocial', 'prosocial', 'prosocial', 'individualist', 'individualist', 'individualist', 'pure_selfish', 'pure_selfish', 'pure_selfish'],
    'innovator_effect': ['high_openness_innovator'] + ['prosocial']*4 + ['individualist']*3 + ['pure_selfish']*2
}

fig, axes = plt.subplots(2, 5, figsize=(24, 10))
plot_idx = 0

for scenario_name in ['all_selfish', 'all_prosocial', 'mixed', 'varied_altruism', 'innovator_effect']:
    print(f"Training agents for {scenario_name} heatmap...")
    agents = get_agents_for_scenario(scenario_name, mixes[scenario_name], seed=42)
    
    # Plot agent 0 (prosocial/selfish depending on scenario)
    agent0 = agents[0]
    # Average Q-values across battery levels for each action
    q_avg = np.mean(agent0.q, axis=1)  # shape (24, 3)
    
    ax = axes[0, plot_idx]
    im = ax.imshow(q_avg.T, aspect='auto', cmap='YlOrRd', origin='lower',
                   extent=[0, 23, 0, 2])
    ax.set_xticks([0, 6, 12, 18, 23])
    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(['Share 0%', 'Share 50%', 'Share 100%'])
    ax.set_xlabel('Hour of Day')
    ax.set_title(f'{scenario_name}\nAgent 0 ({mixes[scenario_name][0]})')
    plt.colorbar(im, ax=ax, label='Avg Q-value')
    
    # Plot agent 3 (other type in mixed scenarios)
    if len(agents) > 3:
        agent3 = agents[3]
        q_avg3 = np.mean(agent3.q, axis=1)
        
        ax2 = axes[1, plot_idx]
        im2 = ax2.imshow(q_avg3.T, aspect='auto', cmap='YlOrRd', origin='lower',
                        extent=[0, 23, 0, 2])
        ax2.set_xticks([0, 6, 12, 18, 23])
        ax2.set_yticks([0, 1, 2])
        ax2.set_yticklabels(['Share 0%', 'Share 50%', 'Share 100%'])
        ax2.set_xlabel('Hour of Day')
        ax2.set_title(f'{scenario_name}\nAgent 3 ({mixes[scenario_name][3]})')
        plt.colorbar(im2, ax=ax2, label='Avg Q-value')
    
    plot_idx += 1

plt.suptitle('Q‑table Heatmaps: Average Action Values by Hour', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('results/qtable_heatmaps.png', dpi=150, bbox_inches='tight')
plt.show()

# ========== 2. STATISTICAL TESTS ==========
print("\n" + "="*80)
print("STATISTICAL TESTS")
print("="*80)

# Load all data
all_data = {}
for scenario in scenarios:
    metrics_list = []
    for seed_folder in os.listdir(os.path.join(base_dir, scenario)):
        csv_path = os.path.join(base_dir, scenario, seed_folder, 'final_metrics.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            metrics_list.append(df.iloc[0].to_dict())
    if metrics_list:
        all_data[scenario] = pd.DataFrame(metrics_list)

# Test 1: All-selfish vs All-prosocial (comfort)
print("\n1. All-Selfish vs All-Prosocial Community Comfort:")
t_stat, p_val = stats.ttest_ind(all_data['all_selfish']['comfort'],
                                 all_data['all_prosocial']['comfort'])
print(f"   t = {t_stat:.3f}, p = {p_val:.4f}")
if p_val < 0.05:
    print("   → Statistically significant difference (p < 0.05)")
else:
    print("   → No significant difference")

# Test 2: Prosocial vs Selfish comfort in Mixed scenario
print("\n2. Prosocial vs Selfish Comfort in Mixed Community:")
t_stat, p_val = stats.ttest_rel(all_data['mixed']['prosocial_comfort'],
                                 all_data['mixed']['selfish_comfort'])
print(f"   t = {t_stat:.3f}, p = {p_val:.4f}")
if p_val < 0.05:
    print("   → Statistically significant difference (p < 0.05)")
else:
    print("   → No significant difference")

# Test 3: Prosocial vs Selfish comfort in Varied Altruism
print("\n3. Prosocial vs Selfish Comfort in Varied Altruism:")
t_stat, p_val = stats.ttest_rel(all_data['varied_altruism']['prosocial_comfort'],
                                 all_data['varied_altruism']['selfish_comfort'])
print(f"   t = {t_stat:.3f}, p = {p_val:.4f}")
if p_val < 0.05:
    print("   → Statistically significant difference (p < 0.05)")
else:
    print("   → No significant difference")

# Test 4: Innovator Effect vs Mixed community comfort
print("\n4. Innovator Effect vs Mixed Community Comfort:")
t_stat, p_val = stats.ttest_ind(all_data['innovator_effect']['comfort'],
                                 all_data['mixed']['comfort'])
print(f"   t = {t_stat:.3f}, p = {p_val:.4f}")
if p_val < 0.05:
    print("   → Statistically significant difference (p < 0.05)")
else:
    print("   → No significant difference")

# Test 5: Community comfort comparison across all scenarios (ANOVA)
print("\n5. One‑way ANOVA: Community Comfort across all scenarios:")
scenario_comforts = [all_data[s]['comfort'].values for s in scenarios]
f_stat, p_val = stats.f_oneway(*scenario_comforts)
print(f"   F = {f_stat:.3f}, p = {p_val:.4f}")
if p_val < 0.05:
    print("   → Significant differences exist among scenarios")
else:
    print("   → No significant differences")

# Save test results
results_text = []
results_text.append("STATISTICAL TEST RESULTS")
results_text.append("="*60)

t1 = stats.ttest_ind(all_data['all_selfish']['comfort'], all_data['all_prosocial']['comfort'])
results_text.append(f"\n1. All-Selfish vs All-Prosocial Comfort: t={t1.statistic:.3f}, p={t1.pvalue:.4f}")

t2 = stats.ttest_rel(all_data['mixed']['prosocial_comfort'], all_data['mixed']['selfish_comfort'])
results_text.append(f"\n2. Mixed Prosocial vs Selfish: t={t2.statistic:.3f}, p={t2.pvalue:.4f}")

t3 = stats.ttest_rel(all_data['varied_altruism']['prosocial_comfort'], all_data['varied_altruism']['selfish_comfort'])
results_text.append(f"\n3. Varied Prosocial vs Selfish: t={t3.statistic:.3f}, p={t3.pvalue:.4f}")

t4 = stats.ttest_ind(all_data['innovator_effect']['comfort'], all_data['mixed']['comfort'])
results_text.append(f"\n4. Innovator vs Mixed Community Comfort: t={t4.statistic:.3f}, p={t4.pvalue:.4f}")

f_stat, p_val = stats.f_oneway(*scenario_comforts)
results_text.append(f"\n5. ANOVA all scenarios: F={f_stat:.3f}, p={p_val:.4f}")

with open('results/statistical_tests.txt', 'w') as f:
    f.write('\n'.join(results_text))

print("\nResults saved to results/statistical_tests.txt")
print("="*80)