import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import os

from thesis_plot_style import (
    C, FA_FONTS, SCENARIO_COLORS, SCENARIO_LABELS, apply_rc, fa,
    label_bars, save_fig, style_bars, style_data_axes, style_legend,
)

OUT = 'results/figures'
BASE = 'results'
QTABLE_OUT = f'{BASE}/qtable_heatmaps.png'
os.makedirs(OUT, exist_ok=True)
apply_rc()

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
# Figure 3-5: OCEAN-to-RL Parameter Mapping (conceptual schematic)
# EN conversion 2026-08-16 — Persian originals (also in git HEAD 1731705):
#   title 'نگاشت ویژگی‌های شخصیت OCEAN به پارامترهای یادگیری تقویتی';
#   traits 'گشودگی/وظیفه‌شناسی/برون‌گرایی/توافق‌پذیری/روان‌رنجوری';
#   'کف اکتشاف' · 'وزن عدالت در پاداش' · 'ثابت در میانگین جمعیتی'
with plt.rc_context({'font.family': 'sans-serif'}):
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 11); ax.set_ylim(0, 8); ax.axis('off')
    ax.set_title('Mapping OCEAN Personality Traits to RL Parameters',
                 fontweight='bold', fontsize=12, pad=12)
    traits = [
        ('Openness', C['purple'], True),
        ('Conscientiousness', C['blue'], False),
        ('Extraversion', C['orange'], False),
        ('Agreeableness', C['green'], True),
        ('Neuroticism', C['red'], False),
    ]
    ys = [7.0, 5.6, 4.2, 2.8, 1.4]
    for (name, col, active), y in zip(traits, ys):
        if active:
            _box(2.0, y, 3.4, 0.9, name, col, fs=10, fc='tint')
        else:
            _box(2.0, y, 3.4, 0.9, name, C['grey'], fs=10, fc='tint')
        if active:
            sym = (r'$\varepsilon_{\min}$', 'exploration floor') if name == 'Openness' \
                else (r'$w_{\mathrm{fair}}$', 'fairness weight in reward')
            ax.annotate('', xy=(6.0, y), xytext=(3.9, y),
                        arrowprops=dict(arrowstyle='->', color=col, lw=2.2))
            _box(7.8, y, 3.0, 0.9, sym[0], col, fs=12, fc='tint')
            ax.text(7.8, y - 0.6, sym[1], ha='center', va='center',
                    fontsize=7.5, color=col)
        else:
            ax.text(5.6, y, 'fixed at population mean', ha='center', va='center',
                    fontsize=8.5, fontstyle='italic', color=C['grey'])
    save_fig(fig, f'{OUT}/v01_ocean_to_rl_mapping.png')
    plt.close(fig)

# ═══════════════════════════════════════════════
# Figure 3-2: Ring Topology (conceptual schematic)
# EN conversion 2026-08-16 — Persian original title (also in git HEAD 1731705):
#   'توپولوژی حلقه‌ای ریزشبکه محله‌ای با ۱۰ خانه'
with plt.rc_context({'font.family': 'sans-serif'}):
    fig, ax = plt.subplots(figsize=(9, 9))
    ax.set_xlim(-3.4, 3.4); ax.set_ylim(-3.6, 3.4)
    ax.axis('off'); ax.set_aspect('equal')
    ax.set_title('Ring-Topology Neighbourhood Microgrid with 10 Houses',
                 fontweight='bold', fontsize=12, pad=12)
    n = 10
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    R = 2.35

    def house_icon(cx, cy, s=0.34):
        ax.add_patch(mpatches.Polygon(
            [(cx - 1.15 * s, cy + 0.5 * s), (cx + 1.15 * s, cy + 0.5 * s),
             (cx, cy + 1.25 * s)], facecolor=C['blue'], alpha=0.25,
            edgecolor=C['blue'], lw=1.4, zorder=4))
        ax.add_patch(mpatches.Rectangle(
            (cx - s, cy - 0.55 * s), 2 * s, 1.05 * s,
            facecolor='white', edgecolor=C['blue'], lw=1.6, zorder=4))
        ax.add_patch(mpatches.Rectangle(
            (cx - 0.7 * s, cy + 0.6 * s), 1.4 * s, 0.3 * s,
            facecolor=C['blue'], alpha=0.55, zorder=5))
        ax.add_patch(mpatches.Rectangle(
            (cx - 0.35 * s, cy - 0.4 * s), 0.7 * s, 0.28 * s,
            facecolor=C['teal'], alpha=0.6, edgecolor=C['teal'], lw=0.8, zorder=5))

    for i in range(n):
        a1, a2 = angles[i], angles[(i + 1) % n]
        ax.plot([R * np.cos(a1), R * np.cos(a2)],
                [R * np.sin(a1), R * np.sin(a2)],
                color=C['grey'], lw=2.5, zorder=1)
    for i, a in enumerate(angles):
        x, y = R * np.cos(a), R * np.sin(a)
        house_icon(x, y)
        ax.text(x, y - 0.8, str(i + 1), ha='center', va='top', fontsize=9,
                fontweight='bold', color=C['dark'])
    save_fig(fig, f'{OUT}/v02_ring_topology.png')
    plt.close(fig)

# ═══════════════════════════════════════════════
# Figure 3-6: Two-Phase Energy Sharing (conceptual schematic)
# EN conversion 2026-08-16 — Persian originals (also in git HEAD 1731705):
#   'فاز ۱ — محلی' · 'فاز ۲ — اشتراک' · 'خروجی مصرف‌شده در همان خانه' ·
#   'تولید خورشیدی' · 'نیاز ساعتی' · 'شارژ باتری' · 'تخلیه باتری' ·
#   'مازاد قابل صادرات' · 'نیاز تأمین‌نشده' · 'تولید > نیاز؟' · 'بله/خیر' ·
#   '(ظرفیت ۷ کیلووات‌ساعت)' · 'مازاد صادرشدنی' · 'اقدام عامل: ۰٪/۵۰٪/۱۰۰٪' ·
#   'ارسال به همسایه' · 'کاهش نیاز تأمین‌نشده' · 'ذخیره مازاد در باتری' ·
#   'هدررفت انرژی' · 'مازاد به فاز ۲ منتقل می‌شود'
with plt.rc_context({'font.family': 'sans-serif'}):
    fig, ax = plt.subplots(figsize=(12, 6.5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6.5); ax.axis('off')
    ax.text(0.3, 5.6, 'Phase 1 — Local', fontsize=10, fontweight='bold',
            color=C['blue'], va='center')
    ax.text(0.3, 2.4, 'Phase 2 — Sharing', fontsize=10, fontweight='bold',
            color=C['purple'], va='center')
    ax.text(8.6, 5.9, 'output consumed in the same house',
            fontsize=7.5, fontstyle='italic', color=C['grey'])
    boxes_p1 = [
        (1.0, 4.5, 1.6, 0.6, 'Solar generation', C['blue']),
        (3.0, 4.5, 1.4, 0.6, 'Hourly demand', C['dark']),
        (7.5, 5.2, 1.6, 0.6, 'Battery charge', C['green']),
        (7.5, 3.8, 1.6, 0.6, 'Battery discharge', C['red']),
        (9.8, 5.2, 1.6, 0.6, 'Exportable surplus', C['green']),
        (9.8, 3.8, 1.6, 0.6, 'Unmet demand', C['red']),
    ]
    for args in boxes_p1:
        _box(*args, fc='tint')
    diamond = mpatches.Polygon([(5.2, 4.9), (6.0, 4.5), (5.2, 4.1), (4.4, 4.5)],
                               facecolor=C['orange'], alpha=0.15,
                               edgecolor=C['orange'], lw=1.5)
    ax.add_patch(diamond)
    ax.text(5.2, 4.5, 'Generation > demand?', ha='center', va='center', fontsize=8,
            fontweight='bold', color=C['orange'])
    ax.text(5.9, 4.9, 'Yes', fontsize=7, color=C['green'], fontweight='bold')
    ax.text(5.9, 4.1, 'No', fontsize=7, color=C['red'], fontweight='bold')
    _arrow(3.7, 4.5, 4.4, 4.5, C['blue'])
    _arrow(1.8, 4.5, 2.3, 4.5, C['dark'])
    _arrow(5.7, 4.9, 6.7, 5.2, C['green'])
    _arrow(5.7, 4.1, 6.7, 3.8, C['red'])
    _arrow(8.3, 5.2, 9.0, 5.2, C['green'])
    _arrow(8.3, 3.8, 9.0, 3.8, C['red'])
    ax.text(6.0, 5.55, '(7 kWh capacity)', ha='center', va='center',
            fontsize=7, color=C['green'])
    boxes_p2 = [
        (1.5, 1.5, 1.6, 0.6, 'Exportable surplus', C['green']),
        (3.5, 1.5, 1.6, 0.6, 'Agent action:\n0% / 50% / 100%', C['purple']),
        (5.5, 1.5, 1.4, 0.6, 'Send to neighbour', C['blue']),
        (7.5, 1.9, 1.8, 0.6, 'Reduces unmet demand', C['green']),
        (7.5, 1.1, 1.8, 0.6, 'Store surplus in battery', C['teal']),
        (10.0, 1.5, 1.6, 0.6, 'Energy waste', C['red']),
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
    ax.text(11.15, 3.5, 'Surplus\ncarried to Phase 2', ha='center',
            va='center', fontsize=7.5, color=C['dark'])
    save_fig(fig, f'{OUT}/v03_two_phase_sharing.png')
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
ax.set_title('The Four Hourly Demand Profile Types', fontweight='bold', fontsize=11)
ax.set_xticks([0, 6, 12, 18, 23]); ax.set_xlim(0, 23); ax.set_ylim(0, 1.4)
leg = ax.legend(loc='upper right'); style_legend(leg); style_data_axes(ax, grid_axis='both')
ax.text(23, 0.05, 'Daily Total Range: 8.4–9.6 kWh',
        ha='right', va='bottom', fontsize=8, fontstyle='italic', color=C['grey'])
fig.tight_layout(); save_fig(fig, f'{OUT}/v04_demand_profiles.png')
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
            fontsize=8, color=C['dark'],
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))
ax.text(12, 0.2, 'Eq. 3-1: G(h) = G$_\\max$ sin($\\pi$(h-6)/12) W',
        ha='center', fontsize=8, fontstyle='italic', color=C['grey'])
ax.text(12, 0.05, 'Cloudy days with 15% probability (Bernoulli draw)',
        ha='center', fontsize=8, fontstyle='italic', color=C['grey'])
ax.set_xlabel('Hour of Day'); ax.set_ylabel('Solar Generation (kW)')
ax.set_title('Half-Sine Solar Irradiance Model', fontweight='bold', fontsize=11)
ax.set_xticks([0, 6, 12, 18, 23]); ax.set_xlim(0, 23); ax.set_ylim(0, 1.5)
leg = ax.legend(loc='upper left'); style_legend(leg); style_data_axes(ax, grid_axis='both')
fig.tight_layout(); save_fig(fig, f'{OUT}/v05_solar_curve.png')
plt.close(fig)

# ═══════════════════════════════════════════════
# Figure 3-7: Experimental Community Compositions (conceptual schematic)
# EN conversion 2026-08-16 — Persian originals (also in git HEAD 1731705):
#   'ترکیب‌های جامعه در سناریوهای آزمایش' · 'همه خودخواه' · 'همه نوع‌دوست' · 'آمیخته' ·
#   'نوع‌دوستی متغیر' · 'اثر نوآور' · 'نوع‌دوست، wf=0.8' · 'نوع‌دوست، wf=0.5' ·
#   'فردگرا، wf=0.2' · 'کاملاً خودخواه، wf=0.0' · 'نوآور، εmin=0.05'
with plt.rc_context({'font.family': 'sans-serif'}):
    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.set_xlim(-1.6, 12); ax.set_ylim(-1.5, 6.8); ax.axis('off')
    ax.set_title('Community Compositions in Experimental Scenarios',
                 fontweight='bold', fontsize=12, pad=10)
    scenarios_grid = [
        ('All Selfish', [C['red']] * 10),
        ('All Prosocial', [C['green']] * 10),
        ('Mixed', [C['green']] * 5 + [C['red']] * 5),
        ('Varied Altruism',
         [C['teal']] + [C['green']] * 3 + [C['yellow']] * 3 + [C['red']] * 3),
        ('Innovator Effect',
         [C['purple']] + [C['green']] * 4 + [C['yellow']] * 3 + [C['red']] * 2),
    ]
    for row, (label, colors) in enumerate(scenarios_grid):
        y = 5.6 - row * 1.15
        ax.text(-1.2, y, label, ha='right', va='center', fontsize=9,
                fontweight='bold', color=C['dark'])
        for col, c in enumerate(colors):
            ax.add_patch(plt.Circle((col + 0.5, y), 0.35,
                                    facecolor=c, edgecolor='white', lw=1.5,
                                    alpha=0.85))
        if row == 0:
            for col in range(10):
                ax.text(col + 0.5, y + 0.55, str(col), ha='center', va='center',
                        fontsize=7, color=C['grey'])
    leg_y = -0.55
    for i, (c, lbl) in enumerate([
        (C['teal'], 'Altruistic, wf=0.8'),
        (C['green'], 'Prosocial, wf=0.5'),
        (C['yellow'], 'Individualist, wf=0.2'),
        (C['red'], 'Purely selfish, wf=0.0'),
        (C['purple'], 'Innovator, εmin=0.05'),
    ]):
        row = i // 3
        col = i % 3
        cx = 0.6 + col * 3.9
        cy = leg_y - row * 0.6
        ax.add_patch(plt.Circle((cx, cy), 0.2, facecolor=c, edgecolor=C['grey']))
        ax.text(cx + 0.32, cy, lbl, ha='left', va='center', fontsize=7.5, color=C['dark'])
    save_fig(fig, f'{OUT}/v06_community_compositions.png')
    plt.close(fig)

# ═══════════════════════════════════════════════
# Figure 4-3: Emergent Reciprocity Mechanism (conceptual schematic)
# EN conversion 2026-08-16 — Persian originals (also in git HEAD 1731705):
#   'مکانیزمِ برخاستهٔ مقابله‌به‌مثل (متقابلیت)' · 'نوع‌دوست مازاد را هم‌ساعت ۱۰ تا ۱۶
#   می‌فرستد' · 'باتری همسایه پایدار می‌ماند' · 'همسایه شب‌هنگام انرژی برمی‌گرداند' ·
#   'نوع‌دوست هنگام کسری دریافت می‌کند' · 'بازخورد تقویتی' ·
#   'چرخه فضیلت (نوع‌دوست)' · 'چرخه‌های شرورانه (خودخواه)'
with plt.rc_context({'font.family': 'sans-serif'}):
    fig, ax = plt.subplots(figsize=(8.5, 8.5))
    ax.set_xlim(-2.7, 2.7); ax.set_ylim(-2.7, 2.7)
    ax.axis('off'); ax.set_aspect('equal')
    ax.set_title('Emergent Reciprocity Mechanism',
                 fontweight='bold', fontsize=12, pad=12)
    def draw_cycle(positions, edge_color, fill_color):
        half_w, half_h = 0.95, 0.4
        for (x, y), text, _ in positions:
            ax.add_patch(FancyBboxPatch((x - half_w, y - half_h), half_w * 2, half_h * 2,
                                        boxstyle="round,pad=0.08",
                                        facecolor=fill_color, edgecolor=edge_color,
                                        lw=2.5, alpha=0.15))
            ax.text(x, y, text, ha='center', va='center', fontsize=8.5,
                    fontweight='bold', color=C['dark'])
        n = len(positions)
        for i in range(n):
            x1, y1 = positions[i][0]
            x2, y2 = positions[(i + 1) % n][0]
            dx, dy = x2 - x1, y2 - y1
            d = np.sqrt(dx**2 + dy**2)
            ux, uy = dx / d, dy / d
            off1 = half_w if abs(ux) > abs(uy) else half_h
            off2 = half_w if abs(ux) > abs(uy) else half_h
            x1a, y1a = x1 + ux * off1, y1 + uy * off1
            x2a, y2a = x2 - ux * off2, y2 - uy * off2
            ax.annotate('', xy=(x2a, y2a), xytext=(x1a, y1a),
                        arrowprops=dict(arrowstyle='->', color=edge_color,
                                        lw=2.5, alpha=0.9))
    draw_cycle([
        ((-1.0, -0.65), 'Prosocial sends surplus\n10:00–16:00', C['green']),
        ((1.0, -0.65), 'Neighbour battery\nstays stable', C['teal']),
        ((1.0, 0.65), 'Neighbour returns\nenergy at night', C['blue']),
        ((-1.0, 0.65), 'Prosocial receives\nwhen in deficit', C['purple']),
    ], C['green'], C['green'])
    ax.text(0, 0.45, '+', ha='center', va='center', fontsize=20,
            fontweight='bold', color=C['green'])
    ax.text(0, 0.02, 'Reinforcing feedback', ha='center', va='center',
            fontsize=9, fontstyle='italic', color=C['green'])
    ax.plot([-2.5, -2.1], [-2.35, -2.35], color=C['green'], lw=2.5)
    ax.text(-1.8, -2.35, 'Virtuous cycle (prosocial)', ha='left', va='center',
            fontsize=9, color=C['green'], fontweight='bold')
    ax.plot([-2.5, -2.1], [-2.65, -2.65], color=C['red'], lw=2.5)
    ax.text(-1.8, -2.65, 'Vicious cycles (selfish)', ha='left', va='center',
            fontsize=9, color=C['red'], fontweight='bold')
    save_fig(fig, f'{OUT}/v07_reciprocity_cycle.png')
    plt.close(fig)

# ═══════════════════════════════════════════════
# Figure 4-9: Innovator Effect Mechanism (conceptual schematic)
# EN conversion 2026-08-16 — Persian originals (also in git HEAD 1731705):
#   'مکانیزم اثر نوآور: غیرقابل‌پیش‌بینی بودن، نه کاهش اشتراک' ·
#   'عامل نوآور εmin = 0.05 (در برابر 0.01)' · 'ادامه اکتشاف تصادفی پس از همگرایی
#   بقیه' · 'همسایه‌ها نمی‌توانند انتظار پایدار شکل دهند' · 'تغییر به احتکار دفاعی' ·
#   'نابرابری بیشتر' · 'آسایش کمتر' · 'خاموشی بیشتر' · 'گشودگی بالاتر (OCEAN)' ·
#   'مسئله اکتشافِ دیگری' · 'عرضه انرژی غیرقابل‌پیش‌بینی' · 'استراتژی خودحفاظتی'
with plt.rc_context({'font.family': 'sans-serif'}):
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.set_xlim(0, 12); ax.set_ylim(-0.3, 5.5); ax.axis('off')
    ax.set_title('Innovator Effect Mechanism: Unpredictability, Not Reduced Sharing',
                 fontweight='bold', fontsize=12, pad=10)
    _arrow(2.3, 4.2, 2.7, 4.2, C['purple'])
    _arrow(4.9, 4.2, 5.4, 4.2, C['orange'])
    _arrow(7.4, 4.2, 8.1, 4.2, C['red'])
    _arrow(9.0, 3.4, 9.0, 2.4, C['red'])
    for cx, cy, text, color in [
        (1.2, 4.2, 'Innovator agent\nεmin = 0.05 (vs 0.01)', C['purple']),
        (3.8, 4.2, 'Continues random exploration\nafter others converge', C['orange']),
        (6.4, 4.2, 'Neighbours cannot form\nstable expectations', C['red']),
        (9.0, 4.2, 'Shift to defensive hoarding', C['dark']),
    ]:
        _box(cx, cy, 2.2, 0.8, text, color, fs=8.5, fc='tint')
    for cx, cy, text, color in [
        (5.6, 1.6, 'Higher inequality', C['red']),
        (7.8, 1.6, 'Lower comfort', C['red']),
        (10.0, 1.6, 'More blackouts', C['red']),
    ]:
        _box(cx, cy, 1.8, 0.7, text, color, fs=8, fc='tint')
    ax.text(0.8, 3.6, 'Higher openness (OCEAN)', ha='center', va='center',
            fontsize=7, fontstyle='italic', color=C['grey'])
    ax.text(3.8, 3.4, 'The alter-exploration problem', ha='center', va='center',
            fontsize=7, fontstyle='italic', color=C['grey'])
    ax.text(6.4, 3.4, 'Unpredictable energy supply', ha='center', va='center',
            fontsize=7, fontstyle='italic', color=C['grey'])
    ax.text(9.0, 3.4, 'Self-protective strategy', ha='center', va='center',
            fontsize=7, fontstyle='italic', color=C['grey'])
    save_fig(fig, f'{OUT}/v08_innovator_effect.png')
    plt.close(fig)

# ═══════════════════════════════════════════════
# Figure 1-1: Tragedy of the Commons (conceptual schematic, Persian)
with plt.rc_context({'font.family': FA_FONTS}):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis('off')
    ax.set_title(fa('تراژدی منابع مشترک در اشتراک انرژی: دوراهی احتکار در برابر اشتراک'),
                 fontweight='bold', fontsize=12, pad=10)
    ax.add_patch(FancyBboxPatch((0.3, 0.3), 4.2, 4.2,
                                 boxstyle="round,pad=0.08",
                                 facecolor=C['green'], edgecolor=C['grey'], lw=1.5, alpha=0.12))
    ax.text(2.4, 4.6, fa('تراژدی منابع مشترک\n(هاردین، ۱۹۶۸)'),
            ha='center', va='center', fontsize=9, fontweight='bold', color=C['green'])
    for x, y in [(1.0, 3.2), (2.5, 3.7), (1.8, 2.5), (3.2, 2.9)]:
        ax.plot(x, y, 'o', color=C['orange'], markersize=16, zorder=5)
    ax.add_patch(mpatches.FancyBboxPatch((1.2, 0.6), 1.5, 0.8,
                                          boxstyle="round,pad=0.05",
                                          facecolor=C['orange'], alpha=0.5))
    ax.text(1.95, 1.0, fa('چراگاه فرسوده'), ha='center', va='center',
            fontsize=7, color=C['orange'], fontweight='bold')
    ax.text(2.4, 0.35, fa('هر چوپان سود خود را بیشینه می‌کند\n↓\nمنبع برای همه نابود می‌شود'),
            ha='center', va='center', fontsize=6.5, color=C['grey'], fontstyle='italic')
    ax.add_patch(FancyBboxPatch((5.5, 0.3), 4.2, 4.2,
                                 boxstyle="round,pad=0.08",
                                 facecolor=C['blue'], edgecolor=C['grey'], lw=1.5, alpha=0.12))
    ax.text(7.6, 4.6, fa('قیاس اشتراک انرژی\n(این پژوهش)'),
            ha='center', va='center', fontsize=9, fontweight='bold', color=C['blue'])
    for i, angle in enumerate(np.linspace(0, 2 * np.pi, 6, endpoint=False)):
        col = C['green'] if i < 3 else C['red']
        x = 7.6 + 1.5 * np.cos(angle)
        y = 2.8 + 1.5 * np.sin(angle)
        ax.add_patch(mpatches.Rectangle((x - 0.3, y - 0.25), 0.6, 0.4,
                                         facecolor='white', edgecolor=col, lw=2))
        ax.add_patch(mpatches.Polygon([(x - 0.35, y + 0.15), (x + 0.35, y + 0.15),
                                        (x, y + 0.35)], facecolor=col, alpha=0.3))
        label = fa('کامل') if i < 3 else fa('خاموشی')
        ax.text(x, y - 0.45, label, ha='center', va='top', fontsize=6.5,
                fontweight='bold', color=col)
    ax.text(7.6, 0.35, fa('هر خانوار مازاد خود را احتکار می‌کند\n↓\nهدررفت انرژی و خاموشی همسایه'),
            ha='center', va='center', fontsize=6.5, color=C['grey'], fontstyle='italic')
    ax.text(5.0, 2.4, fa('عقلانیت فردی\n↓\nناعقلانیتی جمعی'),
            ha='center', va='center', fontsize=10, fontweight='bold', color=C['dark'],
            bbox=dict(facecolor='white', edgecolor=C['grey'], boxstyle='round,pad=0.4'))
    save_fig(fig, f'{OUT}/v09_tragedy_commons.png')
    plt.close(fig)

# ═══════════════════════════════════════════════
# Fig 4-10 / SOTA comparison rebuilt from real baseline_comparison.csv
# (thesis Table 4-10: 5 OCEAN-MARL scenarios + 4 reproduced baselines + control)
fig, ax = plt.subplots(figsize=(13, 5))
bdf = pd.read_csv(f'{BASE}/baseline_comparison.csv')
order = ['OCEAN-MARL all-selfish', 'OCEAN-MARL all-prosocial', 'OCEAN-MARL mixed',
         'OCEAN-MARL varied-altruism', 'OCEAN-MARL innovator-effect',
         'Charbonnier marginal-IQL', 'Kusatake NSGA-II', 'Behrunani GNE',
         'May & Huang PPO', 'always_default (control)']
labels = ['OCEAN-MARL\nAll Selfish', 'OCEAN-MARL\nAll Prosocial', 'OCEAN-MARL\nMixed',
          'OCEAN-MARL\nVaried Altruism', 'OCEAN-MARL\nInnovator Effect',
          'Charbonnier\net al. (2022)', 'Kusatake\net al. (2023)', 'Behrunani\net al. (2023)',
          'May & Huang\n(2023)', 'always_default\n(control)']
comfort = [bdf[bdf['method'] == m]['comfort'].mean() for m in order]
c_std = [bdf[bdf['method'] == m]['comfort'].std(ddof=1) for m in order]
fairness = [bdf[bdf['method'] == m]['fairness'].mean() for m in order]
f_std = [bdf[bdf['method'] == m]['fairness'].std(ddof=1) for m in order]
x = np.arange(len(order)); w = 0.38
ours = [True] * 5 + [False] * 5
ax.bar(x - w/2, comfort, w, yerr=c_std, color=C['blue'], capsize=6,
       edgecolor=[C['dark'] if o else C['grey'] for o in ours],
       linewidth=[1.2 if o else 0.6 for o in ours],
       label='Community Comfort', alpha=0.85, zorder=3)
ax.bar(x + w/2, fairness, w, yerr=f_std, color=C['green'], capsize=6,
       edgecolor=[C['dark'] if o else C['grey'] for o in ours],
       linewidth=[1.2 if o else 0.6 for o in ours],
       label="Jain's Fairness Index", alpha=0.85, zorder=3)
for i, (c, fs) in enumerate(zip(comfort, fairness)):
    ax.text(i - w/2, c + c_std[i] + 0.004, f'{c:.3f}', ha='center', fontsize=7.5, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))
    ax.text(i + w/2, fs + f_std[i] + 0.004, f'{fs:.3f}', ha='center', fontsize=7.5, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))
ax.axvline(4.5, color=C['grey'], lw=0.8, ls='--', zorder=0)
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=8.5)
ax.set_ylabel('Score')
ax.set_title('Comparison with State-of-the-Art Energy MARL Studies', fontweight='bold', fontsize=11)
ax.set_ylim(0.86, 0.97)
leg = ax.legend(loc='lower right'); style_legend(leg); style_data_axes(ax)
ax.text(0.03, -0.12, '\u2020 Reproduced baselines + always_default control; bars = mean \u00b1 SD over 5 seeds',
        transform=ax.transAxes, fontsize=7, fontstyle='italic', color=C['grey'])
fig.subplots_adjust(bottom=0.25)
save_fig(fig, f'{OUT}/v10_sota_comparison.png')
plt.close(fig)

# ═══════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7, 7))
lc = np.load(f'{BASE}/analysis_support/house_comfort/lorenz_curves.npy',
             allow_pickle=True).item()
houses = np.linspace(0, 1, 11)
ax.plot([0, 1], [0, 1], '--', color=C['grey'], lw=1.5, label='Perfect Equality', alpha=0.7)
ax.fill_between(houses, houses, lc['mixed'], alpha=0.12, color=C['blue'])
ax.fill_between(houses, houses, lc['innovator_effect'], alpha=0.12, color=C['red'])
ax.plot(houses, lc['mixed'], '-', color=C['blue'], lw=2.5,
        label='Mixed Scenario (Gini = 0.079)', marker='o', markersize=4, markevery=2)
ax.plot(houses, lc['innovator_effect'], '-', color=C['red'], lw=2.5,
        label='Innovator Effect (Gini = 0.096)', marker='s', markersize=4, markevery=2)
ax.annotate('Gini = 0.079', xy=(0.55, 0.52), fontsize=9,
            color=C['blue'], fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))
ax.annotate('Gini = 0.096', xy=(0.55, 0.44), fontsize=9,
            color=C['red'], fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))
ax.set_xlabel('Cumulative Share of Houses (poorest $\\to$ richest)')
ax.set_ylabel('Cumulative Share of Comfort')
ax.set_title('Lorenz Curves — Mixed vs. Innovator Effect\n'
             '(mean of per-episode cross-sectional distributions, last 1,000 episodes)',
             fontweight='bold', fontsize=11)
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect('equal')
leg = ax.legend(loc='upper left'); style_legend(leg); style_data_axes(ax, grid_axis='both')
fig.tight_layout(); save_fig(fig, f'{OUT}/v11_lorenz_curve.png')
plt.close(fig)

# ═══════════════════════════════════════════════
# Figure 3-1: System Architecture Flowchart (conceptual schematic)
# EN conversion 2026-08-16 — Persian originals (also in git HEAD 1731705):
#   'معماری سیستم: حلقه شبیه‌سازی ده‌بلوکی' · 'حلقه محیط' · 'به‌روزرسانی یادگیری' ·
#   '1: بازنشانی محیط (باتری 50٪، آب‌وهوای تصادفی)' · '2: تولید خورشیدی (نیم‌سینوسی،
#   Eq. 3-1)' · '3: تحقق تقاضا (4 الگوی مصرف)' · '4: مشاهده وضعیت (ساعت، سطح باتری)' ·
#   '5: اشتراک انرژی (ε-حریصانه از Q)' · '6: محاسبه پاداش (Eq. 3-2 تا 3-4)' ·
#   '7: به‌روزرسانی Q(s,a) (Eq. 3-5)' · '9: ساعت بعدی (h+1) یا پایان قسمت (h=23)' ·
#   '10: ثبت معیارها (هر 100 قسمت)' · 'قسمت بعد'
with plt.rc_context({'font.family': 'sans-serif'}):
    fig, ax = plt.subplots(figsize=(10, 9.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 9.5); ax.axis('off')
    ax.set_title('System Architecture: Ten-Block Simulation Loop',
                 fontweight='bold', fontsize=13, pad=15)
    def arch_box(cx, cy, w, h, text, color, fs=8.5):
        ax.add_patch(FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                                     boxstyle="round,pad=0.08",
                                     facecolor=color, edgecolor=color,
                                     lw=1.8, alpha=0.12))
        ax.text(cx, cy, text, ha='center', va='center', fontsize=fs,
                fontweight='bold', color=C['dark'])
    def arch_arrow(x1, y1, x2, y2, color=C['dark'], lw=1.8):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=lw))

    ax.text(1.5, 9.2, 'Environment loop', ha='center', va='bottom',
            fontsize=7.5, fontweight='bold', color=C['blue'])
    ax.text(8.5, 9.2, 'Learning updates', ha='center', va='bottom',
            fontsize=7.5, fontweight='bold', color=C['green'])

    left_boxes = [
        (1.5, 8.0, '1: Reset environment\n(battery 50%, random weather)', C['blue']),
        (1.5, 6.4, '2: Solar generation\n(half-sine, Eq. 3-1)', C['blue']),
        (1.5, 4.8, '3: Demand realisation\n(4 consumption patterns)', C['blue']),
        (1.5, 3.2, '4: Observe state\n(hour, battery level)', C['blue']),
        (1.5, 1.6, '5: Energy sharing\n(ε-greedy on Q)', C['teal']),
    ]
    right_boxes = [
        (8.5, 8.0, '6: Compute reward\n(Eqs. 3-2 to 3-4)', C['green']),
        (8.5, 6.4, '7: Update Q(s,a)\n(Eq. 3-5)', C['green']),
        (8.5, 4.8, '8: Reduce exploration\n(ε = max(ε_min, ε × 0.999))', C['orange']),
        (8.5, 3.2, '9: Next hour (h+1)\nor episode end (h=23)', C['orange']),
        (8.5, 1.6, '10: Log metrics\n(every 100 episodes)', C['purple']),
    ]

    for cx, cy, text, color in left_boxes:
        arch_box(cx, cy, 2.6, 0.85, text, color)
    for cx, cy, text, color in right_boxes:
        arch_box(cx, cy, 2.6, 0.85, text, color)

    for i in range(4):
        y_center = 8.0 - i * 1.6
        arch_arrow(1.5, y_center - 0.425, 1.5, y_center - 1.6 + 0.425, C['blue'])

    arch_arrow(1.5, 1.6 - 0.425, 4.5, 0.5, C['teal'])
    arch_arrow(4.5, 0.5, 8.5, 0.5, C['teal'], lw=1.2)
    arch_arrow(8.5, 0.5, 8.5, 8.0 - 0.425, C['green'])

    for i in range(4):
        y_center = 8.0 - i * 1.6
        arch_arrow(8.5, y_center - 0.425, 8.5, y_center - 1.6 + 0.425, C['green'])

    ax.annotate('', xy=(0.7, 3.2), xytext=(0.7, 4.8),
                arrowprops=dict(arrowstyle='->', color=C['teal'], lw=1.5,
                                connectionstyle='arc3,rad=0.5'))
    ax.text(0.35, 4.0, 'h < 23', ha='center', va='center', fontsize=7,
            fontstyle='italic', color=C['teal'],
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    ax.annotate('', xy=(1.5, 8.0 + 0.425), xytext=(8.5, 1.6),
                arrowprops=dict(arrowstyle='->', color=C['purple'], lw=1.5,
                                connectionstyle='arc3,rad=-0.45',
                                linestyle='dashed'))
    mid_x, mid_y = 5.8, 5.5
    ax.text(mid_x, mid_y, 'Next episode', ha='center', va='center', fontsize=7.5,
            fontstyle='italic', color=C['purple'],
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    save_fig(fig, f'{OUT}/v12_system_architecture.png')
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
        bars = ax.bar(x, vals, yerr=stds, color=SCENARIO_COLORS, capsize=6, alpha=0.85)
        style_bars(bars, highlight_indices=[4])
        ax.set_xticks(x)
        ax.set_xticklabels([s.replace(' ', '\n') for s in SCENARIO_LABELS], fontsize=8)
        ax.set_title(title, fontweight='bold', fontsize=10)
        ax.set_ylim(ymin, ymax)
        style_data_axes(ax)
        label_bars(ax, bars, vals, fmt=fmt, offset=0.01 if '3f' in fmt else 0.05, fontsize=7, errs=stds)
    fig.suptitle('Community-Level Metrics Across Five Scenarios', fontweight='bold', fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    save_fig(fig, f'{OUT}/v13_community_metrics.png')
    plt.close(fig)

    # Fig 4-2: Agent-Type Comfort Split
    fig, ax = plt.subplots(figsize=(8, 5))
    type_scenarios = ['mixed', 'varied_altruism', 'innovator_effect']
    labels = ['Mixed', 'Varied\nAltruism', 'Innovator\nEffect']
    pro = [all_data[s]['prosocial_comfort'].mean() for s in type_scenarios]
    sel = [all_data[s]['selfish_comfort'].mean() for s in type_scenarios]
    p_std = [all_data[s]['prosocial_comfort'].std() for s in type_scenarios]
    s_std = [all_data[s]['selfish_comfort'].std() for s in type_scenarios]
    gaps = ['+2.9 pp**\n(p=0.0011)', '+2.0 pp*\n(p=0.0472)', '+1.9 pp']
    x = np.arange(3); w = 0.35
    b1 = ax.bar(x - w/2, pro, w, yerr=p_std, label='Prosocial Agents', color=C['blue'],
                capsize=6, alpha=0.85, edgecolor=C['grey'], linewidth=0.6)
    b2 = ax.bar(x + w/2, sel, w, yerr=s_std, label='Selfish Agents', color=C['red'],
                capsize=6, alpha=0.85, edgecolor=C['grey'], linewidth=0.6)
    for i, g in enumerate(gaps):
        y_max = max(pro[i] + p_std[i], sel[i] + s_std[i])
        ax.annotate(g, xy=(i, y_max + 0.015), ha='center', fontsize=8,
                    fontweight='bold', color=C['dark'],
                    bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylabel('Mean Comfort (Last 1,000 Episodes)')
    ax.set_title('Prosocial vs. Selfish Agent Comfort\nin Mixed-Type Communities',
                 fontweight='bold', fontsize=11)
    ax.set_ylim(0.87, 0.98)
    leg = ax.legend(loc='upper right'); style_legend(leg); style_data_axes(ax)
    fig.tight_layout(); save_fig(fig, f'{OUT}/v14_agent_comfort_split.png')
    plt.close(fig)

    # Fig 4-3: Gini Coefficient (from verified gini_reanalysis.csv / gini_more_scenarios.csv)
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(5)
    gini_labels = ['Mixed', 'All Selfish', 'Varied\nAltruism', 'All\nProsocial', 'Innovator\nEffect']
    gini_order = ['mixed', 'all_selfish', 'varied_altruism', 'all_prosocial', 'innovator_effect']
    gini_vals, gini_stds = [], []
    for s in gini_order:
        if s in ('mixed', 'innovator_effect'):
            df = pd.read_csv(f'{BASE}/gini_reanalysis.csv')
        else:
            df = pd.read_csv(f'{BASE}/gini_more_scenarios.csv')
        gs = df[df['scenario'] == s]['gini'].values
        gini_vals.append(np.mean(gs))
        gini_stds.append(np.std(gs))
    print(f'  v15 gini (CSV-derived): '
          f'{[round(v, 4) for v in gini_vals]} std {[round(v, 4) for v in gini_stds]}')
    ymin = max(0, min(gini_vals) - 0.02)
    ymax = max(gini_vals) + 0.02
    gini_bar_colors = [C['blue'], C['red'], C['yellow'], C['green'], C['purple']]
    bars = ax.bar(x, gini_vals, yerr=gini_stds, capsize=6, color=gini_bar_colors, alpha=0.85)
    style_bars(bars, highlight_indices=[4], linewidth=0.6)
    bars[-1].set_linewidth(2.5)
    pct = (gini_vals[-1] - gini_vals[0]) / gini_vals[0] * 100
    ax.annotate(f'+{pct:.0f}% vs Mixed\n(p=0.047)', xy=(4, gini_vals[-1] + gini_stds[-1] + 0.001),
                ha='center', fontsize=9, fontweight='bold', color=C['red'])
    ax.set_xticks(x); ax.set_xticklabels(gini_labels, fontsize=9)
    ax.set_ylabel('Gini Coefficient')
    ax.set_title('Gini Coefficient by Scenario', fontweight='bold', fontsize=11)
    ax.set_ylim(ymin, ymax); style_data_axes(ax)
    label_bars(ax, bars, gini_vals, fmt='{:.4f}', offset=0.0005, fontsize=8, errs=gini_stds)
    save_fig(fig, f'{OUT}/v15_gini_comparison.png')
    plt.close(fig)

    # Fig 4-4: Sharing Frequency
    fig, ax = plt.subplots(figsize=(10, 5))
    freq_labels = ['All Selfish', 'All Prosocial', 'Mixed\nProsocial',
                   'Mixed\nSelfish', 'Varied Altruism\nProsocial', 'Varied Altruism\nSelfish',
                   'Innovator\nExplorers', 'Innovator\nSelfish']
    qtab_dir = f'{BASE}/analysis_support/qtab'
    freq_groups = [
        ('all_selfish', range(10)),
        ('all_prosocial', range(10)),
        ('mixed', range(0, 5)),
        ('mixed', range(5, 10)),
        ('varied_altruism', range(0, 4)),
        ('varied_altruism', range(4, 10)),
        ('innovator_effect', range(0, 5)),
        ('innovator_effect', range(5, 10)),
    ]
    freq_vals, freq_stds = [], []
    for sc, idx in freq_groups:
        q = np.load(f'{qtab_dir}/{sc}_q.npy')
        best = np.argmax(q, axis=4)
        freqs = [np.sum(best[s, a] >= 1) / best[s, a].size
                 for s in range(q.shape[0]) for a in idx]
        freq_vals.append(np.mean(freqs) * 100)
        freq_stds.append(np.std(freqs) * 100)
    print(f'  v16 sharing freq (qtab-derived): '
          f'{[round(v, 2) for v in freq_vals]} std {[round(v, 2) for v in freq_stds]}')
    freq_colors = [C['red'], C['green'], C['green'], C['red'],
                   C['green'], C['red'], C['purple'], C['red']]
    x = np.arange(8)
    bars = ax.bar(x, freq_vals, yerr=freq_stds, capsize=6, color=freq_colors, alpha=0.85)
    style_bars(bars, linewidth=0.6)
    ax.axhline(y=13.1, color=C['grey'], linestyle='--', lw=1.5, alpha=0.8,
               label='Overall mean (~13.1%)', zorder=0)
    ax.set_xticks(x); ax.set_xticklabels(freq_labels, fontsize=8.5)
    ax.set_ylabel('Sharing Frequency (%)')
    ax.set_title("Proportion of Q-Table States Where\nGreedy Action is to Share",
                 fontweight='bold', fontsize=11)
    ax.set_ylim(8, 18)
    leg = ax.legend(loc='upper right'); style_legend(leg); style_data_axes(ax)
    label_bars(ax, bars, freq_vals, fmt='{:.2f}%', offset=0.35, fontsize=7.5, errs=freq_stds)
    fig.tight_layout(); save_fig(fig, f'{OUT}/v16_sharing_frequency.png')
    plt.close(fig)

    # Fig 4-7: Q-table heatmaps (v17 Persian + thesis English from saved .npy)
    def _render_qtable_heatmaps(save_path, persian=False):
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
        en_names = {
            'pure_selfish': 'pure_selfish', 'individualist': 'individualist',
            'prosocial': 'prosocial', 'altruistic': 'altruistic',
            'high_openness_innovator': 'high_openness_innovator',
        }
        fa_names = {
            'pure_selfish': 'خودخواه محض', 'individualist': 'فردگرا',
            'prosocial': 'نوع‌گرا', 'altruistic': 'نوع‌دوست',
            'high_openness_innovator': 'مبتکر',
        }
        en_labels = {
            'all_selfish': 'All Selfish', 'all_prosocial': 'All Prosocial',
            'mixed': 'Mixed', 'varied_altruism': 'Varied Altruism',
            'innovator_effect': 'Innovator Effect',
        }
        fa_labels = {
            'all_selfish': 'همگی خودخواه', 'all_prosocial': 'همگی نوع‌گرا',
            'mixed': 'مختلط', 'varied_altruism': 'نوع‌گرایی متنوع',
            'innovator_effect': 'اثر نوآور',
        }
        share_labels = ([fa('سهم ۰٪'), fa('سهم ۵۰٪'), fa('سهم ۱۰۰٪')] if persian
                        else ['Share 0%', 'Share 50%', 'Share 100%'])
        xlabel = fa('ساعت روز') if persian else 'Hour of Day'
        cbar_label = fa('میانگین مقدار Q') if persian else 'Mean Q-value'
        suptitle = (fa('نقشه‌های حرارتی مقادیر Q میانگین‌شده در هر ساعت برای عامل‌های نماینده')
                    if persian else
                    'Q-table Heatmaps: Average Action Values by Hour\n'
                    '(mean over battery levels; seed 42)')
        font_ctx = {'font.family': FA_FONTS} if persian else {'font.family': 'sans-serif'}

        with plt.rc_context(font_ctx):
            fig, axes = plt.subplots(2, 5, figsize=(24, 10))
            for i, sc in enumerate(h_scenarios):
                q = np.load(f'{BASE}/analysis_support/qtab/{sc}_q.npy')
                counterpart = 8 if sc == 'innovator_effect' else 3
                for row, house in enumerate([0, counterpart]):
                    q_avg = q[0, house].mean(axis=1)
                    ax = axes[row, i]
                    im = ax.imshow(q_avg.T, aspect='auto', cmap='YlOrRd', origin='lower',
                                   extent=[0, 23, 0, 2], interpolation='nearest')
                    ax.set_xticks([0, 6, 12, 18, 23])
                    ax.set_yticks([0, 1, 2])
                    ax.set_yticklabels(share_labels, fontsize=8)
                    ax.set_xlabel(xlabel, fontsize=9)
                    agent_t = (fa_names if persian else en_names)[h_mixes[sc][house]]
                    scen_l = (fa_labels if persian else en_labels)[sc]
                    if persian:
                        ax.set_title(fa(f'{scen_l} — عامل {house} ({agent_t})'),
                                     fontweight='bold', fontsize=10)
                    else:
                        ax.set_title(f'{scen_l}\nAgent {house} ({agent_t})',
                                     fontweight='bold', fontsize=10)
                    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
                    cbar.set_label(cbar_label, fontsize=8)
                    cbar.ax.tick_params(labelsize=7)
            fig.suptitle(suptitle, fontweight='bold', fontsize=14 if persian else 13)
            fig.tight_layout(rect=[0, 0, 1, 0.96])
            save_fig(fig, save_path)
            plt.close(fig)

    _render_qtable_heatmaps(f'{OUT}/v17_qtable_heatmaps.png', persian=True)
    _render_qtable_heatmaps(QTABLE_OUT, persian=False)

    # Fig 4-8: Scarcity Sensitivity (data from cloud_sensitivity_reanalysis.csv)
    fig, ax = plt.subplots(figsize=(8, 5))
    cs = pd.read_csv(f'{BASE}/cloud_sensitivity_reanalysis.csv')
    cp = sorted(cs['cloud_prob'].unique())
    pm = [cs[cs['cloud_prob'] == c]['prosocial_comfort'].mean() for c in cp]
    sm = [cs[cs['cloud_prob'] == c]['selfish_comfort'].mean() for c in cp]
    ps = [cs[cs['cloud_prob'] == c]['prosocial_comfort'].std(ddof=0) for c in cp]
    ss = [cs[cs['cloud_prob'] == c]['selfish_comfort'].std(ddof=0) for c in cp]
    ax.errorbar(cp, pm, yerr=ps, label='Prosocial Agents', color=C['blue'],
                lw=2.5, marker='o', markersize=8, capsize=6, markeredgecolor='white',
                markeredgewidth=0.8)
    ax.errorbar(cp, sm, yerr=ss, label='Selfish Agents', color=C['red'],
                lw=2.5, marker='s', markersize=8, capsize=6, markeredgecolor='white',
                markeredgewidth=0.8)
    gap = (pm[0] - sm[0]) * 100
    ax.annotate(f'Gap = {gap:.2f} pp\n(p=0.0011)', xy=(25, 0.90), fontsize=9, fontweight='bold',
                color=C['dark'], bbox=dict(facecolor='white', edgecolor=C['grey'], boxstyle='round'))
    ax.set_xlabel('Cloudy Day Probability (%)'); ax.set_ylabel('Mean Comfort (Last 1,000 Episodes)')
    ax.set_title('Prosocial vs. Selfish Comfort\nas a Function of Cloudy Day Probability',
                 fontweight='bold', fontsize=11)
    ax.set_xticks(cp); ax.set_xlim(10, 40); ax.set_ylim(0.75, 0.96)
    leg = ax.legend(loc='lower left'); style_legend(leg); style_data_axes(ax, grid_axis='both')
    ax.text(0.5, 0.02, 'Cloudy days halve solar generation (W=0.5)',
            transform=ax.transAxes, fontsize=8, fontstyle='italic',
            ha='center', color=C['grey'])
    fig.tight_layout(); save_fig(fig, f'{OUT}/v18_scarcity_sensitivity.png')
    plt.close(fig)

# Figure 2-1 (NEW): Conceptual Framework — Personality-Adjusted Coordination Model
# EN conversion 2026-08-16 — Persian originals (also in git HEAD 1731705):
#   'چارچوب مفهومی: مدل هماهنگی تعدیل‌شده با شخصیت' · 'سطح فردی: موقعیت در فضای شخصیت
#   OCEAN' · 'توافق‌پذیری ← وزن عدالت اجتماعی w_fair' · 'گشودگی ← کف اکتشاف ε_min' ·
#   'سه بُعد دیگر ثابت در میانگین جمعیتی' · 'تعیین پارامترهای عامل' ·
#   'سطح عامل: عامل یادگیری کیو مستقل' · 'فضای وضعیت: ساعت، سطح باتری' ·
#   'سه اقدام اشتراک گسسته' · 'پاداش = ترکیب محدب (آسایش شخصی، عدالت اجتماعی)' ·
#   'سیاست ε-حریصانه (ε_min از گشودگی)' · 'برهم‌کنش عامل‌ها' ·
#   'سطح جامعه: پیامدهای نوظهور' · 'توزیع آسایش سطح جامعه' · 'الگوهای اشتراک انرژی' ·
#   'تاب‌آوری: روز ابری / عامل نوآور' · 'بازخورد هماهنگی'
with plt.rc_context({'font.family': 'sans-serif'}):
    fig, ax = plt.subplots(figsize=(11, 8.5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8.8); ax.axis('off')
    ax.set_title('Conceptual Framework: Personality-Adjusted Coordination Model',
                 fontweight='bold', fontsize=13, pad=14)

    def panel(x, y, w, h, color, title, fs=10):
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle="round,pad=0.12",
                                    facecolor=color, edgecolor=color,
                                    lw=2, alpha=0.08))
        ax.add_patch(FancyBboxPatch((x, y + h - 0.55), w, 0.55,
                                    boxstyle="round,pad=0.12",
                                    facecolor=color, edgecolor=color,
                                    lw=2, alpha=0.25))
        ax.text(x + w / 2, y + h - 0.275, title, ha='center', va='center',
                fontsize=fs, fontweight='bold', color=color)
        return ax

    def sub_box(cx, cy, w, h, text, color, fs=8.5):
        ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                    boxstyle="round,pad=0.08",
                                    facecolor='white', edgecolor=color,
                                    lw=1.6, alpha=0.95))
        ax.text(cx, cy, text, ha='center', va='center', fontsize=fs,
                fontweight='bold', color=C['dark'])

    def v_arrow(x, y1, y2, color, lw=2.2):
        ax.annotate('', xy=(x, y2), xytext=(x, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=lw))

    # ── Level 1: Individual (OCEAN personality space) ──
    panel(0.6, 6.3, 10.8, 1.9, C['blue'],
          'Individual level: position in OCEAN personality space')
    sub_box(2.6, 6.95, 3.4, 0.95,
            'Agreeableness\n» social fairness weight w_fair', C['green'], fs=8.5)
    sub_box(6.0, 6.95, 3.4, 0.95,
            'Openness\n» exploration floor ε_min', C['purple'], fs=8.5)
    sub_box(9.6, 6.95, 3.0, 0.95,
            'Other three dimensions\nfixed at population mean', C['grey'], fs=8)

    v_arrow(6.0, 6.1, 5.45, C['blue'])
    ax.text(6.9, 5.78, 'Determines agent parameters', ha='center', va='center',
            fontsize=8, fontstyle='italic', color=C['blue'])

    # ── Level 2: Agent (Q-learning) ──
    panel(0.6, 3.7, 10.8, 1.9, C['purple'],
          'Agent level: independent Q-learning agent')
    sub_box(1.9, 4.35, 3.2, 0.95,
            'State space:\nhour, battery level', C['blue'], fs=8.5)
    sub_box(4.9, 4.35, 2.6, 0.95,
            'Three discrete\nsharing actions', C['dark'], fs=8.5)
    sub_box(7.9, 4.35, 4.0, 0.95,
            'Reward = convex combination\n(personal comfort, social fairness)',
            C['green'], fs=8)
    ax.text(6.0, 3.92, 'ε-greedy policy (ε_min from openness)',
            ha='center', va='center', fontsize=7.5, fontstyle='italic', color=C['purple'])

    v_arrow(6.0, 3.5, 2.85, C['purple'])
    ax.text(6.9, 3.18, 'Agent interactions', ha='center', va='center',
            fontsize=8, fontstyle='italic', color=C['purple'])

    # ── Level 3: Community (emergent outcomes) ──
    panel(0.6, 1.0, 10.8, 1.9, C['green'],
          'Community level: emergent outcomes')
    sub_box(2.6, 1.65, 3.4, 0.95,
            'Community-level\ncomfort distribution', C['blue'], fs=8.5)
    sub_box(6.0, 1.65, 3.4, 0.95,
            'Energy sharing\npatterns', C['purple'], fs=8.5)
    sub_box(9.6, 1.65, 3.0, 0.95,
            'Resilience:\ncloudy day / innovator agent', C['orange'], fs=8)

    # Feedback: dashed arrow from community level back up to individual level
    ax.annotate('', xy=(11.2, 6.35), xytext=(11.2, 2.9),
                arrowprops=dict(arrowstyle='->', color=C['grey'], lw=1.8,
                                linestyle='dashed'))
    ax.text(10.85, 4.6, 'Coordination\nfeedback', ha='center', va='center',
            fontsize=7.5, fontstyle='italic', color=C['grey'],
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))

    save_fig(fig, f'{OUT}/v2_1_conceptual_framework.png')
    plt.close(fig)

print(f'All visuals saved to {OUT}/ and {QTABLE_OUT}')