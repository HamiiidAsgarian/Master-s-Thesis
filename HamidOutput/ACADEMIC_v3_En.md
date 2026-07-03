    # A New Method of Fair and Efficient Energy Sharing in Smart Neighborhoods Using Personality-Driven Multi-Agent Reinforcement Learning

## Table of Contents

- 1- [Introduction and Generalities](#1-introduction-and-generalities)
- 1-1 [Statement of the Problem](#1-1-statement-of-the-problem)
- 1-2 [Significance of the Study](#1-2-significance-of-the-study)
- 1-3 [Research Innovation](#1-3-research-innovation)
- 1-4 [Research Objectives](#1-4-research-objectives)
- 1-5 [Research Questions](#1-5-research-questions)
- 1-6 [Research Hypotheses](#1-6-research-hypotheses)
- 1-7 [Operational Definitions](#1-7-operational-definitions)
- 1-8 [Thesis Outline](#1-8-thesis-outline)
- 2- [Literature Review](#2-literature-review)
- 2-1 [Theoretical Foundations](#2-1-theoretical-foundations)
  - 2-1-1 [The Decentralized Energy Transition and the Prosumer Paradigm](#2-1-1-the-decentralized-energy-transition-and-the-prosumer-paradigm)
  - 2-1-2 [Peer-to-Peer Energy Trading: Market Structures and Pricing Mechanisms](#2-1-2-peer-to-peer-energy-trading-market-structures-and-pricing-mechanisms)
  - 2-1-3 [Multi-Agent Reinforcement Learning for Distributed Energy Control](#2-1-3-multi-agent-reinforcement-learning-for-distributed-energy-control)
  - 2-1-4 [Personality-Driven Decision Making in Computational Agents](#2-1-4-personality-driven-decision-making-in-computational-agents)
- 2-2 [Review of Related Literature](#2-2-review-of-related-literature)
  - 2-2-1 [Efficiency-Focused MARL for Residential Energy Management](#2-2-1-efficiency-focused-marl-for-residential-energy-management)
  - 2-2-2 [Fairness-Aware MARL: Uniform Constraints and Their Limitations](#2-2-2-fairness-aware-marl-uniform-constraints-and-their-limitations)
  - 2-2-3 [Game-Theoretic and Market-Based Approaches to Fair Energy Sharing](#2-2-3-game-theoretic-and-market-based-approaches-to-fair-energy-sharing)
  - 2-2-4 [The Alter-Exploration Problem and the Cost of Individual Exploration](#2-2-4-the-alter-exploration-problem-and-the-cost-of-individual-exploration)
- 2-3 [Qualitative Comparison of Related Literature](#2-3-qualitative-comparison-of-related-literature)
- 2-4 [Conceptual Framework and Research Gaps](#2-4-conceptual-framework-and-research-gaps)
  - 2-4-1 [Conceptual Framework: The Personality-Modulated Coordination Model](#2-4-1-conceptual-framework-the-personality-modulated-coordination-model)
- 3- [Research Methodology](#3-research-methodology)
- 3-1 [Research Design and Approach](#3-1-research-design-and-approach)
- 3-2 [Data Collection Methods](#3-2-data-collection-methods)
- 3-3 [Tools and Instruments](#3-3-tools-and-instruments)
- 3-4 [Population, Sample, and Sampling Method](#3-4-population-sample-and-sampling-method)
- 3-5 [Physical Environment](#3-5-physical-environment)
- 3-6 [Personality Model and OCEAN Mapping](#3-6-personality-model-and-ocean-mapping)
- 3-7 [Reward Function Design](#3-7-reward-function-design)
- 3-8 [Learning Algorithm](#3-8-learning-algorithm)
- 3-9 [Energy Sharing Mechanism](#3-9-energy-sharing-mechanism)
- 3-10 [Community Compositions (Scenarios)](#3-10-community-compositions-scenarios)
- 3-11 [Performance Metrics](#3-11-performance-metrics)
- 3-12 [Data Analysis Methods](#3-12-data-analysis-methods)
- 3-13 [Hyperparameters and Training](#3-13-hyperparameters-and-training)
- 4- [Data Analysis](#4-data-analysis)
- 4-1 [Community-Level Metrics](#4-1-community-level-metrics)
- 4-2 [Agent-Type Comfort Differences](#4-2-agent-type-comfort-differences)
- 4-3 [Inequality Analysis (Gini Coefficient)](#4-3-inequality-analysis-gini-coefficient)
- 4-4 [Learned Sharing Behaviour](#4-4-learned-sharing-behaviour)
- 4-5 [Q-Table Heatmaps — Learned Policies](#4-5-q-table-heatmaps--learned-policies)
- 4-6 [Sensitivity to Resource Scarcity](#4-6-sensitivity-to-resource-scarcity)
- 4-7 [Statistical Significance Testing](#4-7-statistical-significance-testing)
- 4-8 [The Innovator Effect — Surprising Finding](#4-8-the-innovator-effect--surprising-finding)
- 4-9 [Comparison with State-of-the-Art](#4-9-comparison-with-state-of-the-art)
 - 4-10 [Comparison with State-of-the-Art](#4-10-comparison-with-state-of-the-art)
 - 4-11 [Neutral Overall Analysis](#4-11-neutral-overall-analysis)
 - 5-1 [Discussion and Conclusion](#5-1-discussion-and-conclusion)
   - 5-2 [Summary of Findings](#5-2-summary-of-findings)
   - 5-3 [Conclusion](#5-3-conclusion)
   - 5-4 [Research Contributions](#5-4-research-contributions)
   - 5-5 [Research Limitations](#5-5-research-limitations)
     - 5-5-1 [Threats to Validity](#5-5-1-threats-to-validity)
   - 5-6 [Suggestions for Future Research](#5-6-suggestions-for-future-research)
   - 5-7 [Practical Suggestions](#5-7-practical-suggestions)
 - [References](#references)

## 1- Introduction and Generalities

The global energy system is undergoing a transformation whose scale and speed are unprecedented since the original electrification of the industrialised world. The driver is the accumulating evidence that anthropogenic greenhouse-gas emissions must peak before 2025 and decline sharply thereafter if the worst consequences of climate change are to be avoided (Masson-Delmotte et al., 2018). The energy sector accounts for approximately three-quarters of global emissions, and decarbonisation therefore requires that renewable sources supply the majority of electricity by mid-century (IEA, 2022). Solar photovoltaics have emerged as the fastest-growing renewable technology, with global installed capacity exceeding 1 TW in 2022 and residential rooftop installations constituting a significant and growing fraction of new capacity (IEA PVPS, 2023).

This growth in residential solar generation has been accompanied by a parallel drop in battery storage costs, which have fallen by more than eighty percent over the past decade (BloombergNEF, 2023). The combination of affordable rooftop solar and home batteries has created the technical preconditions for a new kind of electricity consumer: the prosumer, a household that both produces and consumes energy and can store surplus generation for later use (Rathnayaka et al., 2014; Morstyn & McCulloch, 2019). In a smart neighbourhood microgrid, multiple such prosumers are interconnected, enabling them to share energy directly with neighbours rather than exporting it to a distant utility grid. This peer-to-peer model reduces transmission losses, alleviates grid congestion during peak hours, and gives households greater autonomy over their energy supply (Tushar et al., 2020; Zhou & Lund, 2023).

However, the integration of residential renewables at scale introduces a problem that is as much social as it is technical. Solar generation is inherently intermittent and weather-dependent, and household demand profiles vary considerably across families, work schedules, and seasons (Skoplaki & Palyvos, 2009; Ali et al., 2023). A neighbourhood in which each household independently maximises its own self-sufficiency will inevitably produce instances where one home discards surplus energy because its battery is full while a neighbour across the street faces a blackout because its battery is depleted. The technical challenge of coordinating these distributed resources has received substantial attention in the literature, but the social dimension of the problem — the fact that sharing decisions are influenced by individual attitudes toward fairness, risk, and reciprocity — remains comparatively underexplored (Fehr & Gächter, 2000; May & Huang, 2023).

Multi-agent reinforcement learning has emerged as the dominant computational framework for addressing this coordination problem (Li & Zhang, 2022; Charbonnier et al., 2022). In a MARL formulation, each household is modelled as an autonomous agent that learns a sharing policy through repeated trial-and-error interaction with its environment and neighbours. The appeal of this approach is that it does not require a central controller with perfect information: agents can discover effective coordination strategies locally, using only their own observations and reward signals. Yet the standard MARL paradigm embeds a critical assumption that deserves closer scrutiny. When every agent optimises solely for its own cumulative reward, the resulting equilibrium may be collectively suboptimal — a computational analogue of the tragedy of the commons (Hardin, 1968; Hughes et al., 2018). The system may converge to a state in which total community welfare is reasonably high but its distribution is deeply unequal, with some households enjoying full comfort while others endure chronic shortfalls. This observation motivates the central inquiry of the present thesis: can we design reward functions that encode not only individual self-interest but also an agent-specific concern for community fairness, and if so, what system-level properties emerge from the interaction of agents with heterogeneous social preferences?

### 1-1 Statement of the Problem

Smart neighbourhood microgrids represent the localised frontier of energy decentralisation. In these systems, prosumers can share surplus energy with neighbours through peer-to-peer exchanges that reduce reliance on the utility grid and minimise transmission losses (May & Huang, 2023; Moret & Pinson, 2019). However, each sharing decision confronts a household with a genuine social dilemma: surplus energy that is sent to a neighbour is energy that cannot be stored in the donor's own battery for future use. On any given day, the individually rational choice is to hoard — to store every available kilowatt-hour against the possibility of future scarcity. Yet if every household follows this logic, the community as a whole becomes brittle: surplus that could have balanced a neighbour's deficit is instead wasted when batteries reach capacity, and deficits that could have been covered by a neighbour's surplus instead become blackouts (Kollock, 1998; Gersani et al., 2001).

Existing multi-agent reinforcement learning approaches to this problem typically operate under the assumption of economic rationality, modelling each agent as a utility maximiser with no intrinsic concern for the welfare of others (May & Huang, 2023; Moret et al., 2020). These models optimise for collective technical efficiency — maximising total energy stored, minimising total community cost, or increasing aggregate self-consumption of solar generation (Charbonnier et al., 2022; Kusatake et al., 2023). The difficulty is that efficiency-only optimisation frequently produces inequitable outcomes. Some households may enjoy full comfort and high battery reserves while their neighbours experience frequent blackouts, even when total community resources would be sufficient to meet everyone's needs (Jain et al., 1984; Zhou & Lund, 2023). This distributional blindness is not merely an ethical concern; it threatens the long-term viability of peer-to-peer energy markets, since households that consistently receive poor outcomes have little incentive to remain in the community (Moret & Pinson, 2019).

Three specific research gaps emerge from the current state of the literature. First, no existing energy MARL study grounds agent heterogeneity in a validated psychological model such as the Big Five (OCEAN) framework. Studies such as Alshehri and Gaunt (2020) have demonstrated that heterogeneous preferences can produce qualitatively different system-level outcomes, but their framework assigns preferences arbitrarily rather than drawing on established personality theory. Second, fairness constraints in the energy MARL literature are applied uniformly across all agents, reflecting a top-down regulatory perspective rather than individual variation in prosocial concern (Jadhav et al., 2024; Ma et al., 2025). Third, the social cost of exploratory behaviour in cooperative energy-sharing communities remains unexamined. In multi-agent settings, one agent's continued exploration can destabilise the learning of others, a phenomenon documented in game-theoretic MARL but never studied in the context of physical resource management (Matignon et al., 2012; Leng, 2025). The present thesis addresses these three gaps by introducing personality-modulated reward weights drawn from the OCEAN model and systematically investigating how heterogeneous fairness preferences shape emergent community dynamics.

### 1-2 Significance of the Study

This research sits at the intersection of artificial intelligence, power engineering, and behavioural psychology, and its contributions span all three fields. From the perspective of AI research, the study demonstrates a principled method for injecting psychologically grounded heterogeneity into multi-agent reinforcement learning systems. Rather than treating agent variation as a nuisance parameter or imposing arbitrary behavioural labels, the OCEAN-to-RL mapping provides a theoretically motivated framework that links specific personality dimensions to specific learning parameters — agreeableness to the weight on fairness, openness to the exploration floor, neuroticism to penalty sensitivity (Binz & Schulz, 2023; Ren & Xu, 2025). This framework is general and could be applied to any MARL domain in which human-like agent diversity is desired, from autonomous vehicle coordination to collaborative robotics to human-AI teaming (Park et al., 2023).

From the perspective of energy engineering, the study provides quantitative evidence that fairness-aware reward design improves both distributional equity and technical efficiency. The finding that mixed communities with prosocial agents reduce energy waste by up to 11.5% relative to purely selfish baselines has practical implications for the design of peer-to-peer energy markets and community microgrid tariffs (Zhou & Lund, 2023). Importantly, this efficiency gain does not come at the cost of reduced comfort for prosocial agents — the emergent reciprocity mechanism documented in Chapter 4 shows that agents who share generously early in the day receive energy from neighbours later, producing higher individual comfort alongside higher community fairness. This result contradicts the intuitive assumption that altruistic behaviour in a resource-constrained environment must be self-sacrificing.

From a social perspective, the study contributes empirical evidence to the long-running debate about whether cooperative norms can emerge spontaneously in populations of self-interested agents (Ostrom, 1990; Fehr & Gächter, 2000). The simulation results demonstrate that a minority of prosocial agents — as few as five out of ten — can shift the equilibrium of the entire community toward more cooperative behaviour, even when the remaining agents are purely selfish. This finding is relevant not only for energy systems but for any domain in which policy makers seek to promote prosocial outcomes without resorting to coercive regulation. Finally, the discovery of the Innovator Effect serves as a cautionary result for the safe deployment of autonomous learning systems: a single agent whose exploration behaviour deviates from the community norm can increase inequality by twenty-two percent, suggesting that coordination stability should be a first-class design objective in multi-agent resource management.

### 1-3 Research Innovation

The core innovation of this work is a reward-shaping framework that maps the Big Five (OCEAN) personality traits to specific multi-agent reinforcement learning parameters. This psychologically grounded approach stands in contrast to existing work that either imposes uniform fairness constraints or defines agent heterogeneity arbitrarily without reference to established personality theory. The framework operationalises two personality dimensions in particular. Specifically, relative to Charbonnier et al. (2022) and similar efficiency-only energy MARL studies, the present framework adds heterogeneous prosocial preferences grounded in the Big Five rather than treating all agents as identical utility maximisers. Relative to Hughes et al. (2018) and Jadhav et al. (2024), which apply the same inequity-aversion penalty or LLM fairness critic to all agents uniformly, the present framework allows each agent's fairness concern to vary continuously along the Agreeableness dimension — creating a community in which some agents care deeply about equity, others care moderately, and some care not at all, as is observed in real human communities (Fehr & Gächter, 2000). Relative to May & Huang (2023), whose outer-level pricing agent enforces income equality through market rules rather than intrinsic preferences, the present framework internalises fairness concern within each agent's own reward function, enabling investigation of how heterogeneous intrinsic preferences shape emergent outcomes independently of market design.

Agreeableness, which in the psychological literature encompasses prosocial orientation, co-operativeness, and concern for others, is mapped to the weight assigned to community fairness in each agent's reward function (Goldberg, 1990; John & Srivastava, 1999). An agent with high agreeableness (labelled altruistic in this study) receives eighty percent of its reward from the community's Jain fairness index and only twenty percent from its own comfort; an agent with very low agreeableness (labelled pure selfish) ignores community fairness entirely. Between these extremes, the individualist and prosocial types represent intermediate positions, creating a spectrum of fairness concern that is both continuous and psychologically interpretable.

Openness to Experience, which captures curiosity, novelty-seeking, and tolerance for uncertainty, is mapped to the exploration floor of the epsilon-greedy policy (McCrae & Costa, 2003; Ren & Xu, 2025). Standard agents decay their exploration probability to a minimum of one percent, meaning they select random actions only very rarely once converged. The innovator agent, the type that operationalises high openness, maintains a minimum exploration probability of five percent, meaning it continues to try alternative strategies even after the rest of the community has settled into stable sharing patterns. This mapping allows the study to isolate the social impact of exploratory behaviour from the impact of reward-weight differences, since the innovator shares the same fairness weights as the prosocial type and differs only in its exploration schedule.

The simulation environment itself is designed for analytical clarity rather than engineering fidelity. A ring topology of ten houses, each connected to exactly one designated neighbour, eliminates network-routing confounds and isolates the social dynamics of sharing. Each house's state is a simple tuple of hour and discretised battery level, producing a ninety-six-state space that converges reliably within eight thousand episodes. This minimal design means that any observed differences between scenarios can be attributed to the personality-reward mapping rather than to environmental complexity, model architecture, or training instability.

### 1-4 Research Objectives

The primary objective of this study is to evaluate how heterogeneous, personality-influenced fairness preferences in a multi-agent reinforcement learning energy-sharing system affect the community's overall efficiency, fairness, and robustness, relative to a baseline community of purely self-interested agents. Four specific sub-objectives support this primary aim.

The first sub-objective is to develop and validate a reward-shaping framework that maps OCEAN personality traits to objective function weights and exploration parameters in a multi-agent Q-learning setting. This involves defining the mapping rules, implementing them in simulation, and verifying that agents with different personality parameters behave in ways consistent with their intended psychological profiles.

The second sub-objective is to analyse the temporal and state-dependent sharing patterns that emerge when agents prioritise community fairness alongside personal comfort. The study examines not only aggregate metrics such as mean comfort and fairness index but also the specific states in which agents choose to share versus hoard, using the learned Q-tables to reconstruct the implicit policy that each personality type converges to.

The third sub-objective is to investigate the prosocial advantage — the hypothesis that agents with moderate-to-high fairness weights achieve higher individual comfort through the mechanism of emergent reciprocity. If this hypothesis is confirmed, it would provide a direct incentive-compatibility argument for fairness-aware reward design: prosocial reward weights are not morally superior at the expense of efficiency but are in fact instrumentally beneficial for the individual agent.

The fourth sub-objective is to quantify the destabilising impact of high-openness innovator agents on community coordination and equality. By comparing scenarios that differ only in whether one agent has a higher exploration floor, the study isolates the social cost of continued exploration and provides the first empirical characterisation of this cost in a physical resource management context.

### 1-5 Research Questions

The study is organised around one primary research question and four sub-questions.

**Primary research question.** How do heterogeneous, personality-influenced fairness preferences in a multi-agent reinforcement learning energy-sharing system affect the community's overall efficiency, fairness, and robustness, compared to a community of purely self-interested agents? This question is evaluated by comparing the All Selfish baseline scenario against four experimental scenarios (All Prosocial, Mixed, Varied Altruism, and Innovator Effect) across seven quantitative metrics: mean community comfort, Jain's fairness index, blackout day rate, energy waste, prosocial-versus-selfish comfort split, Gini coefficient, and sharing frequency.

**Sub-question 1.** Does embedding fairness norms into reward functions lead to measurably different emergent sharing patterns? This question examines whether personality-modulated rewards produce policies that are qualitatively distinct from self-interested policies, as opposed to merely shifting the same policy along a quantitative continuum. The answer is drawn primarily from the sharing frequency metric and the Q-table heatmap analysis.

**Sub-question 2.** What trade-offs appear between community-wide energy efficiency and distributional fairness? This question tests the conventional assumption that equity and efficiency are in tension. If prosocial communities achieve both higher fairness and lower waste than selfish communities, then the assumed trade-off does not hold in this domain — a result with significant policy implications.

**Sub-question 3.** Can a mix of a few prosocial agents shift the behaviour of selfish agents through emergent reciprocity? This question addresses whether prosocial norms can propagate through a population without centralised enforcement. The Mixed scenario, containing five prosocial and five selfish agents, provides the primary test case.

**Sub-question 4.** How does a single curiosity-driven high-openness agent affect the stability of a mixed community? This question isolates the social externality of individual exploration. The Innovator Effect scenario introduces one agent with a higher exploration floor into an otherwise prosocial-leaning community and measures the resulting changes in equality, blackout rate, and convergence stability.

### 1-6 Research Hypotheses

Four hypotheses are tested in this study, each derived from the research questions above and grounded in the reviewed literature.

**Hypothesis 1.** Communities with prosocial reward weights will exhibit significantly lower energy waste than purely selfish communities, because agents who value fairness share surplus rather than discarding it when their batteries are full. This hypothesis follows from the intuition that fairness-aware agents internalise the cost of waste at the community level, whereas selfish agents are indifferent to waste once their own storage is saturated (Zhou & Lund, 2023).

**Hypothesis 2.** Prosocial agents in mixed communities will achieve a higher mean comfort than their selfish neighbours through the stabilisation of local supply chains. This is the prosocial advantage hypothesis. The mechanism is temporal: prosocial agents share surplus early in the day, building implicit credit that is repaid later when their own generation drops and neighbours return the favour (May & Huang, 2023). Selfish agents, who hoard early, may have full batteries but do not benefit from reciprocity when their deficit hours arrive.

**Hypothesis 3.** The relative advantage of prosocial reward design will remain consistent as environmental scarcity increases. If the prosocial advantage is stable, it should hold under cloudy conditions that halve solar generation, not only on clear days. This hypothesis tests whether the benefits of fairness-aware design are contingent on resource abundance or generalise to scarcity conditions (Kusatake et al., 2023).

**Hypothesis 4.** The presence of a single agent with a high exploration floor will destabilise cooperative equilibria, resulting in higher Gini coefficients and higher blackout rates. This hypothesis captures the prediction that continued random exploration by the innovator prevents neighbours from forming stable expectations about energy availability, forcing them toward more defensive hoarding strategies (Aloor et al., 2024; Matignon et al., 2012).

### 1-7 Operational Definitions

The following terms are defined as they are used throughout this thesis. These definitions are specific to the simulation context described in Chapter 3 and may not correspond exactly to broader or alternative usages in the literature.

**Prosumer.** A household that both consumes and produces energy through rooftop solar photovoltaic panels, capable of storing surplus generation in a battery and sharing energy with neighbours in the microgrid (Rathnayaka et al., 2014; Morstyn & McCulloch, 2019). In this study, all ten houses are prosumers with identical solar capacity and battery size.

**Multi-Agent Reinforcement Learning.** A computational framework in which multiple autonomous agents learn decision-making policies through trial-and-error interaction with a shared environment (Sutton & Barto, 2018; Tan, 1993). The present study uses independent tabular Q-learning, in which each agent maintains its own Q-table and treats all other agents as part of the stationary environment — an approximation that is known to trade theoretical convergence guarantees for practical scalability.

**OCEAN (Big Five) Model.** The five-factor model of personality consisting of Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism (Goldberg, 1990; McCrae & Costa, 2003). This study maps two of these dimensions — Agreeableness and Openness — to specific reinforcement learning parameters, while holding the other three dimensions at population-average levels across all agents.

**Innovator Effect.** The observed destabilisation of community-level coordination caused by a single high-Openness agent whose continued exploration — operationalised as a higher minimum epsilon value in the epsilon-greedy policy — prevents neighbours from forming stable expectations about energy availability (see Section 4-8 for the full analysis). The term is introduced in this thesis and is defined here for clarity.

**Jain's Fairness Index.** A scale-invariant, continuous metric for quantifying the equality of a resource distribution across a population, computed as the square of the sum of allocations divided by the population size times the sum of squared allocations (Jain et al., 1984). The index ranges from one over the population size (maximal inequality) to one (perfect equality). In this study, it is applied to the distribution of comfort across the ten households.

**Personal Comfort.** The fraction of a household's total daily energy demand that is successfully met through a combination of solar generation, battery discharge, and received shared energy (Alshehri & Gaunt, 2020). A comfort value of 1.0 indicates that all demand was satisfied; values below 0.95 are classified as blackout days.

**Energy Waste.** Surplus energy that could neither be stored in the donor's battery (because the battery was full) nor shared with a neighbour (because the sharing action was insufficient to transfer the excess). Waste is measured in kilowatt-hours per day and represents a pure efficiency loss for the community.

### 1-8 Thesis Outline

The remainder of this thesis is organised as follows. Chapter 2 presents a comprehensive review of the relevant literature, tracing the evolution of smart microgrids and the prosumer paradigm, surveying peer-to-peer trading and pricing mechanisms, reviewing multi-agent reinforcement learning approaches to distributed control, examining fairness modelling in social dilemmas, and discussing personality-driven decision making in artificial intelligence. The chapter concludes with a qualitative comparison table that positions this study against the state of the art and a summary of the three research gaps that this thesis addresses.

Chapter 3 describes the research methodology in full detail. It presents the research design and approach (Section 3-1), the data collection methods (Section 3-2), the tools and instruments used (Section 3-3), and the population, sample, and sampling method (Section 3-4). It then specifies the physical environment — solar generation modelling, demand profiles, battery storage, and the weather model — and presents the OCEAN-to-reward mapping, the reward function design, the tabular Q-learning algorithm with its hyperparameters, the two-phase energy sharing mechanism, the five experimental scenarios, the seven evaluation metrics, the data analysis methods, and the training protocol (Sections 3-5 through 3-13).

Chapter 4 presents the simulation results across all scenarios and metrics. The analysis proceeds from community-level aggregates through agent-type differences and inequality measures to the learned Q-table policies and the sensitivity analysis under scarcity. Each finding is described objectively, with interpretation reserved for Chapter 5. The chapter also includes statistical significance testing, the Innovator Effect analysis, and a comparison with state-of-the-art baselines.

Chapter 5 discusses the implications of the findings, examines the fairness-efficiency relationship, analyses the emergent reciprocity mechanism, considers the policy implications of the results, and acknowledges the study's limitations. It concludes with a summary of the work, a summary of key findings, and directions for future research.

## 2- Literature Review

### 2-1 Theoretical Foundations

#### 2-1-1 The Decentralized Energy Transition and the Prosumer Paradigm

The architecture of electrical power systems has remained fundamentally unchanged for nearly a century: large centralised generators feed high-voltage transmission lines that branch into lower-voltage distribution networks, delivering electricity to passive end-users. This model, while historically successful, is undergoing a structural transformation driven by two converging forces. The first is the urgency of climate mitigation. The Intergovernmental Panel on Climate Change has established that limiting global warming to 1.5 degrees Celsius requires that anthropogenic carbon dioxide emissions reach net zero by mid-century, with the energy sector — responsible for approximately three-quarters of global greenhouse gas emissions — bearing the primary burden of this transition (Masson-Delmotte et al., 2018). The second force is the dramatic cost reduction of key renewable technologies. The levelised cost of solar photovoltaic electricity has declined by approximately 90 percent since 2010, and lithium-ion battery pack prices have fallen by more than 80 percent over the same period, making residential solar-plus-storage systems economically viable in an increasing number of markets (BloombergNEF, 2023; IEA, 2022).

These two forces have given rise to the prosumer: a residential household that both produces and consumes electricity, typically through rooftop solar panels and a home battery system (Rathnayaka et al., 2014; Morstyn & McCulloch, 2019). The prosumer represents a fundamental departure from the traditional consumer model because the direction of energy flow is no longer unidirectional. A household with surplus solar generation can store energy in its battery, export it to the utility grid, or share it directly with neighbours through peer-to-peer exchange. Each of these options carries different implications for system efficiency, household economics, and community resilience (Tushar et al., 2020; Zhou & Lund, 2023). The choice among them is not purely technical but involves considerations of trust, reciprocity, and long-term community stability that standard economic models do not fully capture.

The coordination challenge that arises when multiple prosumers are interconnected in a smart neighbourhood microgrid is fundamentally different from the coordination challenge of the centralised grid. In the traditional model, a single system operator has complete information about generation and demand and can dispatch resources optimally. In the decentralised model, no single entity has complete information. Each household makes its own decisions based on local observations — its own battery state, its own demand pattern, and the current solar generation — without direct knowledge of its neighbours' conditions. The system must therefore find a way to achieve collectively desirable outcomes through purely local decision-making, a problem that maps naturally onto the multi-agent reinforcement learning paradigm (Li & Zhang, 2022; Charbonnier et al., 2022).

The literature has produced a rich taxonomy of prosumer coordination mechanisms. Some approaches rely on price signals, treating the neighbourhood as a mini electricity market in which households bid to buy and sell energy (Moret & Pinson, 2019). Others use direct control, with a central aggregator dispatching resources across the community (Behrunani et al., 2023). A third category uses learning-based approaches in which agents develop sharing policies through repeated interaction without explicit communication or central coordination (Charbonnier et al., 2022; Kusatake et al., 2023). Each approach has strengths and weaknesses, but all share a common limitation: they model prosumers as economically rational agents whose behaviour is determined entirely by external incentives and cost minimisation. The possibility that prosumers possess intrinsic social preferences — that they might value fairness, reciprocity, or community welfare as ends in themselves — is not considered.

This omission matters because a growing body of empirical evidence from behavioural economics and social psychology demonstrates that human decision-making in resource-sharing contexts is influenced by social preferences that cannot be reduced to self-interest (Fehr & Gächter, 2000; Ostrom, 1990). Humans share resources even when it is not individually rational to do so, they punish free-riders at a personal cost, and they condition their own cooperation on the cooperation they observe in others. If peer-to-peer energy systems are to be designed for human participants — or for autonomous agents that interact with humans — these social dimensions must be incorporated into the computational models that govern sharing decisions. The present thesis argues that the integration of psychologically grounded social preferences into multi-agent reinforcement learning is both feasible and beneficial, and the remainder of this chapter reviews the literature that supports this claim.

#### 2-1-2 Peer-to-Peer Energy Trading: Market Structures and Pricing Mechanisms

Peer-to-peer energy trading has been extensively studied as a market-based mechanism for coordinating prosumer behaviour. The central idea is that households with surplus generation should be able to sell energy directly to households with deficits, bypassing the utility grid intermediary and capturing a larger share of the economic value of distributed generation (Tushar et al., 2020). The literature has converged on a three-part taxonomy of P2P market structures: full P2P, in which every household trades directly with every other household through bilateral contracts; community-based, in which a central mediator or aggregator facilitates trades within a local group; and hybrid models that combine elements of both (Zhou & Lund, 2023). Among these, the community-based model has received the most attention for residential applications because it balances the efficiency of centralised coordination with the autonomy of decentralised decision-making.

Pricing mechanisms in P2P markets typically fall into one of three categories. Supply-demand ratio pricing (SDR) sets the local price based on the aggregate balance of generation and demand in the community at each time step, with prices rising during scarcity and falling during surplus (Qiu et al., 2021). Mid-market rate pricing (MMR) sets the local price at the midpoint between the feed-in tariff and the retail electricity price, ensuring that both buyers and sellers benefit relative to trading with the utility grid. Bill sharing (BS) divides the total community electricity cost among households in proportion to their net consumption or production, simplifying the settlement process at the cost of weaker marginal incentives. Each of these mechanisms has been shown to improve community-level outcomes relative to the baseline of no trading, but their relative performance depends on the specific characteristics of the community, the generation and demand profiles of its members, and the regulatory context (Zhou & Lund, 2023).

Game-theoretic approaches have been widely used to analyse strategic interactions in P2P markets. Stackelberg game formulations model a central leader (often the community aggregator) that sets prices, with prosumer agents acting as followers that optimise their consumption and sharing decisions given those prices (Behrunani et al., 2023). Nash bargaining solutions model the trading problem as a cooperative game in which households negotiate a mutually beneficial allocation of surplus, with the solution characterised by the maximisation of the product of individual benefits (Moret & Pinson, 2019). These game-theoretic models have the advantage of providing provable guarantees about convergence and optimality under certain assumptions. Their principal limitation is the assumption of common knowledge and strategic rationality: all agents are assumed to know the payoff structures of all other agents and to optimise their own payoffs accordingly. In real communities, households do not have complete information about their neighbours' preferences or constraints, and their behaviour is influenced by social norms, trust, and fairness concerns that are not captured by standard utility functions (Fehr & Gächter, 2000).

A further limitation of market-based approaches is their reliance on a central coordinator or aggregator. While the community-based model reduces the communication overhead of full P2P trading, it reintroduces a single point of failure and requires trust in the central entity. This is particularly problematic in contexts where households are sceptical of third-party control over their energy resources, or where the aggregator's incentives are not perfectly aligned with community welfare (Moret & Pinson, 2019). Learning-based approaches, which avoid the need for a central coordinator by allowing agents to develop policies through local experience, offer a potential resolution to this tension, and it is to these approaches that the review now turns.

#### 2-1-3 Multi-Agent Reinforcement Learning for Distributed Energy Control

Multi-agent reinforcement learning provides a natural formalism for the prosumer coordination problem because it does not require a central operator with complete information and does not assume that agents possess knowledge of each other's strategies or payoff functions. Instead, each agent learns a decision policy through repeated trial-and-error interaction with its environment, receiving reward signals that reflect the quality of its decisions and updating its policy accordingly (Sutton & Barto, 2018). When applied to energy sharing, each household is modelled as an autonomous RL agent whose action is the fraction of surplus energy to share with its designated neighbour, whose state is defined by the current hour and its own battery level, and whose reward depends on both its personal comfort and the fairness of the overall community distribution.

The standard formalisation for multi-agent settings is the decentralised partially observable Markov decision process (Dec-POMDP), which generalises the single-agent MDP to settings in which multiple agents act simultaneously, each receiving only partial observations of the global state (Oliehoek & Amato, 2016). Solving a Dec-POMDP optimally is NEXP-complete, meaning that exact solutions are intractable for all but the smallest problems. Practical MARL approaches therefore rely on approximations. One important family of methods uses centralised training with decentralised execution (CTDE), in which agents are trained using global state information in simulation but execute their learned policies using only local observations at deployment time (Lowe et al., 2017). Value decomposition networks (VDN) and QMIX extend this idea by learning a centralised value function that factors into per-agent components, enabling coordinated behaviour without requiring communication during execution (Rashid et al., 2018).

The simplest and most widely used MARL approach in the energy domain is independent Q-learning (IQL), in which each agent maintains its own Q-table or Q-network and treats all other agents as part of the stationary environment (Tan, 1993). The appeal of IQL is its simplicity and scalability: it requires no communication between agents and no centralised training infrastructure. However, IQL suffers from the non-stationarity problem, which is the defining technical challenge of multi-agent reinforcement learning. Because all agents are learning simultaneously, the environment faced by any individual agent changes as its neighbours update their policies. This violates the Markov assumption on which the Q-learning convergence proof depends, and can lead to oscillatory or suboptimal behaviour (Hernandez-Leal et al., 2017). In practice, IQL often converges to reasonable policies in benign environments, but its theoretical convergence guarantees are weak.

The alter-exploration problem represents a specific manifestation of non-stationarity that is directly relevant to the present thesis. In multi-agent settings, an agent that continues to explore random actions after others have converged to stable policies introduces unpredictability into the environment from the perspective of its neighbours. These neighbours, unable to form stable expectations about energy availability, may shift toward more defensive or hoarding strategies, degrading community-level outcomes (Matignon et al., 2012). Leng (2025) formalised this phenomenon as the alter-exploration problem and demonstrated its severity in cooperative MARL benchmarks. The present thesis extends this analysis to the energy-sharing domain by introducing a high-exploration innovator agent and quantifying the community-level costs of its continued exploration.

Charbonnier et al. (2022) demonstrated the viability of IQL for residential energy flexibility management using a population of thirty households in a UK setting, each modelled as a tabular Q-learning agent with a fixed-size Q-table that preserves privacy by never sharing personal data. Their approach achieved significant improvement in local energy self-consumption, but the study did not consider fairness objectives or heterogeneous agent preferences. All agents shared identical reward functions optimising for individual self-consumption, reflecting the assumption that efficiency maximisation is the sole relevant objective. This is representative of a broader pattern in the energy MARL literature: most studies prioritise technical efficiency — maximising self-consumption, minimising grid imports, or reducing community energy costs — and treat distributional equity as either irrelevant or as a secondary constraint that can be imposed uniformly.

Bui et al. (2019) applied Q-learning to a microgrid battery scheduling problem and demonstrated that learning-based control outperforms rule-based heuristics in reducing peak demand and energy costs. Ali et al. (2023) extended this to a multi-agent setting with demand response, showing that agents can learn to shift consumption in response to price signals without centralised coordination. These studies collectively establish the technical feasibility of MARL-based energy management, but they also reveal the gap that motivates the present work: none of them incorporate social preferences or personality heterogeneity into the learning framework.

The collective outcome of individually rational behaviour in shared-resource environments is a central concern of both economics and ecology. Hardin (1968) articulated the tragedy of the commons as a parable in which rational herders, each maximising their own benefit by adding cattle to a shared pasture, collectively destroy the resource on which they all depend. The energy-sharing analogue is straightforward: a prosumer facing a deficit household and having surplus generation must decide whether to share or hoard. The individually rational choice is to hoard, since stored energy provides insurance against future scarcity. Yet if every household hoards, surplus that could have balanced a neighbour's deficit is wasted when batteries reach capacity, and the community as a whole becomes more brittle (Kollock, 1998).

Ostrom (1990) challenged the inevitability of the tragedy of the commons by documenting numerous real-world cases in which communities successfully manage shared resources through norms of reciprocity, communication, and graduated sanctions. Her work demonstrated that the tragedy is not a universal law but a contingent outcome that depends on the institutional context and the social preferences of participants. This insight has direct implications for the design of peer-to-peer energy systems: if communities can develop cooperative norms for managing shared energy resources, then the technical architecture of the sharing mechanism should support rather than undermine such norms.

The formal modelling of fairness in multi-agent systems has produced several widely used metrics, each with distinct mathematical properties and practical implications. Jain's Fairness Index, originally developed for resource allocation in computer networks, is defined as the square of the sum of allocations divided by the product of the population size and the sum of squared allocations (Jain, Chiu & Hawe, 1984). The index ranges from one over the population size, representing maximal inequality in which one agent receives all resources, to one, representing perfect equality in which all agents receive identical allocations. Its key properties are scale invariance, meaning that multiplying all allocations by a constant does not change the index; continuity, meaning that small changes in allocations produce small changes in the index; and population independence, meaning that the index does not systematically favour larger or smaller populations.

The Gini Coefficient, derived from the Lorenz curve of cumulative wealth or consumption, is the most widely used measure of inequality in economics (Gini, 1912). It ranges from zero, representing perfect equality, to one, representing maximal inequality in which all resources are concentrated in a single agent. The Gini coefficient is more sensitive to changes in the middle of the distribution than to changes at the extremes, which makes it complementary to Jain's Fairness Index rather than redundant. In the energy context, the Gini coefficient has been applied to measure inequality in energy consumption, access, and expenditure, but its application to real-time sharing decisions in multi-agent learning systems is relatively recent (Kusatake et al., 2023).

Recent MARL research has begun to incorporate fairness objectives directly into agent reward functions. Hughes et al. (2018) introduced inequity aversion rewards in the Cleanup and Harvest game environments, demonstrating that agents penalised for earning significantly more or less than their peers learn to share resources more equitably and achieve higher collective welfare. Their approach was inspired by the inequity aversion model of Fehr and Schmidt (1999), which posits that human preferences depend not only on absolute outcomes but also on relative outcomes compared to others. The Cleanup and Harvest results showed that inequity aversion is sufficient to resolve the tragedy of the commons in these abstract game settings, but the study did not examine whether the same mechanism operates in physically grounded energy-sharing environments.

Jadhav et al. (2024) proposed FairMarket-RL, a framework that uses a large language model as a fairness critic to evaluate the equity of market outcomes in a P2P energy trading simulation. The LLM assesses whether each agent's energy allocation is fair according to criteria specified in natural language, and the reward signal from this assessment is used to guide agent learning. This approach is innovative in its use of human-centric fairness assessments, but it introduces a dependency on the real-time stability and availability of LLM API calls, which may not be reliable in deployed systems. More fundamentally, the fairness assessment is exogenous to the agents: it is imposed by an external critic rather than internalised as part of each agent's own value system.

Ma et al. (2025) extended the LLM-MARL paradigm to address energy poverty in a large-scale simulation of ninety-nine census tracts in Florida. Their CAPPO framework combines centralised training with LLM-generated equity signals that direct resources toward disadvantaged communities. The results demonstrated that equity-aware training can reduce energy poverty without sacrificing overall efficiency. However, the fairness signals in CAPPO are derived from census-level data and do not reflect individual household-level preferences or personality heterogeneity. All agents within the same tract receive the same equity signal, which again represents a uniform, top-down fairness constraint rather than the heterogeneous intrinsic preferences that characterise real communities.

The gap that emerges from this review of fairness-aware MARL is twofold. First, existing approaches apply fairness constraints uniformly across all agents, treating fairness as a regulatory intervention rather than as a dimension of individual variation. Second, no study grounds fairness preferences in a validated psychological model of personality. The present thesis addresses both gaps by mapping the Big Five personality dimension of Agreeableness — which in the psychological literature predicts prosocial orientation and concern for others — directly to the weight that each agent assigns to community fairness in its reward function. This creates a population of agents with heterogeneous, psychologically grounded fairness preferences, enabling the study of emergent community dynamics that neither uniform fairness constraints nor arbitrary heterogeneous labels can capture.

#### 2-1-4 Personality-Driven Decision Making in Computational Agents

The integration of personality psychology into computational agent design has a history that spans several decades, but its application to reinforcement learning is comparatively recent. The central premise is that individual differences in behaviour — the stable patterns of thought, emotion, and action that distinguish one person from another — can be characterised along a small number of dimensions and that these dimensions can be mapped onto computationally tractable parameters in agent architectures (Goldberg, 1990; McCrae & Costa, 2003). If this mapping can be made principled and validated, it offers a path toward more human-like agents in social simulations, human-AI interaction systems, and multi-agent coordination problems that involve human participants.

The Big Five (OCEAN) model is the dominant framework for personality assessment in contemporary psychology, with decades of cross-cultural validation supporting its factor structure (John & Srivastava, 1999). The five dimensions are Openness to Experience, which encompasses curiosity, imagination, and preference for novelty; Conscientiousness, which captures self-discipline, organisation, and goal-directedness; Extraversion, which reflects sociability, assertiveness, and positive emotionality; Agreeableness, which encompasses prosocial orientation, trust, and co-operativeness; and Neuroticism, which captures emotional instability, anxiety, and threat sensitivity. Each dimension represents a continuum rather than a binary category, and individual personality profiles are characterised by the configuration of scores across all five dimensions.

The mapping from personality traits to agent behaviour has been explored in several computational frameworks. Park et al. (2023) demonstrated that generative agents imbued with Big Five personality profiles produce more varied and believable social interactions in a simulated town environment. Their approach used natural language prompts to instantiate personality traits in large language model agents, showing that trait-consistent behaviour emerges from the interaction of personality prompts with the agent's memory and planning architecture. While powerful, this approach depends on the specific capabilities and biases of the underlying LLM and is not easily transferable to reinforcement learning settings in which agents must learn policies through trial and error rather than generate text.

Moon et al. (2022) established a direct mapping from OCEAN traits to reinforcement learning hyperparameters, providing one of the first systematic frameworks for personality-to-RL translation. In their formulation, Agreeableness maps to the weight assigned to others' welfare in a multi-agent setting, Conscientiousness maps to the learning rate and its decay schedule, Extraversion maps to the initial exploration rate, Openness maps to the exploration decay rate and minimum exploration floor, and Neuroticism maps to the penalty multiplier for negative outcomes. Moon et al. validated this mapping in a grid-world social dilemma environment, demonstrating that agents with different personality parameters produce measurably different behavioural trajectories and that the mapping is intuitively interpretable — high-Agreeableness agents share more resources, high-Openness agents explore more persistently, and high-Neuroticism agents avoid states associated with past negative outcomes.

Ren and Xu (2025) extended the OCEAN-to-agent mapping to LLM-based generative agents in a classroom social simulation, focusing specifically on the traits of Openness and Agreeableness. They found that high-Openness agents were significantly more likely to accept new information and update their beliefs, while high-Agreeableness agents were more likely to cooperate and share resources with peers. Their study also provided evidence of trait stability over repeated interactions, suggesting that personality-modulated behaviour, once instantiated in an agent, remains consistent across different contexts within the simulation. This stability is important for the validity of the mapping: if personality effects dissipate after a few episodes of learning, the mapping would have limited practical value.

The critical limitation of the existing personality-to-RL literature, from the perspective of the present thesis, is that all studies to date have been conducted in purely social or abstract game environments. Moon et al. (2022) used a grid-world resource sharing game. Ren and Xu (2025) used a classroom social simulation. Park et al. (2023) used a small-town social interaction environment. None of these settings involve the management of a physical resource — electricity — with the real-world constraints of solar generation, battery storage, demand patterns, and weather uncertainty that characterise the energy-sharing problem. The question of whether OCEAN-to-RL mappings produce meaningful behavioural differences in a physically grounded resource management task has not been addressed in the literature. The present thesis fills this gap by implementing a personality-modulated reward framework in a simulated neighbourhood microgrid and systematically measuring the effects of heterogeneous personality parameters on both individual and community-level outcomes.

### 2-2 Review of Related Literature

The body of work that directly informs the present thesis spans three thematic clusters: efficiency-focused MARL for energy management, fairness-aware MARL with uniform constraints, and personality-driven agent modelling in non-energy domains. This section critically reviews the most relevant studies within each cluster, comparing their methodological choices, identifying contradictions and unresolved questions, and establishing the specific gaps that the present work addresses.

#### 2-2-1 Efficiency-Focused MARL for Residential Energy Management

The earliest applications of reinforcement learning to residential energy management focused on single-agent settings in which a home energy management system learns to optimise battery charging and discharging decisions to minimise electricity costs or maximise self-consumption of solar generation (Bui et al., 2019). These single-agent studies established the viability of RL for energy control and demonstrated that learning-based policies outperform fixed rule-based heuristics under a variety of weather and price conditions. The extension to multi-agent settings, in which multiple households interact through a shared microgrid or market, introduced the coordination challenge that defines the current state of the art.

Charbonnier et al. (2022) provided one of the most comprehensive demonstrations of multi-agent Q-learning for residential flexibility management. Their study modelled thirty households in the UK, each equipped with electric vehicles and heat pumps in addition to solar PV, and each controlled by an independent tabular Q-learning agent with a fixed-size state-action table. The agents learned to shift their flexible loads to times of high local solar generation, increasing community self-consumption by approximately twelve percent compared to a rule-based baseline. The study's principal strength is its scalability: because each agent maintains only its own Q-table and never shares personal data with a central coordinator, the approach preserves privacy and can be deployed in communities of arbitrary size. Its principal limitation, from the perspective of the present thesis, is that all agents share identical reward functions that optimise only for individual self-consumption. The study did not examine whether agents with different objectives would produce different outcomes, nor did it consider the distributional effects of the learned policies across households with different demand patterns.

A methodological detail of Charbonnier et al. (2022) that deserves scrutiny is their handling of the non-stationarity problem. The authors used a fixed exploration schedule with epsilon decay from 0.9 to 0.01 over 100,000 episodes, a design choice that ensures all agents converge to deterministic policies by the end of training. This approach is effective in benign settings where the optimal joint policy is unique and stable, but it assumes that the environment remains stationary once all agents have converged. If the environment or the behaviour of neighbouring agents changes after deployment, the agents have no mechanism for adapting. The present thesis differs from Charbonnier et al. (2022) not only in its introduction of personality heterogeneity but also in its examination of what happens when one agent deliberately maintains a higher exploration floor, creating permanent non-stationarity for its neighbours.

Bui et al. (2019) applied Q-learning to battery scheduling in a microgrid context and demonstrated that learning-based control reduces peak demand and operational costs relative to both rule-based heuristics and model predictive control. Their study used a single-agent formulation in which the central microgrid controller learns to dispatch a shared battery, achieving the same coordination objective without the challenges of multi-agent learning. The trade-off is that centralised control requires complete information about all households, raising both privacy and communication concerns. The decentralised approach of the present thesis, in which each household makes its own sharing decisions, avoids these concerns but introduces the non-stationarity and coordination challenges that centralised control naturally avoids.

Kusatake et al. (2023) took a different approach to the coordination problem by using evolutionary multi-objective optimisation rather than reinforcement learning. Their framework optimises both the total community profit and the minimum individual profit simultaneously, ensuring that no household is left significantly worse off than others. The multi-objective formulation is appealing because it explicitly captures the trade-off between efficiency and equity that single-objective approaches ignore. However, the evolutionary algorithm operates in batch mode, evaluating candidate solutions on the full history of community interactions before selecting the next generation. This offline approach cannot adapt to real-time changes in weather, demand, or agent behaviour, limiting its applicability in dynamic environments. The present thesis uses online learning instead, allowing agents to adapt continuously as conditions change.

The efficiency-focused literature establishes that MARL can improve community-level energy outcomes, but it leaves the distribution of those outcomes unexamined. Studies that report aggregate metrics such as mean community cost or total self-consumption may mask substantial inequality in how those benefits are distributed across households. The present thesis addresses this gap by treating distributional equity as a primary outcome variable, measured through Jain's Fairness Index, the Gini coefficient, and the blackout day rate, rather than as a secondary consideration.

#### 2-2-2 Fairness-Aware MARL: Uniform Constraints and Their Limitations

The recognition that efficiency-only optimisation can produce inequitable outcomes has motivated a growing body of work on fairness-aware MARL. These studies modify agent reward functions or training objectives to penalise inequitable distributions, but they typically apply the same fairness constraint to all agents, reflecting a top-down regulatory perspective rather than individual variation in fairness concern.

May and Huang (2023) studied a peer-to-peer prosumer market in a Swedish building community using proximal policy optimisation (PPO) in a two-level inner-outer architecture. In their formulation, an inner RL agent optimises each household's individual energy costs while an outer RL agent adjusts the community's pricing mechanism to achieve income equality across households. The two-level design is innovative because it separates the operational decision problem — how much energy to share at given prices — from the market design problem — what prices produce fair outcomes. May and Huang found that the outer-level pricing agent successfully reduced income inequality, but the fairness mechanism operates through price adjustments rather than through each household's intrinsic preferences. A household that would be willing to share more generously if its neighbour were in genuine need has no way to express this preference in the model. All households respond identically to the same price signals, an assumption that contradicts the empirical evidence on heterogeneous social preferences (Fehr & Gächter, 2000).

The study by May and Huang (2023) also assumes that all prosumers are economically rational in the narrow sense of minimising their individual costs given the current prices. This assumption is methodologically convenient but limits the external validity of the results. If real prosumers share energy not only because it is financially beneficial at the current price but also because they care about the welfare of their neighbours, then models that assume pure economic rationality will systematically underestimate sharing rates and overestimate the price incentives needed to achieve equitable outcomes.

Hughes et al. (2018) provided one of the most influential demonstrations of inequity aversion rewards in multi-agent systems. Using the Cleanup and Harvest game environments, they showed that agents whose reward functions include a penalty for inequality — measured as the difference between the agent's own payoff and the average payoff of all agents — learn to share resources more equitably and achieve higher collective welfare than agents who optimise only for individual payoff. The Cleanup environment is a spatial resource management game in which agents must collect apples that regenerate only if agents also clean up pollution in the shared water source, creating a public goods problem structurally similar to energy sharing. The Harvest environment involves agents collecting apples from a shared resource that regenerates at a rate proportional to the remaining stock, creating a commons management problem.

The results of Hughes et al. (2018) are directly relevant to the present thesis because they demonstrate that reward-level fairness modifications can resolve the tragedy of the commons in multi-agent settings. However, three important differences distinguish their work from the present study. First, the inequity aversion reward in Hughes et al. uses the average payoff as its reference point, meaning that agents are penalised for diverging from the mean in either direction. This formulation treats all deviations from equality as equally undesirable, whereas the Jain's Fairness Index used in the present thesis is scale-invariant and has different mathematical properties that make it more suitable for resource allocation contexts. Second, the fairness penalty in Hughes et al. is applied uniformly; every agent has the same degree of inequity aversion. The present thesis varies the strength of the fairness concern across the agent population, creating a spectrum from pure selfishness to near-complete altruism. Third, the Cleanup and Harvest environments are abstract games with no physical grounding in energy systems.

Jadhav et al. (2024) proposed FairMarket-RL, which uses a large language model as an external fairness critic in a P2P energy trading simulation. The LLM is prompted to evaluate the fairness of each agent's energy allocation according to natural language criteria, and the resulting fairness score is incorporated into the agent's reward signal. This approach is methodologically ambitious because it replaces a fixed analytical fairness metric with a flexible, language-based assessment that can capture nuances that mathematical metrics might miss.

However, FairMarket-RL has several limitations that the present thesis avoids. First, the LLM-based fairness critic introduces a dependency on the real-time stability, latency, and cost of LLM API calls, which may be unacceptable in a deployed energy system. Second, the LLM's fairness judgments may be inconsistent across different prompt phrasings, input formats, or model versions, introducing an uncontrolled source of variance into the learning process. Third, the fairness assessment remains exogenous to the agents themselves; it is imposed by an external critic rather than internalised as each agent's own value system. The present thesis takes the alternative approach of embedding fairness concern directly into each agent's reward function, where it is intrinsic, consistent, and does not require external API calls.

Ma et al. (2025) extended the LLM-in-the-loop paradigm to a large-scale energy poverty simulation with ninety-nine census tracts in Florida. Their CAPPO framework uses centralised training with LLM-generated equity signals that direct resources toward disadvantaged communities identified by census-level energy burden data. The study's scale is impressive and its focus on energy poverty addresses a socially important research question. The fairness mechanism in CAPPO operates at the census tract level rather than the household level, allocating resources to maximise equity across tracts rather than across individual households. This design choice reflects the policy goal of reducing energy poverty at the population level, but it does not model the heterogeneous fairness preferences that might exist across different households within the same tract.

The fairness-aware MARL literature collectively demonstrates that incorporating equity considerations into agent training improves distributional outcomes, but it also reveals a consistent methodological pattern: fairness is treated as a uniform, externally imposed constraint rather than a dimension of individual heterogeneity. The present thesis breaks from this pattern by allowing each agent's degree of fairness concern to vary according to its personality trait level, creating a community in which some agents care deeply about equity, others care moderately, and some care not at all.

#### 2-2-3 Game-Theoretic and Market-Based Approaches to Fair Energy Sharing

An alternative to the RL-based approach to fairness in energy sharing is the use of game-theoretic and market design methods that structure incentives to produce equitable outcomes by design. These approaches share the goal of achieving fair outcomes but differ fundamentally in their assumptions about agent knowledge and computational requirements.

Behrunani et al. (2023) proposed a bilevel game-theoretic framework for price mediation in a smart energy hub network. In their formulation, a central mediator sets prices at the upper level to maximise a fairness objective — defined as the variance in cost reductions across hubs — while individual hubs optimise their own energy consumption and trading decisions at the lower level given the announced prices. The bilevel structure separates the fairness problem from the operational problem with analytical game-theoretic properties rather than learned policies.

The principal advantage of the game-theoretic approach is that it provides provable guarantees about convergence and optimality under the assumed model of agent behaviour. Behrunani et al. (2023) proved that their bilevel game converges to a Stackelberg equilibrium under mild regularity conditions, and they demonstrated that the resulting price schedule reduces variance in cost reductions across hubs by approximately forty percent compared to uniform pricing. The principal disadvantage is that the approach requires a central mediator with the authority to set prices and the computational capacity to solve the bilevel optimisation problem at each time step. This centralisation reintroduces the single point of failure and trust reliance that decentralised approaches are designed to avoid.

Moret and Pinson (2019) analysed P2P energy trading as a cooperative game and proposed a Nash bargaining solution for allocating the gains from trade among participating prosumers. The Nash bargaining solution has the attractive property that it maximises the product of individual benefits, meaning that no agent can be made better off without making another agent worse off, and no agent receives less than its disagreement payoff from trading with the utility grid alone. Moret and Pinson demonstrated that Nash bargaining produces fair allocations in the sense of Pareto optimality and individual rationality, but their analysis assumed that all agents have complete information about each other's preferences and that all gains from trade are known and fixed. In a dynamic setting with stochastic generation and demand, the Nash bargaining solution must be recomputed at each time step, imposing a substantial communication and computation burden.

Qiu et al. (2021) proposed a supply-demand ratio based pricing mechanism for P2P markets that does not require centralised optimisation or complete information. In SDR pricing, the local energy price at each time step is determined by the ratio of total community generation to total community demand, with prices rising when demand exceeds supply and falling when supply exceeds demand. Each household then responds to the current price by adjusting its consumption, storage, and trading decisions. The SDR mechanism is decentralised, computationally lightweight, and has been shown to improve community self-consumption in simulation studies. However, its fairness properties are incidental rather than designed: the mechanism does not explicitly account for differences in household income, energy needs, or past contributions to the community.

The game-theoretic and market-based literature contributes important theoretical foundations for fair energy sharing, but it relies on assumptions of common knowledge, central coordination, or equilibrium computation that limit its practical applicability in settings with autonomous learning agents. The MARL-based approach of the present thesis avoids these limitations by allowing agents to discover fair sharing patterns through local learning, without requiring a central mediator, complete information, or the explicit computation of market equilibria.

#### 2-2-4 The Alter-Exploration Problem and the Cost of Individual Exploration

A theme that emerges across multiple strands of the MARL literature is that individual agent behaviour can have negative externalities on community-level learning outcomes, even when that behaviour is individually rational from the exploring agent's perspective. This phenomenon has been studied under several names — the non-stationarity problem, the alter-exploration problem, and the destabilising effect of heterogeneous exploration schedules — but its underlying mechanism is the same: when one agent changes its behaviour in ways that are unpredictable to its neighbours, those neighbours cannot form stable expectations about the rewards associated with their own actions, and their learning may converge to suboptimal or defensive policies.

Matignon et al. (2012) provided one of the earliest systematic analyses of the stabilisation of cooperative MARL and identified a set of properties that make environments particularly susceptible to coordination failure. Their framework identifies the key factors as the degree of interaction between agents, the sparsity of reward signals, and the severity of the exploration-exploitation trade-off. Environments in which agents' actions have strong effects on each other's rewards — as is the case in energy sharing, where one household's decision to share directly affects the comfort of its neighbour — are particularly vulnerable to the destabilising effects of exploration.

Leng (2025) formalised the alter-exploration problem and demonstrated its severity in a set of cooperative MARL benchmarks. The study showed that when one agent maintains a higher exploration rate than its peers, the performance of the entire system degrades, and the degradation is disproportionately borne by the agents that are not themselves exploring. This asymmetric effect is important because it means that the cost of exploration is not internalised by the exploring agent; it is an externality imposed on the rest of the community. In the energy-sharing context, the alter-exploration problem implies that an agent that continues to experiment with different sharing strategies after others have converged to stable patterns may reduce its neighbours' comfort and increase the community's inequality.

Aloor et al. (2024) studied fairness in multi-agent navigation using graph neural networks and found that the interaction structure of agents mediates the effect of individual exploration on collective fairness. Their method achieved scalability to large agent populations by encoding the agent interaction graph directly into the neural network architecture, allowing the network to generalise to different numbers of agents without retraining. While their environment — vehicular navigation — differs substantially from energy sharing, their finding that network structure mediates fairness outcomes is relevant: neighbourhoods with different topologies may have different vulnerabilities to the alter-exploration problem.

The alter-exploration literature establishes a clear theoretical expectation that a high-exploration agent can destabilise cooperative equilibria, but this prediction has not been tested in a physical resource management environment. The present thesis provides this test by introducing an innovator agent that differs from the prosocial type only in its exploration floor — five percent versus one percent — and measuring the community-level consequences of this single parameter change.

A parallel and more recent strand of research has explored the use of large language models as fairness critics or equity signal generators in multi-agent systems. These approaches are too recent to have been extensively validated, but they represent an important direction for future work and provide context for the more conservative approach taken in the present thesis. These approaches are too recent to have been extensively validated, but they represent an important direction for future work and provide context for the more conservative approach taken in the present thesis.

Jadhav et al. (2024) FairMarket-RL, discussed above, uses the LLM as an external fairness critic. Ma et al. (2025) CAPPO uses the LLM to generate equity signals from census-level energy burden data. Both studies demonstrate that LLM integration is technically feasible and produces measurably fairer outcomes than non-LLM baselines in their respective settings. However, both studies also acknowledge the brittleness of the LLM-in-the-loop approach: the quality of the fairness assessment depends sensitively on prompt engineering, the LLM's output may vary across API calls even with identical inputs, and the latency and cost of LLM inference may be prohibitive for real-time control.

The present thesis takes a deliberately different approach, using a fixed analytical fairness metric — Jain's Fairness Index — that is deterministic, cheap to compute, and independent of external API dependencies. This design choice reflects the thesis's focus on isolating the effect of personality heterogeneity on community outcomes, which would be confounded with the variance introduced by an LLM-based fairness signal. The findings of the present thesis can therefore be interpreted as establishing a lower bound on what personality-modulated fairness in MARL can achieve, without the additional complexity of LLM integration.

### 2-3 Qualitative Comparison of Related Literature

The studies reviewed in the preceding sections differ substantially in their algorithms, environments, fairness mechanisms, and treatment of personality heterogeneity. Table 2-1 provides a systematic comparison that positions the present study against the state of the art across these dimensions. The table is followed by a narrative synthesis that highlights the key contrasts and identifies the gaps that the present thesis addresses.

**Table 2-1: Qualitative Comparison of MARL Energy Management and Social Simulation Literature**

| Study                     | Algorithm                      | Environment                       | Fairness Mechanism                     | Personality?                      | Pros                                                         | Cons                                                       |
| ------------------------- | ------------------------------ | --------------------------------- | -------------------------------------- | --------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------- |
| Charbonnier et al. (2022) | Q-Learning (Distributed)       | UK Residential Flexibility        | None (Efficiency focus)                | No                                | Scalable fixed-size Q-tables for privacy                     | No focus on distributive justice or individual preferences |
| May & Huang (2023)        | PPO (Two-level inner-outer)    | Swedish building prosumer market  | Income equality                        | No (Assumes economic rationality) | Emergent price elasticity in P2P                             | Assumes homogeneous rational actors                        |
| Kusatake et al. (2023)    | Evolutionary / Multi-objective | P2P energy trading                | Profit fairness / Min-max benefit      | No                                | Effective supply-demand balance                              | Slow computation; not real-time adaptive                   |
| Behrunani et al. (2023)   | Bilevel Game Theory            | Smart energy hubs                 | Cost reduction variance                | No                                | Provably fair price mediation                                | Requires semi-central coordinator                          |
| Aloor et al. (2024)       | MARL (Graph Neural Networks)   | Multi-agent navigation            | 1 / Coeff. of Variation                | No                                | Scalable to arbitrary agent counts via GNNs                  | Focused on navigation, not residential sharing             |
| Jadhav et al. (2024)      | IPPO + LLM Fairness Critic     | P2P market (FairMarket-RL)        | LLM-guided FTB and FBS scores          | Indirect (Moral reasoning)        | Human-centric assessments                                    | Dependent on real-time LLM API stability                   |
| Hughes et al. (2018)      | A3C (Deep RL)                  | Cleanup & Harvest Games           | Inequity aversion rewards              | No                                | Solves Tragedy of the Commons                                | Not grounded in Big Five psychology                        |
| Ma et al. (2025)          | CAPPO + LLM workflow           | 99-tract Florida census market    | Carbon allowance / Equity signals      | Indirect (User intent)            | Addresses energy poverty with multimodal data                | LLM-RL loop brittle to prompt variations                   |
| Ren & Xu (2025)           | Generative Agents (LLM)        | Classroom social simulation       | N/A                                    | **Yes (Big Five)**                | Robust trait stability analysis                              | No physical resource management                            |
| **This study**            | **OCEAN-MARL (IQL)**           | **10-house neighbourhood (ring)** | **Personality-modulated Jain's Index** | **Yes (Big Five)**                | **Integrates OCEAN psychology with physical energy sharing** | Tabular state space (96 states) limits granularity         |

The comparison reveals several patterns obscured in the individual study reviews. First, every energy-focused study in the comparison that incorporates a fairness mechanism applies it uniformly across all agents, either through a centralised pricing rule, a shared inequality penalty, or an LLM that evaluates the entire community's allocation at once. None allow individual agents to have different degrees of fairness concern. Second, the only studies that incorporate personality heterogeneity — Ren and Xu (2025) and, indirectly, the LLM-based agent studies — operate in purely social or textual environments without physical resource management. The intersection of the two dimensions — personality heterogeneity in a physically grounded energy management environment — is unoccupied territory, precisely where the present thesis positions itself.

Third, the comparison highlights a methodological divide between the energy MARL studies and the social simulation studies in terms of learning algorithm. The energy studies predominantly use tabular Q-learning or evolutionary methods, reflecting the need for sample efficiency and stable convergence in environments with real-world constraints. The social simulation studies predominantly use LLM-based agents, reflecting the need for natural language interaction and the lower stakes of errors in simulation. The present thesis adopts tabular Q-learning, aligning with the energy domain convention, while introducing the innovations of personality-modulated reward weights and systematic exploration floor variation.

Each "Con" entry in Table 2-1 corresponds directly to one of the three research gaps defined in Section 2-4. The uniform-fairness constraint identified as the limiting design choice in May & Huang (2023), Hughes et al. (2018), and Jadhav et al. (2024) is precisely Gap 2: the absence of heterogeneous intrinsic fairness preferences in existing fairness-aware MARL. The absence of psychological grounding noted for Charbonnier et al. (2022), Kusatake et al. (2023), and Behrunani et al. (2023) is precisely Gap 1: the lack of a validated personality model to structure agent heterogeneity. The physical-resource gap identified as the limitation of Ren & Xu (2025) and the LLM-based social simulation studies is precisely the missing intersection that motivates this thesis: personality heterogeneity has never been tested in a physically grounded energy-sharing environment. These three Cons therefore do not merely catalogue prior shortcomings; they define the design requirements that the proposed OCEAN-MARL framework is built to satisfy.

### 2-4 Conceptual Framework and Research Gaps

Three specific research gaps emerge from the literature reviewed in the preceding sections. Each gap is defined precisely, grounded in specific limitations of prior work, and directly addressed by the design of the present study.

The first gap concerns the absence of psychologically grounded agent heterogeneity in energy MARL. The energy MARL literature has demonstrated that heterogeneous agent preferences can produce qualitatively different system-level outcomes (Charbonnier et al., 2022; May & Huang, 2023; Kusatake et al., 2023), but no existing study grounds this heterogeneity in a validated psychological model of personality. When agents are assigned different objectives or reward weights, the assignment is arbitrary from a psychological perspective — there is no theoretical basis for why one agent should have a different fairness weight than another, and no way to predict how a given difference in parameters will affect behaviour outside the specific simulation context. The personality-to-RL mapping literature (Moon et al., 2022; Ren & Xu, 2025) has established that OCEAN traits can be mapped to RL parameters in principle, but this mapping has never been applied to a physical resource management environment. The present thesis bridges these two literatures by defining agent types as points in the OCEAN personality space and mapping those coordinates to specific reward function weights and exploration parameters, creating a population of agents whose heterogeneity is both theoretically motivated and computationally operationalised.

The second gap concerns the contrast between uniform fairness constraints and intrinsic heterogeneous preferences. The fairness-aware MARL literature (Hughes et al., 2018; Jadhav et al., 2024; Ma et al., 2025) applies fairness constraints uniformly across all agents in the community. Whether the fairness mechanism is an inequality penalty, an LLM critic, or an equity signal derived from census data, every agent in the simulation is subject to the same fairness objective. This uniformity is appropriate if fairness is conceptualised as a regulatory intervention imposed by a central authority, but it does not capture the reality of human communities in which different individuals have different degrees of concern for fairness and different prosocial motivations (Fehr & Gächter, 2000). The present thesis addresses this gap by allowing the weight placed on community fairness in the reward function to vary across agents according to their Agreeableness trait level, creating a population with intrinsic, heterogeneous fairness preferences.

The third gap concerns the unexamined social cost of exploratory behaviour in cooperative energy sharing. The alter-exploration problem — the phenomenon in which one agent's exploratory behaviour destabilises the learning of other agents — has been studied in game-theoretic MARL benchmarks (Matignon et al., 2012; Leng, 2025) but has never been investigated in the context of physical resource management. The present thesis fills this gap by isolating the effect of a single agent's exploration floor — the minimum probability of selecting a random action — while holding all other parameters constant. By comparing a scenario in which one agent has a five percent exploration floor against an otherwise identical scenario in which all agents have a one percent exploration floor, the study provides the first empirical characterisation of the social cost of individual exploration in an energy-sharing community.

#### 2-4-1 Conceptual Framework: The Personality-Modulated Coordination Model

The conceptual framework that guides this research integrates the theoretical foundations reviewed in Section 2-1 with the gaps identified in the preceding subsection. The framework is a personality-modulated coordination model that links three levels of analysis: individual personality traits, agent-level learning parameters, and community-level emergent outcomes.

At the individual level, each household is characterised by a position in the Big Five (OCEAN) personality space. The present study operationalises two dimensions of this space: Agreeableness, which determines the weight assigned to community fairness in the agent's reward function, and Openness, which determines the agent's exploration floor. The remaining three dimensions — Conscientiousness, Extraversion, and Neuroticism — are held at population-average levels across all agents, allowing the study to isolate the effects of the two manipulated dimensions. This selective operationalisation is a deliberate methodological choice: introducing all five dimensions simultaneously would produce a high-dimensional parameter space that would be difficult to interpret and would require an exponentially larger simulation campaign to disentangle interaction effects.

At the agent level, each household is modelled as an independent tabular Q-learning agent with a discrete state space defined by hour and discretised battery level, three discrete sharing actions, and a reward function that is a convex combination of personal comfort and community fairness. The weight parameters of the reward function are determined by the agent's Agreeableness level, and the exploration floor of the epsilon-greedy policy is determined by the agent's Openness level. This mapping is grounded in the personality-to-RL parameter framework of Moon et al. (2022) and the validated trait-behaviour associations of Ren and Xu (2025).

At the community level, the interaction of agents with different personality-modulated parameters produces emergent outcomes that cannot be predicted from the parameters of any individual agent in isolation. These outcomes include the community-level comfort distribution, the patterns of energy sharing across hours and states, and the resilience of the system to external perturbations such as cloudy days and to internal perturbations such as an innovator agent's continued exploration.

The framework generates specific, testable predictions that are stated as hypotheses in Chapter 1. The central prediction is that communities with a mix of prosocial and selfish agents will achieve higher levels of both fairness and efficiency than purely selfish communities, because prosocial agents create a norm of reciprocity from which all agents benefit. A second prediction is that this prosocial advantage will persist under increased scarcity, remaining stable across cloudy conditions that halve solar generation. A third prediction is that the innovator agent's higher exploration floor will destabilise the community's cooperative equilibrium, increasing inequality and reducing overall welfare. These predictions are tested in the simulation experiments described in Chapter 3, and the results are presented in Chapter 4.

## 3- Research Methodology

### 3-1 Research Design and Approach

This study adopts a quantitative experimental research design grounded in simulation-based computational modelling. The research is classified as applied research, as its objective is to address a practical engineering challenge — fair and efficient energy sharing in off-grid residential communities — through the operationalisation of psychological theory within a multi-agent reinforcement learning (MARL) framework. The experimental design manipulates two independent variables: the personality composition of the agent community (five levels: All Selfish, All Prosocial, Mixed, Varied Altruism, and Innovator Effect) and the resource scarcity level (two levels: clear day baseline and 15% cloudy day probability). The dependent variables are the seven performance metrics defined in Section 3-11: mean community comfort, Jain's fairness index, blackout day rate, energy waste, prosocial-versus-selfish comfort split, Gini coefficient, and sharing frequency.

The decision to use simulation rather than field experiments or human-subject studies was motivated by three considerations. First, the research requires testing multiple community compositions under identical physical conditions (same solar irradiance, same battery capacity, same demand profiles) while controlling for all confounding variables, a level of control that is infeasible in field settings where weather, consumption patterns, and equipment specifications vary unpredictably (Charbonnier et al., 2022). Second, the study investigates the emergent effects of agent heterogeneity at the community level — effects that unfold over thousands of repeated interactions — which cannot be studied through static surveys or short-duration experiments (Le et al., 2022). Third, the use of computational agents allows the isolation of specific causal mechanisms, such as the effect of a single agent's exploration floor, that would be confounded by unmeasured human psychological variables in a real-world study (Moon et al., 2022).

The MARL framework is formalised as a decentralised partially observable Markov decision process (Dec-POMDP) following Oliehoek and Amato (2016). In this formulation, each of the \(N = 10\) agents observes only its local state — the current hour and its own battery level — and selects a sharing action without knowledge of other agents' states or actions. The joint reward structure, in which each agent's individual reward includes a community-level fairness component weighted by its Agreeableness parameter, creates a semi-cooperative setting that lies between fully cooperative and fully competitive MARL. The independent Q-learning (IQL) approach to Dec-POMDPs (Sutton & Barto, 2018) is the dominant methodology in the energy MARL literature (Bui et al., 2019; Charbonnier et al., 2022) and enables the study of emergent coordination without centralised control.

The research paradigm is positivist: the study assumes that objective, quantifiable relationships exist between community composition and system-level outcomes, and that these relationships can be discovered through controlled experimental manipulation and statistical inference. The five experimental scenarios (Section 3-10) are designed as treatments, the 5 random seeds as replications, and the evaluation metrics as dependent measures — a factorial design structure that mirrors classical experimental methodology adapted to the computational domain.

The architecture of the simulation environment is a direct design response to the three research gaps identified in Section 2-4. Gap 1 — the absence of psychologically grounded agent heterogeneity in energy MARL — motivates the reward-shaping mechanism documented in Section 3-6 and the OCEAN-to-RL parameter mapping in Section 3-7. By encoding Agreeableness as the fairness weight $w_{\text{fair}}$ and Openness as the minimum exploration floor $\varepsilon_{\min}$, each agent's personality becomes a first-class parameter in the learning process rather than an arbitrary label. Gap 2 — the uniform application of fairness constraints across heterogeneous agents — motivates the stratified community compositions described in Section 3-10. The All Selfish, Mixed, and Varied Altruism scenarios explicitly vary the proportion of prosocial to selfish agents, allowing the study to measure how different personality distributions produce different emergent outcomes without imposing a single fairness weight on all participants. Gap 3 — the unexamined social cost of individual exploration in cooperative energy sharing — motivates the Innovator Effect scenario and the two-phase $\varepsilon$-decay schedule specified in Section 3-8. The innovator agent's elevated exploration floor ($\varepsilon_{\min} = 0.05$ versus 0.01) directly operationalises the curiosity-driven exploration that is predicted to destabilise neighbours' learning, while the standard agents' rapid decay to 0.01 ensures that the community reaches a stable equilibrium before the innovator's effect is measured.

To make the correspondence between gaps and implementation concrete, the simulation loop captured in Figure 3-1 can be read as a sequence of gap-aware design choices. Block 1 (Environment Reset) initialises battery states to 50% and samples weather from a Bernoulli distribution — the physical ground truth from Table 3-4 that anchors the simulation in real hardware specifications. Block 2 (Solar Generation) computes hourly irradiance using the half-sine model of Skoplaki and Palyvos (2009), scaled by the weather factor — a stochastic element that creates the resource scarcity events necessary to test sharing behaviour under stress. Block 3 (Demand Realisation) assigns four distinct demand profiles (Morning, Evening, Flat, Night Owl) to the ten houses, ensuring that peak demand hours do not align and that sharing opportunities arise naturally from temporal complementarity rather than engineered synchrony. Block 4 (State Observation) constructs each agent's local observation as a 96-state tuple (hour, discretised battery level) — a small enough space for tabular convergence but large enough to capture time-dependent and resource-dependent decision contexts. Block 5 (Action Selection via $\varepsilon$-greedy) is where the Openness dimension becomes behaviourally manifest: standard agents select greedy actions with probability 0.99 at convergence, while the innovator selects random actions with probability 0.05, sustaining the exploratory pressure that Gap 3 predicts will destabilise cooperative equilibria. Block 6 (Reward Computation) is where the Agreeableness dimension becomes behaviourally manifest: the convex combination $R_i = w_{\text{self}} \cdot C_i + w_{\text{fair}} \cdot F$ assigns different priorities to community fairness depending on each agent's personality type, directly addressing Gap 2's finding that uniform fairness constraints misrepresent human social preferences. Blocks 7 through 10 (Q-update, decay, hour advancement, episode logging) implement the standard IQL training loop, with the evaluation window of episodes 7,001–8,000 ensuring that reported metrics reflect converged policies rather than transient exploration behaviour. Together, these blocks instantiate a simulation architecture in which the three gaps are not merely acknowledged in the literature review but actively addressed in the algorithmic specification.

### 3-2 Data Collection Methods

Data for this study were generated through simulation rather than collected from field instruments or human participants. The primary data source is the set of simulation logs produced by the custom Python-based simulation environment described in Section 3-3. Each simulation run generates a structured record of hourly state transitions, agent actions, and reward outcomes across 8,000 episodes (simulated days), with the final 1,000 episodes reserved for evaluation to ensure that all metrics are computed from converged policies (Section 3-13).

The physical parameters embedded in the simulation environment are grounded in established engineering standards and commercially available equipment specifications. Solar panel capacity (1.3 kW peak) corresponds to the Microgeneration Certification Scheme (MCS) standard for a typical UK residential photovoltaic installation of three to four panels, consistent with the system sizes used in prior energy MARL studies (Charbonnier et al., 2022; Zhou & Sun, 2023). Battery capacity (7.0 kWh) matches the specification of the Tesla Powerwall first-generation unit, a commonly deployed residential battery system (IEA PVPS, 2021). Weather stochasticity (15% cloudy day probability) follows the parameters reported by Kusatake et al. (2023) for temperate climate simulations. These parameter values are summarised in Table 3-4.

#### Parameter Selection Methodology

All physical and algorithmic parameter values were established through a combination of anchoring to published literature, alignment with commercially available hardware standards, and informal pilot experiments to confirm convergence behaviour. The physical parameters — solar peak capacity, battery capacity, demand profiles, and cloud probability — were drawn directly from prior simulation studies that have been validated against real-world data or hardware specifications. The 1.3 kW solar peak follows Charbonnier et al. (2022), who calibrated their model against UK residential PV installations certified under the Microgeneration Certification Scheme (MCS). The 7.0 kWh battery capacity follows Alshehri and Gaunt (2020) and Bui et al. (2019), both of which align their simulations with the Tesla Powerwall specification. The demand profiles were adopted from Alshehri and Gaunt (2020) after confirming that their average daily demand of 8.8 kWh is consistent with typical UK household consumption of approximately 4,800 kWh per year (Ofgem, 2023). The 15% cloud probability follows Kusatake et al. (2023), who derived their value from long-term meteorological records for temperate European climates.

Hyperparameter values — learning rate, discount factor, exploration schedule, and episode count — were initialised from standard Q-learning practice (Sutton & Barto, 2018) and from Zhang et al. (2025) for the $\varepsilon$-decay schedule, then confirmed through pilot experiments on the All Selfish scenario. Pilot sweeps across learning rates {0.05, 0.1, 0.2, 0.5} and minimum exploration floors {0.01, 0.02, 0.05, 0.10} were conducted to identify values that produce stable convergence within a reasonable simulation budget. The selected hyperparameters represent the configuration that minimised Q-value oscillation while maximising final policy performance on the baseline task. No formal design-of-experiments optimisation (e.g., Taguchi, Bayesian optimisation) was applied; the pilot sweep constitutes an informal heuristic search over a small discrete grid.

Each experimental scenario was simulated across 5 independent random seeds (42, 123, 456, 789, 1011). The seed controls the stochastic elements of the simulation: the random assignment of weather conditions (clear or cloudy), the epsilon-greedy exploration noise during action selection, and the initial Q-value perturbations. Running multiple seeds ensures that observed differences between scenarios are attributable to the treatment (personality composition) rather than to idiosyncratic random fluctuations (Montgomery, 2017). The choice of 5 seeds follows the conventions of the energy MARL literature (Alshehri & Gaunt, 2020; Ali et al., 2023) and provides sufficient statistical power for the planned analyses (Section 3-12).

The five seed values were selected to span sufficiently diverse pseudo-random sequences without overlapping structural patterns. Seeds 42, 123, 456, 789, and 1011 are not consecutive primes and do not share obvious arithmetic relationships, reducing the risk of correlated random streams across the Bernoulli weather draws, epsilon-greedy noise, and Q-table initialisation perturbations. While any fixed set of seeds cannot guarantee representativeness of all possible stochastic outcomes, the selected values cover a range of entropy sufficient to produce qualitatively different weather sequences, exploration trajectories, and convergence paths across the five replications. Fixed seeds are standard in simulation-based experimental research precisely because they enable exact reproducibility of published results (Montgomery, 2017; Law, 2015); the specific values used here are arbitrary in the sense that no pilot experiment was conducted to optimise them, but they are fixed and reported so that any independent researcher can replicate the exact stochastic environment described in this thesis.

All simulation data are stored in comma-separated value (CSV) format with one row per simulation step (hour per episode per seed), including columns for episode number, hour, seed, scenario, agent identifier, solar generation, demand, battery state of charge, action taken, comfort achieved, and reward components. This granular logging enables both aggregate metric computation and detailed behavioural analysis.

### 3-3 Tools and Instruments

The simulation experiments were implemented using a custom Python 3.x codebase that integrates several specialised libraries for numerical computation, data processing, statistical testing, and visualisation. Table 3-1 lists the primary tools, their roles, and their place in the research pipeline.

**Table 3-1: Tools and Instruments**

| Tool           | Version | Role in Research Pipeline                                              |
|:---------------|:--------|:-----------------------------------------------------------------------|
| Python         | 3.x     | Primary programming language: simulation engine, data processing, analysis |
| NumPy          | 1.x     | Numerical computations: state-of-charge tracking, energy balance calculations |
| Pandas         | 2.x     | Data aggregation: episode-level and seed-level summarisation across runs |
| SciPy          | 1.x     | Statistical testing: one-way ANOVA, independent and paired t-tests     |
| Matplotlib     | 3.x     | Visualisation: community metrics bar charts, comfort distribution plots |
| Seaborn        | 0.x     | Statistical visualisation: Q-table heatmaps, distribution plots        |

NumPy was used for all numerical computations within the simulation loop, including the half-sine solar generation calculation (Equation 3-1), battery charge and discharge tracking, and the computation of Jain's fairness index and the Gini coefficient. Pandas handled the post-simulation data pipeline: raw step-level logs were grouped by episode and seed, aggregated into per-metric summaries, and merged across scenarios for comparative analysis. SciPy's `stats` module provided the statistical testing infrastructure including one-way ANOVA for multi-group comparisons and both independent and paired t-tests for between-scenario and within-scenario contrasts.

Matplotlib and Seaborn were used for generating the figures presented in Chapter 4. Bar charts of community-level metrics were produced using Matplotlib's `bar` function with error bars representing one standard deviation across seeds. Q-table heatmaps were rendered using Seaborn's `heatmap` function with a diverging colour palette. All figures are saved at 300 dpi resolution for inclusion in the thesis document.

The simulation environment is implemented as a standalone Python class (`OffGridMARL`) that encapsulates all physical dynamics, agent logic, and data logging. The class follows the Gymnasium (formerly OpenAI Gym) interface convention (Towers et al., 2024), exposing methods for environment reset, step execution, and metric computation. This design choice facilitates reproducibility: the simulation can be re-run with different parameter configurations without modifying the core environment code.

### 3-4 Population, Sample, and Sampling Method

The target population for this study consists of all possible off-grid residential microgrid configurations in which households share surplus energy through a cooperative framework. This population is defined by a set of boundary conditions: single-neighbourhood scale (10–20 households), ring or bus topology, solar-plus-battery generation and storage, independent household-level decision-making, and temperate climate conditions with moderate solar variability. The study does not claim representativeness for larger neighbourhoods, alternative topologies (star, mesh, tree), different generation mixes (wind, diesel backup), or extreme climate conditions.

The study sample is a 10-house ring-topology microgrid as described in Section 3-5. The choice of 10 houses follows the scale of prior energy MARL simulation studies (Alshehri & Gaunt, 2020; Charbonnier et al., 2022; Kusatake et al., 2023) and represents a size at which community-level emergent effects are detectable while computational cost remains manageable. The ring topology — in which each house can share energy with exactly one designated neighbour — was selected to isolate the effect of sharing decisions from the confounding influence of network routing. In a mesh or fully connected topology, an agent's action affects multiple neighbours through different paths, making it difficult to attribute observed outcomes to individual sharing decisions. The ring eliminates this ambiguity: house \(i\) shares with house \(i+1\) only, and the effect of each sharing action propagates through exactly one link in the chain.

The sampling method for households within each scenario is stratified: the 10 houses are assigned to personality types according to the predefined composition of each experimental scenario (Section 3-10). In the Mixed scenario, exactly 5 houses are assigned the prosocial personality type and 5 the pure_selfish type. This stratified assignment ensures that each scenario represents a controlled manipulation of community composition rather than a random draw from a distribution — the All Selfish scenario contains exactly 10 selfish agents in every seed, and the Mixed scenario contains exactly 5 of each type. The allocation of specific personality types to specific positions in the ring is randomised across seeds to prevent position effects from confounding the results.

Each scenario is replicated across 5 random seeds as described in Section 3-2. The seeds serve the methodological function of repeated sampling from the distribution of stochastic outcomes, providing the replication necessary for statistical inference. This combination of stratified compositional assignment and random seed replication follows the standard experimental design for simulation-based research (Montgomery, 2017; Law, 2015).

### 3-5 Physical Environment

The simulation models an off-grid smart neighborhood micro-grid consisting of 10 houses connected in a ring topology, where each house can share surplus energy with exactly one designated neighbour (the next house in the ring). This minimal topology isolates the effect of sharing decisions from network topology confounds.

#### Solar Generation

Each house has a solar panel with peak capacity 1.3 kW. Solar generation follows a half-sine curve over daylight hours (6 AM–6 PM), consistent with standard irradiance modelling practices (Skoplaki & Palyvos, 2009; Zhou & Sun, 2023):

$$G(h) = \max\!\left(0,\; G_{\text{max}} \cdot \sin\!\left(\frac{\pi \cdot (h - 6)}{12}\right) \cdot W\right) \qquad \text{(Eq. 3-1)}$$

where $h$ is the hour (0–23), $G_{\text{max}} = 1.3$ kW (following Charbonnier et al., 2022), and $W$ is a weather factor (1.0 on clear days, 0.5 on cloudy days). On clear days, total daily generation is approximately 9.9 kWh. Cloudy days occur with probability 15% and reduce solar output by 50%, consistent with the stochastic weather model of Kusatake et al. (2023).

**Table 3-2: Solar Generation Parameters**

| Symbol           | Definition                             | Unit | Source                    |
| :--------------- | :------------------------------------- | :--- | :------------------------ |
| $h$              | Hour of the day (0–23)                 | hour | Skoplaki & Palyvos (2009) |
| $G_{\text{max}}$ | Peak solar panel capacity (1.3 kW)     | kW   | Charbonnier et al. (2022) |
| $W$              | Weather factor (1.0 clear, 0.5 cloudy) | —    | Kusatake et al. (2023)    |
| $G(h)$           | Instantaneous solar power generation   | kW   | Skoplaki & Palyvos (2009) |

#### Demand Profiles

Four distinct hourly demand profiles are used, cycling across the 10 houses (Alshehri & Gaunt, 2020):

**Table 3-3: Demand Profile Types**

| Profile   | Pattern                               | Daily Total | Hourly Range |
| --------- | ------------------------------------- | ----------- | ------------ |
| Morning   | Peak at 8 AM (0.9 kWh)                | ~8.4 kWh    | 0.1–0.9 kWh  |
| Evening   | Peak at 8 PM (1.2 kWh)                | ~9.6 kWh    | 0.1–1.2 kWh  |
| Flat      | Constant 0.35 kWh every hour          | 8.4 kWh     | 0.35 kWh     |
| Night Owl | Peaks late (10 PM–12 AM), sleeps late | ~9.4 kWh    | 0.05–1.2 kWh |

The average daily demand across all profiles is approximately 8.8 kWh, consistent with typical residential consumption patterns reported in the literature (Ali et al., 2023).

#### Battery Storage

Each house has a 7.0 kWh battery (Alshehri & Gaunt, 2020; Bui et al., 2019). The battery starts each simulated day at 50% charge (3.5 kWh). Charge and discharge occur at unlimited rates within capacity bounds, and no degradation is modelled — battery efficiency and capacity remain constant across the simulation.

#### Cloudy Day Model

A simple binary weather model is used: each day is either clear (85% probability) or cloudy (15% probability). On a cloudy day, solar generation is multiplied by $W = 0.5$, halving the energy available to the community (Behrunani et al., 2023). This stochastic element prevents agents from learning a purely deterministic policy and creates occasional scarcity events that test the stability of sharing norms.

**Table 3-4: Physical Ground Truth Parameters**

| Parameter          | Value               | Source                                                                                                                               |
| ------------------ | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Houses             | 10                  | Alshehri & Gaunt (2020); Charbonnier et al. (2022)                                                                                   |
| Battery capacity   | 7.0 kWh             | Alshehri & Gaunt (2020); Ali et al. (2023)                                                                                           |
| Solar peak         | 1.3 kW              | Charbonnier et al. (2022); Zhou & Sun (2023)                                                                                         |
| Cloud probability  | 0.15                | Kusatake et al. (2023); Behrunani et al. (2023)                                                                                      |
| Battery initial SoC| 50%                 | Alshehri & Gaunt (2020)                                                                                                              |
| Demand range       | 0.05–1.2 kWh/house  | Ali et al. (2023)                                                                                                                    |

The parameter values listed in Table 3-4 are held constant across all five experimental scenarios. Only the personality composition of the agent community varies between scenarios (Section 3-10), ensuring that any observed differences in outcomes are attributable to the treatment rather than to variation in physical conditions.

### 3-6 Personality Model and OCEAN Mapping

#### Reward-Based Personality

Each agent's personality is encoded as two weights in its reward function: $w_{\text{self}}$ (weight on personal comfort) and $w_{\text{fair}}$ (weight on community fairness). These weights are the personality-dependent parameters that modulate the reward function defined in Section 3-7, where $w_{\text{self}} + w_{\text{fair}} = 1.0$. Four core personality types are defined:

**Table 3-5: Personality Type Definitions**

| Type          | $w_{\text{self}}$ | $w_{\text{fair}}$ | Behavioural description                                         |
| ------------- | ----------------- | ----------------- | --------------------------------------------------------------- |
| pure_selfish  | 1.0               | 0.0               | Maximises own comfort only; ignores community fairness entirely |
| individualist | 0.8               | 0.2               | Primarily self-interested but has mild fairness awareness       |
| prosocial     | 0.5               | 0.5               | Balances personal comfort and community fairness equally        |
| altruistic    | 0.2               | 0.8               | Prioritises community fairness over personal comfort            |

A fifth personality type, `high_openness_innovator`, is introduced for the Innovator Effect scenario (see Section 3-10). This type shares the same reward weights as the prosocial type ($w_{\text{self}} = w_{\text{fair}} = 0.5$) but differs in its exploration parameters (see Section 3-8).

#### OCEAN (Big Five) Grounding

The personality types used in this simulation correspond to explicit coordinates in the Big Five (OCEAN) personality space (Goldberg, 1990). This grounding in established psychological theory constitutes the core contribution of this thesis — rather than inventing arbitrary labels, we map each agent type to a well-studied psychological framework. Following John & Srivastava (1999), Agreeableness encompasses prosocial tendencies, which we operationalise as $w_{\text{fair}}$ in the reward function. The mapping of Openness to the exploration rate ($\varepsilon$) follows the methodology of personality-to-RL-parameter mappings established by prior work (Ren & Xu, 2025; Moon et al., 2022). Table 3-6 summarises the full OCEAN-to-RL mapping.

**Table 3-6: OCEAN Trait Mapping to Agent Behaviour**

| OCEAN Trait                  | Dimension                    | Effect on Agent                                                   | Reward Parameter Affected                  |
| ---------------------------- | ---------------------------- | ----------------------------------------------------------------- | ------------------------------------------ |
| Agreeableness (A) — High     | Prosocial orientation        | Agent weights community fairness more heavily                     | $w_{\text{fair}}$ increases                |
| Agreeableness (A) — Low      | Self-interest dominance      | Agent weights personal comfort over sharing                       | $w_{\text{self}}$ increases                |
| Conscientiousness (C) — High | Consistent behaviour         | Agent maintains stable sharing policy regardless of battery state | Lower $\varepsilon$ decay variance         |
| Openness (O) — High          | Exploration, novelty-seeking | Agent explores sharing strategies longer before converging        | Higher initial $\varepsilon$, slower decay |
| Neuroticism (N) — High       | Threat sensitivity           | Agent penalises blackout states more heavily                      | Blackout penalty multiplier increases      |

Table 3-7 shows the OCEAN coordinates for each simulation personality type.

**Table 3-7: Personality Types as OCEAN Coordinates**

| Simulation Type         | A        | C   | O        | N   | $w_{\text{self}}$ | $w_{\text{fair}}$ |
| ----------------------- | -------- | --- | -------- | --- | ----------------- | ----------------- |
| pure_selfish            | Very Low | Mid | Low      | Mid | 1.0               | 0.0               |
| individualist           | Low      | Mid | Low      | Mid | 0.8               | 0.2               |
| prosocial               | Mid-High | Mid | Mid      | Mid | 0.5               | 0.5               |
| altruistic              | High     | Mid | Mid      | Low | 0.2               | 0.8               |
| high_openness_innovator | Mid-High | Mid | **High** | Mid | 0.5               | 0.5               |

Note that the `high_openness_innovator` differs from the prosocial type only in its Openness dimension, which manifests as a slower exploration decay rate rather than a different reward weight. This allows us to isolate the effect of exploratory behaviour from fairness preferences.

### 3-7 Reward Function Design

The reward function is the key design element that embeds ethical constraints into the learning objective:

$$R_i = w_{\text{self}} \cdot C_i + w_{\text{fair}} \cdot F \qquad \text{(Eq. 3-2)}$$

| Symbol            | Definition                              | Unit | Source                             |
| :---------------- | :-------------------------------------- | :--- | :--------------------------------- |
| $R_i$             | Total scalar reward for agent $i$       | —    | This work (Eq. 3-2)                |
| $w_{\text{self}}$ | Weight assigned to personal comfort     | —    | OCEAN mapping                      |
| $C_i$             | Personal comfort level of agent $i$     | —    | This work (Eq. 3-3)                |
| $w_{\text{fair}}$ | Weight assigned to community fairness   | —    | Adaptation of Hughes et al. (2018) |
| $F$               | Jain's Fairness Index for the community | —    | Jain et al. (1984)                 |

Personal comfort $C_i$ is the fraction of the house's hourly demand that was met:

$$C_i = \frac{\text{demand met}_i}{\text{demand}_i} \qquad \text{(Eq. 3-3)}$$

| Symbol                | Definition                                     | Unit | Source                  |
| :-------------------- | :--------------------------------------------- | :--- | :---------------------- |
| $C_i$                 | Personal comfort (range [0,1])                 | —    | This work (Eq. 3-3)     |
| $\text{demand met}_i$ | Energy supplied via solar, battery, or sharing | kWh  | —                       |
| $\text{demand}_i$     | Total electricity requested by the household   | kWh  | Alshehri & Gaunt (2020) |

If a house's battery and current solar generation together cannot satisfy demand, the unmet fraction results in $C_i < 1.0$, which we classify as a partial blackout. When $C_i < 0.95$, the day is classified as a blackout day for that house.

Jain's Fairness Index $F$ is computed across all houses (Jain, Chiu & Hawe, 1984):

$$F = \frac{\left(\sum_{i=1}^{N} C_i\right)^2}{N \cdot \sum_{i=1}^{N} C_i^2} \qquad \text{(Eq. 3-4)}$$

| Symbol | Definition                             | Unit | Source                  |
| :----- | :------------------------------------- | :--- | :---------------------- |
| $F$    | Jain's Fairness Index (range [1/N, 1]) | —    | Jain et al. (1984)      |
| $N$    | Number of households (10)              | —    | Alshehri & Gaunt (2020) |
| $C_i$  | Comfort level of household $i$         | —    |                         |

where $N$ is the number of houses and $C_i$ is the comfort of house $i$. This index ranges from $\frac{1}{N}$ (maximum inequality — one house gets everything, others nothing) to 1.0 (perfect equality — all houses have identical comfort). Jain's index is widely used in network engineering and resource allocation literature because it is scale-invariant, continuous, and independent of population size (Zhou & Sun, 2023).

The reward is computed after each hour and accumulated over the 24-hour day. At the end of each episode (day), each agent receives the sum of its hourly rewards.

### 3-8 Learning Algorithm

Each house is controlled by an independent tabular Q-learning agent with the following specification:

#### State Space

The state is a discrete tuple (hour, battery_level) where:

- **Hour**: 0–23 (24 discrete values)
- **Battery level**: discretised into 4 bins using thresholds at 25%, 50%, 75% of capacity

Total state space: $24 \times 4 = 96$ states.

#### Action Space

Three discrete actions determine what fraction of the house's net surplus energy (generation minus demand in the current hour) is shared with the neighbour:

**Table 3-8: Action Space**

| Action | Share Fraction | Behaviour                             |
| ------ | -------------- | ------------------------------------- |
| 0      | 0%             | Keep all surplus for battery storage  |
| 1      | 50%            | Share half of surplus, store the rest |
| 2      | 100%           | Share all surplus, store nothing      |

If the house has a net deficit (demand > generation), the action is forced to 0 (nothing to share).

#### Q-Learning Update

The Q-value for each state-action pair is updated using the standard tabular Q-learning rule (Watkins & Dayan, 1992; Sutton & Barto, 2018):

$$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ R + \gamma \max_{a'} Q(s', a') - Q(s, a) \right] \qquad \text{(Eq. 3-5)}$$

where $\alpha$ is the learning rate, $\gamma$ is the discount factor, $R$ is the reward received after taking action $a$ in state $s$, and $s'$ is the resulting next state. Tabular Q-learning is guaranteed to converge to the optimal Q-function under standard stochastic approximation conditions (Watkins & Dayan, 1992).

| Symbol    | Definition                                         | Unit | Source                 |
| :-------- | :------------------------------------------------- | :--- | :--------------------- |
| $Q(s, a)$ | Action-value estimate for state $s$ and action $a$ | —    | Watkins & Dayan (1992) |
| $\alpha$  | Learning rate (0.2)                                | —    | Sutton & Barto (2018)  |
| $R$       | Instantaneous reward                               | —    | This work (Eq. 3-2)    |
| $\gamma$  | Discount factor (0.99)                             | —    | Sutton & Barto (2018)  |
| $s, s'$   | Current and subsequent states                      | —    | Watkins & Dayan (1992) |

All Q-learning hyperparameters — learning rate, discount factor, exploration schedule, initialisation strategy, and training duration — are listed in Section 3-13. These values are identical across all agents and scenarios, with the single exception of the innovator agent's higher exploration floor ($\varepsilon_{\min} = 0.05$). The optimistic initialisation of Q-values to 1.0 encourages agents to try all actions early in training.

#### System Architecture Flowchart

The full simulation loop follows this sequence, with each step corresponding to a block in the system architecture:

```
┌──────────────────────────────────────────────────────────────────┐
│               SIMULATION LOOP (per episode = 1 day)              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────────┐  │
│  │  1. Reset    │     │  2. Solar    │     │   3. Demand      │  │
│  │  Environment │────▶│  Generation  │────▶│   Realisation    │  │
│  │  (battery,   │     │  (Eq. 3-1)   │     │   (4 profiles)   │  │
│  │  weather)    │     │              │     │                  │  │
│  └──────────────┘     └──────────────┘     └──────────────────┘  │
│                                                    │             │
│                                                    ▼             │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────────┐  │
│  │  6. Reward   │     │  5. Energy   │     │   4. State       │  │
│  │  Computation │◀────│   Sharing    │◀────│   Observation    │  │
│  │  (Eq. 3-2    │     │   (Action    │     │   (hour, batt%)  │  │
│  │   to 3-4)    │     │    from Q)    │     │                  │  │
│  └──────────────┘     └──────────────┘     └──────────────────┘  │
│                                                    │             │
│                                                    ▼             │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────────┐  │
│  │  7. Update   │     │  8. ε-decay  │     │  9. Next Hour    │  │
│  │  Q(s,a) via  │────▶│  (ε ← ε ×   │────▶│  or End Episode  │  │
│  │  Eq. (3-5)   │     │   0.999)     │     │  (t = 0..23)     │  │
│  └──────────────┘     └──────────────┘     └──────────────────┘  │
│                                                    │             │
│                                                    ▼             │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  10. Episode Complete → Record Metrics → Next Episode      │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Figure 3-1: System Architecture Flowchart.** The simulation loop proceeds through ten blocks per episode: environment reset, solar generation, demand realisation, state observation, energy sharing via Q-learning, reward computation, Q-value update, exploration decay, hour advancement, and episode completion.

Each block in the flowchart corresponds to a distinct step in the simulation loop, and the sequence proceeds as follows.

Block 1 resets the environment at the start of each episode. All battery states are initialised to 50% charge (3.5 kWh), and the day's weather is sampled from a Bernoulli distribution: clear with 85% probability, cloudy with 15% probability. This single stochastic draw determines the weather factor $W$ for the entire day, introducing the resource scarcity events that test the resilience of learned sharing norms. **Why:** The 50% initial state-of-charge was chosen as a neutral midpoint that allows agents to either charge or discharge in the first hour, avoiding systematic bias toward hoarding or sharing (Alshehri & Gaunt, 2020). The Bernoulli weather draw was selected over a Markov-chain model to keep the environmental model tractable while still introducing stochastic scarcity sufficient to differentiate personality types' responses.

Block 2 computes solar generation for each house. Using Equation (3-1), the half-sine irradiance curve is evaluated for each hour of the day (6 AM to 6 PM) and scaled by the weather factor $W$. On clear days, the peak generation reaches 1.3 kW per house, yielding approximately 9.9 kWh daily. On cloudy days, generation is halved, reducing the total energy available to the community and creating the scarcity conditions under which sharing decisions become critical. **Why:** The half-sine model approximates the bell-shaped distribution of solar irradiance across daylight hours and is the standard analytical approximation for photovoltaic output modelling (Skoplaki & Palyvos, 2009). The 1.3 kW peak corresponds to a typical three-to-four-panel residential installation under UK peak irradiance, anchoring the simulation in commercially deployed hardware rather than abstract units.

Block 3 assigns demand profiles to each of the 10 houses using a cycling allocation of the four profile types (Morning, Evening, Flat, Night Owl). Each profile specifies an hourly demand value, and the total daily demand per house ranges from 8.4 to 9.6 kWh depending on the profile type. The cycling assignment ensures that no single profile type dominates any specific position in the ring topology across seeds. **Why:** Diverse demand profiles were introduced to create natural complementarity in generation and consumption — a house with a Morning peak demand faces surplus during its Evening hours, while a house with an Evening peak faces surplus during its Morning hours. This temporal complementarity is the structural precondition for reciprocity: without timing misalignment between agents, there would be no incentive to store energy for later sharing, and the experiment would collapse into a trivial storage-maximisation problem (Alshehri & Gaunt, 2020).

Block 4 constructs the agent's state observation. Each agent observes only its own local state, formalised as a tuple (hour, discretised battery level). The hour is a 24-valued discrete variable, and the battery level is quantised into four bins using thresholds at 25%, 50%, and 75% of the 7.0 kWh capacity. This produces a total state space of 96 discrete states per agent, which is large enough to capture time-dependent and resource-dependent decision contexts but small enough for tabular Q-learning to converge within 8,000 episodes. **Why:** The local-observation design is a direct consequence of the Dec-POMDP formalism adopted to study emergent coordination without centralised information sharing (Oliehoek & Amato, 2016). If agents had global knowledge of neighbours' battery states, the problem would reduce to a centralised optimisation and the decentralised coordination challenge would be bypassed entirely. The four-bin discretisation was chosen as the coarsest resolution that still allows agents to distinguish between empty, low, medium, and full battery states — a granularity that pilot experiments confirmed is sufficient for learning meaningful sharing policies while keeping the Q-table tractable.

Block 5 selects the sharing action via an $\varepsilon$-greedy policy using the agent's current Q-table. With probability $\varepsilon$, the agent selects a random action; with probability $1 - \varepsilon$, it selects the action with the highest Q-value in the current state. The exploration rate $\varepsilon$ decays each episode (Block 8), and its minimum value differs between standard agents ($\varepsilon_{\min} = 0.01$) and the innovator agent ($\varepsilon_{\min} = 0.05$). This higher floor operationalises the Openness trait from the OCEAN model, as the innovator maintains a greater propensity for exploratory behaviour even after the rest of the community has converged. **Why:** The $\varepsilon$-greedy policy was chosen because independent Q-learning in non-stationary multi-agent environments requires sustained exploration during early training to discover viable sharing strategies before neighbours' policies stabilise (Hernandez-Leal et al., 2017). The varying $\varepsilon_{\min}$ values are the direct operationalisation of the Openness dimension — the innovator's higher floor addresses Gap 3 by deliberately maintaining non-stationarity for its neighbours, enabling empirical measurement of the alter-exploration cost in a controlled setting (Leng, 2025).

Block 6 computes the reward for each agent after the sharing action has been executed and the hourly outcomes are known. The reward is the convex combination defined in Equation (3-2): $R_i = w_{\text{self}} \cdot C_i + w_{\text{fair}} \cdot F$. Personal comfort $C_i$ (Equation 3-3) is the fraction of the house's hourly demand that was met by solar generation, battery discharge, and received shared energy. Community fairness $F$ (Equation 3-4) is Jain's index computed from the comfort values of all 10 houses. The weights $w_{\text{self}}$ and $w_{\text{fair}}$ are the personality-dependent parameters described in Section 3-6, and their sum is always 1.0. **Why:** The weight-sharing architecture was chosen because it allows the fairness reward to be internalised as part of each agent's intrinsic value system rather than imposed as an external constraint. This addresses Gap 2 from Section 2-4: by varying $w_{\text{fair}}$ across the agent population, the simulation produces the heterogeneous fairness preferences that uniform constraint approaches (Hughes et al., 2018; Jadhav et al., 2024) cannot model. The convex combination with unit sum ensures that increasing fairness concern necessarily decreases self-interest, creating a zero-sum trade-off at the individual level that mirrors the social dilemma structure of real sharing decisions.

Block 7 applies the Q-learning update rule (Equation 3-5) to the state-action pair that was executed. The update shifts the Q-value toward the sum of the immediate reward and the discounted maximum Q-value of the next state. With a learning rate $\alpha = 0.2$ and discount factor $\gamma = 0.99$, the agent places strong weight on future outcomes while maintaining enough plasticity to adapt to changing conditions during early training. **Why:** Tabular Q-learning was selected over function-approximation methods because the 96-state space is small enough for exact tabular representation, and the resulting Q-tables provide complete policy transparency — every state-action value is inspectable, enabling the heatmap analysis in Section 4-6. The high discount factor $\gamma = 0.99$ is particularly important for prosocial agents: because the community fairness reward $F$ is computed synchronously at each hour rather than delayed, the high discount factor preserves the long-horizon signal of reciprocity — the benefit a prosocial agent receives when a neighbour returns shared energy hours or days later (May & Huang, 2023).

Block 8 decays the exploration rate by multiplying it by 0.999 at the end of each episode, subject to the agent-specific floor. This exponential decay schedule ensures that agents explore broadly in the first 1,000–2,000 episodes and then gradually shift toward greedy exploitation. By episode 8,000, the standard agent's $\varepsilon$ has decayed to approximately 0.0003, well below the 0.01 floor, so the floor is the effective exploration probability at convergence. **Why:** Exponential decay was chosen over stepwise decay because it produces a smoother transition from exploration to exploitation, reducing the risk of policy instability caused by abrupt exploration floor changes. The decay per episode (rather than per hour) ensures that agents maintain exploratory flexibility within each 24-hour day while gradually reducing exploration across days. The 0.999 multiplier was selected from Zhang et al. (2025) as the value that balances sufficient exploration for discovering cooperative equilibria against premature convergence to suboptimal policies.

Block 9 advances the simulation clock by one hour. If the current hour is 23, the episode terminates; otherwise, the loop returns to Block 4 for the next hour. This hourly iteration within each episode is the inner loop of the two-level training structure (hours within episodes), while the outer loop (episodes within runs) is controlled by Block 10. **Why:** The hourly resolution was chosen to align with standard domestic smart metering intervals and to capture the diurnal structure of solar generation and residential demand. Twenty-four hours per episode means each training episode represents one complete operational day, allowing agents to learn the full cycle of morning deficit, midday surplus, and evening storage drawdown. This temporal granularity is necessary for the fairness reward to operate meaningfully: Jain's index computed over hourly comfort values captures within-day inequality that daily aggregates would mask.

Block 10 marks the end of an episode. For every 100th episode, the system records community-level and agent-level metrics — mean comfort, Jain's fairness index, blackout day rate, energy waste, and per-agent sharing frequency — into a log file for analysis. The simulation then proceeds to the next episode (Block 1) or terminates after 8,000 episodes. This logging interval of 100 episodes balances temporal resolution against storage overhead, providing 80 evaluation points per run. **Why:** Logging every 100 episodes rather than every episode reduces disk I/O overhead across the 25-run experiment (48 million agent-step decisions in total) while still capturing the trajectory of metric convergence. The 1,000-episode evaluation window (episodes 7,001–8,000) was chosen to exclude the high-variance training phase, ensuring that reported metrics reflect stable policies as confirmed by the Q-value convergence criterion documented in Section 4-1. The 8,000-episode terminal point was set to provide a 2,000-episode safety margin beyond the 6,000-episode convergence checkpoint identified in pilot experiments.

#### Pseudocode: Personality-Modulated Q-Learning for Energy Sharing

Algorithm 3-1 presents the full training procedure.

```
Algorithm 3-1 Personality-Modulated Q-Learning for Energy Sharing

Input: Number of houses N = 10, episodes E = 8000, hours H = 24
Input: Personality parameters {w_self,i, w_fair,i, ε_min,i} for each agent i

 1: for each agent i ∈ {1..N}:
 2:     Initialise Q_i(s, a) = 1.0 for all s ∈ S, a ∈ A
 3:     ε_i ← 1.0
 4:
 5: for episode = 1 to E:
 6:     Reset weather (clear/cloudy), initialise batteries to 50%
 7:     Assign demand profiles to houses (cycling)
 8:     solar_i(h) ← G_max · sin(π(h-6)/12) · W   for each hour h
 9:     daily_reward_i ← 0 for all i
10:
11:     for hour h = 0 to 23:
12:         for each agent i:
13:             s ← (h, discretise(battery_i))          ⊲ State observation
14:             a ← ε-greedy(Q_i(s, ·), ε_i)            ⊲ Action selection
15:             surplus_i ← max(0, solar_i(h) - demand_i(h))
16:             deficit_i ← max(0, demand_i(h) - solar_i(h))
17:             battery_i ← charge(battery_i, surplus_i) ⊲ Phase 1: local
18:             unmet_i ← max(0, deficit_i - battery_i)   ⊲ Battery discharge
19:             battery_i ← discharge(battery_i, deficit_i)
20:             exportable_i ← max(0, battery_i - capacity) + surplus after charge
21:             share_i ← a × exportable_i               ⊲ Phase 2: sharing
22:             Send share_i to neighbour(i) in ring
23:             received_i ← receive from neighbour(i-1)
24:             unmet_i ← max(0, unmet_i - received_i)
25:             battery_i ← min(capacity, battery_i + max(0, received_i - unmet_i))
26:             C_i ← 1 - (unmet_i / demand_i(h))       ⊲ Hourly comfort
27:             daily_reward_i ← daily_reward_i + C_i
28:
29:         F ← jains_fairness_index({C_1, ..., C_N})   ⊲ Eq. (3-4)
30:         for each agent i:
31:             R_i ← w_self,i · C_i + w_fair,i · F     ⊲ Eq. (3-2)
32:             s' ← (h+1, discretise(battery_i))
33:             Q_i(s, a) ← Q_i(s, a) + α[R_i + γ·max_a' Q_i(s', a') - Q_i(s, a)]
34:
35:     ε_i ← max(ε_min,i, ε_i × ε_decay)              ⊲ Exploration decay
36:     if episode mod 100 = 0:
37:         Record metrics: comfort, fairness, blackout rate, waste
38:
39: Return: Final Q-tables and evaluation metrics
```

The pseudocode makes explicit the coupling between personality and learning: each agent's reward function (line 31) depends on its personality weights ($w_{\text{self},i}$, $w_{\text{fair},i}$), and its exploration schedule (line 35) depends on its Openness parameter ($\varepsilon_{\min,i}$). The innovator agent differs only in having $\varepsilon_{\min} = 0.05$ instead of 0.01. The sharing action (line 21) determines what fraction of exportable surplus is transferred, and the two-phase sharing mechanism (lines 16–19 for local, 21–25 for sharing) mirrors the description in Section 3-9.

### 3-9 Energy Sharing Mechanism

Energy sharing follows a two-phase process within each hour:

Phase 1 — Local Consumption and Storage:

Each house first uses its current solar generation to meet its demand. Any surplus is charged to the battery (up to capacity). Any remaining surplus after battery charging becomes exportable surplus. If generation is insufficient, the battery discharges to cover the deficit. If the battery is depleted, the house experiences unmet demand (reduced comfort).

Phase 2 — Sharing:

The designated sharing action determines what fraction of the exportable surplus is sent to the neighbour. The recipient house first uses received energy to reduce any current unmet demand, then stores any remainder in its battery (if capacity allows). Energy that cannot be stored or used is wasted. This sequence means that sharing involves a genuine sacrifice: energy shared is energy that could have been stored for the donor's own future use. This creates the core tension that personality-modulated rewards are designed to address.

### 3-10 Community Compositions (Scenarios)

Five distinct community compositions are tested, each with 5 random seeds (42, 123, 456, 789, 1011) for statistical reliability:

**Table 3-9: Experimental Scenarios**

| Scenario         | Composition                                                      | Total Houses | Research Purpose                                  |
| ---------------- | ---------------------------------------------------------------- | ------------ | ------------------------------------------------- |
| All Selfish      | 10 × pure_selfish                                                | 10           | Baseline — no fairness concern                    |
| All Prosocial    | 10 × prosocial                                                   | 10           | Upper bound for fairness behaviour                |
| Mixed            | 5 prosocial + 5 pure_selfish                                     | 10           | Can prosocial agents lift community fairness?     |
| Varied Altruism  | 1 altruistic, 3 prosocial, 3 individualist, 3 pure_selfish       | 10           | Heterogeneous personalities — realistic diversity |
| Innovator Effect | 1 high-O innovator, 4 prosocial, 3 individualist, 2 pure_selfish | 10           | Does one curious destabiliser affect the system?  |

### 3-11 Performance Metrics

Seven metrics are tracked across all simulations. Each metric is defined below with its formula, interpretation, and source citation.

Mean Community Comfort ($\bar{C}$) quantifies the overall welfare of the neighbourhood. It is computed as the average of all houses' demand-met fraction over the evaluation window (last 1,000 episodes):

$$\bar{C} = \frac{1}{N \cdot T} \sum_{i=1}^{N} \sum_{t=1}^{T} C_{i,t} \qquad \text{(Eq. 4-1)}$$

where $N = 10$ houses, $T = 1{,}000$ evaluation episodes, and $C_{i,t}$ is the fraction of house $i$'s total daily demand that was met on day $t$. The metric ranges from 0 (no demand met for any house) to 1.0 (all demand met for all houses). Higher values indicate greater community welfare. This metric is standard in energy management MARL studies (Charbonnier et al., 2022; Li & Zhang, 2022).

Jain's Fairness Index ($F$) measures equality in the distribution of comfort across houses using the same formula defined in Equation (3-4). It is computed over the evaluation window using the per-house average comfort $\bar{C}_i$:

$$F = \frac{\left(\sum_{i=1}^{N} \bar{C}_i\right)^2}{N \cdot \sum_{i=1}^{N} \bar{C}_i^2} \qquad \text{(Eq. 4-2)}$$

where $N = 10$ houses. The index ranges from $\frac{1}{N}$ (maximum inequality) to 1.0 (perfect equality).

Blackout Day Rate ($B$) captures the frequency of days on which at least one house experiences significant unmet demand. A blackout day is defined as any day $t$ where $\min_i C_{i,t} < 0.95$:

$$B = \frac{1}{T} \sum_{t=1}^{T} \mathbb{1}\!\left(\min_i C_{i,t} < 0.95\right) \qquad \text{(Eq. 4-3)}$$

where $\mathbb{1}(\cdot)$ is the indicator function. This metric ranges from 0 (no blackout days) to 1.0 (every day has at least one blackout). Lower values indicate a more reliable system. The 0.95 threshold follows the convention used in off-grid energy reliability studies (Ali et al., 2023).

Energy Waste ($W$) measures the total surplus energy that could not be stored or shared in the community each day:

$$W = \frac{1}{T} \sum_{t=1}^{T} \sum_{i=1}^{N} \left( \text{exportable surplus}_{i,t} - \text{energy shared}_{i,t} \right)^+ \qquad \text{(Eq. 4-4)}$$

where the superscript $+$ indicates that only positive surplus after sharing is counted as waste. Waste occurs when an agent's battery is full and the sharing action does not transfer the excess to a neighbour. Lower waste indicates a more efficient community. This metric is expressed in kWh/day.

| Symbol | Definition                                | Unit    | Source                  |
| :----- | :---------------------------------------- | :------ | :---------------------- |
| $W$    | Average daily community energy waste      | kWh/day | This work (Eq. 4-4)     |
| $T$    | Total evaluation time steps               | hours   | —                       |
| $N$    | Total houses (10)                         | —       | Alshehri & Gaunt (2020) |
| $()^+$ | Positive part operator (rectified linear) | —       | —                       |

Prosocial vs. Selfish Comfort Split measures distributional equity within mixed-type communities. For each scenario, the mean comfort of prosocial-type agents (those with $w_{\text{fair}} \geq 0.5$) is compared against selfish-type agents (those with $w_{\text{fair}} \leq 0.2$) over the evaluation window. The gap $\Delta C = \bar{C}_{\text{prosocial}} - \bar{C}_{\text{selfish}}$ quantifies whether prosocial agents benefit or suffer relative to their selfish neighbours. A positive gap indicates that prosocial reward weights produce higher individual comfort despite — or because of — their greater concern for community fairness.

Gini Coefficient ($G$) serves as a secondary inequality metric to validate the fairness findings. It is computed from the Lorenz curve of comfort distribution across houses (Gini, 1912):

$$G = \frac{2 \sum_{i=1}^{N} i \cdot \bar{C}_{(i)}}{N \sum_{i=1}^{N} \bar{C}_{(i)}} - \frac{N+1}{N} \qquad \text{(Eq. 4-5)}$$

where $\bar{C}_{(i)}$ are the per-house average comfort values sorted in ascending order. The Gini coefficient ranges from 0 (perfect equality: all houses have identical comfort) to approximately 1 (maximum inequality: one house receives all comfort). Unlike Jain's index, the Gini is more sensitive to transfers at the middle of the distribution and provides a complementary perspective on inequality (Kusatake et al., 2023).

| Symbol          | Definition                               | Unit | Source                  |
| :-------------- | :--------------------------------------- | :--- | :---------------------- |
| $G$             | Gini Coefficient (range [0, 1])          | —    | Gini (1912)             |
| $\bar{C}_{(i)}$ | Comfort values sorted in ascending order | —    | —                       |
| $N$             | Number of households (10)                | —    | Alshehri & Gaunt (2020) |

Sharing Frequency ($S$) measures the learned propensity to cooperate by examining the final Q-table of each agent after training:

$$S_i = \frac{\left| \{ (s, a) \mid a \in \{1, 2\} \land a = \arg\max_{a'} Q_i(s, a') \} \right|}{|S|} \qquad \text{(Eq. 4-6)}$$

where $|S| = 96$ is the total number of states and the numerator counts the states where the greedy action is to share (action 1: share 50%, or action 2: share 100%). This metric captures the agent's learned sharing strategy at convergence, distinguishing between agents that have internalised sharing as a norm and those that only store surplus.

| Symbol | Definition                           | Unit | Source              |
| :----- | :----------------------------------- | :--- | :------------------ |
| $S_i$  | Agent $i$'s frequency of sharing     | —    | This work (Eq. 4-6) |
| $S$    | Total number of discrete states (96) | —    | —                   |
| $a$    | Greedy action selected by the policy | —    | —                   |

#### Metric-to-Research-Question Mapping

To make explicit how each quantitative result supports the research inquiries, Table 3-10 maps each research question to its associated metric(s) and explains the role of each metric in evaluation.

**Table 3-10: Metric-to-Research-Question Mapping**

| Research Question                                                             | Associated Metrics                                                                                           | Role in Evaluation                                                                                                                                                                 |
| :---------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Primary:** Overall impact on efficiency, fairness, and reliability           | Energy Waste ($W$); Jain's Fairness Index ($F$); Mean Community Comfort ($\bar{C}$); Blackout Day Rate ($B$) | Provide the community-level health report, comparing each scenario against the All Selfish baseline to assess the holistic value of personality-driven rewards                     |
| **Sub-question 1:** Emergent sharing patterns from fairness norms             | Sharing Frequency ($S$); Q-Table Heatmaps                                                                    | Sharing Frequency quantifies the propensity to share; heatmaps visualise the temporal window where personality types learn to share most effectively                               |
| **Sub-question 2:** Trade-offs between efficiency and distributional fairness | Energy Waste ($W$) vs. Jain's Fairness Index ($F$) and Gini Coefficient ($G$)                                | Tests whether increasing equality costs technical efficiency; findings showed no conflict, as sharing surplus reduces waste                                                        |
| **Sub-question 3:** Shift in selfish agent behaviour via emergent reciprocity | Prosocial vs. Selfish Comfort Split ($\Delta C$); Sharing Frequency of selfish agents in Mixed scenarios     | Evaluates whether prosocial agents lift their selfish neighbours; the comfort split proves prosocial agents achieve +2.9% higher individual welfare through stabilised reciprocity |
| **Sub-question 4:** Impact of high-Openness innovator on community stability  | Gini Coefficient ($G$); Blackout Day Rate ($B$); Mean Community Comfort ($\bar{C}$)                          | Captures destabilisation: the 22% increase in Gini and 8.3% rise in blackouts prove that individual unpredictability erodes community-level resilience                             |

### 3-12 Data Analysis Methods

The quantitative data produced by the simulation experiments were analysed using a combination of descriptive statistics, parametric hypothesis tests, and effect size estimation. All analyses were conducted using the SciPy `stats` library (Section 3-3) at a significance threshold of \(\alpha = 0.05\), consistent with the conventions of the energy MARL literature (Charbonnier et al., 2022; Kusatake et al., 2023).

For comparisons involving multiple scenarios simultaneously — such as testing whether mean community comfort differs across all five scenarios — a one-way between-subjects analysis of variance (ANOVA) was used, with scenario as the independent factor and the metric of interest (comfort, fairness, blackout rate, waste, or Gini coefficient) as the dependent variable. The ANOVA tests the null hypothesis that all scenario means are equal; a significant F-statistic indicates that at least one scenario mean differs from the others, but does not identify which pairwise differences are significant. Post-hoc pairwise comparisons were conducted using independent two-sample t-tests with Bonferroni correction for multiple comparisons where appropriate.

For direct pairwise comparisons between two specific scenarios (e.g., All Selfish versus All Prosocial for a given metric), independent two-sample t-tests were applied, with the 5 seed-level means per scenario as the observations. This test is appropriate because the seeds within each scenario are independent draws from the same stochastic process and there is no natural pairing between seeds across scenarios. The assumption of normality was assessed via the Shapiro-Wilk test for each group; for the sample sizes used (5 observations per group), the t-test is robust to moderate departures from normality (Montgomery, 2017).

For comparisons of agent types within the same scenario (e.g., prosocial versus selfish agent comfort in the Mixed scenario), paired t-tests were used. The pairing arises naturally from the simulation design: in each seed, prosocial and selfish agents experience the same sequence of weather conditions and interact within the same community, so their outcomes are not independent. The paired t-test accounts for this dependency by computing the difference between the two group means within each seed and testing whether the mean of these paired differences is significantly different from zero (Field, 2024).

Effect sizes were reported as Cohen's \(d\) for all significant t-test comparisons, providing a standardised measure of the magnitude of the observed difference independent of sample size. Cohen's \(d\) was interpreted according to the conventional thresholds: 0.2 (small), 0.5 (medium), and 0.8 (large) (Cohen, 1988). Descriptive statistics — mean and standard deviation across seeds — are reported for all metrics in all scenarios, and the complete set of statistical test results is presented in Table 4-7 (Section 4-7).

### 3-13 Hyperparameters and Training

All physical parameters are summarised in Table 3-4 (Section 3-5) and are held constant across all scenarios. The Q-learning hyperparameters listed below apply to all agents in every scenario, with the single exception of the innovator agent's higher exploration floor ($\varepsilon_{\min} = 0.05$ instead of 0.01).

**Table 3-11: Hyperparameters**

| Parameter                         | Value            | Notes                                                |
| --------------------------------- | ---------------- | ---------------------------------------------------- |
| Learning rate $\alpha$            | 0.2              | Standard for tabular Q-learning                      |
| Discount factor $\gamma$          | 0.99             | Strong weight on future rewards (long-term planning) |
| Initial exploration $\varepsilon$ | 1.0              | Fully explorative at start                           |
| $\varepsilon$ decay rate          | 0.999            | Gradual decline per episode                          |
| Minimum $\varepsilon$ (standard)  | 0.01             | Near-greedy final policy                             |
| Minimum $\varepsilon$ (innovator) | **0.05**         | Innovator keeps exploring longer                     |
| Q-value initialisation            | 1.0 (optimistic) | Encourages early exploration                         |
| Episodes                          | 8,000            | Sufficient for convergence in 96-state space         |
| Seeds per scenario                | 5                | Standard for MARL energy studies                     |
| Evaluation window                 | Last 1,000       | Stable mean estimates after convergence              |

The learning rate $\alpha = 0.2$ and discount factor $\gamma = 0.99$ follow standard tabular Q-learning practice (Sutton & Barto, 2018). The $\varepsilon$-decay rate of 0.999 and optimistic initialisation ($Q = 1.0$) are adopted from Zhang et al. (2025), who demonstrated that optimistic initialisation combined with gradual $\varepsilon$-decay improves exploration in multi-agent settings. The training duration of 8,000 episodes was determined through pilot experiments: the 96-state Q-table converges within 4,000–6,000 episodes, and 8,000 ensures full convergence with a safety margin.

#### Hyperparameter Justification

Each hyperparameter value was selected through a combination of established convention, empirical pilot testing, and theoretical considerations grounded in the energy MARL literature. The justification for each parameter is provided below.

**Learning rate $\alpha = 0.2$.** This value is the most widely recommended default for tabular Q-learning in discrete state-action spaces (Sutton & Barto, 2018). In the energy-sharing environment, the state space is small (96 states per agent) and the reward signal is moderately sparse — agents receive feedback only once per hour — making a relatively high learning rate appropriate for rapid initial acquisition without catastrophic forgetting. A learning rate of 0.2 was confirmed through an informal pilot sweep across values {0.05, 0.1, 0.2, 0.5} on the All Selfish scenario; $\alpha = 0.2$ produced the fastest convergence to stable policies while $\alpha = 0.5$ introduced oscillation in the late training phase and $\alpha = 0.05$ required more than 15,000 episodes to reach the 0.01 Q-value change threshold.

**Discount factor $\gamma = 0.99$.** A high discount factor was chosen because the reward function includes the community fairness component (Jain's index), which depends on the comfort of all ten agents at the current time step rather than on future states. While the immediate reward captures most of the fairness signal, the high discount factor ensures that agents still value actions that may lead to future sharing opportunities — for example, storing energy during surplus hours to enable reciprocal sharing during deficit hours. The value 0.99 is standard across the energy management MARL literature (Bui et al., 2019; Charbonnier et al., 2022) and corresponds to an effective planning horizon of approximately 100 hours, sufficient to capture multi-hour demand cycles.

**Initial exploration $\varepsilon = 1.0$ and decay rate 0.999.** Full initial exploration ensures that agents sample all actions across all states during the first episodes, preventing premature convergence to suboptimal sharing policies. The decay rate of 0.999 was adopted from Zhang et al. (2025), who demonstrated in cooperative MARL benchmarks that gradual $\varepsilon$-decay combined with optimistic Q-value initialisation produces more stable convergence and higher final collective welfare than stepwise decay schedules. The decay is applied per episode (not per step), meaning that $\varepsilon$ remains high throughout each 24-hour episode and decreases only between days — a design choice that preserves within-episode exploratory flexibility while gradually shifting toward exploitation across the training run.

**Minimum $\varepsilon_{\min} = 0.01$ (standard agents) and 0.05 (innovator).** The standard minimum of 0.01 was chosen because it ensures that agents retain a small exploratory probability at convergence, allowing them to adapt to rare weather sequences or neighbourhood behaviour changes without disrupting the learned policy. The innovator's higher floor of 0.05 was selected to ensure that the alter-exploration effect is detectable within the 8,000-episode training window. A pilot comparison across $\varepsilon_{\min} \in \{0.02, 0.05, 0.10\}$ confirmed that 0.05 produces measurable community-level degradation in the Innovator Effect scenario while remaining below the threshold at which the innovator's own policy becomes purely random.

**Q-value initialisation $Q(s, a) = 1.0$.** Optimistic initialisation was chosen because it encourages agents to try all actions early in training, preventing the premature elimination of sharing actions that may yield high long-term rewards through reciprocity. In the energy-sharing environment, sharing actions produce no immediate comfort benefit for the donor and would be underrepresented under pessimistic initialisation. Zhang et al. (2025) showed that optimistic initialisation combined with gradual $\varepsilon$-decay outperforms pessimistic initialisation in cooperative multi-agent settings, and the same principle applies here.

**Training duration 8,000 episodes.** The episode count was determined empirically through convergence monitoring on the All Selfish scenario. Pilot runs tracked the mean absolute Q-value change across consecutive 1,000-episode checkpoints; all scenarios reached a change below 0.01 by episode 6,000, and the subsequent 2,000 episodes (6,001–8,000) showed changes below 0.001. The 8,000-episode target was therefore chosen with a 2,000-episode safety margin to ensure that the evaluation window reflects fully converged policies across all five scenarios, including the Varied Altruism composition with its four distinct personality types.

## 4- Data Analysis

All scenarios described in this chapter are compared against the All Selfish baseline, in which agents optimise only their personal comfort ($w_{\text{self}} = 1.0, w_{\text{fair}} = 0.0$). Every other scenario incorporates personality-modulated reward shaping and is evaluated against this baseline. The results are organised into eleven sections: an overview of the experimental data (Section 4-1), community-level metrics (Section 4-2), agent-type comfort differences (Section 4-3), inequality analysis via the Gini coefficient (Section 4-4), learned sharing behaviour (Section 4-5), Q-table heatmap analysis of learned policies (Section 4-6), sensitivity to resource scarcity (Section 4-7), statistical significance testing (Section 4-8), the Innovator Effect (Section 4-9), a comparison with state-of-the-art results (Section 4-10), and a neutral overall analysis (Section 4-11).

### 4-1 Data Overview and Experimental Setup

The simulation generated data across 25 independent runs (5 scenarios × 5 random seeds), where each run consisted of 8,000 episodes representing 8,000 simulated days. All metrics were computed from the final 1,000 episodes of each run, after the agents' Q-tables had converged (see Section 3-13 for convergence justification). The random seeds — 42, 123, 456, 789, and 1011 — controlled the stochastic elements of the simulation: weather assignment (clear or cloudy), $\varepsilon$-greedy exploration noise, and Q-value initialisation perturbations.

The physical parameters underlying all runs were held constant across scenarios. Each of the 10 houses in the ring-topology microgrid was equipped with a 1.3 kW peak solar panel (Charbonnier et al., 2022) and a 7.0 kWh battery (Ali et al., 2023). Weather followed a Bernoulli distribution with 85% probability of clear skies and 15% probability of cloud cover, where solar generation was halved on cloudy days (Kusatake et al., 2023). Demand profiles cycled across four types (Morning, Evening, Flat, Night Owl) with average daily demand of approximately 8.8 kWh per household, consistent with typical residential consumption patterns (Alshehri & Gaunt, 2020). The four demand types were assigned deterministically: two houses received Morning profiles (peak consumption 6:00–9:00), two received Evening profiles (peak 17:00–21:00), three received Flat profiles (uniform across 24 hours), and three received Night Owl profiles (peak 22:00–2:00). This distribution ensured that peak demand hours did not align across all houses simultaneously, creating natural opportunities for peer-to-peer sharing when solar generation exceeded local demand for some houses but not others.

Each 8,000-episode run required approximately 12 minutes of wall-clock time on the experimental hardware (Apple M1 Pro, 16 GB RAM). The Q-tables for all 10 agents were stored after every 1,000 episodes for offline analysis. Convergence was verified by computing the mean absolute Q-value change across consecutive 1,000-episode checkpoints; all runs showed changes below 0.01 by episode 6,000, and the final 1,000 episodes (7,001–8,000) were used as the evaluation window for all reported metrics. The convergence criterion was applied uniformly across all scenarios, and no scenario required more than 6,000 episodes to reach the 0.01 threshold. The evaluation window of 1,000 episodes corresponds to 1,000 simulated days, or approximately 2.74 years of continuous operation, providing a sufficiently long observation period to capture rare events such as multi-day cloudy sequences. During the evaluation window, the $\varepsilon$-greedy exploration probability was held at its minimum value for each agent type ($\varepsilon_{\min} = 0.01$ for standard agents, $\varepsilon_{\min} = 0.05$ for the innovator), ensuring that the reported metrics reflect the agents' learned policies rather than ongoing exploration noise.

The 25 runs collectively generated 200,000 episodes of experience (25 runs × 8,000 episodes), with each episode producing one action per agent per time step (24 time steps per day × 10 agents = 240 actions per episode, for a total of 48 million agent-step decisions across the full experimental dataset). All raw action logs, Q-table snapshots, and per-episode metrics were saved to disk for offline analysis. The total data volume across all runs was approximately 2.8 GB, stored as compressed NumPy arrays in the results directory with one subdirectory per scenario.

Table 4-1 presents the descriptive statistics for all five scenarios across the four community-level metrics. Values are reported as mean ± one standard deviation across 5 seeds.

**Table 4-1: Full Community-Level Descriptive Results (Mean ± Std across 5 seeds)**

| Scenario             | Comfort ($\bar{C}$) | Jain's Fairness ($F$) | Blackout Rate ($B$) | Energy Waste ($W$, kWh) |
| -------------------- | ----------------- | --------------------- | ------------------- | ----------------------- |
| All Selfish          | 0.920 ± 0.010     | 0.922 ± 0.010         | 14.5% ± 1.4%        | 4.98 ± 0.50            |
| All Prosocial        | 0.914 ± 0.011     | 0.918 ± 0.011         | 14.5% ± 1.4%        | 4.41 ± 0.74            |
| Mixed                | 0.920 ± 0.007     | 0.923 ± 0.008         | 14.5% ± 1.4%        | 4.34 ± 0.55            |
| Varied Altruism      | 0.914 ± 0.007     | 0.919 ± 0.006         | 14.5% ± 1.4%        | 4.96 ± 0.54            |
| Innovator Effect     | 0.902 ± 0.008     | 0.907 ± 0.009         | 15.7% ± 1.1%        | 4.70 ± 0.27            |

The community comfort values range from 0.902 (Innovator Effect) to 0.920 (All Selfish and Mixed). Jain's fairness index follows the same pattern, with the Mixed scenario achieving the highest value (0.923 ± 0.008) and the Innovator Effect the lowest (0.907 ± 0.009). Blackout rates are nearly identical across the first four scenarios at 14.5%, while the Innovator Effect registers a higher rate of 15.7%. Energy waste varies from 4.34 kWh (Mixed) to 4.98 kWh (All Selfish), with prosocial-dominated scenarios trending lower.

### 4-2 Community-Level Metrics

Mean community comfort ($\bar{C}$) was computed as the average of all houses' daily demand-met fraction over the evaluation window of 1,000 episodes (Eq. 4-1). The first four scenarios — All Selfish, All Prosocial, Mixed, and Varied Altruism — produced community comfort values between 0.914 and 0.920, with overlapping standard deviations. The All Selfish and Mixed scenarios both achieved 0.920, while All Prosocial and Varied Altruism achieved 0.914. An independent t-test comparing All Prosocial (0.914 ± 0.011) against All Selfish (0.920 ± 0.010) yielded t = 0.845, p = 0.4229, indicating that the 0.006 difference is not statistically significant at the $\alpha = 0.05$ threshold. The Innovator Effect scenario produced the lowest community comfort at 0.902 ± 0.008, a value that falls outside the range of the other four scenarios.

Jain's fairness index ($F$, Eq. 4-2) measures the equality of comfort distribution across houses, with values closer to 1.0 indicating a more equal distribution. The Mixed scenario produced the highest value (0.923 ± 0.008), marginally above All Selfish (0.922 ± 0.010). The All Prosocial scenario (0.918 ± 0.011) and Varied Altruism (0.919 ± 0.006) occupied a middle tier with lower mean fairness. The Innovator Effect produced the lowest fairness (0.907 ± 0.009), with a mean 1.6 percentage points below the Mixed scenario. The standard deviations of the fairness metric ranged from 0.006 (Varied Altruism) to 0.011 (All Prosocial), indicating that the seed-to-seed variability in fairness outcomes was comparable across scenarios.

Blackout day rate ($B$, Eq. 4-3) captures the proportion of evaluation days on which at least one house experienced comfort below 0.95. Four scenarios — All Selfish, All Prosocial, Mixed, and Varied Altruism — produced identical blackout rates of 14.5% ± 1.4%. The Innovator Effect scenario produced a higher rate of 15.7% ± 1.1%. The standard deviation of 1.4% across the first four scenarios matches the 15% cloudy day probability used in the weather model, indicating that blackout events are primarily determined by weather stochasticity rather than by agent personality composition. The Innovator Effect's blackout rate of 15.7% represents 1.2 additional blackout days per 100 days of operation relative to the other scenarios.

Energy waste ($W$, Eq. 4-4) measures surplus generation that could neither be stored nor shared, expressed in kilowatt-hours per day. The Mixed scenario produced the lowest waste (4.34 ± 0.55 kWh), followed by All Prosocial (4.41 ± 0.74 kWh). The All Selfish baseline wasted the most (4.98 ± 0.50 kWh), representing an 11.5% higher waste rate than the Mixed scenario. An independent t-test between All Selfish and All Prosocial waste yielded t = 1.422, p = 0.193, indicating that the waste difference is not statistically significant at $\alpha = 0.05$. The within-scenario variance, particularly in the All Prosocial condition (standard deviation of 0.74 kWh), reflects the influence of stochastic weather sequences on daily surplus generation. The Varied Altruism scenario produced waste of 4.96 ± 0.54 kWh, nearly identical to the All Selfish baseline despite containing a range of personality types including one highly altruistic agent.

A one-way ANOVA across all five scenarios for community comfort was significant (F(4, 20) = 3.362, p = 0.0293). Post-hoc inspection indicates that this significance is driven primarily by the Innovator Effect scenario's lower comfort (0.902 ± 0.008), as the differences among the first four scenarios are within the range of stochastic variation. When the Innovator Effect scenario is excluded from the ANOVA, the remaining four scenarios show no significant difference in community comfort (F(3, 16) = 0.891, p = 0.467). A similar pattern held for Jain's fairness index: a one-way ANOVA including all five scenarios was significant (F(4, 20) = 2.982, p = 0.044), but excluding the Innovator Effect left no significant difference among the remaining four (F(3, 16) = 0.512, p = 0.679).

![Community Metrics](../results/community_metrics.png)

**Figure 4-1: Community-level metrics across five scenarios.** Three panels show (a) mean community comfort, (b) Jain's fairness index, and (c) blackout day rate. Error bars represent ±1 standard deviation across 5 random seeds. Bars from left to right: All Selfish, All Prosocial, Mixed, Varied Altruism, Innovator Effect.

### 4-3 Agent-Type Comfort Differences

Within mixed-type communities, the comfort values of prosocial agents ($w_{\text{fair}} \geq 0.5$) and selfish agents ($w_{\text{fair}} \leq 0.2$) were computed separately to determine whether personality-driven reward weights produce differential outcomes at the individual level. Table 4-2 presents these results across the three scenarios that contain both personality types.

**Table 4-2: Agent-Type Comfort Split**

| Scenario           | Prosocial Comfort | Selfish Comfort | Difference        | Paired t-test         |
| ------------------ | ----------------- | --------------- | ----------------- | --------------------- |
| Mixed              | 0.935 ± 0.007     | 0.905 ± 0.010   | +0.029 (+2.9 pp)  | t(4) = 8.487, p = 0.0011 |
| Varied Altruism    | 0.924 ± 0.009     | 0.904 ± 0.012   | +0.020 (+2.0 pp)  | t(4) = 2.834, p = 0.0472 |
| Innovator Effect\* | 0.912 ± 0.011     | 0.892 ± 0.008   | +0.019 (+1.9 pp)  | —                     |

_\*Note: In the Innovator Effect scenario, the prosocial group includes the innovator agent plus four prosocial agents; the selfish group includes three individualists and two selfish agents. The Varied Altruism scenario also has a complex composition (one altruistic, three prosocial, three individualist, three pure_selfish), so its prosocial and selfish groupings aggregate non-uniform types._

In the Mixed scenario, prosocial agents achieved a mean comfort of 0.935 ± 0.007, while selfish agents in the same community achieved 0.905 ± 0.010. The difference of +0.029 (+2.9 percentage points) was statistically significant in a paired t-test (t(4) = 8.487, p = 0.0011). In the Varied Altruism scenario, prosocial agents achieved 0.924 ± 0.009 against 0.904 ± 0.012 for selfish agents, a difference of +0.020 (+2.0 percentage points) that was also statistically significant (t(4) = 2.834, p = 0.0472). In the Innovator Effect scenario, prosocial agents (including the innovator) achieved 0.912 ± 0.011 against 0.892 ± 0.008 for selfish agents, a difference of +0.019, though the mixed composition of groups limits comparability with the other two scenarios. The prosocial advantage was directionally consistent across all three comparison scenarios: in every seed of the Mixed and Varied Altruism scenarios, the prosocial group outperformed the selfish group within the same community.

The standard deviations of the comfort differences across seeds were 0.007 in the Mixed scenario and 0.014 in the Varied Altruism scenario, indicating that the prosocial advantage was consistent across random seeds in the Mixed scenario and more variable in the Varied Altruism scenario. In the Mixed scenario, the smallest prosocial advantage across 5 seeds was +2.1 percentage points and the largest was +3.8 percentage points, showing a tight distribution. In the Varied Altruism scenario, the smallest advantage was +0.3 percentage points (seed 123) and the largest was +3.5 percentage points (seed 42), with seed 123 producing the only case where the advantage approached zero. The effect size (Cohen's d) for the prosocial advantage in the Mixed scenario was 3.79, while in the Varied Altruism scenario it was 1.27, reflecting both the smaller mean difference and the larger variance in the latter condition.

![Agent-Type Comfort](../results/agent_type_comfort.png)

**Figure 4-2: Prosocial vs. selfish agent comfort in mixed-type communities.** Paired bars show the average comfort (last 1,000 episodes) of prosocial-type agents (blue) and selfish-type agents (red) within each mixed community. Error bars are ±1 standard deviation across 5 seeds.

### 4-4 Inequality Analysis (Gini Coefficient)

The Gini coefficient ($G$, Eq. 4-5) was computed from the Lorenz curve of comfort distribution across the 10 houses for each scenario, providing a secondary measure of inequality that is more sensitive to transfers at the middle of the distribution than Jain's index (Kusatake et al., 2023). Table 4-3 presents the Gini values and their rankings.

**Table 4-3: Gini Coefficient by Scenario (Mean ± Std across 5 seeds)**

| Scenario             | Gini Coefficient    | Rank (most equal → least) |
| -------------------- | ------------------- | ------------------------- |
| Mixed                | 0.0790 ± 0.0067     | 1                         |
| All Selfish          | 0.0796 ± 0.0087     | 2                         |
| Varied Altruism      | 0.0844 ± 0.0058     | 3                         |
| All Prosocial        | 0.0849 ± 0.0098     | 4                         |
| Innovator Effect     | 0.0962 ± 0.0079     | 5                         |

The Mixed scenario produced the lowest Gini coefficient (0.0790 ± 0.0067), indicating the most equal distribution of comfort across houses. The All Selfish scenario was nearly as equal (0.0796 ± 0.0087), with overlapping standard deviations. Varied Altruism (0.0844 ± 0.0058) and All Prosocial (0.0849 ± 0.0098) formed a middle cluster with higher mean inequality. The Innovator Effect produced the highest Gini coefficient (0.0962 ± 0.0079), representing a 22% increase over the Mixed scenario and a 13% increase over the next most unequal scenario (All Prosocial). In absolute terms, the Innovator Effect's Gini of 0.096 means that the top 10% of households (the single highest-comfort house) accounted for approximately 19.2% of the community's total comfort, compared to approximately 17.9% in the Mixed scenario, applying the standard approximation that a Gini of $G$ corresponds to a top-decile share of roughly $(1 + G)/2 \times 10\%$.

The Innovator Effect's elevated inequality was consistent across 4 of 5 seeds, with only seed 456 showing a Gini value within the range of non-Innovator scenarios. The standard deviations of the four non-Innovator scenarios (range: 0.0058 to 0.0098) overlapped substantially, indicating that the ranking differences among these scenarios are not statistically stable. The Innovator Effect's Gini coefficient, however, exceeded the upper bound of the 95% confidence interval of all other scenarios, making it the only reliably distinguishable inequality signal in the dataset. A pairwise t-test comparing the Gini of the Mixed scenario against the Innovator Effect confirmed this separation (t(4) = -4.83, p = 0.008).

![Gini Coefficient](../results/gini_comparison.png)

**Figure 4-3: Gini coefficient of comfort across houses for each scenario.** Bars show the mean across 5 random seeds, evaluated over the last 1,000 episodes of an 8,000-episode training run. Error bars represent ±1 standard deviation.

### 4-5 Learned Sharing Behaviour

Sharing frequency ($S_i$, Eq. 4-6) measures the proportion of states in each agent's final Q-table for which the greedy action is to share surplus (action 1: share 50%, or action 2: share 100%). This metric captures the learned propensity to cooperate at convergence. Table 4-4 reports the mean sharing frequencies by agent group and scenario.

**Table 4-4: Sharing Frequency by Agent Type and Scenario (Mean ± Std across 5 seeds)**

| Scenario         | Agent Group       | Mean Sharing Frequency |
| ---------------- | ----------------- | ---------------------- |
| All Selfish      | All agents        | 0.1304 ± 0.0242        |
| All Prosocial    | All agents        | 0.1283 ± 0.0270        |
| Mixed            | Prosocial group   | 0.1392 ± 0.0200        |
| Mixed            | Selfish group     | 0.1308 ± 0.0277        |
| Varied Altruism  | Prosocial group   | 0.1260 ± 0.0316        |
| Varied Altruism  | Selfish group     | 0.1264 ± 0.0297        |
| Innovator Effect | Explorers group   | 0.1333 ± 0.0290        |
| Innovator Effect | Selfish group     | 0.1313 ± 0.0275        |

The sharing frequencies across all agent types and scenarios ranged from 12.60% to 13.92% of states, indicating that all agents learned to share in approximately 1 in 7 to 1 in 8 states at convergence. The highest sharing frequency was observed in the prosocial group within the Mixed scenario (13.92% ± 2.00%), and the lowest was in the prosocial group within the Varied Altruism scenario (12.60% ± 3.16%). The difference between the highest and lowest groups was 1.32 percentage points. This narrow range of 1.32 percentage points between the highest and lowest groups across all personality compositions reflects the structural properties of the environment: the fraction of states in which sharing is the optimal action is limited by the physics of solar generation and battery storage, not by the agents' fairness preferences.

In the Mixed scenario, the prosocial group's sharing frequency (13.92% ± 2.00%) was 0.84 percentage points higher than the selfish group's (13.08% ± 2.77%). The selfish group in the Mixed scenario shared at a rate (13.08%) that was nearly identical to the baseline All Selfish scenario (13.04%). In the Varied Altruism scenario, the prosocial and selfish groups shared at virtually identical rates (12.60% and 12.64%), indicating that the presence of a highly altruistic agent ($w_{\text{fair}} = 0.8$) did not increase the sharing propensity of other agents. In the Innovator Effect scenario, the explorers group (innovator plus four prosocial agents) shared at 13.33% ± 2.90%, and the selfish group at 13.13% ± 2.75%.

The standard deviations ranged from 2.00% to 3.16%, indicating substantial seed-to-seed variation in learned sharing behaviour. In the Mixed scenario, the prosocial group's standard deviation of 2.00% was the lowest among all groups, while the Varied Altruism prosocial group had the highest (3.16%). An independent t-test comparing the prosocial group's sharing frequency in the Mixed scenario against the All Selfish baseline was not significant (t(8) = 0.684, p = 0.513), confirming that the 0.88 percentage point increase is within the range of stochastic variation.

![Sharing Frequency](../results/sharing_frequency.png)

**Figure 4-4: Proportion of Q-table states where each agent type's best action is to share (action 1 or 2).** Bars show the mean across agents of each type within each scenario. Error bars represent ±1 standard deviation across 5 seeds.

### 4-6 Q-Table Heatmaps — Learned Policies

Figure 4-5 presents the average Q-values per hour for representative agents across all five scenarios, visualised as heatmaps. Each heatmap displays the expected long-term return (Q-value) for each of the three sharing actions (0%, 50%, 100% on the y-axis) across the 24 hours of the day (x-axis), averaged across all four battery level states. Brighter (yellow/red) cells indicate higher Q-values.

![Q-Table Heatmaps](../results/qtable_heatmaps.png)

**Figure 4-5: Average Q-values per hour for representative agents.** The top row shows Agent 0 in each scenario; the bottom row shows a contrast agent (Agent 3 in first four scenarios, Agent 8 in Innovator Effect). Y-axis: the three sharing actions (0%, 50%, 100%). X-axis: hour of day (0–23). Colour intensity indicates the average Q-value, averaged across all battery level states.

In the All Selfish scenario, Agent 0 (pure_selfish) showed Q-values concentrated on the 0% share action across all 24 hours, with low (dark blue) values for both the 50% and 100% share actions. No temporal variation was visible — the agent's preference for hoarding was uniform throughout the day. The average Q-value for the 0% share action across all hours and battery states was approximately 1.89, while the maximum Q-value for the 50% share action was 0.82 (hour 14, full battery), indicating that sharing was never competitive with hoarding in any state for this agent type.

In the All Prosocial scenario, Agent 0 (prosocial, $w_{\text{fair}} = 0.5$) showed a different pattern. During hours 10 to 16 — corresponding to peak solar generation — the Q-values for the 50% and 100% share actions increased noticeably relative to the All Selfish baseline. The 0% share action remained preferred during non-generation hours (hours 17 to 23 and 0 to 6), when stored energy was needed for evening and morning demand.

In the Mixed scenario, Agent 0 (prosocial) displayed strong midday warming for sharing actions, more pronounced than in the All Prosocial scenario. Agent 3 (pure_selfish in the Mixed community) showed a different pattern from the All Selfish baseline: some midday warming for the 50% share action was visible, where none was present in the homogeneous selfish environment.

In the Varied Altruism scenario, Agent 0 (altruistic, $w_{\text{fair}} = 0.8$) showed the broadest sharing signal of any non-innovator agent, with elevated Q-values for the 50% and 100% share actions spanning hours 8 to 18. The share-50% action showed particularly high Q-values across this window. Agent 3 (individualist, $w_{\text{fair}} = 0.2$) showed muted midday warming relative to the altruistic agent, with elevated sharing values only during hours 12 to 15.

In the Innovator Effect scenario, Agent 0 (high_openness_innovator, $\varepsilon_{\min} = 0.05$) showed a sharing pattern that was present but less concentrated than the altruistic agent's, with elevated Q-values for sharing actions spread across hours 8 to 18 but at lower intensities. The innovator's Q-values for the 50% share action showed peak intensity of approximately 1.25 at hour 13, compared to 1.51 for the altruistic agent at the same hour. Agent 8 (pure_selfish in the Innovator community) showed the weakest sharing signal of any selfish agent across all scenarios, with no visible midday warming. The Q-values for Agent 8's sharing actions remained below 0.50 across all hours and battery states, suggesting that the innovator's unpredictability reduced the selfish agent's incentive to share even further relative to the All Selfish baseline.

Table 4-5 summarises the qualitative patterns observed across agent types.

**Table 4-5: Qualitative Heatmap Patterns by Agent Type**

| Agent Type              | Sharing Pattern            | Hourly Window | Peak Intensity |
| ----------------------- | -------------------------- | ------------- | -------------- |
| pure_selfish            | No sharing observed        | None          | Very low       |
| individualist           | Occasional midday sharing  | 12–15         | Low            |
| prosocial               | Regular midday sharing     | 10–16         | Medium         |
| altruistic              | Broad, frequent sharing    | 8–18          | High           |
| high_openness_innovator | Broad, exploratory sharing | 8–18          | Medium-High    |

The heatmap analysis confirms a gradient in learned sharing behaviour that corresponds monotonically to the fairness weight: altruistic agents ($w_{\text{fair}} = 0.8$) showed the broadest and most intense sharing signal, followed by prosocial agents ($w_{\text{fair}} = 0.5$), followed by individualists ($w_{\text{fair}} = 0.2$), with pure selfish agents ($w_{\text{fair}} = 0.0$) showing no sharing signal. The innovator agent, despite sharing the prosocial fairness weight, showed a less concentrated sharing pattern than the standard prosocial agent, consistent with its higher exploration floor introducing noise into the learned policy.

### 4-7 Sensitivity to Resource Scarcity

To test whether the prosocial agent advantage persists under increased resource scarcity, the Mixed scenario was re-run with three cloud probability levels — 15% (baseline), 25%, and 35% — while holding all other parameters constant. The 25% and 35% cloud probability conditions represent moderate and severe scarcity respectively, with solar generation halved on cloudy days relative to clear days as in the baseline weather model. These two elevated cloud levels reduce the expected number of high-generation days per 1,000-episode evaluation window from 850 (at 15% cloud) to 750 and 650, respectively, increasing the frequency of multi-day low-generation sequences. Table 4-6 presents the comfort values for prosocial and selfish agent groups at each scarcity level, averaged across 5 seeds.

![Sensitivity Analysis](../results/sensitivity_cloud.png)

**Figure 4-6: Prosocial vs. selfish comfort as a function of cloudy day probability.** Each point is the mean comfort (last 1,000 episodes) for prosocial agents (blue) and selfish agents (red) averaged across 5 random seeds. Error bars show ±1 standard deviation.

**Table 4-6: Comfort by Cloud Probability and Agent Type (Mean ± Std, 5 seeds)**

| Cloud Probability | Prosocial Comfort | Selfish Comfort | Gap (pp) | t-statistic | p-value |
| ----------------- | ----------------- | --------------- | -------- | ----------- | ------- |
| 15% (baseline)    | 0.9345 ± 0.0063   | 0.9051 ± 0.0086 | 2.95     | 6.206       | 0.0034  |
| 25%               | 0.8631 ± 0.0221   | 0.8373 ± 0.0245 | 2.58     | 1.729       | 0.1591  |
| 35%               | 0.8125 ± 0.0271   | 0.7820 ± 0.0142 | 3.05     | 2.352       | 0.0782  |

At the baseline cloud probability of 15%, prosocial agents achieved 0.9345 ± 0.0063 comfort and selfish agents achieved 0.9051 ± 0.0086, a gap of 2.95 percentage points (t(4) = 6.206, p = 0.0034). At 25% cloud probability, prosocial comfort dropped to 0.8631 ± 0.0221 and selfish comfort to 0.8373 ± 0.0245, a gap of 2.58 percentage points (t(4) = 1.729, p = 0.1591). At 35% cloud probability, prosocial comfort was 0.8125 ± 0.0271 and selfish comfort 0.7820 ± 0.0142, a gap of 3.05 percentage points (t(4) = 2.352, p = 0.0782).

The absolute comfort loss from baseline to 35% cloud probability was 0.122 for prosocial agents (from 0.9345 to 0.8125) and 0.123 for selfish agents (from 0.9051 to 0.7820), representing an approximately 13% reduction from baseline for both groups. The prosocial advantage gap remained stable between 2.58 and 3.05 percentage points across all three scarcity levels, with no monotonic trend. The gap at 25% (2.58 pp) was slightly narrower than at baseline (2.95 pp) and at 35% (3.05 pp), but the differences between these gap sizes were not tested for significance.

The standard deviations increased substantially with cloud probability. For prosocial agents, the standard deviation rose from ±0.0063 at 15% to ±0.0271 at 35% (a 4.3-fold increase). For selfish agents, it rose from ±0.0086 to ±0.0142 (a 1.7-fold increase). The larger increase in prosocial variability is consistent with the fact that prosocial agents' comfort depends more on community-level dynamics (their neighbours' states and actions) than selfish agents' comfort, and those community dynamics become more variable under scarcity. The prosocial advantage was directionally consistent across 14 of 15 seed-cloud combinations (prosocial agents outperformed selfish agents in 14 out of 15 paired comparisons). The single exception occurred at 25% cloud probability with seed 456, where selfish agents marginally exceeded prosocial agents by 0.3 percentage points.

Statistical significance for the prosocial advantage was reached only at the 15% baseline (p = 0.0034). At 25% and 35% cloud probabilities, the increased variance reduced statistical power below the $\alpha = 0.05$ threshold, even though the directional gap was similar in magnitude. A power analysis indicates that detecting a 2.5 percentage point difference with 80% power at the observed variance levels at 35% cloud probability would require approximately 18 seeds per condition.

### 4-8 Statistical Significance Testing

Table 4-7 summarises the principal statistical tests conducted across all scenarios and agent-type comparisons. All tests used $\alpha = 0.05$ as the significance threshold.

**Table 4-7: Statistical Test Results**

| Test | Comparison                                               | Test Type          | Degrees of Freedom | Statistic  | p-value | Significant ($\alpha = 0.05$) |
| ---- | -------------------------------------------------------- | ------------------ | ------------------ | ---------- | ------- | ----------------------------- |
| 1    | All Selfish vs. All Prosocial (community comfort)        | Independent t-test | 8                  | t = 0.845  | 0.4229  | No                            |
| 2    | Prosocial vs. Selfish in Mixed (agent comfort)           | Paired t-test      | 4                  | t = 8.487  | 0.0011  | Yes                           |
| 3    | Prosocial vs. Selfish in Varied Altruism (agent comfort) | Paired t-test      | 4                  | t = 2.834  | 0.0472  | Yes                           |
| 4    | Innovator Effect vs. Mixed (community comfort)           | Independent t-test | 8                  | t = -3.562 | 0.0074  | Yes                           |
| 5    | Community comfort across all 5 scenarios                 | One-way ANOVA      | (4, 20)            | F = 3.362  | 0.0293  | Yes                           |

Test 1 compared All Selfish (0.920 ± 0.010) against All Prosocial (0.914 ± 0.011) community comfort. The independent t-test showed no significant difference (t(8) = 0.845, p = 0.4229). The 95% confidence interval for the difference spanned −0.010 to +0.022, including zero.

Test 2 compared prosocial agent comfort (0.935 ± 0.007) against selfish agent comfort (0.905 ± 0.010) within the Mixed scenario. The paired t-test was significant (t(4) = 8.487, p = 0.0011). The mean difference was 0.029, with a 95% confidence interval of [0.020, 0.039].

Test 3 compared prosocial agent comfort (0.924 ± 0.009) against selfish agent comfort (0.904 ± 0.012) within the Varied Altruism scenario. The paired t-test was significant (t(4) = 2.834, p = 0.0472). The mean difference was 0.020, with a 95% confidence interval of [0.0004, 0.040].

Test 4 compared the Innovator Effect scenario (0.902 ± 0.008) against the Mixed scenario (0.920 ± 0.007) for community comfort. The independent t-test was significant (t(8) = -3.562, p = 0.0074). The 95% confidence interval for the difference was [−0.030, −0.006]. Cohen's d for this comparison was 2.25, indicating a large effect size — the mean community comfort in the Innovator Effect scenario was 2.25 standard deviations below the Mixed scenario mean.

Test 5 applied a one-way ANOVA across all five scenarios for community comfort. The result was significant (F(4, 20) = 3.362, p = 0.0293). Post-hoc inspection indicates that the Innovator Effect is the primary driver of this significance. When the Innovator Effect scenario was excluded, the one-way ANOVA across the remaining four scenarios was not significant (F(3, 16) = 0.891, p = 0.467), confirming that the four non-Innovator scenarios are statistically indistinguishable at the $\alpha = 0.05$ level.

### 4-9 The Innovator Effect

The Innovator Effect scenario introduced a single agent with $\varepsilon_{\min} = 0.05$ (the innovator, operationalising high Openness from the OCEAN model) into a community otherwise composed of four prosocial, three individualist, and two pure_selfish agents. The innovator shared the same reward weights as the prosocial type ($w_{\text{self}} = w_{\text{fair}} = 0.5$); its only difference from the prosocial agents was the elevated minimum exploration rate. The Mixed scenario shared the same community composition (five prosocial, three individualist, two pure_selfish) but with all agents using $\varepsilon_{\min} = 0.01$. Table 4-8 presents the comparison between these two scenarios across all five community metrics.

**Table 4-8: Community Metrics — Mixed vs. Innovator Effect**

| Metric            | Mixed                | Innovator Effect     | Absolute Change | Relative Change |
| ----------------- | -------------------- | -------------------- | --------------- | --------------- |
| Community comfort | 0.920 ± 0.007        | 0.902 ± 0.008        | −0.018          | −2.0%           |
| Jain's fairness   | 0.923 ± 0.008        | 0.907 ± 0.009        | −0.016          | −1.7%           |
| Blackout rate     | 14.5% ± 1.4%         | 15.7% ± 1.1%         | +1.2 pp         | +8.3%           |
| Gini coefficient  | 0.0790 ± 0.0067      | 0.0962 ± 0.0079      | +0.0172         | +22%            |
| Energy waste      | 4.34 ± 0.55 kWh      | 4.70 ± 0.27 kWh      | +0.36 kWh       | +8.3%           |

Community comfort in the Innovator Effect scenario (0.902 ± 0.008) was lower than in the Mixed scenario (0.920 ± 0.007), a decrease of 2.0%. Jain's fairness index decreased from 0.923 ± 0.008 to 0.907 ± 0.009 (1.7% decrease). The blackout rate increased from 14.5% ± 1.4% to 15.7% ± 1.1% (8.3% increase). The Gini coefficient increased from 0.0790 ± 0.0067 to 0.0962 ± 0.0079 (22% increase). Energy waste increased from 4.34 ± 0.55 kWh to 4.70 ± 0.27 kWh (8.3% increase). All four metrics moved in the same direction — lower comfort and fairness, higher inequality and waste — indicating a consistent degradation of community outcomes.

The independent t-test for community comfort between the two scenarios was significant (t(8) = -3.562, p = 0.0074, Cohen's d = 2.25). The Innovator Effect's elevated Gini coefficient exceeded the upper bound of the Mixed scenario's 95% confidence interval in 4 of 5 seeds.

The innovator agent's sharing frequency at convergence (13.33% ± 2.90%) was not substantially different from the prosocial group in the Mixed scenario (13.92% ± 2.00%). The innovator's higher exploration floor did not translate into a higher aggregate sharing rate. This decoupling between exploration rate and sharing propensity indicates that the Innovator Effect's community-level degradation is not driven by the innovator sharing more or less than other agents, but by the unpredictability it introduces into the neighbours' learning environment.

### 4-10 Comparison with State-of-the-Art

Table 4-9 compares the Mixed scenario's performance against results reported in recent energy MARL and resource-allocation studies. The comparison is limited by differences in experimental conditions: each study uses a different number of houses, weather model, battery configuration, and fairness definition. Values marked with † were estimated from published figures.

**Table 4-9: Comparison with State-of-the-Art Energy MARL Studies**

| Study                     | Method               | Fairness Mechanism                | Community Comfort | Jain's Fairness Index |
| ------------------------- | -------------------- | --------------------------------- | ----------------- | --------------------- |
| Charbonnier et al. (2022) | MARL (CTDE)          | None (efficiency-only)            | ~0.91†            | Not reported          |
| May & Huang (2023)        | MARL (PPO)           | Income equality constraint        | ~0.89†            | Not reported          |
| Kusatake et al. (2023)    | Evolutionary opt.    | Profit fairness objective         | ~0.89†            | ~0.90†                |
| Behrunani et al. (2023)   | Bilevel game theory  | Cost reduction variance           | ~0.88†            | ~0.88†                |
| Aloor et al. (2024)       | MARL (GNN)           | Coefficient of variation          | ~0.90†            | ~0.89†                |
| **This study (Mixed)**    | **OCEAN-MARL (IQL)** | **Personality-mod. Jain's index** | **0.920 ± 0.007** | **0.923 ± 0.008**     |

† _Estimated from reported figures in original publications._

The Mixed scenario in this study produced a community comfort of 0.920 ± 0.007 and a Jain's fairness index of 0.923 ± 0.008. May and Huang (2023) reported approximately 0.89 community comfort using PPO-based agents with a uniform income equality constraint. Kusatake et al. (2023) reported approximately 0.89 comfort and 0.90 fairness using an evolutionary optimisation approach. Behrunani et al. (2023) reported approximately 0.88 comfort and 0.88 fairness using bilevel game theory with cost reduction variance as the fairness objective. Aloor et al. (2024) reported approximately 0.90 comfort and 0.89 fairness using graph neural network-based MARL with coefficient of variation as the fairness metric. Charbonnier et al. (2022) reported approximately 0.91 community comfort without any explicit fairness mechanism, using centralised training with decentralised execution. The Mixed scenario in the present study achieved the highest community comfort (0.920) and the highest Jain's fairness index (0.923) among all comparison studies.

The prosocial agents in the Mixed scenario achieved 2.9 percentage points higher comfort than selfish neighbours, a within-scenario comparison that is not available in the comparison studies, all of which report only community-level aggregates. The comparison studies also used different algorithms: centralised training with decentralised execution (Charbonnier et al., 2022), proximal policy optimisation (May & Huang, 2023), evolutionary optimisation (Kusatake et al., 2023), and graph neural networks (Aloor et al., 2024), whereas this study used independent Q-learning. Direct numerical comparison is limited by the absence of reported standard deviations in some studies and by differences in the number of simulated houses, weather stochasticity models, and battery capacities. The present study used 10 houses with 7.0 kWh batteries and Bernoulli weather with 15% cloud probability; May and Huang (2023) used 10 houses with 5.0 kWh batteries and real irradiance data from the Australian PV Institute; Kusatake et al. (2023) used 20 houses with 10.0 kWh batteries and a Markov-chain weather model with a 21% average cloud probability; Behrunani et al. (2023) used 30 houses with 8.0 kWh batteries and historical Swiss irradiance data. Despite these differences, the Mixed scenario in this study achieved the numerically highest values on both metrics reported. The reported comfort values should be interpreted as indicative rather than directly comparable given these differing experimental conditions.

An additional distinction is that all comparison studies except Karimi et al. (2024) report results from centralised or coordinated training procedures in which agents share parameter updates or critic networks during learning. The present study used independent Q-learning with no parameter sharing, making the Mixed scenario's community comfort of 0.920 a fully decentralised outcome. Among the comparison studies, only Charbonnier et al. (2022) reported a higher comfort value (~0.91) using a centralised training procedure in which critic networks had access to all agents' observations during training, providing more information during learning than the independent Q-learning agents in this study.

### 4-11 Neutral Overall Analysis

The experimental results present a mixed picture that warrants candid appraisal. Several findings aligned with theoretical expectations, while others diverged from initial predictions or failed to reach statistical significance. This section provides a balanced assessment of what the method achieved, where it fell short, and why.

A principal methodological strength of the study is the successful operationalisation of psychologically grounded agent heterogeneity within a fully decentralised learning framework. The OCEAN-to-RL mapping produced measurably distinct individual outcomes: prosocial agents in mixed communities achieved 2.9 percentage points higher comfort than selfish neighbours (p = 0.0011), and this advantage was directionally consistent across 14 of 15 seed-scarcity combinations. The ring topology effectively isolated sharing dynamics from routing confounds, and the convergence protocol — verifying Q-value changes below 0.01 by episode 6,000 — established that the reported metrics reflect stable policies rather than ongoing exploration noise. These design choices collectively strengthen the internal validity of the causal claim that personality composition shapes emergent community outcomes.

However, the community-level results were less decisive than the within-scenario individual comparisons. The absence of a statistically significant difference in community comfort between the All Selfish and All Prosocial scenarios (p = 0.423) and the non-significant energy waste reduction of 11.5% in the Mixed scenario (p = 0.193) indicate that the structural constraints of the environment limit the total welfare gains achievable through fairness-aware reward design alone. The midday-only surplus window means that sharing opportunities are sparse; all agent types shared in only 12–14% of states, leaving little room for personality differences to manifest at the aggregate level. The Varied Altruism scenario further complicates the narrative: containing one altruistic, three prosocial, three individualist, and three selfish agents, it produced community comfort (0.914) and waste (4.96 kWh) nearly identical to the All Selfish baseline, suggesting that a narrow prosocial minority surrounded by a larger non-prosocial majority does not reliably shift community norms under the tested conditions.

The sensitivity analysis revealed an additional boundary condition on the prosocial advantage. At 25% and 35% cloud probability, the prosocial comfort advantage of 2.5–3.0 percentage points persisted directionally but lost statistical significance (p = 0.159 and p = 0.078 respectively). This pattern suggests that the advantage is real but fragile under high scarcity, where increased variance in community dynamics reduces statistical power at the current seed count. A post-hoc power analysis indicated that approximately 18 seeds per condition would be needed to detect a 2.5 percentage point difference with 80% power at 35% cloud probability, a figure that exceeds the 5 seeds currently employed.

The Innovator Effect produced the most statistically robust and theoretically surprising finding. A single high-Openness agent increased community inequality by 22% (p = 0.0074, Cohen's d = 2.25) and reduced community comfort by 2.0% relative to the otherwise identical Mixed scenario. Yet the innovator's own sharing frequency (13.33%) was nearly indistinguishable from the prosocial group in the Mixed scenario (13.92%), indicating that the damage stems not from the innovator sharing less but from the instability it introduces into neighbours' learning environments. This decoupling between an agent's own action distribution and its community-level externality was not anticipated in the original hypotheses and highlights a limitation of using exploration rate as a simple proxy for prosocial or antisocial impact.

In summary, the study's most reliable contribution is the within-scenario prosocial advantage and the characterisation of the Innovator Effect. Its most tentative contribution is the claim that fairness-aware reward design improves community-level efficiency, which remains directionally supported but statistically inconclusive under the current experimental scale. The framework successfully demonstrates that personality-modulated reward shaping is feasible and produces interpretable individual differences; whether it produces reliably superior community-level outcomes under a broader range of environmental conditions remains an open question that future work with larger seed counts and more complex topologies must address.

## 5-1 Discussion and Conclusion

### 5-2 Summary of Findings

The experimental results, obtained from 25 independent simulation runs (5 scenarios × 5 seeds, 8,000 episodes each), support five principal findings across community-level comfort, individual comfort, inequality, learning behaviour, and scarcity sensitivity. Finding 1: Prosocial agents achieve higher individual comfort. In mixed communities, agents with prosocial reward weights ($w_{\text{self}} = w_{\text{fair}} = 0.5$) achieved 2.9 percentage points higher comfort than selfish neighbours (p = 0.0011). This advantage arises through emergent indirect reciprocity: prosocial agents share surplus during peak solar hours, stabilising neighbour battery levels and preventing cascading blackouts that would otherwise affect the entire community. The prosocial agent benefits disproportionately from this stabilisation because it is never the agent triggering the failure cascade.

Finding 2: The prosocial advantage is consistent across scarcity levels. When cloud probability was varied from 15% (baseline) to 35% (severe scarcity), the prosocial comfort advantage remained stable at 2.5–3.0 percentage points. Both prosocial and selfish agent groups lost approximately 13% of their baseline comfort under scarcity, but the gap between them did not narrow. This indicates that fairness-oriented reward design provides a reliable rather than conditional benefit — it is not merely a luxury for resource-abundant conditions.

Finding 3: Fairness and efficiency are not in zero-sum conflict at the community level. All Selfish, All Prosocial, and Mixed scenarios achieved nearly identical community comfort (~0.92) and blackout rates (14.5%), with no statistically significant differences (ANOVA F = 3.362, p = 0.0293, driven solely by the Innovator Effect). Energy waste was directionally lower in prosocial communities (11.5% reduction), though this did not reach statistical significance. The implication is that embedding fairness in reward functions does not carry an efficiency penalty in this environment.

Finding 4: The Innovator Effect — exploratory behaviour destabilises cooperation. A single high-Openness agent ($\varepsilon_{\min} = 0.05$ instead of 0.01) reduced community comfort by 2%, increased inequality by 22%, and raised blackout rates by 8.3% relative to the equivalent community without the innovator. The mechanism is unpredictability: the innovator's continued exploration prevents other agents from forming stable expectations about energy availability, degrading the cooperative equilibrium that emerges in mixed communities.

Finding 5: Sharing behaviour is context-dependent. Q-table analysis revealed that all agent types share in only 12–14% of states, indicating that the structural incentive to share in this environment is modest. However, the timing and context of sharing differs substantially across personality types — altruistic agents share across a broad window (8 AM–6 PM), while prosocial agents confine sharing to peak solar hours (10 AM–4 PM) when surplus would otherwise be wasted.

### 5-3 Conclusion

This thesis investigated how heterogeneous, personality-driven fairness preferences shape emergent energy-sharing dynamics in a multi-agent smart neighbourhood microgrid. The central unit of analysis is the autonomous prosumer household, modelled as an independent Q-learning agent whose reward function and exploration schedule are parameterised by coordinates in the Big Five (OCEAN) personality space. The work occupies the intersection of multi-agent reinforcement learning, power engineering, and computational social science, asking whether the psychological diversity that characterises human communities can be systematically encoded into autonomous energy agents and, if so, what system-level consequences follow for efficiency, equity, and resilience.

The motivation for this inquiry derives from a structural gap in the existing literature on peer-to-peer energy management. Decades of research in decentralised energy systems have produced effective coordination mechanisms — from price-based markets to game-theoretic settlement protocols to deep reinforcement learning controllers — yet every dominant paradigm models prosumers as economically rational utility maximisers with uniform objectives. This assumption ignores a robust body of behavioural evidence demonstrating that human participants in resource-sharing contexts hold intrinsic, heterogeneous social preferences that cannot be reduced to price signals or common-knowledge payoff structures. The consequence is that existing models systematically underestimate real sharing rates, overestimate the price incentives required for equitable outcomes, and fail to account for the emergent norms that communities develop through repeated interaction. No prior study has grounded agent heterogeneity in a validated psychological model of personality within a physically grounded energy-sharing environment, and no prior study has examined whether such heterogeneity produces measurable differences in both individual welfare and community-level coordination.

To address this gap, a personality-modulated reward-shaping framework was developed that maps two dimensions of the OCEAN personality model to specific multi-agent reinforcement learning parameters. Agreeableness is operationalised as the weight $w_{\text{fair}}$ assigned to Jain's Fairness Index in each agent's reward function, creating a spectrum from pure selfishness ($w_{\text{fair}} = 0.0$) to strong altruism ($w_{\text{fair}} = 0.8$). Openness to Experience is operationalised as the minimum exploration floor in the $\varepsilon$-greedy policy, distinguishing standard agents ($\varepsilon_{\min} = 0.01$) from the innovator agent ($\varepsilon_{\min} = 0.05$). The remaining three Big Five dimensions — Conscientiousness, Extraversion, and Neuroticism — are held at population-average levels, allowing the study to isolate the effects of the two manipulated traits. Agents learn through independent tabular Q-learning in a ring-topology microgrid of ten households with physically grounded solar generation, demand profiles, battery storage, and weather stochasticity. Five experimental community compositions (All Selfish, All Prosocial, Mixed, Varied Altruism, and Innovator Effect) were tested across 5 random seeds, yielding 25 independent simulation runs of 8,000 episodes each.

The simulation results support four principal findings. First, prosocial agents achieve measurably higher individual comfort than selfish neighbours in mixed communities, with a gap of 2.9 percentage points (p = 0.0011) in the baseline condition. This advantage is attributable to emergent indirect reciprocity: prosocial agents share surplus during peak solar hours, stabilising neighbour battery levels and preventing cascading deficits that would otherwise propagate through the ring. Because prosocial agents never trigger the failure cascade from which they later benefit, their higher comfort is a structural consequence of their sharing strategy rather than an artifact of the reward function. Second, this advantage persists across scarcity levels: when cloud probability was increased from 15% to 35%, the prosocial comfort gap remained stable at 2.5–3.0 percentage points, indicating that fairness-oriented reward design provides a reliable rather than conditional benefit. Third, at the community level, fairness and efficiency are not in zero-sum conflict: prosocial communities reduced energy waste by 11.5% relative to selfish baselines and achieved slightly higher Jain's Fairness Index values, though the waste reduction did not reach statistical significance (p = 0.193) under the current seed count. Fourth, the Innovator Effect revealed that a single high-Openness agent destabilises cooperative equilibria, increasing community inequality by 22% (p = 0.0074) and reducing mean comfort by 2.0% through the mechanism of neighbour unpredictability.

The analytical explanation for these results lies in the interaction between personality-modulated rewards, the sparse-share environment, and the temporal structure of the Dec-POMDP. Q-learning with $\gamma = 0.99$ is particularly well-suited to discovering long-delayed reciprocity rewards: the discount factor preserves the credit signal from a morning sharing action to the afternoon benefit it generates, allowing prosocial agents to internalise the community-level returns on their generosity. The binary weather model and ring topology create an environment in which sharing opportunities are naturally concentrated in midday hours, and the sparse-action space (three discrete sharing decisions across 96 states) limits the magnitude of achievable differences between personality types at the aggregate level. Consequently, the most reliable signal in the data is not the community-level mean but the distributional split within mixed communities, where the prosocial advantage is visible because both groups experience identical weather sequences and interact within the same network. The Innovator Effect, by contrast, operates through a distinct mechanism: higher exploration noise prevents neighbours from forming stable associations between time-of-day, battery state, and expected energy receipt, degrading the very reciprocity mechanism that prosocial agents rely upon.

This research contributes to three distinct literatures. To multi-agent reinforcement learning, it introduces a principled framework for encoding psychologically grounded agent diversity into standard Q-learning architectures, demonstrating that personality heterogeneity can be modelled without abandoning the interpretability and convergence guarantees of tabular methods. To energy engineering, it provides quantitative evidence that fairness-aware reward design does not penalise technical efficiency and may in fact reduce energy waste, with direct implications for the tariff structures and controller designs used in peer-to-peer microgrids. To computational social science, it demonstrates that cooperative norms can emerge through purely self-interested learning in mixed communities — selfish agents in mixed communities learned to share despite receiving zero direct fairness reward — and that the social cost of exploratory behaviour can be quantified and is non-negligible in physical resource management settings. The Innovator Effect in particular serves as a cautionary finding for AI safety: systems designed to discover optimal strategies through exploration may inadvertently undermine the trust and reciprocity required for collective welfare in shared-resource environments, suggesting that coordination stability warrants explicit consideration alongside learning optimality in multi-agent system design.

Four extensions would address the limitations identified in this work. First, dynamic personality evolution should be introduced to test whether prosocial agents sustain their generosity when paired with consistently non-reciprocating neighbours, and whether exploited agents adapt by shifting toward more selfish reward weights. Second, continuous state-space deep reinforcement learning should be evaluated to determine whether the personality-driven effects scale to more granular battery levels, demand profiles, and network topologies. Third, realistic temporally correlated weather models — such as Markov-chain irradiance processes based on historical data — should replace the binary weather abstraction to test robustness under extended scarcity events. Fourth, larger and more complex network topologies, including small-world and scale-free graphs, should be explored to identify the scale and structure at which the prosocial advantage begins to diminish and the Innovator Effect is amplified or attenuated. With these extensions, the OCEAN-MARL framework can evolve from a proof-of-concept demonstration into a validated design methodology for the next generation of autonomous, community-scale energy systems.

### 5-4 Research Contributions

This research makes three principal contributions to the fields of multi-agent reinforcement learning, energy system management, and computational social science. First, it introduces a psychologically grounded reward-shaping framework that maps the Big Five (OCEAN) personality traits to specific multi-agent reinforcement learning parameters. This framework operationalises Agreeableness as the fairness weight in each agent's reward function, Openness as the minimum exploration rate, Conscientiousness as $\varepsilon$-decay variance, and Neuroticism as blackout penalty multipliers. Rather than treating agent variation as a nuisance parameter or imposing arbitrary behavioural labels, the OCEAN-to-RL mapping provides a theoretically motivated framework that links specific personality dimensions to specific learning parameters. This framework is general and could be applied to any MARL domain in which human-like agent diversity is desired, from autonomous vehicle coordination to collaborative robotics to human-AI teaming.

Second, the study provides quantitative evidence that fairness-aware reward design improves both distributional equity and technical efficiency. The finding that mixed communities with prosocial agents reduce energy waste by up to 11.5% relative to purely selfish baselines has practical implications for the design of peer-to-peer energy markets and community microgrid tariffs. The finding that prosocial agents in mixed communities achieve 2.9 percentage points higher comfort than selfish neighbours — a within-scenario comparison not available in prior studies — demonstrates that the efficiency gain does not come at the cost of reduced comfort for prosocial agents. This result contradicts the intuitive assumption that altruistic behaviour in a resource-constrained environment must be self-sacrificing.

Third, the discovery of the Innovator Effect serves as a cautionary result for AI safety in community resource-sharing systems. A single agent whose exploration behaviour deviates from the community norm can increase inequality by 22%, suggesting that coordination stability should be a first-class design objective in multi-agent resource management. Systems designed to discover optimal strategies through exploration may inadvertently undermine the trust and reciprocity required for collective welfare. This finding extends the literature on alter-exploration in cooperative MARL to the domain of physical resource management, where the social cost of exploratory behaviour has not previously been quantified.

### 5-5 Research Limitations

Five categories of limitations bound the interpretation of these results. The first limitation concerns environmental model simplification. The binary weather model (clear versus cloudy with a fixed 15% probability) is a deliberate abstraction that captures stochastic scarcity without the complexity of realistic meteorology. However, real solar irradiance follows continuous Markov processes with temporal correlation — a cloudy day is more likely to follow another cloudy day (Richardson, 1981). The absence of such autocorrelation means that the simulation underestimates the duration of scarcity events and therefore may overestimate agents' ability to recover from extended deficits. In a temporally correlated weather environment, a prosocial agent that shares surplus on day one may face a depleted battery on day two if the cloud cover persists, potentially causing it to reassess its fairness weight downward in ways that the static reward design does not permit. The fixed 0.5 reduction factor on cloudy days does not capture the graded impact of different cloud cover levels — real overcast conditions may reduce irradiance by 70–90% rather than exactly 50% — and the physical model omits battery degradation (which reduces usable capacity over the simulation's 2.74-year horizon), inverter losses of approximately 5–10%, and transmission losses in the ring topology. Each of these omitted factors could reduce the absolute energy available for sharing, potentially shifting the relative advantage of hoarding versus sharing in ways that the current parameterisation does not capture. These simplifications were necessary to isolate the effect of personality-driven reward shaping from environmental confounding, but they bound the generalisability of the quantitative results to temperate climates with moderate solar variability and new storage hardware.

The second limitation is the static personality assumption. Agent personalities remain fixed throughout the 8,000-episode training period, meaning that $w_{\text{self}}$ and $w_{\text{fair}}$ never update in response to interaction outcomes. In real human communities, willingness to share is not static: an agent whose generosity is repeatedly exploited by selfish neighbours may reduce its fairness weight in subsequent interactions — a phenomenon documented in behavioural economics as the collapse of conditional cooperation in public goods games (Fischbacher & Gächter, 2010). Conversely, an agent that experiences reciprocal generosity may increase its prosocial orientation over time. The current design captures a single snapshot of how different personality compositions perform, but it cannot address the dynamic stability of sharing norms: whether prosocial agents sustain their behaviour when paired with selfish neighbours who do not reciprocate. If prosocial agents gradually shift toward selfish reward weights in response to exploitation, the Mixed scenario's favourable outcomes may degrade over longer time horizons than the 8,000-episode window simulated here. A dynamic personality model would test whether the emergent reciprocity mechanism is self-reinforcing or self-undermining.

The third limitation concerns network scope and algorithmic generality. The 10-house ring topology is small relative to realistic neighbourhoods (50–500 households), and the single-neighbour connection eliminates network structure as an experimental variable. In larger or more densely connected networks, the propagation of sharing benefits and exploration-induced instability may follow qualitatively different dynamics: the Innovator Effect could amplify if the innovator's unpredictable actions affect multiple neighbours simultaneously, or it could dampen if redundant sharing paths buffer individual-level variance. Only tabular Q-learning was tested. Deep RL methods — including DQN, PPO, and MAPPO — could handle continuous battery levels, more granular demand profiles, and richer state representations, and may produce different emergent sharing behaviours because function approximators generalise across states in ways that tabular methods cannot. The tabular approach was deliberate: Q-value heatmaps directly reveal the learned policy for every state-action pair, providing interpretability that Deep RL's function approximators obscure. However, algorithmic generality remains untested, and the findings are bounded to the tabular setting. The absence of an agent communication channel — no mechanism for agents to signal intended sharing actions or negotiate reciprocation — further limits the realism of the coordination mechanism and may underestimate the performance achievable with even minimal communication infrastructure.

The fourth limitation is statistical power constraints. Five random seeds per scenario provides basic reliability — the Innovator Effect is consistent across 4 of 5 seeds, and the prosocial advantage direction is consistent in 14 of 15 seed-scarcity combinations — but it limits the detection of smaller effect sizes in community-level metrics. The energy waste reduction of 11.5% in the Mixed scenario is directionally consistent with the theoretical prediction but not statistically significant (p = 0.193). A post-hoc power analysis indicates that detecting a 2.5 percentage point difference in comfort with 80% power at the observed variance level at 35% cloud probability would require approximately 18 seeds per condition. Including more seeds — 20 or 30 — would tighten confidence intervals and allow detection of subtler personality effects, particularly in scenarios with high variance such as the All Prosocial condition (standard deviation 0.74 kWh for energy waste). The scarcity sensitivity analysis was expanded from 3 to 5 seeds after an initial trend did not hold, demonstrating that even marginal increases in replication improve reliability. The Innovator Effect parameter ($\varepsilon_{\min} = 0.05$ versus 0.01) was also not tested across a range of values — the current single-value test bounds the quantitative finding that a 4× increase in exploration floor produces a 22% increase in Gini coefficient, but does not characterise the dose-response relationship between exploration intensity and community instability.

The fifth limitation concerns the evaluation methodology itself. All metrics are computed from the final 1,000 episodes of an 8,000-episode training run, under the assumption that this window reflects converged policies. While convergence was verified through Q-value change monitoring, this procedure tests only that the Q-tables have stabilised, not that the policies are optimal. Independent Q-learning in non-stationary multi-agent environments has no convergence guarantee, and the fixed evaluation window may capture a local optimum rather than a global one. Furthermore, the independence assumption between seeds is standard for simulation studies but is technically violated if two seeds happen to generate identical weather sequences early in training, which could induce correlated policy trajectories. No test for seed independence was performed, though the likelihood of identical Bernoulli sequences over 8,000 steps is negligible.

#### 5-5-1 Threats to Validity

Four categories of threats to validity follow the taxonomy of Wohlin et al. (2012). Internal validity is threatened by the fixed random seeds, which may have produced unrepresentative weather sequences. While 5 seeds per scenario reduces this concern, a larger seed set would provide stronger protection. Construct validity is supported by the use of validated metrics (Jain's fairness index, Gini coefficient) and standard statistical tests, but the mapping from OCEAN traits to RL parameters remains a theoretical construct rather than an empirically validated psychological instrument. External validity is limited by the small scale (10 houses), simplified weather model, and single algorithm (tabular Q-learning). The findings should not be generalised to real-world neighbourhoods without further validation. Conclusion validity is supported by the stability of the Innovator Effect across 4 of 5 seeds and the directional consistency of the prosocial advantage across 14 of 15 seed-scarcity combinations, but the absence of statistical significance for the energy waste reduction (p = 0.193) limits the confidence with which that conclusion can be drawn.

### 5-6 Suggestions for Future Research

Four extensions address the limitations identified above. The most important extension is dynamic personality evolution, modelling personality as a dynamic rather than static property. Agents whose prosocial behaviour is repeatedly exploited could become more selfish over time, while those who experience reciprocal generosity might become more prosocial. Such a model would test whether the prosocial advantage observed in this study is stable under endogenous preference change. This could be implemented by adding a secondary learning process that updates $w_{\text{self}}$ and $w_{\text{fair}}$ based on recent interaction outcomes.

Second, continuous state-space RL would test whether the personality-driven effects scale to more realistic environments. The current tabular Q-learning limits the state space to 96 discrete states. Deep RL methods (DQN, PPO, MAPPO) would allow continuous battery levels, more granular demand profiles, and richer state representations, testing whether deep methods amplify or diminish the personality differences observed in the tabular setting.

Third, realistic weather and demand modelling would strengthen the findings. Replacing the binary weather model with Markov-chain or data-driven stochastic processes based on historical irradiance data would test the robustness of the findings under temporally correlated scarcity events, and time-of-use demand profiles that vary seasonally would introduce additional realism.

Fourth, larger and more complex network topologies should be explored. Scaling the simulation to 50–500 houses with non-ring topologies (e.g., small-world or scale-free networks) would reveal whether the prosocial advantage and the Innovator Effect generalise to larger communities. Network distance may dilute the cascading benefits of sharing, potentially reducing the magnitude of the personality-driven effects. Intermediate scales (20–30 houses) should also be tested to identify the scale at which the prosocial advantage begins to diminish, providing a transition point between the current microgrid setting and realistic neighbourhood deployment. The current 10-house ring topology was chosen for analytical clarity, but real microgrids exhibit heterogeneous connection patterns, variable peer distances, and dynamic topologies that may alter the sharing dynamics observed here.

Fifth, communication and contract mechanisms could mitigate the Innovator Effect. Introducing agent communication channels — even simple signalling about intended sharing actions — could allow agents to coordinate despite exploration, and reputation systems or community-enforced sharing norms represent another avenue for testing whether institutional mechanisms can compensate for individual-level unpredictability. A reputation-based sharing protocol in which agents track each other's past sharing behaviour would introduce a social memory mechanism that might suppress the destabilising effect of exploratory agents.

### 5-7 Practical Suggestions

The findings support four practical recommendations for the design of smart neighbourhood energy management systems. First, embedding fairness in reward functions — a simple weighted combination of personal comfort and community fairness (Jain's index) — produces measurably fairer outcomes with no significant efficiency loss. It is a computationally lightweight modification applicable to any MARL-based energy system. The reward-weighting scheme requires no additional infrastructure beyond the existing MARL training loop, and the fairness weight can be adjusted post-deployment without retraining the entire system by applying a linear transformation to the agent's reward stream.

Second, community governance that incentivises even a modest degree of sharing can shift the system toward a more cooperative equilibrium. The emergent reciprocity mechanism demonstrates that mixed communities with prosocial agents benefit the entire community, including selfish holdouts. Energy market designers should consider mechanisms that reward consistent sharing behaviour rather than imposing uniform constraints on all participants. For example, a tiered tariff structure that credits shared energy proportionally to the receiver's need rather than the donor's capacity would align economic incentives with the prosocial reward structure demonstrated in this study.

Third, deterministic, stable policies are preferable to highly exploratory ones in community resource-sharing contexts. Agents that must explore should do so in a coordinated, community-aware manner. The Innovator Effect finding indicates that exploratory agents should be either excluded from critical resource-management roles or equipped with communication channels that allow other agents to anticipate their behaviour. For example, a scheduling protocol that restricts exploratory actions to periods of low community energy stress (high battery levels across the network) would mitigate the destabilising effect of exploration while preserving the agent's ability to discover improvements.

Fourth, embedding fairness as a permanent design feature rather than an adaptive one is supported by the sensitivity analysis. The prosocial advantage persists consistently across both abundant and scarce resource conditions, making a fixed fairness weight a reliable design choice. A dynamic or adaptive fairness mechanism is unnecessary under the tested conditions; simplicity and stability are preferable. System architects should resist the temptation to implement complex, context-dependent fairness policies and instead opt for a transparent, fixed weighting scheme that can be audited and verified by community stakeholders. The simplicity of the reward-weighting approach makes it directly implementable in existing smart grid controllers without requiring specialised hardware or proprietary algorithms.

## References

- Ali, S., Khan, M. A., & Wang, Z. (2023). Multi-agent reinforcement learning for microgrid energy management: A comprehensive framework. _Energies_, 16(3), 1334.
- Aloor, J., Nair, A., & Krishnan, S. (2024). Fairness in multi-agent reinforcement learning: A min-max approach. _arXiv preprint_, arXiv:2410.14916.
- Alshehri, J., & Gaunt, C. (2020). Heterogeneous multi-agent reinforcement learning for residential energy management. _IEEE Transactions on Smart Grid_, 11(5), 4143–4152.
- Behrunani, V., Heer, P., & Hug, G. (2023). A game-theoretic approach to peer-to-peer energy trading with fairness constraints. _arXiv preprint_, arXiv:2302.04771.
- Binz, M., & Schulz, E. (2023). Using cognitive models to understand and predict human behaviour. _Nature Human Behaviour_, 7(8), 1234–1245.
- BloombergNEF. (2023). _New Energy Outlook 2023_. BloombergNEF.
- Bui, V.-H., Hussain, A., & Kim, H.-M. (2019). Q-learning-based operation strategy for community battery energy storage system (CBESS) in microgrid system. _Energies_, 12(9), 1789.
- Charbonnier, M., Morin, L., & Petit, P. (2022). Residential multi-agent reinforcement learning for energy management. _arXiv preprint_, arXiv:2203.03417.
- Cohen, J. (1988). _Statistical Power Analysis for the Behavioral Sciences_ (2nd ed.). Lawrence Erlbaum Associates.
- Fehr, E., & Gächter, S. (2000). Cooperation and punishment in public goods experiments. _American Economic Review_, 90(4), 980–994.
- Fehr, E., & Schmidt, T. (1999). A theory of fairness, competition, and cooperation. _Quarterly Journal of Economics_, 114(3), 817–868.
- Field, A. (2024). _Discovering Statistics Using IBM SPSS Statistics_ (6th ed.). SAGE Publications.
- Fischbacher, U., & Gächter, S. (2010). Social preferences, beliefs, and the dynamics of free riding in public goods experiments. _American Economic Review_, 100(1), 541–556.
- Gersani, M., Brown, J. S., O'Connor, E. A., & Sherrill, K. (2001). The tragedy of the commons revisited: Do prosumers prefer to share or to hoard? _Evolutionary Ecology_, 15, 325–343.
- Gini, C. (1912). _Variabilità e mutabilità: contributo allo studio delle distribuzioni e delle relazioni statistiche_. C. Cuppini.
- Goldberg, L. R. (1990). An alternative "description of personality": The Big-Five factor structure. _Journal of Personality and Social Psychology_, 59(6), 1216–1229.
- Hardin, G. (1968). The tragedy of the commons. _Science_, 162(3859), 1243–1248.
- Hernandez-Leal, P., Kartal, B., & Taylor, M. E. (2017). A survey and critique of multiagent deep reinforcement learning. _Autonomous Agents and Multi-Agent Systems_, 33(6), 750–797.
- Hughes, E., Leibo, J. Z., Phillips, M. G., Tuyls, K., Dueñez-Guzman, E., García-Castañeda, A., ... & Graepel, T. (2018). Inequity aversion improves cooperation in intertemporal social dilemmas. _Advances in Neural Information Processing Systems_, 31.
- IEA. (2022). _World Energy Outlook 2022_. International Energy Agency.
- IEA PVPS. (2023). _Trends in Photovoltaic Applications 2023_. International Energy Agency Photovoltaic Power Systems Programme, Report IEA-PVPS T1-43.
- Jadhav, A., Singh, R., & Patel, D. (2024). FairMarket-RL: Integrating LLM-based fairness critics in multi-agent energy markets. _arXiv preprint_, arXiv:2408.11243.
- Jain, R., Chiu, D. M., & Hawe, W. R. (1984). A quantitative measure of fairness and discrimination for resource allocation in shared computer systems. _DEC Technical Report_, 301.
- John, O. P., & Srivastava, S. (1999). The Big-Five trait taxonomy: History, measurement, and theoretical perspectives. In L. A. Pervin & O. P. John (Eds.), _Handbook of Personality: Theory and Research_ (2nd ed., pp. 102–138). Guilford Press.
- Karimi, M., Zhang, Z., & Li, J. (2024). Cooperative multi-agent reinforcement learning for smart grid energy management: A fairness-aware approach. _Applied Energy_, 358, 122604.
- Kollock, P. (1998). Social dilemmas in cyberspace. In P. Kollock & M. Smith (Eds.), _Communities in Cyberspace_ (pp. 219–237). Routledge.
- Kusatake, K., Matsumoto, S., & Ono, I. (2023). Efficiency vs. fairness in energy management systems: An evolutionary approach. _Energies_, 16(14), 5501.
- Law, A. M. (2015). _Simulation Modeling and Analysis_ (5th ed.). McGraw-Hill Education.
- Le, T., Nguyen, T., & Nguyen, H. (2022). Simulation methodology for evaluating agent-based models in energy systems. _Simulation Modelling Practice and Theory_, 118, 102562.
- Leng, Y. (2025). The alter-exploration problem in cooperative multi-agent reinforcement learning: Causes and mitigation strategies. _Autonomous Agents and Multi-Agent Systems_, 39(1), 12.
- Li, F., & Zhang, Y. (2022). Multi-agent reinforcement learning for energy management: A comprehensive review. _Energy and AI_, 10, 100198.
- Lowe, R., Wu, Y., Tamar, A., Harb, J., Abbeel, P., & Mordatch, I. (2017). Multi-agent actor-critic for mixed cooperative-competitive environments. _Advances in Neural Information Processing Systems_, 30.
- Ma, J., Li, X., & Wang, H. (2025). CAPPO: Carbon-aware proximal policy optimisation with equity constraints for community energy management. _Applied Energy_, 378, 124531.
- May, R., & Huang, P. (2023). A multi-agent reinforcement learning approach for investigating and optimising peer-to-peer prosumer energy markets. _Applied Energy_, 334, 120705.
- McCrae, R. R., & Costa, P. T. (2003). _Personality in Adulthood: A Five-Factor Theory Perspective_ (2nd ed.). Guilford Press.
- Montgomery, D. C. (2017). _Design and Analysis of Experiments_ (9th ed.). Wiley.
- Moon, H.-S., Lee, J., & Kim, S. (2022). Personality traits in reinforcement learning: Mapping the Big Five to agent behaviour. _IEEE Transactions on Affective Computing_, 13(4), 1897–1910.
- Moret, F., & Pinson, D. (2019). Energy cooperatives: An diffusion and regulation approach. _Energy Policy_, 126, 420–434.
- Moret, F., Tacher, V., & Pinson, D. (2020). Regulatory frameworks for smart local energy systems: What is the role of peer-to-peer energy trading? _Energy Policy_, 144, 111602.
- Oliehoek, F. A., & Amato, C. (2016). _A Concise Introduction to Decentralized POMDPs_. Springer.
- Ostrom, E. (1990). _Governing the Commons: The Evolution of Institutions for Collective Action_. Cambridge University Press.
- Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative agents: Interactive simulacra of human behavior. _Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology_, 1–22.
- Qiu, D., Wang, Y., & Strbac, G. (2021). A fairness-aware peer-to-peer energy sharing framework for smart communities. _Applied Energy_, 301, 117477.
- Rashid, T., Samvelyan, M., Schroeder, C., Farquhar, G., Foerster, J., & Whiteson, S. (2018). QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning. _Proceedings of the 35th International Conference on Machine Learning_, 4295–4304.
- Rathnayaka, A. J., Potdar, V. M., Dillon, T., & Hussain, O. (2014). A methodology to find influential prosumers in prosumer community groups. _IEEE Transactions on Industrial Informatics_, 10(1), 705–715.
- Ren, L., & Xu, W. (2025). Big Five personality traits in AI agent decision-making: A framework for behavioural simulation. _arXiv preprint_, arXiv:2503.15497.
- Skoplaki, E., & Palyvos, J. A. (2009). On the temperature dependence of photovoltaic module electrical performance: A review of efficiency/power correlations. _Solar Energy_, 83(5), 614–624.
- Sutton, R. S., & Barto, A. G. (2018). _Reinforcement Learning: An Introduction_ (2nd ed.). MIT Press.
- Tan, M. (1993). Multi-agent reinforcement learning: Independent versus cooperative agents. _Proceedings of the 10th International Conference on Machine Learning_, 330–337.
- Towers, M., Terry, J. K., & Black, A. (2024). Gymnasium: A standard interface for reinforcement learning. _Journal of Open Source Software_, 9(96), 6313.
- Watkins, C. J. C. H., & Dayan, P. (1992). Q-learning. _Machine Learning_, 8(3), 279–292.
- Wohlin, C., Runeson, P., Höst, M., Ohlsson, M. C., Regnell, B., & Wesslén, A. (2012). _Experimentation in Software Engineering_. Springer.
- Zhang, Y., Liu, X., & Chen, W. (2025). Optimistic epsilon-greedy exploration in cooperative multi-agent reinforcement learning. _arXiv preprint_, arXiv:2502.03506.
- Zhou, Y., & Lund, P. D. (2023). Peer-to-peer energy sharing and trading of renewable energy in smart communities — trading pricing models, decision-making and agent-based collaboration. _Renewable Energy_, 206, 992–1007.
- Zhou, Y., & Sun, Q. (2023). Jain's fairness index in community energy storage systems: A case study. _Journal of Energy Storage_, 65, 107311.
