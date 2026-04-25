from offgrid_marl import run_simulation
import os

scenarios = {
    'all_selfish': ['pure_selfish']*6,
    'all_prosocial': ['prosocial']*6,
    'mixed': ['prosocial']*3 + ['pure_selfish']*3,
    'varied_altruism': ['altruistic', 'prosocial', 'prosocial', 'individualist', 'individualist', 'pure_selfish']
}

seeds = [42, 123, 456, 789, 1011]  # 5 seeds

base_dir = 'results'
os.makedirs(base_dir, exist_ok=True)

for scenario_name, mix in scenarios.items():
    for seed in seeds:
        path = os.path.join(base_dir, scenario_name, f'seed_{seed}')
        print(f"\nRunning {scenario_name} seed {seed}...")
        run_simulation(num_houses=6, episodes=8000, battery_cap=7.0, solar_max=1.3,
                       personality_mix=mix, seed=seed, verbose=False,
                       save_path=path)
        print(f"Saved to {path}")