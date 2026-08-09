import numpy as np, os, json, csv
from offgrid_marl import House, Community, DEMAND_PROFILES, PERSONALITIES, run_simulation

BATTERY_SIZES = [3.5, 5.0, 7.0, 9.0]
SEED = 42
EPISODES = 8000
SOLAR_MAX = 1.3
WEATHER_CLOUD_PROB = 0.15
NUM_HOUSES = 10
MIX = ['prosocial'] * 5 + ['pure_selfish'] * 5
BASE = 'results/battery_sensitivity'


def run_always_default(battery_cap, save_path):
    demand_keys = list(DEMAND_PROFILES.keys())
    house_configs = [{'personality': PERSONALITIES[MIX[i]],
                      'demand': DEMAND_PROFILES[demand_keys[i % len(demand_keys)]]}
                     for i in range(NUM_HOUSES)]
    np.random.seed(SEED)
    houses = [House(i, cfg['demand'], battery_cap, cfg['personality'], SOLAR_MAX)
              for i, cfg in enumerate(house_configs)]
    community = Community(houses, {i: [(i + 1) % NUM_HOUSES] for i in range(NUM_HOUSES)})
    comfort_mean, fairness_l, blackout_days, total_waste = [], [], [], []
    agent_comforts = [[] for _ in houses]
    for ep in range(EPISODES):
        community.reset_day()
        wf = 1.0 if np.random.random() > WEATHER_CLOUD_PROB else 0.5
        fairness = 1.0
        for hour in range(24):
            actions = {h.id: 0.0 for h in houses}
            comforts, fairness = community.step(hour, actions, wf)
        ep_comforts = np.array([max(0.0, h.demand_met) for h in houses])
        comfort_mean.append(np.mean(ep_comforts))
        fairness_l.append(fairness)
        blackout_days.append(1.0 if np.any(ep_comforts < 0.95) else 0.0)
        total_waste.append(sum(h.wasted for h in houses))
        for i in range(len(houses)):
            agent_comforts[i].append(ep_comforts[i])
    last_n = 1000
    metrics = {
        'scenario': 'control_always_default',
        'battery_cap': battery_cap,
        'seed': SEED,
        'comfort': np.mean(comfort_mean[-last_n:]),
        'fairness': np.mean(fairness_l[-last_n:]),
        'blackout_rate': np.mean(blackout_days[-last_n:]),
        'waste': np.mean(total_waste[-last_n:]),
        'prosocial_comfort': np.mean([np.mean(a[-last_n:]) for a in agent_comforts[:NUM_HOUSES // 2]]),
        'selfish_comfort': np.mean([np.mean(a[-last_n:]) for a in agent_comforts[NUM_HOUSES // 2:]]),
    }
    os.makedirs(save_path, exist_ok=True)
    with open(os.path.join(save_path, 'final_metrics.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(metrics.keys()))
        w.writeheader(); w.writerow(metrics)
    json.dump({'scenario': 'control_always_default', 'battery_cap': battery_cap,
               'episodes': EPISODES, 'seed': SEED}, open(os.path.join(save_path, 'config.json'), 'w'), indent=2)
    return metrics


def main():
    os.makedirs(BASE, exist_ok=True)
    print(f"{'batt_kWh':>8} | {'always_default':^44} | {'mixed (Q-learning 8000ep)':^44}")
    print(f"{'':>8} | {'comfort':>7}{'F':>8}{'blackout':>9}{'waste':>7} | "
          f"{'comfort':>7}{'F':>8}{'blackout':>9}{'waste':>7}")
    print('-' * 100)
    rows = []
    for size in BATTERY_SIZES:
        tag = f'batt{size:g}'
        d_path = os.path.join(BASE, tag, 'always_default')
        m_path = os.path.join(BASE, tag, 'mixed')
        d = run_always_default(size, d_path)
        run_simulation(num_houses=NUM_HOUSES, episodes=EPISODES, battery_cap=size,
                       solar_max=SOLAR_MAX, personality_mix=MIX, seed=SEED,
                       verbose=False, save_path=m_path)
        with open(os.path.join(m_path, 'final_metrics.csv')) as f:
            m = next(csv.DictReader(f))
        rows.append((size, d, m))
        print(f"{size:>6.1f}  | {d['comfort']:>7.3f}{d['comfort'] + d['fairness']:>8.3f}"
              f"{d['blackout_rate'] * 100:>8.1f}%{d['waste']:>7.2f} | "
              f"{float(m['comfort']):>7.3f}{float(m['comfort']) + float(m['fairness']):>8.3f}"
              f"{float(m['blackout_rate']) * 100:>8.1f}%{float(m['waste']):>7.2f}")
    out = os.path.join(BASE, 'summary.csv')
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['battery_cap', 'run', 'comfort', 'fairness', 'F',
                    'blackout_rate', 'waste'])
        for size, d, m in rows:
            w.writerow([size, 'always_default', d['comfort'], d['fairness'],
                        d['comfort'] + d['fairness'], d['blackout_rate'], d['waste']])
            w.writerow([size, 'mixed', m['comfort'], m['fairness'],
                        float(m['comfort']) + float(m['fairness']),
                        m['blackout_rate'], m['waste']])
    print(f"\nSaved to {BASE}/")


if __name__ == '__main__':
    main()
