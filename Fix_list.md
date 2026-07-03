# Fix List — ACADEMIC_v3_En.md

Comprehensive issue tracking table for resolving all Professor feedback points on the thesis draft. Each row includes Priority, Issue description, Document Location, Fixed Percentage (0% = not started, 100% = fully resolved), Target Fix Agent, and Possible Solution type.

---

| # | Priority | Issue | Location | Fixed % | Target Fix Agent | Possible Solution |
|---|----------|-------|----------|---------|------------------|-------------------|
| 1 | **High** | **Missing dedicated Neutral Overall Analysis section** — No section titled "Neutral Overall Analysis" exists; the ToC references `4-10 Neutral Overall Analysis` but the actual heading is `4-10 Comparison with State-of-the-Art`. The professor explicitly requested a structured subsection at the end of results that honestly appraises: *"this was good because..., this was bad because..."* without hype. This content is currently only partially scattered across Section 5-1. | End of Section 4 (between 4-10 and 5-1) | **100%** | Researcher / Analyst | Add new subsection `4-10 Neutral Overall Analysis` after the SoTA comparison. Write 2–3 long neutral paragraphs covering: (a) methodological strengths of the approach, (b) unexpected or negative findings with honest interpretation, (c) areas where the method performed worse than expected or showed no effect. Remove the mismatched ToC entry and update accordingly. |
| 2 | **High** | **Conclusion (Section 5-2) is too short** — Currently ~10 lines. The professor requests a multi-paragraph in-depth conclusion covering: (a) what the work was, (b) why it was done, (c) what research gap existed, (d) what the proposed method was, (e) summary of results, (f) analytical explanation of *why* those results occurred, and (g) a dedicated paragraph for future works. | Section 5-2 | **100%** | Researcher | Expand Section 5-2 into 6–8 full scientific paragraphs. Restructure to cover: recap of gap → recap of proposed method → summary of key findings → analytical interpretation ("because...") → theoretical contribution → practical contribution → future works paragraph. Do not use bullet lists or slide-style numbering. |
| 3 | **Medium** | **Flowchart not explicitly tied to literature-review rationale** — Figure 3-1 and Algorithm 3-1 exist but are placed directly in Section 3 without a connecting narrative that traces back to *why* the method was designed this way based on gaps identified in Section 2. The professor wants the flowchart to serve as the logical bridge: "gap → proposed method → here is the architecture." | Section 3-1 or 3-8 (before flowchart) / Section 2-4-1 | 0% | Researcher | Add 1–2 paragraphs at the start of Section 3-1 (or immediately before the flowchart in 3-8) that explicitly trace: (a) each of the three gaps from Section 2-4, (b) how each gap motivated a specific design choice in the simulation architecture, and (c) how the flowchart blocks instantiate those design choices. Reference specific boxes in Figure 3-1. |
| 4 | **Medium** | **Insufficient justification for random seed values** — Seeds {42, 123, 456, 789, 1011} are listed with the justification "follows conventions of the literature." The professor asks: *why these specific seeds?* Were they chosen arbitrarily, through a pilot experiment, or based on a specific methodology (e.g., Taguchi, Latin hypercube)? | Section 3-2 / Section 4-1 | **100%** | Researcher / Analyst | Add a subsection or paragraph explaining seed selection methodology. Options: (a) state they were arbitrary but fixed for reproducibility with citation of reproducibility standards (e.g., Montgomery, 2017), or (b) if a specific methodology was used, describe it. Add seed range justification (not all prime/sequential, covers sufficient entropy). |
| 5 | **Medium** | **Insufficient justification for hyperparameter values (learning rate, ε-decay, episode count, seed count)** — Some hyperparameters cite Zhang et al. (2025) or Sutton & Barto (2018), but the professor wants to know the full basis: pilot experiments? Taguchi design? Black-box tuning? Directly from a specific cited paper? Specifically questioned: learning rate 0.2, ε-decay 0.999, 8,000 episodes, 5 seeds minimum ε values. | Section 3-13 / Section 3-2 | **100%** | Researcher | Expand Section 3-13 with a subsection "Hyperparameter Justification" that explains the basis for each parameter value: standard practice, cited paper, or pilot experiment. For 8,000 episodes specifically, note the convergence check (Section 4-1 mentions Q-value change < 0.01 by episode 6,000) as empirical justification. Cite Montgomery (2017) or Law (2015) for the 5-seed convention if used. |
| 6 | **Medium** | **Limitations need deeper explanation of *why* each matters** — Limitations are written as paragraphs (addressing the format complaint), but the professor wants more concrete mechanistic explanations: e.g., *why exactly* does a binary weather model limit generalisability? *What specifically* breaks if personalities are fixed? *What concrete alternative results* might a continuous state space produce? Current descriptions are decent but need expansion. | Section 5-4 (and 5-4-1 Threats to Validity) | **100%** | Researcher | Expand each of the four limitation paragraphs with: (1) a concrete consequence example, (2) a reference to empirical evidence of the consequence, and (3) how it specifically *bounds* the study's conclusions. For example, for the binary weather model: cite studies using Markov-chain weather models, explain how autocorrelated cloudy days would test a different regime of trust/reciprocity duration. For fixed personalities: cite literature on preference dynamics in repeated games. |
| 7 | **Medium** | **Flowchart boxes need explicit "what happens + why" explanations** — The professor states: *"if the flowchart is our basis, each box must be explained: what happens and what is the reason."* While Section 3-8 explains most blocks, the explanations are primarily *descriptive* (what happens) and underdeveloped on *why* (design rationale). The why-reasoning should connect back to Section 2-4 gaps. | Section 3-8 (Blocks 1–10 explanations) | **100%** | Researcher | For each of the 10 flowchart blocks, add a "Why?" sentence or sentence that connects the design choice to a research gap or literature justification. Example: Block 5 (ε-greedy) → "The ε-greedy policy was chosen because independent Q-learning requires sufficient exploration to discover sharing strategies in a non-stationary multi-agent environment (Hernandez-Leal et al., 2017), and the varying ε-min values are the direct operationalisation of the Openness dimension." |
| 8 | **Low** | **ToC entry `4-10 Neutral Overall Analysis` is mismatched with actual heading** — The table of contents lists `4-10 Neutral Overall Analysis` but the section is titled `4-10 Comparison with State-of-the-Art`, causing a structural mismatch. Once Issue #1 is addressed and a new 4-10 neutral analysis section is added, the ToC must be updated consistently. | Table of Contents (lines 50–52) / Section 4 headings | **100%** | Programmer | After adding the new neutral analysis subsection, update ToC entries to match. Likely restructure: rename current 4-10 to `4-10 Comparison with State-of-the-Art`, add new `4-11 Neutral Overall Analysis`, and renumber subsequent sections (5-Discussion becomes 5-1, etc.). Ensure all internal cross-references use updated numbering. |
| 9 | **Low** | **Section 4 lacks interpretation guidance statement** — The professor says results sections should include interpretation guidance: *"under each chart, detailed explanation of what the chart reveals."* Currently captions are adequate but could include more explicit interpretation statements (e.g., "This pattern indicates that..."). | All figure captions in Section 4 (Figures 4-1 through 4-6, and Tables 4-1 through 4-9) | **100%** | Analyst | Review each figure caption and ensure 1–2 sentences of interpretive guidance are included: what the result means, why it matters, how it connects to a hypothesis. Many captions already have good descriptions; add the "so what?" clause. |
| 10 | **Low** | **Section 5-1 (Summary of Findings) mixes summary with hyped language** — The professor says to avoid hype. Phrases like "the single most surprising finding" or "the most important extension" may overclaim. The summary of findings should be more measured. | Section 5-1 (lines 1080–1090) | **100%** | Researcher | Tone-adjust Section 5-1 sentences. Replace superlatives ("most surprising," "highest," "most important") with precise quantitative statements. Use "directionally consistent," "the largest observed effect," or "a notable finding" instead. |
| 11 | **Low** | **Parameter tables in equations could be more consistently formatted** — Some equations have parameter tables (e.g., Eq. 3-1, 3-2, 3-4, 3-5, 4-1–4-6), but a few are missing or inconsistent. The professor notes: *"all parameter tables must be explained."* | Equations throughout Sections 3-5 through 4-5 | **100%** | Programmer / Researcher | Audit all equations in Sections 3 and 4. Add a parameter table after any equation currently missing one (format: Symbol | Definition | Unit | Source). Ensure all parameters — including trivial ones like $N$, $T$, $()^+$ operator — are defined with sources. Currently most are present but a few symbols (e.g., $()^+$ in Eq. 4-4, $\varepsilon$-decay 0.999) need clearer sourcing. |
| 12 | **Low** | **Physical environment parameter sourcing needs a clear statement of "Ground Truth" methodology** — Section 3-5 and Table 3-4 list values with citations, but the professor asks: *"what is the scientific basis? Was it from prior work, pilot experiments, or a formal design of experiments?"* Need one explicit paragraph stating the methodology for parameter selection. | Section 3-5 (near Table 3-4) / Section 3-2 | **100%** | Researcher | Insert a short subsection or paragraph titled "Parameter Selection Methodology" stating that all physical and hyperparameter values were anchored to published literature (prior studies), followed by the specific citations. Where values deviated from cited ranges, note that they were chosen for consistency with the chosen topology. If any values were tuned via informal pilot experiments, state that honestly. |
| 13 | **Low** | **Research Innovations paragraph (1-3) could more explicitly contrast with each cited baseline study** — Currently Section 1-3 describes the innovation in general terms and Table 2-1 provides the detailed comparison. The professor wants the gap-to-innovation bridge to be very explicit in the early framing. | Section 1-3 (lines 89–97) | **100%** | Researcher | Add 2–3 sentences in Section 1-3 that explicitly state: relative to [X], our approach differs by [Y]; relative to [Z], we add [W]. Make the contrast with prior work explicit right where the innovation is claimed, not deferred to Table 2-1 alone. |
| 14 | **Low** | **Table 2-1 Pros/Cons column should be explicitly referenced in the narrative** — The professor's feedback point #4 requests both a Pros/Cons table *and* a narrative that connects it to the literature review conclusions. Currently the table exists and is good, but the narrative in Section 2-3 could more explicitly *chase* each row's "Con" to identify which gap this study addresses. | Section 2-3 (lines 305–327) | **100%** | Researcher | In Section 2-3, after the table, add a paragraph that works through each Con entry and states: "This Con corresponds to Gap #N in our framework." This creates a direct chain: Table 2-1 Con → Literature Gap in 2-4 → Design Response in Chapter 3. |

---

## Fix Order and Workflow

### Sprint 1 — Structural & Critical (Weeks 1–2)
1. **Issue #1 (Priority: High):** Add Section 4-10 Neutral Overall Analysis
   - Sub-tasks: Write analysis paragraphs → Remove mismatched ToC entry → Add new 4-11 → Renumber downstream sections → Update all internal cross-references
   - **Fixed %:** 0% → 100%

2. **Issue #2 (Priority: High):** Expand Section 5-2 Conclusion
   - Sub-tasks: Draft 6–8 paragraphs covering all professor-requested topics → Remove any slide-style numbering → Ensure future works paragraph is comprehensive
   - **Fixed %:** 0% → 100%

### Sprint 2 — Content & Rationale (Weeks 2–3)
3. **Issue #3 (Priority: Medium):** Bridge flowchart to literature gaps
   - Add transitional paragraphs in Section 3-1 with explicit gap-to-box mapping
   - **Fixed %:** 0% → 100%

4. **Issue #4 (Priority: Medium):** Justify random seeds
   - Add seed-selection paragraph in Section 3-2 or 4-1
   - **Fixed %:** 0% → 100%

5. **Issue #5 (Priority: Medium):** Justify hyperparameters
   - Add "Hyperparameter Justification" subsection in Section 3-13
   - **Fixed %:** 0% → 100%

6. **Issue #6 (Priority: Medium):** Deepen limitations explanations
   - Expand each of the four limitation paragraphs with concrete consequences and citations
   - **Fixed %:** 0% → 100%

### Sprint 3 — Detail & Polish (Week 3–4)
7. **Issue #7 (Priority: Medium):** Add "why" to each flowchart box
   - Append "Why this design choice?" rationale to Blocks 1–10 explanations
   - **Fixed %:** 0% → 100%

8. **Issue #8 (Priority: Low):** Fix ToC mismatch and renumber
   - Update ToC, section headings, and cross-references
   - **Fixed %:** 0% → 100%

9. **Issue #9 (Priority: Low):** Add interpretation to figure captions
   - Append 1–2 interpretive sentences to each caption
   - **Fixed %:** 50% → 100%

10. **Issue #10 (Priority: Low):** Remove hype from Section 5-1
    - Tone-adjust superlatives
    - **Fixed %:** 0% → 100%

11. **Issue #11 (Priority: Low):** Complete parameter table audit
    - Add missing tables or fill gaps in existing ones
    - **Fixed %:** 40% → 100%

12. **Issue #12 (Priority: Low):** Add parameter methodology statement
    - New subsection in Section 3-5
    - **Fixed %:** 0% → 100%

13. **Issue #13 (Priority: Low):** Strengthen innovation contrast in Section 1-3
    - Add explicit comparisons
    - **Fixed %:** 20% → 100%

14. **Issue #14 (Priority: Low):** Link Table 2-1 Cons to gaps in Section 2-3
    - Add gap-mapping paragraph
    - **Fixed %:** 30% → 100%

---

## Progress Tracking

| Sprint | Issues Targeted | Target Complete Date |
|--------|-----------------|----------------------|
| 1 | #1, #2 | Week 2 |
| 2 | #3, #4, #5, #6 | Week 3 |
| 3 | #7–#14 | Week 4 |

**Overall Completion:** 100% (14 of 14 issues fully resolved in ACADEMIC_v3_En.md)

---

*Generated: Based on Professor feedback in `Latest_Professor_Opinion.md` against draft `HamidOutput/ACADEMIC_v3_En.md`*
