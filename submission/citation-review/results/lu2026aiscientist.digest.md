# Digest: lu2026aiscientist

**Full citation (from PDF):** Chris Lu, Cong Lu, Robert Tjarko Lange, Yutaro Yamada, Shengran Hu, Jakob Foerster, David Ha & Jeff Clune. "Towards end-to-end automation of AI research." *Nature*, Vol. 651, pp. 914–919, 26 March 2026. DOI 10.1038/s41586-026-10265-5. Received 8 July 2025; Accepted 11 February 2026; Published online 25 March 2026. Open access. Affiliations: Sakana AI (Tokyo); FLAIR, University of Oxford; University of British Columbia; Vector Institute. First four authors contributed equally.

> NOTE: This is the peer-reviewed *Nature* (2026) version of "The AI Scientist." It is NOT the 2024 arXiv preprint. Numbers here (e.g., reviewer accuracy, model set, workshop details) are the published-version figures and may differ from the preprint.

---

## Thesis / Problem
Automating science end-to-end has been a long-standing AI ambition, but no system had navigated the *entire* research life cycle from conception to publication. The paper presents **The AI Scientist**, a pipeline that autonomously generates research ideas, writes code, runs experiments, plots/analyses data, writes the full manuscript, and performs its own automated peer review. The central claimed milestone: one fully AI-generated manuscript passed the first round of blind peer review for a workshop at a top-tier ML conference (ICLR 2025 ICBINB). The authors argue paper quality scales with both foundation-model capability and test-time compute, implying future systems will be substantially more capable.

## Method (mechanism)
Two core automated systems working in concert:

**1. The AI Scientist** — an agentic system, run in two modes:
- **Template-based**: given a human-provided starting code template that reproduces a training run of a popular algorithm (e.g., a small transformer on Shakespeare). Three phases: (a) idea generation (LLM as mutation operator growing an idea archive; novelty checked against Semantic Scholar API, up to 10 rounds of literature-search queries; ideas scored on interestingness/novelty/feasibility, each 1–10); (b) experiment execution (multi-step plan of up to 5 experiments, executed sequentially via the Aider coding assistant, with automated debugging — up to 4 reattempt cycles per experiment, 7,200 s timeout per experiment); (c) manuscript generation (Aider fills a LaTeX template; related-work section built via Semantic Scholar API up to 20 search rounds; automatic LaTeX compilation-error correction, up to 5 rounds).
- **Template-free (open-ended)**: no fixed starting codebase. Uses a **parallelized agentic tree search**. An "experiment progress manager" coordinates four stages: (1) preliminary investigation, (2) hyperparameter tuning, (3) research-agenda execution, (4) ablation studies. Each stage runs its own tree search with explicit stopping criteria; each node has a max runtime of 1 h; an LLM evaluator picks the best leaf node to seed the next stage. Node types: buggy/non-buggy, hyperparameter, ablation, replication, aggregation. Plots are critiqued by a vision-language model (VLM). Model assignment: **OpenAI o3** for idea generation + code critique; **Anthropic Claude Sonnet 4** for code generation; **OpenAI GPT-4o** for cost-efficient vision-language tasks + best-first node selection; **OpenAI o4-mini** for cost-efficient reasoning in the review stage. Datasets pulled dynamically from HuggingFace Hub. Manuscript writing via direct LaTeX generation with a reasoning model (e.g., OpenAI o1) + reflection cycles. Full template-free run takes several hours to over 15 h.

**2. The Automated Reviewer** — built on **o4-mini**, adheres to official **NeurIPS reviewer guidelines** (NeurIPS 2022 ReviewerGuidelines). Processes a manuscript PDF; outputs a structured JSON review (summary, strengths, weaknesses, questions, limitations, ethical concerns, numerical scores for soundness/presentation/contribution/overall 1–10/confidence) and an accept/reject decision. Robustness via a **5-review ensemble + meta-review** where an LLM acts as area chair. Validated against real human decisions using ICLR data from the public OpenReview dataset, benchmarked against the NeurIPS 2021 consistency experiment as the inter-human agreement baseline.

## FACTS TABLE (exhaustive)

| Value / finding | Exact location | Context |
|---|---|---|
| Workshop acceptance rate = **70%** | Abstract (p.914); Limitations (p.917) | ICLR 2025 ICBINB workshop acceptance rate. Contrasted with 32% main conference. |
| ICLR 2025 main conference acceptance = **32%** | Limitations (p.917) | Contrast to the 70% workshop rate; supports "workshops have much higher acceptance rates." |
| One AI-generated manuscript **passed first round of peer review** at a top-tier ML conference workshop | Abstract; Human evaluation results (p.916) | Central claimed milestone. Workshop = ICBINB @ ICLR 2025. |
| **3** generated manuscripts submitted to the workshop | Human evaluation (p.916) | All produced without human modification; manually filtered/selected from larger pool. |
| Submissions were among **43 papers** reviewed for the workshop | Human evaluation (p.916) | Denominator for the workshop review pool. |
| **1 of 3** AI papers accepted / met the bar | Human evaluation (p.916); Limitations (p.917) | The other two did not meet the bar (Supplementary Table D9). |
| Accepted paper avg reviewer score = **6.33** (individual scores **6, 7, 6**) | Human evaluation (p.916); Fig. 2 caption | Above avg acceptance threshold. Scores = 6 (weak accept), 7 (accept), 6 (weak accept), before meta-review. |
| Accepted paper ranked in **top 45%** of papers submitted for peer review | Fig. 2 caption (p.916) | Ranking of the accepted AI paper within the workshop pool. |
| Accepted paper reported a **negative result** | Human evaluation (p.916) | Aligned with the ICBINB workshop's focus on interesting negative results. |
| Paper **withdrawn** per pre-established protocol (organizers said it "would have been accepted in all likelihood") | Human evaluation (p.916); Ethics (p.917) | All AI submissions withdrawn after review regardless of outcome. NOT formally published/accepted. |
| Internal team review: **1 met workshop bar, none met main-ICLR-conference bar** | Human evaluation (p.916) | Team of human AI researchers (Supplementary Info C.2). |
| Fit for paper-score vs model-release-date: **R² = 0.517, P < 0.00001** | Fig. 1b caption + figure (p.915) | Extracted text showed "R = 0.517"; the figure confirms it is **R²**. Statistically significant positive correlation. |
| n = **6** template-free points, n = **3** template-based points (Fig 1b) | Fig. 1b caption (p.915) | Replication counts for the model-release-date scaling plot. |
| Fig 1b model set (x-axis, ~July 2023–July 2025) | Fig. 1b (p.915) | GPT-4, Gemini-1.5, Sonnet-3, GPT-4o, Sonnet-3.5, Gemini-2.0, Sonnet-3.7, o1, o3, Sonnet-4, Gemini-2.5. |
| Automated Reviewer balanced accuracy: **69% (pre-cutoff 2017–2024)** vs **66% (post-cutoff 2025)** | Automated evaluation (p.916); Fig. 1c | Drop of 69%→66% attributed to *possible* data contamination; effect deemed "at most minimal." |
| Human reviewer balanced accuracy = **66%** (0.66) | Table 1 (p.915) | NeurIPS 2021 consistency experiment baseline. |
| Automated Reviewer "comparable balanced accuracy with humans (**69% vs 66%**)" | Methods, Validation (p.919) | HERE 69% = Automated Reviewer (pre-cutoff), 66% = Human. DISTINCT from the 69%→66% contamination comparison (which is automated pre vs automated post). Both comparisons coincidentally involve "66%." |
| Automated Reviewer F1 = **0.62** vs inter-human F1 = **0.49** | Methods, Validation (p.919); Table 1 | Automated reviewer higher F1 than inter-human group agreement (NeurIPS 2021). |
| **Table 1 — Human (NeurIPS):** BA 0.66, Acc 0.73, F1 0.49, AUC 0.65, FPR 0.17, FNR 0.52 | Table 1 (p.915) | Human reviewer consistency baseline (NeurIPS 2021 consistency experiment). |
| **Table 1 — Automated Reviewer, pre-cutoff (2017–2024):** BA 0.69±0.04, Acc 0.65±0.10, F1 0.62±0.09, AUC 0.69±0.09, FPR 0.45±0.10, FNR 0.17±0.08 | Table 1 (p.915) | Error margins = 95% bootstrapped CIs. |
| **Table 1 — Automated Reviewer, post-cutoff (2025):** BA 0.66±0.03, Acc 0.63±0.09, F1 0.67±0.09, AUC 0.65±0.10, FPR 0.52±0.10, FNR 0.17±0.07 | Table 1 (p.915) | "Clean" data after knowledge cutoff. |
| **Table 1 — Random decision (pre-cutoff):** BA 0.50, Acc 0.54, F1 0.47, AUC 0.52, FPR 0.47, FNR 0.43 | Table 1 (p.915) | Baseline. |
| **Table 1 — Always reject (pre-cutoff):** BA 0.50, Acc 0.65, F1 0.00, AUC 0.50, FPR 0.00, FNR 1.00 | Table 1 (p.915) | Baseline. |
| **Table 1 — Random decision (post-cutoff):** BA 0.52, Acc 0.51, F1 0.48, AUC 0.49, FPR 0.50, FNR 0.48 | Table 1 (p.915) | Baseline. |
| **Table 1 — Always reject (post-cutoff):** BA 0.50, Acc 0.56, F1 0.00, AUC 0.50, FPR 0.00, FNR 1.00 | Table 1 (p.915) | Baseline. |
| Contamination test datasets: **1,000 papers (2017–2024)** potentially in training + a "clean" **2025** dataset | Automated evaluation (p.916) | Design to test data contamination in reviewer decisions. |
| Automated review = **5-run ensemble**; error bars = **95% bootstrapped CIs, 5,000 replicates** | Fig. 1c caption (p.915) | Reviewer robustness / statistics setup. |
| z-tests on subsampled accuracy (automated n = **698/876**, human n = **412**): no significant difference pre-cutoff **P = 0.319**, post-cutoff **P = 0.921** | Fig. 1c caption (p.915) | Two-sample z-tests. |
| Non-parametric bootstrap on F1 scores: automated **outperformance, P < 0.001** | Fig. 1c caption (p.915) | Automated reviewer significantly better F1. |
| More test-time compute → higher paper quality (Fig. 3c) | Intro (p.914); Fig. 3c (p.917) | Scaling number of experimental tree-search nodes improves scores. n = 30 per compute point; scores ~3.2–4.0 across 5–30 nodes. |
| NeurIPS 2021 consistency experiment: ~**10%** of submissions randomly sent to **two independent review committees** | Methods, Validation (p.919) | Inter-reviewer consistency benchmark used as human baseline. |
| Idea self-assessed scores: interestingness, novelty, feasibility, each on a **1–10 scale** | Methods, Template-based (p.918) | Structured idea object attributes. |
| Novelty check: up to **10 rounds** of literature-search queries | Methods, Template-based (p.918) | Semantic Scholar API. |
| Experiment execution: plan of up to **5 experiments**; debugging up to **4 reattempt cycles**; **7,200 s** timeout per experiment | Methods, Template-based (p.918) | Template-based execution parameters. |
| Related-work / citation section: up to **20 search rounds** on Semantic Scholar API | Generating manuscripts (p.915); Methods (p.918) | Citation construction; per-citation textual justification generated. |
| LaTeX compilation error correction: up to **5 rounds** | Methods, Template-based (p.918) | Template-based manuscript compilation. |
| Template-free node max runtime = **1 h**; full run **several hours to >15 h** | Methods, Template-free (p.918–919) | Compute/time budget. |
| Stage-2 stopping: convergence in training curves + successful execution across **at least two datasets** | Methods, Template-free (p.918) | Progress-manager stopping criteria. |
| "Length of tasks AI can reliably complete is doubling every **7 months**" | Limitations (p.917) | Cited from METR (ref. 40); used to argue rapid future improvement. |
| Model roles (template-free): o3 = ideation/critique; Claude Sonnet 4 = code gen; GPT-4o = VLM/vision + node selection; o4-mini = review-stage reasoning | Methods, Template-free (p.918); Automated Reviewer (p.919) | Explicit per-component model assignment. |
| IRB / ethics protocol number = **H24-02652** (University of British Columbia) | Discussion (p.917); Ethics approval (p.919) | UBC Behavioral Research Ethics Board. |
| Code: template-based + reviewer at github.com/SakanaAI/AI-Scientist; template-free at github.com/SakanaAI/AI-Scientist-v2 (Apache 2.0) | Code availability (p.919) | Public repos. |

## Scope & explicit limitations
- **Computational ML experiments only** — the system currently conducts experiments entirely on the computer; extension to wet-lab / automated chemistry labs is future work.
- Peer-review success is at a **workshop** (explicitly a lower bar than the main conference), and only **1 of 3** submissions met that bar; the accepted paper was **withdrawn** and never formally published.
- The system **cannot yet meet top-tier publication standards, nor even do so consistently for workshops.**
- Common failure modes explicitly listed: naive/underdeveloped ideas, incorrect implementation of the main idea, lack of deep methodological rigour, experimental-implementation errors, **duplicating figures between main text and appendix**, and hallucinations including **inaccurate citations**.
- Known AI weaknesses acknowledged: easily fooled, overconfidently wrong (hallucinations), though progress is being made.
- ICLR-vs-NeurIPS reviewer comparison is "not exact" — different submission pools (distribution shift); authors justify it as the only feasible comparison (ICLR is the only main ML conference releasing all accept/reject decisions; NeurIPS 2021 is the only modern human consistency experiment).
- Ethical/societal risks flagged: overwhelming peer review, inflating research credentials, repurposing others' ideas without credit, eliminating scientist jobs, unethical/dangerous experiments.

## Does NOT claim / boundaries
- Does **NOT** claim a fully AI-generated paper was formally *published* or *accepted into the archival record* — it passed review at a workshop and was withdrawn by protocol; organizers only said it "would have been accepted in all likelihood."
- Does **NOT** claim main-conference-level quality; explicitly states none of the three papers met the main ICLR conference bar.
- Does **NOT** claim the Automated Reviewer beats humans across the board — it claims *comparable* balanced accuracy and *superior* F1 vs inter-human agreement; on some metrics (e.g., FPR) it is worse than humans (Table 1: automated FPR 0.45–0.52 vs human 0.17).
- Does **NOT** claim data contamination was ruled out — it claims contamination *may exist* (69%→66% drop) but had "at most, a minimal effect."
- Does **NOT** claim consistency/reliability — repeatedly frames current results as a first step whose value depends on projected future improvement.
- The **70% figure is specifically the ICLR 2025 ICBINB workshop acceptance rate**, not a general workshop rate and not the AI system's own success rate.

## Section map
- **Abstract** (p.914)
- **Intro** (untitled opening, p.914) — history of automated science; overview of contributions; Automated Reviewer + compute/model scaling claims.
- **Generating manuscripts** (p.915) — four-phase pipeline; template-based vs template-free; citation/related-work construction.
- **Automated evaluation of generated papers** (p.915–916) — Automated Reviewer design, Table 1, OpenReview validation, contamination test, model/compute scaling (Fig 1b, 3c).
- **Human evaluation results** (p.916) — "AI scientist Turing test," 3 submissions to ICBINB@ICLR 2025, 6.33 score, top 45%, withdrawal protocol, internal review.
- **Limitations** (p.917) — 70% vs 32% acceptance rates, failure modes, task-length doubling (7 months), AI weaknesses.
- **Discussion / ethics** (p.917) — societal risks, IRB permissions, safe open-ended AI.
- **Online content / References 1–48** (p.918)
- **Methods** (p.918–919): The AI Scientist (foundational tech; template-based; template-free with progress manager, tree search, node types, VLM, dataset access, manuscript writing); The Automated Reviewer (review process, validation); Ethics approval; Data availability; Code availability; References 49–64.
- **Fig. 1** (p.915): a=workflow, b=score vs model-release-date (R²=0.517), c=automated vs human balanced accuracy.
- **Table 1** (p.915): human vs automated reviewer metrics, pre/post cutoff.
- **Fig. 2** (p.916): accepted AI paper sections; scores 6/7/6, top 45%.
- **Fig. 3** (p.917): a=four-stage experimentation, b=example tree search, c=compute scaling (n=30/point).
