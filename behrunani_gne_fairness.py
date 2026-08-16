import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, json, csv, argparse, time

from offgrid_marl import DEMAND_PROFILES

ALG_NAME = 'baseline_behrunani'

# ========== ENVIRONMENT CONSTANTS (identical to main runs) ==========
NUM_HOUSES = 10
BATTERY_CAP = 7.0
SOLAR_MAX = 1.3
WEATHER_CLOUD_PROB = 0.15

# ========== GAME SETTINGS (per spec, with adaptation documented) ==========
# Adaptation (mistranslation correction, NOT a method finding): Behrunani's
# original "cost reduction" is a monetary quantity (CHF/kWh, revenue from
# selling surplus). Absent a price mechanism in our environment, we use its
# direct energy-unit analog as the benefit term: L_i = unmet_energy + wasted
# energy (kWh). Each house minimizes own energy loss plus a community penalty
# limiting variance in cost reduction across houses.
LAMBDA = 1.0        # fairness penalty weight (free parameter, reported)
ETA = 0.1           # projected gradient step
MAX_ITER = 50       # best-response iterations per hour
TOL = 1e-3          # convergence: max |Delta s| < TOL
GRAD_EPS = 1e-4     # central finite-difference step
S_INIT = 0.5        # initial share for surplus houses (default, reported)
# Jacobi update (per spec: each s_i updated holding s_{-i} at the previous
# iteration's values); rounding to {0, 0.5, 1.0} only at execution.


# ========== PRECOMPUTED DAY TABLES ==========
demand_keys = list(DEMAND_PROFILES.keys())
DEMAND_TABLE = np.array([DEMAND_PROFILES[demand_keys[i % 4]] for i in range(NUM_HOUSES)]).T  # (24,10)
HOURS = np.arange(24)
SOLAR_CLEAR = np.where((HOURS >= 6) & (HOURS <= 18),
                       SOLAR_MAX * np.sin(np.pi * (HOURS - 6) / 12.0), 0.0)  # (24,)


def hour_net(hour, weather_factor):
    return SOLAR_CLEAR[hour] * weather_factor - DEMAND_TABLE[hour]


# ========== ONE-HOUR OUTCOME (mirrors step_energy + receive_help) ==========
def hour_outcome(net, battery, s, hour):
    """Returns comfort(10), next battery(10), unmet_energy(10), wasted_energy(10).
    s in [0,1]; only surplus houses' entries are used (deficit houses always 0)."""
    dmd = DEMAND_TABLE[hour]
    comfort = np.ones(NUM_HOUSES)
    to_share = np.zeros(NUM_HOUSES)
    unmet_e = np.zeros(NUM_HOUSES)
    waste = np.zeros(NUM_HOUSES)
    for i in range(NUM_HOUSES):
        if net[i] > 0:
            share = net[i] * s[i]
            keep = net[i] - share
            charge = min(keep, BATTERY_CAP - battery[i])
            battery[i] += charge
            to_share[i] = share
            waste[i] = keep - charge
        else:
            deficit = -net[i]
            draw = min(deficit, battery[i])
            battery[i] -= draw
            unmet = deficit - draw
            unmet_e[i] = unmet
            comfort[i] = max(0.0, (dmd[i] - unmet) / dmd[i]) if dmd[i] > 0 else 1.0
    for i in range(NUM_HOUSES):
        amt = to_share[i]
        if amt <= 0:
            continue
        r = (i + 1) % NUM_HOUSES
        um = (1.0 - comfort[r]) * dmd[r] if comfort[r] < 1.0 else 0.0
        if um > 0 and amt > 0:
            red = min(um, amt)
            comfort[r] = (comfort[r] * dmd[r] + red) / dmd[r]
            amt -= red
            unmet_e[r] = max(0.0, unmet_e[r] - red)
        battery[r] += min(amt, BATTERY_CAP - battery[r])
    return comfort, battery, unmet_e, waste


# ========== PER-HOUR GAME ==========
def loss_value(s_val, i, s_base, L0, net, battery, hour, lam):
    """J_i with house i's share set to s_val, others at s_base (Jacobi step)."""
    sv = s_base.copy()
    sv[i] = s_val
    _, _, u, w = hour_outcome(net.copy(), battery.copy(), sv, hour)
    L = u + w
    dL = L0 - L
    if lam == 0:
        return L[i]
    return L[i] + lam * (dL[i] - dL.mean()) ** 2


def solve_hour(net, battery, hour, lam=LAMBDA):
    """Solve the per-hour best-response game. Returns the continuous s vector,
    plus diagnostics: iterations used, converged flag, and whether the game had
    any teeth (nonzero donor gradient at the initial point)."""
    donors = np.where(net > 0)[0]
    s = np.zeros(NUM_HOUSES)
    s[donors] = S_INIT
    if len(donors) == 0:
        return s, 0, True, False

    _, _, u0, w0 = hour_outcome(net.copy(), battery.copy(), np.zeros(NUM_HOUSES), hour)
    L0 = u0 + w0

    teeth = False
    for i in donors:
        g = (loss_value(s[i] + GRAD_EPS, i, s, L0, net, battery, hour, lam)
             - loss_value(s[i] - GRAD_EPS, i, s, L0, net, battery, hour, lam)) / (2 * GRAD_EPS)
        if abs(g) > 1e-6:
            teeth = True
            break

    iters = 0
    converged = False
    for it in range(MAX_ITER):
        grad = np.zeros(NUM_HOUSES)
        for i in donors:
            grad[i] = (loss_value(s[i] + GRAD_EPS, i, s, L0, net, battery, hour, lam)
                       - loss_value(s[i] - GRAD_EPS, i, s, L0, net, battery, hour, lam)) / (2 * GRAD_EPS)
        s_new = np.clip(s - ETA * grad, 0.0, 1.0)
        delta = np.max(np.abs(s_new - s))
        s = s_new
        iters += 1
        if delta < TOL:
            converged = True
            break
    return s, iters, converged, teeth


# ========== RUN ONE SEED ==========
def run_behrunani_seed(seed, days=500, lam=LAMBDA, verbose=True):
    np.random.seed(seed)
    weather_seq = [1.0 if np.random.random() > WEATHER_CLOUD_PROB else 0.5
                   for _ in range(days)]

    day_comfort = np.zeros(days)
    day_fairness = np.zeros(days)
    day_blackout = np.zeros(days)
    day_waste = np.zeros(days)
    day_share = np.zeros(days)        # mean share fraction over donor-hours
    day_iters = np.zeros(days)        # mean iterations over donor-hours
    day_teeth = np.zeros(days)        # fraction of donor-hours with nonzero gradient
    day_dlvar = np.zeros(days)        # variance of cost reduction (fairness check)
    day_n_donor_hours = np.zeros(days)

    if verbose:
        print(f"\nSeed {seed}: {days} days, per-hour best-response game "
              f"(lambda={lam}, eta={ETA}, max_iter={MAX_ITER}, s0={S_INIT})...")

    t0 = time.perf_counter()
    for d in range(days):
        wf = weather_seq[d]
        battery = np.full(NUM_HOUSES, BATTERY_CAP * 0.5)
        end_comfort = None
        total_waste = 0.0
        donor_hours = 0
        iters_sum = 0.0
        teeth_sum = 0.0
        share_sum = 0.0
        dlvar_sum = 0.0

        for hour in range(24):
            net = hour_net(hour, wf)
            s, iters, converged, teeth = solve_hour(net, battery, hour, lam)

            # fairness metric for this hour: variance of cost reduction
            _, _, u0, w0 = hour_outcome(net.copy(), battery.copy(),
                                        np.zeros(NUM_HOUSES), hour)
            L0 = u0 + w0
            s_r = np.round(s * 2) / 2.0
            _, _, u, w = hour_outcome(net.copy(), battery.copy(), s_r, hour)
            dL = L0 - (u + w)
            dlvar_sum += dL.var()

            n_donors = int(np.sum(net > 0))
            if n_donors > 0:
                donor_hours += 1
                iters_sum += iters
                teeth_sum += 1.0 if teeth else 0.0
                share_sum += s[net > 0].mean()

            # execute the (discretized) actions -> advance battery
            comfort, battery, _, waste = hour_outcome(net.copy(), battery.copy(), s_r, hour)
            end_comfort = comfort
            total_waste += waste.sum()

        day_comfort[d] = end_comfort.mean()
        day_fairness[d] = (end_comfort.sum() ** 2) / (NUM_HOUSES * np.sum(end_comfort ** 2))
        day_blackout[d] = 1.0 if np.any(end_comfort < 0.95) else 0.0
        day_waste[d] = total_waste
        day_share[d] = share_sum / donor_hours if donor_hours else 0.0
        day_iters[d] = iters_sum / donor_hours if donor_hours else 0.0
        day_teeth[d] = teeth_sum / donor_hours if donor_hours else 0.0
        day_dlvar[d] = dlvar_sum / 24.0
        day_n_donor_hours[d] = donor_hours

        if verbose and (d + 1) % 50 == 0:
            print(f"  day {d+1}/{days}: comfort={day_comfort[d]:.3f}, "
                  f"fairness={day_fairness[d]:.3f}, waste={day_waste[d]:.2f}, "
                  f"share={day_share[d]:.2f}, iters={day_iters[d]:.1f}, "
                  f"teeth={day_teeth[d]*100:.0f}%, ({time.perf_counter() - t0:.1f}s)")

    elapsed = time.perf_counter() - t0
    return {
        'seed': seed, 'days': days, 'lam': lam, 'weather_seq': weather_seq,
        'comfort': day_comfort, 'fairness': day_fairness, 'blackout': day_blackout,
        'waste': day_waste, 'share': day_share, 'iters': day_iters,
        'teeth': day_teeth, 'dlvar': day_dlvar, 'n_donor_hours': day_n_donor_hours,
        'elapsed': elapsed, 'per_day_sec': elapsed / days,
    }


# ========== PLOTTING ==========
def plot_seed(history, title, save_path):
    from thesis_plot_style import C, save_fig, style_data_axes, style_legend

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))

    ax = axes[0]
    ax.plot(history['comfort'], label='Mean Comfort', color=C['blue'], lw=2, alpha=0.9)
    ax.plot(history['fairness'], label="Jain's Fairness", color=C['green'], lw=2, alpha=0.9)
    ax.set_xlabel('Day'); ax.set_ylabel('Score'); ax.set_ylim(0, 1.05)
    ax.set_title('Community Performance', fontweight='bold', fontsize=10)
    leg = ax.legend(loc='lower right'); style_legend(leg); style_data_axes(ax)

    ax = axes[1]
    ax.plot(history['waste'], color=C['blue'], lw=2, alpha=0.85, label='Waste (kWh)')
    ax.plot(history['share'], color=C['green'], lw=2, alpha=0.85, label='Mean share frac')
    ax.set_xlabel('Day')
    ax.set_title('Daily Waste & Chosen Sharing', fontweight='bold', fontsize=10)
    leg = ax.legend(loc='upper right'); style_legend(leg); style_data_axes(ax)

    ax = axes[2]
    ax.plot(history['iters'], color=C['red'], lw=2, alpha=0.85, label='Mean iterations')
    ax.plot(history['teeth'], color=C['purple'], lw=2, alpha=0.85, label='Donor-hours w/ signal')
    ax.set_xlabel('Day')
    ax.set_title('Game Convergence & Signal', fontweight='bold', fontsize=10)
    leg = ax.legend(loc='upper right'); style_legend(leg); style_data_axes(ax)

    fig.suptitle(title, fontsize=13, fontweight='bold')
    fig.tight_layout()
    save_fig(fig, save_path)
    plt.close(fig)


# ========== SAVE RESULTS (same schema as main runs + scenario label) ==========
def save_results(save_path, history, scenario=ALG_NAME):
    os.makedirs(save_path, exist_ok=True)
    comfort = float(np.mean(history['comfort']))
    fairness = float(np.mean(history['fairness']))
    blackout_rate = float(np.mean(history['blackout']))
    waste = float(np.mean(history['waste']))
    f_end = comfort + fairness

    metrics = {
        'scenario': scenario,
        'seed': history['seed'],
        'comfort': comfort,
        'fairness': fairness,
        'F': f_end,
        'blackout_rate': blackout_rate,
        'waste': waste,
        'prosocial_comfort': comfort,
        'selfish_comfort': comfort,
    }
    with open(os.path.join(save_path, 'final_metrics.csv'), 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(metrics.keys()))
        writer.writeheader()
        writer.writerow(metrics)

    config = {
        'algorithm': ALG_NAME,
        'method': ('per-hour decentralized best-response game solved fresh each hour '
                   '(no learning across days); projected gradient, Jacobi update '
                   '(s_-i held at previous iteration values)'),
        'adaptation': ('Behrunani et al. 2023 original "cost reduction" is a monetary '
                       'quantity (revenue from selling surplus in a Stackelberg price '
                       'game). Absent a price mechanism in our environment, we '
                       'implement the inner-level equilibrium-seeking mechanism only '
                       'with the direct energy-unit analog as benefit term: '
                       'L_i = unmet_energy + wasted_energy (kWh). Each house minimizes '
                       'J_i = L_i(s) + lambda*(DeltaL_i - mean(DeltaL))^2, '
                       'DeltaL_i = L_i(0) - L_i(s). This is a mistranslation '
                       'correction (comfort was never the right quantity for donors); '
                       'NOT a modification of Behrunani\'s method.'),
        'objective': 'J_i = L_i + lambda*(DeltaL_i - mean(DeltaL))^2, L_i in kWh',
        'lambda': history['lam'],
        'eta': ETA,
        'max_iterations': MAX_ITER,
        'tol': TOL,
        'gradient': f'central finite difference (eps={GRAD_EPS})',
        'initial_s': S_INIT,
        'discretization': 'continuous s in [0,1] solved in-game; rounded to '
                          '{0.0, 0.5, 1.0} only at execution',
        'topology': 'ring; donor i shares to recipient (i+1)%10',
        'num_houses': NUM_HOUSES,
        'days': history['days'],
        'battery_cap': BATTERY_CAP,
        'solar_max': SOLAR_MAX,
        'weather_cloud_prob': WEATHER_CLOUD_PROB,
        'seed': history['seed'],
        'env': 'identical to main OCEAN-MARL runs',
    }
    with open(os.path.join(save_path, 'config.json'), 'w') as f:
        json.dump(config, f, indent=2)

    plot_seed(history, f"Baseline Behrunani GNE (lambda={history['lam']}, "
                       f"seed {history['seed']})",
              os.path.join(save_path, 'results_plot.png'))


# ========== SANITY CHECK (10 days, gate before full run) ==========
def run_sanity_check(base_dir='results', days=10, seed=42):
    print(f"Behrunani GNE sanity check: {days} days, seed {seed}\n")
    h1 = run_behrunani_seed(seed, days=days, lam=1.0, verbose=True)
    h0 = run_behrunani_seed(seed, days=days, lam=0.0, verbose=False)

    lines = []
    lines.append("=" * 72)
    lines.append("BEHRUNANI GNE (energy-cost adaptation) — TIMING & SANITY CHECK")
    lines.append("=" * 72)

    lines.append(f"\n(a) Convergence (lambda=1.0):")
    lines.append(f"  mean iterations per donor-hour: {h1['iters'].mean():.2f} "
                 f"(max {h1['iters'].max():.0f}, cap {MAX_ITER})")
    teeth_frac = np.average(h1['teeth'], weights=np.maximum(h1['n_donor_hours'], 1))
    lines.append(f"  donor-hours where the game has nonzero gradient at s0: "
                 f"{teeth_frac*100:.1f}% (signal exists)")

    lines.append(f"\n(b) Fairness penalty teeth (lambda=1.0 vs lambda=0.0):")
    for lbl, h in [('lambda=0', h0), ('lambda=1', h1)]:
        lines.append(f"  {lbl}: mean dL var/day={h['dlvar'].mean():.4f} kWh^2, "
                     f"share={h['share'].mean():.2f}, comfort={h['comfort'].mean():.3f}, "
                     f"waste={h['waste'].mean():.2f} kWh, blackout={h['blackout'].mean()*100:.1f}%")
    lines.append(f"  -> fairness term changes chosen sharing: "
                 f"{(h1['share'].mean()-h0['share'].mean()):+.3f}")

    lines.append(f"\n(c) Runtime:")
    lines.append(f"  {h1['elapsed']:.1f}s for {days} days ({h1['per_day_sec']:.3f}s/day)")
    lines.append(f"  extrapolated: {h1['per_day_sec']*500:.0f}s/seed, "
                 f"x5 seeds = {h1['per_day_sec']*2500/60:.1f} min")

    lines.append(f"\nChosen-policy summary (lambda=1.0, {days} days):")
    lines.append(f"  mean comfort: {h1['comfort'].mean():.3f}  fairness: {h1['fairness'].mean():.3f}")
    lines.append(f"  blackout rate: {h1['blackout'].mean()*100:.1f}%  waste: {h1['waste'].mean():.2f} kWh")

    print("\n".join(lines))

    save_dir = os.path.join(base_dir, 'baseline_behrunani_sanity')
    os.makedirs(save_dir, exist_ok=True)
    save_results(save_dir, h1)
    with open(os.path.join(save_dir, 'sanity_report.txt'), 'w') as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nSanity artifacts saved to {save_dir}")


# ========== MAIN ==========
def main():
    ap = argparse.ArgumentParser(description="Behrunani GNE fairness baseline "
                                             "(per-hour best-response game)")
    ap.add_argument('--sanity', action='store_true',
                    help='run short sanity check (default 10 days) and exit')
    ap.add_argument('--days', type=int, default=None,
                    help='days per seed (sanity default 10, full default 500)')
    ap.add_argument('--seeds', type=int, nargs='*', default=None,
                    help='seeds (full run default: 42 123 456 789 1011)')
    ap.add_argument('--lambda', dest='lam', type=float, default=LAMBDA)
    ap.add_argument('--scenario', default=None,
                    help='scenario label for final_metrics.csv (default '
                         'baseline_behrunani)')
    ap.add_argument('--base_dir', default='results')
    args = ap.parse_args()

    if args.sanity:
        run_sanity_check(base_dir=args.base_dir,
                         days=args.days if args.days else 10, seed=42)
        return

    seeds = args.seeds if args.seeds else [42, 123, 456, 789, 1011]
    days = args.days if args.days else 500
    scenario = args.scenario if args.scenario else ALG_NAME
    for seed in seeds:
        path = os.path.join(args.base_dir, scenario, f'seed_{seed}')
        print(f"\n=== Running {scenario} seed {seed} ({days} days, "
              f"lambda={args.lam}) ===")
        history = run_behrunani_seed(seed, days=days, lam=args.lam, verbose=True)
        save_results(path, history, scenario=scenario)
        print(f"Saved to {path}")
    print("\nFull Behrunani baseline run complete.")


if __name__ == "__main__":
    main()
