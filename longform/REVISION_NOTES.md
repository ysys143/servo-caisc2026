# 논문 수정 방향 노트

**출처:** CMU LTI Prometheus AI 리뷰어 + Agy/Codex AI Council 교차 검토  
**대상 논문:** Formalizing AI Scientist System (SERVO 프레임워크)  
**날짜:** 2026-05-31

---

## 수정 우선순위 요약

```
전략   하이브리드 — 이론(명제)이 엄밀성 담당, 서베이는 현 수준 유지·"증거→예시"로 역할 강등
1순위  항목 4  POMDP/BED 형식화 보강 (선택 A): 명제 2~3개 증명 → 논문의 새 엄밀성 핵심
2순위  항목 2  V-completeness를 "명제"로 재구성 (서베이는 예시). systems.csv/Kappa 미실행
3순위  항목 1  "first" 제거 + 선행 3편 인용 (필수·저렴)
4순위  항목 3  Coscientist loop-partial 정정 (예시 정확성, 필수·저렴)
제목   "Formalizing" 유지 — 형식화가 엄밀성 담당하므로 정당화됨 (retitle B/C 철회)
```

---

## 전략 확정 (2026-05-31): 하이브리드 — 이론 보강 + 서베이 현수준

**결정:** 항목 2의 rigor-first(이중코딩·Kappa·systems.csv 빌드)는 **철회**. 대신 **이론(명제)이 엄밀성을 담당**하고 **서베이는 현 수준 유지하되 "증거"에서 "예시(illustration)"로 역할 강등**.

**근거:** V-completeness 주장을 형식 모델에서 도출되는 명제로 재구성하면, 주장의 입증 부담이 질적 코딩에서 증명으로 이동한다. 그러면 항목 2의 "재현 불가능한 질적 코딩" 비판은 **서베이의 인식론적 지위 변경**(증거→예시)으로 해소된다 — 코딩이 더 이상 입증 부담을 지지 않으므로.

**각 항목 귀결:**
- **항목 4** → 선택 A(이론 보강)로 전환. 직전의 "lens 톤다운(선택 B)"은 폐기. 논문의 새 엄밀성 중심.
- **항목 2** → systems.csv/Kappa 미실행. V-completeness를 명제로 재구성 + 표를 "예시"로 재프레이밍 + 보편 주장("without exception/every/determines") 약화 + Limitations에 "서베이 코딩은 예시적·질적" 명시.
- **항목 1·3** → 변경 없음, 필수·저렴 (인용/정확성). 시스템이 예시가 되므로 정확한 기술이 오히려 더 중요.
- **제목** → "Formalizing" 유지 (형식화가 엄밀성 담당하므로 정당화). retitle B/C 철회.

**명제 초안 (3 open problem ↔ 3 proposition 매핑):**

V층을 관측/보상 채널의 속성으로 캐스팅: `V_empirical`=관측함수 O가 informative·unbiased / `V_semantic`=O에 systematic error / `V_human`=고품질이나 간헐적, novelty 식별에 필수.

- **Prop 1 (충분성, BED gap)**: V가 belief의 충분통계를 보존하는 unbiased·calibrated 신호이고 정책이 BED/EIG를 따르면, bounded-S·stationary-T 하위문제에서 belief가 수렴하고 루프가 닫힌다. (차용: POMDP/active-learning 수렴, EIG myopic optimality)
- **Prop 2 (편향 drift)**: V가 편향 추정자(예: V_semantic systematic error)이면 EIG 정책이 편향된 고정점으로 수렴 — 루프는 계산적으로 닫히나 잘못된 표적에. (차용: 오설정 가능도 하의 베이즈 사후 불일치)
- **Prop 3 (novelty 비식별성)**: 표적의 일부(novelty/significance)가 어떤 자동 채널로도 측정 불가(V_human 필수)하면, 자동 validator로는 그 성분의 추정자가 존재하지 않는다 → V_human 없이 novelty에 대한 완전자율 루프 폐쇄 불가. (impossibility형 — "novelty 비자동성" open problem의 형식화)
- **(선택) Prop 4 (M_s 충분성)**: M이 history의 충분통계를 보존하지 못하면 정책이 degrade. (차용: belief-MDP 충분통계)

→ 세 open problem(novelty 비자동성·BED gap·M_s 미발달)이 그대로 Prop 3·1/2·4로 형식화됨. V-completeness가 Prop 1~3의 공통 축.

**서베이=예시 매핑:** Coscientist(V_human only→Prop 3 binding, loop-partial) / AI Sci 2026(3층 V→Prop 1 근접) / GNoME(calibrated V_empirical+EIG-proxy→Prop 1 충족, loop closed) / Agent Lab(편향 V_semantic→Prop 2 위험).

**리스크 관리:** 명제가 정의 재진술로 무너지면 순환논증 → 이론 리뷰어가 죽임. 방어: 명제를 **명시적 제한 가정 하에서** 진술(예: "bounded-S, calibrated V_empirical 하위문제에서") + 차용 정리(불일치·수렴)에 reduction. open-ended 일반항은 증명 범위 밖임을 명시(항목 4 리뷰어의 "비표준 가정" 지적 동시 해소).

> 아래 "항목 2/4 상세 섹션"의 rigor-first/lens 서술은 **이 결정으로 supersede됨**. 이력 보존용으로 남김.

---

## 통합 수정 체크리스트 (single source of truth)

> 4개 항목의 concrete action + 검토 중 발견한 gap(a~d) 전부 포함. 각 행에 (항목) 태그. `[실행후]` = systems.csv/Kappa 결과 확보 후 수치 채워 수정.

### A. 원고 본문 (`main.tex`; `main_ko.tex` 동일 미러)

- [ ] **L67 초록** — (1) "systems lack a unifying formal framework" → "recent LLM-agent 하위분야" 범위 한정
- [ ] **L67 초록** — (2, gap a) "V completeness ... **determines** whether closed-loop ... feasible" → 인과 톤 보정 `[실행후]` [중요] 초록에도 같은 인과 주장 있음, 본문만 고치면 불완전
- [ ] **L79 contributions** — (1·4, gap c) "decomposes **any** AI Scientist system" 의 "any"(보편) + "formal framework" 톤 점검
- [ ] **L94 POMDP 튜플** — (4, 선택 A) b₀·h 추가해 튜플 완비 + 명제 성립 제한영역(bounded-S 하위문제) 정의. open-ended 일반항은 증명 범위 밖임을 명시
- [ ] **L96 직후** — (4, 선택 A) 비표준 가정(R 미명세·S 무한·T 비정상) 하에서 명제가 성립하는 제한 영역을 형식적으로 한정
- [ ] **L100–107 BED + 신규 명제** — (4, 선택 A) Prop 1~3(+4) statement·가정·차용정리 추가. EIG 적용 조건(θ·prior·simulator) 명시
- [ ] **L116 Related Work** — (1·4) "no prior work explicitly applies BED as a design target" 의 first 함의 제거 + Robot Scientist/NovelSeek/Co-Scientist 선행성 인정 문장
- [ ] **§3 ¶3 직후** — (1) 선행 프레임워크 단락 신규 삽입 (리뷰어 지정 위치)
- [ ] **L181 / L191 / L298 Coscientist** — (3) "$V_h$ only / loop does not close" → "loop-partial (task-opt)". L191 "measurement results are not fed back" 사실오류 교체
- [ ] **L323 / L409 / L488 V-completeness 주장** — (2) "primary determinant / determines / every advance"를 **명제(Prop 1~3)로 재구성** + 보편표현 약화("consistent with our propositions; surveyed systems illustrate"). κ/systems.csv 미사용
- [ ] **L481 Limitations** — (2) "단일 1차 코더 + 구조화 2차 코딩, 관측적 설계(인과 아닌 연관), n=15" 추가
- [x] **제목** — (4) **"Formalizing AI Scientist Systems" 유지**. 하이브리드에서 형식화(Prop 1~3)가 엄밀성을 담당하므로 (i)이론정리 약속이 실제 이행됨 → 제목 정당화. retitle B/C 철회. 본문에 "we formalize via SERVO + propositions; the survey illustrates them"로 형식화 대상 명확화

### B. 표 (`tab:` 환경)

- [ ] **tab:core-comparison (L287)** — (3) Coscientist `Loop closed? No → Partial (task-opt)`
- [ ] **tab:core-comparison (L287)** — (1, gap b·d) **Robot Scientist · NovelSeek 행 추가** → 역방향 SERVO 매핑을 표로 직접 제시
- [ ] **tab:core-comparison / tab:domain-comparison** — (2) CSV에서 **TeX**(`\input{}`)로 생성, 외부 HTML 참조 폐기

### C. 참고문헌 (`references.bib`)

- [ ] **Sparkes 2010 (Robot Scientist)** — 신규 추가
- [ ] **NovelSeek/InternAgent (Zhang 2025, arXiv:2505.16938)** — 신규 추가
- [x] `gottweis2026coscientist` — **이미 존재**, 본문 인용·분석만 추가 (1)
- [ ] Poupart 2011 — 선택 (kaelbling1998pomdp로 충분)

### D. 형식화 보강 (항목 4 선택 A) — 하이브리드의 엄밀성 핵심

- [ ] **§2 형식 모델 보강** — belief update 정의, V층=관측/보상 채널 속성으로 캐스팅
- [ ] **Prop 1 (충분성/BED)** — statement+proof (차용: POMDP 수렴, EIG myopic optimality)
- [ ] **Prop 2 (편향 drift)** — statement+proof (차용: 오설정 가능도 사후 불일치)
- [ ] **Prop 3 (novelty 비식별성)** — statement+proof (impossibility형, novelty 비자동성 형식화)
- [ ] **(선택) Prop 4 (M_s 충분통계)** — statement+proof
- [ ] **서베이 표 → 명제 "예시"로 재프레이밍** (현 수준 유지, 신규 코딩 없음)
- ~~systems.csv / build_servo_tables.py / reliability_report.md~~ (rigor-first 철회로 미사용)

### 선결정 사항 (착수 전 합의)

1. [해결] **항목 4 = 선택 A** (하이브리드): Prop 1~3 형식화가 엄밀성 담당
2. [해결] **제목 = "Formalizing" 유지**
3. **명제 가정 범위**: Prop 1~3 성립 제한가정(bounded-S, calibrated V_empirical 등)을 어디까지 좁힐지 — 비자명성 vs 증명가능성 균형 (**핵심 선결정**)
4. **Prop 4(M_s) 포함 여부**: 3개 vs 4개
- ~~V_completeness 척도 / Coder B 프롬프트~~ (systems.csv 철회로 불필요)

### 의존 순서

```
명제 설계(Prop 1~3 statement+가정) → 증명(차용정리 reduction) → §2 형식모델 본문화
        ↓ (병렬, 결과 무관)
  항목 1(bib 2건+선행단락) · 항목 3(Coscientist 정정) · 서베이 표→예시 재프레이밍
        ↓
  V-completeness 본문(L67②·L323·L409·L488)을 명제 참조로 재서술 + Limitations(서베이=예시·질적) 추가
```

---

## 항목 1: 독창성 과대주장 수정

**비판 요약:** Robot Scientist(2010), NovelSeek(2025), Co-Scientist(Nature 2026) 등 선행 통합 프레임워크를 누락했고, "we are the first to apply BED as a design target" 주장이 근거 부족.

**수정 방향:**

- "we are the first" 표현 전면 제거
- 아래 3편을 Related Work 및 비교 테이블에 추가:
  - Sparkes et al. (2010) Robot Scientist — SERVO의 generator/executor/validator/memory/policy와 컴포넌트 수준에서 겹침
  - Zhang et al. (arXiv 2025) NovelSeek — "unified, closed-loop" 동일 언어 사용
  - Gottweis et al. (Nature 2026-05-19) Co-Scientist — V-completeness 논지와 직결
- 이들이 SERVO 컴포넌트(S, G, E, V, M, π, H)에 어떻게 매핑되는지 역방향 분석 추가
- 기여를 "새 시스템 제안"이 아닌 **"기존 시스템들을 비교 가능하게 만드는 재현 가능한 진단 좌표계 제안"** 으로 재포지셔닝
- 방어 가능한 novelty 표현:
  - "V 4층 분해, M 3층 분해, H 인간 개입 매개변수를 결합한 진단 좌표계"
  - "현재 시스템들의 정책을 BED/EIG라는 규범적 기준에 비추어 비교하고, 간극을 open problem으로 제시"

**Co-Scientist(Gottweis, Google, Nature 2026) 추가 시 정확한 SERVO 매핑** (항목 3에서 이관 — 원래 이 시스템이 항목 1 누락 인용 대상):

| 컴포넌트 | 내용 |
|---|---|
| S | 인간 연구자가 정의한 연구 질문 공간 |
| G | Generation → Reflection → Evolution → Elo 토너먼트 기반 가설 개선 |
| E | 물리적 실험 실행 없음. 실험 프로토콜 제안 수준 |
| V | LLM reflection/ranking + 인간 전문가 평가 + 독립 wet-lab 검증 |
| M | 가설·평가·피드백의 지속 컨텍스트 |
| π | supervisor 비동기 운영, 연구 방향·최종 판단은 인간 협업 구조 |
| H | H ≈ 0.6–0.8 (협업형, 높음) |

- 본문에서 Co-Scientist를 "완전 자율 추구 분파(H→0)" vs "인간-AI 협업 최적화 분파(H→0.7)" 패러다임 분기의 후자 대표 사례로 활용 → V_human·H가 자동화 불가능한 참신성 판단을 보완한다는 논지를 실증적으로 뒷받침(저자에게 유리).
- AML 세포주·간 오가노이드·항생제 내성 wet-lab 검증으로 V_empirical 기여 공정 기술.
- **주의:** 논문 §6 "collective AI co-scientist"(Taniguchi CPC 인용)는 Google Co-Scientist와 별개 개념. 본문에서 명칭 충돌 주의 — Google 시스템은 구체 사례, collective co-scientist는 향후 다중에이전트 확장 비전.

---

## 항목 2: V-completeness 방법론 재현성 보강

**비판 요약:** V-completeness 논지가 투명한 선정 기준 없이 임의 선별된 시스템에서 도출됨. 재현 불가능.

**수정 방향:**

- Methods 섹션 신설 또는 보강:
  - 검색 범위, 기간, 키워드 명시
  - 포함 기준(Inclusion Criteria): G→E→V 루프를 최소 1회 연결하거나 제어하는 시스템
  - 제외 기준(Exclusion Criteria): 탐색 정책 π와 피드백 루프 없는 단순 파이프라인, 예측 도구(AlphaFold 등)
- V 계층별 판정 루브릭 표 추가:
  - `V_syntax`: 컴파일·스키마·타입체크 — 결정론적 통과/실패
  - `V_semantic`: LLM judge·루브릭·텍스트 평가
  - `V_empirical`: 실험·벤치마크·wet-lab 측정
  - `V_human`: 참신성·유의성·커뮤니티 위치화 판단
- 부록에 전체 코딩 매트릭스 공개: 각 시스템별 증거 문장, 판정, 불확실성 플래그
- 가능하면 복수 코더 교차 평가 일치도(Cohen's Kappa) 제시

**[SUPERSEDED 2026-05-31 → 하이브리드]** ~~rigor-first(이중코딩·Kappa·systems.csv)~~ 철회됨. 상단 "전략 확정: 하이브리드" 참조. 항목 2는 V-completeness를 **명제로 재구성**하고 서베이는 현 수준 예시로 둔다. 아래 rigor-first 상세는 이력 보존용(미실행).

**리뷰어 검증으로 확인된 추가 사실 (2026-05-31):**

- 리뷰어가 자동 검증 코드를 실행해 `tbl-0.html`, `tbl-1.html` 파일이 preprint 디렉토리에 부재함을 확인했다고 주장. **단, 이는 부분적 false positive다** — 검토 대상은 영문 `main.tex`(495줄, 7개 table 환경)였고, 표들은 inline LaTeX로 **소스에 실제로 존재**한다(`tab:core-comparison` L287, `tab:domain-comparison` L411). "tbl-0.html/tbl-1.html 부재"는 CMU 리뷰어 파이프라인이 PDF→OCR/HTML 변환 시 표를 외부 참조로 처리하다 누락한 **변환 아티팩트**이지 원고 결함이 아니다.
- **AI 리뷰어 인용 부정확성**: 리뷰어가 "인용"한 `"V completeness co-varies with loop closability without exception"` 문구는 현재 main.tex에 **존재하지 않는다**. 실제 문장은 L323 `"the completeness of V is the primary determinant of closed-loop feasibility"`, L409 `"V completeness determines π capability and closed-loop feasibility"`. AI 리뷰어가 원문에 없는 문장을 따옴표로 제시한 것은 그 자체로 반박 가능한 약점(저자 rebuttal에서 지적 가능).
- **그럼에도 substantive 비판은 유효**: 표가 존재해도 (1) 조작적 점수 기준, (2) inter-coder 일치도, (3) 음성 사례, (4) 민감도 분석이 없다. 프레임워크가 V를 명명 강조하므로 **확증 편향** 위험 실재. 실제 원고의 강한 주장:
  - L323 `"primary determinant of closed-loop feasibility"`
  - L488 `"every architectural advance ... is ultimately a gain in V completeness"`
- 체크리스트가 "방법론 §5·§6에 완전 기술"이라 주장하나 실제론 포함/제외 기준·코더 지침·기계 가독 테이블 없음. LLM이 문헌 검색·컴포넌트 추출 수행한 점이 감사 추적 필요성을 오히려 높임.

**전략 함의**: 저자는 rebuttal에서 (a) 표는 소스에 존재(변환 아티팩트), (b) 인용 문구 부정확을 지적해 리뷰어 신뢰도를 깎으면서, **동시에** 아래 선택 A로 재현성을 실제로 강화하면 가장 강한 포지션. "비판이 틀렸다"가 아니라 "지적한 파일 문제는 변환 탓이나, 더 깊은 재현성 우려는 정당하므로 수용한다"는 톤.

---

### 선택 A 실행 계획 — 엄밀 코딩 방법론 (rigor-first 확정)

**원칙:** claim 강도는 입력이 아니라 **출력**이다. 주장을 미리 낮추지 않고, 표준화된 코딩 프로토콜을 먼저 구축·실행한 뒤 그 결과(일치도·민감도·반례 유무)가 지지하는 정확한 강도로 주장을 보정한다.

**솔직한 천장(ceiling):** 최대 엄밀화해도 n≈15, 변수 동시변동, 관측적(통제 조작 불가) 설계이므로 도달 가능한 최강 주장은 "투명한 이중 코딩 프로토콜 하에서 반례 없이 견고한 강한 연관 + 메커니즘적으로 가장 그럴듯한 인과 병목"이다. "입증된 인과 결정 요인(determines)"은 설계상 불가. 엄밀성은 바닥(감사가능성·주관성 감소·견고성)을 최대로 올리며, 천장은 설계가 정한다.

**단계 0 — 조작적 코딩 루브릭 (`coding_protocol.md`) — 핵심 산출물**

"표준화된 코드에 의거"의 실체. 각 셀을 **원문 직접 인용으로 yes/no 답 가능한 지표**로 정의해 주관성을 제거 가능한 범위까지 제거한다.

*V 4층 — 각각 이진 지표 {0,1}, 각 셀에 직접 인용 필수:*
- `V_syntax`: 결정론적 자동 pass/fail 검사(컴파일·스키마·타입·포맷)가 존재하는가
- `V_semantic`: LLM/루브릭 기반 출력 점수화가 존재하는가
- `V_empirical`: 측정된 실험/벤치마크 결과가 루프에 피드백되는가
- `V_human`: validity/novelty 판정에 인간 판단이 필수인가
- `V_completeness`: 위 자동화 층 수에서 파생되는 순서형 척도 (사전 정의된 격자)

*loop_status — 3경계 조작화 (항목 3의 모호성을 구조적으로 해소):*
- `L_task`: task-optimization 경계에서 결과가 이후 선택에 반영되는 피드백 루프가 문서화됐는가
- `L_measurement`: 측정→분석 루프가 자동인가(인간 위임 아님)
- `L_discovery`: novelty 검증 포함 hypothesis→experiment→new-hypothesis 자율 사이클이 있는가
- `loop_status` 레이블 = 세 이진값에서 파생 (none / partial@경계 / closed@경계). Coscientist 사례: `L_task=1, L_measurement=0, L_discovery=0` → "partial (task-opt)"

*H — 순서형 {0, .25, .5, .75, 1}, 인간이 G/π/V_human 중 무엇을 수행하는지 규칙 기반.*

각 셀 레코드: `value | direct_quote | source_location | coder_id`.

**단계 1 — 이중 독립 코딩 + 일치도 (필수, 선택 아님)**

- **Coder A (저자)**: `AI_Scientist_Analysis.md` §4~5 기반, 단 원문 인용으로 재검증.
- **Coder B (독립 LLM 에이전트)**: `coding_protocol.md` + 원문 PDF만 제공, **V-completeness 가설에 blind**(확증 편향 차단). 프롬프트 전문 공개.
  - 주의: 논문 자신이 LLM-as-judge 편향(§7.6)을 비판 → Coder B는 주관적 품질 점수가 아니라 **명시적 텍스트로 답 가능한 구조적/이진 지표에만** 사용. "구조화된 2차 코딩"으로 명명하고 Kappa는 객관성 주장이 아니라 투명성 지표로 제시.
- 필드별 Cohen's Kappa 산출 → 불일치는 문서화된 근거로 adjudicate → 일치율 보고.

**단계 2 — 민감도/견고성 (필수)**

- 코더 불일치 OR `uncertainty_note` 플래그 셀 전부에 대해 대안 레이블로 재코딩.
- 모든 재코딩 조합에서 V-completeness ↔ loop-closure 연관이 유지되는지 재검정 → 견고성 보고.

**단계 3 — 반례 탐색 (필수, Popper식 falsification)**

- 명시적으로 탐색: (a) V-incomplete인데 loop-closed, (b) V-complete인데 loop-open.
- 발견 시 보편 주장 한정; 미발견 시 "탐색 절차 + 반례 없음" 보고. 이것이 인과 주장을 방어하는 유일한 정당 근거.

**단계 4 — 산출물 빌드 (`analysis/`)**

```
analysis/
├── coding_protocol.md        # 포함/제외 기준 + 조작적 루브릭 + 코더 지침 + Coder B 프롬프트
├── systems.csv               # 15편 × (셀값+인용+출처+코더) 매트릭스, 이중 코딩
├── build_servo_tables.py     # CSV→TeX 표 생성 + 검증 + Kappa + 민감도 + 반례 리포트
└── reliability_report.md     # Kappa·민감도·반례 결과 (= claim 보정의 근거)
```

- `build_servo_tables.py` 검증 함수(빌드 실패 조건): 모든 셀에 직접 인용 존재 / 인용 출처 파일 실재(리뷰어 verify 미러) / 표 아티팩트 생성 / Kappa 계산 완료.
- 표는 **TeX**(`\input{tbl-core.tex}`)로 생성해 외부 HTML 참조 누락(CMU 지적)을 구조적으로 회피. 대상: `tab:core-comparison`(main.tex L287) + `tab:domain-comparison`(L411); 나머지 8개 \sgmvpi 표는 CSV 행에서 파생.

**단계 5 — claim 보정 (방법론 실행 결과의 함수)**

`reliability_report.md` 결과에 따라 원고 문장을 보정. 예상 결과 기준 권장 보정:
- L323 `"the primary determinant of closed-loop feasibility"` → `"the strongest and most robust correlate of closed-loop feasibility across our double-coded set (κ=…, no counterexamples found)"`
- L409 `"V completeness determines π capability..."` → `"V completeness is the dimension most tightly associated with π capability and loop closure; we argue it is the most plausible causal bottleneck"`
- L488 `"every architectural advance ... is ultimately a gain in V"` → `"every advance in our sample coincides with a V-completeness gain; no counterexample was found under the coding protocol"`
- 한글 main_ko.tex L478도 동일 톤. **단 보정 문구의 κ·반례 수치는 실제 실행 후 채움** — 임의로 적지 않는다.

**Methods/부록 반영:** `coding_protocol.md`를 부록 방법론 섹션으로, `reliability_report.md` 요약을 본문에. Limitations에 "단일 1차 코더 + 구조화 2차 코딩, 관측적 설계로 인과 아닌 연관 보고, n=15" 명시.

**항목 1·3과의 시너지:** `source_quote` 수집은 항목 3(Coscientist 재코딩 근거)·항목 1(선행연구 SERVO 매핑) 자료와 중복 → 세 항목 동시 처리 시 한계비용 감소. `loop_status`의 3경계 정의가 항목 3을 직접 해소.

**예상 난점:** (1) `source_quote` 수집 — 15편 PDF에서 셀별 인용 추출(노동집약, 단 PDF 전량 보유). (2) Coder B blind 설정 — 가설 누설 없는 프롬프트 설계 필요. (3) Kappa가 낮게 나올 위험 — 그 경우 루브릭이 덜 조작적이라는 신호이므로 루브릭을 더 이진화해 재코딩(이 자체가 방법론 개선).

---

## 항목 3: Coscientist(Boiko) 기술 수정

> **[정정 2026-05-31]** 이전 노트는 이 항목을 Google의 **Co-Scientist**(Gottweis, Nature 2026)로 잘못 다뤘다. CMU 리뷰어 항목 3은 ref [6] = **Boiko et al. 2023 "Coscientist"**(화학 자율 합성, GPT-4+RoboRXN)에 관한 것이다. 두 시스템은 별개:
> - **Coscientist**(한 단어) = Boiko 2023, 화학 wet-lab — **항목 3 대상**
> - **Co-Scientist**(하이픈) = Gottweis 2026, Google Gemini 다중에이전트 — **항목 1의 누락 인용 대상**
>
> 위 표(Elo 토너먼트·H≈0.7·AML/오가노이드)는 Google Co-Scientist 내용이므로 **항목 1**로 이관해야 한다. 첫 턴 AI council이 제목의 "Coscientist"를 "Co-Scientist"로 오독한 데서 비롯된 오류.

**비판 요약:** 논문이 Coscientist를 "단일 GC-MS 측정($V_h$만)"으로 축소해 cross-system V-completeness 진행(약→강)의 가장 약한 끝에 배치하는데, 이는 과도한 압축이다. Coscientist는 6개 다양한 태스크, tool-use, 로봇 실행, 반복적 반응 최적화를 포함했다.

**평가 기준:** Quality, Originality, Clarity

**원고 대조 (영문 main.tex, 리뷰 대상):**

| 위치 | 실제 서술 | 검증 |
|---|---|---|
| L181 (Coscientist 표) | `$V$ & $V_\text{human}$ only: author inspection + single GC-MS measurement` | 리뷰어 지적과 일치 — "single GC-MS" 실재 |
| L191 ((B) Loop) | `The loop does not close ... measurement results are not fed back to the agent.` | **여기가 핵심 약점** |
| L298 (core 표) | Coscientist: Loop closed? = `No`, $V$ completeness = `$V_h$ only` | 일치 |
| L488 (결론) | `from Coscientist's single-measurement $V_\text{human}$ ...` | 진행의 약한 끝으로 사용 — 일치 |

**검증 결과 — 항목 2와 다르게 substantive하게 유효:**

1. **리뷰어 verbatim "인용"은 또 부정확**: 리뷰어가 따옴표로 제시한 `"Coscientist's single GC-MS measurement ($V_h$ only) prevents loop closure entirely"`는 원고에 그대로 존재하지 않는다. L181("single GC-MS")+L298("$V_h$ only")+L191("loop does not close")을 합성한 문장. → 항목 2와 동일한 AI 리뷰어 인용 날조 패턴. rebuttal에서 지적 가능.
2. **그러나 내용 비판은 정당**: 원고 L191 `"measurement results are not fed back to the agent"`는 **사실상 부정확**하다. Boiko의 palladium 교차커플링 반응 최적화 실험에서 에이전트는 측정 결과를 재사용했다(원문: "normalized advantage values increase over time, ... reuse the information obtained"). 즉 task-level 최적화 피드백 루프는 실재했다. "루프가 전혀 닫히지 않는다"는 서술은 너무 절대적.
3. Boiko 측 인용(6개 태스크·palladium 교차커플링·semi-autonomous)은 진짜 — Nature 2023 초록의 실제 문장.

**수정 방향 (리뷰어 제안 수용 권장):**

- 원고 L181/L191/L298의 Coscientist 코딩을 **"loop-none"이 아니라 "loop-partial (task-level optimization feedback)"**로 재코딩. 단 자율적 novelty/discovery 검증은 없음을 명확히 유지.
- L191 문장 교체안:
  > "Coscientist demonstrates semi-autonomous experimental design and execution across multiple chemistry tasks, including iterative reaction-optimization settings in which measured outcomes inform later choices. In Servo terms it supports constrained task-level feedback, but it does not provide an autonomous validator for the novelty or significance of a discovery claim; those judgments remain human-mediated. We therefore code Coscientist as loop-partial rather than loop-closed."
- core 표(L296/L298): Coscientist의 `Loop closed? No` → `Partial (task-opt)`. 표는 이미 AgentLab을 `Partial`로 코딩하므로 어휘 일관.

**중요 — 이 수정은 논지를 해치지 않는다:**

- V-completeness 진행 논지는 그대로 유지된다. Coscientist는 여전히 약한 끝($V_e$/$V_s$/자율 novelty 검증 부재). loop status만 "none→partial"로 정확화하는 것이며, 오히려 분석의 신뢰도를 높인다.
- **항목 2와의 연결**: 이 비판의 본질은 "루프 폐쇄를 어느 경계에서 판정하는가"(task-optimization 경계 vs physical-measurement 경계 vs scientific-novelty 경계)다. 항목 2의 코딩 프로토콜에서 **loop-closure 경계 정의를 명시**하면 항목 2·3을 동시에 해소. systems.csv의 `loop_status` 컬럼에 "어느 경계 기준인지"를 기록해야 함.

---

## 항목 4: POMDP/BED 형식적 기반 처리

**비판 요약:** POMDP/BED 연결이 선언적으로만 제시됨. 수식 전개·명제·증명 없음.

**전략 선택 (둘 중 하나 결정 필요):**

### 선택 A: 이론 보강 (formal theory paper 유지)
다음 내용을 추가해야 함:
- POMDP 튜플과 SERVO 튜플(S, G, E, V, M, π) 간 명시적 매핑
- M과 belief b(S)의 수식적 관계 정의
- V(o) → r이 reward function인지 명확화
- Proposition 추가 예시:
  - Prop 1: V_empirical이 calibrated되고 belief update 가능할 때 BED policy는 myopic Bayes-optimal이 됨
  - Prop 2: V_semantic이 biased estimator이면 EIG 기반 정책도 systematic drift 유발
  - Prop 3: M_s가 belief sufficient statistic 미보존 시 policy degradation 발생

### 선택 B: Claim 낮추기 (현실적 선택, 현재 원고에 더 적합)
- "Formalizing" 대신 "A Diagnostic Framework for AI Scientist Systems"에 가깝게 포지셔닝
- POMDP/BED는 "normative lens" 또는 "conceptual grounding"으로 표현
- 현재 원고 내용과 일치하며 수정 비용 낮음

**Codex 권고:** 현재 원고 상태라면 선택 B가 더 현실적.

> **[SUPERSEDED 2026-05-31 → 하이브리드]** 최종 결정은 **선택 A(이론 보강)**. 하이브리드에서 형식화가 엄밀성을 담당하므로 lens 톤다운(선택 B)이 아니라 Prop 1~3 증명을 추가한다. 상단 "전략 확정: 하이브리드" 참조. 아래 선택 A/B 상세는 이력 보존용.

**원고 대조 (영문 main.tex §2 "POMDP Formulation"·§3 BED, L89–109 + Related Work L116):**

| 위치 | 실제 서술 | 리뷰어 지적과의 관계 |
|---|---|---|
| L91 | "maintains a belief state $b(s)$ updated by observations $o$" | belief는 **서술로만** 존재, 갱신 규칙 수식 없음 |
| L94 | `POMDP = (S, A, T, R, Ω, O, γ)` — **7-튜플**, `T: S×A→Δ(S)`, `R: S×A→ℝ`, `O: S×A→Δ(Ω)` 각각 형식 사상 부여 | 리뷰어 "튜플이 reward/transition/observation 누락" 주장은 **틀림** |
| L96 | "departs from standard POMDPs in three ways: (1) R not pre-specified; (2) S unbounded; (3) T non-stationary" | 리뷰어 핵심 지적과 정확히 일치 — 표준 요건을 스스로 위반 선언 |
| L100–107 | BED EIG 수식(eq:eid): θ=parameters, prior/posterior entropy | prior p(θ)·simulator p(y\|θ,d) 명세 없음 — open-ended 적용 조건 미정의 |
| L109 | "no current AI Scientist system explicitly implements EIG-optimal policies" | intractability를 BED-practice gap으로 인정 (선택 B 디딤돌) |
| L116 | "To our knowledge, no prior work explicitly applies BED as a design target..." | **항목 1의 "first" 주장 출처** — hedged지만 리뷰어 표적 |
| L150 | "In the BED interpretation, $\pi^* = \arg\max_d \mathrm{EIG}(d)$" | 규범적 기준은 제시하나 open-ended에서 계산 가능성 미해결 |

**검증 결과 — 항목 2·3과 동일 패턴:**

1. **리뷰어 인용 부분 부정확**: 리뷰어는 원고 튜플을 `(S,A,T,R,Ω,O)`로 인용하고 "일부 요소 누락"이라 했으나, 실제 L94는 γ 포함 7-튜플이며 T/R/O에 형식 사상을 부여한다. 누락된 것은 초기 belief b₀·horizon h뿐 — "reward/transition/observation 누락"은 **틀림**. rebuttal에서 지적 가능.
2. **그러나 substantive 비판은 정당**: 원고가 (a) "Formally ... POMDP"(L94)라 선언하면서 (b) L96에서 표준 POMDP 3대 요건을 스스로 깨고 (c) 깨진 환경에서 belief update·정책이 어떻게 정의되는지 수식으로 제시하지 않는다. 형식이라 부르되 형식적 작업을 안 함 — 리뷰어 핵심 정확.
3. BED도 EIG 수식만 있고 open-ended에서 prior/simulator 조달 방법 부재. "π* = argmax EIG"는 aspiration.

**판정:** 항목 4는 항목 3과 함께 **substantive하게 유효**. 단 "튜플 요소 누락"은 부정확하므로, 저자는 "튜플은 거의 완전(b₀·h만 추가 필요)하나 **비표준 환경의 형식적 처리가 미흡**"으로 정확히 재규정해 대응.

**권장 대응 (선택 B + 부분 선택 A 혼합):**

- L91–94 "Following the POMDP formulation, we model ... as POMDPs" → "we use the POMDP formalism as an **organizing lens**"로 톤 조정. L109의 intractability 인정과 자연 연결.
- L96 직후 1문장 추가: 표준 가정 위반 시 SERVO는 완전한 형식 모델이 아니라 **부분관측 의사결정에서 영감받은 컴포넌트 분해**임을 명시(리뷰어 제안 수용).
- BED: "θ·prior·simulator가 명세 가능한 하위문제에서만 직접 적용, 그 외엔 EIG는 aspiration"으로 적용 범위 한정.
- **항목 1과의 연결**: L116 "no prior work explicitly applies BED as a design target"를 약화하면, BED를 규범적 lens로 낮추는 항목 4 대응과 톤 일치. 두 항목 동시 처리 권장.
- **부분 선택 A(선택적)**: 형식 강도 유지 시 belief b(s)↔M 관계, V(o)→r의 reward 해석만이라도 1개 Proposition으로 명시. 단 현재 원고는 선택 B 중심이 현실적(Codex 판단).

---

## 핵심 전략 재정리

> "우리가 최초로 formalized했다" → "기존 AI Scientist 시스템들을 비교 가능하게 만드는 재현 가능한 진단 좌표계를 제안한다"

이 한 문장의 프레이밍 전환이 4개 비판을 동시에 완화하는 핵심입니다.

**4개 항목 검증 요약 (원고 대조 후):**

| 항목 | substantive 유효성 | 리뷰어 인용 정확성 | 핵심 대응 |
|---|---|---|---|
| 1 독창성 과대주장 | 유효 | — (인용 아님) | "first"(L116) 제거 + 선행 3편 추가 |
| 2 V-completeness 재현성 | **부분 false positive**(표는 소스 존재) + substantive 유효 | 날조 ("without exception" 없음) | systems.csv 빌드 + 표현 약화 |
| 3 Coscientist 오기술 | 유효 | 날조 (verbatim 합성) | loop-none → loop-partial 재코딩 |
| 4 POMDP/BED 미흡 | 유효 | 부분 부정확 ("튜플 누락" 틀림) | POMDP를 lens로 톤 조정 + BED 범위 한정 |

**공통 패턴:** AI 리뷰어가 verbatim "인용"을 반복 날조(항목 2·3)하거나 부정확 기술(항목 4)한다. 저자 rebuttal은 매 항목에서 (a) 인용/사실 오류를 먼저 지적해 리뷰어 신뢰도를 깎고 (b) 그럼에도 정당한 substantive 우려는 수용하는 2단 구성이 최적. 단 substantive 측면은 항목 1·3·4 모두, 항목 2는 부분적으로 유효하므로 실제 수정은 반드시 수행.
