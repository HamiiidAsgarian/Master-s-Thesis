import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, json

# ========== CONFIGURATION ==========
scenarios = ['all_selfish', 'all_prosocial', 'mixed', 'varied_altruism', 'innovator_effect']
scenario_labels = {
    'all_selfish': 'All Selfish',
    'all_prosocial': 'All Prosocial',
    'mixed': 'Mixed\n(5 Prosocial + 5 Selfish)',
    'varied_altruism': 'Varied Altruism\n(1 Altruistic, 3 Prosocial,\n3 Individualist, 3 Selfish)',
    'innovator_effect': 'Innovator Effect\n(1 High-O, 4 Prosocial,\n3 Individualist, 2 Selfish)'
}
base_dir = 'results'

# ========== LOAD DATA ==========
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

# ========== PLOT 1: Comfort Comparison ==========
fig, axes = plt.subplots(1, 3, figsize=(16, 6))
colors_scenarios = ['#e74c3c', '#2ecc71', '#3498db', '#9b59b6', '#f39c12']

# 1a. Mean Community Comfort
ax = axes[0]
x_pos = np.arange(len(scenarios))
comfort_means = [all_data[s]['comfort'].mean() for s in scenarios]
comfort_stds = [all_data[s]['comfort'].std() for s in scenarios]
bars = ax.bar(x_pos, comfort_means, yerr=comfort_stds, 
              color=colors_scenarios, capsize=8, alpha=0.8)
ax.set_xticks(x_pos)
ax.set_xticklabels([scenario_labels[s] for s in scenarios], fontsize=9)
ax.set_ylabel('Mean Comfort')
ax.set_title('Community Comfort by Scenario')
ax.set_ylim([0, 1])
ax.grid(axis='y', alpha=0.3)
for bar, val in zip(bars, comfort_means):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.02,
            f'{val:.3f}', ha='center', fontweight='bold')

# 1b. Jain's Fairness
ax = axes[1]
fairness_means = [all_data[s]['fairness'].mean() for s in scenarios]
fairness_stds = [all_data[s]['fairness'].std() for s in scenarios]
bars = ax.bar(x_pos, fairness_means, yerr=fairness_stds,
              color=colors_scenarios, capsize=8, alpha=0.8)
ax.set_xticks(x_pos)
ax.set_xticklabels([scenario_labels[s] for s in scenarios], fontsize=9)
ax.set_ylabel("Jain's Fairness Index")
ax.set_title('Community Fairness by Scenario')
ax.set_ylim([0, 1])
ax.grid(axis='y', alpha=0.3)
for bar, val in zip(bars, fairness_means):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.02,
            f'{val:.3f}', ha='center', fontweight='bold')

# 1c. Blackout Rate
ax = axes[2]
blackout_means = [all_data[s]['blackout_rate'].mean() * 100 for s in scenarios]
blackout_stds = [all_data[s]['blackout_rate'].std() * 100 for s in scenarios]
bars = ax.bar(x_pos, blackout_means, yerr=blackout_stds,
              color=colors_scenarios, capsize=8, alpha=0.8)
ax.set_xticks(x_pos)
ax.set_xticklabels([scenario_labels[s] for s in scenarios], fontsize=9)
ax.set_ylabel('Blackout Rate (%)')
ax.set_title('Blackout Frequency by Scenario')
ax.grid(axis='y', alpha=0.3)
for bar, val in zip(bars, blackout_means):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
            f'{val:.1f}%', ha='center', fontweight='bold')

plt.suptitle('Community-Level Metrics Across Scenarios', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('results/community_metrics.png', dpi=150, bbox_inches='tight')
plt.show()

# ========== PLOT 2: Agent-Type Comfort Comparison ==========
fig, ax = plt.subplots(figsize=(10, 6))

# Only mixed, varied_altruism, and innovator_effect have meaningful agent-type splits
scenarios_with_types = ['mixed', 'varied_altruism', 'innovator_effect']
x_labels = []
prosocial_means = []
selfish_means = []
prosocial_stds = []
selfish_stds = []

for s in scenarios_with_types:
    if s in all_data:
        x_labels.append(scenario_labels[s])
        prosocial_means.append(all_data[s]['prosocial_comfort'].mean())
        selfish_means.append(all_data[s]['selfish_comfort'].mean())
        prosocial_stds.append(all_data[s]['prosocial_comfort'].std())
        selfish_stds.append(all_data[s]['selfish_comfort'].std())

x_pos = np.arange(len(x_labels))
width = 0.35

bars1 = ax.bar(x_pos - width/2, prosocial_means, width, yerr=prosocial_stds,
               label='Prosocial', color='#3498db', capsize=6, alpha=0.8)
bars2 = ax.bar(x_pos + width/2, selfish_means, width, yerr=selfish_stds,
               label='Selfish', color='#e74c3c', capsize=6, alpha=0.8)

ax.set_xticks(x_pos)
ax.set_xticklabels(x_labels, fontsize=10)
ax.set_ylabel('Mean Comfort')
ax.set_title('Comfort by Personality Type (Mixed Communities)')
ax.legend()
ax.set_ylim([0, 1])
ax.grid(axis='y', alpha=0.3)

for bar, val in zip(bars1, prosocial_means):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.02,
            f'{val:.3f}', ha='center', fontsize=9)
for bar, val in zip(bars2, selfish_means):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.02,
            f'{val:.3f}', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('results/agent_type_comfort.png', dpi=150, bbox_inches='tight')
plt.show()

# ========== PRINT SUMMARY TABLE ==========
print("\n" + "="*80)
print("SUMMARY STATISTICS (Mean ± Std across seeds)")
print("="*80)
for scenario in scenarios:
    if scenario in all_data:
        df = all_data[scenario]
        print(f"\n{scenario_labels[scenario].replace(chr(10), ' ')}:")
        print(f"  Comfort:      {df['comfort'].mean():.3f} ± {df['comfort'].std():.3f}")
        print(f"  Fairness:     {df['fairness'].mean():.3f} ± {df['fairness'].std():.3f}")
        print(f"  Blackout Rate: {df['blackout_rate'].mean()*100:.1f}% ± {df['blackout_rate'].std()*100:.1f}%")
        print(f"  Waste:        {df['waste'].mean():.2f} ± {df['waste'].std():.2f} kWh")
        if 'prosocial_comfort' in df.columns:
            print(f"  Prosocial:    {df['prosocial_comfort'].mean():.3f} ± {df['prosocial_comfort'].std():.3f}")
            print(f"  Selfish:      {df['selfish_comfort'].mean():.3f} ± {df['selfish_comfort'].std():.3f}")
            diff = df['prosocial_comfort'].mean() - df['selfish_comfort'].mean()
            print(f"  Difference:   {diff:.3f}")

print("\n" + "="*80)
print("Analysis complete! Plots saved in results/")
print("="*80)