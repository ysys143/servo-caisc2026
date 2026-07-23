# SERVO v5 AuthorAlignment rubric (T5)

- 상태: **v5-rubric-4** (charter B.7 + B.8 구현). v5-rubric-3의 6사례 full run(전 사례 validated)이 class-level coverage/consistency의 **스키마 구조 gap**을 드러내 version bump(charter B.8 절차: version up + 이유 + 기존 alignment 폐기 + 재생성).
  - **POLICY 축 재설계(charter B.4 재작성 2026-07-23; version 유지 v5-rubric-4):** charter B.4가 재작성되어 policy를 `explicit_bed` compliance label 채점에서 **BED 렌즈에 의한 5축 분해**로 바꿨다. 이에 맞춰 policy portion(신설 §6)을 5축(control_dependence / selection_signal / selection_objective / candidate_execution_rule / formal_epistemic_utility_evidence)으로 재작성한다. 이는 AuthorAlignment 문법(§1 component_mapping / §2 functional_relation / §3 tags / §4 절차)을 건드리지 않는 **charter-B.4-driven 문서 갱신**이므로 version bump이 아니며 기존 alignment 재생성을 요구하지 않는다(policy 산출물만 재생성). `servo_v5_schema.yaml`의 policy 객체와 `servo_v5_policy/C0X.json` 6종이 함께 갱신됐다.
  - **POLICY schema-v3 재도출(contract §B, 2026-07-23; version 유지 v5-rubric-4):** 저자 조건부 승인 spec(contract §B)에 따라 5축을 **7축으로 재도출**했다. `control_dependence`는 `none`을 폐기하고 `fixed_or_predefined`(출처 확인된 결과-독립)와 `not_reported`(출처 침묵)로 분리; `selection_objective`는 `performance`→`performance_improvement`, `exploration` 폐기, `diversity_directed_selection` 신설; **신규** `generation_scope`(G/S 수준 provenance, 표 A 열 아님)와 `candidate_selection_rule`을 추가; `candidate_execution_rule`은 objective가 섞인 `expected_discrimination_selected`를 삭제하고 실행-방식 enum(all_selected/one_at_a_time/batch/until_success/until_budget/source_unreported)으로 재정의; `formal_epistemic_utility_evidence`의 리터럴 `none`→`not_reported`. §6를 7축으로 재작성. 이 역시 AuthorAlignment 문법을 건드리지 않는 **contract-§B-driven policy-only 갱신**이므로 version bump이 아니다(policy 산출물만 재생성). `servo_v5_schema.{yaml,py}`의 policy 계약, `servo_v5_policy/C0X.json` 6종, `build_servo_v5_tables.py`의 policy/Table-A 부분, policy 테스트가 함께 갱신됐다.
  - **v5-rubric-3 -> v5-rubric-4 변경 이유(six-case full run; 전 사례 validated이나 class-level gap):** 6개 사례를 v5-rubric-3로 전면 생성·검증한 결과 개별 레코드는 통과하나 문법(스키마·표현) 자체의 **3개 구조 gap + 2개 부수 정합**이 체계적(cross-case)으로 드러났다. 스키마 소유자와 합의된 스키마 구조 수정이다(`servo_v5_schema.yaml`/`servo_v5_io.py` 반영 완료).
    - **SCHEMA GAP 3건:** (1) **비발생 modality의 disposition host 부재** — `polarity=explicit_denial`은 지금까지 functional_relation의 `proposition_tags`에만 실렸으나, negative/absence 규칙(§2)은 positive functional_relation을 금지하므로 autonomy/absence 부정(C01-P05/P73/P14, C02-P40/P47, C03-P12, C04-P23/P32, C05-P09/P24)이 구조적으로 기록 불가였다. **수정: component_mapping에 optional `polarity`{neutral, explicit_denial} 필드를 직접 허용**(absence 서술이 component_mapping만 낳아도 polarity=explicit_denial 기록 가능; §2 negative/absence 참조). 또한 occurrence_class enum에 `reported_only_as_capability` modality 대응값이 없어 능력(capability) 인용(C01-P77/P10/P84, C04-P09, C06-P16)에 disposition이 없었다 — **occurrence_class enum에 `capability_only` 추가** {single_event, cross_run_trend, architecture, habitual_procedure, capability_only}. (2) **generator source_role: rubric-text-vs-enum 모순** — rubric은 "G produces/revises candidate"라 하나 ROLE enum(source_role/target_role)에 generator가 없어 모든 generation edge가 비일관 proxy(C01 inquiry_state vs C04/C05 candidate->candidate self-loop)로 강제됐다. **수정: ROLE enum(source_role AND target_role)에 `generation` 추가**, §2 per-step 골격을 `generation produces candidate`/`generation revises candidate`로 정규화(inquiry_state/self-loop proxy 퇴역). observation != evaluation 등 나머지 불변 유지. (3) **alignment_id 2자리 cap의 데이터 손실** — `^{case}-A\d{2}$`가 사례당 99개로 제한, C06은 119개 생성 후 ~25개 trim됐다. **수정: alignment_id를 3자리로 확대**(`servo_v5_io.py` `[0-9]{2,3}`; alignment id만, proposition/claim id는 유지).
    - **부수 정합 2건:** (a) **external-as-evaluator 골격** — external은 ROLE에 있으나 evaluator/source로 미형식화. §2에 `external evaluates candidate`/`external evaluates artifact` 골격을 추가해 외부 리뷰어/검증자(C02-P39/C03-P15/C04-P20-22/C06-P06-32)를 균일 매핑. (b) **V per-step target 확대** — `V evaluates {observation | candidate}`를 `V evaluates {observation | candidate | artifact}`로 확대해 저자 논문에 대한 리뷰어 평가(C02-P38/P39, C04-P20/P22)를 candidate 강제 없이 수용.
    - **NOT a gap(유지 확정):** reported_as_procedure -> 비발생 규칙과 그 아래 cross-step feedback 억제(C02/C03/C04/C06 procedure props)는 의도적으로 강화된 v3 증거 문턱으로 rubric-정합·정당하며 완화 시 audit 판정을 역전시키므로 **그대로 둔다**(§3 occurrence gating·§4.6 decomposition guard 불변).
    - **charter B.8에 따라 이 version bump는 C01 포함 전 사례 alignment를 v5-rubric-4로 전면 재생성하고 v5-rubric-3 alignment를 폐기할 것을 요구한다.** 동결 불변 유지: observation != evaluation, predicate 이름 금지, closure-score aggregation 금지, source_context_note 제외, source_term 문자적.
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
- **optional `polarity`(v5-rubric-4):** component_mapping 레코드는 optional top-level `polarity ∈ {neutral, explicit_denial}` 필드를 가질 수 있다. 부재·부정 서술(§2 negative/absence)이 positive functional_relation 없이 component_mapping만 낳을 때 `explicit_denial`을 여기 싣는다(생략 시 neutral로 간주). functional_relation은 이 필드를 top-level로 갖지 못하며 polarity는 `proposition_tags[].polarity`에 싣는다.
- **순수 존재·아키텍처 서술 규칙(v5-rubric-3; §4.6와 정합):** occurrence/read/write/decision-use가 **전혀 없는** 순수 존재·아키텍처 서술 — 예: "there is a MySQL database storing all data"(=M), "provides an interface for X"(=W_A 또는 해당 component) — 은 **component_mapping(basis=source_explicit)만 emit하고 functional_relation은 만들지 않는다.** 이는 §1의 "such storage IS M"과 §4.6 억지 매핑 금지를 화해시킨다. relation은 quote가 실제 read/write/use act를 서술할 때만 생성한다.
- **domain/world model = prior knowledge(v5-rubric-3):** 도메인·세계 모델(예: yeast-metabolism model / iFF708)은 기본적으로 prior knowledge다. 시스템이 그것을 **버전관리·갱신**하면 `A`(artifact)로 매핑하고, 아니면 component 없는 **prior-knowledge 입력**으로 두어 M/I_t로 강제하지 않는다. 개정될 때 update-target: 모델이 시스템의 versioned artifact이면 기본 `evaluation revises artifact`; decision-state 변화가 **명시**된 경우에만 `evaluation updates inquiry_state`.

## 2. functional_relation (assertion_kind=functional_relation, 조합형 B.7)
`(source_role, relation_type, target_role, temporal_scope)`:
- ROLE ∈ {candidate, action, execution, observation, evaluation, inquiry_state, memory, artifact, policy, environment, external, generation}
  - **(v5-rubric-4) `generation`**은 후보 생성기(component G)의 functional_relation ROLE이다. 이전에는 generation edge에 전용 ROLE이 없어 inquiry_state나 candidate->candidate self-loop 같은 비일관 proxy로 강제됐다. 이제 generator 기점 관계는 `generation`을 source_role로 쓴다(아래 골격 참조).
- relation_type ∈ {produces, evaluates, updates, conditions, selects, revises, reads, writes, triggers}
- temporal_scope ∈ {per_step, cross_step}

per-step structural (형식 골격):
- generation `produces` candidate; pi `selects` action; E `produces` execution; O_env `produces` observation; V `evaluates` {observation | candidate | artifact}; M `writes`/`reads`. (**v5-rubric-4:** generator 기점은 source_role=`generation`; `G produces candidate` proxy 퇴역. V target에 artifact 추가.)
- **V 평가 대상(v5-rubric-4로 확대): `V evaluates {observation | candidate | artifact}`.** V의 per-step 평가 대상은 observation에 국한되지 않는다. idea/candidate scoring(가설·후보를 채점·심사·평가)은 `target_role=candidate`로 축복한다(`V evaluates candidate`). **(v5-rubric-4)** 저자·authored artifact(논문·manuscript·code version)를 평가·심사·리뷰하는 서술은 `target_role=artifact`로 매핑한다(`V evaluates artifact`) — 리뷰어가 산출물을 평가할 때 candidate로 강제하지 않는다(예: C02-P38/P39, C04-P20/P22). **observation != evaluation 불변은 유지** — O_env가 낳는 raw observation과 V의 평가는 여전히 별개 role이며, cross-step에서 둘을 다시 합치지 않는다.
- **pi는 NAMED picked action 요구(v5-rubric-3): rank-only는 V.** `pi selects action`은 quote에 **명명된(picked) action/후보**가 있을 때만 생성한다. 순위만 매기고(rank/score only) 선택된 action이 명시되지 않으면 pi가 아니라 V(`V evaluates candidate`, 즉 evaluation 생산)로 매핑한다.

cross-step feedback (연구질문의 대상; **observation != evaluation** 필수):
- observation `updates` inquiry_state
- evaluation `updates` inquiry_state
- inquiry_state `conditions` policy
- evaluation `triggers` execution (repair 유형)
- evaluation `revises` artifact
- evaluation `revises` candidate (v5-rubric-3; 진화하는 idea/candidate 개정. **A(versioned artifact)로 강제하지 않는다** — candidate가 시스템의 versioned artifact가 아닐 때 이 경로 사용)
- generation `revises` candidate (v5-rubric-4; candidate lineage — 이전 후보를 개정해 다음 후보를 생성, generator 기점. source_role=`generation`; 이전 `G revises candidate` proxy 퇴역)
- memory `conditions` candidate
- memory `conditions` policy

external retrieval 골격 (v5-rubric-3 신설; external은 지금까지 relation template 없는 ROLE였다):
- E `reads` external (검색·조회 ACT가 외부 정보원을 읽음; 이때 경계는 E↔O_env가 아니라 E↔external)
- external `conditions` candidate (검색된 외부 지식이 후보 생성을 조건화)
- external `conditions` policy (검색된 외부 지식이 다음 결정 규칙을 조건화; decision-use가 명시된 경우만)
  - 주: "supply/input" 의미는 relation_type enum(§2 상단)에 supply가 없으므로 `conditions`로 표현한다(외부 지식이 후보·정책을 조건화).

external evaluator 골격 (v5-rubric-4 신설; external은 knowledge source뿐 아니라 evaluator/source로도 매핑된다):
- external `evaluates` candidate (외부 리뷰어·워크숍·수동 심사자가 후보·아이디어를 평가·심사·채점)
- external `evaluates` artifact (외부 리뷰어·검증자가 authored artifact/논문·code version을 평가·심사·검증; human reviewer/peer review/manual verification)
  - 외부 주체가 시스템 밖에서 후보·산출물을 평가하는 서술을 균일하게 매핑한다(예: C02-P39, C03-P15, C04-P20-22, C06-P06/P32). 시스템 내부 V(component)의 평가(`V evaluates ...`)와 구별 — 평가 주체가 external이면 source_role=`external`.

금지: predicate 이름(execution_repair/experimental_adaptation/artifact_revision/discovery_cycle)을 relation 값으로 쓰지 않는다. 모든 feedback을 evaluation 기점으로 만들지 않는다.
- **negative/absence 처리(v5-rubric-2 신설; v5-rubric-4로 host 확정):** 부재·부정 서술("no human decision-making", "not fully automated", "without X", "does not")은 positive functional_relation을 assert하지 **않는다**. 예: "no human decision-making was involved" -> `external conditions policy`를 만들면 안 됨(정반대 의미). 이런 문장은 (i) relation을 만들지 않거나, (ii) 명시적 반대 증거일 때만 `polarity=explicit_denial`로 기록한다(관계 방향을 뒤집지 않는다). **disposition host(v5-rubric-4):** functional_relation을 낳는 proposition이면 그 레코드의 `proposition_tags[].polarity=explicit_denial`에 싣고, 부재 서술이 **오직 component_mapping만** 낳으면(negative 규칙상 positive functional_relation 금지) 그 component_mapping 레코드의 optional top-level `polarity=explicit_denial` 필드에 직접 싣는다(GAP 1: 비발생 modality의 disposition host). 부재는 T6에서 support_status를 낮추는 근거이지 relation의 존재 근거가 아니다.
- `boundary_status`: 출처가 E↔O_env 경계를 제공하면 `reported`; 미제공이면 `boundary_unreported`(E를 observation 생산자로 임의 지정 안 함). observation 관련 relation에 적용.
  - **(v5-rubric-3 확장) O_env↔V 경계도 동일하게 보고한다.** 측정 파이프라인에서 raw/측정 신호와 기계적 변환(smoothing, parameter extraction)은 `O_env`(observation), confirm/refute/threshold/통계적 결정 step은 `V`(evaluation). 출처가 이 O_env↔V 분기를 제공하면 `reported`, 미제공이면 `boundary_unreported`(측정·변환 step을 임의로 V로 승격하지 않는다). E↔O_env 규칙을 mirror한다.

## 3. per-proposition 태그 (T6 derive_claim 입력; 판정 아님, quote 문법 기반)
각 소비 proposition에 대해 alignment 레코드가 부여(원본 proposition에는 저장 안 함, B.1 누출 금지):
- `describes_single_event`: quote가 단일 발생 사건 서술(특정 과거/현재 발생). 예: "Coscientist modifies the protocol ... which ran successfully".
- `describes_cross_run_trend`: quote가 다중 실행/집계 추세. 예: "changes among runs", "increase over time".
- `structurally_inferred`: 순서·연결이 quote에 명시되지 않고 구조 추론(대부분 false; positive witness에서 금지, charter B.3).
- `polarity`: `explicit_denial`(명시적 반대 증거) 또는 `neutral`.
- modality(proposition에서 가져옴)와 결합: `reported_only_as_capability`는 single_event일 수 없다(능력 서술은 occurrence 아님); **(v5-rubric-4)** 이 경우 `occurrence_class=capability_only`로 기록한다.
- **`occurrence_class`(v5-rubric-3 신설; SCHEMA FOLLOW-UP): `reported_as_procedure` = 비발생(non-occurrence).** modality=`reported_as_procedure`인 절차적/아키텍처(습관적) 인용은 특정 발생 사건을 서술하지 않는다. 이런 proposition은 component_mapping과, 시스템이 돌도록 명시된 standing loop을 서술하는 **per-step STRUCTURAL functional_relation**(§2 per-step 골격)은 emit할 수 있으나, `describes_single_event`나 `describes_cross_run_trend`로 태그해서는 **안 되며**, quote에 특정 occurrence가 명시되지 않는 한 **CROSS-STEP feedback relation을 license하지 않는다**(§2 cross-step set 금지). disposition을 `occurrence_class ∈ {single_event, cross_run_trend, architecture, habitual_procedure, capability_only}`로 기록한다: 순수 아키텍처 서술=`architecture`, 습관적 절차=`habitual_procedure`, **(v5-rubric-4) modality=`reported_only_as_capability`인 능력 서술=`capability_only`**(occurrence 아님; single_event/cross_run_trend 금지). **스키마 반영 전 임시 표현:** describes_single_event=false ∧ describes_cross_run_trend=false ∧ structurally_inferred=false + 사유(예: "reported_as_procedure; standing loop, no stated occurrence"). SCHEMA FOLLOW-UP은 상단 changelog 참조.

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

## 6. Policy 7축 분해 (BED 렌즈; charter B.4 / contract §B schema-v3 재도출, 2026-07-23)

policy는 AuthorAlignment(§1~§4)와 **별개의 case-level 산출물**이다(`servo_v5_policy/C0X.json`, 사례당 flat record 1개, id·record list 없음). **BED는 compliance label이 아니라 분석 렌즈다** — "시스템이 BED를 준수하는가"를 채점하지 않는다(POMDP를 렌즈로만 쓰는 것과 대칭). 모두 adaptive해 보이는 선택 정책들의 목적과 선택 논리를 서로 **다르게** 판정하기 위해 일곱 축으로 분해한다. 각 축값은 rationale에서 **proposition_ids에 정박**한다(억지 매핑 금지; 출처가 지지하지 않으면 축값을 넣지 않는다).

**설계 원칙(schema-v3, 절대 불변):** (a) 목적(`selection_objective`)과 규칙(`candidate_selection_rule`/`candidate_execution_rule`)을 **절대 재혼합하지 않는다** — 규칙 축에 objective 값을 넣지 않는다. (b) **빈값/침묵을 부재 증거로 쓰지 않는다** — 출처가 결과-무관을 확인하면 `fixed_or_predefined`, 출처 침묵이면 `not_reported`.

- **`control_dependence`** (enum LIST, 무엇이 선택을 변화시키는가): `fixed_or_predefined`(결과-독립 무조건 진행이 **출처에서 확인됨**) / `failure`(오류·예외가 수선을 구동) / `score`(품질·성능 점수가 선택을 구동) / `observation_result`(실행 결과가 다음 선택을 조건화) / `uncertainty`(불확실성이 선택을 구동) / `candidate_disagreement`(후보 간 불일치가 선택을 구동) / `not_reported`(공개 자료로 판정 불가; source silence). 이전 `none` 폐기. 예: `fixed_or_predefined`는 C04-P23(자율모드 서브태스크 순차 진행)·C05-P13~P16(결정적 4단계 방법). **출처 침묵을 절대 fixed로 취급하지 않는다.**
- **`selection_signal`** (free-string LIST, 비어 있지 않음): 선택을 실제 구동하는 **구체적 신호명**. control_dependence와 겹칠 수 있으나 더 구체적으로 명명한다(예: "reaction yield", "sequence similarity (PSI-BLAST/FASTA)", "assessment-agent idea score (0-10)"). **신호가 보고됐어도 후속 선택에 쓰이지 않으면** selection_signal에는 남기되 control_dependence는 `not_reported`/`fixed_or_predefined`로 둔다(신호 존재 ≠ 통제 의존).
- **`selection_objective`** (enum LIST, π 목적 facet만): `local_repair`(국소 수선) / `performance_improvement`(성능·품질 향상) / `uncertainty_reduction`(측정·추정 불확실성 감소) / `hypothesis_model_discrimination`(가설·모델 판별) / `diversity_directed_selection`(**선택 단계**의 다양성 선택). 이전 `performance`→`performance_improvement`. 이전 `exploration`은 폐기하고, 생성 단계 성분은 `generation_scope`로, 선택(π) 단계 다양성은 `diversity_directed_selection`로 분해한다.
- **`generation_scope`** (enum LIST, **신규 G/S 수준 provenance 축; 표 A 열 아님**): `fixed_space`(고정 후보 공간) / `search_space_expansion`(표현·검색공간 확장) / `candidate_diversification`(생성 단계 후보 다양화). 퇴역 `exploration`의 **생성 단계** 성분을 흡수한다. 문헌유사도·중복회피·다양성 서술이 **생성 단계**에 있으면 여기(예: C03-P43/P44 중복회피, C04-P15 top-program 다양성, C06-P11/P16 고온·유사도-방지), **표현·검색공간 확장**이면 `search_space_expansion`(예: C03-P20 open-ended discovery). **선택(π) 단계**의 다양성 필터는 여기가 아니라 `selection_objective`의 `diversity_directed_selection`(예: C02-P12/P13 생성-후 유사도 필터). 각 재분류를 proposition_id로 정박.
- **`candidate_selection_rule`** (enum LIST, **신규 — 후보 집합에서 무엇을 고르는가**): `fixed`(고정) / `threshold`(임계값 필터) / `top_k_ranked`(점수 상위) / `sampled_subset`(표집 부분집합) / `sequential_choice`(순차 선택) / `exhaustive`(전수) / `not_reported`.
- **`candidate_execution_rule`** (enum LIST, **재정의 — 선택된 후보를 어떻게 실행하는가; objective 절대 불포함**): `all_selected`(선택분 전부 실행) / `one_at_a_time`(하나씩) / `batch`(일괄·병렬) / `until_success`(성공까지) / `until_budget`(예산·시도한도까지) / `source_unreported`. 이전 `expected_discrimination_selected`(목적+메커니즘 혼합) **삭제**. **주의:** discrimination을 *목적*으로 갖는 것(`selection_objective`)과 후보를 실제로 어떻게 고르고 실행하는가(두 rule 축)는 별개다 — C05는 목적이 판별이어도 후보를 전부 시험하므로 `selection_rule=exhaustive`, `execution_rule=all_selected`로 분리 기록한다.
- **`formal_epistemic_utility_evidence`** (string): BED의 명시적 수학구조(posterior/likelihood/EIG/VOI/epistemic_utility)를 selection rule에 직접 쓴다는 보고의 인용, 없으면 리터럴 `"not_reported"`. **보조 facet일 뿐 핵심 label 아니다.** 여섯 사례 전부 `"not_reported"`이며, per-case 판정이 아니라 **corpus-level limitation으로 각주에 한 번만** 기술한다.

금지: BED를 mechanism label이나 compliance(present/absent) 판정으로 쓰지 않는다. `explicit_bed=false 6/6` 같은 결과를 중심 표로 만들지 않는다. 산출은 7축 분해이며, C05(`hypothesis_model_discrimination`/`uncertainty_reduction` 목적 + `exhaustive`/`all_selected` rule)가 점수-클러스터(`performance_improvement` 목적 + `top_k_ranked`/`threshold`/`sequential_choice` rule)와 실제로 갈리는 것이 이 분해의 요점이다.

## Annex A — documentation notes (non-normative, v5-rubric-4 freeze)

v5-rubric-4 freeze verdict(six-case full run)가 "documentation-annex candidates, NOT version-bump triggers"로 분류한 저빈도 항목 3건을 기록한다. 아래는 의도적 설계 선택이며 규칙 변경이나 gap이 아니다.

- **external-actor verb granularity**: external 골격(§2)은 `external evaluates {candidate|artifact}`만 축복한다. 인간의 SELECTION(예: C03의 수동 필터링·제출물 선정)이나 수동 REVISION(C05)은 전용 predicate 없이 `external evaluates ...`로 근사되거나 component_mapping만 남는다. human-vs-system 경계를 보존하기 위함이며, 이 빈도에서 전용 `external selects`/`external revises`를 신설하는 것은 불필요하다고 판단했다.
- **capability_only의 cross-step host 비대칭**: occurrence_class는 functional_relation.proposition_tags에만 실릴 수 있으므로, capability로 서술된 관계가 capability_only를 기록하려면 반드시 functional_relation을 emit해야 한다. v4에서 polarity는 component_mapping에도 host를 얻었으나(§1) occurrence_class는 얻지 못했다 — 사소한 host 비대칭이며, 소수 proposition에 국한되고 방어 가능하다고 판단했다.
- **actor 없는 부정(denial)은 표현 불가**: explicit_denial은 host로 리터럴 source_term을 요구한다(component_mapping 또는 functional_relation.proposition_tags). actor·tool을 전혀 명명하지 않는 autonomy denial(예: C05-P25)은 host가 없어 explicit_denial을 실을 수 없고 스킵된다 — by-design 한계로 여기 정직하게 기록해 두며, 필요하면 T6가 quote에서 직접 회수한다.
