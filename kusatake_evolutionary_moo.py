import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, json, csv, argparse, time

from offgrid_marl import DEMAND_PROFILES

from pymoo.core.problem import Problem
from pymoo.core.mutation import Mutation
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.ux import UX
from pymoo.optimize import minimize
from pymoo.termination import get_termination

ALG_NAME = 'baseline_kusatake'

# ========== ENVIRONMENT CONSTANTS (identical to main runs) ==========
NUM_HOUSES = 10
BATTERY_CAP = 7.0
SOLAR_MAX = 1.3
WEATHER_CLOUD_PROB = 0.15
FRACS = np.array([0.0, 0.5, 1.0])

# ========== NSGA-II SETTINGS (per spec) ==========
POP_SIZE = 60
N_GENERATIONS = 40
# Decision vector x in {0,1,2}^(24h x 10 houses), flattened house-major.
N_VAR = 24 * NUM_HOUSES

# Objective selection rule: pick the Pareto-front solution maximizing F1 - F2,
# where F1 = mean comfort (max) and F2 = std of comfort (min).
SELECTION_RULE = 'argmax(F1 - F2)'


# ========== PRECOMPUTED DAY TABLES ==========
demand_keys = list(DEMAND_PROFILES.keys())
DEMAND_TABLE = np.array([DEMAND_PROFILES[demand_keys[i % 4]] for i in range(NUM_HOUSES)]).T  # (24,10)
HOURS = np.arange(24)
SOLAR_CLEAR = np.where((HOURS >= 6) & (HOURS <= 18),
                       SOLAR_MAX * np.sin(np.pi * (HOURS - 6) / 12.0), 0.0)  # (24,)


def day_net_table(weather_factor):
    """(24,10) signed net production = solar - demand, one day at given weather."""
    return np.outer(SOLAR_CLEAR, np.ones(NUM_HOUSES)) * weather_factor - DEMAND_TABLE


# ========== FAST VECTORIZED DAY EVALUATOR ==========
# Mirrors Community.step / House.step_energy / receive_help exactly:
#   donor keeps (1-frac)*surplus (charges battery, overflow -> waste),
#   recipient receives donor's to_share (fills unmet demand first, then battery),
#   battery starts each day at 50% and carries through the 24 hours.
# X: (P, 240) integer action vectors. Returns comforts (P,10), waste (P,).
def evaluate_day_vec(X, net_table):
    X = np.asarray(X, dtype=int)
    P = X.shape[0]
    pos_net = np.maximum(net_table, 0.0)
    frac = np.take(FRACS, X).reshape(P, 24, NUM_HOUSES)
    to_share = pos_net[None, :, :] * frac
    received = np.roll(to_share, 1, axis=2)  # house i receives from donor (i-1)%N

    battery = np.full((P, NUM_HOUSES), BATTERY_CAP * 0.5)
    comfort = np.ones((P, NUM_HOUSES))
    wasted = np.zeros(P)

    for h in range(24):
        nh = net_table[h]
        dmd = DEMAND_TABLE[h]
        keep = pos_net[h] - to_share[:, h]
        charge = np.minimum(keep, BATTERY_CAP - battery)
        battery += charge
        wasted += keep.sum(axis=1) - charge.sum(axis=1)

        deficit = np.maximum(-nh, 0.0)[None, :]
        draw = np.minimum(deficit, battery)
        battery -= draw
        unmet = deficit - draw
        safe = np.where(dmd > 0, dmd, 1.0)[None, :]
        comfort_new = np.where(dmd > 0, np.maximum(0.0, (dmd[None, :] - unmet) / safe), 1.0)
        comfort = np.where(nh > 0, 1.0, comfort_new)

        r = received[:, h]
        unmet_e = np.where(comfort < 1.0, (1.0 - comfort) * dmd[None, :], 0.0)
        red = np.minimum(unmet_e, r)
        comfort = np.where(comfort < 1.0, (comfort * dmd[None, :] + red) / safe, comfort)
        battery += np.minimum(r - red, BATTERY_CAP - battery)

    return comfort, wasted


# ========== PYMOO PROBLEM (one instance per day) ==========
class DayProblem(Problem):
    def __init__(self, net_table):
        super().__init__(n_var=N_VAR, n_obj=2, xl=0, xu=2, vtype=int)
        self.net_table = net_table

    def _evaluate(self, X, out, *args, **kwargs):
        comfort, _ = evaluate_day_vec(X, self.net_table)
        out["F"] = np.column_stack([-comfort.mean(axis=1), comfort.std(axis=1)])


# ========== INTEGER UNIFORM MUTATION ==========
class IntUniformMutation(Mutation):
    """Re-samples each gene to a uniform value in {0,1,2} with probability prob."""

    def __init__(self, prob=1.0 / N_VAR):
        super().__init__()
        self.prob = prob

    def _do(self, problem, X, **kwargs):
        X = np.array(X, dtype=float)
        mask = np.random.random(X.shape) < self.prob
        X[mask] = np.random.randint(0, 3, size=X.shape)[mask]
        return X


# ========== SOLVE ONE DAY WITH NSGA-II ==========
def solve_day(net_table, day_seed, pop_size=POP_SIZE, n_gen=N_GENERATIONS):
    problem = DayProblem(net_table)
    algorithm = NSGA2(pop_size=pop_size,
                      sampling=IntegerRandomSampling(),
                      crossover=UX(prob=0.5),
                      mutation=IntUniformMutation())
    res = minimize(problem, algorithm,
                   get_termination('n_gen', n_gen),
                   seed=day_seed, verbose=False, save_history=False)

    F = res.F  # (n_front, 2) with F1 = -mean_comfort
    score = -F[:, 0] - F[:, 1]  # F1 - F2
    idx = int(np.argmax(score))
    best_x = np.asarray(res.X[idx], dtype=int).reshape(24, NUM_HOUSES)
    return {
        'best_x': best_x,
        'best_objs': F[idx],
        'front_size': len(F),
        'front_score_max': float(score.max()),
    }


# ========== RUN ONE SEED (500 days, no learning across days) ==========
def run_kusatake_seed(seed, days=500, verbose=True):
    np.random.seed(seed)
    weather_seq = [1.0 if np.random.random() > WEATHER_CLOUD_PROB else 0.5
                   for _ in range(days)]

    comfort_mean = np.zeros(days)
    fairness = np.zeros(days)
    blackout = np.zeros(days)
    waste = np.zeros(days)
    share_frac = np.zeros(days)
    front_sizes = np.zeros(days, dtype=int)
    chosen_score = np.zeros(days)

    if verbose:
        print(f"\nSeed {seed}: solving {days} days independently with NSGA-II "
              f"(pop={POP_SIZE}, gen={N_GENERATIONS})...")

    t0 = time.perf_counter()
    for d in range(days):
        net_table = day_net_table(weather_seq[d])
        day_seed = seed * 100000 + d
        res = solve_day(net_table, day_seed)

        comfort, waste_day = evaluate_day_vec(res['best_x'].ravel()[None, :], net_table)
        comforts = comfort[0]
        comfort_mean[d] = comforts.mean()
        fairness[d] = (comforts.sum() ** 2) / (NUM_HOUSES * np.sum(comforts ** 2))
        blackout[d] = 1.0 if np.any(comforts < 0.95) else 0.0
        waste[d] = waste_day[0]
        share_frac[d] = res['best_x'].mean() / 2.0
        front_sizes[d] = res['front_size']
        chosen_score[d] = res['front_score_max']

        if verbose and (d + 1) % 50 == 0:
            print(f"  day {d+1}/{days}: comfort={comfort_mean[d]:.3f}, "
                  f"fairness={fairness[d]:.3f}, share_frac={share_frac[d]:.2f}, "
                  f"front={front_sizes[d]}, "
                  f"({time.perf_counter() - t0:.1f}s elapsed)")
    elapsed = time.perf_counter() - t0

    return {
        'seed': seed,
        'days': days,
        'weather_seq': weather_seq,
        'comfort_mean': comfort_mean,
        'fairness': fairness,
        'blackout': blackout,
        'waste': waste,
        'share_frac': share_frac,
        'front_sizes': front_sizes,
        'chosen_score': chosen_score,
        'elapsed': elapsed,
        'per_day_sec': elapsed / days,
    }


# ========== PLOTTING ==========
def plot_seed(history, title, save_path):
    days = history['days']
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    ax = axes[0]
    ax.plot(history['comfort_mean'], label='Mean Comfort', alpha=0.8)
    ax.plot(history['fairness'], label="Jain's Fairness", alpha=0.8)
    ax.set_xlabel('Day'); ax.set_ylabel('Score'); ax.set_ylim([0, 1.05])
    ax.set_title('Community Performance'); ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1]
    ax.plot(history['waste'], color='tab:blue', alpha=0.7, label='Waste (kWh)')
    ax.plot(np.convolve(history['blackout'], np.ones(50) / 50, mode='valid'), color='red',
            label='Blackout rate (50-day avg)')
    ax.set_xlabel('Day'); ax.set_ylabel('kWh / rate')
    ax.set_title('Daily Waste & Blackout'); ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[2]
    ax.plot(history['share_frac'], color='tab:green', alpha=0.7, label='Chosen share frac')
    ax.plot(history['front_sizes'], color='tab:purple', alpha=0.7, label='Pareto front size')
    ax.set_xlabel('Day')
    ax.set_title('Chosen Sharing & Front Size'); ax.legend(fontsize=8); ax.grid(alpha=0.3)

    fig.suptitle(title, fontsize=13, fontweight='bold')
    fig.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(fig)


# ========== SAVE RESULTS (same schema as main runs + scenario label) ==========
def save_results(save_path, history):
    os.makedirs(save_path, exist_ok=True)
    comfort = float(np.mean(history['comfort_mean']))
    fairness = float(np.mean(history['fairness']))
    blackout_rate = float(np.mean(history['blackout']))
    waste = float(np.mean(history['waste']))
    f_end = comfort + fairness

    metrics = {
        'scenario': ALG_NAME,
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

    # Companion weather-stratified summary (sunny vs cloudy). The pooled
    # final_metrics.csv is kept for drop-in ANOVA compatibility; this table
    # carries the honest story: on sunny days the comfort objectives saturate
    # so NSGA-II has no signal, whereas on cloudy days it genuinely optimizes.
    wseq = np.array(history['weather_seq'])
    sunny = wseq >= 1.0
    cloudy = ~sunny
    rows = []
    for label, mask in [('sunny', sunny), ('cloudy', cloudy)]:
        if mask.sum() == 0:
            continue
        cm = float(np.mean(history['comfort_mean'][mask]))
        fa = float(np.mean(history['fairness'][mask]))
        bl = float(np.mean(history['blackout'][mask]))
        wa = float(np.mean(history['waste'][mask]))
        rows.append({'weather': label, 'days': int(mask.sum()),
                     'comfort': cm, 'fairness': fa, 'F': cm + fa,
                     'blackout_rate': bl, 'waste': wa,
                     'share_frac': float(np.mean(history['share_frac'][mask]))})
    with open(os.path.join(save_path, 'weather_split_metrics.csv'), 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    config = {
        'algorithm': ALG_NAME,
        'method': ('each day solved independently by NSGA-II (no learning across days); '
                   'decision vector x in {0,1,2}^(24h x 10 houses) -> share fraction '
                   '[0%, 50%, 100%]'),
        'objectives': 'F1 = mean comfort (max), F2 = std of comfort (min)',
        'selection': SELECTION_RULE,
        'caveat': ('on sunny days (wf=1.0, ~85%) comfort objectives saturate '
                   '(comfort=1.0, std=0.0 for every action vector) -> NSGA-II has no '
                   'selective pressure and argmax(F1-F2) returns an arbitrary but '
                   'reproducible policy; on cloudy days (wf=0.5) NSGA-II genuinely '
                   'optimizes. See weather_split_metrics.csv.'),
        'pymoo_algorithm': 'NSGA2',
        'pop_size': POP_SIZE,
        'generations': N_GENERATIONS,
        'crossover': 'uniform (prob 0.5)',
        'mutation': f'integer uniform re-sample (prob 1/{N_VAR})',
        'num_houses': NUM_HOUSES,
        'days': history['days'],
        'battery_cap': BATTERY_CAP,
        'solar_max': SOLAR_MAX,
        'weather_cloud_prob': WEATHER_CLOUD_PROB,
        'seed': history['seed'],
        'env': 'identical to main OCEAN-MARL runs (demand profiles, ring topology, '
               'battery start 50%, weather generator)',
    }
    with open(os.path.join(save_path, 'config.json'), 'w') as f:
        json.dump(config, f, indent=2)

    plot_seed(history, f"Baseline Kusatake NSGA-II (seed {history['seed']})",
              os.path.join(save_path, 'results_plot.png'))


# ========== TIMING + SANITY CHECK (gate before full run) ==========
def run_timing_check(base_dir='results', days=10, seed=42):
    print(f"Kusatake NSGA-II timing/sanity check: {days} days, seed {seed} "
          f"(pop={POP_SIZE}, gen={N_GENERATIONS})\n")
    history = run_kusatake_seed(seed, days=days, verbose=True)

    front = history['front_sizes']
    lines = []
    lines.append("=" * 72)
    lines.append("KUSATAKE NSGA-II — TIMING & SANITY CHECK")
    lines.append("=" * 72)
    lines.append(f"\nRuntime:")
    lines.append(f"  {history['elapsed']:.1f}s for {days} days  "
                 f"({history['per_day_sec']:.3f}s/day)")
    lines.append(f"  extrapolated: {history['per_day_sec']*500:.0f}s/seed, "
                 f"x5 seeds = {history['per_day_sec']*2500/60:.1f} min")

    lines.append(f"\nPareto front (per day):")
    lines.append(f"  front size: min={front.min()}, max={front.max()}, "
                 f"mean={front.mean():.1f}, nontrivial(front>1) days="
                 f"{(front>1).sum()}/{days}")

    lines.append(f"\nChosen solution (argmax F1-F2), averaged over {days} days:")
    lines.append(f"  mean comfort:   {history['comfort_mean'].mean():.3f}")
    lines.append(f"  Jain's fairness:{history['fairness'].mean():.3f}")
    lines.append(f"  blackout rate:  {history['blackout'].mean()*100:.1f}%")
    lines.append(f"  avg waste:      {history['waste'].mean():.2f} kWh")
    lines.append(f"  chosen share fraction: {history['share_frac'].mean():.2f} "
                 f"(0=never share, 1=always 100%)")

    lines.append(f"\nAlways-default reference (x = all 0%, same days):")
    wf = history['weather_seq']
    cs, ws, bs = [], [], []
    for w in wf:
        net = day_net_table(w)
        c, wst = evaluate_day_vec(np.zeros((1, N_VAR), dtype=int), net)
        cs.append(c[0].mean()); ws.append(wst[0]); bs.append(np.any(c[0] < 0.95))
    lines.append(f"  mean comfort: {np.mean(cs):.3f}  blackout: {np.mean(bs)*100:.1f}%  "
                 f"waste: {np.mean(ws):.2f} kWh")

    print("\n".join(lines))

    save_dir = os.path.join(base_dir, 'baseline_kusatake_timing')
    os.makedirs(save_dir, exist_ok=True)
    save_results(save_dir, history)
    with open(os.path.join(save_dir, 'timing_report.txt'), 'w') as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nTiming artifacts saved to {save_dir}")


# ========== MAIN ==========
def main():
    ap = argparse.ArgumentParser(description="Kusatake evolutionary MOO baseline "
                                             "(NSGA-II per day)")
    ap.add_argument('--timing', action='store_true',
                    help='run short timing + sanity check (default 10 days) and exit')
    ap.add_argument('--days', type=int, default=None,
                    help='days per seed (timing default 10, full default 500)')
    ap.add_argument('--seeds', type=int, nargs='*', default=None,
                    help='seeds (full run default: 42 123 456 789 1011)')
    ap.add_argument('--base_dir', default='results')
    args = ap.parse_args()

    if args.timing:
        run_timing_check(base_dir=args.base_dir,
                         days=args.days if args.days else 10, seed=42)
        return

    seeds = args.seeds if args.seeds else [42, 123, 456, 789, 1011]
    days = args.days if args.days else 500
    for seed in seeds:
        path = os.path.join(args.base_dir, 'baseline_kusatake', f'seed_{seed}')
        print(f"\n=== Running {ALG_NAME} seed {seed} ({days} days) ===")
        history = run_kusatake_seed(seed, days=days, verbose=True)
        save_results(path, history)
        print(f"Saved to {path}")
    print("\nFull Kusatake baseline run complete.")


if __name__ == "__main__":
    main()
