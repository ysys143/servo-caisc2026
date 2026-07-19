# ScientistOne: citation and parity audit

## Audit boundary and method

- Audited source: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/ScientistOne - Towards Human-Level Autonomous Research via Chain-of-Evidence.pdf` only.
- The source reports 35 PDF pages. I read the extracted text in PDF page order from page 1 through page 35, including the main text, references, and appendices. No other PDF was opened.
- No API call and no model call was made. The PDF's own descriptions of academic APIs and LLM-backed checks are source content, not actions performed in this audit.
- Page references below are PDF page numbers.

## Citation inventory and manuscript occurrence

The core inventory is `submission/analysis/citation_audit/core14-manifest.json`, entry index 13:

| Field | Inventory value | Audit result |
|---|---|---|
| system | `scientistone` / ScientistOne | matches the PDF title and system name (p. 1) |
| citation key | `meng2026scientistone` | matches `submission/references.bib:207-212`, including title, authors, arXiv `2605.26340`, and year 2026 |
| PDF path | ScientistOne Core Systems PDF | exact requested target |
| SHA-256 | `9d4fa9d1e9e6b1cdccfeff02fecbd28b5b961594952a1ac96e00ad135bed0a51` | matches the inventory record |
| page count | 35 | matches `pdfinfo` |
| version status | `exact` | consistent with the inspected file metadata: arXiv `2605.26340v1`, 25 May 2026 |
| `manuscript_link_ids` | `[]` | no EN or KO citation-link record exists |

`submission/references.bib` contains the bibliography record, but the target citation is not used in the main manuscript: `submission/main.tex` has no occurrence of `meng2026scientistone`, `ScientistOne`, or `Meng` as a citation/text occurrence, and `submission/main_ko.tex` likewise has none. The catalog does contain `scientistone` in `submission/analysis/multicoder/systems_desc.json:15` and `submission/analysis/multicoder/target_systems.md:29`; those are catalog surfaces, not manuscript citations. Verdict: **bibliographic inventory present, manuscript citation absent, frozen catalog description present**.

## Frozen description: sentence-level evidence

Frozen description from `core14-manifest.json` and `systems_desc.json`:

> A research system grounded in the literature. A problem investigator builds a citation graph, filters thousands of papers to an elite set, and produces an experiment brief; an ideator proposes and ranks approaches. A parallel explore-exploit search runs branches, versions, and iterations with spec-violation pruning and automatic ablations. A four-part audit re-runs scores, checks spec violations, verifies reference APIs, and checks code-method alignment (reporting zero hallucinated citations). Memory is backed by files (citation graph, structured notes, logs). Computational benchmarks only; fully autonomous with no required human gate.

| Frozen claim | Direct PDF evidence | Judgment |
|---|---|---|
| Literature-grounded research system | CoE requires claims to trace to grounding evidence (pp. 4-5). Stage 1 Problem Investigator builds a citation graph from seed papers, reads up to 100 full-text PDFs per topic, and produces a grounded experiment brief (pp. 2, 4-5). | **Supported.** “Grounded in the literature” is accurate, with the operational scope described above. |
| Investigator builds citation graph, filters thousands to an elite set, produces brief | The citation graph and up-to-100-full-text-PDF brief are explicit (pp. 2, 4-5). The paper also says thousands of papers are filtered before generation (p. 4). | **Supported, but “elite set” is a catalog compression.** The PDF describes filtering to a smaller grounded set; it does not define “elite” as a formal term. |
| Ideator proposes and ranks approaches | Ideator generates candidates, scores novelty and feasibility, and distributes top-ranked proposals to parallel branches (p. 5). | **Supported.** |
| Parallel explore-exploit search over branches, versions, iterations | PEE orchestrator uses isolated branches; Solver iterates up to E evaluated versions per node, retains top-K branches, creates new branches, and repeats for I iterations across B branches (p. 5). | **Supported.** |
| Specification-violation pruning and automatic ablations | Best-run selector removes solutions flagged for specification violations and runs ablations on the selected solution (p. 5). | **Supported.** “Automatic” follows the described pipeline, but the sentence should not imply that every judgment is deterministic: I2 uses majority-vote LLM judgment (pp. 6-7). |
| Four-part audit | CoE Integrity Audit has I1 Score Verification, I2 Specification Violation, I3 Reference Verification, and I4 Method-Code Alignment (pp. 2, 6-7). | **Supported.** |
| Re-runs scores and checks specification violations | I1 re-runs submitted solutions on the golden evaluator; I2 checks code against evaluator and task specification (pp. 6-7). | **Supported, bounded to the ADRS audit setup.** |
| Verifies reference APIs | I3 resolves bibliography entries through Semantic Scholar, arXiv, OpenAlex, and CrossRef, with LLM disambiguation (pp. 6-7). | **Supported.** This verifies bibliographic existence/near-misses, not full claim-to-passage entailment. The paper explicitly says existence is far from sufficient (p. 15). |
| Checks code-method alignment | I4 compares the paper method with solution code using multiple independent judgments and majority vote (p. 7). | **Supported, with the paper's judgment-noise limitation.** |
| Reports zero hallucinated citations | Table 1 reports ScientistOne reference verification `0/337`; the text calls this zero hallucinated references (pp. 8-10). | **Supported for the evaluated 15 ADRS papers and 337 bibliography entries only.** Not a universal property of all possible runs or citations. |
| Memory backed by files: graph, notes, logs | The PDF explicitly names recorded evidence artifacts, including citation graph, structured research brief, evaluator scores, execution logs, ablation results, solver code, and source tags such as `experimental_log.md:N` (pp. 4-7, 10-11). | **Supported in substance.** The exact frozen parenthetical “structured notes” is not a named component in the inspected main text; “structured artifacts/briefs/logs” is safer. |
| Computational benchmarks only | Main evaluation is ADRS systems-optimization with fixed evaluators (pp. 7-8, 12). Additional tests are MLE-Bench and Parameter Golf, also computational (pp. 14, 32-33). The limitations explicitly distinguish untested wet-lab/open-ended domains (p. 15). | **Supported for this paper's evaluated tasks.** |
| Fully autonomous with no required human gate | The paper repeatedly labels ScientistOne “end-to-end autonomous” and describes a final paper produced by the pipeline (pp. 2, 4-6). | **Downgrade / do not publish as frozen.** The same paper states that all I1-I3 flagged results were manually verified by human reviewers and I4 was human-validated on a sample (p. 9); it also says automated ScholarPeer does not replace human expert evaluation (p. 15). “No required human gate” is not established as a deployment or submission claim. |

## Fully autonomous and human-gate review

The strongest source-supported formulation is: **“an end-to-end autonomous research pipeline for the reported computational benchmark workflow, with native claim verification and a post-hoc audit.”** This preserves the paper's system label without asserting that humans are unnecessary for scientific acceptance or audit validity.

Evidence against the unqualified frozen wording:

- “End-to-end autonomous” describes the system architecture and pipeline (pp. 2, 4, 14), not a proof that no human can or must intervene.
- Human reviewers manually verified every I1-I3 flagged result, and human reviewers validated I4 judgments on a sample (p. 9).
- The authors state that ScholarPeer is an automated proxy and “does not replace human expert evaluation” (p. 15).
- The authors also state that the checks cover structural integrity, not scientific correctness or novelty (pp. 15-16). Therefore zero hallucinated references and high audit scores cannot support “fully autonomous scientific discovery” or autonomous certification of validity.
- The system has one observed method-code misaligned paper (14/15 alignment), and the paper says the Claim Verifier catches nearly all such misrepresentation, not all of it (p. 10). The numeric CPR is approximately 99% after manual inspection, not 100% (pp. 10-11).

Verdict: **REFUTED as an unqualified frozen claim; CONFIRMED only when narrowed to the paper's computational pipeline execution and explicitly separated from human audit/expert acceptance.**

## Citation scope

Because `meng2026scientistone` has no EN or KO manuscript occurrence, there is no current manuscript sentence whose formal citation scope can be validated. The bibliography entry is currently unused by both language manuscripts. If cited later, the citation can support the system architecture, CoE mechanisms, reported audit results, and reported benchmark outcomes, but scope must retain the paper's bounds:

- Use `0/337` only for the 15-paper evaluation and its bibliography entries, not as a universal guarantee.
- Use the four-part audit description for the named I1-I4 checks; do not turn reference existence verification into passage-level citation correctness.
- Keep “human expert” statements tied to the paper's reported ADRS comparison and distinguish canonical re-runs from original-published baseline scores (pp. 12-13).
- Do not cite the paper as proving scientific novelty, scientific correctness, or human-free publication. The limitations expressly disclaim those conclusions (pp. 15-16).
- The paper's results include post-hoc human verification and majority-vote LLM judgments; omit those qualifiers only at the cost of materially overstating autonomy or audit certainty.

## EN/KO parity

There is no ScientistOne sentence or citation occurrence in `submission/main.tex` or `submission/main_ko.tex`, and no EN/KO link ID in the inventory. Therefore manuscript parity is **N/A for positive claims, but complete for absence**: neither language currently cites or describes this source in the manuscript.

The frozen description is English-only in `submission/analysis/multicoder/systems_desc.json`; no Korean counterpart was found on the audited manuscript surfaces. If a Korean catalog/manuscript description is added, it must preserve the same distinctions in both languages: computational benchmark scope, `0/337` evaluation scope, reference-existence versus citation-entailment limits, human validation of audit findings, and the narrowed autonomy wording. Translating the current final phrase literally as “완전 자율이며 필수적인 인간 게이트가 없다” would create the same unsupported overclaim in Korean.

## Final verdict

**MINOR REVISION / autonomy wording blocker for the frozen catalog sentence.** The architecture and four audit mechanisms are source-supported. The citation inventory is present and bibliographically correct, but the source is not cited in either manuscript. Replace the final frozen clause with a bounded computational-pipeline formulation and retain the human-review and structural-integrity limitations before using the description as evidence.

EVIDENCE_COMPLETE: yes
