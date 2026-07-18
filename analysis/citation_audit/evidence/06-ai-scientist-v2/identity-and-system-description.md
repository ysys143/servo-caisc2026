# `ai_scientist_v2` Identity and Frozen System Description Audit

## Lane Scope

- Active source only: `ai_scientist_v2`.
- Assigned checks: local PDF identity and version, SHA-256, page count, sequential reading of all 69 PDF pages, visual inspection of the central workflow figures and tables, and clause-level assessment of the frozen supplementary description.
- Source PDF: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/The AI Scientist-v2 Workshop-Level Automated Scientific Discovery via Agentic Tree Search.pdf`.
- No other source PDF was opened. No external model or API was called.
- The core manifest assigns no manuscript citation key or manuscript occurrence to this catalog-only system; this lane therefore assesses the frozen system description against the local PDF itself.

## Source Identity

- PDF-internal title: *The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search* (PDF p. 1).
- PDF-internal authors: Yutaro Yamada, Robert Tjarko Lange, Cong Lu, Shengran Hu, Chris Lu, Jakob Foerster, Jeff Clune, and David Ha (PDF p. 1).
- Affiliations: Sakana AI, University of British Columbia, Vector Institute, FLAIR at the University of Oxford, and Canada CIFAR AI Chair (PDF p. 1).
- Document identifier and version: `arXiv:2504.08066v1 [cs.AI]`, dated 10 April 2025 in the arXiv margin stamp (PDF p. 1).
- The rendered title page separately shows `2025-4-14`, and `pdfinfo` reports a creation/modification timestamp of 14 April 2025. These are local document dates; the explicit arXiv version marker remains `v1`.
- Document status: an arXiv v1 preprint/technical report about The AI Scientist-v2 and a controlled ICLR 2025 ICBINB workshop-submission experiment. It is not itself a workshop proceedings paper. One generated manuscript is reproduced inside the report and was described as acceptance-worthy, but it was withdrawn before publication (PDF pp. 1-2, 8-10, 31-44).
- Absolute PDF path: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/The AI Scientist-v2 Workshop-Level Automated Scientific Discovery via Agentic Tree Search.pdf`.
- SHA-256: `53bafd3028e3f8829a3d85220e84dcf0d18934f9b75c092a60de303ff3644bd2`.
- `pdfinfo` page count: 69.
- PDF properties: unencrypted, A4 (`595.276 x 841.89` pt), PDF 1.5, 8,923,691 bytes. The metadata title and author fields are blank, so identity is taken from the rendered title page and arXiv margin stamp.
- Version status: `exact`. The path, SHA-256, 69-page count, title, authors, arXiv identifier, and `v1` marker agree with the frozen core manifest and the local file.

## Full-Text Coverage

- PDF pp. 1-2: title, arXiv identity, abstract, contributions, comparison with v1, and workshop-evaluation claims.
- PDF pp. 3-4: Figure 1, prior-system context, generalized idea generation, Semantic Scholar novelty search, and removal of the human-authored template dependency.
- PDF pp. 5-7: four experiment-manager stages, stopping criteria, stage checkpointing, replication, Figure 2, parallel agentic tree search, node types, execution/error handling, LLM node selection, and aggregation.
- PDF pp. 7-8: Hugging Face dataset loading, VLM checks during experiment execution and manuscript reflection, and Figure 3.
- PDF pp. 9-10: human-evaluation protocol, three workshop submissions, withdrawal agreement, internal human evaluation, two rounds of human selection, and the exact within-run autonomy claim.
- PDF pp. 11-15: content and human assessment of the acceptance-worthy generated paper, external reviewer excerpts, limitations, related work, and conclusion.
- PDF pp. 16-18: complete references.
- PDF p. 19: author contributions, including human reading, validation, code checking, and submission selection.
- PDF p. 20: supplementary table of contents.
- PDF pp. 21-30: model/tree-search hyperparameters and complete idea-generation, experiment, plotting, write-up, reflection, VLM review, and duplicate-check prompts.
- PDF p. 31: Table 4, listing one acceptance-worthy and two rejected workshop submissions.
- PDF pp. 32-40: the complete generated compositional-regularization manuscript, including annotations, figures, references, and supplement.
- PDF pp. 41-44: human AI Scientist Team scientific review and code review of that manuscript.
- PDF pp. 45-52: the complete generated label-noise manuscript, including its idea, annotations, figures, references, and supplement.
- PDF pp. 53-56: human team review and code review of the label-noise manuscript.
- PDF p. 57: external workshop reviews of the label-noise manuscript.
- PDF pp. 58-64: pest-detection idea, manual dataset preparation disclosure, and the complete generated pest-detection manuscript.
- PDF pp. 65-67: human team scientific review and code review of the pest-detection manuscript.
- PDF pp. 67-69: all three external workshop reviews of the pest-detection manuscript.
- Pages 1-69 were read in that order with page-bounded, layout-preserving extraction. Embedded generated manuscripts restart their own page numbering; every citation in this audit uses the enclosing 69-page PDF's page number.

## Visual Inspection

- PDF p. 1 was rendered at 180 dpi. It confirms the complete title, eight-author list, `arXiv:2504.08066v1 [cs.AI] 10 Apr 2025` stamp, and separate `2025-4-14` title-page date.
- PDF p. 2 was rendered at 150 dpi. Table 1 explicitly contrasts domain-general drafting, tree-based execution planning, parallel experiments, a VLM reviewer, and a human result labeled `Workshop Acceptance-Worthy`.
- PDF p. 3 was rendered at 150 dpi. Figure 1 shows idea generation and Semantic Scholar novelty checking, four tree-based experiment stages, plotting plus VLM feedback, manuscript generation, and final LLM paper reviewing.
- PDF p. 6 was rendered at 150 dpi. Figure 2 visually distinguishes buggy, non-buggy, hyperparameter, ablation, replication, aggregation, and best nodes across four stages. The figure is a workflow schematic, not an empirical comparison of search effectiveness.
- PDF p. 8 was rendered at 150 dpi. Figure 3 reproduces the acceptance-worthy generated paper and records scores 6, 7, and 6 before meta-review.
- PDF p. 21 was rendered at 150 dpi. Tables 2-3 show the model assignments and execution budget: Claude 3.5 Sonnet v2 for code generation; GPT-4o for feedback and summary agents; 21 Stage-1 nodes and 12 nodes for each later stage; one-hour maximum runtime per node.
- PDF p. 31 was rendered at 150 dpi. Table 4 confirms three submissions, one shown as accepted with score 6.33 and two rejected.
- PDF pp. 42, 55, and 66 were rendered at 150 dpi. These code-review pages visually confirm that human team members inspected generated code after the runs and found dataset overlap, an implemented-but-unused temperature-scaling method, and a failed domain-adaptation/multi-dataset path.

## Frozen Description

> An LLM research pipeline for machine-learning experiments. From a broad topic prompt it generates many candidate ideas; a human selects a few (without editing them), then each run autonomously refines the hypothesis, writes and executes code, and produces a manuscript. An experiment-progress manager coordinates staged experimentation with agentic tree search and replication nodes reporting mean and standard deviation over seeds; a vision-language model gives figure-quality feedback during runs. Outputs were assessed by an automated reviewer and one cleared a workshop peer-review bar. Computational experiments only.

## Clause-Level Assessment

| Frozen clause | Status | PDF evidence and assessment |
|---|---|---|
| "An LLM research pipeline for machine-learning experiments" | **Supported** | The report presents an end-to-end LLM-agent pipeline that formulates ML hypotheses, writes and runs Python experiments, aggregates results, writes manuscripts, and reviews them (PDF pp. 1, 3-8). The three demonstrated domains are compositional regularization, image-classifier calibration under label noise, and image classification for pest detection (PDF pp. 31-69). This is bounded computational ML research, not general-domain or physical science. |
| "From a broad topic prompt it generates many candidate ideas" | **Supported with exact scale and input boundary** | For the workshop experiment, humans supplied the ICBINB theme and the system generated about 20 core-ML ideas. Humans then modified the prompt toward applied real-world domains, yielding about 20 more ideas (PDF p. 10). The idea prompt requires at least one Semantic Scholar search and asks the agent to assess novelty and feasibility (PDF pp. 21-23). Thus `many` means roughly 40 in this reported experiment, under human-supplied and later human-modified topical prompts. |
| "a human selects a few (without editing them)" | **Supported, but incomplete as a map of human selection** | Humans selected three ideas from the roughly 40 AI-generated candidates, and the paper explicitly says they did not modify those ideas (PDF p. 10). However, humans also ran each selected idea with multiple seeds and then selected the single best complete manuscript for submission after inspecting coherence and scientific quality (PDF p. 10). Author contributions confirm that team members read and validated many generated papers, selected submissions, and checked code (PDF p. 19). The frozen clause accurately records the first gate but omits the second, output-level gate. |
| "then each run autonomously refines the hypothesis, writes and executes code, and produces a manuscript" | **Supported with setup qualifications** | The authors state that within any selected run, hypothesis refinement, code generation and execution, analysis, visualization, and writing occurred without human content editing (PDF pp. 9-10). Figure 1 and Sections 3.1-3.4 document those stages (PDF pp. 3-8). This autonomy begins after humans provide the theme, choose the idea, start multiple seeds, and provision resources. For the pest experiment, humans additionally downloaded a Kaggle dataset and reduced it to one tenth before the run because the system could not obtain the real-world dataset autonomously (PDF p. 58). |
| "An experiment-progress manager coordinates staged experimentation with agentic tree search" | **Supported as an implemented mechanism; comparative benefit not demonstrated here** | The manager coordinates preliminary investigation, hyperparameter tuning, research-agenda execution, and ablation stages with explicit stage criteria and LLM-selected checkpoints (PDF pp. 5-7; Figures 1-2 on PDF pp. 3, 6). Nodes are expanded in parallel, debugged or refined according to status, and scored by an LLM using metrics, dynamics, and plots (PDF p. 7). The PDF describes and diagrams the mechanism but provides no tree trace, ablation against linear search, or controlled result showing that tree search itself caused deeper or better science. |
| "replication nodes reporting mean and standard deviation over seeds" | **Supported as a mechanism, with limited output-level auditability** | The manager launches multiple replications of selected experiments at stage completion, and replication nodes use different random seeds; aggregation nodes combine them into figures showing means and standard deviations (PDF pp. 5-7). Generated figures include shaded summaries, and an author annotation says the shading should be identified as standard deviation across three or four independent runs (PDF p. 35). The PDF does not provide a complete node/seed ledger for every submitted result, so it establishes the design and examples rather than universal execution fidelity. |
| "a vision-language model gives figure-quality feedback during runs" | **Supported as a mechanism; quality improvement is not established** | During tree execution, a VLM critiques figures for labels, legends, and misleading presentation; flagged nodes become buggy. During manuscript reflection it checks figure-caption-text alignment, clarity, and duplication (PDF pp. 5, 7-8, 28-31). Yet the appended outputs still contain wrong captions, duplicated plots, unreadable figures, and missing results that later human reviewers identified (PDF pp. 35-41, 46-57). There is no VLM ablation or before/after metric demonstrating improved figure quality. |
| "Outputs were assessed by an automated reviewer" | **Supported with scope qualification** | Figure 1 includes a terminal `LLM Paper Reviewing` stage, Table 1 marks a VLM reviewer, and the text describes an iterative AI-reviewer component augmented with VLM feedback (PDF pp. 1-3, 7-8). However, this PDF does not report automated reviewer scores or agreement for the three submitted manuscripts, and it does not establish evaluator reliability. Separate human team scientific/code reviews and external human workshop reviews supplied the documented quality judgments (PDF pp. 8-13, 41-44, 53-57, 65-69). The automated review is a pipeline step, not an independent certification. |
| "one cleared a workshop peer-review bar" | **Supported if read as acceptance-worthy human review scores, not publication** | Three generated manuscripts entered blind ICBINB workshop review. One received 6, 6, and 7, averaging 6.33, above the stated acceptance threshold and around the top 45% of 43 submissions (PDF pp. 2, 8-9, 12, 31). The report alternates between `accepted` and the more precise statement that it would have been accepted after meta-review if human-generated. By prior agreement, any accepted AI paper was withdrawn; it did not appear in the public OpenReview forum or official record (PDF pp. 9, 13). `Cleared a peer-review bar` is defensible only with this withdrawal and non-publication qualification. |
| "Computational experiments only" | **Supported** | All reported experiments are Python/ML runs on synthetic arithmetic, standard image datasets, and a downloaded crop image dataset. There is no wet-lab, physical intervention, or real-world deployment. Workshop reviewers explicitly note that the pest system was not tested in a real-world agricultural deployment (PDF pp. 58-69). Human dataset preparation, idea/output selection, code checking, and peer review occurred around the computational runs but do not turn them into physical experiments. |

## Mechanisms Versus Demonstrated Effects

### Directly documented mechanisms

- Generalized LLM idea generation with Semantic Scholar search and structured novelty/feasibility reflection (PDF pp. 4, 21-23).
- Four-stage experiment management, parallel tree expansion, execution-based buggy/non-buggy status, LLM best-node selection, debugging, hyperparameter, ablation, replication, and aggregation nodes (PDF pp. 5-7).
- Python execution and structured `.npy` result storage, followed by plotting and VLM inspection (PDF pp. 5, 7, 23-25).
- Single-pass manuscript generation followed by reasoning-model and VLM reflection, plus an LLM paper-review stage (PDF pp. 3-4, 7-8, 25-31).
- Multiple seed runs for each selected idea and mean/standard-deviation aggregation (PDF pp. 5-7, 10).

### Effects not established by this PDF

- The claim that tree search produces deeper, more systematic, or scientifically better exploration than v1 is not supported by a controlled tree-versus-linear comparison.
- The claim that VLM feedback significantly improves visual quality is not supported by an ablation or measured before/after quality change. Human review found persistent figure and caption failures after that feedback stage.
- Automated paper review is not validated against the human workshop judgments in this report and should not be characterized as calibrated, reliable, or certifying.
- Workshop-level quality was not consistent: one of three submitted papers was acceptance-worthy, two were rejected, and the authors' internal review judged none to meet top-tier main-conference standards (PDF pp. 9, 13, 31, 53, 65).
- End-to-end autonomy does not cover topic definition, candidate selection, compute provisioning, every dataset acquisition step, final manuscript selection, submission, or post-run scientific/code validation.

## Human and External Boundaries

1. Humans supplied the workshop theme, then altered the prompt to solicit applied-domain ideas (PDF p. 10).
2. Humans selected three initial ideas without editing their content (PDF p. 10).
3. Humans initiated multiple seed runs for each idea and selected the best complete manuscript from those outputs (PDF p. 10).
4. Humans manually downloaded and downsampled the pest dataset before that system run (PDF p. 58).
5. Team members read generated papers, inspected code, re-ran selected checks, and documented scientific and implementation errors after generation (PDF pp. 19, 41-44, 53-56, 65-67).
6. External workshop reviewers evaluated the three submissions. One received acceptance-worthy scores; all AI-generated submissions were withdrawn under the prearranged protocol (PDF pp. 8-13, 31, 57, 67-69).

## Output Evidence and Failure Modes

- The acceptance-worthy compositional-regularization paper is genuine output evidence, but human code review found about 57% test/train overlap in a representative data-generation check, ambiguous embedding-versus-hidden-state terminology, incorrect figure interpretation, and limited task scope (PDF pp. 32-44).
- The rejected label-noise paper claimed temperature-scaling results even though the method was implemented but never executed. It also omitted reliability diagrams, duplicated figures, and described results not shown (PDF pp. 45-57). This is direct evidence that access to code/plans plus automated review did not ensure claim-result alignment.
- The rejected pest paper described domain adaptation and multi-dataset training although the successful selected implementation did not contain those mechanisms. The actual domain-adaptation path failed, and the pipeline selected code that ran without errors instead (PDF pp. 58-69).
- These appendices demonstrate that the pipeline produced executable research artifacts and complete manuscripts. They simultaneously bound any stronger inference that successful execution, VLM review, or LLM review guarantees scientific soundness.

## Recommended Corrected Description

The AI Scientist-v2 is an LLM-agent pipeline for computational machine-learning research. Given a human-supplied broad topic or workshop prompt, it generates candidate ideas with literature search; in the reported ICBINB experiment, humans selected three unedited ideas from roughly 40 candidates. Within each selected seed run, the system refined the hypothesis, generated and executed code, analyzed results, produced figures, and wrote a manuscript. A four-stage experiment manager coordinated parallel agentic tree search, including debugging, hyperparameter, ablation, replication, and aggregation nodes; replication and aggregation were designed to report means and standard deviations across seeds. VLM feedback checked figures during experimentation and manuscript reflection, and an LLM paper-review stage was present, but this report does not validate either automated reviewer as a reliable quality gate. Humans also selected the best completed manuscript from multiple runs, manually prepared the pest dataset, and performed post-run scientific and code review. Of three manuscripts submitted to human ICBINB review, one received scores of 6, 6, and 7 and exceeded the stated workshop threshold, but it was withdrawn and not published. All scientific experiments were computational; there was no wet-lab or real-world deployment.

## Overall Verdict

**`minor_revision`** for the frozen supplementary description.

The central scope and mechanisms are accurate: computational ML research, broad-prompt idea generation, an explicit human idea-selection gate, autonomous activity within a selected run, staged agentic tree search, replication/aggregation, VLM feedback, automated paper review, and one acceptance-worthy workshop result. Revision is still required to expose the second human selection gate over completed manuscripts, the manual pest-dataset preparation, the lack of demonstrated quality gains from tree search/VLM/automated review, and the fact that the threshold-clearing manuscript was withdrawn rather than published.

## Completion Checklist

- [x] PDF title, complete author list, arXiv identifier, subject class, and version checked against the rendered first page.
- [x] Absolute path, SHA-256, file properties, and 69-page count verified locally.
- [x] Version status assessed as `exact` against the frozen core manifest.
- [x] PDF pages 1-69 read in order, including references, author contributions, all prompts, all three generated manuscripts, internal reviews, code reviews, and workshop reviews.
- [x] Central workflow figures and Tables 1-4 rendered and visually inspected.
- [x] Human code-review figures on PDF pp. 42, 55, and 66 rendered and inspected.
- [x] Every clause of the frozen supplementary description assessed.
- [x] Implemented mechanisms separated from claimed or unmeasured effects.
- [x] Within-run autonomy separated from human prompting, idea selection, seed/run selection, dataset preparation, submission, and post-run checking.
- [x] Workshop threshold crossing separated from formal publication and public scientific record.
- [x] Only the assigned evidence file was created.

SYSTEM_DESCRIPTION_ASSESSED: yes
EVIDENCE_COMPLETE: yes
