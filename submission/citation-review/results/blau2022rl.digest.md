# Digest: blau2022rl (BLIND first-pass reading)

**Title:** Optimizing Sequential Experimental Design with Deep Reinforcement Learning
**Authors:** Tom Blau, Edwin V. Bonilla, Iadine Chades, Amir Dezfouli (CSIRO's Data61; CSIRO's Land and Water, Australia)
**Venue:** ICML 2022 (Proceedings of the 39th ICML, PMLR 162, 2022). arXiv:2202.00821v3, 17 Jun 2022.
**Source read:** full main body + appendices A–F (22 pp).

---

## Thesis / Problem

Bayesian optimal experimental design (BOED) casts experiment design as maximizing **expected information gain (EIG)** — the expected reduction in entropy from prior to posterior over model parameters θ. Doing this **non-myopically** over a budget of T experiments requires nested expectations whose cost/error explodes with T, and is intractable by direct estimation.

Recent **amortized** methods (notably Deep Adaptive Design, DAD, Foster et al. 2021) train a design policy that maps history → next design by maximizing a lower bound (SPCE) on total EIG. But DAD (a) backpropagates gradients through the policy so it **requires a differentiable probabilistic model**, (b) works only on **continuous design spaces**, and (c) is a **pure-exploitation** deterministic policy that may under-explore.

**This paper's contribution:** reduce the policy-optimization problem to solving a **Markov decision process (MDP)** — specifically a Hidden-Parameter MDP (HIP-MDP) — and solve it with **modern deep reinforcement learning**. Because RL exploits the Policy Gradient Theorem, the EIG objective need not be differentiable; RL also handles discrete action spaces and brings built-in exploration (stochastic policies, entropy regularization).

## Method — IMPORTANT confirmation: "RL for EIG/BOED"

**YES — this paper uses reinforcement learning to optimize the design policy for Bayesian optimal experimental design, and the RL return is constructed to equal a lower bound on the expected information gain (EIG).**

Mechanics:
- The total EIG of a policy π, EIG_T(π), is lower-bounded by the **sequential prior contrastive estimation (SPCE)** bound (Eq. 6), building on the single-experiment **PCE** bound of Foster et al. (2020).
- They formulate SED as a **HIP-MDP** (Doshi-Velez & Konidaris 2016): states are history summaries, actions are designs, θ is the hidden parameter drawn once per episode from the prior p(θ), and the reward is a factorization of the SPCE integrand g(θ,h_t).
- **Theorem 1** (naive/sparse variant): terminal-only reward R = g(θ,h_T) at t=T, 0 otherwise, γ=1 ⇒ expected return J(π) = SPCE(π,L,T).
- **Theorem 2** (main result, dense reward, Eq. 13): a per-step factorized reward assigns each experiment its marginal contribution to the final EIG; sum of rewards over any prefix = g(θ,h_t). γ=1 ⇒ J(π) = SPCE(π,L,T). This gives a dense (non-sparse) learning signal and a Markovian state via a permutation-invariant history summary B_ψ (encoder inherited from Foster et al. 2021).
- **Theorem 3** (App. A.3): the Q-function can be learned from **prior samples only** (roll out policy, draw θ from prior), without inferring posteriors.
- Solving the MDP: **REDQ (Randomized Ensembled Double Q-learning, Chen et al. 2021)** trains all policies (a generalization of Soft Actor-Critic with an ensemble of N critics). Implemented in **Pyro** (Bingham et al. 2018) and **Garage** (Garage Contributors 2019). Code: https://github.com/csiro-mlai/RL-BOED.
- Ablation **NAIVE-RL** = Theorem-1 sparse reward with same policy architecture, isolating the effect of the dense reward factorization.

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| d* = argmax_d E_p(y\|d)[H(p(θ)) − H(p(θ\|y,d))] | Eq. 1–2, §1–2 | Definition of EIG-maximizing optimal design |
| Nesting depth grows O(T); nested-MC convergence rate O(n^{−1/(T+1)}) | §1 (p.1–2), cites Rainforth et al. 2018 | Why non-myopic BOED by direct estimation is intractable |
| BOED attributed to Lindley, 1956 | §1 | Origin of the formalism |
| PCE lower bound (Eq. 3) attributed to Foster et al. (2020) | §2 | Single-experiment contrastive EIG bound |
| SPCE lower bound (Eq. 6); DAD = maximizing SPCE via SGD | §2.1, cites Foster et al. 2021 | Sequential bound; DAD defined |
| J(π) = SPCE(π,L,T) | Thms 1 (Eq. 11), 2 (Eq. 16) | RL return equals the SPCE lower bound on total EIG |
| HIP-MDP tuple ⟨S,A,Θ,T,R,γ,ρ0,PΘ⟩ | §3.1, cites Doshi-Velez & Konidaris 2016 | Framework used because θ is hidden/unobservable at test time |
| REDQ (Chen et al. 2021) used to train ALL policies | §4, App. C.1 | RL algorithm; generalization of Soft Actor-Critic |
| Frameworks: Pyro (Bingham et al. 2018), Garage (Garage Contributors 2019) | §4 | Implementation |
| **Source location:** 2 signal sources in 2-D plane; design = 2-D sample coordinate | §4.1.1, App. B.1 | Continuous problem, budget **30** experiments; from Foster et al. 2021 |
| Source-location EIG estimated with SPCE, L=1e6 | Fig. 1, Table 1 | 2000 rollouts (RL, DAD), 1000 (VPCE, random) |
| **Table 1 (EIG @ t=30, lower/upper):** Random 1.624±0.053 / 1.639±0.057; VPCE 7.766±0.069 / 7.802±0.072; DAD 10.965±0.041 / 12.380±0.086; RL 11.73±0.040 / 12.362±0.062; NAIVE-RL 9.789±0.045 / 9.898±0.049 | Table 1 | Upper bound via SNMC. RL best lower bound; RL≈DAD on upper bound |
| RL's 2000 rollouts split among 10 agents, each own random seed | §4.1.1 | RL is seed-sensitive |
| **CES:** compare 2 baskets, rate 0–1; latents (ρ,α,u); design space **6-dimensional** | §4.1.2, App. B.2 | Continuous behavioral-economics problem; budget **10**; from Foster et al. 2020 |
| CES EIG estimated with SPCE, L=1e7 | Fig. 2, Table 2 | — |
| **Table 2 (EIG @ t=10, lower/upper):** Random 8.099±0.153 / 16.451±0.685; VPCE 9.547±0.137 / 24.396±2.024; DAD 10.774±0.077 / 13.374±0.150; RL 13.965±0.064 / 17.794±0.226; NAIVE-RL 12.131±0.058 / 15.641±0.166 | Table 2 | RL lower bound > DAD upper bound |
| CES design box-plots: DAD proposes narrow near-center designs; RL proposes across whole space | Fig. 3 | Evidence RL explores more; 6 design elements, 2000 rollouts |
| **Prey population:** control initial prey pop, measure # consumed after **24 h**; estimate attack rate + handling time | §4.2, App. B.3 | **Discrete** problem, design N0∈[1,300]; budget **10**; from Moffat et al. 2020 |
| Prey EIG estimated with SPCE, L=1e6 | Fig. 4, Table 3 | 2000 (RL), 1000 (VPCE, random), 500 (SMC) rollouts |
| **Table 3 (EIG @ t=10, lower/upper):** Random 3.923±0.042 / 3.925±0.043; VPCE 4.396±0.046 / 4.42±0.050; SMC 4.521±0.065 / 4.523±0.063; RL 4.456±0.032 / 4.459±0.033; NAIVE-RL 4.375±0.032 / 4.376±0.032 | Table 3 | SMC–RL lower-bound gap < std error; relative effect size ~1% |
| **Table 4 deployment time (s), 100 replications** — CES: Random 2.37e-5±1.51e-7; VPCE 146.944±1.397; PCE-BO 23.830±0.771; DAD 1.25e-4±3.37e-7; RL 1.35e-3±4.18e-6. Prey: Random 1.29e-4±4.94e-7; VPCE 20.550±1.893; SMC 81.252±4.310; RL 1.50e-3±3.23e-6 | Table 4 | RL orders of magnitude faster than SMC/VPCE; ≈DAD (both a NN forward pass) |
| Non-differentiable CES: run under pytorch `no_grad`; DAD & VPCE fail (need gradients); VPCE replaced by PCE-BO (Bayesian opt of myopic PCE) | §4.4, Fig. 5 | RL outperforms all gradient-free baselines; RL results ≈ Fig. 2 (same seeds) |
| RL hyperparams (App. C.1): Source N=2,M=2, iters 2e4, contrastive 1e5, T=30, γ=0.9, τ=1e-3, LRπ=1e-4, LRqf=3e-4, buffer 1e7 | Table, App. C.1 | — |
| CES: N=2,M=2, iters 2e4, contrastive 1e5, T=10, γ=0.9, τ=5e-3, LRπ=3e-4, LRqf=3e-4, buffer 1e6 | App. C.1 | — |
| Prey: N=10,M=2, iters 4e4, contrastive 1e4, T=10, γ=0.95, τ=1e-2, LRπ=1e-4, LRqf=1e-3, buffer 1e6 | App. C.1 | — |
| **Empirically chose γ≠1** despite theorems requiring γ=1 (γ=1 needed for J(π)=SPCE equality) | App. C.1 note | γ∈{0.9,0.95} used in practice for better performance |
| Summary net B_ψ: 2 FC layers ×128 ReLU + 64-unit linear output; policy net outputs Tanh-Gaussian (cont.) or Gumbel-Softmax logits (discrete) | App. C.1 | Architecture |
| Hardware: Slurm node, 1× Nvidia Tesla P100 GPU, 4 cores Intel Xeon E5-2690; SMC on CPU (R code) | App. D | — |
| Non-myopic check: simplified source location d=1,k=1,T=2; myopic (γ=0) vs non-myopic (γ=1) agents; 1e5 rollouts, L=1e4 | App. E, Fig. 6 | Non-myopic agent sacrifices early EIG for higher EIG at t=T; from Foster et al. 2021 setup |
| Claim: "to the best of our knowledge, this is the first work that makes generic RL algorithms applicable for optimal design of experiments" | §5 Related Work | Nearest prior: Huan & Marzouk 2016; Shen & Huan 2021 (specific dynamic-programming, needs explicit posteriors on discretized grid) |

## Scope & Limitations
- Three benchmark problems only (source location, CES, prey population); 2 continuous + 1 discrete.
- On the **discrete** prey problem RL does **not** beat myopic baselines (SMC/VPCE) — it matches them (within error bars); authors note it "does not outperform" despite having non-myopic capability, and offer candidate explanations (myopic baselines use explicit posteriors; possible representation-learning degradation; possibly small myopic/non-myopic optimality gap — unknown, no theoretical bounds).
- RL is noted to be **highly sensitive to random seed** (mitigated by 10-agent averaging).
- Theorems require γ=1, but practice uses γ<1 (a pragmatic deviation).
- Both amortized methods (RL, DAD) are trained to maximize the **lower** bound, not the upper bound.

## Does NOT claim / boundaries
- Does NOT claim to beat all baselines on discrete problems (explicitly matches, not exceeds).
- Does NOT provide theoretical optimality/regret bounds for the learned policy vs true non-myopic optimum.
- Does NOT introduce a new EIG estimator — it reuses SPCE/PCE/SNMC from Foster et al. (2019/2020/2021).
- Not about LLMs, autonomous "AI scientists," symbolic regression, materials discovery, or chemistry — this is a methods paper on RL-based BOED / sequential experimental design policy learning.
- Deployment-time cost is a forward pass (fast); the RL training cost is offline and not framed as cheap.

## Section map
- §1 Introduction (BOED, EIG, intractability of non-myopic design, amortization/DAD limits, contribution).
- §2 Background (BOED, EIG Eq. 2, PCE Eq. 3; §2.1 SED + SPCE + DAD; §2.2 RL/MDP).
- §3 RL for Sequential Experiment Design (§3.1 HIP-MDPs + Thm 1; §3.2 the SED MDP + dense reward Eq. 13 + Thm 2; §3.3 advantages incl. discrete/black-box + exploration).
- §4 Experimental Results (§4.1 continuous: source location, CES; §4.2 discrete: prey population; §4.3 deployment-time benefits; §4.4 non-differentiable likelihood).
- §5 Related Work. §6 Discussion.
- Appendices: A proofs (Thms 1–3), B experiment details, C algorithm/hyperparameters, D hardware, E non-myopic solutions, F learning curves.
