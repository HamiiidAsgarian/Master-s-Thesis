### **Chapter Two: Literature Review (مروری بر ادبیات تحقیق و پیشینه تحقیق)**

#### **2.1 Introduction to Smart Microgrids and the Prosumer Paradigm**
The global energy landscape is undergoing a fundamental transition from centralized power plants toward decentralized systems characterized by distributed energy resources (DERs). In this new paradigm, residential households are no longer passive consumers but **prosumers** who generate renewable energy (primarily through solar PV), store it in battery energy storage systems (BESS), and actively manage their consumption. This shift improves grid resilience and aligns with decarbonization goals, yet it necessitates advanced **Energy Management Systems (EMS)** capable of coordinating these fragmented resources at scale. Peer-to-peer (P2P) energy trading has emerged as a key mechanism, allowing prosumers to share surplus energy directly with neighbors to match local demand and reduce reliance on the utility grid.

#### **2.2 P2P Trading Mechanisms and Pricing Models**
Current literature categorizes P2P coordination into two main types: **mediated competition**, where agents maximize individual utility, and **mediated cooperation**, where a social planner or collective function guides agents toward a socially desirable outcome. 
*   **Pricing Strategies:** Common internal pricing models include the **Mid-Market Rate (MMR)**, **Supply and Demand Ratio (SDR)**, and **Bill Sharing (BS)**. 
*   **Game Theoretic Approaches:** Research has utilized non-cooperative Stackelberg games, Nash-type games for fair pricing, and bargaining theory to address conflicts between system reliability and participant profit.
*   **Optimization Frameworks:** Traditional methods like Mixed-Integer Linear Programming (MILP) or Alternating Direction Method of Multipliers (ADMM) are effective for global coordination but often suffer from exponential time complexity and privacy concerns when scaled to thousands of prosumers.

#### **2.3 Multi-Agent Reinforcement Learning (MARL) in Energy Management**
To address the limitations of centralized optimization, MARL has become a dominant framework for distributed control. MARL agents learn sequential decision-making through trial-and-error interactions in a shared environment, typically modeled as a **Decentralized Partially Observable Markov Decision Process (Dec-POMDP)**.
*   **Scalability and Privacy:** Strategies such as **Centralized Training with Decentralized Execution (CTDE)** allow agents to rehearsal coordination in a simulated environment while maintaining privacy during implementation. 
*   **Coordination Challenges:** A fundamental hurdle in MARL is the **non-stationarity problem**, where the environment changes as agents simultaneously learn and explore. Recent advances have introduced **marginal rewards** to isolate an agent's individual contribution to community goals and **factored critics (FACMAC)** to improve training efficiency in dense reward environments.

#### **2.4 Modeling Fairness in Distributed Resource Sharing**
While early studies focused on community-wide efficiency, recent research emphasizes **distributive justice**. 
*   **Fairness Metrics:** Common metrics include **Jain’s Fairness Index**, which measures equality across a population, and the **Gini Coefficient**, used to quantify income or comfort inequality.
*   **Fairness-Aware MARL:** Frameworks like **FairMarket-RL** utilize Large Language Models (LLMs) as real-time fairness critics to evaluate trading episodes through a human-centric lens. Other studies incorporate **inequity aversion** into agent rewards, showing that agents who balance self-interest with a need to minimize reward disparities are more likely to achieve cooperative equilibria. However, these models typically assume either uniform fairness preferences or arbitrary heterogeneity.

#### **2.5 Personality-Driven Decision Making in AI Agents**
The integration of psychological theory into AI decision-making is a nascent but critical field. 
*   **OCEAN Model Grounding:** Recent studies demonstrate that LLM-based agents can effectively simulate the **Big Five (OCEAN) personality traits**—Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism. 
*   **Behavioral Impacts:** Research shows that **Openness to Experience** has the strongest impact on information acceptance and exploration. However, this "curiosity" can lead to high-risk joint actions where unilateral deviations cause steep penalties—a phenomenon that can destabilize coordination in resource-sharing environments. This highlights a critical gap: existing energy simulations lack a principled mapping of psychological traits to physical energy management actions.

#### **2.6 Comparison of Related Literature**

| Author (Year)                    | Method         | Fairness Metric         | Agent Heterogeneity           | Innovation / Pros                    | Research Gap / Cons                           |
| :------------------------------- | :------------- | :---------------------- | :---------------------------- | :----------------------------------- | :-------------------------------------------- |
| **Charbonnier (2022)**           | MARL (CTDE)    | None (Efficiency)       | Generation profiles           | Fixed-size Q-tables for scalability. | No focus on equity or personality.            |
| **May & Huang (2023)**           | MARL (PPO)     | Income Equality         | Demand/Supply profiles        | Emergent price elasticity in P2P.    | Assumes economic rationality only.            |
| **Kusatake (2023)**              | Evolutionary   | Profit Fairness         | Preferences                   | Optimized supply-demand balance.     | Not adaptive to real-time MARL.               |
| **Behrunani (2022)**             | Bilevel Game   | Cost Reduction Variance | Hub types                     | Provably fair price-mediation.       | Requires a semi-central coordinator.          |
| **Jadhav (2024)**                | LLM-RL         | FTB & FBS Scores        | Seller/Buyer                  | Moral reasoning in reward shaping.   | Brittle LLM-dependent feedback loop.          |
| **Aloor (2024)**                 | MARL (GNN)     | Coeff. of Variation     | Priority awareness            | Min-max fair goal assignment.        | Focused on navigation, not energy.            |
| **Hughes (2018)**                | MARL           | Inequity Aversion       | Homogeneous                   | Solves Tragedy of the Commons.       | No grounding in OCEAN psychology.             |
| **Ren & Xu (2025)** [arxiv:2503] | LLM Agents     | N/A                     | OCEAN Traits                  | Maps personality to behavior.        | No physical resource management.              |
| **This Thesis**                  | **OCEAN-MARL** | **Jain's & Gini**       | **Psychological & Technical** | **Personality-modulated rewards.**   | **Addresses the lack of behavioral realism.** |

#### **2.7 Summary of Research Gaps**
Based on the existing literature, several fundamental gaps have been identified:
1.  **Lack of Psychological Grounding:** While studies have introduced "heterogeneous preferences" in energy markets, they fail to ground these definitions in established psychological theory like the **Big Five (OCEAN) model**, resulting in arbitrary agent behavior definitions.
2.  **Top-Down vs. Intrinsic Fairness:** Most current models impose a **uniform, community-wide fairness constraint**. There is a lack of research on how **intrinsic, personality-driven preferences** shape emergent sharing norms when agents are allowed to be selfish or prosocial.
3.  **The Impact of Unpredictable Agents:** While exploration is standard in RL, its social cost in a shared neighborhood is under-researched. The **"Innovator Effect"**—where excessive exploratory behavior (High Openness) destabilizes a cooperative equilibrium—represents a critical oversight in current grid resilience literature.

**This research bridges these gaps** by presenting a reward-shaping framework that maps OCEAN traits to specific weights ($w_{self}$ vs. $w_{fair}$), demonstrating how psychologically-grounded agents manage the "Tragedy of the Commons" during energy scarcity.