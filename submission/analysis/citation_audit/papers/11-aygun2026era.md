# `aygun2026era` Full-Text Audit

## Source Identity

- **Citation key:** `aygun2026era`. The bibliography identifies *An AI system to help scientists write expert-level empirical software*, Nature (2026), DOI `10.1038/s41586-026-10658-6`, arXiv `2509.06503`.
- **PDF title:** *ERA - An AI System to Help Scientists Write Expert-Level Empirical Software*.
- **Authors:** Eser Aygün et al.; the title page lists Google DeepMind, Google Research, Google Platforms and Devices, MIT, Harvard, McGill, and Caltech affiliations (p. 1).
- **Identifier/version:** arXiv `2509.06503v2`, dated 15 May 2026; version status `exact` for the audited source.
- **Absolute PDF path:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/ERA - An AI System to Help Scientists Write Expert-Level Empirical Software.pdf`.
- **SHA-256:** `6a974d0c446c54653ffdf2765e75ab252e97aca3a201d930abacf91ec4d6a165`.
- **PDF extent:** 78 pages.
- **Scope restriction:** The three specified ERA evidence files and repository-local citation-manifest/bibliography context were used. No API/model call was made and no other PDF was opened.

## Full-Text Coverage

Pages **1-78** were read sequentially, including the abstract, introduction, Results, Discussion, related work, Methods, references, code-availability material, Extended Data, Supplementary Notes, Supplementary Figures, Supplementary Tables, prompts, and example code. Coverage includes the architecture and results on pp. 1-19, references on pp. 20-24, source declarations on p. 25, and supplementary/extended material on pp. 26-78. Coverage is complete.

## Problem and Context

ERA addresses the time and design-search bottleneck in scientific software. The source narrows the operational problem to **scorable tasks**: software is generated, executed in a sandbox, and evaluated by a measurable task metric or leaderboard (pp. 2-4, 13). Its context combines LLM code generation, tree search, AutoML/generative programming, empirical benchmarking, and prompt-mediated access to papers, textbooks, expert advice, Deep Research, and AI co-scientist outputs (pp. 2-3, 11-15).

The paper positions ERA against one-shot generation, best-of-N, genetic/generative programming, AutoML, LLM-plus-search systems, and broader science agents (pp. 11-12). It explicitly distinguishes high performance on predictive or computational objectives from genuine discovery requiring theory, causality, or mathematics (p. 12). This distinction is material for SERVO: benchmark optimization is evidence of computational performance, not automatic evidence of scientific novelty or physical validation.

## Structure and Argument

The paper moves from the scorable-task motivation and ERA schematic to Kaggle calibration, scRNA-seq batch integration, COVID hospitalization forecasting, GIFT-Eval forecasting, and additional geospatial, neural-activity, and numerical-integration tasks (pp. 1-10). Discussion and related work establish the empirical-software boundary and safety concerns (pp. 11-12). Methods then specify code mutation, flat global tree search, scoring, model comparison, recombination, prompts, datasets, splits, and compute budgets (pp. 13-19). Extended Data and supplementary material supply ablations, prompts, adherence checks, figures, tables, and generated code (pp. 26-78).

The argument establishes a code-level generate-execute-score-regenerate loop with historical branching and optional research-idea/recombination inputs. It does not establish a wet-lab stage, universal physical escalation capability, general scientific understanding, or robustness beyond the reported task objectives and benchmark conditions.

## Methods and Evidence

ERA receives a task description, metric, data/code, and optional research idea. An LLM writes or rewrites Python code; the candidate executes in a sandbox; score, logs, and node information are retained; a PUCT-inspired acquisition rule selects a node for further expansion; visits are backpropagated in a global flat tree (pp. 3, 13-14). The selection score uses rank-normalized empirical score plus exploration, with a flat prior and `c_puct = 1` tuned on Kaggle. This is closer to Flat UCB than recursive rollout-based MCTS, and code mutation is prompt-mediated rather than a syntax-level random mutation operator.

The evidence spans 16 Kaggle Playground competitions; OpenProblems v2.0.0 scRNA-seq holdouts totaling 1,747,937 cells; CovidHub forecasting over 52 jurisdictions, four horizons, and 23 quantiles; a fixed 2025-05-18 GIFT-Eval snapshot; DLRSD segmentation; ZAPBench neural activity prediction; and 38 oscillatory integrals split 19/19 train/holdout (pp. 3-10, 16-19, 35-38). Research ideas are injected through prompts, and recombination uses an LLM comparison of parent methods before a hybrid-strategy prompt. Human experts manually checked method adherence, recombination content, and some data preparation (pp. 5, 7, 17, 26, 34, 67-70).

For SERVO, the bounded mapping is: `S` is the supplied task/data/literature or method description; `G` is LLM code generation plus flat-tree search; `E` is sandbox execution; `V` is the task-specific score, held-out evaluation, logs, and manual checks; and `M` is score- and prompt-mediated branching/recombination. There is no physical experiment or general scientific peer-review feedback loop in the evaluated core workflow.

## Findings

- On the 16-task Kaggle development benchmark, ERA tree search outperformed single-call, Best-of-1000, and AIDE comparisons; the benchmark is a calibration task, not by itself a sophisticated scientific discovery test (pp. 3-4).
- In scRNA-seq, ERA beat corresponding published results for 8/9 replicated methods. BBKNN (TS) reported a 14% overall improvement over ComBat and matched or exceeded published BBKNN on every dataset and 11/13 metrics (pp. 4-6). Across 87 methods, 40 beat all methods then on the OpenProblems leaderboard, with failures and zero-scored metrics requiring interpretation (pp. 5-6, 16).
- In COVID forecasting, 14 strategies beat the official ensemble on the stated three-week held-out evaluation; 11/26 recombinations beat both parents. The explicit held-out-date comparison reports WIS 11.63 for the best recombination, 12.85 for the ensemble, and 14.39 for Google Retrospective (pp. 7-9; Supplementary Fig. S12, p. 49).
- On the fixed GIFT-Eval snapshot, the per-dataset solution scored MASE 0.671 versus 0.679 and 0.680 for named baselines; the unified solution scored 0.734 (p. 71). Lower MASE is better, and the source does not claim a current live-leaderboard result.
- Additional results include DLRSD mIoU 0.80-0.82, ZAPBench comparisons under different compute regimes, and 17/19 held-out oscillatory integrals solved within 3% (pp. 35-38, 53, 56, 73).
- With 128 nodes, ERA beat Best-of-N for all tested model/task combinations except GPT-5 batch integration (p. 15). This is a model/task-conditioned comparison, not universal superiority.

## Limitations

ERA optimizes the supplied metric, so benchmark and metric design determine what is rewarded. Search was tuned and selected under task-specific data, prompts, node budgets, and infrastructure; scRNA-seq search used 20,000-cell development data while larger holdouts exposed OOM/time failures that were not explicitly selected against (pp. 6, 16, 26). GIFT-Eval results are tied to the 2025-05-18 snapshot, and later benchmark changes make live comparisons unsound (p. 18).

The workflow is resource-intensive, with per-node costs ranging from 1.2 minutes/CPU for COVID to 192.2 minutes/GPU for ZAPBench; costs scale with explored nodes (p. 57). External model-generated ideas, summaries, embeddings, and prompt engineering contribute to several strongest results, so they do not isolate the tree-search algorithm. Manual adherence and data checks limit a claim of complete autonomy. DLRSD uses reported prior results, and ZAPBench comparator regimes differ. LLM behavior, model versions, datasets, leaderboards, and infrastructure reduce reproducibility. The source also warns that lowered technical barriers create safety risks (pp. 12, 18, 35-38, 57).

The “genuine discovery” discussion is conditional: the paper reports separate mathematical and in-silico neural-mechanism deployments, but those examples are not independently established by the benchmark tables in this PDF (p. 38). They must not be collapsed into the main benchmark verdict.

## Citation Assessments

### EN-C061: `submission/main.tex:230`

**Role:** direct; section “The Experiment Fidelity Gap.” The cited sentence claims that ERA optimizes within a fixed computational evaluator, generates expert-level empirical software, uses a held-out quality metric, and has no physical escalation.

- **Computational evaluator / optimization:** `SUPPORTED`, severity `none`. The source defines scorable tasks, sandbox execution, empirical scoring, and tree-search expansion (pp. 2-3, 13).
- **Fixed evaluator:** `SUPPORTED_WITH_QUALIFICATION`, severity `minor`. “Fixed” is accurate for each reported benchmark objective, but not a universal statement about every ERA deployment (pp. 2, 10, 13).
- **Expert-level empirical software:** `SUPPORTED`, severity `minor`. This is the paper's performance characterization and title framing, not proof of general scientific expertise or discovery (pp. 1-2, 10-12).
- **Held-out quality metric:** `SUPPORTED`, severity `none`. Separate validation/holdout evaluation is explicit for OpenProblems, GIFT-Eval, and DLRSD (pp. 5, 18, 35).
- **No physical escalation:** `SUPPORTED_WITH_QUALIFICATION`, severity `minor`. The evaluated tasks are computational and contain no physical stage, but the PDF does not establish a universal negative about ERA's capabilities outside the reported workflow (pp. 2-5, 12-13).

**Bounded citation verdict:** `PASS` (bounded). The citation supports the sentence when “fixed,” “held-out,” and “without physical escalation” are read within ERA's reported computational tasks. Recommended wording: “ERA likewise optimizes within a fixed computational evaluator in its reported tasks, generating expert-level empirical software judged on held-out quality metrics; the paper's evaluated workflow contains no physical-escalation stage~\\citep{aygun2026era}.”

### KO-C055: `submission/main_ko.tex:278`

The Korean occurrence preserves the same five claim units and citation. `고정된 계산 평가기` corresponds to fixed computational evaluator, `물리적 승격` to physical escalation, and `별도로 유보된 품질 지표` is understandable but less exact than `홀드아웃 품질 지표`. Verdict: `PASS` (bounded), severity `minor` terminology note. Recommended parity wording narrows scope identically: “ERA도 마찬가지로 보고된 과제에서는 고정된 계산 평가기 안에서 최적화하여 홀드아웃 품질 지표로 평가되는 전문가 수준의 경험적 소프트웨어를 생성하며, 논문이 평가한 워크플로에는 물리적 승격 단계가 없다~\\citep{aygun2026era}.”

## Korean Parity

EN-C061 and KO-C055 are **equivalent** in claim structure and citation placement. Neither language adds a quantitative claim or omits a material qualifier. The only parity issue is terminology: Korean `별도로 유보된 품질 지표` should preferably be `홀드아웃 품질 지표`. Both versions should bound the physical-escalation statement to the reported/evaluated workflow. Overall parity: **PASS with a terminology note**.

## Overall Verdict

**`minor_revision` for the frozen description; citation status `PASS, bounded`.** The source identity and 78-page coverage are exact and complete. EN-C061 and KO-C055 are adequately supported when scoped to the reported computational workflow. The frozen supplementary description is substantially faithful, but “flat-UCB global search tree” should be qualified as PUCT-inspired/Flat-UCB-like, “beating the best human methods” should be limited to named benchmark/leaderboard comparisons, and “computational only” should remain explicit. No citation-invalidating defect is present.

## Completion Checklist

- [x] Citation key, bibliography metadata, title, authors, identifier, version, absolute PDF path, SHA-256, and page count recorded.
- [x] Pages 1-78 covered in order, including references, methods, Extended Data, prompts, and supplementary material.
- [x] Research problem, historical/disciplinary context, prior work, structure, methods, findings, limitations, and SERVO implications assessed.
- [x] Frozen supplementary description assessed clause by clause with verdict, severity, and scope correction.
- [x] EN-C061 occurrence assessed with claim-unit reasoning and bounded PASS.
- [x] KO-C055 occurrence assessed with claim-unit reasoning and bounded PASS.
- [x] English/Korean parity assessed as equivalent with a terminology note.
- [x] Quantitative values, denominators, metrics, conditions, and benchmark limitations recorded where available.
- [x] No API/model call made and no other PDF opened.
- [x] System description assessed against the full source.

AUDIT_COMPLETE: yes
PAGES_COVERED: 1-78
EN_LINKS_COVERED: EN-C061:aygun2026era
KO_LINKS_COVERED: KO-C055:aygun2026era
SYSTEM_DESCRIPTION_ASSESSED: yes
VERDICT: minor_revision
