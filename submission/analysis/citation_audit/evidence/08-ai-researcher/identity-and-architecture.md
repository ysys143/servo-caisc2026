# AI-Researcher: identity and architecture audit

## Audit boundary and source identity

- **Audited source:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/AI-Researcher Autonomous Scientific Innovation.pdf`
- **Title:** *AI-Researcher: Autonomous Scientific Innovation*
- **Authors:** Jiabin Tang, Lianghao Xia, Zhonghang Li, and Chao Huang; The University of Hong Kong.
- **Version/date shown in the PDF:** arXiv:2505.18705v1, 24 May 2025; the footer identifies it as a preprint under review.
- **Extent:** 38 PDF pages, letter size. The PDF has been read sequentially from page 1 through page 38, including figures, tables, references, and Appendix A.1-A.7 prompts.
- **SHA-256:** `a3f3334cc67685b925c9523dc19149806ee996e331623f84912e0354b18c9bce`.
- **Manifest comparison:** exact match to `submission/analysis/citation_audit/core14-manifest.json` for path, hash, page count, title, and system identity. The manifest has no manuscript citation occurrence for this catalog-only system.
- **Scope constraint:** This audit used only the specified PDF and repository-local manifest/context. No API or model call was made, and no other paper PDF was opened.

## 38-page complete structure and reading record

| PDF pages | Contents and role in the paper |
|---|---|
| 1-2 | Title, abstract, Introduction, Figure 1, motivation, claimed end-to-end pipeline, and three claimed innovations: Resource Analyst, iterative implementation refinement, and hierarchical documentation. |
| 3-4 | Scientist-Bench task formulation and construction. Inputs are references `R`, an instruction `I`, and datasets `D`; Level 1 is guided innovation and Level 2 omits the explicit instruction. Benchmark paper selection, reference extraction, instruction generation, anonymization, and two-stage code/scientific evaluation are specified. |
| 5-6 | Evaluation-framework continuation and Figure 2; the three-stage AI-Researcher framework begins. Knowledge Acquisition finds papers/repositories; Resource Analyst decomposes concepts, extracts formulas from LaTeX, maps them to code, and creates a plan. |
| 7-8 | Idea Generator and divergent-convergent selection of five directions; Code Agent, Advisor Agent, multi-stage refinement, prototype-to-full experiments, and Automated Documentation Agent. Figure 3 shows the forward research trajectory from plan to implementation, experiments, and writing. |
| 9-10 | Experiment settings, 22-paper Scientist-Bench statistics, Level 1/Level 2 protocols, completion/correctness metrics, and LLM-as-judge setup. The paper reports 93.8% completeness and mean correctness 2.65 for the stated Claude-series evaluation, while the judge protocol uses multiple named LLMs. |
| 11-12 | RQ1 continuation and pairwise AI-versus-human evaluation. Tables 2 and associated text report evaluator-dependent ratings and comparable percentages; the evaluators disagree materially. |
| 13-15 | RQ3 open-ended results, RQ4 backbone comparison, RQ5 ICLR accepted/rejected pair validation, and Table 5. The paper reports 32 accepted/rejected pairs and 65.62%-90.62% selection accuracy, with Gemini excluded from primary experiments. |
| 16-18 | RQ6 rotation-VQ case study, claimed emergent experimental thoroughness, Figure 10 failure cases, domain-knowledge and reasoning-depth limitations, and future directions. |
| 19-20 | Related work, implementation-fidelity discussion, multi-turn premature completion, and memory-management limitations. The paper explicitly says the current implementation has no dedicated external memory and relies primarily on the LLM context window and summaries. Evaluation limitations and conclusion follow. |
| 21-22 | References [1]-[27]. These pages are part of the 38-page source and were read as references, not as separate sources. |
| 23-24 | Appendix A, tool definitions, and Knowledge Acquisition Agent tools/system prompt. |
| 25-26 | Knowledge Acquisition continuation, Resource Analyst Paper Analyst and Code Analyst tools/prompts. |
| 27-29 | Plan Agent prompt and Code Agent tools, self-contained-project rules, no direct imports from reference codebases, and implementation checklist. |
| 30-31 | Advisor Agent architecture, Judge Agent, Code Review Agent, and Experiment Analysis Agent tools/prompts. |
| 32-35 | Automated Documentation Agent's three-stage structure, section-writing, and methodology-review prompts. |
| 35-38 | Scientist-Bench benchmark-construction prompts: five-step reference extraction, Level-1 research-instruction generation, model-name/self-reference anonymization. |

## Problem statement and context

The paper frames scientific discovery as a large, uncertain solution-space search requiring literature synthesis, hypothesis generation, experimental adaptation, implementation fidelity, and scholarly communication (pp. 1-3). It argues that ordinary agents handle narrower task automation but do not coordinate the full path from literature to publication-quality report. It also identifies a benchmark gap: autonomous research systems lack a standardized comparison against human-authored scientific work (pp. 2-4).

The paper positions AI-Researcher among tool-integration, multi-agent collaboration, and self-directed agent frameworks, then among end-to-end AI research systems (pp. 18-19). Its own framing is ambitious: “fully autonomous” and “complete scientific discovery lifecycle.” However, the operational setup still begins from user-provided references, a specified or benchmark-derived research setting, available datasets, and a containerized workspace. The paper's own discussion also records important limits: missing dedicated external memory, summary compression across stages, premature task completion in multi-turn coding, shallow theoretical analysis, and LLM reviewers' tendency to overvalue presentation (pp. 17-20).

## Architecture and method

1. **Knowledge acquisition.** The user provides 10-15 reference papers. The Knowledge Acquisition Agent searches for relevant papers and code repositories, selects at least five codebases using recency, stars/popularity, documentation, relevance, and citation impact, and retrieves associated arXiv/LaTeX material (pp. 5-6; Appendix A.2, pp. 24-25). The appendix prompt additionally prefers Python/local execution and PyTorch and tells the agent to choose 5-8 repositories.
2. **Resource analysis and planning.** The Resource Analyst uses Paper Analyst and Code Analyst sub-agents to decompose an idea into atomic concepts, extract mathematical definitions/formulas from papers, locate corresponding code, and form bidirectional paper-code concept profiles. A Plan Agent turns these notes into dataset, model, training, and testing plans (p. 6; Appendix A.3, pp. 25-28).
3. **Divergent-convergent ideation.** The Idea Generator searches for gaps, contradictions, and patterns, produces five distinct directions, and ranks them on scientific novelty, technical soundness, and transformative potential. One direction is selected for development (p. 7). The paper describes this as exploration beyond direct recombination, but it is still generated from the acquired literature/code context.
4. **Implementation and validation.** A Code Agent creates a self-contained project and is instructed not to import directly from reference codebases. A Judge/Code Review/Advisor arrangement checks atomic concepts against the implementation. The Code Agent first tests small data or 1-2 epochs, then performs full experiments after feedback; repeated failure can be classified as “unfeasible” (pp. 7-8; Appendix A.4-A.5, pp. 28-31).
5. **Documentation.** The Documentation Agent synthesizes reasoning traces, execution logs, code, and results. It first builds a hierarchical LaTeX structure, then writes subsections using content and templates, then reviews the methodology against an academic checklist (p. 8; Appendix A.6, pp. 32-35).
6. **Evaluation.** Scientist-Bench uses 22 target papers across diffusion models, vector quantization, graph neural networks, and recommender systems. Level 1 supplies an extracted research instruction; Level 2 supplies references and datasets without that instruction. Code is assessed for completeness/correctness, and passing outputs are pairwise compared with human target papers by multiple LLM judges on novelty, rigor, and empirical validation (pp. 3-5, 9-15). Appendix A.7 gives reference extraction, instruction-generation, and anonymization prompts (pp. 35-38).

The architecture is predominantly forward: literature and resource analysis precede ideation; the selected idea proceeds through planning, coding, review, experiments, and documentation. The implementation/advisor loop feeds results and critiques back into implementation refinement, but the paper does not specify a result-to-ideation feedback loop. The paper also explicitly acknowledges that the current system has no dedicated external memory (pp. 19-20).

## Frozen supplementary description

Frozen text from `core14-manifest.json`:

> An LLM pipeline for machine-learning research across a few domains. A knowledge-acquisition step reads reference papers to scope the problem; a divergent-convergent step generates several research directions and selects one by novelty, soundness, and transformative-potential criteria; code and advisor agents implement and run experiments in containers with multi-stage refinement. Outputs were compared pairwise against human papers by several LLM judges on a benchmark. It uses no external memory beyond the model context, and the pipeline runs forward without feeding results back to ideation.

## Clause-level cross-check

| Frozen clause | Verdict | PDF-grounded assessment |
|---|---|---|
| “An LLM pipeline for machine-learning research across a few domains.” | **Supported, with scope qualification** | The paper presents a multi-agent LLM pipeline and evaluates four named domains in Table 1: diffusion models, vector quantization, graph neural networks, and recommender systems (pp. 3, 9). “A few domains” is accurate for the reported evaluation, but the paper also claims intended use across diverse AI domains; the evidence is not a general-domain demonstration. |
| “A knowledge-acquisition step reads reference papers to scope the problem.” | **Supported, but incomplete** | Knowledge Acquisition starts from 10-15 user-provided reference papers, retrieves/filters repositories and related papers, and Resource Analyst extracts concepts, formulas, code mappings, and plans (pp. 5-6; Appendix A.2-A.3, pp. 24-28). The clause should expose that the input is human-supplied references and that code repositories/LaTeX are also acquired. |
| “A divergent-convergent step generates several research directions and selects one by novelty, soundness, and transformative-potential criteria.” | **Supported** | The Idea Generator explicitly produces five conceptually distinct directions and selects one using Scientific Novelty, Technical Soundness, and Transformative Potential (p. 7). “Several” is less precise than the paper's stated five. The selection is agentic ranking, not an externally validated novelty test. |
| “Code and advisor agents implement and run experiments in containers with multi-stage refinement.” | **Supported, with role and container qualification** | Code Agent and Advisor Agent form an iterative implementation/review cycle; prototype tests precede full experiments and unsuccessful paths can be marked unfeasible (pp. 7-8). Docker/container execution is stated for analysis and the secure research environment (p. 6), while Appendix prompts describe the workspace as `/workplace` and the Code Agent's execution tools; the frozen wording should not imply that every operation is independently proven container-isolated. |
| “Outputs were compared pairwise against human papers by several LLM judges on a benchmark.” | **Supported** | Scientist-Bench compares generated reports against corresponding human target papers; the protocol uses pairwise ratings, multiple LLM evaluators, and 22 benchmark papers (pp. 3-5, 9-15). The paper reports strong evaluator divergence, so the clause should retain that these are LLM-judge assessments rather than human peer-review outcomes. |
| “It uses no external memory beyond the model context.” | **Supported, but wording needs precision** | Section 6.2 explicitly states that the present implementation has no dedicated external memory-management system and relies primarily on the LLM's native context window, with summarized prior-stage outputs (pp. 19-20). This does **not** mean the system has no external research materials: it reads papers, repositories, LaTeX, code, datasets, logs, and project files. The accurate claim is “no dedicated cross-stage external memory system.” |
| “The pipeline runs forward without feeding results back to ideation.” | **Supported for the documented architecture** | Figure 2 and Figure 3 place ideation before implementation and documentation; the explicit feedback cycle is between Code Agent, Advisor Agent, experiments, and implementation refinement (pp. 5, 7-8). No paper passage or prompt specifies returning experimental results to the Idea Generator to regenerate/rerank research directions. This is a claim about the documented control flow, not proof that no hidden implementation path exists. |

## Verdict and corrected frozen description

**Overall verdict: `minor_revision`.** The frozen description captures the system identity and main control-flow architecture. It should be revised for reproducibility and to avoid two misleading compressions: “no external memory” must distinguish memory architecture from external research files, and the container claim should be scoped to the stated secure research environment rather than treated as independently demonstrated for every agent operation. It should also state the exact five ideation directions and the 22-paper/four-domain evaluation scope.

Suggested corrected description:

> An LLM multi-agent pipeline evaluated on machine-learning research tasks in four reported domains. It begins from user-provided reference papers and acquires related papers, code repositories, and LaTeX material to scope and formalize the problem. An Idea Generator produces five directions and selects one using novelty, technical soundness, and transformative-potential criteria. Code, advisor/review, and experiment-analysis agents implement and refine the selected idea through prototype and full experiments in the stated containerized research environment. Generated outputs are compared pairwise with 22 human target papers in Scientist-Bench by multiple LLM judges. The implementation has no dedicated cross-stage external-memory system beyond the LLM context and summarized artifacts, and its documented feedback loop refines implementation/experiments rather than feeding results back into ideation.

## Evidence completion

- [x] PDF identity, hash, and 38-page extent fixed against the repository manifest.
- [x] Pages 1-38 read sequentially, including figures, tables, references, and Appendix A.1-A.7.
- [x] Problem statement, context, architecture, methods, evaluation, limitations, and conclusion recorded.
- [x] Every clause of the frozen supplementary description assessed with enclosing PDF pages.
- [x] No API/model call made; no other paper PDF opened.

EVIDENCE_COMPLETE: yes
