# NovelSeek / InternAgent: identity and architecture audit

## Audit scope and source control

- **Audited source:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Reference/NovelSeek - When Agent Becomes the Scientist.pdf`
- **Source restriction:** this audit directly read this one PDF only. No API call, model call, web lookup, or other PDF was used.
- **Length:** 34 PDF pages, verified from the PDF page tree and read page-by-page. Page references below are PDF page numbers.
- **Source identity:** the filename and local audit key call the item “NovelSeek”, but the PDF itself identifies the work as **InternAgent: When Agent Becomes the Scientist - Building Closed-Loop System from Hypothesis to Verification** (p. 1). The first-page metadata line is `arXiv:2505.16938v3 [cs.AI] 22 Jul 2025` (p. 1).

## Paper identity

The paper presents the Shanghai Artificial Intelligence Laboratory InternAgent team and links a project page, GitHub repository, and Hugging Face page on the title page (p. 1). The abstract calls InternAgent a “unified closed-loop multi-agent framework” for autonomous scientific research across multiple fields (p. 2). It claims three headline properties: scalability across 12 scientific research tasks, interactivity through human-expert feedback and multi-agent interaction, and efficiency gains relative to human effort (p. 2).

The paper's own object is therefore **InternAgent**, not a separately named system called NovelSeek. “NovelSeek” is retained here only because it is the frozen audit identifier and the supplied PDF filename.

## Complete 34-page structure

This is the page-by-page structural map of the complete PDF, including the appendix and software/application material:

| Pages | Content |
|---|---|
| 1 | Title, authors/links, overview figure showing 12 supported task types |
| 2-3 | Abstract; Introduction; motivation/challenges; contributions; start of InternAgent overview |
| 4-7 | Section 2.1: self-evolving idea generation with human-interactive feedback; Survey, Code Review, Idea Innovation, Assessment, and Orchestration agents; idea self-evolution figure |
| 8-9 | Section 2.2 idea-to-methodology construction; methodology initialization/refinement; Section 2.3 evolutionary experimental planning/execution; exception-guided debugging; adaptive planning |
| 9-12 | Section 3 experiments; task descriptions, datasets/baselines, metrics, implementation details, and start of quantitative results |
| 13-17 | Quantitative comparison tables, experiment statistics/costs, ablations, and comparison with AI-Scientist-V2/AI-Researcher |
| 18-20 | Section 4 case studies; AutoRYP, AutoMD, AutoPower, and experimental-planning/adaptive-evolution visual examples |
| 20-21 | Human evaluation and Table 10; Section 5 related work |
| 22 | Related-work continuation; Section 6 conclusion and future work |
| 23-26 | References |
| 27 | Appendix A contributions/acknowledgments; Appendix B evaluation details begins |
| 28-29 | Reviewer-style scoring rubric; evaluator qualifications and procedure; Appendix C software development/application interface |
| 30 | Trial-application material and AutoTPPR planning visual example |
| 31-34 | Additional generated idea/method/code case studies for AutoRYP/AutoMD/AutoPower/AutoSenCls/Auto3DCls/Auto2DCls; software-platform figure on p. 34 |

The rendered pages confirm that the latter pages are not blank or missing: pages 31-34 contain two-column idea/method/code artifacts and p. 34 also contains Figure 13 and application-interface text.

## Problem statement, context, and motivation

The Introduction defines Autonomous Scientific Discovery as using LLMs and robotics to perform scientific research without direct human intervention (p. 2). The paper motivates automation of data analysis, hypothesis generation, experiment design, and result interpretation. It identifies two central obstacles:

1. **Proposal quality:** generating hypotheses that are both novel and effective requires balancing creativity, scientific validity, and broad contextual understanding (p. 2).
2. **Closed-loop validation:** a system must design experiments, execute them, analyze results, and refine hypotheses while handling cross-domain integration, unexpected variables, noise, and uncertainty (p. 2).

The claimed response is an end-to-end pipeline with four named modules: self-evolving idea generation, human-interactive feedback, idea-to-methodology construction, and multi-round experiment planning/execution (pp. 2-3). The paper frames the contribution as reducing human effort while validating generated modules experimentally, and reports that baselines and generated code were open-sourced for reproducibility (p. 3).

## Architecture and method

### 1. Self-evolving idea generation

Figure 2 and Section 2.1 divide the capability among specialized agents (pp. 4-7):

- **Survey Agent:** searches literature in literature-review and deep-research modes. It generates keyword combinations from task descriptions, ranks relevance, and expands the survey after an initial pass (pp. 4-5).
- **Code Review Agent:** analyzes baseline repositories, file structure, functions, dependencies, and context. It uses Python `ast` parsing for static structure analysis and produces human-readable summaries (p. 5).
- **Idea Innovation Agent:** generates ideas from task definitions, baseline methods, and scientific knowledge, then evolves ideas using novelty, feasibility, and scientific-validity feedback (pp. 5-6).
- **Assessment Agent:** evaluates ideas across multiple dimensions, supplies explanations, and promotes diversity among highly ranked ideas (p. 6).
- **Orchestration Agent:** coordinates the agents, synchronizes data flow, chooses workflow timing, and manages when human feedback is solicited, especially for high-scoring ideas (p. 7).

The implementation details later state that the survey/code-review/generation/self-evolving/orchestration agents use GPT-4o; the survey reviews 50 papers, the generation stage makes 15 ideas, each is evolved into 3 ideas, and the top 5 continue until four evolutions (p. 12). This is paper-reported configuration, not an independently rerun result.

### 2. Human-interactive feedback

The paper explicitly distinguishes two feedback sources: (1) feedback directly provided by humans and (2) feedback automatically generated by an agent (p. 6). Human feedback can redirect an idea toward domain-specific requirements, after which the system regenerates or adjusts ideas. The Orchestration Agent controls the timing of this feedback (p. 7). Figure 2 also depicts a human-interactive feedback path in the idea-generation subsystem (p. 4).

The interface is not described as a mandatory approval gate for every run. The paper describes it as a collaboration capability and presents a platform with user entry, task selection, idea-tree visualization, human-computer interaction, code generation, and auto-debug interfaces (p. 34). The paper also says future functionality includes custom dataset uploads and academic idea-thinking modes (p. 34).

### 3. Idea-to-methodology construction

Section 2.2 describes a Method Development Agent with two capabilities (p. 8):

- **Methodology initialization:** combines the idea with task descriptions, baseline code/methods, and relevant literature to make an executable method structure.
- **Methodology refinement:** iteratively applies structured critiques, automated assessments, expert feedback, and current literature to improve rigor and completeness.

The Method Development Agent collaborates with the Assessment Agent and Orchestration Agent. The paper's formal descriptions make the transformation `idea -> initial methodology -> refined methodology` explicit, but the equations are conceptual interfaces rather than a fully specified reproducible algorithm (p. 8).

### 4. Experimental planning, execution, and adaptive evolution

Section 2.3 presents two linked mechanisms (pp. 8-9):

- **Exception-guided debugging:** execution attempts produce runtime exceptions; the system captures the traceback, analyzes it, modifies code, and retries. Aider is used for single-file or limited-scope implementation tasks, while the paper describes project-level/multi-file handling separately (pp. 8-9).
- **Experimental planning and adaptive evolution:** the implementation is planned at architectural, module, and function levels; after execution, performance and logs inform the next plan step. Figure 2 labels the loop as experimental plan -> coding agent -> execution/training logs -> performance reflection/next plan step (p. 4; expanded in pp. 9 and 20).

The implementation details state that the method is initialized/refined once, and the maximum Aider run number is 5 while the multi-round experimental execution limit is 3 (p. 12). The paper evaluates 12 tasks spanning scientific and AI modalities, with task-specific datasets, baselines, and metrics (pp. 9-12).

## Unified multi-agent loop

The paper's loop can be reconstructed from the prose and Figure 2 as:

`task + literature + baseline repository -> survey/code understanding -> idea generation -> assessment/ranking/diversity -> optional human/agent feedback -> idea evolution -> methodology initialization -> methodology refinement -> experimental plan -> code implementation/debugging -> execution/training -> result/performance feedback -> adaptive next plan and further experiments`.

Evidence for each transition is distributed across the paper rather than specified as one executable protocol:

- The contribution statement explicitly names idea generation, idea-to-methodology transformation, experiment execution, and result feedback as one closed cycle (p. 3).
- Section 2.1 supplies the multi-agent idea and feedback stages (pp. 4-7).
- Section 2.2 supplies the methodology bridge and critique/refinement stages (p. 8).
- Section 2.3 supplies execution, exception recovery, and adaptive planning (pp. 8-9).
- The conclusion restates that the system starts from an initial idea, refines it, transforms it into a detailed methodology, implements it through multi-round planning/execution, and thereby completes the closed loop (p. 22).

**Qualification:** “closed-loop” is directly supported as the authors' architecture claim. The paper demonstrates computational experiments and code/result feedback; it does not establish a physical wet-lab robotics loop in this 34-page source. The 12 tasks shown on pp. 1 and 9-12 are computational/AI research tasks.

## Frozen supplementary description: clause-by-clause comparison

Frozen description under audit:

> “A unified multi-agent framework that runs idea generation, conversion of ideas into methodology, computational experiment execution, and result feedback in a loop across many tasks, reporting improvements on task benchmarks relative to baselines. A human-interaction interface is optional rather than required for operation. Experiments are computational.”

| Frozen clause | PDF evidence | Decision |
|---|---|---|
| “A unified multi-agent framework” | Abstract and Section 2 call InternAgent a unified closed-loop multi-agent framework; Figure 2 shows specialized agents and an Orchestration Agent (pp. 2, 4, 7). | **CONFIRMED.** |
| “runs idea generation” | Self-evolving idea-generation capability and Idea Innovation Agent are described in Sections 2.1 (pp. 4-6). | **CONFIRMED.** |
| “conversion of ideas into methodology” | Section 2.2 explicitly describes idea-to-methodology construction, initialization, and refinement (p. 8). | **CONFIRMED.** |
| “computational experiment execution” | The experiments are code/data/model tasks across 12 AI/science benchmarks; the pipeline includes Coding Agent, execution, logs, and debugging (pp. 1, 4, 8-12). | **CONFIRMED, with scope stated as computational in this source.** |
| “and result feedback” | The contribution and conclusion explicitly include result feedback; performance/log feedback drives the next plan step (pp. 3-4, 9, 22). | **CONFIRMED.** |
| “in a loop” | The authors repeatedly call the system closed-loop and describe multi-round execution and adaptive evolution (pp. 2-4, 8-9, 22). | **CONFIRMED as the paper's architectural claim.** |
| “across many tasks” | Figure 1 lists 12 task types; Section 3 says 12 distinct tasks and details their datasets/baselines (pp. 1, 9-12). | **CONFIRMED.** “Many” is less precise than the paper's number: **12**. |
| “reporting improvements on task benchmarks relative to baselines” | Abstract reports concrete gains; Tables 1-9 report task performance, statistics, costs, ablation, and comparisons; the text says InternAgent improves over baselines and compares against DOLPHIN/AI-Scientist-V2/AI-Researcher (pp. 2, 12-17). | **CONFIRMED as a reported result.** This audit does not independently verify the numbers. |
| “A human-interaction interface” | The paper explicitly describes human-interactive feedback and a software platform with user-entry, task-selection, idea-tree, human-computer interaction, code-generation, and auto-debug interfaces (pp. 4, 6-7, 34). | **CONFIRMED.** |
| “is optional rather than required for operation” | The paper describes human feedback as a capability and shows automated agent feedback as a separate feedback type (p. 6), but does not state this exact “optional rather than required” rule or provide a no-human ablation of the full system. | **PARTIALLY SUPPORTED / wording is an inference.** The safer source-faithful wording is “human interaction is supported and can enter the feedback workflow; agent-generated feedback is also described.” |
| “Experiments are computational.” | All enumerated tasks use datasets, baseline code, training/evaluation metrics, and computational models; no physical wet-lab experiment is described in the paper (pp. 1, 9-17). | **CONFIRMED for this PDF.** |

## Bottom-line audit finding

The frozen description is substantively aligned with the PDF for identity-level architecture: InternAgent is a unified multi-agent, idea-to-methodology-to-computation loop evaluated across 12 tasks. The only clause requiring qualification is the categorical claim that the human interface is “optional rather than required.” The PDF supports a human-interactive capability plus agent-generated feedback, but it does not explicitly formalize optionality as an operational guarantee. The PDF identity itself should be recorded as **InternAgent**, with “NovelSeek” treated as the local audit/file alias.

EVIDENCE_COMPLETE: yes
