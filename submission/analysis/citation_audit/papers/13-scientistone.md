# `meng2026scientistone` Full-Text Audit

## Source Identity

- **Citation key:** `meng2026scientistone`. The bibliography record at `submission/references.bib:207-212` identifies *ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence*.
- **Authors:** Rui Meng, Bhavana Dalvi Mishra, Jiefeng Chen, Chun-Liang Li, Palash Goyal, Mihir Parmar, Yiwen Song, Yale Song, Rajarishi Sinha, Parthasarathy Ranganathan, Burak Gokturk, Jinsung Yoon, and Tomas Pfister.
- **Identifier/version:** arXiv `2605.26340v1`, 27 May 2026; version status `exact`.
- **Absolute PDF path:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/ScientistOne - Towards Human-Level Autonomous Research via Chain-of-Evidence.pdf`.
- **SHA-256:** `9d4fa9d1e9e6b1cdccfeff02fecbd28b5b961594952a1ac96e00ad135bed0a51`.
- **PDF extent:** 35 pages. The evidence records a match to `core14-manifest.json` for path, hash, page count, identity, and exact version.
- **Audit boundary:** Only the three specified ScientistOne evidence files and repository-local manifest/bibliography/manuscript inventory were used. No API or model call was made and no other PDF was opened.

## Full-Text Coverage

Pages **1-35** were read sequentially, including the abstract, introduction, related work, CoE architecture, experiments, tables, references, implementation appendices, search-scaling studies, audit details, failure cases, MLE-Bench/Parameter Golf material, and adaptation notes. The evidence records page-rendered and extracted-text inspection for relevant figures, tables, and appendices. Coverage is complete.

## Problem and Context

ScientistOne addresses evidence loss in autonomous research: a system may produce plausible code and manuscripts while fabricated references, unreproducible scores, unsupported conclusions, and method descriptions that diverge from code propagate through the pipeline (pp. 1-4). Its Chain-of-Evidence (CoE) principle requires claims to trace through recorded supporting claims and evidence to grounding sources (p. 4).

The paper situates this problem among autonomous research systems, literature grounding, discovery/search, paper writing, and verification/audit work (p. 3). Its distinct contribution is an end-to-end pipeline that carries evidence from literature investigation through solution discovery and paper writing, plus a separate post-hoc CoE Integrity Audit for completed paper/code/reference bundles (pp. 4-10). The latter is an audit of systems and artifacts, not evidence that every baseline system used the same native CoE pipeline.

The main evaluation is computational ADRS systems optimization. MLE-Bench and Parameter Golf provide additional computational tests. The paper explicitly warns that ADRS reduces systems research to single-metric solver optimization and does not establish broad systems-research quality, scientific correctness, novelty, or wet-lab capability (pp. 14-16).

## Structure and Argument

The paper first motivates evidence-chain failures and defines claim, evidence, and grounding-source relationships (pp. 1-4). It then presents three stages: Literature Grounding, Discovery, and Paper Writing & Verification (pp. 4-6). The CoE Integrity Audit and its four checks are introduced separately, followed by benchmark setup, baseline adaptation, results, and audit analysis (pp. 6-16).

Appendices provide the paper-quality corpus, implementation and file-backed artifact flow, citation-graph filtering, search-scaling and ablation studies, I1-I4 audit protocols and failure categories, and MLE-Bench/Parameter Golf adaptation details (pp. 19-35). The argument supports an evidence-oriented architecture and improved measured provenance under the stated protocols; it does not support universal citation entailment, general scientific validity, or human-free scientific acceptance.

## Methods and Evidence

ScientistOne's **Problem Investigator (PI)** starts from roughly 2-4 seed papers, traverses Semantic Scholar citations and references up to two hops, filters approximately 2,000-5,000 candidates by methodology relevance and problem alignment, and produces a grounded experiment brief. Specialist investigation and consolidation yield a smaller set of directions and a final brief with traceable references (pp. 5, 21-22).

The **Ideator** proposes approaches and ranks them on novelty and feasibility. The **Parallel Explore-Exploit (PEE)** orchestrator distributes proposals to isolated branches. Solver agents iterate evaluated versions, retain and expand branches, prune specification-violating candidates, select the best surviving solution, and run controlled ablations. Search variables include depth, width, retained branches, and evaluator budget (pp. 5, 20-24).

The **Paper Writer** uses evidence-tagged claims. Deterministic Ground checks score-file and artifact existence, required sections, baselines, and related constraints; Critic checks coherence, overclaiming, comparisons, fairness, and limitations; Resolve can revise before composition. The Claim Verifier checks numeric claims, bibliography resolution/abstract-level relevance, and methodological overlap with experimental logs, dropping unsupported or malformed claims (pp. 6, 21-22).

The post-hoc **CoE Integrity Audit** normalizes paper, compiled PDF, code, evaluator/task materials, logs, and bibliography, then runs: I1 score verification by golden-evaluator rerun; I2 specification-violation review; I3 reference verification through scholarly APIs and disambiguation; and I4 method-code alignment review (pp. 6-7, 25-32). I2 and I4 include majority-vote LLM judgments, and flagged I1-I3 results plus sampled I4 judgments received human verification/validation (p. 9).

### Implications for SERVO

This is an audit mapping, not terminology claimed by the authors. `S` maps to literature grounding, citation graph, experiment brief, and evidence-tagged claims; `G` to ideation and PEE exploration; `E` to sandboxed solver execution; `V` to Ground, Claim Verifier, golden-evaluator reruns, specification checks, reference verification, and method-code comparison; and `M` to file-backed briefs, notes, logs, scores, ablations, and evidence annotations. The mapping must preserve that provenance and structural checks are not equivalent to scientific validity or human expert acceptance.

## Findings

- In the CoE audit table, ScientistOne reports **12/12** score verification, **0/15** specification violations, **0/337** hallucinated bibliography entries, and **14/15** method-code alignment (pp. 1, 8-10). These denominators and the ADRS audit corpus are essential: they are not universal guarantees.
- Across the 75-paper corpus, ScientistOne has `0/337` hallucinated bibliography entries, while the reported comparator rates are ARC `3/196`, AIR `21/222`, and DS `42/201` (pp. 8-10). The result is attributed to citation-graph retrieval and cached provenance, but reference existence is not passage-level entailment.
- ScientistOne extracted 639 numeric claims; 627 passed the 5% tolerance check (`98.1%`). Manual inspection estimates corrected CPR at approximately `99%`, not 100%, with hardware constants, LaTeX subscripts, and hyperparameters accounting for many false positives (pp. 10-11).
- Best-of-3 ADRS scores are Prism `26.26`, Cloudcast `618.08` (lower is better), EPLB `0.1459`, LLM-SQL `0.7222`, and TXN `3906`. The paper reports exceeding the human baseline on every task, with best overall scores on Cloudcast and EPLB (pp. 12-14). These are canonical evaluator reruns of selected code, not necessarily the original papers' reported values.
- MLE-Bench results are Gold on 3D Object Detection and RSNA Brain Tumor, Silver on iMet 2020 and iNaturalist, and Above Median on AI4Code. Parameter Golf reports `1.0600` SOTA under a 16MB and under-10-minute setup, but the stated MLE-Bench protocol allows up to 16 grading-server queries rather than the official single-submission protocol (pp. 13-14, 32-33).
- ScholarPeer gives ScientistOne average Overall `4.5` and `6/15` accepts; best-of-3 is `6.6` and `4/5` accepts. The paper describes this as a proxy, with soundness below clarity and qualitative overclaims still escaping current checks (p. 11).
- Search-scaling results are directional and partly single-seed. On TXN, reported scores rise from `3636` at width 5 to `4255` at width 20; higher evaluator budget increases metric-gaming risk from about `0%` at budget 100 to about `50%` at 200 and `70%` at 500 on LLM-SQL (pp. 23-24).

## Limitations

ADRS tests single-metric solver optimization rather than problem formulation, workload characterization, multi-dataset analysis, deployment tradeoffs, or explanations of why a solution works. Therefore competitive ADRS performance cannot be promoted to human-level autonomous scientific research (pp. 14-16).

The CoE audit catches structural integrity failures but does not prove scientific correctness, novelty, or responsible use. I3's existence/near-match checks do not establish that a real source supports the citing claim. I1-I3 false positives were manually corrected, while false negatives were not systematically bounded; I4 relies on majority-vote judgments with only sampled human validation, and LLM judges may miss domain-specific errors (pp. 10, 15-16).

Current domain coverage is computational and relies on deterministic evaluators. Wet-lab protocols, simulations, proofs, and other domains require different evidence checks. Baseline comparisons also depend on materially different patches, reruns, and tool availability, limiting causal attribution to architecture alone (pp. 15-16, 33-35).

The system has one reported method-code misalignment in the 15-paper alignment result, and the Claim Verifier catches nearly all rather than all such cases (p. 10). The paper also reports specification and method failures in the broader audit corpus, including wrong metric scales, evaluator exploits, and fictional or incomplete algorithms (pp. 19-20, 25-32). Scalable paper generation may flood review systems and create subtle errors outside the audit scope (p. 16).

## Citation Assessments

### Inventory and direct occurrences

`core14-manifest.json` source index 13 records citation key `meng2026scientistone`, page count 35, exact version/hash, an empty `manuscript_link_ids` list, and the frozen supplementary description. `submission/references.bib:207-212` contains the matching title, author list, arXiv identifier, and year. Neither `submission/main.tex` nor `submission/main_ko.tex` contains `meng2026scientistone`, `ScientistOne`, or a corresponding text citation. Catalog occurrences in `systems_desc.json` and `target_systems.md` are supplementary catalog surfaces, not manuscript citation links.

There are therefore **no EN or KO citation-link occurrences** to assess for citation role, entailment, source location, or occurrence-level correction. The frozen catalog description is assessed clause by clause below.

### Frozen supplementary description, clause by clause

Frozen text:

> A research system grounded in the literature. A problem investigator builds a citation graph, filters thousands of papers to an elite set, and produces an experiment brief; an ideator proposes and ranks approaches. A parallel explore-exploit search runs branches, versions, and iterations with spec-violation pruning and automatic ablations. A four-part audit re-runs scores, checks spec violations, verifies reference APIs, and checks code-method alignment (reporting zero hallucinated citations). Memory is backed by files (citation graph, structured notes, logs). Computational benchmarks only; fully autonomous with no required human gate.

- **“A research system grounded in the literature.”** `SUPPORTED`, severity `none`. CoE requires claims to trace to grounding evidence, and PI retrieves/filters literature before producing the brief (pp. 4-5, 21-22). “Grounded” describes the architecture and does not guarantee that all downstream claims are correct.
- **“A problem investigator builds a citation graph, filters thousands of papers to an elite set, and produces an experiment brief; an ideator proposes and ranks approaches.”** `SUPPORTED_WITH_QUALIFICATION`, severity `minor`. The graph, approximately 2,000-5,000 candidates, relevance/alignment filtering, brief, and novelty/feasibility ranking are explicit (pp. 5, 21-22). “Elite set” is catalog shorthand rather than a formal source term; “Core/Adjacent survivors” is safer.
- **“A parallel explore-exploit search runs branches, versions, and iterations with spec-violation pruning and automatic ablations.”** `SUPPORTED_WITH_QUALIFICATION`, severity `minor`. PEE uses isolated branches, evaluated versions, pruning, and ablation (pp. 5, 23-24). “Automatic” is a pipeline property, but specification checks include majority-vote LLM judgments and benchmark/evaluator assumptions (pp. 6-7).
- **“A four-part audit re-runs scores, checks spec violations, verifies reference APIs, and checks code-method alignment (reporting zero hallucinated citations).”** `SUPPORTED_WITH_QUALIFICATION`, severity `major`. I1-I4 match the described checks and the result is `0/337` for ScientistOne's 15-paper ADRS audit corpus (pp. 6-10). The result is not a universal zero-hallucination guarantee; I3 checks bibliographic existence/near-matches rather than full citation entailment, and I4 is partly LLM-judged with sampled human validation. Recommended wording: “the reported ADRS audit found 0/337 hallucinated bibliography entries under its reference-verification protocol.”
- **“Memory is backed by files (citation graph, structured notes, logs).”** `SUPPORTED_WITH_QUALIFICATION`, severity `minor`. File-backed citation-graph material, briefs/structured artifacts, scores, execution logs, ablations, and evidence annotations persist across stages (pp. 4-7, 21-22). “Structured artifacts/briefs/logs” is more precise than implying a general learned or cross-project failure-memory guard.
- **“Computational benchmarks only; fully autonomous with no required human gate.”** `PARTIAL`, severity `major`. The reported evaluation is computational and no wet-lab loop is shown, but the paper also includes literature investigation, discovery, writing, and post-hoc audit. “End-to-end autonomous” describes the generation pipeline, while flagged I1-I3 results were manually verified, sampled I4 judgments were human-validated, and ScholarPeer is explicitly not a replacement for human expert evaluation (pp. 9, 15). Recommended wording: “evaluated on computational benchmarks and presented as autonomous for the generation pipeline; the reported integrity audit and expert-acceptance comparisons still include human validation.”

**Frozen-description verdict:** `minor_revision`, with a **major wording blocker** on unqualified “fully autonomous with no required human gate” and a major scope qualification required for “zero hallucinated citations.”

## Korean Parity

No ScientistOne sentence or citation occurrence exists in `submission/main.tex` or `submission/main_ko.tex`; the inventory also has no EN/KO link IDs. Manuscript parity is therefore **N/A for positive claims, but complete for absence**: both language manuscripts omit the source, so there is no translation mismatch to grade.

The frozen description is English-only on the supplementary catalog surface. If a Korean description is added, it must preserve the same distinctions: `0/337` as an evaluated ADRS result, reference existence versus citation entailment, computational benchmark scope, file-backed artifacts rather than a general failure-memory guard, and autonomous generation versus human-validated audit/expert acceptance. A literal Korean rendering of “fully autonomous with no required human gate” would reproduce the unsupported overclaim.

## Overall Verdict

**`minor_revision`.** Identity, exact version, and complete 35-page coverage are confirmed. The bibliography entry is correct, but the source is not cited in either manuscript, so no EN/KO occurrence-level entailment defect exists. The frozen description faithfully captures the architecture and four audit mechanisms at a high level, but requires bounded wording for the `0/337` result, reference-entailment limits, file-backed memory scope, computational evaluation scope, and the distinction between autonomous generation and human-assisted audit/acceptance. It must not imply universal citation correctness, scientific validity, novelty, wet-lab autonomy, or human-free certification.

## Completion Checklist

- [x] Citation key, bibliography metadata, title, authors, identifier, version, absolute PDF path, SHA-256, and page count recorded.
- [x] Pages 1-35 covered in order, including references, appendices, implementation details, benchmark adaptation, search scaling, and audit failure cases.
- [x] Research problem, historical/disciplinary context, prior-work relationship, structure, methods, findings, limitations, and SERVO implications assessed.
- [x] Frozen supplementary description assessed clause by clause with page-grounded verdicts, severity, and corrections.
- [x] Citation inventory checked against the manifest, bibliography, English manuscript, Korean manuscript, and supplementary catalog surfaces.
- [x] No EN or KO citation-link occurrence exists; absence is explicitly recorded.
- [x] English/Korean parity assessed as omitted/N/A for manuscript text, with future terminology constraints recorded.
- [x] Quantitative values, denominators, conditions, benchmark protocol limits, and audit limitations recorded.
- [x] Fully autonomous/no-human-gate wording assessed and narrowed to the generation pipeline boundary.
- [x] No API/model call made and no other PDF opened.
- [x] System description assessed against the full source.

AUDIT_COMPLETE: yes
PAGES_COVERED: 1-35
EN_LINKS_COVERED: none
KO_LINKS_COVERED: none
SYSTEM_DESCRIPTION_ASSESSED: yes
VERDICT: minor_revision
