# `ai_scientist_v2` Architecture and Full-Text Evidence

## Scope and reading contract

- Active source: `ai_scientist_v2` only.
- PDF: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/The AI Scientist-v2 Workshop-Level Automated Scientific Discovery via Agentic Tree Search.pdf`.
- The local PDF was read sequentially from enclosing PDF page 1 through page 69, including the references, author contributions, supplementary hyperparameters, all prompts, all three generated manuscripts, internal scientific/code reviews, and workshop reviews.
- No API call, model call, web retrieval, or second source PDF was used for this lane.
- This file is evidence only. It does not infer a citation verdict for the manuscript because this system has no manuscript citation occurrence in the core manifest.

## Identity and document structure

- Title: *The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search*.
- Authors: Yutaro Yamada, Robert Tjarko Lange, Cong Lu, Shengran Hu, Chris Lu, Jakob Foerster, Jeff Clune, and David Ha.
- PDF identity: `arXiv:2504.08066v1 [cs.AI]`, 10 April 2025; the title page separately displays `2025-4-14`.
- Enclosing PDF length: 69 pages. The generated papers embedded in the supplement restart their own page numbers; all page references below mean the enclosing PDF page.
- The report is an arXiv preprint/technical report describing the system and an ICLR 2025 ICBINB workshop experiment. The threshold-clearing generated manuscript was withdrawn and did not become a workshop publication.

The document has four functional layers:

1. Pages 1-15: system claim, architecture, human evaluation, limitations, related work, and conclusion.
2. Pages 16-19: references and author contributions. The contributions are operationally important because they explicitly disclose human reading, code checking, validation, and submission selection.
3. Pages 20-30: supplementary hyperparameters and the complete prompts for idea generation, experimentation, plotting/aggregation, writing, reflection, VLM review, and duplicate checking.
4. Pages 31-69: Table 4 and three complete AI-generated workshop submissions, with internal scientific review, internal code review, and available external workshop reviews.

## End-to-end architecture reconstructed from the PDF

### Input, idea generation, and literature context

The pipeline begins from a human-supplied broad topic or workshop description. The idea-generation prompt asks the LLM to propose novel, feasible research proposals in a structured JSON format containing a name, title, hypothesis, related work, abstract, experiments, and risks. It requires at least one Semantic Scholar search before finalizing an idea (pp. 3-4, 21-23). Thus literature search is an in-loop novelty/context aid, not an independent novelty certification mechanism.

For the reported ICBINB run, the workshop theme was extracted from the official workshop website. The system generated roughly twenty core-ML ideas, then the authors modified the prompt toward applied domains and generated roughly twenty more. Humans selected three unedited ideas, two from the first batch and one from the second, for full execution (p. 10). This is a genuine human funding/prioritization gate before a run.

### Template-free experiment initialization

The stated v2 change from v1 is removal of a human-authored code template. The experiment prompt instead asks the LLM to write a working Python baseline from data preparation through training, evaluation, and visualization. The system therefore starts from an idea and prompt context, but it still depends on human topic definition, idea selection, compute provisioning, and any unavailable data preparation.

### Four-stage experiment-progress manager

The manager coordinates four stages (pp. 5-6):

1. Preliminary investigation: create and execute a minimal working prototype and establish feasibility/correctness.
2. Hyperparameter tuning: stabilize a baseline through parameters such as learning rate and epochs; the reported stopping criterion includes convergence and successful execution on at least two datasets.
3. Research-agenda execution: implement the central hypothesis and use the allocated budget; unusually short runs can trigger a request for greater complexity.
4. Ablation studies: test the importance of components or assumptions, again until the allocated budget is exhausted.

At the end of each stage the manager uses an LLM evaluator to select a best-performing node, records a checkpoint, and seeds the next stage. It also launches replications of selected experiments so aggregation can report means and standard deviations over different random seeds (pp. 5-7). The paper describes these mechanisms but does not provide a complete node/seed ledger for every submitted result.

### Agentic tree search and node lifecycle

Figure 2 (p. 6) and Section 3.2.2 define a node as an experiment script, high-level plan, error trace if present, runtime, metrics, LLM feedback, visualization script, figure paths, VLM feedback, and final buggy/non-buggy status. A node executes by generating a plan and Python code, running it immediately, saving metrics/losses to structured NumPy files, producing plots, and sending those plots to a VLM.

- Execution failure records the error and marks the node buggy.
- Successful execution still passes through plotting and VLM critique; issues such as missing labels, missing legends, or misleading visuals also mark the node buggy.
- Non-buggy nodes are refined; buggy nodes are debugged using the stored error.
- Several existing nodes are expanded in parallel. A predefined debug probability gives buggy nodes priority; otherwise a best-first choice among non-buggy nodes uses LLM judgments about performance metrics, training dynamics, and plot quality.
- Child nodes are executed concurrently, with a maximum debug depth and per-node runtime limit.
- Hyperparameter nodes avoid repeated configurations; ablation nodes avoid repeated conditions; replication nodes use different seeds; aggregation nodes only consolidate previous replication outputs and do not run a new experiment.

The tree is therefore an execution-and-selection scaffold around LLM-generated code. The document does not present a controlled comparison against linear search, a tree trace proving greater depth, or an ablation establishing that tree search itself caused better scientific results.

### Data loading and experiment artifacts

Section 3.3 prompts use of Hugging Face Hub and `datasets.load_dataset` for standard datasets, while acknowledging that this is ad hoc and not universal (p. 7). The experiment and plotting prompts require actual saved arrays and existing data rather than invented values. The pipeline stores scripts, summaries, figures, feedback, and checkpoints as node artifacts. The pest case is an explicit boundary: humans downloaded and reduced the Kaggle dataset before execution because the system could not autonomously obtain that real-world data (p. 58).

### VLM feedback loop

VLM feedback is inserted at two locations (pp. 7-8, 28-30):

1. During tree execution, the VLM critiques generated figures for labels, legends, clarity, and misleading presentation; a flagged result becomes buggy feedback for later debugging.
2. During manuscript reflection, screenshots of each figure, its caption, and the text mentioning `Figure X` are presented together. The VLM checks figure-caption-text alignment, visual clarity, and duplicate figures between the main paper and appendix.

This is a documented mechanism, not a demonstrated quality guarantee. The supplement still contains wrong captions, duplicated plots, unreadable figures, and missing or unexecuted results that human review identified (pp. 35-41, 46-57, 65-69). No VLM ablation or before/after quality metric is reported.

### Manuscript generation and review

The v2 writing path is single-pass manuscript generation followed by reasoning-model reflection rather than the incremental Aider loop described for v1 (pp. 3-4, 25-28). The write-up prompt is workshop-specific and uses target page length plus current compiled length. Reflection is asked to improve scientific clarity, formatting, figures, and compliance without human text editing within a selected run.

The pipeline includes an LLM paper-review stage and VLM figure review (Figure 1, pp. 3, 7-8). However, the report does not give automated-reviewer agreement, calibration, or an independent reliability analysis against workshop reviewers. Automated review is a pipeline component, not a certification gate.

## Human selection and autonomy boundary

The paper's strongest autonomy claim is local to a selected seed run. Within that run, hypothesis refinement, code generation, execution, analysis, visualization, and manuscript writing were performed without human content editing (pp. 9-10). The broader end-to-end process still contains these human actions:

1. Define or modify the high-level workshop/topic prompt.
2. Select three initial ideas from about forty candidates without editing their content.
3. Initiate multiple random-seed runs for each selected idea.
4. Inspect completed manuscripts and choose one best output per idea based on coherence and scientific quality.
5. Manually acquire and downsample the pest dataset.
6. Read generated papers, check implementations, and perform scientific and code review.
7. Select the submission and coordinate workshop/IRB/withdrawal procedures.

The author-contribution page (p. 19) confirms these were not merely hypothetical safeguards: authors read and validated many AI-generated papers, checked code, evaluated submissions, selected submissions, and led detailed analyses. “Fully autonomous” therefore describes content generation inside each selected run, not autonomous research prioritization, dataset acquisition, output selection, or external publication.

## Evaluation and evidence from all three generated papers

Table 4 (p. 31) lists three workshop submissions: one acceptance-worthy compositional-regularization paper and two rejected papers on label noise/calibration and pest detection. The report states that three AI-generated manuscripts were mixed into 43 ICBINB submissions, blind to which were AI-generated. One received 6, 6, and 7, averaging 6.33 and exceeding the stated workshop threshold; it would have been accepted after meta-review if human-generated. Under a prior agreement, accepted AI manuscripts were withdrawn, so this was peer-review evidence but not public publication.

### C.1, pp. 32-44: compositional regularization

The generated paper proposes a temporal-consistency regularizer for LSTM sequence models and tests synthetic arithmetic expression generalization. The AI team review finds the idea interesting and the negative result useful, but identifies unclear embedding-versus-hidden-state terminology, missing foundational citations, incorrect figure interpretation, narrow synthetic tasks, and a representative roughly 57% train/test overlap. Code review also questions an apparently perfect attention-model result as task-simplicity dependent. Workshop reviewers accepted the paper's negative-result contribution but requested stronger intuition, more architectures, and broader datasets. This appendix demonstrates executable end-to-end output while also showing that execution and review did not eliminate methodological errors.

### C.2, pp. 45-57: label noise and calibration

The second generated paper studies test accuracy and expected calibration error under label noise. Its internal review and code review document a serious claim-artifact mismatch: temperature scaling was implemented but not actually executed, reliability diagrams were absent, figures were duplicated or not aligned with the text, and some results were described without displayed evidence. External reviews recognize the topic but criticize limited analysis and presentation. This is direct counterevidence to any claim that the automated review loop reliably certifies figure/result fidelity.

### C.3, pp. 58-69: pest detection

The third generated paper addresses real-world pest detection with domain adaptation and multi-dataset ideas. The report discloses manual Kaggle data preparation and a one-tenth reduction before the run (p. 58). Internal code review finds that the successful selected path did not implement the claimed domain adaptation/multi-dataset mechanism; the intended path failed, while a code path that ran without errors was selected. External reviewers consequently treat the work as a computational preliminary study rather than evidence of real-world agricultural deployment. This bounds both the autonomy claim and the system's ability to recover scientifically from implementation failure.

## Limitations, context, and interpretive boundaries

The authors themselves state that only one of three submissions was accepted-worthy, that workshop acceptance is weaker than main-track acceptance, and that genuinely novel high-impact hypotheses, innovative methods, and deep domain justification remain difficult (pp. 13-14). They explicitly discuss citation inaccuracies, insufficient methodological rigor, responsible disclosure, IRB approval, reviewer opt-out, and withdrawal from the official record (pp. 9, 13).

The related-work section situates v2 among v1, AI-Researcher, Agent Laboratory, agentRxiv, CycleResearcher, self-driving-lab protocol systems, idea-generation studies, MLEBench/AIDE, METR, SciCode, BixBench, and AI Co-Scientist systems (pp. 14-15). This context supports a rapidly evolving computational-agent landscape, but the report's own evaluation remains three ML manuscripts in one workshop setting.

The defensible description is consequently: an LLM-agent computational-ML pipeline that, after human topic and idea selection, autonomously generates and executes code, performs staged tree-based experimentation with replication/aggregation, generates and reviews figures, and writes manuscripts. It demonstrated one acceptance-worthy result in a controlled workshop experiment, but the result was withdrawn; the report does not establish that tree search, VLM feedback, or automated reviewing independently improves scientific quality or guarantees correctness.

## Sequential full-text coverage log

| Enclosing pages | Material read and recovered |
|---|---|
| 1-2 | Title/identity, abstract, v1 comparison, contribution claims, Table 1, workshop score and withdrawal framing. |
| 3-4 | Figure 1, background, v1 limitations, scaffolding/tree-search context, generalized idea generation, Semantic Scholar use, template removal, section roadmap. |
| 5-7 | Experiment-progress manager, four stages and stopping criteria, node schema, execution/error/plot/VLM lifecycle, Figure 2, parallel selection/expansion, hyperparameter/ablation/replication/aggregation nodes, Hugging Face loading. |
| 7-8 | Two VLM insertion points, screenshot/caption/text checks, Figure 3, transition to human evaluation. |
| 8-10 | Three-submission protocol, 43-submission blind review, scores 6/6/7, withdrawal agreement, IRB/transparency, internal review, roughly forty ideas, human selection, multiple seeds, best-manuscript selection, within-run autonomy. |
| 10-13 | Generated compositional paper synopsis, author assessment, code/data-overlap concerns, reviewer excerpts and scores, limitations and ethical safeguards. |
| 14-15 | Related work, benchmark/context claims, conclusion and future-looking claims. |
| 16-18 | All references, including cited systems, benchmarks, scaffolding, and scientific-discovery context. |
| 19-20 | Author contributions and supplementary table of contents; human validation, code checks, selection, and review roles. |
| 21-23 | Hyperparameter tables; model assignments; node budgets; runtime; idea-generation and reflection prompts; required literature search and structured idea schema. |
| 24-27 | Experiment-generation, plotting/aggregation, write-up, and reflection prompts; requirements to use real saved data and obey page limits. |
| 28-30 | VLM review and image-review prompts; figure-caption-text alignment, clarity, duplication, and manuscript refinement checks. |
| 31 | Table 4 overview of three generated submissions and status/score summary. |
| 32-40 | Full compositional-regularization manuscript, figures, appendices, generated references, and its experimental claims/results. |
| 41-44 | AI Scientist Team scientific review and code review, including overlap, terminology, figure errors, and task-scope limitations. |
| 45-52 | Full label-noise/calibration manuscript, idea, methods, results, figures, supplement, and generated references. |
| 53-56 | Internal scientific/code reviews of label-noise paper, including unexecuted temperature scaling, missing/duplicated figures, and claim-result mismatch. |
| 57 | External workshop reviews of label-noise paper and their criticism of analysis/presentation. |
| 58-64 | Pest-detection idea, manual dataset acquisition/reduction disclosure, full generated manuscript, methods, experiments, figures, and references. |
| 65-67 | Internal scientific/code reviews of pest paper, including failed domain-adaptation path and selected runnable but narrower implementation. |
| 67-69 | Three external workshop reviews of pest paper and limits on real-world/deployment interpretation. |

## Evidence conclusion

The source supports the existence and broad architecture of The AI Scientist-v2, including template-free code generation, a four-stage experiment manager, parallel agentic tree search, replication/aggregation, VLM feedback, and manuscript generation/review. It also documents the necessary human gates and concrete failure modes in the generated outputs. It does not support treating the system as autonomous across topic selection, candidate funding, data acquisition, output selection, submission, or post-run validation; nor does it establish a causal quality advantage for tree search or VLM feedback.

SYSTEM_DESCRIPTION_ASSESSED: yes
EVIDENCE_COMPLETE: yes
