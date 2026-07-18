# lu2024aiscientist: Source Identity and Bilingual Mapping

## Lane Scope

- Active source only: `lu2024aiscientist`.
- Assigned checks: BibTeX/PDF identity and version; complete EN/KO occurrence mapping; omitted, added, and meaning-shifted claims; attribution and citation-placement parity.
- Manifest inventory: 5 EN links and 3 KO links.
- Source-support judgments below are based only on the supplied PDF. Manuscript comparisons use `main.tex`, `main_ko.tex`, and the manifest solely to identify and compare the claims being audited.

## Source Identity

- Citation key: `lu2024aiscientist`.
- BibTeX type: `@article`.
- BibTeX title: *The AI Scientist: Towards fully automated open-ended scientific discovery*.
- BibTeX authors: Chris Lu; Cong Lu; Robert Tjarko Lange; Jakob Foerster; Jeff Clune; David Ha.
- BibTeX venue/identifier: `arXiv preprint arXiv:2408.06292` (2024).
- Absolute PDF path: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/The AI Scientist_ Towards Fully Automated Open-Ended Scientific Discovery.pdf`.
- SHA-256: `00fc4a18db7b314b5def5d9236c6af6cb9325605dcb4827cc82b0f8a462356fe`.
- `pdfinfo` page count: 186.
- PDF-internal title: *The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery* (PDF p. 1).
- PDF-internal authors: Chris Lu, Cong Lu, Robert Tjarko Lange, Jakob Foerster, Jeff Clune, and David Ha, in the same order as the BibTeX entry (PDF p. 1).
- PDF-internal stable identifier/version: `arXiv:2408.06292v3 [cs.AI] 1 Sep 2024` (PDF p. 1).
- DOI: none stated in the PDF or BibTeX entry.
- Version status: `exact`. The title, complete author list and order, year, and arXiv work identifier all match. The PDF is specifically arXiv v3; the BibTeX entry identifies the same arXiv work without pinning a version. That omission is not an identity mismatch.
- Manifest consistency: the manifest's path, SHA-256, 186-page count, and `exact` status match the locally verified file.

## PDF Evidence Reviewed

- PDF p. 1: title, authors, arXiv v3 imprint, abstract, claimed independent research process, full-paper writing, simulated review, and repeatable open-ended archive.
- PDF pp. 2-3: end-to-end paper-generation pipeline; ideation, literature search, experiments, manuscript writing, reviewing, archive feedback; Figure 1; the `65% vs. 66% balanced accuracy` contribution statement.
- PDF pp. 4-7: separate idea scores; paper-review fields; 500-paper ICLR 2022 evaluation; calibrated thresholding; five reflections, five ensembled reviews, one-shot prompting, and meta-review; reviewer limitations visible in Table 1 and its discussion.
- PDF pp. 17-21: relationship to prior systems, the paper's own single-system synthesis claim, reviewer/data limitations, implementation and hallucination failures, safety limits, and the discussion of end-to-end automation.
- PDF pp. 30-35: appendix contents and the actual idea-generation and paper-review prompts, including separate 1-10 `Interestingness`, `Feasibility`, and `Novelty` fields.
- Visual inspection was performed on PDF pp. 1, 3, 6, 18, 31, and 32 to confirm the title/version layout, Figure 1, Table 1, limitations list, and score-field separation.

## Link Mapping Summary

| EN link | KO link(s) | Cardinality | Korean parity | Mapping result |
|---|---|---|---|---|
| `EN-C001:lu2024aiscientist` | `KO-C001:lu2024aiscientist` | one-to-one | `equivalent` | The citation-bearing proliferation/shared-vocabulary sentence is substantively equivalent. |
| `EN-C003:lu2024aiscientist` | `KO-C022:lu2024aiscientist` (partial relocation) | many-to-one from EN; one-to-many from KO | `meaning_shifted` | The explicit EN description of The AI Scientist as a closed-loop manuscript-writing pipeline is deleted from the KO introduction. A weaker end-to-end/closed-loop classification reappears through the broad KO core-systems citation and table. |
| `EN-C013:lu2024aiscientist` | `KO-C008:lu2024aiscientist` | one-to-one | `equivalent` | Same multi-source attribution and same individual-characterization/no-common-framework synthesis. |
| `EN-C027:lu2024aiscientist` | `KO-C022:lu2024aiscientist` (partial relocation) | many-to-one from EN; one-to-many from KO | `meaning_shifted` | KO retains categorical table cells (`LLM self-score`, closed loop `Yes (greedy)`, and biased `V_s`) but omits the five-review configuration, 0.65/0.66 metric, priority wording, and sentence-level source placement. |
| `EN-C047:lu2024aiscientist` | none | one-to-zero | `omitted` | The source-specific `1-10 score` example is absent from KO. |
| no EN link at the corresponding core-systems setup sentence | `KO-C022:lu2024aiscientist` | zero-to-one at the sentence level | `added` | KO adds a four-source citation to its core-systems setup paragraph; the corresponding EN paragraph at line 142 has no citation. The same KO link also serves as an omnibus relocation for portions of EN-C003 and EN-C027. |

All five EN IDs and all three KO IDs are accounted for. There is no unmapped manifest link.

## Citation Assessments

### EN-C001 / KO-C001

- Locations: EN line 69, Introduction; KO line 88, Introduction.
- Claim: AI Scientist systems that independently generate hypotheses, execute experiments, and synthesize knowledge have proliferated rapidly, while the field lacks a shared formal vocabulary.
- Role: `joint` background citation. Six sources share the citation command.
- PDF evidence: the abstract says The AI Scientist generates ideas, writes code, executes experiments, visualizes results, writes a full paper, and runs a simulated review, with repetition possible in an open-ended archive (PDF p. 1). The pipeline is expanded on PDF pp. 2-3.
- Verdict: `PARTIAL`; severity `minor`; `joint-only` for the trend claim.
- Reason: this source directly establishes one qualifying AI Scientist system and its broad autonomous workflow. One system paper does not independently establish rapid field-wide proliferation or the absence of a shared vocabulary. Those are manuscript-level syntheses requiring the full source set or explicit author framing.
- Correction: attribute only the example to this source, or frame the trend as the manuscript's synthesis: "Recent systems include end-to-end pipelines such as The AI Scientist...".
- Bilingual result: `equivalent`. Attribution and citation placement are the same for this citation-bearing sentence. The following EN sentence has a separate link, EN-C003, and is not part of this one-to-one pair.

### EN-C003

- Location: EN line 69, Introduction.
- Claim: The AI Scientist is a closed-loop manuscript-writing pipeline.
- Role: `direct`, in a two-source citation with the 2026 successor.
- PDF evidence: the paper calls the system a fully automated and scalable pipeline for end-to-end paper generation and lists ideation, literature search, experiment iterations, manuscript writing, and peer reviewing (PDF p. 2). It says the loop can run open-endedly "in principle" (PDF p. 2), and Figure 1 shows archive feedback returning to idea generation (PDF p. 3).
- Verdict: `SUPPORTED_WITH_QUALIFICATION`; severity `minor`.
- Reason: `manuscript-writing pipeline` and computational feedback closure are supported. The source qualifies repeated open-ended operation as possible "in principle" rather than reporting a validated indefinitely running discovery loop.
- Correction: "an end-to-end paper-generation pipeline that can, in principle, repeat through archive feedback."
- Bilingual result: `meaning_shifted`. KO deletes this sentence and its local citation from the introduction. Related categorical content is later compressed into the KO table under the broad `KO-C022` citation, but the manuscript-writing description and the source's "in principle" qualification disappear.

### EN-C013 / KO-C008

- Locations: EN line 90, Related Work; KO line 109, Related Work.
- Claim: prior work qualitatively characterizes individual systems but provides no shared framework for cross-system comparison.
- Role: `joint` background citation in a four-source command.
- PDF evidence: the source is a detailed characterization of one system and presents its own end-to-end pipeline (PDF pp. 1-7). Its related-work section describes its contribution as synthesizing prior strands into "a single autonomous open-ended system" rather than constructing a taxonomy for comparing several systems (PDF p. 17).
- Verdict: `PARTIAL`; severity `minor`.
- Reason: the source supports the "individual system characterization" half. It cannot establish the universal absence of a shared cross-system framework; absence cannot be inferred from this paper's silence, and the paper itself uses broad "first comprehensive framework" priority language for its own pipeline (PDF p. 1).
- Correction: "These works characterize individual systems; we use them as inputs to a new cross-system comparison framework." This makes the absence/comparison statement explicitly the present manuscript's synthesis.
- Bilingual result: `equivalent`. Wording, multi-source attribution, and citation position are materially the same.

### EN-C027

- Location: EN line 166, Analysis of Core AI Scientist Systems.
- Claim family: The AI Scientist adds a semantic validator through a five-review GPT-4o ensemble; reports balanced accuracy 0.65 versus human 0.66; thereby enables the first structurally closed loop; and operates on a biased, uncalibrated validator.
- Role: mixed `direct` quantitative evidence plus `interpretive` framework mapping and priority claim.
- PDF evidence:
  - Table 1 evaluates 500 ICLR 2022 papers and reports balanced accuracy `0.65 +/- 0.04` for calibrated GPT-4o (1-shot) at threshold 6 versus `0.66` for the human baseline (PDF p. 6).
  - The selected reviewer configuration uses five self-reflection rounds, five ensembled reviews, one example, and meta-aggregation (PDF pp. 6-7). The paper separately states that ensembling did not materially improve performance but could reduce variance (PDF p. 7).
  - The paper explicitly says decisions may be post-calibrated by thresholding and labels the relevant Table 1 block `Calibrated` (PDF p. 6).
  - The paper flags contamination risk, submission/camera-ready mismatch, no rebuttal, and no vision access (PDF p. 18), and reports inaccurate conclusions and occasional hallucinated results (PDF pp. 18-19).
  - The paper claims a first end-to-end fully automated framework, but repeated open-ended operation is qualified as possible "in principle" (PDF pp. 1-3).
- Verdict: `PARTIAL`; severity `major`.
- Reason: the architecture and 0.65/0.66 figures are supported under their actual 500-paper, thresholded evaluation condition. The source does not support calling the evaluated reviewer `uncalibrated`; it explicitly labels the reported thresholded result calibrated. The PDF supports substantial reliability threats, but those are not equivalent to demonstrating score calibration failure. The broad `first structurally closed loop` wording also converts an author priority claim and an in-principle loop into an unqualified comparative conclusion.
- Correction: "The system uses a GPT-4o reviewer with five generated reviews and meta-aggregation; after threshold calibration on 500 ICLR 2022 papers, the reported balanced accuracy is 0.65 +/- 0.04 versus 0.66 for the human baseline. The source also identifies contamination, data, modality, and hallucination threats, so this benchmark does not validate a trustworthy novelty gate."
- Bilingual result: `meaning_shifted`. No KO sentence preserves the quantitative claim or local citation. KO Table 1 cells at lines 207-210 retain only categorical interpretations under the earlier omnibus `KO-C022` citation. This weakens traceability and removes the PDF's evaluation conditions.

### EN-C047

- Location: EN line 215, The Lack of Validated Automated Novelty Gates.
- Claim: novelty, significance, and correctness are collapsed into one scalar, exemplified by The AI Scientist's 1-10 score.
- Role: `direct` example.
- PDF evidence: the actual idea-generation JSON contains three separate 1-10 fields: `Interestingness`, `Feasibility`, and `Novelty` (PDF pp. 31-32). The paper reviewer also emits separate `soundness`, `presentation`, `contribution`, `overall`, and `confidence` scores plus a decision (PDF p. 5). The related-work discussion says the reviewer judges novelty and interestingness (PDF p. 17), but the PDF never establishes that novelty, significance, and correctness are collapsed into a single 1-10 scalar.
- Verdict: `CONTRADICTED`; severity `major`.
- Reason: the cited implementation preserves multiple distinct score fields. Although it also emits an overall paper score, the PDF does not show that the overall score is the sole scalar replacing novelty, significance, and correctness.
- Correction: "The AI Scientist relies on LLM-generated scalar judgments, but it records separate 1-10 scores for interestingness, feasibility, and novelty and separate reviewer dimensions plus an overall score." A broader collapse claim needs a different source or direct evidence about how the final acceptance decision combines these dimensions.
- Bilingual result: `omitted`. KO contains no `lu2024aiscientist` link or source-specific 1-10 example corresponding to this sentence. Its later discussion of contamination-controlled novelty criteria is not a translation of the cited example.

### KO-C022

- Location: KO line 195, Analysis of Core AI Scientist Systems.
- Claim family: the framework is applied to four end-to-end systems; within this sample, closed-loop systems also have more complete validators, while generator, executor, and policy also advance. The citation also sits immediately before a table that classifies AI Scientist 2024 as `LLM self-score`, closed `Yes (greedy)`, greedy policy, and biased semantic validator.
- Role: `joint` and `interpretive`, in a four-source citation.
- PDF evidence: The AI Scientist is directly presented as an end-to-end system with ideation, experiment execution, paper writing, reviewing, and archive feedback (PDF pp. 1-3). The PDF supplies an automated semantic reviewer and its evaluation (PDF pp. 5-7), along with extensive reliability limits (PDF pp. 18-21).
- Verdict: `PARTIAL`; severity `minor` for this source's share of the joint claim.
- Reason: this PDF supports including The AI Scientist as one of the end-to-end systems and supports several raw features used in the table. It does not establish the four-system comparison, the SERVO `V`-completeness ordering, or the cross-system co-occurrence between loop closure and validator completeness. Those are the current manuscript's joint synthesis.
- Correction: keep the source citation for The AI Scientist's row-level facts, but label the comparative pattern explicitly as the present manuscript's coding/synthesis and cite the coding basis at the row or caption where feasible.
- Bilingual result: `added` at the paragraph level and `one-to-many` as a relocation. The corresponding EN setup paragraph at line 142 is uncited. At the same time, KO-C022 absorbs only reduced fragments of EN-C003 and EN-C027 into a broad paragraph/table citation, so it is not a faithful sentence-level counterpart to either EN link.

## Attribution and Placement Findings

1. `EN-C001`/`KO-C001` and `EN-C013`/`KO-C008` preserve source sets, attribution, and local placement.
2. EN gives The AI Scientist a direct citation immediately after the closed-loop pipeline label (`EN-C003`). KO removes that sentence and shifts weaker attribution to a broad citation before the core-systems table (`KO-C022`).
3. EN places the sole-source citation directly after the `0.65 vs. 0.66` metric (`EN-C027`), but the surrounding sentence also makes calibration and priority claims not fully established by that source. KO removes the metric and sentence-level citation, leaving only categorical table annotations under an omnibus citation.
4. `EN-C047` has no KO citation or source-specific claim. This omission avoids reproducing a source-contradicted example in KO but creates substantive bilingual divergence.
5. `KO-C022` is an added citation relative to the corresponding EN core-systems setup paragraph. Its scope is broader than any one cited source because it precedes both a cross-system inference and a multi-row interpretive table.

## Overall Verdict

- Identity/version: `exact`.
- Link accounting: complete, 5/5 EN and 3/3 KO.
- Bilingual parity: not equivalent overall. Two links are direct equivalents; one KO omnibus link consolidates and weakens portions of two EN links while adding paragraph-level citation placement; one EN source-specific claim is omitted entirely.
- Substantive citation status: `major_revision`. The reviewer metric is only partly and conditionally represented, while the `1-10 score` example is contradicted by the PDF's separate score fields.

## Completion Checklist

- [x] BibTeX identity checked against the PDF title page.
- [x] arXiv identifier and PDF version checked from the PDF itself.
- [x] Absolute path, SHA-256, and page count verified locally.
- [x] Every manifest EN and KO link ID mapped.
- [x] Omitted, added, and meaning-shifted claims identified.
- [x] Attribution and citation-placement differences checked.
- [x] Every source-support conclusion grounded in cited PDF pages.
- [x] Relevant figures, table, limitations, and prompt pages visually inspected.
- [x] Assigned file only created; no manuscript, bibliography, rubric, or manifest edits made by this lane.

EVIDENCE_COMPLETE: yes
