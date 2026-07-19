# Digest: liu2025researchbench

**Full title:** ResearchBench: Benchmarking LLMs in Scientific Discovery via Inspiration-Based Task Decomposition
**arXiv:** 2503.21248v3 [cs.CL], dated 20 Apr 2026
**Authors:** Yujie Liu, Zonglin Yang (co-first), Tong Xie, Jinjie Ni, Ben Gao, Yuqiang Li, Shixiang Tang, Wanli Ouyang, Erik Cambria, Dongzhan Zhou (Fudan, Shanghai AI Lab, NTU, UNSW, NUS, Wuhan Univ.)

Basis: this PDF only. Line numbers refer to the pdftotext extraction.

---

## Thesis / Problem

LLMs show potential as scientific research copilots, but their ability to *discover high-quality research hypotheses* is "unexamined due to the lack of a dedicated benchmark" (lines 18-22). The paper introduces ResearchBench, "the first large-scale benchmark for evaluating LLMs on a sufficient set of scientific discovery sub-tasks—inspiration retrieval, hypothesis composition, and hypothesis ranking" (lines 23-25). "Sufficient" is a technical claim: "perfectly solving these sub-tasks perfectly solves the overall discovery task" (lines 25, 61-64).

Central empirical claim: across 12 disciplines, LLMs "excel at inspiration retrieval—an out-of-distribution task—suggesting their ability to surface novel knowledge associations" (lines 34-37). LLMs are framed as "research hypothesis mines" (lines 176-180, 194-196, 1604-1616).

---

## Method — what ResearchBench evaluates (captured precisely)

The benchmark decomposes hypothesis formulation into **three sub-tasks** and measures LLM performance on each separately:
1. **Inspiration retrieval** — given research question + candidate papers, retrieve the ground-truth inspiration papers (metric: Hit Ratio).
2. **Hypothesis composition** — given research background + ground-truth inspirations, generate a hypothesis (metric: normalized 6-point Likert "Matched score" / 5).
3. **Hypothesis ranking** — pairwise rank the ground-truth hypothesis against negatives (metric: pairwise accuracy).

### (a) Inspiration-based decomposition? — YES, explicitly and centrally.
- It is in the title: "via Inspiration-Based Task Decomposition."
- The decomposition is credited to **Yang et al. (2025b) = MOOSE-Chem** (lines 61-64, 206, 210-213, 253, 277-284). ResearchBench adopts, not invents, this decomposition.
- Fundamental assumption: "a majority of ... hypotheses can originate from a research background and several inspirations" (lines 253-258), h = f(b, i_1,...,i_k) (Eq. 1, line 266). Grounded in cognitive science (Koestler 1964; Benedek et al. 2012; Lee & Chung 2024) — creative ideas from "cohesive association of two (or more) seemingly unrelated pieces of knowledge" (lines 68-72).
- Worked example used throughout: backpropagation = research background (multi-layer logistic regression) + inspiration (chain rule in calculus) (lines 74-77).

### (b) Restricts to POST-2024 to control contamination? — YES.
Exact wording:
- Abstract: "To prevent data contamination, we focus exclusively on publications from 2024 onward, ensuring minimal overlap with LLM pretraining data" (lines 29-31).
- Body: "To prevent data contamination, we select only papers published from 2024 onward" (lines 159-160); "we apply the agentic framework only to papers published in 2024 or later, thereby minimizing overlap with the pretraining data of LLMs" (lines 371-374).
- Scalability claim: "as the LLM's pretraining data cutoff date moves forward, the framework can automatically extract more recent papers to avoid overlapping" (lines 160-163, 31-33) -> "contamination-free automatic renewal."
- **Stricter subset (Appendix A.1):** an additional re-run "includes only papers published after **July 2024**" to be "farther away from the baseline model cutoff dates" (lines 1906-1908). Models marked with dagger have cutoff strictly before Jul 2024, "meaning the strict subset is theoretically invisible to them" (lines 1910-1911). Strict vs. Original results are "very close ... consistent with normal sample variance" (lines 2046-2048).

### (c) What it measures and does NOT measure (re: expert-baseline / novelty gap)
- It **measures** LLM performance on the three decomposed sub-tasks and reports per-discipline and overall scores. It presents "the first large-scale study on out-of-distribution (OOD) inspiration retrieval" (lines 191-193).
- **Expert evaluation is used ONLY to validate the decomposition/extraction accuracy** of the automated framework (91.9% / 82.3%), NOT to establish a human performance baseline on the tasks (lines 150-158, 839-860, App. A.2).
- It does **NOT** close, measure, or report any **expert-baseline gap for novelty**. There is no human-vs-LLM performance comparison on inspiration retrieval / composition / ranking, and no novelty-scoring against expert judgment. The "novel knowledge associations" claim is inferred from high OOD retrieval accuracy, not from a human-novelty benchmark.
- It does **NOT** measure fine-grained hypothesis discovery ("not specifically designed for fine-grained hypothesis discovery ... introduced ... in MOOSE-Chem2 (Yang et al., 2025a)", lines 1687-1691).
- It does **NOT** evaluate use of external experimental feedback for hypothesis updating (lines 1692-1695).

---

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| 1386 papers (downloaded / total benchmark) | lines 85-86, 142, 1055 | total corpus size; "Overall" in Table 1 |
| 12 disciplines | lines 82, 293, 1673, 1682 | benchmark coverage |
| Per-discipline paper counts (Table 1) | lines 116-142 | Cell=152, Chem(Chemistry)=113, ETS(Earth Sci)=114, MS(Material Sci)=116, Phys(Physics)=132, EGS(Energy Sci)=117, EVS(Environmental Sci)=116, BL(Biology)=115, BS(Business)=115, Law=97, Math=113, AT(Astronomy)=86; sum=1386 |
| 12 LLMs evaluated | lines 866-873 | Llama-3.2-1B, Llama-3.1-8B, Llama-3.1-70B, Gemini 2.0 Flash, Gemini 2.0 Flash Thinking (FT), Qwen Turbo, Qwen Plus, Claude 3.5 Haiku, Claude 3.5 Sonnet, DeepSeek-V3, GPT-4o Mini, GPT-4o |
| 5 experts / PhD students | lines 150-152, 843, 2056 | Physics(1), Chemistry(2), Materials Science(1), Astronomy(1) |
| 62 papers sampled for expert check | lines 153, 844 | decomposition-accuracy validation |
| 91.9% decomposition accuracy (major issues only) | lines 154-155, 859-860 | expert validation |
| 82.3% decomposition accuracy (major + minor issues) | lines 155-156, 860 | expert validation |
| 5 major cases (3 inspiration ID, 2 hypothesis extraction) + 6 minor (research question) | lines 855-858 | expert error breakdown |
| Candidate set = 75 papers (2-3 groundtruth + 25 negatives per distance level) | lines 883-884, 1044-1045 | inspiration retrieval setup |
| Round 1: 75 -> 5 groups of 15, top 3 each -> 15 (=20% retained) | lines 1046-1049 | retrieval procedure |
| Round 2: 15 -> top 3 overall = 4% (3/75) | lines 1049-1052 | retrieval procedure |
| 100 citation-adjacent papers (Crossref API) per benchmark paper | lines 393-395 | 1st-level negatives |
| 50 semantic-adjacent papers (Semantic Scholar API) | lines 394-395 | 1st-level negatives |
| 2000 papers/discipline via Web of Science | line 399 | 2nd & 3rd-level negative pool |
| 25 negatives sampled per distance level | lines 401-403 | negative set composition |
| GPT-4o top-4% inspiration retrieval = 45.7% (45.65% overall in Table 2b) | lines 168-169, 1061, 833-834 | headline retrieval result |
| ~80% groundtruth found at 20% retained (most models) | line 1058 | retrieval round 1 |
| >40% accuracy at 4% retained; GPT-4o leads at 45.65% | lines 1059-1061 | retrieval round 2 |
| **Inspiration retrieval Overall @20% (Table 2a):** Llama-3.2-1B 33.68, Llama-3.1-8B 75.92, Qwen Turbo 76.17, GPT-4o Mini 78.74, Gemini2.0FT 78.89, Gemini2.0 Flash 79.24, Qwen Plus 80.27, DeepSeek-V3 80.74, Claude3.5 Haiku 80.89, Llama-3.1-70B 81.18, Claude3.5 Sonnet 81.43, GPT-4o 83.43 | lines 612-623 | Table 2a "Overall" col |
| **Inspiration retrieval Overall @4% (Table 2b):** Llama-3.2-1B 11.91, Llama-3.1-8B 37.87, Gemini2.0FT 40.18, GPT-4o Mini 40.59, Qwen Turbo 41.21, Gemini2.0 Flash 41.46, Claude3.5 Sonnet 41.62, Qwen Plus 43.43, Claude3.5 Haiku 44.28, DeepSeek-V3 44.78, Llama-3.1-70B 44.87, GPT-4o 45.65 | lines 823-834 | Table 2b "Overall" col |
| Scaling law (retrieval): grows fast before/during 8B params, bottleneck ~70B | lines 1067-1073 | retrieval scaling finding |
| Negative-inspiration Distance Level 1 @20% ~ 23.57%-56.11% (rises with model) | lines 912-964, Table 3 | closer papers selected far more than L2/L3 (which are ~2-15% and <1% resp.) — table text is column-scrambled in extraction; qualitative finding: "closer papers are more likely to be selected" (lines 1074-1078) |
| Hypothesis composition: 6-point Likert 0-5; normalize avg / 5 | lines 1551-1554 | composition metric |
| **Hypothesis composition Overall (Table 4):** Claude3.5 Haiku 42.56, Llama-3.1-8B 45.68, Gemini2.0FT 46.30, Gemini2.0 Flash 50.15, Llama-3.1-70B 50.92, GPT-4o Mini 52.47, Qwen Turbo 52.71, GPT-4o 53.37, DeepSeek-V3 53.79, Qwen Plus 57.46 | lines 1262-1271 | Table 4 "Overall" col (note: 10 models; Claude 3.5 Sonnet & Llama-3.2-1B absent from this table) |
| Hypothesis ranking setup: 16 hyps/paper = 1 groundtruth + 15 negatives (5 from top negative-inspirations+bg question; 10 from groundtruth-inspiration subsets) | lines 1565-1575 | ranking construction |
| Ranking accuracy = correct pairwise / 15; each pair compared twice (reversed) & averaged | lines 1576-1585 | ranking metric + position-bias mitigation |
| **Hypothesis ranking Overall (Table 5):** Llama-3.1-70B 38.06, GPT-4o Mini 40.13, Gemini2.0 Flash 45.11, Qwen Turbo 45.48, Gemini2.0FT 45.49, Qwen Plus 45.56, Claude3.5 Haiku 48.86, Llama-3.1-8B 55.65, GPT-4o 59.60, DeepSeek-V3 80.99, Claude3.5 Sonnet 81.59 | lines 1461-1471 | Table 5 "Overall" col (11 models; Llama-3.2-1B absent) |
| Ranking scaling law: more params + better pretraining significantly improve ranking (differs from retrieval) | lines 1586-1589 | ranking scaling finding |
| **Position bias (Table 6)** WW / RW / RR (both-wrong / one-right-one-wrong / both-right): GPT-4o Mini 33.83/64.83/1.33; Qwen Plus 25.00/69.33/5.67; Llama-3.1-8B 2.50/91.67/5.83; Llama-3.1-70B 52.67/39.17/8.17; Gemini2.0 Flash 35.50/51.67/12.83; Claude3.5 Haiku 28.17/58.17/13.67; Gemini2.0FT 36.50/49.67/13.83; Qwen Turbo 39.33/45.67/15.00; GPT-4o 11.50/61.50/27.00; DeepSeek-V3 1.74/21.83/76.44; Claude3.5 Sonnet 3.17/19.17/77.67 | lines 1485-1531 | Table 6 (WW=both wrongly ranked, RW=one right one wrong, RR=both rightly ranked) |
| Llama-3.1-8B self-contradictory 91.67% of time; Claude 3.5 Sonnet only 19.17% | lines 1592-1594 | position bias extremes |
| Model cutoff dates (Table 7): GPT-4o & GPT-4o Mini Oct 2023; Llama-3.1-8B/70B Dec 2023; Gemini2.0 Flash/FT Jun 2024; Claude3.5 Sonnet Apr 2024; Claude3.5 Haiku Jul 2024; Qwen Plus/Turbo/DeepSeek-V3 unspecified | lines 1864-1904 | contamination analysis |
| Strict subset = papers after July 2024; Original = full 2024 | lines 1906-1911 | contamination re-run |
| Strict vs Original (Table 8 retrieval @4%): e.g. GPT-4o 45.65->45.22, Llama-3.1-8B 37.87->37.57 | lines 1912-1957 | contamination stability |
| Error analysis: 100 incorrect cases per sub-task | lines 1621-1622 | failure categorization |
| Retrieval errors: 56% title/abstract overlap only; 23% missed cross-discipline papers; 4% misunderstood question; 17% other | lines 1622-1631 | error analysis |
| Composition errors: 52% missing key elements; 27% poor inspiration combination; 13% fluent-but-misaligned; 8% minor | lines 1631-1640 | error analysis |
| Ranking errors: 83% order-of-comparison; 11% subtle distinctions; 6% other | lines 1641-1647 | error analysis |
| Funding: National Science and Technology Major Project (2025ZD0121802) | lines 1703-1705 | acknowledgments |

Metrics recap: retrieval = Hit Ratio; composition = normalized Likert (0-5) / 5; ranking = pairwise accuracy (out of 15). Ranking uses pairwise (Eq. 4) rather than absolute scoring (Eq. 3) because pairwise is "more robust and reliable (Si et al., 2024)" (lines 300-304).

---

## Scope & explicit limitations (Limitations section, lines 1681-1701)

1. Covers **only 12 disciplines** due to "budget and resource constraints"; disciplines chosen "based on data and resource availability rather than deliberate curation"; no discipline excluded post hoc for failing decomposition (lines 1682-1686).
2. **Not designed for fine-grained hypothesis discovery** (that task is MOOSE-Chem2 / Yang et al. 2025a); extension would need fine-grained labels + tailored metrics (lines 1687-1691).
3. **Not designed to evaluate experimental-feedback-driven hypothesis updating** (cites Liu et al. 2025, Romera-Paredes et al. 2024, Novikov et al. 2025, Shojaee et al. 2025a, Weng et al. 2025) (lines 1692-1695).
4. Using auto-collected labels for **model training remains underexplored** (lines 1696-1701).

Additional insight-level limitations (Sec 5.3): retrieval bottleneck is training-data distribution (sparse inter-domain links), "not model reasoning" (lines 1652-1656); composition limited by next-token likelihood favoring familiar combinations (lines 1657-1660); ranking limited by autoregressive positional bias (lines 1661-1665).

---

## Does NOT claim / boundaries

- Does **NOT** claim to close or measure an expert/human-baseline gap for novelty. Human experts appear only as validators of extraction accuracy, never as a task-performance baseline.
- Does **NOT** claim LLMs autonomously produce validated novel discoveries — the "research hypothesis mines" framing is a positioning/interpretation of sub-task results, contingent on the sufficiency argument (lines 1604-1616).
- Does **NOT** invent the inspiration decomposition; it is imported from MOOSE / MOOSE-Chem (Yang et al. 2024, 2025b).
- Does **NOT** evaluate code-writing or experimental implementation (contrasts itself with DiscoveryBench, ScienceAgentBench, PaperBench, LLM-SRBench; lines 220-232).
- Does **NOT** claim contamination is impossible — mitigates it via 2024-onward selection + post-July-2024 strict subset + earliest model versions (lines 1861-1863).
- Hypothesis composition and ranking are reported as only **moderate** ("LLMs show strong retrieval but only moderate composition and ranking, indicating they capture useful associations yet lack deeper integrative reasoning", lines 1674-1676); composition "remains challenging, as none of the models achieve consistently high performance" (lines 1557-1559).

---

## Section map

- **1. Introduction** (lines 39-196): motivation, decomposition, Table 1, headline results, contributions.
- **2. Related Work** — 2.1 Inspiration-Based Scientific Discovery (204-213); 2.2 Benchmarking LLMs (216-232, contrasts IdeaBench, DiscoveryBench, ScienceAgentBench, PaperBench, LLM-SRBench).
- **3. Benchmark Construction** — 3.1 Theoretical Foundation (238-304, Eqs. 1-4, sufficiency argument); 3.2 LLM-Based Agentic Framework (306-378, Fig. 1: inspiration decomposition -> necessary checker -> sufficient checker; self-refine Madaan et al. 2023; Semantic Scholar + Crossref); 3.3 Negative Inspiration Selection (379-412, three distance levels); 3.4 Expert Evaluation (839-860).
- **4. Experiments** (862-876) — 4.1 Inspiration Retrieval (877-1078, Tables 2-3); 4.2 Hypothesis Composition (1079-1559, Fig. 2, Table 4); 4.3 Hypothesis Ranking (1561-1596, Tables 5-6).
- **5. Analysis** — 5.1 LLMs as Research Hypothesis Mines (1602-1616); 5.2 Error Analysis (1617-1647); 5.3 Insights & Challenges (1648-1665).
- **6. Conclusion** (1667-1679).
- **Limitations** (1681-1701); **Acknowledgments** (1703-1705); **References** (1707-1851).
- **Appendix A**: A.1 Data Contamination Analysis (Tables 7-10); A.2 Expert Evaluation Details & Guidelines; A.3 Prompt for Retrieving Inspirations; A.4 Prompt for Evaluating Generated Hypothesis (Table 11 scoring); A.5 Prompt for Pairwise Ranking; A.6 Prompts for Mutate/Refine/Recombine; A.7 Detailed Example of Framework (AlCuFe quasicrystal terahertz absorber); A.8 Examples of the three subtasks.
