# Digest: kaelbling1998pomdp

**Full cite:** L.P. Kaelbling, M.L. Littman, A.R. Cassandra, "Planning and acting in partially observable stochastic domains," *Artificial Intelligence* 101 (1998) 99–134. Received 11 Oct 1995; revised 17 Jan 1998. (Elsevier)

Authors' affiliations: Kaelbling (Computer Science Dept, Brown University); Littman (Computer Science, Duke University); Cassandra (Microelectronics and Computer Technology Corporation / MCC, Austin TX).

---

## Thesis / Problem

The paper brings operations-research techniques to bear on choosing **optimal actions in partially observable stochastic domains**. The motivating problem is a robot navigating an office building whose actions and observations are both unreliable (a move may stall or overshoot; a corridor may look like a corner). Such problems are modeled as **partially observable Markov decision processes (POMDPs)**. Two stated contributions: (1) recapitulate operations-research work on POMDPs and connect it to related AI work; (2) present a **novel exact algorithm (the "witness" algorithm)** for solving POMDPs off line, and show how a **finite-memory (finite-state) controller** can sometimes be extracted from the solution.

## Method — CONFIRMED: classical POMDP with Bayesian belief-state update

**Yes — this is unambiguously the classical POMDP formulation with a belief state updated by observations via Bayesian update.** Specific confirmation from the text:

- A POMDP is defined as a tuple ⟨S, A, T, R, Ω, O⟩ where ⟨S,A,T,R⟩ is an MDP, Ω is a finite set of observations, and O: S×A → Π(Ω) is the observation function giving a probability distribution over observations (Section 3.1).
- "A POMDP is an MDP in which the agent is unable to observe the current state. Instead, it makes an observation based on the action and resulting state" (Section 3.1).
- The agent is decomposed into a **state estimator (SE)** and a **policy (π)** (Fig. 2, Section 3.2). The SE "is responsible for updating the belief state based on the last action, the current observation, and the previous belief state."
- The **belief state b is a probability distribution over S** ("Our choice for belief states will be probability distributions over states of the world"), and it is a **sufficient statistic** for past history and initial belief state (Section 3.2).
- The **Bayesian belief update** is given explicitly (Section 3.3): starting from Pr(s′|o,a,b), applying Bayes' rule yields

  b′(s′) = O(s′,a,o) · Σ_{s∈S} T(s,a,s′) b(s) / Pr(o|a,b)

  where the denominator Pr(o|a,b) is a normalizing constant. The state-estimation function SE(b,a,o) outputs the new belief state b′.
- Because the belief state is a sufficient statistic, the optimal policy is the solution of a continuous-space "**belief MDP**" over the set B of belief states, with transition function τ(b,a,b′) and belief-reward ρ(b,a)=Σ_s b(s)R(s,a) (Section 3.4).
- Solution method: **value iteration** over belief space. The optimal t-step value function is **piecewise-linear and convex (PWLC)**, represented as the upper surface of a set of linear functions (α-vectors), one per **policy tree**. The **witness algorithm** computes a parsimonious set of policy trees per action (Q_a^t) in time polynomial in |S|,|A|,|Ω|,|V_{t−1}|,|Q_a^t| (Section 4). Infinite-horizon value function remains convex but may have infinitely many facets; approximated by finite-horizon value iteration (Section 4.6).

The paper also lays out the MDP background first (Section 2): tuple ⟨S,A,T,R⟩, Markov property, finite-/infinite-horizon discounted optimality, stationary vs. nonstationary policies, value iteration (Bellman error termination).

---

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| *Artificial Intelligence* 101 (1998) 99–134 | header | Journal, volume, year, page range |
| Received 11 October 1995; revised 17 January 1998 | header | Submission dates |
| MDP = tuple ⟨S, A, T, R⟩ | §2.1 | S finite states, A finite actions, T: S×A→Π(S) transition, R: S×A→ℝ reward |
| T(s,a,s′) | §2.1 | Probability of ending in s′ given start s, action a |
| R(s,a) | §2.1 | Expected immediate reward for action a in state s |
| Discount factor 0 < γ < 1 | §2.2 | Infinite-horizon discounted model; Σ γ^t r_t |
| Discounted sum = expected reward if run terminates each step w.p. (1−γ) | §2.2 | Interpretation of γ |
| Finite-horizon objective: E[Σ_{t=0}^{k−1} r_t] | §2.2 | Maximize expected sum over next k steps |
| Stationary policy π: S→A; nonstationary = time-indexed sequence π_t | §2.2 | Two policy kinds |
| Howard [24] showed a stationary optimal policy exists for infinite-horizon discounted | §2.2 | Attribution to Howard 1960 |
| Bellman error termination: |V_t(s)−V_{t−1}(s)| < ε | §2.3, Alg.1 | Value-iteration stopping criterion |
| Greedy policy loss bound: max_s |V_{πVt}(s) − V*(s)| < 2εγ/(1−γ) | §2.3 | If Bellman error < ε |
| t* polynomial in |S|,|A|, max|R(s,a)|, 1/(1−γ) | §2.3 | Horizon after which greedy policy = optimal [62] |
| POMDP = tuple ⟨S, A, T, R, Ω, O⟩ | §3.1 | Adds Ω (observations), O (observation function) |
| O(s′,a,o) | §3.1 | Prob. of observation o given action a, resulting state s′ |
| Belief state b = probability distribution over S; 0 ≤ b(s) ≤ 1, Σ b(s)=1 | §3.2, §3.3 | Sufficient statistic for history |
| Bayesian belief update b′(s′) = O(s′,a,o)·Σ_s T(s,a,s′)b(s) / Pr(o|a,b) | §3.3 | Core belief-update equation; SE(b,a,o)=b′ |
| Belief-MDP reward ρ(b,a) = Σ_s b(s)R(s,a) | §3.4 | Reward on belief states |
| Example: 4 states (1 goal), 2 observations, 2 actions (EAST/WEST) | §3.2, Fig.3 | Actions succeed w.p. 0.9, else opposite direction |
| Initial belief [0.333, 0.333, 0.000, 0.333] | §3.2 | Equal over 3 nongoal states |
| After EAST (no goal): [0.100, 0.450, 0.000, 0.450] | §3.2 | One-step belief update |
| After 2nd EAST (no goal): [0.100, 0.164, 0.000, 0.736] | §3.2 | Two-step belief update |
| Optimal t-step value function is piecewise-linear and convex (PWLC) | §4.1 | Upper surface of α-vector linear functions |
| V_p(b) = b · α_p, with α_p = ⟨V_p(s_1),…,V_p(s_n)⟩ | §4.1 | Value of policy tree p at belief b |
| V_t(b) = max_{p∈P} b·α_p | §4.1 | Optimal t-step value = best policy tree |
| Exhaustive-enumeration superset size = |A||V_{t−1}|^{|Ω|} | §4.3 | Exponential in |Ω|; then pruned [42,58] |
| Witness algorithm run time polynomial in |S|,|A|,|Ω|,|V_{t−1}|,|Q_a^t| | §4.4 | Per-iteration complexity |
| Polynomial-in-|V_t| algorithm would settle "NP = RP?" | §4.4 | Complexity-theoretic barrier [34] |
| Q_a^t(b) = Σ_s b(s)R(s,a) + γ Σ_o Pr(o|a,b) V_{t−1}(b′_o) | §4.4 | Action-conditioned Q-function; V_t(b)=max_a Q_a^t(b) |
| Witness LP: maximize δ s.t. improvement + simplex constraints | §4.4.3, Alg.3 | Finds witness point; δ ≤ 0 means no improvement |
| Incremental pruning [67], generalized [7], empirically faster than witness | §4.5 | Zhang & Liu; Cassandra, Littman, Zhang |
| Cheng's linear support algorithm | §4.5 | Low-order poly for 2-state problems; corners exponential in higher dim |
| Infinite-horizon value function remains convex [63], may have infinitely many facets | §4.6 | Approximable by finite-horizon [51,59] |
| **Tiger problem:** states s_l, s_r; actions LEFT, RIGHT, LISTEN | §5.1 | Canonical POMDP example |
| Tiger reward +10 (correct door), penalty −100 (tiger door), listen cost −1 | §5.1 | Reward structure |
| LISTEN accuracy: correct observation w.p. 0.85 (TL/TR); wrong w.p. 0.15 | §5.1 | Observation model in state s_l/s_r |
| LEFT/RIGHT reset: transition to s_l w.p. 0.5, s_r w.p. 0.5; observations 0.5/0.5 | §5.1 | Door-opening resets problem |
| Expected reward for random door open = (−100+10)/2 = −45 | §5.2 | Why listening (value −1) beats guessing |
| t=1 optimal mapping: all three actions optimal for some belief | §5.2, Fig.10 | Open right if tiger likely left, etc. |
| t=2 and t=3 optimal mappings: LISTEN only (never open) | §5.2, Figs.11–12 | Because opening resets belief to (0.5,0.5) |
| t=2 value function has 5 linear regions / 5 policy trees | §5.2, Fig.12 | Multiple trees with same root action |
| t>3 mappings begin to open doors for some beliefs | §5.2, Fig.13 | Structure emerges at t=4 |
| Discounted tiger: stable structure appears at t=56, constant through t=105 | §5.3, Fig.14 | Vectors differ only after 15th decimal place |
| Tiger with LISTEN reliability reduced 0.85 → 0.65 needs larger plan graph | §5.4, Fig.18 | Must hear tiger 5× more on one side; more memory as reliability drops |
| Plan graph = finite-state controller | §5.4 | "keep listening until heard tiger twice more on one side than the other" |
| Witness impractical for |S|>15 and |Ω|>15 | §7 | Experimental limitation [34] |
| Solved 89-state, 16-observation hallway navigation via approximation | §7 | Function approximation + simulation [33] |
| Kalman filter [26] cited as continuous-space analog | Intro | Contrasted with discrete/multimodal belief |
| BURIDAN [30], C-BURIDAN [14] most closely related AI planning work | §6 | Probabilistic planning comparison |

---

## Scope & Limitations (as stated by the paper)

- **Enumerated (flat) state representation required.** "A weakness of the methods described in this paper is that they require the states of the world to be represented enumeratively, rather than through compositional representations such as Bayes nets or probabilistic operator descriptions" (§1). Factored/compact POMDP algorithms were only beginning to appear [6,14] with no proven speedup over flat representations (§6.6).
- **Finite state, action, and observation spaces**; static underlying dynamics assumed throughout the comparison (§6).
- **Exact algorithms scale poorly:** even the witness algorithm becomes impractical for |S|>15 and |Ω|>15 (§7).
- **Infinite-horizon exactness not guaranteed.** Exact finite-time solution possible only for POMDPs with *finitely transient* optimal policies; otherwise only approximate solutions are attainable and the sets V_t grow each iteration (§5.3).
- **No a priori bound on plan-graph (controller) size** in terms of problem size (§5.4).
- Some infinite-horizon POMDPs have **no finite-state optimal plan**; optimal behavior may require counting (stack machine), pushdown automata, or possibly Turing machines — "in the limit, a plan is actually a program" (§6.7).
- **Model assumed known.** The paper assumes a complete and correct model of world dynamics, observation model, and reward; model *acquisition/learning* is explicitly deferred to future work (§7).

## Does NOT claim / Boundaries

- Does **not** claim the witness algorithm is the only or fastest exact method; explicitly notes incremental pruning [7,67] is "empirically faster" (§4.5) and that Cheng's linear support can beat witness on some families (§4.4).
- Does **not** address learning the POMDP model from data (offered only as a future direction via HMM-learning extensions, Chrisman [11], McCallum [40,41]) (§7).
- Does **not** claim tractability in general — highlights the NP=RP barrier and the impracticality beyond small problems (§4.4, §7).
- Does **not** use factored/propositional representations; explicitly flat state space (§1, §6.6).
- Does **not** treat continuous state spaces in the base model (the only uncountable space introduced is the belief space, i.e., the belief MDP) (§2.1, §3.4).
- Does **not** claim information-gathering actions are a distinct action class — a key conceptual point is that there is **no distinction between actions to change the world and actions to gain information**; every action has both effects (§1, §3.2).

## Section Map

- **(Untitled intro paragraphs, pp. 99–100):** robot-navigation motivation; Kalman filter contrast; discrete/multimodal uncertainty.
- **§1 Introduction:** framing as planning under uncertainty; policies as situation→action mappings; two contributions; flat-representation weakness; unified treatment of world-changing vs. information-gathering actions.
- **§2 Markov decision processes:** 2.1 basic framework (⟨S,A,T,R⟩, Markov property); 2.2 acting optimally (horizons, discounting, stationary/nonstationary policies, value functions, greedy policy); 2.3 value iteration (Algorithm 1, Bellman error, convergence bounds).
- **§3 Partial observability:** 3.1 POMDP framework (⟨S,A,T,R,Ω,O⟩); 3.2 problem structure (SE + policy, belief state, sufficient statistic, 4-state example); 3.3 computing belief states (Bayesian update SE(b,a,o)); 3.4 finding an optimal policy (belief MDP).
- **§4 Value functions for POMDPs:** 4.1 policy trees (PWLC, α-vectors); 4.2 value functions as vector sets (domination, parsimonious representation, pruning); 4.3 one step of value iteration (exhaustive enumeration); 4.4 the witness algorithm (Algorithm 2, witness theorem, witness LP Algorithm 3, complexity); 4.5 alternative approaches (Sondik one-pass/two-pass, Cheng linear support, incremental pruning, White & Scherer); 4.6 the infinite horizon.
- **§5 Understanding policies:** 5.1 the tiger problem; 5.2 finite-horizon policies; 5.3 infinite-horizon policies; 5.4 plan graphs (finite-state controllers).
- **§6 Related work:** 6.1 imperfect knowledge; 6.2 initial state; 6.3 transition model; 6.4 observation model; 6.5 objective; 6.6 representation of problems; 6.7 plan structures.
- **§7 Extensions and conclusions:** scaling limits, function approximation, model acquisition.
- **Appendix A:** proof of the witness theorem (Theorem A.1).
- **References:** 69 entries.

---

*Digest based solely on the source PDF (36 pp.). No external claims consulted.*
