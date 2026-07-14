# 참조 가이드 — 이 저장소에서 작업할 때 어디를 볼 것인가

> 이 저장소(`CAISc_2026`)는 **산출물 저장소**다: SERVO 논문(제출·채택)과 시뮬레이션 스켈레톤이 전부라, 배경 자료·지형·이론적 맥락은 여기에 없다.
> 그 맥락은 **자매 저장소 두 곳**에 산다. 이 가이드는 "여기서 작업할 때 저 경로들을 이렇게 참조하라"를 정리한다.

---

## 0. 자산 지형 (3개 저장소의 역할)

| 저장소 | 경로 | 역할 | 한 줄 |
|--------|------|------|------|
| **지형 / 지식베이스** | `/Users/jaesolshin/Documents/GitHub/ai_scientist/` | AI Scientist 분야 전체를 (S,G,E,V,M,π,H)로 수집·분석 | "무엇이 있고 왜 안 되는가"의 지도. OKF 번들 + 개념문서 ~161편 |
| **산출물 (이 repo)** | `/Users/jaesolshin/Documents/GitHub/CAISc_2026/` | SERVO 논문(개별 이론) + MiroFish 시뮬 | CAISc 2026 채택. `submission/`이 정본 |
| **후속 자산** | `/Users/jaesolshin/Documents/GitHub/aisci_abm/` | SERVO를 CPC-MS 집단으로 확장한 SERVO-MS | 리뷰가 요청한 "CPC-MS 차별화·경험적 검증"의 답 |

**자산 사슬**: `ai_scientist`(지형) -> `CAISc_2026/submission`(SERVO, 채택) -> `aisci_abm`(SERVO-MS 확장) -> `CAISc_2026/simulation`(MiroFish ABM 검증).

---

## 1. 지형 저장소(`ai_scientist`) 항해법

### 1.1 진입점 — 항상 여기부터
- **`AI_Scientist_Analysis.md`** (약 1,534줄) — **마스터 분석 노트이자 그래프 허브**. 전체를 종합한다. 섹션 지도:
  - §1 분류체계 · §2 이론적 위치(POMDP/BED) · §3 일반구조 · §4~5 핵심 논문 (S,G,E,V,M,π) 매핑
  - §6 프레임워크 정교화(6.6 π_learned 축) · §7 미해결 문제(7.8 S-표현, 7.9 답-양식) · §8 결론(발전 Phase·분파)
  - §9 도메인별 분석(수학~사회과학) · §10 통합결론(10.1 V 결정성, 10.3 환각 침투) · §11 타 서베이 좌표 매핑
  - 빠른 목차: `grep -nE '^#{2,3} ' AI_Scientist_Analysis.md`
- **`index.md`** — OKF 루트 목차. 6개 tier로 진입.
- **`log.md`** — 변경 이력. "제출 이후 무엇이 새로 들어왔나"는 여기 + git log로 확인.

### 1.2 OKF 번들 규약 (자료를 찾고 넣는 법)
- 6개 tier: `0_Theoretical_Foundations` · `1_AI_Scientist_Core` · `2_Domain_Applications` · `3_Self_Evolving_Agents` · `4_Epistemic_Agents_Risk` · `5_Wet_Lab_Infrastructure`. 각 tier에 `index.md`(목차).
- **논문 = concept `.md`**: PDF마다 동반 `.md`(frontmatter `type: paper`, `resource` 필드가 PDF를 가리킴). 개념 본문 + `[[위키링크]]`로 그래프 엣지.
- **비-PDF 웹 소스**: 각 tier의 `_resources/`에 `type: resource` 스텁.
- Obsidian vault로 열면 graph view로 개념 연결 열람 가능(dot-folder는 자동 무시).
- **특정 시스템/논문 찾기**: 해당 tier `index.md`에서 링크 따라가거나 `grep -ri '시스템명' <tier>/`.

### 1.3 지형을 갱신하는 법 — 손으로 넣지 말 것
- 새 논문/자원(arXiv·DOI·Nature URL, X 스크린샷 등)이 생기면 **`paper-update` 스킬**을 쓴다. PDF 다운로드 -> 분류 -> OKF concept 문서 생성 -> `AI_Scientist_Analysis.md`·`index.md`·`log.md` 갱신 -> (해당 시) TeX 갱신까지 자동.
- 트리거: "새 논문 추가", "논문 업데이트", "이 논문 넣어줘", arXiv/DOI/Nature 링크 공유.

---

## 2. 후속 자산 저장소(`aisci_abm`) 구성

| 파일 | 내용 |
|------|------|
| `servo-ms-model.md` | SERVO-MS 새 모델. 튜플 `(S,{G_i},{E_i},{V_i}∪C,{M_i}∪W,{π_i}∪Π,Ψ,H)` + 명제 P1–P6 (P4–P6 = 집단 고유) |
| `servo-ms-failure-modes.md` | 실패 양식을 베이지안 수렴조건 C1–C9 위반으로 연역 (C1–C6 개별, C7–C9 집단 신규) |
| `servo-ms-abstract.md` | **AI4Sci Korea 2026** 거버넌스 트랙 제출 초록(316단어) + 제목후보 + ABM 상전이 설계(C7·C7×C8·C9/MiroFish) |

이 세 문서가 CAISc 리뷰(특히 AI 2의 "CPC-MS 미차별화")에 대한 후속 응답의 골격이다. 상세는 `CAISc_2026/POST_SUBMISSION_AND_REVIEW.md` 참조.

---

## 3. "X가 필요하면 -> 여기" 조견표

| 필요 | 경로 |
|------|------|
| SERVO 개념 전체 배경·근거 | `ai_scientist/AI_Scientist_Analysis.md` (그래프 허브) |
| 특정 시스템/논문의 상세(예: NovelSeek, GNoME, Robin) | 해당 tier `index.md` -> concept `.md`; 또는 `grep -ri` |
| 도메인별 병목(수학 novelty, 화학 wet-lab 등) | `AI_Scientist_Analysis.md` §9 |
| 미해결 문제·open problem 근거 | 동 §7 (7.1 novelty · 7.2 BED · 7.8 S-표현 · 7.9 답-양식) |
| 벤치마크·평가 사다리(CORE-Bench·AstaBench·ICML2026) | 동 §7.3 |
| RSI/자기진화 분파(Sakana·Anthropic·Red Queen) | 동 §8 분파 + tier `3_Self_Evolving_Agents/` |
| 환각·기만·신뢰 위험 | 동 §10.3 + tier `4_Epistemic_Agents_Risk/` |
| 집단 확장(CPC-MS·SERVO-MS)·실패분류 | `aisci_abm/servo-ms-*.md` |
| 리뷰 대응·제출후 수집 요약 | `CAISc_2026/POST_SUBMISSION_AND_REVIEW.md` |
| SERVO 정본 원고 | `CAISc_2026/submission/main.tex` (EN) · `main_ko.tex` (KO) |
| 컴파일·산출물 규칙 | `CAISc_2026/CLAUDE.md` |
| 최근 무엇이 추가됐나 | `ai_scientist/log.md` + `git -C ai_scientist log --oneline` |

---

## 4. 정본·사본 주의 (혼동 방지)

- **SERVO 정본은 이 저장소 `CAISc_2026/submission/`**이다(채택 제출본 `72_Formalizing_AI_Scientist_Sy.pdf`, 소스 `main.tex`/`main_ko.tex`).
- `ai_scientist/`에도 `formalizing_ai_scientist.md`·`formalizing_AI_scientist.pdf`·`paper/`가 있으나 이는 **초기/미러 사본**이다. 원고를 고칠 때는 반드시 `CAISc_2026/submission/`을 건드린다.
- MiroFish/시뮬레이션 정본은 `CAISc_2026/simulation/`. (SERVO-MS ABM 설계 노트는 `aisci_abm/`.)

---

## 5. 작업 시작 루틴 (권장)

1. 이 저장소에서 무언가를 하려면, 먼저 `ai_scientist/AI_Scientist_Analysis.md`의 관련 § 를 읽어 배경을 잡는다(허브 -> 세부).
2. 특정 시스템이 필요하면 tier `index.md` 또는 grep으로 concept 문서를 연다.
3. 새 자료가 생기면 손으로 넣지 말고 `paper-update` 스킬로 지형에 편입한다.
4. 원고·시뮬은 이 저장소의 정본만 수정하고, `CLAUDE.md`의 컴파일 순서를 지킨다.
