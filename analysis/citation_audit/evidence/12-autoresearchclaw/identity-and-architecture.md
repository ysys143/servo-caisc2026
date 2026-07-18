# AutoResearchClaw: identity and architecture audit

## Audit boundary and source identity

- **Audited source:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/AutoResearchClaw - Self-Reinforcing Autonomous Research with Human-AI Collaboration.pdf`
- **Title:** *AutoResearchClaw: Self-Reinforcing Autonomous Research with Human-AI Collaboration*.
- **Authors:** Jiaqi Liu, Shi Qiu, Mairui Li, Bingzhou Li, Haonian Ji, Siwei Han, Xinyu Ye, Peng Xia, Zihan Dong, Congyu Zhang, Letian Zhang, Guiming Chen, Haoqin Tu, Xinyu Yang, Lu Feng, Xujiang Zhao, Haifeng Chen, Jiawei Zhou, Xiao Wang, Weitong Zhang, Hongtu Zhu, Yun Li, Jieru Mei, Hongliang Fei, Jiaheng Zhang, Linjie Li, Linjun Zhang, Yuyin Zhou, Sheng Wang, Caiming Xiong, James Zou, Zeyu Zheng, Cihang Xie, Mingyu Ding, and Huaxiu Yao. Affiliations are listed on PDF p. 1.
- **Identifier/version/date:** `arXiv:2605.20025v1`, 19 May 2026 (PDF p. 1).
- **Extent:** 23 PDF pages. Pages 1-23 were read sequentially, including figures/tables, references, Appendices A-J, the benchmark rubric, case-study artifacts, failure analysis, export audit, and ethics section. The final page is p. 23; extracted text contains a trailing page boundary after it.
- **SHA-256:** `be1d9a2c31d05052009ce1850b4573d9ae2010bc001bb2486c686647729ca491`.
- **Manifest comparison:** exact match to `submission/analysis/citation_audit/core14-manifest.json` for path, SHA-256, page count, identity, and version status.
- **Scope constraint:** Only this PDF was opened. No other PDF was opened and no API/model call was made. The frozen supplementary description was compared as repository-local text, not treated as an additional source.

## Problem statement and context

The paper frames autonomous research as an iterative loop rather than idea-to-paper linearization: hypotheses are challenged, experiments fail and inform revision, and lessons persist across cycles (pp. 1-2). It identifies three coupled deficiencies in prior systems: single-agent confirmation of its own hypotheses, termination/discarding after execution failure, and stateless runs that do not carry experience forward (pp. 1-3). The paper's central position is that these should be solved jointly because hypothesis quality, execution robustness, and accumulated experience reinforce one another (p. 2).

The related-work comparison claims that AutoResearchClaw is the first listed combination of end-to-end execution, multi-agent debate, self-healing, anti-fabrication verification, cross-run evolution, HITL gates, and sandbox security (p. 3, Table 1). This is the paper's positioning claim, not an independently verified priority claim.

## Complete 23-page reading record

| PDF pages | Contents read |
|---|---|
| 1 | Title, authors, abstract, GitHub link, Introduction opening. The abstract states five mechanisms and reports ARC-Bench and HITL headline results. |
| 2 | Introduction continuation: coupled problem diagnosis, five mechanisms, ARC-Bench contribution, targeted HITL claim, domain-specific extension, and safeguards. |
| 3 | Table 1 comparison; Related Work on autonomous research, multi-agent debate/cross-run learning, and human-AI collaboration. |
| 4 | Sections 3.1-3.3: 23-stage/three-phase overview, K=3 hypothesis/result debate, cascading code generation, Docker/network policy, and Pivot/Refine opening. |
| 5 | Self-healing continuation; Sections 3.4-3.6: verified numeric registry, four-layer citation pipeline, seven HITL modes, SmartPause, persistent lesson store, and decay equation. |
| 6 | Cross-run decay continuation; Experiments overview and setup: ARC-Bench, evaluation modes, CD:CE:RA weights, reviewers, baselines, common GPT-5.3-codex backbone, and page-6 result transition. |
| 7 | Table 2 results; end-to-end HITL table; Result Analysis and execution failure analysis; scientific-domain coverage setup. |
| 8 | Biology/statistics/HEP results and caveats; domain-specific agents and software; end-to-end HITL ablation and targeted-vs-dense intervention interpretation. |
| 9 | Table 5 component ablation, best-of-N protocol, debate/healing/evolution/verification findings, and T10 case-study opening. |
| 10 | T10 case study: identical zero outputs versus differentiated CoPilot outputs; verification limits; Conclusion. |
| 11-12 | Conclusion continuation, ethics pointer, and all references. References were read as part of this PDF and no cited paper PDF was opened. |
| 13 | Appendix A full 23-stage definitions and Table 6; Appendix B prompt architecture opening. |
| 14 | Algorithm/pseudocode, domain detection cascade, prompt banks, profiles/adapters, and cross-domain architecture. |
| 15 | Table 7 domain support; domain-differentiated roles; Topic_Init and Code_Generation deep dives. |
| 16 | Table 8 full stage requirements, outputs, verification constraints, and citation API pipeline. |
| 17 | Code-generation requirements; Appendix C Docker sandbox/security model; Appendix D ARC-Bench architecture opening. |
| 18 | ARC-Bench topic table, methods, metrics, and benchmark coverage. |
| 19-20 | Rubric equations, artifact sources, strict judge protocol, criteria, timeout/cross-validation rules, HITL mode map, and design-space exploration including K and lesson half-life. |
| 21 | T10 artifact comparison table; Appendix G pointer; Appendix H invalid-run failure analysis. |
| 22 | Appendix I export defects and compile audit; Appendix J positive impact, scientific integrity, researcher responsibility, and misuse risks. |
| 23 | Ethics continuation: verification/citation/HITL safeguards, Docker isolation, estimated $3-15 run cost, scripted rather than live HITL, and IRB caveat. |

## Architecture extracted from the paper

### Three phases and 23 stages

The pipeline is organized as Discovery, Experimentation, and Writing (p. 4). Appendix A gives the complete stage contract (pp. 13, 16):

1. `Topic_Init`; 2. `Problem_Decompose`; 3. `Search_Strategy`; 4. `Literature_Collect`; 5. `Literature_Screen`; 6. `Knowledge_Extract`; 7. `Synthesis`; 8. `Hypothesis_Gen`; 9. `Experiment_Design`; 10. `Code_Generation`; 11. `Resource_Planning`; 12. `Experiment_Run`; 13. `Iterative_Refine`; 14. `Result_Analysis`; 15. `Research_Decision`; 16. `Paper_Outline`; 17. `Paper_Draft`; 18. `Peer_Review`; 19. `Paper_Revision`; 20. `Quality_Gate`; 21. `Knowledge_Archive`; 22. `Export_Publish`; 23. `Citation_Verify`.

Each stage declares typed/validated input and output fields, acceptance criteria, and an error-code namespace; checkpoint resumption is supported (p. 4, p. 13). The paper says the current 23-stage granularity followed experiments with coarse 12-stage and finer 30+ alternatives (p. 13).

### Five mechanisms

- **Structured debate:** K=3 role-specialized agents plus a synthesizer at hypothesis generation and result analysis. ML roles are Innovator/Pragmatist/Contrarian and Optimist/Skeptic/Methodologist (pp. 4-5). HEP-ph substitutes domain roles (pp. 14-15).
- **Self-healing execution:** complexity scoring selects a code-generation cascade; AST/import/ablation checks run before execution. Docker execution uses dependency-install, data-acquisition, then network-disabled experiment phases. Failures produce targeted repairs and a Proceed/Refine/Pivot decision (p. 4, pp. 13-17).
- **Verifiable reporting:** a read-only numeric registry whitelists per-condition means, standard deviations, and seed values. Strict-section unmatched numbers reject the document; other unmatched claims become visible placeholders. Citation verification uses DOI/CrossRef, OpenAlex title matching, arXiv lookup, Semantic Scholar fallback, then an LLM relevance classification (p. 5).
- **HITL collaboration:** seven empirical modes are Full-Auto, Gate-Only, CoPilot, Thorough, Step-by-Step, Pre-Experiment, and Post-Experiment. CoPilot targets six high-leverage points; SmartPause is an additional uncertainty-driven routing mechanism (p. 5, Appendix E p. 20).
- **Cross-run evolution:** lessons are extracted not only from repairs, but also Pivot/Refine decisions, HITL feedback, and verification results. Each has category, severity, and mitigation; retrieval is time-decayed with default half-life 30 days (pp. 5-6, Appendix F p. 20).

### Domain and sandbox architecture

The system detects domain by forced override, keyword matching, or LLM classification, then selects a prompt bank and domain adapter (pp. 14-15). Native banks are ML and HEP-ph; profiles/adapters extend coverage to biology, chemistry, theoretical physics, economics, mathematics, and computational neuroscience (p. 15). The reported extension executes domain-specific agents in a Claude Code subprocess with pre-installed packages (pp. 7-8). The sandbox runs as a non-root host UID/GID container with resource limits, pre-cached datasets, AST security checks, forbidden-call/module checks, and a read-only evaluation harness (p. 17).

## Main empirical claims and stated limitations

- ARC-Bench is a 25-topic ML experiment-stage benchmark, plus a 20-topic scientific-domain extension (p. 6). The CoPilot strict score is 0.648 versus AI Scientist v2 0.419, reported as +54.7%; Full-Auto is 0.596 (pp. 6-7).
- The end-to-end HITL ablation covers 10 topics and seven modes. CoPilot reports mean quality 7.27 and 87.5% accept among valid outputs; Full-Auto reports 4.03 and 25.0%; Step-by-Step reports 5.19 and 50.0% (p. 7, p. 8).
- The component ablation uses three reruns per configuration-topic pair. Removing self-healing reduces completion from 10/10 to 6/10; removing verification raises apparent acceptance but manual audit finds fabricated values in 3 of 5 accepted papers (p. 9).
- The T10 case shows the numeric gate is necessary but insufficient: real logged all-zero values can still be scientifically uninformative (p. 10, Appendix G p. 21).
- The paper reports 11 of 13 invalid canonical HITL runs failing at paper drafting, with heterogeneous upstream causes, and calls for graceful degradation (p. 21). It also reports substantial export defects and only 4/5 step-by-step and 3/5 full-auto single-pass local compile rates in the audited deliverables (p. 22). These are material limitations to any “verified end-to-end paper” characterization.
- HITL experiments used scripted interventions, not live human participants; the authors explicitly identify this as a future-study limitation (p. 23). The benchmark judge is rubric-assisted and compares agent reviewers plus a human held-out subset, rather than constituting a live scientific peer-review study (pp. 19-20).

## Frozen supplementary description clause-by-clause comparison

Frozen clause: “A multi-domain research system using structured multi-agent debate.”

- **CONFIRMED.** The paper describes a multi-domain architecture with native ML/HEP-ph banks and profile/adapter support for additional domains (pp. 14-15), and structured K=3 debate at hypothesis and result stages (pp. 4-5).

Frozen clause: “A hypothesis stage (innovator, pragmatist, contrarian) and a results stage (optimist, skeptic, methodologist) produce and interpret hypotheses.”

- **CONFIRMED with scope note.** These are the ML-bank roles and the paper assigns them exactly as stated (p. 4). The result-stage panel assesses findings and synthesizes supported versus unsupported claims; it does not simply “interpret hypotheses” in the abstract. HEP-ph uses different domain roles (pp. 14-15).

Frozen clause: “a self-healing executor decides per run to proceed, refine, or pivot (regenerating the hypothesis), running in a sandbox.”

- **CONFIRMED, with one wording correction.** Proceed/Refine/Pivot is explicit (pp. 4-5, 14). Refine repairs the current direction; Pivot returns to hypothesis generation with a new direction (p. 4). Execution occurs in Docker with three-phase network isolation and a read-only metric harness (pp. 4, 17). “Regenerating the hypothesis” is accurate for Pivot but too broad for every decision and should be scoped to the Pivot path.

Frozen clause: “A hallucination-verification layer fact-checks numbers and citations.”

- **CONFIRMED but underspecified.** Numeric verification is registry-based and deterministic at document-check time; unmatched strict-section values reject the draft and non-strict claims become placeholders (p. 5). Citation verification is a four-layer resolver plus an LLM relevance classifier; hallucinated references are removed (p. 5). The paper itself cautions that this does not guarantee correct conclusions or submission-ready formatting (p. 22).

Frozen clause: “experiments use an external benchmark rather than wet-lab.”

- **PARTIALLY CONFIRMED / TOO NARROW.** ARC-Bench is central and the paper contains no wet-lab experiment (pp. 6-10). However, the paper also reports computational domain tasks using MadGraph/Pythia/Delphes/FeynRules/MadAnalysis5 and COBRApy/BiGG/optlang/GLPK, plus statistics tasks (pp. 7-8). “External benchmark” should be replaced with “computational benchmark and domain-specific software tasks; no wet-lab is reported.”

Frozen clause: “A cross-project failure memory turns past mistakes into guards.”

- **PARTIALLY CONFIRMED / MISFRAMED.** The persistent store is cross-run, not explicitly cross-project (pp. 5-6). It stores lessons from repair attempts, Pivot/Refine decisions, HITL gate feedback, and verification results, including successful-line lessons, each with category, severity, and mitigation. The paper says lessons become future safeguards, but the mechanism is natural-language prompt overlays with time decay, not only hard guards (p. 6). Recommended wording: “a persistent cross-run, time-decayed lesson store turns failures, decisions, feedback, and verification outcomes into future prompt guidance.”

Frozen clause: “a seven-level human-intervention mode (full-auto to step-by-step) is supported.”

- **REFUTED AS WRITTEN; CORRECTED TO CONFIRMED.** The paper supports **seven intervention modes**, not a single seven-level ordinal scale (p. 5; Appendix E p. 20). The modes are not presented as a strict monotonic ladder: CoPilot outperforms Step-by-Step, and Pre-/Post-Experiment isolate different locations of intervention (pp. 8-10). “Full-Auto to step-by-step” describes the endpoints, but omits Gate-Only, CoPilot, Thorough, Pre-Experiment, and Post-Experiment and wrongly implies a level ordering.

## Overall audit verdict

**Identity: CONFIRMED. Architecture: CONFIRMED. Frozen description: minor revision required.** The clause captures the paper's central mechanisms and the no-wet-lab computational setting, but it should use “seven intervention modes,” narrow Pivot's hypothesis regeneration to the Pivot branch, replace “cross-project failure memory” with the paper's broader cross-run lesson store, and state the domain-task extension rather than reducing all experiments to an external benchmark. The paper's own appendices also require retaining the caveat that numeric/citation verification does not establish scientific validity and that the reported HITL study used scripted interventions.

EVIDENCE_COMPLETE: yes
