# Thesis Visuals — Complete Specification & AI Image Generation Prompts

> **Thesis:** A New Method of Fair and Efficient Energy Sharing in Smart Neighborhoods Using Personality-Driven Multi-Agent Reinforcement Learning
>
> **Total visuals:** 18 (7 required by List of Figures + 11 recommended conceptual/infographic visuals)

---

## Part A — Conceptual / Schematic Visuals (Best for AI Image Generators)

These are diagrams, maps, and infographics that an image generator can produce well.

---

### Visual 1: OCEAN-to-RL Parameter Mapping

**Type:** Schematic / Mapping diagram
**Placement:** Ch.1 §1-3 (Research Innovation) or Ch.2 §2-4 (Conceptual Framework)
**Caption:** Figure 2-1: OCEAN-to-RL parameter mapping. The Big Five personality dimensions are mapped to specific reinforcement learning hyperparameters, enabling psychologically grounded agent heterogeneity.

**Description:**
A five-column diagram. Left side lists the five OCEAN traits with icons: Openness (compass/explore icon), Conscientiousness (gear/organization icon), Extraversion (people/social icon), Agreeableness (heart/handshake icon), Neuroticism (alert/shield icon). Arrows map each to an RL parameter on the right. Agreeableness → w_fair (fairness weight in reward function, range 0.0–0.8). Openness → ε_min (exploration floor, 0.01 standard vs 0.05 innovator). Conscientiousness → ε-decay variance. Neuroticism → blackout penalty multiplier. Extraversion → held at population average. Include axis labels showing continuum from low to high for each trait.

**AI Prompt:**
```
Create a professional academic-style schematic diagram for a PhD thesis in energy AI. The diagram maps the Big Five (OCEAN) personality traits to reinforcement learning parameters. Left column: five rectangles labeled Openness (compass icon), Conscientiousness (gear icon), Extraversion (people icon), Agreeableness (handshake/heart icon), Neuroticism (shield icon). From each, an arrow points right to RL parameters. Agreeableness → w_fair (fairness weight, 0.0 to 0.8) in a reward function box. Openness → ε_min (exploration floor, 0.01 vs 0.05) in an epsilon-greedy policy box. Conscientiousness → ε-decay variance. Neuroticism → blackout penalty multiplier. Extraversion: held at population average (dashed arrow, no parameter change). Bottom of diagram has a note: "Thesis Contribution — Psychologically Grounded Agent Heterogeneity." Use a clean blue/grey academic color palette, sans-serif fonts, no shadows or 3D effects. White background. Suitable for publication in a scientific thesis.
```

---

### Visual 2: Ring Topology Microgrid — System Overview

**Type:** Network topology diagram
**Placement:** Ch.3 §3-5 (Physical Environment)
**Caption:** Figure 3-2: Ring-topology smart neighbourhood microgrid. Ten prosumer households are connected in a ring; each house has rooftop solar panels, a home battery, and a bidirectional P2P energy link to its designated neighbour.

**Description:**
A circular ring of 10 houses (numbered 0–9). Each house is shown as a simple building icon with three components: a rooftop solar panel (blue PV cells), a battery icon (rectangle with lightning bolt) inside the house, and a bidirectional arrow along the ring edge between each house and its neighbour. The ring forms a closed loop. Optionally show the utility grid connection as a dashed line from one house going off to the side (for when the community imports/exports). Color-code houses by personality type in the Mixed scenario (5 green/prosocial, 5 red/selfish). Include a legend.

**AI Prompt:**
```
Create a clean academic network topology diagram for a smart microgrid thesis. Ten identical house icons arranged in a circle (ring topology), numbered 0 through 9 clockwise. Each house has a blue solar panel on its roof and a battery icon (gray rectangle with lightning symbol) visible inside. Bidirectional arrows along the edges of the ring connect each house to its neighbor, forming a closed loop. Color 5 houses green (labeled "prosocial") and 5 houses red (labeled "selfish") — alternating pattern. One house has a dashed line extending outward labeled "Utility Grid Connection (import/export)." Title at top: "Figure 3-2: Ring Topology Smart Neighbourhood Microgrid." Clean white background, simple flat icons, no 3D. Academic style suitable for a thesis.
```

---

### Visual 3: Two-Phase Energy Sharing Mechanism

**Type:** Flowchart / Process diagram
**Placement:** Ch.3 §3-9 (Energy Sharing Mechanism)
**Caption:** Figure 3-3: Two-phase energy sharing mechanism within each hour. Phase 1 handles local consumption and storage; Phase 2 handles peer-to-peer sharing of exportable surplus.

**Description:**
Split into two clearly labeled horizontal lanes. **Phase 1 (Local):** Solar Generation → meets Hourly Demand → surplus goes to Battery (up to 7.0 kWh capacity) → if battery full, surplus becomes Exportable Surplus. If generation < demand, Battery discharges to cover deficit → if battery depleted, Unmet Demand (comfort < 1.0). **Phase 2 (Sharing):** Exportable Surplus → Agent chooses action (0%, 50%, 100% share) → shared energy sent to neighbour → Neighbour first reduces any Unmet Demand, then stores remainder in battery → any remaining energy that cannot be stored or used is Waste. Show these as labeled boxes with arrows. Use green for positive flows (energy used/stored), red for negative (unmet demand, waste), blue for decision points.

**AI Prompt:**
```
Create a two-phase process flowchart for an energy sharing mechanism in a smart microgrid thesis. Split the diagram horizontally into two labeled lanes: PHASE 1 (LOCAL) at top and PHASE 2 (SHARING) below.

Phase 1 boxes in order: [Solar Generation] → [Hourly Demand] → decision diamond: "Generation > Demand?" Yes branch: [Charge Battery (7 kWh cap)] → if battery full: [Exportable Surplus]. No branch: [Discharge Battery] → if battery depleted: [Unmet Demand ⚠️].

Phase 2 boxes: [Exportable Surplus] → [Agent Action: 0% / 50% / 100% Share] → [Send to Neighbour] → [Neighbour: Reduce Unmet Demand First] → [Store Remainder in Battery] → if cannot store/use: [Energy Waste].

Use green arrows for energy used/stored flows, red arrows for unmet demand and waste, blue for action decisions. Clean academic style, white background, suitable for a thesis figure.
```

---

### Visual 4: Four Demand Profile Types

**Type:** Line chart (4 lines, 24 hours)
**Placement:** Ch.3 §3-5 (Physical Environment / Demand Profiles)
**Caption:** Figure 3-4: The four hourly demand profiles used in the simulation. Morning (peak 8 AM), Evening (peak 8 PM), Flat (constant 0.35 kWh), and Night Owl (peak 10 PM–2 AM). Profiles cycle across the 10 houses.

**Description:**
A 24-hour line chart (x-axis: hour 0–23, y-axis: kWh demand 0–1.4). Four lines in different colors: Morning (blue) peaks at 0.9 kWh at hour 8, Evening (orange) peaks at 1.2 kWh at hour 20, Flat (green) constant at 0.35, Night Owl (purple) peaks at 1.2 kWh between hour 22–2, low during day. Include a legend, axis labels, and a note that daily totals range from 8.4–9.6 kWh.

**AI Prompt:**
```
Generate a clean 24-hour line chart for a thesis on residential energy demand. X-axis: "Hour of Day (0–23)" with tick marks at 0, 6, 12, 18, 23. Y-axis: "Demand (kWh)" from 0 to 1.4.

Four lines with different colors and styles:
1. "Morning" (blue solid line) — near zero at hour 0, rising to peak 0.9 at hour 8, then declining to near zero by hour 14, staying low.
2. "Evening" (orange dashed line) — low all day, rising sharply after hour 16 to peak 1.2 at hour 20, then declining to low by hour 23.
3. "Flat" (green dotted line) — constant horizontal line at 0.35 for all 24 hours.
4. "Night Owl" (purple dash-dot line) — high values 1.0–1.2 between hour 22 and hour 2, very low 0.05 during midday.

Include a legend in the top-right corner. Add annotation: "Daily Total Range: 8.4–9.6 kWh." Clean white background, academic sans-serif font, no grid or minimal light grid. Suitable for a PhD thesis figure.
```

---

### Visual 5: Solar Generation Curve (Clear vs Cloudy)

**Type:** Line chart (2 lines)
**Placement:** Ch.3 §3-5 (Physical Environment / Solar Generation)
**Caption:** Figure 3-5: Half-sine solar irradiance model. Clear days (W=1.0) produce ~9.9 kWh daily; cloudy days (W=0.5) halve generation, creating scarcity conditions.

**Description:**
A line chart showing the half-sine curve from Eq. 3-1. X-axis: hour 0–23, Y-axis: kW generation 0–1.4. Two lines: Clear day (solid yellow/orange) peaks at 1.3 kW at hour 12, follows half-sine shape from hour 6 to 18. Cloudy day (dashed gray) at half amplitude, peaks at 0.65 kW. Shade the area under each curve to emphasize the energy difference. Add annotation: "Cloudy days occur with 15% probability (Bernoulli draw)."

**AI Prompt:**
```
Create a line chart for a thesis showing the half-sine solar irradiance curve. X-axis: "Hour of Day" (0–23) with ticks at 0, 6, 12, 18. Y-axis: "Solar Generation (kW)" from 0 to 1.4.

Two lines:
1. "Clear Day (W=1.0)" — thick yellow/orange solid line. Zero from hour 0–5, rises in a smooth half-sine arc from hour 6, peaks at 1.3 kW at exactly hour 12 (noon), descends symmetrically back to zero by hour 18. Area under this curve filled with light yellow/orange semi-transparent.
2. "Cloudy Day (W=0.5)" — gray dashed line at exactly half the amplitude of the clear curve, peaking at 0.65 kW. Area filled with light gray semi-transparent.

Annotate the peak: "Peak: 1.3 kW (clear), 0.65 kW (cloudy)." Add a note at top: "Eq. 3-1: G(h) = G_max · sin(π(h-6)/12) · W." Clean white background, academic sans-serif font. Suitable for a PhD thesis figure.
```

---

### Visual 6: Five Community Compositions

**Type:** Visual matrix / Grid of agents
**Placement:** Ch.3 §3-10 (Community Compositions / Scenarios)
**Caption:** Figure 3-6: The five experimental community compositions. Each row is a scenario; each circle is an agent, color-coded by personality type.

**Description:**
A 5-row × 10-column grid of circles. Each row is a scenario: All Selfish (10 red circles), All Prosocial (10 green circles), Mixed (5 green + 5 red), Varied Altruism (1 dark blue [altruistic] + 3 green + 3 yellow [individualist] + 3 red), Innovator Effect (1 purple [innovator] + 4 green + 3 yellow + 2 red). Each column is a house position (0–9). Include a color legend at the bottom: dark blue = altruistic (w_fair=0.8), green = prosocial (w_fair=0.5), yellow = individualist (w_fair=0.2), red = pure selfish (w_fair=0.0), purple = innovator (ε_min=0.05). Add scenario labels on the left.

**AI Prompt:**
```
Create a visual matrix for a thesis showing 5 experimental scenarios of agent compositions. Layout: 5 horizontal rows, each with 10 circles arranged left to right (representing 10 houses). Each row is labeled on the left:

Row 1 "All Selfish": all 10 circles red.
Row 2 "All Prosocial": all 10 circles green.
Row 3 "Mixed": 5 green circles then 5 red circles.
Row 4 "Varied Altruism": 1 dark blue, 3 green, 3 yellow, 3 red.
Row 5 "Innovator Effect": 1 purple, 4 green, 3 yellow, 2 red.

Color legend at bottom: dark blue = "Altruistic (w_fair=0.8)", green = "Prosocial (w_fair=0.5)", yellow = "Individualist (w_fair=0.2)", red = "Pure Selfish (w_fair=0.0)", purple = "Innovator (ε_min=0.05)."

Title at top: "Figure 3-6: Experimental Community Compositions." Clean white background, flat circle icons, academic style. Suitable for a thesis methods chapter.
```

---

### Visual 7: The Prosocial Advantage — Emergent Reciprocity Cycle

**Type:** Causal loop / Feedback cycle diagram
**Placement:** Ch.5 §5-2 (Summary of Findings) or Ch.4 §4-3 (Agent-Type Comfort Differences)
**Caption:** Figure 5-1: The emergent reciprocity mechanism. Prosocial agents who share surplus early in the day receive energy from neighbours later, producing higher individual comfort alongside higher community fairness.

**Description:**
A circular causal loop diagram. Start at top: "Prosocial Agent Shares Surplus (10 AM–4 PM)" → arrow down to "Neighbour's Battery Stabilized" → arrow to "Neighbour Has Energy to Share Later (Evening)" → arrow to "Prosocial Agent Receives Energy During Deficit Hours" → arrow back up to top (reinforcing loop). Alongside, show "Selfish Agent Hoards" → arrow to "Full Battery, No Sharing" → arrow to "No Reciprocity from Neighbours" → arrow to "Lower Comfort During Deficit" (balancing/dead-end). Use green arrows for virtuous cycle, red for vicious cycle. Add a "+" sign at the center of the loop indicating it's a reinforcing feedback loop.

**AI Prompt:**
```
Create a causal loop diagram for a thesis showing the emergent reciprocity mechanism in energy sharing. Circular layout.

Bottom half (virtuous cycle, green arrows):
Start at top: "Prosocial Agent Shares Surplus (10 AM–4 PM)" (green box) → arrow curving right → "Neighbour's Battery Stabilized" (green box) → arrow → "Neighbour Returns Energy Later (Evening)" (green box) → arrow → "Prosocial Agent Receives During Deficit Hours" (green box) → arrow curving back up → "Higher Individual Comfort + Community Fairness." A "+" symbol in the center of this loop labeled "Reinforcing Feedback."

Top half (vicious cycle, red arrows):
"Selfish Agent Hoards Surplus" (red box) → arrow curving left → "Battery Full, No Sharing" (red box) → arrow → "Neighbour Has No Reciprocity" (red box) → arrow → "Selfish Agent Faces Deficit Alone" (red box) → arrow → "Lower Comfort, No Community Benefit."

Title at top: "Figure 5-1: The Emergent Reciprocity Mechanism." Clean academic style, sans-serif font, white background. Suitable for a PhD thesis.
```

---

### Visual 8: The Innovator Effect Mechanism

**Type:** Causal chain diagram
**Placement:** Ch.4 §4-9 (The Innovator Effect)
**Caption:** Figure 4-7: The Innovator Effect causal mechanism. A single high-Openness agent (ε_min=0.05) destabilises cooperative equilibria through neighbour unpredictability.

**Description:**
A left-to-right causal chain. Start: "Innovator Agent (ε_min=0.05 instead of 0.01)" → arrow → "Continues Random Exploration After Others Converged" → arrow → "Neighbours Cannot Form Stable Expectations About Energy Availability" → arrow → "Neighbours Shift to Defensive Hoarding Strategies" → three downward arrows from this box: "↑ Gini Coefficient (+22%)", "↓ Community Comfort (−2.0%)", "↑ Blackout Rate (+8.3%)" with the exact values from Table 4-8. Use red/dark colors for negative outcomes. Include a comparison inset box: "Mixed Scenario (no innovator): Gini = 0.079, Comfort = 0.920" vs "Innovator Effect: Gini = 0.096, Comfort = 0.902."

**AI Prompt:**
```
Create a causal chain diagram for a thesis illustrating the Innovator Effect mechanism. Left-to-right flow.

Box 1 (left): "Innovator Agent: ε_min = 0.05 (vs 0.01 standard)" in purple — label "Higher Openness (OCEAN)."
Arrow right →
Box 2: "Continues Random Exploration After Others Converged" — label "Alter-Exploration Problem."
Arrow right →
Box 3: "Neighbours Cannot Form Stable Expectations" — label "Unpredictable Energy Availability."
Arrow right →
Box 4: "Neighbours Shift to Defensive Hoarding" — label "Self-Protective Strategy."

From Box 4, three downward arrows (red/dark) to three outcome boxes:
1. "↑ Gini Coefficient +22% (0.079 → 0.096)" with an upward red arrow.
2. "↓ Community Comfort −2.0% (0.920 → 0.902)" with a downward red arrow.
3. "↑ Blackout Rate +8.3% (14.5% → 15.7%)" with an upward red arrow.

Inset comparison box (bottom right): "Mixed Scenario: Gini 0.079, Comfort 0.920, Blackouts 14.5% | Innovator Effect: Gini 0.096, Comfort 0.902, Blackouts 15.7%." Title at top: "Figure 4-7: The Innovator Effect Mechanism." Clean academic white background. Suitable for a PhD thesis.
```

---

### Visual 9: Tragedy of the Commons — Energy Sharing Analogy

**Type:** Side-by-side comparison / Analogy diagram
**Placement:** Ch.1 §1-1 (Statement of the Problem) or Ch.2 §2-2-1
**Caption:** Figure 1-1: The tragedy of the commons in energy sharing. Left: Hardin's pasture — each herder adds cattle until the pasture is destroyed. Right: Energy microgrid — each household hoards surplus until the community suffers cascading blackouts.

**Description:**
A two-panel comparison. **Left panel (Traditional):** A green pasture with cattle, fence, "Tragedy of the Commons (Hardin, 1968)" label. Several cows, overgrazed patches. **Right panel (Energy Analogy):** A ring of 10 houses. Some houses have high battery charge (green), some are empty (red). Arrows showing surplus being discarded (waste) and deficits becoming blackouts. Center text between the two panels: "Analogous Social Dilemma: Individual Rationality → Collective Irrationality." Use consistent visual language across both panels.

**AI Prompt:**
```
Create a side-by-side analogy diagram for a thesis. Split into two panels with a vertical divider.

LEFT PANEL — "Tragedy of the Commons (Hardin, 1968)": A simple green pasture illustration with a fence. 5–6 cartoon cows grazing. One area of the pasture is overgrazed (brown/dirt). A farmer is adding another cow. Label: "Each herder maximises their own benefit → resource is destroyed."

RIGHT PANEL — "Energy Sharing Analogy (This Study)": A ring of 10 simple house icons with solar panels. 3 houses are green with "FULL" battery labels. 3 houses are red with "BLACKOUT" or "DEPLETED" labels. Arrows show surplus energy being discarded (waste symbol) from full houses. Label: "Each household hoards → surplus wasted, neighbours blackout."

Center between panels: Large text — "Individual Rationality → Collective Irrationality."

Title at top: "Figure 1-1: The Tragedy of the Commons in Energy Sharing." Clean academic style, flat illustrations, white background. Suitable for a thesis introduction chapter.
```

---

### Visual 10: State-of-the-Art Comparison

**Type:** Horizontal bar chart (comparison)
**Placement:** Ch.4 §4-10 (Comparison with State-of-the-Art)
**Caption:** Figure 4-8: Comparison with state-of-the-art energy MARL studies. The Mixed scenario of this study achieves the highest community comfort and Jain's fairness index among all comparison studies.

**Description:**
A grouped horizontal bar chart. Y-axis: study names (Charbonnier 2022, May & Huang 2023, Kusatake 2023, Behrunani 2023, Aloor 2024, This Study — Mixed). Two bars per study side by side: Community Comfort (blue) and Jain's Fairness Index (green). X-axis: 0.80–0.95 score range. This Study's bars should be visually highlighted (e.g., slightly brighter color or outlined) to draw attention. Include data values at the end of each bar. Add a footnote: "† Values estimated from published figures."

**AI Prompt:**
```
Create a horizontal grouped bar chart comparing this thesis against 5 prior studies. Y-axis (vertical, left): Study names in this order from top to bottom: "Charbonnier et al. (2022)", "May & Huang (2023)", "Kusatake et al. (2023)", "Behrunani et al. (2023)", "Aloor et al. (2024)", "This Study — Mixed (OCEAN-MARL)". X-axis (horizontal, bottom): Score range from 0.80 to 0.95.

For each study, two bars side by side:
- "Community Comfort" in blue
- "Jain's Fairness Index" in orange/green

Data from Table 4-9:
Charbonnier: comfort≈0.91, fairness=not reported (show only comfort bar)
May & Huang: comfort≈0.89, fairness=not reported
Kusatake: comfort≈0.89, fairness≈0.90
Behrunani: comfort≈0.88, fairness≈0.88
Aloor: comfort≈0.90, fairness≈0.89
This Study: comfort≈0.920, fairness≈0.923 (highlight these bars with a brighter shade and an outline)

Add data labels at the end of each bar. Add a legend. Footnote at bottom: "† Values estimated from published figures." Title: "Figure 4-8: Comparison with State-of-the-Art Energy MARL Studies." Clean academic style, white background, sans-serif font.
```

---

### Visual 11: Lorenz Curve — Gini Coefficient Illustration

**Type:** Line chart (2 Lorenz curves)
**Placement:** Ch.4 §4-4 (Inequality Analysis)
**Caption:** Figure 4-9: Lorenz curves of comfort distribution for the Mixed scenario (Gini=0.079) and Innovator Effect scenario (Gini=0.096). The Innovator Effect's greater deviation from the line of perfect equality reflects its 22% higher inequality.

**Description:**
A standard Lorenz curve chart. X-axis: Cumulative share of houses (0–100%, poorest to richest). Y-axis: Cumulative share of comfort (0–100%). Three lines: (1) Perfect equality diagonal (45° dashed gray line), (2) Mixed scenario (blue, close to diagonal), (3) Innovator Effect (red, further below). Shade the area between each line and the diagonal to visualize the Gini coefficient. Add Gini value annotations next to each curve. Use the actual data: Mixed Gini=0.079, Innovator Gini=0.096.

**AI Prompt:**
```
Create a Lorenz curve chart for a thesis showing inequality in comfort distribution. X-axis: "Cumulative Share of Houses (poorest → richest)" from 0% to 100%. Y-axis: "Cumulative Share of Comfort" from 0% to 100%.

Three lines:
1. "Perfect Equality" — a dashed gray 45-degree diagonal line from (0,0) to (100,100).
2. "Mixed Scenario (Gini = 0.079)" — blue solid line, very close to the diagonal, barely deviating.
3. "Innovator Effect (Gini = 0.096)" — red solid line, visibly below the blue line, a clear gap from the diagonal.

Shade the area between each curve and the diagonal lightly in matching transparent colors. Annotate each curve with its Gini value. Add a legend. The Innovator Effect curve should be noticeably further from the diagonal. Title: "Figure 4-9: Lorenz Curves — Mixed vs. Innovator Effect." Clean academic style, white background.
```

---

## Part B — Data-Driven Charts (Best Generated Programmatically)

These are quantitative result figures. Generate them with matplotlib/seaborn or equivalent plotting library for numerical accuracy, then embed as images.

---

### Visual 12 (Fig 3-1): System Architecture Flowchart

**Type:** Block flowchart (already in thesis as pseudocode)
**Data source:** Algorithm 3-1 in §3-8
**Description:** 10-block simulation loop. Should match the ASCII flowchart already in the thesis. Blocks: (1) Reset Environment, (2) Solar Generation (Eq. 3-1), (3) Demand Realisation (4 profiles), (4) State Observation (hour, batt%), (5) Energy Sharing (ε-greedy from Q), (6) Reward Computation (Eq. 3-2 to 3-4), (7) Q(s,a) Update (Eq. 3-5), (8) ε-decay (ε ← ε × 0.999), (9) Next Hour or End Episode (t=0..23), (10) Episode Complete → Record Metrics. Use the ASCII art in the thesis as the exact reference.

**AI Prompt:**
```
Create a 10-block system architecture flowchart for a simulation loop in a reinforcement learning thesis. The blocks should be arranged in a circular/sequential layout from top-left, flowing clockwise.

Block 1: "Reset Environment (battery 50%, weather draw)" 
Block 2: "Solar Generation (half-sine, Eq. 3-1)"
Block 3: "Demand Realisation (4 profiles)"
Block 4: "State Observation (hour, battery level)"
Block 5: "Energy Sharing (ε-greedy from Q-table)"
Block 6: "Reward Computation (Eq. 3-2 to 3-4)"
Block 7: "Q(s,a) Update (Eq. 3-5: Q = Q + α[R + γmaxQ' - Q])"
Block 8: "ε-decay (ε = max(ε_min, ε × 0.999))"
Block 9: "Next Hour (h+1) or End Episode (h=23)"
Block 10: "Record Metrics (every 100 episodes)"

Connect blocks with arrows in sequence 1→2→3→4→5→6→7→8→9→10, with block 9 looping back to block 4 via a curved arrow labeled "h < 23". Block 10 loops back to block 1 via an arrow labeled "next episode." Use blue filled boxes with white text, clean sans-serif font. Title: "Figure 3-1: System Architecture Flowchart." White background, academic style.
```

---

### Visual 13 (Fig 4-1): Community-Level Metrics Across Five Scenarios

**Type:** Grouped bar chart (3 panels or 1 grouped chart)
**Data source:** Table 4-1
**Data:**
| Scenario | Comfort | Jain's Fairness | Blackout Rate | Energy Waste |
|---|---|---|---|---|
| All Selfish | 0.920±0.010 | 0.922±0.010 | 14.5%±1.4% | 4.98±0.50 |
| All Prosocial | 0.914±0.011 | 0.918±0.011 | 14.5%±1.4% | 4.41±0.74 |
| Mixed | 0.920±0.007 | 0.923±0.008 | 14.5%±1.4% | 4.34±0.55 |
| Varied Altruism | 0.914±0.007 | 0.919±0.006 | 14.5%±1.4% | 4.96±0.54 |
| Innovator Effect | 0.902±0.008 | 0.907±0.009 | 15.7%±1.1% | 4.70±0.27 |

**AI Prompt:**
```
Create a grouped bar chart with 4 panels for a thesis, showing community-level metrics across 5 scenarios. X-axis for all panels: 5 scenario names — "All Selfish", "All Prosocial", "Mixed", "Varied Altruism", "Innovator Effect."

Panel A (top left): "Mean Community Comfort" Y-axis 0.89-0.93. Bars: All Selfish 0.920, All Prosocial 0.914, Mixed 0.920, Varied Altruism 0.914, Innovator Effect 0.902.

Panel B (top right): "Jain's Fairness Index" Y-axis 0.89-0.93. Bars: All Selfish 0.922, All Prosocial 0.918, Mixed 0.923, Varied Altruism 0.919, Innovator Effect 0.907.

Panel C (bottom left): "Blackout Day Rate" Y-axis 13-17%. Bars: All Selfish 14.5, All Prosocial 14.5, Mixed 14.5, Varied Altruism 14.5, Innovator Effect 15.7.

Panel D (bottom right): "Energy Waste (kWh/day)" Y-axis 3.5-5.5. Bars: All Selfish 4.98, All Prosocial 4.41, Mixed 4.34, Varied Altruism 4.96, Innovator Effect 4.70.

Add error bars (±1 standard deviation). Color bars: All Selfish=red, All Prosocial=green, Mixed=blue, Varied Altruism=yellow, Innovator Effect=purple. Overall title: "Figure 4-1: Community-Level Metrics Across Five Scenarios." Clean academic style, white background, sans-serif font.
```

---

### Visual 14 (Fig 4-2): Prosocial vs Selfish Agent Comfort

**Type:** Paired bar chart
**Data source:** Table 4-2
**Data:**
| Scenario | Prosocial Comfort | Selfish Comfort | Gap |
|---|---|---|---|
| Mixed | 0.935±0.007 | 0.905±0.010 | +2.9 pp** |
| Varied Altruism | 0.924±0.009 | 0.904±0.012 | +2.0 pp* |
| Innovator Effect | 0.912±0.011 | 0.892±0.008 | +1.9 pp |

**AI Prompt:**
```
Create a paired bar chart for a thesis showing prosocial vs selfish agent comfort in mixed-type communities. X-axis: 3 scenarios — "Mixed", "Varied Altruism", "Innovator Effect." For each scenario, two bars side by side: blue bar = "Prosocial Comfort" and red bar = "Selfish Comfort."

Data:
Mixed: Prosocial 0.935, Selfish 0.905 (gap +2.9pp)
Varied Altruism: Prosocial 0.924, Selfish 0.904 (gap +2.0pp)
Innovator Effect: Prosocial 0.912, Selfish 0.892 (gap +1.9pp)

Y-axis: "Mean Comfort (Last 1,000 Episodes)" from 0.87 to 0.95.

Add error bars (±1 standard deviation). Annotate each gap above the paired bars. Add asterisks for significance: Mixed "** p=0.0011", Varied Altruism "* p=0.0472". Add a legend. Title: "Figure 4-2: Prosocial vs. Selfish Agent Comfort in Mixed-Type Communities." Clean academic style, white background.
```

---

### Visual 15 (Fig 4-3): Gini Coefficient by Scenario

**Type:** Bar chart
**Data source:** Table 4-3
**Data:** Mixed 0.0790±0.0067, All Selfish 0.0796±0.0087, Varied Altruism 0.0844±0.0058, All Prosocial 0.0849±0.0098, Innovator Effect 0.0962±0.0079

**AI Prompt:**
```
Create a bar chart for a thesis showing Gini coefficients across 5 scenarios. X-axis: "Mixed", "All Selfish", "Varied Altruism", "All Prosocial", "Innovator Effect" (in this order, ranked most equal to least). Y-axis: "Gini Coefficient" from 0.07 to 0.10.

Bar heights: Mixed 0.0790, All Selfish 0.0796, Varied Altruism 0.0844, All Prosocial 0.0849, Innovator Effect 0.0962.

Add error bars (±1 standard deviation). Color bars: Mixed=green, All Selfish=blue, Varied Altruism=yellow, All Prosocial=green, Innovator Effect=red. Highlight the Innovator Effect bar with a different shade or outline since it's significantly higher. Add annotation above Innovator Effect bar: "+22% vs Mixed (p=0.008)". Title: "Figure 4-3: Gini Coefficient by Scenario." Clean academic style, white background.
```

---

### Visual 16 (Fig 4-4): Sharing Frequency by Agent Type

**Type:** Bar chart
**Data source:** Table 4-4
**Data:** All Selfish (all) 13.04%, All Prosocial (all) 12.83%, Mixed Prosocial 13.92%, Mixed Selfish 13.08%, Varied Altruism Prosocial 12.60%, Varied Altruism Selfish 12.64%, Innovator Explorers 13.33%, Innovator Selfish 13.13%

**AI Prompt:**
```
Create a bar chart for a thesis showing sharing frequency by agent type and scenario. X-axis: 8 groups labeled — "All Selfish (All)", "All Prosocial (All)", "Mixed Prosocial", "Mixed Selfish", "VA Prosocial", "VA Selfish", "Innovator Explorers", "Innovator Selfish." Y-axis: "Sharing Frequency (%)" from 10% to 16%.

Bar heights: 13.04, 12.83, 13.92, 13.08, 12.60, 12.64, 13.33, 13.13. All bars in narrow range 12.6-13.9%. Color prosocial-type bars green, selfish-type bars red.

Add error bars. Add a horizontal reference line at the overall mean (~13.1%). Title: "Figure 4-4: Proportion of Q-Table States Where Greedy Action is to Share." Clean academic style, white background.
```

---

### Visual 17 (Fig 4-5): Q-Table Heatmaps

**Type:** Heatmap grid (10 subplots)
**Data source:** §4-6
**Description:** A 2×5 or 5×2 grid of heatmaps. Each heatmap: x-axis = hour (0–23), y-axis = 3 sharing actions (0%, 50%, 100%), color = average Q-value (blue=low, yellow/red=high). Show 10 representative agents across all 5 scenarios. Reference the exact qualitative patterns described in §4-6 (All Selfish: no sharing visible; All Prosocial: midday warming for share actions; Mixed: strong sharing; Varied Altruism: altruist broadest sharing; Innovator: less concentrated).

**AI Prompt:**
```
Create a 5×2 grid of heatmaps for a thesis showing Q-values per hour for representative agents. Each heatmap: X-axis "Hour of Day" (0-23), Y-axis "Share Action" (0%, 50%, 100%), color intensity (blue=low, yellow/red=high). Title each subplot with scenario and agent.

Row 1: "All Selfish — Agent 0 (pure_selfish)" — all blue/cool colors, no warm cells.
Row 2: "All Prosocial — Agent 0 (prosocial)" — some warm (yellow) cells at hours 10-16 for 50% and 100% actions.
Row 3: "Mixed — Agent 0 (prosocial)" — stronger warm cells at hours 10-16 for sharing actions. "Mixed — Agent 3 (selfish)" — slightly warm but less intense.
Row 4: "Varied Altruism — Agent 0 (altruistic)" — broad warm region across hours 8-18 for both share actions, highest intensity. "VA — Agent 3 (individualist)" — muted warm cells only at hours 12-15.
Row 5: "Innovator Effect — Agent 0 (innovator)" — warm but less intense, scattered hours 8-18. "Innovator — Agent 8 (selfish)" — all cool/blue, weakest sharing signal.

Use a blue-to-yellow/red colormap (e.g., viridis or coolwarm). Colorbar on the right side. Overall title: "Figure 4-5: Average Q-Values Per Hour for Representative Agents." Academic style.
```

---

### Visual 18 (Fig 4-6): Sensitivity to Resource Scarcity

**Type:** Line chart with two lines + error bands
**Data source:** Table 4-6
**Data:**
| Cloud Probability | Prosocial Comfort | Selfish Comfort |
|---|---|---|
| 15% (baseline) | 0.9345±0.0063 | 0.9051±0.0086 |
| 25% | 0.8631±0.0221 | 0.8373±0.0245 |
| 35% | 0.8125±0.0271 | 0.7820±0.0142 |

**AI Prompt:**
```
Create a line chart for a thesis showing the sensitivity of prosocial vs selfish comfort to resource scarcity. X-axis: "Cloud Probability" with ticks at 15%, 25%, 35%. Y-axis: "Mean Comfort (Last 1,000 Episodes)" from 0.75 to 0.95.

Two lines:
1. "Prosocial Agents" — blue line with circle markers. Points: (15%, 0.9345), (25%, 0.8631), (35%, 0.8125). Blue shaded error band around it.
2. "Selfish Agents" — red line with square markers. Points: (15%, 0.9051), (25%, 0.8373), (35%, 0.7820). Red shaded error band.

Both lines slope downward as cloud probability increases. The gap between them stays roughly constant (~2.5-3.0 pp). Add a legend. Annotate the gap at 15%: "Gap = 2.95 pp (p=0.0034)." Add note: "Cloudy days halve solar generation (W=0.5)." Title: "Figure 4-6: Prosocial vs. Selfish Comfort as a Function of Cloudy Day Probability." Clean academic style, white background.
```

---

## Summary Table

| # | Visual | Type | Best Method | Section |
|---|--------|------|-------------|---------|
| 1 | OCEAN-to-RL Mapping | Schematic | AI Image Gen | Ch.2 §2-4 |
| 2 | Ring Topology Microgrid | Network diagram | AI Image Gen | Ch.3 §3-5 |
| 3 | Two-Phase Energy Sharing | Flowchart | AI Image Gen | Ch.3 §3-9 |
| 4 | Four Demand Profiles | Line chart | Plot programmatically | Ch.3 §3-5 |
| 5 | Solar Generation Curve | Line chart | Plot programmatically | Ch.3 §3-5 |
| 6 | Five Community Compositions | Visual matrix | AI Image Gen | Ch.3 §3-10 |
| 7 | Emergent Reciprocity Cycle | Causal loop | AI Image Gen | Ch.4 §4-3 |
| 8 | Innovator Effect Mechanism | Causal chain | AI Image Gen | Ch.4 §4-9 |
| 9 | Tragedy of the Commons Analogy | Side-by-side | AI Image Gen | Ch.1 §1-1 |
| 10 | State-of-the-Art Comparison | Bar chart | Plot programmatically | Ch.4 §4-10 |
| 11 | Lorenz Curve | Line chart | Plot programmatically | Ch.4 §4-4 |
| 12 | Fig 3-1: System Architecture | Flowchart | AI Image Gen | Ch.3 §3-8 |
| 13 | Fig 4-1: Community Metrics | Bar chart | Plot programmatically | Ch.4 §4-2 |
| 14 | Fig 4-2: Agent Comfort Split | Paired bar chart | Plot programmatically | Ch.4 §4-3 |
| 15 | Fig 4-3: Gini Coefficient | Bar chart | Plot programmatically | Ch.4 §4-4 |
| 16 | Fig 4-4: Sharing Frequency | Bar chart | Plot programmatically | Ch.4 §4-5 |
| 17 | Fig 4-5: Q-Table Heatmaps | Heatmap grid | Plot programmatically | Ch.4 §4-6 |
| 18 | Fig 4-6: Scarcity Sensitivity | Line chart | Plot programmatically | Ch.4 §4-7 |

**Recommended workflow:**
1. Generate conceptual/schematic visuals (#1–3, #6–9, #12) via AI image generator using the prompts above
2. Plot data-driven charts (#4–5, #10–11, #13–18) via matplotlib/seaborn for numerical accuracy
3. Ensure all figures use consistent fonts, color schemes, and styling
4. After generation, regenerate any containing English text in Farsi for the final Persian thesis submission
