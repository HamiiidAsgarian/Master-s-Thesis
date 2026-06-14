from offgrid_marl import run_simulation
import os

# Does one curiosity-driven, slow-converging agent stabilize or destabilize a mixed community's energy sharing system?
scenarios = {
    'all_selfish': ['pure_selfish']*10,
    'all_prosocial': ['prosocial']*10,
    'mixed': ['prosocial']*5 + ['pure_selfish']*5,
    'varied_altruism': ['altruistic', 'prosocial', 'prosocial', 'prosocial', 'individualist', 'individualist', 'individualist', 'pure_selfish', 'pure_selfish', 'pure_selfish'],
    'innovator_effect': ['high_openness_innovator'] + ['prosocial']*4 + ['individualist']*3 + ['pure_selfish']*2
}

seeds = [42, 123, 456, 789, 1011]  # 5 seeds

base_dir = 'results'
os.makedirs(base_dir, exist_ok=True)

for scenario_name, mix in scenarios.items():
    for seed in seeds:
        path = os.path.join(base_dir, scenario_name, f'seed_{seed}')
        print(f"\nRunning {scenario_name} seed {seed}...")
        run_simulation(num_houses=10, episodes=8000, battery_cap=7.0, solar_max=1.3,
                       personality_mix=mix, seed=seed, verbose=False,
                       save_path=path)
        print(f"Saved to {path}")