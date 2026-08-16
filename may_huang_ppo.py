import numpy as np
import torch
import torch.nn as nn
from torch.distributions import Categorical
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, json, csv, argparse, time

from offgrid_marl import DEMAND_PROFILES, House, Community

ALG_NAME = 'baseline_may_huang'

# ========== ENVIRONMENT CONSTANTS (identical to main runs) ==========
NUM_HOUSES = 10
BATTERY_CAP = 7.0
SOLAR_MAX = 1.3
WEATHER_CLOUD_PROB = 0.15
ACTIONS = [0.0, 0.5, 1.0]
DEMAND_MAX = 1.2

# ========== PPO HYPERPARAMETERS (May & Huang, adapted) ==========
# Adaptation (documented in config): original has a bi-level price-planner agent
# with a 2-tier learning rate; we reproduce the prosumer-level PPO mechanism
# only (no price mechanism in our environment) -> single tier, lr 3e-4 both.
LR = 3e-4
GAMMA = 0.998
GAE_LAMBDA = 0.98
CLIP_EPS = 0.2
UPDATE_EPOCHS = 4
BATCH_SIZE = 256          # PPO minibatch (scaled from their 4000)
ROLLOUT_SIZE = 2048       # transitions collected before each PPO update
ENTROPY_COEF = 0.01
HIDDEN = 32               # 2-layer MLP width

# Frozen-evaluation settings for the validation sanity check
EVAL_EPISODES = 200
EVAL_SEED = 999


# ========== NETWORK (independent actor-critic per house) ==========
class AgentNet(nn.Module):
    """Shared trunk, actor head -> 3 logits, critic head -> scalar value."""

    def __init__(self, obs_dim, n_actions=3, hidden=HIDDEN):
        super().__init__()
        self.trunk = nn.Sequential(nn.Linear(obs_dim, hidden), nn.Tanh(),
                                   nn.Linear(hidden, hidden), nn.Tanh())
        self.actor_head = nn.Linear(hidden, n_actions)
        self.critic_head = nn.Linear(hidden, 1)

    def features(self, x):
        return self.trunk(x)

    def action_dist(self, x):
        return Categorical(logits=self.actor_head(self.features(x)))

    def value(self, x):
        return self.critic_head(self.features(x)).squeeze(-1)


# ========== WORLD CONSTRUCTION (environment unchanged from main runs) ==========
def build_world(num_houses=10, battery_cap=7.0, solar_max=1.3):
    demand_keys = list(DEMAND_PROFILES.keys())
    neutral = {'w_self': 1.0, 'w_fair': 0.0}
    houses = []
    for i in range(num_houses):
        demand = DEMAND_PROFILES[demand_keys[i % len(demand_keys)]]
        houses.append(House(i, demand, battery_cap, neutral, solar_max))
    sharing_pairs = {i: [(i + 1) % num_houses] for i in range(num_houses)}
    community = Community(houses, sharing_pairs)
    return houses, community


def build_agents(num_houses=10, obs_dim=5, seed=42):
    torch.manual_seed(seed)
    nets = [AgentNet(obs_dim) for _ in range(num_houses)]
    opts = [torch.optim.Adam(n.parameters(), lr=LR) for n in nets]
    return nets, opts


# ========== OBSERVATION ==========
# Per house: (hour/24, battery_frac, demand_norm, solar_norm, community_surplus)
# "community_surplus" = aggregate positive net across houses this hour (the
# minimal public signal, analog of their 3 public components).
def compute_surplus(houses, hour, wf):
    s = 0.0
    for h in houses:
        net = h.get_net(hour, wf)
        if net > 0:
            s += net
    return s / (NUM_HOUSES * SOLAR_MAX)


def make_obs(houses, hour, wf, surplus_norm):
    obs = np.zeros((NUM_HOUSES, 5))
    for i, h in enumerate(houses):
        obs[i] = [hour / 24.0, h.battery / h.battery_cap,
                  h.demand[hour] / DEMAND_MAX,
                  h.solar(hour, wf) / SOLAR_MAX, surplus_norm]
    return obs


# ========== GAE ==========
def compute_gae(rewards, values, dones, gamma=GAMMA, lam=GAE_LAMBDA):
    T = len(rewards)
    returns = np.zeros(T)
    advantages = np.zeros(T)
    gae = 0.0
    for t in reversed(range(T)):
        next_val = 0.0 if dones[t] else values[t + 1]
        delta = rewards[t] + gamma * next_val - values[t]
        gae = delta + gamma * lam * (0.0 if dones[t] else gae)
        advantages[t] = gae
        returns[t] = gae + values[t]
    return returns, advantages


# ========== PPO UPDATE (one agent, its own rollout data) ==========
def ppo_update(net, opt, obs, act, old_logp, returns, adv):
    obs = torch.tensor(obs, dtype=torch.float32)
    act = torch.tensor(act, dtype=torch.long)
    old_logp = torch.tensor(old_logp, dtype=torch.float32)
    returns = torch.tensor(returns, dtype=torch.float32)
    adv = torch.tensor(adv, dtype=torch.float32)
    adv = (adv - adv.mean()) / (adv.std() + 1e-8)

    stats = {'policy_loss': 0.0, 'value_loss': 0.0, 'entropy': 0.0, 'kl': 0.0,
             'n_updates': 0}
    n = len(obs)
    for _ in range(UPDATE_EPOCHS):
        perm = torch.randperm(n)
        for i in range(0, n, BATCH_SIZE):
            idx = perm[i:i + BATCH_SIZE]
            with torch.no_grad():
                old_dist = Categorical(logits=net.actor_head(net.features(obs[idx])))
                old_p = old_dist.log_prob(act[idx])
            dist = net.action_dist(obs[idx])
            new_logp = dist.log_prob(act[idx])
            ratio = torch.exp(new_logp - old_logp[idx])
            surr1 = ratio * adv[idx]
            surr2 = torch.clamp(ratio, 1.0 - CLIP_EPS, 1.0 + CLIP_EPS) * adv[idx]
            policy_loss = -torch.min(surr1, surr2).mean()
            entropy = dist.entropy().mean()
            value = net.value(obs[idx])
            value_loss = (value - returns[idx]).pow(2).mean()
            loss = policy_loss + 0.5 * value_loss - ENTROPY_COEF * entropy

            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(net.parameters(), 0.5)
            opt.step()

            with torch.no_grad():
                kl = (old_p - new_logp).mean().item()
            stats['policy_loss'] += policy_loss.item()
            stats['value_loss'] += value_loss.item()
            stats['entropy'] += entropy.item()
            stats['kl'] += kl
            stats['n_updates'] += 1
    for k in ('policy_loss', 'value_loss', 'entropy', 'kl'):
        stats[k] /= max(1, stats['n_updates'])
    return stats


# ========== SIMULATION LOOP ==========
def run_ppo_simulation(num_houses=10, episodes=8000, battery_cap=7.0,
                       solar_max=1.3, seed=42, weather_cloud_prob=0.15,
                       reward_variant='cf', verbose=True):
    np.random.seed(seed)
    torch.manual_seed(seed)
    houses, community = build_world(num_houses, battery_cap, solar_max)
    nets, opts = build_agents(num_houses, obs_dim=5, seed=seed)

    if verbose:
        sample_solar = sum(houses[0].solar(h, 1.0) for h in range(24))
        avg_demand = np.mean([h.daily_demand for h in houses])
        print(f"Solar gen/day (clear): ~{sample_solar:.1f} kWh, Avg demand: {avg_demand:.1f} kWh")
        print(f"Battery: {battery_cap} kWh (start 50%), independent PPO per house: "
              f"lr={LR}, gamma={GAMMA}, gae_lambda={GAE_LAMBDA}, clip={CLIP_EPS}, "
              f"batch={BATCH_SIZE}, epochs={UPDATE_EPOCHS}, hidden={HIDDEN}\n")

    history = {
        'comfort_mean': [], 'fairness': [], 'blackout_days': [], 'total_waste': [],
        'agent_comforts': [[] for _ in houses],
        'policy_loss': [], 'value_loss': [], 'entropy': [], 'kl': [],
    }

    # per-agent rollout buffers
    buf = {i: {'obs': [], 'act': [], 'logp': [], 'val': [], 'rew': [], 'done': []}
           for i in range(num_houses)}

    def flush_update(i):
        returns, adv = compute_gae(np.array(buf[i]['rew']),
                                   np.array(buf[i]['val']),
                                   np.array(buf[i]['done'], dtype=bool))
        s = ppo_update(nets[i], opts[i], buf[i]['obs'], buf[i]['act'],
                       buf[i]['logp'], returns, adv)
        buf[i] = {'obs': [], 'act': [], 'logp': [], 'val': [], 'rew': [], 'done': []}
        return s

    for ep in range(episodes):
        community.reset_day()
        weather_factor = 1.0 if np.random.random() > weather_cloud_prob else 0.5
        ep_rewards = np.zeros(num_houses)

        ep_obs = [[] for _ in range(num_houses)]
        ep_act = [[] for _ in range(num_houses)]
        ep_logp = [[] for _ in range(num_houses)]
        ep_val = [[] for _ in range(num_houses)]
        ep_rew = [[] for _ in range(num_houses)]

        for hour in range(24):
            surplus = compute_surplus(houses, hour, weather_factor)
            obs = make_obs(houses, hour, weather_factor, surplus)
            done = (hour == 23)

            actions = {}
            act_idx = np.zeros(num_houses, dtype=int)
            logp = np.zeros(num_houses)
            val = np.zeros(num_houses)
            with torch.no_grad():
                for i in range(num_houses):
                    o = torch.tensor(obs[i], dtype=torch.float32)
                    dist = nets[i].action_dist(o)
                    a = dist.sample()
                    actions[i] = ACTIONS[a.item()]
                    act_idx[i] = a.item()
                    logp[i] = dist.log_prob(a).item()
                    val[i] = nets[i].value(o).item()

            prev_waste = sum(h.wasted for h in houses)
            comforts, fairness = community.step(hour, actions, weather_factor)
            step_waste = sum(h.wasted for h in houses) - prev_waste
            for i in range(num_houses):
                if reward_variant == 'cf_waste':
                    r_i = comforts[i] + fairness - step_waste
                else:
                    r_i = comforts[i] + fairness
                ep_rewards[i] += r_i
                ep_obs[i].append(obs[i])
                ep_act[i].append(act_idx[i])
                ep_logp[i].append(logp[i])
                ep_val[i].append(val[i])
                ep_rew[i].append(r_i)

        # end of episode: push to buffers, then update when rollouts fill up
        update_stats = None
        for i in range(num_houses):
            buf[i]['obs'].extend(ep_obs[i])
            buf[i]['act'].extend(ep_act[i])
            buf[i]['logp'].extend(ep_logp[i])
            buf[i]['val'].extend(ep_val[i])
            buf[i]['rew'].extend(ep_rew[i])
            buf[i]['done'].extend([False] * 23 + [True])
            if len(buf[i]['rew']) >= ROLLOUT_SIZE:
                update_stats = flush_update(i)

        ep_comforts = np.array([max(0.0, h.demand_met) for h in houses])
        mean_comfort = np.mean(ep_comforts)
        had_blackout = np.any(ep_comforts < 0.95)
        total_waste = sum(h.wasted for h in houses)

        history['comfort_mean'].append(mean_comfort)
        history['fairness'].append(fairness)
        history['blackout_days'].append(1.0 if had_blackout else 0.0)
        history['total_waste'].append(total_waste)
        for i in range(num_houses):
            history['agent_comforts'][i].append(ep_comforts[i])

        if update_stats is not None:
            history['policy_loss'].append(update_stats['policy_loss'])
            history['value_loss'].append(update_stats['value_loss'])
            history['entropy'].append(update_stats['entropy'])
            history['kl'].append(update_stats['kl'])

        if verbose and (ep + 1) % 2000 == 0:
            print(f"Ep {ep+1:4d}: comfort={mean_comfort:.3f}, fairness={fairness:.3f}, "
                  f"blackout%={np.mean(history['blackout_days'][-2000:])*100:.1f}%, "
                  f"waste={np.mean(history['total_waste'][-2000:]):.2f} kWh, "
                  f"entropy={history['entropy'][-1] if history['entropy'] else float('nan'):.3f}")

    return nets, houses, community, history


# ========== PLOTTING ==========
def plot_learning(history, title, save_path):
    from thesis_plot_style import C, save_fig, style_data_axes, style_legend

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))

    ax = axes[0, 0]
    ax.plot(history['comfort_mean'], label='Mean Comfort', color=C['blue'], lw=2, alpha=0.9)
    ax.plot(history['fairness'], label="Jain's Fairness", color=C['green'], lw=2, alpha=0.9)
    ax.set_xlabel('Episode'); ax.set_ylabel('Score'); ax.set_ylim(0, 1.05)
    ax.set_title('Community Performance', fontweight='bold', fontsize=10)
    leg = ax.legend(loc='lower right'); style_legend(leg); style_data_axes(ax)

    ax = axes[0, 1]
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

    ax = axes[1, 0]
    ax.plot(history['policy_loss'], label='Policy loss', color=C['blue'], lw=2, alpha=0.9)
    ax.plot(history['value_loss'], label='Value loss', color=C['orange'], lw=2, alpha=0.9)
    ax.set_xlabel('PPO update'); ax.set_ylabel('Loss')
    ax.set_title('PPO Losses', fontweight='bold', fontsize=10)
    leg = ax.legend(loc='upper right'); style_legend(leg); style_data_axes(ax)

    ax = axes[1, 1]
    ax.plot(history['entropy'], label='Entropy', color=C['green'], lw=2, alpha=0.9)
    ax.plot(history['kl'], label='KL', color=C['purple'], lw=2, alpha=0.9)
    ax.axhline(np.log(3), color=C['grey'], ls='--', lw=1, label='max ln(3)')
    ax.set_xlabel('PPO update'); ax.set_ylabel('nats')
    ax.set_title('Entropy & KL', fontweight='bold', fontsize=10)
    leg = ax.legend(loc='upper right'); style_legend(leg); style_data_axes(ax)

    fig.suptitle(title, fontsize=13, fontweight='bold')
    fig.tight_layout()
    save_fig(fig, save_path)
    plt.close(fig)


# ========== SAVE RESULTS (same schema as main runs + scenario label) ==========
def save_results(save_path, history, nets, seed, episodes, weather_cloud_prob,
                 battery_cap=7.0, solar_max=1.3, reward_variant='cf',
                 scenario=None):
    os.makedirs(save_path, exist_ok=True)
    scenario = scenario or ALG_NAME
    last_n = min(1000, episodes)
    final_comfort = np.mean(history['comfort_mean'][-last_n:])
    final_fairness = np.mean(history['fairness'][-last_n:])
    final_blackout = np.mean(history['blackout_days'][-last_n:])
    final_waste = np.mean(history['total_waste'][-last_n:])
    overall = np.mean([np.mean(history['agent_comforts'][i][-last_n:])
                       for i in range(len(nets))])
    f_seq = (np.array(history['comfort_mean'][-last_n:]) +
             np.array(history['fairness'][-last_n:]))
    f_end = np.mean(f_seq)

    metrics = {
        'scenario': scenario,
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
        'method': ('independent PPO (IPPO-style) per house; single level only. '
                   'Original May & Huang has a bi-level price-planner agent with '
                   'continuous price action; we reproduce the prosumer-level PPO '
                   'mechanism only - the price-planner is out of scope given no '
                   'price mechanism in our environment (documented adaptation).'),
        'reward': ('r_i,t = comfort_i,t + Jain_fairness_t (raw, GAE credit '
                   'assignment)' if reward_variant == 'cf' else
                   'r_i,t = comfort_i,t + Jain_fairness_t - step_waste_kWh '
                   '(waste-augmented sensitivity variant)'),
        'observation': '[hour/24, battery_frac, demand_norm, solar_norm, '
                       'community_surplus_norm] per house',
        'architecture': '2-layer MLP (32-32, tanh), shared trunk, actor head (3 '
                        'logits) + critic head (value); independent nets per house',
        'lr': LR,
        'gamma': GAMMA,
        'gae_lambda': GAE_LAMBDA,
        'clip_epsilon': CLIP_EPS,
        'update_epochs': UPDATE_EPOCHS,
        'batch_size': BATCH_SIZE,
        'rollout_size': ROLLOUT_SIZE,
        'entropy_coef': ENTROPY_COEF,
        'num_houses': len(nets),
        'episodes': episodes,
        'battery_cap': battery_cap,
        'solar_max': solar_max,
        'weather_cloud_prob': weather_cloud_prob,
        'seed': seed,
    }
    with open(os.path.join(save_path, 'config.json'), 'w') as f:
        json.dump(config, f, indent=2)

    plot_learning(history, f"Baseline May & Huang PPO (seed {seed})",
                  os.path.join(save_path, 'results_plot.png'))


# ========== FROZEN EVALUATION (greedy vs always-default) ==========
def system_reward(comforts, fairness):
    return float(np.mean(comforts)) + float(fairness)


def evaluate_greedy(nets, houses, community, weather_seq):
    Fs, comfs, fairs, wastes = [], [], [], []
    for wf in weather_seq:
        community.reset_day()
        for hour in range(24):
            surplus = compute_surplus(houses, hour, wf)
            obs = make_obs(houses, hour, wf, surplus)
            actions = {}
            with torch.no_grad():
                for i in range(len(houses)):
                    o = torch.tensor(obs[i], dtype=torch.float32)
                    a = nets[i].action_dist(o).logits.argmax().item()
                    net_i = houses[i].get_net(hour, wf)
                    actions[i] = ACTIONS[a] if net_i > 0 else 0.0
            comforts, fairness = community.step(hour, actions, wf)
            if hour == 23:
                Fs.append(system_reward(comforts, fairness))
                comfs.append(np.mean(comforts))
                fairs.append(fairness)
                wastes.append(sum(h.wasted for h in houses))
    return (np.mean(Fs), np.mean(comfs), np.mean(fairs), np.mean(wastes))


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


# ========== VALIDATION / SANITY REPORT ==========
def run_sanity(base_dir='results', episodes=800, seed=42):
    nets, houses, community, history = run_ppo_simulation(
        num_houses=10, episodes=episodes, battery_cap=7.0, solar_max=1.3,
        seed=seed, weather_cloud_prob=0.15, verbose=True)

    lines = []
    lines.append("=" * 72)
    lines.append(f"MAY & HUANG PPO (single-level, independent per house) — "
                 f"SANITY (episodes={episodes}, seed={seed})")
    lines.append("=" * 72)

    n_upd = len(history['policy_loss'])
    lines.append(f"\nTraining diagnostics ({n_upd} PPO updates):")
    if n_upd > 0:
        w = max(1, n_upd // 10)
        for name, series in [('policy loss', history['policy_loss']),
                             ('value loss', history['value_loss']),
                             ('entropy', history['entropy']),
                             ('KL', history['kl'])]:
            head = float(np.mean(series[:w]))
            tail = float(np.mean(series[-w:]))
            trend = "down" if tail < head else ("up" if tail > head + 1e-6 else "flat")
            lines.append(f"  {name:<11} first10%={head:+.4f}  last10%={tail:+.4f}  -> {trend}")
        ent = np.array(history['entropy'])
        ln3 = np.log(3)
        lines.append(f"  entropy: max possible ln(3)={ln3:.3f}; last entropy={ent[-1]:.3f} "
                     f"({ent[-1]/ln3*100:.0f}% of max) - {'sensible' if 0.05 < ent[-1] < 0.95*ln3 else 'CHECK'}")
    else:
        lines.append("  no PPO updates completed in this run (raise episodes)")

    last_n = min(1000, episodes)
    lines.append(f"\nTraining metrics (last {last_n} episodes, stochastic policy):")
    lines.append(f"  comfort: {np.mean(history['comfort_mean'][-last_n:]):.3f}")
    lines.append(f"  fairness:{np.mean(history['fairness'][-last_n:]):.3f}")
    lines.append(f"  blackout: {np.mean(history['blackout_days'][-last_n:])*100:.1f}%")
    lines.append(f"  waste: {np.mean(history['total_waste'][-last_n:]):.2f} kWh")

    rng = np.random.RandomState(EVAL_SEED)
    weather_seq = [1.0 if rng.random() > 0.15 else 0.5 for _ in range(EVAL_EPISODES)]
    F_g, comf_g, fair_g, waste_g = evaluate_greedy(nets, houses, community, weather_seq)
    F_d, comf_d, fair_d = evaluate_default(community, weather_seq)

    lines.append(f"\nFrozen evaluation ({EVAL_EPISODES} matched days, greedy policy):")
    lines.append(f"  Learned greedy: F={F_g:.4f}  comfort={comf_g:.3f}  "
                 f"fairness={fair_g:.3f}  waste={waste_g:.2f} kWh")
    lines.append(f"  Always-default : F={F_d:.4f}  comfort={comf_d:.3f}  fairness={fair_d:.3f}")
    lines.append(f"  F gain over default: {F_g - F_d:+.4f}")
    if F_g > F_d + 1e-4:
        lines.append("  -> learned policy beats always-default.")
    elif F_g < F_d - 1e-4:
        lines.append("  -> learned policy is WORSE than always-default (check reward/obs).")
    else:
        lines.append("  -> learned policy ~ equals always-default (not learning).")

    print("\n".join(lines))

    save_dir = os.path.join(base_dir, 'baseline_may_huang_sanity')
    os.makedirs(save_dir, exist_ok=True)
    save_results(save_dir, history, nets, seed, episodes, 0.15)
    with open(os.path.join(save_dir, 'sanity_report.txt'), 'w') as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nSanity artifacts saved to {save_dir}")


# ========== MAIN ==========
def main():
    ap = argparse.ArgumentParser(description="May & Huang PPO baseline "
                                             "(independent PPO per house)")
    ap.add_argument('--sanity', action='store_true',
                    help='short training pass + report (episodes defaults to 800)')
    ap.add_argument('--episodes', type=int, default=None,
                    help='episodes (full run default 8000, sanity default 800)')
    ap.add_argument('--seeds', type=int, nargs='*', default=None,
                    help='seeds (full run default: 42 123 456 789 1011)')
    ap.add_argument('--weather_cloud_prob', type=float, default=0.15)
    ap.add_argument('--reward', choices=['cf', 'cf_waste'], default='cf',
                    help="reward variant: 'cf' (spec, comfort+fairness) or "
                         "'cf_waste' (sensitivity, comfort+fairness-waste)")
    ap.add_argument('--scenario', default=None,
                    help='scenario label/folder override for save_results '
                         '(default: baseline_may_huang)')
    ap.add_argument('--base_dir', default='results')
    args = ap.parse_args()

    if args.sanity:
        episodes = args.episodes if args.episodes else 800
        run_sanity(base_dir=args.base_dir, episodes=episodes, seed=42)
        return

    seeds = args.seeds if args.seeds else [42, 123, 456, 789, 1011]
    episodes = args.episodes if args.episodes else 8000
    scenario = args.scenario or ALG_NAME
    for seed in seeds:
        path = os.path.join(args.base_dir, scenario, f'seed_{seed}')
        print(f"\nRunning {scenario} seed {seed} ({episodes} episodes, "
              f"reward={args.reward})...")
        nets, houses, community, history = run_ppo_simulation(
            num_houses=10, episodes=episodes, battery_cap=7.0, solar_max=1.3,
            seed=seed, weather_cloud_prob=args.weather_cloud_prob,
            reward_variant=args.reward, verbose=True)
        save_results(path, history, nets, seed, episodes, args.weather_cloud_prob,
                     reward_variant=args.reward, scenario=scenario)
        print(f"Saved to {path}")
    print(f"\nMay & Huang PPO baseline run complete ({scenario}).")


if __name__ == "__main__":
    main()
