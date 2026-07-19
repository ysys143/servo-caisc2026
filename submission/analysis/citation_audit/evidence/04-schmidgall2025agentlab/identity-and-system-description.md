# `agent_laboratory` Identity and Frozen System Description Audit

## Lane Scope

- Active source only: `agent_laboratory` / `schmidgall2025agentlab`.
- Assigned checks: PDF/BibTeX identity and version, SHA-256, page count, sequential reading of all 84 PDF pages, visual inspection of relevant figures and tables, and clause-level assessment of the frozen supplementary description.
- Source PDF: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/Agent Laboratory - Using LLM Agents as Research Assistants.pdf`.
- No other source PDF was opened. No external model or API was called.

## Source Identity

- Citation key: `schmidgall2025agentlab`.
- BibTeX type: `@article`.
- BibTeX title: *Agent Laboratory: Using LLM agents as research assistants*.
- BibTeX authors: Samuel Schmidgall; Yusheng Su; Ze Wang; Ximeng Sun; Jialian Wu; Xiaodong Yu; Jiang Liu; Michael Moor; Zicheng Liu; Emad Barsoum.
- BibTeX publication: *arXiv preprint arXiv:2501.04227* (2025).
- PDF-internal title: *Agent Laboratory: Using LLM Agents as Research Assistants* (PDF p. 1).
- PDF-internal authors: Samuel Schmidgall, Yusheng Su, Ze Wang, Ximeng Sun, Jialian Wu, Xiaodong Yu, Jiang Liu, Michael Moor, Zicheng Liu, and Emad Barsoum, in the same order as the BibTeX record (PDF p. 1).
- PDF-internal stable identifier and version: `arXiv:2501.04227v2 [cs.HC]`, dated 17 June 2025; the rendered title page is dated 18 June 2025 (PDF p. 1).
- DOI: none stated in the BibTeX record or local PDF.
- Absolute PDF path: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/Agent Laboratory - Using LLM Agents as Research Assistants.pdf`.
- SHA-256: `67b9543ae1d8e3ad86a65e2a436ddbd12700d7c8f4a66c5b4c2a6fccc1674d75`.
- `pdfinfo` page count: 84.
- PDF metadata title and authors match the PDF title page. The file is an unencrypted, 84-page arXiv-generated PDF.
- Version status: `exact`. The title, complete author list and order, arXiv identifier, and year match the BibTeX record. The BibTeX entry does not pin an arXiv revision, while the local file identifies itself as v2. The path, hash, page count, and `exact` status match both audit manifests.

## Full-Text and Visual Coverage

- PDF pp. 1-4: title page, abstract, introduction, contributions, background, related work, and the human-assistance motivation.
- PDF pp. 5-10: three-stage workflow; literature review; planning; data preparation; iterative `mle-solver`; result interpretation; `paper-solver`; NeurIPS-style review; report refinement; autonomous and co-pilot modes.
- PDF pp. 10-18: autonomous-mode study design and human sample; human and automated reviewer results; co-pilot studies; cost, runtime, reliability, and MLE-Bench evaluation.
- PDF pp. 19-22: workflow limitations, self-evaluation, hallucination, failure modes, ethics, discussion, intended assistant scope, and conclusion.
- PDF pp. 22-30: complete reference list.
- PDF p. 31: hyperparameters and hardware, including one reviewer during paper writing and three reviewers during report refinement.
- PDF pp. 32-40: base/context prompts, phase prompts, commands, and role descriptions for the PhD, ML engineer, postdoc, and professor agents.
- PDF pp. 41-45: `mle-solver` tools, professor reward-model prompt, code repair, execution/reflection, and code-generation prompts.
- PDF pp. 45-56: `paper-solver` tools and prompts, section-specific writing guidance, and the complete NeurIPS-style automated reviewer form, including Originality and Accept/Reject fields.
- PDF pp. 57-64: complete autonomous-mode human-evaluation survey.
- PDF pp. 65-74: complete preselected-topic co-pilot survey.
- PDF pp. 75-84: complete custom-topic co-pilot survey.
- Pages 1-84 were read in order with page-bounded, layout-preserving extraction. PDF pp. 1, 5, 7, 8, 13, and 31 were rendered at 150 dpi and visually inspected. The renders confirm the required human idea/notes input and full workflow (Fig. 1), optional human checkpoints and automated reward/reviewer components (Fig. 2), iterative code scoring (Fig. 3), report review (Fig. 4), the `6.1` versus `3.8` reviewer comparison (Fig. 6), and reviewer-count hyperparameters (Table 1).

## Frozen Description

> A human-directed assistant: a person supplies the research idea and ongoing direction, and LLM agents carry out literature review, an iterative code-writing-and-execution loop for experiments, and writing. The only automated quality check is an LLM reviewer applying conference guidelines, which was documented to over-estimate quality by about +2.3 points relative to human graduate-student reviewers. There is no autonomous certification of novelty.

## Clause-Level Assessment

| Frozen clause | Status | PDF evidence and assessment |
|---|---|---|
| "A human-directed assistant" | **Supported with qualification** | The stated purpose is to assist human scientists in executing their own ideas, and the discussion calls the system a co-pilot and human-centered workflow (PDF pp. 2, 21-22). However, the implementation also has an autonomous mode in which the initial idea is the only human input (PDF p. 10). The phrase is accurate as product intent, but not as a claim that every run is continuously human-directed. |
| "a person supplies the research idea" | **Supported** | The abstract, Fig. 1, introduction, and mode definition all make a human-provided research idea the initial input (PDF pp. 1-2, 10). Agent Laboratory deliberately does not originate the top-level research question in the evaluated workflow. |
| "and ongoing direction" | **Supported only for co-pilot mode; contradicted if presented as required in all modes** | In co-pilot mode, a human checkpoint follows each subtask and the user can proceed or repeat the subtask with high-level notes (PDF p. 10; survey instructions on PDF pp. 65-84). In autonomous mode, there is no human involvement after the initial research idea and phases advance sequentially (PDF pp. 10-11). The description must mark ongoing direction as optional and mode-specific. |
| "LLM agents carry out literature review" | **Supported** | The PhD agent iteratively queries arXiv, reads abstracts and selected full texts, judges relevance, and curates a review for later stages (PDF pp. 5-6, 34, 36-37). The 84-page appendix includes the exact search, full-text, and add-paper commands. |
| "an iterative code-writing-and-execution loop for experiments" | **Supported with qualification** | `mle-solver` repeatedly edits or replaces code, compiles and repairs it, executes it, scores successful programs, reflects on errors/results, and maintains top programs (PDF pp. 6-7, 31, 41-45; Fig. 3). The default research-code score is an LLM professor reward model assessing alignment among the plan, code, and output; the separate MLE-Bench evaluation substitutes a dev-set metric (PDF pp. 6-7, 18, 42). This is genuine code/result iteration, but its default score is subjective rather than an independently calibrated empirical validator. |
| "and writing" | **Supported with an important output boundary** | `paper-solver` creates a LaTeX scaffold, writes eight sections, searches arXiv, edits and compiles the report, and uses review feedback during refinement (PDF pp. 8-10, 45-56; Fig. 4). The authors explicitly say the output is a research report that helps a human understand and scale up the work, not a replacement for human academic paper writing (PDF pp. 8, 19; human-evaluation instructions on PDF pp. 57, 65, 76). |
| "The only automated quality check is an LLM reviewer applying conference guidelines" | **Contradicted because `only` is false; reviewer role itself is supported** | The paper reviewer does simulate NeurIPS review and returns originality, quality, clarity, significance, soundness, presentation, contribution, overall score, confidence, and Accept/Reject (PDF pp. 9-10, 50-56). Report refinement uses three reviewer agents, after which the PhD agent may finalize or revisit planning, experimentation, interpretation, or writing (PDF p. 10; Table 1 on PDF p. 31). But the workflow also has Python and LaTeX compilation checks, automated code repair, an LLM professor scoring experiment code/output from 0 to 1, self-reflection, and top-program/top-paper selection (PDF pp. 6-8, 31, 41-47). The conference reviewer is therefore not the only automated quality-control signal, and none of these checks independently verifies scientific truth. |
| "[the reviewer] was documented to over-estimate quality by about +2.3 points relative to human graduate-student reviewers" | **Supported with exact provenance and scope** | Fifteen autonomous-mode papers were generated from five fixed questions across three model backends. Ten volunteer PhD students each reviewed three randomly assigned papers (PDF pp. 10-12). Across that generated-paper set, the automated reviewers' mean NeurIPS Overall score was `6.1/10`, while the human reviewers' mean was `3.8/10`, a `+2.3` automated-minus-human difference (PDF pp. 12-14; Fig. 6 on PDF p. 13). The discrepancy appears across all listed criteria and all three backends, but `+2.3` specifically denotes the mean **Overall** score on this autonomous-output sample, not a calibrated error on arbitrary papers, a novelty score, or a universal reviewer bias. The source itself concludes that automated scores do not predict human scores and calls for human evaluation alongside them (PDF pp. 14, 21). |
| "There is no autonomous certification of novelty" | **Supported with qualification; too absolute if read as no automated novelty assessment** | No dedicated novelty-search gate, contamination-controlled test, expert-calibrated novelty classifier, or independent novelty certificate appears anywhere in the 84 pages. Humans provide the research question, while the literature agent retrieves relevant work (PDF pp. 1-2, 5-6, 10). However, the automated conference reviewer explicitly assigns an `Originality` score from 1 to 4, evaluates novelty in its rubric, and emits Accept/Reject; those reviews can drive further refinement or finalization (PDF pp. 9-10, 50-56). Thus the source supports saying there is no **independently validated or dedicated** autonomous novelty-certification mechanism, but not saying the system performs no automated novelty assessment at all. The authors identify subjective research-idea evaluation as an unreliable foundation of both solvers (PDF p. 19). |

## Requested Provenance Checks

### `+2.3`

- **Compared objects:** the same set of 15 reports produced in autonomous mode from five topics and three LLM backends (PDF pp. 10-12).
- **Automated side:** NeurIPS-style reviewer scores generated within Agent Laboratory; mean Overall `6.1/10` (PDF pp. 9-10, 12-14; Fig. 6 on PDF p. 13).
- **Human side:** ten volunteer PhD students, each assigned three reports; mean Overall `3.8/10` (PDF pp. 10-13).
- **Arithmetic and direction:** `6.1 - 3.8 = +2.3`; equivalently, human scores were 2.3 points lower. The paper repeatedly describes automated scores as over-estimates (PDF pp. 2, 12-14).
- **Boundary:** it is an average Overall-score gap on generated reports, not balanced accuracy, calibration error, causal proof that the reviewer causes poor research, or a direct novelty-rating gap.

### Human Input

- **Required in both modes:** a human provides the initial research idea; Fig. 1 also depicts user notes as input (PDF pp. 1-2).
- **Autonomous mode:** no further human involvement; each subtask advances automatically (PDF pp. 10-11).
- **Co-pilot mode:** a human reviews each subtask output and chooses proceed or repeat with high-level feedback (PDF p. 10). Survey participants chose either a fixed or custom topic and interacted through these checkpoints (PDF pp. 65-84).
- **Evaluation evidence:** co-pilot outputs improved external Overall score by `+0.58` over autonomous outputs but remained below the NeurIPS acceptance average; the authors also report difficulty steering agents to match exact researcher intent (PDF pp. 15-16).
- **Conclusion:** human provision of the idea is mandatory; ongoing direction is optional, not a universal architectural gate.

### Reviewer Role

- During `paper-solver`, one configured reviewer supplies reward-like report scores; during report refinement, three reviewer agents evaluate the draft (PDF pp. 9-10, 31).
- The reviewer uses an adapted NeurIPS form with multidimensional ratings, textual strengths/weaknesses, questions, limitations, ethical concerns, an Overall score, and Accept/Reject (PDF pp. 9, 50-56).
- A PhD agent consumes the reviews and decides whether to finalize or revisit earlier subtasks, so review can affect planning, experiments, interpretation, and writing within the same run (PDF p. 10).
- The reviewer does not execute or audit the experiment code, establish factual correctness, calibrate novelty, or supply external peer review. The authors empirically show poor agreement with human evaluations and warn that subjective LLM self-evaluation is unreliable (PDF pp. 12-14, 19, 21).

### Automated Novelty Certification

- The workflow has no separate novelty database filter, similarity threshold, external expert panel, or validated novelty benchmark.
- The literature-review agent's retrieval and curation provide context but do not issue a novelty decision (PDF pp. 5-6, 34, 36-37).
- The paper reviewer does assess `Originality` and considers whether tasks, methods, or combinations are novel before returning an overall decision (PDF pp. 9, 51-56).
- Accordingly, **no dedicated or trustworthy novelty certification** is supported, while **some automated novelty assessment** is plainly implemented. These statements must not be collapsed.

## Material Boundaries and Omissions

1. **Two human-interaction modes are collapsed.** The frozen description describes co-pilot behavior as if it were mandatory, but autonomous mode requires only the initial idea (PDF p. 10).
2. **The output is a foundation report.** The authors do not claim that `paper-solver` replaces final human paper writing, and they report hallucinated experimental details in generated reports (PDF pp. 8, 19-20).
3. **Automated quality control is plural.** Compiler checks, code repair, LLM experiment scoring, self-reflection, paper scoring, and three-agent report refinement coexist (PDF pp. 6-10, 31, 41-56).
4. **The `+2.3` metric has a narrow denominator.** It is the average Overall-score difference for 15 autonomous generated reports reviewed by ten volunteer PhD students, not a general calibration result (PDF pp. 10-14).
5. **The reviewer includes originality but is not a novelty certificate.** Its rubric produces an originality score and Accept/Reject, yet no source evidence establishes reliable novelty discrimination (PDF pp. 50-56; limitation on PDF p. 19).
6. **Scientific validity remains weak.** The paper documents hallucinated results, zero-accuracy runs, token-limit failures, host-system command execution, and manual removal of generated `exit()` calls (PDF pp. 19-20).

## Recommended Corrected Description

Agent Laboratory is an LLM-based machine-learning research assistant that requires a human-provided research idea. In autonomous mode it proceeds without further human input; in co-pilot mode a human may review every subtask and request a repeat with high-level feedback. Its agents perform literature review, planning and data preparation, iterative code generation/execution/scoring, result interpretation, and LaTeX research-report writing and refinement. Automated controls include compilation and repair, an LLM reward model for experiment code and output, and NeurIPS-style paper reviewers; the reviewers are not independent scientific validators. On 15 autonomous generated reports, their mean Overall score was `6.1/10`, compared with `3.8/10` from ten volunteer PhD-student reviewers, an automated-minus-human gap of `+2.3`. The system has no dedicated or independently validated novelty-certification gate, although its automated paper reviewer does score originality and issue Accept/Reject decisions. The generated report is intended as a foundation for subsequent human research and writing, not a trustworthy final paper by itself.

## Overall Verdict

**`major_revision`** for the frozen supplementary description.

The required human idea, agent-run literature review, iterative code execution, report writing, NeurIPS-style reviewer, and `+2.3` mean Overall-score gap are all directly source-grounded. Material revision is still required because ongoing human direction is optional and mode-specific, the reviewer is not the workflow's only automated quality-control mechanism, and the absolute novelty sentence obscures the automated originality assessment that does exist. The corrected description must also preserve the source's intended output boundary: a research foundation for human follow-up, not a validated final scientific result.

## Completion Checklist

- [x] BibTeX title, complete author list, year, and arXiv identifier checked against the PDF.
- [x] Absolute PDF path, SHA-256, and 84-page count verified locally.
- [x] Version status assessed as `exact`; local file identified as arXiv v2.
- [x] PDF pages 1-84 read in order, including references, prompts, survey instruments, and final page.
- [x] Figures 1-4 and 6 plus hyperparameter Table 1 inspected through rendered PDF pages.
- [x] Every clause of the frozen supplementary description assessed.
- [x] `+2.3` provenance, scale, comparison group, arithmetic, and scope documented.
- [x] Required versus optional human input separated by operating mode.
- [x] Reviewer role separated from compilers, code scoring, and scientific validation.
- [x] Absence of dedicated novelty certification separated from the implemented originality score.
- [x] Only the assigned evidence file was created.

SYSTEM_DESCRIPTION_ASSESSED: yes
EVIDENCE_COMPLETE: yes
