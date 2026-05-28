# Paper 2 — 프로젝트 컨텍스트

## 1. 프로젝트 취지

본 프로젝트는 paper_1("Formalizing AI Scientist Systems")의 핵심 주장 중 하나를 실험적으로 검증하기 위해 시작됐다.

paper_1은 AI Scientist 시스템을 S,G,E,V,M,π 프레임워크로 분석하고, 세 가지 미해결 과제를 제시한다. 그 중 **Open Problem 1**은 다음과 같다:

> "참신성 평가는 자동화될 수 없다. 다층적 자동화 프록시에도 불구하고 인간 판단에 여전히 의존한다."

paper_1에서 이 주장은 이론적 분석과 문헌 검토에 근거한다. paper_2의 목적은 이 주장을 **시뮬레이션 실험으로 직접 검증**하는 것이다.

핵심 테제: **참신성은 가설의 내재적 속성이 아니라 연구공동체의 집단적 판단(community arbitration)에서 창발하는 사회적 속성이다.** 따라서 고립된 에이전트(혹은 자동화된 시스템)는 지역 메모리만으로 전역적 참신성을 신뢰성 있게 평가할 수 없다.

---

## 2. 학회 정보 — CAISc 2026

| 항목 | 내용 |
|------|------|
| 이름 | Conference for AI Scientists (CAISc 2026) |
| 형식 | 온라인 학술대회 |
| 일정 | 2026년 7월 24–25일 |
| 제출 마감 | 2026년 5월 31일 23:59 AoE |
| 사이트 | https://caisc2026.github.io/ |
| 투고 플랫폼 | OpenReview (이중 맹검) |
| 분량 | 최대 8페이지 (참고문헌·체크리스트 제외) |
| 템플릿 | NeurIPS 2024 스타일 (공식 Overleaf 제공) |

**대회 취지:**  
AI 시스템을 단순 분석 도구가 아닌 과학 발견의 적극적 기여자로 인정하는 최초 유형의 학술대회. 주요 저자가 AI이거나, 아이디어 생성~원고 작성의 상당 부분을 AI가 수행한 논문을 대상으로 한다.

**트랙:**
- Track 1 (Verifiable Problems): 자동 검증 가능한 지정 문제
- Track 2 (Open-Ended Problems): 이론적 발전, 실험, 방법론 혁신

**본 논문 대상 트랙:** Track 2

**시상:**  
Spotlight — Anthropic + OpenAI $15,000 모델 크레딧 + Jarvis Labs $7,500 컴퓨팅 크레딧

---

## 3. 기본 아이디어

### 출발점

paper_1에서 검증기(V)의 최상층인 V_human은 "연구공동체가 가설의 위치를 인식론적 공간에서 집단적으로 결정하는 과정"으로 정의된다. 이 층은 현재 어떤 AI Scientist 시스템도 자동화하지 못했다.

기존 주장 방식: 문헌 검토를 통한 논증.  
우리의 방식: **에이전트 시뮬레이션을 통한 직접 검증.**

### 핵심 질문

> 지역 메모리(M_s)를 가진 에이전트가 전역적 참신성을 얼마나 정확히 판단할 수 있는가?  
> 이 정확도는 커뮤니티 연결 구조(topology)에 얼마나 의존하는가?

### 가설

- **H1:** 고립된 에이전트는 자신이 모르는 것을 모두 "참신하다"고 판단 → 허위 참신성 비율이 매우 높다.
- **H2:** 소셜 네트워크 연결이 늘수록 허위 참신성 비율이 감소한다 (비선형적으로).
- **H3:** 완전 공유(shared memory) 상태에서는 반대로 진짜 참신한 것도 "이미 알려진 것"으로 판단된다 (recall↓).
- **H4:** 개별 분류기 정확도(classifier_accuracy)가 높아져도 topology 효과보다 영향이 작다 → 커뮤니티 구조가 지배적 변수.

### 초기 실험 결과 (pilot)

| 토폴로지 | FNR | True Recall |
|---------|-----|-------------|
| isolated | ~0.96 | ~0.98 |
| lattice | ~0.27 | ~0.43 |
| small_world | ~0.04 | ~0.12 |
| shared | ~0.003 | ~0.007 |

H1–H4 모두 초기 결과에서 지지됨. classifier_accuracy(0.6→0.9) 변화의 효과는 topology 변화보다 훨씬 작음.

### paper_1과의 관계

현재 논의 중인 방향:
- **옵션 A:** paper_2로 독립 제출 (시뮬레이션 심화)
- **옵션 B:** paper_1의 실험 섹션으로 통합 (Open Problem 1 직접 검증)
- **옵션 C:** 이번 마감에는 paper_1만 내고 paper_2는 다음 기회로

---

## 4. MiroFish

### 개요

MiroFish는 2026년 1월 공개된 오픈소스 다중 에이전트 예측 시뮬레이션 엔진이다. CAMEL AI의 OASIS 프레임워크를 기반으로 하며, 수천 개의 LLM 에이전트가 각자 개성·장기 메모리·행동 논리를 가지고 상호작용하며 창발적 패턴을 만든다.

- GitHub: https://github.com/nikmcfly/MiroFish-Offline (Offline/로컬 포크)
- 공식: https://evermx.com/open-source/mirofish-swarm-intelligence-ai-simulation-prediction-engine
- Stack: Python 3.11–3.12 + Vue.js + Neo4j + Ollama

### 왜 MiroFish인가

본 실험의 핵심은 **지식이 분산된 커뮤니티에서 창발하는 합의 과정**이다. 이는 MiroFish가 설계된 핵심 유스케이스와 정확히 일치한다:

- 에이전트별 독립적 메모리 → 지식 분산 구현
- 신뢰 네트워크 기반 소통 → topology 변수 구현
- 사회적 영향 및 의견 전파 → V_human 창발 동역학 구현
- 이벤트 주입(hypothesis submission) → AI Scientist 출력 시뮬레이션

### 현재 구현 상태

현재 `src/simulation.py`는 MiroFish의 핵심 아이디어를 **경량 Python으로 직접 구현**한 버전이다 (networkx + numpy, LLM 불필요). MiroFish 실제 엔진을 연결하면 에이전트에 LLM 개성과 메모리를 부여해 더 현실적인 시뮬레이션이 가능하다.

**단계별 계획:**
1. 현재 경량 버전으로 기본 실험 완료 → 논문에 결과 포함
2. (선택) MiroFish 실제 엔진으로 LLM 에이전트 버전 구현 → 심화 버전

---

## 5. 다음 단계

- [ ] 실험 파라미터 스윕 확대 (n_reviewers, n_hypotheses 변화)
- [ ] human_oracle 조건 추가 실험
- [ ] 결과 시각화 (topology별 FNR 곡선)
- [ ] paper_1 통합 vs. 독립 제출 결정
- [ ] 체크리스트 작성
