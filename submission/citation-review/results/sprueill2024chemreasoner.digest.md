# Digest: sprueill2024chemreasoner (BLIND first-pass)

**Paper:** ChemReasoner: Heuristic Search over a Large Language Model's Knowledge Space using Quantum-Chemical Feedback
**Venue/ID:** ICML 2024 (PMLR 235); arXiv:2402.10980v5, 9 Dec 2024 [physics.chem-ph]
**Authors:** Henry W. Sprueill, Carl Edwards, Khushbu Agarwal, Mariefel V. Olarte, Udishnu Sanyal, Conrad Johnston, Hongbin Liu, Heng Ji, Sutanay Choudhury (PNNL; UIUC; Azure Quantum, Microsoft)
**Code/data:** https://github.com/pnnl/chemreasoner

---

## Thesis / Problem
Discovery of new catalysts is essential for energy-efficient chemical processes. Linking microscopic surface properties to macroscopic catalytic performance via chemical descriptors is a barrier (Nørskov et al. 2011). ChemReasoner is an AI-guided **computational screening** framework that unifies LLM linguistic reasoning (hypothesis generation) with **quantum-chemistry-based feedback from 3D atomistic representations**. Catalyst discovery is framed as an uncertain-environment search where an agent (the LLM) iteratively combines LLM-derived hypotheses with GNN-derived feedback, steered by scoring functions on adsorption energies / reaction-energy barriers.

## Method — SEARCH type (IMPORTANT)
- **Heuristic tree search implemented as BEAM SEARCH.** Explicit: "Each layer of the search tree is pruned using a beam search algorithm (Rubin & Reddy, 1977), leaving only those nodes with the highest rewards." (p.4). Beam-width parameter = 6.
- Algorithm 1 is a beam search: generate N children per node, keep top-M by reward, expand to target depth d, return argmax-reward node.
- **NOT MCTS in this paper.** MCTS belongs to the predecessor it builds on — Sprueill et al. (2023) "Monte Carlo Thought Search." ChemReasoner "builds upon Sprueill et al. (2023)" but (a) swaps LLM-computed rewards for true computational-chemistry rewards, and (b) adds a context-aware LLM **Planner** that auto-generates the action space. The search mechanism itself = beam/heuristic tree search, not MCTS.
- Two variants: **ChemReasoner-Expert** (action space hand-defined by catalysis experts, static) vs **ChemReasoner-Planner** (LLM generates its own action space each step, zero human input, adapts to context).

## Method — VALIDATION signal (IMPORTANT)
- **In-loop reward = computational surrogate (GNN), not DFT, not physical.** A GNN (GemNet-dT, Gasteiger et al. 2021, from Open Catalyst Project) trained on DFT simulations predicts adsorption energy from relaxed 3D atomistic structures. Two reward functions: (1) adsorption-energy-based; (2) reaction-pathway-based (smallest max energy jump, Eq. 1).
- **DFT (Quantum ESPRESSO) used ONLY for post-hoc/offline validation** of top-scoring candidates, not in the search loop. DFT called "gold standard" but "significant computational cost" forces GNN use for high-throughput. GNN vs DFT diverge "in some cases significantly" (Table 3).
- **NO physical execution.** Purely computational; no wet-lab synthesis, no robotic experiment. Real-world efficacy checked via **literature evaluation** of predicted catalysts + DFT. Impact statement explicitly: goal is "not necessarily to claim the discovery of a novel catalyst."

## FACTS TABLE (exhaustive)
| Value | Location | Context |
|---|---|---|
| 145 queries total | §4.1 Dataset; Abstract of exp | Benchmark, 3 categories |
| OpenCatalyst = 86 queries | §4.1 | Catalyst per adsorbate (OC20 adsorbates) |
| BioFuels = 39 queries | §4.1 | Biofuel catalyst discovery; modified to metallic catalysts |
| CO2-Fuel / CO2-Conversion = 20 queries | §4.1, §B.4 | CO2→methanol & ethanol (X-anol); reaction-pathway reward |
| Dataset augments Sprueill et al. (2023) | §4.1 | First two categories adopted from it; CO2-Fuel added new |
| LLMs = GPT-3.5-turbo, GPT-4 | §4.1 System Impl.; §C.5 | LLaMA2 tried but instruction-following "too limited to allow an evaluation" |
| GNN = GemNet-dT (Gasteiger et al. 2021) | §4.1, §A | From Open Catalyst Project; reward model |
| Max search depth = 5 | §5.2 | Ntree grows exponentially with depth |
| Branching factor Nactions = 8 (default) | §5.2, §C.1 | Ablation §C.4: rewards rise for max-actions 2–6, best at 8 & 10 |
| Beam width = 6 | §5.2 | Nodes expanded per iteration |
| Expert = 2·Ntree LLM inferences; Planner = 3·Ntree | §5.2 | Planner does extra planning inference per node |
| Full 145-query benchmark, Nmax=300 → 28,000–42,000 LLM inferences | §5.2 | Scale of experiment |
| LLM inference batch size = 48, async | §5.2 | Throughput |
| Nstructs = 16 (default) | §5.2/§A | Sampled adsorbate+catalyst configs; lowest-energy kept |
| Nrelax = 64 (default max iters) | §5.2/§A | Relaxation stops at 64 or Fmax<0.05 eV/Å |
| Adsorption-energy reward = Nstructs·Nrelax GNN inferences | §5.2 | Per single reward eval |
| Reaction-pathway reward = Nstructs·Nrelax·Npathway·Nrstep GNN inferences | §5.2 | Per single reward eval |
| 9,216 GNN inferences per reaction-pathway reward | §5.2 | CO2-fuel: 2 pathways × 4–5 steps |
| GNN batch size = 40; ~0.5 s per L-BFGS batch on A100/V100 | §5.2, §C.5 | Relaxation via L-BFGS (PyTorch) |
| GPT-4 → 11.28% reduction in avg search depth | §4 (results) | vs GPT-3.5; efficiency gain |
| Adsorbate placed 1.87 Å above surface | §A | Structure sampling |
| Rotation: ≤15° x-axis, ≤360° z-axis | §A | Orientation sampling |
| Bimetallic AB ratio 2:1; trimetallic 1:1:1 | §A | >3 elements → penalty value |
| Lattice: FCC, BCC, HCP only | §5.3, §A | Others skipped/penalized; limitation for multimetallic |
| >700,000+ atomistic trajectories released | §1 | Public data contribution |
| 5 reaction pathways initially from LLM → narrowed to 2 per application | §3.3 | CO2→methanol/ethanol; not re-evaluated per tree |
| Table 1 OpenCatalyst best = Planner-GPT4 2.36 | Table 1 | CoT 0.37 / SC 0.73 / Expert 1.90 / Planner 2.36 (GPT-4 col) |
| Table 1 BioFuels best = Planner-GPT4 4.15 | Table 1 | Expert 3.90, Planner 4.15 (GPT-4) |
| Table 1 CO2-Conversion best = Expert-GPT3.5 0.78 | Table 1 | Expert best here, on GPT-3.5-turbo |
| Planner beats Expert in 2 of 3 categories | §1 contributions, §4 | OpenCatalyst & BioFuels; Expert wins CO2-Conversion |
| Table 2 GPT-4 top-5 = Pd, Cu, Ru, Rh, Pt | Table 2 | CO2→methanol |
| Table 2 Expert top-5 = Cu-Zn, Fe, Ni, Co, Cu-Cr | Table 2 | Includes commercial-catalyst elements |
| Table 2 Planner top-5 = Pd-Au, Pt-Ru, Ru-Au, Rh-Pd, Pt-Au | Table 2 | Bimetallic precious-metal alloys |
| Commercial methanol catalyst = Cu/ZnO/Al2O3 | §5.4 (Etim et al. 2020) | Expert predictions overlap its elements |
| ChemReasoner recommended CuAlZn for CO2→methanol | §6 Conclusion | "current commercially viable catalyst" |
| DFT stack: Quantum ESPRESSO, PBE, DFT-D3, PAW (pslibrary), AiiDA | §C.2 | Post-hoc validation only |
| Table 3: GNN vs DFT diverge significantly | §5.3, Table 3 | e.g. CuZn CHOH: GNN 0.552 vs DFT 5.951 eV |
| Materials Project structure finder (Jain et al. 2013) | Fig. 4 | Visualization of 3D structures |
| Reward Eq. 1: r(c) = −min_paths max_steps (E_ads,t − E_ads,t−1) | §3.3 | Smallest "hill to climb" over reaction path |

## Scope & Limitations (author-stated)
- Reliance on pre-defined reference lattice structures (FCC/BCC/HCP) may not reflect realistic catalyst structures, esp. multimetallic; multimetallic bulks built by random element placement → defects.
- GNN predictions diverge from DFT ground truth in some cases significantly (Table 3), making validation of predicted catalysts difficult.
- Text→3D-structure conversion identified as a key error source; future work should improve it.
- Open-source LLMs (LLaMA2) lacked instruction-following/throughput required.
- LLM's notion of a "good catalyst" may not align with complex reaction-pathway reward (CO2-Conversion); suggests RLHF-style fine-tuning as future work.

## Does NOT claim / Boundaries
- Does **NOT** claim physical/experimental discovery of a novel catalyst; no wet-lab synthesis or testing. Impact statement: purpose is to discuss strengths/weaknesses of the AI tool, "not necessarily to claim the discovery of a novel catalyst."
- Does **NOT** use DFT as the in-loop reward — GNN surrogate only; DFT is offline validation of top candidates.
- Does **NOT** use MCTS in this framework — uses beam/heuristic tree search. (MCTS = predecessor Sprueill 2023 "Monte Carlo Thought Search.")
- Validation of the flagship CuAlZn / Cu-Zn result is by **literature match to the known commercial catalyst + DFT**, framed as method validation, not a novel-discovery claim.

## Section Map
- §1 Introduction (3 contributions: framework; planner surpasses expert in 2/3; domain-grounding via quantum-chemical feedback beyond adsorption energy)
- §2 Background & Related Work (2.1 Catalysis; 2.2 LLMs for Chemistry) + Algorithm 1
- §3 System and Methods (3.1 Heuristic Search [beam]; 3.2 Planner-Guided Search; 3.3 Reward via Structure Optimization & Energy Prediction — adsorption-energy & reaction-pathway rewards, Eq. 1)
- §4 Experiments (RQ1 performance improvement; RQ2 key components/complexity trade-off; RQ3 hypothesis testing; 4.1 setup, Table 1)
- §5 Towards Explainable Reasoning (5.1 Expert vs Planner action spaces; 5.2 complexity params; 5.3 DFT-based rewards & GNN-DFT divergence; 5.4 CO2 hydrogenation case study, Table 2)
- §6 Conclusion; Impact Statement
- Appendices: A GNN adsorption-energy calc; B Dataset design (B.1 prompt, B.2 OpenCatalyst, B.3 BioFuels, B.4 CO2-Conversion, B.5 symbols parsing, B.6 planner prompt); C Search analysis (C.1 param selection, C.2 DFT validation, C.3 search depth, C.4 action ablation, C.5 scaling); D Multi-modal chemistry models; E Full planner-driven execution trace (GPT-4)
