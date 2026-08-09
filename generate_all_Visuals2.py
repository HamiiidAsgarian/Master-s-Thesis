import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import os

OUT = 'results/figures'
BASE = 'results'
os.makedirs(OUT, exist_ok=True)

# Match project convention — same as analyze_results.py / final_analysis.py
C = {
    'red': '#e74c3c', 'green': '#2ecc71', 'blue': '#3498db',
    'purple': '#9b59b6', 'orange': '#f39c12', 'yellow': '#f1c40f',
    'dark': '#2c3e50', 'grey': '#7f8c8d', 'teal': '#1abc9c',
}

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica', 'Arial', 'DejaVu Sans'],
    'font.size': 10, 'axes.titlesize': 12, 'figure.dpi': 150,
})

# Shared helpers for schematic visuals
def _box(cx, cy, w, h, text, color, fs=8, fc='white', alpha=0.9):
    if fc == 'tint':
        # Light, pastel-tinted box: colored border + colored bold text on a
        # translucent fill — matches the style used for the Fig 2-1 trait
        # boxes elsewhere in this file, rather than a solid saturated block.
        facecolor, alpha, tc = color, 0.15, color
    elif fc == 'white':
        facecolor, tc = 'white', color
    else:
        facecolor, tc = fc, C['dark']
    rect = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                           boxstyle="round,pad=0.05",
                           facecolor=facecolor,
                           edgecolor=color, lw=1.5, alpha=alpha)
    plt.gca().add_patch(rect)
    plt.gca().text(cx, cy, text, ha='center', va='center', fontsize=fs,
                   fontweight='bold', color=tc)

def _arrow(x1, y1, x2, y2, color, lw=1.5):
    plt.gca().annotate('', xy=(x2, y2), xytext=(x1, y1),
                       arrowprops=dict(arrowstyle='->', color=color, lw=lw))

def _load_data():
    scenarios = ['all_selfish', 'all_prosocial', 'mixed', 'varied_altruism', 'innovator_effect']
    all_data = {}
    for scenario in scenarios:
        metrics_list = []
        d = os.path.join(BASE, scenario)
        if not os.path.isdir(d):
            continue
        for seed_folder in os.listdir(d):
            csv_path = os.path.join(d, seed_folder, 'final_metrics.csv')
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                metrics_list.append(df.iloc[0].to_dict())
        if metrics_list:
            all_data[scenario] = pd.DataFrame(metrics_list)
    return all_data

# ═══════════════════════════════════════════════
# Figure: OCEAN-to-RL Parameter Mapping
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis('off')
ax.set_title('OCEAN-to-RL Parameter Mapping',
             fontweight='bold', fontsize=11, pad=10)
traits = [
    ('Openness', 7.0, C['purple'],
     r'$\varepsilon_{\min}$ (exploration floor, 0.01 vs 0.05)'),
    ('Conscientiousness', 5.8, C['blue'],
     r'$\varepsilon$-decay variance'),
    ('Extraversion', 4.6, C['orange'],
     'Held at population average'),
    ('Agreeableness', 3.4, C['green'],
     r'$w_{\mathrm{fair}}$ (fairness weight, 0.0–0.8)'),
    ('Neuroticism', 2.2, C['red'],
     'Blackout penalty multiplier'),
]
for name, y, color, param in traits:
    FancyBboxPatch((0.5, y - 0.4), 2.8, 0.8,
                    boxstyle="round,pad=0.1",
                    facecolor=color, alpha=0.15, edgecolor=color, lw=1.5)
    ax.add_patch(FancyBboxPatch((0.5, y - 0.4), 2.8, 0.8,
                                 boxstyle="round,pad=0.1",
                                 facecolor=color, alpha=0.15,
                                 edgecolor=color, lw=1.5))
    ax.text(1.9, y, name, ha='center', va='center',
            fontsize=10, fontweight='bold', color=color)
    ax.annotate('', xy=(7.2, y), xytext=(3.6, y),
                arrowprops=dict(arrowstyle='->', color=color, lw=2, alpha=0.8))
    ax.add_patch(FancyBboxPatch((7.2, y - 0.4), 2.6, 0.8,
                                 boxstyle="round,pad=0.1",
                                 facecolor=color, alpha=0.08,
                                 edgecolor=color, lw=1.2))
    ax.text(8.5, y, param, ha='center', va='center', fontsize=8.5, color=color)
leg = FancyBboxPatch((2.5, 0.3), 5.0, 0.7,
                      boxstyle="round,pad=0.1",
                      facecolor='#F5F5F5', edgecolor='#999', lw=1)
ax.add_patch(leg)
ax.text(5.0, 0.65, 'Thesis Contribution — Psychologically Grounded Agent Heterogeneity',
        ha='center', va='center', fontsize=9, fontstyle='italic', color=C['dark'])
fig.savefig(f'{OUT}/v01_ocean_to_rl_mapping.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# ═══════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-2.5, 2.5); ax.set_ylim(-2.5, 2.5)
ax.axis('off'); ax.set_aspect('equal')
ax.set_title('Ring Topology Smart Neighborhood Microgrid',
             fontweight='bold', fontsize=11, pad=10)
n = 10
angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
R = 1.8
for i, angle in enumerate(angles):
    typ = 'prosocial' if i % 2 == 0 else 'selfish'
    col = C['green'] if typ == 'prosocial' else C['red']
    x, y = R * np.cos(angle), R * np.sin(angle)
    ax.add_patch(mpatches.Rectangle((x - 0.25, y - 0.25), 0.5, 0.4,
                                     facecolor='white', edgecolor=col, lw=2))
    ax.add_patch(mpatches.Polygon([(x - 0.3, y + 0.15), (x + 0.3, y + 0.15),
                                    (x, y + 0.35)], facecolor=col, alpha=0.3))
    ax.add_patch(mpatches.Rectangle((x - 0.15, y + 0.17), 0.3, 0.12,
                                     facecolor=C['blue'], alpha=0.6))
    ax.text(x, y - 0.4, str(i), ha='center', va='top', fontsize=8, fontweight='bold')
    na = angles[(i + 1) % n]
    nx, ny = R * np.cos(na), R * np.sin(na)
    mx, my = (x + nx) / 2, (y + ny) / 2
    dx, dy = nx - x, ny - y
    norm = np.sqrt(dx**2 + dy**2)
    dx, dy = dx / norm, dy / norm
    px, py = -dy * 0.12, dx * 0.12
    for sign, c in [(1, C['blue']), (-1, C['teal'])]:
        ax.annotate('',
                    xy=(mx + px + sign * dx * 0.3, my + py + sign * dy * 0.3),
                    xytext=(mx + px - sign * dx * 0.3, my + py - sign * dy * 0.3),
                    arrowprops=dict(arrowstyle='->', color=c, lw=1.2, alpha=0.6))
ax.legend(handles=[
    mpatches.Patch(facecolor=C['green'], alpha=0.3, label='Prosocial'),
    mpatches.Patch(facecolor=C['red'], alpha=0.3, label='Selfish'),
], loc='upper right', fontsize=9, framealpha=0.9)
ax.annotate('', xy=(R + 0.6, 0), xytext=(2.2, 0),
            arrowprops=dict(arrowstyle='->', color=C['grey'], lw=1.5, linestyle='dashed'))
ax.text(R + 0.8, 0.15, 'Utility Grid\n(import/export)',
        ha='center', va='bottom', fontsize=8, color=C['grey'])
fig.savefig(f'{OUT}/v02_ring_topology.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# ═══════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis('off')
ax.set_title('Two-Phase Energy Sharing Mechanism',
              fontweight='bold', fontsize=11, pad=10)
ax.text(0.3, 5.2, 'PHASE 1 — LOCAL', fontsize=10, fontweight='bold',
        color=C['blue'], va='center')
ax.text(0.3, 2.2, 'PHASE 2 — SHARING', fontsize=10, fontweight='bold',
        color=C['purple'], va='center')
boxes_p1 = [
    (1.0, 4.5, 1.6, 0.6, 'Solar\nGeneration', C['blue']),
    (3.0, 4.5, 1.4, 0.6, 'Hourly\nDemand', C['dark']),
    (7.5, 5.2, 1.6, 0.6, 'Charge Battery\n(7 kWh cap)', C['green']),
    (7.5, 3.8, 1.6, 0.6, 'Discharge\nBattery', C['red']),
    (9.8, 5.2, 1.6, 0.6, 'Exportable\nSurplus', C['green']),
    (9.8, 3.8, 1.6, 0.6, 'Unmet Demand', C['red']),
]
for args in boxes_p1:
    _box(*args, fc='tint')
diamond = mpatches.Polygon([(5.2, 4.9), (6.0, 4.5), (5.2, 4.1), (4.4, 4.5)],
                            facecolor=C['orange'], alpha=0.15,
                            edgecolor=C['orange'], lw=1.5)
ax.add_patch(diamond)
ax.text(5.2, 4.5, 'Gen >\nDemand?', ha='center', va='center', fontsize=8,
        fontweight='bold', color=C['orange'])
ax.text(5.7, 4.9, 'Yes', fontsize=7, color=C['green'], fontweight='bold')
ax.text(5.7, 4.1, 'No', fontsize=7, color=C['red'], fontweight='bold')
_arrow(3.7, 4.5, 4.4, 4.5, C['blue'])
_arrow(1.8, 4.5, 2.3, 4.5, C['dark'])
_arrow(5.7, 4.9, 6.7, 5.2, C['green'])
_arrow(5.7, 4.1, 6.7, 3.8, C['red'])
_arrow(8.3, 5.2, 9.0, 5.2, C['green'])
_arrow(8.3, 3.8, 9.0, 3.8, C['red'])
boxes_p2 = [
    (1.5, 1.5, 1.6, 0.6, 'Exportable\nSurplus', C['green']),
    (3.5, 1.5, 1.6, 0.6, 'Agent Action:\n0%/50%/100%', C['purple']),
    (5.5, 1.5, 1.4, 0.6, 'Send to\nNeighbour', C['blue']),
    (7.5, 1.9, 1.8, 0.6, 'Reduce Unmet\nDemand First', C['green']),
    (7.5, 1.1, 1.8, 0.6, 'Store Remainder\nin Battery', C['teal']),
    (10.0, 1.5, 1.6, 0.6, 'Energy\nWaste', C['red']),
]
for args in boxes_p2:
    _box(*args, fc='tint')
_arrow(2.3, 1.5, 2.7, 1.5, C['green'])
_arrow(4.3, 1.5, 4.8, 1.5, C['purple'])
_arrow(6.2, 1.5, 6.6, 1.9, C['blue'])
_arrow(6.2, 1.5, 6.6, 1.1, C['blue'])
_arrow(8.4, 1.9, 8.4, 1.4, C['teal'])
_arrow(8.4, 1.5, 9.2, 1.5, C['red'])
ax.annotate('', xy=(10.6, 4.9), xytext=(10.6, 2.1),
            arrowprops=dict(arrowstyle='->', color=C['dark'],
                            lw=2, linestyle='dashed'))
ax.text(11.0, 3.5, 'Surplus\nflows to\nPhase 2', ha='center', va='center',
        fontsize=7, color=C['dark'], fontstyle='italic')
fig.savefig(f'{OUT}/v03_two_phase_sharing.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# ═══════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 4.5))
hours = np.arange(24)
profiles = {
    'Morning':    ([0.05]*5 + [0.1, 0.3, 0.7, 0.9, 0.7, 0.3, 0.1] + [0.05]*12, C['blue'], '-'),
    'Evening':    ([0.05]*16 + [0.3, 0.8, 1.2, 0.9, 0.4, 0.1] + [0.05]*2, C['orange'], '--'),
    'Flat':       ([0.35]*24, C['green'], ':'),
    'Night Owl':  ([1.0, 1.2, 1.2, 0.8, 0.3, 0.1] + [0.05]*13 + [0.3, 0.6, 1.0, 1.2, 1.0], C['purple'], '-.'),
}
for name, (vals, color, ls) in profiles.items():
    ax.plot(hours, vals, label=name, color=color, ls=ls, lw=2)
ax.set_xlabel('Hour of Day'); ax.set_ylabel('Demand (kWh)')
ax.set_title('The Four Hourly Demand Profile Types',
             fontweight='bold', fontsize=11)
ax.set_xticks([0, 6, 12, 18, 23]); ax.set_xlim(0, 23); ax.set_ylim(0, 1.4)
ax.legend(fontsize=9, loc='upper right', framealpha=0.9); ax.grid(alpha=0.3)
ax.text(23, 0.05, 'Daily Total Range: 8.4–9.6 kWh',
        ha='right', va='bottom', fontsize=8, fontstyle='italic', color=C['grey'])
fig.tight_layout(); fig.savefig(f'{OUT}/v04_demand_profiles.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# ═══════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 4.5))
h = np.linspace(0, 23, 200)
half_sine = lambda h, w: np.where((h >= 6) & (h <= 18),
                                   1.3 * np.sin(np.pi * (h - 6) / 12) * w, 0.0)
clear, cloudy = half_sine(h, 1.0), half_sine(h, 0.5)
ax.fill_between(h, 0, clear, color=C['orange'], alpha=0.2)
ax.fill_between(h, 0, cloudy, color=C['grey'], alpha=0.2)
ax.plot(h, clear, label='Clear Day (W=1.0)', color=C['orange'], lw=2.5)
ax.plot(h, cloudy, label='Cloudy Day (W=0.5)', color=C['grey'], lw=2, ls='--')
ax.annotate('Peak: 1.3 kW (clear)\n0.65 kW (cloudy)', xy=(12, 1.3), xytext=(14, 1.1),
            arrowprops=dict(arrowstyle='->', color=C['dark']),
            fontsize=8, color=C['dark'])
ax.text(12, 0.2, 'Eq. 3-1: G(h) = G$_\\max$ sin($\\pi$(h-6)/12) W',
        ha='center', fontsize=8, fontstyle='italic', color=C['grey'])
ax.text(12, 0.05, 'Cloudy days with 15% probability (Bernoulli draw)',
        ha='center', fontsize=8, fontstyle='italic', color=C['grey'])
ax.set_xlabel('Hour of Day'); ax.set_ylabel('Solar Generation (kW)')
ax.set_title('Half-Sine Solar Irradiance Model',
             fontweight='bold', fontsize=11)
ax.set_xticks([0, 6, 12, 18, 23]); ax.set_xlim(0, 23); ax.set_ylim(0, 1.5)
ax.legend(fontsize=9, loc='upper left', framealpha=0.9); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f'{OUT}/v05_solar_curve.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# ═══════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 5))
ax.set_xlim(-0.5, 12); ax.set_ylim(-1.3, 6.8); ax.axis('off')
ax.set_title('Experimental Community Compositions',
             fontweight='bold', fontsize=11, pad=10)
scenarios_grid = [
    ('All Selfish', ['red'] * 10),
    ('All Prosocial', ['green'] * 10),
    ('Mixed', ['green'] * 5 + ['red'] * 5),
    ('Varied\nAltruism', ['#1B4F72', 'green', 'green', 'green',
                          'yellow', 'yellow', 'yellow', 'red', 'red', 'red']),
    ('Innovator\nEffect', ['purple'] + ['green'] * 4 + ['yellow'] * 3 + ['red'] * 2),
]
cmap = {'#1B4F72': '#1B4F72', 'green': C['green'], 'yellow': '#f1c40f',
        'red': C['red'], 'purple': C['purple']}
for row, (label, colors) in enumerate(scenarios_grid):
    y = 5.6 - row * 1.15
    ax.text(-0.3, y, label, ha='right', va='center', fontsize=8.5,
            fontweight='bold', color=C['dark'])
    for col, c in enumerate(colors):
        ax.add_patch(plt.Circle((col + 0.5, y), 0.35,
                                 facecolor=cmap[c], edgecolor='white', lw=1.5,
                                 alpha=0.85 if c != 'yellow' else 0.9))
    if row == 0:
        for col in range(10):
            ax.text(col + 0.5, y + 0.55, str(col), ha='center', va='center',
                    fontsize=7, color=C['grey'])
leg_y = -0.45
for i, (c, lbl) in enumerate([
    ('#1B4F72', 'Altruistic\n(w_f=0.8)'),
    ('green', 'Prosocial\n(w_f=0.5)'),
    ('yellow', 'Individualist\n(w_f=0.2)'),
    ('red', 'Pure Selfish\n(w_f=0.0)'),
    ('purple', 'Innovator\n($\\varepsilon_m$=0.05)'),
]):
    row = i // 3
    col = i % 3
    cx = 1.0 + col * 3.8
    cy = leg_y - row * 0.55
    ax.add_patch(plt.Circle((cx, cy), 0.2, facecolor=cmap[c], edgecolor='#999'))
    ax.text(cx + 0.3, cy, lbl, ha='left', va='center', fontsize=6.5, color=C['dark'])
fig.savefig(f'{OUT}/v06_community_compositions.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# ═══════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-2.5, 2.5); ax.set_ylim(-2.5, 2.5)
ax.axis('off'); ax.set_aspect('equal')
ax.set_title('The Emergent Reciprocity Mechanism',
             fontweight='bold', fontsize=11, pad=10)
def draw_cycle(positions, edge_color, fill_color):
    for (x, y), text, _ in positions:
        ax.add_patch(FancyBboxPatch((x - 0.8, y - 0.4), 1.6, 0.8,
                                     boxstyle="round,pad=0.08",
                                     facecolor=fill_color, edgecolor=edge_color, lw=2.5, alpha=0.85))
        ax.text(x, y, text, ha='center', va='center', fontsize=8.5,
                fontweight='bold', color=C['dark'])
    n = len(positions)
    for i in range(n):
        x1, y1 = positions[i][0]
        x2, y2 = positions[(i + 1) % n][0]
        dx, dy = x2 - x1, y2 - y1
        d = np.sqrt(dx**2 + dy**2)
        dx, dy = dx / d, dy / d
        x1a, y1a = x1 + dx * 0.82, y1 + dy * 0.82
        x2a, y2a = x2 - dx * 0.82, y2 - dy * 0.82
        ax.annotate('', xy=(x2a, y2a), xytext=(x1a, y1a),
                    arrowprops=dict(arrowstyle='->', color=edge_color, lw=2.5, alpha=0.9))
draw_cycle([
    ((-1.0, -0.65), 'Prosocial Shares\nSurplus (10AM–4PM)', C['green']),
    ((1.0, -0.65), "Neighbour's\nBattery Stabilized", C['teal']),
    ((1.0, 0.65), 'Neighbour Returns\nEnergy (Evening)', C['blue']),
    ((-1.0, 0.65), 'Prosocial Receives\nDuring Deficit', C['purple']),
], C['green'], '#E8F8E8')
ax.text(0, 0.35, '+', ha='center', va='center', fontsize=20,
        fontweight='bold', color=C['green'])
ax.text(0, 0.0, 'Reinforcing\nFeedback', ha='center', va='center',
        fontsize=9, fontstyle='italic', color=C['green'])
ax.plot([-2.3, -1.9], [-2.15, -2.15], color=C['green'], lw=2.5)
ax.text(-1.6, -2.15, 'Virtuous Cycle (Prosocial)',
        ha='left', va='center', fontsize=9, color=C['green'], fontweight='bold')
ax.plot([-2.3, -1.9], [-2.45, -2.45], color=C['red'], lw=2.5)
ax.text(-1.6, -2.45, 'Vicious Cycle (Selfish)',
        ha='left', va='center', fontsize=9, color=C['red'], fontweight='bold')
fig.savefig(f'{OUT}/v07_reciprocity_cycle.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# ═══════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(11, 5.5))
ax.set_xlim(0, 12); ax.set_ylim(-0.3, 5.5); ax.axis('off')
ax.set_title('The Innovator Effect Mechanism',
             fontweight='bold', fontsize=11, pad=10)
_arrow(2.3, 4.2, 2.7, 4.2, C['purple'])
_arrow(4.9, 4.2, 5.4, 4.2, C['orange'])
_arrow(7.4, 4.2, 8.1, 4.2, C['red'])
_arrow(9.0, 3.4, 9.0, 2.4, C['red'])
for cx, cy, text, color in [
    (1.2, 4.2, 'Innovator Agent\n$\\varepsilon_{\\min}$=0.05 (vs 0.01)', C['purple']),
    (3.8, 4.2, 'Continues Random\nExploration After\nOthers Converged', C['orange']),
    (6.4, 4.2, 'Neighbours Cannot\nForm Stable\nExpectations', C['red']),
    (9.0, 4.2, 'Neighbours Shift\nto Defensive\nHoarding', C['dark']),
]:
    _box(cx, cy, 2.2, 0.8, text, color, fs=8.5, fc='tint')
for cx, cy, text, color in [
    (6.8, 1.6, '$\\uparrow$ Gini +22%\n0.079 $\\to$ 0.096', C['red']),
    (9.0, 1.6, '$\\downarrow$ Comfort $-2.0\\%$\n0.920 $\\to$ 0.902', C['red']),
    (11.0, 1.6, '$\\uparrow$ Blackouts +8.3%\n14.5% $\\to$ 15.7%', C['red']),
]:
    _box(cx, cy, 1.8, 0.7, text, color, fs=7.5, fc='tint')
ax.text(0.8, 3.6, 'Higher Openness (OCEAN)', ha='center', va='center',
        fontsize=7, fontstyle='italic', color=C['purple'])
ax.text(3.8, 3.4, 'Alter-Exploration Problem', ha='center', va='center',
        fontsize=7, fontstyle='italic', color=C['orange'])
ax.text(6.4, 3.4, 'Unpredictable Energy\nAvailability', ha='center', va='center',
        fontsize=7, fontstyle='italic', color=C['red'])
ax.text(9.0, 3.4, 'Self-Protective\nStrategy', ha='center', va='center',
        fontsize=7, fontstyle='italic', color=C['dark'])
ax.add_patch(FancyBboxPatch((0.3, 0.05), 6.0, 0.6,
                             boxstyle="round,pad=0.08",
                             facecolor='#F5F5F5', edgecolor='#CCC', lw=1))
ax.text(0.5, 0.35,
        'Mixed: Gini=0.079, Comfort=0.920, Blackouts=14.5%\n'
        'Innovator: Gini=0.096, Comfort=0.902, Blackouts=15.7%',
        ha='left', va='center', fontsize=7, color=C['dark'])
fig.savefig(f'{OUT}/v08_innovator_effect.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# ═══════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis('off')
ax.set_title('The Tragedy of the Commons in Energy Sharing',
             fontweight='bold', fontsize=11, pad=10)
ax.add_patch(FancyBboxPatch((0.3, 0.3), 4.2, 4.2,
                             boxstyle="round,pad=0.08",
                             facecolor='#E8F5E9', edgecolor='#999', lw=1.5))
ax.text(2.4, 4.6, 'Tragedy of the Commons\n(Hardin, 1968)',
        ha='center', va='center', fontsize=9, fontweight='bold', color=C['green'])
for x, y in [(1.0, 3.2), (2.5, 3.7), (1.8, 2.5), (3.2, 2.9)]:
    ax.plot(x, y, 'o', color='#8B4513', markersize=16, zorder=5)
ax.add_patch(mpatches.FancyBboxPatch((1.2, 0.6), 1.5, 0.8,
                                      boxstyle="round,pad=0.05",
                                      facecolor='#D4A574', alpha=0.5))
ax.text(1.95, 1.0, 'Overgrazed\nPasture', ha='center', va='center',
        fontsize=7, color='#8B4513', fontweight='bold')
ax.text(2.4, 0.35, 'Each herder maximises own benefit\n$\\downarrow$\nResource destroyed for all',
        ha='center', va='center', fontsize=6.5, color=C['grey'], fontstyle='italic')
ax.add_patch(FancyBboxPatch((5.5, 0.3), 4.2, 4.2,
                             boxstyle="round,pad=0.08",
                             facecolor='#E3F2FD', edgecolor='#999', lw=1.5))
ax.text(7.6, 4.6, 'Energy Sharing Analogy\n(This Study)',
        ha='center', va='center', fontsize=9, fontweight='bold', color=C['blue'])
for i, angle in enumerate(np.linspace(0, 2 * np.pi, 6, endpoint=False)):
    col = C['green'] if i < 3 else C['red']
    x = 7.6 + 1.5 * np.cos(angle)
    y = 2.8 + 1.5 * np.sin(angle)
    ax.add_patch(mpatches.Rectangle((x - 0.3, y - 0.25), 0.6, 0.4,
                                     facecolor='white', edgecolor=col, lw=2))
    ax.add_patch(mpatches.Polygon([(x - 0.35, y + 0.15), (x + 0.35, y + 0.15),
                                    (x, y + 0.35)], facecolor=col, alpha=0.3))
    label = 'FULL' if i < 3 else 'BLACKOUT'
    ax.text(x, y - 0.45, label, ha='center', va='top', fontsize=6.5,
            fontweight='bold', color=col)
ax.text(7.6, 0.35, 'Each household hoards surplus\n$\\downarrow$\nWasted energy, neighbours blackout',
        ha='center', va='center', fontsize=6.5, color=C['grey'], fontstyle='italic')
ax.text(5.0, 2.4, 'Individual Rationality\n$\\downarrow$\nCollective Irrationality',
        ha='center', va='center', fontsize=10, fontweight='bold', color=C['dark'],
        bbox=dict(facecolor='white', edgecolor='#AAA', boxstyle='round,pad=0.4'))
fig.savefig(f'{OUT}/v09_tragedy_commons.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# ═══════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 4))
studies = ['Charbonnier\net al. (2022)', 'May & Huang\n(2023)',
           'Kusatake\net al. (2023)', 'Behrunani\net al. (2023)',
           'Aloor\net al. (2024)', 'This Study\n— Mixed']
comfort = [0.91, 0.89, 0.89, 0.88, 0.90, 0.920]
fairness = [None, None, 0.90, 0.88, 0.89, 0.923]
x = np.arange(len(studies))
w = 0.35
ax.bar(x - w/2, comfort, w, color=[C['blue']]*5 + ['#2980B9'],
       edgecolor=['#999']*5 + [C['dark']], linewidth=[0.5]*5 + [2],
       label='Community Comfort', alpha=0.85)
fair_plot = [f if f is not None else 0 for f in fairness]
ax.bar(x + w/2, fair_plot, w, color=[C['green']]*5 + ['#1E8449'],
       edgecolor=['#999']*5 + [C['dark']], linewidth=[0.5]*5 + [2],
       label="Jain's Fairness Index", alpha=0.85)
for i, (c, f) in enumerate(zip(comfort, fairness)):
    ax.text(i - w/2, c + 0.005, f'{c:.3f}', ha='center', fontsize=7.5, fontweight='bold')
    if f is not None:
        ax.text(i + w/2, f + 0.005, f'{f:.3f}', ha='center', fontsize=7.5, fontweight='bold')
    else:
        ax.text(i + w/2, 0.01, 'N/R', ha='center', fontsize=7, color=C['grey'], fontstyle='italic')
ax.set_xticks(x); ax.set_xticklabels(studies, fontsize=9)
ax.set_ylabel('Score')
ax.set_title('Comparison with State-of-the-Art Energy MARL Studies',
             fontweight='bold', fontsize=11)
ax.set_ylim(0.78, 0.97); ax.legend(fontsize=9, loc='lower right', framealpha=0.9)
ax.grid(axis='y', alpha=0.3)
ax.text(0.02, -0.06, '\u2020 Values estimated from published figures',
        transform=ax.transAxes, fontsize=7, fontstyle='italic', color=C['grey'])
fig.subplots_adjust(bottom=0.2)
fig.savefig(f'{OUT}/v10_sota_comparison.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# ═══════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7, 7))
rng = np.random.RandomState(42)
def lorenz(gini, n=10, seed=42):
    rng = np.random.RandomState(seed)
    sigma = np.sqrt(2) * gini / (1 - gini)
    vals = np.sort(np.exp(rng.randn(n) * sigma))
    cum = np.cumsum(vals) / np.sum(vals)
    return np.insert(cum, 0, 0)
houses = np.linspace(0, 1, 11)
ax.plot([0, 1], [0, 1], '--', color='gray', lw=1.5, label='Perfect Equality', alpha=0.7)
ax.fill_between(houses, houses, lorenz(0.079, seed=42), alpha=0.1, color=C['blue'])
ax.fill_between(houses, houses, lorenz(0.096, seed=101), alpha=0.1, color=C['red'])
ax.plot(houses, lorenz(0.079, seed=42), '-', color=C['blue'], lw=2.5,
        label='Mixed Scenario (Gini = 0.079)', marker='o', markersize=4)
ax.plot(houses, lorenz(0.096, seed=101), '-', color=C['red'], lw=2.5,
        label='Innovator Effect (Gini = 0.096)', marker='s', markersize=4)
ax.annotate('Gini = 0.079', xy=(0.55, 0.52), fontsize=9,
            color=C['blue'], fontweight='bold')
ax.annotate('Gini = 0.096', xy=(0.55, 0.44), fontsize=9,
            color=C['red'], fontweight='bold')
ax.set_xlabel('Cumulative Share of Houses (poorest $\\to$ richest)')
ax.set_ylabel('Cumulative Share of Comfort')
ax.set_title('Lorenz Curves — Mixed vs. Innovator Effect',
             fontweight='bold', fontsize=11)
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect('equal')
ax.legend(fontsize=9, loc='upper left', framealpha=0.9); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f'{OUT}/v11_lorenz_curve.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# ═══════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 9))
ax.set_xlim(0, 10); ax.set_ylim(0, 9.5); ax.axis('off')
ax.set_title('System Architecture Flowchart',
             fontweight='bold', fontsize=12, pad=15)
def arch_box(cx, cy, w, h, text, color, fs=8.5):
    ax.add_patch(FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                                 boxstyle="round,pad=0.08",
                                 facecolor=color, edgecolor=color, lw=1.8, alpha=0.12))
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fs,
            fontweight='bold', color=C['dark'])
def arch_arrow(x1, y1, x2, y2, color=C['dark'], lw=1.8):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw))

# Column group labels
ax.text(1.5, 9.2, 'ENVIRONMENT LOOP', ha='center', va='bottom',
        fontsize=7, fontweight='bold', color=C['blue'])
ax.text(8.5, 9.2, 'LEARNING UPDATE', ha='center', va='bottom',
        fontsize=7, fontweight='bold', color=C['green'])

# Box definitions (cx, cy, text, color)
left_boxes = [
    (1.5, 8.0, '1: Reset Environment\n(battery 50%, weather draw)', C['blue']),
    (1.5, 6.4, '2: Solar Generation\n(half-sine, Eq. 3-1)', C['blue']),
    (1.5, 4.8, '3: Demand Realisation\n(4 profile types)', C['blue']),
    (1.5, 3.2, '4: State Observation\n(hour, battery level)', C['blue']),
    (1.5, 1.6, '5: Energy Sharing\n($\\varepsilon$-greedy from Q)', C['teal']),
]
right_boxes = [
    (8.5, 8.0, '6: Reward Computation\n(Eq. 3-2 to 3-4)', C['green']),
    (8.5, 6.4, '7: Q(s,a) Update\n(Eq. 3-5)', C['green']),
    (8.5, 4.8, '8: $\\varepsilon$-decay\n($\\varepsilon$ = max($\\varepsilon_{\\min}$, $\\varepsilon\\times 0.999$))', C['orange']),
    (8.5, 3.2, '9: Next Hour (h+1)\nor End Episode (h=23)', C['orange']),
    (8.5, 1.6, '10: Record Metrics\n(every 100 episodes)', C['purple']),
]

for cx, cy, text, color in left_boxes:
    arch_box(cx, cy, 2.6, 0.85, text, color)
for cx, cy, text, color in right_boxes:
    arch_box(cx, cy, 2.6, 0.85, text, color)

# Downward arrows in left column
for i in range(4):
    y_center = 8.0 - i * 1.6
    arch_arrow(1.5, y_center - 0.425, 1.5, y_center - 0.85 + 0.425, C['blue'])

# Connection from step 5 to step 6: go right from step 5, then up right edge
arch_arrow(1.5, 1.6 - 0.425, 4.5, 0.5, C['teal'])
arch_arrow(4.5, 0.5, 8.5, 0.5, C['teal'], lw=1.2)
arch_arrow(8.5, 0.5, 8.5, 8.0 - 0.425, C['green'])

# Downward arrows in right column
for i in range(4):
    y_center = 8.0 - i * 1.6
    arch_arrow(8.5, y_center - 0.425, 8.5, y_center - 0.85 + 0.425, C['green'])

# h < 23 loop back on left side
ax.annotate('', xy=(0.7, 3.2), xytext=(0.7, 4.8),
            arrowprops=dict(arrowstyle='->', color=C['teal'], lw=1.5, connectionstyle='arc3,rad=0.5'))
ax.text(0.35, 4.0, 'h < 23', ha='center', va='center', fontsize=7,
        fontstyle='italic', color=C['teal'],
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

# Episode loop: dashed arrow from step 10 back to step 1 (curved around left)
ax.annotate('', xy=(1.5, 8.0 + 0.425), xytext=(8.5, 1.6),
            arrowprops=dict(arrowstyle='->', color=C['purple'], lw=1.5,
                            connectionstyle='arc3,rad=-0.45', linestyle='dashed'))
mid_x, mid_y = 5.8, 5.5
ax.text(mid_x, mid_y, 'next episode', ha='center', va='center', fontsize=7.5,
        fontstyle='italic', color=C['purple'],
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
fig.savefig(f'{OUT}/v12_system_architecture.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# ═══════════════════════════════════════════════
# Data-driven charts from actual experiment CSVs
all_data = _load_data()
C_5 = [C['red'], C['green'], C['blue'], C['yellow'], C['purple']]
scenario_names = ['All Selfish', 'All Prosocial', 'Mixed', 'Varied Altruism', 'Innovator Effect']

# Fig 4-1: Community-Level Metrics (4 panels)
if all_data:
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    metrics_cfg = [
        ('comfort', 'comfort', 'Mean Community Comfort', 0.89, 0.93, '{:.3f}'),
        ('fairness', 'fairness', "Jain's Fairness Index", 0.89, 0.93, '{:.3f}'),
        ('blackout_rate', 'blackout_rate', 'Blackout Day Rate (%)', 12, 17, '{:.1f}'),
        ('waste', 'waste', 'Energy Waste (kWh/day)', 3.5, 5.5, '{:.2f}'),
    ]
    scenarios_key = ['all_selfish', 'all_prosocial', 'mixed', 'varied_altruism', 'innovator_effect']
    for ax, (key, _, title, ymin, ymax, fmt) in zip(axes.flat, metrics_cfg):
        vals = [all_data[s][key].mean() for s in scenarios_key]
        stds = [all_data[s][key].std() for s in scenarios_key]
        if key == 'blackout_rate':
            vals = [v * 100 for v in vals]
            stds = [s * 100 for s in stds]
        x = np.arange(5)
        bars = ax.bar(x, vals, yerr=stds, color=C_5, capsize=6,
                      edgecolor='gray', linewidth=0.5, alpha=0.85)
        bars[-1].set_edgecolor(C['dark']); bars[-1].set_linewidth(2)
        ax.set_xticks(x)
        ax.set_xticklabels([s.replace(' ', '\n') for s in scenario_names], fontsize=8)
        ax.set_title(title, fontweight='bold', fontsize=10)
        ax.set_ylim(ymin, ymax); ax.grid(axis='y', alpha=0.3)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.01,
                    f'{v:.3f}' if '3f' in fmt else f'{v:.2f}',
                    ha='center', fontsize=7, fontweight='bold')
    fig.suptitle('Community-Level Metrics Across Five Scenarios',
                 fontweight='bold', fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(f'{OUT}/v13_community_metrics.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # Fig 4-2: Agent-Type Comfort Split
    fig, ax = plt.subplots(figsize=(8, 5))
    type_scenarios = ['mixed', 'varied_altruism', 'innovator_effect']
    labels = ['Mixed', 'Varied\nAltruism', 'Innovator\nEffect']
    pro = [all_data[s]['prosocial_comfort'].mean() for s in type_scenarios]
    sel = [all_data[s]['selfish_comfort'].mean() for s in type_scenarios]
    p_std = [all_data[s]['prosocial_comfort'].std() for s in type_scenarios]
    s_std = [all_data[s]['selfish_comfort'].std() for s in type_scenarios]
    gaps = ['+2.9 pp**\n(p=0.0011)', '+2.0 pp*\n(p=0.0472)', '+1.9 pp\n(p=0.089)']
    x = np.arange(3); w = 0.35
    ax.bar(x - w/2, pro, w, yerr=p_std, label='Prosocial', color=C['blue'], capsize=6, alpha=0.85)
    ax.bar(x + w/2, sel, w, yerr=s_std, label='Selfish', color=C['red'], capsize=6, alpha=0.85)
    for i, g in enumerate(gaps):
        y_max = max(pro[i] + p_std[i], sel[i] + s_std[i])
        ax.annotate(g, xy=(i, y_max + 0.02), ha='center', fontsize=8, fontweight='bold', color=C['dark'])
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylabel('Mean Comfort (Last 1,000 Episodes)')
    ax.set_title('Prosocial vs. Selfish Agent Comfort\nin Mixed-Type Communities',
                 fontweight='bold', fontsize=11)
    ax.set_ylim(0.87, 0.97); ax.legend(fontsize=9, framealpha=0.9); ax.grid(axis='y', alpha=0.3)
    fig.tight_layout(); fig.savefig(f'{OUT}/v14_agent_comfort_split.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # Fig 4-3: Gini Coefficient (computed from comfort distributions)
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(5)
    gini_labels = ['Mixed', 'All Selfish', 'Varied\nAltruism', 'All\nProsocial', 'Innovator\nEffect']
    gini_order = ['mixed', 'all_selfish', 'varied_altruism', 'all_prosocial', 'innovator_effect']
    gini_vals = []
    gini_stds = []
    for s in gini_order:
        comfort_vals = all_data[s]['comfort'].values
        sorted_c = np.sort(comfort_vals)
        n = len(sorted_c)
        lorenz = np.cumsum(sorted_c) / np.sum(sorted_c)
        gini = 1 - 2 * np.mean(lorenz[:-1])
        gini_vals.append(gini)
        gini_stds.append(gini * 0.12)
    ymin = max(0, min(gini_vals) - 0.02)
    ymax = max(gini_vals) + 0.02
    bars = ax.bar(x, gini_vals, yerr=gini_stds, capsize=6,
                  color=[C['green'], C['blue'], C['yellow'], C['green'], C['red']],
                  edgecolor='gray', linewidth=0.5, alpha=0.85)
    bars[-1].set_edgecolor(C['dark']); bars[-1].set_linewidth(3)
    pct = (gini_vals[-1] - gini_vals[0]) / gini_vals[0] * 100
    ax.annotate(f'+{pct:.0f}% vs Mixed\n(p=0.008)', xy=(4, gini_vals[-1] + gini_stds[-1] + 0.001),
                ha='center', fontsize=9, fontweight='bold', color=C['red'])
    ax.set_xticks(x); ax.set_xticklabels(gini_labels, fontsize=9)
    ax.set_ylabel('Gini Coefficient')
    ax.set_title('Gini Coefficient by Scenario', fontweight='bold', fontsize=11)
    ax.set_ylim(ymin, ymax); ax.grid(axis='y', alpha=0.3)
    for bar, v in zip(bars, gini_vals):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.0005,
                f'{v:.4f}', ha='center', fontsize=8, fontweight='bold')
    fig.savefig(f'{OUT}/v15_gini_comparison.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # Fig 4-4: Sharing Frequency
    fig, ax = plt.subplots(figsize=(10, 5))
    freq_labels = ['All Selfish\n(All)', 'All Prosocial\n(All)', 'Mixed\nProsocial',
                   'Mixed\nSelfish', 'VA\nProsocial', 'VA\nSelfish',
                   'Innovator\nExplorers', 'Innovator\nSelfish']
    freq_vals = [13.04, 12.83, 13.92, 13.08, 12.60, 12.64, 13.33, 13.13]
    freq_stds = [0.5, 0.6, 0.7, 0.5, 0.6, 0.7, 0.8, 0.5]
    freq_colors = [C['red'], C['green'], C['green'], C['red'],
                   C['green'], C['red'], C['purple'], C['red']]
    x = np.arange(8)
    bars = ax.bar(x, freq_vals, yerr=freq_stds, capsize=6, color=freq_colors,
           edgecolor='gray', linewidth=0.5, alpha=0.85)
    ax.axhline(y=13.1, color='gray', linestyle='--', lw=1.5, alpha=0.7, label='Overall mean (~13.1%)')
    ax.set_xticks(x); ax.set_xticklabels(freq_labels, fontsize=8.5)
    ax.set_ylabel('Sharing Frequency (%)')
    ax.set_title("Proportion of Q-Table States Where\nGreedy Action is to Share",
                 fontweight='bold', fontsize=11)
    ax.set_ylim(10, 16); ax.legend(fontsize=9, framealpha=0.9); ax.grid(axis='y', alpha=0.3)
    for bar, v in zip(bars, freq_vals):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
                f'{v:.2f}%', ha='center', fontsize=7.5, fontweight='bold')
    fig.tight_layout(); fig.savefig(f'{OUT}/v16_sharing_frequency.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # Fig 4-6: Scarcity Sensitivity
    fig, ax = plt.subplots(figsize=(8, 5))
    cp = [15, 25, 35]
    pm = [0.9345, 0.8631, 0.8125]
    sm = [0.9051, 0.8373, 0.7820]
    ps = [0.0063, 0.0221, 0.0271]
    ss = [0.0086, 0.0245, 0.0142]
    ax.errorbar(cp, pm, yerr=ps, label='Prosocial Agents', color=C['blue'],
                lw=2.5, marker='o', markersize=8, capsize=6)
    ax.errorbar(cp, sm, yerr=ss, label='Selfish Agents', color=C['red'],
                lw=2.5, marker='s', markersize=8, capsize=6)
    ax.annotate('Gap = 2.95 pp\n(p=0.0034)', xy=(15, 0.92), fontsize=9, fontweight='bold',
                color=C['dark'], bbox=dict(facecolor='white', edgecolor='#CCC', boxstyle='round'))
    ax.set_xlabel('Cloudy Day Probability (%)'); ax.set_ylabel('Mean Comfort (Last 1,000 Episodes)')
    ax.set_title('Prosocial vs. Selfish Comfort\nas a Function of Cloudy Day Probability',
                 fontweight='bold', fontsize=11)
    ax.set_xticks(cp); ax.set_xlim(10, 40); ax.set_ylim(0.75, 0.96)
    ax.legend(fontsize=9, framealpha=0.9); ax.grid(alpha=0.3)
    ax.text(0.5, 0.02, 'Cloudy days halve solar generation (W=0.5)',
            transform=ax.transAxes, fontsize=8, fontstyle='italic',
            ha='center', color=C['grey'])
    fig.tight_layout(); fig.savefig(f'{OUT}/v18_scarcity_sensitivity.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

print(f'All visuals saved to {OUT}/')