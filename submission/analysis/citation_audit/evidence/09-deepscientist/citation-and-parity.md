# DeepScientist: Citation, Catalog, and English/Korean Parity Audit

## Scope and source control

- **Audited source:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/DeepScientist Advancing Frontier-Pushing Scientific Findings.pdf`
- **PDF identity:** *DeepScientist: Advancing Frontier-Pushing Scientific Findings Progressively*; Yixuan Weng, Minjun Zhu, Qiujie Xie, Qiyao Sun, Zhen Lin, Sifan Liu, Yue Zhang; arXiv:2509.26603v1, 30 Sep 2025.
- **Version status:** `exact`.
- **PDF pages:** 19. PDF SHA-256: `76c3805b2344c32f3245f0500bcfd8ae129cd221f821da509817121c1485cae8`.
- **Coverage:** PDF pages 1-19 read in order, including figures/tables, references (pp. 11-14), human-review appendix (pp. 15-16), implementation details (pp. 17-18), and generated-paper links (p. 19). Rendered visual checks included pp. 1, 4, 6, 8, 9, 15, 17, and 19; no relevant extraction/layout ambiguity remained.

## Catalog-only and direct citation occurrence

The frozen manifest entry is catalog-only:

- `core14-manifest.json:158-166` has `citation_key: null` and `manuscript_link_ids: []`.
- `target_systems.md:25` labels the item `DeepScientist (Weng 2025)` with citation `(catalog)` and descriptor `exceeds SOTA`.
- The English manuscript and Korean manuscript contain no direct DeepScientist citation occurrence or Korean DeepScientist catalog row. The only catalog description is the English frozen description in `systems_desc.json:11` and its duplicated supplementary description in `core14-manifest.json:166`.

**Result:** `catalog-only: yes`; **direct citation occurrences:** `none`; **English linked occurrences:** `none`; **Korean linked occurrences:** `none`.

This means there is no citation entailment verdict to assign to a manuscript sentence. The audit target is the frozen catalog description and its parity status, not a bibliography citation.

## Frozen description, sentence-by-sentence evidence

Frozen text (`systems_desc.json:11` / `core14-manifest.json:166`):

> A system that searches for methods exceeding a target state-of-the-art, formalized as Bayesian optimization over a value function. A surrogate LLM reviewer scores candidate ideas; a coding agent implements them in a sandbox with internet access on top of existing repositories, promoting a candidate only when it beats the baseline. A UCB acquisition function balances exploitation and exploration; a findings memory accumulates unverified, implemented, and SOTA-exceeding results. Across three computational domains it reported exceeding human SOTA; three human experts performed final verification and hallucination filtering.

### Sentence 1

**Claim:** DeepScientist searches for methods exceeding a target SOTA and formalizes discovery as Bayesian optimization over a value function.

**PDF evidence:** pp. 2-4 define the objective as maximizing a latent black-box true-value function `f` over candidate methods (Eq. 1), explicitly place the problem in Bayesian Optimization, and describe the target as surpassing the selected human SOTA. The three starting methods and tasks are listed in Table 1 on p. 5.

**Verdict:** `SUPPORTED_WITH_QUALIFICATION`, severity `minor`. The paper presents Bayesian Optimization as a formal modeling framework, but the candidate-method space is conceptual and not explicitly defined (p. 4). The value is approximated by an LLM surrogate, not directly observed as a calibrated scientific-value function. “Searches for methods exceeding a target state-of-the-art” is accurate for the stated experimental objective, not a general guarantee of discovery beyond every SOTA.

### Sentence 2

**Claim:** An LLM reviewer scores ideas; a coding agent implements them in a sandbox with internet access over existing repositories; a candidate is promoted only when it beats the baseline.

**PDF evidence:** pp. 4-5 describe the surrogate LLM reviewer and its utility, quality, and exploration scores; the coding agent performs repository-level implementation in a sandbox with full permissions and internet access; successful validation promotes an Implement Finding to a Progress Finding only after surpassing the baseline. Appendix C, p. 17, adds that the baseline repository is duplicated into a sandbox and the agent is confined to that directory; DeepScientist independently reruns the main script after completion.

**Verdict:** `SUPPORTED_WITH_QUALIFICATION`, severity `minor`. “Only when it beats the baseline” correctly describes Progress Finding promotion, but not every intermediate record: hypotheses can enter memory as Idea Findings and selected candidates become Implement Findings before success. The paper also says human supervisors manually inspected experimental results (pp. 5, 17), so the operational workflow is not wholly unattended despite the system authors’ “fully autonomous” framing.

### Sentence 3

**Claim:** UCB balances exploitation and exploration, and Findings Memory accumulates unverified, implemented, and SOTA-exceeding results.

**PDF evidence:** pp. 4-5 show the three-stage cycle and Eq. 2: `wu vu + wq vq` is the exploitation score and `kappa ve` is the exploration score. The same pages describe Findings Memory records as Idea, Implement, and Progress Findings, with prior human knowledge and system findings retained for subsequent exploration. Appendix C, p. 17, records `K=15`, `wu=1`, `wq=1`, and `kappa=1`.

**Verdict:** `SUPPORTED`, severity `none`. The wording is a faithful compact description of the mechanism. “Accumulates” should be read as the paper’s operational Findings Memory, not as a claim that every stored result has been independently verified.

### Sentence 4

**Claim:** Across three computational domains, the system reported exceeding human SOTA; three human experts performed final verification and hallucination filtering.

**PDF evidence:** pp. 2 and 5 identify three computational tasks: Agent Failure Attribution, LLM Inference Acceleration, and AI Text Detection. Table/Figure 3 on p. 6 reports DeepScientist values of 29.31/47.46 accuracy, 193.90 tokens/s, and 0.863 AUROC versus the listed human baselines; the reported relative improvements include +183.7%, +1.9%, and +7.9%. Pages 5, 7-8, 15, and 17 describe three human experts/program-committee reviewers, human review of five generated papers, and manual inspection to filter hallucinations.

**Verdict:** `SUPPORTED_WITH_QUALIFICATION`, severity `major`. The PDF reports these results and human checks, but “exceeding human SOTA” is scope-limited to the three selected computational benchmarks and the paper’s comparison setup. It does not establish broad superiority over human science. The human review evidence also reveals substantial weaknesses: average DeepScientist paper rating 5.00 versus ICLR 2025 average 5.08, soundness 2.27, and reviewers’ recurring concerns about missing baselines, insufficient ablations, and weak empirical rigor (pp. 7-8 and 15). The description should therefore retain “reported” and explicitly preserve benchmark scope and human verification rather than imply independently certified scientific breakthroughs.

## Overclaim and parity findings

1. **Main overclaim risk:** The frozen description compresses a benchmark result into “exceeding human SOTA.” This is defensible only with the three-task/selected-baseline qualifier. The PDF itself makes stronger first-of-kind and frontier-wide claims in the abstract, introduction, and conclusion (pp. 1-2, 10), but its own review appendix documents important limits.
2. **Autonomy risk:** “System” and the underlying paper’s “fully autonomous” language can obscure required human supervision. Three experts supervised verification and filtered hallucinations; Appendix C says all experimental results were manually inspected (pp. 5, 17). A safer catalog phrasing would say “autonomous exploration and implementation pipeline with human verification.”
3. **Validation risk:** The description says “final verification and hallucination filtering,” which is supported, but should not be read as full scientific validation. The paper reports that approximately 60% of sampled failed trials ended in implementation errors and that reviewers found insufficient validation/analysis in generated papers (pp. 8, 15-17).
4. **English/Korean parity:** `equivalent` is not applicable because there is no Korean counterpart occurrence. The Korean manuscript has no DeepScientist entry, citation, or translated frozen description. Therefore parity status is **`omitted` (catalog absent in Korean)**, not `equivalent` and not `meaning_shifted`.

## Recommended frozen-description disposition

Keep the catalog-only status and the core mechanism description. Revise the last sentence, if the frozen artifact is allowed to change, to preserve scope and oversight:

> Across three computational benchmark domains, it reported improvements over the selected human SOTA baselines; three human experts supervised final verification and hallucination filtering, while the paper’s reviewer analysis identified substantial empirical-rigor limitations.

This recommendation is a wording correction, not a citation correction, because no direct manuscript citation occurrence exists.

## Completion

`catalog-only: yes`

`DIRECT_CITATION_OCCURRENCES: none`

`EN_LINKS_COVERED: none`

`KO_LINKS_COVERED: none`

`KOREAN_PARITY: omitted (no Korean catalog occurrence)`

`EVIDENCE_COMPLETE: yes`
