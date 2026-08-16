"""Canonical matplotlib styling for OCEAN-MARL thesis figures.

All thesis visuals should import palette, rcParams, and helpers from here
so data charts and schematics stay consistent across generate_all_Visuals2.py,
advanced_analysis.py, and baseline validation plots.
"""
import arabic_reshaper
import bidi.algorithm
import matplotlib.pyplot as plt

# ── Palette (north-star §5) ────────────────────────────────────────────────
C = {
    'red': '#e74c3c',
    'green': '#2ecc71',
    'blue': '#3498db',
    'purple': '#9b59b6',
    'orange': '#f39c12',
    'yellow': '#f1c40f',
    'dark': '#2c3e50',
    'grey': '#7f8c8d',
    'teal': '#1abc9c',
}

SCENARIO_COLORS = [
    C['red'], C['green'], C['blue'], C['yellow'], C['purple'],
]
SCENARIO_KEYS = [
    'all_selfish', 'all_prosocial', 'mixed', 'varied_altruism', 'innovator_effect',
]
SCENARIO_LABELS = [
    'All Selfish', 'All Prosocial', 'Mixed', 'Varied Altruism', 'Innovator Effect',
]

FA_FONTS = ['Geeza Pro', 'DejaVu Sans', 'Arial Unicode MS']

RC_PARAMS = {
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica', 'Arial', 'DejaVu Sans'],
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 150,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': C['grey'],
    'axes.linewidth': 0.8,
    'grid.color': C['grey'],
    'grid.alpha': 0.3,
    'grid.linestyle': '-',
    'lines.linewidth': 2.0,
    'patch.linewidth': 0.8,
    'savefig.facecolor': 'white',
    'savefig.edgecolor': 'none',
    'savefig.bbox': 'tight',
}


def apply_rc():
    """Apply global rcParams once at script start."""
    plt.rcParams.update(RC_PARAMS)


def fa(s):
    """Shape a Persian string for matplotlib (joining + RTL)."""
    return bidi.algorithm.get_display(arabic_reshaper.reshape(s))


def style_data_axes(ax, grid_axis='y'):
    """Standard academic axis styling for data charts."""
    ax.grid(axis=grid_axis, alpha=0.3, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(C['grey'])
    ax.spines['bottom'].set_color(C['grey'])
    ax.tick_params(colors=C['dark'], length=4, width=0.8)


def style_bars(bars, highlight_indices=None, edgecolor=None, linewidth=0.6):
    """Apply consistent bar edges; optionally highlight selected bars."""
    edgecolor = edgecolor or C['grey']
    highlight_indices = highlight_indices or []
    for i, bar in enumerate(bars):
        if i in highlight_indices:
            bar.set_edgecolor(C['dark'])
            bar.set_linewidth(2.0)
        else:
            bar.set_edgecolor(edgecolor)
            bar.set_linewidth(linewidth)
        bar.set_alpha(0.85)


def style_legend(legend):
    """Consistent legend frame for thesis figures."""
    if legend is None:
        return
    frame = legend.get_frame()
    frame.set_facecolor('white')
    frame.set_edgecolor(C['grey'])
    frame.set_alpha(0.95)
    frame.set_linewidth(0.6)


def label_bars(ax, bars, values, fmt='{:.3f}', offset=0.01, fontsize=7.5, errs=None):
    """Place value labels above bar tops (or error-bar caps when *errs* given)."""
    for i, (bar, val) in enumerate(zip(bars, values)):
        cap_top = bar.get_height() + (errs[i] if errs is not None else 0)
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            cap_top + offset,
            fmt.format(val),
            ha='center',
            va='bottom',
            fontsize=fontsize,
            fontweight='bold',
            color=C['dark'],
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1),
        )


def save_fig(fig, path, dpi=150):
    """Save figure with consistent white background and tight bbox."""
    fig.savefig(path, dpi=dpi, bbox_inches='tight', facecolor='white', edgecolor='none')


def plot_performance_panel(ax, x, comfort, fairness, xlabel='Episode', title='Community Performance'):
    """Reusable comfort + Jain panel used in baseline validation plots."""
    ax.plot(x, comfort, label='Mean Comfort', color=C['blue'], lw=2, alpha=0.9)
    ax.plot(x, fairness, label="Jain's Fairness", color=C['green'], lw=2, alpha=0.9)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Score')
    ax.set_ylim(0, 1.05)
    ax.set_title(title, fontweight='bold', fontsize=10)
    leg = ax.legend(loc='lower right')
    style_legend(leg)
    style_data_axes(ax)
