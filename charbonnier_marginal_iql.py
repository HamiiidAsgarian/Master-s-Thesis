import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, json, csv, argparse

from offgrid_marl import DEMAND_PROFILES, House, Community

ALG_NAME = 'baseline_charbonnier'

# ========== HYPERPARAMETERS (Charbonnier et al. 2022, per spec) ==========
GAMMA = 0.99
ALPHA = 0.01
BETA = 0.5
EPS0 = 0.5
EPS_DECAY = 0.999
EPS_MIN = 0.05
ACTIONS = [0.0, 0.5, 1.0]
Q_INIT = 1.0

# Frozen-evaluation settings for the validation sanity check
EVAL_EPISODES = 200
EVAL_SEED = 999

SNAP_ATTRS = ['battery', 'demand_met', 'received', 'exported', 'wasted',
              'total_blackout_hours']


# ========== MARGINAL (ROLE-FREE) Q-LEARNING AGENT ==========
class MarginalAgent:
    def __init__(self, house_id, state_bins=[0.25, 0.5, 0.75],
                 alpha=ALPHA, beta=BETA, gamma=GAMMA, eps=EPS0,
                 eps_decay=EPS_DECAY, min_eps=EPS_MIN):
        self.id = house_id
        self.state_bins = state_bins
        self.num_bat = len(state_bins) + 1
        self.q = np.ones((24, self.num_bat, 3)) * Q_INIT
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.epsilon = eps
        self.eps_decay = eps_decay
        self.min_eps = min_eps
        self.actions = ACTIONS

    def get_state(self, hour, battery_frac):
        battery_frac = max(0.0, min(1.0, battery_frac))
        for i, thr in enumerate(self.state_bins):
            if battery_frac <= thr:
                return (hour, i)
        return (hour, len(self.state_bins))

    def select_action(self, state, can_share):
        if not can_share:
            return 0.0
        if np.random.random() < self.epsilon:
            return np.random.choice(self.actions)
        h, b = state
        return self.actions[np.argmax(self.q[h, b])]

    def greedy_action(self, state):
        h, b = state
        return self.actions[np.argmax(self.q[h, b])]

    def update(self, state, action, reward, next_state, done):
        h, b = state
        nh, nb = next_state
        act_idx = self.actions.index(action)
        best_next = np.max(self.q[nh, nb]) if not done else 0.0
        delta = reward + self.gamma * best_next - self.q[h, b, act_idx]
        lr = self.alpha if delta >= 0 else self.beta * self.alpha
        self.q[h, b, act_idx] += lr * delta

    def decay_epsilon(self):
        self.epsilon = max(self.min_eps, self.epsilon * self.eps_decay)


# ========== STATE SNAPSHOT / RESTORE (for counterfactual reward) ==========
def snapshot_houses(houses):
    return [{a: getattr(h, a) for a in SNAP_ATTRS} for h in houses]


def restore_houses(houses, snap):
    for h, s in zip(houses, snap):
        for a in SNAP_ATTRS:
            setattr(h, a, s[a])


# ========== SYSTEM REWARD F ==========
# F_t = mean comfort + Jain's fairness index  (F in [0, 2])
def system_reward(comforts, fairness):
    return float(np.mean(comforts)) + float(fairness)


# ========== WORLD CONSTRUCTION (environment unchanged from main runs) ==========
def build_world(num_houses=10, battery_cap=7.0, solar_max=1.3):
    demand_keys = list(DEMAND_PROFILES.keys())
    neutral = {'w_self': 1.0, 'w_fair': 0.0}
    houses = []
    agents = []
    for i in range(num_houses):
        demand = DEMAND_PROFILES[demand_keys[i % len(demand_keys)]]
        houses.append(House(i, demand, battery_cap, neutral, solar_max))
        agents.append(MarginalAgent(i))
    sharing_pairs = {i: [(i + 1) % num_houses] for i in range(num_houses)}
    community = Community(houses, sharing_pairs)
    return houses, agents, community


# ========== SIMULATION LOOP ==========
# Marginal reward is the TRUE end-of-day counterfactual:
#   r_i,t = F_end − F_end^(default_i)
# where F_end = mean comfort + fairness at end of day, and F_end^(default_i) is
# obtained by re-running hours t..23 with agent i's action at hour t replaced by
# share-0% and every other action (agent i's included) held fixed at what was
# actually chosen.
def run_baseline_simulation(num_houses=10, episodes=8000, battery_cap=7.0,
                            solar_max=1.3, seed=42, weather_cloud_prob=0.15,
                            verbose=True):
    np.random.seed(seed)
    houses, agents, community = build_world(num_houses, battery_cap, solar_max)

    if verbose:
        sample_solar = sum(houses[0].solar(h, 1.0) for h in range(24))
        avg_demand = np.mean([h.daily_demand for h in houses])
        print(f"Solar gen/day (clear): ~{sample_solar:.1f} kWh, Avg demand: {avg_demand:.1f} kWh")
        print(f"Battery: {battery_cap} kWh (start 50%), role-free marginal IQL (END-OF-DAY F): "
              f"alpha={ALPHA}, beta={BETA}, gamma={GAMMA}, eps0={EPS0}, decay={EPS_DECAY}, min={EPS_MIN}\n")

    history = {
        'comfort_mean': [], 'fairness': [], 'blackout_days': [],
        'total_waste': [],
        'agent_rewards': [[] for _ in agents],
        'agent_comforts': [[] for _ in agents],
        'cf_skip': 0, 'cf_used': 0, 'cf_reward_samples': 0, 'cf_reward_sum': 0.0,
        'cf_reward_by_hour_sum': np.zeros(24),
        'cf_reward_by_hour_n': np.zeros(24),
    }

    for ep in range(episodes):
        community.reset_day()
        weather_factor = 1.0 if np.random.random() > weather_cloud_prob else 0.5
        ep_rewards = np.zeros(len(agents))

        day_actions = [None] * 24
        day_states = [None] * 24
        day_next_states = [None] * 24
        day_nets = [None] * 24
        pre_states = [None] * 24

        for hour in range(24):
            states, nets = {}, {}
            for agent in agents:
                h = community.houses[agent.id]
                bat_frac = h.battery / h.battery_cap
                states[agent.id] = agent.get_state(hour, bat_frac)
                nets[agent.id] = h.get_net(hour, weather_factor)
            actions = {}
            for agent in agents:
                can_share = nets[agent.id] > 0
                actions[agent.id] = agent.select_action(states[agent.id], can_share)
            pre_states[hour] = snapshot_houses(houses)
            comforts, fairness = community.step(hour, actions, weather_factor)
            next_states = {}
            for agent in agents:
                h = community.houses[agent.id]
                if hour < 23:
                    next_states[agent.id] = agent.get_state(hour + 1, h.battery / h.battery_cap)
                else:
                    next_states[agent.id] = (0, 0)
            day_actions[hour] = actions
            day_states[hour] = states
            day_next_states[hour] = next_states
            day_nets[hour] = nets

        end_state = snapshot_houses(houses)
        F_end = system_reward(comforts, fairness)  # hour-23 values

        for hour in range(24):
            actions = day_actions[hour]
            nets = day_nets[hour]
            for agent in agents:
                # Counterfactual only matters if this agent actually could have
                # deviated to share-0%. Otherwise r_i,t = 0 by construction.
                if nets[agent.id] > 0 and actions[agent.id] > 0.0:
                    cf_actions = dict(actions)
                    cf_actions[agent.id] = 0.0
                    restore_houses(houses, pre_states[hour])
                    cf_comforts, cf_fairness = community.step(hour, cf_actions, weather_factor)
                    for h2 in range(hour + 1, 24):
                        cf_comforts, cf_fairness = community.step(h2, day_actions[h2], weather_factor)
                    F_end_cf = system_reward(cf_comforts, cf_fairness)
                    restore_houses(houses, end_state)
                    r = F_end - F_end_cf
                    history['cf_used'] += 1
                    history['cf_reward_samples'] += 1
                    history['cf_reward_sum'] += r
                    history['cf_reward_by_hour_sum'][hour] += r
                    history['cf_reward_by_hour_n'][hour] += 1
                else:
                    r = 0.0
                    history['cf_skip'] += 1
                ep_rewards[agent.id] += r
                agent.update(day_states[hour][agent.id], day_actions[hour][agent.id],
                             r, day_next_states[hour][agent.id], done=(hour == 23))

        for agent in agents:
            agent.decay_epsilon()

        ep_comforts = np.array([s['demand_met'] for s in end_state])
        mean_comfort = np.mean(ep_comforts)
        had_blackout = np.any(ep_comforts < 0.95)
        total_waste = sum(h.wasted for h in houses)

        history['comfort_mean'].append(mean_comfort)
        history['fairness'].append(fairness)
        history['blackout_days'].append(1.0 if had_blackout else 0.0)
        history['total_waste'].append(total_waste)
        for i in range(len(agents)):
            history['agent_rewards'][i].append(ep_rewards[i])
            history['agent_comforts'][i].append(ep_comforts[i])

        if verbose and (ep + 1) % 2000 == 0:
            print(f"Ep {ep+1:4d}: comfort={mean_comfort:.3f}, fairness={fairness:.3f}, "
                  f"blackout%={np.mean(history['blackout_days'][-2000:])*100:.1f}%, "
                  f"waste={np.mean(history['total_waste'][-2000:]):.2f} kWh, eps={agents[0].epsilon:.3f}")

    return agents, community, history


# ========== PLOTTING ==========
def plot_learning(history, title, save_path):
    from thesis_plot_style import C, save_fig, style_data_axes, style_legend

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))

    ax = axes[0]
    ax.plot(history['comfort_mean'], label='Mean Comfort', color=C['blue'], lw=2, alpha=0.9)
    ax.plot(history['fairness'], label="Jain's Fairness", color=C['green'], lw=2, alpha=0.9)
    ax.set_xlabel('Episode'); ax.set_ylabel('Score'); ax.set_ylim(0, 1.05)
    ax.set_title('Community Performance', fontweight='bold', fontsize=10)
    leg = ax.legend(loc='lower right'); style_legend(leg); style_data_axes(ax)

    ax = axes[1]
    blackout = np.array(history['blackout_days'])
    window = 500
    if len(blackout) > window:
        rolling = np.convolve(blackout, np.ones(window) / window, mode='valid')
        ax.plot(range(window - 1, len(blackout)), rolling, color=C['red'], lw=2)
    else:
        ax.plot(blackout, color=C['red'], lw=2)
    ax.set_xlabel('Episode'); ax.set_ylabel('Frequency')
    ax.set_title(f'Blackout Rate ({window}-ep moving avg)', fontweight='bold', fontsize=10)
    style_data_axes(ax)

    ax = axes[2]
    rewards = np.array(history['agent_rewards'])
    mean_r = rewards.mean(axis=0)
    if len(mean_r) > 200:
        ax.plot(np.convolve(mean_r, np.ones(200) / 200, mode='valid'), color=C['purple'], lw=2)
    else:
        ax.plot(mean_r, color=C['purple'], lw=2)
    ax.set_xlabel('Episode'); ax.set_ylabel('Mean Marginal Reward')
    ax.set_title('Mean Agent Reward (200-ep smooth)', fontweight='bold', fontsize=10)
    style_data_axes(ax)

    fig.suptitle(title, fontsize=13, fontweight='bold')
    fig.tight_layout()
    save_fig(fig, save_path)
    plt.close(fig)


# ========== SAVE RESULTS (same schema as main runs + scenario label) ==========
def save_results(save_path, history, agents, seed, episodes, weather_cloud_prob,
                 battery_cap=7.0, solar_max=1.3):
    os.makedirs(save_path, exist_ok=True)
    last_n = min(1000, episodes)
    final_comfort = np.mean(history['comfort_mean'][-last_n:])
    final_fairness = np.mean(history['fairness'][-last_n:])
    final_blackout = np.mean(history['blackout_days'][-last_n:])
    final_waste = np.mean(history['total_waste'][-last_n:])
    overall = np.mean([np.mean(history['agent_comforts'][i][-last_n:])
                       for i in range(len(agents))])
    f_seq = (np.array(history['comfort_mean'][-last_n:]) +
             np.array(history['fairness'][-last_n:]))
    f_end = np.mean(f_seq)

    metrics = {
        'scenario': ALG_NAME,
        'seed': seed,
        'comfort': final_comfort,
        'fairness': final_fairness,
        'F': f_end,
        'blackout_rate': final_blackout,
        'waste': final_waste,
        'prosocial_comfort': overall,
        'selfish_comfort': overall,
    }
    with open(os.path.join(save_path, 'final_metrics.csv'), 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(metrics.keys()))
        writer.writeheader()
        writer.writerow(metrics)

    config = {
        'algorithm': ALG_NAME,
        'role_free': True,
        'reward': 'marginal (end-of-day): r_i,t = F_end - F_end^default_i, '
                 'F = mean_comfort + jain_fairness, CF re-runs hours t..23 with action swapped to 0%',
        'update': 'hysteretic (alpha for delta>=0, beta*alpha for delta<0)',
        'num_houses': len(agents),
        'episodes': episodes,
        'battery_cap': battery_cap,
        'solar_max': solar_max,
        'weather_cloud_prob': weather_cloud_prob,
        'gamma': GAMMA, 'alpha': ALPHA, 'beta': BETA,
        'eps0': EPS0, 'eps_decay': EPS_DECAY, 'eps_min': EPS_MIN,
        'q_init': f'optimistic {Q_INIT}',
        'seed': seed,
    }
    with open(os.path.join(save_path, 'config.json'), 'w') as f:
        json.dump(config, f, indent=2)

    plot_learning(history, f"Baseline Charbonnier Marginal IQL (seed {seed})",
                  os.path.join(save_path, 'results_plot.png'))


# ========== POLICY INSPECTION HELPERS ==========
def action_distribution(agents):
    """Avg fraction of the 96 states preferring each action (argmax over Q)."""
    counts = np.zeros(3)
    for agent in agents:
        best = np.argmax(agent.q, axis=2)  # (24, 4)
        for a in range(3):
            counts[a] += np.sum(best == a)
    return counts / (len(agents) * 24 * agent.num_bat)


def sharing_frequency(agents):
    dist = action_distribution(agents)
    return float(dist[1] + dist[2])


def per_hour_share_fraction(agents):
    """Avg fraction of battery-bins (and agents) preferring to share, per hour."""
    f = np.zeros(24)
    for agent in agents:
        best = np.argmax(agent.q, axis=2)  # (24, 4)
        f += np.mean(best >= 1, axis=1)
    return f / len(agents)


# ========== FROZEN EVALUATION (greedy vs always-default) ==========
def evaluate_greedy(agents, community, weather_seq):
    Fs, comfs, fairs = [], [], []
    surplus = np.zeros(24)
    shared = np.zeros(24)
    for wf in weather_seq:
        community.reset_day()
        for hour in range(24):
            states, nets = {}, {}
            for agent in agents:
                h = community.houses[agent.id]
                states[agent.id] = agent.get_state(hour, h.battery / h.battery_cap)
                nets[agent.id] = h.get_net(hour, wf)
            actions = {}
            for agent in agents:
                can_share = nets[agent.id] > 0
                actions[agent.id] = agent.greedy_action(states[agent.id]) if can_share else 0.0
                if can_share:
                    surplus[hour] += 1
                    if actions[agent.id] > 0.0:
                        shared[hour] += 1
            comforts, fairness = community.step(hour, actions, wf)
            if hour == 23:
                Fs.append(system_reward(comforts, fairness))
                comfs.append(np.mean(comforts))
                fairs.append(fairness)
    realized = np.divide(shared, surplus, out=np.zeros_like(shared),
                         where=surplus > 0)
    return np.mean(Fs), np.mean(comfs), np.mean(fairs), realized, surplus


def evaluate_default(community, weather_seq):
    Fs, comfs, fairs = [], [], []
    for wf in weather_seq:
        community.reset_day()
        for hour in range(24):
            actions = {i: 0.0 for i in range(len(community.houses))}
            comforts, fairness = community.step(hour, actions, wf)
            if hour == 23:
                Fs.append(system_reward(comforts, fairness))
                comfs.append(np.mean(comforts))
                fairs.append(fairness)
    return np.mean(Fs), np.mean(comfs), np.mean(fairs)


# ========== VALIDATION REPORT ==========
def build_validation_report(agents, history, episodes, seed):
    last_n = min(1000, episodes)
    comfort = np.mean(history['comfort_mean'][-last_n:])
    fairness = np.mean(history['fairness'][-last_n:])
    blackout = np.mean(history['blackout_days'][-last_n:])
    waste = np.mean(history['total_waste'][-last_n:])
    mean_r = np.mean([np.mean(history['agent_rewards'][i][-last_n:])
                      for i in range(len(agents))])

    total = history['cf_skip'] + history['cf_used']
    skip_ratio = history['cf_skip'] / total if total else 0.0
    dist = action_distribution(agents)
    sf = sharing_frequency(agents)
    hours = per_hour_share_fraction(agents)

    n = history['cf_reward_by_hour_n']
    mean_marg_hour = np.where(n > 0, history['cf_reward_by_hour_sum'] / np.maximum(n, 1), 0.0)
    pos_hours = [h for h in range(24) if mean_marg_hour[h] > 1e-4]
    neg_hours = [h for h in range(24) if mean_marg_hour[h] < -1e-4]
    share_hours = [h for h in range(24) if hours[h] > 0.05]
    max_share_hour = int(np.argmax(hours))
    differentiated = float(np.ptp(hours)) > 0.1

    lines = []
    lines.append("=" * 72)
    lines.append(f"CHARBONNIER MARGINAL IQL (END-OF-DAY) — VALIDATION (episodes={episodes}, seed={seed})")
    lines.append("=" * 72)
    lines.append(f"\nFinal metrics (last {last_n} episodes):")
    lines.append(f"  Mean comfort:       {comfort:.3f}")
    lines.append(f"  Jain's fairness:    {fairness:.3f}")
    lines.append(f"  Blackout day rate:  {blackout*100:.1f}%")
    lines.append(f"  Avg daily waste:    {waste:.2f} kWh")
    lines.append(f"  Mean agent reward:  {mean_r:.4f}")

    lines.append(f"\nCounterfactual accounting (hourly agent-steps, whole run):")
    lines.append(f"  computed (real CF):      {history['cf_used']}")
    lines.append(f"  skipped (net<=0 or a=0): {history['cf_skip']}")
    lines.append(f"  skip ratio:              {skip_ratio*100:.1f}%")
    if history['cf_reward_samples']:
        lines.append(f"  mean marginal reward of computed CF: "
                     f"{history['cf_reward_sum']/history['cf_reward_samples']:.4f}")

    lines.append(f"\nQ-table policy (avg over {len(agents)} agents x 96 states):")
    lines.append(f"  prefer Share 0% : {dist[0]*100:.1f}%")
    lines.append(f"  prefer Share 50%: {dist[1]*100:.1f}%")
    lines.append(f"  prefer Share 100%: {dist[2]*100:.1f}%")
    lines.append(f"  sharing frequency (any share): {sf*100:.1f}%")

    lines.append(f"\nHour differentiation of learned policy (avg over agents & battery bins):")
    lines.append(f"  differentiated across hours: {'YES' if differentiated else 'NO'} "
                 f"(range {hours.min()*100:.1f}%..{hours.max()*100:.1f}%)")
    lines.append(f"  hour with max sharing preference: {max_share_hour} ({hours[max_share_hour]*100:.1f}%)")
    lines.append(f"  hours preferring any sharing (>5%): {share_hours if share_hours else 'none'}")
    lines.append(f"  learned share frac by hour: "
                 + " ".join(f"{h}:{hours[h]*100:.0f}%" for h in range(24)))

    lines.append(f"\nTraining marginal signal by hour (mean over computed CFs):")
    lines.append(f"  hours with positive mean marginal: {pos_hours if pos_hours else 'none'}")
    lines.append(f"  hours with negative mean marginal: {neg_hours if neg_hours else 'none'}")
    if len(pos_hours) > 0:
        shared_at_pos = [h for h in pos_hours if hours[h] > 0.05]
        lines.append(f"  policy shares at positive-marginal hours: "
                     f"{'YES' if shared_at_pos else 'NO'} ({shared_at_pos})")
    return lines


def run_validation(base_dir='results', episodes=3000, seed=42):
    agents, community, history = run_baseline_simulation(
        num_houses=10, episodes=episodes, battery_cap=7.0, solar_max=1.3,
        seed=seed, weather_cloud_prob=0.15, verbose=True)

    report = build_validation_report(agents, history, episodes, seed)

    # Frozen evaluation on a matched weather sequence (both policies see same days)
    rng = np.random.RandomState(EVAL_SEED)
    weather_seq = [1.0 if rng.random() > 0.15 else 0.5 for _ in range(EVAL_EPISODES)]
    F_g, comf_g, fair_g, realized, surplus = evaluate_greedy(agents, community, weather_seq)
    F_d, comf_d, fair_d = evaluate_default(community, weather_seq)

    surplus_hours = [h for h in range(24) if surplus[h] > 0]
    pos_hours = [h for h in range(24) if history['cf_reward_by_hour_n'][h] > 0
                 and history['cf_reward_by_hour_sum'][h] / history['cf_reward_by_hour_n'][h] > 1e-4]
    share_hours = [h for h in surplus_hours if realized[h] > 0.05]
    overall_realized = np.sum(realized * surplus) / np.sum(surplus) if np.sum(surplus) > 0 else 0.0

    eval_lines = [
        f"\nFrozen evaluation ({EVAL_EPISODES} matched days):",
        f"  Learned greedy policy: F={F_g:.4f}  comfort={comf_g:.3f}  fairness={fair_g:.3f}",
        f"  Always-default (0%)  : F={F_d:.4f}  comfort={comf_d:.3f}  fairness={fair_d:.3f}",
        f"  F gain over default  : {F_g - F_d:+.4f}",
        f"\nRealized sharing under greedy policy (fraction of surplus steps where share > 0):",
        f"  overall realized sharing: {overall_realized*100:.1f}% of {int(np.sum(surplus))} surplus steps",
        f"  by hour: " + " ".join(f"{h}:{realized[h]*100:.0f}%" for h in surplus_hours),
        f"  hours with realized sharing (>5%): {share_hours if share_hours else 'none'}",
    ]
    if pos_hours:
        eval_lines.append(
            f"  shares at positive-marginal hours {pos_hours}: "
            f"{'YES' if any(h in share_hours for h in pos_hours) else 'NO'}")

    if abs(history['cf_reward_sum']) < 1e-9 and history['cf_reward_samples'] > 0:
        interp = "Marginal reward is structurally ~0 -> no learning signal."
    elif F_g > F_d + 1e-4:
        interp = ("Marginal signal is informative and the learned policy beats always-default.")
    elif F_g < F_d - 1e-4:
        interp = ("Marginal signal is informative; the learned policy is WORSE than always-default "
                  "(sharing depletes donors more than it helps -> near-always-default is the rational outcome).")
    else:
        interp = "Learned policy ~ equals always-default."
    eval_lines.append(f"\nInterpretation:")
    eval_lines.append(f"  {interp}")

    print("\n".join(report))
    print("\n".join(eval_lines))

    # Persist validation artifacts separately so results/baseline_charbonnier/
    # stays clean for the real seed runs.
    save_dir = os.path.join(base_dir, 'baseline_charbonnier_validation')
    os.makedirs(save_dir, exist_ok=True)
    save_results(save_dir, history, agents, seed, episodes, 0.15)
    with open(os.path.join(save_dir, 'validation_report.txt'), 'w') as f:
        f.write("\n".join(report))
        f.write("\n")
        f.write("\n".join(eval_lines))
        f.write("\n")
    print(f"\nValidation artifacts saved to {save_dir}")


# ========== MAIN ==========
def main():
    ap = argparse.ArgumentParser(description="Charbonnier marginal IQL baseline")
    ap.add_argument('--validation', action='store_true',
                    help='short sanity run + report (episodes defaults to 3000)')
    ap.add_argument('--episodes', type=int, default=None,
                    help='episodes (full run default 8000, validation default 3000)')
    ap.add_argument('--seeds', type=int, nargs='*', default=None,
                    help='seeds (full run default: 42 123 456 789 1011)')
    ap.add_argument('--weather_cloud_prob', type=float, default=0.15)
    ap.add_argument('--base_dir', default='results')
    args = ap.parse_args()

    if args.validation:
        episodes = args.episodes if args.episodes else 3000
        run_validation(base_dir=args.base_dir, episodes=episodes, seed=42)
        return

    seeds = args.seeds if args.seeds else [42, 123, 456, 789, 1011]
    episodes = args.episodes if args.episodes else 8000
    for seed in seeds:
        path = os.path.join(args.base_dir, 'baseline_charbonnier', f'seed_{seed}')
        print(f"\nRunning {ALG_NAME} seed {seed} ({episodes} episodes)...")
        agents, community, history = run_baseline_simulation(
            num_houses=10, episodes=episodes, battery_cap=7.0, solar_max=1.3,
            seed=seed, weather_cloud_prob=args.weather_cloud_prob, verbose=True)
        save_results(path, history, agents, seed, episodes, args.weather_cloud_prob)
        print(f"Saved to {path}")
    print("\nFull Charbonnier baseline run complete.")


if __name__ == "__main__":
    main()
