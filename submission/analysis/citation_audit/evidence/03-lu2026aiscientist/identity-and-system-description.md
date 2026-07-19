# `ai_scientist_2026` Identity and Frozen System Description Audit

## Lane Scope

- Active source only: `ai_scientist_2026` / `lu2026aiscientist`.
- Assigned checks: PDF/BibTeX identity, version, SHA-256, page count, complete reading of PDF pages 1-9, visual inspection of relevant figures and tables, and clause-level assessment of the frozen supplementary description.
- Source PDF: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/Towards end-to-end automation of AI research.pdf`.
- No other source PDF was opened. No external model or API was called.

## Source Identity

- Citation key: `lu2026aiscientist`.
- BibTeX type: `@article`.
- BibTeX title: *Towards end-to-end automation of AI research*.
- BibTeX authors: Chris Lu; Cong Lu; Robert Tjarko Lange; Yutaro Yamada; Shengran Hu; Jakob Foerster; David Ha; Jeff Clune.
- BibTeX publication: *Nature* 651, 914-919 (2026).
- BibTeX DOI: `10.1038/s41586-026-10265-5`.
- PDF-internal title: *Towards end-to-end automation of AI research* (PDF p. 1; printed p. 914).
- PDF-internal author list: Chris Lu, Cong Lu, Robert Tjarko Lange, Yutaro Yamada, Shengran Hu, Jakob Foerster, David Ha, and Jeff Clune (PDF p. 1).
- PDF-internal DOI: `10.1038/s41586-026-10265-5` (PDF p. 1 and document metadata).
- PDF publication facts: received 8 July 2025, accepted 11 February 2026, published online 25 March 2026; *Nature* volume 651, issue dated 26 March 2026, printed pages 914-919 (PDF pp. 1-6).
- Absolute PDF path: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/Towards end-to-end automation of AI research.pdf`.
- SHA-256: `a75e0d93447f400179136bf18d909df29e0c8ccaeba076a1dfb1beeef0e0e10d`.
- `pdfinfo` page count: 9.
- PDF metadata: title and DOI identify the same Nature article; the file has 9 PDF pages, including the six printed article pages and three online Methods pages.
- Version status: `exact`. The title, complete author list and order, journal, volume, printed page range, year, and DOI all match the BibTeX record. The hash, page count, and path also match `core14-manifest.json`.

## Full-Text and Visual Coverage

- PDF p. 1: abstract, end-to-end scope, two operating modes, automated reviewer motivation, computational ML scope, and external workshop setup.
- PDF p. 2: four-phase workflow; archive growth and novelty checking; template-based versus template-free execution; experiment journal; manuscript construction; Fig. 1.
- PDF p. 3: reviewer ensemble and benchmark; pre- and post-cutoff results; external workshop submission protocol and reviewer scores; Table 1.
- PDF p. 4: limitations, human and system failure modes, computational-only boundary, ethics, and Fig. 2.
- PDF p. 5: conclusion, references, and Fig. 3 on staged agentic tree search and compute scaling.
- PDF p. 6: remaining references, licensing, and publication information.
- PDF p. 7: Methods for both modes, template-based archive-conditioned ideation, template-free generalized ideation, four-stage experiment manager, and tree-search setup.
- PDF p. 8: node execution, best-first expansion, replication and aggregation nodes, VLM feedback, dataset access, manuscript writing, and reviewer design.
- PDF p. 9: five-review meta-review, reviewer validation and caveat, ethics, datasets, code availability, author contributions, and disclosures.
- Pages 1-9 were read in order using page-bounded extraction. PDF pp. 2-5 were also rendered at 180 dpi and visually inspected. The render confirms Fig. 1's scoring/archive and workflow diagram, Table 1's reviewer metrics, Fig. 2's workshop-paper evidence, and Fig. 3's tree-search schematic, real run, and compute-scaling panel.

## Frozen Description

> A successor LLM system using agentic tree search over experiment plans, with replication nodes that re-run experiments and report results as mean and standard deviation over random seeds. It includes an automated LLM reviewer (about 0.69 balanced accuracy) and an open-endedness archive that conditions later search. One output cleared an external workshop peer-review bar. Experiments are computational only; no physical experiment.

## Clause-Level Assessment

| Frozen clause | Status | PDF evidence and assessment |
|---|---|---|
| "A successor LLM system" | **Supported with qualification** | The article evaluates a template-based system and a more open-ended, template-free system; the latter is the tree-search version and its code is released as `AI-Scientist-v2` (PDF pp. 1-2, 7, 9). The article itself generally calls both variants "The AI Scientist," so "successor" is a reasonable catalogue label for the template-free version, not the paper's precise system name for every reported result. |
| "using agentic tree search over experiment plans" | **Supported for the template-free mode only** | The template-free system runs four experiment stages, each with its own tree search, and represents each node with a plan, executable script, results, plots, critiques, and status (PDF pp. 2, 5, 7-8; Fig. 3). A real tree and a compute-scaling experiment are shown in Fig. 3b,c (PDF p. 5). The template-based mode instead follows a linear plan, so the clause should name the template-free variant. |
| "with replication nodes that re-run experiments" | **Supported as an implemented method description; not independently demonstrated in the main article** | Methods explicitly defines replication nodes as rerunning a parent experiment with different random seeds and says several are typically created (PDF p. 8). Fig. 3a includes replication and aggregation node types in the system schematic (PDF p. 5). The nine-page article does not present a node-level execution trace or generated-paper result that independently verifies that replication nodes ran in a particular reported paper. |
| "and report results as mean and standard deviation over random seeds" | **Supported as an implemented method description; output evidence deferred** | Methods says aggregation nodes combine replication-node outputs and generate figures that explicitly show mean and s.d. (PDF p. 8). This directly supports the intended reporting mechanism. Fig. 1b and Fig. 3c contain error bars for separate paper-generation or compute-scaling experiments, but they are standard errors and are not evidence of a generated paper's replication-node mean/s.d. output (PDF pp. 2, 5). The main article therefore documents the mechanism but does not display its claimed downstream artifact. |
| "It includes an automated LLM reviewer" | **Supported** | The o4-mini reviewer reads a manuscript PDF, produces structured rubric fields and a preliminary decision, and combines five independent reviews through an area-chair-style meta-review (PDF pp. 2-3, 8-9). |
| "about 0.69 balanced accuracy" | **Supported with a necessary condition** | Table 1 reports `0.69 +/- 0.04` balanced accuracy for the Automated Reviewer on ICLR papers from 2017-2024, before its stated knowledge cutoff (PDF p. 3). On the cleaner 2025 post-cutoff set, it falls to `0.66 +/- 0.03` (PDF p. 3). The human `0.66` comparator comes from a separate NeurIPS 2021 consistency experiment with a different paper pool, and the authors explicitly say the comparison is not exact (PDF pp. 3, 9). The unqualified number hides the pre-cutoff condition and possible contamination. |
| "an open-endedness archive" | **Supported as architecture** | The workflow iteratively grows an archive of research directions and hypotheses; each idea records a title, rationale, and experimental plan (PDF p. 2). The template-based Methods section says new ideas are variations or extensions of existing ideas in the growing archive and records separate interestingness, novelty, and feasibility scores (PDF p. 7). |
| "[the archive] conditions later search" | **Supported only for later idea generation, with limited demonstration** | The clearest operational statement is that each template-based iteration proposes ideas as variations or extensions of ideas already in the archive (PDF p. 7). The main text points to an example progression in Supplementary Information C.4 (PDF p. 2), which is not contained in this nine-page file. No archive ablation or causal comparison establishes that archive feedback improves later ideas. The phrase should not be read as saying that the archive conditions best-first experimental tree search: that search is guided by metrics, training dynamics, plot quality, and node status (PDF p. 8). |
| "One output cleared an external workshop peer-review bar" | **Supported with qualification** | Three generated papers were submitted, with IRB and organizer approval, to the ICLR 2025 ICBINB workshop's blind external review process. One received scores 6, 7, and 6 (mean 6.33), above the workshop's average acceptance threshold; organizers said it would in all likelihood have been accepted if it had not been withdrawn under the pre-established protocol (PDF pp. 1-4; Fig. 2). This is actual external reviewer evidence, not an automated-reviewer simulation. It was not a formal final acceptance: all AI papers were withdrawn, the workshop acceptance rate was 70%, two of three did not clear the bar, and internal human researchers judged that none met the main-conference bar (PDF pp. 3-4, 9). |
| "Experiments are computational only" | **Supported and demonstrated for the reported scope** | The paper explicitly says it focuses on machine learning because the experiments occur entirely on computers and later states that the system presently conducts computational experiments only (PDF pp. 1, 4). The data-availability section lists text, image, and HuggingFace datasets used by the two variants (PDF p. 9). |
| "no physical experiment" | **Supported** | No reported system run controls a physical apparatus or collects wet-lab measurements. The authors describe applying the playbook to automated chemistry laboratories only as future work (PDF p. 4). Human paper selection, code checking, and workshop review do not constitute physical scientific experiments. |

## Demonstrated Versus Described

| Item requested for special checking | Evidence class | Assessment |
|---|---|---|
| Archive feedback | **Method-level operation described; effect not demonstrated** | The archive is explicit in the workflow and template-based algorithm, and later ideas are said to extend archived ideas (PDF pp. 2, 7). The article does not show an archive ablation, a complete same-run archive trace, or evidence that archive feedback improves research quality. It also does not establish archive conditioning of the experiment-tree policy. |
| External workshop review | **Demonstrated, with selection and withdrawal qualifications** | Actual external workshop reviewers scored three submissions, with one above the threshold (PDF p. 3; Fig. 2 on PDF p. 4). Humans manually filtered outputs at each stage before submission, checked topic alignment, code implementation, and formatting, and all papers were withdrawn before a formal acceptance outcome (PDF pp. 3, 9). |
| Replication mean and s.d. | **Architecture and intended output described; no direct generated-output demonstration in this file** | Replication and aggregation node behavior is explicit in Methods and schematic form (PDF pp. 5, 8). The main article does not reproduce a generated paper's seed-level values, aggregate script, or mean/s.d. figure attributable to those nodes. |
| Computational-only scope | **Both declared and instantiated** | The scope is stated directly (PDF pp. 1, 4), and all reported execution substrates are code, computational training/evaluation, and public datasets (PDF pp. 2, 5, 7-9). Physical laboratories are future work only (PDF p. 4). |

## Material Boundaries and Omissions

1. **Two modes are compressed into one description.** Tree search and replication nodes belong to the template-free version; linear experiment execution and the most explicit archive-conditioned idea loop are described separately for the template-based version (PDF pp. 2, 7-8).
2. **Human filtering precedes the workshop result.** Humans manually selected promising outputs at each stage and checked workshop fit, implementation, and formatting before three papers were submitted (PDF p. 3). The scientific workflow within each selected paper was not human-modified, but selection was not autonomous.
3. **The workshop claim is bounded.** One of three papers exceeded a relatively low workshop threshold, with 70% workshop acceptance versus 32% for the ICLR main conference; it was withdrawn and never received a final acceptance (PDF pp. 1, 3-4).
4. **Reviewer validity is conditional.** The headline `0.69` is a pre-cutoff result. Post-cutoff balanced accuracy is `0.66`, and comparison with the human baseline uses different conference paper pools (PDF pp. 3, 9).
5. **The paper documents severe reliability limits.** It reports naive ideas, incorrect method implementations, inadequate rigor, experimental errors, duplicate figures, inaccurate citations, and hallucinations; it says the system cannot yet meet top-tier standards or consistently meet workshop standards (PDF p. 4).
6. **The archive and replication claims need evidence labels.** Both are concrete algorithm descriptions, but this local article does not provide an ablation or a direct generated-artifact trace proving their effect or use in the externally reviewed paper (PDF pp. 2, 5, 7-8).

## Recommended Corrected Description

The Nature article evaluates template-based and template-free versions of The AI Scientist. Its template-free version uses a four-stage agentic tree search for computational machine-learning experiments; Methods specifies replication nodes that rerun parent experiments with different seeds and aggregation nodes intended to produce mean-and-s.d. figures, although the nine-page article does not show a generated paper's seed-level replication artifact. The system includes a five-review o4-mini meta-reviewer whose balanced accuracy was `0.69 +/- 0.04` on pre-cutoff ICLR papers and `0.66 +/- 0.03` on a post-cutoff set. An idea archive is described as conditioning later idea generation, but its causal benefit and its use as feedback to the experiment-tree policy are not demonstrated here. After manual selection and checking, one of three AI-generated submissions scored above the ICLR 2025 ICBINB workshop threshold in external blind review, but all submissions were withdrawn and none received final publication acceptance. All reported scientific experiments are computational; physical-laboratory extension is future work.

## Overall Verdict

**`minor_revision`** for the frozen supplementary description.

The central system facts are source-grounded: the template-free tree search, replication and aggregation node definitions, automated reviewer, external workshop evaluation, and computational-only boundary all appear explicitly. Revision is still needed to avoid merging the two modes, to condition the `0.69` metric on the pre-cutoff set, to distinguish a likely workshop acceptance from formal acceptance, and to label archive feedback and replication mean/s.d. as documented mechanisms rather than independently demonstrated effects or artifacts in this nine-page article.

## Completion Checklist

- [x] BibTeX title, complete author list, journal, volume, pages, year, and DOI checked against the PDF.
- [x] Absolute PDF path, SHA-256, and nine-page count verified locally.
- [x] Version status assessed as `exact`.
- [x] PDF pages 1-9 read in order.
- [x] Fig. 1, Table 1, Fig. 2, and Fig. 3 rendered and visually inspected.
- [x] Every clause of the frozen supplementary description assessed.
- [x] Archive feedback classified as a described method whose effect is not demonstrated here.
- [x] External workshop review classified as demonstrated, with manual-selection and withdrawal boundaries.
- [x] Replication mean/s.d. classified as a documented mechanism without a displayed generated-output trace in this file.
- [x] Computational-only scope classified as stated and demonstrated.
- [x] Only the assigned evidence file was created.

SYSTEM_DESCRIPTION_ASSESSED: yes
EVIDENCE_COMPLETE: yes
