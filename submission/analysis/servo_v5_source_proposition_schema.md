# SERVO v5 SourceProposition ledger 스키마

- 상태: DRAFT (charter v5.0-rules Part B.1 구현)
- 지위: charter의 세 객체(SourceProposition / AuthorAlignment / DerivedDecisionClaim) 중 **첫째**. 판정·해석 없이 출처가 직접 말한 것만 저장한다.

## 파일 배치

- `analysis/servo_v5_source_propositions/<case_id>.json` (사례별 1파일)
- 파일럿: `analysis/servo_v5_source_propositions/C01.json`

## SourceProposition 레코드 필드

| 필드 | 내용 | 규칙 |
|---|---|---|
| `proposition_id` | `<case_id>-P<nn>` | 안정적, 재사용 금지 |
| `case_id` | 사례 식별자 | |
| `source_pdf_sha256` | 원 PDF 해시 | fail-closed 감사 |
| `locator` | `{pdf_page, para_anchor?}` | 페이지 필수 |
| `exact_quote` | 출처 원문 그대로 | 축약 금지; 불가피한 생략은 `[...]`로 표시하고 최소화 |
| `modality` | `directly_reported` / `reported_as_procedure` / `reported_only_as_capability` | 아래 규칙 |
| `named_actors` | 출처가 **직접 명명**한 행위자만 | 추론 금지 |
| `named_inputs` | 직접 명명된 입력 | 추론 금지 |
| `named_outputs` | 직접 명명된 출력 | 추론 금지 |
| `source_context_note` | (선택) 출처 표현상 필요한 최소 메모 | 판정 금지 (charter B.8 허용/금지 목록) |

### modality 규칙 (증거 해상도, 판정 아님)

- quote의 **문법적 양태에서만** 결정한다. `support_status`를 함의하지 않는다.
- `directly_reported`: 실제 발생을 서술(과거/현재 사건). 예: "Coscientist uses the Docs searcher module ... modifies the protocol".
- `reported_as_procedure`: 시스템이 일반적으로 무엇을 하도록 규정된다는 절차 서술. 예: "the system then evaluates each candidate".
- `reported_only_as_capability`: 능력·가능성 서술. 예: "the model **can** effectively reuse the information".

## 금지 — 다른 객체로 이동

| 기존 ledger의 필드/내용 | 이동 대상 |
|---|---|
| `decision_role`, `evaluator_substrate`, component mapping(S/G/E/V/M/pi) | `AuthorAlignment` |
| `adjudication`, established/unknown, closure predicate | `DerivedDecisionClaim` |
| 4축(`support_status`/`claim_scope`/`alignment_kind`/`occurrence_resolution`) | `DerivedDecisionClaim` |
| permitted/prohibited stronger claim | 감사용 경계 정보(별도). status 직접 결정 금지 |

## 작성 규율 (B.3 단조 하향과 정합)

1. **원 PDF에서 추출한다.** 기존 closure matrix·adjudication·evidence_ledger를 출발점으로 삼지 않는다(있으면 quote 대조용으로만).
2. **판정에 필요한 것만 고르지 않는다.** 해당 configuration을 서술하는 proposition을 폭넓게 기록한다(negative/무관해 보이는 것 포함).
3. 하나의 quote = 하나의 proposition. 여러 주장을 담은 문장은 분할하되 원문 경계를 지킨다.
4. source silence는 proposition을 만들지 않는다(부재를 기록하지 않는다). 부재 판정은 DerivedDecisionClaim에서 `unresolved`로 처리한다.
