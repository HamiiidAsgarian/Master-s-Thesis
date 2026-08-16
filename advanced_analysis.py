import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, json, csv
from scipy import stats

from thesis_plot_style import apply_rc, save_fig

apply_rc()

# ========== CONFIGURATION ==========
scenarios = ['all_selfish', 'all_prosocial', 'mixed', 'varied_altruism', 'innovator_effect']
base_dir = 'results'

# ========== 1. Q-TABLE HEATMAPS (from saved .npy — same source as generate_all_Visuals2.py) ==========
# Thesis figure 4-7 consumes results/qtable_heatmaps.png. Regenerate via:
#   python generate_all_Visuals2.py
# This block remains for backward compatibility when advanced_analysis.py is run alone.

def plot_qtable_heatmaps_from_npy(save_path='results/qtable_heatmaps.png'):
    h_scenarios = ['all_selfish', 'all_prosocial', 'mixed', 'varied_altruism', 'innovator_effect']
    h_mixes = {
        'all_selfish': ['pure_selfish'] * 10,
        'all_prosocial': ['prosocial'] * 10,
        'mixed': ['prosocial'] * 5 + ['pure_selfish'] * 5,
        'varied_altruism': ['altruistic', 'prosocial', 'prosocial', 'prosocial',
                            'individualist', 'individualist', 'individualist',
                            'pure_selfish', 'pure_selfish', 'pure_selfish'],
        'innovator_effect': ['high_openness_innovator'] + ['prosocial'] * 4 +
                            ['individualist'] * 3 + ['pure_selfish'] * 2,
    }
    en_labels = {
        'all_selfish': 'All Selfish', 'all_prosocial': 'All Prosocial',
        'mixed': 'Mixed', 'varied_altruism': 'Varied Altruism',
        'innovator_effect': 'Innovator Effect',
    }
    fig, axes = plt.subplots(2, 5, figsize=(24, 10))
    for i, sc in enumerate(h_scenarios):
        q = np.load(os.path.join(base_dir, 'analysis_support/qtab', f'{sc}_q.npy'))
        counterpart = 8 if sc == 'innovator_effect' else 3
        for row, house in enumerate([0, counterpart]):
            q_avg = q[0, house].mean(axis=1)
            ax = axes[row, i]
            im = ax.imshow(q_avg.T, aspect='auto', cmap='YlOrRd', origin='lower',
                           extent=[0, 23, 0, 2], interpolation='nearest')
            ax.set_xticks([0, 6, 12, 18, 23])
            ax.set_yticks([0, 1, 2])
            ax.set_yticklabels(['Share 0%', 'Share 50%', 'Share 100%'], fontsize=8)
            ax.set_xlabel('Hour of Day', fontsize=9)
            ax.set_title(f"{en_labels[sc]}\nAgent {house} ({h_mixes[sc][house]})",
                         fontweight='bold', fontsize=10)
            cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
            cbar.set_label('Mean Q-value', fontsize=8)
            cbar.ax.tick_params(labelsize=7)
    fig.suptitle('Q-table Heatmaps: Average Action Values by Hour\n'
                 '(mean over battery levels; seed 42)',
                 fontsize=13, fontweight='bold')
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    save_fig(fig, save_path)
    plt.close(fig)
    print(f"Saved {save_path}")

print("Plotting Q-table heatmaps from saved analysis_support/qtab/*.npy ...")
plot_qtable_heatmaps_from_npy()

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