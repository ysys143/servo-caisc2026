# ERA: identity and architecture

## Audit scope and source

- **Single source read:** `ERA - An AI System to Help Scientists Write Expert-Level Empirical Software.pdf`, arXiv `2509.06503v2`, dated 15 May 2026, printed date 2026-5-19.
- **Authors/affiliations:** Eser Aygün et al.; the title page lists Google DeepMind, Google Research, Google Platforms and Devices, MIT, Harvard, McGill, and Caltech affiliations (p. 1).
- **Physical scope:** 78 pages. The page sequence was read from p. 1 through p. 78, including the main paper, references, Extended Data figures/tables, Supplementary Notes, Supplementary Figures, Supplementary Tables, prompts, and example code. No other PDF was opened and no API/model call was used for this audit.
- **Source-level identity:** The paper calls the system **Empirical Research Assistance (ERA)**, an AI system that creates expert-level scientific software to maximize a quality metric (p. 1). The title's “write” framing should not be read as a manuscript-writing system: the operational object is code/software for scorable empirical tasks.

## Full-paper structure and page coverage

| Pages | Material read and structural role |
|---|---|
| 1 | Title, authors, affiliations, abstract, keywords. Identity, claimed task class, headline results, and distinction between empirical software and general scientific progress. |
| 2-3 | Introduction and start of Results. Motivation: scientific software is slow, design choices are not exhaustively searched. ERA combines LLM code rewriting, tree search, a sandbox, quality scores, and externally supplied research ideas. Figure 1 defines the schematic, benchmark comparison, and research-idea injection/recombination view. |
| 4-6 | Scorable-task overview; Kaggle Playground Benchmark; scRNA-seq batch-integration setup and results. Six scientific/engineering task families are introduced. The benchmark uses 16 2023 playground competitions, public leaderboard percentile, and direct Kaggle scoring. OpenProblems holdout evaluation and BBKNN/ComBat results begin here. |
| 7-9 | Remaining scRNA-seq results and COVID-19 hospitalization forecasting. The paper reports method adherence checks, embedding-based diversity analysis, recombination, and external research-idea sources. The COVID results include 14 strategies beating the official CovidHub ensemble, with the paper attributing them to recombination, Deep Research, AI co-scientist, and a replicated baseline. |
| 10 | GIFT-Eval time-series forecasting and transition to Discussion. Per-dataset and unified solutions are described; the unified solution is optimized across datasets. |
| 11-12 | Discussion and related positioning. ERA is compared with genetic programming, generative programming, one-shot code generation, AutoML, LLM-plus-search systems, and science agents. The authors explicitly distinguish optimizing scorable predictive software from genuine discovery involving theory, causality, and mathematics; they also state safety risks and summarize the empirical claims. |
| 13-19 | Methods. Code mutation and flat PUCT tree search; algorithm and score/rank definitions; model comparison; recombination experiments; Gemini embeddings; task-specific datasets, splits, prompts, and evaluation details for scRNA-seq, COVID forecasting, GIFT-Eval, geospatial segmentation, ZAPBench, and numerical integration. |
| 20-24 | References [1]-[89]. These pages establish the cited context but are not independent ERA implementation documentation. |
| 25 | Code availability, author contributions, acknowledgements, competing-interest declaration. The paper states that a reference implementation, best solutions, and a tree-search inspection UI are publicly available. |
| 26-33 | Extended Data Figures 1-8 and their legends. These show benchmark comparisons, ablations, solution trees/breakthrough plots, COVID forecasts/recombination, and GIFT-Eval search evolution. They provide result visualizations, not a different control architecture. |
| 34 | Extended Data Tables 1-2. Manual adherence judgments for replicated methods and a scRNA-seq method comparison table. |
| 35-38 | Supplementary Notes. Additional discussion of the six scientific problems, generated solutions, and the boundary between empirical optimization and scientific discovery, with task-specific result/context material. |
| 39-56 | Supplementary Figures S1-S20. Experimental design, scRNA-seq UMAP/metric and tree-search analyses, COVID validation/visual checks/recombination/trees, GIFT-Eval and geospatial plots, ZAPBench, and numerical-integration solution trees and held-out scores. |
| 57-59 | Supplementary Tables S1-S5. Per-node computational costs and sandbox type; 16 Kaggle competitions; Kaggle prompt; expert advice prompt; boosted-decision-tree prompt. |
| 60-61 | Supplementary Table S6. Concrete generated BBKNN (TS) code, continued. This makes the code-producing role explicit. |
| 62 | Supplementary Table S7. Prompt for comparing two baseline solutions and generating a recombination summary. |
| 63-66 | Supplementary Tables S8-S10. COVID data splits, method descriptions used to replicate CovidHub models, and the prompt that injects those descriptions into tree search. |
| 67-70 | Supplementary Table S11, continued. Expert manual inspection of adherence for replicated COVID models, including Follow, Partially Follow, and Follow + Innovate judgments. |
| 71-73 | Supplementary Tables S12-S14. GIFT-Eval leaderboard, example unified-solution configurations, and geospatial benchmark comparison. |
| 74-76 | Supplementary Tables S15-S17. Deep Research prompt, formatting prompt, and hybrid-strategy prompt. These show that external ideas and recombination are prompt-mediated inputs to code search. |
| 77-78 | Supplementary Tables S18-S19. Existing-paper summarization prompt and example BBKNN description supplied to ERA. These close the paper with the literature-to-code prompt path and an example of method guidance. |

## Problem, motivation, and context

The problem is not open-ended autonomous science in the strongest sense. The paper starts from **empirical software** whose output can be scored by a measurable metric. Such software is central to scientific modeling, but domain-specific implementations are slow, laborious, and commonly shaped by intuition or expediency rather than systematic search (pp. 2-3). ERA is proposed to make this search broad and fast by generating and evaluating many code candidates.

The paper's context is deliberately hybrid:

1. **Scientific-software bottleneck:** software creation limits how many hypotheses or design choices can be explored (pp. 2, 11-12).
2. **Search and optimization:** tree search is used to preserve diverse candidates, backtrack, and exploit score jumps rather than relying on one-shot generation or independent best-of-N calls (pp. 3-5, 13-15).
3. **Research-idea integration:** papers, textbooks, search results, Deep Research, AI co-scientist outputs, expert advice, and existing method descriptions can be injected into prompts (pp. 2-3, 7-9, 15, 62, 74-78).
4. **Scorable scientific tasks:** the demonstrations cover scRNA-seq batch integration, COVID hospitalization forecasting, time-series forecasting, geospatial segmentation, zebrafish neural-activity prediction, and difficult numerical integration (pp. 2-4, 10, 16-19, 35-56).
5. **Boundary condition:** the Discussion explicitly says that optimizing predictive models is distinct from genuine scientific discovery requiring theories, causal mechanisms, and mathematical frameworks (p. 12). Thus “towards scientific discovery” is an aspiration/extension claim, while the evaluated core is advanced empirical software engineering with automated scores.

## System identity and architecture

### Core control loop

The operational loop is:

1. Input a scorable problem description, evaluation metric, relevant data/code, and optional research idea or method description.
2. Prompt an LLM to produce Python code or rewrite a parent candidate.
3. Execute the candidate in a sandbox.
4. Compute the task-specific quality score and retain logs/other node information.
5. Select a node for expansion using a PUCT-inspired score balancing exploitation and exploration.
6. Generate one novel child conditioned on the selected parent, execute and score it, append it to the global tree, and backpropagate visits (pp. 3, 13-14).

This is a computational generate-execute-score-regenerate loop. The evaluator is a task metric/leaderboard or held-out benchmark score, not a general scientific-truth or novelty validator.

### Search implementation

The search is a **global flat tree**, closer to Flat UCB than conventional AlphaZero-style recursive MCTS. Every node is eligible for expansion; selection uses a PUCT-inspired acquisition score with rank-normalized task scores and visit-based exploration. The authors tuned `c_puct = 1` on the Kaggle benchmark. The LLM's sampling supplies stochasticity; node scoring does not use random game rollouts (pp. 13-14).

The tree is used to backtrack and branch from historical candidates when a line plateaus. The paper reports saturation after roughly 300-1000 nodes, with task-specific runs including 500 nodes for scRNA-seq and 128-node comparisons in the ERA-versus-best-of-N study (pp. 13, 16).

### Research-idea and recombination path

Research ideas are not a separately specified autonomous hypothesis generator inside the core loop. They are prompt inputs. The paper describes direct user injection, search-engine/literature access, expert advice, summaries of papers, Deep Research, AI co-scientist outputs, and summaries comparing two existing solutions (pp. 2-3, 7-9; Supplementary Tables S4, S7, S15-S19).

For recombination, the authors select top nodes from baseline searches, ask Gemini to explain technical similarities and differences between two parent methods, add that explanation to a hybrid-strategy prompt, and run ERA again. This produced 55 scRNA-seq and 28 COVID hybrid methods in the described experiments (p. 15; Supplementary Tables S7 and S17). The paper's own wording says that ideas are part of prompts, while mutations occur at code level (p. 13).

### Evaluation and demonstrations

- Kaggle: 16 playground competitions; public leaderboard percentile; comparison to single calls, best-of-1000 calls, and AIDE (pp. 3-5, 57-59).
- scRNA-seq: OpenProblems v2.0.0 holdout, 1,747,937 total cells; nine selected methods; eight of nine corresponding published results beaten in pairwise comparisons; BBKNN (TS) reported 14% overall improvement over ComBat (pp. 4-7, 39-42, 60-62).
- COVID forecasting: CovidHub-oriented models, rolling WIS evaluation, replication and recombination; 14 strategies reported above the official ensemble (pp. 7-10, 43-49, 63-70).
- GIFT-Eval: per-dataset and unified time-series solutions, with leaderboard and configurations (pp. 10, 18-19, 50, 71-72).
- Geospatial segmentation, ZAPBench, and numerical integration: additional expert-level software demonstrations with Extended Data and Supplementary Figures/Tables (pp. 35-56, 73).

The validation signal in all of these is a defined computational metric, often with train/validation/holdout splits and, in some cases, manual code-adherence inspection. Manual inspection checks whether a generated implementation follows a requested method; it is not the loop's primary acceptance gate (pp. 5-7, 34, 67-70).

## Frozen supplementary description and clause-by-clause audit

The frozen description audited here is:

> ERA is an LLM-plus-tree-search system for generating and optimizing empirical scientific software on scorable tasks. It prompts an LLM to rewrite code, executes candidates in a sandbox, and uses task scores to explore a candidate tree. Research ideas from papers, expert advice, search/research agents, and previous solutions can be injected into prompts, including an LLM-mediated recombination step. It was evaluated across Kaggle and six scientific/engineering task families, with reported expert-level or leaderboard-beating results. The system closes a computational generate-execute-score-regenerate loop, but its evaluator is a task metric rather than a general novelty or scientific-truth validator.

| Frozen clause | Verdict | Direct PDF evidence and qualification |
|---|---|---|
| “LLM-plus-tree-search system” | **Supported** | The abstract and Fig. 1 identify an LLM and Tree Search; Methods defines PUCT-inspired flat tree search (pp. 1, 3, 13-14). |
| “generating and optimizing empirical scientific software” | **Supported** | The system identity is Empirical Research Assistance and the paper repeatedly defines the target as software maximizing a measurable quality score (pp. 1-3, 11-12). |
| “on scorable tasks” | **Supported, central scope** | The Results section explicitly defines scorable tasks and lists six scientific/engineering task families; the Kaggle benchmark is also score-driven (pp. 2-4). |
| “prompts an LLM to rewrite code” | **Supported** | The LLM receives task description, metric, data, and optional ideas; Methods says it rewrites existing candidates and generates one child conditioned on a parent (pp. 3, 13-14). |
| “executes candidates in a sandbox” | **Supported** | The schematic and Methods specify sandbox execution; Supplementary Table S1 reports sandbox type and execution cost (pp. 3, 13, 57). |
| “uses task scores to explore a candidate tree” | **Supported** | Scores become rank scores in PUCT selection; candidates are appended and visits backpropagated (pp. 13-14). |
| “research ideas from papers, expert advice, search/research agents, and previous solutions can be injected into prompts” | **Supported with scope qualification** | The paper documents literature summaries, expert advice, Deep Research, AI co-scientist, prior method descriptions, and previous solution recombination (pp. 2-3, 7-9, 15, 62, 74-78). These are available inputs/workflows, not proof that every run automatically retrieves all sources. |
| “including an LLM-mediated recombination step” | **Supported** | Parent solutions are compared by Gemini, the comparison is inserted into a hybrid prompt, and ERA searches from it (p. 15; Supplementary Tables S7 and S17). |
| “evaluated across Kaggle and six scientific/engineering task families” | **Supported, with benchmark distinction** | Kaggle contains 16 playground competitions; the six named scientific tasks are scRNA-seq, COVID forecasting, time series, geospatial segmentation, ZAPBench, and numerical integration (pp. 2-4, 10, 57). |
| “reported expert-level or leaderboard-beating results” | **Supported as the paper's reported result claim** | The abstract and Results report leaderboard/benchmark gains and expert-level performance; the exact metrics, splits, comparisons, and limitations are task-specific (pp. 1, 4-12, 18-19, 34, 39-56, 71-73). This wording should not be expanded into a claim of universal human superiority. |
| “closes a computational generate-execute-score-regenerate loop” | **Supported** | Candidate generation, sandbox execution, scoring, tree selection, and iterative child generation are explicit in Fig. 1 and Methods (pp. 3, 13-14). |
| “evaluator is a task metric rather than a general novelty or scientific-truth validator” | **Supported and important limitation** | The score is task-specific; the paper itself distinguishes empirical predictive optimization from genuine discovery and says the evaluated problems primarily emphasize automated scoring (p. 12; Methods pp. 13-19). |

### Frozen-clause conclusion

**Overall verdict: `supported_with_scope_qualification`.** The frozen description accurately identifies ERA and its computational architecture. The required qualification is that research-idea injection is prompt-mediated and may be user-, literature-, or agent-supplied rather than an always-on autonomous ideation module; and “expert-level/leaderboard-beating” is a reported, task- and split-specific outcome, not a general claim about scientific discovery or truth.

## Architecture-level limitations and non-equivalences

1. **Metric closure is not scientific closure.** The loop closes around a measurable task score. It does not autonomously certify novelty, causal explanation, theoretical correctness, or real-world scientific significance (p. 12; pp. 13-19).
2. **External research is an input channel.** Papers and research-agent outputs can guide the LLM, but the PDF does not define a persistent memory, autonomous literature policy, or general hypothesis-generation controller. The core implementation is code mutation with ideas in prompts (pp. 2-3, 13, 62, 74-78).
3. **Human involvement remains in the experimental setup and auditing.** Task selection, advice, method selection, prompt construction, benchmark design, and manual adherence checks are documented. The paper does not claim that all scientific problem formulation is autonomous (pp. 4-7, 15-19, 34, 67-70).
4. **Benchmark success has task-specific validity boundaries.** Leaderboard and holdout results demonstrate performance on the selected metrics and splits. They do not by themselves establish transfer to unscored scientific questions or physical experiments (pp. 4-12, 16-19, 39-56).
5. **Safety risk is acknowledged.** The authors state that automating expert software lowers the barrier to sophisticated computational work, including in sensitive domains (p. 12). This is a risk statement, not an implemented safety validator.

## Evidence completeness

- [x] Identity, title, authors, date/version, and affiliations recorded from p. 1.
- [x] Pages 1-78 read and structurally accounted for.
- [x] Problem statement, motivation, and surrounding methodological context recorded.
- [x] Core architecture, search rule, evaluator, prompt inputs, recombination path, and evaluation scope recorded.
- [x] Frozen supplementary description stated and every clause assessed with enclosing PDF pages.
- [x] Boundary between computational score optimization and genuine scientific discovery recorded.

EVIDENCE_COMPLETE: yes
