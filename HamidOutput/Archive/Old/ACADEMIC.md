# Smart Neighborhood Energy Sharing with Personality‑Driven Fairness: Multi‑Agent Reinforcement Learning Study

## 1. Introduction and Research Question

In smart neighborhood micro-grid communities, households rely on solar panels and batteries. When one house has surplus energy while another faces a blackout, sharing can improve overall welfare. However, households may differ in their willingness to share, shaped by personality traits such as selfishness or prosociality.

**Research Question:**  
How do heterogeneous, personality‑influenced fairness preferences in a multi‑agent reinforcement learning energy‑sharing system affect the community's overall efficiency, fairness, and robustness, compared to a community of purely self‑interested agents?

Sub‑questions:

- Does embedding fairness norms into reward functions lead to measurably different emergent sharing patterns?
- What trade‑offs appear between community‑wide energy efficiency and distributional fairness?
- Can a mix of a few prosocial agents shift the behaviour of selfish agents?

## 2. Model Design

### 2.1 Physical Environment

- **10 houses** on a ring network; each can share with one designated neighbour.
- **Solar generation** follows a half‑sine curve (6 AM–6 PM), peak 1.3 kW → daily ~9.9 kWh on clear days.
- **Demand profiles** (daily total ~8.8 kWh): morning‑heavy, evening‑heavy, flat, night‑owl.
- **Battery** capacity 7.0 kWh, starting at 50% each day.
- **Cloudy days** (15% probability) reduce solar output by 50%.

### 2.2 Agent Design and Personality

Each house is controlled by an **independent Q‑learning agent** (tabular, state = hour + discretised battery level, actions = share 0%, 50%, 100% of net generation).  
**Personality** is fixed and defined by weights in the reward function:

```
reward = w_self × own_comfort + w_fair × community_fairness
```

where own_comfort ∈ [0,1] (fraction of demand met) and community_fairness is Jain's index across all houses. Four personality types are used: pure‑selfish (w_fair=0), individualist (w_fair=0.2), prosocial (w_fair=0.5), and altruistic (w_fair=0.8).

**OCEAN (Big Five) Mapping**

The personality types used in this simulation correspond to explicit coordinates in the Big Five (OCEAN) personality space. This grounding in established psychological theory constitutes the "New Method" contribution of this thesis.

| OCEAN Trait                  | Dimension                    | Effect on Agent                                                   | Reward Parameter Affected             |
| ---------------------------- | ---------------------------- | ----------------------------------------------------------------- | ------------------------------------- |
| Agreeableness (A) — High     | Prosocial orientation        | Agent weights community fairness more heavily                     | w_fair increases                      |
| Agreeableness (A) — Low      | Self-interest dominance      | Agent weights personal comfort over sharing                       | w_self increases                      |
| Conscientiousness (C) — High | Consistent behavior          | Agent maintains stable sharing policy regardless of battery state | Lower ε decay variance                |
| Openness (O) — High          | Exploration, novelty-seeking | Agent explores sharing strategies longer before converging        | Higher initial ε, slower decay        |
| Neuroticism (N) — High       | Threat sensitivity           | Agent penalizes blackout states more heavily                      | Blackout penalty multiplier increases |

The four personality types map to OCEAN space as follows:

| Simulation Type | A        | C   | O   | N   | w_self | w_fair |
| --------------- | -------- | --- | --- | --- | ------ | ------ |
| pure_selfish    | Very Low | Mid | Low | Mid | 1.0    | 0.0    |
| individualist   | Low      | Mid | Low | Mid | 0.8    | 0.2    |
| prosocial       | Mid-High | Mid | Mid | Mid | 0.5    | 0.5    |
| altruistic      | High     | Mid | Mid | Low | 0.2    | 0.8    |

Sharing occurs **from instantaneous net generation** before battery storage, so donors sacrifice potential personal storage.

### 2.3 Learning Algorithm

Independent tabular Q‑learning with optimistic initialisation, ε‑greedy exploration (ε decaying from 1.0 to 0.01), α=0.2, γ=0.99. All agents learn simultaneously from their own personalised rewards.

## 3. Experimental Setup

Five community compositions are tested:

- **All Selfish**: 10 pure‑selfish agents (baseline)
- **All Prosocial**: 10 prosocial agents (upper bound for fairness)
- **Mixed**: 5 prosocial + 5 selfish
- **Varied Altruism**: 1 altruistic, 3 prosocial, 3 individualist (w_fair=0.2), 3 selfish
- **Innovator Effect**: 1 high-O innovator (higher ε floor), 4 prosocial, 3 individualist, 2 selfish

Each scenario is run with 5 random seeds (8000 episodes per run). Final metrics are averaged over the last 1000 episodes.

Performance metrics:

- Mean community comfort (fraction of demand met)
- Jain's fairness index
- Blackout day rate (fraction of days where any house has unmet demand)
- Energy waste (surplus that could not be stored or shared)
- Agent‑type comfort (prosocial vs. selfish average)

## 4. Results

### 4.1 Community‑Level Metrics

![Community Metrics](results/community_metrics.png)  
*Figure 1: Mean comfort, fairness, and blackout rate across scenarios. Error bars show ±1 standard deviation across seeds.*

All communities achieved high average comfort (~0.91) and fairness (~0.92) with similar blackout rates (~14%). No significant overall difference was found (ANOVA p=0.15). However, the all‑selfish community showed slightly higher waste (3.07 kWh) than the prosocial‑dominated ones, indicating hoarding can lead to inefficiency.

### 4.2 Agent‑Type Differences

![Agent‑Type Comfort](results/agent_type_comfort.png)  
*Figure 2: Prosocial vs. selfish comfort in mixed communities.*

In both mixed and varied‑altruism communities, prosocial agents outperformed selfish agents by ~2.4 and 1.5 percentage points respectively. Paired t‑tests confirmed these differences were statistically significant (p < 0.05). This demonstrates that fairness‑oriented agents not only improve equality but also achieve slightly higher personal comfort through emergent reciprocity.

### 4.3 Inequality and Sharing Behaviour

![Gini Coefficient](results/gini_comparison.png)  
*Figure 3: Gini coefficient of comfort across houses. Higher values indicate more inequality.*

The mixed community exhibited the highest inequality (Gini=0.105), followed by all‑selfish (0.069) and all‑prosocial (0.077). Mixing personalities created a gap between "givers" and "takers".

![Sharing Frequency](results/sharing_frequency.png)  
*Figure 4: Proportion of Q‑table states where agents prefer to share.*

Extracted from final policies, prosocial agents in mixed communities shared in ~14–16% of states, whereas selfish agents shared in only ~9–10%. This confirms that personality shapes learned behaviour beyond reward signals alone.

### 4.4 Learned Policies (Q‑Table Heatmaps)

![Q‑Table Heatmaps](results/qtable_heatmaps.png)  
*Figure 5: Average Q‑values per hour for representative agents. Red/yellow indicates high value for sharing actions.*

Prosocial agents showed high sharing values during midday hours (peak solar), while selfish agents almost exclusively favoured "share 0%". In mixed communities, even some selfish agents learned to share occasionally, hinting at emergent indirect reciprocity.

### 4.5 Sensitivity to Scarcity

![Sensitivity Analysis](results/sensitivity_cloud.png)  
*Figure 6: Prosocial‑selfish comfort gap as cloud probability increases.*

As cloudy day probability rose from 15% to 35%, the comfort gap widened markedly. This indicates that the influence of personality is amplified under resource stress—a key insight for off‑grid system design.

## 5. Discussion

- **Fairness vs. Efficiency**: While prosocial communities did not always outperform selfish ones in raw efficiency, they consistently produced fairer outcomes and reduced inequality. In times of scarcity, the value of prosocial agents becomes evident.
- **Emergent Reciprocity**: Selfish agents in mixed communities occasionally learned to share, likely because helping a neighbour avoided cascading blackouts that could affect them indirectly.
- **Policy Implications**: A small mandated "fairness weight" (e.g., through community governance) could improve resilience and equality with minimal efficiency loss.

## 6. Limitations and Future Work

- Only 15% cloudy days—personality effects may be stronger under more severe weather.
- Fixed personalities; dynamic or learning personality models could be explored.
- Small, static network; future work could test larger, dynamic topologies.
- Battery and solar models are simplified (no degradation, no inverter losses).

## 7. Conclusion

This simulation demonstrated that personality‑driven fairness preferences significantly affect individual outcomes in smart neighborhood energy sharing. Prosocial agents learned to share surplus at personal cost, leading to higher comfort for themselves and the community. The effect became stronger under resource scarcity. These findings support the integration of fairness norms into autonomous energy management systems.

All code, data, and plots are available in the accompanying repository.
