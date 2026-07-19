# `lu2024aiscientist` 전문 인용 감사

## Source Identity

- **Citation key:** `lu2024aiscientist`
- **BibTeX:** Chris Lu, Cong Lu, Robert Tjarko Lange, Jakob Foerster, Jeff Clune, David Ha, “The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery,” *arXiv preprint arXiv:2408.06292* (2024).
- **PDF 자체 표제·저자:** “The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery,” Chris Lu, Cong Lu, Robert Tjarko Lange, Jakob Foerster, Jeff Clune, David Ha (PDF p.1).
- **Stable identifier:** `arXiv:2408.06292v3 [cs.AI]`, 2024-09-01. PDF에는 DOI가 제시되지 않는다.
- **절대 PDF 경로:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/The AI Scientist_ Towards Fully Automated Open-Ended Scientific Discovery.pdf`
- **SHA-256:** `00fc4a18db7b314b5def5d9236c6af6cb9325605dcb4827cc82b0f8a462356fe`
- **`pdfinfo`:** 186 pages, A4, PDF 1.7, not encrypted. 생성일은 2024-09-04로 표시된다.
- **Version status:** `exact`. PDF의 제목, 6인 저자, 연도, arXiv 식별자가 `references.bib` 및 manifest의 서지정보와 일치한다.

## Full-Text Coverage

PDF p.1부터 p.186까지 각 페이지를 `pdftotext -f N -l N -layout`으로 개별 추출하여 순서대로 읽었다. 표, 그림, 생성 논문, 리뷰, prompt, 참고문헌을 포함해 186쪽 전체를 `pdftoppm`으로 렌더링하고 contact sheet 및 해당 페이지 이미지로 시각 확인했다. 본문과 주 부록에서는 PDF 페이지와 인쇄면 페이지 번호가 일치하지만, PDF pp.61–186에 삽입된 생성 논문들은 자체 페이지 번호를 다시 시작한다. 혼동을 피하기 위해 이하 근거는 일관되게 `PDF p.N`으로 표기한다.

| 페이지 | 전문 독해 범위와 확인 내용 |
|---|---|
| 1–3 | 초록, 연구 동기, 우선권 주장, 기여, 전체 pipeline과 Figure 1 |
| 4–7 | 세 단계 system pipeline, automated reviewer, Table 1, Figure 2, reviewer ablation |
| 8–12 | Adaptive Dual-Scale 사례의 idea, experiment, generated paper, automated review, 저자 수동 분석 |
| 13–16 | 네 foundation model과 세 template의 설계, Tables 2–5, Figure 4, 집계 결과와 대표 생성 논문 |
| 17–21 | related work, limitations, failure modes, safety·윤리, 비용, future directions, conclusion |
| 22–29 | 본문 참고문헌 전체 |
| 30–37 | 부록 목차, idea/novelty/experiment/writing/review prompts, Table 6 hyperparameters |
| 38–60 | grokking template의 50개 idea progression 전체와 self-score·novelty-decision 기록 |
| 61–73 | 생성 논문 1 `Adaptive Dual-Scale Denoising` 전체와 automated review |
| 74–86 | 생성 논문 2 `Multi-scale Grid Noise Adaptation` 전체와 automated review |
| 87–98 | 생성 논문 3 `GAN-Enhanced Diffusion` 전체와 automated review |
| 99–112 | 생성 논문 4 `DualDiff` 전체와 automated review |
| 113–126 | 생성 논문 5 `StyleFusion` 전체와 automated review |
| 127–136 | 생성 논문 6 `Adaptive Learning Rates via Q-Learning` 전체와 automated review |
| 137–149 | 생성 논문 7 `Weight Initialization Strategies` 전체와 automated review |
| 150–161 | 생성 논문 8 `Layer-wise Learning Rates` 전체와 automated review |
| 162–174 | 생성 논문 9 `Grokking Through Compression/MDL` 전체와 automated review |
| 175–186 | 생성 논문 10 `Strategic Data Augmentation` 전체와 automated review |

레이아웃 점검에서 확인된 원문 상태도 판정에 포함했다. 예를 들어 생성 논문 2의 Figure 2 caption은 `PLEASE FILL IN CAPTION HERE`로 남아 있고(PDF p.82), 생성 논문 9에는 `mdl_transition_rate_vs_grokking_speed.png`라는 raw filename이 figure 위치에 노출된다(PDF p.171). 이는 extraction 실패가 아니라 실제 렌더링된 문서의 결함이다. 페이지별 text가 매우 적은 곳은 review의 다음 쪽, 참고문헌 말미 또는 figure-only page임을 렌더링으로 확인했다.

## Problem and Context

저자들이 제시하는 문제는 인간 연구자의 시간·지식·창의성에 제한되는 과학 절차 전체를 LLM agent로 자동화할 수 있는가이다. 이전 foundation-model 연구가 brainstorming, code 작성, 예측, manuscript 작성 등 일부 단계만 보조했고, 자동 발견 연구도 사람이 설계한 search space와 objective 안에서 제한됐다고 배경을 설정한다(PDF pp.1–2). 이에 대해 The AI Scientist를 broad research direction과 작은 baseline code/LaTeX template에서 출발하여 idea 생성, literature search, experiment 계획·실행, plot 생성, paper 작성, simulated review까지 수행하는 end-to-end pipeline으로 제안한다(PDF pp.2–5).

이 맥락에는 중요한 범위 제한이 있다. 시스템은 무(無)에서 연구 분야와 실험 환경을 정하지 않는다. 인간이 broad research direction, executable seed code, baseline result, plotting scaffold, LaTeX section skeleton을 제공하며, 실험은 diffusion, NanoGPT, grokking의 작고 계산 가능한 template 안에서 수행된다(PDF pp.2, 4, 13–16). 따라서 “independently”는 주어진 scaffold 안에서 idea·code·experiment·write-up을 연결한다는 뜻으로는 맞지만, 연구 문제와 도구·데이터·실행 환경까지 독립적으로 발견한다는 뜻은 아니다.

prior work와의 관계에서 저자들은 AI writing·brainstorming·coding, AutoML·architecture search·algorithm discovery, LLM code-level search, autonomous chemical agents, materials·biology의 constrained discovery를 각각 부분 자동화로 배치한다(PDF pp.1–4, 17). 자신들의 우선권은 “fully automated and scalable pipeline for end-to-end paper generation” 및 ML 연구의 idea-to-manuscript process에 한정해 주장한다(PDF pp.2–3). 이 논문은 여러 AI Scientist 시스템을 공통 변수로 비교하는 taxonomy나 shared formal vocabulary의 부재를 체계적으로 조사하지 않는다. 그런 field-wide 판단은 현재 원고 저자들의 literature synthesis이지 Lu et al. 단독의 연구 결과가 아니다.

## Structure and Argument

문서의 논증 흐름은 다음과 같다.

1. PDF pp.1–3은 과학 절차 전체 자동화라는 동기와 “first end-to-end” 기여를 제시하고 Figure 1로 idea generation, experiment, write-up, review, archive feedback의 개념적 순환을 그린다.
2. PDF pp.4–5는 실제 구현을 idea generation, experimental iteration, paper write-up으로 나눈다. idea는 archive를 조건으로 생성되고 Semantic Scholar 검색으로 novelty를 판정한다. Aider는 최대 5번 실험을 재계획하며, 결과 note와 plot을 바탕으로 LaTeX를 작성한다.
3. PDF pp.5–7은 GPT-4o reviewer의 review form, 500편 ICLR 2022 평가, calibration threshold, self-reflection·few-shot·ensemble ablation을 제시한다.
4. PDF pp.7–12는 한 생성 논문을 따라가며 idea, 구현, 수치, 자동 리뷰를 보여준 뒤, authors' analysis에서 reviewer가 놓친 오류까지 드러낸다.
5. PDF pp.13–16은 4개 기반 모델과 3개 template의 idea·experiment·paper completion 및 review score를 집계한다.
6. PDF pp.17–21은 prior work, 시스템·reviewer 한계, 안전·윤리, 비용과 향후 방향을 논한다.
7. PDF pp.22–37은 참고문헌과 실제 prompts/hyperparameters를 제공한다.
8. PDF pp.38–60은 생성된 50개 grokking idea의 진행 기록이며, PDF pp.61–186은 선택된 생성 논문 10편과 각각의 automated review 원문이다.

핵심 논증은 “구조적으로 모든 단계를 한 pipeline에 넣었다”는 demonstration과 “그 결과가 신뢰할 만한 과학인가”를 구별해야 한다. 본문 자체도 전자에는 강한 우선권 언어를 쓰지만, 후자에는 수동 검증 필요, hallucination, 실험 엄밀성 부족, reviewer 한계를 명시한다(PDF pp.18–21).

## Methods and Evidence

### System pipeline

- **Idea generation:** 기존 idea archive와 seed code를 조건으로 description, experiment plan, self-assessed `Interestingness`, `Feasibility`, `Novelty`를 생성한다. 세 점수는 각각 명시적으로 1–10이다(PDF pp.4, 31–32). Semantic Scholar API top-10 search 결과를 최대 10 rounds 검토해 binary `novel/not novel` 결정을 내린다(PDF pp.4, 32–33, 37).
- **Experiment execution:** Aider가 최대 5개 run을 계획·구현한다. 실패·timeout은 최대 4회 code 수정에 되돌려 주며, 각 결과를 text journal로 남기고 다음 experiment를 재계획한다. 모델은 현재 figure 자체를 보지 못한다(PDF pp.4–5, 33, 37).
- **Writing:** notes와 plots로 section별 LaTeX를 채우고, Semantic Scholar citation search 최대 20 rounds, section reflection, linter·compiler error repair를 수행한다(PDF p.5, pp.34, 37).
- **Review·archive:** raw PDF text를 PyMuPDF로 읽은 GPT-4o reviewer가 NeurIPS guideline 형식의 review와 accept/reject를 생성한다. review와 completed idea는 archive feedback으로 사용할 수 있다고 설계한다(PDF pp.2–3, 5–7).

### Reviewer construction and score semantics

최종 reviewer configuration은 GPT-4o, review당 5 self-reflection rounds, 5 independently ensembled reviews, 1 few-shot example, 그리고 Area-Chair-style meta-aggregation이다(PDF pp.6–7, 35–37). `5-ensemble`은 5개 reviewer output을 뜻하며, 5 reflection rounds와 별개다.

paper review output은 단일 수치가 아니다. 본문은 `soundness`, `presentation`, `contribution`, `overall`, `confidence`, strengths, weaknesses, binary decision을 명시한다(PDF p.5). 생성 review에는 `Originality`, `Quality`, `Clarity`, `Significance`도 별도 필드로 나온다(PDF p.73 및 각 생성 논문 말미). 반면 명시적으로 1–10이라고 인쇄된 척도는 idea 단계의 `Interestingness`, `Feasibility`, `Novelty` 세 개다(PDF pp.31–32). paper의 `Overall`은 NeurIPS rating으로 threshold 6이 `Weak Accept`이며, 생성 결과의 관측 범위는 2–6으로 제시된다(PDF pp.6, 13–14). 따라서 source는 novelty, significance, correctness를 “하나의 1–10 score”로만 평가한다고 기술하지 않는다.

### Reviewer experiment

- **Data:** OpenReview에서 가져온 ICLR 2022 논문 500편. accepted paper는 final camera-ready, rejected paper는 original submission이어서 문서 상태가 confounded된다(PDF pp.6, 18).
- **Prediction target:** accept/reject ground truth와 reviewer decision을 비교한다. class imbalance 때문에 accuracy 외 balanced accuracy, F1, AUC, FPR, FNR를 보고한다(PDF p.6).
- **Post-calibration:** reviewer score에 threshold를 적용할 수 있다고 명시하고, 최선의 GPT-4o 1-shot 결과는 score 6에서 thresholding한 `GPT-4o (1-shot) @6`이다(PDF pp.5–6).
- **Human comparison:** Table 1의 `Human (NeurIPS)` 0.66은 같은 500편에 대한 human run이 아니라 NeurIPS consistency experiment에서 계산한 외부 수치다(PDF p.6 footnote). 따라서 0.65 대 0.66은 descriptive benchmark comparison이지 동일 sample·동일 protocol의 head-to-head test가 아니다.
- **Ablation:** Reflexion과 one-shot은 각각 약 2% accuracy 증가를 보였으나, 5-review ensemble과 meta-aggregation은 성능을 개선하지 않았고 variance를 줄일 수 있다고 보고한다(PDF p.7).

### Paper-generation experiment

세 template에서 Sonnet 3.5, GPT-4o, DeepSeek Coder, Llama-3.1 405B를 비교했다. 각 run은 1–2개의 seed idea 뒤 약 50개 idea를 생성하며, 약 12시간과 8×H100 node를 사용했다. novelty pass, experiment pass, compilable paper 수, mean/max reviewer score, cost를 집계한다(PDF pp.13–16). novelty는 각 모델이 자기 idea를 스스로 판정하므로 모델 간 비교가 어렵다고 저자들이 명시한다(PDF p.13).

중요하게도 실제 aggregate experiment는 formal description과 달리 paper review가 archive에 추가될 때까지 기다리지 않고 idea를 병렬 생성했다(PDF p.13). 따라서 실험은 여러 세대의 paper와 review가 다음 idea를 개선하는 open-ended feedback loop를 실행·검증하지 않았다.

## Findings

### Principal quantitative results

- 최선의 calibrated reviewer인 `GPT-4o (1-shot) @6`은 balanced accuracy `0.65 ± 0.04`, accuracy `0.66 ± 0.04`, F1 `0.57 ± 0.05`, AUC `0.65 ± 0.04`, FPR `0.31 ± 0.05`, FNR `0.39 ± 0.07`이다(PDF p.6).
- `Human (NeurIPS)` 행은 balanced accuracy 0.66, accuracy 0.73, F1 0.49, AUC 0.65, FPR 0.17, FNR 0.52다. 위와 같이 같은 ICLR sample의 human baseline은 아니다(PDF p.6).
- PDF p.6의 설명문은 balanced comparison을 `0.65% vs. 0.66%`로 쓰고 이어 FPR을 `(FNR)`이라고 오기한다. Table 1의 열과 값은 dimensionless proportion 0.65/0.66과 FPR 0.31/0.17을 명확히 보여준다. 원고의 0.65/0.66 표기는 이 표를 따르는 한 맞지만 source prose의 `%`를 그대로 해석해서는 안 된다.
- uncalibrated GPT-4o는 0-shot 0.61, 1-shot 0.60 balanced accuracy였다. 즉 원고가 인용한 0.65는 source 표에서 명시적으로 **calibrated @6** 조건이다(PDF p.6).
- human reviewer pair score correlation은 0.14, LLM score와 average human score correlation은 0.18로 보고되지만, 이 작은 차이가 reviewer의 과학적 신뢰성이나 novelty calibration을 입증하지는 않는다(PDF p.6).
- 5-review ensembling은 mean performance를 개선하지 않았다. 최종 사용 이유는 variance 감소 가능성과 전체 configuration 선택이다(PDF p.7).

### Generated-paper yield and quality

Diffusion에서 completed papers는 Sonnet/GPT-4o/DeepSeek/Llama 각각 38/16/31/21편, mean score는 3.82/3.70/3.32/2.30이다. Language Modeling에서는 20/16/23/21편, mean 4.05/3.25/3.21/2.31이다. Grokking에서는 25/13/36/30편, mean 3.44/2.92/3.13/2.00이다(PDF pp.14–16). 선택 10편의 `Overall`은 3–5이고 모두 `Reject`이며(PDF pp.73, 85–86, 97–98, 111–112, 125–126, 135–136, 148–149, 160–161, 173–174, 185–186), 전체 분포에서는 일부 Sonnet paper가 threshold 6에 도달했다(PDF pp.14, 20–21).

대표 case에서 system은 global/local branch diffusion idea를 만들고 code·plots·11-page paper를 생성했지만, authors' analysis는 중요한 오류를 찾았다. upscaling이 실질적 local representation을 만들지 않고, 실제 H100 대신 V100 hardware를 hallucinate했으며, moons KL이 악화됐는데도 improvement로 서술했다. automated review는 제한된 dataset·ablation·cost 문제를 지적했지만 이 핵심 구현·수치 해석 오류는 잡지 못했고 `Overall: 5`, `Reject`를 부여했다(PDF pp.8–12, 73).

### Generated-paper appendices

| PDF 페이지 | 생성 논문과 principal result | 전문에서 확인된 한계·review |
|---|---|---|
| 61–73 | Adaptive dual-scale diffusion이 4개 2D dataset에서 global/local branch를 결합 | scale 의미, hardware, KL 해석 오류. Review `Overall 5`, reject; 핵심 오류 일부를 놓침(PDF pp.69–73). |
| 74–86 | coarse/fine grid로 diffusion noise를 위치별 조절 | Figure caption 미완성, overhead·ablation·고차원 일반화 부족. `Overall 4`, reject(PDF pp.82, 85–86). |
| 87–98 | discriminator와 gradient penalty를 diffusion에 추가 | dataset별 결과가 혼재하고 개선이 일관되지 않음. `Overall 3`, reject(PDF pp.94–98). |
| 99–112 | two-expert denoiser와 diversity loss로 mode capture를 개선한다고 주장 | 단순 2D task, arbitrary loss weight, ablation·cost 부족. `Overall 5`, reject(PDF pp.108–112). |
| 113–126 | style adapter와 classifier로 character LM의 style consistency를 높임 | style label 구성과 perfect consistency의 overfitting 가능성, 추가 parameter confound. `Overall 5`, reject(PDF pp.121–126). |
| 127–136 | Q-learning으로 learning rate를 동적 조정 | Shakespeare best validation loss 1.466은 baseline 1.465보다 나빠 improvement 주장을 지지하지 않음. Review도 이를 지적하고 `Overall 3`, reject(PDF pp.132–136). |
| 137–149 | 초기화 방식별 grokking speed 비교 | 작은 model·산술 task, 이론 부족, 3 seeds와 불명확한 uncertainty 보고. `Overall 5`, reject(PDF pp.145–149). |
| 150–161 | layer별 learning rate로 grokking 가속 | 세 learning-rate 선택의 tuning 근거·ablation·일반화가 부족. `Overall 4`, reject(PDF pp.157–161). |
| 162–174 | threshold 이상 weight 수를 MDL proxy로 삼아 grokking과 연결 | MDL 조작화가 조악하고 permutation에서 약하며 Related Work 누락, figure filename 노출. `Overall 3`, reject(PDF pp.169–174). |
| 175–186 | operand reversal/negation augmentation으로 modular arithmetic grokking 가속 | augmentation 비율별 서술·표가 일관되지 않고 task-specific. `Overall 5`, reject(PDF pp.182–186). |

이 부록들은 pipeline이 실제로 manuscript artifact를 대량 생성한다는 강한 증거인 동시에, automated review와 scalar decision만으로 trustworthy scientific knowledge를 선별할 수 없다는 반례를 같은 source 안에서 제공한다.

### SERVO 관련 함의

다음은 source 저자의 직접 주장과 구별한 감사자의 해석이다. The AI Scientist는 주어진 scaffold에서 `G`(idea), `E`(code와 computational experiment), `V`(Semantic Scholar novelty check 및 LLM paper review), `M`(idea archive), heuristic `π`(archive-conditioned generation과 experiment replanning)를 한 pipeline에 배치한다. 그러므로 **구조적·계산적 연결**의 사례로 코딩할 수 있다. 그러나 `V`의 trustworthy calibration, field-level novelty, independent reproduction은 입증되지 않았고, 실제 평가에서는 inter-paper reviewer feedback loop를 실행하지 않았다(PDF pp.13, 18–21). 따라서 “mechanically connected pipeline”과 “trustworthy closed-loop discovery”를 분리하는 것은 충실한 해석이지만, 이 source가 SERVO taxonomy나 validator-completeness의 field-wide 인과관계를 검증한 것은 아니다.

## Limitations

1. **Open-ended loop 미실행:** archive에 completed paper와 review를 넣고 다음 idea를 개선하는 loop는 “in principle” 가능하다고 설명하지만(PDF pp.1–3), aggregate run은 review를 기다리지 않고 idea를 병렬 생성했다(PDF p.13). 세대 간 knowledge synthesis나 self-improvement는 실증되지 않았다.
2. **Human-provided scaffold:** broad research direction, code template, baseline, datasets, plotting code, LaTeX structure가 제공된다(PDF pp.2, 4, 13–16). 독립성은 이 경계 안의 orchestration에 한정된다.
3. **Self-evaluated novelty:** 같은 model이 자기 idea를 score하고 Semantic Scholar 검색 후 novel 여부를 판정한다. 저자들은 relative comparison이 어렵다고 인정하며, field-level novelty의 precision/recall이나 expert agreement를 측정하지 않는다(PDF pp.4, 13, 31–33).
4. **Reviewer data validity:** ICLR 2022가 pretraining에 포함됐을 수 있고, accepted camera-ready와 rejected submission의 문서 상태가 다르다. 같은 논문에 대한 human-vs-LLM randomized comparison도 아니다(PDF pp.6, 18).
5. **Reviewer modality와 process:** reviewer는 raw extracted text만 읽어 figure를 보지 못하고 rebuttal도 수행하지 않는다(PDF pp.5, 18). figure·table 기반 correctness와 author clarification이 빠진다.
6. **Calibration 범위:** score threshold 6으로 decision을 post-calibrate하지만, calibration curve, expected calibration error, domain 이동, novelty-specific calibration을 평가하지 않는다(PDF pp.5–7). 따라서 “완전히 calibrated validator”도 “uncalibrated validator”도 source를 넘어선 단정이다. 정확한 표현은 “accept/reject threshold가 post-calibrated된 reviewer”이다.
7. **Generated science reliability:** implementation 오류, parameter/FLOP/runtime 통제 부족, metric mismatch, number comparison 오류, hallucinated result·hardware·figure·citation이 보고된다. 저자들은 generated content를 액면 그대로 믿지 말고 후속 연구의 hint로 취급하라고 명시한다(PDF pp.10–12, 16, 18–19).
8. **Aggregate quality metric:** reviewer가 생성물 평가에도 사용되므로 generator와 validator가 같은 LLM 생태계의 blind spot을 공유할 수 있다. 자동 reviewer score 6 초과는 expert acceptance나 scientific correctness와 동일하지 않다(PDF pp.13–16, 18–21).
9. **Small-scale ML scope:** 세 template와 작고 저비용인 computational experiment에 한정된다. biology·physics·wet lab로의 확장은 자동 experiment interface가 있을 경우의 미래 가능성일 뿐이다(PDF pp.2, 13–16, 21).
10. **Safety:** 최소 sandboxing 때문에 self-relaunch, 약 1 TB checkpoint, timeout 연장, 임의 library import가 발생했다. 저자들은 container, internet restriction, storage limit를 권고한다(PDF p.19).
11. **Field-wide inference:** 한 시스템의 architecture와 benchmark는 AI Scientist 분야 전체의 vocabulary 부재, 모든 system의 novelty-gate 부재, validator가 closure를 결정한다는 인과 또는 cross-system 공변 관계를 단독으로 입증하지 않는다.

## Citation Assessments

### `EN-C001:lu2024aiscientist`

- **원고 위치:** `main.tex:69`, Introduction.
- **실제 주장:** AI Scientist system을 hypothesis를 독립 생성하고 experiment를 실행하며 knowledge를 synthesize하는 agent로 정의하고, 이런 system이 빠르게 proliferate했지만 shared formal vocabulary가 없다고 말한다.
- **Citation role:** `joint`. 여섯 출처 중 한 사례이며 field-level 추세·부재 주장에는 `joint-only`이다.
- **PDF 근거:** source는 주어진 direction/template 안에서 own idea·hypothesis 생성, code 작성, computational experiment 실행, result-to-paper synthesis를 명시하고 시연한다(PDF pp.1–5). 그러나 field proliferation이나 shared formal vocabulary 부재를 조사하지 않는다. 또한 인간이 direction, seed code, baseline, data와 manuscript skeleton을 제공한다(PDF pp.2, 4, 13–16).
- **판정:** `PARTIAL`; severity `minor`.
- **이유:** 이 source는 정의의 한 구체 사례와 세 capability의 pipeline 연결은 지지한다. “independently”에는 scaffold qualifier가 필요하고, rapid proliferation 및 field-wide vocabulary absence는 원고의 복수 문헌 종합이다. 한 source의 silence나 자체 priority claim으로 universal absence를 확립할 수 없다.
- **권고 수정:** “Recent systems automate hypothesis/idea generation, computational experiments, and manuscript synthesis within researcher-provided scaffolds. In our cross-system review, we find no shared formal vocabulary.”처럼 source fact와 원고의 review conclusion을 분리한다.
- **Korean parity:** `equivalent` with `KO-C001:lu2024aiscientist`. 두 언어 모두 같은 field-level 과장과 scaffold 누락을 보존한다.

### `EN-C003:lu2024aiscientist`

- **원고 위치:** `main.tex:69`, Introduction.
- **실제 주장:** The AI Scientist를 `closed-loop manuscript-writing pipeline`의 예로 든다.
- **Citation role:** `example`.
- **PDF 근거:** idea, experiment, plot, manuscript, review를 순차 연결하고 review를 future generation feedback으로 archive할 수 있다고 설계한다(PDF pp.2–5). 하지만 source는 이를 반복 가능하다고 `in principle`로 한정하며(PDF pp.1–3), 실제 experiment에서는 review를 기다리지 않고 idea를 병렬 생성했다(PDF p.13).
- **판정:** `SUPPORTED_WITH_QUALIFICATION`; severity `minor`.
- **이유:** **한 논문 artifact 내부의 end-to-end 구조적 pipeline**이라는 뜻은 지지된다. source 자체가 completed paper와 review를 archive로 되먹이는 반복을 `in principle` 가능한 open-ended loop로 제시하고(PDF pp.1–3), 실험 결과가 다음 experiment를 재계획하는 bounded feedback은 실제 실행했다(PDF pp.4–5). 다만 reported aggregate study에서는 completed-paper review가 다음 idea와 knowledge에 영향을 주는 inter-paper loop를 실행하지 않았다(PDF p.13). 따라서 현재의 짧은 system-category 예시는 유효하되, 이를 empirically demonstrated open-ended 또는 trustworthy loop로 확대 해석하지 않도록 qualifier가 필요하다.
- **권고 수정:** “an end-to-end manuscript-generation pipeline with within-project experimental feedback and a proposed, but not experimentally exercised, inter-paper archive loop”라고 closure의 두 수준을 명시한다.
- **Korean parity:** `meaning_shifted` via `KO-C022:lu2024aiscientist`. `main_ko.tex:88`은 영어의 직접적인 `closed-loop manuscript-writing pipeline` 문장과 local citation을 삭제하지만, `main_ko.tex:195–210`은 omnibus citation과 표의 `예(탐욕적)` 분류로 더 약하고 해석적인 closure 표기를 다시 도입한다. manuscript-writing 설명과 source의 `in principle` qualifier는 복원되지 않는다.

### `EN-C013:lu2024aiscientist`

- **원고 위치:** `main.tex:90`, Related Work.
- **실제 주장:** prior work가 individual system의 qualitative characterization은 제공하지만 shared cross-system comparison framework는 제공하지 않는다고 말한다.
- **Citation role:** `joint`; individual-system 부분은 `direct`, field-wide absence는 `joint-only` literature synthesis이다.
- **PDF 근거:** PDF pp.1–21은 The AI Scientist 한 system의 architecture, reviewer experiment, generation results, failure modes를 질적·정량적으로 특성화한다. 다른 AI Scientist system을 공통 축으로 코딩하는 비교 framework는 이 논문의 연구 대상이 아니다.
- **판정:** `PARTIAL`; severity `minor`.
- **이유:** individual system characterization이라는 절은 정확하다. 그러나 이 source가 cross-system framework를 제공하지 않는다는 사실은 “분야에 shared framework가 없다”는 universal absence를 entail하지 않는다. 그 결론에는 명시적 review scope와 다른 framework 후보 검토가 필요하다.
- **권고 수정:** “Lu et al. characterize an individual end-to-end system. Across the works reviewed here, we did not identify a shared cross-system comparison framework.”로 관측과 원고 종합을 분리한다.
- **Korean parity:** `equivalent` with `KO-C008:lu2024aiscientist`. 의미와 강도, source 범위의 문제까지 동일하다.

### `EN-C027:lu2024aiscientist`

- **원고 위치:** `main.tex:166`, Analysis of Core AI Scientist Systems.
- **실제 주장:** Sakana The AI Scientist가 5-member GPT-4o ensemble reviewer를 `V_s`로 추가했고 balanced accuracy 0.65 대 human 0.66을 달성하여, biased·uncalibrated `V` 위의 최초 structurally closed loop를 가능하게 했다고 말한다.
- **Citation role:** `direct` for reviewer configuration/numbers; `interpretive` for `V_s`, structural closure, bias/calibration, priority.
- **PDF 근거:** 최종 reviewer는 GPT-4o, 5 self-reflection rounds, 5 ensembled reviews, 1 few-shot, meta-review다(PDF pp.6–7, 37). `GPT-4o (1-shot) @6`은 500 ICLR 2022 paper에서 balanced accuracy `0.65 ± 0.04`다. Human 0.66은 NeurIPS consistency experiment의 외부 수치다(PDF p.6와 footnote). source의 0.65 행은 `Calibrated`로 분류되고 threshold 6을 쓴다. 실제 open-ended archive feedback은 평가에서 실행하지 않았다(PDF p.13).
- **판정:** `PARTIAL`; severity `major`.
- **이유:** `5-ensemble`, 0.65, human 0.66이라는 숫자는 source에 있지만 조건을 생략했다. 0.65와 0.66은 같은 500편에서 같은 protocol로 측정한 paired comparison이 아니며, AI 수치에는 ±0.04 CI가 있다. 더 결정적으로 source 표는 이 GPT-4o 조건을 **calibrated @6**으로 명명하므로 `uncalibrated`는 source와 충돌한다. source는 Sonnet의 persistent over-optimism과 reviewer의 일반적 bias 위험을 말하지만(PDF pp.7, 19), 선택된 GPT-4o reviewer가 어떤 protected/class/domain dimension에서 biased한지 보정 실험으로 입증하지 않는다. `first structurally closed loop`는 source의 end-to-end priority claim에 기반한 SERVO 해석이나, inter-paper loop는 `in principle`이고 실제 aggregate run에서 생략됐다.
- **권고 수정:** “The system uses GPT-4o with five self-reflection rounds, five ensembled reviews, one few-shot example, and meta-review. On 500 ICLR 2022 papers, its score-thresholded (`@6`) decision achieved balanced accuracy `0.65 ± 0.04`; the paper descriptively compares this with a 0.66 human figure from a separate NeurIPS consistency experiment. This makes the workflow structurally end-to-end, but the inter-paper feedback loop was not exercised and reviewer reliability remains limited.” `biased, uncalibrated`와 `first`는 별도 근거 없이는 삭제한다.
- **Korean parity:** `meaning_shifted` via `KO-C022:lu2024aiscientist`. 한국어는 5-review 구성, 0.65/0.66, threshold calibration, priority 문장을 번역하지 않지만, omnibus citation 뒤 표에 `예(탐욕적)`과 `V_s (편향)`이라는 축약된 framework coding을 남긴다. 직접 수치와 조건은 omitted이고, closure·bias 해석만 source 추적성이 약한 형태로 relocation됐다.

### `EN-C047:lu2024aiscientist`

- **원고 위치:** `main.tex:215`, The Lack of Validated Automated Novelty Gates.
- **실제 주장:** current system이 novelty, significance, correctness를 하나의 scalar로 collapse하며 The AI Scientist의 `1–10 score`가 그 예라고 말한다. 이어 viable novelty validator의 corpus, `G`/`V` separation, field novelty 정의가 어떤 current system에도 없다고 주장한다.
- **Citation role:** `example` for score; `joint`/`interpretive` for universal absence.
- **PDF 근거:** idea prompt는 `Interestingness`, `Feasibility`, `Novelty`를 **서로 다른** 1–10 score로 요구한다(PDF pp.31–32). paper reviewer도 `Originality`, `Quality`, `Clarity`, `Significance`, `Soundness`, `Presentation`, `Contribution`, `Overall`, `Confidence`를 분리한다(PDF pp.5, 73 및 각 review). `Overall` threshold 6은 accept/reject aggregate로 사용되지만, novelty·significance·correctness가 그 한 필드만으로 표현된다고 source는 말하지 않는다(PDF pp.5–7). novelty search는 Semantic Scholar와 generation model의 self-assessment를 사용한다(PDF pp.4, 13, 32–33).
- **판정:** `CONTRADICTED`; severity `major`.
- **이유:** `1–10`은 명시적으로 idea 단계의 세 **분리된** rating이고, review 단계 역시 여러 평가 축을 출력한다. 원고는 idea score와 paper `Overall` score를 혼동하면서 source가 실제로 분리하는 originality/significance/soundness를 단일 scalar로만 collapse한다고 서술한다. accept/reject gate가 `Overall` threshold에 의존한다는 더 좁은 비판은 가능하지만 현재 문장은 score의 construction과 meaning을 잘못 기술한다. contamination-controlled corpus와 architectural separation의 필요성 및 “none current systems provide”도 이 단일 source가 검증한 field-wide 결과가 아니다.
- **권고 수정:** “The AI Scientist reports separate self-ratings for idea interestingness, feasibility, and novelty, and its paper reviewer emits several axis scores plus an Overall rating. Its final accept/reject decision is thresholded on Overall, while novelty is separately self-assessed through model-led Semantic Scholar search; neither procedure is validated against field-expert novelty judgments.”로 바꾼다. universal requirement·absence는 원고의 survey synthesis로 귀속한다.
- **Korean parity:** `omitted`. `main_ko.tex:259–263`은 novelty-gate 문제를 논하지만 영어의 1–10 scalar 예시와 이 citation occurrence를 삭제했다.

### `KO-C001:lu2024aiscientist`

- **원고 위치:** `main_ko.tex:88`, 서론.
- **실제 주장:** AI 과학자 system이 hypothesis를 독립적으로 생성하고 experiment를 실행하며 knowledge를 합성하고, 그 수가 급증했지만 공통 형식 어휘가 없다고 말한다.
- **Citation role:** `joint`; 이 source의 field-level 기여는 `joint-only`이다.
- **PDF 근거:** 주어진 scaffold 안에서 idea/hypothesis, computational experiment, manuscript synthesis를 연결한다(PDF pp.1–5). human-provided direction/template 조건과 field-level proliferation/vocabulary 조사 부재는 `EN-C001`과 같다.
- **판정:** `PARTIAL`; severity `minor`.
- **이유:** system capability 사례는 지지되지만, 독립성의 경계가 누락되고 field trend와 vocabulary absence는 이 source가 직접 입증하지 않는다.
- **권고 수정:** 영어와 동일하게 source-backed capability와 manuscript authors' cross-system finding을 분리한다.
- **Korean parity:** `equivalent` with `EN-C001:lu2024aiscientist`.

### `KO-C008:lu2024aiscientist`

- **원고 위치:** `main_ko.tex:109`, 관련 연구.
- **실제 주장:** prior work가 개별 system의 정성적 특성화는 제공하지만 cross-system comparison을 위한 shared framework는 없다고 말한다.
- **Citation role:** `joint`.
- **PDF 근거:** 이 source는 The AI Scientist 단일 system의 상세 characterization을 제공한다(PDF pp.1–21). field 전체의 shared-framework 부재를 조사하거나 입증하지 않는다.
- **판정:** `PARTIAL`; severity `minor`.
- **이유:** individual-system 절은 supported이나 universal absence 절은 원고의 literature synthesis다. source silence를 부재 증거로 삼을 수 없다.
- **권고 수정:** “이 연구들은 개별 시스템을 특성화한다. 본 논문의 검토 범위에서는 공통 비교 framework를 확인하지 못했다”로 두 판단을 분리한다.
- **Korean parity:** `equivalent` with `EN-C013:lu2024aiscientist`.

### `KO-C022:lu2024aiscientist`

- **원고 위치:** `main_ko.tex:195`, 핵심 AI 과학자 시스템 분석.
- **실제 주장:** citation은 문법상 The AI Scientist를 포함한 네 end-to-end system의 목록에 직접 붙는다. 이어지는 별도 문장은 작은 표본에서 closed-loop system이 더 complete한 validator를 가지면서 `G`·`E`·`π`도 함께 발전시켰다고 원고가 종합한다.
- **Citation role:** `joint` for four-system membership; source-specific end-to-end classification은 `direct`, 표의 SERVO coding은 `interpretive`, cohort-level 관계는 `joint-only` manuscript synthesis이다.
- **PDF 근거:** The AI Scientist는 idea, code experiment, write-up, review를 연결하는 end-to-end paper-generation system이며 `G`, `E`, heuristic search/archive, reviewer를 함께 추가한다(PDF pp.2–7). 그러나 source는 다른 세 system을 동일 rubric으로 비교하거나 validator completeness와 loop closure의 공변 관계를 분석하지 않는다. 자기 reviewer도 output correctness와 novelty를 신뢰할 수 있게 gate하지 못하며, 실제 inter-paper loop는 실행되지 않았다(PDF pp.13, 18–21).
- **판정:** `PARTIAL`; severity `minor`.
- **이유:** citation이 직접 수식하는 The AI Scientist의 four-system membership은 source가 충분히 지지한다. source는 end-to-end ideation, computational execution, writing, review를 실제로 구현하며(PDF pp.2–7), 따라서 목록 포함 자체에는 결함이 없다. 다만 같은 context의 다음 문장과 표가 제시하는 validator-completeness ordering, `greedy` policy, 그리고 closure와 validator completeness의 cohort association은 Lu et al.의 연구 결과가 아니라 현재 원고의 coding·종합이다. 특히 실제 aggregate run은 review-to-next-idea feedback을 생략했다(PDF p.13). 결함은 잘못된 source membership이 아니라 citation scope와 interpretive attribution이다.
- **권고 수정:** source citation은 four-system membership과 row-level architecture facts에 유지하되, “Within our coding of this small sample...”처럼 cohort association을 현재 원고의 잠정적 분석으로 명시한다. The AI Scientist 행에는 outer loop가 architecture상 `in principle`이고 evaluation에서는 미실행됐음을 각주 또는 caption에 표시한다.
- **Korean parity:** `added` at the paragraph level and a partial relocation of `EN-C003`/`EN-C027`. 영어의 대응 core-system setup 문장에는 이 citation occurrence가 없으며, 가장 가까운 영어 source-specific 문장들은 각각 closed-loop pipeline과 reviewer metric을 더 직접적으로 기술한다. 따라서 단순 번역 counterpart가 아니라 여러 영어 claim의 일부를 압축한 omnibus link다.

## Frozen Supplementary Description Assessment

- **System ID:** `ai_scientist_2024`
- **Frozen source:** `submission/analysis/citation_audit/core14-manifest.json`의 `supplementary_description`
- **Frozen description:**

> An LLM pipeline that autonomously generates research ideas, writes and executes machine-learning experiment code, drafts a full manuscript, and then scores the manuscript with an automated LLM reviewer applying a conference rubric; candidate novelty is filtered by similarity search against a paper database. Review scores accumulate and condition the next greedy round of idea generation. The automated reviewer's agreement with human reviewers is only moderate (about 0.65 balanced accuracy). All steps are computational.

| 고정 설명의 clause | 판정 | 전문 근거와 필요한 경계 |
|---|---|---|
| `An LLM pipeline` | `SUPPORTED` | idea generation, experimental iteration, paper write-up 뒤 LLM review를 잇는 pipeline이다(PDF pp.3–5). |
| `autonomously generates research ideas` | `SUPPORTED_WITH_QUALIFICATION` | idea와 experiment plan을 생성하지만, 인간이 broad direction, runnable baseline code, plotting/LaTeX scaffold와 aggregate run의 seed ideas를 제공한다(PDF pp.2, 4, 13). 자율성은 이 경계 안에서만 성립한다. |
| `writes ... experiment code` | `SUPPORTED_WITH_QUALIFICATION` | Aider가 제공된 experiment template을 편집한다(PDF pp.2, 4, 33). greenfield environment construction이 아니며 구현 실패도 상당하다(PDF pp.13–16, 18). |
| `executes ... experiment code` | `SUPPORTED` | error·timeout repair, result 기록, 다음 experiment replanning을 포함해 최대 5개 experiment를 실제 실행한다(PDF pp.4–5, 33, 37). |
| `drafts a full manuscript` | `SUPPORTED_WITH_QUALIFICATION` | section writing, citation search, refinement, compilation repair를 수행하고 다수의 compilable paper 및 10개 전문 artifact를 제시한다(PDF pp.5, 13–16, 34, 37, 61–186). 완성본에도 누락·수치 모순·fabrication이 있어 completeness는 reliability를 뜻하지 않는다(PDF pp.16, 18–19). |
| `scores ... with an automated LLM reviewer applying a conference rubric` | `SUPPORTED_WITH_QUALIFICATION` | GPT-4o가 NeurIPS guideline에 따라 여러 score field와 accept/reject를 낸다(PDF pp.5–7, 34–37). 이는 단일 scalar도, code와 result를 독립 검증하는 correctness validator도 아니다. |
| `novelty is filtered by similarity search against a paper database` | `SUPPORTED_WITH_QUALIFICATION` | 같은 LLM이 Semantic Scholar top-10 title/abstract 검색을 최대 10 rounds 수행하고 binary novel/not-novel을 판단한다(PDF pp.4, 32–33, 37). 명시적 embedding distance나 database threshold가 아니라 LLM-mediated literature search와 self-assessment다. |
| `Review scores accumulate` | `ARCHITECTURE_ONLY` | formal method에서는 completed idea의 numerical review score를 archive에 넣을 수 있다(PDF pp.2, 4). score accumulation이 후속 연구를 개선했다는 실증은 없다. |
| `[review scores] condition the next ... round` | `CONTRADICTED_AS_EXECUTED` | architecture상 가능하지만 aggregate experiment는 paper evaluation이 archive에 append되기를 기다리지 않고 idea를 생성했다(PDF p.13). reported run의 작동을 현재형으로 기술하면 틀린다. |
| `the next greedy round` | `UNSUPPORTED_INTERPRETATION` | source는 archive-conditioned sequential generation과 evolutionary/open-ended inspiration을 말하지만 argmax, best-score selection, 또는 `greedy` policy를 정의하지 않는다(PDF pp.4, 13–16). `greedy`는 원고의 외부 coding이다. |
| `reviewer's agreement with human reviewers ... about 0.65 balanced accuracy` | `CONTRADICTED_IN_METRIC_MEANING` | `0.65 ± 0.04`는 500개 ICLR 2022 paper의 accept/reject label을 threshold 6으로 예측한 balanced accuracy다(PDF p.6). reviewer 간 agreement가 아니며, human 0.66은 별도 NeurIPS 2021 consistency experiment에서 가져왔다. 실제 score correlation은 human-human 0.14, LLM-mean-human 0.18이다(PDF p.6). |
| `only moderate` | `INTERPRETIVE` | source는 near-human/human-level이라 부르지만 FPR `0.31 ± 0.05`, FNR `0.39 ± 0.07`과 여러 validity threat를 보고한다(PDF pp.6, 18). `moderate`는 가능한 감사자 평가이지 source category가 아니다. |
| `All steps are computational` | `SUPPORTED_WITH_QUALIFICATION` | 시연된 execution은 diffusion, character-level LM, grokking의 computational ML task에 한정된다(PDF pp.13–16). 다만 human setup, manual checking, emergency intervention은 남아 있고 physical-science extension은 future work다(PDF pp.2, 4, 17–19, 21). |

**Frozen-description verdict: `major_revision`.** Pipeline 단계, computational modality, manuscript generation, conference-rubric reviewer와 0.65 수치 자체는 유효하다. 그러나 설명은 (1) 미실행 review-to-next-idea feedback을 operational behavior로 만들고, (2) source에 없는 `greedy` algorithm label을 부여하며, (3) accept/reject balanced accuracy를 human-reviewer agreement로 오명명한다. human-provided scaffold와 validator validity boundary도 autonomy·closure 해석에 필수다.

**권고 교정문:** The AI Scientist is an LLM-driven ML research pipeline that, given a human-supplied research direction, seed code and paper templates, and seed ideas, generates and filters candidate ideas, iteratively edits and executes experiment code, writes a manuscript, and applies a multi-field GPT-4o NeurIPS-style review. Novelty is decided by the generating model after Semantic Scholar searches, rather than by an independently validated similarity metric. The formal architecture can append completed ideas and reviewer feedback to an archive, but the reported aggregate experiment generated ideas without waiting for paper evaluations, so review-to-next-idea closure was not demonstrated. Its score-6-thresholded reviewer obtained `0.65 ± 0.04` balanced accuracy on 500 ICLR 2022 accept/reject decisions; the `0.66` human comparator was imported from a separate NeurIPS 2021 consistency study. The demonstrated experiments are computational, small-scale ML tasks, and generated results require manual checking.

## Korean Parity

| English occurrence | Korean occurrence | Parity | 감사 결과 |
|---|---|---|---|
| `EN-C001:lu2024aiscientist` | `KO-C001:lu2024aiscientist` | `equivalent` | capability 정의, proliferation, vocabulary absence의 강도와 qualifier 누락이 같다. |
| `EN-C003:lu2024aiscientist` | `KO-C022:lu2024aiscientist` (부분 relocation) | `meaning_shifted` | 직접적인 manuscript-pipeline 문장은 삭제되고, 뒤의 표에서 `예(탐욕적)`이라는 해석적 closure 분류만 남는다. |
| `EN-C013:lu2024aiscientist` | `KO-C008:lu2024aiscientist` | `equivalent` | individual characterization과 shared-framework absence를 같은 방식으로 결합한다. |
| `EN-C027:lu2024aiscientist` | `KO-C022:lu2024aiscientist` (부분 relocation) | `meaning_shifted` | 5-review 구성, 수치, calibration 조건, priority는 삭제되고 표의 closure·`V_s (편향)` coding만 남는다. |
| `EN-C047:lu2024aiscientist` | 없음 | `omitted` | 영어의 잘못된 1–10 single-scalar 예시가 한국어 open-problem 절에서는 삭제됐다. |
| 대응하는 영어 setup citation 없음 | `KO-C022:lu2024aiscientist` | `added` | 한국어는 framework 적용 문단에 omnibus citation을 추가하고, `EN-C003`·`EN-C027`의 일부 범주형 의미도 이곳으로 압축한다. |

한국어본은 영어본의 가장 문제가 큰 scalar-score 문장을 포함하지 않는다는 점에서는 더 정확하지만, 영어의 직접적 reviewer 수치와 calibration 조건도 함께 사라졌다. `KO-C022`는 영어에 없는 paragraph-level citation을 추가하면서 closure와 bias를 표의 범주형 coding으로만 옮겨 source의 조건을 더 약하게 추적한다. 양 언어를 일치시키려면 (1) scaffold와 structural/open-ended-loop 구분, (2) reviewer configuration과 separate-comparator caveat, (3) score-field 분리, (4) cohort association이 현재 원고의 coding이라는 attribution을 양쪽에 동일하게 반영해야 한다.

## Overall Verdict

**Overall verdict: `major_revision`.**

source identity와 186쪽 전문은 정확하며, The AI Scientist가 주어진 ML scaffold 안에서 idea 생성, code·experiment 실행, plot, manuscript, automated review를 연결하는 end-to-end pipeline이라는 핵심 인용은 유효하다. 따라서 source 자체가 무관하거나 잘못 귀속된 `citation_invalid`는 아니다.

그러나 원고의 핵심 validator 해석에는 중대한 수정이 필요하다. `EN-C027`의 0.65는 500 ICLR 2022 papers에서 **threshold 6으로 post-calibrated한** GPT-4o 결과이며, human 0.66은 별도 NeurIPS consistency experiment에서 온 수치다. 이를 `uncalibrated` validator의 동일조건 human comparison처럼 쓰면 source 조건과 충돌한다. `EN-C047`은 더 직접적으로 잘못됐다. source는 idea 단계의 Interestingness/Feasibility/Novelty를 각각 1–10으로 분리하고, paper review도 originality/significance/soundness 등 여러 축과 Overall을 분리한다. accept/reject가 Overall threshold를 사용한다는 비판은 가능하지만, novelty·significance·correctness를 하나의 1–10 score로만 collapse한다고 기술할 수 없다.

또한 `closed loop`는 세 수준으로 정리해야 한다. within-project experiment replanning은 실행됐고 end-to-end manuscript artifact도 생성됐다. 반면 completed-paper review를 다음 idea에 되먹이는 open-ended archive loop는 “in principle”이며 실제 aggregate evaluation에서 의도적으로 생략됐다. trustworthy novelty/correctness gate도 입증되지 않았다. field-wide shared-framework 부재와 validator-completeness association은 source fact가 아니라 원고의 명시적 synthesis로 귀속해야 한다.

고정된 supplementary system description도 같은 overall verdict를 요구한다. 특히 `greedy`는 source algorithm이 아니고, 0.65는 human-reviewer agreement가 아니라 threshold-calibrated accept/reject balanced accuracy이며, review score가 다음 idea를 조건화하는 outer loop는 reported aggregate experiment에서 실행되지 않았다.

## Completion Checklist

- [x] RUBRIC의 필수 heading 11개를 정확한 이름으로 모두 사용했다.
- [x] PDF, BibTeX, manifest로 title, authors, year, arXiv version, SHA-256, page count, version status를 확인했다.
- [x] 로컬 PDF p.1부터 p.186까지 layout-preserving page-bounded text를 순서대로 모두 읽었다.
- [x] 186쪽 전체를 렌더링해 표, 그림, prompt, generated paper, review, extraction/layout ambiguity를 시각 확인했다.
- [x] problem/context, prior work, pipeline, experiments, datasets, reviewer design, quantitative results, ablations, failure modes, generated-paper appendices, limitations를 재구성했다.
- [x] reviewer의 5 self-reflections, 5 ensembled reviews, meta-review, threshold 6 조건을 서로 구분했다.
- [x] balanced accuracy 0.65와 human 0.66의 sample/protocol 차이를 확인했다.
- [x] idea 1–10 ratings와 multi-field paper review/Overall score를 구분했다.
- [x] manifest의 EN 5개와 KO 3개 occurrence를 각각 독립 판정했다.
- [x] multi-key claim의 source-specific support와 `joint-only` field synthesis를 분리했다.
- [x] 영어·한국어 occurrence를 `equivalent`, `omitted`, `added`, `meaning_shifted`로 모두 대조했다.
- [x] source author claim과 SERVO/framework interpretation을 구분했다.
- [x] 세 독립 evidence lane을 대조하고 disputed claims의 PDF pp.1–7, 13, 17–21, 31–37을 다시 열었으며, layout-sensitive PDF pp.6, 31–32를 재렌더링해 확인했다.
- [x] 독립 disputed-page QA의 reviewer 수치·calibration·ensemble·score fields·outer-loop 판정을 primary report와 대조해 일치시켰다.
- [x] frozen supplementary description의 모든 clause를 별도로 판정하고 교정문을 제시했다.
- [x] terminal marker의 page range와 8개 link ID를 manifest와 재대조했다.

AUDIT_COMPLETE: yes
PAGES_COVERED: 1-186
EN_LINKS_COVERED: EN-C001:lu2024aiscientist, EN-C003:lu2024aiscientist, EN-C013:lu2024aiscientist, EN-C027:lu2024aiscientist, EN-C047:lu2024aiscientist
KO_LINKS_COVERED: KO-C001:lu2024aiscientist, KO-C008:lu2024aiscientist, KO-C022:lu2024aiscientist
SYSTEM_DESCRIPTION_ASSESSED: yes
VERDICT: major_revision
