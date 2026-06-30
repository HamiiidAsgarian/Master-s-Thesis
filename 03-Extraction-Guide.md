# Extraction Guide — Organized by Thesis Section

**Purpose:** When writing each thesis section, open this file to see which papers to query in Notebook LM, what data to extract, and where it goes in your thesis.

---

## Phase 1: Introduction & Literature Review

### 1A. Problem Motivation (Introduction — "Why does this matter?")

| Paper | Data to extract | Notebook LM prompt location |
|-------|-----------------|---------------------------|
| #11 Equity Aware Trading | Quote about energy poverty, why equity matters in P2P energy | 02-refs.md → Group A → #11 |
| #1 Charbonnier 2022 | Context for residential energy MARL | 02-refs.md → Group A → #1 |
| Li & Zhang 2022 (Old) | Survey findings on MARL+energy field | 02-refs.md → Group A → (Old) Li & Zhang |

### 1B. Comparative Literature Table (Phase 1 — 10–12 papers)

For **each** paper below, extract the same 6 fields: Algorithm, Environment, Fairness Mechanism, Personality? (Yes/No), Pros, Cons/Gaps.

| Paper | Key angle for comparative table |
|-------|-------------------------------|
| #1 Charbonnier 2022 | Scalable MARL for residential — no fairness/personality → gap |
| #6 Kusatake 2023 | Efficiency vs fairness in P2P — explicit fairness trade-off, no OCEAN |
| #7 Charbonnier 2023 | Deep MARL SOTA — no fairness, no personality |
| #9/29 Aloor 2024 | Cooperation + fairness in MARL — no OCEAN |
| #10 Behrunani 2023 | Game theory fairness — not RL, no personality |
| #12 Jadhav 2025 | LLM-guided fairness — very recent, no OCEAN |
| #14 Ali 2023 | Microgrid MARL — no fairness/personality |
| #18 Jin 2024 | Suggestion sharing as implicit fairness — no OCEAN |
| #28 Fairness in MARL Smart Grids | Unifies fairness+MARL+grids — no OCEAN |
| #13 Q-Learning CBESS | Q-learning for community battery — fairness? |
| Alshehri & Gaunt 2020 (Old) | **Key Gap** — heterogeneous MARL, NO personality → your novelty |
| #19 Mu 2024 | Background on cooperation in MARL |

**Prompt for each:** Copy from 02-refs.md → Group A → [ID]. Ask for Algorithm, Environment, Fairness, Personality?, Pros, Cons, and quantitative results.

### 1C. Gap Analysis (End of Literature Review)

Summarize: Everyone does fairness OR MARL OR energy, but **no one** combines OCEAN personality + fairness reward shaping in MARL for energy.

Key gap evidence papers:
- **Alshehri & Gaunt 2020**: Closest to you (heterogeneous agents), but **no psychology** → your gap
- **#27 Personality Traits in RL**: Proves OCEAN→RL mapping exists (in other domains) but **not in energy**
- **#17 Ren & Xu 2025**: Big Five in AI is active area, **but not applied to energy MARL**

---

## Phase 2: Proposed Method

### 2A. Q-Learning Equation (Method Section)

| Paper | Extract | Use in thesis |
|-------|---------|---------------|
| Sutton & Barto 2018 (Old) | Q-learning update formula + all symbol definitions | "Our algorithm uses the standard Q-learning update (Sutton & Barto, 2018):" |
| Watkins & Dayan 1992 (Old) | Convergence proof statement | "Tabular Q-learning converges to optimal Q* under standard conditions (Watkins & Dayan, 1992)" |
| #21 Huh 2023 | CTDE definition + Independent Q-learning justification | "We follow the CTDE paradigm (Huh & Mohapatra, 2023), specifically Independent Q-learning..." |
| #22 Leng 2025 | Non-stationarity formalization | "...which mitigates the non-stationarity problem inherent in MARL (Leng, 2025)" |

### 2B. OCEAN-Based Reward Function (Core Innovation)

| Paper | Extract | Use in thesis |
|-------|---------|---------------|
| #25 Goldberg 1990 | Big Five trait names and definitions | "The OCEAN framework (Goldberg, 1990) provides five dimensions of personality..." |
| #26 John & Srivastava 1999 | Agreeableness definition (cooperation, altruism, trust) | "...we operationalize Agreeableness as \(w_{fair}\) in the reward (John & Srivastava, 1999)" |
| DeYoung & Peterson 2007 (New) | Agreeableness → Compassion + Politeness aspects | Shows you're using the modern refined model |
| #8 Hughes 2018 | Inequity aversion formula + fairness in RL reward | **Directly justifies your \(w_{fair}\) term**: "Following Hughes et al. (2018), we add an inequity aversion term to the reward..." |
| #27 Personality Traits in RL | Specific OCEAN→RL hyperparameter mappings | Defends methodology: "Mapping OCEAN to RL parameters follows established work [27]" |
| #17 Ren & Xu 2025 | Big Five → decision-making mapping | Shows this is current research (2025) |

### 2C. Solar Generation Equation

| Paper | Extract | Use in thesis |
|-------|---------|---------------|
| #23 Microgrid Energy Mgt | Solar generation formula they use | "Solar output is modeled following [#23]..." |
| #24 Smart Home Energy Mgt | Weather probability model | "...with stochastic weather as in [#24]" |

---

## Phase 3A: Physical Environment & Parameters

### Hyperparameter Ground Truth Table

Every number in your simulation needs a citation. Use these extracts:

| Parameter | Value | Source paper | What to extract |
|-----------|-------|-------------|-----------------|
| Battery capacity | 7.0 kWh | #23 | Exact kWh value + page |
| Solar peak | 1.3 kW | #23 | Exact kW value + page |
| Demand profiles | ~8.8 kWh/day | #24 | Hourly demand values |
| Cloud probability | 15% | #24 | Probability value + page |
| Solar reduction | 50% | #24 | Reduction % + page |
| Learning rate \(\alpha\) | your value | Sutton & Barto | Standard range justification |
| Discount \(\gamma\) | your value | Sutton & Barto | Standard range justification |

**Prompts to use in Notebook LM:**
- #23 prompt → 02-refs.md → Group D
- #24 prompt → 02-refs.md → Group D

---

## Phase 3B: Evaluation Metrics

| Metric | Source paper | What to extract |
|--------|-------------|-----------------|
| Jain's Fairness Index | Jain et al. 1984 (Old) | Formula \(\frac{(\sum x_i)^2}{n \sum x_i^2}\), symbol defs, range [0,1] |
| Gini Coefficient | Gini 1912 (#30) | Lorenz curve formula, range [0,1] interpretation |
| Comfort Rate | Your own | No citation needed (your definition) |
| Blackout Rate | Your own | No citation needed (your definition) |
| Sharing Frequency | Your own | No citation needed (your definition) |

**Prompts:** 02-refs.md → Group E

---

## Phase 4: Results & Interpretation

### 4A. SOTA Comparison

Compare your best scenario (Mixed or Prosocial) against these papers:

| Paper | What to extract for comparison |
|-------|-------------------------------|
| #1 Charbonnier 2022 | Their Jain's Index, blackout rate, cost savings |
| #6 Kusatake 2023 | Their fairness index and efficiency metric |
| #7 Charbonnier 2023 | Their deep MARL performance numbers |
| #9/29 Aloor 2024 | Their fairness + cooperation results |
| #10 Behrunani 2023 | Their game-theoretic cost/fairness outcomes |
| #12 Jadhav 2025 | Their LLM-guided fairness results |
| Alshehri & Gaunt 2020 | Their heterogeneous MARL results |

**Prompt for each:** Copy from 02-refs.md → Group A → [ID]. Ask specifically for quantitative results (Jain's, Gini, costs).

### 4B. Interpretation of Specific Results

| Finding | Explain using paper |
|---------|-------------------|
| Innovator underperforms | #20 Zhang 2025: "high exploration disrupts cooperative groups" |
| Selfish baseline is inefficient | Fehr & Gächter 2000: "free-rider problem in public goods" |
| Mixed shows intermediate results | Fischbacher & Gächter 2010: "behavioral spillover theory" |

**Prompts:** 02-refs.md → Group F

---

## Phase 5: Limitations & Conclusion

No new extraction needed. Use the extracted data from above.

---

## Phase 6: Final Polish — Reference Audit Checklist

Before submitting, verify:
- [ ] Every equation has a citation (use Group B and Group C extracts)
- [ ] Every parameter table has a source (use Group D extracts)
- [ ] Every symbol in every equation is defined (use all extracts)
- [ ] Every claim about prior work is cited (use Group A extracts)
- [ ] Jain's and Gini formulas cite original sources (Group E)
- [ ] SOTA comparison numbers cite specific papers (Group A)
- [ ] Social dilemma / exploration theory cites Fehr & Gächter / Zhang (Group F)
