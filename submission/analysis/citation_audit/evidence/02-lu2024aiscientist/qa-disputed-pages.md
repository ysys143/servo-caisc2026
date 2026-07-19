# Independent QA of disputed pages: `lu2024aiscientist`

## Source and method

- Source PDF: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/The AI Scientist_ Towards Fully Automated Open-Ended Scientific Discovery.pdf`
- SHA-256: `00fc4a18db7b314b5def5d9236c6af6cb9325605dcb4827cc82b0f8a462356fe`
- `pdfinfo` reports 186 A4 pages, an embedded text layer, and no encryption.
- Text check: independently extracted physical PDF pp. 1-7, 11-13, 31-37 with Poppler `pdftotext -f N -l N -layout`; a whole-PDF text search was used only to enumerate every occurrence of `calibrat*` and threshold wording.
- Visual check: independently rendered physical PDF pp. 3, 5-7, 11, 13, 31-32, and 37 at 170 dpi with `pdftoppm -png`, then inspected the rendered page images. Table grouping, footnote placement, score-field boundaries, figure arrows, and printed page numbers agree with the text extraction.
- Page references below are physical PDF pages, which match the printed page numbers on the inspected pages.

## 1. Reviewer balanced accuracy 0.65 versus human 0.66

**Direct observations**

- Table 1 is headed as an evaluation on 500 ICLR 2022 papers. Its best AI row is `GPT-4o (1-shot) @6`, under the `Calibrated` block, with balanced accuracy `0.65 +/- 0.04` (PDF p. 6).
- The human row is labeled `Human (NeurIPS)` and gives balanced accuracy `0.66` (PDF p. 6). Its footnote states, in a short source excerpt, `Numbers are calculated ... the NeurIPS consistency experiment` (PDF p. 6).
- The prose likewise says the 500-paper ground truth came from ICLR 2022 OpenReview, then describes the 73% human accuracy as a value reported in the NeurIPS 2021 consistency experiment (PDF p. 6).
- The prose prints `0.65% vs. 0.66%`, but the table and the contribution summary on PDF p. 3 show proportions/percentages corresponding to 0.65/0.66 or 65%/66%. The two extra percent signs on p. 6 are a source typo, not evidence for sub-one-percent performance.

**Verdict: SUPPORTED ONLY WITH MATERIAL QUALIFICATION.** The two balanced-accuracy values are present, but they are not a paired, same-sample human-versus-AI experiment. The AI estimate is from 500 ICLR 2022 papers and includes a `+/- 0.04` interval; the human value is imported from a separate NeurIPS consistency experiment. Writing only “0.65 vs. human 0.66” hides a consequential protocol difference.

## 2. Calibration and threshold

**Direct observations**

- The reviewer description says decisions may be `post-calibrated by thresholding` the reviewer score (PDF pp. 5-6).
- Table 1 visually separates `Uncalibrated` GPT-4o rows from `Calibrated` rows. The cited 0.65 result is specifically `GPT-4o (1-shot) @6` in the latter block (PDF p. 6).
- The prose identifies 6 as the decision threshold and calls it a NeurIPS `Weak Accept`; it says this is approximately the average score of accepted papers (PDF p. 6).
- A whole-PDF search found no probability-calibration curve, expected calibration error, novelty-calibration evaluation, or domain-shift calibration experiment. The paper's use of “calibrated” is limited to decision-score thresholding; PDF p. 7 similarly describes thresholding Sonnet scores at 8.

**Verdict: “UNCALIBRATED” IS CONTRADICTED FOR THE REPORTED 0.65 DECISION RULE; BROADER CALIBRATION IS UNTESTED.** The source explicitly calls the `@6` result calibrated after thresholding. It would also overstate the evidence to call the validator fully probabilistically calibrated or novelty-calibrated. The source-faithful description is “accept/reject decisions post-calibrated by a reviewer-score threshold of 6.”

## 3. Five-review ensemble

**Direct observations**

- The method text reports `5 rounds of self-reflection, 5 ensembled reviews`, one review example, followed by an Area-Chair-style meta-review (PDF p. 6).
- The final configuration is restated as GPT-4o with five self-reflection rounds, five reviews, meta-aggregation, and one few-shot example (PDF p. 7). Table 6 independently lists reviewer hyperparameters `Number of Reflections = 5`, `Number of Fewshot Examples = 1`, and `Number of Ensembled Reviews = 5` (PDF p. 37).
- Figure 2 and its caption state that five-review ensembling and meta-aggregation did not affect reviewer performance, though they may reduce variance (PDF p. 7).

**Verdict: CONFIGURATION SUPPORTED; PERFORMANCE ATTRIBUTION NOT SUPPORTED.** Calling the deployed reviewer a five-review GPT-4o ensemble with meta-aggregation is accurate. Claiming that ensembling caused the 0.65 result or improved mean accuracy is not: the paper's own ablation reports no performance gain from that component. The Table 1 row itself is labeled by model, shot count, and threshold, not by an isolated ensemble treatment.

## 4. Separate score dimensions versus one 1-10 scalar

**Direct observations**

- The idea-generation JSON asks for three distinct fields: `Interestingness`, `Feasibility`, and `Novelty`. Each is separately rated from 1 to 10 (PDF pp. 31-32).
- The automated paper reviewer separately emits soundness, presentation, contribution, overall, and confidence scores plus an accept/reject decision (PDF p. 5). The displayed generated review also separately records originality, quality, clarity, significance, soundness, presentation, contribution, overall, and confidence (PDF pp. 11-12).
- The final accept/reject operation can be thresholded on the reviewer score/Overall score at 6 (PDF pp. 5-6), but this decision rule does not erase the separately recorded dimensions.

**Verdict: THE “ONE 1-10 SCALAR” DESCRIPTION IS CONTRADICTED.** The PDF does not collapse novelty, significance, and correctness into one sole 1-10 field. It uses three separate 1-10 idea ratings and a multi-field paper review that also has an Overall score. A narrower criticism that final acceptance is thresholded on Overall is supported; presenting that as the construction of all underlying judgments is not.

## 5. Whether cross-generation archive feedback was executed

**Direct observations**

- The abstract and introduction qualify repetition as possible `in principle` and describe completed ideas and reviewer feedback entering an archive for future generations (PDF pp. 1-3). Figure 1 draws a dotted return path from paper review to idea generation and says review can be feedback to future generations (PDF p. 3).
- The idea-generation mechanism does execute archive-conditioned idea iteration, and the within-project experiment stage replans after intermediate results (PDF pp. 4, 7-8). These are real loops, but neither proves that a completed paper's review was consumed by a later paper-generation cycle.
- In the aggregate experiment, the authors explicitly report a departure from the formal design: they generated ideas `without waiting for paper evaluations` to be appended to the archive so that generation could be parallelized (PDF p. 13).

**Verdict: THE PROPOSED OUTER LOOP WAS NOT EXECUTED IN THE REPORTED AGGREGATE EVALUATION.** The PDF demonstrates archive-conditioned idea generation and within-project experiment feedback. It does not demonstrate the disputed completed-paper-review-to-next-generation feedback loop; PDF p. 13 says that dependency was deliberately bypassed. Therefore “architecturally proposed/in-principle cross-generation feedback” is supported, while “experimentally exercised cross-generation review feedback” is not.

## QA conclusion

The disputed-page recheck independently confirms the need for `major_revision`: the five-review configuration is real, but the human comparison needs its separate-protocol caveat; the cited 0.65 rule is threshold-calibrated in the source's terminology; the one-scalar characterization conflicts with explicit multi-field scoring; and the inter-paper archive loop was proposed but not exercised in the reported aggregate runs.

EVIDENCE_COMPLETE: yes
