import numpy as np

class QLearningAgent:
    def __init__(self, house_id, personality, state_bins, num_actions=3,
                 alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.9995, min_epsilon=0.01):
        self.id = house_id
        self.w_self = personality['w_self']
        self.w_fair = personality['w_fair']
        
        # State discretisation: e.g., hour (0-23), own battery low/med/high
        self.state_bins = state_bins  # tuple of bin edges for battery (list of bins)
        # We'll define state space sizes
        self.num_hours = 24
        self.num_battery_levels = len(state_bins) + 1  # for discretisation
        self.num_actions = num_actions
        
        # Q-table: shape (num_hours, num_battery_levels, num_actions)
        self.q_table = np.zeros((self.num_hours, self.num_battery_levels, num_actions))
        
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
    
    def discretize_state(self, hour, battery_level):
        """Convert continuous battery (kWh) to discrete bin index."""
        # battery_level is in kWh, we compare to capacity
        # state_bins are fractions or absolute thresholds? Let's define as percentages of capacity
        # For now we'll pass the fraction (battery/capacity) and discretise.
        bat_frac = battery_level  # expecting fraction 0..1
        for idx, threshold in enumerate(self.state_bins):
            if bat_frac <= threshold:
                bat_idx = idx
                break
        else:
            bat_idx = len(self.state_bins)
        return (int(hour), bat_idx)
    
    def select_action(self, state_tuple, surplus_exists):
        """Epsilon-greedy action selection. If no surplus, action 0 (none) forced."""
        if not surplus_exists:
            return 0
        if np.random.random() < self.epsilon:
            return np.random.randint(self.num_actions)
        else:
            hour, bat_idx = state_tuple
            return np.argmax(self.q_table[hour, bat_idx, :])
    
    def update(self, state, action, reward, next_state, done):
        hour, bat_idx = state
        next_hour, next_bat = next_state
        current_q = self.q_table[hour, bat_idx, action]
        max_next = np.max(self.q_table[next_hour, next_bat, :]) if not done else 0.0
        td_target = reward + self.gamma * max_next
        self.q_table[hour, bat_idx, action] += self.alpha * (td_target - current_q)
    
    def decay_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
    
    def compute_reward(self, own_comfort, community_fairness):
        return self.w_self * own_comfort + self.w_fair * community_fairness