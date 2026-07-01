To address the professor's feedback and ensure the document meets the requirements for formal mathematical rigor, the following formal parameter tables have been developed for each core equation in your thesis. These tables replace the previous inline definitions with the required structure: **Symbol, Definition, Unit, and Source**.

### **1. Solar Generation Model**

The solar output for each household is modeled using a half-sine curve during daylight hours.

$$G(h) = \max\!\left(0,\; G_{\text{max}} \cdot \sin\!\left(\frac{\pi \cdot (h - 6)}{12}\right) \cdot W\right)$$

| Symbol           | Definition                                     | Unit | Source                    |
| :--------------- | :--------------------------------------------- | :--- | :------------------------ |
| $h$              | Hour of the day (0–23)                         | hour |                           |
| $G_{\text{max}}$ | Peak solar panel capacity (1.3 kW)             | kW   | Charbonnier et al. (2022) |
| $W$              | Weather factor (1.0 for clear, 0.5 for cloudy) | —    | Kusatake et al. (2023)    |
| $G(h)$           | Instantaneous solar power generation           | kW   | Skoplaki & Palyvos (2009) |

---

### **2. Personality-Driven Reward Function**

The reward function encodes individual agent motivations by weighting self-interest against community equity.

$$R_i = w_{\text{self}} \cdot C_i + w_{\text{fair}} \cdot F$$

| Symbol            | Definition                              | Unit | Source                             |
| :---------------- | :-------------------------------------- | :--- | :--------------------------------- |
| $R_i$             | Total scalar reward for agent $i$       | —    |                                    |
| $w_{\text{self}}$ | Weight assigned to personal comfort     | —    | OCEAN mapping                      |
| $C_i$             | Personal comfort level of agent $i$     | —    |                                    |
| $w_{\text{fair}}$ | Weight assigned to community fairness   | —    | Adaptation of Hughes et al. (2018) |
| $F$               | Jain's Fairness Index for the community | —    | Jain et al. (1984)                 |

---

### **3. Personal Comfort Metric**

Comfort is operationalized as the fraction of a household's requested energy demand that was successfully met.

$$C_i = \frac{\text{demand met}_i}{\text{demand}_i}$$

| Symbol                | Definition                                     | Unit | Source                  |
| :-------------------- | :--------------------------------------------- | :--- | :---------------------- |
| $C_i$                 | Personal comfort (range)                       | —    |                         |
| $\text{demand met}_i$ | Energy supplied via solar, battery, or sharing | kWh  |                         |
| $\text{demand}_i$     | Total electricity requested by the household   | kWh  | Alshehri & Gaunt (2020) |

---

### **4. Jain’s Fairness Index**

This primary fairness metric quantifies the equality of comfort distribution across the neighborhood.

$$F = \frac{\left(\sum_{i=1}^{N} C_i\right)^2}{N \cdot \sum_{i=1}^{N} C_i^2}$$

| Symbol | Definition                             | Unit | Source             |
| :----- | :------------------------------------- | :--- | :----------------- |
| $F$    | Jain's Fairness Index (range [1/N, 1]) | —    | Jain et al. (1984) |
| $N$    | Number of households (10)              | —    |                    |
| $C_i$  | Comfort level of household $i$         | —    |                    |

---

### **5. Q-Learning Update Rule**

Agents update their expected utility estimates based on received rewards and future state potential.

$$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ R + \gamma \max_{a'} Q(s', a') - Q(s, a) \right]$$

| Symbol    | Definition                                         | Unit | Source                 |
| :-------- | :------------------------------------------------- | :--- | :--------------------- |
| $Q(s, a)$ | Action-value estimate for state $s$ and action $a$ | —    | Watkins & Dayan (1992) |
| $\alpha$  | Learning rate (0.2)                                | —    | Sutton & Barto (2018)  |
| $R$       | Instantaneous reward                               | —    |                        |
| $\gamma$  | Discount factor (0.99)                             | —    | Sutton & Barto (2018)  |
| $s, s'$   | Current and subsequent states                      | —    |                        |

---

### **6. Energy Waste Metric**

Efficiency is measured by the amount of surplus energy that could neither be stored nor shared.

$$W = \frac{1}{T} \sum_{t=1}^{T} \sum_{i=1}^{N} \left( \text{exportable surplus}_{i,t} - \text{energy shared}_{i,t} \right)^+$$

| Symbol | Definition                                | Unit    | Source |
| :----- | :---------------------------------------- | :------ | :----- |
| $W$    | Average daily community energy waste      | kWh/day |        |
| $T$    | Total evaluation time steps               | hours   |        |
| $N$    | Total houses (10)                         | —       |        |
| $()^+$ | Positive part operator (rectified linear) | —       |        |

---

### **7. Gini Coefficient**

The Gini coefficient is used as a secondary validator for distributional inequality.

$$G = \frac{2 \sum_{i=1}^{N} i \cdot \bar{C}_{(i)}}{N \sum_{i=1}^{N} \bar{C}_{(i)}} - \frac{N+1}{N}$$

| Symbol          | Definition                               | Unit | Source      |
| :-------------- | :--------------------------------------- | :--- | :---------- |
| $G$             | Gini Coefficient (range)                 | —    | Gini (1912) |
| $\bar{C}_{(i)}$ | Comfort values sorted in ascending order | —    |             |
| $N$             | Number of households (10)                | —    |             |

---

### **8. Sharing Frequency**

This metric measures the learned cooperative propensity by counting sharing states in the final Q-table.

$$S_i = \frac{\left| \{ (s, a) \mid a \in \{1, 2\} \land a = \arg\max_{a'} Q_i(s, a') \} \right|}{|S|}$$

| Symbol | Definition                           | Unit | Source                               |
| :----- | :----------------------------------- | :--- | :----------------------------------- | --- | --- |
| $S_i$  | Agent $i$'s frequency of sharing     | —    |                                      |
| $      | S                                    | $    | Total number of discrete states (96) | —   |     |
| $a$    | Greedy action selected by the policy | —    |                                      |
