#!/usr/bin/env python3
"""
Generate training convergence figure (شکل ۴-۱-الف) for the thesis.

Runs all 5 scenarios × 5 seeds, logs per-episode community comfort,
then plots mean ± SD curves with an evaluation-window marker.

Output: results/figures/fig_training_convergence.png
"""
import os, sys, csv, time
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from offgrid_marl import run_simulation

RESULTS = os.path.join(os.path.dirname(__file__), 'results')
SCENARIOS = {
    'all_selfish':      ['pure_selfish'] * 10,
    'all_prosocial':    ['prosocial'] * 10,
    'mixed':            ['prosocial'] * 5 + ['pure_selfish'] * 5,
    'varied_altruism':  ['altruistic', 'prosocial', 'prosocial', 'prosocial',
                         'individualist', 'individualist', 'individualist',
                         'pure_selfish', 'pure_selfish', 'pure_selfish'],
    'innovator_effect': ['high_openness_innovator'] + ['prosocial'] * 4 +
                         ['individualist'] * 3 + ['pure_selfish'] * 2,
}
SEEDS = [42, 123, 456, 789, 1011]
EPISODES = 8000
LOG_EVERY = 100  # downsample for CSV storage

LEGEND_LABELS = {
    'all_selfish': 'All Selfish',
    'all_prosocial': 'All Prosocial',
    'mixed': 'Mixed',
    'varied_altruism': 'Varied Altruism',
    'innovator_effect': 'Innovator Effect',
}


def run_all():
    """Run all scenario×seed combos and return per-episode comfort arrays."""
    all_data = {}  # scenario -> seed -> np.array of comfort per episode
    total = len(SCENARIOS) * len(SEEDS)
    done = 0
    t0 = time.time()

    for sc_name, mix in SCENARIOS.items():
        all_data[sc_name] = {}
        for seed in SEEDS:
            done += 1
            print(f'[{done}/{total}] {sc_name} seed={seed} ...', end=' ', flush=True)
            agents, community, history = run_simulation(
                num_houses=10, episodes=EPISODES, seed=seed,
                verbose=False, personality_mix=mix,
            )
            comfort = np.array(history['comfort_mean'])
            all_data[sc_name][seed] = comfort
            print(f'OK ({len(comfort)} eps, final={comfort[-1000:].mean():.4f})')

    elapsed = time.time() - t0
    print(f'\nAll runs done in {elapsed:.1f}s ({elapsed/60:.1f} min)')
    return all_data


def save_csv(all_data):
    """Save per-episode data to CSV for reproducibility."""
    csv_path = os.path.join(RESULTS, 'training_convergence_per_episode.csv')
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        header = ['episode']
        for sc in SCENARIOS:
            for seed in SEEDS:
                header.append(f'{sc}_seed{seed}')
        w.writerow(header)
        for ep in range(EPISODES):
            row = [ep]
            for sc in SCENARIOS:
                for seed in SEEDS:
                    row.append(f'{all_data[sc][seed][ep]:.6f}')
            w.writerow(row)
    print(f'Saved per-episode CSV: {csv_path}')


def make_figure(all_data):
    """Generate the convergence figure with mean ± SD bands."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    try:
        from thesis_plot_style import C, save_fig, style_data_axes, style_legend
        has_style = True
    except ImportError:
        has_style = False

    if has_style:
        colors = {
            'all_selfish':     C['red'],
            'all_prosocial':   C['green'],
            'mixed':           C['blue'],
            'varied_altruism': C['yellow'],
            'innovator_effect': C['purple'],
        }
    else:
        colors = {
            'all_selfish':     '#d62728',
            'all_prosocial':   '#2ca02c',
            'mixed':           '#1f77b4',
            'varied_altruism': '#bcbd22',
            'innovator_effect': '#9467bd',
        }

    fig, ax = plt.subplots(figsize=(10, 5.5))

    # --- Main plot: mean +/- SD bands (episodes 0-8000, y 0.80-1.0) ---
    #
    # IMPORTANT: raw per-episode SD across seeds is dominated by high-frequency
    # exploration noise (individual episodes swing all over 0.2-1.0 early on).
    # Plotted directly, those bands are wider than the whole 0.80-1.0 y-range
    # for long stretches, so each scenario's band paints the entire column and
    # whichever scenario is drawn LAST ends up visually covering everyone
    # else's band *and* lines. Two fixes:
    #   1. Smooth each seed's curve with a rolling mean before computing the
    #      cross-seed mean/SD used for the *main* plot band (the raw signal is
    #      still shown, unsmoothed, in the early-training inset below).
    #   2. Draw ALL bands first, then draw ALL mean lines on top in a second
    #      pass, so a later scenario's band can never bury an earlier
    #      scenario's line.
    SMOOTH_WINDOW = 200  # episodes; only affects main-plot bands, not the inset

    def rolling_mean(x, w):
        if w <= 1:
            return x
        kernel = np.ones(w) / w
        # 'same'-length centered smoothing with edge padding so length is preserved
        padded = np.pad(x, (w // 2, w - 1 - w // 2), mode='edge')
        return np.convolve(padded, kernel, mode='valid')

    episodes = np.arange(EPISODES)
    smoothed_stats = {}
    for sc_name in SCENARIOS:
        seeds_data = np.array([all_data[sc_name][s] for s in SEEDS])  # (5, 8000)
        smoothed = np.array([rolling_mean(row, SMOOTH_WINDOW) for row in seeds_data])
        mean = smoothed.mean(axis=0)
        std = smoothed.std(axis=0, ddof=1)
        smoothed_stats[sc_name] = (mean, std)

    # Pass 1: bands only (drawn back-to-front so nothing later swamps earlier lines)
    for sc_name in SCENARIOS:
        mean, std = smoothed_stats[sc_name]
        ax.fill_between(episodes, mean - std, mean + std,
                         color=colors[sc_name], alpha=0.15, zorder=1)

    # Pass 2: lines on top, always visible regardless of band overlap
    for sc_name in SCENARIOS:
        mean, std = smoothed_stats[sc_name]
        ax.plot(episodes, mean, color=colors[sc_name], lw=2,
                 label=LEGEND_LABELS[sc_name], zorder=3)

    ax.axvline(x=7000, color='gray', ls='--', lw=1.5, label='Evaluation Window Starts', zorder=2)
    ax.set_xlabel('Episode', fontsize=12)
    ax.set_ylabel('Community Comfort', fontsize=12)
    ax.set_title('Training Convergence: Community Comfort over 8,000 Episodes',
                 fontsize=13, fontweight='bold')
    ax.set_xlim(0, EPISODES)
    ax.set_ylim(0.80, 1.0)
    ax.legend(loc='lower right', fontsize=9)
    ax.grid(True, alpha=0.3, color='#cccccc', zorder=0)
    ax.set_axisbelow(True)
    if has_style:
        style_data_axes(ax)

    fig.subplots_adjust(left=0.08, right=0.98, top=0.93, bottom=0.14)

    # --- Save PNG ---
    out_png = os.path.join(RESULTS, 'figures', 'fig_training_convergence.png')
    if has_style:
        save_fig(fig, out_png)
    else:
        fig.savefig(out_png, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'Figure saved: {out_png} ({os.path.getsize(out_png)//1024} KB)')
    return out_png


def make_early_training_figure(all_data, colors_override=None):
    """Standalone figure for the raw, unsmoothed early-training chaos
    (episodes 0-1000, full 0.0-1.0 y-range). Separate from the main
    convergence figure rather than an inset, so it gets its own full-size
    axes instead of being squeezed into a corner (and can't cover anything).
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    try:
        from thesis_plot_style import C, save_fig, style_data_axes, style_legend
        has_style = True
    except ImportError:
        has_style = False

    if colors_override is not None:
        colors = colors_override
    elif has_style:
        colors = {
            'all_selfish':     C['red'],
            'all_prosocial':   C['green'],
            'mixed':           C['blue'],
            'varied_altruism': C['yellow'],
            'innovator_effect': C['purple'],
        }
    else:
        colors = {
            'all_selfish':     '#d62728',
            'all_prosocial':   '#2ca02c',
            'mixed':           '#1f77b4',
            'varied_altruism': '#bcbd22',
            'innovator_effect': '#9467bd',
        }

    INSET_EPS = 1000
    fig, ax = plt.subplots(figsize=(8, 5))
    for sc_name in SCENARIOS:
        seeds_data = np.array([all_data[sc_name][s] for s in SEEDS])
        mean = seeds_data.mean(axis=0)
        ax.plot(np.arange(INSET_EPS), mean[:INSET_EPS], color=colors[sc_name],
                lw=1.8, label=LEGEND_LABELS[sc_name])

    ax.set_xlim(0, INSET_EPS)
    ax.set_ylim(0.0, 1.0)
    ax.set_xlabel('Episode', fontsize=12)
    ax.set_ylabel('Community Comfort', fontsize=12)
    ax.set_title('Early Training: Raw Exploration Behavior (Episodes 0\u20131,000)',
                 fontsize=13, fontweight='bold')
    ax.legend(loc='lower right', fontsize=9)
    ax.grid(True, alpha=0.3, color='#cccccc', zorder=0)
    ax.set_axisbelow(True)
    if has_style:
        style_data_axes(ax)

    fig.subplots_adjust(left=0.1, right=0.98, top=0.92, bottom=0.12)

    out_png = os.path.join(RESULTS, 'figures', 'fig_training_early.png')
    if has_style:
        save_fig(fig, out_png)
    else:
        fig.savefig(out_png, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'Figure saved: {out_png} ({os.path.getsize(out_png)//1024} KB)')
    return out_png


if __name__ == '__main__':
    csv_path = os.path.join(RESULTS, 'training_convergence_per_episode.csv')
    if os.path.exists(csv_path):
        print(f'Loading existing per-episode CSV: {csv_path}')
        all_data = {}
        with open(csv_path) as f:
            reader = csv.reader(f)
            header = next(reader)
            for sc in SCENARIOS:
                all_data[sc] = {}
            for row in reader:
                ep = int(row[0])
                idx = 1
                for sc in SCENARIOS:
                    for seed in SEEDS:
                        if ep == 0:
                            all_data[sc][seed] = []
                        all_data[sc][seed].append(float(row[idx]))
                        idx += 1
        for sc in SCENARIOS:
            for seed in SEEDS:
                all_data[sc][seed] = np.array(all_data[sc][seed])
        print(f'Loaded {len(all_data["mixed"][42])} episodes per seed')
    else:
        all_data = run_all()
        save_csv(all_data)
    make_figure(all_data)
    make_early_training_figure(all_data)
