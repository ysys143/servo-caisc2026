# Digest: cranmer2020symbolic

**Full title:** Discovering Symbolic Models from Deep Learning with Inductive Biases
**Venue:** 34th Conference on Neural Information Processing Systems (NeurIPS 2020), Vancouver, Canada
**Preprint:** arXiv:2006.11287v2 [cs.LG], 18 Nov 2020
**Authors:** Miles Cranmer (Princeton), Alvaro Sanchez-Gonzalez (DeepMind), Peter Battaglia (DeepMind), Rui Xu (Princeton), Kyle Cranmer (NYU), David Spergel (Flatiron Inst. / Princeton), Shirley Ho (Flatiron / NYU / Princeton / CMU)
**Code:** https://github.com/MilesCranmer/symbolic_deep_learning

_(Digest built ONLY from this paper's PDF; extracted text at `results/_cranmer_fulltext.txt`.)_

---

## Thesis / Problem
Closed-form symbolic expressions are compact, interpretable, and generalize well, but finding them is hard: classical symbolic regression (genetic-algorithm brute force) scales exponentially with the number of input variables/operators and is intractable for high-dimensional problems. Deep learning handles high dimensions but yields uninterpretable black boxes that extrapolate poorly. The paper proposes a **general framework that combines both**: distill symbolic representations out of a trained deep model by imposing strong inductive biases, so that symbolic regression only has to operate on low-dimensional internal components.

## Method (IMPORTANT - directly answers the audit question)
**YES: it discovers symbolic models by FITTING EQUATIONS TO DATA - specifically by extracting symbolic expressions from the internal components of a trained Graph Neural Network via symbolic regression.** Four-step pipeline (Sec. 2):
1. Engineer a deep model with a **separable internal structure** giving a good inductive bias. For interacting particles they use **Graph Networks (GNs/GNNs)** [4], whose internals are three explicit learned functions: edge/"message" function phi^e, node function phi^v, global function phi^u (usually MLPs).
2. Train the GN **end-to-end** on data (supervised; predict acceleration, energy, or overdensity).
3. **Fit symbolic (closed-form analytic) expressions to the distinct internal functions** phi^e, phi^v, phi^u by recording their observed inputs/outputs over the training set and running symbolic regression on those (input -> output) samples.
4. **Replace** the learned functions with the fitted symbolic expressions, then refit constants a second time to remove accumulated approximation error.

Crucial enabler: **compact internal representations.** During training they regularize the messages to be low-dimensional (three strategies: hard **Bottleneck** = set message dim to 2/3; **L1** penalty; **KL** penalty toward a Gaussian prior). Compressing the latent/message space to the true dimensionality makes the messages become (linear transformations / rotations of) the true force vectors, which makes symbolic regression on them tractable. This "factorizes" a high-dimensional problem into small sub-problems, e.g. reducing a search over (10^9)^2 = 10^18 candidate equations to 2x10^9.

**Search is STOCHASTIC, NOT deterministic.** The symbolic regression engine is **eureqa** [2] (Schmidt & Lipson), which "works by using a genetic algorithm to combine algebraic expressions stochastically ... similar to natural selection, where the 'fitness' ... is defined in terms of simplicity and accuracy." Their own package **PySR** [27] (also genetic-algorithm based) is used for the success/failure table. Operators allowed: +, -, x, /, >, <, ^, exp, log, IF(.,.,.), plus real constants. Model selection uses an Occam's-razor score: maximize the fractional drop in MAE per unit complexity, -d log(MAE_c)/d c.

**Explicitly NOT a new symbolic-regression algorithm.** "this method is not a new symbolic regression technique by itself; rather, it is a way of extending any existing symbolic regression method to high-dimensional datasets by the use of a neural network with a well-motivated inductive bias." eureqa is interchangeable with other SR packages [27-36].

Extended/generalized version of the authors' earlier workshop paper [5] (Cranmer et al. 2019, "Learning Symbolic Physics with Graph Networks", arXiv:1909.05862).

---

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| NeurIPS 2020 (34th), Vancouver, Canada | p.1 footer | Publication venue |
| arXiv:2006.11287v2, 18 Nov 2020 | header | Preprint id/date |
| 4-step framework (engineer separable model -> train end-to-end -> fit symbolic exprs to internal functions -> replace) | Sec. 2, p.2 | Core method |
| GN internals = phi^e (edge/message), phi^v (node), phi^u (global) | Sec. 2, p.3 | Symbolic-regression targets |
| phi^e, phi^v, phi^u approximated by MLPs; two hidden layers, 300 hidden nodes each, ReLU | Sec. 2 / App. A | Architecture |
| Message dim L^e' = 100 (Standard & L1), 200 (KL), 2 or 3 (Bottleneck) | App. A.1 | Message sizes per strategy |
| 4 training strategies: Standard, Bottleneck, L1, KL | Sec. 4.1, p.6 | Compactness treatments |
| L1 regularization weight alpha1 = 10^-2 | Sec. 4.1 / App. A.1 | Message reg constant |
| Weight reg alpha2 = 10^-8 | App. A.1 | Network weight reg |
| KL prior mu=0, sigma=1; alpha1=1 (beta=1 VAE) | App. A.2 | KL-model spec |
| SR engine = eureqa [2]; genetic algorithm, stochastic | Sec. 2, p.3 | Symbolic regression tool |
| Alternative SR = PySR [27] (authors' package) | Sec. 2 / App. C | Used for success/fail table |
| Operators: +, -, x, /, >, <, ^, exp, log, IF(.,.,.), real constants | Sec. 2 / App. C | SR operator set |
| Occam score: maximize -d log(MAE_c)/d c | Sec. 4.1 / App. C | Model-selection criterion |
| High-dim factorization: (10^9)^2 = 10^18 -> 2x10^9 equations | Sec. 2, p.3-4 | Tractability argument |
| 6 force laws: 1/r, 1/r^2, charge (q1q2/r^2), damped spring, discontinuous, spring (r-1)^2 | Sec. 4.1 / App. B | Newtonian test forces |
| Simulations: 4 or 8 particles, 2D & 3D, 10,000 sims, 1000 time steps, adaptive RK4 | Sec. 4.1 / App. B | N-body dataset |
| Table 1: R^2 of message-vs-true-force fit; L1 highest (~1.000 several), Standard low (0.000-0.036) | Sec. 4.1, p.7 | Messages correlate with forces |
| Recovered spring 2D L1: phi^e1 ~ 1.36 dy + 0.60 dx - (0.60 dx+1.37 dy)/r - 0.0025 | Sec. 4.1, p.7 | Example extracted force law |
| Recovered 1/r^2 3D bottleneck: phi^e1 ~ (0.021 dx m2 - 0.077 dy m2)/r^3 | Sec. 4.1, p.7 | Example extracted force law |
| Recovered discontinuous 2D L1: phi^e1 ~ IF(r>2, 0.15r dy+0.19r dx, 0) - 0.038 | Sec. 4.1, p.7 | Example extracted force law |
| Hamiltonian model = "FlatHGN" (Flattened Hamiltonian Graph Network) | Sec. 3 / 4.2 / App. A.4 | H = sum H_self + sum H_pair |
| FlatHGN built on HGN [46] = Hamiltonian NN [47,48] + GN; similar to Lagrangian GN [49] and [50] | Sec. 3 / App. A.4 | Provenance of variant |
| Extracted charge potential: H_pair ~ 0.0019 q1q2 / r | Sec. 4.2 / App. C | Recovered Hamiltonian term |
| FlatHGN message dim = 1 (scalar), no reg needed | Sec. 4.2 | By-design constraint |
| Cosmology data = Quijote simulations [51] | Sec. 4.3 | Dark matter dataset source |
| Zeroth sim, final timestep (present day), 215,854 dark matter halos | Sec. 4.3, p.8 | Cosmology subset |
| Connect halos within 50 distance units -> 30,437,218 directional edges, 71 neighbors/halo avg | Sec. 4.3, p.8 | Graph construction |
| 1 distance unit ~ 3 million light years | Sec. 4.3 | Scale |
| Cosmology GN: 500 hidden units, L1 reg scale 10^-2, 100 message dims | Sec. 4.3 / App. E | Cosmology hyperparams |
| Discovered message vector space is 1-dimensional (1 comp sigma~10^-2, other 99 <10^-8) | App. E, p.24 | Learned latent dimensionality |
| Overdensity delta = (rho - <rho>)/<rho> | Sec. 4.3 | Prediction target |
| Table 2 losses <\|delta-delta_hat\|>: Constant 0.421; Simple/Traditional 0.121/0.120; Best-without-mass 0.120; **Best-with-mass 0.0882** | Sec. 4.3, p.8 | Formula comparison |
| Hand-designed formula loss 0.121 vs discovered 0.0882 | Sec. 4.3, p.8 | New formula beats hand-designed |
| Dark matter ~ 85% of total matter in Universe [54,55] | Sec. 4.3 | Cosmology context |
| Symbolic generalization test: mask 20% (halos delta_i>1) | Sec. 4.3, p.9 | OOD experiment |
| GN error: train 0.0634, OOD 0.142 | Sec. 4.3, p.9 | GN degrades OOD |
| Symbolic expr error: train 0.0811, OOD **0.0892** | Sec. 4.3, p.9 | Symbolic generalizes far better OOD |
| Tools: PyTorch [43], PyTorch Geometric [44], Adam [45] | Sec. 2 (Implementation) | Frameworks |
| Python packages: numpy, scipy, sklearn, jupyter, matplotlib, pandas, torch, tensorflow, jax, torch_geometric | Acknowledgments | Stack |
| Table 5: force-law recovery success/fail - Bottleneck all pass; L1 mostly pass (fails Charge); Standard all fail; KL mixed | App. C | Reconstruction reliability |
| 65 references | pp.10-14 | Bibliography size |
| Marcus [57] cited re: combining neural nets + symbolic priors | Sec. 4.3 | "next decade in AI" reference |

---

## Scope & Limitations
- Domain: **interacting particle systems / physics** (Newtonian dynamics, Hamiltonian dynamics, cosmological dark-matter halos). Method presented as general but demonstrated only on GNs for these physics-style problems.
- Reconstruction **does not always succeed** - fails for strategies (e.g. Standard, some KL) that can't find compact right-dimensional representations. Two failed-example extractions shown (Spring 3D KL; 1/r 3D Standard). Authors "do not attempt to make any general statements about when symbolic regression ... will fail or succeed."
- Requires **known/engineered inductive bias** and a **separable** internal structure; needs the true latent dimensionality to be low (or discoverable via sparsity).
- eureqa hyperparameters are opaque/untunable; switched to PySR for controlled experiments (equations equivalent given enough time).
- Cosmology formula's novel terms are "less clear"; detailed physical interpretation deferred to a future astrophysics study.

## Does NOT claim / boundaries (important for citation accuracy)
- **Not a new symbolic-regression algorithm** - it extends existing SR (eureqa/PySR) to high-dim data via a neural factorization.
- **Not a deterministic search** - SR is a stochastic genetic algorithm.
- **No LLM, no autonomous agent, no automated hypothesis-generation loop, no experiment execution.** It is a supervised deep-learning + symbolic-regression distillation pipeline run by researchers.
- The Newtonian-mechanics analogy in Fig. 2 is "purely for explanatory purposes, ... not explicit"; messages can be high-dimensional and nodes need not be physical particles.
- Does not claim to replace GNNs generally; the GN provides the factorization that makes SR feasible.
- Symbolic-regression-of-PDEs packages [37-42] are noted as related but **not used** ("not applicable to our use-cases").

## Section Map
- **1 Introduction** - motivation (symbolic vs deep learning trade-offs), Wigner epigraph.
- **2 Framework** - 4-step pipeline; GN internals (phi^e, phi^v, phi^u); symbolic regression via eureqa; compact/regularized representations; high-dim factorization argument; implementation (PyTorch/PyG/Adam).
- **3 Case studies** - Newtonian dynamics; Hamiltonian dynamics (FlatHGN); dark-matter halos (cosmology).
- **4 Experiments & results** - 4.1 Newtonian (recover force laws, Tables 1 & 3); 4.2 Hamiltonian (recover potentials); 4.3 Cosmology (new dark-matter overdensity formula, Table 2; OOD symbolic generalization).
- **5 Conclusion.**
- **Appendices A-E** - A model/GN implementation & math of message=force; B simulations; C symbolic-regression details, Tables 4-5, pure-eureqa baseline; D video/code; E cosmological experiments, Table 6 best-fit params.
