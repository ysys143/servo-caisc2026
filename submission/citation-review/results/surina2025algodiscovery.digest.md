# Digest: surina2025algodiscovery (BLIND first-pass)

**Title:** Algorithm Discovery With LLMs: Evolutionary Search Meets Reinforcement Learning
**Authors:** Anja Surina, Amin Mansouri, Lars Quaedvlieg, Amal Seddas, Maryna Viazovska, Emmanuel Abbe, Caglar Gulcehre (EPFL; Apple)
**Venue/ID:** arXiv:2504.05108v4 [cs.AI], 4 Aug 2025
**Method name:** EvoTune. Code: https://claire-labo.github.io/EvoTune/

---

## Thesis / Problem
Discovering efficient algorithms is a long-standing challenge requiring human expertise. LLM+evolutionary-search methods (e.g., FunSearch) accelerate algorithm discovery but treat the LLM as a **static generator**, wasting the signal from evolutionary exploration. Thesis: **augment LLM-based evolutionary search by continuously refining the search operator (the LLM itself) via reinforcement-learning fine-tuning**, using evaluation scores of generated programs as reward. Evolutionary search provides exploration; RL distills patterns from discoveries to steer future search (framed via Sutton's "Bitter Lesson": search + learning are synergistic).

## Method — direct answers to the audit questions
**Does it do ALGORITHM DISCOVERY via LLM-guided search + evolutionary search + RL? YES — all three, tightly coupled in one loop.**
- **LLM-guided:** An instruction-tuned LLM generates candidate algorithms as executable **Python programs** (a priority/heuristic function) conditioned on a Chain-of-Thought prompt built from sampled program-score pairs.
- **Evolutionary search:** FunSearch-style, **island-based program database** (islands + score-clustered within islands; Tanese 1989, Cantú-Paz 1998). Bootstraps from best programs found so far; gradient-free selection/variation/diversity.
- **RL:** After every `f_RL` search iterations, the LLM policy is fine-tuned with **DPO** (Rafailov et al. 2024) — but in an **off-policy setting with non-fixed inputs** (not standard offline DPO), on preference pairs (higher- vs lower-scoring outputs, plus valid-vs-failed pairs). Uses a **forward-KL-regularized DPO** variant to preserve output diversity. Authors argue (App. A.5) this is genuinely RL (MDP formulation, reduces to an offline one-step bandit). EvoTune **alternates** the two phases (Algorithm 1).

**Does it close the loop via reliable EMPIRICAL / BENCHMARK validation? YES — the loop is closed by empirical program execution.** Every generated program is **executed and scored on held-out validation instances** (optimality gap / MSE); scores are the reward signal that drives both database updates and RL. Evaluated across validation, validation-perturbed, and test splits, **averaged over 10 seeds** (4 seeds for Hashcode/LLM-SR). This is empirical/benchmark validation, not proof or self-assessment.

## FACTS TABLE (exhaustive) — value | location | context
| Value | Location | Context |
|---|---|---|
| EvoTune | throughout | Proposed method name |
| FunSearch (Romera-Paredes et al. 2024) | §1, §4.2 | Baseline = evolutionary search only, no LLM training |
| DPO (Rafailov et al. 2024) | §3.2 | RL-Update algorithm chosen; off-policy, non-fixed inputs |
| Forward KL (vs reverse KL) | §3.2, Fig 3b | Design choice preserving diversity; forward KL wins ablation |
| β = 0.4 | App A.8 | DPO KL regularization strength (set "high") |
| Llama3.2 1B Instruct; Phi 3.5 Mini Instruct (3.8B); Granite 3.1 2B Instruct | §4.2 | Three instruction-tuned LLMs tested |
| 1B–3.8B params | §6 | Model size range studied |
| 10 random seeds | §4.2 | Main results averaging |
| 4 seeds | Fig 4 caption | Hashcode + LLM-SR results |
| Budgets 9.6k / 16k / 22.4k | Table 1 | Sampling budgets (programs sampled) |
| T = 2800; ~22,400 samples | App A.8 | Max timestep / total outputs |
| m = 2 | App A.8/A.4 | Programs concatenated per prompt |
| K = 8 outputs/prompt | App A.8 | Generations per prompt |
| 6 islands | App A.8 | Program database islands |
| f_RL = 400 (alternate after 3,200 outputs) | App A.8 | RL frequency |
| temp 0.9, top-k 100, nucleus p 0.95, max 2048 tokens | App A.8 | Sampling params; TGI inference |
| LoRA rank 64, α 32; 2 epochs; AdamW | App A.8 | Fine-tuning config; TRL + Accelerate |
| LR grid [3×10⁻⁵, 5×10⁻⁷]; schedule α_t = α_init·√(1000/t) | App A.8 | Learning-rate tuning/decay |
| Exec limits: 60s BP/FP, 90s TSP; 5 GB mem | App A.8 | Program constraints |
| **Bin Packing** (Coffman Jr 1984) | §4.1 | Task 1; evolve `priority()`; OR-Library (Beasley 1990); 20 val instances, 500 items; excess-bins over lower bound (Martello & Toth 1990) |
| **TSP** (Jünger 1995; Gutin & Punnen 2006) | §4.1 | Task 2; evolve penalty-matrix heuristic used in Guided Local Search (Voudouris & Tsang 1999); Elkai solver ref (Dimitrovski 2019); val 100×(c=100)+100×(c=200); perturb p=0.2 |
| **Flatpack** (Bonnet et al. 2023 / Jumanji) | §4.1 | Task 3; evolve placement scorer; 45 val instances (15×9×9, 20×11×11, 10×15×15); blocks ≤3×3 |
| Hash Code Datacenter Opt (2015): EvoTune **418** > human **407**; FunSearch **414** | §4.2, App A.9 | Budget 10,000 functions; EvoTune surpasses top human team |
| Hash Code Self-Driving (2018): neither beats human; percentiles 87.6% (EvoTune) / 87.1% (FunSearch) | App A.9 | Budget 20,000 functions; DOES NOT beat human here |
| LLM-SR (Shojaee et al. 2024): E. coli growth, Stress-Strain | §4.1, App A.9 | Symbolic regression tasks; ~10,000 samples (≈2,500 iters) |
| Stress-Strain: Phi-3.5 (3.8B) EvoTune ID 0.0033 / OOD 0.0035 beats Mixtral 8x7B (0.0162/0.0946) and GPT-3.5-turbo (0.0210/0.0516) | Table 2 | NMSE, lower better; small model beats larger proprietary |
| E. coli: EvoTune ID 0.0082/OOD 0.0322 beats own FunSearch (0.0383/0.0636) but Mixtral (0.0026/0.0037) still best | Table 2 | Competitive, not universally best |
| Best programs: BP gap **2.06** (Phi 3.5), TSP gap **2.446** (Granite), FP gap **0.0829** (Llama) | Listings 1–3 | Single best evolved heuristics |
| TSPLib: 29 instances; baselines POMO, LEHD, NeuralGLS, KGLS | App A.12, Table 4 | Non-LLM comparison, generalization test (unseen in training) |
| EvoTune trained tmax=20; deployed tmax=100/200/1000 → avg gap 0.82 / 0.69 / **0.32** | Table 4 | At tmax=1000 beats all: KGLS 0.36, NeuralGLS 0.96, LEHD 1.92, POMO 2.02 |
| Human-designed heuristics: BP 5.37 → EvoTune 2.06 (FunSearch 2.96); FP 0.1092 → EvoTune 0.0829 (FunSearch 0.0898) | Table 5 | Both beat human starting heuristics; EvoTune best |
| ReSTEM (Gulcehre 2023; Singh 2023) underperforms DPO, sensitive to HPs | §4.2, App A.13 | Alternative RL variant; DPO better across 3 LRs |
| "To the best of our knowledge, we are the **first** to demonstrate the potential of tightly integrating LLM-based evolutionary search with RL in the loop" | §1 (contributions) | Novelty claim |
| Prior LLM+evo work distinguished: ELM (Lehman 2023, RL only conditions generation, not search), EoH (Liu 2024), ReEvo (Ye 2024), Liu 2023a/b (no reward feedback), FunSearch | §5 | Positioning vs related work |

## Scope & Limitations (paper's own)
- LLMs limited to **1B–3.8B**, sampling budget ≤ **22.4k** outputs; larger models/budgets needed to know full potential (§6).
- RL phase adds **extra compute cost**; training-vs-inference cost trade-offs at scale left to future work (§6).
- Evolutionary search alone can converge to suboptimal solutions with limited budget — the problem EvoTune targets (§6).

## Does NOT claim / boundaries
- **Explicitly NOT aiming for SOTA** on benchmarks; uses small open-source LLMs; tasks are "testbeds" for evaluating the training-vs-no-training contribution (App A.12).
- Does **not** operate on problem instances directly like Neural Combinatorial Optimization; it searches for an **algorithm/heuristic** reusable at any problem size (App A.3).
- **Does not beat human teams** on the Hash Code Self-Driving task within budget (App A.9); not universally best on E. coli (Table 2).
- Scope is **algorithm discovery for combinatorial optimization + symbolic regression** — NOT a general autonomous "AI scientist," hypothesis generator, lab-automation, or scientific-writing system. No wet-lab, no literature synthesis, no autonomous experiment design beyond program search.
- Prompt improvements / in-context example scaling gave no considerable gains — the improvement comes from **in-weight** RL training (§4.2).

## Section map
1. Introduction (motivation, contributions) — §1
2. Preliminaries (LLM notation; evolutionary search Eq.1; RL objective Eq.2; DPO loss Eq.3) — §2
3. EvoTune (Algorithm 1; 3.1 Evolutionary search + program database; 3.2 RL training, preference dataset, diversity/forward-KL) — §3
4. Experiments (4.1 Evaluation tasks: BP/TSP/FP + Hashcode + LLM-SR; 4.2 Results: Table 1, top-50 reward, unique solutions, score distributions, forward-vs-reverse KL, ReSTEM, non-LLM baselines) — §4
5. Related Work (evo search w/ LLMs; prompt optimization; self-improvement) — §5
6. Conclusion (+ limitations) — §6
Ethics; Acknowledgements; References
Appendix A.1–A.13 (eval tasks; GLS; extended related work/NCO; program database; RL formulation/MDP; DPO filtering; prompts; experimental details; Hashcode+LLM-SR results incl. Table 2; additional BP/TSP/FP results incl. Table 3, Fig 5–9 t-SNE; generated programs Listings 1–3; non-LLM comparison Tables 4–5; ReSTEM Algorithm 2, Fig 10)
