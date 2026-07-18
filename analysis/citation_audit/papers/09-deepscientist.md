# `deepscientist` Full-Text Audit

## Source Identity

- **Citation key:** none. DeepScientist is a catalog-only core system; no direct English or Korean manuscript occurrence is assigned.
- **PDF title:** *DeepScientist: Advancing Frontier-Pushing Scientific Findings Progressively*.
- **Authors:** Yixuan Weng, Minjun Zhu, Qiujie Xie, Qiyao Sun, Zhen Lin, Sifan Liu, and Yue Zhang, Engineering School, Westlake University.
- **Identifier/version:** `arXiv:2509.26603v1`, 30 Sep 2025; version status `exact`.
- **Absolute PDF path:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/DeepScientist Advancing Frontier-Pushing Scientific Findings.pdf`.
- **SHA-256:** `76c3805b2344c32f3245f0500bcfd8ae129cd221f821da509817121c1485cae8`.
- **PDF extent:** 19 pages. The supplied evidence and `core14-manifest.json` agree on identity, path, hash, and page count.
- **Scope restriction:** Only the three specified evidence files and repository-local manifest context were used. No API/model call was made, and no other paper PDF was opened.

## Full-Text Coverage

PDF pages **1-19** were read sequentially, including figures, tables, references on pp. 11-14, Appendices A-C on pp. 15-18, and generated-paper links on p. 19. The evidence records visual checks of relevant pages including pp. 1, 4, 6, 8, 9, 15, 17, and 19. Coverage is complete; no relevant extraction or layout ambiguity remains.

## Problem and Context

The paper addresses goal-directed computational scientific discovery: repeatedly identifying limitations of selected state-of-the-art methods, proposing candidate methods, implementing them, and validating improvements. It motivates this against undirected recombination in earlier AI Scientist-style systems, arguing that scientific progress should be anchored to explicit frontier limitations (pp. 1-3).

The disciplinary context is machine-learning research with rapid computational feedback, not general science or wet-lab autonomy. The three starting tasks are Agent Failure Attribution, LLM Inference Acceleration, and AI Text Detection. The paper models candidate methods as a conceptual search space with an expensive latent value function and uses Bayesian-optimization language to organize the search (pp. 3-5).

## Structure and Argument

The paper proceeds from motivation and the goal-oriented objective (pp. 1-3), through related work and the optimization formulation (pp. 3-4), to the three-stage architecture: **Strategize & Hypothesize**, **Implement & Verify**, and **Analyze & Report** (pp. 4-5). It then reports task results and paper-quality evaluation (pp. 6-8), analyzes trajectories, failure causes, and parallel scaling (pp. 8-10), and closes with ethics, human responsibility, limitations, and implementation/cost details (pp. 10-18). References and links to three generated papers appear on pp. 11-14 and 19.

The argument supports the existence of a staged, memory-backed search and implementation pipeline. It does not establish that every generated result is independently reproducible, that the small scaling study is a general scaling law, or that generated papers meet ordinary peer-review standards.

## Methods and Evidence

Findings Memory stores Idea, Implement, and Progress Findings, combining human knowledge with system-generated records. An LLM reviewer assigns utility, quality, and exploration scores from 0 to 100. A UCB score combines exploitation and exploration; the selected candidate is implemented in an existing SOTA repository inside a sandbox with internet access. Successful baseline-surpassing validation promotes an Implement Finding to a Progress Finding, after which analysis agents perform ablations, new-dataset checks, and synthesis (pp. 4-5, 17).

The experiments use manually reproduced baselines, two servers with eight H800 GPUs each, and three human supervisors. Reported funnel totals are over 5,000 ideas, about 1,100 implemented/validated candidates, and 21 progress findings. The paper also reports a one-week parallel experiment at 4, 8, and 16 GPUs, logs for 300 failed implementations, and manual inspection plus an independent CLI rerun for implementation verification (pp. 5, 8-9, 17).

## Findings

- For Agent Failure Attribution, A2P is reported at 47.46% accuracy versus a 16.67% listed baseline in the algorithm-generated setting, a reported relative improvement of 183.7%.
- For LLM Inference Acceleration, ACRA is reported at 193.90 tokens/s versus 190.25, a reported improvement of 1.9%.
- For AI Text Detection, PA-Detect is reported at 0.863 AUROC versus 0.800, with 60 ms versus 117 ms latency and a reported AUROC improvement of 7.9%.
- The AI-text trajectory is described as T-Detect -> TDT -> PA-Detect. The paper reports 2,472 ideas for this trajectory and 21 progress findings overall.
- A five-paper human review praised ideation and novelty but reported average soundness of 2.27 and holistic rating 5.00 versus an ICLR 2025 average of 5.08, with recurring concerns about missing baselines, ablations, motivation studies, and empirical rigor (pp. 7, 15).

These are reported benchmark results under the paper's selected baselines and protocols. They do not by themselves certify broad human-level scientific superiority.

## Limitations

The search has low yield: the paper reports approximately 1-3% selected success in one analysis and 1-5% more broadly, while exact denominators and scopes differ. Approximately 60% of sampled failures are attributed to implementation errors; a separate account reports about half of initial implementation attempts failing from internal timeouts. These figures must not be conflated (pp. 8, 16-17).

The method is intended for rapid-feedback computational domains and is described as impractical for high-cost pretraining or pharmaceutical synthesis. Reported total cost is about $100,000. Scaling evidence is limited to a small one-week range, with 1, 4, and 11 progress findings at 4, 8, and 16 GPUs. Baselines were manually reproduced, outputs were manually inspected, three experts supervised verification, and the authors retain human goal-setting and final responsibility. The Analyze & Report module is not open-sourced, and the complete pipeline depends on named agent implementations and container infrastructure (pp. 5, 8-11, 17-18).

### Implications for SERVO

This is an audit-level mapping, not terminology claimed by the authors. `S` maps to the selected SOTA limitations, literature, repositories, and datasets; `G` to Strategize & Hypothesize and UCB-based candidate selection; `E` to sandboxed coding and experiments; `V` to baseline comparison, reruns, ablations, human inspection, and paper review; `M` to Findings Memory; and `pi` to the staged agent policy that selects, implements, promotes, and analyzes findings. The mapping must preserve that memory records and promotion rules do not remove human oversight or prove independent scientific validation.

## Citation Assessments

### Catalog-only status and direct occurrences

`core14-manifest.json` records `citation_key: null` and `manuscript_link_ids: []` for DeepScientist. The English and Korean manuscripts contain no direct DeepScientist citation occurrence or Korean catalog row. Therefore there is **no catalog-only direct occurrence** to assess: no occurrence ID, source line, citation role, manuscript claim, or occurrence-level entailment verdict exists.

### Frozen supplementary description

Frozen text:

> A system that searches for methods exceeding a target state-of-the-art, formalized as Bayesian optimization over a value function. A surrogate LLM reviewer scores candidate ideas; a coding agent implements them in a sandbox with internet access on top of existing repositories, promoting a candidate only when it beats the baseline. A UCB acquisition function balances exploitation and exploration; a findings memory accumulates unverified, implemented, and SOTA-exceeding results. Across three computational domains it reported exceeding human SOTA; three human experts performed final verification and hallucination filtering.

- **“searches for methods exceeding a target state-of-the-art”** - `SUPPORTED_WITH_QUALIFICATION`, severity `minor`. The objective and selected starting SOTA methods are explicit (pp. 2, 5-6), but this is a bounded objective for three reported tasks, not a universal guarantee.
- **“formalized as Bayesian optimization over a value function”** - `SUPPORTED_WITH_QUALIFICATION`, severity `minor`. The paper defines a latent black-box value function over a conceptual method space (pp. 3-4), while the operational mechanism uses LLM scores and UCB rather than a demonstrated calibrated conventional posterior.
- **“A surrogate LLM reviewer scores candidate ideas”** - `SUPPORTED`, severity `none`. Utility, quality, and exploration scores are described on pp. 4-5.
- **“a coding agent implements them in a sandbox with internet access on top of existing repositories”** - `SUPPORTED`, severity `none`. Repository-level implementation, sandbox permissions, internet access, baseline duplication, and CLI rerun are described on pp. 5 and 17.
- **“promoting a candidate only when it beats the baseline”** - `SUPPORTED_WITH_QUALIFICATION`, severity `minor`. Baseline-surpassing validation is the Progress Finding promotion rule, but Idea and Implement Findings exist before success, and human inspection remains part of the workflow (pp. 5, 17).
- **“A UCB acquisition function balances exploitation and exploration”** - `SUPPORTED`, severity `none`. Equation (2) combines utility/quality exploitation with exploration value; Appendix C fixes `K=15`, `wu=1`, `wq=1`, and `kappa=1` (pp. 5, 17).
- **“a findings memory accumulates unverified, implemented, and SOTA-exceeding results”** - `SUPPORTED`, severity `none`. The three Finding types and their retention for later cycles are described on pp. 4-5. This does not imply that every stored result is independently verified.
- **“Across three computational domains it reported exceeding human SOTA”** - `SUPPORTED_WITH_QUALIFICATION`, severity `major`. The paper reports improvements over selected human baselines in three computational tasks (pp. 5-6), but the phrase must retain “reported” and benchmark scope; it cannot imply broad superiority over human science.
- **“three human experts performed final verification and hallucination filtering”** - `SUPPORTED_WITH_QUALIFICATION`, severity `major`. Three experts and manual inspection/filtering are documented (pp. 5, 7-8, 15, 17), but the review also found weak soundness, missing ablations, and incomplete validation. Human checks are not equivalent to full independent scientific validation.

**Frozen-description verdict:** `minor_revision`. The mechanism description is substantially faithful. The last sentence should be narrowed to “Across three computational benchmark domains, it reported improvements over the selected human SOTA baselines; three human experts supervised final verification and hallucination filtering, while reviewer analysis identified substantial empirical-rigor limitations.”

## Korean Parity

There are no direct English or Korean occurrence links: `EN_LINKS_COVERED: none` and `KO_LINKS_COVERED: none`. Korean parity is therefore **`omitted`**, not `equivalent` or `meaning_shifted`, because the Korean manuscript has no DeepScientist catalog entry or translated frozen description. This is not a citation error; it is catalog absence. Any future Korean description should preserve the three-benchmark scope, the distinction between human supervision and scientific validation, and the LLM/UCB/memory mechanism.

## Overall Verdict

**`minor_revision`.** Source identity is exact and full 19-page coverage is complete. There is no direct manuscript citation to invalidate or approve. The frozen catalog description accurately captures the principal architecture, but its “human SOTA” wording needs explicit benchmark scope and its human verification clause should not imply complete scientific validation. The report remains catalog-only, with no EN/KO direct occurrence.

## Completion Checklist

- [x] Source identity, authors, arXiv identifier, absolute PDF path, SHA-256, page count, and exact version status recorded.
- [x] PDF pages 1-19 covered in order, including references, appendices, and generated-paper links.
- [x] Research problem, context, prior-work relationship, structure, methods, findings, limitations, and SERVO implications assessed.
- [x] Frozen supplementary description assessed clause by clause with page-grounded verdicts and severity.
- [x] Catalog-only status and absence of direct EN/KO citation occurrences confirmed.
- [x] English/Korean parity classified as `omitted` because no Korean counterpart exists.
- [x] Quantitative results, denominators/scope cautions, human-review findings, cost, failure, scaling, and reproducibility limits recorded.
- [x] No API/model call made and no other paper PDF opened.
- [x] System description assessed against the full source.

AUDIT_COMPLETE: yes
PAGES_COVERED: 1-19
EN_LINKS_COVERED: none
KO_LINKS_COVERED: none
SYSTEM_DESCRIPTION_ASSESSED: yes
VERDICT: minor_revision
