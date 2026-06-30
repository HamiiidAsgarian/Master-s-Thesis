# Master Reference Strategy & Extraction Guide

**Purpose:** This document is the single source of truth for all references needed for the thesis. It merges the raw links from `02-refs.md` with the previously cited papers. It explicitly outlines **what papers we have**, **why we need them**, and **exactly what data to extract** from each for the thesis.

---

## 1. The Master Reference Inventory

This table consolidates all 30+ papers across all dimensions of the thesis.

### A. Literature Review & Comparative Papers (Phase 1)
| ID | Citation | Purpose / Why We Have It |
|:---|:---|:---|
| #1 | Charbonnier et al. (2022). Scalable MARL for distributed control... | **Primary Comparison:** Methodologically similar work on residential energy flexibility. |
| #6 | Kusatake et al. (2023). P2P energy sharing... | **Primary Comparison:** Analyzes efficiency vs. fairness trade-offs. |
| #7 | Charbonnier et al. (2023). Centralised rehearsal... | Shows the state-of-the-art progression to Deep MARL. |
| #9/29 | Aloor et al. (2024). Cooperation and Fairness in MARL. | Direct comparison for balancing global efficiency with individual fairness. |
| #10 | Behrunani et al. (2023). Designing Fairness in Autonomous P2P... | Game-theory baseline to contrast with your RL approach. |
| #12 | Jadhav et al. (2025). FairMarket-RL: LLM-Guided Fairness... | Most recent SOTA using LLMs for fairness (shows timeliness of topic). |
| #28 | Fairness in MARL for Smart Grids (arXiv:2305.11450) | Specifically links fairness, MARL, and smart grids. Perfect for gap analysis. |
| (Old) | Li & Zhang (2022). MARL for energy management: A comprehensive review. | General MARL energy survey for the introduction. |
| (Old) | Alshehri & Gaunt (2020). Heterogeneous MARL for residential energy... | **Key Gap Paper:** Has heterogeneous agents but lacks the psychological foundation you provide. |

### B. MARL Algorithm Foundations (Phase 1 & 2)
| ID | Citation | Purpose / Why We Have It |
|:---|:---|:---|
| #21 | Huh & Mohapatra (2023). MARL: A Comprehensive Survey. | Explains CTDE paradigm. Used to justify why you chose Independent Q-learning over MADDPG. |
| #22 | Leng (2025). Systematic Survey of MARL (arXiv:2507.06278). | Discusses non-stationarity in MARL, framing the problem your state-space solves. |
| (Old) | Sutton & Barto (2018). RL: An Introduction. | Foundation for the Q-learning update equation. |
| (Old) | Watkins & Dayan (1992). Q-learning. | Original convergence proof for Q-learning. |

### C. Psychological Foundation & Reward Shaping (Phase 2)
| ID | Citation | Purpose / Why We Have It |
|:---|:---|:---|
| #25 | Goldberg (1990). An alternative "description of personality"... | **Foundational:** First mention of the Big Five / OCEAN structure. |
| #26 | John & Srivastava (1999). The Big Five trait taxonomy... | Explains what traits like Agreeableness mean (justifies your $w_{fair}$ weights). |
| (Old) | McCrae & Costa (2003). Personality in Adulthood... | Secondary psychological foundation. |
| #8 | Hughes et al. (2018). Inequity aversion improves cooperation... | **Crucial:** Justifies adding a fairness/inequity term directly into the RL reward function. |
| #27 | Personality Traits in RL Agents (arXiv:2212.11252) | Proves that mapping Big Five to RL parameters is a valid, modern AI methodology. |
| #17 | Ren & Xu (2025). Impact of Big Five on AI Agent Decision-Making. | Contextualizes Big Five in modern agent design. |

### D. Energy Environment Ground-Truth Parameters (Phase 3A)
| ID | Citation | Purpose / Why We Have It |
|:---|:---|:---|
| #23 | RL for Microgrid Energy Management (arXiv:2108.06450). | **Ground Truth:** Justifies using a 7.0 kWh battery and specific residential load sizes. |
| #24 | Deep RL for Smart Home Energy Management (arXiv:1912.11215). | **Ground Truth:** Justifies hourly demand profiles and stochastic solar (weather) probabilities. |

### E. Evaluation Metrics (Phase 3B)
| ID | Citation | Purpose / Why We Have It |
|:---|:---|:---|
| (Old) | Jain et al. (1984). A quantitative measure of fairness... | Original formula and source for Jain's Fairness Index. |
| #30 | Gini, C. (1912). Variabilità e mutabilità. | Original formula and source for the Gini Coefficient. |

### F. Results, Interpretation & Future Work (Phase 4 & 5)
| ID | Citation | Purpose / Why We Have It |
|:---|:---|:---|
| #20 | Zhang et al. (2025). Optimistic ε-Greedy Exploration for Cooperative MARL. | **Innovator Effect:** Explains theoretically why high exploration disrupts cooperative groups. |
| (Old) | Fehr & Gächter (2000). Cooperation and punishment... | Social dilemma theory context for why selfish agents dominate without fairness rules. |
| (Old) | Fischbacher & Gächter (2010). Social preferences, beliefs... | Behavioral spillover theory. |

---

## 2. Data Extraction Protocol (What we need to pull from each paper)

When you sit down to write, you must open these PDFs and extract specific information. Follow this protocol:

### For the Comparative Literature Table (Group A)
Extract these exactly to build the 10-12 paper table for Phase 1:
1. **Algorithm Used:** (e.g., Independent Q-learning, MADDPG, Game Theory)
2. **Environment:** (e.g., P2P Grid, EV Charging, 10-house microgrid)
3. **Fairness Mechanism:** (e.g., Reward shaping, LLM critic, hard constraints)
4. **Personality Modeling?** (Yes/No — *Spoiler: Most will be No, which proves your novelty*)
5. **Pros:** What did they do well?
6. **Cons / Gaps:** What did they miss that *you* are solving?

### For the SOTA Comparison in Results (Group A)
To satisfy the professor's demand to compare your results with others (Phase 4):
1. **Fairness Metric:** Find their final Jain's Index or Gini coefficient.
2. **Efficiency/Cost Metric:** Find their blackout rate or overall cost savings.
3. *Note: We will put these numbers side-by-side with your "Mixed" and "Prosocial" scenario results to prove your method is competitive.*

### For the Equations (Group B, C, & E)
When writing Phase 2 and Phase 3B:
1. **The Formula:** Extract the exact mathematical representation.
2. **The Parameters:** Note how they define their symbols (so you can match your $w_{self}$, $w_{fair}$, $G_{max}$ formatting).

### For the Simulation Ground Truth (Group D)
To satisfy the professor's critique about "invented numbers" (Phase 3A):
1. **Solar Peak Capacity:** Find the exact kW number they used for residential PV.
2. **Battery Capacity:** Find the exact kWh they used.
3. **Weather Probability:** Find how they modeled cloudy days or solar variance.
4. *Note: You will write: "Following the residential microgrid parameters established in [Citation #23] and [Citation #24], the simulation uses a 7.0 kWh battery..."*

---

## 3. Unverified/Deprecated Links (To Ignore)
The following links from the original raw list should be ignored unless absolutely necessary, as they are unverified ResearchGate links or tangentially related:
- ID 2, 4, 11, 13 (Unverified ResearchGate links — we have better arXiv/published alternatives now).
- ID 16 (Park 2023 - Generative Agents) — Too focused on LLMs playing the Sims, distracts from the energy MARL focus.
