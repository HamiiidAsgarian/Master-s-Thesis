import numpy as np
import matplotlib.pyplot as plt
import os, json, csv

# ========== PERSONALITY PROFILES ==========
PERSONALITIES = {
    'pure_selfish':            {'w_self': 1.0, 'w_fair': 0.0},
    'individualist':           {'w_self': 0.8, 'w_fair': 0.2},
    'prosocial':               {'w_self': 0.5, 'w_fair': 0.5},
    'altruistic':              {'w_self': 0.2, 'w_fair': 0.8},
    'high_openness_innovator': {'w_self': 0.5, 'w_fair': 0.5},
}

# ========== DEMAND PROFILES (24h) ==========
DEMAND_PROFILES = {
    'morning':  [0.1,0.1,0.1,0.1,0.2,0.4,0.7,0.9,0.6,0.4,0.3,0.2,
                 0.2,0.2,0.2,0.2,0.3,0.4,0.5,0.6,0.5,0.3,0.2,0.1],
    'evening':  [0.1,0.1,0.1,0.1,0.1,0.1,0.2,0.2,0.3,0.3,0.3,0.4,
                 0.4,0.4,0.4,0.5,0.6,0.8,1.0,1.2,1.0,0.6,0.3,0.2],
    'flat':     [0.35]*24,
    'night_owl':[0.05,0.05,0.05,0.05,0.05,0.05,0.1,0.1,0.2,0.2,0.3,0.3,
                 0.4,0.5,0.6,0.7,0.8,1.0,1.2,1.0,0.8,0.5,0.3,0.1],
}

# ========== ENVIRONMENT ==========
class House:
    def __init__(self, house_id, demand, battery_cap, personality, solar_max=1.3):
        self.id = house_id
        self.demand = np.array(demand)
        self.daily_demand = np.sum(demand)
        self.battery_cap = battery_cap
        self.battery = battery_cap * 0.5
        self.solar_max = solar_max
        self.personality = personality
        self.w_self = personality['w_self']
        self.w_fair = personality['w_fair']
        self.demand_met = 1.0
        self.exported = 0.0
        self.received = 0.0
        self.wasted = 0.0
        self.total_blackout_hours = 0

    def reset_day(self):
        self.battery = self.battery_cap * 0.5
        self.received = 0.0
        self.exported = 0.0
        self.wasted = 0.0
        self.demand_met = 1.0

    def solar(self, hour, weather_factor=1.0):
        if hour < 6 or hour > 18:
            return 0.0
        day_hour = hour - 6
        return max(0.0, self.solar_max * np.sin(np.pi * day_hour / 12.0) * weather_factor)

    def get_net(self, hour, weather_factor=1.0):
        return self.solar(hour, weather_factor) - self.demand[hour]

    def step_energy(self, hour, net, share_fraction=0.0):
        wasted = 0.0
        if net > 0:
            to_share = net * share_fraction
            keep = net - to_share
            free = self.battery_cap - self.battery
            charge = min(keep, free)
            self.battery += charge
            wasted = keep - charge
            self.wasted += wasted
            self.demand_met = 1.0
            return to_share, wasted
        else:
            deficit = -net
            draw = min(deficit, self.battery)
            self.battery -= draw
            unmet = deficit - draw
            if self.demand[hour] > 0:
                self.demand_met = max(0.0, (self.demand[hour] - unmet) / self.demand[hour])
            else:
                self.demand_met = 1.0
            if unmet > 0.01:
                self.total_blackout_hours += 1
            return 0.0, 0.0

    def receive_help(self, amount, hour):
        unmet = (1.0 - self.demand_met) * self.demand[hour] if self.demand_met < 1.0 else 0.0
        reduce = 0.0
        if unmet > 0 and amount > 0:
            reduce = min(unmet, amount)
            self.demand_met = (self.demand_met * self.demand[hour] + reduce) / self.demand[hour]
            amount -= reduce
        free = self.battery_cap - self.battery
        stored = min(amount, free)
        self.battery += stored
        self.received += stored + reduce
        return stored + reduce


class Community:
    def __init__(self, houses, sharing_pairs):
        self.houses = {h.id: h for h in houses}
        self.N = len(houses)
        self.sharing_pairs = sharing_pairs

    def reset_day(self):
        for h in self.houses.values():
            h.reset_day()

    def jain_fairness(self):
        comforts = np.array([max(0.0, h.demand_met) for h in self.houses.values()])
        sum_c = np.sum(comforts)
        sum_sq = np.sum(comforts**2)
        if sum_sq == 0 or self.N == 0:
            return 0.0
        return (sum_c**2) / (self.N * sum_sq)

    def step(self, hour, actions, weather_factor=1.0):
        transfers = {}
        for h_id, house in self.houses.items():
            net = house.get_net(hour, weather_factor)
            frac = actions[h_id] if net > 0 else 0.0
            to_share, _ = house.step_energy(hour, net, share_fraction=frac)
            transfers[h_id] = to_share

        for donor_id, amount in transfers.items():
            if amount <= 0:
                continue
            recipients = self.sharing_pairs.get(donor_id, [])
            if not recipients:
                continue
            per_recipient = amount / len(recipients)
            for rec_id in recipients:
                self.houses[rec_id].receive_help(per_recipient, hour)
                self.houses[donor_id].exported += per_recipient

        comforts = np.array([max(0.0, h.demand_met) for h in self.houses.values()])
        fairness = self.jain_fairness()
        return comforts, fairness


# ========== Q‑LEARNING AGENT ==========
class QLAgent:
    def __init__(self, house_id, personality, state_bins=[0.25, 0.5, 0.75],
                 alpha=0.2, gamma=0.99, eps=1.0, eps_decay=0.999, min_eps=0.01):
        self.id = house_id
        self.w_self = personality['w_self']
        self.w_fair = personality['w_fair']
        self.state_bins = state_bins
        self.num_bat = len(state_bins) + 1
        self.q = np.ones((24, self.num_bat, 3)) * 1.0
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = eps
        self.eps_decay = eps_decay
        self.min_eps = min_eps
        self.actions = [0.0, 0.5, 1.0]

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
        act_idx = np.argmax(self.q[h, b])
        return self.actions[act_idx]

    def update(self, state, action, reward, next_state, done):
        h, b = state
        nh, nb = next_state
        act_idx = self.actions.index(action)
        best_next = np.max(self.q[nh, nb]) if not done else 0.0
        td_target = reward + self.gamma * best_next
        self.q[h, b, act_idx] += self.alpha * (td_target - self.q[h, b, act_idx])

    def decay_epsilon(self):
        self.epsilon = max(self.min_eps, self.epsilon * self.eps_decay)

    def compute_reward(self, own_comfort, community_fairness):
        return self.w_self * own_comfort + self.w_fair * community_fairness


# ========== PLOTTING ==========
def plot_results(history, title="Simulation Results"):
    from thesis_plot_style import C, style_data_axes, style_legend
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    ax = axes[0, 0]
    ax.plot(history['comfort_mean'], label='Mean Comfort', color=C['blue'], lw=2, alpha=0.9)
    ax.plot(history['fairness'], label="Jain's Fairness", color=C['green'], lw=2, alpha=0.9)
    ax.set_xlabel('Episode'); ax.set_ylabel('Score')
    ax.set_title('Community Performance', fontweight='bold', fontsize=11)
    leg = ax.legend(loc='lower right'); style_legend(leg); ax.set_ylim([0, 1.05]); style_data_axes(ax)

    ax = axes[0, 1]
    blackout = np.array(history['blackout_days'])
    window = 500
    if len(blackout) > window:
        rolling = np.convolve(blackout, np.ones(window)/window, mode='valid')
        ax.plot(range(window-1, len(blackout)), rolling, color=C['red'], lw=2)
    else:
        ax.plot(blackout, color=C['red'], lw=2)
    ax.set_xlabel('Episode'); ax.set_ylabel('Frequency')
    ax.set_title(f'Blackout Rate ({window}-ep moving avg)', fontweight='bold', fontsize=11)
    ax.set_ylim([0, 1.05]); style_data_axes(ax)

    ax = axes[1, 0]
    n_agents = len(history['agent_comforts'])
    final_comf = [np.mean(history['agent_comforts'][i][-1000:]) for i in range(n_agents)]
    colors = [C['red'] if i >= n_agents//2 else C['blue'] for i in range(n_agents)]
    ax.bar(range(n_agents), final_comf, color=colors, alpha=0.85, edgecolor=C['grey'], linewidth=0.5)
    ax.set_xlabel('Agent ID'); ax.set_ylabel('Mean Comfort (last 1000 ep)')
    ax.set_title('Final Comfort per Agent', fontweight='bold', fontsize=11)
    ax.set_ylim([0, 1]); style_data_axes(ax)
    from matplotlib.patches import Patch
    leg = ax.legend(handles=[Patch(facecolor=C['blue'], label='Prosocial'),
                             Patch(facecolor=C['red'], label='Selfish')], loc='lower right')
    style_legend(leg)

    ax = axes[1, 1]
    for i in range(n_agents):
        rewards = np.array(history['agent_rewards'][i])
        if len(rewards) > 200:
            smoothed = np.convolve(rewards, np.ones(200)/200, mode='valid')
            label = f"Agent {i} ({'Prosocial' if i<n_agents//2 else 'Selfish'})"
            color = C['blue'] if i < n_agents//2 else C['red']
            ax.plot(smoothed, label=label, color=color, alpha=0.7)
    ax.set_xlabel('Episode'); ax.set_ylabel('Smoothed Reward')
    ax.set_title('Agent Rewards (200‑ep smoothing)', fontweight='bold', fontsize=11)
    leg = ax.legend(fontsize=8); style_legend(leg); style_data_axes(ax)

    fig.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


# ========== SIMULATION RUNNER ==========
def run_simulation(num_houses=10, episodes=8000, battery_cap=7.0, solar_max=1.3,
                   personality_mix=None, seed=42, verbose=True,
                   save_path=None, weather_cloud_prob=0.15):
    if personality_mix is None:
        personality_mix = ['prosocial']*5 + ['pure_selfish']*5

    demand_keys = list(DEMAND_PROFILES.keys())
    house_configs = []
    for i in range(num_houses):
        pers = PERSONALITIES[personality_mix[i]]
        dkey = demand_keys[i % len(demand_keys)]
        demand = DEMAND_PROFILES[dkey]
        house_configs.append({'personality': pers, 'demand': demand})

    np.random.seed(seed)

    houses = []
    agents = []
    for i, cfg in enumerate(house_configs):
        house = House(i, cfg['demand'], battery_cap, cfg['personality'], solar_max)
        houses.append(house)
        pers_name = personality_mix[i]
        if pers_name == 'high_openness_innovator':
            agent = QLAgent(i, cfg['personality'], min_eps=0.05)
        else:
            agent = QLAgent(i, cfg['personality'])
        agents.append(agent)

    sharing_pairs = {i: [(i+1) % num_houses] for i in range(num_houses)}
    community = Community(houses, sharing_pairs)

    if verbose:
        sample_solar = sum([houses[0].solar(h, weather_factor=1.0) for h in range(24)])
        avg_demand = np.mean([h.daily_demand for h in houses])
        print(f"Solar gen/day (clear): ~{sample_solar:.1f} kWh, Avg demand: {avg_demand:.1f} kWh")
        print(f"Battery: {battery_cap} kWh (start 50%)\n")

    history = {
        'comfort_mean': [], 'fairness': [], 'blackout_days': [],
        'total_waste': [],
        'agent_rewards': [[] for _ in agents],
        'agent_comforts': [[] for _ in agents],
    }

    for ep in range(episodes):
        community.reset_day()
        weather_factor = 1.0 if np.random.random() > weather_cloud_prob else 0.5
        ep_rewards = np.zeros(len(agents))

        for hour in range(24):
            states = {}
            nets = {}
            for agent in agents:
                h = community.houses[agent.id]
                bat_frac = h.battery / h.battery_cap
                states[agent.id] = agent.get_state(hour, bat_frac)
                nets[agent.id] = h.get_net(hour, weather_factor)

            actions = {}
            for agent in agents:
                can_share = nets[agent.id] > 0
                actions[agent.id] = agent.select_action(states[agent.id], can_share)

            comforts, fairness = community.step(hour, actions, weather_factor)

            done = (hour == 23)
            for agent in agents:
                h = community.houses[agent.id]
                own_comfort = h.demand_met
                reward = agent.compute_reward(own_comfort, fairness)
                ep_rewards[agent.id] += reward

                if not done:
                    next_bat_frac = h.battery / h.battery_cap
                    next_state = agent.get_state(hour+1, next_bat_frac)
                else:
                    next_state = (0, 0)

                agent.update(states[agent.id], actions[agent.id], reward, next_state, done)

        for agent in agents:
            agent.decay_epsilon()

        ep_comforts = np.array([max(0.0, h.demand_met) for h in houses])
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

        if verbose and (ep+1) % 2000 == 0:
            blackout_pct = np.mean(history['blackout_days'][-2000:]) * 100
            avg_waste = np.mean(history['total_waste'][-2000:])
            print(f"Ep {ep+1:4d}: comfort={mean_comfort:.3f}, fairness={fairness:.3f}, "
                  f"blackout%={blackout_pct:.1f}%, waste={avg_waste:.2f} kWh, eps={agents[0].epsilon:.3f}")

    # ===== SAVE RESULTS =====
    if save_path:
        os.makedirs(save_path, exist_ok=True)
        last_n = 1000
        final_comfort = np.mean(history['comfort_mean'][-last_n:])
        final_fairness = np.mean(history['fairness'][-last_n:])
        final_blackout = np.mean(history['blackout_days'][-last_n:])
        final_waste = np.mean(history['total_waste'][-last_n:])
        
        n_pro = num_houses // 2
        pro_comf = np.mean([np.mean(history['agent_comforts'][i][-last_n:]) for i in range(n_pro)])
        self_comf = np.mean([np.mean(history['agent_comforts'][i][-last_n:]) for i in range(n_pro, num_houses)])

        metrics = {
            'seed': seed,
            'comfort': final_comfort,
            'fairness': final_fairness,
            'blackout_rate': final_blackout,
            'waste': final_waste,
            'prosocial_comfort': pro_comf,
            'selfish_comfort': self_comf
        }
        with open(os.path.join(save_path, 'final_metrics.csv'), 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=metrics.keys())
            writer.writeheader()
            writer.writerow(metrics)

        config = {
            'personality_mix': personality_mix,
            'num_houses': num_houses,
            'episodes': episodes,
            'battery_cap': battery_cap,
            'solar_max': solar_max,
            'seed': seed
        }
        with open(os.path.join(save_path, 'config.json'), 'w') as f:
            json.dump(config, f, indent=2)

        fig = plot_results(history, title=f"Scenario: {personality_mix}")
        fig.savefig(os.path.join(save_path, 'results_plot.png'), dpi=150, bbox_inches='tight')
        plt.close(fig)

    return agents, community, history


# ========== MAIN (for single test run) ==========
if __name__ == "__main__":
    print("=" * 60)
    print("SMART NEIGHBORHOOD ENERGY SHARING MARL SIMULATION")
    print("=" * 60)

    mix = ['prosocial']*5 + ['pure_selfish']*5

    agents, community, history = run_simulation(
        num_houses=10,
        episodes=8000,
        battery_cap=7.0,
        solar_max=1.3,
        personality_mix=mix,
        seed=42,
        save_path='results/mixed/seed_42'  # save this test run
    )

    last_n = 1000
    final_comfort = np.mean(history['comfort_mean'][-last_n:])
    final_fairness = np.mean(history['fairness'][-last_n:])
    final_blackout = np.mean(history['blackout_days'][-last_n:])
    final_waste = np.mean(history['total_waste'][-last_n:])

    print("\n" + "=" * 60)
    print(f"FINAL RESULTS (last {last_n} episodes):")
    print(f"  Mean Comfort:         {final_comfort:.3f}")
    print(f"  Jain's Fairness:      {final_fairness:.3f}")
    print(f"  Blackout Day Rate:    {final_blackout:.1%}")
    print(f"  Avg Daily Waste:      {final_waste:.2f} kWh")

    n_pro = 5
    pro_comf = np.mean([np.mean(history['agent_comforts'][i][-last_n:]) for i in range(n_pro)])
    self_comf = np.mean([np.mean(history['agent_comforts'][i][-last_n:]) for i in range(n_pro, 10)])
    print(f"  Prosocial avg comfort: {pro_comf:.3f}")
    print(f"  Selfish avg comfort:   {self_comf:.3f}")
    print(f"  Difference:            {abs(pro_comf - self_comf):.3f}")
    print("=" * 60)

    plt.show()
    print("\nSimulation complete!")