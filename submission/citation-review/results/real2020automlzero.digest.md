# Digest: real2020automlzero (BLIND first-pass)

**Full title:** AutoML-Zero: Evolving Machine Learning Algorithms From Scratch
**Authors:** Esteban Real*, Chen Liang*, David R. So, Quoc V. Le (*equal contribution). Google Brain / Google Research, Mountain View, CA.
**Venue:** Proceedings of the 37th International Conference on Machine Learning (ICML), Vienna, PMLR 119, 2020. (arXiv:2003.03384v2, 30 Jun 2020). 23 pages incl. supplement.
**Source PDF:** ai_scientist/2_Domain_Applications/CS/AutoML-Zero - Evolving Machine Learning Algorithms From Scratch.pdf

---

## Thesis / Problem
Prior AutoML progress (esp. neural architecture search) relies on **constrained search spaces built from sophisticated, expert-designed layers/components**, which (a) bias results toward human-designed algorithms, and (b) impose a design burden that undermines AutoML's goal of saving human time. The paper's goal: show it is possible **today** to automatically discover **complete ML algorithms** — model, optimization, initialization, etc. — using **only basic mathematical operations** as building blocks (no ML-specific primitives, no derivatives, no assumption that a neural network or gradients even exist). They call this **AutoML-Zero** (spirit of "minimal human participation," cf. AlphaZero/Silver et al. 2017). Framed explicitly as **preliminary / a promising new direction**, not a finished product.

## Method — direct answers to the audit questions
- **Evolutionary search (evolving ML algorithms from basic operations)? YES, central.** The main search method is **regularized evolution** (Real et al. 2019) with **tournament selection** (Goldberg & Deb 1991): keep a population of P algorithms (initially empty), each cycle pick T<P at random, select best as parent, copy + mutate to child, remove oldest. Three mutation types: (i) insert/remove a random instruction, (ii) randomize a whole component function, (iii) modify one argument. Algorithms = programs with three component functions **Setup / Predict / Learn** operating on scalar/vector/matrix memory, using a vocabulary of **65 ops** (Suppl. Table S1) chosen to be "high-school level" math — deliberately **excluding ML concepts, matrix decompositions, and derivatives**, so any gradient/backprop must itself be evolved. Random search (RS) used only as a **baseline**; paper explicitly moves away from RS because the space is sparse.
- **Closes a loop via reliable BENCHMARK / EMPIRICAL validation? YES.** Quality of each algorithm is measured **empirically**: candidate algorithms evaluated by **accuracy on held-out tasks** (median accuracy across tasks during search; model selection on Tselect; final report on held-out **CIFAR-10 test set** with **5 random seeds**, mean ± std). Generalization checked on **SVHN, downsampled ImageNet, Fashion-MNIST**. Findings backed by **statistical-significance testing** (p-values), **30-repeat experiments with controls**, and **ablation / knock-out / knock-in** studies. This is high-reliability empirical validation (measured accuracy on real image-classification benchmarks), not proxy/self-judged.
- **Interpretability a noted limitation? YES — explicitly.** (1) They position **symbolic** discovery as *more* interpretable/transferable than **numerically** learned optimizers ("a set of coefficients ... hard to interpret"). BUT (2) they candidly report that **interpreting the evolved algorithms "required effort due to the complexity of their raw code"** (Sec. 5 / Suppl. S8) — needing automatic static-analysis simplification, hunting for motifs that recur across runs, then ablations/knock-outs to confirm. (3) **Hyperparameter coupling**: e.g. evolution sets `s7 = v2·v2` because it coincidentally yields a good hyperparameter value; requires **time-consuming manual decoupling / manual inspection** (Suppl. S7). So interpretability is presented as a comparative advantage of symbolic search yet still a real, labor-intensive limitation.

---

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| 65 ops | Sec 3.1 / Suppl. S2, Table S1 | Full op vocabulary in search space (high-school math, no calculus/derivatives) |
| 3 component functions (Setup, Predict, Learn) | Abstract/Sec 3.1 | Program representation of an ML algorithm |
| ~1 in 10^12 | Sec 1 | Rarity of a good algorithm to learn even a trivial task (space sparsity) |
| 10,000 models/second/cpu core | Sec 1 | Throughput of their open-source infra |
| 2k–10k algorithms/second/cpu core | Sec 3.2 | Search throughput with proxy tasks + upgrades |
| 4x speedup | Sec 1 / 3.2 | From Functional Equivalence Checking (FEC) |
| 5x throughput | Sec 3.2 | From hurdles (So et al. 2019) |
| 10 train + 10 validation steps | Sec 3.2 / Suppl. S3 | Steps used to fingerprint an algorithm for FEC |
| 20 predictions truncated + hashed | Suppl. S3 | Fingerprint construction |
| 100k fingerprint–accuracy pairs | Suppl. S3 | FEC LRU cache size |
| 75th percentile / save 75% compute | Suppl. S3 | Hurdle threshold set to 75th pct of unique accuracies (rolling) |
| 100 < W < 1000 (typical) | Sec 3.2 | Number of worker processes |
| Every 100–10000 evaluations, upload 50 algs (half pop) | Suppl. S3 | Migration protocol |
| P = 100–1000; T = 10; U = 0.9 | Sec 3.2 / Suppl. S5 | Meta-params: population, tournament size, mutation prob |
| Run time: 5 days | Sec 3.2 | Experiment duration |
| Constant mutation: ×U[0.5,2.0], sign flip 10% | Suppl. S3 | Real-valued constant mutation rule |
| Instruction removal 2x more likely than addition | Suppl. S3 | Prevents program bloat |
| 8 ≤ F ≤ 256 | Sec 3 | Projected feature dimensionality (proxy tasks) |
| Original dim 3072 | Sec 3 / Suppl. S7 | Full CIFAR-10 dimensionality for final eval |
| Linear regression difficulty = 10^7 | Sec 4.1 | 1 acceptable algorithm per 10^7 (RS success rate) |
| Evolution 5x more efficient than RS (linear reg.) | Sec 4.1 | Even on the easy task |
| Evolution/RS success ratios: 23000, 150, 5.6/2.9 | Fig 4 | Relative success at difficulties up to 10^12 |
| D=1 → hard-codes teacher weights; D=100 → "invents" backprop | Sec 4.1 | Rediscovers gradient-descent-trained 2-layer NN (Fig 5) |
| Candidate better in 13 out of 20 experiments | Sec 4.2 | vs hand-designed 2-layer FC NN on Tselect |
| **Best evolved: 84.06 ± 0.10%** | Sec 4.2 | CIFAR-10 test, 5 seeds |
| Linear baseline (logistic reg.): 77.65 ± 0.22% | Sec 4.2 | Comparison |
| Nonlinear baseline (2-layer FC NN): 82.22 ± 0.17% | Sec 4.2 | Comparison |
| SVHN: 88.12 vs 59.58 (lin) vs 85.14 (nonlin) | Sec 4.2 | Generalization |
| ImageNet (downsampled): 80.78 vs 76.44 vs 78.44 | Sec 4.2 | Generalization |
| Fashion-MNIST: 98.60 vs 97.90 vs 98.21 | Sec 4.2 | Generalization |
| 4 evolved techniques: input noise, multiplicative (bilinear) interactions, normalized gradients, weight averaging/accumulation | Sec 4.2 | Notable discovered features, ablation-verified |
| Ablation drops: noise −0.16%, bilinear −1.46%, normalized grad −1.20%, weight averaging −4.11% | Suppl. S8 | 4 of 6 code sections caused large drops |
| Noisy ReLU (few data): expt 8/30 vs control 0/30, p < 0.0005 | Sec 4.3 (Fig 7a) | Adaptation to few examples (80 ex / 100 epochs) |
| Learning-rate decay (fast training): expt 30/30 vs control 3/30, p < 10^-14 | Sec 4.3 (Fig 7b) | 800 ex / 10 epochs; decay via iterated arctan (≈exponential) |
| Weight-mean-as-LR (multiclass): expt 24/30 vs control 0/30, p < 10^-11 | Sec 4.3 (Fig 7c) | 10-class CIFAR-10; LR = sin(abs(mean(W))) |
| 45 class pairs; 100 projections → 4500 tasks | Suppl. S4 | Binary task generation; 8000/2000 train/valid each |
| 36 pairs → Tsearch, 9 pairs → Tselect | Sec 4.2 | Search vs selection split |
| 10-class: 1000 tasks, 80% Tsearch; 45K/5K train/valid | Suppl. S5 | Multiclass task generation |
| Ops allowed (Sec 4.2): 7 / 58 / 58 for Setup/Predict/Learn | Sec 4.2 | Enlarged op set |
| Hyperparam RS tuning: scale each constant ×[0.001,1000] log-scale, up to 10k trials | Suppl. S7 | Best algo has only 3 constants; few hundred trials sufficed |
| Search-method ablation Best Accuracy (1k proc): Base 0.703 → +Mig 0.707 → +FEC 0.724 → +MNIST 0.729 → +Hurdle 0.738 | Table S2 / Fig 8 | 4 upgrades each beneficial |
| Success fraction (1k proc): 0.00→0.00→0.13→0.27→0.53 | Table S2 | Fraction beating plain NN (0.750) |
| Ablation repeated at 100 and 10 processes | Tables S3, S4 | Same conclusions across compute scales |
| Terminate on NaN/Inf; error > emax=100; runtime > 4x plain NN | Suppl. S3 | Degenerate-algorithm handling; amin=0 |
| Experiments ran in 2019; electricity matched with renewable energy | Sec 4 footnote | — |
| Code open-sourced | Sec 1 footnote | github.com/google-research/google-research/tree/master/automl_zero |

## Scope & Limitations (stated by the authors)
- Results are **"preliminary successes"** / **"promising"**; explicitly framed as an initial demonstration of a research direction, not SOTA.
- Search space **cannot currently represent** techniques crucial in SOTA models — e.g. **batch normalization** and **convolution** (Sec 4.2).
- Implicit bias remains: **one example processed at a time**, so batch techniques (batch-norm) would need loops or higher-order tensors; **multi-layer nets** can only arise by discovering each layer independently — loops/function calls would help (Sec 5).
- **Interpreting** evolved code is hard (complex raw code; needs static analysis + motif-finding + ablations) — Sec 5 / S8.
- **Hyperparameter coupling** hinders tuning/selection; requires **manual decoupling** (Sec 5 / S7).
- **Crossover** and **geographic structure** (preliminary implementations) **did not help** (Sec 5).
- The evolved weight-averaging is actually **accumulation** (W0 = Σ Wt) not averaging — noted difference, but "no effect" on classification accuracy (Sec 4.2).
- Meta-parameters largely **not tuned** at full scale (decided in small expts, taken from prior work, or untuned).
- The search **method itself was NOT the focus** of the study (Sec 5).

## Does NOT claim / boundaries
- Does NOT claim to beat state-of-the-art image classifiers; baselines are simple linear/2-layer NN, and it explicitly **cannot** do batch-norm/convolution.
- Does NOT claim a fully automated interpretation pipeline — decoupling and interpretation are **manual / "time-consuming"**, flagged as future work.
- Does NOT assume existence of a neural network or gradients (deliberately) — these must be evolved.
- Does NOT retain the **self-reflexivity / self-improvement** requirement of early program-synthesis work (Lenat 1983; Schmidhuber 1987) — dropped it.
- Does NOT (in this paper) use LLMs, agents, or any language-model component — purely evolutionary program search over a fixed op vocabulary.
- Not a claim about scientific discovery in natural sciences; the "knock-out/knock-in" analogy to molecular biology is only a **methodological analogy** for interpretation.

## Section map
- **1. Introduction** — motivation, AutoML-Zero proposal, contributions, sparsity (1 in 10^12), FEC 4x, throughput.
- **2. Related Work** — AutoML paradigms, numerically vs symbolically discovered optimizers (Bengio et al. 1994; Bello et al. 2017), program synthesis; extended in Suppl. S1.
- **3. Methods** — 3.1 Search Space (Setup/Predict/Learn, memory, 65 ops, Fig 1 eval pseudocode); 3.2 Search Method (regularized evolution, mutations Fig 2/3, FEC, hurdles, migration, MNIST diversity).
- **4. Results** — 4.1 Finding simple neural nets in a difficult space (RS vs evolution, Fig 4; rediscover backprop NN, Fig 5); 4.2 Searching with minimal human input (Fig 6, 84.06%, discovered techniques, generalization); 4.3 Discovering algorithm adaptations (Fig 7: noisy ReLU, LR decay, weight-mean LR).
- **5. Conclusion & Discussion** — upgrades ablation (Fig 8), interpretation difficulty, hyperparameter coupling, search-space limits (batch-norm/conv), future work.
- **Author Contributions / Acknowledgements / References.**
- **Supplement:** S1 additional related work; S2 search space (Table S1, ops); S3 search method details (FEC, parallelism, hurdles, degenerate termination); S4 task generation; S5 detailed experiment setups; S6 evolved raw code (Figs S1, S2); S7 algorithm selection/evaluation + hyperparameter coupling; S8 interpreting algorithms (ablations); S9 more search-method ablations (Tables S2–S4); S10 baselines (Table S5).
