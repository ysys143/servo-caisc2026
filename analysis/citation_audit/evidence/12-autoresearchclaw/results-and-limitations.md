# AutoResearchClaw: results and limitations evidence

## Scope and source control

- **Single source read:** `AutoResearchClaw - Self-Reinforcing Autonomous Research with Human-AI Collaboration.pdf`.
- **Extent checked:** PDF pages 1-23, in order. The PDF metadata reports 23 pages.
- **Audit method:** direct page-by-page reading of extracted text and page-rendered content. No other PDF was opened. No API or model call was made for this audit.
- Page references below are PDF page numbers, not the printed section page where these differ.

## Experimental design

- **System shape (pp. 1-4, 13-16):** AutoResearchClaw is a 23-stage pipeline spanning Discovery, Experimentation, and Writing. The stages include scoping/literature work, debate-based hypothesis generation, experiment design, code generation, sandboxed execution, iterative refinement, result analysis, Proceed/Refine/Pivot research decisions, paper drafting/review/revision, quality gating, lesson archiving, export, and citation verification.
- **Contracts and checkpoints (p. 13):** every stage declares JSON-schema inputs/outputs, validation/acceptance criteria, and error namespaces; checkpoint resumption is supported. The paper explains that 12 stages caused overloaded intermediate work, while 30+ caused excessive context reconstruction, motivating the 23-stage compromise.
- **Benchmark (pp. 6-8, 17-20):** ARC-Bench has 25 CPU-executable ML topics (T01-T25), plus a 20-topic scientific-domain extension: 10 high-energy physics, 7 systems biology, and 3 statistics tasks. The experiment-stage rubric weights Code Development, Code Execution, and Result Analysis as 25:25:50. Two independent agent reviewers grade cells; disagreements above 0.20 per leaf are re-adjudicated.
- **Controlled comparison (p. 6):** AI Scientist v2 and AIDE-ML use the same stated LLM backbone, sandbox, and per-experiment time budgets as AutoResearchClaw. The comparison is experiment-stage focused because some baselines do not reliably produce complete papers.
- **Execution design (pp. 4, 17):** generated experiments run in Docker with dependency-install, data-acquisition, and offline-execution phases. A read-only evaluation harness owns metric reporting. AST/security/import checks block or warn on specified unsafe calls/modules. Complexity scoring selects a code-generation cascade; the stated threshold is `tau = 0.6`.

## Multi-agent debate

- **Architecture (pp. 1-2, 4, 13-15):** debate occurs at hypothesis generation and result analysis, with `K=3` agents plus a synthesizer. Hypothesis roles are Innovator, Pragmatist, and Contrarian; result roles are Optimist, Skeptic, and Methodologist. The synthesizer must produce falsifiable hypotheses with testability criteria/baselines and later distinguish supported from unsupported claims.
- **Domain adaptation (pp. 14-15):** the HEP-ph bank changes roles to Theorist/Phenomenologist/Experimentalist for hypothesis work and Model-Builder/Phenomenologist/Experimentalist for result analysis. Other domains use profiles/adapters over the ML bank.
- **Design-space result (p. 20):** `K=2` reduced hypothesis diversity by 23%; `K=5` increased tokens by 67% for only 8% more diversity over `K=3`. The authors therefore call `K=3` the diversity-per-token sweet spot for ML topics, while noting specialized domains may benefit from different role sets.
- **Ablation result (p. 9):** removing debate produced the largest quality drop, `-1.37` with `p=0.003`; the paper attributes this to loss of feasibility filtering and skeptical result scrutiny.

## Self-healing executor and failure memory

- **Self-healing loop (pp. 4-6, 14, 16-17):** failures are captured as signatures, diagnosed, and repaired with targeted fixes. The decision loop can Proceed when evidence supports the hypothesis, Refine when the direction is sound but results are weak, or Pivot when the direction is fundamentally flawed. The pseudocode allows up to 2 pivots and 10 refines, with repair attempts inside execution.
- **Failure preservation (p. 4):** the system preserves recoverable artifacts and runs conditions breadth-first so partial completion remains informative if execution stops. Static checks include identical-ablation detection, hardcoded-metric detection, and a degenerate-metric warning when all conditions are identical.
- **Sandbox constraints (pp. 4, 17):** Phase 2 disables network access during execution; containers run as the host UID:GID with stated memory/shared-memory/time limits. The paper describes this as preventing exfiltration and downloading precomputed results, but this is a design claim, not an independently verified security evaluation in this audit.
- **Cross-run evolution (pp. 5-6, 14, 16):** lessons are extracted from repairs, Pivot/Refine decisions, HITL feedback, and verification. Each lesson has category, severity, and mitigation. Retrieval uses `w(l) = s(l) * exp(-ln(2) * delta_t / T_1/2)` with default half-life 30 days; lessons are prompt overlays, not model retraining.
- **Evolution tuning (p. 20):** a 7-day half-life discarded useful lessons too quickly, while infinite half-life accumulated contradictory advice after 15 runs; 30 days reportedly influenced 3-5 later runs while fading over time.
- **Ablation (p. 9):** removing self-healing reduced completion from 10/10 to 6/10 despite three attempts per topic. Removing evolution reduced completion from 10/10 to 9/10 and quality by 0.48, described as reliability improvement mainly through avoiding known failure modes rather than raising the quality ceiling. Removing both debate and healing reduced completion to 4/10, quality to 3.47, and acceptance to 0.

## Hallucination and result verification

- **Numeric registry (p. 5):** execution creates a whitelist of per-condition means, standard deviations, and seed measurements. Draft tables are populated only from the registry; a post-generation verifier checks numeric claims per condition. Unmatched claims in Abstract/Results/Experiments reject the document; other-section claims become visible placeholders. The writing agent can read but not modify the registry.
- **Citation pipeline (pp. 5, 13-16):** references are checked through DOI resolution (CrossRef), fuzzy title matching (OpenAlex), arXiv lookup, and Semantic Scholar fallback, followed by an LLM relevance classification into Verified/Suspicious/Hallucinated. Hallucinated references are removed before finalization. The paper presents these as safeguards, not proof that conclusions are scientifically correct.
- **Benchmark grounding criteria (pp. 6, 19-20):** numerical claims must trace to captured artifacts; verdicts must agree with measured direction; missing conditions/datasets/seeds are penalized. A timeout forces Code Execution to zero, retains code credit, and caps Result Analysis at 0.1 when writing never executes.
- **Verification ablation (p. 9):** without verification, apparent acceptance rose from 3/10 to 5/10, but manual audit found 3 of those 5 papers contained values absent from any measurement record. The paper treats the lower verified acceptance as the integrity cost of rejecting fabricated numbers.
- **Important limitation (pp. 10, 21):** verification is necessary but not sufficient. In Topic T10, Full-Auto passed the numeric gate because identical zero values were real logged measurements, yet they did not answer the research question. The gate cannot establish that measurements are scientifically informative or semantically appropriate.

## Human intervention modes

- **Seven modes (pp. 5, 7-8, 20):** Full-Auto (0 interventions); Gate-Only (literature screening, experiment design, quality gate); Thorough (phase boundaries); CoPilot (six high-leverage points plus SmartPause); Step-by-Step (all 23 stages); Pre-Experiment (early stages 5, 8, 9); and Post-Experiment (late stages 14, 17, 20).
- **SmartPause (p. 5):** pauses when estimated uncertainty exceeds a learned threshold. The threshold adapts to approval history, pausing more often where the researcher frequently overrides the system.
- **End-to-end ablation (pp. 7-9, 20):** across 10 topics, the table reports Full-Auto valid 8/10, mean quality 4.03, accept 25%; Gate-Only 10/10, 5.03, 50%; CoPilot 8/10, 7.27, 87.5%; Thorough 7/10, 4.86, 42.9%; Step-by-Step 10/10, 5.19, 50%; Pre-Experiment 8/10, 4.28, 37.5%; Post-Experiment 6/10, 5.08, 50%. The paper text also says CoPilot used 19 targeted interventions and Step-by-Step 29, while the table's `Interventions` column lists 6 and 23 respectively; this internal discrepancy should be preserved as an audit caveat rather than silently resolved.
- **Interpretation (pp. 8-10):** more intervention is not monotonic. Pre-Experiment improves feasibility but cannot enforce later claim discipline; Post-Experiment can improve faithfulness but cannot create missing evidence. Gate-Only is presented as a low-cost operating point, while CoPilot is strongest because it combines early design guidance with late claim checking.
- **T10 case (pp. 10-11, 21):** Full-Auto generated eight indistinguishable zero-bias/zero-variance CV conditions and scored 4.0; CoPilot prompted checks for nonzero contrasts, LOOCV feasibility, and log-bounded claims, producing differentiated results across nine pipelines and scoring 8.0. The authors use this to argue for targeted intervention at experimental bottlenecks.

## Benchmark results

- **Main experiment-stage result (pp. 1-2, 6-7):** AutoResearchClaw CoPilot overall strict score `0.648`, versus AI Scientist v2 `0.419` and AIDE-ML `0.511`; the paper reports improvements of 54.7% and 26.8%, respectively. Full-Auto scored `0.596`.
- **Dimension scores (p. 7):** CoPilot/Full-Auto/AI Scientist v2/AIDE-ML were respectively Code Development `0.968/0.938/0.712/0.958`, Code Execution `0.578/0.562/0.442/0.415`, Result Analysis `0.523/0.442/0.261/0.336`, and Overall `0.648/0.596/0.419/0.511`. The largest relative comparison cited is Result Analysis: CoPilot versus AI Scientist v2, 100.4%.
- **Failure counts (p. 7):** Full-Auto failed to produce valid results on 2/25 topics, both complex multi-file dependency cases; AI Scientist v2 failed on 6/25, concentrated in iterative-refinement topics.
- **Cross-domain result (pp. 7-8):** CoPilot means were Biology `0.912`, Statistics `0.898`, HEP-ph `0.489`, Overall `0.867`. AIDE-ML scored `0.452` in Statistics and `0.090` overall; AI Scientist v2 `0.418` and `0.084` overall. Both baselines scored zero on Biology and HEP-ph because the paper says required stacks were unavailable under fair-input conditions. The HEP result still incurred penalties for insufficient deliverables and unsupported meta-claims; one Statistics run was excluded from its column mean for missing metric artifacts.

## Reported limitations and audit-relevant caveats

- **Evidence quality is not equivalent to execution success (pp. 10, 21-22):** a complete manuscript can contain scientifically uninformative, real measurements. The T10 collapse is the clearest example.
- **Failure handling remains incomplete (p. 21):** 11 of 13 invalid canonical HITL runs failed at Stage 17. Recurring causes were no usable metrics upstream, environment/dependency breakage, dataset/resource failure, and over-ambitious or invalid designs. The hard anti-fabrication block is described as correct but currently conflating heterogeneous causes; the authors propose graceful degradation that surfaces upstream causes and limitations.
- **Export and formatting defects (p. 22):** in an audit of 20 canonical Full-Auto + Step-by-Step deliverables, abstract-before-`maketitle` occurred 20/20; malformed Markdown-style section headings 17/20; duplicated figures 16/20; “Learned Skills”/a-evolve leakage 9/20; pseudo-citations 2/20; and citation voids occurred in a small count. Local single-pass pdflatex passed 4/5 Step-by-Step and 3/5 Full-Auto samples, which the authors explicitly call necessary but insufficient for submission readiness.
- **Citation breadth (p. 22):** across five audited topics, Full-Auto had 94 citations and Step-by-Step 59, but some individual papers were below expected norms (examples include 2, 4, 7, and 13 citations). HITL improved citation discipline more reliably than breadth.
- **Human-study limitation (p. 23):** the HITL experiments used scripted interventions, not live human participants; future live-researcher studies would require appropriate IRB review.
- **Cost and misuse (p. 23):** the current implementation is reported to cost approximately `$3-15` in LLM usage per run. The authors note risks of submission flooding, superficial novelty, and over-reliance on automated judgments.
- **Scope of safeguards (pp. 22-23):** citation and numeric checks reduce unsupported evidence but do not guarantee correct scientific conclusions, submission-ready formatting, or responsible use. The authors retain human responsibility for problem selection, interpretation, final claims, and submission decisions.
- **Study-design caveats (pp. 6, 9, 19-20):** the system is stochastic and path-dependent, so the component ablation uses best-of-N with three reruns per configuration-topic pair; these figures are not directly comparable to the single-run HITL table. Cross-system comparisons are mostly ML experiment-stage comparisons, and the scientific-domain baseline gaps partly reflect environment/software availability rather than only reasoning capability.

## Bottom line

The PDF supports a claim that AutoResearchClaw improves the measured experiment-stage and end-to-end outcomes under its stated benchmark, sandbox, reviewer, and scripted-HITL protocols. The strongest evidence is the combination of debate/self-healing ablations, registry-based anti-fabrication checks, and the T10 contrast between real-but-uninformative output and human-guided differentiated experiments. The PDF does **not** support treating verification as proof of scientific validity, treating benchmark scores as live-human generalization, or treating the export pipeline as submission-ready without further review.

EVIDENCE_COMPLETE: yes
