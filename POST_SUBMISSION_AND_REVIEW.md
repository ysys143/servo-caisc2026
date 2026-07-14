# 제출 이후 수집 자산 & CAISc 2026 리뷰 대응 노트

> 작성: 2026-07-15 · 대상: `submission/72_Formalizing_AI_Scientist_Sy.pdf` (SERVO, Track 2 Accept)
> 목적: (A) camera-ready 확정 이후 지형도에 축적·발전시킨 것 정리, (B) 리뷰 4건에 대한 대응 전략. rebuttal이 아니라 **camera-ready 반영 / 후속 이월**의 2트랙으로 분류.

마커: `[NEW]` = 제출 후 확실히 신규(git 커밋 앵커) · `[NEW++]` = 핵심 신규 자산 · `[EXT]` = 계속 확장 중인 클러스터에 추가된 2026 항목.

---

## 0. 결정 구조 (사실 기록)

| 리뷰어 | 유형 | 판정 | 확신 |
|--------|------|------|------|
| Program Chairs | 결정 | **Accept** | — |
| Reviewer LcMY | 인간 | Accept (2) | Medium |
| AI 1 | AI | Accept (2) | Medium |
| AI 2 | AI | Accept (2) | Medium |
| AI 3 | AI | **Reject (1)** | Medium |

- AI 3인 중 2 Accept / 1 Reject의 **split verdict** -> 정책상 인간 전문가(LcMY) 배정 -> Accept -> Chairs 최종 Accept.
- 전체 191편 중 80편(41.9%), **Track 2 (Open-Ended) 171편 중 67편(39.2%)**. Archival.
- **판본 주의**: OpenReview 메타데이터(제목 "A Unified Framework...", 초록)는 **원 제출본(5/30)** 것으로 세 번째 open problem을 "semantic memory M_s 미발달"로 표기. 심사된 최종본(`72_Formalizing`, 제목 "A Component Framework...")은 이를 **"experiment fidelity gap"으로 교체**(commit `0a6254c`). LcMY가 세 문제를 novelty gates·BED-practice·experiment fidelity로 명시 -> 리뷰어는 교체된 최종본을 봄. camera-ready 시 메타데이터 동기화 필요.

---

## A. 제출(camera-ready 6/11) 이후 수집·발전 자산

지형도(`ai_scientist/AI_Scientist_Analysis.md`)와 별도 모델 문서(`aisci_abm/`)에 축적.

### A1. RSI / 자기진화 분파  [NEW]
- **Sakana RSI Lab**, **Anthropic RSI Institute** — 재귀적 자기개선을 별도 연구 축으로 신설(§8 self-evolving 분파 확장, commit `f3fa3c6`).
- **Red Queen Gödel Machine** (arXiv:2606.26294), **Digital Red Queen** (2601.03335) — 공진화·자기수정 압력을 SERVO 루프에 얹는 사례(`9521293`).
- 대응 관련: "π가 추론시 탐색 vs 가중치 학습으로 분리"되는 축(§6.6)의 실물. RSI는 π_learned가 오라클-완전 도메인에서만 일어난다는 §10.1 corollary의 테스트베드.

### A2. 프레임워크 정교화 — 새 축  [NEW]
- **§6.6 π_inference vs π_learned** (`7d0a43c`): 정책을 추론시 탐색과 post-training 가중치 학습으로 분리. post-training은 오라클-완전 도메인에서만(§10.1 corollary).
- **§7.9 답-양식(answerability) 매핑** (`c26e90a`): 미해결 문제를 경험적/개념적/원리적-미결정 3층으로 분류. novelty 자동화 불가는 "능력 부족"이 아니라 답-양식의 귀결(V_human 사후 정당화 -> 원리적 미결정).

### A3. S(탐색공간) 표현 문제  [NEW]
- **§7.8** (`75e77cb`): BED/ADO를 발견에 적용하려면 S를 먼저 표현해야 함. ADOpy는 θ가 모수화된 인지모델에서만 작동. 자연어(표현력↑, EIG 정의 불가) <-> 파라미터(EIG 가능, 표현력↓) <-> 온톨로지/KG(중간층)의 트레이드오프. night science(Yanai & Lercher) 연결. AlphaFold식 "표현학습 -> 압축된 잠재공간 위 탐색" 경로.

### A4. 관측·측정 강화  [NEW]
- **§9.5 MouseMapper** (`fc61040`): 관측 함수 O를 강화하는 "측정 증폭기". S를 압축하는 §7.8 경로와 직교(O 강화 vs S 압축).

### A5. 벤치마크·평가 사다리 클러스터  [EXT]
- **CORE-Bench**(2409.11363, 재현성 270태스크), **AstaBench**(Ai2, 11벤치·2,400문제 — non-convenience 표본틀), **AutoMedBench**(2606.01961), **SR-Scientist**(ICLR 2026).
- **ICML 2026 신호 3편**(`5f79760`, [[icml2026-taehyung-kim-collection]]): Stanton(Anthropic) **"Recapitulation is not discovery"** + 4단 평가 사다리(recall->proxy->rediscovery->real experiment, 과학 에이전트 칸 공백), Jiao(OpenAI) **"benchmark->benchwork"**(GPT-Rosalind·비오염 LabWorkBench), Zou(Stanford) Virtual Lab/Paperclip.
- **Measuring the Gap**(2607.01233): 평가를 개별 아이디어 -> **분포 divergence**로 이동. LLM 아이디어가 bridge형·synthesis에 체계적으로 편향됨을 실증 -> §7.1 novelty 근거 보강.

### A6. 이데이션·문헌 클러스터  [EXT]
- **SciAtlas**(2605.22878, 43M논문 KG, M_semantic 외부화 최대규모), **Alien Space of Science**(2603.01092, idea atoms·인지가용성), **Spacer**(2508.17661, 의도적 탈맥락화).

### A7. 집단 확장 이론 — 핵심 신규 자산  [NEW++]
`aisci_abm/`에 별도 문서로:
- **`servo-ms-model.md`**: SERVO를 CPC-MS(Taniguchi 2025) 집단 동역학으로 확장한 새 모델. 튜플 `(S, {G_i}, {E_i}, {V_i}∪C, {M_i}∪W, {π_i}∪Π, Ψ, H)` — 각 컴포넌트를 "분산 개별 + 공유"로 이중화. 명제 **P1–P6**(P1–P3 = SERVO 확장, **P4–P6 = 집단 고유**: 재귀성/모델붕괴, 합의 MH ergodicity, 분산 검증가능성). P4–P6은 개별 SERVO에 대응 명제가 **없음** — 이것이 확장의 기여.
- **`servo-ms-failure-modes.md`**: 실패 양식을 베이지안 수렴조건 **C1–C9** 위반으로 연역(C1–C6 개별, C7–C9 집단 신규). 개수가 임의가 아니라 조건집합 크기에서 도출.
- **`servo-ms-abstract.md`**: **AI4Sci Korea 2026** 거버넌스 트랙(1-2, Chair Young-Kuk Kim) 제출 초록 초안(316단어, 2026-07-14 작성). 제목후보 + ABM 상전이 설계(헤드라인: C7 재귀붕괴 · C7×C8 결합 · C9 혼합임계/MiroFish; 나머지는 "in principle"). 이 초록이 후속 응답을 실제 venue로 내보내는 통로.

### A8. 인프라 — OKF 번들 재구성  [NEW]
- concept 문서 161편 + index.md/log.md + Obsidian graph(`d0f2111`->`3bd1cf6`). 향후 자원 편입 규약 확립.

---

## B. 리뷰 대응 전략

### B.0 대응 원칙
채택 논문이므로 **rebuttal 없음**. 두 트랙으로:
- **(i) camera-ready 반영** — 주장 톤 정렬, 인용 보강, 표본 확장, 후속 forward-pointer.
- **(ii) 후속 이월** — 경험적 검증·human coding·ABM. 방법론 비판(κ·순환)은 camera-ready로 못 닫고 후속으로만 닫힘.

### B.1 비판 -> 대응 매핑

| # | 비판 (제기자) | 트랙 | 대응 | 이미 있는 자산 |
|---|--------------|------|------|--------------|
| 1 | **서술적·경험적 검증 부재** (4인 전원) | (ii)+(i) | 후속: SERVO-MS의 예측내용(C1–C9) + MiroFish/거버넌스 ABM이 "작동 입증". camera-ready: 후속 연구 forward-pointer 1문단 | A7, A5(CORE-Bench·AstaBench·PaperBench = 외부 V 시험대) |
| 2 | **형식화가 payoff 대비 과잉 / 명제가 기지 결과의 직접 적용** (LcMY·AI1·AI2·AI3) | (i)+(ii) | 형식장치는 **집단화할 때 load-bearing**이 됨(P4–P6는 posterior-consistency류로 환원 안 됨: 모델붕괴·MH·분산검증). §11.3이 "단일 프레임워크 통합"의 유일성 입증 | A7(P4–P6), §11.3 비교표 |
| 3 | **V-completeness 주장이 자기 hedging보다 강함** (AI3 핵심·AI2) | (i) | camera-ready: "necessary constraint" 구절을 초록/§8의 hedging("hypothesis-generating, not evidence-backed")과 톤 정렬. 집단 재구성(C=집단 검증자)이 인과 주장을 **검정 가능**하게 만드는 지점 명시 | A7(C), §7.9 |
| 4 | **표본 4개(convenience)·선택/생존 편향** (AI1·AI2·AI3) | (i)+(ii) | 제출 후 카탈로그가 표본을 대폭 확장(RSI 분파·ideation·benchmark). AstaBench(2,400문제)=non-convenience 표본틀. camera-ready: Table 1 확장 또는 확장 카탈로그 각주 | A1·A5·A6 |
| 5 | **V-completeness ordinal κ=0.39 + LLM-coder 순환성** (AI1·AI2·AI3) | (ii) | 가장 깊은 방법론 비판 — camera-ready로 못 닫음. 순환성 자체가 논문 테제(LLM-V 신뢰불가)의 실연이나, 정직하게는 **human expert coding** 필요(후속). "AI 3이 AI-Scientist 논문을 reject"한 이번 심사가 실물 사례 | §7.6, failure-modes 문서 |
| 6 | **CPC-MS와 미차별화** (AI2 약점 5) | (ii)->강점 | **SERVO-MS가 정확히 그 답.** 리뷰어가 요청한 차별화를 후속이 실현 = 후속 논문의 정당성을 심사자가 문서로 남김 | A7(`servo-ms-model.md`) |
| 7 | **autonomous-labs·execution-grounded 가설생성 인용 보강** (LcMY) | (i) | camera-ready: §7.4 wet-lab(ORGANA·AutoLabs·**Robin** Nature 2026) + §7.5 execution-grounded(SR-Scientist·PiFlow·HypER) 인용 추가 | §7.4, §7.5 |

### B.2 방법론 비판(#5)의 정직한 처리
- κ=0.39(fair)·저자 대비 음의 Cohen κ는 **V-completeness ordinal이 아직 신뢰할 구성물이 아님**을 뜻함. 논문은 이미 calibration 하위구성물(κ=0.79)로 후퇴해 방어했으나, 진단 논변의 상당부가 ordinal 위에 서 있음.
- **순환성**: cross-system coding을 LLM coder만으로 수행 -> "LLM-V는 novelty에 신뢰불가"라는 자기 테제와 충돌. camera-ready에서 **feature가 아니라 한계로 명시**하고, 후속에서 인간 도메인 전문가 coder로 재계측.
- **살아있는 실증**: 이번 심사(AI 3인 중 1 reject; AI Involvement Checklist가 저술 에이전트의 *systematic citation fabrication*·*analytical overconfidence* 자백)는 C1/과신 실패의 첫 실물 사례 -> `servo-ms-failure-modes.md` 사례절에 편입 후보.

### B.3 camera-ready 체크리스트 (가능한 것만)
- [ ] OpenReview 메타데이터(제목·초록) <-> 최종본 동기화(M_s -> experiment fidelity).
- [ ] V-completeness 강한 구절 <-> hedging 톤 정렬(#3).
- [ ] §7.4/§7.5 최신 autonomous-lab·execution-grounded 인용 보강(#7).
- [ ] LLM-coder 순환성을 한계로 명시(#5).
- [ ] 후속(SERVO-MS 집단 확장 + ABM) forward-pointer 1문단(#1·#2·#6).
- [ ] (선택) 확장 카탈로그를 부록/각주로 표본 편향 완화(#4).
- [ ] **camera-ready 마감일 확인** (미확인 — CAISc 공지/OpenReview 확인 필요).

---

## C. 다음 단계 (지형만, 강요 없음)

- **후속 논문 축**: #1·#2·#6이 한 점으로 수렴 — "SERVO를 CPC-MS 집단으로 확장(P4–P6) + ABM으로 붕괴조건 검증". 리뷰어가 요청한 것이 그대로 후속의 논지.
- **AI4Sci 거버넌스 트랙**: "언제 어떻게 무너지는가"의 ABM 검증을 담을 venue. **초록 제출본 초안 이미 존재**(`aisci_abm/servo-ms-abstract.md`, 316단어, Track 1-2). 남은 것은 (a) ABM 상전이 1개 확보(오럴 조건), (b) 실제 제출 여부 확인 — 초안은 있으나 제출 완료는 미확인.
- **실패분류 문서 보강**: 이번 심사의 AI-리뷰어 아이러니 + Checklist 자백을 C1/과신 실물 사례로 편입.
- **camera-ready 실작업**: B.3 체크리스트 중 (i)트랙만 실제 원고에 반영.
