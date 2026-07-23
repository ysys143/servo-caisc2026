# SERVO v5 AuthorAlignment rubric (T5)

- 상태: **FROZEN v5-rubric-1** (charter B.7 + B.8 구현). rubric audit(C01 pilot + 대조사례 blind pilot) 후 version freeze로 승격. 이 버전에 대해 C01을 생성하고, C01 결과로 rubric을 **자유 변경하지 않는다**(charter B.8: 수정 시 version up + 이유 기록 + 기존 alignment 폐기 + 재생성).
- 입력: frozen source proposition의 **T5 consumable projection** = {proposition_id, locator, exact_quote, modality, named_actors, named_inputs, named_outputs}. **`source_context_note`는 읽지 않는다**(freeze projection에서 제외, charter B.8). alignment는 오직 quote와 named_*에서 도출한다.
- 출력: `servo_v5_alignments/C0X.json`, schema `servo_v5_schema.yaml` author_alignment(조합형).

## 원칙
- alignment는 해석이나 **새 사실을 만들지 않는다**: `servo_mapping.source_term`은 소비 proposition의 named_* 또는 exact_quote에 문자적으로 등장해야 한다.
- 하나의 proposition은 0개 이상 alignment를 낳는다. `component_mapping`과 `functional_relation`은 별도 레코드(`assertion_kind`).
- alignment는 판정(support_status/claim_scope/occurrence_resolution)을 내리지 **않는다**. 그건 T6 `derive_claim`.

## 1. component_mapping (assertion_kind=component_mapping)
source_term(quote/named_*에 등장) -> component:
- **G**: 후보(hypothesis/idea/candidate/program/design) 생성.
- **pi**: 후보 중 선택 또는 다음 action 결정 (select/choose/decide next/rank-then-pick).
- **E**: action을 환경·도구에 적용 (execute/run/perform on robot/tool/compiler).
- **O_env**: 실행 결과로 새 observation 생성 (measurement/spectrum/growth curve/yield/GC-MS result). **E와 구별** — E는 실행 occurrence anchor, O_env는 값을 낳는 환경·측정 법칙.
- **V**: observation/artifact 평가 (evaluate/assess/score/review/critique/verify/test).
- **M**: 정보 저장·검색 substrate (store/record/database/archive/memory).
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
