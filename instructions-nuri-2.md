Here's the Charbonnier baseline spec, ready to hand to OpenCode as-is.

---

## Baseline Spec: `charbonnier_marginal_iql`

**Goal:** Reproduce Charbonnier et al. (2022)'s core mechanism — independent Q-learning with a _marginal/counterfactual reward signal_ and _hysteretic learning rates_ — inside our existing 10-house environment, replacing personality-driven reward weighting entirely. Everything else (environment, houses, PV/battery parameters, weather stochasticity, episode/seed count) stays identical to our main OCEAN-MARL runs, so this is a controlled comparison.

### 1. Environment — unchanged

- Same 10-house ring topology, same PV peak (1.3 kW), battery (7.0 kWh), cloud probability (15%), same synthetic weather generator and seeds used for the main scenarios.
- Same state space: 96 states (24 hours × 4 battery bins).
- Same action space: 3 discrete actions — share 0%, 50%, 100% of surplus.

### 2. Reward function — replace entirely

Remove the personality-weighted reward `R_i = w_self · C_i + w_fair · F`. Replace with Charbonnier's **marginal reward**:

```
r_i,t = F_t − F_t^(default_i)
```

Where:

- `F_t` = total system reward actually achieved at step t (use the same system-level metric already defined in our pipeline — comfort + fairness combined, whatever `F` currently resolves to at the system level).
- `F_t^(default_i)` = counterfactual total system reward at step t **if agent i had instead taken the default action (share 0%)**, holding all other 9 agents' actions fixed at what they actually chose.

Implementation: after the real environment step, re-run the system-level reward calculation once per agent with that agent's action swapped to 0%-share and everyone else's action unchanged (no need to re-run the full environment transition, just recompute the reward function with the substituted action vector). This gives each agent a personalized marginal-contribution signal without any personality/OCEAN input anywhere in the loop.

### 3. Q-learning update — hysteretic

Standard Q-update, but with **asymmetric learning rates** depending on the sign of the TD error:

```
δ = r_i,t + γ · max_a Q(s', a) − Q(s, a)

if δ ≥ 0:  Q(s,a) ← Q(s,a) + α · δ
if δ < 0:  Q(s,a) ← Q(s,a) + (β · α) · δ
```

### 4. Hyperparameters

| Param                    | Value                                | Note                                                                     |
| ------------------------ | ------------------------------------ | ------------------------------------------------------------------------ |
| γ (discount)             | 0.99                                 | matches Charbonnier                                                      |
| α (base learning rate)   | 0.01                                 | matches Charbonnier                                                      |
| β (hysteretic reduction) | 0.5                                  | matches Charbonnier                                                      |
| ε (exploration, initial) | 0.5                                  | matches Charbonnier's fixed value                                        |
| ε decay                  | 0.999                                | reuse our own schedule shape for comparability                           |
| ε_min                    | 0.05                                 | same floor as our "innovator" setting, for consistent exploration budget |
| Episodes                 | 8,000                                | match our main runs exactly                                              |
| Seeds                    | same 5 seeds as main OCEAN-MARL runs | required for paired statistical tests                                    |

### 5. What to remove

- Any OCEAN/personality parameter injection, per-agent fairness weight, or innovator/prosocial/selfish role assignment. This run is **role-free** — every agent uses the identical algorithm.

### 6. Output format

Produce the same metrics CSV schema already used for our main scenario runs (per-episode or per-evaluation-window: Jain's index, Gini coefficient, blackout rate, energy waste %, per-agent comfort, mean reward), one file per seed, so it plugs directly into the existing ANOVA/post-hoc pipeline without reformatting. Label this run `baseline_charbonnier` in whatever scenario-name column the pipeline uses.

### 7. Sanity check before trusting results

Before running the full 8,000×5-seed comparison, do one short validation run and report back: does the marginal reward signal actually produce sensible behavior (agents learning to share more than 0% when it benefits the system), or does something degenerate happen (e.g., all agents converge to always-default)? Paste me the summary metrics from that short run before scaling up.

---

Have OpenCode implement this, run the short validation pass, and paste me the output. Once that checks out, we scale to the full run and move to spec #2 (Kusatake).
