# Claims and English/Korean Parity Evidence: `lu2026aiscientist`

## Scope and source control

- Active source: `ai_scientist_2026` / `lu2026aiscientist` only.
- PDF: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/Towards end-to-end automation of AI research.pdf`
- PDF SHA-256: `a75e0d93447f400179136bf18d909df29e0c8ccaeba076a1dfb1beeef0e0e10d`
- Identity: Chris Lu et al., *Towards end-to-end automation of AI research*, Nature 651 (2026), DOI `10.1038/s41586-026-10265-5`.
- Version result: `exact`. The PDF title, authors, journal, year, and DOI match `submission/references.bib` and the frozen core-14 manifest.
- Coverage: all PDF pages 1-9 were read in order with layout-preserving extraction. No other source PDF was opened.
- Visual checks: PDF pages 2-5 were rendered at 180 dpi. Fig. 1, Table 1, Fig. 2, and Fig. 3 were inspected rather than inferred from extracted text.

## Full-text traversal and exact-page rechecks

| PDF page | Material checked |
|---|---|
| 1 | Abstract, motivation, claimed end-to-end scope, computational ML domain, and external-review setup |
| 2 | Fig. 1 workflow, idea archive, novelty checking, stage-to-stage feedback, manuscript generation, and terminal automated review |
| 3 | Table 1 reviewer metrics, contamination split, five-review ensemble, manual filtering, and ICLR workshop review outcome |
| 4 | Fig. 2 and limitations, including acceptance-rate context, failure modes, and computational-only experiments |
| 5 | Fig. 3 four-stage agentic tree, best-node progression, and compute scaling |
| 6 | References and publication context |
| 7 | Methods for template-based and template-free systems, experiment journal, idea archive, and stage transitions |
| 8 | Tree-node selection, replication and aggregation nodes, VLM checks, and Automated Reviewer definition |
| 9 | Five-review meta-review, reviewer validation caveat, ethics protocol, withdrawal, data, and code availability |

Before fixing the verdicts below, the relevant conclusions were re-opened on exact PDF pages 1, 2, 3, 4, 5, 7, 8, and 9. The rendered pages establish that Fig. 1 places `Paper AI review` at the end of the depicted write-up path, Table 1 separates pre-cutoff and post-cutoff metrics, Fig. 2 concerns external workshop review, and Fig. 3 concerns experiment-tree search.

## Occurrence audits

### `EN-C001:lu2026aiscientist`

- Manuscript location: English line 69, Introduction.
- Claim: AI Scientist systems independently generate hypotheses, execute experiments, and synthesize knowledge; such systems have proliferated rapidly; the field lacks a shared formal vocabulary.
- Citation role: `joint` / background.
- Joint-only scope: `yes`. This source can establish one system instance, not field-wide proliferation or absence of a shared vocabulary.
- Exact evidence: PDF page 1 says the system creates ideas, writes code, runs and analyses experiments, writes a manuscript, and reviews it. The same page says full-lifecycle automation had remained out of reach until this system, while recent progress had automated individual components.
- Entailment: `PARTIAL`.
- Severity: `minor`.
- Reasoning: the source supports inclusion of The AI Scientist as an end-to-end example. It does not independently establish rapid proliferation of full AI Scientist systems, and it does not survey terminology sufficiently to establish the field-wide vocabulary-absence claim. Its own historical framing distinguishes proliferating component tools from the previously missing full pipeline.
- Attribution: proliferation and vocabulary absence must remain the citing manuscript's multi-source synthesis, not a finding attributed to Lu et al.
- Proposed correction: distinguish growth in AI research components and systems from the narrower claim that many complete end-to-end systems have proliferated, or cite a dedicated field survey for the latter and for terminology fragmentation.
- Korean parity: `equivalent` to `KO-C001` for the sentence actually carrying this grouped citation.

### `EN-C003:lu2026aiscientist`

- Manuscript location: English line 69, Introduction.
- Claim: The AI Scientist is a closed-loop manuscript-writing pipeline.
- Citation role: `example` with an interpretive system label.
- Joint-only scope: `no` for the Nature 2026 system itself; the co-cited 2024 system must be assessed separately.
- Exact evidence: PDF page 1 calls it an end-to-end pipeline spanning ideation through peer review. PDF page 2 and rendered Fig. 1 show iterative idea archiving, experiment results informing future planning, and best checkpoints seeding later stages. PDF pages 5, 7, and 8 show staged tree search and feedback. PDF page 2 places automated paper review after manuscript generation.
- Entailment: `SUPPORTED_WITH_QUALIFICATION`.
- Severity: `minor`.
- Reasoning: the overall research pipeline contains computational feedback loops and writes complete manuscripts. However, the source does not show the final Automated Reviewer decision feeding back into manuscript revision or experiment search; Fig. 1 depicts it as terminal. Thus `closed-loop` is sound for iterative ideation/experimentation, but should not imply reviewer-gated manuscript rewriting.
- Attribution: `closed-loop` is the citing manuscript's faithful taxonomy, not terminology used as a formal claim by Lu et al.
- Proposed correction: use `an end-to-end manuscript-writing pipeline with iterative idea and experiment search` if the intended loop boundary includes the final reviewer.
- Korean parity: `omitted`. The Korean Introduction retains the grouped proliferation sentence but omits the English sentence that identifies The AI Scientist as a closed-loop manuscript-writing pipeline.

### `EN-C013:lu2026aiscientist`

- Manuscript location: English line 90, Related Work.
- Claim: prior works characterize individual systems but offer no shared framework for cross-system comparison.
- Citation role: `joint` / background.
- Joint-only scope: `yes` for the cross-literature conclusion.
- Exact evidence: the full PDF is organized around one system and its two modes, with workflow, experiments, reviewer benchmarking, human evaluation, limitations, and methods. It does not define a taxonomy for comparing multiple AI Scientist systems.
- Entailment: `SUPPORTED_WITH_QUALIFICATION`.
- Severity: `minor`.
- Reasoning: the absence of a cross-system framework is a fair characterization of this paper. Calling its characterization merely `qualitative` understates substantial quantitative content, including Table 1 reviewer metrics and Fig. 3 compute scaling, although the paper also contains extensive qualitative system description.
- Attribution: the absence of a shared framework across the entire literature is the citing manuscript's synthesis; silence in one paper cannot prove a universal absence claim.
- Proposed correction: say `provides system-specific qualitative and quantitative characterization but no shared cross-system comparison framework`.
- Korean parity: `equivalent` to `KO-C008`; both versions have the same scope and the same `qualitative` understatement.

### `EN-C028:lu2026aiscientist`

- Manuscript location: English line 166, Analysis of Core AI Scientist Systems.
- Claim bundle: the Nature system stacks replication-based empirical validation, an automated reviewer with balanced accuracy 0.69, and actual ICLR workshop peer review; it therefore has the most validator layers in the class, while its biased, uncalibrated automated reviewer is the internal acceptance gate.
- Citation role: `direct` for the method and number, plus `interpretive` for the SERVO layer and gate mapping.
- Joint-only scope: `yes` for `most layers in the class` and for any cross-system validator ranking; `no` for the source-local method and metric.
- Entailment: `PARTIAL`.
- Severity: `major`.
- Clause-level evidence and verdicts:

| Clause | Exact source evidence | Verdict |
|---|---|---|
| Replication nodes rerun experiments and report mean and s.d. | PDF page 8 states that replication nodes use different random seeds and aggregation nodes produce figures showing mean and s.d. | `SUPPORTED` |
| Automated Reviewer balanced accuracy is 0.69 | Rendered Table 1 on PDF page 3 reports `0.69 +/- 0.04` only for papers from 2017-2024, before the model knowledge cutoff. The post-cutoff 2025 value is `0.66 +/- 0.03`. PDF page 9 repeats 69% versus human 66% but warns that the ICLR and NeurIPS paper pools differ, so the comparison is not exact. | `SUPPORTED_WITH_QUALIFICATION` |
| Generated papers received actual ICLR-workshop peer review | PDF page 3 reports three selected submissions to the ICLR 2025 ICBINB workshop, manual filtering at each stage, and one paper that organizers said would likely have been accepted; PDF pages 4 and 9 state that all were withdrawn under the protocol. | `SUPPORTED_WITH_QUALIFICATION` |
| External peer review is a stacked internal `V_h` system layer or decisive gate | Fig. 1 on PDF page 2 depicts Automated Reviewer output at the end of the write-up path. The external workshop review is presented on PDF pages 3-4 as a separate human-evaluation experiment, not as feedback controlling idea generation, tree expansion, manuscript revision, or an internal acceptance decision. | `UNSUPPORTED` |
| The Automated Reviewer is the system's internal acceptance gate | PDF pages 2 and 8-9 show that it emits accept/reject reviews and is used to evaluate papers and configurations. Stage progression is instead controlled by idea filtering, stage-specific LLM evaluators, best-first node selection, and fixed budgets on PDF pages 2, 5, 7, and 8. No reviewed page shows its decision gating continued search or system acceptance. | `UNSUPPORTED` |
| The reviewer is biased and uncalibrated | Table 1 on PDF page 3 reports FPR `0.45 +/- 0.10` pre-cutoff and `0.52 +/- 0.10` post-cutoff versus human FPR `0.17`, which supports concern about lenient false acceptance. The paper performs classification/agreement evaluation, not a calibration analysis, and does not label the reviewer biased or uncalibrated. | `PARTIAL` for bias concern; `UNSUPPORTED` for calibration status |
| This system has the most validator layers in the class | A single-system paper cannot establish a cross-system superlative. | `NOT_ASSESSABLE` from this source alone |

- Reasoning: the citation directly supports replication/aggregation nodes and the conditioned 0.69 value. It also supports that external reviewers evaluated three selected outputs. It does not support converting that external study into an operational human validator inside the system, and it does not establish that the Automated Reviewer gates the loop. `Uncalibrated` is not interchangeable with high FPR or imperfect balanced accuracy.
- Attribution: `V_e`, `V_s`, `V_h`, `internal gate`, `biased`, `uncalibrated`, and `most layers` are SERVO interpretations. They must be marked as the citing authors' coding and defended independently rather than written as if Lu et al. reported them.
- Proposed correction: `The Nature system adds replication and aggregation nodes (mean and s.d. across seeds) and a five-review meta-reviewer. Table 1 reports balanced accuracy 0.69 +/- 0.04 pre-cutoff and 0.66 +/- 0.03 post-cutoff. In a separate external evaluation, three manually selected papers entered ICLR-workshop review and one would likely have been accepted, but all were withdrawn. The source does not show either the Automated Reviewer or workshop review acting as an internal gate, and it does not report calibration.`
- Korean parity: `omitted` for the detailed source-specific claim. `KO-C022` reuses this key for a broader cross-system synthesis, but does not translate the replication, reviewer metric, workshop condition, layer superlative, or gate/calibration assertions.

### `KO-C001:lu2026aiscientist`

- Manuscript location: Korean line 88, Introduction.
- Claim: AI Scientist systems independently generate hypotheses, execute experiments, and synthesize knowledge; they have increased rapidly; the field lacks shared formal vocabulary.
- Citation role: `joint` / background.
- Joint-only scope: `yes`.
- Exact evidence: PDF page 1 supports this paper as one end-to-end system but says that the full research-life-cycle system had previously remained out of reach, while individual components had expanded.
- Entailment: `PARTIAL`.
- Severity: `minor`.
- Reasoning: identical to `EN-C001`; this paper is a valid instance but cannot independently establish the field-wide trend or absence claim.
- Attribution: preserve the claim as a multi-source author synthesis.
- Proposed correction: distinguish the expansion of component agents from proliferation of complete AI Scientist systems, and add a field-level source for the vocabulary claim.
- Korean parity: `equivalent` to `EN-C001`.

### `KO-C008:lu2026aiscientist`

- Manuscript location: Korean line 109, Related Work.
- Claim: prior works give qualitative descriptions of individual systems but no common cross-system framework.
- Citation role: `joint` / background.
- Joint-only scope: `yes`.
- Exact evidence: the full PDF characterizes and evaluates one pipeline and does not propose a cross-system taxonomy; Table 1 and Figs. 1-3 also make the characterization substantially quantitative.
- Entailment: `SUPPORTED_WITH_QUALIFICATION`.
- Severity: `minor`.
- Reasoning: the no-cross-system-framework characterization is fair for this source, but `qualitative` understates the paper's quantitative evaluation.
- Attribution: the literature-wide absence remains the citing authors' synthesis.
- Proposed correction: replace `qualitative characterization` with `system-specific qualitative and quantitative characterization`.
- Korean parity: `equivalent` to `EN-C013`.

### `KO-C022:lu2026aiscientist`

- Manuscript location: Korean line 195, Core AI Scientist System Analysis.
- Claim: SERVO is applied to four end-to-end systems; within the small sample, closed-loop systems also have more complete validators, while `G`, `E`, and `pi` advance too.
- Citation role: `joint` / interpretive.
- Joint-only scope: `yes`. The association is a cross-system coding result and cannot follow from this PDF alone.
- Exact evidence: PDF pages 1-2 support classifying this system as end to end. PDF pages 5 and 7-8 support advances in tree-search policy, code execution, replication, aggregation, and automated review. They do not define SERVO completeness or test the manuscript's cross-system association. External workshop review is an evaluation experiment, not a demonstrated in-loop human gate.
- Entailment: `PARTIAL`.
- Severity: `minor` for this broad occurrence, with the operational-gate problem escalated under `EN-C028`.
- Reasoning: the source supplies one appropriate system datapoint, but neither the four-system membership claim nor the co-occurrence between closure and validator completeness is independently entailed. Those require joint reconciliation of all four sources and the manuscript's coding rules.
- Attribution: label the relationship explicitly as the citing manuscript's small-sample interpretation.
- Proposed correction: retain the small-sample caveat and state that source papers establish system features while the closure/completeness association is derived from SERVO coding; do not count external workshop review as an internal gate without a separate operational criterion.
- Korean parity: `meaning_shifted`. Its closest English text is the uncited broad synthesis at English line 142, whereas the only English `lu2026aiscientist` occurrence in the core analysis (`EN-C028`) is a detailed source-specific method/metric/gate claim. The citation has therefore moved to a materially different claim in Korean.

## Parity matrix

| English occurrence | Korean occurrence | Parity | Material consequence |
|---|---|---|---|
| `EN-C001` | `KO-C001` | `equivalent` | Same grouped background limitations apply. |
| `EN-C003` | none | `omitted` | Korean text lacks the closed-loop manuscript-pipeline example. |
| `EN-C013` | `KO-C008` | `equivalent` | Same quantitative-understatement qualification applies. |
| `EN-C028` | no equivalent; key appears in `KO-C022` | `omitted` / `meaning_shifted` | Korean omits all source-specific validator facts and moves the key to a broad cross-system synthesis. |

## Lane conclusion

- All 7 manifest links were independently audited: `EN-C001`, `EN-C003`, `EN-C013`, `EN-C028`, `KO-C001`, `KO-C008`, and `KO-C022`.
- Overall lane verdict: `major_revision`.
- Major issue: `EN-C028` conflates source-reported evaluation components with operational validator gates and states calibration status without a calibration analysis.
- Minor issues: grouped field-level claims are joint-only, `qualitative` understates the paper's evidence, 0.69 lacks its pre-cutoff condition, and the Korean version omits or relocates two English claims.

EVIDENCE_COMPLETE: yes
