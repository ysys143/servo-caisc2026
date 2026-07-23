# SERVO v5 재구축 헌장 (Reconstruction Charter)

- 상태: **FROZEN v5.0-rules (1차 동결, 2026-07-23)** — Part A/B/C/D 규칙 동결. 이후 규칙 변경은 새 버전 번호를 요구하며, holdout 코딩 이후의 변경은 해당 사례를 formative로 만들고 untouched holdout 재확보를 요구한다. 유예 항목: B-prime 텍스트 최종 동결(분석 레이어 재구축 후), E.6(적대검증 주체, 실행 단계).
- 작성일: 2026-07-23
- 목적: v4.1을 역사 버전으로 동결하고, source proposition -> decision-semantic claim -> evidence graph 순서의 v5 계열을 재구축하기 위한 단일 기준 문서.
- 지위: 저자 승인 시 이 문서가 FROZEN 되고, 이후 모든 v5 재분석·재코딩·논문 개정은 이 문서를 규범으로 삼는다. 이 문서가 동결되기 전에는 어떤 v5 산출물(코드·스키마·표·본문)도 생성하지 않는다.
- 근거: 8개 단서(이전 세션 종합 분석) + 현재 저장소 실측 대조.

---

## 0. 이 문서를 만든 이유 (churn 진단)

반복 수정의 공통 실패 패턴은 다음이었다.

1. 기존 `established` 셀을 유지해야 한다고 암묵적으로 가정한다.
2. 새 validator 조건을 추가한다.
3. 기존 판정을 살리기 위해 event, endpoint, artifact, time suffix를 보충한다.
4. 출처가 말하지 않은 occurrence까지 구조적으로 생성한다.
5. 테스트는 통과하지만 의미론적 허구가 더 정교해진다.

현재 브랜치명 `codex/schema-first-servo-consistency`와 최근 커밋(`enforce schema 4 artifact and occurrence contracts`, `reject inferred closure recurrence`)이 이 패턴의 흔적이다. **v5의 핵심은 schema 4.1을 더 정교하게 고치는 것이 아니라, 거짓인 판정을 낮추면서 유한하게 수렴하는 것이다.**

### 0.1 실측 증거 (2026-07-23 확인)

`analysis/servo2_closure_witnesses.csv`에서 다음을 확인했다.

- **C06**: W10(execution_repair), W11(experimental_adaptation), W12(artifact_revision)가 이벤트 `EV21;EV51;EV38`을 상호 공유한다.
- **C01**: W01(execution_repair), W15(artifact_revision)가 `EV01;EV48`을 공유한다.
- `EV48/EV49/EV50/EV51`처럼 번호가 뒤로 튀는 이벤트 + `execution_status=trace_demonstrated`는 구조적으로 추론된 successor/production 이벤트일 가능성이 크다.

즉 v4.1의 테스트 111개 PASS는 **schema 내부 정합성**만 증명하며, 새 decision-semantic 계약의 통과 증거가 아니다.

---

## Part A — 주장 틀 동결 (헌법 1단계)

> 규칙: 이 파트는 코드보다 먼저 동결한다. 사례를 보고 나서 주장 틀을 조정하지 않는다.

### A.1 연구 질문 (primary)

> **What decision-theoretic structure is actually instantiated by contemporary AI Scientist systems, and which scientific feedback relations remain absent, external, or merely reported?**

- 논문의 **주어는 실제 의사결정 구조**이며, provenance schema가 아니다.
- 현재 논문(main_post-submit.tex:80)의 질문("Which evaluation event is connected to which later action? ...")은 정신은 같으나 **provenance/graph를 앞세운 프레이밍**이다. v5는 이를 의사결정 구조 중심으로 다시 정박한다.
- 하위 질문(현행 유지 가능): 어떤 evaluation event가 어떤 later action에 연결되는가; 어떤 artifact version이 그 연결을 담는가; 어떤 feedback이 bounded reported configuration 안에서 established 되는가.

### A.2 기여 (contributions)

1. 동시대 AI Scientist 시스템이 실제로 인스턴스화하는 **의사결정 구조의 명시적 계약**과 그 source-traceable 적용.
2. 어떤 과학적 feedback 관계가 **부재/외부/보고만 됨(reported only)**인지 구분하는 typed functional relation 어휘.
3. 여섯 사례에 대한 재현 가능한(source proposition 기반) 적용과, 하나의 결정적 replay worked case(FunSearch).

**명시적 비기여(what the contribution is NOT):** 완전한 ontology, 인과 이론, 모집단 taxonomy, 성능 순위, 첫 통합 프레임워크 주장.

### A.3 비주장 범위 (non-claims) — 동결

- V(검증기) completeness가 신뢰 가능한 자율 발견의 보편적 필요/충분 조건이라는 주장 안 함.
- 어떤 predicate status도 신뢰 가능한 과학적 결과(trustworthy scientific outcome)를 정의하지 않는다.
- convenience sample이며 모집단을 대표/망라하지 않는다.
- POMDP 완전 인스턴스화나 BED 우선권 주장 안 함. 단 POMDP/BED는 "용어만 차용"이 아니라 SERVO의 분석 범주를 만든 **구성적 이론 자원**이다(완전 구현을 시스템에 요구·채점하지 않을 뿐이다).
- gate-reliability와 "trustworthy closure"의 연관은 정의상 순환으로 철회됨(재도입 금지).

### A.4 논증 계층 순서 (동결)

논문과 분석의 논증 골격은 반드시 다음 순서다.

> **POMDP/BED 의미론 -> SERVO 대응 -> 증거·provenance**

- 반대 순서(graph -> schema -> 의미 부여)는 "mathy cosmetic"으로 규정하며 금지한다.
- 판정 기준: **POMDP/BED를 제거했을 때 최소 두 사례의 분류나 핵심 결론이 실제로 사라져야 한다.** 사라지지 않으면 decision-theoretic 골격은 장식이며 A.4를 다시 설계한다. 핵심은 BED를 응용한 구별이 **사례 해석과 결론을 바꾸는가**이며(양성 explicit_bed 사례가 하나도 없어도 무관), "BED가 없으면 BED 부재를 진술 못 함" 같은 순환 논증은 근거에서 제외한다.

---

## Part B — 규칙 동결 (헌법 2단계)

> 규칙: 분석 규칙을 사례보다 먼저 동결한다. 규칙이 강화됐는데 기존 판정의 증거가 부족하면 판정을 낮춘다(단조 하향). 기존 판정을 살리기 위해 event나 schema를 추가하지 않는다.

### B.1 세 객체 분리 (source ledger에 판정 답안 금지)

세 객체를 물리적으로 분리한다. 하나의 파일/레코드가 두 역할을 겸하지 않는다.

| 객체 | 저장 내용 | 금지 |
|---|---|---|
| `SourceProposition` | 인용문, locator(page/para), modality, **직접 언급된** actor/input/output만 | 판정, alignment, "permitted derived claim" 삽입 금지 |
| `AuthorAlignment` | source 개념을 SERVO component/relation에 대응한 **해석** | 새 사실 생성 금지 |
| `DerivedDecisionClaim` | 동결된 rule이 proposition+alignment에 적용되어 생성한 **판정** | proposition 단계에서 미리 답을 넣는 순환 금지 |

- `permitted/prohibited stronger claims`는 **감사용 경계 정보로만** 사용하고 최종 status를 직접 결정하지 않는다.
- modality(directly reported / reported as procedure / reported only as capability)는 `SourceProposition`의 **증거 해상도** 필드이지 판정이 아니다.

### B.2 4축 레코드 (증거·해석·판정 축 분리)

기능 관계의 값을 한 축에 섞지 않는다. 최소 네 축으로 분리한다.

| 축 | 허용값 | 비고 |
|---|---|---|
| `support_status` | `supported` / `unresolved` / `contradicted` / `not_applicable` | 판정 상태 |
| `claim_scope` | `architecture` / `procedure` / `aggregate_run` / `occurrence` | 주장 해상도 |
| `alignment_kind` | `source_explicit` / `author_aligned` | 해석 관계 |
| `occurrence_resolution` | `resolved` / `unresolved` / `not_applicable` | occurrence 해결 여부 |

- `not_applicable`은 **사전에 동결된 적용성 규칙**이 있을 때만.
- `contradicted`는 **명시적 반대 증거**가 있을 때만.
- **Source silence는 항상 `unresolved`** (절대 `not_applicable`이나 `supported` 아님).

### B.3 단조 하향 원칙 (수렴 장치)

- 규칙이 강화되고 기존 판정의 증거가 부족하면 **판정을 낮춘다.**
- 기존 판정을 살리기 위해 event/endpoint/artifact/time-suffix/schema를 **추가하지 않는다.**
- inferred occurrence는 positive witness에서 **금지**된다(구조적으로 추론된 event는 later execution/successor evidence를 공급할 수 없다).
- 재분석은 기존 matrix가 아니라 **source proposition에서 다시 시작**한다. 현재 v4.1 closure matrix를 출발점으로 삼지 않는다.

### B.4 Policy = BED에서 유도한 선택·정보·목적 구별에 의한 분해 (compliance 채점 아님) — 2026-07-23 재작성

**관계 방향(동결):** `BED → SERVO의 분석 문법 → 실제 시스템 분석`. 그 역(`SERVO 분석 → 각 시스템이 BED를 구현했는지 채점`)은 금지한다. **BED는 SERVO 바깥의 평가 기준이 아니라 SERVO의 분석 범주 자체를 만든 구성적 이론 자원**이며, 다만 완전한 BED 구현을 시스템에 요구하지 않는다.

**교정(저자 지적):** 이전 B.4는 `explicit_bed`를 mechanism label로 두어 "시스템이 BED를 준수하는가"를 채점했다. 이는 POMDP를 "시스템이 POMDP인가" 판정에 쓰지 않는 것과 **비대칭**이며, BED를 구성적 자원이 아니라 외부 compliance 기준으로 들이댄 오류다. `explicit_bed`를 별도 binary 필드로 옮기는 것도 이름만 바꾼 같은 오류다. **BED가 제공하는 시좌는 "이 시스템이 BED인가?"가 아니라 다음 구별들이다:** 단순 반복 vs 결과 조건부 선택 / 점수 최적화 vs 정보 획득 / 모든 후보 실행 vs 선택적 실험 / 오류 수정 vs 가설 구별 / 결과 저장 vs 결정 정보 갱신 / 불확실성의 단순 언급 vs 불확실성을 이용한 실험 선택.

정책은 다섯 축으로 분해한다(각 다중값 가능). 선택 대상(후보/실험조건/fidelity/후속 action)은 각 축에서 서술한다:
1. `control_dependence` — 무엇이 선택을 변화시키는가: none(fixed)/failure/score/observation_result/uncertainty/candidate_disagreement.
2. `selection_signal` — 선택을 실제 구동하는 신호(control_dependence와 겹칠 수 있음; 더 구체적 신호를 명명).
3. `selection_objective` — 선택 목적: local_repair/performance/exploration/uncertainty_reduction/hypothesis_or_model_discrimination.
4. `candidate_execution_rule` — 어떤 후보가 실제 실행되는가: all/score_ranked_subset/uncertainty_subset/expected_discrimination_selected.
5. `formal_epistemic_utility_evidence` — BED의 명시적 수학구조(posterior/likelihood/EIG/VOI/epistemic_utility)의 보고 여부·인용. **보조 evidence facet일 뿐 핵심 label 아니다.**

**핵심 결과의 형태(동결):** 중심 결과는 "explicit_bed 유무"가 아니라 **해체(decomposition)**다. BED에서 유도한 선택·정보·목적 구별을 적용하자, 모두 "iterative"·"closed-loop"로 뭉뚱그려지던 시스템들이 서로 **다른 피드백 구조**로 분해된다 — 일부는 실패를 복구하고(C01), 일부는 점수를 향상하며(점수-클러스터 C02/C03/C04/C06), 일부는 관찰에 따라 후속 실험을 변경하지만, 공개 자료에서 불확실성 감소나 경쟁 가설 구별을 선택 목적으로 삼는지는 대부분 확인되지 않는다(C05만 목적 수준에서 근접). "어느 사례도 명시적 EIG 목적함수를 보고하지 않는다"는 것은 **BED의 실패가 아니라 SERVO가 드러낸 마지막 제한적 관찰** 한 줄이며, corpus-level limitation으로만 기술한다.

금지:
- BED를 mechanism label이나 compliance(present/absent) 판정으로 쓰지 않는다.
- `explicit_bed=false 6/6`을 중심 표·핵심 결과로 제시하지 않는다(SERVO를 BED 구현 체크리스트로 축소하는 오류).

분해 산출 예(compliance 아니라 해석 분해):
- C01: 실패 복구 + yield/score-directed exploitation. 정보 획득을 위한 실험 선택은 아님.
- C03: performance metric best-first + redundancy 회피 exploration. uncertainty-directed design은 아님.
- C05: 가설 구별을 선택 목적으로 삼는 유일 사례(uncertainty_reduction/hypothesis_or_model_discrimination). 그러나 20개 가설을 전부 시험하므로 기대판별 기반 down-selection(expected_discrimination_selected)은 확인되지 않음 — active-learning 지향과 형식적 BED 선택규칙 사이의 간극.

### B.5 형식 경계 (동결)

일관된 최소 식:

```
a_t   ~ pi(· | I_t)
o_{t+1} ~ O_env(· | a_t)      # 결정적 특수경우는 Dirac
v_{t+1} = V(o_{t+1})
I_{t+1} = U(I_t, o_{t+1}, v_{t+1})
```

- `I_t`는 새 component가 아니라 S_t, M_t, 과거 평가·제약 중 **해당 결정 시점에 접근 가능한 source-bounded view**.
- 역할: `G`는 후보 생성, `pi`는 후보 중 action 선택, `E`는 intervention 수행, `O_env`가 observation 생성, `V`는 observation 평가.
- 출처가 executor-environment 경계를 제공하지 않으면 **`boundary_unreported`**로 둔다. E를 observation 생산자로 임의 지정하지 않는다.
- "result -> update"처럼 observation과 evaluation을 다시 합치는 표현 금지. **typed relation**으로 기록한다.
- 현행 논문(main_post-submit.tex:154-166, 198)은 이 형식을 이미 상당 부분 반영. v5는 스키마 enum에 `boundary_unreported`를 추가하고 표기를 통일한다.

### B.6 적용성·반박·침묵 규칙 요약

- source silence -> `unresolved`.
- explicit contrary evidence -> `contradicted`.
- predeclared out-of-scope -> `not_applicable` (이유 명시 필수).
- 어떤 contract 변경도 holdout 코딩 이후에 발생하면 그 사례는 formative가 되고 새 untouched holdout이 필요하다.

---

## Part B.7 — typed functional relation schema (조합형) — 2026-07-23 확정

`relation_asserted`는 charter 최초 동결 시 미명시였다(빈칸 채우기이며 동결 규칙 변경 아님). T1 구현이 단일 enum(step 활동)으로 도출했으나 두 결함이 있었다: (a) 활동(step)과 관계(relation)가 한 enum에 혼재, (b) feedback을 전부 evaluation 기점으로 만들어 **observation ≠ evaluation**(B.5) 구분을 훼손. 조합형으로 확정한다.

AuthorAlignment는 `assertion_kind`로 두 종류를 구분한다.
- `component_mapping`: `source_term → component`(S/G/E/V/M/pi/A/W_A/external/O_env), `basis`.
- `functional_relation`: `(source_role, relation_type, target_role, temporal_scope, basis)`.
  - ROLE(source_role/target_role) ∈ {candidate, action, execution, observation, evaluation, inquiry_state, memory, artifact, policy, environment, external}
  - `relation_type` ∈ {produces, evaluates, updates, conditions, selects, revises, reads, writes, triggers}
  - `temporal_scope` ∈ {per_step, cross_step}

원칙(동결):
- **observation ≠ evaluation.** cross-step feedback이 전부 evaluation 기점이면 안 된다. 최소 cross-step feedback set: observation→inquiry_state(updates), evaluation→inquiry_state(updates), inquiry_state→policy(conditions), evaluation→execution(triggers), evaluation→artifact(revises), memory→candidate(conditions/reads), memory→policy(conditions).
- predicate 이름(execution_repair, experimental_adaptation, artifact_revision, discovery_cycle)을 relation 값으로 **쓰지 않는다**(E.2 퇴역 유지). feedback은 role·type·scope 조합으로 서술한다.
- relation을 closure score나 predicate status로 **aggregate하지 않는다.** relation의 status는 DerivedDecisionClaim의 4축(support_status 등)에서만.
- basis(source_explicit/author_aligned)와 boundary_status(reported/boundary_unreported)는 functional_relation에도 적용.

## Part B.8 — source-layer purity & T5 alignment rubric 경계 — 2026-07-23 확정

용어 수정: source layer는 "판정이 전혀 없는" 층이 아니라 **SERVO 의미론적 alignment와 derived 판정이 없는** source layer다. modality 분류·coreference·문장 분할·범위 설정은 약한 해석을 포함한다. 제거 대상은 모든 해석이 아니라 SERVO component·feedback relation·closure·policy class에 관한 **의미론적 누출**이다.

### source_context_note 허용/금지 (필드명 `notes_verbatim` -> `source_context_note`)
- 허용: (a) 문장에 생략된 직접 목적어의 source-local 복원, (b) 대명사의 동일 문단 내 지시 대상, (c) quote 전후 문맥, (d) 표·그림·본문 연결, (e) modality 판정 근거, (f) 문장 분할 이유, (g) OCR/typography 정규화 설명.
- 금지(제거 또는 T5로 이동): memory update, repair channel, candidate conditioning, human-authority boundary, observation-to-state / evaluation-to-artifact relation, policy adaptation, BED-like, occurrence evidence. **T5 입력 코드는 이 필드를 읽지 않는다.**

### T5 alignment rubric 경계 (freeze 대상)
- Component mapping: G=후보 생성, pi=선택/다음행동 결정, E=action을 환경·도구에 적용, O_env=실행결과로 새 observation 생성, V=observation/artifact 평가, M=정보 저장, I_t=저장정보가 실제 decision input으로 사용. **memory_write != decision-relevant state update.**
- Functional relations: 조합형 유지(B.7). 최소 cross-step 구별은 B.7 set. 모든 feedback을 evaluation_to_*로 만들지 않는다.
- Policy: BED 렌즈의 5축 분해(B.4) — control_dependence/selection_signal/selection_objective/candidate_execution_rule/formal_epistemic_utility_evidence. BED를 compliance label(explicit_bed present/absent)로 채점하지 않는다. formal_epistemic_utility_evidence(posterior/likelihood/EIG/epistemic-utility의 직접 사용 보고)는 보조 facet이며, 어느 사례도 이를 보고하지 않음은 corpus-level limitation으로만 기술.
- Evidence status(기능 의미와 별도 축): directly_reported, procedure_described, capability_only, aggregate_occurrence_reported, occurrence_traced, author_aligned, unresolved. **procedure_described와 occurrence_traced를 ordinal closure level로 합치지 않는다.**

### rubric freeze 순서 (역방향 오염 금지)
source freeze -> alignment rubric freeze -> C01 pilot -> rubric audit(C01 + 대조사례 C05 또는 C03/C06의 5~10 경계 proposition blind pilot; 표현 오류만 수정) -> rubric version freeze -> C01 포함 전 사례 동일 버전 재생성.
C01 결과를 보고 rubric을 자유 변경 금지. 수정 필요 시: (1) rubric version up, (2) 이유 기록, (3) 기존 alignment 폐기, (4) 처음부터 재생성.

### T5 착수 6조건 (모두 충족 전 AuthorAlignment 생성 금지)
1. C01 coverage note가 pilot/incomplete 아님. 2. 6사례 동일 inclusion rule 문서화. 3. 모든 source proposition이 PDF/승인 source artifact에 결속. 4. source_context_note에서 SERVO 의미론 누출 제거. 5. 9개 modality warning 개별 disposition 완료. 6. source freeze manifest + downstream invalidation 규칙 생성.

## Part C — v4.1 -> v5 이관·폐기 목록 (실측 기반)

### C.1 주분석에서 퇴역(폐기) — 역사자료/파생쿼리로만 유지

- **4-predicate closure matrix**(execution_repair, experimental_adaptation, artifact_revision, discovery_cycle_feedback)를 **주분석에서 퇴역**한다. 새 주분석은 typed functional relations이며, 과거 predicate는 역사 자료 또는 worked case의 파생 query로만 남긴다.
  - 대상 파일: `servo2_closure_statuses.csv`, `servo2_closure_witnesses.csv`, `servo2_predicates.py`, `servo2_closure.py`, `predicate_contract.md`(historical 태그).
  - 논문 영향: Table 2(`tab:status-matrix`, main_post-submit.tex:270-277), predicate patterns 표(`tab:predicate-patterns`, 231-247)를 주분석에서 내리고 부록/역사로 이동.
- **공유 event 기반 established witness 폐기**: W01/W15(EV01,EV48 공유), W10/W11/W12(EV21,EV51,EV38 공유), 및 구조적 inferred successor에 의존하는 established(현재 established revision/repair witness 전부 재검토 대상).

### C.2 역사 보존 (historical, non-authoritative)

- v4.1 전체(`servo_schema.yaml` 4.1.0, `servo2_*` 트랙, 111 테스트, closure matrix)를 **historical 버전으로 태그**하고 삭제하지 않는다.
- Schema 1 잔재(`servo_core_systems.csv`, `servo_validator_channels.csv`, `core_servo_evidence_ledger.json`, `multicoder/`)는 현행대로 historical.

### C.3 신설 (v5)

- `SourceProposition` ledger (B.1) — 인용문·locator·modality·직접 actor/input/output만. **여섯 사례를 여기서부터 재생성.**
- `AuthorAlignment` 레코드 (B.1).
- `DerivedDecisionClaim` 레코드 (B.2 4축).
- Policy class 다중 레이블 + 목적 facet 테이블 (B.4).
- `boundary_unreported` 상태 (B.5).
- worked case: FunSearch deterministic replay (Part D.3).

### C.4 논문 본문 영향 (요약)

- Introduction 연구질문 재정박(A.1): decision-theoretic structure 우선.
- 논증 순서 재편(A.4): Background(POMDP/BED)를 결론까지 이어지는 골격으로 승격, SERVO를 그 대응으로, provenance를 파생으로.
- 주분석 표 교체: closure matrix -> typed functional relation 표 + policy class 표.
- worked case 섹션 신설(FunSearch replay).
- **리스크: 이는 제출본의 논증 골격 재편이다.** camera-ready 대체인지 별도 후속본인지는 Part E.1에서 저자가 결정.

---

## Part D — 실행 순서와 종료 조건

### D.1 실행 순서 (헌법 — churn 방지)

> 주장 틀 동결 -> 규칙 동결 -> source proposition ledger -> 여섯 사례 재분석 -> worked case -> evidence layer -> 3차 적대 검증 -> 원자적 공개

1. **주장 틀 동결** (Part A) — 저자 승인.
2. **규칙 동결** (Part B) — 저자 승인.
3. `SourceProposition` ledger 작성 (판정 없이).
4. 여섯 사례를 source proposition에서 재분석(4축 DerivedDecisionClaim). 부족한 증거는 단조 하향.
5. worked case: FunSearch deterministic replay.
6. evidence layer(graph/provenance)를 **마지막에 파생**.
7. 3차 적대 검증 통과.
8. 원고·표·PDF·패키지를 **단일 생성 경로**에서 원자적으로 공개.

### D.2 종료 조건 (수렴 판정)

- 연구질문·기여·비주장 범위가 먼저 동결됐다.
- 분석 규칙이 사례보다 먼저 동결됐다.
- 여섯 사례가 기존 matrix가 아니라 source proposition부터 재생성됐다.
- 부족한 증거는 단조 하향됐고, inferred occurrence는 positive witness에서 배제됐다.
- **A.4 falsification gate:** POMDP/BED를 제거했을 때 최소 두 사례의 분류나 핵심 결론이 실제로 사라져야 한다. **순환 금지:** 어떤 개념을 제거하면 그 개념의 부재를 진술 못 하는 것은 자명하므로("BED를 제거하면 BED absent를 못 씀"), 이는 PASS 근거가 될 수 없다 — 실제 **사례 판정**이 달라지는지를 본다. 올바른 counterfactual: (a) observation/evaluation 구별 제거 시 C01-D06 boundary demotion·C05의 O_env/V 분리가 실제로 사라지는가; (b) BED에서 유도한 정보상태·`selection_signal`·`selection_objective`·`candidate_execution_rule` 구별을 제거하면 여섯 사례가 다시 **동일한 "adaptive/closed-loop"로 뭉개지는가** — 즉 실패복구(C01)·점수향상+탐색(점수-클러스터 C02/C03/C04/C06)·가설구별 지향(C05)의 서로 다른 피드백 구조가 하나의 서술로 합쳐지는가. 판정 기준은 **사례 해석과 결론이 실제로 바뀌는가**이며 양성 explicit_bed 사례가 0이어도 무관하다(오히려 균일한 performance-direction은 BED 시좌가 드러낸 결과다). 두 사례 이상에서 서술이 실제로 합쳐지면 load-bearing. 다만 출처가 차이를 지지하지 않을 때만 억지 PASS 금지 — 그 경우 BED를 이론적 동기·향후 분석 기준으로 **축소**한다(D.2 (ii)).
  - **실패 처리(원인별):** gate 실패 시 A(상위 정박)로 **무언(無言) 후퇴 금지.** (i) 분석 설계가 약해서 실패면 policy classification·typed functional relation을 재설계한다; (ii) 이론 골격이 실제로 무용하면 decision-theoretic contribution을 **명시적으로 축소하고 그 실패를 문서화**한다. 어느 경우든 실패를 감춘 채 프레이밍만 약화하는 것은 금지한다. (ii)의 결과가 겸손한 프레이밍이 되는 것은 정직한 축소로서 허용되나, 반드시 실패가 본문/헌장에 기록되어야 한다.
- AI-Researcher(또는 제2 모델)는 동결 후 rule-stability check로만 사용.
- 최종 label을 보지 않은 인간 제2검토자가 경계 사례와 FunSearch trace를 독립 판정.
- 세 차례 적대 검증을 모두 통과.
- 원고·표·PDF·패키지가 단일 생성 경로에서 나온다.

### D.3 worked case 사양 — FunSearch deterministic replay

- 원 실험 재현이 아니라 **a deterministic, traceable FunSearch instantiation/replay**로 정확히 명명한다.
- 공식 저장소(google-deepmind/funsearch)를 **고정 commit에 pin**하고, 고정 candidate provider와 seed로 bounded two-step trace를 생성한다.
- 원 논문(Nature 2023)의 procedure claim과 로컬 trace evidence를 **분리**한다.
- 원래 사용된 proprietary LLM이나 완전한 archived trace는 공개되지 않으므로, 재현이 아님을 본문에 명시.

---

## Part E — 저자 결정 (2026-07-23 1차 확정)

- **E.1 산출물 정체성 [확정]:** (a) **저장소 방법론 먼저.** v5 분석 레이어를 저장소 내부에서 재구축하고, 논문(camera-ready/후속본) 반영 여부는 결과를 본 뒤 별도 결정. 가장 안전한 순서.
- **E.2 closure predicate 처리 [확정]:** (a) **완전 퇴역.** 4-predicate를 주분석에서 내리고 부록/역사 또는 worked case의 파생 query로만 유지. Table 2 교체.
- **E.3 연구질문 프레이밍 [확정: B-prime 계열, 재구축 가설]:** 교차검증(Claude 대조 + ChatGPT 비판, 2026-07-23) 결과, decision-first 전면 교체(B)를 채택하되 과잉 전제를 제거한 **B-prime**로 확정. A(상위 정박)는 **fallback이 아니다** — draft A는 참고 이력으로만 보존(`scratchpad/intro_draft_A_anchor.tex`).
  - B는 프레이밍 후보가 아니라 **재구축 가설**이며, A.4 판정 기준(D.2)은 그 가설의 **falsification gate**다.
  - B-prime 필수 수정(적용됨): (1) "at each step a search policy maps I_t to action" 등 모든 사례에 policy/step-mapping 존재를 선취하는 문장 제거; (2) "scientific progress depends on feedback relations" 등 과학 일반 인과 주장 제거; (3) I_t를 존재론적 state로 선취 금지("information exposed as available at decision time"); (4) POMDP/BED를 단순 용어차용이 아니라 diagnostic distinction 제공으로 명시; (5) 퇴역한 4-predicate 언급 삭제 -> typed functional relations + claim_scope 해상도로; (6) "instrumentation"은 문헌 6사례엔 부적절("evidential representation"), FunSearch replay에만 사용; (7) observation/evaluation, iteration/adaptation, adaptive-selection/BED 구별을 Intro에 예고.
  - 목표 텍스트 초안: `scratchpad/intro_draft_B_prime.tex` (B, B-prime 원안은 `intro_draft_B_replace.tex`).
  - **유보(Claude 조정):** B-prime 텍스트의 최종 **동결은 분석 레이어(D.1 3~6) 재구축 후**. B-prime가 선취하는 요소(worked-case 예고, occurrence-level resolution)가 실제 분석 결과와 일치하는지 확인한 뒤 동결. **방향은 지금 확정, 텍스트는 분석 후 동결.** 하류(Abstract/Background/Framework) 재작성도 D.1 순서(analysis -> manuscript)를 따른다.
- **E.4 여섯 사례 [기본 유지]:** 현행 C01~C06(Coscientist, AI Scientist 2024/2026, Agent Laboratory, Robot Scientist, InternAgent) 유지. 변경 시 명시.
- **E.5 worked case [확정]:** **FunSearch deterministic replay.** Part D.3 사양.
- **E.6 제2검토자/적대검증 실행 주체 [미정]:** 인간 제2검토자와 3차 적대검증 수행 주체·방법은 실행 단계에서 확정.

---

## 부록: 8개 단서 -> 현재 상태 대조 (요약)

| # | 단서 | 현재 v4.1 | 판정 |
|---|---|---|---|
| 1 | 연구질문=의사결정 구조, POMDP/BED->SERVO->provenance | Framework 중심, graph 프레이밍 | 미반영(A.1, A.4) |
| 2 | 단조 하향 | established 다수 보존 | 미반영(B.3) |
| 3 | 4축 분리 | 단일 status + evidence/execution_status | 부분(B.2) |
| 4 | 3객체 분리 | ledger json 부재, py만 | 미반영(B.1) |
| 5 | Policy 다중 레이블 | pi 서술형, enum 없음 | 미반영(B.4) |
| 6 | 형식/O_env/boundary_unreported | 본문 154-166,198에 상당 반영 | 부분 반영(B.5) |
| 7 | 충돌 witness(event 재사용) | W01/W15, W10-W12 공유 실측 | 확인됨(C.1) |
| 8 | FunSearch replay | DA01 mini-case만 | 미구현(D.3) |
