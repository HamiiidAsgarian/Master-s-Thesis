ACADEMIC_v3_En is our own writingOk.

### **Chapter 3: Research Methodology (روش‌شناسی تحقیق)**

This chapter delineates the systematic procedures, mathematical frameworks, and computational tools used to investigate the impact of personality-driven fairness in smart neighborhood energy sharing. Following the structural requirements of Islamic Azad University, this section provides a reproducible "recipe" for the simulation, grounding every parameter and formula in established literature (azad.pdf; Latest_Professor_Opinion_En.md).

#### **3.1. Research Design and Approach (طرح و روش تحقیق)**

This study is classified as **applied research** (تحقیق کاربردی) and utilizes a **quantitative, experimental approach** via computer simulation. The research objective is to observe emergent social coordination within a **Decentralized Partially Observable Markov Decision Process (Dec-POMDP)** (Sutton & Barto, 2018; Watkins & Dayan, 1992). This approach allows for the isolation of individual personality variables—specifically **Agreeableness** and **Openness**—to measure their effect on community efficiency and distributional equity (Ren & Xu, 2025).

#### **3.2. Data Collection Methods (روش‌های گردآوری داده‌ها)**

Primary data is generated through **simulation logs** from the Multi-Agent Reinforcement Learning (MARL) environment.

- **Primary Data Generation:** The environment utilizes synthetic energy datasets based on real-world residential standards. PV generation is modeled according to the **MCS Standard** (typical UK installation), and battery storage follows common specifications like the **Tesla Powerwall 1** (IEA PVPS, 2021).
- **Reliability and Sampling:** To ensure statistical robustness, data is aggregated from **5 independent random seeds** per scenario, a practice standard in residential MARL studies (Alshehri & Gaunt, 2020). Each simulation run spans **8,000 episodes** (days) to ensure Q-table convergence (ACADEMIC_v3_En).

#### **3.3. Tools and Instruments (ابزارهای تحقیق)**

The research is implemented in **Python 3.x**, utilizing a specialized scientific stack:

- **Numerical Logic:** `NumPy` for battery state-of-charge (SoC) management and energy balance.
- **Data Aggregation:** `Pandas` for cleaning and analyzing longitudinal simulation logs.
- **Statistical Validation:** `SciPy` for conducting **one-way ANOVA** and **independent t-tests** to verify the significance of findings (ACADEMIC_v3_En).
- **Visualization:** `Matplotlib` and `Seaborn` for generating **Q-table heatmaps** to interpret learned sharing norms (Bui et al., 2019).

#### **3.4. Population, Sample, and Sampling Method (جامعه، نمونه و روش نمونه‌گیری)**

The "population" represents all possible configurations of decentralized residential microgrids. This study selects a **sample of 10 households** connected in a **ring topology** to isolate sharing behavior from network routing complexities (Charbonnier et al., 2022). **Stratified sampling** is used to define five distinct community scenarios (All Selfish, All Prosocial, Mixed, Varied Altruism, and Innovator Effect) (ACADEMIC_v3_En).

#### **3.5. System Implementation and Mathematical Basis**

##### **3.5.1. Solar Generation Model**

Residential solar output $G(h)$ follows a half-sine curve during daylight hours (6 AM–6 PM) (Skoplaki & Palyvos, 2009):
$$G(h) = \max\!\left(0,\; G_{\text{max}} \cdot \sin\!\left(\frac{\pi \cdot (h - 6)}{12}\right) \cdot W\right) \qquad \text{(Eq. 3-1)}$$

| Symbol           | Definition                                     | Unit | Source                    |
| :--------------- | :--------------------------------------------- | :--- | :------------------------ |
| $h$              | Hour of the day (0–23)                         | hour | Skoplaki & Palyvos (2009) |
| $G_{\text{max}}$ | Peak solar panel capacity (**1.3 kW**)         | kW   | Charbonnier et al. (2022) |
| $W$              | Weather factor (**1.0** clear, **0.5** cloudy) | —    | Kusatake et al. (2023)    |

##### **3.5.2. Personality-Modulated Reward Function**

The core innovation is the reward $R_i$, weighting self-interest against community equity (ACADEMIC*v3_En):
$$R_i = w*{\text{self}} \cdot C*i + w*{\text{fair}} \cdot F \qquad \text{(Eq. 3-2)}$$

| Symbol            | Definition                           | Unit | Source                             |
| :---------------- | :----------------------------------- | :--- | :--------------------------------- |
| $R_i$             | Total scalar reward for agent $i$    | —    | ACADEMIC_v3_En (2026)              |
| $w_{\text{self}}$ | Weight for personal comfort          | —    | OCEAN mapping                      |
| $C_i$             | Personal comfort level (**Eq. 3-3**) | —    | Alshehri & Gaunt (2020)            |
| $w_{\text{fair}}$ | Weight for community fairness        | —    | Adaptation of Hughes et al. (2018) |
| $F$               | Jain’s Fairness Index (**Eq. 3-4**)  | —    | Jain et al. (1984)                 |

##### **3.5.3. Q-Learning Algorithmic Basis**

Agents update estimates using Independent Q-Learning (IQL):
$$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ R + \gamma \max_{a'} Q(s', a') - Q(s, a) \right] \qquad \text{(Eq. 3-5)}$$

| Symbol   | Definition                    | Unit | Source                                   |
| :------- | :---------------------------- | :--- | :--------------------------------------- |
| $\alpha$ | Learning rate (**0.2**)       | —    | Sutton & Barto (2018)                    |
| $\gamma$ | Discount factor (**0.99**)    | —    | Ali et al. (2023); Sutton & Barto (2018) |
| $s, s'$  | Current and subsequent states | —    | Watkins & Dayan (1992)                   |

#### **3.6. Data Analysis Methods (روش‌های تجزیه و تحلیل داده‌ها)**

The simulation results are evaluated using **Metric-to-Research-Question Mapping** (Table 3-4) to ensure all inquiries are addressed quantitatively (Latest_Professor_Opinion_En.md):

- **Efficiency:** Measured by **Mean Community Comfort ($\bar{C}$)** and **Daily Energy Waste ($W$)**. Prosocial sharing is hypothesized to reduce waste by avoiding hoarding (Zhou & Lund, 2023).
- **Fairness:** Measured by **Jain’s Fairness Index ($F$)** (Jain et al., 1984) and the **Gini Coefficient ($G$)** (Gini, 1912; Kusatake et al., 2023).
- **Robustness:** Assessed through the **Blackout Day Rate ($B$)**, defined as days where $\min C_i < 0.95$ (Ali et al., 2023).
- **Stability:** Investigated via the **"Innovator Effect"**, where a high exploration floor ($\varepsilon_{\min} = 0.05$ vs **0.01**) is tested for its impact on Gini (+22% inequality) (ACADEMIC_v3_En).

**Table 3-3: Physical Ground Truth Parameters**
| Parameter | Value | Source |
| :--- | :--- | :--- |
| Households | **10** | Alshehri & Gaunt (2020) |
| Battery Capacity | **7.0 kWh** | Bui et al. (2019) |
| Cloud Probability | **0.15** | Kusatake et al. (2023) |
| Episodes | **8,000** | Full convergence basis |
