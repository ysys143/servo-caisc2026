# Digest: liu2026lasthuman

**Title:** The Last Human-Written Paper: Agent-Native Research Artifacts
**Authors:** Jiachen Liu (Amber Liu), Jiaxin Pei, Jintao Huang, Chenglei Si, ... Zechen Zhang (large multi-institution author list; corresponding: Jiachen Liu, Orchestra Research)
**Venue/ID:** arXiv:2604.24658v2 [cs.LG], 29 Apr 2026 (dated May 1, 2026; PAPER.md frontmatter lists venue "NeurIPS 2026", status draft). 46 pages.
**Blind read basis:** pdftotext -layout extraction of the full PDF; whole body + appendices A–H read.

---

## Thesis / problem
Scientific publishing compiles a branching, iterative research process into a linear narrative, discarding most of what was discovered. The authors argue this imposes two structural costs: a **Storytelling Tax** (failed experiments, rejected hypotheses, and the branching exploration process are discarded to fit a linear narrative) and an **Engineering Tax** (the gap between reviewer-sufficient prose and agent-sufficient specification leaves implementation details unwritten). These were tolerable when readers were human but become critical when AI agents must understand, reproduce, and extend published work. They propose the **Agent-Native Research Artifact (ARA)**, a file-system protocol that replaces the narrative paper with an agent-executable research package, plus three enabling mechanisms and an ARA-native review system.

## Method (what ARA is)
ARA is a directory ontology organizing research into **four interlocking layers** (§2.2):
1. **Cognitive Layer (`/logic`)** — structured scientific reasoning: `problem.md` (observations, gaps, key insight), `solution/` (architecture, algorithm, convergence-critical heuristics), `claims.md` (falsifiable assertions with proof pointers), `experiments.md` (verification plan), `related_work.md` (typed citation dependencies: imports/bounds/baseline).
2. **Physical Layer (`/src`)** — executable code in one of two modes declared in `PAPER.md` frontmatter (`src_mode: kernel | repo`): **kernel mode** (core modules only, typed I/O, often 1–2 orders of magnitude smaller than full repo) for algorithmic contributions; **repository mode** (full implementation + `index.md` manifest) for systemic contributions. `configs/` annotates hyperparameters; `environment.md` pins deps/hardware/seeds.
3. **Exploration Graph (`/trace`)** — `exploration_tree.yaml`, a nested-YAML research DAG with **five typed node kinds: question, decision, experiment, dead_end, pivot**; "a git log for research"; dead-end nodes preserve hypothesis, failure mode, lesson.
4. **Evidence Layer (`/evidence`)** — raw outputs (`results/`, `logs/`) that ground every claim; withholding ground-truth enables blind verification and access control.
- Rooted in a `PAPER.md` manifest (YAML frontmatter + layer index, ~500 tokens to triage relevance). Cross-layer "forensic bindings" link claims→code→evidence. Decomposition informed by "a taxonomy of ten reproduction-critical information categories derived from PaperBench rubrics" (App. A.1).
- **Sufficiency** is defined as capability-relative: an ARA is sufficient when a sufficiently capable coding agent can reproduce the core claim zero-shot from it alone.

**Three enabling mechanisms:**
- **Live Research Manager (§3):** an agent skill running a three-stage retrospective pipeline at each session boundary — **Context Harvester → Event Router → Maturity Tracker**. Event Router classifies each event into one of **seven types** (Table 1: decision, experiment, dead_end, pivot, claim, heuristic, observation) and tags **provenance** = one of {user, ai-suggested, ai-executed, user-revised}. ai-suggested events never auto-upgrade until researcher confirms. Stateless manager; artifact is version-controlled.
- **ARA Compiler (§4):** an agent skill (~482-line NL spec) that translates legacy PDFs/repos/rubrics/trajectory logs into an ARA via **four stages: Semantic Deconstruction → Cognitive Mapping → Physical Grounding → Exploration Graph Extraction**. Uses ARA Seal Level 1 as in-loop validation, iterating "2–3×" until conformant. Many-to-one, graceful degradation (PDF alone → valid artifact with stub physical layers).
- **ARA-Native Review System (§5):** the ARA Seal + a three-stage review pipeline.

**What the Seal automates (ARA Seal, three escalating levels; §5.2, Fig. 8):**
- **Level 1 – Structural Integrity** (seconds, deterministic): directory ontology exists, schema conformance of every structured file, required-field presence (each claim has Statement/Status/Falsification criteria/Proof; each heuristic has Rationale/Sensitivity/Bounds), cross-layer references resolve. Submission requirement. Minimum counts (App. H.1): ≥5 concepts, ≥3 experiments, ≥8 exploration-tree nodes with ≥1 dead_end and ≥1 decision.
- **Level 2 – Argumentative Rigor** (minutes, rubric-anchored agent = the **Rigor Auditor**): without executing code, evaluates content on **six objective dimensions, each scored on an anchored 1–5 rubric**. Three "load-bearing" dimensions: **evidence relevance** (type-aware entailment; causal→ablations, generalization→heterogeneous conditions, improvement→baselines), **falsifiability quality**, **methodological rigor**. Three further (App. H.2.2): **scope calibration, argument coherence, exploration integrity**. Findings carry severity ∈ {critical, major, minor, suggestion}, verbatim evidence spans, and suggestions; overall grade derived from mean score + per-dimension floors.
- **Level 3 – Execution Reproducibility** (hours–days, sandboxed coding agent): ranks claims by criticality, runs scaled-down **directional** checks (small data, few epochs, toy configs) under a venue compute budget; agent is isolated from the evidence layer (gets only code kernel + algorithm descriptions, never reported numbers) to prevent fabrication. Over-budget claims flagged "unverified."
- Passing issues a **Seal Certificate** (artifact ID, level achieved, timestamp, environment hash, per-claim reproduction outcomes).

**Three-stage review pipeline (§5.3, Fig. 9), CI/CD-style:** Stage 1 Conceptual Verification (minutes; Level 1 + Level 2), Stage 2 Empirical Verification (hours–days; Level 3), Stage 3 Human Review (days–weeks; significance/novelty/taste only).

**How the Rigor Auditor works (§7.5 + App. H.2.2):** a Claude Code SDK agent given only the artifact directory (manifest + source PDF withheld). It parses claims/experiments/heuristics/gaps/exploration-tree nodes; builds claim–experiment, claim–dependency, and rejected-node maps; scores the six dimensions (D1 evidence relevance, D2 falsifiability, D3 scope calibration, D4 argument coherence, D5 exploration integrity, D6 methodological rigor) on 1–5 anchors; emits severity-labeled findings and an overall grade.

---

## FACTS TABLE (exhaustive — value/finding | exact location | context)

### Headline / abstract
| Value / finding | Location | Context |
|---|---|---|
| QA accuracy **72.4% → 93.7%** | Abstract (p.1); Table 3 "Overall" row; PAPER.md abstract (App. A.3.1) | Understanding eval, ARA vs baseline, on PaperBench+RE-Bench |
| Reproduction success **57.4% → 64.4%** | Abstract; §7.3; Table 11 "Mean" | difficulty-weighted success rate, ARA vs baseline |
| On RE-Bench's **five** open-ended extension tasks, preserved failure traces accelerate progress but "can also constrain a capable agent from stepping outside the prior-run box depending on the agent's capabilities" | Abstract; §7.4 | Extension result is mixed / capability-dependent |

### §1 Introduction quantitative claims
| Value / finding | Location | Context |
|---|---|---|
| **24,008** agent runs across **21** frontier models on RE-Bench | §1 (p.2); Table 2; App. E.3 | METR eval-analysis-public dataset (Wijk et al. 2025) |
| Failed runs = **90.2%** of total dollar cost, **59.2%** of tokens | §1 (p.2); App. E.3 (Table 10) | cost of discarded exploration |
| Median failed-to-success token ratio **113×** | §1; App. E.3 (Table 10) | per-run cost of rediscovery |
| **8,921** expert-annotated reproduction requirements across **23** ICML 2024 papers | §1 (p.2); Table 2; Fig. 3 | PaperBench (Starace et al. 2025) |
| Only **45.4%** are fully specified in source PDF | §1; §7.1; Fig. 3; Table 8; App. A.3.3 (O4) | headline info-gap figure |
| Code development most underspecified category, **37.3% sufficient** | §1 (p.2); Table 8 | per-category sufficiency |
| Missing hyperparameters alone = **26.2%** of all gaps | §1 (p.2); Fig. 3b; Table 9 | gap-type distribution |
| LLM adoption associated with paper-production increases of **23.7%–89.3%** across fields | §1 (p.2) | cites Kusumegi et al. 2025 |

### Fig. 3 / Table 8 — information sufficiency by task category (of 8,921 reqs)
| Category (n) | Sufficient | Partial | Absent | Location |
|---|---|---|---|---|
| Code Development (3,942) | 37.3% | 54.9% | 7.8% | Fig. 3a; Table 8 |
| Code Execution (4,355) | 50.5% | 47.9% | 1.6% | Fig. 3a; Table 8 |
| Result Analysis (624) | (per Fig.: ~45.4%/50.2%/4.4% region — see note) | | | Fig. 3a |
| **Overall (8,921)** | **45.4%** | **50.2%** | **4.4%** | Fig. 3a; Table 8 (line ~2216) |

### Fig. 3b / Table 9 — gap type distribution (of 8,921)
| Gap type | Share | count (Table 9) | Location |
|---|---|---|---|
| Missing hyperparameter | 26.2% | 2,558 | Fig. 3b; Table 9 |
| Vague description | 21.9% | — | Fig. 3b; Table 9 |
| Cross-reference only | 13.4% | — | Fig. 3b |
| Missing code detail | 10.9% | 1,064 | Fig. 3b; Table 9 |
| Missing baseline detail | 10.8% | — | Fig. 3b |
| Missing URL | 5.5% | — | Fig. 3b |
| Figure only | 5.1% | — | Fig. 3b |
| Ambiguous specification | 4.1% | 399 | Fig. 3b; Table 9 |
| Implicit assumption | 1.5% | — | Fig. 3b |

### §7.2 Understanding / Table 3 (450 paired outcomes; Claude Sonnet 4.6 answerer, Claude Opus 4.6 ternary judge 1.0/0.5/0.0)
| Category | n | ARA acc | BL acc | ARA tok (K/Q) | BL tok (K/Q) | Location |
|---|---|---|---|---|---|---|
| A: Fidelity (both) | 300 | 95.6 | 80.8 | 84.6 | 88.5 | Table 3 |
| — A PaperBench | 230 | 96.7 | 89.8 | 86.3 | 97.7 | Table 3 |
| — A RE-Bench | 70 | 92.1 | 51.4 | 79.0 | 58.2 | Table 3 |
| B: Detail (PaperBench) | 115 | 92.6 | 67.8 | 183.0 | 178.3 | Table 3 |
| C: Failure (RE-Bench) | 35 | 81.4 | 15.7 | 139.3 | 58.0 | Table 3 |
| **Overall** | **450** | **93.7** | **72.4** | 114.0 | 109.1 | Table 3 |

- **450 questions = 15 per target × 30 targets** (23 PaperBench papers + 7 RE-Bench tasks). Cat A = 10/target (both benchmarks); Cat B = 5/PaperBench paper; Cat C = 5/RE-Bench task. | §7.2 Setup
- Overall +21.3%; per-category gaps: **Cat A +14.8%** (12% fewer tokens), **Cat B +24.8%** (comparable tokens), **Cat C +65.7%**. | §7.2 Results
- Token scaling on ARA: 61K (explicit) / 96K (scattered) / 153K (implicit-failure); baseline flat 83K–118K. | §7.2 (App. E.4 gives 60.9K/95.5K/152.7K; baseline 82.8K–118.2K)
- **McNemar χ² = 95.15, p < 10⁻¹⁰**; ARA correct on **141** questions baseline misses; baseline correct on **18** ARA misses. | App. E.5
- Difficulty tiers: **T1 explicit** ARA 97.3% / BL 83.8% (n=74); **T2 scattered** ARA 95.6% / BL 79.0% (n=193); **T3 implicit** ARA 91.0% / BL 60.5% (n=172); **unanswerable** (n=26) ARA 92.3% vs BL 86.5% abstention. | App. E.4
- Benchmark split: PaperBench (n=345) ARA 95.4% vs BL 82.5%; RE-Bench (n=105) ARA 88.6% vs BL 39.5%. | App. E.4

### §7.3 Reproduction
| Value / finding | Location | Context |
|---|---|---|
| **15** PaperBench papers, **10** tasks each = **150** tasks, **1,743** rubric requirements | §7.3; App. F.1 | task curation |
| Difficulty split: **50 easy, 49 medium, 51 hard** | §7.3; App. F.1 | stratification |
| Per-paper: 5–15 rubric leaves; ≥3 easy/≥3 medium/≥3 hard | App. F.1 | task design |
| Difficulty-weighted (1:2:3): **ARA 64.4% vs BL 57.4%** | §7.3; Table 11 Mean | primary metric |
| Win/tie/loss across papers **8/5/2** | §7.3; App. F.1 | per-paper outcome |
| Per-difficulty: easy 85.1% vs 80.2% (**+4.9%**); medium 68.5% vs 62.9% (**+5.6%**); hard 54.5% vs 46.0% (**+8.5%**) | Fig. 11; App. F.2 | advantage widens monotonically with difficulty |
| Wilcoxon signed-rank **p = 0.028**; sign pattern 8–2 **p = 0.039** (exact binomial) | App. F.1 | significance |
| Budgets: 14–20M tokens/paper (cache reads discounted to 10%); expected numbers masked as [X]%; blinded Opus 4.6 judge yes/partial/no | §7.3 Protocol | setup |
| Largest ARA wins: **fre +21.3%, mechanistic-understanding +20.7%, pinn +19.5%** | App. F.2 | (main text §7.3 lists fre/mechanistic-understanding/pinn as largest) |
| fre ARA: reimplemented JAX→PyTorch (**1.8 GB GPU vs JAX's 30.8 GB**), trained **17 models** across 3 domains, completed all med/hard; baseline completed only **3 training attempts** | §7.3; App. F.2 | case study |
| Baseline win: **self-expansion (−7.3%)** — the ARA agent fabricated results (identical accuracy across configs), caught by blinded judge | §7.3; App. F.2 | one clear baseline win |
| Fabrication across all 15 papers: **2 baseline runs (bbox, mechanistic-understanding) + 1 ARA run (self-expansion)** | §7.3; App. F.2 | "structured artifacts reduce but do not eliminate" |
| Narrow ties: adaptive-pruning (−2.3%), rice (−1.9%); rice ARA matched quality with 2.5× less compute (3.7h vs 9.1h, 131K vs 195K tok) | App. F.2 | ties on papers with strong repos |

Table 11 full per-paper (14 papers listed) Mean: easy 85.1/80.2, med 68.5/62.9, hard 54.5/46.0, weighted **ARA 64.4 / Base 57.4**. (Note: main text says "15 papers," Table 11 lists 14 rows + Mean.)

### §7.4 Extension (RE-Bench)
| Value / finding | Location | Context |
|---|---|---|
| **5 of 7** RE-Bench tasks used: triton_cumsum, restricted_mlm, fix_embedding, nanogpt_chat_rl, rust_codecontests | §7.4; App. G.1 | task selection |
| Excluded: optimize_llm_foundry (no MALT corpus), small_scaling_law (sparse MALT, no Claude-4 entries) | §7.4; App. G.1 | why excluded |
| **59.2%** of agent tokens (and **90.2%** of dollar cost) on RE-Bench spent on dead-end exploration | §7.4 | restates §1/E.3 |
| Harness: Claude Agent SDK, tools {Bash, Read, Edit, Write, Glob, Grep}, **8 h SLURM wall-clock + $50 API-spend cap** per run | §7.4 Protocol | |
| All 5 tasks on Sonnet 4.6; triton_cumsum + restricted_mlm also on **Sonnet 4.5** | §7.4 | base-model comparison |
| ARA ends with better best score on **rust_codecontests, nanogpt_chat_rl, fix_embedding**; paper agent ends ahead on **triton_cumsum, restricted_mlm** (Sonnet 4.6) | §7.4 Results; Fig. 12 | mixed outcome |
| ARA reaches useful first move earlier on **all five** tasks | §7.4 | "early acceleration" |
| Sonnet 4.5 inverts: ARA **0.27** vs paper **0.64** on triton_cumsum; ARA **0.73** vs paper **1.03** on restricted_mlm | §7.4; App. G.6 (Figs. 14,15) | weaker base → ARA wins these two |
| Example timings: rust_codecontests ARA commits at t=9 min (H12) vs paper agent notices same idea at t=395 min | §7.4 | trace head-start |

### §7.5 / Table 4 — Rigor Auditor (Level 2) mutation benchmark
Corpus: **23 PaperBench ARAs that pass Level 1 × 5 injection types = 115 mutations** (one injection per type per ARA). Manifest hidden from auditor. Each injection is its own oracle; scored strictly on whether auditor surfaces the seeded defect as a finding.

| Injection type | Expected severity | n | Detected | Location |
|---|---|---|---|---|
| Fabricated claim | Critical | 23 | **23 (100%)** | Table 4; Table 14 |
| Rebutted-branch leak | Critical | 23 | **23 (100%)** | Table 4; Table 14 |
| Over-claim (scope) | Major | 23 | **23 (100%)** | Table 4; Table 14 |
| Missing falsification | Major | 23 | **21 (91%)** | Table 4; Table 14 (misses: bam C02, bbox C04) |
| Orphan experiment | Minor | 23 | **5 (22%)** | Table 4; Table 14 |
| **Overall** | — | **115** | **95 (82.6%)** | Table 4 |

- **Blind spot = orphan experiments (5/23, 22%)**; attributed to the auditor's claim-centric traversal (never enumerates experiments lacking an inbound `Verifies` edge). Suggested fix: move orphan detection into Level 1 as a deterministic structural check. | §7.5; App. H.2.2
- **LLM-as-judge pathology 1 — grade inflation:** in **17 of 23** ARAs the auditor's reported overall mean is rounded up just enough to clear the Accept threshold. | §7.5
- **LLM-as-judge pathology 2 — finding–score decoupling:** on **22 of 23** rebutted-branch-leak cases correctly flagged critical (D5), the corresponding dimension score does not drop to the rubric-prescribed level (auditor still assigns D5 ∈ {3,4} where anchors prescribe 1 or 2). | §7.5; App. H.2.2
- Lesson drawn: LLMs should generate findings, with overall verdict computed deterministically from the findings list. | §7.5

### Level 1 (App. H.2.1)
| Value / finding | Location | Context |
|---|---|---|
| All **23 PaperBench + 7 RE-Bench = 30** ARAs converge to a Level-1 pass within **≤3 iterations** of the generate–validate–fix loop | App. H.2.1 | Compiler convergence |
| **First-iteration pass rate = 0/30** (all require ≥1 feedback round) | App. H.2.1 | "non-trivial filter, not a rubber stamp" |
| Level-1 failure distribution: dangling cross-layer references **42%**, missing schema fields **31%**, insufficient node counts **14%**, YAML/frontmatter parse errors **8%**, missing mandatory files **5%** | App. H.2.1 | |
| Level 3 verification rate = the same **64.4%** difficulty-weighted reproduction rate (§7.3) | §7.5; App. H.2.3 | Level 3 ≡ Reproduction eval |

### App. E.2 / E.3 detailed breakdowns
| Value / finding | Location | Context |
|---|---|---|
| Below-reference exploration total: **59.2% of tokens / 90.2% of dollar cost ($63,483 total)** | Table 10; App. E.3 | 24,008 runs, 21 models, 228 tasks |
| Below-reference run rate: overall **31.6%**, RE-Bench **73.4%** | Table 10 | |
| Cost split: dead-end exploration **44.8%**, re-derivation of known solutions **14.4%** (of tokens) | Table 10 | |
| Classic hyperparameters = only **17.2%** of leaf requirements; remaining **82.8%** are eval protocols/experiment matrices/tricks | App. A.1.2 | "hyperparameters necessary but not sufficient" |
| Largest single category = combinatorial cross-product of models/datasets/configs = **24.1%** | App. A.1.2 | |
| Dataset Acquisition only **5.4% sufficient** (25.5% entirely absent); Evaluation/Metrics **30.0%** sufficient | App. E.2 | fine-grained coverage |
| Info-category shares (of 10): Mathematical formulation **4.5%**, Implementation tricks **4.2%**, Data pipeline **3.8%**, Environment/infrastructure **2.9%** | App. A.1 (§7 categories) | |

### Related-Work quantitative characterizations (ARA paper's claims ABOUT other works — relevant for citation audit)
| Claim as stated | Location | Cited work |
|---|---|---|
| "EXP-Bench reports only **0.5% end-to-end experiment success despite 20–35% component accuracy**" | §8 Related Work | Kon et al. 2025 (EXP-Bench) |
| "LLMs detect **fewer than 46%** of paper–code discrepancies" | §8 | Baumgärtner & Gurevych 2026 |
| "even the strongest LLMs implement **fewer than 40%** of novel contributions correctly, with semantic misalignment as the dominant failure mode" | §8; App. A.3.3 (O3, cites ResearchCodeBench/Hua et al. 2025) | Jimenez 2024; Chen 2025; Hua 2025 |
| knowledge-graph approaches "yielding up to **10.9% PaperBench gains**" | §8 | Liu 2026b; Luo et al. 2025 |
| large-scale experiment logs "retain **>99.99% more search history** than their corresponding papers report" | §8 | Pineda Arango 2021; Ying 2019; Gijsbers 2019 |

### App. A.3 — "this paper's own ARA" (internal artifact; note internal inconsistencies)
| Value / finding | Location | Note |
|---|---|---|
| Claims: **16 falsifiable claims** | A.3.1 directory (`claims.md # 16`), Layer Index, A.3.7 ("all 16 claims") | consistent = 16 |
| Heuristics: **23** (directory listing / Layer Index) BUT **18** ("18 heuristics total"; "all 18 heuristics") | A.3.1 vs A.3.4/A.3.7 | INTERNAL INCONSISTENCY (23 vs 18) |
| Exploration tree: **114-node decision DAG** (directory, Layer Index) BUT **94-node tree** ("94-node tree", "94 nodes total", "94 preliminary observations") | A.3.1 vs A.3.5/A.3.7 | INTERNAL INCONSISTENCY (114 vs 94) |
| Sessions: **38 session logs** (directory, Layer Index) BUT **36 sessions** ("all 36 sessions", "36 session records") | A.3.1 vs A.3.6/A.3.7 | INTERNAL INCONSISTENCY (38 vs 36) |
| 94 unpromoted/staged observations in `staging/observations.yaml` | A.3.1 | |
| PAPER.md frontmatter: title "Agent-Native Research Artifacts", authors ["Amber Liu","Zechen Zhang"], venue "NeurIPS 2026", status draft, date_created 2026-03-12, last_updated 2026-04-27 | A.3.1 | |

---

## Scope & explicit limitations (§10 Limitations)
1. **Evaluation scope:** study covers **only machine-learning papers**. Whether ARA generalizes to experimental sciences with physical execution, or theoretical disciplines where the Physical Layer is largely absent, is "empirically untested." Human-annotated benchmark built by annotators familiar with both the ARA format and the selected papers, so performance on unfamiliar/niche-domain artifacts "may differ from the reported figures."
2. **Fidelity ceiling:** "ARA fidelity is bounded by the source of supervision." The Compiler represents only what the PDF contains; omitted details cannot be recovered by any extraction method. The Live Research Manager closes this but assumes an AI-native workflow with a coding agent present throughout. For researchers outside such sessions, the Compiler's artifact inherits the PDF's omissions; hand-authoring reintroduces the documentation burden.
3. **Deployment prerequisites (not yet implemented):** adversarial robustness and privacy guarantees are "aspirational" — the current system lacks sandboxed execution, content-level anomaly detection, and granular access control for the Exploration Graph. Schema evolution / stable migration for major revisions (auto-rewriting archival artifacts, long-term checker availability, deprecation policy) remains future work.

Additional in-body scope notes: ARA's design "extends to any digitalised research whose contribution can be expressed as code, configurations, and grounded data, including computational social science, economics, and dry-lab biology"; **physical-world interventions (wet-lab biology, materials synthesis) fall outside scope until the experimental record is digitalised** (§7.1).

## Does NOT claim / boundaries
- Does **not** claim full-scale exact-number reproduction; Level 3 is explicitly **directional** ("test whether claimed properties hold qualitatively rather than reproducing exact numbers"); full-scale reproduction is optional/post-acceptance/community-driven.
- Does **not** claim to automate the human-judgment (Stage 3) layer — significance/novelty/taste; explicitly states this layer "has no automated oracle and we do not attempt to measure it."
- Does **not** claim the extension benefit is uniform — it is capability-dependent; a preserved trace can **constrain** a more capable agent (paper agent overtakes ARA on 2/5 tasks under Sonnet 4.6). The claimed value "appears to scale with the gap between what the trace documents and what the agent can discover on its own."
- Does **not** claim the Rigor Auditor is complete — documents a 22% orphan-experiment detection blind spot and two LLM-as-judge scoring pathologies (grade inflation, finding–score decoupling).
- Does **not** claim to replace human reviewers — automates "mechanical" checking to redirect expert attention.
- Structured artifacts "reduce but do not eliminate" hallucinated/fabricated results (1 ARA fabrication case remained).
- Number of injection/violation types tested by the mutation benchmark = **5** (fabricated claim, missing falsification, orphan experiment, over-claim, rebutted-branch leak); number of Rigor Auditor scoring **dimensions = 6**. (Do not conflate these two counts.)

## Section map
- **§1 Introduction** — Storytelling Tax & Engineering Tax; motivating stats (24,008 runs / 90.2% cost / 8,921 reqs / 45.4% specified); three trends; existing efforts (FAIR, RO-Crate, nanopubs, AGENTS.md).
- **§2 The ARA Protocol** — 2.1 Design Philosophy ("Knowledge over Narrative"); 2.2 Architecture (four layers).
- **§3 The Live Research Manager** — 3.1 Design Principles (P1 silent/framework-independent, P2 faithful provenance, P3 comprehensive capture); 3.2 System Design (Context Harvester→Event Router→Maturity Tracker; Table 1 seven event types).
- **§4 The ARA Compiler** — 4.1 Design Principles (universal input/canonical output; high-fidelity; knowledge lineage); 4.2 Implementation (top-down 4-stage generation; iterative refinement; source-aware enrichment; collective inference).
- **§5 ARA Verification and Review** — 5.1 Principles (automate mechanical / reproducibility foundational); 5.2 The ARA Seal (Levels 1–3, Fig. 8); 5.3 Three-Stage Review Pipeline (Fig. 9).
- **§6 The (Human+AI)² Research Network** — Fig. 10; /submit, /retrieve, /fork; publishing as Git-like operation.
- **§7 Evaluation** — 7.1 Datasets/Motivation (Table 2); 7.2 Knowledge Extraction (Table 3); 7.3 Reproduction (Fig. 11); 7.4 Extension (Fig. 12); 7.5 ARA-Native Review Systems (Table 4).
- **§8 Related Work** — dimensional gap (Table 5); machine-readable artifacts; reproducibility infra; negative knowledge; agent tooling.
- **§9 Future Work** — near/medium/long term.
- **§10 Limitations** — evaluation scope; fidelity ceiling; deployment prerequisites.
- **§11 Conclusion.**
- **References.**
- **Appendices:** A (protocol/ten categories/physical modes/this paper's own ARA), B (Compiler skill), C (Live Research Manager), D (implementation details, referenced), E (Understanding eval: E.2 gap taxonomy Tables 8–9, E.3 exploration cost Table 10, E.4 per-category mechanism, E.5 stats), F (Reproduction: F.1 design, F.2 per-paper Table 11), G (Extension: G.1–G.6, Figs. 12–15), H (Review system: H.1 Seal validation, H.2.1 Level-1 convergence, H.2.2 Level-2 mutation Table 14, H.2.3 Level-3).

---
*Digest built blind from the paper's own text only; locations cited to section/table/figure and (where useful) the paper's own internal artifact excerpts. Numbers transcribed exactly incl. denominators. Flagged three internal numeric inconsistencies in App. A.3 (heuristics 23 vs 18, tree 114 vs 94 nodes, sessions 38 vs 36) as the paper's own wording.*
