# ScientistOne: identity and architecture audit

## Audit boundary and source identity

- **Audited source:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/ScientistOne - Towards Human-Level Autonomous Research via Chain-of-Evidence.pdf`
- **Title:** *ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence*.
- **Authors:** Rui Meng, Bhavana Dalvi Mishra, Jiefeng Chen, Chun-Liang Li, Palash Goyal, Mihir Parmar, Yiwen Song, Yale Song, Rajarishi Sinha, Parthasarathy Ranganathan, Burak Gokturk, Jinsung Yoon, and Tomas Pfister (PDF p. 1).
- **Date/version:** 27 May 2026; the PDF identifies itself as an arXiv-style manuscript (p. 1). No separate version claim is inferred beyond the PDF itself.
- **Extent:** 35 PDF pages. Pages 1-35 were read sequentially, including figures, tables, references, appendices, implementation details, benchmark adaptation notes, and audit failure cases.
- **SHA-256:** `9d4fa9d1e9e6b1cdccfeff02fecbd28b5b961594952a1ac96e00ad135bed0a51` (matches `core14-manifest.json`).
- **Scope constraint:** Only this ScientistOne PDF was opened for the audit. No other PDF was opened. No API or model call was made. Repository-local manifest text was used only to recover the frozen supplementary description.

## Problem statement and context

The paper identifies an evidence-chain problem in autonomous research. A conventional multi-stage agent can produce a coherent-looking manuscript while errors introduced in literature synthesis, experiment design, score reporting, citations, or method description are propagated and amplified across later stages (pp. 1-2). Existing evaluation often measures surface quality, benchmark score, or acceptance-like judgments without checking whether claims are supported by the underlying artifacts (pp. 1-4).

The paper's response is **Chain-of-Evidence (CoE)**: every claim should be traceable through recorded supporting claims and evidence to a grounding source (p. 4). ScientistOne is presented as an end-to-end autonomous system that maintains this chain from literature grounding through discovery, paper writing, and verification (pp. 4-6). The paper also introduces a separate **CoE Integrity Audit**, a post-hoc cross-system audit of completed paper/code/reference bundles rather than a component that makes every baseline system CoE-compliant (pp. 6, 9-10).

The evaluation context is computational. The main benchmark is ADRS, a set of systems-optimization tasks with a golden evaluator and human/agent baselines (pp. 6-8, 12-14). The paper reports additional generalization on MLE-Bench tasks and other computational tasks, but explicitly limits the claim: ADRS reduces systems research to single-metric optimization and should not be equated with broad systems research or scientific validity (pp. 14-16).

## Complete 35-page reading record

| PDF pages | Contents read |
|---|---|
| 1 | Title, authors, abstract, contributions, headline CoE audit results, and introduction opening. |
| 2 | Introduction continuation: evidence-chain failure modes, motivation, three-stage system overview, and contribution claims. |
| 3 | Related work: autonomous research systems, literature grounding, discovery/search, paper writing, and verification/audit positioning. |
| 4 | Chain-of-Evidence principle, claim/evidence terminology, and transition to ScientistOne's system description. |
| 5 | Figure 1 and pipeline overview; Stage 1 literature grounding and PI brief; Stage 2 discovery and parallel branches. |
| 6 | Stage 3 Paper Writing & Verification; Claim Verifier; Figure 2 and four CoE Integrity Audit checks. |
| 7 | Audit check definitions; benchmark setup; artifact normalization; evaluator and audit protocol details. |
| 8 | Baseline systems, ADRS adaptation, controlled comparison, and Table 1 setup. |
| 9 | CoE audit results and analysis: score verification, specification violations, reference integrity, and method-code alignment. |
| 10 | Reference-integrity analysis, method-code alignment, and limits of the forensic audit. |
| 11 | Score-verification error analysis and corrected numerical interpretation; additional audit caveats. |
| 12 | Table 3 solution-discovery results, task setup, and comparison with human/agent baselines. |
| 13 | Cloudcast/EPLB/other task results, generated algorithmic pipelines, and task-level analysis. |
| 14 | Generalization results, MLE-Bench and parameter-golf discussion, and conclusion of empirical results. |
| 15 | Conclusion, open problems, and beginning of limitations. |
| 16 | Limitations: benchmark scope/depth, domain coverage, reference verification depth, reviewer limitations, adaptation, and false negatives. |
| 17-18 | Full reference list. References were read as part of this PDF; cited papers were not opened. |
| 19 | Appendix A paper-quality statistics and structural statistics for the 75-paper audit corpus. |
| 20 | Appendix A failure-case examples, including evaluator/specification and evidence-chain failures. |
| 21 | Appendix B system implementation details: file-backed stages and citation-graph grounding. |
| 22 | Appendix B literature filtering, investigation rounds, evidence annotations, and Ground/Claim Verifier behavior. |
| 23-24 | Appendix C Solution Discovery search scaling; parallel branches, tree width/depth, explore-exploit settings, and ablation/search results. |
| 25-26 | Appendix D CoE Audit Details and Appendix E I1 score-verification failure categories and examples. |
| 27-30 | Appendix E I2 specification-violation and I3 hallucinated-reference categories, tables, examples, and near misses. |
| 31-32 | Appendix E I4 method-code alignment failure analysis, including method/implementation inversion and partial alignment. |
| 33-35 | Appendix F MLE-Bench/parameter-golf evaluation and Appendix G adaptation/implementation notes, including backend and tool-routing details. |

## Architecture extracted from the paper

### Three stages

1. **Literature Grounding (Stage 1).** The Problem Investigator (PI) starts from seed papers, traverses a citation graph through Semantic Scholar, filters the graph by methodology relevance and problem alignment, conducts multi-round specialist investigation, and produces a grounded experiment brief (pp. 5, 21-22). Appendix B describes approximately 2-4 seed papers, up to two citation hops, a graph of roughly 2,000-5,000 papers, tiering into Core/Adjacent/Peripheral, and a gate requiring sufficient relevant literature (p. 21).
2. **Discovery (Stage 2).** The Ideator proposes candidate approaches from the PI brief, scores novelty and feasibility, and sends ranked proposals to the Parallel Explore-Exploit (PEE) orchestrator. Isolated branches run solver iterations, evaluate candidates, prune specification violations, select the best surviving solution, and perform ablations (p. 5). Appendix C studies branch width, tree shape, node budget, and iterations; the search is not merely a single linear run (pp. 23-24).
3. **Paper Writing & Verification (Stage 3).** The Paper Writer produces LaTeX through a claim-grounded pipeline. Claims are tagged to evidence such as score-file entries, citation keys, or ablation results; deterministic Ground checks validate tags and artifact existence, while a Critic checks alignment, contradictions, and overclaims. A Claim Verifier checks claims against declared evidence before final output (pp. 6, 22).

### Four-part CoE Integrity Audit

The post-hoc audit normalizes `paper.tex`, compiled PDF, solution code, evaluator/task materials, logs, and `references.bib` into a common artifact bundle (pp. 6-7, 25). It then runs four independent checks:

- **I1 Score Verification:** extract the paper score and re-run the submitted solution on the golden evaluator; compare within an adaptive tolerance (pp. 6-7, 25-26).
- **I2 Specification Violation:** use multiple LLM judgments against the code, evaluator, and task specification, with majority voting, to flag code that violates task rules (pp. 6, 27-30).
- **I3 Reference Verification:** resolve each bibliography entry through academic APIs, then use disambiguation to distinguish valid near-matches from hallucinated references (pp. 6, 10, 27-30).
- **I4 Method-Code Alignment:** compare the paper's described method, ablations, and implementation; the reported unit is an aligned paper, with sampled human validation of LLM judgments (pp. 6, 9-10, 31-32).

ScientistOne's reported audit results are 12/12 score verification, 0/15 specification violations, 0/337 hallucinated bibliography entries, and 14/15 method-code alignment (pp. 1, 9-10). These are results under the stated benchmark, artifact, adaptation, evaluator, and majority-vote protocols, not a proof of general scientific correctness. The paper explicitly notes limits including domain-specific false negatives, reference existence checks that do not establish citation entailment, LLM-review blind spots, and benchmark shallowness (pp. 15-16).

### Memory and autonomy boundary

The system's memory is file-backed: citation graph material, structured notes, experiment briefs, evaluator logs, score files, ablation results, and evidence annotations persist between stages (pp. 5-6, 21-22). This supports traceability and stage handoff, but the source does not establish a general cross-project failure-memory mechanism that turns every past failure into a hard guard.

The paper presents ScientistOne as fully autonomous and does not require a human gate in its described pipeline (pp. 1, 5-6). However, the audit itself is not human-free: all I1-I3 flagged results were manually verified, I4 judgments were validated on a sample, and the evaluation uses human reviewers for audit confirmation (p. 9). Therefore “fully autonomous” is a generation/pipeline property and must not be read as “no human involvement anywhere in the evaluation or audit.”

## Frozen supplementary description, clause by clause

Frozen description from `submission/analysis/citation_audit/core14-manifest.json`:

> A research system grounded in the literature. A problem investigator builds a citation graph, filters thousands of papers to an elite set, and produces an experiment brief; an ideator proposes and ranks approaches. A parallel explore-exploit search runs branches, versions, and iterations with spec-violation pruning and automatic ablations. A four-part audit re-runs scores, checks spec violations, verifies reference APIs, and checks code-method alignment (reporting zero hallucinated citations). Memory is backed by files (citation graph, structured notes, logs). Computational benchmarks only; fully autonomous with no required human gate.

### 1. “A research system grounded in the literature.”

**CONFIRMED.** The CoE principle starts from grounding sources, and Stage 1 retrieves and filters literature before the experiment brief is produced (pp. 4-5, 21-22). “Grounded” describes the intended architecture; it does not guarantee that all downstream claims are scientifically correct.

### 2. “A problem investigator builds a citation graph, filters thousands of papers to an elite set, and produces an experiment brief.”

**CONFIRMED, with bounded wording.** PI starts from seed papers, traverses citations/references, produces a graph of approximately 2,000-5,000 papers, filters by methodology relevance and problem alignment into tiers, and outputs a research/experiment brief (pp. 5, 21-22). “Elite set” is a reasonable shorthand for Core/Adjacent survivors, but the paper's actual tier names and threshold gate should be retained in a formal description.

### 3. “An ideator proposes and ranks approaches.”

**CONFIRMED.** The Ideator generates candidate approaches from the PI brief and scores them on novelty and feasibility before distributing top-ranked proposals to parallel branches (p. 5).

### 4. “A parallel explore-exploit search runs branches, versions, and iterations with spec-violation pruning and automatic ablations.”

**CONFIRMED.** PEE runs isolated parallel branches; Solver agents iterate, candidate solutions are evaluated, specification-violation candidates are pruned, and the selected solution undergoes ablation experiments (p. 5). Appendix C confirms that branch width, tree/node budget, and iteration configuration are explicit search variables (pp. 23-24). “Automatic” is supported as a pipeline behavior, subject to the benchmark implementation and evaluator assumptions.

### 5. “A four-part audit re-runs scores, checks spec violations, verifies reference APIs, and checks code-method alignment (reporting zero hallucinated citations).”

**CONFIRMED, but the scope is essential.** The four checks are I1 Score Verification, I2 Specification Violation, I3 Reference Verification, and I4 Method-Code Alignment (pp. 6-7). The source reports 0/337 hallucinated references for ScientistOne (pp. 1, 9-10). This is a result for 15 ScientistOne papers in the ADRS audit corpus, not a universal zero-hallucination guarantee. I3 uses academic APIs plus LLM disambiguation, while I4 is partly LLM-judged and human-validated only on a sample (pp. 6, 9, 16, 27-32).

### 6. “Memory is backed by files (citation graph, structured notes, logs).”

**CONFIRMED, with scope note.** The implementation description explicitly uses file-backed stage communication and records citation-graph materials, structured notes, experiment briefs, scores, logs, evidence annotations, and ablation artifacts (pp. 21-22). The clause accurately describes persistence, but it should not be expanded into a claim of a general learned or cross-project failure-memory guard system.

### 7. “Computational benchmarks only; fully autonomous with no required human gate.”

**PARTIALLY CONFIRMED / NEEDS QUALIFICATION.** The evaluated work is computational and the paper presents no wet-lab loop; ADRS, MLE-Bench, parameter-golf, and the other named tasks are computational (pp. 6-8, 12-16, 33-35). “Benchmarks only” is too narrow if read as the entire system's scope: the paper includes literature investigation, generated solver algorithms, paper writing, and an audit corpus in addition to benchmark scoring. “Fully autonomous with no required human gate” is supported for the described generation pipeline (pp. 1, 5-6), but the evaluation/audit explicitly uses human verification of flagged results and sampled I4 judgments (p. 9). Recommended wording: “evaluated on computational benchmarks and presented as fully autonomous at generation time; the reported integrity audit still includes human verification of flagged/sampled judgments.”

## Overall audit verdict

**Identity: CONFIRMED. Architecture: CONFIRMED. Frozen description: MINOR_REVISION.** The frozen description captures the core system accurately: literature-grounded PI, ranked ideation, PEE search with pruning/ablations, four integrity checks, and file-backed evidence. The required corrections are bounded scope: (1) qualify zero hallucinated citations as the reported `0/337` ADRS audit result; (2) do not imply that file-backed memory is a general cross-project failure guard; and (3) distinguish autonomous generation from the human-assisted verification used in the reported audit. “Computational benchmarks only” should be softened so it does not erase the literature, discovery, writing, and verification components.

EVIDENCE_COMPLETE: yes
