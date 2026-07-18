# ERA: citation and parity audit

## Audit scope

- Single source opened: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/ERA - An AI System to Help Scientists Write Expert-Level Empirical Software.pdf`
- PDF metadata: 78 pages.
- SHA-256: `6a974d0c446c54653ffdf2765e75ab252e97aca3a201d930abacf91ec4d6a165`
- The PDF was read page-by-page from page 1 through page 78, including the main text, references, extended-data material, supplementary notes, supplementary figures, and supplementary tables. No other PDF was opened. No API or model call was made.

## Manuscript occurrences

### EN-C061

Source: `submission/main.tex:230`, section `The Experiment Fidelity Gap`.

> ERA likewise optimizes within a fixed computational evaluator, generating expert-level empirical software judged by a held-out quality metric without physical escalation~\citep{aygun2026era}.

Claim units:

1. ERA optimizes within a computational evaluator.
2. The evaluator is fixed for the cited comparison.
3. The output is expert-level empirical software.
4. The quality judgment uses held-out data/metrics.
5. The cited ERA work does not perform a physical escalation in the evaluated workflow.

### KO-C055

Source: `submission/main_ko.tex:278`, section `실험 충실도 격차`.

> ERA도 마찬가지로 고정된 계산 평가기 안에서 최적화하여, 물리적 승격 없이 별도로 유보된 품질 지표로 판정되는 전문가 수준의 경험적 소프트웨어를 생성한다~\citep{aygun2026era}.

The Korean occurrence preserves the same five claim units. `물리적 승격` corresponds to physical escalation, and `고정된 계산 평가기` corresponds to fixed computational evaluator. The phrase `별도로 유보된 품질 지표` is understandable, but `홀드아웃 품질 지표` would be a more exact technical rendering of `held-out quality metric`.

## ERA evidence

| Claim | Direct PDF evidence | Assessment |
|---|---|---|
| Computational evaluator and optimization | p. 2 defines ERA as an AI system that creates software for `scorable tasks`; p. 3 describes code being executed and scored in a sandbox; p. 13 says generated code is executed and assigned an empirical score, with tree search selecting the next candidate. | **Supported.** |
| Fixed evaluator/task objective | p. 2 defines the task as maximizing a measurable quality score; p. 10 says scientific software creation is converted into a search for a program whose output maximizes a quality score; p. 13 says the implementation was chosen for optimal performance on the Kaggle benchmark. | **Supported with scope limitation.** “Fixed” is accurate for each reported benchmark/evaluation objective, not a claim that every possible ERA deployment has one immutable evaluator. |
| Expert-level empirical software | The title uses “expert-level empirical software”; p. 2 says ERA produces software outperforming the state of the art on scorable tasks; p. 10 reports expert-level performance on three additional domains; p. 11 reports expert-level performance on public leaderboards and academic literature across fields. | **Supported as the paper's performance characterization.** It should not be read as proof of general scientific expertise or genuine discovery. |
| Held-out quality metric | p. 5 states that ERA is optimized on a separate dataset and the selected solution is reported on holdout OpenProblems datasets; p. 18 states that the GIFT-Eval solution is evaluated on the held-out test set; p. 35 reports an explicitly held-out test set for geospatial segmentation. | **Supported.** The wording is technically precise when “held-out” refers to the relevant benchmark split. |
| No physical escalation in the evaluated workflow | The paper lists computational/scorable tasks and describes sandbox execution (pp. 2-5, 13). p. 12 explicitly distinguishes optimizing empirical predictive models from genuine scientific discovery and says the evaluated core problems emphasize empirical software engineering. | **Supported only as a bounded inference.** The cited paper does not state a universal negative that ERA can never escalate physically. The manuscript should scope this to “the evaluated ERA workflow” or “the paper's reported computational tasks.” |

## Citation-range review

The citation is placed after the ERA sentence and is reasonably read as supporting the complete ERA-specific clause. The source directly supports the evaluator, empirical score, held-out evaluation, and the computational nature of the reported tasks. It does not independently support the stronger universal formulation that ERA has no physical escalation capability in all settings. That part is an inference from the paper's reported scope and must remain explicitly bounded.

Recommended English wording if a strict source-bounded formulation is required:

> ERA likewise optimizes within a fixed computational evaluator in its reported tasks, generating expert-level empirical software judged on held-out quality metrics; the paper's evaluated workflow contains no physical-escalation stage~\citep{aygun2026era}.

Recommended Korean parity wording:

> ERA도 마찬가지로 보고된 과제에서는 고정된 계산 평가기 안에서 최적화하여 홀드아웃 품질 지표로 평가되는 전문가 수준의 경험적 소프트웨어를 생성하며, 논문이 평가한 워크플로에는 물리적 승격 단계가 없다~\citep{aygun2026era}.

## EN/KO parity verdict

**PASS with a terminology note.** EN-C061 and KO-C055 assert the same relationship and attach the same citation. There is no material translation omission or added quantitative claim. The only recommended correction is replacing `별도로 유보된 품질 지표` with `홀드아웃 품질 지표` and, for maximum source fidelity, narrowing the physical-escalation assertion to the reported/evaluated workflow in both languages.

## Final verdict

**Citation status: PASS, bounded.** The citation is adequate for the sentence when “fixed computational evaluator,” “held-out quality metric,” and “without physical escalation” are understood within ERA's reported computational experiments. **Overclaim risk: medium** if the sentence is read as a universal claim about ERA beyond this paper. The source-bounded wording above removes that risk.

EVIDENCE_COMPLETE: yes
