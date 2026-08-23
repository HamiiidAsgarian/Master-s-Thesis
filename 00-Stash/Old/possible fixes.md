Following the professor's feedback and drawing from the foundational sources, here are the detailed fixes for your master's thesis.

### **Fix 1: Strengthening the Introduction**
**Innovation Statement Upgrade:**
The primary innovation of this study is the integration of **behavioral psychology—specifically the Big Five (OCEAN) model**—with technical **Energy Management Systems (EMS)** controlled by MARL. While previous fairness-aware MARL frameworks for energy sharing have used top-down mathematical constraints or uniform community rewards, this work models **intrinsic, heterogeneous fairness preferences** at the individual agent level. This allows for the investigation of emergent social dynamics, such as the **"Innovator Effect,"** where individual exploration parameters (mapping to Openness) significantly impact community-wide resilience.

**Equation Citations:**
*   **Reward Function:** The personality-weighted objective $R_i = w_{\text{self}} \cdot C_i + w_{\text{fair}} \cdot F$ adapts the concept of **inequity aversion** rewards and **marginal utility** of sharing.
*   **Solar Model:** The sine-wave generation model follows standard irradiance modeling practices used for simulating building clusters.

---

### **Fix Section 2: Model Design (Citations & Parameters)**
To address the professor’s request for "ground truth" and sourcing:

| Component            | Description                | Equation / Value                                                      | Source / Scientific Basis                          |
| :------------------- | :------------------------- | :-------------------------------------------------------------------- | :------------------------------------------------- |
| **Solar Generation** | Daily half-sine curve      | $G(h) = \max(0, G_{max} \cdot \sin(\frac{\pi(h-6)}{12}) \cdot W)$     | **Skoplaki & Palyvos (2009)**; **ISO 13790**       |
| **Grid Cost**        | Time-dependent coefficient | $C_{tg} = P_{\text{grid}} + (\text{Carbon} \cdot \text{Social Cost})$ | **Charbonnier et al. (2022)**                      |
| **Battery Level**    | Energy Balance             | $E^{t+1}_i = E^t_i + b^{in}_i - b^{out}_i - d^{EV}_i$                 | **May & Huang (2023)**; **1.pdf**                  |
| **Peak Solar**       | $G_{max} = 1.3$ kW         | Capacity per household                                                | Standard residential PV sizing for UK/EU regions.  |
| **Battery Cap.**     | $E_{max} = 7.0$ kWh        | Residential Storage                                                   | Standard residential BESS used for P2P simulation. |

---

### **Fix Section 3: Experimental Setup (Metrics & Prose)**
The professor asked for prose + formulas for metrics:

1.  **Personal Comfort ($C_i$):** Defined as the ratio of demand met to demand requested. $C_i = \frac{\text{demand\_met}_i}{\text{demand}_i}$. This metric is critical for assessing individual welfare and identifying partial blackouts ($C_i < 0.95$).
2.  **Jain's Fairness Index ($F$):** A continuous, scale-invariant metric used to quantify distributional equality across all agents.
    $$F = \frac{\left(\sum_{i=1}^{N} C_i\right)^2}{N \cdot \sum_{i=1}^{N} C_i^2}$$
    *(Cite: Jain et al., 1984)*
3.  **Gini Coefficient ($G$):** An alternative measure of inequality used to validate the Lorenz curves of benefit distribution.
    $$G = \frac{\sum_{i=1}^{N} \sum_{j=1}^{N} |C_i - C_j|}{2N^2 \cdot \bar{C}}$$
    *(Cite: Ren & Xu, 2025)*
4.  **Hyperparameters:** $\alpha = 0.2$, $\gamma = 0.99$. These standard Q-learning parameters are based on the foundational texts by **Sutton & Barto (2018)**.

---

### **Fix Section 4: Results (SOTA Comparison & Neutral Analysis)**
**SOTA Comparison:**
Compared to the "economically rational" agents in **May & Huang (2023)**, who focus solely on community net loss, our prosocial agents achieve a **2.9 percentage point higher comfort** in mixed communities. This demonstrates that personality-modulated rewards can outperform pure profit maximization by fostering emergent reciprocity.

**Neutral Overall Analysis (Subsection 4.9):**
"The OCEAN-MARL framework successfully identified that while prosocial reward weighting improves efficiency (reducing waste by 11.5%), it does not significantly decrease the community-level blackout rate, which remains largely dictated by external weather shocks. The system's performance was optimal in the Mixed scenario but degraded noticeably in the presence of an 'Innovator' agent. This suggests that while intrinsic fairness is technically beneficial, coordination is highly sensitive to agent unpredictability."

---

### **Fix Section 6: Limitations (Scientific Paragraphs)**
*   **Weather Dynamics:** The current binaryClear/Cloudy weather model is a simplification. Real-world solar generation is subject to stochastic, temporal correlations (e.g., Markov-chain weather patterns), which could further stress sharing norms.
*   **Static Personalities:** This study utilizes fixed OCEAN coordinates for each agent. In real-world neighborhoods, personality traits can be dynamic; agents may exhibit **behavioral spillover** or decrease sharing (becoming less Agreeable) if they experience repeated exploitation.

---

### **Fix Section 7: Conclusion (Deepened Structure)**
1.  **Summary of Problem:** Smart grids face a Tragedy of the Commons where hoarding prevents community-level resilience.
2.  **Proposed Method:** We introduced OCEAN-grounded reward shaping ($w_{self}$ vs $w_{fair}$) to model human-centric fairness.
3.  **Synthesis of Findings:** Prosocial agents achieve higher comfort (+2.9%) via reciprocity, and sharing reduces system waste by 11.5%.
4.  **The Analysis:** The "Innovator Effect" reveals that predictability is the foundation of cooperation; excessive curiosity (High Openness) destabilizes the grid (+22% inequality).
5.  **Future Works:** Focus on larger network scales (50+ homes) and the integration of **LLM-based fairness critics** to move beyond static Q-tables.

---

### **Fix Section 8: Missing References**
Add the following to your reference list:
*   **Jain, R., et al. (1984).** A quantitative measure of fairness and discrimination for resource allocation. *DEC Technical Report*.
*   **Sutton, R. S., & Barto, A. G. (2018).** *Reinforcement Learning: An Introduction*. MIT Press.
*   **May, R., & Huang, P. (2023).** A MARL approach for investigating P2P prosumer energy markets. *Applied Energy*.
*   **Ren, Z., & Xu, Y. (2025).** Impact of Big Five Traits on AI Agent Decision-Making. *arxiv:2503.15497*.