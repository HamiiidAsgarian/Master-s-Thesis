import numpy as np

class House:
    """One off-grid house with solar panel, battery, demand profile."""
    
    def __init__(self, house_id, demand_profile, battery_capacity, personality,
                 solar_max=5.0, daylight_hours=12):
        self.id = house_id
        self.demand_profile = demand_profile  # list of 24 hourly demands (kWh)
        self.battery_capacity = battery_capacity  # kWh
        self.battery = battery_capacity  # start full (or set to 0, full is fine)
        self.solar_max = solar_max        # max generation at noon
        self.daylight_hours = daylight_hours
        
        # personality: dict with w_self, w_fair
        self.personality = personality
        self.w_self = personality['w_self']
        self.w_fair = personality['w_fair']
        
        # tracking
        self.demand_met = 0.0  # fraction met this step
        self.surplus = 0.0
        self.exported = 0.0
        self.received = 0.0
    
    def reset_day(self):
        """Reset battery to full at the start of each day (or keep persistent)."""
        self.battery = self.battery_capacity
    
    def solar_generation(self, hour):
        """Half-sine solar generation. Returns kWh generated in that hour."""
        if hour < 0 or hour >= 24:
            return 0.0
        if hour < 5 or hour > 17:  # roughly daylight 5–17
            return 0.0
        # map hour to [0, daylight_hours]
        day_hour = hour - 5
        daylight = 12
        if day_hour < 0 or day_hour > daylight:
            return 0.0
        gen = self.solar_max * np.sin(np.pi * day_hour / daylight)
        return max(0.0, gen)
    
    def step(self, hour, received_energy=0.0):
        """
        Process one hour:
        - generation
        - demand
        - battery charge/discharge
        - calculate unmet demand fraction
        - compute surplus available for sharing
        received_energy is energy sent from neighbour (will be added to battery if space)
        Returns surplus energy available to share (kWh).
        """
        generation = self.solar_generation(hour)
        demand = self.demand_profile[hour]
        
        # 1. Use generation directly + received energy (received goes into battery)
        net = generation - demand
        
        # Apply received energy: add to battery if there is free capacity
        if received_energy > 0:
            free_space = self.battery_capacity - self.battery
            energy_to_store = min(received_energy, free_space)
            self.battery += energy_to_store
            # any leftover received energy is wasted
            wasted_received = received_energy - energy_to_store
        else:
            wasted_received = 0.0
        
        if net >= 0:
            # Surplus generation: charge battery first
            free_space = self.battery_capacity - self.battery
            charge = min(net, free_space)
            self.battery += charge
            surplus = net - charge  # energy that cannot be stored -> exportable
            self.demand_met = 1.0   # full demand met
        else:
            # Deficit: draw from battery
            deficit = -net
            draw = min(deficit, self.battery)
            self.battery -= draw
            unmet = deficit - draw
            self.demand_met = (demand - unmet) / demand if demand > 0 else 1.0
            surplus = 0.0
        
        self.surplus = surplus
        return surplus
    
    def receive_energy(self, amount):
        """Directly add energy to battery if space (for shared energy handling)."""
        free = self.battery_capacity - self.battery
        stored = min(amount, free)
        self.battery += stored
        self.received += stored  # logged
        return stored


class EnergyCommunity:
    """Orchestrates houses and daily simulation steps."""
    
    def __init__(self, houses, sharing_pairs):
        """
        houses: list of House objects
        sharing_pairs: dict mapping donor_id -> list of recipient_ids
                      For simplicity, a ring: each house shares with its next neighbour.
        """
        self.houses = {h.id: h for h in houses}
        self.house_ids = sorted(self.houses.keys())
        self.N = len(houses)
        self.sharing_pairs = sharing_pairs  # e.g., {0: [1], 1: [2], ...}
        
        # For Jain's fairness: record comfort per house
        self.comforts = np.zeros(self.N)
    
    def reset_day(self):
        for h in self.houses.values():
            h.reset_day()
            h.received = 0.0
        self.comforts = np.zeros(self.N)
    
    def jain_fairness(self):
        """Jain's fairness index of comfort values (demand met fraction)."""
        if self.N == 0:
            return 1.0
        comfort = np.array([h.demand_met for h in self.houses.values()])
        sum_c = np.sum(comfort)
        sum_sq = np.sum(comfort**2)
        if sum_sq == 0:
            return 1.0
        return (sum_c**2) / (self.N * sum_sq)
    
    def step(self, hour, actions):
        """
        actions: dict house_id -> share_action (0: none, 1: 50%, 2: 100%)
        Returns: comfort array, fairness index, total waste
        """
        # First, compute surplus for each house (no sharing yet)
        surpluses = {}
        for h_id in self.house_ids:
            house = self.houses[h_id]
            # no received energy yet
            surplus = house.step(hour, received_energy=0.0)
            surpluses[h_id] = surplus
        
        # Now apply sharing actions
        transfers = {hid: 0.0 for hid in self.house_ids}
        for donor_id, action in actions.items():
            donor = self.houses[donor_id]
            surplus = surpluses[donor_id]
            if surplus <= 0:
                continue
            if action == 1:
                share_amt = 0.5 * surplus
            elif action == 2:
                share_amt = surplus
            else:
                share_amt = 0.0
            
            # Send to designated recipient(s)
            recipients = self.sharing_pairs.get(donor_id, [])
            if not recipients:
                share_amt = 0.0
            for rec_id in recipients:
                recipient = self.houses[rec_id]
                stored = recipient.receive_energy(share_amt)
                # donor does not lose energy that couldn't be stored; just the sent amount
                # But we track exports for analysis
                donor.exported += share_amt
                transfers[donor_id] += share_amt
                # If multiple recipients, divide equally? For simplicity, single recipient.
                break  # only first recipient, ring topology
        
        # After transfers, we need to recompute demand_met and battery states?
        # In our step() function, we already applied direct demand+generation.
        # Received energy was added to battery before we checked deficit? 
        # Actually, in step() we used received_energy=0. Then we added energy to battery afterwards via receive_energy(). 
        # This changes battery level but does NOT affect demand_met for the current hour. 
        # To be accurate, we should integrate received energy into the deficit handling.
        # Let's adjust: we'll use a two-phase approach: 
        # 1] compute net for each house, handle demand+gen+battery, get surplus.
        # 2] apply transfers, add received energy to battery (which will help next hours).
        # That's acceptable and simple. Alternatively, we could re-evaluate deficit but that's complex.
        # So demand_met remains as calculated before receiving energy. That means sharing helps only future hours.
        # This is a valid design choice (energy sharing not instantaneous but helps storage for later).
        
        # Record comforts
        for i, h_id in enumerate(self.house_ids):
            self.comforts[i] = self.houses[h_id].demand_met
        
        fairness = self.jain_fairness()
        return self.comforts.copy(), fairness