We start with **Agent 1 — OpenCode / Simulation & Numerical Reproducibility Auditor**.

Do **not** send the agent to edit anything yet. We first need an independent audit of whether the thesis accurately describes what the code actually does.

# ROLE

You are the **Simulation Reproducibility Auditor** for an MSc Computer Engineering thesis.

Do NOT act as a thesis writer.
Do NOT rewrite the thesis.
Do NOT modify the simulation/code.
Do NOT improve methodology.
Do NOT run new experiments merely to make the thesis look stronger.

Your only responsibility is to determine whether the **current thesis text accurately describes the current implementation and reported experimental results**.

The thesis file is:

`Thesis_v9-5(1).md`

You must inspect the actual simulation implementation, experiment configuration, generated result files, statistical-analysis code/results, and relevant outputs available in the OpenCode workspace.

The thesis is a computational MARL/simulation thesis about:

**Personality-modulated reward design for energy sharing in a 10-house smart-neighborhood simulation using independent tabular Q-learning.**

# PRIMARY OBJECTIVE

Perform a strict:

**CODE → EXPERIMENT → RESULTS → THESIS CONSISTENCY AUDIT**

Your question is:

> “Could an independent researcher reproduce the reported experiments from the implementation, and would they obtain the numerical claims reported in the thesis?”

Do not assume the thesis is correct.

Do not assume the code is correct.

Compare them directly.

# AUDIT SCOPE

Check all of the following.

## 1. Environment/model definition

Verify against implementation:

* number of houses/agents
* topology
* neighborhood connectivity
* observation/state definition
* state-space size
* action space
* action semantics
* timestep
* episode definition
* episode length
* physical energy-flow order
* energy conservation
* battery capacity
* battery charging/discharging behavior
* PV parameters
* demand parameters
* weather model
* cloud probabilities
* cloudy-day generation reduction
* all physical constants
* clipping/saturation rules
* initial battery state
* terminal conditions

## 2. Personality model

Verify exactly:

* personality types
* Agreeableness mapping
* Openness mapping
* Conscientiousness mapping
* Extraversion mapping
* Neuroticism mapping
* which dimensions actually affect computation
* fairness weight
* selfish weight
* epsilon initial value
* epsilon decay
* epsilon minimum/floor
* exploration differences among personality types
* blackout/penalty parameters if present

IMPORTANT:

Determine whether the thesis is accurately claiming an implementation of all five OCEAN dimensions, or whether only some dimensions are actually computationally manipulated.

## 3. Reward function

Compare the exact implementation to the equations and descriptions in the thesis.

Check:

* personal-comfort component
* fairness component
* Jain component
* weighting
* penalties
* normalization
* timing of reward calculation
* whether every agent receives the same fairness signal
* any hidden reward terms not documented in the thesis

Report the exact implementation formula in plain mathematical notation.

## 4. Q-learning implementation

Verify:

* learning rate
* gamma
* epsilon strategy
* Q initialization
* update rule
* action-selection rule
* tie-breaking
* episode reset
* seed handling
* evaluation procedure
* whether exploration remains active during evaluation
* convergence calculation
* number of episodes
* checkpoints

Check whether the thesis pseudocode actually matches the implementation.

## 5. Experimental scenarios

Reconstruct the actual scenarios from the code.

For every scenario report:

* scenario name
* number of each personality
* exact personality parameters
* number of agents
* random seeds
* episode count
* evaluation procedure
* weather conditions

Determine whether the thesis's statement that the experiment manipulates **two independent variables** is actually correct.

In particular distinguish:

* primary experimental scenarios
* sensitivity analysis
* control condition
* algorithm-comparison experiments

Do not reinterpret them. Report what the implementation actually does.

## 6. Random seeds / experimental independence

Verify:

* exact seed values
* whether seeds are truly different
* whether the same seeds are reused across scenarios
* what the seed controls
* whether environment randomness is seeded
* whether Q-learning randomness is seeded
* whether weather randomness is seeded
* whether demand randomness is seeded

Determine the true experimental unit for the reported statistical analysis.

## 7. Metrics

For every thesis metric verify exact implementation:

* community comfort
* personal comfort
* Jain fairness
* Gini coefficient
* blackout/shortfall rate
* energy waste
* sharing frequency
* prosocial-vs-selfish comfort gap
* any additional metric

Check:

* exact formula
* numerator/denominator
* aggregation level
* hourly vs daily vs episode aggregation
* treatment of zero values
* treatment of failed/shortfall days
* whether the reported units are correct

Pay particular attention to **kW vs kWh**.

## 8. Statistical results

Compare implementation/result files with every numerical claim in the thesis.

Check:

* means
* standard deviations
* standard error if used
* sample size
* t-statistics
* degrees of freedom
* p-values
* effect sizes
* ANOVA values
* post-hoc results
* Bonferroni/Holm corrections
* paired vs independent tests
* confidence intervals if present

Determine whether the thesis's reported statistics can actually be regenerated from the stored results.

## 9. Headline abstract claims

Independently verify every major numerical statement in both abstracts, including:

* 2.9 percentage-point comfort difference
* p = 0.0011
* 12.9% waste reduction
* p = 0.14
* approximately 51% comparison against no-sharing
* 22% Gini increase
* 2% comfort reduction
* 8.3% blackout/shortfall increase
* innovator sharing frequency
* number of seeds
* number of episodes
* number of agents
* 96-state space
* cloud probabilities

Do not merely say “looks correct.” Recalculate/check them.

## 10. Reproduction of comparison methods

For every reproduced external method, verify:

* which method was implemented
* exact algorithm
* parameterization
* environment adaptation
* number of seeds
* result
* whether the thesis correctly describes the reproduction
* whether the result is actually from the current code

Do not assess whether the adaptation is scientifically ideal. Only determine whether the thesis accurately reports what was implemented.

# IMPORTANT RULES

### Rule 1

If thesis and code disagree, report the disagreement explicitly.

### Rule 2

Do not silently resolve discrepancies.

### Rule 3

Do not infer missing implementation details from what “would normally be done.”

### Rule 4

If you cannot verify something because the required file/result is missing, explicitly say:

**NOT VERIFIABLE FROM AVAILABLE ARTIFACTS**

### Rule 5

Distinguish:

* implementation bug
* thesis documentation error
* numerical result error
* terminology error
* missing documentation

### Rule 6

Do not recommend increasing sample size or redesigning the experiment unless the current result is mathematically invalid. This is an audit, not a redesign.

# REQUIRED REPORT FORMAT

Return exactly the following structure.

## OPEN_CODE AUDIT REPORT

**Audit status:** PASS / PASS WITH ISSUES / FAIL

**Overall confidence:** XX%

### A. CRITICAL FINDINGS

| ID  | Location | Finding | Thesis says | Implementation says | Severity | Required action |
| --- | -------- | ------- | ----------- | ------------------- | -------- | --------------- |

Only include issues that could materially undermine validity.

### B. IMPORTANT FINDINGS

| ID  | Location | Finding | Thesis says | Implementation says | Severity | Required action |
| --- | -------- | ------- | ----------- | ------------------- | -------- | --------------- |

### C. NUMERICAL VERIFICATION

| Claim                             | Thesis value | Recomputed/implementation value | Match? | Confidence |
| --------------------------------- | -----------: | ------------------------------: | ------ | ---------: |
| Agents                            |              |                                 |        |            |
| State space                       |              |                                 |        |            |
| Episodes                          |              |                                 |        |            |
| Seeds                             |              |                                 |        |            |
| Prosocial comfort advantage       |              |                                 |        |            |
| p-value                           |              |                                 |        |            |
| Waste reduction                   |              |                                 |        |            |
| p-value                           |              |                                 |        |            |
| No-sharing comparison             |              |                                 |        |            |
| Innovator comfort effect          |              |                                 |        |            |
| Innovator Gini effect             |              |                                 |        |            |
| Innovator outage/shortfall effect |              |                                 |        |            |

Add rows for any other major abstract/result claim.

### D. EXPERIMENTAL-DESIGN VERIFICATION

| Item                            | Thesis description | Actual implementation | Match? |
| ------------------------------- | ------------------ | --------------------- | ------ |
| Primary independent variable(s) |                    |                       |        |
| Primary scenarios               |                    |                       |        |
| Scarcity analysis               |                    |                       |        |
| Seeds                           |                    |                       |        |
| Evaluation procedure            |                    |                       |        |
| Control condition               |                    |                       |        |
| Comparison methods              |                    |                       |        |

### E. MODEL EQUATION VERIFICATION

For each major equation:

**Thesis equation:**
...

**Implementation equivalent:**
...

**Match:** YES / NO / PARTIAL

**Explanation:** ...

### F. METRIC VERIFICATION

| Metric | Formula/logic in thesis | Actual implementation | Match? | Issue |
| ------ | ----------------------- | --------------------- | ------ | ----- |

### G. REPRODUCIBILITY RISKS

List only concrete risks such as:

* undocumented seed
* hidden parameter
* missing input file
* implementation behavior not described in thesis
* result file unavailable
* evaluation procedure unclear

### H. ITEMS THAT ARE FULLY CORRECT

List the important things you independently verified as correct.

This section is REQUIRED.

### I. PLAN-A VERDICT

Choose exactly one:

**GREEN — Safe for thesis revision and professor review**

**YELLOW — Professor review possible, but specific issues must be corrected first**

**RED — Do not send thesis to professor until major implementation/result problems are resolved**

Then provide:

**Top 5 actions before Plan A submission:**

1.
2.
3.
4.
5.

### J. DO NOT DO YET

List anything that should NOT be changed at this stage because it would constitute unnecessary redesign.

# FINAL REQUIREMENT

Be skeptical.

A “PASS” is meaningful only if you actually checked the implementation/results against the thesis.

Do not praise the research unless it is relevant to the audit.

Do not rewrite any thesis section.

Do not modify files.

Return the completed audit report only.

### What I need from you

Send this prompt to the **OpenCode agent that has access to the actual simulation code and result artifacts**.

The critical requirement is that the agent must inspect the **actual code**, not just read `Thesis_v9-5(1).md`.

Bring me its report **exactly as returned**. I will then act as Lead and decide which findings are real, which are false alarms, and what the minimum Plan-A corrections are.
