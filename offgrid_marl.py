import numpy as np
import matplotlib.pyplot as plt

# ========== PERSONALITY PROFILES ==========
PERSONALITIES = {
    'pure_selfish':    {'w_self': 1.0, 'w_fair': 0.0},
    'individualist':   {'w_self': 0.8, 'w_fair': 0.2},
    'prosocial':       {'w_self': 0.5, 'w_fair': 0.5},
    'altruistic':      {'w_self': 0.2, 'w_fair': 0.8},
}

# ========== DEMAND PROFILES (24h, daily total ~8.8 kWh) ==========
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
    def __init__(self, house_id, demand, battery_cap, personality, solar_max=1.2):
        self.id = house_id
        self.demand = np.array(demand)
        self.daily_demand = np.sum(demand)
        self.battery_cap = battery_cap
        self.battery = battery_cap * 0.5          # start half‑full
        self.solar_max = solar_max
        self.personality = personality
        self.w_self = personality['w_self']
        self.w_fair = personality['w_fair']
        self.demand_met = 1.0
        self.exported = 0.0
        self.received = 0.0
        self.total_blackout_hours = 0

    def reset_day(self):
        self.battery = self.battery_cap * 0.5
        self.received = 0.0
        self.exported = 0.0
        self.demand_met = 1.0

    def solar(self, hour, weather_factor=1.0):
        if hour < 6 or hour > 18:
            return 0.0
        day_hour = hour - 6
        return max(0.0, self.solar_max * np.sin(np.pi * day_hour / 12.0) * weather_factor)

    def step_own_energy(self, hour, weather_factor=1.0):
        gen = self.solar(hour, weather_factor)
        net = gen - self.demand[hour]
        if net >= 0:
            free = self.battery_cap - self.battery
            charge = min(net, free)
            self.battery += charge
            self.demand_met = 1.0
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

    def battery_available_to_share(self, reserve_fraction=0.1):
        reserve = self.battery_cap * reserve_fraction
        return max(0.0, self.battery - reserve)

    def discharge(self, amount):
        actual = min(amount, self.battery)
        self.battery -= actual
        self.exported += actual
        return actual

    def receive_help(self, amount, hour):
        if self.demand_met >= 1.0:
            free = self.battery_cap - self.battery
            stored = min(amount, free)
            self.battery += stored
            self.received += stored
            return stored
        else:
            unmet = (1.0 - self.demand_met) * self.demand[hour]
            reduce = min(unmet, amount)
            self.demand_met = (self.demand_met * self.demand[hour] + reduce) / self.demand[hour]
            amount -= reduce
            free = self.battery_cap - self.battery
            stored = min(amount, free)
            self.battery += stored
            self.received += stored + reduce
            return stored + reduce


class Community:
    def __init__(self, houses, sharing_pairs, help_packet=1.0):
        self.houses = {h.id: h for h in houses}
        self.N = len(houses)
        self.sharing_pairs = sharing_pairs
        self.help_packet = help_packet

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
        # 1. Own energy balance
        for h_id, house in self.houses.items():
            house.step_own_energy(hour, weather_factor)

        # 2. Costly sharing from battery
        for donor_id, fraction in actions.items():
            if fraction == 0.0:
                continue
            donor = self.houses[donor_id]
            available = donor.battery_available_to_share(reserve_fraction=0.1)  # 10% reserve
            if available <= 0:
                continue
            to_send = min(self.help_packet * fraction, available)
            if to_send == 0:
                continue
            recipients = self.sharing_pairs.get(donor_id, [])
            for rec_id in recipients:
                recipient = self.houses[rec_id]
                sent = donor.discharge(to_send)
                recipient.receive_help(sent, hour)
                break  # one recipient in ring

        comforts = np.array([max(0.0, h.demand_met) for h in self.houses.values()])
        fairness = self.jain_fairness()
        return comforts, fairness


# ========== Q‑LEARNING AGENT ==========
class QLAgent:
    def __init__(self, house_id, personality, state_bins=[0.25, 0.5, 0.75],
                 alpha=0.2, gamma=0.99, eps=1.0, eps_decay=0.9995, min_eps=0.02):
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

    def select_action(self, state, can_help):
        if not can_help:
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


# ========== SIMULATION RUNNER ==========
def run_simulation(num_houses=6, episodes=5000, battery_cap=6.0, solar_max=1.2,
                   personality_mix=None, seed=42, verbose=True):
    if personality_mix is None:
        personality_mix = ['prosocial']*3 + ['pure_selfish']*3

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
        agent = QLAgent(i, cfg['personality'])
        agents.append(agent)

    sharing_pairs = {i: [(i+1) % num_houses] for i in range(num_houses)}
    community = Community(houses, sharing_pairs, help_packet=1.0)

    if verbose:
        sample_solar = sum([houses[0].solar(h, weather_factor=1.0) for h in range(24)])
        avg_demand = np.mean([h.daily_demand for h in houses])
        total_clear = sample_solar + battery_cap * 0.5
        total_cloudy = sample_solar * 0.5 + battery_cap * 0.5
        print(f"Solar gen/day (clear): ~{sample_solar:.1f} kWh, Avg demand: {avg_demand:.1f} kWh")
        print(f"Total energy clear: {total_clear:.1f} kWh, cloudy: {total_cloudy:.1f} kWh")
        print(f"Battery: {battery_cap} kWh (start 50%)\n")

    history = {
        'comfort_mean': [], 'fairness': [], 'blackout_days': [],
        'agent_rewards': [[] for _ in agents],
        'agent_comforts': [[] for _ in agents],
    }

    for ep in range(episodes):
        community.reset_day()
        weather_factor = 1.0 if np.random.random() > 0.2 else 0.5
        ep_rewards = np.zeros(len(agents))

        for hour in range(24):
            states = {}
            can_help_flags = {}
            for agent in agents:
                h = community.houses[agent.id]
                bat_frac = h.battery / h.battery_cap
                states[agent.id] = agent.get_state(hour, bat_frac)
                can_help_flags[agent.id] = h.battery_available_to_share(0.1) > 0.01

            actions = {}
            for agent in agents:
                act = agent.select_action(states[agent.id], can_help_flags[agent.id])
                actions[agent.id] = act

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

        history['comfort_mean'].append(mean_comfort)
        history['fairness'].append(fairness)
        history['blackout_days'].append(1.0 if had_blackout else 0.0)
        for i in range(len(agents)):
            history['agent_rewards'][i].append(ep_rewards[i])
            history['agent_comforts'][i].append(ep_comforts[i])

        if verbose and (ep+1) % 1000 == 0:
            blackout_pct = np.mean(history['blackout_days'][-1000:]) * 100
            print(f"Ep {ep+1:4d}: comfort={mean_comfort:.3f}, fairness={fairness:.3f}, "
                  f"blackout%={blackout_pct:.1f}%, eps={agents[0].epsilon:.3f}")

    return agents, community, history


# ========== PLOTTING ==========
def plot_results(history, title="Simulation Results"):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    ax = axes[0, 0]
    ax.plot(history['comfort_mean'], label='Mean Comfort', alpha=0.8)
    ax.plot(history['fairness'], label="Jain's Fairness", alpha=0.8)
    ax.set_xlabel('Episode'); ax.set_ylabel('Score')
    ax.set_title('Community Performance'); ax.legend(); ax.set_ylim([0,1.05]); ax.grid(alpha=0.3)

    ax = axes[0, 1]
    blackout = np.array(history['blackout_days'])
    window = 200
    if len(blackout) > window:
        rolling = np.convolve(blackout, np.ones(window)/window, mode='valid')
        ax.plot(range(window-1, len(blackout)), rolling, color='red')
    else:
        ax.plot(blackout, color='red')
    ax.set_xlabel('Episode'); ax.set_ylabel('Frequency')
    ax.set_title(f'Blackout Rate ({window}-ep moving avg)'); ax.set_ylim([0,1.05]); ax.grid(alpha=0.3)

    ax = axes[1, 0]
    n_agents = len(history['agent_comforts'])
    final_comf = [np.mean(history['agent_comforts'][i][-500:]) for i in range(n_agents)]
    colors = ['coral' if i >= n_agents//2 else 'skyblue' for i in range(n_agents)]
    ax.bar(range(n_agents), final_comf, color=colors)
    ax.set_xlabel('Agent ID'); ax.set_ylabel('Mean Comfort (last 500 ep)')
    ax.set_title('Final Comfort per Agent'); ax.set_ylim([0,1]); ax.grid(axis='y', alpha=0.3)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(facecolor='skyblue', label='Prosocial'),
                       Patch(facecolor='coral', label='Selfish')])

    ax = axes[1, 1]
    for i in range(n_agents):
        rewards = np.array(history['agent_rewards'][i])
        if len(rewards) > 100:
            smoothed = np.convolve(rewards, np.ones(100)/100, mode='valid')
            label = f"Agent {i} ({'Prosocial' if i<n_agents//2 else 'Selfish'})"
            ax.plot(smoothed, label=label, alpha=0.7)
    ax.set_xlabel('Episode'); ax.set_ylabel('Smoothed Reward')
    ax.set_title('Agent Rewards (100‑ep smoothing)'); ax.legend(fontsize=8); ax.grid(alpha=0.3)

    fig.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


# ========== MAIN ==========
if __name__ == "__main__":
    print("=" * 60)
    print("OFF-GRID ENERGY SHARING MARL SIMULATION")
    print("=" * 60)

    mix = ['prosocial', 'prosocial', 'prosocial',
           'pure_selfish', 'pure_selfish', 'pure_selfish']

    agents, community, history = run_simulation(
        num_houses=6,
        episodes=5000,
        battery_cap=6.0,      # larger battery to make the system solvable
        solar_max=1.2,        # 1.2 kW → ~9.2 kWh/day
        personality_mix=mix,
        seed=42
    )

    last_n = 500
    final_comfort = np.mean(history['comfort_mean'][-last_n:])
    final_fairness = np.mean(history['fairness'][-last_n:])
    final_blackout = np.mean(history['blackout_days'][-last_n:])

    print("\n" + "=" * 60)
    print(f"FINAL RESULTS (last {last_n} episodes):")
    print(f"  Mean Comfort:         {final_comfort:.3f}")
    print(f"  Jain's Fairness:      {final_fairness:.3f}")
    print(f"  Blackout Day Rate:    {final_blackout:.1%}")

    n_pro = 3
    pro_comf = np.mean([np.mean(history['agent_comforts'][i][-last_n:]) for i in range(n_pro)])
    self_comf = np.mean([np.mean(history['agent_comforts'][i][-last_n:]) for i in range(n_pro, 6)])
    print(f"  Prosocial avg comfort: {pro_comf:.3f}")
    print(f"  Selfish avg comfort:   {self_comf:.3f}")
    print(f"  Difference:            {abs(pro_comf - self_comf):.3f}")
    print("=" * 60)

    fig = plot_results(history, title="Mixed Community – Costly Battery Sharing (6 kWh battery)")
    plt.show()
    print("\nSimulation complete!")