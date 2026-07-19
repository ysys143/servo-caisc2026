# Digest: foster2021dad

**Title:** Deep Adaptive Design: Amortizing Sequential Bayesian Experimental Design
**Authors:** Adam Foster*, Desi R. Ivanova*, Ilyas Malik, Tom Rainforth (*equal contribution; Dept. of Statistics, University of Oxford)
**Venue:** ICML 2021 (Proceedings of the 38th ICML, PMLR 139, 2021)
**Identifier:** arXiv:2103.02438v2 [stat.ML], 11 Jun 2021
**Code:** https://github.com/ae-foster/dad
(Base ONLY on this paper.)

---

## Thesis / Problem

Sequential Bayesian optimal experimental design (BOED) lets you adaptively pick each design ξ_t using data gathered from previous steps, maximizing expected information gain (EIG) about latent parameters θ. But the conventional iterative approach requires, **at each step of the live experiment**, (a) re-fitting the posterior p(θ|ξ_{1:t-1}, y_{1:t-1}) and (b) optimizing a **doubly intractable** EIG objective. This is too slow for real-world settings where decisions must be made quickly (e.g. adaptive surveys with a live human participant). DAD's problem: eliminate that per-step runtime cost so adaptive BOED can run in real time.

## Method — IS DAD AN AMORTIZED SEQUENTIAL BED POLICY? → YES, unambiguously.

- **Amortized:** Yes. DAD pays a large **upfront (offline) training cost** to learn a **design network πφ**, then at deployment each design is a **single forward pass** (design decisions "in milliseconds"). This is explicitly framed as amortization, analogous to amortized inference (Stuhlmüller 2013; Cremer 2018 amortization gap). Amortization also shares computation across many repeated deployments of the same experimental framework (e.g. many survey participants).
- **Sequential BED:** Yes. It targets sequential/adaptive BOED (a sequence of designs ξ_1…ξ_T using past outcomes).
- **Learned design POLICY network:** Yes, central. Section 3 introduces a **design function / policy π** mapping the set of all previous design–observation pairs (history h_{t-1}) to the next design ξ_t. DAD represents π ∗ with a neural network πφ (Section 4). Crucially, it **optimizes the policy parameters φ, not individual designs**. Section 4.3 architecture: πφ(h_t) = Fφ2(R(h_t)) where R(h_t)=Σ_k Eφ1(ξ_k,y_k) is a permutation-invariant pooled representation of the history (Theorem 3 permutation invariance → weight sharing across time steps).
- **Amortized EIG / amortized design objective:** Yes. Reformulates sequential BOED from its iterative per-step form into **a single holistic objective** I_T(π) = the total EIG = mutual info between θ and the full history rollout h_T (Theorem 1: total EIG = sum of conditional EIGs = E[log p(h_T|θ,π) − log p(h_T|π)]). This is a function of the **policy**, with designs now random variables. It then derives **contrastive lower/upper bounds** on this objective trainable end-to-end by stochastic gradient ascent — **sequential PCE (sPCE)** lower bound L_T(π,L) and **sequential Nested Monte Carlo (sNMC)** upper bound U_T(π,L), both tightening as L→∞ at rate O(L⁻¹). Training uses these bounds directly, **sidestepping posterior inference AND intermediate EIG estimation entirely** (builds on the PCE bound of Foster et al. 2020).
- **Real-time adaptive design:** Yes — the explicit motivating claim. "the first approach to allow adaptive BOED to be run in real-time for general problems."
- **Non-myopic:** Yes — a highlighted benefit. Because the policy optimizes total EIG over the whole horizon, it learns **non-myopic** strategies that account for their own future decisions, unlike conventional per-step (myopic) πs.

### Fixed vs. open-ended hypothesis spaces
DAD operates in a **FIXED / closed hypothesis space**, NOT open-ended hypothesis discovery. Setup requires: an explicit parametric likelihood p(y|θ,ξ), a fixed prior p(θ), and a fixed set of latent parameters θ "we wish to learn about." The method learns *where/how to sample* (designs) to reduce uncertainty about a **pre-specified** θ; it never generates, proposes, or searches over new hypotheses/models. It does NOT address open-ended hypothesis spaces or hypothesis generation. (In location finding, even the number of sources K is assumed known.)

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| arXiv:2103.02438v2 [stat.ML], 11 Jun 2021 | Header (p.1) | Version/date |
| ICML 2021, PMLR 139 | p.1 footer | Venue |
| 4 authors (Foster, Ivanova, Malik, Rainforth); Foster & Ivanova equal contribution | p.1 | Authorship, all Oxford |
| Eq (1): I(ξ)=E[log p(y|θ,ξ) − log p(y|ξ)] | §1 | EIG = mutual info between y and θ |
| DAD design decisions made "in milliseconds" via single forward pass | Abstract, §1, §4 | Core speed claim |
| Applications cited: psychology, bioinformatics, pharmacology, physics (survey, epidemiology, clinical trials) | §1, §7 | Motivation domains |
| Theorem 1: total EIG I_T(π)=E[log p(h_T|θ,π) − log p(h_T|π)] | §3 (proof App A) | Holistic policy objective |
| sPCE lower bound L_T(π,L), Theorem 2, ↑ I_T(π) at rate O(L⁻¹) | §4.1 (Eq 11) | Training objective |
| sNMC upper bound U_T(π,L), Theorem 4, ↓ I_T(π) at rate O(1/L) | §4.1 (Eq 13), App A | Evaluation bound |
| g bounded by log(L+1); f potentially unbounded | §4.1, App A | Why lower bound used for training |
| Gradient estimators: reparameterized (Eq 14), complete enumeration (Eq 15, cost O(|Y|^T)), score function/REINFORCE (Eq 16) | §4.2 | Three gradient schemes |
| Theorem 3: permutation invariance of optimal policy | §4.3 (proof App A) | Justifies pooled architecture |
| R(h_t)=Σ_k Eφ1(ξ_k,y_k); πφ(h_t)=Fφ2(R(h_t)); φ={φ1,φ2} | §4.3 (Eq 17) | Encoder-pool-emitter architecture |
| Implemented in PyTorch + Pyro | §6, App D | Frameworks |
| **Location finding:** T=30 experiments, K=2 sources, R^2, inverse-square attenuation | §6.1 | Experiment 1 |
| Table 1 (I30 EIG, L30/U30): Random 8.303±0.043 / 8.322±0.045; Fixed 8.838±0.039 / 8.914±0.038; **DAD 10.926±0.036 / 12.382±0.095**; Variational 8.776±0.143 / 9.064±0.187 | Table 1, §6.1 | DAD best; errors over 256 (variational) / 2048 (others) rollouts |
| DAD deployment: **0.0474±0.0003 s** for all 30 decisions on lightweight CPU vs **8963 s** for variational | §6.1 | ~190,000× faster than variational adaptive |
| Training stability: 16 DAD networks → lower bound 10.91±0.014, upper 12.47±0.046 | §6.1 | Low variance across seeds |
| DAD pretrained T=30 generalizes to T'≠30 (25–35); fixed cannot exceed training length | Fig 2, §6.1 | Design-horizon robustness |
| Location-finding deployment times (App D): Random 0.0026±0.0001; Fixed 0.0018±0.0001; DAD 0.0474±0.0003; Variational 8963.2±42.2 s | App D.1 table | Full timing |
| **Hyperbolic temporal discounting:** T=20, binary Q "£R today or £100 in D days", ξ=(R,D) | §6.2 | Experiment 2 (psychology) |
| Table 2 deployment (T=20 questions): Frye 0.0902±0.0003; Kirby N/A; Fixed N/A; DAD 0.0901±0.0007; Badapted 25.2679±0.1854 (s) | Table 2 | DAD total design time <0.1 s |
| Table 3 bounds (L=5000): Frye 3.500±0.029 / 3.513±0.029; Kirby 1.861±0.008 / 1.864±0.009; Fixed 2.518±0.007 / 2.524±0.007; **DAD 5.021±0.013 / 5.123±0.015**; Badapted 4.454±0.016 / 4.536±0.018 | Table 3 | DAD best, beats bespoke Badapted |
| Baselines HTD: Kirby (2009) human fixed set; Frye et al. (2016) problem-specific adaptive; Badapted = Vincent & Rainforth (2017) PMC + bandit | §6.2 | Comparators |
| **Death process:** epidemiology, infection rate θ, T=4, independent stochastic process per step | §6.3 | Experiment 3 |
| Table 4: Fixed dep N/A, I_T 2.023±0.007; DAD dep 0.0051±12% s, I_T 2.113±0.008; Variational dep 1935.0±2% s, I_T 2.076±0.034; SeqBED* dep 25911.0 s, I_T 1.590 | Table 4 | DAD deploys <0.01 s; SeqBED takes hours |
| Death-process rollout counts: 10,000 (fixed & DAD), 500 (variational), 1 (SeqBED*) | Table 4 caption | Sampling budget |
| Single rollout θ=1.5 fixed: SeqBED 1.590, Variational 1.719, Fixed 1.678, DAD 1.779 (info gain) | §6.3 | DAD highest |
| SeqBED = Kleinegesse et al. (2020) adaptive baseline | §6.3 | Comparator |
| **Non-myopia demo:** 1D location finding, 1 source, T=2, prior θ~N(0,1); myopic ξ1=0, DAD ξ1≈−0.4 | §7, Fig 4 | DAD sacrifices step-1 EIG for better total EIG |
| Breakpoint footnote: myopic places 1st at 1/2 then 1/4 or 3/4; optimal is 1/3 and 2/3 | §3 footnote 1 | Intuition for non-myopia |
| Table 5 ablation (T=10, 2^10=1024 histories, L=5000): Complete enumeration 4.068±0.0124 / 4.090±0.0126; Score function 4.037±0.0126 / 4.058±0.0128 | App D.2.1 | Two gradient estimators statistically equal |
| Location-finding hyperparams: K=2, b=10⁻¹, m=10⁻⁴, α1=α2=1, σ=0.5; prior θk~N(0_d,I_d); log y~N(log µ(θ,ξ),σ) | App D.1 | Model spec |
| LF training: L=2000 inner, 2000 outer, lr 5×10⁻⁵, betas (0.8,0.998), γ=0.98, 50000 grad steps; eval L=5×10⁵ | App D.1 | Adam, exp LR annealing |
| Death-process model: θ~TruncatedNormal(µ=1,σ=1,min=0,max=∞); η=1−exp(−ξθ); y~Binomial(N=50,η) | App D.3 | Settings from Kleinegesse et al. (2020) |
| HTD priors: log k~N(−4.25,1.5), α~HalfNormal(0,2); V1=100/(1+kD); ε=0.01 | App D.2 | Model spec |
| sACE lower bound & sVNMC upper bound (Theorem 5, uses proposal q(θ;h_T)) | App B | More general bounds for fixed L |
| PCE bound origin: Foster et al. (2020), "unified stochastic gradient" SG-BOED | §2.2, §5 | Prior work built on |

## Scope & Limitations (stated by paper)

Explicit limitations (§7 "Limitations and Future Work"):
1. Requires an **explicit likelihood** model — density p(y_t|θ,ξ_t) must be evaluable (cannot handle implicit/simulator-only likelihoods, unlike SeqBED).
2. Requires experiments to be **conditionally independent given θ**: p(y_{1:T}|θ,ξ_{1:T})=Π p(y_t|θ,ξ_t). Fails for e.g. time-series models.
3. Requires **continuous designs** ξ_t for gradient-based optimization.
- Complete-enumeration gradient (Eq 15) only feasible when both T and |Y| are small (cost O(|Y|^T)).
- Notes a link to model-based RL (Sekar et al. 2020) but DAD is distinct (e.g. no observed rewards) — flagged as future work.

## Does NOT claim / boundaries

- Does NOT do hypothesis generation, model discovery, or search over open-ended hypothesis/model spaces — θ and the model are fixed and pre-specified (closed hypothesis space).
- Does NOT eliminate the upfront training cost — it *shifts* cost offline; only the *deployment* cost is near-zero.
- Does NOT handle implicit-likelihood models, non-conditionally-independent experiments, or discrete designs in its present form.
- Does NOT claim optimality — πφ *approximates* the optimal policy π∗ via lower-bound maximization.
- Not an LLM/agent method; no autonomous scientific-discovery or lab-automation framing — pure statistical ML methodology.

## Section Map

- §1 Introduction — motivation, amortization idea, contributions (survey example).
- §2 Background — 2.1 conventional adaptive BOED (per-step posterior + EIG, Eq 3, doubly intractable); 2.2 contrastive info bounds (PCE, Eq 4; Foster et al. 2020).
- §3 Rethinking Sequential BOED — design policy π; Theorem 1 (total EIG as policy functional).
- §4 Deep Adaptive Design — 4.1 sequential contrastive bounds (sPCE/sNMC, Theorems 2 & 4); 4.2 gradient estimation (reparam, enumeration, score/REINFORCE); 4.3 architecture (Theorem 3 permutation invariance, pooling).
- §5 Related Work — sequential BOED inference/estimation/optimization methods; simultaneous estimate+optimize; non-myopic prior work.
- §6 Experiments — 6.1 location finding 2D; 6.2 hyperbolic temporal discounting; 6.3 death process.
- §7 Discussion — why DAD beats non-amortized methods (posterior-free + non-myopic), non-myopia demo, limitations, conclusions.
- Appendices — A proofs; B additional bounds (sACE/sVNMC); C gradient details (score function, expanded reparam); D experiment details + D.2.1 enumeration ablation.
