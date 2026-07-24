# SERVO v5 — rule-stability spot-check (charter D.2(d))

- 상태: analysis 산출물 (2026-07-24). 이 문서는 **charter D.2(d)의 rule-stability check**이며, **inter-coder reliability(ICR)나 수치 κ가 아니다.** charter는 relation 단위에 ICR 지표를 두지 않고(§A.3 gate-reliability 순환 철회), 정성적 검증(blind 인간 판정 + 제2 모델 rule-stability + 적대검증)으로 대체한다. charter D.2(line 257)는 제2 모델을 **label 생성(코딩)이 아니라 rule-stability check로만** 쓰도록 명시한다 — 본 점검은 그 조건을 따른다.

## 무엇을 측정하나 (그리고 무엇을 측정하지 않나)

- **측정:** 동결된 rubric 규칙(`servo_v5_alignment_rubric.md`)을 pivotal 경계 명제에 **규칙대로 적용**하면, 저자와 **독립적인 제2 모델**(비-Claude)이 같은 분류에 도달하는가 = **규칙이 분류를 결정짓는가(rubric determinacy)**.
- **측정 안 함:** (1) 코더 독립 일치도(ICR/κ) — 제2 모델은 저자 코딩 모델(claude-opus)과 훈련을 부분 공유하므로 **완전 독립 코더가 아니다**; (2) 판정의 ground-truth 참/거짓; (3) 전수 신뢰도. 이는 **경계 표본 spot-check**이지 포괄 감사가 아니다.
- **완전한 독립성 요건(charter D.2(a), blind 인간 제2검토자)**은 단일저자 현실로 미충족이며, 원고가 이를 disclosed limitation으로 유지한다. 본 점검은 그 부분 보완일 뿐 대체가 아니다.

## 방법

- 제2 모델: **gpt-5.5**(`codex exec`, 비-Claude), stateless, 저자 label 미제공.
- 입력: rubric 핵심 규칙(functional_relation 튜플, occurrence_class, structurally_inferred, cross-step feedback 규칙, observation≠evaluation) + 동결 source proposition 인용문만.
- 질의: "규칙을 이 명제에 적용하면 (source_role, relation_type, target_role, temporal_scope)와 태그(occurrence_class, structurally_inferred)는?" — 자유 코딩 아닌 **규칙 적용**.
- 대상: 리뷰가 가장 다툰 **두 pivotal 피드백 판정** — (1) C01의 occurrence-established 피드백, (2) C05-A64(B1에서 강등된 판정).

## 결과

| 명제 | 저자 판정 | 제2 모델 규칙적용 | occurrence-established status | relation tuple |
|---|---|---|---|---|
| C01-P01 | evaluation→revises→artifact, cross_step, single_event, **inferred=False** | execution→triggers→action, cross_step, single_event, **inferred=False** | **일치**: stated single-event occurrence (확립) | **갈림** |
| C05-P22 | evaluation→updates→inquiry_state, cross_step, single_event, **inferred=True** (→ 비확립, B1) | candidate→evaluates→evaluation, **per_step**, inferred=False; "결과가 later step에 먹인다고 진술하지 않음" | **일치**: cross-step 피드백 occurrence **비확립** | **갈림** |

## 발견 (정직)

1. **occurrence-established 여부(헤드라인 판정)는 rule-stable.** 독립 제2 모델이 규칙을 적용해 — 저자와 **표현은 다르되 동일 결론** — C01-P01은 진술된 단일 발생(확립), C05-P22는 cross-step 피드백을 **확립하지 않는다**(둘 다 "결과가 later step을 조건화한다는 진술 없음")에 도달했다. 이는 **B1 교정(occurrence-established 피드백 = 정확히 하나, C01)**을 독립적으로 corroborate한다.
2. **relation-tuple 배정은 under-determined(rubric 모호성).** 같은 인용문에 대해 저자와 제2 모델이 서로 다른 (role, relation, target) 튜플을 골랐다(C01: evaluation-revises-artifact vs execution-triggers-action; C05: evaluation-updates-inquiry_state vs candidate-evaluates-evaluation). 즉 **어떤 발생인가(occurrence status)는 규칙이 결정짓지만, 어느 타입 튜플인가는 규칙이 완전히 결정짓지 못한다** — 이는 원고가 이미 "formative"로 disclose한 한계와 정합한다.

## 한계

- 2 판정 spot-check(경계 대상). 추가 피드백 후보(C05-P12 reported_as_procedure / C05-P27 manual update)로의 2차 확장은 제2 모델 호출 타임아웃으로 미완 — 재시도 시 보강 가능.
- 제2 모델은 훈련 공유로 완전 독립 아님 → 이 점검은 rubric determinacy의 정황 증거이지 독립 코더 신뢰도가 아니다.
- 완전한 독립 검증은 charter D.2(a) blind 인간 제2검토자를 요구하며 이는 여전히 미충족(disclosed limitation).
