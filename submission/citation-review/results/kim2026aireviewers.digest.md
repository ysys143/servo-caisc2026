# Digest: kim2026aireviewers

**Full title:** "On the limits and opportunities of AI reviewers: Reviewing the reviews of Nature-family papers with 45 expert scientists"
**Authors:** Seungone Kim, Dongkeun Yoon, Kiril Gashteovski, ... Sean Welleck, Graham Neubig (CMU, KAIST, NEC Labs Europe, and ~25 institutions total; 60+ co-authors)
**Venue/ID:** arXiv:2605.20668v1 [cs.CL], 20 May 2026
**Source read:** full extracted text (`/Users/jaesolshin/.claude-3/jobs/e6b73762/tmp/kim.txt`, 7,881 lines). Main body (§1–7) read in full; appendices A–H skimmed with headline numbers captured.

---

## Thesis / Problem (2–4 sentences)
Existing evaluations of AI (LLM-agent) reviewers judge them only at the aggregate-verdict level (do AI overall scores / accept-reject decisions match humans?), which cannot reveal whether the individual criticisms authors receive are correct, significant, and well-evidenced. The authors argue verdict-level agreement is a fragile benchmark (NeurIPS 2014/2021 consistency experiments: ~half of papers accepted by one committee were rejected by the other) and that evaluation must happen at the level of the individual criticism. They run a large-scale expert annotation study evaluating every review item (atomic criticism) from human and AI reviews of Nature-family papers. Conclusion: current frontier AI reviewers are complements to, not substitutes for, human reviewers.

## Method (what the study actually does)
- **45 domain scientists** (annotators / "meta-reviewers") from 25 institutions: 23 faculty, 7 industry/national-lab/institute research scientists, 6 postdocs, 9 PhD students. Fields: Physical, Biological, Health Sciences.
- They spent **469 hours** rating **2,960 individual review items** (each an atomic criticism targeting one aspect of a paper) from human-written and AI-generated reviews.
- **82 Nature-family papers** (published 10 Jan 2020 – 27 Oct 2025). Breakdown: Nature Communications 73, Nature 2, Nature Computational Science 2, Nature Ecology & Evolution 2, Nature Methods 1, Nature Physics 1, Nature Microbiology 1. By field: 38 Physical, 30 Biological, 14 Health; 27 subject categories.
- Each item rated on **three dimensions** (cascading): Correctness (binary), Significance (3-level ordinal 0–2), Evidence sufficiency (binary). Plus free-form qualitative feedback and a paper-level survey selecting Top-Rated and Lowest-Rated human reviewer.
- **Human reviewers:** first-round official Nature transparent peer reviews (first 3 retained per paper).
- **AI reviewers:** 3 frontier LLMs deployed as agents via OpenHands SDK with filesystem access to source files + tools (shell, file editor, task tracker, web search with publisher domains blocked): **GPT-5.2, Claude Opus 4.5, Gemini 3.0 Pro**. Each capped at 5 review items per paper (a stricter bar than humans, who are uncapped). One review per (paper, model) pair.
- Primary unit of analysis in §3–4 is the **paper (n=82)**, not the item (N=2,960).
- 27 of 82 papers double-annotated → 908 doubly-annotated items for inter-annotator agreement.

---

## FACTS TABLE (exhaustive quantitative results)

### Headline / study scale
| Value | Location | Context |
|---|---|---|
| **45** expert scientists / domain scientists | Title, Abstract, §2.4, §7 | **CONFIRMED 45** (stated identically in title, abstract, methods, conclusion) |
| 25 institutions | §2.4 | annotator affiliations |
| 469 hours | Abstract, §2.4, §7 | total expert annotation time |
| 2,960 review items | Abstract, §2.4, §7 | atomic criticisms rated (N) |
| 82 Nature-family papers | Abstract, §2.2, §7 | study corpus |
| 109 meta-reviews | §2.4 | produced across 82 papers, avg 2.42 papers/scientist |
| 3 AI reviewers | §2.3 | GPT-5.2, Claude Opus 4.5, Gemini 3.0 Pro |
| ≤5 review items per AI review | §2.3 | AI cap; humans uncapped |

### Composite "fully positive" quality (correct + top significance + sufficient evidence) — paper-level mean, Table 4
| Reviewer | Fully-positive rate | Location |
|---|---|---|
| Top-Rated Human | **48.2%** [42.2, 54.3] | Abstract, §3, Table 4 |
| Lowest-Rated Human | 36.2% [30.0, 42.4] | §3, Table 4 |
| GPT-5.2 | **60.0%** [52.3, 67.4] | Abstract, §3, Table 4 |
| Claude Opus 4.5 | 53.1% [45.6, 60.7] | §3, Table 4 |
| Gemini 3.0 Pro | 50.2% [42.7, 57.7] | §3, Table 4 |
| GPT-5.2 vs Top-Rated Human | **60.0% vs 48.2%, p = 0.009** (paired diff −11.6%, d=−0.30) | Abstract, §3, Table 4 |
| Claude Opus 4.5 / Gemini vs Top-Rated Human | statistically indistinguishable (p=.23, p=.65) | §3, Table 4 |
| All 3 AI vs Lowest-Rated Human | exceed by +14.1 to +23.6 pts, all p≤.004 | §3, Table 4 |

### Per-dimension paper-level means (Table 3)
| Reviewer | Correctness % | Significance (0–2) | Evidence % |
|---|---|---|---|
| Top-Rated Human | 92.3 [89.2,95.0] | 1.39 [1.30,1.49] | 92.2 [88.5,95.3] |
| Lowest-Rated Human | 79.1 [73.0,84.6] | 1.30 [1.18,1.42] | 89.7 [84.7,94.0] |
| GPT-5.2 | 86.2 [80.7,91.2] | 1.61 [1.50,1.70] | 97.1 [93.7,99.5] |
| Claude Opus 4.5 | 83.7 [78.2,88.6] | 1.53 [1.43,1.63] | 96.5 [93.1,99.1] |
| Gemini 3.0 Pro | 81.9 [76.5,87.1] | 1.56 [1.46,1.65] | 89.5 [84.0,94.2] |

- Key tradeoff: all 3 AI reviewers **less correct** than Top-Rated Human (by 6–10 pts) but raise **more significant** issues (rank-biserial r=+0.30 to +0.49 vs top human, all p≤.028). Evidence: GPT-5.2/Claude slightly higher than top human (p<.05), Gemini indistinguishable.

### Expert-judged win rates (Table 5, fraction of papers AI matches/exceeds human)
| Reviewer | vs Top-Rated Human | vs Lowest-Rated Human |
|---|---|---|
| GPT-5.2 | 48.6% [38.7,58.5] | 73.4% [64.2,82.4] |
| Claude Opus 4.5 | 32.1% [22.5,42.0] | 68.8% [58.9,78.4] |
| Gemini 3.0 Pro | 30.3% [21.6,39.4] | 59.6% [50.4,69.2] |

### Overlap / diversity (§4, Rogan-Gladen-corrected)
| Value | Location | Context |
|---|---|---|
| AI-AI overlap **21.0%** vs human-human **3.1%** | Abstract, §1 intro | same-target-same-criticism cross-reviewer pairs (rounded figures) |
| A–A 20.9% [16.2,25.4] vs H–H 3.4% | §4, Fig 4 (left) | same figures, §4 body precision |
| H–A overlap 5.1% [0.3,9.0] | §4 | AI–human overlap ≈ near human–human baseline |
| AI surfaces distinct **26%** of issues no human raises | Abstract | uncovered AI items |
| 74.0% [65.5,84.1] of AI items covered by ≥1 human | §4, Table 6 | matched |
| 26.0% [15.9,34.5] uncovered AI items (no human match) | §4, Table 6 | |
| Uncovered AI items: 81.8% correct, 93.5% evidence-sufficient, 48.1% fully positive | Table 6/7 | uncovered items are valid, not hallucinations |
| Single AI recovers 27.1% of a human's items vs 25.8% recovered by another human | Abstract, §4 | same-criticism coverage |
| 3-AI panel covers 83.0% of human items at target level, 46.3% at criticism level | §4 | |
| 65,704 cross-reviewer pairs | §4 | judged by LLM similarity judge (GPT-5.4), 92.7% binary acc, 83.5% 4-way |

### Weaknesses / strengths (§5)
| Value | Location | Context |
|---|---|---|
| **16 recurring weaknesses** | Abstract, §5, §7 | failure modes humans don't share (n=260 comments) |
| 6 strength categories | §5 | n=132 comments |
| 392 comments flagging strength/weakness | §5 | out of 767 item-level + 250 paper-level |
| Top-3 weaknesses drive most incorrect items | Abstract, §5, §7 | (1) limited subfield/field-norm knowledge (W1 n=54), (2) losing track over long papers+supplements / long-context (W3 n=37), (3) overly critical stance inflating minor issues |
| W2 over-harsh/out-of-scope n=46; W4 redundancy n=28; W5 vague/verbose n=24 | §5 | |
| Top strength S1 statistical/methodological rigor n=45; S2 code inspection n=28; S3 domain depth n=27; S4 internal consistency n=15 | §5 | |

### PeerReview Bench (§6.1, Table 8 — 78-paper benchmark, 12 backbone models)
| Model | Precision | Recall | F1 |
|---|---|---|---|
| Claude-Opus-4.5 (top F1) | 75.49 | 38.39 | **50.89** |
| Claude-Opus-4.7 | 71.47 | 39.00 | 50.46 |
| GPT-5.4 (top precision) | 93.81 | 26.55 | 41.38 |
| GPT-5.2 | 88.92 | 32.28 | 47.37 |
| DeepSeek-V4-Pro | 76.75 | 35.47 | 48.52 |
| Gemini-3.0-Pro-Preview | 53.35 | 37.65 | 44.14 |
- Intro summary: "even GPT-5.4, DeepSeek-V4-Pro, and Claude-Opus-4.7 achieve only 41.4%, 48.5%, and 50.5% F1" — substantial headroom remains.

### CMU Paper Reviewer (§6.2, Table 9 — 78 papers)
| Platform | Precision | Recall | F1 |
|---|---|---|---|
| CMU Paper Reviewer (GPT-5.4, 15 items) | **95.46** | 42.32 | **58.64** |
| Stanford Agentic Reviewer | 59.84 | 45.43 | 51.65 |
| OpenAIReview (Claude-Opus-4.7) | 57.57 | 40.98 | 47.88 |
- Intro phrasing: CMU items "more often correct, significant, and well-evidenced (**95.5% vs. 59.8% and 57.6%** for Stanford Agentic Reviewer and OpenAIReview)" — these are the precision numbers.

### Inter-annotator agreement (Table 2)
| Dimension | N | %Agree | Cohen's κ | Gwet's AC1 |
|---|---|---|---|---|
| Correctness | 908 | 85.8% | 0.28 (fair) | 0.82 (almost perfect) |
| Significance | 743 | 59.9% | 0.31 (fair) | 0.44 (moderate) |
| Evidence | 583 | 88.0% | 0.12 (slight) | 0.86 (almost perfect) |

### Meta-reviewer calibration (App F)
- Claude-Opus-4.7 as meta-reviewer: 87.9% / 56.7% / 85.6% per-axis accuracy vs human-human 85.8% / 59.9% / 88.0% (§6.1).
- Ten-class accuracy (Table 49): Claude-Opus-4.7 44.3% vs GPT-5.4 30.1%, Gemini-3.1-Pro 29.0% (10% random baseline).

### Panel composition (App H, 53 papers)
- 3-human panel: 3.9 fully-positive-and-unique items/paper, 25.8 total, 11.5 distinct issues.
- 2H+1AI: matches 3H useful feedback (3.9) with 17% fewer total items.
- All-AI panel: drops to 1.8 fully-positive-and-unique/paper; 3-AI panel yields only 3.1 distinct issues (vs 11.5 for 3 humans).
- Meta-reviewer filter raises efficiency but cuts absolute useful volume (3H: 3.9 → 1.9, a 51% drop).

### Deployment context cited (not this study's results)
- AAAI-26 AI review pilot on all **22,977** main-track submissions [Biswas et al., 2026].
- NeurIPS 2014/2021 consistency: 49.5% / 50.6% of accepted papers rejected by other committee.
- Nature/Science median submission-to-publication 100–160 days [Powell, 2016].

---

## CRITICAL: "+2.3" figure and "Agent Laboratory"
- **NO "+2.3" figure appears anywhere in this paper.** I searched the full 7,881-line extraction: the only "2.3" occurrences are the correctness value "92.3", a cross-reference to "§2.3", and a paper reference. There is **no** "+2.3 point" over/under-estimation statistic of any kind.
- **NO mention of "Agent Laboratory" (or Agent-Lab / AgentLab) anywhere in this paper.** It is not cited, discussed, or referenced.
- This paper does NOT report any "over-estimation of paper quality/scores by +2.3 points" attributed to any tool. If a manuscript attributes such a figure to this paper (kim2026aireviewers), that attribution is **not supported by the source**. The nearest concept in this paper is a *qualitative* AI weakness ("overly critical stance that inflates minor issues," W-category, no numeric +2.3), and a *reversed*-direction quantitative finding: AI reviewers are LESS correct but raise MORE-significant items than the top human (Table 3) — no single "+2.3" over-scoring number.

---

## Scope & explicit limitations (stated by the authors)
- Entire study draws from **one Nature paper submission pool**; conferences, single-discipline journals, or short-timeline venues "may exhibit different dynamics" (App H caveats).
- Per-AI **5-item cap** and the specific **3 frontier models** are experimental-setup choices; a larger item budget would change absolute counts (App H).
- Human reviews capped at first 3 reviewers; AI reviews capped at 5 items (asymmetric, a stricter bar for AI — mitigated by paper-level aggregation, §3).
- Frontier-model behavior "will continue to evolve"; specific numbers should be re-validated for other venues/future models.
- Significance agreement only moderate (Gwet's AC1 = 0.44); the study reports AC1 as primary due to kappa paradox under skewed marginals.
- Open questions the authors flag: whether the correctness/significance tradeoff persists as models improve, whether patterns generalize beyond Nature-family papers, what governance norms should accompany deployment.

## Does NOT claim / boundaries
- Does NOT claim AI reviewers should replace humans — explicitly positions them as **complements/augmentation, not substitutes**.
- Does NOT report a "+2.3 point" over-estimation figure (see above).
- Does NOT evaluate AI reviewers on AI/ML conference papers (deliberately steps outside AI-on-AI-papers norm — uses Physical/Biological/Health Nature-family papers).
- Does NOT claim AI reviewers are uniformly better: only GPT-5.2 exceeds top human on composite; Claude Opus 4.5 and Gemini 3.0 Pro sit between top- and lowest-rated human.
- Does NOT use aggregate verdict/score alignment as its metric (explicitly critiques that approach).

## Section map
- §1 Introduction (peer-review scaling crisis, verdict-level critique, 3 findings preview)
- §2 Preliminaries: study design (2.1 review-item methodology & 3 criteria; 2.2 paper selection/stats Table 1; 2.3 human + AI reviewer setup; 2.4 45 domain-scientist annotators, IRR Table 2)
- §3 In which aspects are AI reviewers better/worse (Tables 3–5: correctness/significance/evidence, fully-positive, win rates)
- §4 Overlap between AI and human reviews (Tables 6–7, Fig 4: coverage, diversity, 21% vs 3% overlap)
- §5 Concrete strengths & weaknesses (Fig 5: 16 weaknesses / 6 strengths, W1/W3/S2 case studies)
- §6 Tools: 6.1 PeerReview Bench (Table 8), 6.2 CMU Paper Reviewer (Table 9)
- §7 Conclusion
- Appendices: A Related Work (Table 10); B extended study design (Tables 11–14, prompts Figs 6–9); C better/worse extended + GLMM (Tables 15–17); D overlap extended + similarity judge calibration (Tables 18–21); E strengths/weaknesses full examples (Tables ~22–45); F meta-reviewer & PeerReview Bench (Tables 46–49); G CMU Paper Reviewer platform; H panel composition analysis for organizers (Tables 52–53)
