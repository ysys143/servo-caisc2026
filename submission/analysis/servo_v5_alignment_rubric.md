# SERVO v5 AuthorAlignment rubric (T5)

- 상태: **v5-rubric-2** (charter B.7 + B.8 구현). v5-rubric-1의 C01 pilot audit가 세 결함을 드러내 version bump(charter B.8 절차: version up + 이유 + 기존 alignment 폐기 + 재생성).
  - **v5-rubric-1 -> v5-rubric-2 변경 이유(C01 pilot audit):** (a) M 정의가 external knowledge retrieval(Google/docs/web search)을 memory로 과다 흡수 -> M을 시스템 내부 persistent storage로 좁히고 external 검색은 external/tool로 분리(§1); (b) G 정의가 code/protocol/query generation에 적용 안 됨 -> G 정의 확장(§1); (c) 부재·부정("no X") 문장 처리 규칙 부재 -> negative/absence 규칙 추가(§2). 기존 `servo_v5_alignments/C01.json`(v5-rubric-1)은 폐기하고 v5-rubric-2로 재생성한다.
- 입력: frozen source proposition의 **T5 consumable projection** = {proposition_id, locator, exact_quote, modality, named_actors, named_inputs, named_outputs}. **`source_context_note`는 읽지 않는다**(freeze projection에서 제외, charter B.8). alignment는 오직 quote와 named_*에서 도출한다.
- 출력: `servo_v5_alignments/C0X.json`, schema `servo_v5_schema.yaml` author_alignment(조합형).

## 원칙
- alignment는 해석이나 **새 사실을 만들지 않는다**: `servo_mapping.source_term`은 소비 proposition의 named_* 또는 exact_quote에 문자적으로 등장해야 한다.
- 하나의 proposition은 0개 이상 alignment를 낳는다. `component_mapping`과 `functional_relation`은 별도 레코드(`assertion_kind`).
- alignment는 판정(support_status/claim_scope/occurrence_resolution)을 내리지 **않는다**. 그건 T6 `derive_claim`.

## 1. component_mapping (assertion_kind=component_mapping)
source_term(quote/named_*에 등장) -> component:
- **G**: 후보 생성 — hypothesis/idea/candidate/program/design **및 code/protocol/experimental-design/search-query/plan 생성**. LLM Planner가 코드·계획·쿼리·프로토콜을 생성하는 서술은 G(생성). (단 그 후보 중 **선택**하거나 다음 action을 정하는 것은 pi.)
- **pi**: 후보 중 선택 또는 다음 action 결정 (select/choose/decide next/rank-then-pick).
- **E**: action을 환경·도구에 적용 (execute/run/perform on robot/tool/compiler).
- **O_env**: 실행 결과로 새 observation 생성 (measurement/spectrum/growth curve/yield/GC-MS result). **E와 구별** — E는 실행 occurrence anchor, O_env는 값을 낳는 환경·측정 법칙.
- **V**: observation/artifact 평가 (evaluate/assess/score/review/critique/verify/test).
- **M**: 시스템 **내부** persistent storage·검색 substrate (episodic/semantic/procedural memory, internal database/archive of the system's own results). **external knowledge retrieval은 M이 아니다** — web/documentation search tool(Google, Docs searcher, Web searcher, API-documentation lookup)은 시스템 밖 지식을 가져오는 것이므로 그 tool은 E(도구 실행) 또는 external(외부 정보원)로 매핑하고, 검색 결과가 저장되어 다음 결정에 쓰인다는 서술이 별도로 있으면 그 저장물만 M/I_t. 단순 "search the internet/documentation"은 M 금지.
- **I_t**: 저장·관측 정보가 **실제 decision input**으로 사용 (used to guide/inform the next decision). **memory_write(M) != decision-relevant state update(I_t)** — 단순 저장은 M, 그 저장물이 다음 결정에 쓰인다는 서술이 있어야 I_t.
- **A**: versioned artifact 상태 (code/protocol/manuscript/model version).
- **W_A**: authored-artifact 합성·수정 interface.
- **external**: 시스템 밖 (human reviewer/workshop/manual selection).
- `basis`: source_term이 명시 component 이름(또는 명백한 동의어)이면 `source_explicit`; 해석이 필요하면 `author_aligned`.

## 2. functional_relation (assertion_kind=functional_relation, 조합형 B.7)
`(source_role, relation_type, target_role, temporal_scope)`:
- ROLE ∈ {candidate, action, execution, observation, evaluation, inquiry_state, memory, artifact, policy, environment, external}
- relation_type ∈ {produces, evaluates, updates, conditions, selects, revises, reads, writes, triggers}
- temporal_scope ∈ {per_step, cross_step}

per-step structural (형식 골격):
- G `produces` candidate; pi `selects` action; E `produces` execution; O_env `produces` observation; V `evaluates` observation; M `writes`/`reads`.

cross-step feedback (연구질문의 대상; **observation != evaluation** 필수):
- observation `updates` inquiry_state
- evaluation `updates` inquiry_state
- inquiry_state `conditions` policy
- evaluation `triggers` execution (repair 유형)
- evaluation `revises` artifact
- memory `conditions` candidate
- memory `conditions` policy

금지: predicate 이름(execution_repair/experimental_adaptation/artifact_revision/discovery_cycle)을 relation 값으로 쓰지 않는다. 모든 feedback을 evaluation 기점으로 만들지 않는다.
- **negative/absence 처리(v5-rubric-2 신설):** 부재·부정 서술("no human decision-making", "not fully automated", "without X", "does not")은 positive functional_relation을 assert하지 **않는다**. 예: "no human decision-making was involved" -> `external conditions policy`를 만들면 안 됨(정반대 의미). 이런 문장은 (i) relation을 만들지 않거나, (ii) 명시적 반대 증거일 때만 소비 proposition의 `polarity=explicit_denial` 태그로 기록한다(관계 방향을 뒤집지 않는다). 부재는 T6에서 support_status를 낮추는 근거이지 relation의 존재 근거가 아니다.
- `boundary_status`: 출처가 E↔O_env 경계를 제공하면 `reported`; 미제공이면 `boundary_unreported`(E를 observation 생산자로 임의 지정 안 함). observation 관련 relation에 적용.

## 3. per-proposition 태그 (T6 derive_claim 입력; 판정 아님, quote 문법 기반)
각 소비 proposition에 대해 alignment 레코드가 부여(원본 proposition에는 저장 안 함, B.1 누출 금지):
- `describes_single_event`: quote가 단일 발생 사건 서술(특정 과거/현재 발생). 예: "Coscientist modifies the protocol ... which ran successfully".
- `describes_cross_run_trend`: quote가 다중 실행/집계 추세. 예: "changes among runs", "increase over time".
- `structurally_inferred`: 순서·연결이 quote에 명시되지 않고 구조 추론(대부분 false; positive witness에서 금지, charter B.3).
- `polarity`: `explicit_denial`(명시적 반대 증거) 또는 `neutral`.
- modality(proposition에서 가져옴)와 결합: `reported_only_as_capability`는 describes_single_event일 수 없다(능력 서술은 occurrence 아님).

## 4. 결정 절차 (proposition 하나)
1. **T5 projection만 본다**(quote/modality/named_*). source_context_note 금지.
2. named_* + quote에서 source_term 식별 -> component_mapping 레코드(들).
3. quote가 서술하는 관계 식별 -> functional_relation 레코드(들) (per-step + 해당 시 cross-step).
4. 소비 proposition에 per-proposition 태그 부여.
5. basis / boundary_status 부여.
6. alignment_id(`C0X-A<nn>`) + proposition_ids 하향 참조.
- proposition이 순수 배경/setup(예: 데이터셋 명명)이라 SERVO 관계가 없으면 alignment를 만들지 않는다(억지 매핑 금지).

## 5. rubric audit & version freeze (charter B.8)
- C01 pilot 생성 후, 대조사례(C05 physical 또는 C03/C06 procedure-heavy)의 5~10 경계 proposition을 **blind**로 재정렬해보고 rubric의 표현상 오류만 수정.
- 통과하면 이 rubric을 **v5-rubric-1 FROZEN**으로 확정하고 C01 포함 전 사례를 같은 버전으로 생성.
- 이후 rubric 변경은 version up + 이유 + 기존 alignment 폐기 + 재생성.
