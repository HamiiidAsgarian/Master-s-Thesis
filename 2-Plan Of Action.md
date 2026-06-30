# Thesis Finalisation — Revised Plan of Action (v2)

**Basis:** `Latest_Professor_Opinion.md` (14 critique points) cross-referenced with `Sim-Documentation.md` (project state & constraints).

Use this as a checklist to track progress. Tasks are ordered by thesis section sequence.
  
---

## Phase 0: Structural Overhaul
- [ ] **Restructure Thesis Outline:** Map the document to the canonical sequence the professor prescribed:
  1. Introduction
  2. Literature Review & Gap Analysis
  3. Proposed Method (Flowchart + Pseudocode + Box-by-box)
  4. Experiment Design (Physical Environment → Parameters → Evaluation Metrics)
  5. Results & Interpretation
  6. Conclusion, Limitations & Future Work
- [ ] **Style Conversion (Global):** Convert *every* bullet-point list and slide-style enumeration (1-2-3-4) in the current draft into full scientific paragraphs with complete sentences and analytical depth.

---

## Phase 1: Introduction & Literature Review
- [ ] **Rewrite Introduction:** Clearly state the problem (inefficient/unfair energy management in smart neighbourhoods), preview the innovation (OCEAN-based reward shaping for ethical MARL), and outline the paper structure.
- [ ] **Gap Analysis:** End the Literature Review chapter with an explicit summary of research gaps that the proposed method addresses.
- [ ] **Comparative Table:** Build a table of 10–12 recent related papers with columns: Idea / Pros / Cons.
- [ ] **Specify Innovation:** Explicitly state that the contribution is a reward-shaping framework mapping Big Five (OCEAN) traits to fairness constraints in MARL — not a novel RL algorithm.

### Reference Check (Phase 1)
- [ ] Every claim about prior work in the Literature Review must have an inline citation.

---

## Phase 2: Proposed Method (Section 3)
- [ ] **Mathematical Foundation:** State the source of all equations (e.g., Q-learning update from Sutton & Barto, 2018). If equations are original, say so explicitly.
- [ ] **Flowchart:** Create a system architecture flowchart (Mermaid) covering the full simulation loop — environment initialisation → agent observation → action selection (ε-greedy with OCEAN-modulated exploration) → energy sharing → reward computation → Q-table update.
- [ ] **Pseudocode:** Write formal pseudocode for the Q-Learning algorithm and the OCEAN-weighted reward mechanism.
- [ ] **Box-by-box Explanation:** For every block in the flowchart, write a paragraph explaining what happens, why it happens, and how it connects to the research gap.
- [ ] **Equations — Prose → Parameters → Citation:** For every equation (solar generation, reward, fairness index), write:
  1. One paragraph of prose explaining the equation's purpose and intuition.
  2. The equation itself.
  3. A parameter table below it defining each symbol (e.g., $HW$, $G_{max}$, $w_{self}$, $w_{fair}$) with units and source citation.

### Reference Check (Phase 2)
- [ ] Every equation must have a citation (unless it is the student's own derivation).
- [ ] Every parameter definition must cite the source of its value where applicable.

---

## Phase 3A: Physical Environment & Parameter Grounding
- [ ] **Parameter Justification (Ground Truth):** For every simulation hyperparameter (1.3 kW solar peak, 7.0 kWh battery, 15 % cloud probability, demand profiles, random seeds, 8000 episodes), provide one of:
  - (a) Citation to a prior study that used the same value.
  - (b) Reference to a systematic experimental design approach (e.g., Taguchi, black-box optimisation).
  - (c) A brief empirical justification (e.g., "determined via grid search over 5 seeds; value X minimised blackout rate").
- [ ] **Hyperparameter Table:** Create a comprehensive table listing all environment and learning hyperparameters with their values, units, and sources.

### Reference Check (Phase 3A)
- [ ] Every numerical value in the hyperparameter table must have a source citation.

---

## Phase 3B: Evaluation Metrics Definition
- [ ] **Define Metrics in Full Paragraphs:** Write standalone prose definitions (not bullet points) for:
  - Comfort Rate
  - Jain's Fairness Index
  - Gini Coefficient (energy inequality)
  - Blackout Rate
  - Sharing Frequency
- [ ] **Metric Formulas:** Present each metric's formula with proper parameter definitions and citations.
- [ ] **Tie Metrics to Research Questions:** Explain which metric addresses which aspect of the research gap (e.g., "Jain's Fairness Index directly quantifies whether the OCEAN-based reward shaping reduces inequality compared to the baseline").

### Reference Check (Phase 3B)
- [ ] Each metric formula must cite its original source (e.g., Jain, 1984 for Fairness Index; Gini, 1912 for Gini coefficient).

---

## Phase 4: Results & Interpretation (Section 5)
- [ ] **Baseline — "No System" Condition:** Introduce the baseline scenario as the condition **where the proposed ethical reward shaping is absent** (e.g., a "No-Sharing" or "Selfish-only RL without fairness" run). This is not merely "All Selfish" — it must represent the absence of the *method*. Present baseline results first, then compare all other scenarios against it.
- [ ] **SOTA Comparison:** After baseline comparison, compare the best-performing scenario (e.g., Mixed or Innovator Effect) against comparable results from the literature (at least 3–5 papers).
- [ ] **Structure Results by Metric:** Present results step by step — one subsection per evaluation metric. For each metric:
  1. Restate the metric and its purpose.
  2. Present the figure/table.
  3. Write a full analytical paragraph interpreting the figure (what it shows, *why* it happened).
  4. Explain *negative* results as thoroughly as positive ones.
- [ ] **Figure Captions → Full Interpretations:** Replace all one-line figure captions with multi-paragraph analytical interpretations.
- [ ] **Statistical Tests in Prose:** Present t-test and ANOVA results in running text, not as raw output dumps.
- [ ] **Neutral Overall Analysis:** End the Results chapter with a subsection summarising objectively: what worked, what did not, and why — no hype, neutral academic tone.

### Reference Check (Phase 4)
- [ ] When comparing with SOTA, cite the relevant papers.
- [ ] Cite statistical test methodology sources if applicable.

---

## Phase 5: Limitations & Conclusion
- [ ] **Rewrite Limitations as Paragraphs:** Convert the current 8-item bullet list into 3–5 focused, standalone scientific paragraphs. For each limitation:
  - State the limitation.
  - Explain *why* it is a limitation (e.g., "Simple weather is a limitation because real solar irradiance follows stochastic Markov processes, which affects the generalisability of learned policies to real-world microgrids").
  - Explain *how* it affects the results.
  - Do **not** let limitations overshadow the contribution — keep them precise and bounded.
- [ ] **Deepen Conclusion:** Write a comprehensive conclusion covering:
  1. What the work is (OCEAN-based reward shaping for ethical MARL).
  2. Why it was done (gap: lack of personality-aware fairness in energy MARL).
  3. The proposed method.
  4. Summary of key results (with brief analytical reasoning).
  5. A dedicated paragraph for **Future Work** (e.g., dynamic personalities, continuous-state RL, real weather models, larger neighbourhoods).

### Reference Check (Phase 5)
- [ ] If future work suggestions reference specific methods or papers, cite them.

---

## Phase 6: Final Polish
- [ ] **Global Reference Audit:** Review the entire document to ensure:
  - Every equation has a citation (or is clearly marked as original).
  - Every table with external numbers has a source.
  - Every parameter in every equation is defined in prose or a table directly below it.
  - Every claim about prior work, benchmarks, or standard metrics is cited.
- [ ] **Proofread for Academic Tone:** Remove hype words, informal phrasing, and colloquialisms.
- [ ] **Cross-check with Sim-Documentation:** Ensure consistency with the 10-house model, OCEAN framework, and current results (do not reference Unity or 6-house remnants).
- [ ] **Final Formatting:** Ensure all figures, tables, equations, and references follow the target venue's style guide.
