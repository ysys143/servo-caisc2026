# Digest: vafa2025foundationmodel (BLIND first-pass)

**Title:** What Has a Foundation Model Found? Using Inductive Bias to Probe for World Models
**Authors:** Keyon Vafa (Harvard), Peter G. Chang (MIT), Ashesh Rambachan (MIT), Sendhil Mullainathan (MIT)
**Venue:** ICML 2025 (42nd Intl. Conf. on Machine Learning, Vancouver; PMLR 267, 2025). arXiv:2507.06952v4 [cs.LG], 27 Dec 2025. 21 pages.
**Code:** https://github.com/keyonvafa/inductive-bias-probes (footnote, p.5)

Digest based ONLY on this paper.

---

## Thesis / Problem

Foundation models rest on the premise that sequence prediction can uncover deeper domain understanding — the paper's running analogy is Kepler (accurate geometric orbit predictions) -> Newton (mechanistic world model) (Abstract; §1, lines 16-20, 70-78). The core question: **does strong predictive/task performance imply the model has internalized the underlying world model?** The paper develops a technique to test whether a foundation model has learned a *postulated* world model, and repeatedly finds that it has not.

### CRUCIAL for audit — Does strong task performance NOT imply an internalized world model?

**YES — this is the paper's central claim and empirical finding.** Direct statements:
- Abstract (lines 29-33): "foundation models can excel at their training tasks yet fail to develop inductive biases towards the underlying world model when adapted to new tasks."
- Abstract (lines 33-38): "foundation models trained on orbital trajectories consistently fail to apply Newtonian mechanics when adapted to new physics tasks... these models behave as if they develop task-specific heuristics that fail to generalize."
- Physics: the transformer predicts orbital trajectories with **R² > 0.9999** (line 689) yet its fine-tuned force predictions imply a **nonsensical law of gravitation** (Fig 1, Table 1), recovering a *different* law for every galaxy sample (§3, lines 913-922).
- Othello/lattice: models generate legal moves **~90–100%** of the time (lines 1087-1089) but have poor inductive bias toward the true board/state; they group states by *legal next-token equivalence* rather than the true world model (§4, lines 1098-1165).
- Conclusion (lines 1283-1288): "while many sequence models excel at next-token prediction tasks, they often have limited inductive bias toward genuine world models. Rather than learning coherent world models... these models may be relying on coarsened state representations or non-parsimonious representations."

## Method — the "inductive bias probe"

Core insight (lines 46-52): "the implicit world model of a foundation model is revealed by how it extrapolates from a small amount of information." The functions a learning algorithm tends to learn when extrapolating from limited data = its **inductive bias** (lines 266-268), motivated by the **no-free-lunch theorem** (Wolpert, 1996) (line 260).

Procedure (Fig 2; §2.3): repeatedly (1) fit the foundation model to small **synthetic datasets consistent with the postulated world model**, (2) extract the learned/extrapolated functions, (3) **compare those functions to the world model's functions** — NOT by "accuracy" (no single accurate function), but by whether extrapolations resemble those the world model allows (lines 253-258).

Two metrics for the special case (binary output Y={0,1}, finite state space Φ) (§2.2):
- **R-IB (respect state):** if two inputs map to the same state, the model should give the same prediction (Eq. 1, line 470-472). Higher = better.
- **D-IB (distinguish state):** if two inputs map to different states, the model should give different predictions (Eq. 2, line 486-489). Higher = better.
- Analogous to precision/recall; both needed (lines 496-501). Trivially high R-IB by constant prediction kills D-IB.

General case (§2.3): **extrapolative predictability** Î(xi,xj) (Eq. 3) vs. an **oracle** foundation model given true state Φ and admissible functions G (Eq. 4-5); inductive bias toward world model IB(s,s̄) (Eq. 6), visualized as a calibration curve — 45° line = perfect inductive bias (Fig 4).

Contrast with prior probing (lines 451-463): standard (linear/SAE) probes measure whether *fixed internal representations* predict state; they are sensitive to how state is represented and can't tell which of many predictable mappings the model actually uses. The inductive bias probe instead studies *how the model learns/behaves when adapted*, depends only on state equality, and is **insensitive to equivalent representations** (lines 462-463).

Alternative-bias hypothesis (§4, lines 1113-1165): models group distinct states with the **same set of legal next tokens**. Formalized by decomposing D-IB into D-IBq= (same legal next-tokens) and D-IBq≠ (different); D-IBq= < D-IBq≠ (statistically significant for all models, Table 9) indicates bias toward the next-token partition rather than true state.

---

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| arXiv:2507.06952v4 [cs.LG], 27 Dec 2025 | line 6 | Version/date |
| ICML 2025, 42nd, Vancouver, PMLR 267 | lines 90-91 | Venue |
| 4 authors: Vafa (Harvard), Chang, Rambachan, Mullainathan (MIT) | lines 4, 88 | Affiliations |
| Vafa supported by Harvard Data Science Initiative; Chang by NSF CSGrad4US Fellowship | lines 1325-1326 | Acknowledgments |
| **109M parameter transformer** (Vaswani et al. 2017) | line 766 | Physics model size |
| **R² > 0.9999** on held-out orbit prediction | line 689 | Trajectory accuracy; beats "most recent position" / "per-orbit mean" baselines (Table 8) |
| 7K bins per coordinate (x,y); coords span −50 to 50 AU | lines 685-687 | Discretization (discretized+cross-entropy beat continuous+MSE) |
| Trained 25 epochs, 8 H100 GPUs | line 687 | Physics pretraining compute |
| Training set: **10M sequences, 20B tokens** | line 755 | Physics pretraining data |
| 1,000 observations per sequence | line 743 | Sequence length |
| Half 6-month intervals, half 1-week; special start token flags interval | lines 745-747 | Time discretization |
| Newton's law used: F = G·m1·m2/‖r‖²·er | lines 759-761 | Ground-truth force law |
| 100 synthetic datasets, outputs = linear functions of state | line 727 | IB probe for physics |
| Fine-tune to predict force vector on our solar system, **1% of true forces** as labels | lines 873-875 | Force-vector experiment (Fig 1) |
| Fine-tune on **10K solar systems** for force magnitude | line 878 | Larger-scale symbolic regression |
| Symbolic regression via **PySR** (Cranmer, 2023; Cranmer et al., 2020) | lines 879-882 | Recovers force law |
| Table 1: recovered force laws differ per galaxy, **never** the true law | Table 1 (lines 791-833) | e.g., F∝sin(sin(1/(r−0.24)))+1.45·(1/r)+1/m2; F∝cos(cos(2.19·m1)); etc. |
| Oracle (kNN, k=2, Euclidean on true state) recovers same correct law for all 5 galaxies | lines 918-919, 1842-1844 | Feasibility check |
| Lattice: states varied **2 to 5**; tokens Σ={L,⊥,R}; init state 1 | lines 899, 909 | Lattice setup |
| Lattice: sequences length 100; **10M training tokens, 100k hold-out** | lines 905-911 | Lattice data |
| Othello: 8×8 board, ≤60 moves/game, 60 squares (middle 4 pre-occupied) | lines 928-931 | Othello setup |
| Othello: **20M training games, 3.8M hold-out games** | lines 933-934 | Othello data |
| Othello board-prediction fine-tune: pretrained on **1M games** | line 1140 | Board reconstruction (Fig 6) |
| 5 model classes: RNN (Elman 1990), LSTM (Hochreiter 1997), Transformer (Vaswani 2017), Mamba (Gu & Dao 2023), Mamba-2 (Dao & Gu 2024) | lines 1052-1054 | Architectures |
| Next-token legality: **~90%** Othello, **100%** lattice (5 states) | lines 1087-1089 | All models "obey state" superficially |
| Table 7 next-token: Lattice all 1.00; Othello RNN .992, LSTM .996, Transformer .999, Mamba .999, Mamba-2 .999 | Table 7 (lines 2545-2567) | Legal-prediction share |
| Table 2 R-IB/D-IB (NTP-trained), Lattice-5: Transformer R-IB .483 / D-IB .677; Othello Transformer R-IB .703 / D-IB .624 | Table 2 (lines 943-1050) | 1=perfect, 0=noninformative; all models poorer on Othello |
| Transformer "consistently does worse than other models" on lattice (all others recurrent/state-space) | lines 1104-1106 | Architecture effect |
| Table 8 orbit MSE (Transformer): 1-step 1.90e-8, 5-step 1.56e-8, 100-step 3.74e-5 | Table 8 (lines 2571-2599) | 200 held-out trajectories, forecast from step 50/500 |
| IB Correlation (Table 6): Edge Balance ACC 0.960, Board Balance ACC 0.610, Majority Tiles ACC 0.477 | Table 6 (lines 2509-2529) | Higher IB -> better transfer |
| Table 9: D-IBq= < D-IBq≠ for all models (statistically significant) | Table 9 (lines 2601-2644) | Bias toward legal next-token partition |
| **LLMs tested:** o3 (OpenAI), Claude 4 Sonnet / "Claude Sonnet 4" (Anthropic), Gemini 2.5 Pro (Google) | line 1850; Table 3 | Appendix D physics-with-LLMs |
| LLM setup: 5 solar systems, 450 obs each; give true force magnitudes for **10** obs (~"2%") in-context; no fine-tuning | lines 1854-1857, Fig 9 | LLMs not told outputs are forces |
| 2,250 observations collected per LLM | line 2088 | LLM eval size |
| Table 3 LLM recovered laws: o3 F∝m1; Claude Sonnet 4 F∝m2^(−0.50); Gemini 2.5 Pro F∝m1 (ground truth F∝m1·m2/r²) | Table 3 (lines 1825-1840) | LLM regressions simpler but still wrong |
| Two-body ablation: pretrain transformer on **10M two-body systems, 10 epochs**, masses Unif(1e-4,1e-2) solar masses | lines 1706-1707 | Robustness (Appendix B.1); still poor IB |
| Two-body symbolic regression: F ∝ m1·exp(r)⁻¹ (nonsensical) | lines 1716-1717 | Fails to recover Newton |
| Physics gen params: planets Unif[1..10], eccentricity Beta(α=0.867,β=3.03) [Kipping 2013], semi-major axis Unif(0.3,42) AU, planet mass LogUniform(1e-7,1e-3), star mass Unif(0.5,5) | lines 1610-1613 | Appendix A |
| Optimizer Adam (Kingma & Ba 2014), lr 6e-4, 2000 warmup, weight decay 0.1, grad clip 1 | lines 1606-1607 | Training |
| Transformer arch: decoder, 12 layers, 12 heads, 768 dims | line 1597 | Appendix A |
| Mamba: 24 layers, 768 dims, SSM state exp 16, block exp 2, conv width 4 | lines 1599-1602 | Appendix A |
| RNN: 6 layers (Othello) / 2 layers (lattice), 768 dims | lines 1593-1595 | Appendix A |
| IB probe impl: 100 datasets × 100 examples; 50 random 6×1 Gaussian projections, pick max Spearman corr; 6D state space | lines 1619-1623 | Appendix B.1 |
| Lattice/Othello outputs Bernoulli(0.5); Othello 210 openings depth 10 (2,100 subseq); lattice 1,000 seq len 100 (100,000 subseq) | lines 1722, 1748, 1757 | Appendix B.2 |
| Force-vector fine-tune: 8 solar-system sequences, 1% obs labeled, MSE 10,000 steps, lr grid 1e-6–5e-4 (best 2e-4) | lines 1764-1767 | Appendix C |
| Symbolic regression: max size 20, binary ops {+,×}, unary ops {sin,cos,exp,inverse}, 3 restarts × 100 iters | lines 1788-1791 | Appendix C |

---

## Scope & Limitations / Boundaries (Does NOT claim)

- **A world model must be specified in advance** to run the probe (Conclusion, lines 1289-1294): "a limitation for analysts searching for the exact representation the model is using." Future work should automate constructing the world model implicit in the model's behavior (lines 1295-1308).
- The probe does **not** claim to read internal weights/representations — deliberately sidesteps mechanistic probing and its reliability issues (Belinkov 2022; complexity concerns) (lines 1215-1220). It measures behavior/inductive bias, "how a model learns, rather than what's encoded in its fixed representations."
- Does **not** claim models learn *nothing*: they excel at next-token prediction and generate legal moves; the claim is specifically that their **inductive bias** is not toward the postulated world model.
- Does **not** claim world models are impossible for such tasks: Lemos et al. (2023) recovered Newton's law from a GNN **by architecturally imposing** Newton's laws as inductive biases; the authors call imposing domain-specific inductive biases "a promising approach" (lines 1245-1251).
- LLM experiment is explicitly **small-scale** (cost-limited: fewer solar systems, in-context not fine-tuned); simpler recovered laws "may be due to differences in experimental setup" — not a like-for-like comparison to the domain-specific models (lines 1846-1858, 2088-2092).
- Positive correlational claim (a practical implication, not just negative): models that score **better on inductive bias probes transfer better** to new tasks relying on the world model (lines 130-133, Table 6, lines 1076-1081).
- Interaction between planets is **omitted** (planet masses ≪ sun) in the main physics simulation (lines 722-724).

## Section Map

- **Abstract** — claims: excel at training task yet fail to develop inductive bias toward world model; orbital models fail Newtonian mechanics; task-specific heuristics.
- **§1 Introduction** — Kepler->Newton framing; inductive bias probe defined; Fig 1 (nonsensical recovered force law); no-free-lunch motivation; heuristics preview.
- **§2 Framework** — data/tasks/foundation model/world model definitions; §2.1 comparing FMs to WMs; §2.2 special case (R-IB Eq.1, D-IB Eq.2, Fig 3); §2.3 general probe (extrapolative predictability Eq.3, oracle Eq.4-5, IB Eq.6, Fig 4); contrast with standard probes.
- **§3 Orbital Mechanics** — background (Kepler/Newton); data & pretraining (109M transformer, R²>0.9999); "Has it recovered Newtonian mechanics?" (poor IB, Fig 4); force-vector & force-magnitude experiments + symbolic regression (Table 1: different law per galaxy); LLM pointer to §D.
- **§4 Other Applications** — lattice & Othello; models (5 classes); next-token performance (Table 7); IB probe results (Fig 5 lattice, Table 2 Othello); "what is the bias toward?" -> legal next-token partition hypothesis (D-IBq=/D-IBq≠, Fig 6, Table 9); transfer results (Table 6).
- **§5 Related Work** — world models (LeCun 2022; Vafa et al. 2024; Toshniwal 2022; Li et al. 2023); representation probes/SAEs and their reliability issues; "bags of heuristics" (jylin04 2024; Nikankin 2024); DFA/formal-language learning; scientific foundation models; physics-law discovery (Lemos et al. 2023 counterpoint); Rashomon effect/model multiplicity (Breiman 2001); causal representation learning (Schölkopf 2021).
- **§6 Conclusion** — summary; limitation that a world model must be specified; call for automated world-model construction.
- **Appendices A–H** — A model/training details; B metric implementation (B.1 physics, B.2 lattice/Othello); C force-prediction details + Fig 8 oracle; D LLM physics experiments (Table 3, Figs 9-10); E IB ablations (Tables 4-5); F transfer results (Table 6); G next-token performance (Tables 7-8); H D-IB decomposition (Table 9).
