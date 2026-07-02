### **Chapter 1: Introduction and Generalities**

#### **1.1. Introduction and Background**

The global energy landscape is currently undergoing a fundamental transformation, shifting from a century-old paradigm of centralized power generation toward a decentralized model characterized by distributed energy resources (DERs). This transition is a vital prerequisite for limiting anthropogenic global warming to 1.5°C above pre-industrial levels, as outlined in the **IPCC Special Reports** (Masson-Delmotte, 2018). Achieving such ambitious climate targets requires that intermittent renewable power supplies provide the majority of total global electricity by 2050 (Masson-Delmotte, 2018; Parry, 2007).

However, the widespread integration of residential renewables—specifically solar photovoltaics (PV) and battery energy storage systems (BESS)—introduces significant challenges related to intermittency and limited controllability (Charbonnier et al., 2022; Skoplaki & Palyvos, 2009). Consequently, a robust, decarbonized power system must rely on structural features such as decentralization and demand response (DR) (Ali et al., 2023; May & Huang, 2023). In this context, residential households have transitioned from passive consumers into **prosumers** who generate, manage, and store their own energy (Morstyn & McCulloch, 2019; Zhou & Lund, 2023). The coordination of these flexible resources can reduce grid congestion, lower household bills, and promote energy independence (Charbonnier et al., 2022; Tushar et al., 2020).

#### **1.2. Statement of the Problem**

Smart neighborhood micro-grids represent the localized frontier of this decentralization. In these systems, prosumers can share surplus energy directly with neighbors through **Peer-to-Peer (P2P) trading**, which reduces reliance on the utility grid and minimizes transmission losses (May & Huang, 2023; Moret & Pinson, 2019). However, P2P energy sharing introduces a profound **social dilemma**: a household with surplus generation must decide whether to store that energy for its own future security or share it with a neighbor facing a deficit (Kollock, 1998; May & Huang, 2023).

Existing Multi-Agent Reinforcement Learning (MARL) approaches to this problem typically operate under the assumption of **"economic rationality"** (May & Huang, 2023; Moret et al., 2020). These models optimize for collective technical efficiency—maximizing total energy stored or minimizing total community cost (Charbonnier et al., 2022; Kusatake et al., 2023). The fundamental problem with efficiency-only optimization is that it frequently produces **inequitable outcomes** (Jain et al., 1984; Moret & Pinson, 2019). Some households may enjoy full comfort and high battery reserves while their neighbors experience frequent blackouts, even when total community resources are sufficient to meet everyone's needs (Zhou & Lund, 2023). This misalignment can lead to the **"Tragedy of the Commons,"** where individual hoarding results in community-level failure during resource scarcity (Gersani et al., 2001; Ostrom, 1990).

The research gap addressed here is the lack of **psychological realism** in current energy management simulations. While previous studies have used heterogeneous agents (Alshehri & Gaunt, 2020), their behavioral definitions are often arbitrary and not grounded in established personality theory. Furthermore, the social cost of individual exploratory behavior—often necessary for reinforcement learning—has been largely ignored, leaving the community vulnerable to destabilization by unpredictable "innovative" agents (Matignon et al., 2012; Tan, 1997).

#### **1.3. Significance of the Study**

This study bridges the fields of artificial intelligence, power engineering, and behavioral psychology. By integrating the **Big Five (OCEAN) personality model** into a physical resource management system, the research moves toward "human-centric" autonomous systems (Park et al., 2023; Ren & Xu, 2025).

Technically, the research demonstrates how decentralized sharing norms can reduce energy waste by up to 11.5%, improving system efficiency without requiring a centralized coordinator (Zhou & Lund, 2023). Socially, it identifies the mechanism of **emergent reciprocity**, where even selfish agents may discover that sharing is instrumentally beneficial for long-term comfort (Johanson et al., 2022; May & Huang, 2023). Finally, the discovery of the **"Innovator Effect"** provides a critical cautionary insight for AI safety: a single agent that explores too aggressively can destabilize coordination norms, increasing community inequality by 22% (Aloor et al., 2024; Matignon et al., 2012).

#### **1.4. Research Innovation**

The core innovation of this thesis is a **reward-shaping framework** that maps the Big Five personality traits to specific MARL parameters (Binz & Schulz, 2023; Sutton & Barto, 2018). Unlike prior work that imposes uniform, top-down fairness constraints (Moret & Pinson, 2019; Qiu et al., 2021), this study models **intrinsic, heterogeneous fairness preferences**.

- **Agreeableness** is mapped to the weight of community fairness ($w_{\text{fair}}$) in the reward function, allowing for a simulated spectrum from "Pure Selfish" to "Altruistic" agents (Hughes et al., 2018; Ibister & Nass, 2000).
- **Openness to Experience** is mapped to the agent's exploration floor ($\varepsilon_{\min}$), investigating the social impact of curiosity-driven behavior (Park et al., 2023).
- The model uses a **10-house ring topology** to isolate social sharing dynamics from network routing complexities (Charbonnier et al., 2022).

#### **1.5. Research Objectives**

**Primary Objective:** To evaluate how heterogeneous, personality-influenced fairness preferences in a MARL energy-sharing system affect the community’s overall efficiency, fairness, and robustness compared to purely self-interested systems.

**Sub-objectives:**

1.  To develop a reward-shaping framework that maps OCEAN traits to specific objective function weights ($w_{\text{self}}$ vs. $w_{\text{fair}}$) (Hughes et al., 2018; Ren & Xu, 2025).
2.  To analyze the temporal sharing patterns that emerge when agents prioritize community fairness alongside personal comfort (Jain et al., 1984).
3.  To investigate the "Prosocial Advantage"—determining if prosocial agents achieve higher individual comfort through emergent reciprocity (May & Huang, 2023).
4.  To quantify the destabilizing impact of high-Openness "innovator" agents on community coordination and equality (Aloor et al., 2024).

#### **1.6. Research Questions**

**Primary Question:** How do heterogeneous, personality-influenced fairness preferences in a multi-agent reinforcement learning energy-sharing system affect the community's overall efficiency, fairness, and robustness, compared to a community of purely self-interested agents?

**Sub-questions:**

1.  Does embedding fairness norms into reward functions lead to measurably different emergent sharing patterns? (Hughes et al., 2018).
2.  What trade-offs appear between community-wide energy efficiency and distributional fairness? (Kusatake et al., 2023).
3.  Can a mix of a few prosocial agents shift the behavior of selfish agents through emergent reciprocity? (Johanson et al., 2022).
4.  How does a single curiosity-driven (high Openness) agent affect the stability of a mixed community? (Matignon et al., 2012).

#### **1.7. Research Hypotheses**

- **H1:** Communities with prosocial reward weights will exhibit significantly lower energy waste than purely selfish communities due to reduced hoarding (Zhou & Lund, 2023).
- **H2:** Prosocial agents in mixed communities will achieve a higher mean comfort than their selfish neighbors through the stabilization of local supply chains (May & Huang, 2023).
- **H3:** The relative advantage of prosocial reward design will remain consistent even as environmental scarcity increases (Kusatake et al., 2023).
- **H4:** The presence of a single agent with a high exploration floor (the "Innovator") will lead to a collapse of cooperative equilibria, resulting in higher Gini coefficients and blackout rates (Aloor et al., 2024; Matignon et al., 2012).

#### **1.8. Operational Definitions**

- **Prosumer:** A household that both consumes and produces energy (via solar PV), capable of sharing surplus generation with neighbors (Morstyn & McCulloch, 2019; Zhou & Lund, 2023).
- **Multi-Agent Reinforcement Learning (MARL):** A framework where multiple autonomous agents learn policies through trial-and-error interaction (Sutton & Barto, 2018; Tan, 1993).
- **OCEAN (Big Five):** A validated five-factor model of personality used to parameterize reward weights and exploration schedules (Binz & Schulz, 2023; McCrae & Costa, 2003).
- **Innovator Effect:** The destabilization of community coordination caused by a single high-Openness agent whose continued exploration prevents neighbors from forming stable expectations (Aloor et al., 2024; Matignon et al., 2012).
- **Jain's Fairness Index ($F$):** A scale-invariant metric used to quantify distributional equality of comfort across the neighborhood (Jain et al., 1984).
- **Personal Comfort ($C_i$):** The fraction of a household's total daily energy demand that was successfully met (Alshehri & Gaunt, 2020).
- **Energy Waste ($W$):** Surplus energy that could neither be stored in the donor's battery nor shared with a neighbor (May & Huang, 2023).
