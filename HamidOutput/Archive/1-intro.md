### **Chapter One: Introduction (کلیات تحقیق)**

#### **1.1 Statement of the Problem**
The transition toward decentralized energy systems has introduced **smart neighborhood micro-grids**, where households act as **prosumers** who both consume and generate renewable energy. While this paradigm enhances resilience, it creates a **social dilemma**: prosumers must decide whether to hoard surplus energy for personal battery storage or share it with neighbors facing deficits. Traditional Multi-Agent Reinforcement Learning (MARL) approaches to this problem prioritize **collective efficiency**, such as minimizing total grid costs or maximizing community self-sufficiency. However, an exclusive focus on efficiency often leads to **inequitable outcomes**, where some households enjoy full comfort while others experience frequent blackouts despite sufficient community resources.

Existing research has attempted to integrate fairness through top-down mathematical constraints or uniform community-wide rewards. These models typically assume agents are **economically rational actors** who optimize solely for profit or net loss. **The fundamental gap** addressed by this research is the lack of **psychological realism** in energy management models. Current literature fails to ground agent preferences in established **psychological theory**, such as the **Big Five (OCEAN) model**, to study how intrinsic personality traits—rather than rigid system rules—shape the stability and robustness of a shared neighborhood grid. This research investigates the tension between individual self-interest and collective well-being (the **Tragedy of the Commons**) by modeling agents with heterogeneous, personality-driven fairness preferences.

#### **1.2 Significance of the Study**
This study is significant because it bridges the fields of **energy engineering, artificial intelligence, and behavioral psychology**. By grounding agent motivations in the OCEAN model (Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism), it provides a more nuanced understanding of **human-centric fairness** in autonomous systems. 

From a technical perspective, the research demonstrates how **decentralized sharing norms** can reduce energy waste and improve system robustness without requiring a centralized coordinator or the sharing of private data. Socially, it highlights the **"Rising Tide Lifts All Boats"** effect, where prosocial behavior leads to emergent reciprocity that benefits even selfish participants. Finally, the study identifies critical risks, such as the **"Innovator Effect,"** where excessive unpredictability in a single agent can destabilize the entire community’s welfare—a vital insight for the future deployment of AI-controlled smart grids.

#### **1.3 Research Objectives**
The primary objective of this thesis is to **evaluate how heterogeneous, personality-influenced fairness preferences in a MARL system affect community efficiency, fairness, and robustness**. Specific sub-objectives include:
*   **To develop a reward-shaping framework** that maps the Big Five personality traits to specific weights in an agent's objective function ($w_{self}$ vs. $w_{fair}$).
*   **To analyze the trade-offs** between community-wide energy efficiency (reduced waste) and distributional fairness (Jain's Index).
*   **To investigate the emergence of reciprocity**, determining if a subset of prosocial agents can shift the behavior of purely self-interested agents.
*   **To assess the impact of exploratory behavior** (the Innovator Effect) on the stability of a cooperative energy-sharing equilibrium.

#### **1.4 Research Hypotheses**
*   **H1:** Embedding **Agreeableness-driven fairness weights** into agent rewards will lead to measurably higher distributional equity (lower Gini coefficient) without a significant loss in community-level comfort.
*   **H2:** In mixed communities, **prosocial agents will achieve higher individual comfort** than selfish neighbors due to emergent reciprocity and reduced risk of cascading failures.
*   **H3:** The relative advantage of prosocial reward design will remain **consistent across different levels of resource scarcity** (e.g., varying weather conditions).
*   **H4:** A single agent with **high Openness (the Innovator)** will destabilize the community's sharing norms, leading to increased inequality and a higher blackout rate.

#### **1.5 Operational Definitions**
*   **Prosumer:** A proactive energy consumer equipped with distributed energy resources (DERs) who actively manages consumption, production, and storage.
*   **MARL (Multi-Agent Reinforcement Learning):** A machine learning paradigm where multiple agents learn to act simultaneously through trial-and-error interactions in a shared environment.
*   **OCEAN (Big Five) Model:** A psychological framework that categorizes personality into five dimensions: Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism.
*   **Jain's Fairness Index:** A metric used to quantify the equality of resource distribution (e.g., energy comfort) across a population.
*   **Innovator Effect:** The destabilizing impact caused by an agent with high exploration rates (High Openness), which creates unpredictability that degrades community coordination.
*   **Smart Neighborhood:** A decentralized power subsystem (micro-grid) where households are connected (e.g., in a **ring topology**) to share energy locally.
*   **Personal Comfort ($C_i$):** The fraction of a household's energy demand met by generation or storage; a value below 0.95 constitutes a **blackout day**.