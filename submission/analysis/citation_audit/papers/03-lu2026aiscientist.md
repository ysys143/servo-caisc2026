# `lu2026aiscientist` 전문 인용 감사

## Source Identity

- **Citation key:** `lu2026aiscientist`
- **BibTeX:** Chris Lu, Cong Lu, Robert Tjarko Lange, Yutaro Yamada, Shengran Hu, Jakob Foerster, David Ha, Jeff Clune, “Towards end-to-end automation of AI research,” *Nature* 651, 914–919 (2026), DOI `10.1038/s41586-026-10265-5`.
- **PDF 자체 표제·저자:** “Towards end-to-end automation of AI research,” 위 8인 저자(PDF p.1; Nature p.914).
- **출판 이력:** received 2025-07-08, accepted 2026-02-11, published online 2026-03-25(PDF p.1).
- **Stable identifier:** DOI `10.1038/s41586-026-10265-5`. 이 PDF에는 별도의 arXiv 식별자가 표제면 식별자로 제시되지 않는다.
- **절대 PDF 경로:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/Towards end-to-end automation of AI research.pdf`
- **SHA-256:** `a75e0d93447f400179136bf18d909df29e0c8ccaeba076a1dfb1beeef0e0e10d`
- **`pdfinfo`:** 9 pages, 595.276 × 790.866 pt, PDF 1.4, 2,774,541 bytes, not encrypted.
- **Version status:** `exact`. PDF의 제목, 저자, 학술지, 권·쪽, 연도, DOI가 `references.bib`와 manifest에 일치한다. 2024 arXiv 논문이 아니라 2026년 *Nature* 출판본이며, template-based 및 확장된 template-free system을 함께 보고한다.

## Full-Text Coverage

로컬 PDF p.1부터 p.9까지 layout-preserving text를 순서대로 읽었다. PDF pp.1–6은 인쇄면 Nature pp.914–919이고, PDF pp.7–9는 Methods와 후속 메타데이터로서 인쇄면 쪽 번호가 보이지 않는다. 이하에서는 혼동을 피하기 위해 `PDF p.N`을 우선 사용하고, 본문 인쇄면 번호가 있는 경우 병기한다.

| PDF 페이지 | 순차 독해 및 확인 내용 |
|---|---|
| 1 (Nature 914) | 표제·서지정보, 초록, 자동 과학의 역사적 동기, end-to-end 우선권 주장, 두 운용 mode, 자동 reviewer와 ICLR workshop 실험의 설정 |
| 2 (Nature 915) | Figure 1 workflow, idea archive·novelty search, template-based/free experiment execution, experimental journal, manuscript generation, automated review |
| 3 (Nature 916) | Table 1 reviewer metrics와 조건, contamination 점검, model/compute scaling, human workshop review, 수동 후보 선별, 3편의 결과 |
| 4 (Nature 917) | Figure 2의 생성 논문, failure modes, workshop와 main-conference bar 차이, 계산 실험 한정, 윤리·IRB·철회 protocol |
| 5 (Nature 918) | Figure 3의 4-stage tree와 compute scaling, 결론, 참고문헌 1–20 |
| 6 (Nature 919) | 참고문헌 21–48, 출판·라이선스 정보 |
| 7 | Methods 개요, 두 mode, template-based 3단계, template-free idea generation과 4-stage progress manager, tree-search 진입부 |
| 8 | node execution cycle, best-first selection, debug/hyperparameter/ablation/replication/aggregation nodes, VLM·dataset·writing enhancement, reviewer 설계 진입부 |
| 9 | 5-review meta-review, reviewer validation 조건과 비교 한계, ethics, data/code availability, author contributions, competing interests |

PDF pp.2–5를 160 dpi PNG로 렌더링해 시각 확인했다. Figure 1에서 ideation–experimentation–write-up 구조, 0.69 전후의 reviewer 막대와 model-release 추세를 확인했고(PDF p.2), Table 1의 각 metric·오차범위·cohort 구분을 확인했다(PDF p.3). Figure 2에서 생성 논문의 실제 지면과 `6, 7, 6` review score를 확인했으며(PDF p.4), Figure 3에서 4개 stage, node 유형, best node 전달, `n=30` compute-scaling points를 확인했다(PDF p.5). 텍스트 추출과 렌더링 사이에 판정을 바꿀 layout 불일치는 없었다.

논문이 여러 세부 분석을 Supplementary Information에 위임하지만 그 파일은 이 9쪽 PDF에 포함되어 있지 않다. 다만 현재 원고의 7개 인용 occurrence와 frozen description을 판정하는 데 필요한 architecture, reviewer 수치, workshop 절차, 계산-only 범위는 본 PDF의 본문·Methods·표·그림에 직접 제시되어 있어 completion을 막지 않는다.

## Problem and Context

저자들이 제기하는 문제는 LLM 이전·초기의 AI가 신소재, 단백질 구조, 수학 증명, 사전 수집 데이터 분석 등 과학 절차의 일부만 자동화했고, 최근 LLM도 가설 생성·문헌 검토·coding 같은 개별 활동은 지원하지만 conception에서 publication까지의 연구 생애주기를 한 시스템이 자율적으로 연결하지 못했다는 것이다(PDF p.1). 이에 The AI Scientist를 idea 생성, 문헌 검색, 실험 계획·code 작성·실행, 결과 분석·시각화, manuscript 작성, automated peer review까지 연결하는 machine-learning research pipeline으로 제안한다(PDF pp.1–2).

역사적 맥락에서 논문은 DENDRAL 계열, computational scientific discovery, materials/protein systems와 최근 LLM ideation·coding agents를 선행 단계로 놓는다(PDF pp.1, 5–6). 이 논문의 고유한 문제의식은 새로운 과학 추론 이론이나 여러 AI Scientist를 비교하는 taxonomy보다, 이미 존재하는 foundation model과 software-engineering agent를 복합 system으로 조직해 실제 paper artifact와 외부 review 결과까지 도달할 수 있는지를 보이는 데 있다.

범위는 명확히 machine learning science에 한정된다. 저자들은 실험이 전적으로 컴퓨터에서 일어나는 분야이기 때문에 이 영역을 선택했다고 설명하고(PDF p.1), 현재 system은 computational experiments만 수행한다고 다시 한정한다(PDF p.4). 또한 자율성의 경계는 mode에 따라 다르다. focused mode는 사람이 제공한 code template와 특정 topic에서 출발하고, template-free mode도 broad workshop theme, public datasets, foundation models와 실행 환경을 전제로 한다(PDF pp.1–3, 7–8). 외부 workshop 제출 후보는 인간 연구자들이 단계별로 수동 선별했다(PDF p.3).

따라서 이 source는 The AI Scientist가 가설·계산 실험·원고를 연결하는 개별 사례라는 점은 강하게 지지한다. 그러나 AI Scientist “분야”의 급속한 증가, 공통 형식 어휘의 부재, validator 계층이 loop closure를 결정한다는 교차 시스템 관계는 이 논문의 연구 질문이나 조사 결과가 아니다. 그것들은 현재 SERVO 원고 저자들의 literature synthesis로 별도 귀속해야 한다.

## Structure and Argument

문서의 논증은 다음 순서로 진행된다.

1. PDF p.1은 부분 자동화의 역사와 end-to-end gap을 제시한 뒤, 두 mode의 The AI Scientist와 외부 workshop review를 핵심 demonstration으로 선언한다.
2. PDF p.2와 Figure 1은 ideation, experimentation, write-up/review를 연결하고, idea archive·literature novelty check·experimental journal을 설명한다.
3. PDF p.3과 Table 1은 Automated Reviewer를 실제 conference accept/reject와 비교하며, pre-cutoff와 post-cutoff cohort 및 별도 NeurIPS human-consistency baseline을 제시한다.
4. 같은 p.3에서 생성 논문 quality의 model/compute scaling과 ICLR 2025 ICBINB workshop 제출 실험을 보고한다. 이 절은 수동 candidate filtering과 selected manuscript 자체의 무수정을 함께 명시한다.
5. PDF p.4는 생성 논문 예시 뒤에 낮은 일관성, implementation error, hallucination, 계산-only 범위, review-system 부담과 윤리 문제를 집중적으로 제한한다.
6. PDF p.5의 Figure 3은 4-stage agentic tree와 compute scaling을 구체화하고, 결론은 workshop bar 통과를 이정표로 해석하되 top-tier quality가 아님을 유지한다.
7. PDF pp.7–9의 Methods는 template-based/free 구현, node 선택·실행, replication/aggregation, VLM feedback, automated reviewer ensemble과 validation protocol을 재현 가능한 수준으로 확장한다.

핵심 논증은 세 층으로 구분해야 한다. 첫째, pipeline이 research artifact를 end-to-end로 생성한다는 architecture claim이다. 둘째, 내부 automated reviewer가 conference decision을 어느 정도 분류한다는 benchmark claim이다. 셋째, 인간 workshop review에서 3편 중 1편이 높은 score를 얻었다는 external evaluation claim이다. 세 번째는 인간 선별과 철회 protocol을 포함하며, 첫 번째 architecture의 완전 자율적 acceptance gate로 자동 편입되지 않는다.

## Methods and Evidence

### 두 운용 mode

- **Template-based:** 사람의 seed code가 간단한 baseline training을 재현한다. LLM은 기존 idea archive의 변형·확장을 생성하고, 각 idea에 interestingness·novelty·feasibility 1–10 self-score를 붙이며 Semantic Scholar 검색 최대 10 rounds로 유사 idea를 걸러낸다(PDF p.7). Aider가 최대 5개 실험을 순차 구현하고, 실패 시 최대 4회 patch/retry하며, 결과와 plot을 experimental journal에 남긴다. 그 journal이 다음 계획과 manuscript 작성의 memory 역할을 한다(PDF pp.2, 7).
- **Template-free:** initial code 없이 high-level proposal에서 시작하지만, o3 idea generation/code critique, Claude Sonnet 4 code generation, GPT-4o visual feedback·node 평가, o1 direct LaTeX generation, o4-mini review를 조합한다(PDF pp.7–9). preliminary investigation, hyperparameter tuning, research agenda execution, ablation의 4 stage를 각각 tree search로 수행한다. stage 1은 working prototype, stage 2는 training-curve stabilization과 최소 2개 dataset 성공, stage 3·4는 compute budget 소진이 stopping rule이다(PDF p.7). 한 complete generation은 문제에 따라 수 시간에서 15시간 이상 걸리며, human scientist가 dataset candidate와 local-data instruction을 갱신할 수 있다(PDF p.8).

### Agentic tree search와 experiment evidence

각 node에서 LLM이 plan과 Python code를 만들고 즉시 실행한다. 오류가 나면 buggy로 종료하며, 성공하면 structured metric을 저장하고 plot을 만들어 VLM critique를 받는다. 시각화 문제가 발견되면 역시 buggy로 표기한다(PDF p.8). 여러 node를 병렬 확장하고, buggy node를 확률적으로 골라 debug하거나 non-buggy node를 GPT-4o의 best-first 평가로 골라 refine한다. stage 경계에서는 LLM evaluator가 leaf 중 하나를 다음 stage root로 선택한다(PDF pp.7–8).

특수 node는 hyperparameter, ablation, replication, aggregation으로 나뉜다. replication node는 parent experiment를 다른 random seed로 다시 실행하며, source는 고정 수가 아니라 “typically several”이라고만 한다. aggregation node는 새 실험을 하지 않고 replication 결과를 모아 mean과 standard deviation을 명시한 figure를 생성한다(PDF p.8). 따라서 “replication node가 mean±s.d.를 보고한다”는 축약은 약간 부정확하다. 재실행은 replication node, 집계·표현은 aggregation node의 역할이다. 또한 9쪽 article은 이 mechanism을 Methods와 Figure 3 schematic으로 명시하지만, 특정 생성 논문의 seed-level trace나 mean/s.d. artifact를 직접 제시하지 않는다. Figures 1b·3c의 error bars는 별도 system-level experiment의 standard error이므로 그 직접 증거가 아니다(PDF pp.2, 5, 8).

Figure 3의 compute experiment는 experimental node budget이 증가할수록 automated-reviewer paper score가 증가하는 경향을 `n=30` run으로 제시한다(PDF p.5). 이는 같은 내부 reviewer가 생성물을 평가한 결과이며, 외부 인간 quality나 과학적 정확성의 직접 척도는 아니다.

### Automated Reviewer

출판본 reviewer는 o4-mini를 사용하며, NeurIPS guideline 형식으로 soundness, presentation, contribution, overall score, confidence, strengths/weaknesses와 accept/reject를 만든다(PDF pp.8–9). 각 paper에 독립 review 5개를 생성하고, 별도 LLM area-chair meta-review가 consensus를 만든다(PDF p.9).

validation은 OpenReview의 ICLR accept/reject를 target으로 한다. Table 1은 knowledge-cutoff 이전 2017–2024 cohort에서 balanced accuracy `0.69 ± 0.04`, accuracy `0.65 ± 0.10`, F1 `0.62 ± 0.09`, AUC `0.69 ± 0.09`, FPR `0.45 ± 0.10`, FNR `0.17 ± 0.08`을 보고한다(PDF p.3). 2025 post-cutoff cohort에서는 balanced accuracy가 `0.66 ± 0.03`이다. 오차범위는 5,000회 replicate의 95% bootstrap confidence interval이며, Figure 1c는 five-run review ensemble과 subsampled automated `n=698/876`(before/after로 인쇄), human `n=412`를 명시한다(PDF pp.2–3). 두 표본 z-test는 pre/post 각각 `P=0.319`, `P=0.921`로 balanced-accuracy 차이가 유의하지 않았고, F1 bootstrap test는 `P<0.001`이었다(PDF p.2). 표의 human row `0.66`은 같은 ICLR papers에 대한 paired human test가 아니라 별도 NeurIPS 2021 consistency experiment의 inter-human agreement다(PDF pp.3, 9). 저자들도 paper pool과 distribution이 달라 비교가 exact하지 않다고 명시한다(PDF p.9). 같은 automated row의 AUC도 `0.69 ± 0.09`이므로 headline `0.69`에는 balanced accuracy라는 metric을 반드시 붙여야 한다.

### External workshop review

저자들은 ICLR leadership·ICBINB workshop organizers·IRB와 협의해 template-free system의 논문 3편을 43편 규모 workshop review pool에 제출했다(PDF p.3). 그 전에 인간 연구자들이 workshop 적합성, code가 idea를 올바르게 구현하고 오류 없이 실행되는지, manuscript formatting이 올바른지를 기준으로 promising outputs를 단계별 수동 선별했다. 선택된 각 논문의 ideation-to-writing workflow 자체에는 인간 수정이 없었다(PDF p.3). reviewers는 일부 submission이 AI-generated임을 알았지만 어느 것인지는 몰랐고, 잠재적 AI paper review를 opt out할 수 있었다(PDF pp.3, 9). 한 편은 `6, 7, 6`, 평균 `6.33`을 받아 평균 acceptance threshold를 넘고 reviewed papers의 상위 45%에 들었으며, organizers는 사전 철회 protocol이 없었다면 받아들여졌을 가능성이 높다고 말했다. 다른 두 편은 기준을 넘지 못했고, 세 편 모두 outcome과 무관하게 철회됐다(PDF pp.3–4).

## Findings

### Principal results

- system은 idea proposal, literature novelty filtering, code/experiment, plot, paper, automated review를 실제 artifact pipeline으로 연결한다(PDF pp.1–2, 7–9).
- Figure 1b에서 model release date와 automated-reviewer paper score의 적합도는 `R² = 0.517`, `P < 0.00001`이다. 각 point의 uncertainty는 standard error이고 template-free point는 `n=6`, template-based point는 `n=3`이다(PDF p.2). 이는 reviewer가 매긴 내부 quality score와의 관계이지 randomized causal estimate나 직접 human validation이 아니다.
- Figure 3c에서 template-free tree의 node budget 증가와 reviewer score 증가가 `n=30` 조건별 run으로 보고된다(PDF p.5). source는 이를 test-time compute scaling evidence로 해석한다.
- Automated Reviewer의 `0.69 ± 0.04` balanced accuracy는 **2017–2024 pre-cutoff ICLR cohort** 조건이다. 2025 post-cutoff 값은 `0.66 ± 0.03`이며, 인간 `0.66`은 별도 NeurIPS consistency study다(PDF p.3).
- pre-cutoff reviewer F1 `0.62 ± 0.09`는 human row `0.49`보다 높지만, reviewer FPR `0.45 ± 0.10`은 human row `0.17`보다 높다(PDF p.3). 이 비대칭은 false-positive 경향을 보여 주지만 probability/score calibration을 측정한 것은 아니다.
- ICBINB workshop은 acceptance rate 70%였고, ICLR 2025 main conference는 32%였다(PDF p.4). 세 AI 논문 중 한 편만 workshop threshold를 넘었으며, authors' internal human review는 세 편 모두 main ICLR bar에는 못 미친다고 판단했다(PDF pp.3–4).
- 현재 experiments는 전부 computational이다(PDF pp.1, 4). physical laboratory execution이나 physical result validation은 수행하지 않았다.

### SERVO 관련 함의

다음은 source 저자들의 직접 terminology가 아니라 감사자의 명시적 mapping이다. The AI Scientist는 `G`에 idea generation과 literature filtering, `E`에 code execution과 computational experiment tree, `M_e`에 experimental journal과 node 기록, `M_s` 후보에 idea archive, `π`에 LLM-guided best-first tree expansion을 둔다. replication/aggregation은 repeated empirical-computational evidence를 만들므로 `V_e` 후보로 볼 수 있고, Automated Reviewer는 `V_s`, workshop review는 외부 `V_h`로 해석할 수 있다.

그러나 이 mapping의 gate 구조는 source fact와 분리해야 한다. replication은 robustness를 높이지만 그 자체가 hypothesis acceptance를 결정한다고 입증되지 않는다. Automated Reviewer는 paper 평가와 system configuration 비교에 사용되지만, reviewer decision이 experiment tree나 external submission을 자동으로 gate했다는 절차는 제시되지 않는다. 실제 workshop candidate gate에는 인간 수동 선별이 있었다(PDF p.3). 외부 workshop review는 system architecture 내부의 autonomous layer가 아니라 연구팀이 수행한 evaluation이다. 따라서 source는 **계산 실험 내부의 반복 feedback과 end-to-end artifact generation**을 지지하지만, `V_e+V_s+V_h`가 하나의 완전 자율적 closed loop로 결합됐다는 강한 해석은 지지하지 않는다.

또한 search policy는 information gain이나 BED objective가 아니라 performance metrics, training dynamics, plot quality를 GPT-4o가 평가하는 heuristic best-first search다(PDF p.8). archive는 후속 idea generation을 조건화하지만, 그 benefit이나 semantic-knowledge accumulation을 독립적으로 검증하지 않는다.

## Limitations

1. **Human boundary:** focused mode는 human code scaffold를 쓰고, template-free workshop run도 broad theme와 dataset/tool environment를 받는다. workshop 제출 후보는 인간이 단계별로 선별하고 implementation correctness를 확인했다(PDF pp.1, 3, 7–9).
2. **Workshop evidence의 낮은 bar와 작은 표본:** 70% acceptance-rate workshop에서 3편 중 1편이 threshold를 넘었다. paper는 실제 publication 전에 모두 철회됐으며, organizers의 “would likely have been accepted” 판단과 score가 핵심 근거다(PDF pp.3–4).
3. **일관성과 correctness:** 저자들은 naive idea, incorrect implementation, methodological shallowness, experimental error, duplicate figures, inaccurate citation을 포함한 hallucination을 명시한다(PDF p.4). pipeline completion은 trustworthy science와 동일하지 않다.
4. **Reviewer comparator mismatch:** `0.69` automated result와 `0.66` human result는 같은 paper pool·protocol의 paired comparison이 아니다. 저자도 ICLR/NeurIPS distribution shift 때문에 exact comparison이 아니라고 쓴다(PDF pp.3, 9).
5. **Contamination과 distribution shift:** pre-cutoff cohort는 model training에 포함됐을 가능성이 있고, post-cutoff balanced accuracy는 0.66으로 낮아진다(PDF p.3). 저자들은 영향이 작다고 해석하지만 contamination 자체는 배제하지 못한다.
6. **Calibration 미평가:** balanced accuracy, F1, AUC, FPR/FNR는 decision discrimination/error를 평가한다. calibration curve, ECE, Brier score, score-to-probability reliability는 보고하지 않는다. 그러므로 source만으로 reviewer를 “calibrated” 또는 “uncalibrated”라고 단정할 수 없다.
7. **Gate provenance:** automated reviewer가 최종 accept/reject를 출력한다는 사실과 그 출력이 research search·paper revision·external submission을 결정하는 gating channel이라는 주장은 다르다. 후자는 source에서 입증되지 않고, external candidate selection은 인간이 했다(PDF p.3).
8. **내부 평가의 순환성:** model release와 compute scaling의 paper-quality 결과는 연구팀의 own Automated Reviewer score를 outcome으로 사용한다(PDF pp.2–3, 5). 외부 human evidence는 workshop 3편에 한정된다.
9. **Open-endedness 범위:** idea archive와 template-free tree가 탐색 폭을 넓히지만 user-specified ML subfield, available models/datasets, stage budget과 heuristic LLM scoring 안에서 작동한다(PDF pp.2, 7–8). field-level novelty나 장기 semantic accumulation은 평가하지 않는다.
10. **Replication evidence level:** replication/aggregation은 Methods에 구현 mechanism으로 기술되지만, 이 9쪽 파일은 특정 생성 논문의 seed-level trace, aggregate script, mean/s.d. output을 직접 보여 주지 않는다(PDF pp.5, 8). 모든 experiment가 replicated됐다고 일반화할 수 없다.
11. **Reporting completeness:** exact prompts, model versions, replication counts, tree hyperparameters와 generated-paper full analyses 상당 부분이 이 로컬 PDF에 없는 Supplementary Information으로 이관된다(PDF pp.2–5, 7–9).
12. **물리적 검증 부재:** 모든 실험이 computational이다. 저자들은 automated chemistry laboratory를 future extension으로만 언급한다(PDF p.4).
13. **안전·사회적 위험:** review overload, literature noise, credit appropriation, credential inflation, job displacement, unethical experiments를 저자들이 직접 위험으로 열거하며, disclosure와 withdrawal norm이 아직 필요하다고 본다(PDF pp.1, 4).

## Citation Assessments

### `EN-C001:lu2026aiscientist`

- **원고 위치:** `main.tex:69`, Introduction.
- **원고 주장:** AI Scientist systems를 “독립적으로 가설을 만들고, 실험을 실행하고, 지식을 합성하는 agents”로 정의하고, 그 수가 빠르게 증가했으나 field에는 shared formal vocabulary가 없다고 말한다.
- **Citation role:** `joint`, `background`.
- **PDF 근거:** The AI Scientist는 idea·hypothesis proposal, computational experiment, analysis와 manuscript synthesis를 연결한다(PDF pp.1–2, 7–8). 다만 focused mode는 human scaffold, template-free mode도 specified domain/tool environment를 전제로 하고 workshop candidate는 인간이 선별했다(PDF pp.1, 3, 7).
- **판정:** `PARTIAL`; severity `minor`.
- **이유:** 이 source는 category member와 capability 예시는 지지한다. 그러나 한 system paper가 field-wide “rapid proliferation”이나 shared formal vocabulary의 보편적 부재를 입증하지 않는다. `independently`도 위 human boundary를 생략하면 과도하다.
- **권고 수정:** “Recent systems connect hypothesis generation, computational experiments, and manuscript synthesis; in our cross-system review we find no shared formal vocabulary”처럼 source observation과 원고 synthesis를 분리한다.
- **Korean parity:** `equivalent` with `KO-C001:lu2026aiscientist`.

### `EN-C003:lu2026aiscientist`

- **원고 위치:** `main.tex:69`, Introduction.
- **원고 주장:** The AI Scientist를 “closed-loop manuscript-writing pipeline”의 예로 든다.
- **Citation role:** `example`, `direct` with interpretive terminology.
- **PDF 근거:** system은 idea, experiment, result journal, paper writing과 automated review를 end to end로 연결한다(PDF pp.1–2). experiment stage에는 result-informed replanning과 tree refinement가 있다(PDF pp.2, 7–8).
- **판정:** `SUPPORTED_WITH_QUALIFICATION`; severity `minor`.
- **이유:** “end-to-end manuscript-generating pipeline”은 직접 지지된다. 그러나 final Automated Reviewer가 manuscript를 다시 고치거나 experiment tree·후속 project를 결정하는 closed feedback gate라는 절차는 보이지 않는다. loop라는 말은 computational experiment 내부 반복과 idea-to-paper completion으로 한정해야 한다.
- **권고 수정:** “end-to-end automated idea-to-manuscript pipelines, with iterative computational experimentation”으로 바꾸거나 `closed-loop`의 경계를 명시한다.
- **Korean parity:** `omitted`. 한국어 서론은 grouped proliferation sentence만 유지하고, “closed-loop manuscript-writing pipeline”이라는 직접 예시를 번역하지 않는다. `KO-C022`의 broader cross-system synthesis는 동일 occurrence의 번역으로 보지 않는다.

### `EN-C013:lu2026aiscientist`

- **원고 위치:** `main.tex:90`, Related Work.
- **원고 주장:** 기존 연구는 개별 system의 qualitative characterization만 제공하고 cross-system comparison을 위한 shared framework는 제공하지 않는다고 말한다.
- **Citation role:** `joint`, `background`.
- **PDF 근거:** source는 The AI Scientist 한 system family를 상세히 설명한다. 동시에 Table 1, Figures 1·3, workshop score처럼 상당한 quantitative evaluation도 포함한다(PDF pp.2–5).
- **판정:** `SUPPORTED_WITH_QUALIFICATION`; severity `minor`.
- **이유:** 이 source가 individual-system study이고 자체 cross-system comparison framework를 제안하지 않는다는 characterization은 타당하다. 다만 “qualitative”는 정량 결과를 과소서술하며, shared framework가 literature 전체에 없다는 보편적 absence claim은 이 source 단독이 아니라 원고의 multi-source synthesis로 귀속해야 한다.
- **권고 수정:** “Prior work characterizes and quantitatively evaluates individual systems; our review introduces a shared cross-system decomposition”으로 원고 기여에 귀속한다.
- **Korean parity:** `equivalent` with `KO-C008:lu2026aiscientist`.

### `EN-C028:lu2026aiscientist`

- **원고 위치:** `main.tex:166`, Analysis of Core AI Scientist Systems.
- **원고 주장:** Nature system이 replication-based `V_e`, balanced accuracy 0.69의 automated `V_s`, ICLR workshop의 실제 peer review `V_h`를 쌓아 class에서 가장 많은 layer를 가지지만, biased·uncalibrated automated reviewer가 internal acceptance gate로 남는다고 말한다.
- **Citation role:** `direct` for component facts, `interpretive` for SERVO labels and gating, `joint-only` for class comparison.

| 세부 clause | PDF 근거 | 판정 |
|---|---|---|
| replication nodes와 mean ± s.d. | 다른 seed 재실행은 replication nodes, mean/s.d. 집계 figure는 aggregation nodes가 수행한다(PDF p.8). | `SUPPORTED_WITH_QUALIFICATION`, severity `minor`; `V_e`는 원고 mapping이다. |
| automated reviewer, balanced accuracy 0.69 | o4-mini 5-review ensemble이며 pre-cutoff ICLR cohort에서 `0.69 ± 0.04`; post-cutoff는 `0.66 ± 0.03`이다(PDF pp.3, 8–9). | `SUPPORTED_WITH_QUALIFICATION`, severity `minor`; 조건을 붙여야 한다. |
| actual peer review via ICLR workshop | 3편이 ICBINB workshop review를 받았고 1편이 threshold를 넘었지만, 후보는 인간이 수동 선별했고 모두 철회됐다(PDF pp.3–4). | `SUPPORTED_WITH_QUALIFICATION`, severity `minor`; external evaluation이지 autonomous architecture layer로 자동 결합되지 않는다. |
| “most layers in the class” | source는 다른 SERVO systems의 layer를 coding·비교하지 않는다. | `NOT_ASSESSABLE`, severity `minor`; 원고의 cross-system synthesis다. |
| reviewer가 “biased”라는 해석 | FPR은 pre-cutoff `0.45 ± 0.10`, post-cutoff `0.52 ± 0.10`으로 별도 human row `0.17`보다 높아 lenient false-positive concern을 뒷받침한다. 다만 paper pool이 다르고 source가 bias를 직접 판정하지 않는다(PDF pp.3, 9). | `PARTIAL`, severity `minor`; 관측된 error asymmetry로 한정해야 한다. |
| reviewer가 “uncalibrated”라는 label | calibration curve, threshold calibration, ECE, Brier score 등 calibration analysis가 전혀 없고 balanced accuracy는 calibration metric이 아니다(PDF pp.2–3, 9). | `UNSUPPORTED`, severity `major`. |
| reviewer가 “internal acceptance gate”라는 label | reviewer는 paper/configuration 평가에 쓰이지만 tree progression은 stage evaluator·best-first policy·budget이 결정한다. workshop 후보는 인간이 선별했다(PDF pp.2–3, 5, 7–9). | `UNSUPPORTED`, severity `major`. |

- **종합 판정:** `PARTIAL`; severity `major`.
- **이유:** 세 구성요소의 존재와 핵심 수치는 실재하지만, 서로 다른 역할을 하나의 autonomous validation stack으로 결합하고 reviewer를 uncalibrated internal gate로 부르는 핵심 해석은 source를 넘는다. 높은 FPR은 false-positive concern의 근거일 뿐 calibration failure나 operational gating의 증거가 아니다.
- **권고 수정:** “The system adds random-seed replication and aggregation, and an o4-mini five-review ensemble that reached `0.69 ± 0.04` balanced accuracy on the 2017–2024 ICLR cohort (`0.66 ± 0.03` post-cutoff). After human selection, three papers entered ICBINB review and one exceeded its score threshold; all were withdrawn. We code these as candidate `V_e`, `V_s`, and external `V_h` layers, but the source does not show that the automated reviewer gated experiment search or submission, and it does not evaluate score calibration.”
- **Korean parity:** `omitted` for the detailed claim, with the key `meaning_shifted` into `KO-C022:lu2026aiscientist`. 한국어는 replication, reviewer metric, workshop condition, layer superlative, gate/calibration assertions를 번역하지 않고 같은 key를 broader cross-system synthesis에 재배치한다.

### `KO-C001:lu2026aiscientist`

- **원고 위치:** `main_ko.tex:88`, 서론.
- **원고 주장:** AI 과학자 system의 capability definition, 급속한 증가와 공통 형식 어휘 부재.
- **Citation role:** `joint`, `background`.
- **PDF 근거:** idea–computational experiment–manuscript 연결은 직접 확인되지만(PDF pp.1–2, 7–8), 독립성에는 human scaffold·selection 경계가 있고 field-wide 증가·어휘 부재는 분석하지 않는다(PDF pp.1, 3).
- **판정:** `PARTIAL`; severity `minor`.
- **이유·수정:** `EN-C001`과 같다. 개별 system capability와 원고의 field synthesis를 분리하고 `independently`를 operational boundary 안으로 제한한다.
- **Korean parity:** `equivalent` with `EN-C001:lu2026aiscientist`.

### `KO-C008:lu2026aiscientist`

- **원고 위치:** `main_ko.tex:109`, 관련 연구.
- **원고 주장:** 선행 연구가 개별 system의 정성적 특성화를 제공하지만 공통 cross-system framework는 없다고 말한다.
- **Citation role:** `joint`, `background`.
- **PDF 근거:** single-system characterization은 맞지만 Table 1·Figures 1–3·workshop review라는 정량 평가가 있고(PDF pp.2–5), field-wide framework absence는 조사하지 않는다.
- **판정:** `SUPPORTED_WITH_QUALIFICATION`; severity `minor`.
- **이유·수정:** `EN-C013`과 같다. 이 paper가 자체 cross-system framework를 제시하지 않는다는 characterization은 맞지만, “정성적”을 “개별 system의 정성·정량 연구”로 바꾸고 literature-wide shared-framework 부재는 현재 원고의 review finding으로 귀속한다.
- **Korean parity:** `equivalent` with `EN-C013:lu2026aiscientist`.

### `KO-C022:lu2026aiscientist`

- **원고 위치:** `main_ko.tex:195`, 핵심 AI 과학자 시스템 분석.
- **원고 주장:** SERVO를 네 end-to-end system에 적용하고, 작은 표본에서 closed-loop system이 더 complete한 validator와 함께 `G`·`E`·`π`도 발전시켰다고 종합한다.
- **Citation role:** `joint`, `interpretive`; cohort 관계에는 `joint-only`.
- **PDF 근거:** The AI Scientist는 end-to-end computational pipeline이며, template-free mode는 idea generation, tree-search experimentation, replication과 review를 추가·확장한다(PDF pp.1–3, 5, 7–9). 그러나 source는 SERVO completeness를 측정하거나 네 system의 covariance를 비교하지 않는다. external workshop candidate에는 human selection이 있었다(PDF p.3).
- **판정:** `PARTIAL`; severity `minor`.
- **이유:** 이 system을 분석 표본에 포함하는 것은 타당하고 `G/E/π` 발전의 source-specific 근거도 있다. closed-loop/validator-completeness association은 source finding이 아니라 원고 coding에서 나온 small-sample synthesis다.
- **권고 수정:** “우리의 구조화 coding에서는”이라는 attribution을 붙이고, Nature system의 loop는 computational tree에서 닫히며 external submission gate는 human-mediated였음을 표 주석에 명시한다.
- **Korean parity:** `meaning_shifted` relative to the detailed `EN-C028` use and `added` as a paragraph-level omnibus citation. 영어 `EN-C003`의 직접 pipeline example은 별도로 `omitted`이며, 이 occurrence의 번역으로 간주하지 않는다.

## Korean Parity

| English occurrence | Korean occurrence | Parity | 감사 결과 |
|---|---|---|---|
| `EN-C001:lu2026aiscientist` | `KO-C001:lu2026aiscientist` | `equivalent` | capability definition과 field-level 증가·어휘 부재를 같은 강도로 서술하며 human-boundary qualifier도 함께 빠진다. |
| `EN-C003:lu2026aiscientist` | 없음 | `omitted` | 한국어 서론에는 “closed-loop manuscript-writing pipeline” 직접 예시가 없다. 뒤의 broad core-analysis occurrence는 번역 대응으로 보지 않는다. |
| `EN-C013:lu2026aiscientist` | `KO-C008:lu2026aiscientist` | `equivalent` | individual characterization과 shared-framework absence를 동일하게 결합하고 quantitative evidence를 “정성적”으로 축소한다. |
| `EN-C028:lu2026aiscientist` | 직접 equivalent 없음; key는 `KO-C022`에 재등장 | `omitted` / `meaning_shifted` | replication, `0.69` 조건, external peer review, bias/calibration/gate 문장은 번역되지 않고, key만 broader cohort synthesis로 이동한다. |
| 직접 대응하는 영어 setup citation 없음 | `KO-C022:lu2026aiscientist` | `added` | 한국어는 framework 적용 문단에 paragraph-level omnibus citation을 추가한다. |

한국어본은 영어 `EN-C028`의 가장 문제가 큰 “biased, uncalibrated internal acceptance gate” 문장을 직접 반복하지 않는다는 점에서는 더 보수적이다. 반면 reviewer의 cohort 조건, human selection, external-review 지위도 함께 사라져 `3단계` coding의 근거와 경계가 불투명해진다. 두 언어를 맞추려면 (1) end-to-end artifact generation과 feedback-gated loop를 분리하고, (2) `0.69`의 cohort·오차범위를 명시하며, (3) external workshop review와 human candidate selection을 system-internal validator와 구분하고, (4) cross-system 관계가 현재 원고의 coding임을 양쪽에 동일하게 표시해야 한다.

## Frozen Supplementary Description Assessment

Frozen description:

> A successor LLM system using agentic tree search over experiment plans, with replication nodes that re-run experiments and report results as mean and standard deviation over random seeds. It includes an automated LLM reviewer (about 0.69 balanced accuracy) and an open-endedness archive that conditions later search. One output cleared an external workshop peer-review bar. Experiments are computational only; no physical experiment.

- **“A successor LLM system” — `SUPPORTED_WITH_QUALIFICATION`.** 출판본은 template-based system과 더 open-ended한 template-free enhancement를 함께 보고하고, code availability에서 후자를 `AI-Scientist-v2` repository로 연결한다(PDF pp.7, 9). 다만 단일 successor만 분석하는 문서가 아니라 두 mode를 함께 평가한다.
- **“using agentic tree search over experiment plans” — `SUPPORTED_WITH_QUALIFICATION`.** 이 방식은 특히 template-free mode에 해당한다. 4 stage별 parallelized agentic tree가 plan·code·metric·plot·critique를 node에 기록하며 LLM-guided best-first expansion을 수행하지만, template-based mode는 linear execution이다(PDF pp.2, 5, 7–8).
- **“replication nodes that re-run experiments and report mean and standard deviation over random seeds” — `SUPPORTED_WITH_QUALIFICATION`.** replication nodes가 다른 random seeds로 parent를 재실행하고, 별도 aggregation nodes가 결과를 모아 mean과 s.d.를 표시한 figures를 만든다(PDF p.8). source는 fixed count가 아니라 “typically several”이라고 하며 모든 experiment의 replication을 보장하지 않는다. 또한 9쪽 article은 mechanism을 기술하지만 특정 generated paper의 seed-level trace나 aggregate mean/s.d. artifact는 직접 보여 주지 않는다.
- **“automated LLM reviewer (about 0.69 balanced accuracy)” — `SUPPORTED_WITH_QUALIFICATION`.** o4-mini 기반 5-review ensemble이 있고, `0.69 ± 0.04`는 2017–2024 pre-cutoff ICLR cohort다. 2025 post-cutoff는 `0.66 ± 0.03`이고 human 0.66은 별도 NeurIPS comparison이다(PDF pp.3, 8–9).
- **“an open-endedness archive that conditions later search” — `SUPPORTED_WITH_QUALIFICATION`.** growing idea archive의 기존 idea를 변형·확장해 후속 idea를 만들고 literature search로 novelty를 거른다(PDF pp.2, 7). 하지만 archive가 template-free experiment-tree node selection을 직접 조건화하거나 장기 semantic memory의 효용을 검증했다는 결과는 없다.
- **“One output cleared an external workshop peer-review bar” — `SUPPORTED_WITH_QUALIFICATION`.** 3편 중 1편이 `6, 7, 6`으로 평균 threshold를 넘고 organizers가 accepted 가능성이 높다고 했지만, workshop acceptance rate는 70%였고 인간이 후보를 선별했으며 모든 논문은 사전 protocol에 따라 철회됐다(PDF pp.3–4).
- **“Experiments are computational only; no physical experiment” — `SUPPORTED`.** source가 현재 computational experiments only라고 직접 한정하고 physical/chemistry extension을 future work로 둔다(PDF pp.1, 4).

**Frozen description verdict:** `minor_revision`. 핵심 architecture와 수치는 실재하지만 replication/aggregation 역할, reviewer cohort, human candidate selection과 withdrawal, archive가 조건화하는 search의 층위를 명시해야 한다.

**Corrected description:**

> The Nature paper reports both the template-based AI Scientist and an expanded template-free mode. The latter uses a four-stage, LLM-guided agentic tree for computational machine-learning experiments. Methods specifies that replication nodes rerun parent experiments under different random seeds and aggregation nodes summarize them with mean and standard deviation, although this nine-page article does not display a generated paper's seed-level replication artifact. Its o4-mini five-review ensemble reached `0.69 ± 0.04` balanced accuracy on a 2017–2024 pre-cutoff ICLR cohort and `0.66 ± 0.03` on a 2025 post-cutoff cohort; neither value is calibration evidence, and the human `0.66` comparator comes from a separate NeurIPS consistency experiment. An idea archive conditions later ideation, but the paper does not establish that it gates experiment-tree search. After human candidate filtering, three generated papers entered an ICLR workshop review and one exceeded the workshop score threshold; all were withdrawn under a pre-established protocol. The reported experiments are computational only.

## Overall Verdict

**Overall verdict: `major_revision`.**

source identity와 9쪽 전문은 정확하다. The AI Scientist가 idea generation, computational experiments, manuscript writing과 automated review를 연결하고, template-free mode에서 staged agentic tree, replication/aggregation, reviewer benchmark와 external workshop review를 보고한다는 핵심 citation은 유효하다. 따라서 source가 무관하거나 잘못 귀속된 `citation_invalid`는 아니다.

그러나 `EN-C028`의 load-bearing 해석은 크게 수정해야 한다. `0.69 ± 0.04`는 일반적 reviewer reliability나 calibration이 아니라 특정 **2017–2024 pre-cutoff ICLR cohort의 balanced accuracy**이고, human `0.66`은 별도 NeurIPS consistency study다. replication과 aggregation은 computational robustness mechanism이지만 hypothesis acceptance gate라고 자동 판정할 수 없다. external workshop review는 인간이 후보를 선별한 별도 연구 평가이며 system-internal autonomous `V_h` layer가 아니다. 높은 FPR은 false-positive bias concern을 부분적으로 뒷받침하지만, source는 automated reviewer를 experiment/search/submission의 internal gate로 입증하지 않으며 calibration을 분석하지도 않는다. 따라서 **“uncalibrated” label과 “internal acceptance gate”는 각각 `UNSUPPORTED`**다.

나머지 occurrence는 system membership과 end-to-end artifact generation을 대체로 지지하지만, field-wide proliferation/shared vocabulary absence와 four-system validator relationship을 source finding처럼 쓰지 말고 원고의 cross-system synthesis로 표시해야 한다. frozen description은 대체로 맞아 minor qualification으로 고칠 수 있으나, 본문 핵심 validator paragraph의 오류가 overall `major_revision`을 결정한다.

## Completion Checklist

- [x] RUBRIC의 필수 heading 11개를 정확한 이름으로 모두 사용했다.
- [x] PDF, BibTeX, manifest로 title, 8인 authors, journal, volume/pages, year, DOI, SHA-256, page count, version status를 확인했다.
- [x] 지정된 로컬 PDF p.1부터 p.9까지 순서대로 모두 읽었다.
- [x] Figure 1, Table 1, Figure 2, Figure 3이 있는 PDF pp.2–5를 렌더링해 layout과 수치를 시각 확인했다.
- [x] problem/context, prior work, document structure, two modes, experiment tree, reviewer benchmark, workshop study, quantitative findings, limitations를 분석했다.
- [x] reviewer `0.69`와 post-cutoff `0.66`, 별도 human `0.66`의 cohort/protocol 차이를 확인했다.
- [x] `0.69 ± 0.04`가 pre-cutoff balanced accuracy이지 calibration evidence가 아님을 benchmark 설계·metric과 대조했다.
- [x] replication nodes와 aggregation nodes의 역할을 분리했다.
- [x] replication mechanism의 Methods 기술과 generated-output 직접 시연 부재를 구분했다.
- [x] system-internal computation, automated review, human candidate selection, external peer review를 구분했다.
- [x] manifest의 EN link 4개와 KO link 3개를 각각 독립 판정했다.
- [x] 영어·한국어 parity를 `equivalent`, `added`, `meaning_shifted`로 대조했다.
- [x] frozen supplementary description의 모든 clause를 page-grounded하게 판정하고 교정문을 제시했다.
- [x] source author claim과 SERVO/framework interpretation을 구분했다.
- [x] 세 support lane `identity-and-system-description.md`, `claims-and-parity.md`, `methods-numbers-limitations.md`의 완료 근거를 primary report와 대조하고 판정 차이를 해소했다.
- [x] 지정된 source 이외의 PDF를 열지 않았고 API/model call을 사용하지 않았다.

AUDIT_COMPLETE: yes
PAGES_COVERED: 1-9
EN_LINKS_COVERED: EN-C001:lu2026aiscientist, EN-C003:lu2026aiscientist, EN-C013:lu2026aiscientist, EN-C028:lu2026aiscientist
KO_LINKS_COVERED: KO-C001:lu2026aiscientist, KO-C008:lu2026aiscientist, KO-C022:lu2026aiscientist
SYSTEM_DESCRIPTION_ASSESSED: yes
VERDICT: major_revision
