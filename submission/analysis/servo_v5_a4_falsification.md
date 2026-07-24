# SERVO v5 — A.4 반증 게이트 (Falsification Gate) 분석

- 상태: analysis (READ-ONLY 산출물, 2026-07-24). 이 문서는 동결된 v5 산출물과 원고를 대상으로 한 판정이며, 어떤 데이터/스키마/코드/표/원고/freeze manifest도 수정하지 않는다. 이 문서는 자기 자신만 재작성한다.
- 근거 문서: `servo_v5_charter.md` (A.1/A.4/B.4/B.5/B.7/D.2), `t11_impl_contract_v3.md` (B: 정책 6축 재도출, D: A.4 재검사), `servo_v5_policy/C0X.json` (**v3 정책 축 7개:** `control_dependence` / `selection_signal` / `selection_objective` / `generation_scope` / `candidate_selection_rule` / `design_selection_rule` / `candidate_execution_rule` + 보조 facet `formal_epistemic_utility_evidence`), `servo_v5_claims/C0X.json`, `servo_v5_alignments/C0X.json`, `tbl-servo-v5-relations.tex`, `main_post-submit.tex`(참조만).
- 대상 게이트: **Charter A.4 / D.2** — POMDP/BED 골격을 제거했을 때 **최소 두 사례의 분류·해석·핵심 결론이 실제로 바뀌어야 한다.** 판정 기준은 **"사례 해석/결론이 바뀌는가"**이지, 특정 어휘를 진술할 수 있는가가 **아니다.** 어떤 개념을 제거하면 그 개념의 부재를 진술 못 하는 것은 자명하므로(순환), PASS 근거가 될 수 없다(D.2).
- **재도출 고지(t11_impl_contract_v3 §D + design axis 2026-07-24):** 정책 레이어가 v3 6축으로 재도출됐고(G1), 이후 reviewer Item 2를 반영해 **실험-설계 선택 축 `design_selection_rule`을 추가(7축)**했다 — action a=(h,d,P,f)에서 후보 h 선택(`candidate_selection_rule`)과 실험 설계 d 선택(`design_selection_rule`)은 별개 축이며, "모든 가설을 시험했다"는 h-선택 사실을 실험-DESIGN 선택 판정으로 오독하지 않는다. 본 문서는 이전 판본의 distinction 2 결론 문장을 **수동 보존하지 않고** 새 7축 값(후보-축과 설계-축 분리)으로 with/without 붕괴표를 **처음부터 재구성**했다. 이전 판본의 판정을 옮겨 오지 않았다.

표기 규약(ASCII). 관계표 셀 — `[occ]` occurrence-established(supported/occurrence/resolved), `[occ?]` occurrence-unresolved(unresolved/occurrence/unresolved — 관계는 typed되나 cross-step 엣지가 structurally_inferred라 occurrence 미확립), `[agg]` aggregate(supported/aggregate_run), `[proc]` reported-as-procedure(supported/procedure), `[cap]` capability-only(unresolved/architecture), `[x]` contradicted, `-` 부재. 정책 축 — enum 값을 그대로 나열(다중값). 화살표 `->`.

---

## 0. 판정 요약 (먼저)

- **판정: PASS — 단, 축(axis) 수준에서만, 그리고 올바른(비순환) 테스트 위에서.** 두 반사실은 각각 독립적으로 >=2 사례의 **해석을 바꾼다** — 즉 선택된 분석 축들은 **분석적으로 유용(informative)**하다(제거 시 사례 해석이 병합됨). 그러나 이 반사실은 SERVO **자신의 축을 제거**하는 것이지 대안 이론을 제거하는 것이 아니며, 동일한 축값은 일반 최적화/워크플로/provenance 어휘로도 진술 가능하다(본문 스스로 인정, §6). 따라서 이 게이트가 보이는 것은 **축의 유용성**이지 **distinction이 POMDP/BED에 유일하게 의존한다는 것이 아니다** — 축을 일반 workflow taxonomy로 relabel해도 모든 분류가 보존된다. POMDP/BED 귀속은 **동기적 참조(motivating reference)**이지 반증 가능한 load-bearing 주장이 아니다. 영어 정박: *"The ablation shows that the selected axes are analytically informative; it does not establish that the distinctions uniquely depend on POMDP/BED."* 순환 논증("BED를 제거하면 BED 부재를 진술 못 함")과 형식 EIG 균일성(`formal_epistemic_utility_evidence`)은 **하중 증거에서 배제**하고 §7 마감 관찰로만 둔다.
- **두 반사실 각각이 독립적으로 >=2 사례의 해석을 바꾼다:**
  1. **관측 vs 평가(O_env/V 축; POMDP 유래 구조점).** `o~O_env(.|a)`와 `v=V(o)`를 하나의 "result" 노드로 합치면 (a) `C01-D06`의 `occurrence_resolution`이 `unresolved`(B.5 경계 강등)에서 `resolved`로 **되돌아가고**(전체 claim 산출물에서 유일한 `resolved->unresolved` 강등), (b) C05의 growth curves(O_env, boundary_unreported)와 confirm/refute(V) 분리가 소멸해 물리 wet-lab 사례가 순진한 "닫힌 발견 루프" 하나로 독해된다. 이 O_env/V 축은 축 수준에서 **사례 판정 자체를 뒤집는**(C01-D06) 가장 견고한 축이나, 이 역시 "일반 provenance 기록으로는 얻을 수 없다"를 넘어 POMDP 이론의 유일성을 입증하지는 않는다(§6 반론 A: 2단계 typed 분리가 필요할 뿐, 그 분리는 POMDP 어휘 없이도 표현될 수 있다).
  2. **adaptive-selection 분해(정책 축) — v3 7축(후보-축 + 설계-축 분리).** 정책 축(`control_dependence`·`selection_signal`·`selection_objective`·`candidate_selection_rule`·`design_selection_rule`·`candidate_execution_rule`)을 벗기면 여섯 사례가 하나의 "결과 조건부 적응 루프(outcome-conditioned adaptive loop)"로 병합한다. 축이 있을 때 C05는 **후보 규칙**(`candidate_selection_rule=exhaustive`/`candidate_execution_rule=all_selected` — 20개 가설 전수 후보선택·전수 실행)으로 성능-클러스터의 **랭크/역치 하선택**(`top_k_ranked`/`threshold`)과 **구별되고**(C05는 여섯 중 유일한 전수 선택), C01(`local_repair`, diversity 없음, `sequential_choice`+`until_success`)은 diversity/score 클러스터와 **구별된다.** 설계 축은 여기에 실험-설계 차원을 더한다 — C03/C05만 `coverage_or_factorial`(체계적 sweep·ablation / Latin-square)이고 나머지는 `fixed_or_standard_design`이다(margin은 C03+C05로 좁다, 정직 기록). 축을 벗기면 이 서로 다른 피드백 구조가 하나의 서술로 합쳐진다 — >=2 사례(실측상 3: C05, C01, 보강 C04)의 해석이 실제로 바뀐다. **M6 교정(C05 `selection_objective`=`not_reported`):** 이전 판본은 C05에 `hypothesis_model_discrimination`+`uncertainty_reduction`(판별/불확실성 목적)을 코딩했으나, 동결 sparkes2010 C05 출처는 측정-검정력 설계(Latin-square)와 confirm/refute 능력만 세울 뿐 **불확실성-/판별-지향 선택 목적을 보고하지 않으며, Adam은 20개 가설을 전부 시험(=실험 선택 자체가 없음)**하므로 정책 산출물은 `selection_objective=not_reported`로 재도출됐다("local source가 지지하는 만큼만" 원칙). 따라서 C05의 구별성은 이제 **discrimination 목적이 아니라 후보 규칙(전수 vs 랭크/역치 하선택)**에 걸린다 — 이 distinction은 약해지되 exhaustive-대-ranked 차이는 여전히 C05를 성능-클러스터에서 떼어내며(부수적으로 C05는 6사례 중 유일하게 `local_repair` 목적이 부재), discrimination 목적은 **재도입하지 않는다.** **reviewer Item 2:** C05의 "20개 가설 전수 시험"은 **후보(h)-선택** 사실(`candidate_selection_rule=exhaustive`/`candidate_execution_rule=all_selected`)일 뿐, 실험-DESIGN을 기대판별로 고르는지에 대한 증거가 아니다 — 설계 축은 별개로 표준/coverage이며 `discrimination_directed`가 아니다(king2004의 기대비용-최소 실험선택은 인용 배경, 동결 sparkes2010 C05 출처 밖). 이 distinction 2 판정은 §4.2/4.3의 with/without-축 반사실만으로 성립하며, §4.4(퇴역 closure 표현)는 관측된 병합이 아닌 **표현적 공백**을 지적하는 하중 없는 교정 주석이다.
- 세 번째 구별(iteration vs adaptation)은 **보강 증거로만** 인정하며, 단독으로는 결정적이지 않음을 §5.3에 정직하게 문서화한다.
- 각 반사실이 >=2 사례를 바꾸므로 A.4 기준(POMDP/BED 제거 시 >=2 사례 변화)을 **축 수준에서 두 경로 독립적으로** 충족한다. 억지 PASS는 아니나, (i) 이 PASS는 **축의 유용성**만 세울 뿐 POMDP/BED 이론에 대한 유일한 의존성(load-bearing theory)을 세우지 않고(B3 재프레이밍 — 축을 일반 optimization/provenance 어휘로 relabel해도 분류 보존), (ii) distinction 2의 margin이 넓지 않다는 점(C05+C01 집중, §6)을 함께 기록한다.

---

## 1. 방법 — 반증 프로토콜

각 구별에 대해: (a) 어떤 POMDP/BED 개념이고 어떤 스키마 필드/판정 규칙으로 구현되는지 명시하고, (b) **그 개념을 제거했을 때 v5 산출물의 사례 해석/판정이 어떻게 바뀌는지**를 반사실로 계산하며, (c) 그 변화가 실제로 어떤 `claim_id`/정책 축/사례 독법을 바꾸는지 특정한다. 그런 뒤 §6에서 **내 PASS에 적대적으로** 각 구별이 장식이라는 논증을 세우고 그 논증이 실패하는지(또는 성립하는지)를 정직하게 확인한다.

**순환 금지 원칙(D.2, 본 분석의 최상위 제약):** "개념 X를 제거하면 X의 부재를 진술 못 한다"는 형태의 논증은 어떤 개념에도 자명하게 성립하므로 근거에서 배제한다. 따라서 `formal_epistemic_utility_evidence=not_reported`(6/6)의 진술 가능성은 A.4의 하중 증거가 **아니다**(§7의 마감 관찰로만 등장). 하중은 오직 §3~§4의 **사례 해석 변화**가 진다. 이전 판본이 하중을 걸었던 `explicit_bed=0/6`·"C05가 BED-present로 오분류" 논증은 v3 스키마에서 해당 라벨(`explicit_bed`)이 폐기됐고 D.2가 금지하는 순환/compliance이므로 본 재작성에서 **사용하지 않는다.**

### 1.1 구별 -> POMDP/BED 개념 -> 스키마 구현 (v3 7축(+design axis)으로 갱신, 퇴역 라벨 제거)

| 구별 | POMDP/BED 개념 | v5 구현 (스키마/판정) |
|---|---|---|
| 1. observation vs evaluation | 관측 커널 `o~O_env(.\|a)` 대 검증기 `v=V(o)` (B.5 형식) | `functional_relation`: `environment->observation(produces)` 대 `evaluation->{observation,candidate}(evaluates)`; `boundary_status=boundary_unreported`; B.5 강등 규칙(`resolved->unresolved`) |
| 2. adaptive-selection 분해 | 실험 선택을 **불확실성 하의 선택(experiment selection under uncertainty)**으로 보는 BED 렌즈(단순반복 vs 결과조건부, 성능향상 vs 불확실성감소, 전수 vs 하선택, 오류수정 vs 가설구별, **후보 h 선택 vs 실험 설계 d 선택**, 표준/coverage 설계 vs 판별-지향 설계) | **v3 정책 분해(B.4/contract §B + design axis):** `control_dependence` / `selection_signal` / `selection_objective` / `candidate_selection_rule` / `design_selection_rule` / `candidate_execution_rule` (+ provenance-only `generation_scope`, 표 A 열 아님) |
| 3. iteration vs adaptation (보강) | 반복 재실행 대 정보상태 `I_{t+1}=U(I_t,o,v)`가 later action을 조건화 | occurrence 규율(B.3) + cross_step `functional_relation`(B.7); occurrence-established 피드백 관계의 수 |

> 퇴역 라벨 주의(v3 재도출 반영): 이전 정책 스키마의 `explicit_bed`·`uncertainty_directed`·`repair_reactive`·`outcome_conditioned`·`exploration`·`none`(control)·`expected_discrimination_selected`(execution)는 **v3 7축 산출물에 존재하지 않는다**(`servo_v5_policy/*.json` 실측). 본 문서는 이 라벨들을 판정 어휘로 사용하지 않는다. control의 `none`은 `fixed_or_predefined`/`not_reported`로 분리됐고, objective의 `exploration`은 pi-수준이면 `diversity_directed_selection`, 생성-수준이면 provenance 필드 `generation_scope`로 재배치됐으며, `performance`는 `performance_improvement`로, execution의 목적+메커니즘 혼합 라벨 `expected_discrimination_selected`는 삭제되고 C05는 objective=`not_reported`(측정-검정력 설계는 있으나 판별-/불확실성-지향 선택 목적은 미보고, M6) / candidate_selection_rule=`exhaustive` / candidate_execution_rule=`all_selected`로 축이 분리됐다. **design axis 추가(reviewer Item 2):** 실험 설계 d 선택을 코딩하는 `design_selection_rule`이 candidate_selection_rule과 별개 축으로 추가됐다 — C05는 후보 축(exhaustive/all_selected)과 무관하게 설계 축이 `fixed_or_standard_design`+`coverage_or_factorial`(discrimination_directed 아님)로 코딩되며, 퇴역 `expected_discrimination_selected`가 혼합했던 "판별 목적 + 판별 실험선택"은 이제 objective(이 출처에서는 `not_reported`)·candidate rule(전수)·design rule(표준/coverage) 세 축으로 완전히 분리된다.

---

## 2. 데이터 스냅샷 (동결 산출물 실측)

### 2.1 Typed feedback-relation 표 (`tbl-servo-v5-relations.tex`)

| Relation kind | C01 | C02 | C03 | C04 | C05 | C06 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| Evaluation -> execution (repair) | - | [agg] | - | - | - | - |
| Evaluation -> artifact (revision) | [occ] | - | - | - | - | - |
| Evaluation/observation -> inquiry_state (update) | [proc] | - | - | - | [occ?] | - |
| Memory -> candidate/policy (conditioning) | [cap] | - | - | [proc] | - | - |
| Generation produces candidate | [occ] | [occ] | [proc] | [agg] | [occ] | [occ] |

**핵심 실측:** forward 생성("Generation produces candidate")을 제외하면 occurrence-established(`[occ]`) **피드백** 관계는 전 사례 통틀어 **정확히 하나**다 — `C01`의 evaluation **revises** artifact(`C01-D01`, single_event, supported/occurrence/resolved). `C05`의 evaluation **updates** inquiry_state는 더 이상 occurrence-established가 아니다: cross_step 엣지 `C05-A64`가 `structurally_inferred=true`(출처가 12/20 확정이 *later* inquiry step을 조건화한다고 진술하지 않음)라 occurrence를 witness하지 못하고, 그 파생 claim `C05-D24`가 `unresolved`/`unresolved`(`[occ?]`)로 강등됐다(B1). 20개 중 12개 확정이라는 per-step 평가(`C05-D23`) 자체는 여전히 supported이나, 그것을 cross-step 피드백으로 올리는 엣지는 미확립이다. occurrence-established "evaluation->execution(experimental adaptation)"는 **어떤 사례에도 없다**(C02는 aggregate `[agg]`에 그침).

### 2.2 정책 7축 분해 표 (`servo_v5_policy/C0X.json`, v3 스키마 + design axis)

값 = v3 enum 그대로. `generation_scope`는 provenance 전용(표 A 열 아님)이나 붕괴 검증을 위해 함께 싣는다. `obs_result`=`observation_result`, `perf_impr`=`performance_improvement`, `div_dir`=`diversity_directed_selection`, `not_rep`=`not_reported`, `fixed_pre`=`fixed_or_predefined`, `fixed_std`=`fixed_or_standard_design`, `cov_fac`=`coverage_or_factorial`. (판별/불확실성 objective `hypothesis_model_discrimination`/`uncertainty_reduction`은 6사례 어디에도 코딩되지 않는다 — C05 `selection_objective`도 `not_reported`, M6.) **`design_selection_rule`(reviewer Item 2)는 candidate_selection_rule과 별개 표 A 열이다** — 후보 h 선택과 실험 설계 d 선택을 분리한다.

| ID | control_dependence | selection_objective | generation_scope | candidate_selection_rule | design_selection_rule | candidate_execution_rule |
|---|---|---|---|---|---|---|
| C01 | failure, obs_result | local_repair, perf_impr | fixed_space | sequential_choice | fixed_std | one_at_a_time, until_success |
| C02 | failure, score, obs_result | local_repair, perf_impr, div_dir | fixed_space | threshold | fixed_std | one_at_a_time, until_budget |
| C03 | failure, score, obs_result | local_repair, perf_impr | search_space_expansion, candidate_diversification | top_k_ranked, sampled_subset | **cov_fac** | batch, until_budget |
| C04 | fixed_pre, failure, score, obs_result | local_repair, perf_impr | candidate_diversification | top_k_ranked, sampled_subset | fixed_std | batch, until_success, until_budget |
| C05 | fixed_pre, score, obs_result | **not_rep** | fixed_space | **exhaustive** | **fixed_std, cov_fac** | **all_selected** |
| C06 | failure, score, obs_result | local_repair, perf_impr | candidate_diversification | top_k_ranked | fixed_std | until_success, until_budget |

- **Selection signal**(자유 텍스트 축, 사례별): C01 = 소프트웨어/실행 오류; 반응 수율; 직전 라운드 관측; normalized advantage. C02 = 컴파일/실행 오류; 자가평가 아이디어 점수(흥미도/신규성/실현성); 자동 리뷰 점수; 실험 결과; 문헌 유사도. C03 = 실행 오류/버그 노드; VLM 지적 플롯 문제; LLM-평가자 성능지표(학습동역학/플롯); 최고 체크포인트 점수; 학습곡선 수렴. C04 = 서브태스크 완료(무조건 자율진행); 컴파일/실행 오류; mle-solver 정렬 점수; professor-agent 보상모델 점수(0-1); 실험 결과. C05 = 고정 4단계 orphan-enzyme 방법; 서열 유사도(PSI-BLAST/FASTA); confirm/refute 통계 결과; 갱신 대상 모델 충돌. C06 = 런타임 예외; 태스크 복잡도(코더 라우팅); 평가 에이전트 점수(0-10, 5차원 가중합); 구조화 비평; 실증 성능 결과.
- **`formal_epistemic_utility_evidence` = `not_reported` (6/6).** 어떤 bounded source도 prior/posterior/likelihood/EIG/VOI/epistemic-utility 항을 **선택 규칙에 직접** 쓴다고 진술하지 않는다. 이는 **보조 facet이자 corpus-level 관찰 한 줄**이며, A.4의 하중 증거가 아니다(§7).

**중심 결과의 형태(B.4):** 표의 핵심은 `formal_epistemic_utility_evidence`의 유무가 **아니라** 분해(decomposition)다. 7축을 적용하자 모두 "iterative/closed-loop"로 뭉뚱그려지던 시스템들이 서로 다른 피드백 구조로 분해된다 — C01은 실패복구+수율 착취(diversity 없음, 순차 선택), 성능-클러스터(C02/C03/C04/C06)는 성능 향상+생성측 다양화로 점수 랭킹, C05는 **선택 목적 미보고(`selection_objective=not_reported`, M6; 6사례 중 유일하게 `local_repair` 목적 부재)에 전수 후보 선택(`exhaustive`)+전수 실행(`all_selected`)**로 성능-클러스터의 랭크/역치 하선택(`top_k_ranked`/`threshold`)과 갈리고, C04는 추가로 상위 `control_dependence=fixed_or_predefined`(자율모드 무조건 진행). **설계 축(reviewer Item 2)이 더하는 차원:** 실험 설계 d 선택에서 C03·C05만 `coverage_or_factorial`(C03 체계적 하이퍼파라미터 sweep + ablation; C05 Latin-square noise-control)이고 나머지 넷은 `fixed_or_standard_design`이다. 어느 사례도 `discrimination_directed`/`information_directed`/`cost_directed` 설계를 보고하지 않으며, C05는 판별-지향 *목적*조차 보고하지 않는다(`selection_objective=not_reported`) — 따라서 C05의 구별성은 판별 목적이 아니라 **후보 규칙(전수 vs 랭크 하선택)**에 걸린다. "20개 가설 전수 시험"은 후보-축 사실이지 설계-축 증거가 아니다(king2004 기대판별 실험선택은 인용 배경).

---

## 3. 반사실 1 — observation vs evaluation (O_env vs V)

### 3.1 이 구별이 하는 일
B.5 형식은 `o_{t+1}~O_env(.|a_t)`(관측 생성)과 `v_{t+1}=V(o_{t+1})`(평가)을 물리적으로 다른 typed relation으로 강제한다. 조합형 스키마(B.7)에서 이는 `environment->observation(produces)` 대 `evaluation->{observation,candidate}(evaluates)`로 나타나고, 출처가 executor-environment 경계를 제공하지 않으면 `boundary_status=boundary_unreported`가 붙는다. B.5 강등 규칙: 어떤 관계가 미보고 E<->O_env 경계를 건너면 관측 occurrence를 확인할 수 없으므로 `occurrence_resolution`을 강등한다.

### 3.2 반사실 — 두 노드를 하나의 "result"로 합치면 (v4.1 이전 회귀)
observation과 evaluation을 하나의 "result->update" 노드로 합치면 "환경/측정이 관측을 생성했다"는 단계가 "평가"와 분리되어 존재하지 않는다. 따라서 `boundary_unreported`가 부착될 **대상 노드 자체가 소멸**하고 B.5 강등 규칙은 발화할 수 없다.

### 3.3 실제로 바뀌는 것 (a) — C01-D06 판정 뒤집힘
`C01-D06`(prop `C01-P04` "GC-MS analysis ... revealed the formation of the target products", alignment `C01-A15` = environment->observation, `boundary_status=boundary_unreported`):
- **현재 v5 판정:** `support_status=supported`, `claim_scope=occurrence`, **`occurrence_resolution=unresolved`**. rationale 원문: *"single_event ... is a real occurrence witness -> resolved. charter B.5: this relation crosses an unreported E<->O_env boundary ... occurrence_resolution lowered resolved->unresolved ... (occurrence undetermined)."*
- **O_env/V 제거 시:** 별도 관측-생성 노드가 없어 강등이 발화하지 않음 -> `occurrence_resolution`이 **`resolved`로 복원.** "피드백 관계는 보이나 측정 경계가 미보고라 관측 occurrence를 확정할 수 없다"는 보수적(정직한) 판정이 사라지고, 확정 occurrence로 (거짓) 상향된다.
- **검증:** `resolved->unresolved` 강등("lowered")은 v5 claim 산출물 전체에서 `C01-D06` **단 하나**다(전체 claim 파일 grep: C01 1건, 나머지 0건). 정확히 과제가 지목한 사례.

### 3.4 실제로 바뀌는 것 (b) — C05 관측/평가 분리 소멸
C05-P12 한 문장에서 "growth curves" = O_env(`C05-A33` component; `C05-A36` environment->observation, boundary_unreported)와 "confirmed or refuted" = V(`C05-A34` component; `C05-A37` evaluation->observation, reported)는 **분리된 두 관계**다. `C05-A37` note는 "'used to update the model'은 reported_as_procedure로 occurrence 진술이 없어 cross-step model-update 관계를 부여하지 않음"이라 명시한다. 두 노드를 합치면:
- growth curves(원측정)와 confirm/refute(평가)가 하나가 되어 물리 wet-lab 사례가 "실험이 결과를 냈고 모델을 갱신했다"는 순진한 **닫힌 발견 루프** 하나로 읽힌다.
- `boundary_unreported`(A36)로 표시된 "측정 과정 미보고" 진단이 사라진다. (원고 Limitations `main_post-submit.tex:359`도 O_env 미인스턴스화 때문에 "execution failure와 environment/measurement failure를 구분할 수 없다"고 이 구분의 부재를 한계로 명시 — 구분이 분석적 일을 하고 있다는 방증.)

**반사실 1 판정: load-bearing.** C01-D06에서 판정을 실제로 뒤집고(>=1 사례), C05의 관측/평가 분리·measurement-boundary 진단을 형성한다(>=2 사례). 순전히 POMDP 관측 커널 개념(O_env)에 의존한다.

---

## 4. 반사실 2 — adaptive-selection 분해 (BED 유도 v3 6축; 후보-축 + 설계-축 분리)

> **이 절은 v3 7축 재도출(design axis 포함) 위에서 처음부터 다시 계산한 붕괴 테스트다.** 순환·compliance 논증(이전 판본의 `explicit_bed` 계열)은 §1의 순환 금지 원칙으로 배제된다. 올바른 테스트(D.2(b))는 **BED 유도 축을 벗겼을 때 여섯 사례의 해석이 하나로 합쳐지는가**이며, 기준은 사례 해석 변화이지 어휘 존재가 아니다.

### 4.1 이 구별이 하는 일
BED 렌즈는 실험 선택을 **불확실성 하의 선택(experiment selection under uncertainty)**으로 본다(B.4). 이 렌즈가 강제하는 질문 — "선택을 무엇이 구동하는가(`control_dependence`: 결과조건부 vs `fixed_or_predefined`), 어떤 신호로(`selection_signal`), 어떤 목적으로(`selection_objective`: 성능향상 vs 불확실성감소 vs 가설구별 vs 다양성-지향), 어떤 후보 h를 고르는가(`candidate_selection_rule`: 전수(`exhaustive`) vs 랭크 하선택(`top_k_ranked`)/역치(`threshold`)/순차(`sequential_choice`)), **어떤 실험 설계 d로 검정하는가(`design_selection_rule`: 표준/고정 `fixed_or_standard_design` vs coverage/factorial `coverage_or_factorial` vs 판별-지향 `discrimination_directed`)**, 선택된 후보를 어떻게 실행하는가(`candidate_execution_rule`: `all_selected` vs `one_at_a_time`/`batch`/`until_success`/`until_budget`)" — 이 §2.2의 분해를 낳는다. **후보 h 선택과 실험 설계 d 선택은 별개 질문이다(a=(h,d,P,f), reviewer Item 2)**: "모든 후보를 시험했다"는 전자의 답일 뿐 후자에 대해 침묵한다. (`generation_scope`는 표 A 열이 아닌 provenance 필드로, 붕괴표에서는 참고로만 취급한다 — §6 참조.)

### 4.2 반사실 — BED 유도 6축을 제거하면 (구체적 붕괴)
`control_dependence`·`selection_signal`·`selection_objective`·`candidate_selection_rule`·`design_selection_rule`·`candidate_execution_rule`를 벗기면, 각 사례의 정책을 서술할 분석 어휘로 남는 것은 오직 "시스템이 관찰된 결과에 따라 후보를 재실행하는 루프를 돈다"뿐이다. 여섯 사례 모두 control에 `observation_result`를 공유하므로, 축 어휘가 사라진 자리에 평문으로 남는 유일한 공통 서술이 바로 이 **"결과 조건부 적응 루프(outcome-conditioned adaptive loop)"**다 — 여섯 사례가 동일하게 이 하나로 읽힌다.

축이 **있을 때**의 독립적 독법 대 **없을 때**의 병합(v3 실측값 기준; `cand_sel`=후보 h 선택, `design`=실험 설계 d 선택 — 별개 축):

| 사례 | selection_objective | cand_sel_rule | design_rule | execution_rule | control 특이값 | 축 있을 때 독법 | 축 없을 때 |
|---|---|---|---|---|---|---|---|
| C01 | local_repair, perf_impr | sequential_choice | fixed_std | one_at_a_time, until_success | (failure, obs_result만) | 실패복구 + 수율 착취, **diversity 없음**, 순차 후보선택·1건씩 성공까지, 표준 OT-2 assay | 결과 조건부 적응 루프 |
| C02 | local_repair, perf_impr, **div_dir** | threshold | fixed_std | one_at_a_time, until_budget | - | 성능 + **pi-수준 신규성 필터**(문헌유사도 역치 폐기), 고정 template 설계, 예산까지 | 결과 조건부 적응 루프 |
| C03 | local_repair, perf_impr | top_k_ranked, sampled_subset | **cov_fac** | batch, until_budget | - | best-first 랭크 하선택 + 확률적 노드 표집, **체계적 hyperparameter sweep + ablation coverage 설계**, 병렬 배치 | 결과 조건부 적응 루프 |
| C04 | local_repair, perf_impr | top_k_ranked, sampled_subset | fixed_std | batch, until_success, until_budget | **fixed_or_predefined** | 성능-클러스터 + 상위 자율모드 **무조건 진행**(fixed_or_predefined), 고정 파이프라인 표준설계 | 결과 조건부 적응 루프 |
| C05 | **not_reported** | **exhaustive** | **fixed_std, cov_fac** | **all_selected** | fixed_or_predefined | 선택 목적 미보고(판별/불확실성 목적 없음, M6), **20개 가설 전수 후보선택·전수 실행**(후보 하선택 없음), **설계는 표준 assay + Latin-square coverage(판별-지향 아님)**, repair·`local_repair` 목적 부재 | 결과 조건부 적응 루프 |
| C06 | local_repair, perf_impr | top_k_ranked | fixed_std | until_success, until_budget | - | 예외유도 디버깅 + 가중합 점수 랭킹, baseline-유래 표준설계 | 결과 조건부 적응 루프 |

### 4.3 병합되는 해석 (>=2 사례) — 하중 증거
- **C05 (여전히 가장 날카롭되, 하중은 후보 규칙이 진다).** 축이 있으면 C05는 유일하게 `candidate_selection_rule = exhaustive`, `candidate_execution_rule = all_selected`(20개 가설 전수), `selection_objective = not_reported`(6사례 중 유일하게 `local_repair` 목적 부재; M6)인 **구별되는 피드백 구조**다(C05-P22: Adam이 20개 가설을 *전부* 시험, 12개 확정). 후보 축(exhaustive/all_selected)을 벗기면 이 구조가 사라지고 C05는 나머지와 같은 "적응 루프"가 되어 **성능-클러스터로 흡수**된다. 즉 "이 사례는 성능-랭크 하선택 루프가 아니라 후보를 하선택 없이 전수 선택·전수 실행한다"는 해석이 소멸한다. **M6 교정(하중 이동):** 이전 판본은 이 병합 하중을 C05의 `uncertainty_reduction`+`hypothesis_model_discrimination` 판별 목적에 걸었으나, 동결 sparkes2010 C05 출처는 판별-/불확실성-지향 선택 목적을 보고하지 않고 Adam은 실험 선택 없이 전부 시험하므로 `selection_objective=not_reported`로 재도출됐다. 따라서 이 하중은 이제 **discrimination 목적이 아니라 전수-대-랭크 후보 규칙 차이**가 진다 — distinction은 약해지되(목적 축이 아니라 후보 축 하나로 지탱) 여전히 C05를 성능-클러스터에서 실제로 떼어낸다; 본 재작성은 판별 목적을 **재도입하지 않는다.** **reviewer Item 2 교정(후보-축과 설계-축의 분리):** 이전 판본은 C05의 "20개 가설 전수 시험"을 곧 "판별 하선택 없음"으로 읽어 **후보(h) 선택과 실험(design d) 선택을 혼동**할 여지가 있었다. v3+design에서 이 둘은 별개 축이다 — (i) 후보 축: `candidate_selection_rule=exhaustive`/`candidate_execution_rule=all_selected`(모든 *가설*을 시험, C05-P22)는 **후보 선택** 사실일 뿐 실험-설계 선택에 대해 침묵한다; (ii) 설계 축: `design_selection_rule=fixed_or_standard_design`+`coverage_or_factorial`(C05-P08/P17: 모델-규정 assay + Latin-square noise-control layout)로, **`discrimination_directed`가 아니다.** 동결 sparkes2010 C05 출처는 기대판별·기대정보 기반 *실험* 선택을 보고하지 않으며(Latin-square는 측정 검정력용, confirm/refute는 결과이지 설계-선택 기준이 아님), king et al. 2004/2009의 "기대비용 최소 실험선택" active-learning은 **인용 배경**(C05 coverage_note)이지 동결 출처가 아니다. 따라서 C05는 판별 *목적* 자체가 `not_reported`이고, (a) 전수 후보 실행(형식 BED의 기대판별 하선택 아님)·(b) 표준/coverage 설계(discrimination_directed 아님)로 각 축이 **독립 진술**된다 — 이전 판본의 목적+메커니즘 혼합 라벨 `expected_discrimination_selected`는 이 진술을 불가능하게 만들었다.
- **C01.** 축이 있으면 C01은 diversity/score 클러스터와 달리 `selection_objective`에 `diversity_directed_selection`이 없고, `candidate_selection_rule=sequential_choice`(랭크 하선택도 역치도 아님), `candidate_execution_rule=one_at_a_time+until_success`다. 즉 "다양화 없는 순수 수율 착취(exploitation-only), 순차 게임식 선택"이다. 6축을 벗기면 이 구별이 사라져 신규성/다양성 선택을 지닌 C02(threshold+div_dir), 랭크 하선택을 지닌 C03/C04/C06(top_k_ranked)과 **구분 불가능**해진다.
- **(보강) C04.** `control_dependence=fixed_or_predefined`(자율모드 무조건 서브태스크 진행)라는 "상위 고정 파이프라인" 독법이 사라지고 나머지 성능-클러스터와 합쳐진다.
- **(보강) 설계 축의 차별.** 실험 설계 축은 C03·C05만 `coverage_or_factorial`(C03 체계적 sweep+ablation coverage; C05 Latin-square)이고 나머지는 `fixed_or_standard_design`이다 — 이 축을 벗기면 C03의 "체계적 요인 coverage 설계"와 C05의 "표준+coverage 설계"가 나머지와 병합된다. 다만 설계 축의 차별력은 C03+C05에 집중되고 4/6이 동일값(`fixed_std`)이라 **주로 distinction 2를 보강**하며 단독 하중은 좁다(정직 기록, §6).

축을 벗기면 >=2 사례(C05, C01; C04·설계축 보강)의 해석이 실제로 합쳐진다. **반사실 2 판정: 선택된 축은 분석적으로 유용(informative)하다 — 그러나 이것이 POMDP/BED 이론에 대한 load-bearing 주장을 세우지는 않는다(B3).** 판별 기준은 **어휘 존재가 아니라 사례 INTERPRETATION의 변화**이며, 위 사례들 모두 축 유무에 따라 독법이 실제로 바뀐다. 다만 이 반사실은 SERVO **자신의 축**을 제거하는 것이지 대안 이론을 제거하는 것이 아니고, 동일한 후보/설계/목적 축값은 일반 최적화·워크플로·provenance 어휘로도 진술 가능하므로 축을 그런 generic taxonomy로 relabel해도 모든 분류가 보존된다 — 따라서 이 판정이 세우는 것은 **축의 유용성**이지 distinction이 POMDP/BED에 유일하게 의존한다는 것이 아니다. 영어 정박: *"The ablation shows that the selected axes are analytically informative; it does not establish that the distinctions uniquely depend on POMDP/BED."*

### 4.4 퇴역 closure 표현의 표현적 공백 (교정 주석 — 관측된 병합 아님, 하중 아님)
퇴역한 4-predicate closure matrix(`execution_repair`, `experimental_adaptation`, `artifact_revision`, `discovery_cycle_feedback`; charter §0/C.1)에는 선택 목적(`selection_objective`)이나 후보 선택/실행 규칙(`candidate_selection_rule`/`candidate_execution_rule`)을 담을 **축이 없었다.** 중요한 정정: 이 표현은 C05를 성능-클러스터와 **같은 계열로 병합하지 않았다.** `servo2_closure_statuses.csv` 실측상 C05의 네 predicate는 모두 판단 유보 또는 범위 밖이다 — `execution_repair=unknown`(insufficient_reporting), `experimental_adaptation=unknown`(insufficient_reporting), `artifact_revision=not_applicable`(out_of_scope), `discovery_cycle_feedback=unknown`(insufficient_reporting). 즉 퇴역 표는 C05를 성능-클러스터로 뭉뚱그린 것이 아니라 **미해결(all-unknown/na)로 남겨두었다.** 이 all-unknown 패턴은 오히려 established 술어를 일부 지닌 성능-클러스터 사례들(C02·C03의 `experimental_adaptation=established`, C04의 두 개, C06의 세 개)과 **구별되는** 패턴이다. 따라서 여기서 지적할 것은 관측된 병합이 아니라 **표현적 공백(expressive gap)**이다: 퇴역 축에는 선택 목적·후보 선택/실행 규칙을 담을 자리가 없어, C05의 exhaustive-selection + all-selected-execution 후보 구조(및 `selection_objective=not_reported`)를 **표현할 수도 구별할 수도 없었고** 단지 C05를 미해결로 남겼다. 이 표현적 공백은 §4.2/4.3의 with/without-축 반사실과 달리 A.4의 >=2-사례 테스트에 **하중을 걸지 않으며**(교정 주석), v3 정책 분해가 비로소 이 구조에 표현 축을 부여한다는 점만을 보인다.

---

## 5. 반사실 3 — iteration vs adaptation (정직한 약점 포함)

### 5.1 이 구별이 하는 일
occurrence 규율(B.3) + cross_step `functional_relation`(B.7)로 "그냥 루프가 돈다"는 bare reading을 분해한다: "반복 재실행"과 "증거가 정보상태를 갱신해 later action을 조건화"를 나눈다.

### 5.2 실제 효과
- bare "it loops" 독법은 여섯 사례 모두에 무차별적 "발견 루프 닫힘"을 부여한다. v5는 이를 분해해 **occurrence-established 피드백 관계가 전 사례 통틀어 정확히 하나**(C01 revision `[occ]`)뿐임을 드러낸다 — C05의 evaluation->inquiry_state update는 cross_step 엣지(`C05-A64`)가 `structurally_inferred`라 occurrence 미확립으로 `[occ?]`(C05-D24, unresolved)로 강등됐다(B1). occurrence-level "experimental adaptation"(evidence->changed action->later execution)은 **어떤 사례에도 없음**(C02는 aggregate `[agg]`)이다(§2.1).
- C02(AI Scientist)는 Aider 오류 수정 루프가 핵심인데 표에서 "Evaluation->execution(repair) = `[agg]`"에 그친다. bare 독법의 "실험 피드백 루프를 닫는다"가 "aggregate repair + generation"으로 강등된다.

### 5.3 정직한 약점 (내 PASS를 이 구별에 걸지 않는 이유)
- mechanism 층에서 결과-조건부 루프(`control_dependence`에 `observation_result` 포함)는 **6/6**(차별력 0)이고, `local_repair` objective는 5/6(C05만 예외)이라 이 층만으로는 사례를 거의 못 가른다.
- 실제 차별력의 대부분은 occurrence 규율(B.3)과 반사실 1(observation/evaluation 분리)에서 **차용**된다 — 이 구별은 상당 부분 distinction 1/B.3와 겹친다.

**반사실 3 판정: 보강 증거로만 인정.** 단독으로는 게이트를 통과시키지 못하며, 이를 감추지 않고 문서화한다(D.2의 "무언 후퇴 금지" 준수).

---

## 6. 적대 검증 — "골격은 장식이다" 논증과 그 성패

D.2에 따라 내 PASS를 무너뜨리려 시도한다. 각 구별에 대해 "이 골격은 decorative(장식)"라는 최강 논증을 세우고 그것이 실패하는지 성립하는지 정직하게 판정한다.

**반론 A (distinction 1 = 장식):** "`boundary_unreported`와 O_env/V 분리는 POMDP가 아니라 평범한 provenance 기록이다. '측정 과정 미상'이라고만 적어도 C01-D06 강등을 얻는다."
- *실패.* 강등은 "환경/측정이 관측을 생성"하는 노드가 "평가"와 **타입으로 분리**되어 있어야 부착 지점이 생긴다. "result"로 뭉치는 평범한 기록은 강등할 줄 모르고 "결과가 나와 사용됨"으로 확정한다. 분석이 occurrence를 *유보*할 줄 아는 이유는 `o~O_env(.|a)` 다음에야 `v=V(o)`가 온다는 2단계 커밋(=POMDP 관측 커널 개념) 때문이다. 강등은 관측 커널 개념에 진짜로 의존한다. 장식 아님.

**반론 B (distinction 2 = 장식):** "7축은 평범한 최적화 어휘(performance/repair/top_k/threshold/diversity/standard-design)의 재명명일 뿐이고, 형식 BED(EIG/posterior)는 6/6 부재이며 판별-지향 설계도 6/6 부재다. C05가 전수 시험이고 C01이 수율 최적화라는 건 논문을 읽으면 나오는 관찰이지 결정이론이 필요 없다. 그러니 '7축=BED 유도'는 장식이다."
- *축 수준에서는 실패하나 이론-귀속 수준에서는 상당 부분 성립 — 그래서 판정을 재프레이밍한다(B3).* **양보(이론-귀속):** 실제로 채워진 셀 값들(`performance_improvement`/`local_repair`/`top_k_ranked`/`threshold`/`sequential_choice`/`exhaustive`)은 **모두 일반 최적화·워크플로 어휘로 진술 가능**하고, 형식 BED(EIG/posterior)는 6/6 부재, 판별-지향 설계도 6/6 부재이며, C05의 판별 목적조차 `not_reported`다(M6 — 정보-지향 값은 어느 셀에서도 발화하지 않는다). 따라서 "이 축들이 POMDP/BED에 **유일하게** 의존한다"는 주장은 **반증 가능한 형태로 성립하지 않는다** — 축을 generic workflow/provenance taxonomy로 relabel해도 모든 분류가 보존되므로, POMDP/BED 귀속은 **동기적 참조(motivating reference)**이지 load-bearing 이론 주장이 아니다. 이 점에서 반론 B는 **옳다.** **그러나 축 수준에서는 실패하는 이유:** relabel이 보존하는 것은 **축의 존재**이지 축의 무해함이 아니다. 하중은 이름표가 아니라 **여섯 사례를 서로 다르게 읽게 만드는 판별 행위**에 있고, "결과조건부인가 `fixed_or_predefined`인가? 후보를 `exhaustive`로 고르는가 랭크 하선택인가? 실험 설계 d를 표준/coverage로 고르는가?"를 모든 사례에 던지는 이 축들을 **제거하면**(§4.2/4.3 반사실) 여섯 사례가 하나의 결과-조건부 루프로 합쳐져 C05(전수·표준coverage설계)와 C01(다양화-없음·순차)의 독법이 소멸한다 — 축은 분석적 일을 한다(**축으로서** 장식 아님). 요컨대 반론 B는 **이론 유일성 주장을 무너뜨리는 데 성공**하나 **축이 informative하다는 사실은 무너뜨리지 못한다** — 그래서 최종 판정은 "이론 load-bearing"이 아니라 "축 informative(motivating reference)"로 둔다. (퇴역 4-predicate matrix는 이 질문을 담을 축이 아예 없어 C05 구조를 표현조차 못 했으나, 이는 관측된 병합이 아니라 표현적 공백일 뿐이고 §4.4대로 하중 증거가 아니다.)
- *정직한 단서 1 (margin):* distinction 2의 하중은 **C05(구별/전수 outlier) + C01(다양화-없음/순차 outlier)**에 집중되며 폭넓은 다-사례 효과가 아니다. 성능-클러스터 네 사례(C02/C03/C04/C06)는 서로 더 닮았고 그 상호 분리는 더 미세한 축값(threshold vs top_k_ranked vs sampled_subset; pi-수준 `diversity_directed_selection`(C02) vs 생성측 diversification)에 걸린다. **설계 축(`design_selection_rule`)도 margin이 좁다** — C03·C05만 `coverage_or_factorial`, 나머지 4는 `fixed_or_standard_design`으로 동일값이라 설계 축의 독립 차별력은 C03+C05에 국한되고 주로 distinction 2를 보강한다(단독 하중 아님). >=2 기준은 넘지만 margin은 넓지 않다. 감추지 않는다.
- *정직한 단서 2 (generation_scope):* 엄밀히는, 벗겨내는 6축 밖의 provenance 필드 `generation_scope`가 붕괴 후에도 잔존하며 약한 생성측 구분(fixed_space vs search_space_expansion vs candidate_diversification)을 남긴다. 그러나 (i) 이는 표 A 정책 열이 아닌 provenance 전용이라 원고-대면 정책 서술을 이루지 않고, (ii) 여섯 사례의 서로 다른 *정책* 해석을 홀로 지지하지 못한다(예: C05 fixed_space = C01/C02 fixed_space로 동일값, 오히려 C05를 C01/C02와 묶는다). 따라서 원고-대면 정책 분해(표 A)는 붕괴하며, `generation_scope` 잔존은 PASS를 약화하지도 대체 근거가 되지도 않는다.

**반론 C (distinction 3 = 장식):** §5.3에서 스스로 인정. 이 반론은 **상당 부분 성립**한다 — 결과-조건부 루프 6/6, 차별력은 대체로 차용. 따라서 distinction 3은 PASS 근거로 세지 않는다.

**결과:** 두 구별(1/2)은 **축으로서 장식이 아니다** — 각각 >=2 사례를 실제로 바꾼다(게이트 충족). 그러나 반론 B가 보였듯 이 축들이 POMDP/BED에 유일하게 의존함은 성립하지 않으므로, 이 **PASS는 "축이 informative"라는 축 수준 결론이지 "이론이 load-bearing"이라는 결론이 아니다(B3).** 3을 장식이라 부르는 논증은 대체로 성공하여 distinction 3은 근거로 세지 않는다. 게이트는 >=2를 요구하고 두 구별(1/2)이 각각 >=2 사례를 바꾸므로 **축 수준 PASS**.

---

## 7. 마감 관찰 — corpus-level limitation (하중 아님, 명시)

`formal_epistemic_utility_evidence = not_reported` (6/6): 어떤 bounded source도 prior/posterior/likelihood/EIG/VOI/epistemic-utility 항을 **선택 규칙에 직접** 쓴다고 진술하지 않는다. C05조차 abductive framing(C05-P04)을 가지나 **선택 목적은 미보고(`selection_objective=not_reported`, M6)**이고 형식 BED 선택규칙도 없으며 20개 가설을 전수 선택·전수 실행한다(`exhaustive`/`all_selected`). 즉 판별-지향 목적 자체가 동결 sparkes2010 출처에 미보고이며, abductive 서술과 형식 BED 선택규칙 사이에는 간극이 있다.

**design_selection_rule 균일성(reviewer Item 2, 하중 아님):** 어떤 bounded source도 `discrimination_directed`/`information_directed`/`cost_directed` 실험 설계를 보고하지 않는다 — 실제 코딩은 `fixed_or_standard_design`(C01/C02/C04/C06) 또는 `coverage_or_factorial`(C03 sweep+ablation, C05 Latin-square)뿐이다. 이는 "설계를 기대판별/기대정보 하에 고른다"는 BED-central 메커니즘이 6사례에서 **관찰되지 않았다**는 corpus-level 관찰이다. 특히 C05는 판별-지향 설계-목적조차 보고하지 않으며(`selection_objective=not_reported`, M6) 설계-선택 메커니즘도 표준/coverage에 그치고, 기대비용-최소 실험선택(king 2004/2009)은 동결 sparkes2010 출처 밖의 **인용 배경**이다. `formal_epistemic_utility_evidence`와 마찬가지로 이 부재의 진술 가능성은 A.4의 하중이 아니다(§1 순환 금지) — 하중은 §4의 분해가 진다. field-wide 부재를 주장하지 않는 신중한 관찰로만 둔다.

- 위 두 균일성은 **A.4의 하중 증거가 아니다.** A.4는 §3~§4의 **사례 해석 변화**(반사실 1·2)가 진다.
- 이 균일성은 **corpus-level limitation 한 줄**로만 기술한다. "BED 개념이 없으면 이 부재를 진술 못 하므로 BED가 load-bearing"이라는 논증은 **순환(D.2 금지)이며 여기서 사용하지 않는다.** BED 렌즈의 하중은 부재를 명명하는 데 있지 않고, 여섯 사례를 서로 다른 피드백 구조로 **분해**하는 데 있다(§4).
- 원고의 대응 표현(`main_post-submit.tex`: "the bounded LLM-case sources used here do not state an EIG objective", "not an asserted field-wide absence")은 이 균일성을 **신중한 한계**로 두며 field-wide 부재를 주장하지 않는다. 본 분석은 그 신중함과 일치한다.

---

## 8. 최종 판정 (Verdict)

**PASS — 단, 축(axis) 수준에서만: 선택된 분석 축들은 informative하나(제거 시 사례 해석이 병합됨), 이것이 POMDP/BED 이론에 대한 유일한 의존성(load-bearing theory)을 입증하지는 않는다.** 영어 정박: *"The ablation shows that the selected axes are analytically informative; it does not establish that the distinctions uniquely depend on POMDP/BED."* POMDP/BED 귀속은 **동기적 참조(motivating reference)**이며(축을 generic optimization/workflow/provenance taxonomy로 relabel해도 모든 분류가 보존됨), 판정은 올바른(비순환) 테스트 위에서만 이뤄진다.

- **distinction 1 (observation vs evaluation): 축 수준 load-bearing, >=2 사례.** 제거 시 `C01-D06`의 `occurrence_resolution`이 `unresolved`->`resolved`로 뒤집히고(데이터셋 유일 경계 강등), C05의 growth curves(O_env)/confirm-refute(V) 분리와 measurement-boundary 진단이 소멸한다. 이 O_env/V 축은 사례 판정을 실제로 뒤집는 가장 견고한 축이나, 그 2단계 typed 분리는 POMDP 어휘 없이도 표현 가능하므로 이론 유일성을 입증하지는 않는다(§6 반론 A).
- **distinction 2 (adaptive-selection 분해): 축 informative, >=2 사례 — 그러나 이론 load-bearing 아님(B3).** 정책 축(`control_dependence`/`selection_signal`/`selection_objective`/`candidate_selection_rule`/`design_selection_rule`/`candidate_execution_rule`)을 벗기면 여섯 사례가 하나의 "결과 조건부 적응 루프"로 병합되며, C05의 **전수 후보 구조(`exhaustive`/`all_selected`)**가 성능-클러스터의 랭크/역치 하선택으로, C01의 다양화-없는 순차 착취 독법이 다양성/랭크 클러스터로 흡수된다. **M6:** C05 `selection_objective`는 `not_reported`로 재도출됐다(동결 sparkes2010은 판별-/불확실성-지향 선택 목적을 보고하지 않고 Adam은 전수 시험 = 실험 선택 없음) — 따라서 C05의 구별성은 이제 **discrimination 목적이 아니라 전수-대-랭크 후보 규칙**이 지며(distinction은 약해지되 성립), 판별 목적은 재도입하지 않는다. **reviewer Item 2:** 실험-설계 축(`design_selection_rule`)이 후보-축과 분리되어, C05의 "20개 가설 전수 시험"이 곧 "실험 판별 없음"이라는 혼동을 제거한다 — C05의 설계는 별개로 표준+coverage(`fixed_or_standard_design`/`coverage_or_factorial`, discrimination_directed 아님; king2004는 인용 배경)이며, 설계 축은 C03·C05만 coverage로 갈려 distinction 2를 보강한다(단독 margin은 C03+C05로 좁음, 정직 기록). margin은 C05+C01에 집중(정직 기록). **이 축 informativeness는 동일 축을 generic taxonomy로 relabel해도 보존되므로 POMDP/BED 이론 귀속을 입증하지 않는다(§6 반론 B).** 이 하중은 §4.2/4.3 반사실만으로 성립하고, §4.4(퇴역 closure 표현)는 관측된 병합이 아닌 표현적 공백을 지적하는 교정 주석으로 하중 밖이다.
- **distinction 3 (iteration vs adaptation): 보강 증거로만.** 결과-조건부 루프 6/6로 단독 차별력이 낮고 distinction 1/B.3와 겹친다.

두 반사실이 각각 독립적으로 >=2 사례를 바꾸므로 A.4 기준(POMDP/BED 제거 시 >=2 사례 변화)을 **축 수준에서** 충족한다. 판별 기준은 어휘 존재가 아니라 사례 해석의 실제 변화다(D.2 순환 금지 준수). 다만 이 충족은 축의 유용성(informativeness)을 세울 뿐 이론 유일성(load-bearing theory)을 세우지 않는다(B3).

## 9. 범위/비주장 정합성 (A.3와의 일관)

이 PASS는 **선택된 분석 축이 informative**함을 보일 뿐(제거 시 사례 해석이 병합됨), POMDP 완전 인스턴스화·BED 우선권·또는 이 축들이 POMDP/BED에 유일하게 의존한다는 이론 주장을 하지 않는다(A.3 준수; POMDP/BED 귀속은 동기적 참조 — 축을 generic taxonomy로 relabel해도 분류 보존). `formal_epistemic_utility_evidence=not_reported`(6/6), C05의 `selection_objective=not_reported`(M6), `design_selection_rule`에서 `discrimination_directed`/`information_directed`/`cost_directed`의 부재(6/6)는 모두 bounded-source 관찰이지 field-wide 부재 주장이 아니며(§7), 원고의 신중한 프레이밍과 일치한다. §4.4는 퇴역 closure 표현의 **표현적 공백**을 지적하는 교정 주석이며(관측된 병합이나 내부 ablation이 아님), A.4의 하중 증거가 아니다. A.4가 확인하는 것은 축 제거 시 **사례 해석이 실제로 바뀌는가**이며, 그 확인은 §3~§4의 반사실로 완결된다.
