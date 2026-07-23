# SERVO v5 AuthorAlignment rubric (T5)

- 상태: **v5-rubric-3** (charter B.7 + B.8 구현). v5-rubric-2의 cross-case blind audit(C05 physical, C06 procedure)가 C01(computational chemistry) 과적합을 드러내 version bump(charter B.8 절차: version up + 이유 + 기존 alignment 폐기 + 재생성).
  - **v5-rubric-2 -> v5-rubric-3 변경 이유(cross-case blind audit, C05/C06):** v5-rubric-2는 C01(computational chemistry)에 튜닝되어 (i) 절차적/아키텍처 인용(modality=reported_as_procedure, corpus의 **42%**)에 disposition이 없었고, (ii) V를 observation-evaluation에만 상정한 과적합, (iii) external knowledge retrieval, (iv) 비발생(non-occurrence) 존재 서술에서 실패했다. audit의 recommended_edits를 적용한다.
    - **PRIMARY 4건:** (1) §3 — reported_as_procedure는 **비발생**. component_mapping과 standing loop을 서술하는 per-step **structural** functional_relation은 허용하되, describes_single_event/describes_cross_run_trend 태그와 CROSS-STEP feedback은 특정 occurrence가 명시되지 않는 한 금지. per-proposition `occurrence_class`(architecture/habitual_procedure) 도입. (2) §2 — V per-step 템플릿을 `V evaluates {observation | candidate}`로 일반화(idea/candidate scoring 축복), candidate revision/lineage cross-step 경로 추가(진화하는 idea를 A로 강제하지 않음), pi는 **named picked action** 요구(rank-only는 pi 아니라 V). (3) §1+§2 — 도메인 공개 DB(KEGG 등)·과학 검색/유사도 도구(PSI-BLAST, FASTA, literature/paper search)를 external knowledge retrieval로 명시(검색 ACT=E, 검색된 SOURCE=external), §2에 external relation skeleton 추가. (4) §1 vs §4.6 — occurrence/read/write/decision-use가 없는 순수 존재/아키텍처 서술은 component_mapping만 emit하고 functional_relation 없음.
    - **SECONDARY 3건:** (5) §1 — domain/world model은 시스템이 버전관리·갱신하면 A, 아니면 uncomponented prior-knowledge 입력(M/I_t 강제 금지). (6) §2 — boundary_status에 O_env↔V split(측정 파이프라인) 추가. (7) §3/§4.6 — decomposition guard: 명시적 act 당 relation 1개, whole-loop 요약("repeats the cycle")은 feedback을 license하지 않음.
    - **charter B.8에 따라 이 version bump는 C01 포함 전 사례 alignment를 v5-rubric-3로 전면 재생성하고 v5-rubric-2 alignment를 폐기할 것을 요구한다.**
  - **SCHEMA FOLLOW-UP(스키마 직접 수정 금지):** edit 1의 `occurrence_class`는 현행 스키마 `proposition_tags`에 없는 필드다(현재 필드: describes_single_event / describes_cross_run_trend / structurally_inferred / polarity). `proposition_tags`에 `occurrence_class`(enum 제안: `single_event` / `cross_run_trend` / `architecture` / `habitual_procedure`) 추가를 **schema owner에게 follow-up**으로 요청한다. 스키마 반영 전까지 architecture/habitual은 describes_single_event=false ∧ describes_cross_run_trend=false ∧ structurally_inferred=false + 사유 명시로 표현한다.
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
- **pi**: 후보 중 선택 또는 다음 action 결정 (select/choose/decide next/rank-then-pick). 단, **명명된(picked) action이 없는 rank-only 채점은 pi가 아니라 V**(evaluation 생산)로 매핑한다(§2 참조).
- **E**: action을 환경·도구에 적용 (execute/run/perform on robot/tool/compiler).
- **O_env**: 실행 결과로 새 observation 생성 (measurement/spectrum/growth curve/yield/GC-MS result). **E와 구별** — E는 실행 occurrence anchor, O_env는 값을 낳는 환경·측정 법칙.
- **V**: observation/artifact 평가 (evaluate/assess/score/review/critique/verify/test).
- **M**: 시스템 **내부** persistent storage·검색 substrate (episodic/semantic/procedural memory, internal database/archive of the system's own results). **external knowledge retrieval은 M이 아니다** — web/documentation search tool(Google, Docs searcher, Web searcher, API-documentation lookup)은 시스템 밖 지식을 가져오는 것이므로 그 tool은 E(도구 실행) 또는 external(외부 정보원)로 매핑하고, 검색 결과가 저장되어 다음 결정에 쓰인다는 서술이 별도로 있으면 그 저장물만 M/I_t. 단순 "search the internet/documentation"은 M 금지. **(v5-rubric-3 확장) 도메인 공개 데이터베이스(예: KEGG, UniProt 류)와 과학 검색·유사도 도구(PSI-BLAST, FASTA, literature/paper search)도 external knowledge retrieval이며 M이 아니다.** 이 경우 **검색 ACT(query·run search·BLAST 실행)는 E(도구 실행), 검색된 SOURCE/knowledge(반환된 DB 레코드·hit·문헌)는 external**로 매핑한다. 반환된 지식이 시스템 내부에 저장되어 다음 결정에 쓰인다는 서술이 별도로 있을 때만 그 저장물이 M/I_t.
- **I_t**: 저장·관측 정보가 **실제 decision input**으로 사용 (used to guide/inform the next decision). **memory_write(M) != decision-relevant state update(I_t)** — 단순 저장은 M, 그 저장물이 다음 결정에 쓰인다는 서술이 있어야 I_t.
- **A**: versioned artifact 상태 (code/protocol/manuscript/model version).
- **W_A**: authored-artifact 합성·수정 interface.
- **external**: 시스템 밖 정보원·주체 (human reviewer/workshop/manual selection, **도메인 공개 DB·과학 검색 도구가 반환한 외부 지식** — KEGG/PSI-BLAST/FASTA/literature hit 등 retrieved knowledge, §2 external retrieval 골격 참조).
- `basis`: source_term이 명시 component 이름(또는 명백한 동의어)이면 `source_explicit`; 해석이 필요하면 `author_aligned`.
- **순수 존재·아키텍처 서술 규칙(v5-rubric-3; §4.6와 정합):** occurrence/read/write/decision-use가 **전혀 없는** 순수 존재·아키텍처 서술 — 예: "there is a MySQL database storing all data"(=M), "provides an interface for X"(=W_A 또는 해당 component) — 은 **component_mapping(basis=source_explicit)만 emit하고 functional_relation은 만들지 않는다.** 이는 §1의 "such storage IS M"과 §4.6 억지 매핑 금지를 화해시킨다. relation은 quote가 실제 read/write/use act를 서술할 때만 생성한다.
- **domain/world model = prior knowledge(v5-rubric-3):** 도메인·세계 모델(예: yeast-metabolism model / iFF708)은 기본적으로 prior knowledge다. 시스템이 그것을 **버전관리·갱신**하면 `A`(artifact)로 매핑하고, 아니면 component 없는 **prior-knowledge 입력**으로 두어 M/I_t로 강제하지 않는다. 개정될 때 update-target: 모델이 시스템의 versioned artifact이면 기본 `evaluation revises artifact`; decision-state 변화가 **명시**된 경우에만 `evaluation updates inquiry_state`.

## 2. functional_relation (assertion_kind=functional_relation, 조합형 B.7)
`(source_role, relation_type, target_role, temporal_scope)`:
- ROLE ∈ {candidate, action, execution, observation, evaluation, inquiry_state, memory, artifact, policy, environment, external}
- relation_type ∈ {produces, evaluates, updates, conditions, selects, revises, reads, writes, triggers}
- temporal_scope ∈ {per_step, cross_step}

per-step structural (형식 골격):
- G `produces` candidate; pi `selects` action; E `produces` execution; O_env `produces` observation; V `evaluates` {observation | candidate}; M `writes`/`reads`.
- **V 평가 대상(v5-rubric-3): `V evaluates {observation | candidate}`.** V의 per-step 평가 대상은 observation에 국한되지 않는다. idea/candidate scoring(가설·후보를 채점·심사·평가)은 `target_role=candidate`로 축복한다(`V evaluates candidate`). **observation != evaluation 불변은 유지** — O_env가 낳는 raw observation과 V의 평가는 여전히 별개 role이며, cross-step에서 둘을 다시 합치지 않는다.
- **pi는 NAMED picked action 요구(v5-rubric-3): rank-only는 V.** `pi selects action`은 quote에 **명명된(picked) action/후보**가 있을 때만 생성한다. 순위만 매기고(rank/score only) 선택된 action이 명시되지 않으면 pi가 아니라 V(`V evaluates candidate`, 즉 evaluation 생산)로 매핑한다.

cross-step feedback (연구질문의 대상; **observation != evaluation** 필수):
- observation `updates` inquiry_state
- evaluation `updates` inquiry_state
- inquiry_state `conditions` policy
- evaluation `triggers` execution (repair 유형)
- evaluation `revises` artifact
- evaluation `revises` candidate (v5-rubric-3; 진화하는 idea/candidate 개정. **A(versioned artifact)로 강제하지 않는다** — candidate가 시스템의 versioned artifact가 아닐 때 이 경로 사용)
- G `revises` candidate (v5-rubric-3; candidate lineage — 이전 후보를 개정해 다음 후보를 생성, generator 기점)
- memory `conditions` candidate
- memory `conditions` policy

external retrieval 골격 (v5-rubric-3 신설; external은 지금까지 relation template 없는 ROLE였다):
- E `reads` external (검색·조회 ACT가 외부 정보원을 읽음; 이때 경계는 E↔O_env가 아니라 E↔external)
- external `conditions` candidate (검색된 외부 지식이 후보 생성을 조건화)
- external `conditions` policy (검색된 외부 지식이 다음 결정 규칙을 조건화; decision-use가 명시된 경우만)
  - 주: "supply/input" 의미는 relation_type enum(§2 상단)에 supply가 없으므로 `conditions`로 표현한다(외부 지식이 후보·정책을 조건화).

금지: predicate 이름(execution_repair/experimental_adaptation/artifact_revision/discovery_cycle)을 relation 값으로 쓰지 않는다. 모든 feedback을 evaluation 기점으로 만들지 않는다.
- **negative/absence 처리(v5-rubric-2 신설):** 부재·부정 서술("no human decision-making", "not fully automated", "without X", "does not")은 positive functional_relation을 assert하지 **않는다**. 예: "no human decision-making was involved" -> `external conditions policy`를 만들면 안 됨(정반대 의미). 이런 문장은 (i) relation을 만들지 않거나, (ii) 명시적 반대 증거일 때만 소비 proposition의 `polarity=explicit_denial` 태그로 기록한다(관계 방향을 뒤집지 않는다). 부재는 T6에서 support_status를 낮추는 근거이지 relation의 존재 근거가 아니다.
- `boundary_status`: 출처가 E↔O_env 경계를 제공하면 `reported`; 미제공이면 `boundary_unreported`(E를 observation 생산자로 임의 지정 안 함). observation 관련 relation에 적용.
  - **(v5-rubric-3 확장) O_env↔V 경계도 동일하게 보고한다.** 측정 파이프라인에서 raw/측정 신호와 기계적 변환(smoothing, parameter extraction)은 `O_env`(observation), confirm/refute/threshold/통계적 결정 step은 `V`(evaluation). 출처가 이 O_env↔V 분기를 제공하면 `reported`, 미제공이면 `boundary_unreported`(측정·변환 step을 임의로 V로 승격하지 않는다). E↔O_env 규칙을 mirror한다.

## 3. per-proposition 태그 (T6 derive_claim 입력; 판정 아님, quote 문법 기반)
각 소비 proposition에 대해 alignment 레코드가 부여(원본 proposition에는 저장 안 함, B.1 누출 금지):
- `describes_single_event`: quote가 단일 발생 사건 서술(특정 과거/현재 발생). 예: "Coscientist modifies the protocol ... which ran successfully".
- `describes_cross_run_trend`: quote가 다중 실행/집계 추세. 예: "changes among runs", "increase over time".
- `structurally_inferred`: 순서·연결이 quote에 명시되지 않고 구조 추론(대부분 false; positive witness에서 금지, charter B.3).
- `polarity`: `explicit_denial`(명시적 반대 증거) 또는 `neutral`.
- modality(proposition에서 가져옴)와 결합: `reported_only_as_capability`는 describes_single_event일 수 없다(능력 서술은 occurrence 아님).
- **`occurrence_class`(v5-rubric-3 신설; SCHEMA FOLLOW-UP): `reported_as_procedure` = 비발생(non-occurrence).** modality=`reported_as_procedure`인 절차적/아키텍처(습관적) 인용은 특정 발생 사건을 서술하지 않는다. 이런 proposition은 component_mapping과, 시스템이 돌도록 명시된 standing loop을 서술하는 **per-step STRUCTURAL functional_relation**(§2 per-step 골격)은 emit할 수 있으나, `describes_single_event`나 `describes_cross_run_trend`로 태그해서는 **안 되며**, quote에 특정 occurrence가 명시되지 않는 한 **CROSS-STEP feedback relation을 license하지 않는다**(§2 cross-step set 금지). disposition을 `occurrence_class ∈ {single_event, cross_run_trend, architecture, habitual_procedure}`로 기록한다: 순수 아키텍처 서술=`architecture`, 습관적 절차=`habitual_procedure`. **스키마 반영 전 임시 표현:** describes_single_event=false ∧ describes_cross_run_trend=false ∧ structurally_inferred=false + 사유(예: "reported_as_procedure; standing loop, no stated occurrence"). SCHEMA FOLLOW-UP은 상단 changelog 참조.

## 4. 결정 절차 (proposition 하나)
1. **T5 projection만 본다**(quote/modality/named_*). source_context_note 금지.
2. named_* + quote에서 source_term 식별 -> component_mapping 레코드(들).
3. quote가 서술하는 관계 식별 -> functional_relation 레코드(들) (per-step + 해당 시 cross-step).
4. 소비 proposition에 per-proposition 태그 부여.
5. basis / boundary_status 부여.
6. alignment_id(`C0X-A<nn>`) + proposition_ids 하향 참조.
- proposition이 순수 배경/setup(예: 데이터셋 명명)이라 SERVO 관계가 없으면 alignment를 만들지 않는다(억지 매핑 금지).
- **decomposition guard(v5-rubric-3; §3와 정합):** **명시적으로 서술된 act 당 functional_relation 1개**만 emit한다. whole-loop 요약 문장을 다수의 발명된 cross-step feedback으로 폭발시키지 않는다. 예: "repeats the cycle" 단독은 feedback relation을 license하지 않는다(cross-step은 quote가 특정 act·연결을 명시할 때만; structurally_inferred cross-step 금지, charter B.3). reported_as_procedure(§3, occurrence_class=architecture/habitual_procedure)와 결합될 때 특히 주의한다.

## 5. rubric audit & version freeze (charter B.8)
- C01 pilot 생성 후, 대조사례(C05 physical 또는 C03/C06 procedure-heavy)의 5~10 경계 proposition을 **blind**로 재정렬해보고 rubric의 표현상 오류만 수정.
- 통과하면 이 rubric을 **v5-rubric-1 FROZEN**으로 확정하고 C01 포함 전 사례를 같은 버전으로 생성.
- 이후 rubric 변경은 version up + 이유 + 기존 alignment 폐기 + 재생성.
