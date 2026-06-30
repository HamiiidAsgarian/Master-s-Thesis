### **Chapter Two: Literature Review**

#### **2.1 Evolution of Smart Microgrids and the Prosumer Paradigm**

The global energy landscape is undergoing a fundamental shift from centralized power generation toward decentralized systems characterized by distributed energy resources (DERs). In this emerging paradigm, residential households have transitioned from passive consumers into **prosumers** who generate renewable energy through solar photovoltaics (PV), manage local demand, and store energy in battery energy storage systems (BESS). While this decentralization aligns with global decarbonization goals to limit warming to 1.5°C, it introduces significant technical and social challenges in coordinating fragmented resources. Effective energy management in these environments requires balancing local self-sufficiency with the stability of the parent grid.

#### **2.2 Peer-to-Peer (P2P) Trading and Pricing Mechanisms**

Peer-to-peer (P2P) energy trading has been proposed as a "consumer-centric" solution that allows prosumers to share surplus energy directly with neighbors. Current literature classifies P2P markets into three categories: Full P2P, Community-based, and Hybrid models, with the community-based design recognized as the most suitable for residential clusters due to the presence of a central mediator or aggregator.

- **Pricing Strategies:** Internal price formation often relies on the **Supply and Demand Ratio (SDR)**, **Mid-Market Rate (MMR)**, or **Bill Sharing (BS)**.
- **Game Theoretic Frameworks:** Many studies employ non-cooperative game theory, such as **Stackelberg games**, where a central leader sets prices and agents act as followers, or **Nash Bargaining** to distribute benefits. However, these models often rely on "economic rationality," assuming agents possess full knowledge of others' strategies or act with consistent self-interest.

#### **2.3 Multi-Agent Reinforcement Learning (MARL) for Distributed Control**

To overcome the computational intractability of centralized optimization in large-scale grids, **Multi-Agent Reinforcement Learning (MARL)** has become a dominant framework. MARL allows autonomous agents to learn sequential decision-making through trial-and-error interactions within a shared environment, typically modeled as a **Decentralized Partially Observable Markov Decision Process (Dec-POMDP)**.

- **Scalability and Privacy:** Approaches such as **Centralized Training with Decentralized Execution (CTDE)** allow agents to rehearsal coordination in simulation using global state data while executing policies locally based only on private observations.
- **Pathologies of Learning:** A critical challenge in MARL is the **non-stationarity problem**, where the environment appears to change as other agents simultaneously learn and adapt. This often leads to suboptimal equilibria or the **"alter-exploration problem,"** where one agent's exploratory actions destabilize the learning of the entire community.

#### **2.4 Modeling Fairness and Social Dilemmas**

The pursuit of technical efficiency often overlooks the **Tragedy of the Commons**, where individual hoarding of energy leads to community-level failure during scarcity.

- **Fairness Metrics:** Common metrics to assess distributional equity include **Jain’s Fairness Index**, which is scale-invariant and population-independent, and the **Gini Coefficient**, derived from Lorenz curves.
- **Fairness-Aware MARL:** Recent frameworks like **FairMarket-RL** and **Equity-Aware P2P** integrate human-centric assessments using Large Language Models (LLMs) as fairness critics or use **inequity aversion** rewards to penalize agents who earn significantly more or less than their peers. Despite these advancements, most models impose a **uniform, top-down fairness constraint** rather than allowing agents to possess heterogeneous, intrinsic social preferences.

#### **2.5 Personality-Driven Decision Making in AI**

The integration of behavioral psychology into AI agent modeling is a nascent but critical field.

- **The Big Five (OCEAN) Model:** Studies have demonstrated that LLM-based agents can effectively simulate the Big Five personality traits—**Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism**.
- **Psychological Grounding:** Recent research shows that traits like **Openness** significantly impact information acceptance and exploration, while **Agreeableness** correlates with prosocial orientation. However, these psychological mappings have primarily been tested in social simulations (e.g., classrooms) and have not yet been applied to the management of physical resources in a microgrid environment.

#### **2.6 Qualitative Comparison of Related Literature**

| Study                            | Algorithm                 | Environment                | Fairness Mechanism                     | Personality?           | Pros                                            | Cons                                    |
| :------------------------------- | :------------------------ | :------------------------- | :------------------------------------- | :--------------------- | :---------------------------------------------- | :-------------------------------------- |
| **Charbonnier (2022)**           | Distributed IQL           | UK Residential Flexibility | None (Efficiency only)                 | No                     | Highly scalable fixed Q-tables.                 | No focus on distributional justice.     |
| **May & Huang (2023)**           | PPO (2-level inner-outer) | virtual Swedish community  | Income Equality metrics                | No                     | Emergent price elasticity.                      | Assumes economic rationality.           |
| **Behrunani (2023)**             | Bilevel Game Theory       | Smart Energy Hubs          | Cost reduction variance                | No                     | Provably fair price mediation.                  | Requires semi-central coordinator.      |
| **Kusatake (2023)**              | Evolutionary / Multi-obj  | P2P prosumer market        | Standard Deviation of benefits         | No                     | Optimizes supply-demand effectively.            | Computationally slow; not real-time.    |
| **Hughes (2018)**                | A3C (Deep RL)             | Cleanup & Harvest Games    | Inequity Aversion rewards              | No                     | Solves Tragedy of the Commons.                  | Not grounded in Big Five psychology.    |
| **Aloor (2024)**                 | MARL (GNN)                | Multi-agent Navigation     | 1 / Coeff. of Variation                | No                     | Min-max fair task assignment.                   | Focused on navigation, not energy.      |
| **Ma et al. (2025)**             | CAPPO + LLM Workflow      | 99 Florida census tracts   | Carbon allowance signaling             | Indirect (User intent) | Addresses energy poverty.                       | Brittle LLM-RL feedback loops.          |
| **Ren & Xu (2025)** [arxiv:2503] | Generative Agents (LLM)   | Virtual Classroom          | N/A                                    | **Yes (Big Five)**     | Robust trait stability analysis.                | No physical resource management.        |
| **Current Thesis (2026)**        | **OCEAN-MARL (IQL)**      | **10-house Ring Topology** | **Personality-Modulated Jain's Index** | **Yes (Big Five)**     | **Couples OCEAN traits with physical sharing.** | Tabular state space limits granularity. |

#### **2.7 Transition to Gap Analysis**

As established in the **Introduction (Section 1.1)**, the existing literature demonstrates a critical lack of **behavioral realism** in energy MARL models. While the technical foundations for scalable energy management are well-documented (e.g., Charbonnier et al., 2022), the industry continues to treat prosumers as homogeneous rational actors. By bridging the gap between **Five-Factor Theory** and **physical resource management**, this study identifies how individual personality—specifically the tension between **Agreeableness** and **Openness**—shapes the robustness of a decentralized smart neighborhood.
