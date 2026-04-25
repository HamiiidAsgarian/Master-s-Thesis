import numpy as np
from environment import House, EnergyCommunity
from agent import QLearningAgent

def run_simulation(house_configs, sharing_pairs, num_episodes=10000,
                   battery_capacity=10.0, solar_max=5.0,
                   state_bins=[0.3, 0.7], alpha=0.1, gamma=0.9):
    """
    house_configs: list of dicts with personality, demand_profile.
    Returns: trained agents, metrics history.
    """
    houses = []
    agents = []
    for i, cfg in enumerate(house_configs):
        house = House(i, cfg['demand'], battery_capacity, cfg['personality'],
                      solar_max=solar_max)
        houses.append(house)
        agent = QLearningAgent(i, cfg['personality'], state_bins,
                               alpha=alpha, gamma=gamma)
        agents.append(agent)
    
    community = EnergyCommunity(houses, sharing_pairs)
    
    # Metrics storage
    history = {
        'comfort_mean': [],
        'fairness': [],
        'blackout_frac': [],
        'reward_per_agent': [[] for _ in agents]
    }
    
    for ep in range(num_episodes):
        community.reset_day()
        # Start day at hour 0
        for h in houses:
            h.demand_met = 1.0  # initial full comfort until we step
        hourly_comforts = []
        hourly_fairness = []
        
        for hour in range(24):
            # 1. Determine states
            states = {}
            surpluses = {}
            for agent in agents:
                h = community.houses[agent.id]
                bat_frac = h.battery / h.battery_capacity
                state = agent.discretize_state(hour, bat_frac)
                # surplus will be computed after step; we need to know if surplus exists.
                # But to decide action before step, we approximate: just run a quick solar-demand check?
                # For simplicity, we assume we compute surplus before action as a separate method.
                # Modify environment: we can add a method to estimate surplus without updating battery.
                # Or we can perform step() to calculate surplus, but that changes battery prematurely.
                # Better: pre-compute surplus using a dedicated function that doesn't modify state.
                # I'll add a quick method in House: `potential_surplus(hour)` based on current battery, generation, demand.
                # Let's add that.
                pass
            
            # We'll implement a `get_potential_surplus` in House
            # For now, proceed with actions then step.
        
        # To keep code simple, I rebuild a clean combined loop. See full code below.
    # Return agents, history
    pass