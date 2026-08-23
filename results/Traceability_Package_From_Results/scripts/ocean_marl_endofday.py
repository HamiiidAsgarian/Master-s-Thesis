import numpy as np
import matplotlib
matplotlib.use('Agg')
import os, json, csv, argparse

from offgrid_marl import DEMAND_PROFILES, PERSONALITIES, House, Community, QLAgent, plot_results

# ========== SCENARIOS (identical to run_experiments.py.py) ==========
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

# Hyperparameters identical to the main runs (offgrid_marl.QLAgent defaults):
# alpha=0.2, gamma=0.99, eps0=1.0, eps_decay=0.999, min_eps=0.01 (innovator 0.05),
# optimistic Q init 1.0.  The ONLY change vs the main runs is the reward horizon.
ACTIONS = [0.0, 0.5, 1.0]
EVAL_EPISODES = 200
EVAL_SEED = 999
SNAP_ATTRS = ['battery', 'demand_met', 'received', 'exported', 'wasted',
              'total_blackout_hours']


# ========== STATE SNAPSHOT / RESTORE (for counterfactual reward) ==========
def snapshot_houses(houses):
    return [{a: getattr(h, a) for a in SNAP_ATTRS} for h in houses]


def restore_houses(houses, snap):
    for h, s in zip(houses, snap):
        for a in SNAP_ATTRS:
            setattr(h, a, s[a])


# ========== PERSONALITY-WEIGHTED END-OF-DAY OBJECTIVE ==========
# Agent i's end-of-day value: F_end(i) = w_self_i * C_i + w_fair_i * F
# (C_i = agent i's demand_met at hour 23; F = Jain's fairness at hour 23).
# Same weights as the original per-step reward, evaluated at end-of-day.
def endofday_value(agent, comforts, fairness):
    return agent.w_self * comforts[agent.id] + agent.w_fair * fairness


# ========== WORLD CONSTRUCTION (same as main run_simulation) ==========
# neutral=True mirrors the Charbonnier baseline's homogeneous condition: every
# house gets the SAME role-free weights {w_self:1.0, w_fair:0.0}, no personality
# roles, identical agents (Q-learning rule is still OCEAN-MARL's).
NEUTRAL = {'w_self': 1.0, 'w_fair': 0.0}


def build_world(mix, num_houses=10, battery_cap=7.0, solar_max=1.3,
                neutral=False):
    demand_keys = list(DEMAND_PROFILES.keys())
    houses, agents = [], []
    for i in range(num_houses):
        if neutral:
            pers, personality = 'neutral', NEUTRAL
        else:
            pers = mix[i]
            personality = PERSONALITIES[pers]
        demand = DEMAND_PROFILES[demand_keys[i % len(demand_keys)]]
        houses.append(House(i, demand, battery_cap, personality, solar_max))
        if pers == 'high_openness_innovator':
            agents.append(QLAgent(i, personality, min_eps=0.05))
        else:
            agents.append(QLAgent(i, personality))
    sharing_pairs = {i: [(i + 1) % num_houses] for i in range(num_houses)}
    community = Community(houses, sharing_pairs)
    return houses, agents, community


# ========== END-OF-DAY OBJECTIVE (SWITCHABLE) ==========
# 'personality': F_end(i) = w_self_i * C_i + w_fair_i * F   (per-agent weights,
#                identical to the main runs' per-step reward, evaluated at hour 23)
# 'community'  : F_end(i) = mean(C) + F                    (role-free, the same
#                community objective for every agent — Charbonnier baseline's F)
# Either way the reward is the TRUE end-of-day counterfactual:
#   r_i,t = F_end(i) − F_end^(default_i)(i)
# where F_end^(default_i)(i) is obtained by re-running hours t..23 with agent i's
# action at hour t replaced by share-0% and every other action held fixed at what
# was actually chosen.
def endofday_value(agent, comforts, fairness, objective):
    if objective == 'community':
        return float(np.mean(comforts)) + float(fairness)
    return agent.w_self * comforts[agent.id] + agent.w_fair * fairness


def _cell_label(objective, homogeneous=False):
    if objective == 'community' and homogeneous:
        return ('D2: community objective x end-of-day horizon x HOMOGENEOUS '
                'role-free env x OCEAN-MARL Q-learning (mirrors Charbonnier env '
                'exactly, swaps only the learning rule)')
    if objective == 'community':
        return ('D: community objective x end-of-day horizon x OCEAN-MARL Q-learning '
                '(completes the 2x2; same objective cell as Charbonnier, same learning '
                'rule as the personality-weighted end-of-day sanity)')
    return ('B: personality-weighted objective x end-of-day horizon x OCEAN-MARL '
            'Q-learning (complements per-step main result in cell A)')


def run_endofday_simulation(mix, num_houses=10, episodes=8000, battery_cap=7.0,
                            solar_max=1.3, seed=42, weather_cloud_prob=0.15,
                            objective='personality', verbose=True,
                            neutral=False):
    np.random.seed(seed)
    houses, agents, community = build_world(mix, num_houses, battery_cap,
                                            solar_max, neutral=neutral)

    if verbose:
        sample_solar = sum(houses[0].solar(h, 1.0) for h in range(24))
        avg_demand = np.mean([h.daily_demand for h in houses])
        env_desc = ('HOMOGENEOUS role-free env (all neutral, no personality roles)'
                    if neutral else 'standard env (personality roles)')
        print(f"Solar gen/day (clear): ~{sample_solar:.1f} kWh, Avg demand: {avg_demand:.1f} kWh")
        print(f"Battery: {battery_cap} kWh (start 50%), END-OF-DAY counterfactual Q-learning "
              f"[objective={objective}, {env_desc}]: alpha=0.2, gamma=0.99, eps0=1.0, "
              f"decay=0.999, min_eps={0.05 if (not neutral and mix and 'high_openness_innovator' in mix) else 0.01}\n")

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

        for hour in range(24):
            actions = day_actions[hour]
            nets = day_nets[hour]
            for agent in agents:
                if nets[agent.id] > 0 and actions[agent.id] > 0.0:
                    cf_actions = dict(actions)
                    cf_actions[agent.id] = 0.0
                    restore_houses(houses, pre_states[hour])
                    cf_comforts, cf_fairness = community.step(hour, cf_actions, weather_factor)
                    for h2 in range(hour + 1, 24):
                        cf_comforts, cf_fairness = community.step(h2, day_actions[h2], weather_factor)
                    r = (endofday_value(agent, comforts, fairness, objective)
                         - endofday_value(agent, cf_comforts, cf_fairness, objective))
                    restore_houses(houses, end_state)
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


# ========== POLICY INSPECTION HELPERS ==========
def action_distribution(agents):
    counts = np.zeros(3)
    for agent in agents:
        best = np.argmax(agent.q, axis=2)
        for a in range(3):
            counts[a] += np.sum(best == a)
    return counts / (len(agents) * 24 * agent.num_bat)


def sharing_frequency(agents):
    dist = action_distribution(agents)
    return float(dist[1] + dist[2])


def per_hour_share_fraction(agents):
    f = np.zeros(24)
    for agent in agents:
        best = np.argmax(agent.q, axis=2)
        f += np.mean(best >= 1, axis=1)
    return f / len(agents)


# ========== SAVE RESULTS (baseline schema + endofday scenario label) ==========
def save_results(save_path, history, agents, scenario, seed, episodes,
                 weather_cloud_prob, battery_cap=7.0, solar_max=1.3,
                 objective='personality', personality_mix=None):
    os.makedirs(save_path, exist_ok=True)
    scenario_label = f'{scenario}_endofday'
    if objective == 'community':
        scenario_label = f'{scenario}_endofday_community'
        if personality_mix == ['neutral'] * len(agents):
            scenario_label = f'{scenario}_endofday_community_homogeneous'
    last_n = min(1000, episodes)
    final_comfort = np.mean(history['comfort_mean'][-last_n:])
    final_fairness = np.mean(history['fairness'][-last_n:])
    final_blackout = np.mean(history['blackout_days'][-last_n:])
    final_waste = np.mean(history['total_waste'][-last_n:])
    f_seq = (np.array(history['comfort_mean'][-last_n:]) +
             np.array(history['fairness'][-last_n:]))
    f_end = np.mean(f_seq)
    overall = np.mean([np.mean(history['agent_comforts'][i][-last_n:])
                       for i in range(len(agents))])

    metrics = {
        'scenario': scenario_label,
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
        'scenario': scenario_label,
        'algorithm': 'ocean_marl_endofday',
        'objective': objective,
        'personality_mix': personality_mix if personality_mix is not None
                           else SCENARIOS[scenario],
        'reward': ('end-of-day counterfactual: r_i,t = F_end(i) - F_end^default_i(i); '
                   + ('F_end(i) = w_self_i*C_i + w_fair_i*F at hour 23'
                      if objective == 'personality'
                      else 'F_end(i) = mean(C) + F at hour 23 (role-free community '
                           'objective, same as Charbonnier baseline)')
                   + '; CF re-runs hours t..23 with action swapped to 0%'),
        'update': 'standard Q-learning (alpha=0.2, symmetric), same as main runs',
        'num_houses': len(agents),
        'episodes': episodes,
        'battery_cap': battery_cap,
        'solar_max': solar_max,
        'weather_cloud_prob': weather_cloud_prob,
        'seed': seed,
    }
    with open(os.path.join(save_path, 'config.json'), 'w') as f:
        json.dump(config, f, indent=2)

    fig = plot_results(history, title=f'OCEAN-MARL end-of-day ({scenario}, seed {seed})')
    fig.savefig(os.path.join(save_path, 'results_plot.png'), dpi=150, bbox_inches='tight')
    import matplotlib.pyplot as plt
    plt.close(fig)

# ========== FROZEN EVALUATION (greedy vs always-default, standard F metric) ==========
def evaluate_greedy(agents, community, weather_seq):
    Fs, comfs, fairs = [], [], []
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
                if can_share:
                    actions[agent.id] = agent.actions[np.argmax(agent.q[states[agent.id]])]
                else:
                    actions[agent.id] = 0.0
            comforts, fairness = community.step(hour, actions, wf)
            if hour == 23:
                Fs.append(float(np.mean(comforts)) + float(fairness))
                comfs.append(np.mean(comforts))
                fairs.append(fairness)
    return np.mean(Fs), np.mean(comfs), np.mean(fairs)


def evaluate_default(community, weather_seq):
    Fs, comfs, fairs = [], [], []
    for wf in weather_seq:
        community.reset_day()
        for hour in range(24):
            actions = {i: 0.0 for i in range(len(community.houses))}
            comforts, fairness = community.step(hour, actions, wf)
            if hour == 23:
                Fs.append(float(np.mean(comforts)) + float(fairness))
                comfs.append(np.mean(comforts))
                fairs.append(fairness)
    return np.mean(Fs), np.mean(comfs), np.mean(fairs)


# ========== SANITY CHECK (3000 episodes, 1 seed) ==========
def run_sanity(base_dir='results', episodes=3000, seed=42, scenario='mixed',
               objective='personality', homogeneous=False):
    if homogeneous:
        mix = ['neutral'] * 10
    else:
        mix = SCENARIOS[scenario]
    agents, community, history = run_endofday_simulation(
        mix, num_houses=10, episodes=episodes, battery_cap=7.0,
        solar_max=1.3, seed=seed, weather_cloud_prob=0.15,
        objective=objective, verbose=True, neutral=homogeneous)

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
    differentiated = float(np.ptp(hours)) > 0.1
    max_share_hour = int(np.argmax(hours))

    rng = np.random.RandomState(EVAL_SEED)
    weather_seq = [1.0 if rng.random() > 0.15 else 0.5 for _ in range(EVAL_EPISODES)]
    F_g, comf_g, fair_g = evaluate_greedy(agents, community, weather_seq)
    F_d, comf_d, fair_d = evaluate_default(community, weather_seq)

    orig = {}
    pf = os.path.join(base_dir, scenario, 'seed_42', 'final_metrics.csv')
    if os.path.exists(pf):
        with open(pf) as fh:
            orig = next(csv.DictReader(fh))
    ctrl = os.path.join(base_dir, 'control_always_default', 'seed_42', 'final_metrics.csv')
    ctrl_d = {}
    if os.path.exists(ctrl):
        with open(ctrl) as fh:
            ctrl_d = next(csv.DictReader(fh))
    char = {}
    pf2 = os.path.join(base_dir, 'baseline_charbonnier', 'seed_42', 'final_metrics.csv')
    if os.path.exists(pf2):
        with open(pf2) as fh:
            char = next(csv.DictReader(fh))
    char_val = {}
    vf = os.path.join(base_dir, 'baseline_charbonnier_validation',
                      'validation_report.txt')
    if os.path.exists(vf):
        with open(vf) as fh:
            for line in fh:
                line = line.strip()
                if 'Learned greedy policy: F=' in line:
                    parts = line.split('F=')[1].split()
                    char_val['greedy_F'] = float(parts[0])
                if 'F gain over default' in line:
                    char_val['gain'] = float(line.split(':')[-1].strip())
                if 'Realized sharing under greedy policy' in line:
                    char_val['sharing'] = line.split(':', 1)[-1].strip()
                if 'overall realized sharing' in line:
                    char_val['sharing'] = line.split(':', 1)[-1].strip()

    lines = []
    lines.append("=" * 78)
    lines.append(f"OCEAN-MARL END-OF-DAY — SANITY ({scenario}, episodes={episodes}, seed={seed})")
    lines.append(f"OBJECTIVE = {objective}  (2x2 cell: {_cell_label(objective, homogeneous)})")
    lines.append("=" * 78)
    lines.append(f"\nTraining metrics (last {last_n} episodes, exploratory policy):")
    lines.append(f"  comfort:  {comfort:.4f}")
    lines.append(f"  fairness: {fairness:.4f}")
    lines.append(f"  F:        {comfort + fairness:.4f}")
    lines.append(f"  blackout: {blackout*100:.1f}%")
    lines.append(f"  waste:    {waste:.2f} kWh")
    lines.append(f"  mean agent reward (end-of-day marginal): {mean_r:.4f}")

    lines.append(f"\nCounterfactual accounting (hourly agent-steps, whole run):")
    lines.append(f"  computed (real CF):      {history['cf_used']}")
    lines.append(f"  skipped (net<=0 or a=0): {history['cf_skip']}")
    lines.append(f"  skip ratio:              {skip_ratio*100:.1f}%")
    if history['cf_reward_samples']:
        lines.append(f"  mean marginal reward of computed CF: "
                     f"{history['cf_reward_sum']/history['cf_reward_samples']:.4f}")
    lines.append(f"  hours with positive mean marginal: {pos_hours if pos_hours else 'none'}")
    lines.append(f"  hours with negative mean marginal: {neg_hours if neg_hours else 'none'}")

    lines.append(f"\nQ-table policy (avg over {len(agents)} agents x 96 states):")
    lines.append(f"  prefer Share 0% : {dist[0]*100:.1f}%")
    lines.append(f"  prefer Share 50%: {dist[1]*100:.1f}%")
    lines.append(f"  prefer Share 100%: {dist[2]*100:.1f}%")
    lines.append(f"  sharing frequency (any share): {sf*100:.1f}%")
    lines.append(f"  differentiated across hours: {'YES' if differentiated else 'NO'} "
                 f"(range {hours.min()*100:.1f}%..{hours.max()*100:.1f}%)")
    lines.append(f"  hour with max sharing preference: {max_share_hour} ({hours[max_share_hour]*100:.1f}%)")

    lines.append(f"\nFrozen evaluation ({EVAL_EPISODES} matched days, greedy policy):")
    lines.append(f"  Learned greedy (end-of-day): F={F_g:.4f}  comfort={comf_g:.3f}  fairness={fair_g:.3f}")
    lines.append(f"  Always-default (0%)        : F={F_d:.4f}  comfort={comf_d:.3f}  fairness={fair_d:.3f}")
    lines.append(f"  F gain over default        : {F_g - F_d:+.4f}")
    lines.append(f"\n2x2 reference points (seed 42):")
    if orig:
        oF = float(orig['comfort']) + float(orig['fairness'])
        lines.append(f"  A. per-step personality-weighted {scenario}: "
                     f"F={oF:.4f} (comfort {float(orig['comfort']):.4f})")
    lines.append(f"  B. end-of-day personality-weighted (prev sanity): "
                 f"greedy F = default, marginal ~0")
    if char:
        lines.append(f"  C. Charbonnier (community x end-of-day, own learning): "
                     f"training F={float(char['comfort'])+float(char['fairness']):.4f} "
                     f"(comfort {float(char['comfort']):.4f})")
        if char_val.get('greedy_F'):
            lines.append(f"     Charbonnier greedy F={char_val['greedy_F']:.4f} "
                         f"(gain {char_val.get('gain', float('nan')):+.4f}), "
                         f"realized sharing {char_val.get('sharing', 'n/a')}")
    if ctrl_d:
        lines.append(f"     always_default control: "
                     f"F={float(ctrl_d['comfort'])+float(ctrl_d['fairness']):.4f} "
                     f"(comfort {float(ctrl_d['comfort']):.4f})")
    lines.append(f"  D. THIS RUN: community x end-of-day x OCEAN-MARL Q-learning -> "
                 f"training F={comfort + fairness:.4f}, greedy F={F_g:.4f}")

    if history['cf_reward_samples'] and abs(history['cf_reward_sum']) < 1e-9:
        interp = "Marginal reward is structurally ~0 -> no learning signal."
    elif F_g > F_d + 1e-4:
        interp = ("End-of-day signal is informative; greedy policy BEATS always-default. "
                  "With the OCEAN-MARL Q-learning rule this isolates the OBJECTIVE "
                  "(community) as the causal factor, independent of horizon.")
    elif F_g < F_d - 1e-4:
        interp = ("Community objective + OCEAN-MARL Q-learning is WORSE than "
                  "always-default -> Charbonnier's learning rule (hysteretic, low "
                  "alpha) is also load-bearing, not just the objective.")
    else:
        interp = "Learned greedy policy ~ equals always-default."
    lines.append(f"\nInterpretation:")
    lines.append(f"  {interp}")

    print("\n".join(lines))

    save_dir = os.path.join(base_dir,
                            f'ocean_marl_endofday_sanity'
                            f"{'_community' if objective == 'community' else ''}"
                            f"{'_homogeneous' if homogeneous else ''}")
    os.makedirs(save_dir, exist_ok=True)
    save_results(save_dir, history, agents, scenario, seed, episodes, 0.15,
                 objective=objective, personality_mix=mix)
    with open(os.path.join(save_dir, 'sanity_report.txt'), 'w') as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nSanity artifacts saved to {save_dir}")


# ========== MAIN ==========
def main():
    ap = argparse.ArgumentParser(description="OCEAN-MARL with end-of-day "
                                             "counterfactual reward")
    ap.add_argument('--sanity', action='store_true',
                    help='sanity run: mixed, 3000 eps, seed 42 + report')
    ap.add_argument('--objective', choices=['personality', 'community'],
                    default='personality',
                    help="end-of-day objective: 'personality' (w_self*C_i+w_fair*F, "
                         "the main runs' weights) or 'community' (mean_comfort+fairness, "
                         "Charbonnier's role-free F)")
    ap.add_argument('--homogeneous', action='store_true',
                    help='sanity only: all houses identical with role-free neutral '
                         'weights {w_self:1.0, w_fair:0.0} (mirrors Charbonnier env); '
                         'use with --objective community')
    ap.add_argument('--episodes', type=int, default=None,
                    help='episodes (full run default 8000, sanity default 3000)')
    ap.add_argument('--scenarios', nargs='*', default=None,
                    help='scenarios (default: all five main scenarios)')
    ap.add_argument('--seeds', type=int, nargs='*', default=None,
                    help='seeds (default: 42 123 456 789 1011)')
    ap.add_argument('--weather_cloud_prob', type=float, default=0.15)
    ap.add_argument('--base_dir', default='results')
    args = ap.parse_args()

    if args.sanity:
        run_sanity(base_dir=args.base_dir,
                   episodes=args.episodes if args.episodes else 3000,
                   seed=42, scenario='mixed', objective=args.objective,
                   homogeneous=args.homogeneous)
        return

    scenarios = args.scenarios if args.scenarios else list(SCENARIOS.keys())
    seeds = args.seeds if args.seeds else [42, 123, 456, 789, 1011]
    episodes = args.episodes if args.episodes else 8000
    for scenario in scenarios:
        for seed in seeds:
            path = os.path.join(args.base_dir, f'{scenario}_endofday', f'seed_{seed}')
            print(f"\nRunning {scenario}_endofday seed {seed} ({episodes} episodes)...")
            agents, community, history = run_endofday_simulation(
                SCENARIOS[scenario], num_houses=10, episodes=episodes,
                battery_cap=7.0, solar_max=1.3, seed=seed,
                weather_cloud_prob=args.weather_cloud_prob,
                objective=args.objective, verbose=True)
            save_results(path, history, agents, scenario, seed, episodes,
                         args.weather_cloud_prob, objective=args.objective)
            print(f"Saved to {path}")
    print("\nEnd-of-day variant full run complete.")


if __name__ == "__main__":
    main()
