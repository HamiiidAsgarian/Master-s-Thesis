### **Chapter Four: Data Analysis (تجزیه و تحلیل داده ها)**

#### **4.1 Overview of Experimental Data**
The data analyzed in this chapter is derived from a series of multi-agent reinforcement learning simulations consisting of **10 households** over **5 distinct community scenarios**. To ensure statistical reliability, each scenario was executed using **5 random seeds**, resulting in a total of 25 independent training runs. Each simulation run spanned **8,000 episodes** (simulated days), with performance metrics averaged over a terminal evaluation window of the final 1,000 episodes.

#### **4.2 Community-Level Performance Analysis**
The primary metrics for community health include **Mean Community Comfort**, **Jain’s Fairness Index**, and the **Blackout Day Rate**.

*   **Metric Uniformity:** Quantitative summary data reveals that the baseline scenarios (**All Selfish**, **All Prosocial**, and **Mixed**) perform nearly identically at the community level. All three achieve a mean comfort level of approximately **0.92** and a fairness index of **0.92**. 
*   **Statistical Significance of Scenarios:** A one-way **ANOVA** conducted across all five scenarios yielded a significant result ($F = 3.362, p = 0.0293$). However, post-hoc analysis reveals that this significance is driven exclusively by the **Innovator Effect** scenario, which underperforms all others.
*   **Weather as a Primary Driver:** Blackout rates were consistent at **14.5%** across most scenarios. This uniformity suggests that blackout frequency is primarily determined by external environmental shocks (the 15% cloudy day probability halving solar output) rather than internal sharing norms.

#### **4.3 Efficiency and Energy Waste**
Efficiency is measured by **Energy Waste** (kWh/day), representing surplus energy that could not be stored or shared.
*   **Prosocial Efficiency:** Waste is measurably lower in prosocial-dominated communities. The **All Prosocial** and **Mixed** scenarios waste **4.41 kWh** and **4.34 kWh** respectively, compared to **4.98 kWh** for the **All Selfish** baseline. This represents an **11.5% reduction in waste**, supporting the hypothesis that prosocial reward weights reduce hoarding-induced inefficiency by sharing surplus before batteries reach capacity.

#### **4.4 Distributional Analysis: Prosocial vs. Selfish Comfort**
Within heterogeneous communities, a significant **"Prosocial Advantage"** emerged at the individual agent level.

| Scenario            | Prosocial Comfort | Selfish Comfort | Difference (Gap) | Statistical Significance |
| :------------------ | :---------------- | :-------------- | :--------------- | :----------------------- |
| **Mixed**           | 0.935 ± 0.007     | 0.905 ± 0.010   | **+2.9 pp**      | $t = 8.487, p = 0.0011$  |
| **Varied Altruism** | 0.924 ± 0.009     | 0.904 ± 0.012   | **+2.0 pp**      | $t = 2.834, p = 0.0472$  |

*   **Emergent Reciprocity:** Prosocial agents consistently achieve higher personal comfort than selfish agents in the same community. This is attributed to **indirect reciprocity**: by sharing surplus, prosocial agents stabilize their neighbors' energy levels, which prevents neighborhood-wide blackouts that would eventually cascade back to the donor.

#### **4.5 Inequality Analysis (Gini Coefficient)**
The **Gini Coefficient** is used to quantify the inequality of comfort distribution.
*   **Symmetry in Selfishness:** Counter-intuitively, the **All Selfish** community is highly equal ($G = 0.0796$), ranking second only to the **Mixed** community ($G = 0.0790$). This is because homogeneous agents with identical selfish strategies behave symmetrically, reaching identical comfort levels through shared hoarding behaviors.
*   **Concentrated Inequality:** The **Innovator Effect** scenario produces the highest inequality ($G = 0.0962$), a **22% increase** compared to the Mixed scenario.

#### **4.6 Learned Sharing Behavior (Q-Table Insights)**
Analysis of the learned Q-tables identifies distinct temporal sharing patterns based on agent personality.
*   **Altruistic agents ($w_{fair} = 0.8$)** exhibit a broad sharing window from **8 AM to 6 PM**.
*   **Prosocial agents ($w_{fair} = 0.5$)** learn to share specifically during peak solar generation (**10 AM to 4 PM**), minimizing their personal risk while maximizing community benefit.
*   **Instrumental Sharing:** Even selfish agents in mixed communities learn to share in **13.08% of states**, discovering that small sacrifices during peak hours are instrumentally beneficial for long-term comfort.

#### **4.7 Sensitivity to Resource Scarcity**
A sensitivity analysis was conducted by varying the probability of cloudy days from **15% to 35%**.
*   **Stable Advantage:** While scarcity imposes absolute losses on all agents (approx. 13% loss in comfort), the prosocial comfort advantage remains remarkably stable at **2.5–3.0 percentage points** across all scarcity regimes.
*   **Reliability of Design:** These results indicate that fairness-oriented reward design provides a **reliable benefit** that is not dependent on the abundance of resources.

#### **4.8 Analysis of the "Innovator Effect"**
The most significant finding is the destabilizing impact of high-Openness agents.
*   **Coordination Failure:** The presence of a single agent with a high exploration floor ($\epsilon_{min} = 0.05$) degrades community outcomes: comfort drops by **2%**, inequality increases by **22%**, and the blackout rate rises by **8.3%**.
*   **Destabilizing Mechanism:** The innovator’s curiosity creates **unpredictability** in energy availability, preventing other agents from forming stable coordination expectations and causing the community’s cooperative equilibrium to collapse.