# Digest: si2024novelideas (BLIND first-pass)

**Full title:** "Can LLMs Generate Novel Research Ideas? A Large-Scale Human Study with 100+ NLP Researchers"
**Authors:** Chenglei Si, Diyi Yang, Tatsunori Hashimoto (Stanford University)
**Venue/ID:** arXiv:2409.04109v1 [cs.CL], 6 Sep 2024 (94 pages incl. appendices)
**Code/data:** https://github.com/NoviScl/AI-Researcher

---

## Thesis / Problem

Prior work proposes LLM "research agents" that autonomously generate and validate ideas, but **no evaluation had shown that LLMs can take the very first step of producing novel, expert-level research ideas**, let alone the whole research process. The paper addresses this with an experimental design that performs the **first head-to-head comparison between expert NLP researchers and an LLM ideation agent**, controlling for confounders. Central question: are current LLMs capable of generating novel ideas comparable to expert humans?

**Headline finding:** LLM-generated ideas are judged **more novel (p < 0.05)** than human expert ideas, while judged **slightly weaker on feasibility**. This is presented as "the first statistically significant conclusion on current LLM capabilities for research ideation."

## Method (directly answers team-lead questions)

- **Large-scale HUMAN STUDY: YES.** Recruited **over 100 highly qualified NLP researchers**. N=49 experts wrote ideas; N=79 experts wrote blind reviews; 24 people did both -> **N=104 total unique participants**. Collected **N=298 unique reviews** ("nearly 300 reviews").
- **Establishes idea-QUALITY BASELINE: YES.** Provides a controlled human expert baseline and standardized evaluation protocol; the concrete result is LLM ideas rated **more novel than human expert ideas**. Positioned as a foundation/baseline for future methods work.
- **Full discovery LOOP: NO — idea generation + human evaluation ONLY.** Explicitly evaluation-centric. Idea *execution* into full projects is Phase II / future work (a sign-up study). An execution agent WAS attempted (Appendix Y) but found **unreliable** (agent skips/modifies steps, mis-defines metrics) and left to future work. Paper repeatedly frames ideation as "only one part of the research process" and "the very first step."
- **3 experiment conditions**, each with 49 ideas: (1) **Human Ideas** (expert-written); (2) **AI Ideas** (top LLM-ranked); (3) **AI Ideas + Human Rerank** (first author manually reranked LLM outputs).
- **LLM ideation agent** = minimalist design, 3 components: (a) paper retrieval for RAG via Semantic Scholar API; (b) idea generation (overgenerate 4000 seed ideas/topic); (c) idea ranking (Swiss-tournament pairwise). Backbone model: **claude-3-5-sonnet-20240620**.
- **7 research topics** (from NLP CfP e.g. COLM): Bias, Coding, Safety, Multilingual, Factuality, Math, Uncertainty. All ideas restricted to **prompting-based NLP research**.
- **Confounder controls:** shared template (title/problem/motivation/method/experiment plan/test cases/fallback), matched topic distribution, and an **LLM style-normalization module** (human judges only 50% accuracy distinguishing AI vs human ideas after normalization).
- **Statistics:** three tests — (1) each review as datapoint, (2) each idea as datapoint (N=49/condition), (3) each reviewer as datapoint — plus linear mixed-effects models (Appendix N). Two-tailed Welch's t-tests with Bonferroni correction. Novelty result significant across all.

---

## FACTS TABLE (exhaustive)

### Headline novelty scores
| Value | Location | Context |
|---|---|---|
| 4.84 | Fig 1, Table 7 | Human Ideas novelty (Test 1, per-review); µ=4.84, σ=1.79, N=119 |
| 5.64 | Fig 1, Table 7 | AI Ideas novelty (Test 1); µ=5.64, σ=1.76, N=109, p=0.00** |
| 5.81 | Fig 1, Table 7 | AI Ideas + Human Rerank novelty (Test 1); µ=5.81, σ=1.66, N=109, p=0.00*** |
| p < 0.05 | Abstract/Fig 1/2 | AI ideas judged more novel than human ideas (headline) |
| p < 0.01 | Sec 5.1 | Both AI conditions vs Human on novelty (Test 1 significance level) |

### Participants & scale
| Value | Location | Context |
|---|---|---|
| 100+ | Title, Sec 1 | "over 100 highly qualified NLP researchers" recruited |
| 49 | Sec 4.1 | N idea writers |
| 79 | Sec 4.1 | N reviewers |
| 24 | Sec 4.1 | reviewers who also wrote ideas (overlap) |
| 104 | Sec 4.1 | total unique participants across both tasks |
| 298 | Sec 4.1 / 4.4 | unique reviews collected ("nearly 300") |
| 26 | Sec 4.2, Table 15 | institutions of idea writers |
| 32 | Sec 4.2, Table 16 | institutions of reviewers |
| 1426 | Sec 4.1 | NLP researchers in OpenNLP Slack (recruitment channel) |
| 71 | Sec 4.1 | institutions in OpenNLP Slack |
| 74246 | Sec 4.1 | Stanford IRB ID |
| $300 | Sec 4.1 | compensation per idea |
| $1000 | Sec 4.1 | bonus for top-5 ideas |
| $25 | Sec 4.1 | compensation per review |
| 10 days | Sec 4.1 | time to write one idea |
| 1 week | Sec 4.1 | time to finish reviews |
| 2 to 7 | Sec 4.1 | reviews assigned per reviewer |
| 2 to 4 | Sec 4.4 | reviewers per idea |
| 3.8 | Table 5/6 | avg reviews per reviewer |

### Reviewer/writer qualifications (Table 2)
| Value | Location | Context |
|---|---|---|
| 12 papers / 477 citations / h-index 5 | Table 2 | idea writers (mean, N=49) |
| 15 papers / 635 citations / h-index 7 | Table 2 | reviewers (mean, N=79) |
| 72 of 79 | Sec 4.2 | reviewers who previously reviewed for major AI venues/journals |
| 36 PhD / 9 Master (of 49) | Table 13 | idea-writer positions (majority PhD) |
| 63 PhD / 7 Postdoc (of 79) | Table 14 | reviewer positions |

### Idea statistics (Table 3)
| Value | Location | Context |
|---|---|---|
| 901.7 words | Table 3 | Human idea length (mean) |
| 1186.3 words | Table 3 | AI idea length (mean) |
| 1174.0 words | Table 3 | AI + Human Rerank length (mean) |
| 5.5 hours | Table 3 | mean time humans spent per idea |
| 3.7 (of 5) | Table 3 | human writers' familiarity with topic |
| 3.0 (of 5) | Table 3 | task difficulty |
| 43% | Sec 6.1 | avg self-reported percentile of submitted idea vs writer's past ideas ("median-level") |
| 37 of 49 | Sec 6.1 | writers who came up with idea on the spot |
| 50 collected, 1 filtered | Appendix J | N=50 originally, 1 excluded as paraphrase -> N=49 |

### Agent / pipeline internals
| Value | Location | Context |
|---|---|---|
| claude-3-5-sonnet-20240620 | Sec 3.1 | backbone model for the agent |
| k=20 | Sec 3.1 | papers kept per retrieval function call |
| N=120 | Sec 3.1 | max papers retrieved |
| 1-10 scale | Sec 3.1 | paper reranking score |
| 4000 | Sec 3.2 | seed ideas generated per topic |
| k=6 | Sec 3.2 | demonstration examples (manually summarized) |
| k=10 | Sec 3.2 / Appendix F | papers randomly selected for RAG (from top-20) |
| 0.8 | Sec 3.2 / 7.1 | cosine-similarity dedup threshold (all-MiniLM-L6-v2, Sentence-Transformers) |
| ~5% | Sec 3.2 | non-duplicated ideas out of all seed ideas |
| 200 | Sec 7.1 | non-duplicate unique ideas out of 4000 seed ideas |
| ~1% | Appendix F | proposals filtered out by novelty/feasibility checks |

### Idea ranking / ICLR proxy (Table 1)
| Value | Location | Context |
|---|---|---|
| 1200 (1.2K) | Sec 3.3 | ICLR 2024 LLM-related submissions scraped for ranker + agreement baselines |
| 71.4% | Sec 3.3 | Claude-3.5-Sonnet zero-shot pairwise accuracy (accept prediction) |
| 61.1% | Sec 3.3 | GPT-4o pairwise accuracy |
| 63.5% | Sec 3.3 | Claude-3-Opus pairwise accuracy |
| N=5 | Sec 3.3 | Swiss-tournament rounds chosen |
| 17 of 49 (text) / 18 (Table 12) | Sec 3.3, Appendix I | overlap between AI+Human Rerank and AI conditions — **INTERNAL INCONSISTENCY: prose says 17 overlap / 32 different; Table 12 totals say 18 overlap / 31 new** |

### Reviewer-agreement / LLM-as-judge (Table 11)
| Value | Location | Context |
|---|---|---|
| 56.1% | Sec 6.3, Table 11 | our inter-reviewer agreement (balanced accuracy) |
| 66.0% | Sec 6.3, Table 11 | NeurIPS 2021 consistency experiment baseline |
| 71.9% | Sec 6.3, Table 11 | ICLR 2024 (1.2K subs) reviewer agreement |
| 50.0% | Table 11 | random baseline / GPT-4o Direct |
| 45.0% | Table 11 | GPT-4o Pairwise |
| 51.7% | Table 11 | Claude-3.5 Direct |
| 53.3% | Table 11, Sec 7.2 | Claude-3.5 Pairwise (best LLM evaluator, still < 56.1% human) |
| 43.3% | Table 11 | "AI Scientist" (Lu et al. 2024) reviewer agent |
| 80 of 298 | Sec 4.4 | reviews that linked existing papers to justify non-novelty |
| 31.7 min | Table 6 | avg time per review |
| 231.9 words | Table 6 | avg review length |

### Metric correlations (Table 10)
| Value | Location | Context |
|---|---|---|
| r=0.725 | Table 10 | Overall–Novelty correlation |
| r=0.854 | Table 10 | Overall–Excitement correlation |
| r<0.1 (0.097) | Table 10 / Sec 6.2 | Overall–Feasibility (almost none) -> reviewers weight novelty/excitement |

### Feasibility trade-off (Test 1, Table 7)
| Value | Location | Context |
|---|---|---|
| 6.61 | Table 7 | Human feasibility (mean) |
| 6.34 | Table 7 | AI feasibility (p=1.00, n.s.) |
| 6.44 | Table 7 | AI+Rerank feasibility (p=1.00, n.s.) — AI slightly lower, not significant |

### Execution agent attempt (Appendix Y, Table 18)
| Value | Location | Context |
|---|---|---|
| 30 + 30 | Appendix Y | safety + factuality ideas tested |
| 17 / 18 | Table 18 | successfully executed (safety/factuality) |
| 13 / 14 | Table 18 | passed style evaluator |
| 5 / 1 | Table 18 | proposed method actually beat baseline — very few |
| claude-3-opus-20240229 | Appendix Y code | model in execution template |

### Phase II / follow-up
| Value | Location | Context |
|---|---|---|
| 23 topics | Sec 10 Q1 | EMNLP 2024 CfP topics used to pre-cache AI ideas for future comparison |
| osf.io/z6qa4 | Sec 10 fn12 | pre-registered analysis plan |

---

## Scope & Limitations (explicit in paper)

- Scope limited to **prompting-based NLP research ideas** across 7 topics (chosen so ideas are cheap to execute in Phase II).
- Ideas evaluated **as written proposals only**, not executed — novelty/feasibility judgments may not predict real project outcomes (acknowledged as "preliminary evaluation").
- Human ideas may be **median-level** (top-43% self-percentile), not experts' best; most generated on the spot within 10 days.
- Reviewing ideas is **inherently subjective** (inter-reviewer agreement 56.1%, below conference reviewing).
- Sample size underpowered to conclusively resolve excitement/overall/feasibility effects.
- **LLMs lack idea diversity** (only ~200 unique of 4000) and **cannot yet reliably evaluate ideas** (LLM-as-judge < human agreement).

## Does NOT claim / boundaries

- Does **NOT** claim LLMs can perform the full research process or an end-to-end autonomous discovery loop — execution is explicitly future work and the execution agent is shown to be unreliable.
- Does **NOT** claim AI ideas are better overall — only **more novel** (and marginally excitement/overall in some tests); feasibility is comparable-to-slightly-lower, not better.
- Does **NOT** claim results generalize beyond prompting-based NLP (conclusions "could be different" in other fields).
- Does **NOT** endorse LLM-as-a-judge for ideas — actively argues against it.

## Section Map

1. Introduction — motivation, headline result, contributions
2. Problem Setup — ideation scope, idea writeup template, review/evaluation design, 3 conditions
3. Idea Generation Agent — 3.1 RAG paper retrieval, 3.2 idea generation (4000 seeds), 3.3 idea ranking (Swiss tournament)
4. Expert Idea Writing and Reviewing — 4.1 recruitment, 4.2 qualifications, 4.3 idea writing, 4.4 idea reviewing
5. Main Result — 5.1 Test 1 (per review), 5.2 Test 2 (per idea), 5.3 Test 3 (per reviewer)
6. In-Depth Analysis — 6.1 human best-idea question, 6.2 novelty/excitement focus, 6.3 subjectivity/agreement
7. Limitations of LLMs — 7.1 lack of diversity, 7.2 unreliable evaluation
8. Qualitative Analysis — 8.1 free-text reviews, 8.2 sampled idea pairs
9. Related Work — idea generation/execution, LLM for research tasks, computational creativity
10. Discussion — Q1-Q4 (best ideas? subjectivity? why prompting-NLP? automate execution?)
11. Ethical Considerations — publication policy, credit, misuse, homogenization, human impact
Positionality Statement; Acknowledgement; References
Appendices A-Y: topics, template, demo, prompts, review form, agent details, dedup examples, overlap, quality control, positions, institutions, mixed-effects, per-topic breakdown, 8 example ideas with reviews (P-W), identities (X), execution agent (Y)
