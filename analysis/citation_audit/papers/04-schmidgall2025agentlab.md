# `schmidgall2025agentlab` 전문 인용 감사

## Source Identity

- **Citation key:** `schmidgall2025agentlab`
- **BibTeX:** Samuel Schmidgall, Yusheng Su, Ze Wang, Ximeng Sun, Jialian Wu, Xiaodong Yu, Jiang Liu, Michael Moor, Zicheng Liu, Emad Barsoum, "Agent Laboratory: Using LLM Agents as Research Assistants," arXiv preprint `arXiv:2501.04227` (2025).
- **PDF 자체 표제와 저자:** 표제와 10인 저자 목록이 BibTeX와 일치한다(PDF p.1).
- **Stable identifier:** `arXiv:2501.04227v2 [cs.HC]`, 2025-06-17 제출본. 표제면에는 2025-06-18 날짜도 인쇄되어 있다(PDF p.1).
- **절대 PDF 경로:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/Agent Laboratory - Using LLM Agents as Research Assistants.pdf`
- **SHA-256:** `67b9543ae1d8e3ad86a65e2a436ddbd12700d7c8f4a66c5b4c2a6fccc1674d75`
- **`pdfinfo`:** 84 pages, A4 595.276 x 841.89 pt, PDF 1.5, 3,644,380 bytes, not encrypted.
- **Version status:** `exact`. PDF의 제목, 저자, arXiv 식별자, 연도가 `references.bib`와 manifest에 일치한다. PDF는 84쪽 전체가 포함된 v2이며, 본문, 참고문헌, configuration, prompts, 세 종류의 survey instrument를 포함한다.

## Full-Text Coverage

로컬 PDF p.1부터 p.84까지 page break를 유지한 layout-preserving text로 순서대로 읽었다. 본문 쪽 번호와 PDF 쪽 번호가 일치한다. 다음 범위를 빠짐없이 확인했다.

| PDF 페이지 | 순차 독해 내용 |
|---|---|
| 1 | 표제, 초록, Figure 1, human-provided idea와 전체 pipeline 개요 |
| 2-4 | 문제의식, 기여, LLM agent, AutoML, AI discovery, autonomous-research 선행연구 |
| 5-10 | Figure 2-4와 literature review, plan, data preparation, `mle-solver`, result interpretation, `paper-solver`, automated review, report refinement, autonomous/co-pilot mode |
| 11-18 | 15개 autonomous paper에 대한 human evaluation, Figure 5-8, automated-versus-human review, co-pilot study, runtime와 cost |
| 18-19 | Figure 9와 10개 low-complexity MLE-Bench task의 `mle-solver` 비교 |
| 19-22 | workflow와 self-evaluation 한계, failure modes, ethics, discussion, conclusion |
| 22-30 | 참고문헌 전체 |
| 31 | Table 1 hyperparameters와 hardware |
| 32-40 | base/context prompts, agent phase descriptions, commands, role prompts |
| 41-50 | `mle-solver` tools, reward/repair/reflection prompts, `paper-solver` prompts와 section tips |
| 51-56 | NeurIPS-style reviewer form와 paper-review prompt |
| 57-64 | autonomous-mode generated-report grading survey 전체 |
| 65-74 | preselected-topic co-pilot survey 전체 |
| 75-84 | custom-topic co-pilot survey 전체 |

PDF pp.1, 5, 7, 8, 11, 13, 15, 17, 18, 31을 160 dpi PNG로 렌더링해 시각 확인했다. Figure 1-4에서 인간 입력, 세 phase, LLM reward loop, compiler와 report-review 경로를 확인했고, Figure 5-9에서 평가 표본과 모든 핵심 수치를 확인했다. PDF p.31의 Table 1에서는 paper writing reviewer 1개, paper refinement reviewer 3개와 solver hyperparameter를 확인했다. 텍스트 추출과 렌더링 사이에 판정을 바꾸는 layout 불일치는 없었다.

PDF pp.9-10에는 생성 paper에 대한 o1-mini review 예시가 포함되어 있다. PDF pp.57-84는 생성 보고서 자체가 아니라 설문지이며, p.57은 한 생성 보고서를 외부 Google Drive 링크로만 가리킨다. 현재 감사 대상 claim과 frozen description은 본 PDF의 architecture, aggregate evaluation, prompts로 판정 가능하므로 외부 보고서를 열지 않았다.

## Problem and Context

논문의 출발점은 연구자가 시간과 자원의 제약 때문에 많은 연구 아이디어를 시험하지 못한다는 문제다(PDF p.2). 저자들은 연구 아이디어를 스스로 고르는 완전 대체형 scientist보다, 사람이 창의적 아이디어와 방향을 담당하고 LLM agent가 문헌 탐색, 계획, 계산 실험, 결과 해석, 보고서 작성을 수행하는 research assistant를 목표로 한다(PDF pp.1-3, 21-22).

이 위치 설정은 이 source를 다른 autonomous-science 논문과 구분한다. 선행 연구의 The AI Scientist와 ResearchAgent는 idea generation까지 자동화하지만, Agent Laboratory는 인간이 제공한 연구 아이디어를 명시적 입력으로 받는다(PDF pp.2, 4-5). 저자들은 LLM ideation의 feasibility, implementation detail, homogenization 한계를 근거로 human-guided ideation이 현재 더 적절하다고 본다(PDF pp.2, 4). 따라서 이 논문에서 `autonomous`는 아이디어가 주어진 뒤의 계산 workflow를 뜻하며, 연구 문제의 독립적 생성까지 포함하지 않는다.

범위도 machine-learning research와 computational experiment에 한정된다. 물리적 실험, wet-lab execution, 독립적인 과학적 novelty certification은 구현하거나 평가하지 않는다. 다만 자동 code execution과 report refinement를 실제로 연결하므로, 단순한 문서 작성 도구보다 넓은 human-initiated research pipeline이다.

## Structure and Argument

논증은 다음 순서로 진행된다.

1. PDF pp.1-3은 연구 아이디어 병목과 human-centered assistant라는 목표를 제시하고, 세 phase와 기여를 요약한다.
2. PDF pp.3-5는 LLM agents, AutoML, AI discovery, research-task automation, autonomous research를 선행 맥락으로 정리한다.
3. PDF pp.5-10은 literature review, experiment planning, data preparation, iterative code search, results interpretation, paper generation과 reviewer-driven refinement를 설명한다.
4. PDF pp.10-14는 5개 topic x 3개 backend의 15개 autonomous output을 인간과 자동 reviewer가 평가한 결과를 제시한다. `+2.3` 격차는 이 부분의 직접 결과다.
5. PDF pp.14-16은 co-pilot mode의 사용성, self-evaluation, external evaluation과 autonomous mode 비교를 제시한다.
6. PDF pp.16-19는 비용, 시간, subtask success와 별도 MLE-Bench 실험을 보고한다.
7. PDF pp.19-22는 hallucination, self-evaluation, repository control, safety 등 한계를 인정하고 human-centered tool이라는 결론으로 돌아간다.
8. PDF pp.31-56은 구현 prompt와 hyperparameter를 공개해 본문의 architecture를 구체화하고, pp.57-84는 평가 설문 문항을 공개한다.

이 논문의 architecture claim, generated-output quality claim, tool-usefulness claim은 분리해야 한다. Pipeline이 code와 report를 생성한다는 사실은 구현 설명과 산출물 평가로 지지된다. 반면 generated research가 top-conference 수준이거나 novelty를 신뢰성 있게 판정한다는 주장은 지지되지 않으며, 저자들도 human score가 acceptance 평균보다 낮고 자동 reviewer가 과대평가한다고 보고한다(PDF pp.12-14, 19-22).

## Methods and Evidence

### Human input와 두 운용 mode

- 모든 run은 인간이 제공한 research idea와 notes에서 시작한다(PDF pp.1-2, Figure 1).
- **Autonomous mode:** 초기 idea 이후에는 인간이 개입하지 않고 subtask가 순차 진행된다(PDF p.10). 따라서 execution은 자동이지만 hypothesis-space entry는 인간이 정한다.
- **Co-pilot mode:** 각 subtask 끝에서 인간이 결과를 검토하고, 다음 단계 진행 또는 high-level notes를 붙인 동일 subtask 재실행을 선택한다(PDF p.10). `ongoing direction`은 이 mode의 선택적 기능이지 모든 run의 필수 조건이 아니다.

### Literature review와 plan

PhD agent가 arXiv API에서 query별 상위 20개 abstract를 받고, 필요한 논문의 full text를 읽은 후 review에 추가한다(PDF pp.5-6, 36-37). Appendix configuration은 최종 paper summary 수를 5개로 둔다(PDF p.31). 이후 PhD와 Postdoc agents가 model, dataset, experiment step을 포함한 plan에 합의한다(PDF p.6).

이 단계는 관련 문헌을 찾고 인간 아이디어를 구체화하지만, 후보 연구 아이디어를 독립 생성하고 field novelty를 판정하는 전용 gate는 아니다. Paper-writing reviewer에는 `Originality` 1-4 항목이 있으나(PDF pp.9-10, 51-55), 이것을 오염 통제된 novelty detector로 검증하지 않는다.

### Computational experiment loop

Data preparation은 Python execution, HuggingFace dataset search, compile check를 사용한다(PDF p.6). `mle-solver`는 기존 top program을 `EDIT` 또는 `REPLACE`하고, 실행 오류를 repair한 뒤, 성공한 code를 score하고, error 또는 결과에 대한 self-reflection을 다음 iteration에 전달한다(PDF pp.6-7, 41-45).

기본 full-pipeline score는 관측 metric 그 자체가 아니다. Professor LLM reward model이 research plan, generated code, printed output의 정합성을 0-1로 평가하고 그 점수로 top-program pool을 갱신한다(PDF pp.6-7, 42). 따라서 experiment result는 다음 code 선택에 피드백되지만, 그 gate는 self-evaluated semantic proxy다. 별도의 MLE-Bench 실험에서만 이 LLM scorer를 20% dev-set task metric으로 대체한다(PDF p.18).

Main text는 compile 실패 repair를 `N_rep=3`으로 적고 Figure 3도 `code repair (x3)`로 표시하지만(PDF pp.6-7), Appendix Table 1은 `Code repair attempts = 2`라고 적는다(PDF p.31). 이것이 initial attempt 뒤 2회 retry를 뜻하는지 configuration drift인지는 설명하지 않아 exact repair count를 확정할 수 없다.

### Report writing와 automated review

`paper-solver`는 8개 section scaffold를 만들고, arXiv search, line edit, LaTeX compilation을 거쳐 report를 작성한다(PDF pp.8-9, 45-50). Paper writing 중에는 Appendix Table 1상 reviewer 1개를 사용하고, final report refinement에는 reviewer 3개를 사용한다(PDF pp.10, 31). PhD agent는 reviewer feedback에 따라 finalize하거나 planning, experimentation, result interpretation으로 돌아갈 수 있다(PDF p.10). 즉 reviewer 외에도 compile/runtime checks, program reward, LaTeX compilation이 자동 gate로 작동한다.

Reviewer는 Lu et al.의 NeurIPS-style form을 가져와 originality, quality, clarity, significance, soundness, presentation, contribution, overall과 decision을 출력한다(PDF pp.9-10, 50-56). PDF pp.9-10의 한 예시는 `Overall=7`, `Accept`를 주면서도 originality enhancement를 weakness로 적는다. 이는 output 예시이지 reviewer calibration 증거는 아니다.

PDF p.9의 `65%` automated accuracy 대 `66%` human accuracy와 F1 `0.57` 대 `0.49`는 Lu et al.에서 가져온 inherited-reviewer claim이다. Agent Laboratory가 이 PDF에서 동일 model, prompt, calibration threshold로 그 benchmark를 재실행한 결과가 아니다. 이 source가 직접 수행한 reviewer 검증은 아래 15개 generated-report human comparison이다.

### Evaluation design

- **Autonomous outputs:** 5개 topic과 3개 backend로 15편을 생성했다. 10명의 volunteer PhD students가 각자 무작위 3편을 읽어 총 30 review assignments를 만들고 experiment quality, report quality, usefulness와 NeurIPS-style 항목을 평가했다(PDF pp.10-13, 57-64). 각 paper에 정확히 2개 review가 균형 배정됐는지는 명시하지 않는다.
- **Automated-human comparison:** 동일 output군의 automated score와 human score 평균을 비교한다. Overall은 6.1/10 대 3.8/10이며, criterion별 격차도 Figure 6에 제시된다(PDF pp.12-14).
- **Co-pilot:** 참여자가 preselected topic과 custom topic을 각각 수행하고 self-evaluation과 external evaluation을 받았다(PDF pp.14-16, 65-84). 모든 phase는 o1-mini를 썼지만 literature-review backend는 별도로 식별하지 않는다. 본문은 co-pilot participant와 external evaluator의 정확한 수도 명시하지 않는다.
- **Runtime/cost:** 2023 MacBook Pro M3 Max, 36 GB 환경에서 phase별 time, model inference cost, average subtask success를 측정했다(PDF pp.16-18, 31). Token count, pricing date, local hardware/electricity, human labor와 failed-run cost는 포함하지 않는다.
- **MLE-Bench:** low-complexity text/tabular 10개 task만 사용하고, Kaggle notebook distilled knowledge와 80/20 train/dev split을 제공했다. 비교 방법의 invalid submission은 valid-score 평균에서 제외했다. MLAB와 OpenHands는 gpt-4o, AIDE는 o1-preview를 쓰지만 `mle-solver` backend, run count, seed, variance는 밝히지 않는다(PDF pp.18-19).

## Findings

### 직접 보고된 결과

- Autonomous mode에서 human-rated experiment/report/usefulness 평균은 gpt-4o `2.6/3.0/4.0`, o1-mini `3.2/3.2/4.3`, o1-preview `2.9/3.4/4.4`다(각 5점 척도, PDF pp.11-12, Figure 5).
- Human NeurIPS-style overall은 gpt-4o `3.5`, o1-mini `3.8`, o1-preview `4.0`으로, 세 backend 평균이 `3.8/10`이다(PDF pp.12-13).
- Automated reviewer 평균은 `6.1/10`, human reviewer 평균은 `3.8/10`으로 정확히 `+2.3` points 높다(PDF pp.12-14, Figure 6). 이 값은 **이 Agent Laboratory PDF가 직접 보고한 결과**다. Backend별 차이는 gpt-4o `6.2-3.5=+2.7`, o1-mini `6.0-3.8=+2.2`, o1-preview `5.9-4.0=+1.9`다.
- 격차는 clarity `3.6/4` 대 `2.4/4`, contribution `2.9/4` 대 `2.1/4` 등 모든 표 항목에서 같은 방향이다(PDF pp.13-14). 그러나 논문은 이 평균 차이에 대한 confidence interval, paired significance test, inter-rater reliability를 제시하지 않는다.
- 단순한 additive offset만 있는 것도 아니다. Automated reviewer는 gpt-4o를 overall 최고, o1-preview를 최저로 두지만 human reviewer 순위는 정확히 반대다(PDF p.13). Source의 `not predictive` 표현은 이 기술적 패턴과 부합하지만 correlation coefficient나 per-paper paired analysis는 없다.
- Co-pilot paper의 external overall은 `4.38/10`으로 autonomous human overall `3.8/10`보다 `+0.58` 높다. 반면 significance는 `-0.05`, contribution은 `+0.03`에 그쳤다(PDF pp.15-16, Figure 7). 따라서 human involvement가 presentation과 quality 일부를 높였다는 근거는 있으나 novelty 또는 scientific contribution을 유의하게 높였다고 볼 수 없다.
- Co-pilot practical ratings는 utility `3.5/5`, continuation `3.75/5`, satisfaction `3.63/5`, usability `4.0/5`다(PDF pp.14-15). 그러나 o1-mini autonomous 결과와 비교하면 co-pilot experiment quality, report quality, usefulness는 각각 `-0.82`, `-0.07`, `-0.55` 낮았다(PDF p.15).
- gpt-4o workflow의 평균 model inference cost는 `$2.33`, time은 `1165.4 s`, displayed average subtask success는 `94.3%`다(PDF pp.17-18). `$2.33`은 비교 대상 약 `$15`보다 `84.47%` 낮아 84% claim은 산술상 맞지만 total research cost 절감이 아니다. `3616.8/1165.4=3.10`이므로 o1-mini보다 `3.2x` 빠르다는 prose는 느슨하게 과대 반올림됐다. o1-preview 대비 `5.32x`는 보고된 `5.3x`와 맞는다.
- Figure 8의 literature-review `60/70/80%`는 success rate인데 prose는 이를 `high rate of failure`라고 잘못 부른다. 실제 failure rate라면 `40/30/20%`다. `94.3/92.8/95.7%`도 7개 phase percentage의 산술 평균이지 complete seven-stage run의 성공 확률이 아니다(PDF pp.17-18).
- MLE-Bench subset에서 `mle-solver`는 10개 모두 2시간 안에 valid submission을 내고 4개 medal을 얻었다. Figure 9는 6/10을 human median 이상으로 표시하지만 English text normalization은 displayed median `0.990`과 동률이므로 엄밀히는 `at or above median`이다(PDF pp.18-19). 이는 제한된 subset, enriched inputs와 별도 dev-metric scorer 조건의 결과다.
- Figure 9의 check marks와 수치를 세면 AIDE도 6개 task에서 human median을 넘지만 prose는 5/10이라고 적는다(PDF pp.18-19). 따라서 competitor count에도 source 내부 불일치가 있다.

### `+2.3`의 정확한 해석

`+2.3`은 일반 인간 전문가 대비 모든 scientific reviewing task에서의 보편적 calibration error가 아니다. 15개 Agent Laboratory autonomous-mode output, 세 backend, 10명 volunteer PhD student의 NeurIPS-style overall score 평균과 system의 automated self-review 평균 차이다(PDF pp.11-14). Source는 반복되는 과대평가 방향을 보여 주지만 통계적 calibration curve나 독립 학술지 표본을 제시하지 않는다. 따라서 `systematic over-estimation`은 이 평가군에 한정해 사용해야 한다.

### SERVO 관련 해석

다음은 source 저자의 용어가 아니라 현재 감사의 framework mapping이다.

- **G/H:** 연구 아이디어는 인간이 공급한다. Autonomous mode도 초기 G를 자동화하지 않으며, co-pilot에서는 인간이 subtask 진행과 재실행을 결정한다(PDF pp.1-2, 10). 따라서 `independently generate hypotheses`로 분류하면 안 된다.
- **E:** computational code generation-execution-reflection loop는 실제 architecture에 존재한다(PDF pp.6-7). 물리적 experiment executor는 없다.
- **V:** Python compile/runtime checks, LLM program reward, LaTeX compilation, NeurIPS-style LLM reviewer가 함께 존재한다(PDF pp.6-10, 31, 41-56). Reviewer만이 유일한 자동 품질 check는 아니다. 다만 scientific acceptance에 가장 가까운 semantic gate는 biased self-reviewer다.
- **pi:** outer workflow는 고정 sequential schedule이며 human co-pilot이 stage transition을 통제한다. 내부 `mle-solver`는 top-program sampling과 LLM score를 이용한 heuristic search를 한다. 실험 데이터를 이용한 Bayesian posterior나 EIG policy는 없다.
- **M:** code, outputs, error history, reflections, previous experiment/report, top programs를 run 안에서 전달한다(PDF pp.7, 31-45). Cross-project semantic memory나 validated novelty archive는 보고하지 않는다.
- **Closure:** 인간이 idea를 준 이후 report까지의 computational workflow에는 내부 feedback loop가 있다. 하지만 autonomous idea generation과 validated novelty gate가 없으므로, discovery 전체를 독립적으로 닫았다고 부르는 것은 부적절하다. `partial`이라는 coding은 이 경계를 명시할 때만 타당하다.

## Limitations

### Source가 명시한 한계

- 자동 reviewer가 human score를 예측하지 못하고 generated work를 과대평가한다(PDF pp.12-14, 19).
- `paper-solver` output은 인간 논문 작성을 대체하는 final paper가 아니라, 인간이 확장하고 다시 쓸 foundation report다(PDF pp.8, 19).
- Fixed paper structure, figure 2개 제한, repository-level code management 부재가 있다(PDF pp.19-20).
- 일부 generated reports는 실행하지 않은 hyperparameter와 result를 hallucinate했다(PDF p.20).
- Literature search 반복 실패, token overflow, 0% experiment accuracy, host `subprocess.run`, unintended `exit()` 등 concrete failure mode가 있다(PDF p.20).
- 대량 저품질 논문, bias, 악용, 안전과 governance 위험을 인정한다(PDF pp.20-21).

### 현재 인용 감사에서 확인한 validity threats

- 10명 volunteer PhD student와 15편이라는 작은 표본이며, 각 paper의 reviewer 수 분포, inter-rater reliability, uncertainty, paired significance가 보고되지 않는다(PDF pp.11-14).
- `significantly improves`라는 초록 표현과 달리 co-pilot improvement에 inferential significance test가 없다. 일부 quality 지표는 autonomous o1-mini보다 낮고 significance/contribution 개선은 거의 없다(PDF pp.14-16).
- Co-pilot participant와 external evaluator 수를 본문과 survey appendix에서 명시하지 않아 분모를 독립적으로 복원할 수 없다.
- Automated review 비교는 system 자신의 generated reports에 한정되며, novelty discrimination을 직접 평가하지 않는다. `Originality` score field의 존재는 novelty certification의 validation이 아니다.
- `mle-solver` full-pipeline search는 LLM reward score를 최적화하고, MLE-Bench만 dev metric을 쓴다. 두 조건을 하나의 empirical-validator 성능으로 합치면 안 된다(PDF pp.6-7, 18-19).
- MLE-Bench는 10개 low-complexity subset, distilled notebook knowledge, method별 다른 backend, invalid-submission 제외 평균을 사용한다. 일반적인 SOTA 주장을 뒷받침하기에는 범위가 좁다(PDF pp.18-19).
- Main text의 repair attempts 3회와 Appendix의 2회가 불일치한다(PDF pp.6, 31).
- `mle-solver` prompt는 at least two figures를 요구하지만 source limitation은 only two figures로 제한된다고 적어 minimum과 hard cap의 관계가 불명확하다(PDF pp.19, 43).
- Figure 8은 literature-review success `60/70/80%`를 제시하지만 prose는 같은 수치를 failure rate로 부르며, `Entire Workflow` percentage는 phase 평균이라 end-to-end reliability로 읽을 수 없다(PDF pp.17-18).
- Figure 9는 AIDE의 above-median task를 6개로 표시하지만 prose는 5개라고 적는다. `mle-solver`의 model backend, run count, seeds와 score uncertainty도 없다(PDF pp.18-19).
- Automated report review가 planning, experiment, interpretation으로 돌아갈 수 있다는 architecture는 제시되지만 실제 backward jump 횟수, 사용 빈도, stopping/convergence rule, outcome ablation은 보고하지 않는다(PDF pp.10, 31). 가능한 outer loop와 실증된 loop benefit을 분리해야 한다.
- 생성 보고서 본문은 PDF에 포함되지 않고 p.57에서 외부 링크로만 제공된다. 현재 평가는 source가 보고한 aggregate result와 공개 prompt를 검증한 것이며, 15개 산출물의 사실 정확성을 재감사한 것은 아니다.

## Citation Assessments

### `EN-C001:schmidgall2025agentlab`

- **Manuscript:** `submission/main.tex:69`, Introduction.
- **Claim:** AI Scientist systems는 가설을 독립 생성하고 실험을 실행하며 지식을 합성하는 agent이고, 빠르게 증가했지만 공통 형식 어휘가 없다는 grouped claim.
- **Citation role:** `joint` background/example. 여섯 key 중 Agent Laboratory의 몫을 독립 평가한다.
- **PDF evidence:** Agent Laboratory는 literature review, computational experiment, report synthesis를 연결하지만, research idea는 사람이 제공한다(PDF pp.1-2, 5-10). 논문은 자체 system을 설명할 뿐 field-wide proliferation이나 shared-vocabulary 부재를 조사하지 않는다.
- **Verdict:** `CONTRADICTED`; severity `major`. 별도로, broad proliferation과 vocabulary-absence synthesis는 `joint-only`이며 이 source 단독으로는 확립되지 않는다.
- **Reasoning:** 이 occurrence의 appositive는 느슨한 capability 목록이 아니라 cited class의 정의다. Agent Laboratory는 experiment/report capability는 갖지만, grouped 정의의 `independently generate hypotheses`는 source가 명시한 human-provided idea와 정면으로 충돌한다. 다른 key와의 joint citation도 이 source 자체의 잘못된 class membership을 구제하지 못한다. 한 source의 침묵으로 field-wide vocabulary absence를 증명할 수도 없다.
- **Proposed correction:** `AI Scientist and AI research-assistant systems - some generating ideas autonomously and others, such as Agent Laboratory, starting from a human-provided idea - increasingly connect literature work, experiments, and synthesis; our review finds no shared formal vocabulary.`
- **Korean parity:** `equivalent` with `KO-C001:schmidgall2025agentlab`; 같은 autonomy 과장과 field-level attribution 문제가 보존된다.

### `EN-C013:schmidgall2025agentlab`

- **Manuscript:** `submission/main.tex:90`, Related Work.
- **Claim:** 네 선행 연구는 개별 system의 qualitative characterization을 제공하지만 cross-system comparison의 shared framework는 제공하지 않는다.
- **Citation role:** `joint` background.
- **PDF evidence:** Source는 architecture, prompts와 qualitative discussion뿐 아니라 human scores, runtime, cost, MLE-Bench 수치를 함께 제공한다(PDF pp.1-22, 31-84). 자체 cross-system formal taxonomy는 제안하지 않는다.
- **Verdict:** `PARTIAL`; severity `minor`; shared-framework absence는 manuscript synthesis.
- **Reasoning:** Agent Laboratory가 개별 system study라는 점은 맞지만 `qualitative`만으로 부르면 정량 평가를 누락한다. 또한 이 논문이 shared framework를 제안하지 않는다는 사실은 literature 전체에 그런 framework가 없다는 증거가 아니다.
- **Proposed correction:** `Prior work provides individual system descriptions and evaluations; in our literature review, these works do not supply a shared cross-system framework.`
- **Korean parity:** `equivalent` with `KO-C008:schmidgall2025agentlab`.

### `KO-C001:schmidgall2025agentlab`

- **Manuscript:** `submission/main_ko.tex:88`, 서론.
- **Claim:** AI 과학자 system이 가설을 독립 생성하고 실험·지식 합성을 수행하며 급속히 증가했지만 공통 형식 어휘가 없다는 grouped claim.
- **Citation role:** `joint` background/example.
- **PDF evidence:** 인간이 research idea를 제공하고, autonomous mode는 그 이후 단계만 자동화한다(PDF pp.1-2, 10). Field-wide 증가와 어휘 부재는 source의 연구 질문이 아니다.
- **Verdict:** `CONTRADICTED`; severity `major`. 별도로, broad field claim은 `joint-only`다.
- **Reasoning:** `EN-C001`과 동일하다. `독립적으로 생성`은 class-definition clause이며, Agent Laboratory를 이 class에 포함하는 것은 source의 핵심 positioning과 정면으로 충돌한다. 다른 cited system이 독립 ideation을 지원하더라도 이 key의 entailment는 회복되지 않는다.
- **Proposed correction:** `독립적으로 아이디어를 생성하는 시스템과 Agent Laboratory처럼 인간이 제공한 아이디어에서 시작하는 연구 보조 시스템이 문헌·계산 실험·종합 단계를 연결하고 있으며, 본 문헌 검토에서는 공통 형식 어휘가 확인되지 않는다.`
- **Korean parity:** `equivalent` with `EN-C001:schmidgall2025agentlab`.

### `KO-C008:schmidgall2025agentlab`

- **Manuscript:** `submission/main_ko.tex:109`, 관련 연구.
- **Claim:** 네 연구는 개별 system의 정성적 특성화를 제공하지만 교차 system framework는 없다.
- **Citation role:** `joint` background.
- **PDF evidence:** Source는 individual architecture와 정량 evaluation을 모두 제공하고, shared taxonomy는 제안하지 않는다(PDF pp.1-22).
- **Verdict:** `PARTIAL`; severity `minor`.
- **Reasoning:** 개별 연구라는 characterization은 맞지만 정량 결과를 과도하게 축소하며, field-level absence는 현재 원고의 review finding으로 귀속해야 한다.
- **Proposed correction:** `선행 연구는 개별 시스템의 구조와 정성·정량 평가를 제공한다. 본 문헌 검토에서 이들 연구를 아우르는 공통 비교 프레임워크는 확인되지 않았다.`
- **Korean parity:** `equivalent` with `EN-C013:schmidgall2025agentlab`.

### `KO-C022:schmidgall2025agentlab`

- **Manuscript:** `submission/main_ko.tex:195`, 핵심 AI 과학자 시스템 분석.
- **Claim:** Framework를 Agent Laboratory를 포함한 네 end-to-end system에 적용하며, 작은 표본에서 closed-loop system과 더 complete validator가 함께 나타난다는 synthesis.
- **Citation role:** `joint` and `interpretive`.
- **PDF evidence:** 저자들은 Agent Laboratory를 human-provided idea에서 code/report까지 이어지는 전체 research pipeline이라고 부른다(PDF pp.1-2, 5-10, 21-22). 내부에는 code-score-reflection loop와 reviewer-driven revisit가 있지만, autonomous G와 validated novelty gate는 없다(PDF pp.6-10). Automated reviewer가 human score를 `+2.3` 과대평가한다(PDF pp.12-14).
- **Verdict:** `SUPPORTED_WITH_QUALIFICATION`; severity `minor`; cross-system association에는 `joint-only`.
- **Reasoning:** Human-initiated end-to-end computational pipeline로 표본에 포함하는 것은 타당하다. 다만 `end-to-end`가 autonomous ideation까지 포함하지 않는다고 명시해야 한다. 이 한 source는 closure-validator 공변 관계를 확립하지 않으며, Agent Laboratory 자체도 compile/reward/reviewer의 여러 check와 partial closure를 가진다.
- **Proposed correction:** `인간 제공 아이디어에서 시작하는 Agent Laboratory를 포함해 네 계산 연구 pipeline에 framework를 적용한다. 다음 표의 closure와 validator coding 및 그 공변 관계는 각 source의 직접 결론이 아니라 본 연구의 provisional cross-system annotation이다.`
- **Korean parity:** `added` relative to the corresponding English core-section setup at `main.tex:142`, which has no citation. English later gives the `+2.3` Agent Laboratory statement at `main.tex:166` but does not cite this primary source there.

## Korean Parity

| English occurrence | Korean occurrence | Parity | Assessment |
|---|---|---|---|
| `EN-C001:schmidgall2025agentlab` | `KO-C001:schmidgall2025agentlab` | `equivalent` | 두 언어 모두 human-provided idea 경계를 지우고 독립 hypothesis generation 정의에 포함한다. |
| `EN-C013:schmidgall2025agentlab` | `KO-C008:schmidgall2025agentlab` | `equivalent` | individual study와 field-level shared-framework absence를 같은 방식으로 결합한다. |
| 직접 대응하는 영어 setup citation 없음 | `KO-C022:schmidgall2025agentlab` | `added` | 한국어 core-section opening은 네 source를 cross-system association과 table 앞에 붙이지만, 대응 영어 opening은 무인용이다. |
| `main.tex:166`의 source-specific `+2.3` 문장 | 직접 대응 없음 | `omitted` | 한국어는 Agent Laboratory의 reviewer 격차와 그 수치 조건을 번역하지 않는다. 영어 문장도 현재 primary key 대신 다른 reviewer-study key만 붙인다. |

두 언어를 맞추려면 (1) human-provided idea와 optional co-pilot direction, (2) 내부 code feedback loop와 autonomy 경계, (3) `+2.3`의 표본 조건, (4) cross-system coding이 원고 저자의 synthesis라는 귀속을 양쪽에 동일하게 넣어야 한다.

## Frozen Supplementary Description Assessment

Frozen description:

> A human-directed assistant: a person supplies the research idea and ongoing direction, and LLM agents carry out literature review, an iterative code-writing-and-execution loop for experiments, and writing. The only automated quality check is an LLM reviewer applying conference guidelines, which was documented to over-estimate quality by about +2.3 points relative to human graduate-student reviewers. There is no autonomous certification of novelty.

| Frozen clause | Evidence | Verdict | Required qualification or correction |
|---|---|---|---|
| `A human-directed assistant` | 논문의 목표와 discussion은 사람의 creative ideation을 보조하는 co-pilot이다(PDF pp.1-2, 21-22). 그러나 autonomous mode는 초기 idea 이후 계속 인간이 지시하지 않는다(PDF p.10). | `SUPPORTED_WITH_QUALIFICATION` | Product intent는 human-centered이지만 모든 run이 continuously human-directed인 것은 아니다. `human-initiated assistant with optional co-pilot direction`으로 쓴다. |
| `a person supplies the research idea` | 두 mode 모두 초기 research idea를 인간이 제공한다(PDF pp.1-2, 10). | `SUPPORTED` | 없음. |
| `and ongoing direction` | 각 subtask checkpoint의 human feedback은 co-pilot mode에만 있다. Autonomous mode는 초기 idea 이후 인간 개입이 없다(PDF p.10). | `SUPPORTED_WITH_QUALIFICATION` | `may supply ongoing direction in co-pilot mode`로 바꾼다. |
| Agents carry out literature review | arXiv search, full-text selection과 curated review를 수행한다(PDF pp.5-6, 32-39). | `SUPPORTED` | 최종 selection maximum과 search failure 한계를 함께 볼 수 있다. |
| iterative code-writing-and-execution loop | `EDIT/REPLACE`, execution, repair, LLM score, reflection, top-program sampling이 반복된다(PDF pp.6-7, 41-45). | `SUPPORTED_WITH_QUALIFICATION` | 실제 code/result iteration이지만 기본 score는 empirical metric이 아니라 subjective LLM plan-alignment reward다. 별도 MLE-Bench run만 dev metric을 쓴다. |
| writing | `paper-solver`가 scaffold, arXiv search, edit, compile, review를 수행한다(PDF pp.8-10, 45-56). | `SUPPORTED_WITH_QUALIFICATION` | 저자들은 output을 final human paper가 아니라 사람이 확장하고 다시 쓰기 위한 foundation report로 제한한다(PDF pp.8, 19). |
| `The only automated quality check is an LLM reviewer` | Python compiler/runtime, code repair, Professor LLM program score, LaTeX compiler와 reviewer가 모두 자동 check다(PDF pp.6-10, 31, 41-56). | `CONTRADICTED`; severity `major` | `Automated checks include syntax/runtime checks, an LLM program reward, LaTeX compilation, and an LLM paper reviewer`로 교정한다. |
| reviewer applies conference guidelines | Reviewer prompt는 NeurIPS form을 채택하고 originality, quality, soundness, overall 등을 평가한다(PDF pp.9-10, 50-56). | `SUPPORTED` | Reviewer 1개가 writing score에, 3개가 refinement에 사용된다는 configuration을 명시할 수 있다(PDF p.31). |
| over-estimates by about `+2.3` relative to graduate-student reviewers | Automated overall `6.1/10`, 10 volunteer PhD students의 human overall `3.8/10`, 차이 `+2.3`이다(PDF pp.11-14). | `SUPPORTED_WITH_QUALIFICATION` | 15개 autonomous output과 세 backend에 한정된 평균 차이이며, 보편적 calibration error로 일반화하지 않는다. 이 수치는 본 source에 직접 귀속한다. |
| `There is no autonomous certification of novelty` | Human이 initial idea를 주고, dedicated novelty test나 validated gate는 없다. 다만 reviewer가 `Originality` 1-4를 자동 채점한다(PDF pp.1-2, 9-10, 51-55). | `SUPPORTED_WITH_QUALIFICATION` | `The reviewer assigns an originality score, but no dedicated or validated autonomous novelty-certification gate is demonstrated`로 쓴다. |

**Corrected description:** Agent Laboratory is a human-initiated machine-learning research assistant. A person supplies the research idea in both modes and may review each subtask and request reruns with notes in co-pilot mode. Agents conduct iterative literature review, planning, data preparation, code generation/execution/refinement, result interpretation, and report writing/refinement. Automated checks include compiler/runtime checks, an LLM reward over the plan, code, and output, LaTeX compilation, and a NeurIPS-style LLM reviewer. On 15 autonomous-mode reports, automated overall review averaged 6.1/10 versus 3.8/10 from 10 volunteer PhD students, a condition-specific `+2.3` self-evaluation gap. The reviewer assigns an originality score, but the paper demonstrates no dedicated or validated autonomous novelty-certification gate.

## Overall Verdict

**`major_revision`**

PDF identity와 citation source 자체는 유효하다. Agent Laboratory를 human-initiated computational research pipeline의 사례로 인용하는 것도 적절하다. 그러나 현재 서론의 grouped definition은 이 system이 hypothesis를 독립 생성한다고 오독하게 만들며, source는 반대로 인간이 idea를 제공하는 차이를 핵심 기여로 강조한다. Frozen description도 automated reviewer를 유일한 quality check라고 잘못 축약한다.

`+2.3`은 다른 논문에서 빌려온 숫자가 아니라 이 PDF pp.12-14와 Figure 6이 직접 보고한 수치다. 따라서 해당 Agent Laboratory claim에는 `schmidgall2025agentlab`을 primary citation으로 붙여야 한다. 다만 이 수치는 15개 autonomous output과 10명 volunteer PhD students 조건의 overall-score gap이며, 일반 novelty calibration 결과로 확대하면 안 된다.

우선 교정 순서는 (1) `EN/KO-C001`에서 independent hypothesis generation을 Agent Laboratory에 적용하지 않기, (2) `+2.3` 문장에 primary source와 평가 조건 붙이기, (3) frozen description에 모든 automated checks와 reviewer의 실제 역할 반영하기, (4) `EN-C013/KO-C008/KO-C022`에서 source fact와 manuscript cross-system synthesis를 분리하기다.

## Completion Checklist

- [x] PDF identity, hash, page count, BibTeX 일치 확인
- [x] PDF pp.1-84를 순서대로 전부 독해
- [x] 본문, 참고문헌, hyperparameters, prompts, review example, survey instruments 확인
- [x] Figures 1-9와 Table 1의 관련 페이지 렌더링 확인
- [x] `EN-C001`, `EN-C013`의 sentence-level entailment와 severity 판정
- [x] `KO-C001`, `KO-C008`, `KO-C022`의 sentence-level entailment와 severity 판정
- [x] 모든 frozen-description clause를 page-grounded하게 판정
- [x] Human direction, novelty, experiment feedback, automated review의 경계 분리
- [x] `+2.3`의 source ownership, sample, metric, comparator 확인
- [x] English/Korean parity와 added/omitted occurrence 확인
- [x] Source claim과 SERVO 해석 분리
- [x] API 또는 외부 model 호출 없이 local PDF만 사용

AUDIT_COMPLETE: yes
PAGES_COVERED: 1-84
EN_LINKS_COVERED: EN-C001:schmidgall2025agentlab, EN-C013:schmidgall2025agentlab
KO_LINKS_COVERED: KO-C001:schmidgall2025agentlab, KO-C008:schmidgall2025agentlab, KO-C022:schmidgall2025agentlab
SYSTEM_DESCRIPTION_ASSESSED: yes
VERDICT: major_revision
