# Other Works Compared — Implementation Audit

This document records the detailed cross-reference audit of 4 baseline methods
reproduced in `baseline_comparison.py` and their individual scripts. Each
section lists: (1) what the original paper specifies, (2) what the thesis
implements, (3) every adaptation made, and (4) a severity rating.

Severity scale:
- **CRITICAL** — core mechanism of the original paper was removed
- **HIGH** — structural change that significantly alters algorithm behavior
- **MEDIUM** — parameter or environment difference; documented in code
- **LOW** — minor cosmetic or naming difference

---

## 1. Charbonnier et al. (2022) — Marginal IQL

**Thesis script**: `charbonnier_marginal_iql.py`
**Original title**: "Optimisation-Informed Multi-Agent Q-Learning for Prosumer Energy Sharing"

### 1.1 What the original paper specifies

| Aspect | Original value |
|:-------|:---------------|
| Algorithm | Independent Q-learning with marginal rewards (MO) |
| Reward | Instantaneous same-hour counterfactual marginal reward: `r_i = F_t - F_t^(default_i)` |
| F composition | Negative sum of grid costs, distribution costs, storage costs (£) |
| Counterfactual horizon | Same-hour (instantaneous) |
| Q-update | Hysteretic (asymmetric): α₀ if δ>0, α₀β if δ≤0 |
| α₀ (base LR) | 0.01 |
| β (hysteretic factor) | 0.5 |
| γ (discount) | 0.99 |
| ε (exploration) | Fixed at 0.5 |
| Q-init | 0 |
| State space | 3 uniform grid cost intervals per day |
| Action space | 10 equal intervals of continuous ψ |
| Prosumers | Up to 30 |
| Topology | Star (central substation, no direct agent communication) |
| Battery | 75 kWh, 22 kW max charge/discharge |
| Solar | CLNR dataset input streams (peak >2 kW) |
| Weather | Historical Oxford Jan 2020/2021 |
| Time resolution | 1 hour |
| Metrics | £/h/prosumer savings, CO₂, grid costs |
| Reported result | 33.7% cost reduction (30 agents) |

### 1.2 What the thesis implements

| Aspect | Thesis value | Deviation |
|:-------|:-------------|:----------|
| Algorithm | Independent Q-learning with marginal rewards | Same principle |
| Reward | End-of-day counterfactual: `R_i = w_self·C_i + w_fair·F` | **HIGH** — different objective (comfort+fairness vs monetary cost) |
| F composition | Jain's fairness index (unitless) | **HIGH** — replaced monetary with fairness |
| Counterfactual horizon | End-of-day (hours t..23) | **MEDIUM** — documented adaptation |
| Q-update | Hysteretic (asymmetric): α₀ if δ>0, α₀β if δ≤0 | Same |
| α₀ | 0.01 | Same |
| β | 0.5 | Same |
| γ | 0.99 | Same |
| ε | Decaying: 0.5 → 0.01 (decay=0.999) | **MEDIUM** — different exploration schedule |
| Q-init | 1.0 | **HIGH** — changes exploration dynamics (optimistic init) |
| State space | 96 states (24h × 4 battery bins: 25%/50%/75%) | **HIGH** — completely different discretization |
| Action space | 3 discrete: {0%, 50%, 100%} | **HIGH** — 10× coarser than original |
| Prosumers | 10 | Different scale |
| Topology | Ring (unidirectional neighbour sharing) | **HIGH** — star vs ring changes information structure |
| Battery | 7 kWh per house | **MEDIUM** — 10× smaller |
| Solar | 1.3 kW peak, half-sine model (Eq. 3-1) | Different model |
| Weather | Bernoulli 85% clear / 15% cloudy (W=0.5) | **MEDIUM** — synthetic vs historical |
| Time resolution | 1 hour | Same |
| Metrics | Comfort (unitless), Jain's fairness (unitless), F, blackout%, waste (kWh) | **HIGH** — different metric set |

### 1.3 Validation results (thesis)

| Metric | Value |
|:-------|:------|
| Learned greedy F | 1.9057 |
| Always-default F | 1.8850 |
| Gain | +0.0207 (+1.1%) |
| Realized sharing (greedy eval) | 76.4% |
| Sharing frequency (learned policy) | 50.9% |

### 1.4 Final results (8,000 eps × 5 seeds)

| Metric | Value |
|:-------|:------|
| Comfort | 0.9401 ± 0.0066 |
| Fairness | 0.9433 ± 0.0076 |
| F | 1.8834 ± 0.0141 |
| Blackout% | 14.5 ± 0.7 |
| Waste | 4.02 ± 0.41 kWh |

### 1.5 Assessment

The **only faithful element** is the hysteretic Q-learning update rule
(α₀=0.01, β=0.5). Everything else — reward function, state/action spaces,
environment, topology, metrics — was changed. The original paper's "marginal
reward" concept (community objective minus counterfactual) is preserved in
spirit but applied to a different objective. The isolation 2×2 analysis in the
thesis identifies the hysteretic update as the actual load-bearing component,
not the marginal reward structure.

**Verdict**: Adaptation of algorithmic principle, not a faithful reproduction.

---

## 2. Kusatake et al. (2023) — NSGA-II Evolutionary MOO

**Thesis script**: `kusatake_evolutionary_moo.py`
**Original title**: "Multi-Objective Optimization for Prosumer Energy Trading"

### 2.1 What the original paper specifies

| Aspect | Original value |
|:-------|:---------------|
| Algorithm | NSGA-II (one of 6 EAs evaluated) + MPMP selection |
| Objectives | F1: maximize total prosumer benefit Σπ(vᵢ); F2: minimize std of benefits |
| Pareto selection | MPMP (Minimum Prosumer's Benefit Maximization Problem) |
| Optimization structure | Per-period (per trading instance), no learning across days |
| Decision variables | Trading quantity x + internal buying/selling prices ω |
| Population size | 10 |
| Sampling size | 10,000 |
| Battery | None specified (no storage dynamics) |
| Solar/Weather | Random generation within Japanese market ranges |
| Prosumers | 10 |
| Environment | Japanese electricity market |
| Metrics | JPY benefit, std of benefit |
| Reported result | 10.5k yen total benefit, ~0.9 std |

### 2.2 What the thesis implements

| Aspect | Thesis value | Deviation |
|:-------|:-------------|:----------|
| Algorithm | NSGA-II | Same |
| Objectives | F1: maximize comfort; F2: minimize std of comfort | **MEDIUM** — comfort proxy for monetary benefit |
| Pareto selection | argmax(F1 - F2) | **MEDIUM** — simplified from MPMP |
| Optimization structure | Per-day independent (fresh NSGA-II each day) | Same principle |
| Decision variables | Share fraction per house per hour (240 variables) | **HIGH** — prices removed entirely |
| Population size | 60 | **MEDIUM** — 6× larger than original |
| Generations | 40 | Not specified in original |
| Crossover | Uniform, prob=0.5 | Not specified in original |
| Mutation | Integer uniform re-sample, prob=1/240 | Not specified in original |
| Battery | 7 kWh per house | **HIGH** — added storage dynamics (not in original) |
| Solar | 1.3 kW peak, half-sine | Different model |
| Weather | Bernoulli 85/15 | Different model |
| Prosumers | 10 | Same count |
| Topology | Ring (unidirectional) | **HIGH** — different trading structure |
| Metrics | Comfort, Jain's fairness, F, blackout%, waste | **HIGH** — different metric set |
| Runtime | 0.211s/day, ~8.8 min total (5 seeds) | — |

### 2.3 Weather split analysis (thesis)

| Condition | Comfort | Fairness | F | N |
|:----------|:--------|:---------|:--|:--|
| Sunny days | 1.000 | 1.000 | 2.000 | ~82% |
| Cloudy days | ~0.6 | ~0.6 | ~1.2 | ~18% |

**Critical finding**: On sunny days (~82% of all days), objectives saturate at
(1.0, 0.0) for every action vector. NSGA-II has no selective pressure. The
chosen solution is essentially arbitrary. The pooled metric averages a
non-sensitive sunny-day value with a genuinely-optimized cloudy-day value.

### 2.4 Final results (500 days × 5 seeds)

| Metric | Value |
|:-------|:------|
| Comfort | 0.9387 ± 0.0064 |
| Fairness | 0.9433 ± 0.0062 |
| F | 1.8820 ± 0.0125 |
| Blackout% | 15.6 ± 1.6 |
| Waste | 4.22 ± 0.10 kWh |

### 2.5 Assessment

The core contribution of the original paper — **internal price optimization**
(ω variables) — was completely removed. The thesis only optimizes share
fractions, which is a simpler problem. The per-day independent optimization
structure is preserved, but the decision space is fundamentally different. The
saturation on sunny days means most of the "optimization" is meaningless.

**Verdict**: Adaptation with significant structural simplification. The pricing
mechanism (paper's main contribution) was removed.

---

## 3. Behrunani et al. (2023) — GNE Fairness

**Thesis script**: `behrunani_gne_fairness.py`
**Original title**: "Fairness-Aware Coordination of Multi-Energy Hubs via
Generalized Nash Equilibrium"

### 3.1 What the original paper specifies

| Aspect | Original value |
|:-------|:---------------|
| Algorithm | Semi-decentralized projected-gradient for v-GNE |
| Game structure | Bilevel: lower = economic dispatch; upper = price mediation |
| Cost function | Monetary (CHF): local assets + bilateral trades |
| Fairness mechanism | Outer-level: minimize variance of normalized cost reductions via bilateral prices |
| Update rule | Projected gradient descent with Jacobi (simultaneous) updates |
| Price mechanism | Mediators for each trade pair + central coordinator |
| Network | 3 heterogeneous hubs (industrial, medium, residential) |
| Battery | Up to 750 kWh (Hub 1) |
| Solar | Up to 2500 kW (Hub 1) |
| Environment | 3-hub Swiss energy network |
| Metrics | % cost reduction, v-GNE fairness |
| Reported result | 28% cost reduction (Hub 2), 2.5% community welfare |

### 3.2 What the thesis implements

| Aspect | Thesis value | Deviation |
|:-------|:-------------|:----------|
| Algorithm | Projected gradient descent | Same principle |
| Game structure | Single-level (no outer price level) | **CRITICAL** — bilevel structure removed |
| Cost function | Energy units: `L_i = unmet_energy + wasted_energy` (kWh) | **HIGH** — monetary → energy units |
| Fairness mechanism | Lagrangian penalty λ=1.0 in cost function | **CRITICAL** — outer price mediation removed |
| Update rule | Projected gradient descent, Jacobi updates | Same |
| Mediators | None | **CRITICAL** — semi-decentralized → fully decentralized |
| Price mechanism | None | **CRITICAL** — core contribution gone |
| Network | 10 identical houses | **HIGH** — heterogeneous hubs → homogeneous houses |
| Battery | 7 kWh × 10 houses | **HIGH** — different scale and structure |
| Solar | 1.3 kW peak per house | Different model |
| Topology | Ring (unidirectional) | **HIGH** — bilateral pairs → ring |
| Environment | 10-house residential ring microgrid | Completely different |
| Metrics | Comfort, fairness, blackout%, waste | Different metric set |
| Convergence | ~9.46 iterations per donor-hour (max 10) | — |

### 3.3 Final results (500 days × 5 seeds)

| Metric | Value |
|:-------|:------|
| Comfort | 0.9171 ± 0.0084 |
| Fairness | 0.9215 ± 0.0080 |
| F | 1.8386 ± 0.0164 |
| Blackout% | 15.6 ± 1.6 |
| Waste | 0.00 ± 0.00 kWh |

**Notable**: Zero waste is mechanistically explained — each agent minimizes its
own waste in each hour, so no surplus is ever wasted. This comes at the cost of
lower community comfort (no cross-hour battery coordination).

### 3.4 Assessment

The **entire bilevel structure** (the paper's main contribution) was removed.
The outer-level price mediation — which is what enforces fairness in the
original — was replaced with a simple Lagrangian penalty. The monetary cost
function was replaced with energy units. The heterogeneous 3-hub network was
replaced with 10 identical houses. This is the most structurally divergent
adaptation among the four baselines.

**Verdict**: Adaptation with critical structural removals. The fairness mechanism
(price mediation) — the paper's core contribution — was entirely absent.

---

## 4. May & Huang (2023) — PPO

**Thesis script**: `may_huang_ppo.py`
**Original title**: "Two-Level Multi-Agent Reinforcement Learning for
Cooperative Energy Trading"

### 4.1 What the original paper specifies

| Aspect | Original value |
|:-------|:---------------|
| Algorithm | Independent PPO (IPPO) with bi-level architecture |
| Architecture | Two-level: outer planner + inner prosumers |
| Planner observation | Grid prices, previous dynamic price, community energy mismatch |
| Planner action space | 42 dimensions: 41 price increments ε ∈ {-1+0.05n : n≤40} + NO-OP |
| Planner LR | 0.0001 |
| Prosumer network | 2 × 256 hidden units, tanh activations, softmax output |
| Prosumer observation | Prices, load, PV supply, SoC, battery capacity, accumulated costs/incomes, invalid action counts |
| Prosumer actions | 4 discrete: {buy, sell, store, NO-OP} |
| Reward | Marginal utility (change in accumulated income - costs) |
| γ | 0.998 |
| GAE λ | 0.98 |
| Gradient clip | 10 |
| Train batch size | 4000 |
| SGD minibatch | 1000 |
| Rollout size | 200 transitions |
| Entropy coeff | 0.025 (agent), 0.125 (planner) |
| Prosumers | 50 households |
| Environment | Virtual Swedish community (Ludvika) |
| Battery | Heterogeneous (variable per household) |
| Weather | Swedish historical local weather |
| Metrics | SEK net loss, self-sufficiency, Gini index |
| Reported result | 28.64% community net loss reduction |

### 4.2 What the thesis implements

| Aspect | Thesis value | Deviation |
|:-------|:-------------|:----------|
| Algorithm | Independent PPO | Same name, but single-level |
| Architecture | Single-level (prosumers only) | **CRITICAL** — half the algorithm removed |
| Planner | None | **CRITICAL** — core contribution gone |
| Prosumer network | 2 × 32 hidden units | **HIGH** — 8× smaller |
| Prosumer observation | [hour/24, battery_frac, demand_norm, solar_norm, community_surplus_norm] | **HIGH** — different features |
| Prosumer actions | 3 discrete: {0%, 50%, 100% share} | **HIGH** — different semantics |
| Reward | Comfort + Jain's fairness | **HIGH** — different objective |
| γ | 0.99 | **MEDIUM** — slightly different |
| GAE λ | 0.98 | Same |
| Gradient clip | 0.5 | **HIGH** — 20× smaller |
| Train batch size | 256 | **HIGH** — 15× smaller |
| Rollout size | 2048 transitions | **HIGH** — 10× larger |
| Entropy coeff | 0.01 | **MEDIUM** — different |
| Prosumers | 10 | Different scale |
| Battery | 7 kWh × 10 houses | Different |
| Topology | Ring | **HIGH** — different structure |
| Weather | Bernoulli 85/15 | Different |
| Metrics | Comfort, fairness, F, blackout%, waste | Different |

### 4.3 Sanity check results (thesis, 800 eps, seed 42)

| Metric | Value |
|:-------|:------|
| Policy loss trend | 0.0082 → 0.0075 (downward) |
| Value loss trend | 542 → 427 (downward) |
| Entropy | 99% of max ln(3) — near random |
| Learned greedy F | 1.8620 |
| Always-default F | 1.8850 |
| Gain | **-0.0230 (WORSE than default)** |

### 4.4 Final results (8,000 eps × 5 seeds)

| Metric | Value |
|:-------|:------|
| Comfort | 0.9058 ± 0.0089 |
| Fairness | 0.9085 ± 0.0084 |
| F | 1.8143 ± 0.0173 |
| Blackout% | 17.3 ± 3.3 |
| Waste | 4.66 ± 0.43 kWh |

### 4.5 Assessment

This is the **least faithful reproduction**. The bi-level architecture IS the
paper's main contribution — the planner coordinates the community through
dynamic pricing. Removing it means PPO has no mechanism to learn cooperative
behavior. The near-maximum entropy confirms the policy is essentially random.
The 256→32 hidden unit reduction and 10→0.5 gradient clip change further
degrade learning capacity. The comparison is unfair to the original paper — it
compares OCEAN-MARL against a crippled version of May & Huang.

**Verdict**: The most structurally divergent adaptation. The paper's core
contribution (bi-level planner) was entirely absent. PPO fails as expected.

---

## 5. Cross-Paper Summary Table

| Aspect | Charbonnier | Kusatake | Behrunani | May & Huang |
|:-------|:------------|:---------|:----------|:------------|
| **CRITICAL deviations** | 0 | 0 | 3 | 2 |
| **HIGH deviations** | 5 | 3 | 3 | 5 |
| **MEDIUM deviations** | 2 | 2 | 0 | 3 |
| Core mechanism removed? | No (hysteretic Q preserved) | Yes (prices removed) | Yes (price mediation removed) | Yes (planner removed) |
| Faithful reproduction? | Partial | Partial | Low | Very low |
| Does it beat always-default? | Yes (+1.1% F) | Yes (+0.7% F) | No (-0.6% F) | No (-1.9% F) |

## 6. Original vs Thesis Environment Comparison

| Feature | Charbonnier | Kusatake | Behrunani | May & Huang | **Thesis** |
|:--------|:------------|:---------|:----------|:------------|:-----------|
| Prosumers | 30 | 10 | 3 hubs | 50 | **10** |
| Topology | Star | Bilateral pairs | Bilateral pairs | Centralized | **Ring** |
| Battery | 75 kWh | None | 750 kWh | Variable | **7 kWh** |
| Solar | CLNR data | Random Japanese | 2500 kW | Swedish data | **1.3 kW peak** |
| Weather | Historical UK | Random | Perfect forecast | Historical Swedish | **Bernoulli 85/15** |
| Time res. | 1 hour | Instantaneous | 24-hour | 1 hour | **1 hour** |
| Prices | Yes (grid tariff) | Yes (internal) | Yes (bilateral) | Yes (dynamic) | **None** |
| Metrics | £ savings, CO₂ | JPY benefit | % cost reduction | SEK net loss | **Comfort, fairness** |

## 7. Honest Assessment for Thesis

### What the thesis does well
1. All 4 methods run in the **identical environment** (not copied from papers)
2. Each has **validation/sanity checks** before full runs
3. **Adaptations are documented** in code comments
4. The isolation 2×2 analysis identifies the **actual causal factor**
   (hysteretic update rule)
5. Results are reported **honestly** — OCEAN-MARL mixed does not outperform
   Charbonnier (p=0.012) or Kusatake (p=0.002)

### What the thesis should clarify
1. These are not faithful reproductions — they are **adaptations of algorithmic
   principles** to a fundamentally different environment
2. The "comparison with state of the art" framing is misleading when baselines
   were stripped of their core mechanisms (prices, planners, mediators)
3. The fair framing would be: "we adapted 4 algorithmic principles to our
   environment and found that hysteretic Q-learning works best"
4. The original papers' reported results are **not directly comparable** because
   environments differ in every dimension (topology, battery, solar, weather,
   metrics, prices)

### Why the results make sense
- **Charbonnier wins** because hysteretic Q-learning stabilizes multi-agent
  learning in ANY environment — it's a robust algorithmic principle
- **Kusatake does well** because per-day optimization is a strong oracle-style
  baseline (but saturates on 82% of days)
- **Behrunani has zero waste** because per-hour myopic optimization always
  minimizes individual waste — but no cross-hour battery coordination hurts
  comfort
- **May & Huang fails** because PPO without a coordinator has no mechanism to
  learn cooperative sharing — the planner IS the algorithm

### Recommended thesis language change

Instead of: "Comparison with State-of-the-Art Energy MARL Studies"

Consider: "Adaptation of Algorithmic Principles from Related Work"

This more accurately reflects what was done and avoids implying that the
numerical results are directly comparable across different environments.

---

*Last updated: 2026-08-17*
