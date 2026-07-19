# Digest: baek2024researchagent (BLIND first-pass)

**Title:** ResearchAgent: Iterative Research Idea Generation over Scientific Literature with Large Language Models
**Authors:** Jinheon Baek (KAIST), Sujay Kumar Jauhar (Microsoft Research), Silviu Cucerzan (Microsoft Research), Sung Ju Hwang (KAIST, DeepAuto.ai)
**Venue/ID:** arXiv:2404.07738v2 [cs.CL], 9 Feb 2025. Code: github.com/JinheonBaek/ResearchAgent
**Source read:** full PDF -> researchagent.txt (2818 lines), read in entirety.

---

## Thesis / Problem
Scientific research is slow, effort-intensive, and requires specialized expertise; novel work stems from deep understanding of prior work + cross-pollination of ideas across domains. The authors propose **ResearchAgent**, an LLM system that assists the **first (ideation) phase** of scientific discovery. It automatically (a) defines novel problems, (b) proposes methods, and (c) designs experiments, then **iteratively refines** them using feedback from LLM-powered ReviewingAgents. Claims to be "the first to leverage and evaluate the capabilities of LLMs to act as mediators in scientific idea generation in an open-ended setting" (lines 173-175).

## Method (answering the IMPORTANT questions)

**Is ResearchAgent an ITERATIVE RESEARCH IDEA GENERATION system over scientific literature?**
YES, unambiguously. Pipeline: start from a **core paper** l0 -> add citation-graph-connected related papers {l1..ln} (narrowed by abstract similarity) -> augment with **top-k entities** retrieved from an **entity-centric knowledge store** (co-occurrence matrix K mined across many papers) -> generate idea `o = [p, m, d]` (problem p, method m, experiment design d) via three sequential LLM steps: `p=LLM(Tp(L))`, `m=LLM(Tm(p,L))`, `d=LLM(Te(p,m,L))` -> **iteratively refine** each of p/m/d with LLM ReviewingAgents (lines 289-481). "Iterative" = iterative *refinement* of the written idea across rounds, not an experimental loop.

**Does it establish QUALITY BASELINES for idea generation (evaluated by humans/LLMs)?**
YES. Dual evaluation: (1) **model-based** (GPT-4 as judge, 5-point Likert per criterion + pairwise win-ratio) and (2) **human** evaluation (10 expert annotators, >=3 papers each, judging ideas from their own papers). Each of problem/method/experiment scored on its own **five criteria**. Since it is a novel task with **no direct baselines** and **no ground-truth answers**, "baselines" are ablated variants (Naive ResearchAgent = core paper only; w/o Entity Retrieval) plus prior **hypothesis-generation** methods (SciMON, Hypothesis Proposer) in Table 3. Human-induced criteria align the GPT-4 judge with real human preferences.

**Does it integrate a full discovery LOOP, or only idea generation?**
**ONLY IDEA GENERATION (ideation phase only).** It does NOT execute experiments, does NOT write/run code, does NOT empirically validate ideas. The third output "experiment design" is a *written design*, not execution. The paper explicitly focuses on the "first phase — idea generation" (lines 171-175) and explicitly contrasts itself against Lu et al. 2024 (AI Scientist), which "aim to automatically generate full research papers (including idea development, code writing, and experiment execution)" (lines 249-251). Limitations reiterate that "validating these generated research ideas with experiments is essential to truly accelerate scientific research" — i.e., left undone (lines 1272-1274). The "loop" present is the **review/refine loop** (ReviewingAgents), NOT a discovery loop with empirical testing.

---

## FACTS TABLE (exhaustive)

| Value | Location (line) | Context |
|---|---|---|
| >7 million academic papers published per year | 146-148 | Intro motivation (cites Fire & Guestrin 2019) |
| Idea `o = [p, m, d]` (problem, method, experiment design) | 313 | Formal definition; decomposed as p=f(L), m=f(p,L), d=f(p,m,L) |
| Core paper citation threshold "e.g., exceeding 100 over 3 months" | 366-367 | Method design choice #1 (illustrative) |
| Core papers = >20 citations | 522-523 | Experimental Setup — ACTUAL threshold used (note: differs from the >100/3mo illustrative figure) |
| Papers after May 01, 2023 | 429, 518 | Chosen because LLMs trained on pre-May-2023 web data |
| 300 papers sampled as core papers | 526-527 | Benchmark size |
| Avg 87 reference papers per core paper | 528-529 | Data statistic |
| 2.17 entities per abstract on average | 530 | Data statistic |
| Knowledge store K ∈ R^(m×m), sparse | 400-402 | Entity co-occurrence matrix, m = # unique entities |
| Entity extraction restricted to titles + abstracts | 431-432 | Cost constraint |
| Entity linker = BLINK (Wu et al. 2020), off-the-shelf | 408, 756-757 | Not custom-trained for science |
| Knowledge store built from papers May 01–Dec 31 2023 + references = 50,091 total | 757-758, 795 | KB construction corpus size |
| Top-k entity retrieval via co-occurrence P(ej|ei)×P(ei), Bayes + independence assumption (Eq 1-2) | 434-460 | Retrieval formulation; embedding-based alternative in App B.3 |
| GPT-4 release Nov 06, 2023; trained up to Apr 2023 | 752-755 | Base model for all main models |
| 10 idea-pairs + scores per criterion, 5-pt Likert, annotators with >=3 papers | 498-501 | Human-induced criteria collection |
| 5 human annotators judge induced criteria: 2 strongly agree, 3 moderately | 534-536 | Criteria quality check |
| 5 criteria per idea aspect (top-5 selected) | 478, 487-488 | Problem/Method/Experiment each have 5 criteria (Table 12) |
| 15 ReviewingAgents (3 ideas × 5 criteria) | 1277-1278 | Refinement architecture |
| Performance saturates after 3 refinement iterations | 1059-1061 | Diminishing returns (aligns w/ Du et al. 2023) |
| 10 expert annotators (>=3 papers), judge own-paper ideas | 745-747 | Human eval design |
| Annotators from US + South Korea; CS, medicine, biology | 1706-1710 | Recruitment |
| 6-page guideline; Label Studio platform | 1710-1712 | Annotation setup |
| Compensation $22.20/hour | 1718 | Human eval cost |
| ~3 idea-sets/hr × 3 sub-ideas × 3 approaches = 9 ideas/hr | 1719-1723 | Annotation throughput |
| 3 rounds of human eval with refinements between | 1724-1725 | Eval protocol |
| Total 150 ideas fully evaluated | 1685-1686 | Human eval scope |
| 20% of ideas double-judged (inter-annotator) | 923 | Reliability check |
| Spearman corr (scoring), Cohen's kappa (pairwise) | 926-928 | Agreement metrics |
| Inter-annotator (Human-Human) scoring: Problem 0.83 / Method 0.76 / Experiment 0.67 | 767-779 (Table 1) | High agreement |
| Inter-annotator pairwise: 0.62 / 0.62 / 0.41 | 767-779 (Table 1) | Experiment lower |
| Human-Model scoring: 0.64 / 0.58 / 0.49; pairwise 0.71 / 0.62 / 0.52 | 781-793 (Table 1) | Model judge validated as proxy |
| GPT-4 Naive RA: P 4.20 / M 4.03 / E 3.92; Full RA: 4.52 / 4.28 / 4.18 | 1107-1114 (Table 4) | Main scores |
| GPT-3.5 Naive 3.56/3.56/3.63; Full 3.58/3.58/3.60 | 1121-1128 (Table 4) | Gain vanishes on weak model |
| Llama3-8B Naive 3.76/3.69/3.54; Full 4.18/4.03/3.95 | 1135-1142 (Table 4) | Gains hold |
| Mixtral-8x7B Naive 3.31/3.27/3.20; Full 3.28/3.35/3.31 | 1149-1156 (Table 4) | Marginal/mixed |
| Qwen1.5-32B Naive 3.64/3.74/3.66; Full 4.02/3.97/3.94 | 1160-1170 (Table 4) | Gains hold |
| Table 3: SciMON Clar 4.04/Rel 4.37/Orig 4.56/Feas 3.98/Signif 4.15 | 1172-1191 | Hypothesis-gen baseline |
| Table 3: Hypothesis Proposer 3.97/4.14/4.07/4.01/4.11 | 1172-1191 | Baseline |
| Table 3: ResearchAgent 4.11/4.88/4.77/4.05/4.81 | 1172-1191 | Superior on Relevance/Originality/Significance |
| Ablation (Table 2): w/o Entities, w/ Random Entities, w/o References, w/ Random References, w/o both | 945-950 | References especially helpful; random > none |
| Entity retrieval (Table 5): co-occurrence 4.52/4.28/4.18 ≈ embedding 4.49/4.34/4.16; w/o 4.35/4.13/4.02 | 1837-1852 | Two retrieval strategies comparable |
| BLINK yields ~3 entities/paper (limited coverage) | 1261-1262 | Limitation |
| Category distribution: CS 25.3%, Medicine 20.7%, Engineering 13.0% (top 3) | 1588-1641, Fig 7 | Domain mix |
| Data source: Semantic Scholar Academic Graph API | 517 | Literature source |
| High-impact core papers -> higher-quality ideas (citation bucketing) | 1193-1207, Fig 6 | Correlation analysis |

## Scope & Limitations
- Ideation phase ONLY; no experiment execution / code / empirical validation (lines 171-175, 1272-1274).
- Knowledge store built only from titles+abstracts of a limited publication set (cost) -> precludes many entities/relations (1256-1260).
- BLINK ~3 entities/paper, open-domain linker, limited coverage (1261-1263).
- LLM-based -> may hallucinate ideas (1266-1268).
- 15 ReviewingAgents / 5 criteria per aspect may not capture full range of perspectives across domains (1275-1290).
- Less suited to theoretical sciences (math, proof generation) (1291-1301).
- Ethics: misuse risk (explosives, malware, surveillance); unintentional plagiarism/regurgitation (1304-1324).

## Does NOT claim / boundaries
- Does NOT run/execute experiments, write code, or empirically test ideas (explicitly distinguished from Lu et al. 2024 AI Scientist).
- Does NOT provide a fully autonomous end-to-end discovery loop — the only loop is review-and-refine on written ideas.
- No ground-truth answers; quality is judged (LLM + human), not verified against empirical outcomes (lines 564-571).
- No direct task baselines exist; comparisons are ablations + prior hypothesis-generation methods (lines 543-559).

## Section map
- 1 Introduction (33); 2 Related Work — LLMs / Hypothesis Generation / Knowledge-Augmented LLMs / Iterative Refinements (213); 3 Method — 3.1 LLM-Powered Idea Generation, 3.2 Knowledge-Augmented LLMs (285); 4 Experimental Setup — 4.1 Data, 4.2 Baselines & Model, 4.3 Evaluation, 4.4 Implementation (508); 5 Results & Analyses (799); 6 Conclusion (1237); Limitations (1253); Ethics (1303); Acknowledgements (1326); References (1341); Appendix A Additional Details + B Additional Results; Tables 6-16 (prompts, criteria rubrics, generated-idea examples).
