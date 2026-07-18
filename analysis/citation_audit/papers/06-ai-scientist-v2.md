# `ai_scientist_v2` Full-Text Audit

## Source Identity

- **Citation key:** none. This is a catalog-only core system; the manuscript has no English or Korean citation occurrence for this source.
- **PDF title:** *The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search*.
- **Authors:** Yutaro Yamada, Robert Tjarko Lange, Cong Lu, Shengran Hu, Chris Lu, Jakob Foerster, Jeff Clune, and David Ha (PDF p. 1).
- **Identifier/version:** `arXiv:2504.08066v1 [cs.AI]`, 10 April 2025 (PDF p. 1). The rendered title page also shows `2025-4-14`; this is a local document date, not a different arXiv version.
- **Absolute PDF path:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/The AI Scientist-v2 Workshop-Level Automated Scientific Discovery via Agentic Tree Search.pdf`
- **SHA-256:** `53bafd3028e3f8829a3d85220e84dcf0d18934f9b75c092a60de303ff3644bd2`.
- **PDF properties:** 69 pages, unencrypted, A4, 8,923,691 bytes. The PDF metadata title/author fields are blank, so identity is taken from the rendered title page and arXiv stamp.
- **Version status:** `exact`. The title, authors, arXiv identifier, `v1` marker, path, hash, and page count agree with the frozen core manifest.
- **Scope:** catalog-only publication artifact audit. No direct manuscript citation link is being evaluated, but the system/method family is substantively represented elsewhere in the manuscript's audited system analysis through the Nature 2026 artifact described below.

## Full-Text Coverage

Pages 1-69 were read sequentially with page-bounded layout-preserving extraction. Coverage included:

- pp. 1-4: identity, abstract, v1 comparison, background, idea generation, Semantic Scholar novelty search, and template removal.
- pp. 5-8: experiment-progress manager, four stages, stopping criteria, parallel agentic tree search, replication and aggregation nodes, Hugging Face loading, VLM feedback, and workflow figures.
- pp. 9-15: workshop evaluation protocol, human selection boundaries, three submissions, withdrawal, internal and external review, limitations, related work, and conclusion.
- pp. 16-20: references, author contributions, and supplementary table of contents.
- pp. 21-30: model assignments, execution budgets, and the complete idea, experiment, plotting, writing, reflection, VLM-review, and duplicate-check prompts.
- pp. 31-44: the complete compositional-regularization output, annotations, human scientific review, and code review.
- pp. 45-57: the complete label-noise output, supplement, human/code review, and workshop reviews.
- pp. 58-69: the pest-detection idea, manual dataset preparation, complete output, human/code review, and three workshop reviews.

Embedded generated papers restart their own printed page numbering. All page references in this report use the enclosing PDF page number. Pages 1, 2, 3, 6, 8, 21, 31, 42, 55, and 66 were also rendered and visually inspected. The central workflow figures, comparison tables, generated-paper figures, and code-review figures were legible enough to verify the relevant layout and labels.

## Problem and Context

The paper addresses the narrow problem of automating computational machine-learning research end to end. It positions v1 as constrained by human-authored code templates and linear, shallow experimentation, then proposes v2 as a more general pipeline that can generate ideas, write and execute code, analyze results, create figures, write manuscripts, and review them (PDF pp. 1-4).

The disciplinary context is LLM-agent scaffolding, code-generation search, automated scientific discovery, and AI-assisted research. The paper connects its tree search to AIDE and related LLM reasoning scaffolds, while distinguishing systems that retain human oversight or omit experimental execution (PDF pp. 3-4, 14-18). Its demonstrated domain is computational ML: synthetic arithmetic, image calibration under label noise, and image classification for pest detection (PDF pp. 31-69). It is not a physical laboratory or real-world deployment system.

The central concern is therefore not whether the system can run code once, but whether a pipeline with idea generation, search, replication, review, and manuscript production can produce research artifacts that survive human evaluation. The authors explicitly frame the workshop experiment as preliminary and distinguish workshop-level acceptance from main-track scientific quality (PDF pp. 9, 13-15).

## Structure and Argument

The document proceeds from abstract and v1 comparison (pp. 1-2), to background and the v2 workflow (pp. 3-8), to a controlled human evaluation (pp. 8-10), detailed analysis of the selected output and reviewers (pp. 10-13), limitations and related work (pp. 13-15), and conclusion (p. 15). References and author contributions follow (pp. 16-19).

The supplementary material then exposes model and execution settings, prompts, and all three generated manuscripts with internal scientific/code reviews and external workshop reviews (pp. 20-69). This structure is important evidence: the paper's claims about autonomy are accompanied by artifacts that also reveal data leakage, figure errors, unused methods, missing citations, and failed domain-adaptation paths.

The argument distinguishes mechanisms from outcomes only imperfectly. The four-stage manager, tree search, replication nodes, and VLM feedback are described as implemented mechanisms (pp. 5-8). The stronger claims that these mechanisms produce deeper exploration, better figures, or reliable scientific quality are not established by a controlled ablation or reviewer-agreement analysis.

### Cross-artifact relationship to the Nature 2026 paper

The already audited Nature 2026 paper (`lu2026aiscientist`) is a separate publication artifact, not a duplicate citation identity. Its Methods explicitly describes a template-free mode using a four-stage agentic tree search, and its code-availability statement points to `github.com/SakanaAI/AI-Scientist-v2`. Those method-family facts are consistent with the architecture described in this 69-page Yamada et al. arXiv preprint (especially PDF pp. 1-8).

This relationship must be represented as a cross-artifact crosswalk, not as a citation merge. Yamada et al. 2025 (`arXiv:2504.08066v1`) is the catalog-only source being audited here; the Nature 2026 paper is the separately cited/assessed publication artifact. The Nature paper's template-free mode provides substantive system-method coverage in the manuscript, while this report provides the full 69-page evidence and the specific workshop/output context of the v2 preprint. The shared repository and method family do not make the two PDFs the same publication or justify transferring every result, reviewer metric, or human-boundary statement from one artifact to the other.

## Methods and Evidence

### Idea generation and human gates

The system receives a human-supplied workshop theme or broad topic prompt. It generates roughly twenty core-ML ideas, then the researchers modify the prompt toward applied domains and generate roughly twenty more. They select three ideas without editing them, run each selected idea multiple times with different seeds, and select the best complete manuscript for submission (PDF p. 10). The prompts require literature search and structured idea output, including novelty and feasibility reasoning (PDF pp. 21-23).

This is autonomous within a selected run, not autonomous from topic definition through submission. Humans provide the theme, choose initial ideas, provision compute, start the runs, select the best output, and conduct post-run scientific and code review. For pest detection, humans manually downloaded and reduced a Kaggle dataset because automatic acquisition was unsuccessful (PDF p. 58). Author contributions explicitly record reading and validating generated papers, selecting submissions, and checking code (PDF p. 19).

### Experiment-progress manager and tree search

The manager coordinates four stages: preliminary investigation, hyperparameter tuning, research-agenda execution, and ablation studies. Stage 1 stops after a working prototype; Stage 2 uses stabilization across training curves and at least two datasets; Stages 3 and 4 end when budget is exhausted, with an additional runtime-complexity check for Stage 3 (PDF pp. 5-6).

Each node contains a plan, Python code, runtime, metrics, error traces, plots, LLM feedback, VLM feedback, and a buggy/non-buggy status. Buggy nodes are debugged; non-buggy nodes are refined. An LLM selects nodes using performance, training dynamics, and plot quality, and new nodes are executed concurrently (PDF pp. 5-7). Hyperparameter, ablation, replication, and aggregation nodes provide specialized roles. Replication nodes use different seeds, while aggregation nodes calculate and visualize means and standard deviations (PDF pp. 6-7).

The source demonstrates the mechanism and its execution schema, but does not present a controlled tree-search-versus-linear-search comparison, a complete node/seed ledger for all outputs, or an outcome showing that tree search itself caused better science. Thus the mechanism is source-grounded; comparative effectiveness is not.

### VLM and manuscript review

VLMs inspect figures during experiments and during manuscript reflection. The checks include labels, legends, misleading visualizations, caption alignment, figure-text alignment, and duplicate figures (PDF pp. 7-8, 28-31). An LLM paper-review stage is also present in the workflow (PDF pp. 1-3, 7-8).

The supplied outputs show the boundary of this evidence. Human review still found inaccurate captions, duplicate figures, missing reliability diagrams, claims about unexecuted temperature scaling, and misleading domain-adaptation descriptions (PDF pp. 35-44, 46-57, 58-69). No automated-review calibration, inter-rater agreement, or before/after VLM ablation is reported.

### Human evaluation protocol

Three AI-generated manuscripts were submitted blind among 43 ICBINB workshop submissions. Reviewers were told that some submissions might be AI-generated but not which ones. One manuscript received scores 6, 6, and 7, averaging 6.33 and exceeding the stated workshop threshold; two were rejected (PDF pp. 8-10, 31). The accepted manuscript was withdrawn by prior agreement and did not enter the public scientific record (PDF pp. 9, 13).

The source also includes internal scientific/code review and external workshop reviews. The internal review judged none of the manuscripts to meet top-tier main-conference standards, and the appendices document concrete flaws in all three output pipelines (PDF pp. 9, 11-14, 41-69).

## Findings

- The system removes v1's human-authored template dependency and uses a domain-general idea-to-manuscript workflow (PDF pp. 1-4).
- It implements four-stage, parallel agentic tree search with debugging, refinement, hyperparameter, ablation, replication, and aggregation nodes (PDF pp. 5-7).
- It includes VLM figure feedback and an automated paper-review stage (PDF pp. 7-8).
- In the reported evaluation, three ideas were selected from roughly forty generated candidates, each selected idea was run under multiple seeds, and one best output per idea was submitted (PDF p. 10).
- One of three submissions cleared the stated workshop threshold with scores 6, 6, and 7; the other two were rejected, and the threshold-clearing paper was withdrawn (PDF pp. 8-10, 31).
- Replication/aggregation is specified to report means and standard deviations over seeds, but the PDF does not provide a complete seed-level audit trail for every reported result (PDF pp. 5-7, 35).
- The generated outputs expose failure modes: approximately 57% train/test overlap in a code-review check, incorrect or duplicated figures, an implemented-but-unused temperature-scaling method, missing evidence for reliability diagrams, and a failed domain-adaptation path (PDF pp. 35-44, 46-57, 58-69).
- The evidence supports computational research automation, not general scientific autonomy, reliable automated validation, physical experimentation, or real-world deployment.

## Limitations

The study is small: three submissions, one workshop, and one threshold-clearing output. The authors themselves state that v2 does not consistently reach workshop level or top-tier conference standards (PDF p. 13). Workshop acceptance is not publication, and this paper's accepted AI-generated manuscript was withdrawn (PDF pp. 9, 13).

The system's autonomy has material human boundaries: topic and prompt selection, initial idea selection, multiple-seed initiation, best-manuscript selection, manual dataset preparation for pest detection, compute/resource provision, and post-run validation (PDF pp. 10, 19, 58). The claim of autonomous execution therefore applies to the interior of a selected run.

The source does not isolate causal effects of agentic tree search, replication, or VLM feedback. It also does not validate the automated reviewer as calibrated or reliable. Persistent output errors show that executable code and automated review do not guarantee scientific soundness (PDF pp. 35-44, 46-57, 65-69).

Generalization is limited by the computational ML tasks, small synthetic or benchmark datasets, and the absence of physical or deployment evaluation. The pest study was not a real-world agricultural deployment; its environmental changes were simulated augmentations, and reviewers found the domain-adaptation and multi-dataset claims misleading (PDF pp. 58-69).

### Implications for SERVO

The following is an audit-level mapping, not terminology used by the source authors. A broad mapping of idea generation, execution, validation, memory, and policy is possible, but the mapping must preserve human gates and the distinction between implemented mechanisms and demonstrated effects.

| SERVO element | Source-grounded mapping | Boundary |
|---|---|---|
| `S` | Generated research ideas and experiment states (PDF pp. 4, 10, 21-23) | Human topic/idea gates define the initial reachable set. |
| `G` | LLM idea generation, literature search, code and hypothesis refinement (PDF pp. 4-7, 21-30) | Novelty reasoning is generated output, not independently certified novelty. |
| `E` | Python experiment generation and execution (PDF pp. 5-7, 23-30) | Computational only; manual data preparation remains possible. |
| `V` | Execution status, metrics, plots, LLM/VLM checks, and human reviews (PDF pp. 5-9, 41-69) | Automated validation is not shown to be calibrated or sufficient. |
| `M` | Checkpoints, stored metrics, error traces, code, plots, and replication aggregates (PDF pp. 5-7) | Complete seed-level auditability is not demonstrated in the report. |
| `pi` | Best-first node selection, debugging/refinement choices, stage transitions, and seed replication (PDF pp. 5-7) | Search policy is described, but its causal scientific benefit is not isolated. |

## Citation Assessments

There are no direct manuscript citation links for `ai_scientist_v2`. The source is included in the core-14 catalog as a system whose frozen supplementary description must be checked against its primary PDF. Consequently, there are no occurrence-level English or Korean claims to assess, no source-line sentence mapping, and no Korean translation parity pair for this artifact.

This does **not** mean that AI Scientist-v2 was absent from substantive analysis. The Nature 2026 citation audit covers the same system/method family through its explicitly identified template-free mode and the `AI-Scientist-v2` code-availability link. The correct distinction is: direct occurrence coverage for this Yamada 2025 PDF is zero, while system-method coverage across the manuscript's audited artifacts is non-zero. The two artifacts remain separate sources and must not be collapsed into one citation identity.

The catalog-only boundary is itself important: absence of manuscript citation links must not be reported as evidence that the manuscript accurately or inaccurately described v2. This report evaluates only the frozen system description and the source's own mechanisms, evidence, limitations, and context.

## Korean Parity

No Korean manuscript occurrence directly cites this Yamada 2025 catalog artifact. Therefore `KO_LINKS_COVERED: none` and Korean parity is not applicable for this artifact. The English side likewise has no direct occurrence; `EN_LINKS_COVERED: none`. This zero-occurrence result is compatible with substantive system-method coverage through the separately audited Nature 2026 template-free artifact.

## Frozen Supplementary Description Assessment

Frozen description:

> An LLM research pipeline for machine-learning experiments. From a broad topic prompt it generates many candidate ideas; a human selects a few (without editing them), then each run autonomously refines the hypothesis, writes and executes code, and produces a manuscript. An experiment-progress manager coordinates staged experimentation with agentic tree search and replication nodes reporting mean and standard deviation over seeds; a vision-language model gives figure-quality feedback during runs. Outputs were assessed by an automated reviewer and one cleared a workshop peer-review bar. Computational experiments only.

- **“An LLM research pipeline for machine-learning experiments” - `SUPPORTED`.** The PDF describes an end-to-end LLM-agent workflow for computational ML experiments and demonstrates arithmetic, calibration, and image-classification tasks (PDF pp. 1, 3-8, 31-69). The scope is not general-domain science or physical experimentation.
- **“From a broad topic prompt it generates many candidate ideas” - `SUPPORTED_WITH_QUALIFICATION`, minor.** The reported workshop run used a human-supplied theme, generated about twenty core-ML ideas, then used a human-modified applied prompt to generate about twenty more (PDF p. 10). “Many” is therefore documented in this bounded setup, not as an unlimited or fully autonomous topic-generation claim.
- **“a human selects a few (without editing them)” - `SUPPORTED_WITH_QUALIFICATION`, minor.** Humans selected three ideas without modifying them (PDF p. 10). The description omits the later human selection of the best complete manuscript from multiple seeds and the human code/scientific checks (PDF pp. 10, 19).
- **“then each run autonomously refines the hypothesis, writes and executes code, and produces a manuscript” - `SUPPORTED_WITH_QUALIFICATION`, minor.** Within a selected run, the source reports no human intervention or editing across hypothesis, code, execution, analysis, visualization, and writing (PDF pp. 9-10). This does not include topic selection, resource setup, seed selection, manual pest-dataset preparation, final output selection, or post-run review (PDF pp. 10, 19, 58).
- **“An experiment-progress manager coordinates staged experimentation with agentic tree search” - `SUPPORTED_WITH_QUALIFICATION`, minor.** The four stages and tree-search mechanism are explicitly implemented and described (PDF pp. 5-7). The source does not demonstrate that tree search itself improves scientific depth or quality over a controlled baseline.
- **“replication nodes reporting mean and standard deviation over seeds” - `SUPPORTED_WITH_QUALIFICATION`, minor.** Replication nodes use different seeds and aggregation nodes are designed to produce means and standard deviations (PDF pp. 5-7). A complete seed-level ledger for all submitted results is not provided, so this is a mechanism claim rather than universal output verification.
- **“a vision-language model gives figure-quality feedback during runs” - `SUPPORTED_WITH_QUALIFICATION`, minor.** VLM checks occur during experiment plotting and manuscript reflection (PDF pp. 7-8, 28-31). The PDF does not show a quality-gain ablation, and human review found residual figure/caption failures (PDF pp. 35-41, 46-57).
- **“Outputs were assessed by an automated reviewer” - `SUPPORTED_WITH_QUALIFICATION`, minor.** An LLM/VLM paper-review stage is present (PDF pp. 1-3, 7-8). Its reliability, calibration, and agreement with human reviewers are not established; documented quality judgments also came from human internal and workshop reviews (PDF pp. 9-13, 41-69).
- **“one cleared a workshop peer-review bar” - `SUPPORTED_WITH_QUALIFICATION`, minor.** One of three submissions scored 6, 6, and 7 and exceeded the stated workshop threshold (PDF pp. 8-10, 31). It was withdrawn before publication and did not enter the public record (PDF pp. 9, 13), so “cleared” must not be read as published or scientifically validated.
- **“Computational experiments only” - `SUPPORTED`.** The experiments are Python/ML runs on synthetic and image datasets. No wet-lab experiment or real-world deployment was conducted; the pest reviewers explicitly identify the absence of real-world deployment (PDF pp. 58-69).

**Frozen-description verdict:** `minor_revision`. The description's central mechanisms and computational scope are accurate. It should be revised to expose the second human output-selection gate, manual pest-data preparation, the non-validated status of automated review/VLM feedback, and the withdrawal/non-publication status of the workshop result.

Recommended corrected description:

> The AI Scientist-v2 is an LLM-agent pipeline for computational machine-learning research. Given a human-supplied topic or workshop prompt, it generates candidate ideas; in the reported ICBINB experiment, humans selected three unedited ideas from roughly forty candidates. Within each selected seed run, the system refined the hypothesis, generated and executed code, analyzed results, produced figures, and wrote a manuscript. A four-stage experiment manager coordinated parallel agentic tree search with debugging, hyperparameter, ablation, replication, and aggregation nodes; replication and aggregation were designed to report means and standard deviations across seeds. VLM and LLM review stages were present, but their quality-gain or reliability was not independently established. Humans selected the best completed manuscript, manually prepared the pest dataset, and performed post-run scientific and code review. Of three submissions to human ICBINB review, one exceeded the stated workshop threshold but was withdrawn before publication. All experiments were computational.

## Overall Verdict

**`minor_revision`** for the frozen supplementary description and **catalog-only source audit complete**. The PDF is an exact, usable primary source for the existence and architecture of AI Scientist-v2. Its evidence supports the described computational pipeline and workshop experiment, but stronger claims about fully autonomous end-to-end research, tree-search benefit, VLM quality improvement, automated-review reliability, or publication are not warranted.

## Completion Checklist

- [x] PDF identity, authors, arXiv identifier, version, path, hash, and page count verified.
- [x] Pages 1-69 read sequentially, including appendices, prompts, generated papers, references, internal reviews, code reviews, and workshop reviews.
- [x] Relevant figures and tables rendered and visually inspected.
- [x] Catalog-only publication-artifact scope confirmed; no direct EN or KO manuscript citation links exist.
- [x] Cross-artifact crosswalk recorded: Nature 2026 template-free mode and `AI-Scientist-v2` repository link provide separate system-method coverage without merging publication identities.
- [x] Every frozen-description clause assessed with exact enclosing-PDF pages.
- [x] Human gates separated from within-run autonomy.
- [x] Implemented mechanisms separated from unmeasured effects.
- [x] Workshop threshold crossing separated from publication and scientific validation.
- [x] No external model/API call used and no other source PDF opened.
- [x] Terminal markers present and consistent with the audit scope.

AUDIT_COMPLETE: yes
PAGES_COVERED: 1-69
EN_LINKS_COVERED: none
KO_LINKS_COVERED: none
SYSTEM_DESCRIPTION_ASSESSED: yes
VERDICT: minor_revision
