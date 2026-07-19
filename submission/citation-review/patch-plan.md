# 인용 정확성 패치 플랜 (14 FLAGGED occurrence → 9 수정 그룹)

**방침:** 이 문서는 검토용이다. 원고(main.tex / main_ko.tex)는 **승인 후** 별도 단계에서 적용한다.
각 수정은 `현재 verbatim → 제안 verbatim`으로 제시하며, EN/KO 비대칭(한쪽에만 존재하는 오류)을 명시한다.
근거는 `citation-review/ledger.tsv` 및 `findings.md`의 evidence를 요약한 것이다.

## 신규 bib 항목 (FIX 3 전제, 검증 요망)

```bibtex
@article{king2004robot,
  title={Functional genomic hypothesis generation and experimentation by a robot scientist},
  author={King, Ross D and Whelan, Kenneth E and Jones, Ffion M and Reiser, Philip G K and Bryant, Christopher H and Muggleton, Stephen H and Kell, Douglas B and Oliver, Stephen G},
  journal={Nature},
  volume={427},
  number={6971},
  pages={247--252},
  year={2004},
  doi={10.1038/nature02236}
}
```
> 저자 목록·페이지는 널리 알려진 값이나, 적용 전 1회 대조 권장.

## 요약 표

| # | 수정 | verdict | EN 위치 | KO 위치 | bib |
|---|---|---|---|---|---|
| 1 | +2.3 과대추정 → `schmidgall2025agentlab` | MISATTRIBUTION (C020,C102) | L166 | (L263 선택) | - |
| 2 | GNoME 736 → `merchant2023gnome` | MISATTRIBUTION (C099,C100) | L230, L444 | L280 | - |
| 3 | Robot Scientist 능동학습/베이즈 → `king2004robot` | MISATTR/OVERCLAIM (C045,C047,C048) | L85, L92, L94 | L111, L113 | **신규** |
| 4 | 순환 타당성에서 `aher2023turing` 제거 | MISATTRIBUTION (C087,C089) | L200, L448 | L377 | - |
| 5 | Aletheia formal → natural-language | MISCHAR (C022) | L69 | (해당없음) | - |
| 6 | SciMuse: 생성품질 → 선택/관심예측 | MISCHAR (C058) | L90 | L109 | - |
| 7 | cranmer 결정적탐색 → 확률적(유전) | MISCHAR (C074) | L440 | L369 | - |
| 8 | ChemCrow surrogate/beam → ReAct/RoboRXN | MISCHAR (C076) | L442 | L371 | - |
| 9 | park2023 full-factorial 완화 | CONTEXT-MISUSE (C091) | L448 | L377 | - |

---

## FIX 1 — Agent Laboratory +2.3 과대추정 오귀속 [C020, C102]

**근거:** `+2.3` 수치·"Agent Laboratory"는 `kim2026aireviewers`(AI 리뷰어 논문)에 **0회 등장**. 이 수치는 Agent Laboratory 원논문(`schmidgall2025agentlab`, 자동 6.1/10 vs 인간 3.8/10 = -2.3)의 자체 결과. 사실 자체는 정확, 인용 키가 틀림.

### EN — main.tex L166 (필수)
현재:
```
but documents $+$2.3-point systematic over-estimation relative to human PhD students---adding a $V$ layer does not guarantee completeness if the layer is unreliable~\citep{kim2026aireviewers}.
```
제안:
```
but documents $+$2.3-point systematic over-estimation relative to the human PhD-student reviewers of the same AI-generated papers---adding a $V$ layer does not guarantee completeness if the layer is unreliable~\citep{schmidgall2025agentlab}.
```
> 핵심: `\citep{kim2026aireviewers}` → `\citep{schmidgall2025agentlab}`. 부수(선택): "relative to human PhD students" → "relative to the human PhD-student reviewers of the same AI-generated papers" (비교 대상은 동일 논문을 채점한 인간 리뷰어이지, 박사과정생 본인 논문 대비가 아님).

### EN — main.tex L211 (변경 불필요)
L211의 `+2.3`은 직접 인용이 없고 `\citep{kim2026aireviewers}`는 뒤의 "45-expert evaluation" 절에 붙어 정당(C103/C104 ACCURATE). 무수정.

### KO — main_ko.tex L263 (선택적 parity)
KO에는 EN L166에 해당하는 core 문단이 없다. `+2.3`은 L263(미해결 문제)에서 산문으로 "Agent Laboratory의 LLM 심사위원은 ... 평균 $+$2.3점을 과대 추정했고"로 서술되고 **직접 인용이 없다**(kim 인용은 뒤 45-전문가 문장에 붙음, 정당). 오귀속은 아니므로 필수 아님.
- 선택: 명시성을 위해 "과대 추정했고" 뒤에 `~\citep{schmidgall2025agentlab}` 추가 가능.

---

## FIX 2 — GNoME 736 실험실현 수치 오귀속 [C099, C100]

**근거:** `736`은 `cheetham2024gnome`(Perspective)에 **0회 등장**. 736은 GNoME 원논문(`merchant2023gnome`)의 수치. cheetham은 "예측≠검증" 정성 논점에만 유효.

### EN — main.tex L230 (필수)
현재:
```
GNoME predicts 380,000 stable compounds via DFT~\citep{merchant2023gnome}, but only 736 have been independently experimentally realized~\citep{cheetham2024gnome}:
```
제안:
```
GNoME predicts 380,000 stable compounds via DFT~\citep{merchant2023gnome}, but only 736 have been independently experimentally realized~\citep{merchant2023gnome}:
```
> 736 인용 → `merchant2023gnome`. (동일 문장 앞에 이미 merchant 인용이 있으니 중복이 부담되면 736 뒤 `~\citep{cheetham2024gnome}`를 삭제만 해도 무방.)

### EN — main.tex L444 (필수, 분할)
현재:
```
of the predicted stable structures, only 736 have been independently experimentally realized, and critics note that predicted compounds should not be equated with validated materials exhibiting demonstrated functionality~\citep{cheetham2024gnome}.
```
제안:
```
of the predicted stable structures, only 736 have been independently experimentally realized~\citep{merchant2023gnome}, and critics note that predicted compounds should not be equated with validated materials exhibiting demonstrated functionality~\citep{cheetham2024gnome}.
```
> 736 → `merchant2023gnome`; cheetham은 정성 논점에만 유지.

### KO — main_ko.tex L280 (필수)
현재:
```
736개만이 독립적으로 실험 실현되었다~\citep{cheetham2024gnome}:
```
제안:
```
736개만이 독립적으로 실험 실현되었다~\citep{merchant2023gnome}:
```
> **KO L373(재료 app-domain)에는 736 수치가 없음** — "예측된 안정 구조 대부분은 여전히 합성·특성화·기능 검증이 필요하다~\citep{cheetham2024gnome}"는 정성 논점(C101 ACCURATE)이므로 무수정. 즉 KO는 L280 한 곳만.

---

## FIX 3 — Robot Scientist 능동학습/베이즈-최적 실험선택 오귀속 [C045, C047, C048]

**근거:** `sparkes2010robot`(2010 리뷰)에는 "active learning"·"Bayes" **0회**. 능동학습·비용기반 실험선택 메커니즘은 King et al. 2004 Nature(sparkes의 ref [23])에 있음. sparkes는 폐루프 실험 설계만 서술.
**주의(해소됨, 2026-07-19):** King 2004 전문 정독 결과 "active learning" 명시 + "선택 = 기대비용 관점의 최적 실험열"·"bayesian analysis ... near-optimal in polynomial time"로 확인됨 → 원고 "Bayesian-optimal"은 **정확히 지지**되므로 완화 불필요. (아래 (선택) 완화 항목은 철회.)

### EN — main.tex L85 (C045)
현재:
```
Domain-specific systems already use active-learning approximations---the Robot Scientist's experiment selection~\citep{sparkes2010robot} and GNoME's DFT-in-the-loop active learning~\citep{merchant2023gnome}---but recent open-ended LLM-based systems ...
```
제안:
```
Domain-specific systems already use active-learning approximations---the Robot Scientist's experiment selection~\citep{king2004robot} and GNoME's DFT-in-the-loop active learning~\citep{merchant2023gnome}---but recent open-ended LLM-based systems ...
```
> `sparkes2010robot` → `king2004robot`(메커니즘 출처). 리뷰까지 병기하려면 `~\citep{king2004robot,sparkes2010robot}`. **KO 대응 문장 없음**(KO 배경절이 이 문장을 압축 제거) → KO 무수정.

### EN — main.tex L92 (C047, OVERCLAIM) / KO L111
EN 현재:
```
...the Robot Scientist~\citep{sparkes2010robot} integrated hypothesis generation, robotic experimentation, and statistical validation in yeast functional genomics, instantiating all six \framework{} components---including an active-learning policy---in physical wet-lab form more than a decade before LLM-based systems.
```
EN 제안(능동학습 성분에 원출처 부여):
```
...the Robot Scientist~\citep{sparkes2010robot} integrated hypothesis generation, robotic experimentation, and statistical validation in yeast functional genomics, instantiating all six \framework{} components---including an active-learning policy~\citep{king2004robot}---in physical wet-lab form more than a decade before LLM-based systems.
```
KO L111 현재:
```
Robot Scientist~\citep{sparkes2010robot}는 효모 기능유전체학에서 가설 생성, 로봇 실험, 통계적 검증을 통합하여 LLM 기반 시스템보다 10년 이상 앞서 \framework{}의 여섯 구성요소 전체---능동학습 정책 포함---를 물리적 습식 실험실 형태로 구체화했다.
```
KO 제안:
```
Robot Scientist~\citep{sparkes2010robot}는 효모 기능유전체학에서 가설 생성, 로봇 실험, 통계적 검증을 통합하여 LLM 기반 시스템보다 10년 이상 앞서 \framework{}의 여섯 구성요소 전체---능동학습 정책 포함~\citep{king2004robot}---를 물리적 습식 실험실 형태로 구체화했다.
```

### EN — main.tex L94 (C048) / KO L113
EN 현재:
```
...a long history of Bayesian-optimal experiment selection in automated science---most directly the Robot Scientist's active-learning policy~\citep{sparkes2010robot};
```
EN 제안:
```
...a long history of Bayesian-optimal experiment selection in automated science---most directly the Robot Scientist's active-learning policy~\citep{king2004robot};
```
KO L113 현재:
```
베이즈 최적 실험 선택은 자동 과학에서 오랜 역사를 가지며---가장 직접적으로는 Robot Scientist의 능동학습 정책~\citep{sparkes2010robot}에서---
```
KO 제안:
```
베이즈 최적 실험 선택은 자동 과학에서 오랜 역사를 가지며---가장 직접적으로는 Robot Scientist의 능동학습 정책~\citep{king2004robot}에서---
```
> (선택) "Bayesian-optimal / 베이즈 최적"을 "cost-based active-learning / 비용기반 능동학습"으로 완화하면 King 2004 실제 방법과 더 정합.

---

## FIX 4 — 순환 타당성에서 aher2023turing 제거 [C087, C089]

**근거:** `aher2023turing`은 외부 인간 데이터와 비교 검증(순환성의 **반대** 안전장치). "circular"·"self-consistency" **0회**. 순환 타당성 논점은 원고 자체의 분석이며 aher는 반례.

### EN — main.tex L200 (C087)
현재:
```
Social science suffers circular validity when $G$ and $E$ share a model~\citep{aher2023turing}, and CS/algorithms close the loop via reliable $V_\text{emp}$ but lack interpretability.
```
제안:
```
Social science suffers circular validity when $G$ and $E$ share a model, and CS/algorithms close the loop via reliable $V_\text{emp}$ but lack interpretability.
```
> `~\citep{aher2023turing}` 삭제. (KO에는 이 산문 문장의 대응이 없음 — KO 무수정.)

### EN — main.tex L448 (C089) / KO L377
EN 현재:
```
...the validator measures the model's self-consistency rather than an external fact~\citep{aher2023turing}---a violation of the identifying-channel condition of Assumption~\ref{asm:tract}.
```
EN 제안:
```
...the validator measures the model's self-consistency rather than an external fact---a violation of the identifying-channel condition of Assumption~\ref{asm:tract}.
```
KO L377 현재:
```
검증기는 외부 사실이 아니라 모델의 자기일관성을 측정한다~\citep{aher2023turing}---이는 가정~\ref{asm:tract}의 식별 채널 조건 위반이다.
```
KO 제안:
```
검증기는 외부 사실이 아니라 모델의 자기일관성을 측정한다---이는 가정~\ref{asm:tract}의 식별 채널 조건 위반이다.
```
> aher를 근처에 유지하려면 "외부 인간 벤치마크 비교로 검증하는 LLM 사회 시뮬레이션 연구"라는 실제 내용으로만 인용.

---

## FIX 5 — Aletheia: formal → natural-language [C022] (EN 단독)

**근거:** Aletheia는 "end-to-end in natural language"(논문 abstract/p.3). 형식 수학 에이전트는 AlphaProof/AlphaGeometry. EN L69만 오류이고 EN L200·EN math app-domain·KO L367은 이미 올바름.

### EN — main.tex L69 (필수)
현재:
```
to formal-mathematics agents (Aletheia~\citep{google2026aletheia}),
```
제안:
```
to natural-language mathematics agents (Aletheia~\citep{google2026aletheia}),
```
> **KO L88(intro)에는 "형식 수학" 라벨이 없음**(단순 \citep 나열) → KO 무수정.

---

## FIX 6 — SciMuse: 생성품질 향상 → 아이디어 선택/관심예측 [C058]

**근거:** SciMuse는 KG 유무로 **생성 관심도에 유의차 없음**을 명시("no significant difference"). KG 기여는 관심도 **예측/선택**(KG 특징만으로 학습한 NN). 지표는 자기보고 '관심도'이지 '품질/신규성'이 아님. 병기된 `lee2025spacer`도 프록시 지표뿐.

### EN — main.tex L90 (필수)
현재:
```
knowledge-graph-driven ideation systems~\citep{gu2024scimuse,lee2025spacer} further show that structuring semantic memory as a relational corpus can substantially improve hypothesis-generation quality, but equally without closing the loop.
```
제안:
```
knowledge-graph-driven ideation systems~\citep{gu2024scimuse,lee2025spacer} further show that structuring semantic memory as a relational corpus can help surface and rank higher-interest research ideas, but equally without closing the loop.
```

### KO — main_ko.tex L109 (필수)
현재:
```
지식 그래프 기반 아이디어 생성 시스템~\citep{gu2024scimuse,lee2025spacer}은 의미 메모리를 관계형 코퍼스로 구조화하면 가설 생성 품질이 향상될 수 있음을 보여주지만, 마찬가지로 루프를 닫지 않는다.
```
제안:
```
지식 그래프 기반 아이디어 생성 시스템~\citep{gu2024scimuse,lee2025spacer}은 의미 메모리를 관계형 코퍼스로 구조화하면 더 흥미로운 연구 아이디어를 발굴·순위화하는 데 도움이 될 수 있음을 보여주지만, 마찬가지로 루프를 닫지 않는다.
```

---

## FIX 7 — 기호회귀 "결정적 탐색" → 확률적(유전 알고리즘) [C074]

**근거:** `cranmer2020symbolic`는 유전 알고리즘(eureqa/PySR) 기반 **확률적** 기호회귀. "결정적 탐색"은 AI Feynman(`udrescu2020afeynman`)에만 해당.

### EN — main.tex L440 (필수)
현재:
```
AI Feynman~\citep{udrescu2020afeynman} and symbolic-model discovery~\citep{cranmer2020symbolic} fit equations to data with deterministic search.
```
제안:
```
AI Feynman~\citep{udrescu2020afeynman} fits equations to data with deterministic search, while symbolic-model discovery~\citep{cranmer2020symbolic} distills equations from trained neural networks via stochastic symbolic regression (genetic algorithms).
```

### KO — main_ko.tex L369 (필수)
현재:
```
AI Feynman~\citep{udrescu2020afeynman}과 기호 모델 발견~\citep{cranmer2020symbolic}은 결정적 탐색으로 데이터에 방정식을 적합한다.
```
제안:
```
AI Feynman~\citep{udrescu2020afeynman}은 결정적 탐색으로, 기호 모델 발견~\citep{cranmer2020symbolic}은 학습된 신경망에서 확률적 기호회귀(유전 알고리즘)로 방정식을 도출한다.
```

---

## FIX 8 — ChemCrow: 대리신호/빔탐색 → ReAct/물리합성 [C076]

**근거:** ChemCrow는 ReAct/도구계획 기반이며("beam" 0회), RoboRXN 로봇 플랫폼에서 DEET·티오우레아 촉매를 **실제 물리 합성**하고 전문가+LLM 평가로 검증. "대리신호/빔탐색"은 ChemReasoner에만 해당(독립 검증 전).

### EN — main.tex L442 (필수)
현재:
```
ChemCrow~\citep{bran2023chemcrow} and ChemReasoner~\citep{sprueill2024chemreasoner} validate computationally with surrogate signals and search by beam.
```
제안:
```
ChemReasoner~\citep{sprueill2024chemreasoner} validates computationally with surrogate signals and searches by beam, whereas ChemCrow~\citep{bran2023chemcrow} plans via ReAct tool-use and validates in part through physical wet-lab execution on a robotic platform (with expert and LLM evaluation).
```

### KO — main_ko.tex L371 (필수)
현재:
```
ChemCrow~\citep{bran2023chemcrow}와 ChemReasoner~\citep{sprueill2024chemreasoner}는 대리 신호로 계산적으로 검증하며 빔 탐색을 쓴다.
```
제안:
```
ChemReasoner~\citep{sprueill2024chemreasoner}는 대리 신호로 계산적으로 검증하며 빔 탐색을 쓰는 반면, ChemCrow~\citep{bran2023chemcrow}는 ReAct 도구 사용으로 계획하고 로봇 플랫폼의 물리적 습식 실험 실행(전문가·LLM 평가 포함)으로 부분 검증한다.
```
> 주의: 이 두 문단은 각각 "$V_\text{emp}$ surrogate; computational loop only" / "대리; 계산 루프만" 헤더를 갖는데, ChemCrow의 물리 실행을 반영하면 헤더도 재검토 대상(단, 원고는 "측정 경계에서 습식 루프 개방"을 이미 별도 서술하므로 헤더 유지 가능).

---

## FIX 9 — park2023 "full-factorial" 완화 [C091]

**근거:** park2023(생성 에이전트 시뮬레이션)은 단일요인(조건 5수준) within-subjects + 누적 절제 설계이며 저자 스스로 "one-way ANOVA 대안 Kruskal-Wallis"로 분석 → full-factorial 아님. full-factorial은 manning2024에만 해당.

### EN — main.tex L448 (필수)
현재:
```
Automated-social-science pipelines~\citep{manning2024automated} and LLM-simulation studies~\citep{aher2023turing,park2023generative} validate with statistical tests over full-factorial designs.
```
제안:
```
Automated-social-science pipelines~\citep{manning2024automated} validate with statistical tests over full-factorial designs, while LLM-simulation studies~\citep{aher2023turing,park2023generative} validate simulated behavior with statistical tests over ablation and controlled comparisons.
```

### KO — main_ko.tex L377 (필수)
현재:
```
자동 사회과학 파이프라인~\citep{manning2024automated}과 LLM 시뮬레이션 연구~\citep{aher2023turing,park2023generative}는 완전 요인 설계에 대한 통계 검정으로 검증한다.
```
제안:
```
자동 사회과학 파이프라인~\citep{manning2024automated}은 완전 요인 설계에 대한 통계 검정으로 검증하고, LLM 시뮬레이션 연구~\citep{aher2023turing,park2023generative}는 절제·통제 비교에 대한 통계 검정으로 시뮬레이션 행동을 검증한다.
```
> (선택) 도메인 비교표의 사회과학 "full-factorial / 완전 요인" 셀(EN Table / KO L245)은 도메인 요약이므로 유지 가능하나, 엄밀히는 manning 기준. 표까지 맞추려면 "controlled/ablation"으로 완화.

---

## 적용 시 검증 체크리스트 (승인 후 단계)
1. references.bib에 `king2004robot` 추가 → `bibtex main` 미정의 키 0.
2. 위 9개 그룹의 EN/KO verbatim 치환 적용(비대칭 준수: EN단독=C022,C045-L85,C087-L200; 736 KO는 L280만).
3. `xelatex main.tex` + `xelatex main_ko.tex` 오류 0, 미해결 인용 0(`\citep` undefined 경고 확인).
4. `python3 citation-review/check.py` → 4 불변식 유지.
5. PDF 복사(main.pdf→servo_caiscfp2026.pdf) + references.bib 변경으로 supplement ZIP 재생성.
6. 적용 후 원장 status: 14 FLAGGED → 재판정(APPLIED/RESOLVED) 기록.
