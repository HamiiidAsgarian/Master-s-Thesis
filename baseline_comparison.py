import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, csv
from scipy import stats

BASE = 'results'
MAIN_SCENARIOS = ['all_selfish', 'all_prosocial', 'mixed', 'varied_altruism',
                  'innovator_effect']
MAIN_LABELS = {
    'all_selfish': 'OCEAN-MARL all-selfish',
    'all_prosocial': 'OCEAN-MARL all-prosocial',
    'mixed': 'OCEAN-MARL mixed',
    'varied_altruism': 'OCEAN-MARL varied-altruism',
    'innovator_effect': 'OCEAN-MARL innovator-effect',
}
BASELINES = [
    ('baseline_charbonnier', 'Charbonnier marginal-IQL'),
    ('baseline_kusatake', 'Kusatake NSGA-II'),
    ('baseline_behrunani', 'Behrunani GNE'),
    ('baseline_may_huang', 'May & Huang PPO'),
]
CONTROL = ('control_always_default', 'always_default (control)')
SEEDS = [42, 123, 456, 789, 1011]


def load_group(folder, label):
    rows = []
    for seed in SEEDS:
        path = os.path.join(BASE, folder, f'seed_{seed}', 'final_metrics.csv')
        if not os.path.exists(path):
            continue
        with open(path) as fh:
            d = next(csv.DictReader(fh))
        rows.append({
            'method': label,
            'seed': seed,
            'comfort': float(d['comfort']),
            'fairness': float(d['fairness']),
            'F': float(d.get('F', float(d['comfort']) + float(d['fairness']))),
            'blackout_rate': float(d['blackout_rate']),
            'waste': float(d['waste']),
        })
    return pd.DataFrame(rows)


# ========== ISOLATION 2x2 (single-seed sanity, seed 42) ==========
def load_single(folder):
    path = os.path.join(BASE, folder, 'final_metrics.csv')
    with open(path) as fh:
        d = next(csv.DictReader(fh))
    return {'comfort': float(d['comfort']), 'fairness': float(d['fairness']),
            'F': float(d.get('F', float(d['comfort']) + float(d['fairness']))),
            'waste': float(d['waste'])}


def isolation_block():
    cells = {
        'A  personality x per-step (main, mixed)': None,
        'B  personality x end-of-day (sanity)': 'ocean_marl_endofday_sanity',
        'C  community x end-of-day, Charbonnier learner': 'baseline_charbonnier/seed_42',
        'D  community x end-of-day, OCEAN-MARL learner (mixed env)':
            'ocean_marl_endofday_sanity_community',
        'D2 community x end-of-day, OCEAN-MARL learner (HOMOGENEOUS env)':
            'ocean_marl_endofday_sanity_community_homogeneous',
    }
    # A from main mixed seed_42
    mp = os.path.join(BASE, 'mixed', 'seed_42', 'final_metrics.csv')
    with open(mp) as fh:
        d = next(csv.DictReader(fh))
    cells['A  personality x per-step (main, mixed)'] = {'comfort': float(d['comfort']),
                                                        'fairness': float(d['fairness']),
                                                        'waste': float(d['waste'])}
    # Charbonnier greedy eval from validation report
    char = None
    vf = os.path.join(BASE, 'baseline_charbonnier_validation', 'validation_report.txt')
    if os.path.exists(vf):
        with open(vf) as fh:
            for line in fh:
                if 'Learned greedy policy: F=' in line:
                    char = float(line.split('F=')[1].split()[0])

    def greedy_from_report(report_path):
        fp = os.path.join(BASE, report_path)
        if not os.path.exists(fp):
            return None
        with open(fp) as fh:
            for line in fh:
                if 'Learned greedy (end-of-day): F=' in line:
                    return float(line.split('F=')[1].split()[0])
        return None

    greedy_refs = {
        'ocean_marl_endofday_sanity': 'ocean_marl_endofday_sanity/sanity_report.txt',
        'ocean_marl_endofday_sanity_community':
            'ocean_marl_endofday_sanity_community/sanity_report.txt',
        'ocean_marl_endofday_sanity_community_homogeneous':
            'ocean_marl_endofday_sanity_community_homogeneous/sanity_report.txt',
    }

    lines = ["\n" + "=" * 100,
             "ISOLATION 2x2: objective x reward horizon  (seed 42, matched eval; "
             "greedy F vs always_default F=1.8850)",
             "=" * 100]
    lines.append(f"{'cell':>52} | {'train F':>8} | {'greedy F':>8} | {'gain':>7} | "
                 f"{'comfort':>7} | {'waste':>6}")
    lines.append('-' * len(lines[-1]))
    for label, info in cells.items():
        if isinstance(info, str):
            r = load_single(info)
            trainF = r['F']
            g = greedy_from_report(greedy_refs[info]) if info in greedy_refs else None
            greedy, gain = (g, g - 1.8850) if g is not None else (float('nan'), float('nan'))
            if char is not None and 'Charbonnier' in label:
                greedy, gain = char, char - 1.8850
            info = r
        else:
            trainF = info['comfort'] + info['fairness']
            greedy, gain = float('nan'), float('nan')
        lines.append(f"{label:>52} | {trainF:8.4f} | {greedy:8.4f} | {gain:+7.4f} | "
                     f"{info['comfort']:7.4f} | {info['waste']:6.2f}")
    lines.append("Greedy gains read from saved sanity reports: B=+0.0000, "
                 "D=+0.0000, D2=+0.0000; C=+0.0207 (76.4% sharing).")
    return lines


def main():
    extra = isolation_block()
    groups = []
    for sc in MAIN_SCENARIOS:
        groups.append(load_group(sc, MAIN_LABELS[sc]))
    for folder, label in BASELINES:
        groups.append(load_group(folder, label))
    groups.append(load_group(CONTROL[0], CONTROL[1]))
    df = pd.concat(groups, ignore_index=True)
    df.to_csv(os.path.join(BASE, 'baseline_comparison.csv'), index=False)

    methods = [g['method'].iloc[0] for g in groups]
    n = len(methods)

    lines = []
    lines.append("=" * 100)
    lines.append("BASELINE + CONTROL COMPARISON  (identical env: 10 houses, PV 1.3 kW,"
                 " battery 7 kWh, cloud 0.15; 5 seeds)")
    lines.append("=" * 100)

    header = f"{'method':>28} | {'comfort':>11} | {'fairness':>11} | {'F':>11} | {'blackout%':>9} | {'waste':>9}"
    lines.append(header)
    lines.append('-' * len(header))
    for m in methods:
        g = df[df['method'] == m]
        c, f, F, bl, wa = (g['comfort'].mean(), g['fairness'].mean(),
                           g['F'].mean(), g['blackout_rate'].mean() * 100,
                           g['waste'].mean())
        cs, fs, Fs, bls, was = (g['comfort'].std(), g['fairness'].std(),
                                g['F'].std(), g['blackout_rate'].std() * 100,
                                g['waste'].std())
        lines.append(f"{m:>28} | {c:6.4f}±{cs:.4f} | {f:6.4f}±{fs:.4f} | "
                     f"{F:6.4f}±{Fs:.4f} | {bl:5.1f}±{bls:.1f} | {wa:5.2f}±{was:.2f}")
    lines.append('-' * len(header))

    ctrl = df[df['method'] == CONTROL[1]].set_index('seed')
    lines.append("\nGAIN OVER always_default control (method - control, per seed, mean±std):")
    ghead = f"{'method':>28} | {'dF':>9} | {'dcomfort':>10} | {'dwaste (kWh)':>13}"
    lines.append(ghead)
    lines.append('-' * len(ghead))
    for m in methods:
        if m == CONTROL[1]:
            continue
        g = df[df['method'] == m].set_index('seed')
        dF = (g['F'] - ctrl['F'])
        dC = (g['comfort'] - ctrl['comfort'])
        dW = (g['waste'] - ctrl['waste'])
        lines.append(f"{m:>28} | {dF.mean():+7.4f}±{dF.std():.4f} | "
                     f"{dC.mean():+7.4f}±{dC.std():.4f} | {dW.mean():+8.2f}±{dW.std():.2f}")

    # ========== STATISTICS ==========
    lines.append("\n" + "=" * 100)
    lines.append("STATISTICAL TESTS (5 seeds per group; seed-matched pairs for "
                 "baselines/control vs main)")
    lines.append("=" * 100)

    # ANOVA across all groups on F, comfort, waste
    for metric in ['F', 'comfort', 'waste']:
        groups_v = [df[df['method'] == m][metric].values for m in methods]
        Fs, p = stats.f_oneway(*groups_v)
        lines.append(f"\nOne-way ANOVA on {metric} across {n} groups: "
                     f"F={Fs:.3f}, p={p:.4f} "
                     + ("-> significant" if p < 0.05 else "-> not significant"))

    # Paired (seed-matched) two-sample tests vs control
    lines.append("\nPaired t-tests vs always_default control (seed-matched):")
    for m in methods:
        if m == CONTROL[1]:
            continue
        g = df[df['method'] == m].set_index('seed')
        for metric, lab in [('F', 'F'), ('comfort', 'comfort')]:
            t, p = stats.ttest_rel(g[metric], ctrl[metric])
            sig = 'SIG' if p < 0.05 else 'ns'
            lines.append(f"  {m:>28} vs control ({metric:>7}): t={t:+6.3f} p={p:.4f} [{sig}]")

    # Headline comparisons between the working baselines and main mixed
    mixed = df[df['method'] == MAIN_LABELS['mixed']].set_index('seed')
    lines.append("\nHeadline comparisons (seed-matched, F):")
    for m in methods:
        if m == CONTROL[1] or m == MAIN_LABELS['mixed']:
            continue
        g = df[df['method'] == m].set_index('seed')
        t, p = stats.ttest_rel(g['F'], mixed['F'])
        lines.append(f"  {m:>28} vs OCEAN-MARL mixed: t={t:+6.3f} p={p:.4f}")

    lines.extend(extra)
    with open(os.path.join(BASE, 'baseline_comparison.txt'), 'w') as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))

    # ========== PLOT ==========
    order = [MAIN_LABELS['mixed'], CONTROL[1]] + \
            [lab for _, lab in BASELINES] + \
            [MAIN_LABELS[s] for s in ['all_selfish', 'all_prosocial',
                                      'varied_altruism', 'innovator_effect']]
    order = [m for m in order if m in methods]
    fig, axes = plt.subplots(1, 3, figsize=(17, 5.5))
    for ax, metric, ylab, titl in [(axes[0], 'F', 'F = comfort + fairness',
                                    'Composite F'),
                                   (axes[1], 'comfort', 'Mean comfort',
                                    'Community comfort'),
                                   (axes[2], 'waste', 'Waste (kWh/day)',
                                    'Energy waste')]:
        means = [df[df['method'] == m][metric].mean() for m in order]
        stds = [df[df['method'] == m][metric].std() for m in order]
        colors = ['#2ecc71' if 'baseline' in m or m == CONTROL[1] else '#3498db'
                  for m in order]
        bars = ax.bar(range(len(order)), means, yerr=stds, capsize=5,
                      color=colors, alpha=0.85, edgecolor='gray', linewidth=0.5)
        ax.set_xticks(range(len(order)))
        ax.set_xticklabels([m.split(' ')[-1] for m in order], rotation=30,
                           ha='right', fontsize=8)
        ax.set_ylabel(ylab)
        ax.set_title(titl, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        for bar, val in zip(bars, means):
            ax.text(bar.get_x() + bar.get_width() / 2, val + (bar.get_height() or 0) + 0.01,
                    f'{val:.3f}', ha='center', fontsize=7)
    fig.suptitle('Baselines + control vs main OCEAN-MARL scenarios (mean±std, 5 seeds)',
                 fontweight='bold')
    fig.tight_layout()
    fig.savefig(os.path.join(BASE, 'baseline_comparison.png'), dpi=150,
                bbox_inches='tight')
    plt.close(fig)

    print(f"\nSaved: results/baseline_comparison.csv / .txt / .png")


if __name__ == '__main__':
    main()
