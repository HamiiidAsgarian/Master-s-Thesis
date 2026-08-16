# Visual Agent Prompts — Thesis Figure Generation

This document catalogs all visual-agent prompts created for generating professional figures via the "Nano Banana" image-generation AI. Each prompt conveys the holistic concept plus mandatory text, letting the visual agent decide layout.

---

## Figure 1-1 — Tragedy of the Commons

| Field | Value |
|:------|:------|
| **Image file** | `v09_tragedy_of_commons.png` |
| **Script** | `generate_all_Visuals2.py` (lines 399–450) |
| **Concept** | Two-panel diagram illustrating Hardin's Tragedy of the Commons metaphor applied to energy sharing. Left panel: the classical grazing land commons with cattle icons. Right panel: the energy analogy — solar panels, batteries, and houses. Both panels show the dilemma between individual hoarding (selfish, leading to system collapse) and collective sharing (cooperative, leading to mutual benefit). |
| **Description** | A two-panel conceptual figure. Left panel shows the classical commons (pasture with livestock), right panel shows the energy sharing analogy (houses with solar panels and batteries). Arrows and labels show the two choices: hoard energy (defection) vs share energy (cooperation). Caption in Persian. |

### Prompt

```
Create a two-panel academic diagram for a Master's thesis. This figure illustrates the Tragedy of the Commons applied to residential energy sharing — Hardin's (1968) metaphor.

PANEL 1 — LEFT (Classical Commons):
- A pastoral scene: green grass representing shared grazing land (the commons)
- Several cattle/livestock icons on the pasture
- A fence or boundary around the pasture
- Label: "The Commons (Hardin, 1968)"
- A visual metaphor showing overgrazing: some areas of grass depleted/bare
- This is the original metaphor — NOT a translation error

PANEL 2 — RIGHT (Energy Analogy):
- Houses with rooftop solar panels and battery storage icons
- Connected by grid lines or arrows showing energy flow
- Two contrasting paths shown:
  - UP path (red): "Hoarding" — arrow pointing to depleted battery, dark house, system stress
  - DOWN path (green): "Sharing" — arrow pointing to balanced batteries, lit houses, community wellbeing
- A central dilemma symbol (fork in road or diverging arrows)

MUST INCLUDE — exact text (all in English):
- Title: "Tragedy of the Commons in Energy Sharing: The Hoarding vs Sharing Dilemma"
- Left panel: "The Commons (Hardin, 1968)"
- Right panel labels: "Hoarding" (red), "Sharing" (green), "Solar generation", "Battery storage", "Neighbour"
- Caption text in Persian: "تراژدی منابع مشترک در اشتراک انرژی: دوراهی احتکار در برابر اشتراک"

STYLE: Clean academic diagram, white background, landscape format, suitable for print at 300 DPI. The two panels should be visually distinct but conceptually linked. The left panel is the classical metaphor; the right panel is the energy application.
```

---

## Figure 2-1 — Conceptual Framework

| Field | Value |
|:------|:------|
| **Image file** | `v2_1_conceptual_framework.png` |
| **Script** | `generate_all_Visuals2.py` (lines 451–530) |
| **Concept** | The complete conceptual framework showing how OCEAN personality traits feed into Q-learning parameters, which produce emergent behaviours (sharing frequency, reciprocity patterns), which in turn produce community-level outcomes (comfort, fairness, Gini inequality). A three-layer input→process→output diagram with a feedback loop. |
| **Description** | Three-column framework: Left column = OCEAN traits (5 rows). Middle column = RL mechanism (reward function, exploration schedule, Q-table). Right column = emergent outcomes (5 metrics). A dashed feedback arrow loops from outcomes back to mechanism. |

### Prompt

```
Create an academic framework diagram for a Master's thesis. This figure shows the complete conceptual framework — how personality traits drive learning parameters, which produce emergent community outcomes.

THREE COLUMNS, left to right:

LEFT COLUMN — "Personality Encoding (OCEAN)":
Five rows, one per OCEAN trait:
- Openness → maps to exploration floor ε_min
- Conscientiousness → fixed at population mean
- Extraversion → fixed at population mean
- Agreeableness → maps to fairness weight w_fair
- Neuroticism → fixed at population mean
Only Openness and Agreeableness have arrows pointing right to the middle column. The other three are greyed out.

MIDDLE COLUMN — "RL Mechanism (Q-Learning)":
Three stacked boxes:
- "Reward Function: R = w_self × C + w_fair × F"
- "Exploration: ε-greedy with ε_min floor"
- "Q-Table: 96 states × 3 actions"
Arrows flow from this column to the right column.

RIGHT COLUMN — "Community Outcomes":
Five outcome metrics:
- "Average Comfort"
- "Jain's Fairness Index"
- "Blackout Rate"
- "Gini Inequality"
- "Energy Waste"

DASHED FEEDBACK ARROW:
A dashed arrow loops from the right column back to the middle column, labelled "Reinforcing feedback loops"

MUST INCLUDE — exact text (all in English):
- Title: "Conceptual Framework: From Personality to Community Outcomes"
- All labels as listed above
- The feedback loop label

STYLE: Clean academic framework diagram, white background, portrait format, suitable for print at 300 DPI. The three columns should be clearly separated with arrows showing information flow left-to-right, and the feedback loop should be visually distinct (dashed).
```

---

## Figure 3-1 — System Architecture Flowchart

| Field | Value |
|:------|:------|
| **Image file** | `v12_system_architecture.png` |
| **Script** | `generate_all_Visuals2.py` (lines 588–645) |
| **Concept** | The 10-block simulation loop showing the sequence of operations in each episode: environment reset → solar generation → demand patterns → state observation → Q-learning action → local consumption → sharing → reward calculation → time advance → episode end/logging. |
| **Description** | A 10-block flowchart showing the complete simulation loop. Blocks are numbered 1–10, arranged in two rows of five. Arrows show the flow. Block 1 loops back from Block 10. Each block has a brief label describing its function. |

### Prompt

```
Create an academic flowchart for a Master's thesis. This figure shows the complete 10-block simulation loop architecture — how each episode of the energy sharing simulation proceeds step by step.

10 BLOCKS arranged in two rows of five, numbered 1–10:

TOP ROW (left to right):
1. "Environment Reset" — batteries to 50%, sample weather (clear/cloudy)
2. "Solar Generation" — half-sine model G(h) = G_max × sin(π(h-6)/12) × W
3. "Demand Patterns" — assign 4 profile types (morning/evening/flat/night owl)
4. "State Observation" — agent sees (hour, battery level) = 96 discrete states
5. "Action Selection" — ε-greedy Q-table: share 0%, 50%, or 100%

BOTTOM ROW (right to left):
6. "Local Consumption" — Phase 1: solar → demand → battery charge/discharge
7. "Energy Sharing" — Phase 2: send share to neighbour in ring topology
8. "Reward Calculation" — R_i = w_self × C_i + w_fair × F (Eq. 3-2)
9. "Q-Update" — Q(s,a) ← Q(s,a) + α[R + γ·max Q(s',a') - Q(s,a)]
10. "Episode End" — log metrics every 100 episodes, check if 8000 episodes done

FLOW ARROWS:
- Blocks 1→2→3→4→5 (top row, left to right)
- Block 5→6 (down to bottom row)
- Blocks 6→7→8→9→10 (bottom row, right to left)
- Block 10→1 (dashed arrow looping back to Block 1)

MUST INCLUDE — exact text (all in English):
- Title: "Simulation Loop Architecture: 10-Block Episode Cycle"
- All block labels as listed
- Numbers 1–10 on each block
- The feedback loop from Block 10 back to Block 1

STYLE: Clean academic flowchart, white background, landscape format, suitable for print at 300 DPI. Blocks should be uniformly sized rectangles with rounded corners. Arrows should be clear with directional heads. The two-row layout should be immediately readable.
```

---

## Figure 3-2 — Ring Topology

| Field | Value |
|:------|:------|
| **Image file** | `v02_ring_topology.png` |
| **Script** | `generate_all_Visuals2.py` (lines 100–140) |
| **Concept** | The 10-house ring topology where each house is a node and energy sharing occurs between adjacent neighbours. Each house has a solar panel and battery. Arrows show the direction of energy flow (unidirectional, clockwise). |
| **Description** | 10 circular nodes arranged in a ring, numbered 0–9. Each node contains a small house icon or label. Arrows connect each node to its clockwise neighbour. Solar panel and battery icons on each node. Caption explains the unidirectional sharing structure. |

### Prompt

```
Create an academic diagram for a Master's thesis. This figure shows the 10-house ring topology used for energy sharing simulation.

CONCEPT:
10 houses arranged in a circle (ring topology), numbered 0 through 9. Each house is represented as a circle with a house icon inside. Energy sharing is unidirectional — each house can only share with its immediate clockwise neighbour.

ELEMENTS:
- 10 circles arranged in a ring, evenly spaced
- Each circle labelled with house number (0–9)
- Each circle contains a small house icon
- Above each house: a small solar panel icon
- Below each house: a small battery icon
- Arrows connecting each house to its clockwise neighbour (house 0 → house 1 → house 2 → ... → house 9 → house 0)
- The arrows should be clearly visible and show direction of energy flow

MUST INCLUDE — exact text (all in English):
- Title: "10-House Ring Topology for Energy Sharing"
- House numbers: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
- Legend: "Unidirectional sharing: each house shares only with its clockwise neighbour"

STYLE: Clean academic diagram, white background, square/circular format, suitable for print at 300 DPI. The ring should be visually balanced with houses evenly spaced. Arrows should be clearly directional. The topology should immediately communicate: each house has exactly one neighbour to share with.
```

---

## Figure 3-5 — OCEAN to RL Parameter Mapping

| Field | Value |
|:------|:------|
| **Image file** | `v01_ocean_to_rl_mapping.png` |
| **Script** | `generate_all_Visuals2.py` (lines 62–97) |
| **Concept** | Shows which of the five OCEAN personality traits are "active" (mapped to specific RL parameters) and which are "inactive" (held fixed). Only Openness → ε_min and Agreeableness → w_fair are active. The other three traits are greyed out with no arrows. |
| **Description** | Five rows, one per OCEAN trait. Active traits (Openness, Agreeableness) have coloured arrows pointing to their RL parameter. Inactive traits (Conscientiousness, Extraversion, Neuroticism) are grey with italic text "fixed at population mean". |

### Prompt

```
Create an academic schematic diagram for a Master's thesis. This figure shows the mapping from the five OCEAN personality traits to specific reinforcement learning parameters. It is the core conceptual contribution of the thesis — showing exactly which personality dimensions matter and how they affect agent behaviour.

CONCEPT:
Five rows, one for each OCEAN personality trait, arranged vertically. Each row has the trait name on the left and what it maps to on the right. Only two of the five traits are "active" — they have a direct arrow connecting them to a specific RL parameter. The other three are "inactive" — they are held fixed and have no arrow, just a grey text note saying they are fixed.

The five rows from top to bottom:

ROW 1 — Openness (ACTIVE, purple):
- Left box: "Openness" in purple
- Arrow pointing right
- Right box: "ε_min" (exploration floor) in purple
- This means: the higher a house's Openness, the higher its minimum exploration rate — it keeps exploring sharing strategies longer instead of settling on a greedy policy

ROW 2 — Conscientiousness (INACTIVE, grey):
- Left box: "Conscientiousness" in grey
- NO arrow
- Grey italic text: "fixed at population mean"
- This dimension is held constant across all agents

ROW 3 — Extraversion (INACTIVE, grey):
- Left box: "Extraversion" in grey
- NO arrow
- Grey italic text: "fixed at population mean"

ROW 4 — Agreeableness (ACTIVE, green):
- Left box: "Agreeableness" in green
- Arrow pointing right
- Right box: "w_fair" (fairness weight in reward) in green
- This means: the more Agreeable a house is, the more weight it gives to social fairness (Jain's index) in its reward function, making it share more generously

ROW 5 — Neuroticism (INACTIVE, grey):
- Left box: "Neuroticism" in grey
- NO arrow
- Grey italic text: "fixed at population mean"

MUST INCLUDE — exact text (all in English):
- Figure title: "Mapping OCEAN Personality Traits to RL Parameters"
- Left column labels: "Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"
- Right column labels (active): "ε_min" with subtitle "exploration floor", "w_fair" with subtitle "fairness weight in reward"
- Right column labels (inactive): "fixed at population mean"
- The two active traits should have clear coloured arrows (purple for Openness, green for Agreeableness)
- The three inactive traits should have NO arrow and be visually muted (grey)

STYLE: Clean academic diagram, white background, landscape format, suitable for print at 300 DPI. The active rows should visually stand out (coloured boxes and arrows), while the inactive rows should recede (grey, no arrows). The visual hierarchy should immediately communicate: "Only two traits matter — the other three are held constant."
```

---

## Figure 3-6 — Two-Phase Energy Sharing Mechanism

| Field | Value |
|:------|:------|
| **Image file** | `v03_two_phase_sharing.png` |
| **Script** | `generate_all_Visuals2.py` (lines 141–207) |
| **Concept** | The two-phase energy sharing flowchart. Phase 1 (top): local consumption — solar generation meets demand, surplus charges battery, deficit discharges battery, leftover becomes exportable surplus or unmet demand. Phase 2 (bottom): sharing — the agent decides what fraction of exportable surplus to send to neighbour, with outcomes being reduced unmet demand, battery storage, or energy waste. |
| **Description** | Two horizontal phases. Phase 1 has a decision diamond "Generation > demand?" with Yes/No branches leading to battery charge/discharge and exportable surplus/unmet demand. Phase 2 has the agent action (0%/50%/100%) leading to send to neighbour, then splitting to reduced unmet demand or battery storage or waste. A dashed arrow connects the phases. |

### Prompt

```
Create an academic flowchart diagram for a Master's thesis. This figure shows the two-phase energy sharing mechanism — how each house first uses energy locally, then decides how much surplus to share with neighbours.

CONCEPT:
The diagram is split into two horizontal phases, one above the other:

PHASE 1 — TOP HALF — "Phase 1 — Local":
This shows what happens inside a single house before any sharing occurs.

Flow:
1. "Solar generation" box (blue) and "Hourly demand" box (dark) feed into a decision diamond
2. Diamond: "Generation > demand?" (orange)
3. If YES (green arrow going up-right): → "Battery charge" box (green, with note "(7 kWh capacity)") → "Exportable surplus" box (green)
4. If NO (red arrow going down-right): → "Battery discharge" box (red) → "Unmet demand" box (red)

PHASE 2 — BOTTOM HALF — "Phase 2 — Sharing":
This shows what happens with any exportable surplus from Phase 1.

Flow:
1. "Exportable surplus" box (green) feeds into → "Agent action: 0% / 50% / 100%" box (purple) — this is the reinforcement learning decision
2. "Send to neighbour" box (blue) — the agent decides what fraction of surplus to send
3. From "Send to neighbour", two arrows split:
   - Upward: "Reduces unmet demand" box (green) — the neighbour receives energy and avoids blackout
   - Downward: "Store surplus in battery" box (teal) — remainder goes into battery storage
4. If battery is full: → "Energy waste" box (red) — excess energy is lost

CONNECTOR between phases:
A dashed vertical arrow on the right side connects "Exportable surplus" from Phase 1 down to "Exportable surplus" in Phase 2, labelled "Surplus carried to Phase 2"

MUST INCLUDE — exact text (all in English):
- Phase labels: "Phase 1 — Local" (top), "Phase 2 — Sharing" (bottom)
- All box labels as listed above
- Diamond text: "Generation > demand?"
- Decision labels: "Yes" (green), "No" (red)
- Connector label: "Surplus carried to Phase 2"
- Battery note: "(7 kWh capacity)"

STYLE: Clean academic flowchart, white background, landscape format, suitable for print at 300 DPI. Decision diamond should be visually distinct from rectangular boxes. Arrows should be clear with direction labels where needed.
```

---

## Figure 3-7 — Community Compositions in Experimental Scenarios

| Field | Value |
|:------|:------|
| **Image file** | `v06_community_compositions.png` |
| **Script** | `generate_all_Visuals2.py` (lines 255–301) |
| **Concept** | Shows the five experimental community compositions — how 10 houses are distributed across personality types in each scenario. Each row is a scenario, each circle is a house, coloured by personality type. Shows the range from uniform (all selfish, all prosocial) to heterogeneous (varied altruism, innovator effect). |
| **Description** | Five rows of 10 coloured circles each. Row 1: All Selfish (10 red). Row 2: All Prosocial (10 green). Row 3: Mixed (5 green + 5 red). Row 4: Varied Altruism (1 teal + 3 green + 3 yellow + 3 red). Row 5: Innovator Effect (1 purple + 4 green + 3 yellow + 2 red). Legend at bottom. |

### Prompt

```
Create an academic diagram for a Master's thesis. This figure shows the five experimental community compositions — how 10 houses are distributed across personality types in each scenario.

CONCEPT:
Five horizontal rows, one for each scenario. Each row contains 10 circles side by side, each circle representing one house. Circles are coloured by personality type. The rows are arranged vertically.

ROW 1 — "All Selfish":
10 red circles

ROW 2 — "All Prosocial":
10 green circles

ROW 3 — "Mixed":
5 green circles + 5 red circles

ROW 4 — "Varied Altruism":
1 teal circle + 3 green circles + 3 yellow circles + 3 red circles

ROW 5 — "Innovator Effect":
1 purple circle + 4 green circles + 3 yellow circles + 2 red circles

LEGEND at the bottom:
- Teal circle: "Altruistic, w_fair = 0.8"
- Green circle: "Prosocial, w_fair = 0.5"
- Yellow circle: "Individualist, w_fair = 0.2"
- Red circle: "Purely selfish, w_fair = 0.0"
- Purple circle: "Innovator, ε_min = 0.05"

MUST INCLUDE — exact text (all in English):
- Title: "Community Compositions in Experimental Scenarios"
- Row labels: "All Selfish", "All Prosocial", "Mixed", "Varied Altruism", "Innovator Effect"
- House numbers (0–9) above the circles in the first row only
- All legend labels as listed above with their parameter values

STYLE: Clean academic diagram, white background, landscape format, suitable for print at 300 DPI. The circles should be large enough to be clearly distinguishable. The visual should immediately communicate the personality diversity in each scenario — from uniform (top two rows) to heterogeneous (bottom two rows).
```

---

## Figure 4-3 — Emergent Reciprocity Mechanism

| Field | Value |
|:------|:------|
| **Image file** | `v07_reciprocity_cycle.png` |
| **Script** | `generate_all_Visuals2.py` (lines 303–356) |
| **Concept** | Two opposing feedback cycles that emerge in mixed communities. The virtuous cycle (green): prosocial agents share surplus during solar hours → neighbour batteries stay stable → neighbours reciprocate at night → prosocial agent receives when in deficit → reinforces sharing. The vicious cycle (red): selfish agents hoard → neighbour batteries deplete → neighbours cannot reciprocate → selfish agent faces deficit alone → reinforces hoarding. |
| **Description** | Two circular cycles of 4 boxes each. Top cycle (green): prosocial sharing loop with reinforcing "+" feedback. Bottom cycle (red): selfish hoarding loop with reinforcing "–" feedback. Legend at bottom. |

### Prompt

```
Create an academic diagram for a Master's thesis. This figure shows the emergent reciprocity mechanism — two opposing feedback cycles that emerge in mixed communities.

CONCEPT:
Two large circular cycles, one above the other, each consisting of 4 boxes arranged in a rectangle and connected by arrows forming a loop.

TOP CYCLE — "Virtuous cycle (prosocial)" in GREEN:

Four boxes arranged clockwise:
- Bottom-left: "Prosocial sends surplus 10:00–16:00"
- Bottom-right: "Neighbour battery stays stable"
- Top-right: "Neighbour returns energy at night"
- Top-left: "Prosocial receives when in deficit"

Arrows connect each box to the next in a clockwise loop. In the centre of the cycle: a green "+" symbol and the text "Reinforcing feedback"

BOTTOM CYCLE — "Vicious cycles (selfish)" in RED:

Four boxes arranged clockwise (same spatial structure):
- Top-left: "Selfish agent hoards surplus"
- Top-right: "Neighbour battery depletes"
- Bottom-right: "Neighbour cannot reciprocate"
- Bottom-left: "Selfish agent faces deficit alone"

Arrows connect each box to the next in a clockwise loop. In the centre: a red "–" symbol and the text "Reinforcing feedback"

MUST INCLUDE — exact text (all in English):
- Title: "Emergent Reciprocity Mechanism"
- Virtuous cycle labels: "Prosocial sends surplus 10:00–16:00", "Neighbour battery stays stable", "Neighbour returns energy at night", "Prosocial receives when in deficit"
- Vicious cycle labels: "Selfish agent hoards surplus", "Neighbour battery depletes", "Neighbour cannot reciprocate", "Selfish agent faces deficit alone"
- Centre labels: "+" and "Reinforcing feedback" (green for virtuous), "–" and "Reinforcing feedback" (red for vicious)
- Legend at bottom: green line "Virtuous cycle (prosocial)", red line "Vicious cycles (selfish)"

STYLE: Clean academic diagram, white background, square format, suitable for print at 300 DPI. The two cycles should be visually distinct (green vs red) and clearly show the contrast between cooperation leading to mutual benefit vs selfishness leading to mutual loss.
```

---

## Summary Table

| Figure | Image File | Script Location | Status |
|:-------|:-----------|:----------------|:-------|
| 1-1 | `v09_tragedy_of_commons.png` | lines 399–450 | ✅ Prompt ready |
| 2-1 | `v2_1_conceptual_framework.png` | lines 451–530 | ✅ Prompt ready |
| 3-1 | `v12_system_architecture.png` | lines 588–645 | ✅ Prompt ready |
| 3-2 | `v02_ring_topology.png` | lines 100–140 | ✅ Prompt ready |
| 3-5 | `v01_ocean_to_rl_mapping.png` | lines 62–97 | ✅ Prompt ready |
| 3-6 | `v03_two_phase_sharing.png` | lines 141–207 | ✅ Prompt ready |
| 3-7 | `v06_community_compositions.png` | lines 255–301 | ✅ Prompt ready |
| 4-3 | `v07_reciprocity_cycle.png` | lines 303–356 | ✅ Prompt ready |
| 3-3 | `v04_demand_profiles.png` | lines 209–227 | ⏳ Pending |
| 3-4 | `v05_solar_curve.png` | lines 229–252 | ⏳ Pending |
| 3-8 | `v13_scenarios_comfort.png` | lines 647–690 | ⏳ Pending |
| 3-9 | `v14_scenarios_fairness.png` | lines 692–735 | ⏳ Pending |
| 4-1 | `v13_scenarios_comfort.png` | lines 647–690 | ⏳ Pending |
| 4-2 | `v14_scenarios_fairness.png` | lines 692–735 | ⏳ Pending |
| 4-4 | `v11_lorenz_curve.png` | lines 532–570 | ⏳ Pending |
| 4-5 | `v15_gini_comparison.png` | lines 737–780 | ⏳ Pending |
| 4-6 | `v16_sharing_frequency.png` | lines 782–825 | ⏳ Pending |
| 4-7 | `v17_punishment_distribution.png` | lines 827–870 | ⏳ Pending |
| 4-8 | `v18_comfort_breakdown.png` | lines 872–933 | ⏳ Pending |
| 4-9 | `v08_innovator_effect.png` | lines 358–397 | ⏳ Pending |
| 4-10 | `v10_sota_comparison.png` | lines 455–530 | ⏳ Pending |

---

*Last updated: 2026-08-16*
