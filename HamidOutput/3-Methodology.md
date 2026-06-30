Methodology### **Chapter Three: Research Methodology (روش اجرای تحقیق)**

#### **3.1 Overview of the Research Framework**
This research proposes a novel **personality-driven Multi-Agent Reinforcement Learning (MARL)** framework to manage energy sharing in a smart neighborhood. Unlike traditional models that treat prosumers as homogeneous rational actors, this methodology integrates behavioral psychology—specifically the **Big Five (OCEAN) model**—into the reward-shaping process of autonomous agents. The framework evaluates how heterogeneous intrinsic preferences for fairness shape emergent community dynamics during energy scarcity.

#### **3.2 Physical Environment and System Modeling**
The simulation environment models an off-grid smart neighborhood micro-grid consisting of **10 houses**. 

*   **Neighborhood Topology:** Houses are arranged in a **ring topology**, where each house can share surplus energy with exactly one designated neighbor. This topology is a deliberate design choice to isolate the social impact of sharing decisions from complex network routing confounds.
*   **Solar Generation Model:** Each house is equipped with a solar panel of **1.3 kW peak capacity** ($G_{max}$). Daily generation follows a half-sine curve over daylight hours (6 AM–6 PM):
    $$G(h) = \max\!\left(0,\; G_{\text{max}} \cdot \sin\!\left(\frac{\pi \cdot (h - 6)}{12}\right) \cdot W\right)$$
    where $h$ is the hour and $W$ is a weather factor. On clear days, total production is approximately **9.9 kWh**.
*   **Residential Demand Profiles:** Four distinct demand patterns (Morning, Evening, Flat, and Night Owl) are distributed across the community to ensure agent heterogeneity. The community-wide average daily demand is **8.8 kWh**.
*   **Battery Energy Storage System (BESS):** Each household possesses a **7.0 kWh battery**, initialized at 50% (3.5 kWh) charge daily. The model assumes an ideal battery with a 100% charge/discharge efficiency to focus on the socio-technical sharing norms.

#### **3.3 Personality-Driven Agent Modeling**
The core innovation of this methodology is the mapping of **OCEAN traits** to agent objective functions.

*   **Reward-Based Personality:** Personality is encoded through two weights in the reward function: $w_{self}$ (personal comfort) and $w_{fair}$ (community fairness).
    $$R_i = w_{\text{self}} \cdot C_i + w_{\text{fair}} \cdot F$$
*   **OCEAN Mapping:** Specific traits are operationalized into MARL parameters. For instance, **High Agreeableness** increases $w_{fair}$, leading to prosocial behavior, while **High Openness** is modeled by a higher exploration floor ($\epsilon_{min} = 0.05$ instead of 0.01), representing "curiosity" or "innovation".

| Simulation Personality | OCEAN Coordinate (High/Low) | $w_{self}$ | $w_{fair}$ |
| :--------------------- | :-------------------------- | :--------- | :--------- |
| **Pure Selfish**       | Very Low Agreeableness      | 1.0        | 0.0        |
| **Individualist**      | Low Agreeableness           | 0.8        | 0.2        |
| **Prosocial**          | Mid-High Agreeableness      | 0.5        | 0.5        |
| **Altruistic**         | High Agreeableness          | 0.2        | 0.8        |
| **Innovator**          | High Openness               | 0.5        | 0.5        |

*(Source:)*

#### **3.4 Multi-Agent Reinforcement Learning Algorithm**
The system utilizes independent **tabular Q-learning agents** to control energy sharing. 

*   **State Space ($S$):** A discrete tuple of (hour of the day, battery level). The battery level is discretized into four bins (25%, 50%, 75%, and 100%) resulting in 96 possible states.
*   **Action Space ($A$):** Agents select from three discrete actions regarding surplus energy:
    1.  **Action 0:** Store all surplus (Selfish).
    2.  **Action 1:** Share half of surplus, store half.
    3.  **Action 2:** Share all surplus (Altruistic).
*   **Optimistic Initialization:** All Q-values are initialized to 1.0, encouraging agents to explore all state-action pairs early in training.

#### **3.5 Performance and Fairness Metrics**
The simulation evaluates results using seven key metrics:
1.  **Mean Community Comfort ($C_{avg}$):** The fraction of total demand met across all houses.
2.  **Jain’s Fairness Index ($F$):** Quantifies equality in comfort distribution.
3.  **Blackout Day Rate:** The percentage of days where a household's comfort falls below 0.95.
4.  **Gini Coefficient:** A secondary inequality metric to validate the fairness of comfort distribution.

#### **3.6 Simulation Logic and Pseudo-code**
The simulation follows a repetitive cycle of interaction, reward computation, and Q-table updates over 8,000 episodes per scenario.

**Algorithm: Personality-Modulated Q-Learning for Energy Sharing**
1.  **Initialize** Q-table $Q(s, a) = 1.0$ for all agents $i \in \{1...10\}$.
2.  **For each episode (Day):**
    *   Set starting battery states and demand profiles.
    *   **For each hour $t \in \{0...23\}$:**
        a. Observe state $s_t = (hour, battery\_level)$.
        b. Select action $a_t$ using $\epsilon$-greedy policy (where $\epsilon$ is determined by Openness).
        c. Calculate surplus/deficit after meeting local demand.
        d. Execute energy sharing with the neighbor based on $a_t$ and the ring topology.
        e. Update battery levels for the next state $s_{t+1}$.
        f. **Compute Reward $R_i$:** Calculate personal comfort $C_i$ and Jain's Index $F$.
        g. **Update Q-table:** 
           $Q(s, a) \leftarrow Q(s, a) + \alpha [R_i + \gamma \max Q(s', a') - Q(s, a)]$.
3.  **End Episode** and reset environment.

This methodology provides a scientifically grounded environment to test the **"Innovator Effect"**—the hypothesis that excessive exploration by a single agent can destabilize the community's cooperative equilibrium.