# `robin` Full-Text Audit

## Source Identity

- **Citation key:** `ghareeb2026robin`. `submission/references.bib` lists *A multi-agent system for automating scientific discovery*, Nature 2026, DOI `10.1038/s41586-026-10652-y`, with note `arXiv:2505.13400`.
- **PDF title:** *Robin: A Multi-Agent System for Automating Scientific Discovery*.
- **Authors:** Ali Essam Ghareeb, Benjamin Chang, Ludovico Mitchener, Angela Yiu, Caralyn J. Szostkiewicz, Jon M. Laurent, Muhammed T. Razzak, Andrew D. White, Michaela M. Hinks, and Samuel G. Rodriques.
- **Identifier/version:** `arXiv:2505.13400v1`, 19 May 2025; version status `exact` for the audited local PDF.
- **Absolute PDF path:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/Robin - A Multi-Agent System for Automating Scientific Discovery.pdf`.
- **SHA-256:** `336d4e3f9065f42918cec8053e020d12c8d8c8031eb4c180764a349d1efa1794`.
- **PDF extent:** 30 pages, matching the frozen manifest.
- **Scope restriction:** Only the three specified Robin evidence files and repository-local citation-manifest context were used. No API/model call was made and no other PDF was opened.

## Full-Text Coverage

Pages **1-30** were read sequentially. Coverage includes abstract, introduction, system and dAMD results (pp. 1-7), implementation and wet-lab/data-analysis methods (pp. 8-11), references (pp. 12-15), prompts (pp. 16-23), supplementary judge and analysis figures (pp. 24-28), and additional disease candidate lists (pp. 29-30). Relevant architecture and result pages, including pp. 1, 3-7, 25, 28, and 30, were visually checked. Coverage is complete.

## Problem and Context

Robin addresses the delay between dispersed biomedical knowledge and testable therapeutic hypotheses, with particular motivation from drug repurposing. It positions prior systems as automating narrower portions of discovery and proposes one continuous workflow covering literature-grounded hypothesis generation, experimental strategy generation, data analysis, and hypothesis refinement (pp. 1-2).

The demonstrated domain is dry age-related macular degeneration (dAMD). Given a disease name, Robin proposes mechanisms, assays, and drug candidates; researchers select and execute physical experiments, then upload data for analysis (pp. 2-4). The source uses both broad intellectual-automation language and the more precise descriptions **semi-autonomous** and **lab-in-the-loop**.

## Structure and Argument

The paper introduces the motivation and dAMD workflow, describes the Crow/Falcon/Finch agents and LLM ranking, reports the phagocytosis and RNA-seq loop, and then discusses implementation, limitations, and supplementary prompts/results. The argument establishes a researcher-mediated iterative system and a testable in-vitro candidate-discovery result. It does not establish autonomous wet-lab execution, clinical efficacy, or external peer-reviewed replication.

## Methods and Evidence

Robin uses Crow for concise literature search and Falcon for deep literature search and candidate evaluation. It identifies 10 disease mechanisms and assay proposals, ranks them with an LLM judge, generates 30 candidate therapies, and ranks candidate reports through pairwise comparisons/tournament logic (pp. 3-4, 8). Finch runs analysis code in an Aviary-controlled Jupyter/Docker environment; up to 10 trajectories can be combined into a consensus (pp. 5, 8).

The dAMD demonstration used ARPE-19 cells, a 96-well phagocytosis assay, pHrodo beads, flow cytometry, and RNA sequencing (pp. 5, 9-11). Researchers performed the experiments, substituted pHrodo beads for the proposed fluorescent outer-segment substrate, supplied data, and performed RNA-seq demultiplexing/alignment. Finch analyzed flow cytometry and differential expression; a human independently analyzed flow cytometry with an additional no-bead background gate (p. 10). Domain experts also materially shaped prompts and calibrated the ranking judge (p. 7-8).

For SERVO, this supports a bounded mapping: `S` is literature, disease mechanisms, assays, and candidate reports; `G` is Robin's hypothesis/assay/candidate generation and LLM ranking; `E` is researcher-executed wet-lab work; `V` is Finch analysis plus human comparison and experimental judgment; `M` is the iterative data-to-hypothesis feedback. This interpretation must retain that the source is lab-in-the-loop and that Finch does not cover the entire experimental or RNA-seq pipeline.

## Findings

- Robin selected an RPE phagocytosis assay after reviewing 151 papers and proposing 10 mechanisms/assays (p. 5).
- The first screen identified ROCK-inhibitor-related activity and led to a follow-up RNA-seq experiment (pp. 5-6).
- The paper reports **3-fold ABCA1 upregulation**, adjusted `p = 2.13 x 10^-83`, in the stated comparison (p. 6).
- In a later candidate round, Finch reported ripasudil at **7.5-fold over DMSO**, while human analysis showed **1.75-fold**; the authors call for more doses and longer incubation before a definitive comparison (pp. 6-7).
- The LLM judge averaged **7.25/10** top-10 overlap with domain experts and repeated pairwise selections were **88%** for the judge versus **61%** for human experts (p. 8; Supplementary Fig. S11, p. 25).
- Eight RNA-seq trajectories contributed to the reported consensus example (p. 6).

These results support a researcher-mediated, in-vitro dAMD hypothesis and associated cell-assay/RNA-seq signals. They do not establish treatment efficacy in animals or humans.

## Limitations

The authors state that Robin generates experimental outlines but not precise executable protocols, and that Finch depends heavily on domain-expert prompt engineering (p. 7). Gating and RNA-seq filtering choices can change conclusions, and agent stochasticity can produce run variation; trajectory consensus mitigates but does not remove that uncertainty (p. 5).

The model is ARPE-19 and the substrate was changed to pHrodo beads for availability, limiting equivalence to native human RPE physiology. The ripasudil comparison is preliminary and lacks the additional dose/incubation conditions the authors say are needed. The PDF reports no animal efficacy, pharmacokinetic, toxicity, or clinical study, and its internal judge/expert comparison is not peer review of the biological finding.

### Human wet-lab and peer-review boundary

Researchers performed the phagocytosis and RNA-seq experiments, uploaded the data, made the substrate substitution, and handled RNA-seq demultiplexing/alignment. Finch's autonomy is limited to specified analysis stages and was independently checked for flow cytometry. The PDF does not document a peer-review procedure or venue decision. “Full manuscript was system-generated” is also broader than the source's explicit claim that Robin produced the main-text hypotheses, experimental plans, data analyses, and data figures; human formatting, procedures, alignment, analysis checks, prompts, and review/support remain part of the record.

## Citation Assessments

### Catalog-only status and direct occurrences

The manifest gives Robin `manuscript_link_ids: []`. Searches of the English and Korean manuscript surfaces found no `ghareeb2026robin`, Robin, or Korean-name occurrence. Therefore there are no direct citation claims, source lines, roles, or occurrence-level entailment verdicts to assess. The source is catalog-only in both languages.

### Frozen supplementary description clause-by-clause assessment

Frozen text:

> A system for biomedical therapeutic discovery (dry age-related macular degeneration). Cooperating agents perform literature search and deep evaluation, rank candidates via an LLM tournament, and design assays. Physical experiments (phagocytosis assays, RNA-seq sequencing and alignment) are performed by humans, while a bioinformatics agent autonomously analyzes flow-cytometry and differential-expression data and meta-analyzes multiple trajectories. Measured outcomes (e.g., phagocytosis improvement, gene upregulation with reported p-values) feed the next round; the full manuscript was system-generated and underwent peer review.

- **“A system for biomedical therapeutic discovery (dry age-related macular degeneration).”** `SUPPORTED_WITH_QUALIFICATION`, severity `minor`: the PDF demonstrates a dAMD therapeutic case study, not biomedical therapeutic discovery generally (pp. 1-7).
- **“Cooperating agents perform literature search and deep evaluation”** `SUPPORTED`, severity `none`: Crow and Falcon provide the concise/deep search and candidate evaluation roles (pp. 3-4).
- **“rank candidates via an LLM tournament”** `SUPPORTED`, severity `none`: pairwise LLM comparisons and BTL/tournament ranking are described (pp. 4, 8). This is surrogate ranking, not biological validation.
- **“and design assays.”** `SUPPORTED_WITH_QUALIFICATION`, severity `minor`: Robin proposes literature-grounded models and assays, but the paper says it does not yet produce precise executable protocols (pp. 3-4, 7).
- **“Physical experiments ... are performed by humans”** `SUPPORTED`, severity `none`: researchers performed the phagocytosis and RNA-seq work and human handling included alignment (pp. 5, 10).
- **“a bioinformatics agent autonomously analyzes ... data”** `SUPPORTED_WITH_QUALIFICATION`, severity `major`: Finch performs the stated flow-cytometry and differential-expression stages, but not autonomous acquisition, complete RNA-seq processing, or analysis independent of expert prompts/human comparison (pp. 7, 10).
- **“and meta-analyzes multiple trajectories.”** `SUPPORTED_WITH_QUALIFICATION`, severity `minor`: the capability and eight-trajectory RNA-seq consensus are reported (pp. 5-6), but this should not imply universal validation of every analysis.
- **“Measured outcomes ... feed the next round”** `SUPPORTED_WITH_QUALIFICATION`, severity `minor`: the demonstrated Y-27632 -> RNA-seq -> candidate iteration supports this for the reported dAMD loop, mediated by uploaded data and human experiments (pp. 5-7).
- **“the full manuscript was system-generated”** `PARTIAL`, severity `major`: the source supports system production of specified main-text scientific content, not an unqualified full-manuscript claim; human procedures, formatting, alignment, checks, and review/support remain documented (pp. 1, 5-11).
- **“and underwent peer review.”** `NOT_ASSESSABLE`, severity `major`: the PDF itself does not document peer review or a venue decision. This clause requires an external record or removal from a PDF-only description.

**Frozen-description verdict:** `minor_revision`. The architecture and demonstrated loop are substantially faithful, but the description must narrow “full manuscript,” bound Finch's autonomy, and treat peer review as externally sourced or omit it.

## Korean Parity

`EN_LINKS_COVERED: none` and `KO_LINKS_COVERED: none`; both language surfaces omit a direct Robin citation and the manifest has no linked occurrence. Parity is therefore **`omitted` / catalog-only**, not `equivalent` or `meaning_shifted`. No English-to-Korean claim mapping exists to evaluate. Any future Korean description should preserve the dAMD case-study scope, human wet-lab execution, partial Finch pipeline, and unverified peer-review clause.

## Overall Verdict

**`minor_revision`.** The source identity is exact and the 30-page audit is complete. The frozen description accurately captures the main architecture and demonstrated feedback loop, but it overstates manuscript-wide system generation, leaves Finch's autonomy too broad, and asserts peer review not established by the audited PDF. There is no direct English or Korean manuscript citation to invalidate; both are catalog-only.

## Completion Checklist

- [x] Citation key, bibliography metadata, title, authors, identifier, version, absolute PDF path, SHA-256, and page count recorded.
- [x] Pages 1-30 covered in order, including references, methods, prompts, and supplementary figures.
- [x] Research problem, context, prior-work relationship, structure, methods, findings, limitations, and SERVO implications assessed.
- [x] Frozen supplementary description assessed clause by clause with evidence, verdict, severity, and correction implications.
- [x] English direct occurrence inventory completed: none; Korean direct occurrence inventory completed: none.
- [x] Korean parity classified as `omitted` / catalog-only.
- [x] Human wet-lab, partial bioinformatics, human-expert, and peer-review boundaries stated.
- [x] Quantitative values, denominators/conditions where available, and scope limitations recorded.
- [x] No API/model call made and no other paper PDF opened.
- [x] System description assessed against the full source.

AUDIT_COMPLETE: yes
PAGES_COVERED: 1-30
EN_LINKS_COVERED: none
KO_LINKS_COVERED: none
SYSTEM_DESCRIPTION_ASSESSED: yes
VERDICT: minor_revision
