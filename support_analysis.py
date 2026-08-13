import numpy as np, os, json, csv, sys
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from offgrid_marl import (House, Community, DEMAND_PROFILES, PERSONALITIES,
                          QLAgent, run_simulation)

BASE = 'results'
SUPPORT = os.path.join(BASE, 'analysis_support')
SEEDS = [42, 123, 456, 789, 1011]
EPISODES = 8000
SOLAR_MAX = 1.3
CLOUD_PROB = 0.15
NUM_HOUSES = 10
MIXED = ['prosocial'] * 5 + ['pure_selfish'] * 5
SELFISH = ['pure_selfish'] * 10
SCENARIOS = {
    'all_selfish': ['pure_selfish'] * 10,
    'all_prosocial': ['prosocial'] * 10,
    'mixed': ['prosocial'] * 5 + ['pure_selfish'] * 5,
    'varied_altruism': ['altruistic', 'prosocial', 'prosocial', 'prosocial',
                        'individualist', 'individualist', 'individualist',
                        'pure_selfish', 'pure_selfish', 'pure_selfish'],
    'innovator_effect': ['high_openness_innovator'] + ['prosocial'] * 4 +
                        ['individualist'] * 3 + ['pure_selfish'] * 2,
}

W_FAIR = {name: np.mean([PERSONALITIES[p]['w_fair'] for p in mix])
          for name, mix in SCENARIOS.items()}


# ========== always_default (no-sharing) runner ==========
def run_always_default(battery_cap, seed, episodes=EPISODES):
    demand_keys = list(DEMAND_PROFILES.keys())
    house_configs = [{'personality': PERSONALITIES[MIXED[i]],
                      'demand': DEMAND_PROFILES[demand_keys[i % len(demand_keys)]]}
                     for i in range(NUM_HOUSES)]
    np.random.seed(seed)
    houses = [House(i, cfg['demand'], battery_cap, cfg['personality'], SOLAR_MAX)
              for i, cfg in enumerate(house_configs)]
    community = Community(houses, {i: [(i + 1) % NUM_HOUSES] for i in range(NUM_HOUSES)})
    comfort_mean, fairness_l, blackout_days, total_waste = [], [], [], []
    for ep in range(episodes):
        community.reset_day()
        wf = 1.0 if np.random.random() > CLOUD_PROB else 0.5
        fairness = 1.0
        for hour in range(24):
            actions = {h.id: 0.0 for h in houses}
            comforts, fairness = community.step(hour, actions, wf)
        ep_comforts = np.array([max(0.0, h.demand_met) for h in houses])
        comfort_mean.append(np.mean(ep_comforts))
        fairness_l.append(fairness)
        blackout_days.append(1.0 if np.any(ep_comforts < 0.95) else 0.0)
        total_waste.append(sum(h.wasted for h in houses))
    last = 1000
    return {
        'comfort': np.mean(comfort_mean[-last:]),
        'fairness': np.mean(fairness_l[-last:]),
        'blackout_rate': np.mean(blackout_days[-last:]),
        'waste': np.mean(total_waste[-last:]),
    }


# ========== instrumented runner (captures Q-tables + action counts) ==========
def run_instrumented(mix, battery_cap, seed, episodes=EPISODES, eval_last=1000):
    np.random.seed(seed)
    demand_keys = list(DEMAND_PROFILES.keys())
    houses, agents = [], []
    for i in range(NUM_HOUSES):
        cfg = {'personality': PERSONALITIES[mix[i]],
               'demand': DEMAND_PROFILES[demand_keys[i % len(demand_keys)]]}
        pers_name = mix[i]
        house = House(i, cfg['demand'], battery_cap, cfg['personality'], SOLAR_MAX)
        houses.append(house)
        if pers_name == 'high_openness_innovator':
            agents.append(QLAgent(i, cfg['personality'], min_eps=0.05))
        else:
            agents.append(QLAgent(i, cfg['personality']))
    community = Community(houses, {i: [(i + 1) % NUM_HOUSES] for i in range(NUM_HOUSES)})

    comfort_mean, fairness_l, blackout_days, total_waste = [], [], [], []
    surplus_steps, share_steps, total_steps = 0, 0, 0

    for ep in range(episodes):
        community.reset_day()
        wf = 1.0 if np.random.random() > CLOUD_PROB else 0.5
        in_eval = (ep >= episodes - eval_last)
        for hour in range(24):
            states, nets = {}, {}
            for agent in agents:
                h = community.houses[agent.id]
                states[agent.id] = agent.get_state(hour, h.battery / h.battery_cap)
                nets[agent.id] = h.get_net(hour, wf)
            actions = {}
            for agent in agents:
                can_share = nets[agent.id] > 0
                actions[agent.id] = agent.select_action(states[agent.id], can_share)
            if in_eval:
                for agent in agents:
                    total_steps += 1
                    if nets[agent.id] > 0:
                        surplus_steps += 1
                        if actions[agent.id] > 0:
                            share_steps += 1
            comforts, fairness = community.step(hour, actions, wf)
            done = (hour == 23)
            for agent in agents:
                h = community.houses[agent.id]
                own_comfort = h.demand_met
                reward = agent.compute_reward(own_comfort, fairness)
                if not done:
                    next_state = agent.get_state(hour + 1, h.battery / h.battery_cap)
                else:
                    next_state = (0, 0)
                agent.update(states[agent.id], actions[agent.id], reward,
                             next_state, done)
        for agent in agents:
            agent.decay_epsilon()
        ep_comforts = np.array([max(0.0, h.demand_met) for h in houses])
        comfort_mean.append(np.mean(ep_comforts))
        fairness_l.append(fairness)
        blackout_days.append(1.0 if np.any(ep_comforts < 0.95) else 0.0)
        total_waste.append(sum(h.wasted for h in houses))

    last = eval_last
    qs = np.array([a.q for a in agents])  # (n_agents, 24, 4, 3)
    return {
        'metrics': {
            'comfort': np.mean(comfort_mean[-last:]),
            'fairness': np.mean(fairness_l[-last:]),
            'blackout_rate': np.mean(blackout_days[-last:]),
            'waste': np.mean(total_waste[-last:]),
        },
        'q': qs,
        'steps': {
            'total': total_steps,
            'surplus': surplus_steps,
            'share': share_steps,
        },
    }


def load_seed_metrics(folder):
    rows = {}
    for seed in SEEDS:
        path = os.path.join(BASE, folder, f'seed_{seed}', 'final_metrics.csv')
        if not os.path.exists(path):
            continue
        with open(path) as fh:
            d = next(csv.DictReader(fh))
        rows[seed] = d
    return rows


def mean_sd(vals):
    return np.mean(vals), np.std(vals, ddof=1)


# ==================================================================
# ANALYSIS 1: 0.5 kWh (battery_cap=5.0) battery sensitivity, 5 seeds
# ==================================================================
def analysis1():
    print("=" * 100)
    print("ANALYSIS 1 — BATTERY CAPACITY SENSITIVITY (0.5 kWh vs 0.7 kWh)")
    print("=" * 100)
    os.makedirs(os.path.join(SUPPORT, 'batt05', 'mixed'), exist_ok=True)
    os.makedirs(os.path.join(SUPPORT, 'batt05', 'always_default'), exist_ok=True)

    mixed05 = {}
    for seed in SEEDS:
        sp = os.path.join(SUPPORT, 'batt05', 'mixed', f'seed_{seed}')
        agents, community, history = run_simulation(
            num_houses=10, episodes=EPISODES, battery_cap=5.0, solar_max=SOLAR_MAX,
            personality_mix=MIXED, seed=seed, verbose=False, save_path=sp)
        with open(os.path.join(sp, 'final_metrics.csv')) as fh:
            d = next(csv.DictReader(fh))
        mixed05[seed] = {k: float(v) for k, v in d.items() if k != 'seed'}

    default05 = {}
    for seed in SEEDS:
        default05[seed] = run_always_default(5.0, seed)

    mixed07 = load_seed_metrics('mixed')
    default07 = load_seed_metrics('control_always_default')

    cols = {
        '0.5 kWh Mixed': mixed05,
        '0.5 kWh No-Sharing': default05,
        '0.7 kWh Mixed (Table 4-1)': {s: {k: float(v) for k, v in d.items()
                                          if k != 'seed'} for s, d in mixed07.items()},
        '0.7 kWh No-Sharing': {s: {k: float(v) for k, v in d.items()
                                   if k != 'seed'} for s, d in default07.items()},
    }
    metric_names = [('comfort', 'Mean Community Comfort'),
                    ('fairness', "Jain's Fairness"),
                    ('waste', 'Energy Waste (kWh/day)'),
                    ('blackout_rate', 'Blackout Rate (%)')]

    hdr = f"{'Metric':>28} | " + " | ".join(f"{c:>30}" for c in cols)
    print(hdr)
    print('-' * len(hdr))
    for key, label in metric_names:
        line = f"{label:>28} | "
        for c, data in cols.items():
            vals = [data[s][key] for s in SEEDS if s in data]
            m, sd = mean_sd(vals)
            if key == 'blackout_rate':
                line += f"{m*100:7.2f}% ± {sd*100:.2f}%     | "
            elif key == 'waste':
                line += f"{m:8.2f} ± {sd:5.2f} kWh | "
            else:
                line += f"{m:8.4f} ± {sd:.4f}     | "
        print(line)
    print('-' * len(hdr))

    print("\nSignificance: mixed vs no-sharing baseline (seed-matched paired t-test)")
    print(f"{'battery':>8} | {'metric':>8} | {'t':>7} | {'p':>8} | {'sig':>4}")
    for batt, m, d in [('0.5', mixed05, default05), ('0.7', cols['0.7 kWh Mixed (Table 4-1)'],
                                                     cols['0.7 kWh No-Sharing'])]:
        for met in ['comfort', 'waste']:
            mv = np.array([m[s][met] for s in SEEDS])
            dv = np.array([d[s][met] for s in SEEDS])
            t, p = stats.ttest_rel(mv, dv)
            sig = 'SIG' if p < 0.05 else 'ns'
            print(f"{batt:>6}kWh | {met:>8} | {t:+6.3f} | {p:.4f} | {sig:>4}")
    return cols


# ==================================================================
# ANALYSIS 2 & 3: Q-value distribution + share-action frequency
# ==================================================================
def q_stats(qs, role_ids=None):
    if role_ids is not None:
        qs = qs[role_ids]
    mean_q = qs.mean()
    var_q = qs.var()
    greedy = np.argmax(qs, axis=3)          # (n,24,4)
    share_states = (greedy >= 1).mean() * 100
    return mean_q, var_q, share_states, greedy


def analysis2_3():
    print("\n" + "=" * 100)
    print("ANALYSIS 2 — Q-VALUE DISTRIBUTION (mixed vs all-selfish baseline)")
    print("=" * 100)

    os.makedirs(os.path.join(SUPPORT, 'qtab'), exist_ok=True)
    mixed_res, selfish_res = {}, {}
    for seed in SEEDS:
        r = run_instrumented(MIXED, 7.0, seed)
        mixed_res[seed] = r
        r2 = run_instrumented(SELFISH, 7.0, seed)
        selfish_res[seed] = r2

    pro_qs = np.array([mixed_res[s]['q'] for s in SEEDS])   # (5, 10, 24, 4, 3)
    self_qs = np.array([selfish_res[s]['q'] for s in SEEDS])

    pro_agents = pro_qs[:, :5]     # prosocial agents in mixed
    mself_agents = pro_qs[:, 5:]   # selfish agents in mixed
    base_agents = self_qs[:, :]    # all-selfish baseline

    rows = []
    for label, arr in [('Mixed (prosocial agents)', pro_agents),
                       ('Mixed (selfish agents)', mself_agents),
                       ('All-selfish baseline', base_agents)]:
        mq, vq, ss, _ = q_stats(arr)
        rows.append((label, mq, vq, ss))
        print(f"  {label:>28}: mean Q = {mq:.4f}, Q variance = {vq:.4f}, "
              f"states greedy=share = {ss:.1f}%")

    # % states where greedy action differs: majority greedy per state, per seed
    def majority_greedy(qs_arr):
        qs_agents = np.argmax(qs_arr, axis=4)   # (seeds, n_agents, 24, 4)
        modes = np.zeros((qs_agents.shape[0], 24, 4), dtype=int)
        for s in range(qs_agents.shape[0]):
            for h in range(24):
                for b in range(4):
                    vals, cnts = np.unique(qs_agents[s, :, h, b], return_counts=True)
                    modes[s, h, b] = vals[np.argmax(cnts)]
        return modes

    g_pro = majority_greedy(pro_agents)
    g_ms = majority_greedy(mself_agents)
    g_base = majority_greedy(base_agents)
    diff_pro = (g_pro != g_base).mean() * 100
    diff_ms = (g_ms != g_base).mean() * 100
    print(f"  % states where greedy action differs (mixed-prosocial vs baseline): "
          f"{diff_pro:.1f}%")
    print(f"  % states where greedy action differs (mixed-selfish vs baseline): "
          f"{diff_ms:.1f}%")

    print("\n" + "=" * 100)
    print("ANALYSIS 3 — SHARE-ACTION FREQUENCY (mixed vs baselines)")
    print("=" * 100)
    m_steps = {s: mixed_res[s]['steps'] for s in SEEDS}
    s_steps = {s: selfish_res[s]['steps'] for s in SEEDS}
    m_share_pct = np.mean([m_steps[s]['share'] / m_steps[s]['total']
                           for s in SEEDS]) * 100
    m_surplus_pct = np.mean([m_steps[s]['surplus'] / m_steps[s]['total']
                             for s in SEEDS]) * 100
    s_share_pct = np.mean([s_steps[s]['share'] / s_steps[s]['total']
                           for s in SEEDS]) * 100
    s_surplus_pct = np.mean([s_steps[s]['surplus'] / s_steps[s]['total']
                             for s in SEEDS]) * 100

    hdr = f"{'Metric':>42} | {'Mixed':>12} | {'All-selfish':>14} | {'No-sharing (0%)':>16}"
    print(hdr)
    print('-' * len(hdr))
    print(f"{'Greedy action = share (states, %)':>42} | {rows[0][3]:10.1f}% | "
          f"{rows[2][3]:12.1f}% | {'0.0% (no Q-learning)':>16}")
    print(f"{'Actual sharing occurred (time steps, %)':>42} | {m_share_pct:10.1f}% | "
          f"{s_share_pct:12.1f}% | {'0.0% (forced a=0)':>16}")
    print(f"{'Exportable surplus available (time steps, %)':>42} | {m_surplus_pct:10.1f}% | "
          f"{s_surplus_pct:12.1f}% | {m_surplus_pct:14.1f}% |")
    print('-' * len(hdr))

    np.save(os.path.join(SUPPORT, 'qtab', 'mixed_q.npy'), pro_qs)
    np.save(os.path.join(SUPPORT, 'qtab', 'selfish_q.npy'), self_qs)
    return mixed_res, selfish_res


# ==================================================================
# ANALYSIS 4: wbar_fair vs waste reduction
# ==================================================================
def analysis4():
    print("\n" + "=" * 100)
    print("ANALYSIS 4 — CORRELATION: wbar_fair vs ENERGY-WASTE REDUCTION")
    print("=" * 100)
    ctrl = load_seed_metrics('control_always_default')
    ctrl_waste = {s: float(d['waste']) for s, d in ctrl.items()}

    scatter = []   # (scenario, seed, wbar_fair, waste_reduction)
    means = {}
    for sc in SCENARIOS:
        m = load_seed_metrics(sc)
        reds = [ctrl_waste[s] - float(m[s]['waste']) for s in SEEDS if s in m]
        means[sc] = np.mean(reds)
        for s in SEEDS:
            if s in m:
                scatter.append((sc, s, W_FAIR[sc], ctrl_waste[s] - float(m[s]['waste'])))

    wbar = np.array([W_FAIR[sc] for sc in SCENARIOS])
    red_mean = np.array([means[sc] for sc in SCENARIOS])
    r_mean, p_mean = stats.pearsonr(wbar, red_mean)

    x_all = np.array([p[2] for p in scatter])
    y_all = np.array([p[3] for p in scatter])
    r_all, p_all = stats.pearsonr(x_all, y_all)

    print(f"Scenario-level (n={len(SCENARIOS)}): wbar_fair vs mean waste reduction")
    print(f"  Pearson r = {r_mean:.4f}, p = {p_mean:.4f}")
    print(f"All points per-seed (n={len(scatter)}):")
    print(f"  Pearson r = {r_all:.4f}, p = {p_all:.4f}")

    print(f"\n{'scenario':>16} | {'wbar_fair':>9} | {'mean waste red.':>15} | "
          f"{'per-seed red.':>24}")
    for sc in SCENARIOS:
        seed_red = [f"{scatter[i][3]:.2f}" for i in range(len(scatter))
                    if scatter[i][0] == sc]
        print(f"{sc:>16} | {W_FAIR[sc]:9.3f} | {means[sc]:15.3f} | "
              f"{', '.join(seed_red):>24}")

    os.makedirs(SUPPORT, exist_ok=True)
    with open(os.path.join(SUPPORT, 'wfair_waste_scatter.csv'), 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['scenario', 'seed', 'wbar_fair', 'waste_reduction_kwh'])
        w.writerows(scatter)
    print(f"\nSaved: {SUPPORT}/wfair_waste_scatter.csv")
    return r_mean, p_mean, r_all, p_all


if __name__ == '__main__':
    analysis1()
    analysis2_3()
    analysis4()
    print("\nAll analyses complete.")
