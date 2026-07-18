# `boiko2023emergent` 전문 인용 감사

## Source Identity

- **Citation key:** `boiko2023emergent`
- **BibTeX:** Daniil A. Boiko, Robert MacKnight, Ben Kline, Gabe Gomes, “Autonomous chemical research with large language models,” *Nature* 624 (2023), 570–578. DOI `10.1038/s41586-023-06792-0`.
- **PDF:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/Boiko 2023 - Autonomous Chemical Research with LLMs.pdf`
- **SHA-256:** `15b340a6fd3cb70ae7f44a96264c051662e4dfd26075604c0c8e94c7c85c959f`
- **`pdfinfo`:** 13 pages, PDF 1.7, title “Autonomous chemical research with large language models,” author metadata “Daniil A. Boiko.”
- **PDF 자체 식별자:** PDF p.1(인쇄면 p.570)에 제목, 저자 4인, DOI, 투고일 2023-04-20, 게재 승인일 2023-10-27, 온라인 출판일 2023-12-20이 명시되어 있다. arXiv 식별자는 PDF와 BibTeX 모두에 없다.
- **Version status:** `exact`. PDF의 제목·저자·연도·저널·권·인쇄면·DOI가 BibTeX와 모두 일치하고, 파일 해시와 페이지 수도 manifest의 값과 일치한다. preprint 동일성 판단이 필요한 경우가 아니다.

## Full-Text Coverage

`pdfinfo`로 13쪽을 확인하고 `pdftotext -layout`으로 전체 및 페이지별 텍스트를 추출한 뒤 PDF p.1부터 p.13까지 순서대로 읽었다. 도표 중심이거나 텍스트 추출이 불완전한 PDF pp.1–2, 5–8, 11–13은 `pdftoppm` 렌더링으로 시각 확인했다. 본문 인쇄면은 PDF pp.1–9가 각각 Nature pp.570–578에 대응하며, PDF p.10은 Data/Code availability와 저자·이해상충 정보, PDF pp.11–13은 Extended Data Figs. 1–3이다.

| PDF page | 읽은 내용 |
|---|---|
| 1 (인쇄면 570) | 초록, LLM·실험실 자동화의 배경, 연구 질문, 6개 과제 개요, Planner 구조 도입 |
| 2 (571) | Fig. 1 전체 아키텍처, `GOOGLE`/`PYTHON`/`DOCUMENTATION`/`EXPERIMENT`, 7개 화합물 합성계획 평가 기준 |
| 3 (572) | Fig. 2 합성계획 결과, web grounding 효과와 실패 사례, documentation search 배경 |
| 4 (573) | Fig. 3 OT-2/ECL 문서 검색, HPLC SLL 실행, cloud-lab 품질관리 한계, 하드웨어 제어 설정 |
| 5 (574) | Fig. 4 liquid-handler/UV–Vis, guiding prompt, Suzuki·Sonogashira 물리 실험, 수동 plate 이동과 제한된 시약 공간 |
| 6 (575) | Fig. 5 reagent 선택·근거·URL 분포·GC–MS 결과, chemical reasoning 및 과거 데이터 기반 후속 행동 문제 설정 |
| 7 (576) | Fig. 6 normalized advantage 식과 최적화 궤적, 두 완전 매핑 반응 데이터셋, 20회 lookup-game 설계 |
| 8 (577) | 최적화 지표·결과·baseline 해석, Discussion의 proof-of-concept/`(semi-)autonomous` 범위, dual-use 논의, 참고문헌 시작 |
| 9 (578) | 참고문헌 17–52, autonomous chemistry와 agent/tool prior work의 출처 관계, 출판자·라이선스 정보 |
| 10 | Data/Code availability, 미공개 데이터·코드·prompt와 재현성 제한, 저자 기여, competing interests, supplement 안내 |
| 11 | Extended Data Fig. 1: 색 식별 실험의 전체 prompt 흐름과 명시적 guiding prompt |
| 12 | Extended Data Fig. 2: Coscientist가 생성한 OT-2 protocol의 labware·reagent transfer·heater-shaker 단계 |
| 13 | Extended Data Fig. 3: 초기 sample 수별 Bayesian optimization 비교와 compound별 advantage 차이 |

감사 범위는 제공된 13쪽짜리 로컬 PDF 전체이다. PDF가 별도 Supplementary Information과 online methods를 가리키지만, 아래 원고 인용 주장들은 이 PDF의 본문·그림·Extended Data만으로 범위와 지지 여부를 판정할 수 있다. supplement에만 있을 수 있는 추가 세부사항은 근거로 간주하지 않았다.

## Problem and Context

논문이 다루는 문제는 강력한 LLM과 laboratory automation을 결합하면 과학자가 자연어로 준 목표에서 출발해 실험을 설계하고, 필요한 정보를 찾고, 계산하고, 실제 장비를 제어하는 agent를 만들 수 있는가이다. 저자들은 이를 세 질문으로 구체화한다: 과학 과정에서 LLM이 무엇을 할 수 있는가, 어느 정도 autonomy가 가능한가, autonomous agent의 결정을 어떻게 이해할 수 있는가(PDF p.1/인쇄면 570).

학문적 맥락은 두 흐름의 결합이다. 하나는 transformer LLM의 자연어·생물학·화학·코드 생성 진전이고, 다른 하나는 autonomous reaction discovery, closed-loop optimization, automated flow system, mobile robotic chemist로 이어진 실험실 자동화 전통이다(PDF pp.1, 9/인쇄면 570, 578). 저자들은 Auto-GPT, BabyAGI, LangChain 같은 contemporaneous autonomous-agent 작업과 독립적·병렬적으로 연구했다고 밝히고, chemistry tool agent인 ChemCrow를 인접 사례로 둔다(PDF pp.1, 9). 따라서 이 논문은 자율 과학 전체의 비교 프레임워크나 최초성 논증이 아니라, GPT-4 기반 단일 화학 연구 agent의 proof of concept와 capability study이다.

선행 chemical automation과 달리 Coscientist의 핵심 기여는 하나의 GPT-4 Planner가 web search, documentation retrieval, code execution, cloud-lab/liquid-handler API를 command action space로 호출하게 만든 점이다. 반대로 전통적 Bayesian optimization과 비교한 최적화 실험은 autonomous discovery의 일반 이론을 제안하지 않고, 기존의 완전 매핑된 반응 데이터에서 LLM이 관측 결과를 다음 선택에 재사용할 수 있는지를 시험한다.

## Structure and Argument

논증은 capability를 단계적으로 쌓는다. 먼저 Fig. 1에서 Planner와 네 command의 모듈 구성을 정의한다. 이어 (1) web-grounded synthesis planning, (2) OT-2와 ECL 문서 검색, (3) 문서에서 ECL SLL code 생성, (4) liquid handler 및 UV–Vis 제어, (5) Suzuki–Miyaura와 Sonogashira 반응의 설계·실행을 차례로 보인다(PDF pp.2–6). 각 단계는 이전 모듈을 더 많이 결합한다.

그 다음 Fig. 6은 물리 실험과 구별되는 lookup-table 최적화 game으로 넘어간다(PDF pp.6–8). 과거 iteration의 yield와 관측을 다음 조건 선택에 제공하여 GPT-4, GPT-3.5, 표준 Bayesian optimization을 비교한다. 마지막 Discussion은 결과를 “proof of concept”와 `(semi-)autonomously`라는 범위로 회수하고, 도구 통합의 잠재력과 dual-use 위험을 함께 논한다(PDF p.8). PDF pp.9–10은 참고문헌·가용성·이해상충, pp.11–13은 주요 실험의 상세 그림과 추가 baseline 분석으로 본문 주장의 조건을 보강한다.

## Methods and Evidence

### 시스템과 도구

- **Planner:** GPT-4 chat-completion instance. 사용자 입력과 command output을 user message로 받고 `GOOGLE`, `PYTHON`, `DOCUMENTATION`, `EXPERIMENT`를 선택한다(PDF pp.1–2).
- **Web searcher:** 별도 LLM이 query를 생성하고 Google Search API 결과와 웹페이지를 탐색한다. 합성계획 benchmark는 7개 화합물, 여러 LLM/검색 조건, 주관적 1–5점 척도를 사용한다(PDF pp.2–3).
- **Documentation searcher:** OT-2 문서 section을 `ada` embedding으로 만들고 distance-based vector search를 수행한다. ECL에서는 114개 experiment function과 1,110개 catalogue sample을 대상으로 prompt-to-function/SLL/sample을 시험한다(PDF p.4).
- **Code execution/automation:** 계산은 격리 Docker container에서 실행하며, 생성 code는 OT-2 Python API 또는 ECL SLL을 통해 장비에 전달된다(PDF pp.2, 4, 12).

### 실험과 데이터

1. **Known-synthesis planning:** 7개 target의 합성 절차를 평가한다. 3점 이상은 chemically correct, 3점 미만은 failure로 정의하지만 label은 본질적으로 주관적이라고 저자들이 인정한다(PDF pp.2–3).
2. **Documentation/API use:** OT-2 heater-shaker와 ECL HPLC function을 검색·요약해 실행 가능한 code를 만든다. ECL 내부 software가 column, mobile phase, gradient 일부를 결정했다(PDF p.4).
3. **Liquid handling/UV–Vis:** 96-well plate 패턴과 미지 색 sample의 위치를 찾는다. 색 문제는 “Think about how would different colors absorb first”라는 guiding prompt가 추가된 뒤 해결됐다(PDF pp.5, 11).
4. **Integrated physical chemistry:** 제한된 source plate에서 Suzuki–Miyaura와 Sonogashira 조건을 선택하고 OT-2 protocol을 실행한다. plate는 사람이 옮겼지만 저자들은 decision-making에는 사람이 개입하지 않았다고 구분한다. 생성 code의 API 오류는 문서 검색 후 수정됐다(PDF pp.5–6, 12).
5. **Iterative optimization:** yield가 모든 조합에 대해 알려진 Suzuki flow와 Buchwald–Hartwig 데이터셋을 lookup table로 사용한다. 최대 20 iterations는 각 공간의 5.2%, 6.9%이며, 일부 GPT-4 조건은 무작위 yield 10개를 prior information으로 받는다(PDF pp.7–8). 이는 새로운 wet-lab measurement를 autonomous하게 획득하는 실험이 아니다.

### 지표와 가정

`normalized advantage`는 현재 yield가 random-strategy 평균보다 나은 정도를 최대-평균 차이로 정규화한다. `normalized maximum advantage`(NMA)는 해당 iteration까지 관측한 최대 advantage이므로 감소할 수 없다(PDF pp.7–8). 최적화 주장은 두 완전 매핑 데이터셋, 고정 iteration budget, lookup된 yield가 정확한 feedback이라는 가정에 의존한다. GPT-4 training data에 해당 데이터셋이 포함됐는지는 알 수 없다.

## Findings

- GPT-4 Web Searcher는 acetaminophen, aspirin, nitroaniline, phenolphthalein의 모든 trial에서 최고점을 받았고, ibuprofen에서 유일하게 최소 acceptable score 3에 도달했다. 반면 ethyl acetate와 benzoic acid에서는 일부 비검색 model보다 낮았다(PDF p.3/인쇄면 572).
- OT-2/ECL 문서 검색에서는 해당 task의 function을 모든 사례에서 올바르게 찾았고, 생성된 HPLC SLL이 ECL에서 실행됐다. 다만 HPLC parameter 일부는 ECL 내부 software가 정했다(PDF p.4/573).
- UV–Vis 색 식별은 성공했지만 guiding prompt가 필요했다(PDF pp.5, 11). 이는 완전 무보조 reasoning 결과가 아니다.
- 물리 cross-coupling에서 target product에 부합하는 GC–MS signal이 Suzuki 9.53 min, Sonogashira 12.92 min에 나타났다(PDF pp.5–6). 그러나 가능한 compound space가 제한됐고 plate 이동은 수동이었다.
- 최적화에서 normalized advantage가 iteration에 따라 증가해 이전 결과를 후속 선택에 재사용했음을 시사한다. GPT-4 두 조건은 해당 비교의 NMA/normalized advantage에서 Bayesian optimization보다 높았지만, 저자들은 exploration/exploitation 차이 때문에 normalized-advantage 궤적 자체가 성능을 대표하지 않을 수 있고 NMA를 봐야 한다고 경고한다(PDF pp.7–8, 13).
- prior yield 10개는 초기 guess를 개선했지만 최종적으로 prior 유무의 GPT-4가 같은 NMA에 수렴했고, derivative에는 유의한 차이가 없었다. compound name과 SMILES 조건의 성능도 유사했다(PDF p.8).

저자들의 가장 강한 결론은 tool access가 GPT-4에 복합 실험 설계·code 생성·부분적 실행 능력을 부여한다는 proof-of-concept이다. “새 발견”의 신뢰성, 일반적인 closed-loop convergence, novelty/significance 판정 능력은 실험하거나 입증하지 않는다.

## Limitations

1. **Semi-autonomy:** Discussion 자체가 시스템을 `(semi-)autonomously` 작동하는 proof of concept로 한정한다(PDF p.8). 물리 실험에서 plate 이동은 수동이고, 저자들이 실험을 감독·수행했으며, GC–MS 분석도 외부 지원을 받았다(PDF pp.5, 10).
2. **Constrained tasks:** cross-coupling 시약 공간은 제한됐고 최적화는 두 historical fully mapped dataset의 lookup game이다. 이는 open-ended hypothesis generation이나 새로운 현상의 discovery가 아니다.
3. **Human/scaffold dependence:** 연구자가 task와 available action space를 설계하고 synthesis answer를 채점했다. UV–Vis 문제는 guiding prompt가 필요했다. novelty와 significance를 system이 독립 판정하는 test는 없다.
4. **평가의 주관성·baseline 조건:** 합성계획 1–5점 label은 주관적이다. GPT-3.5는 JSON schema failure로 관측 수가 적었고, Bayesian optimization과 LLM의 exploration/exploitation 조건이 달라 일부 곡선 비교 해석이 제한된다.
5. **Data contamination:** GPT-4 training data에 반응 데이터셋이 있었는지 불명확하다(PDF p.8).
6. **재현성:** safety를 이유로 full data, code, prompts를 공개하지 않았으며, 공개한 simpler implementation은 같은 결과를 내지 않을 수 있다(PDF p.10). 본 PDF가 가리키는 supplement와 online methods도 현재 로컬 감사 자료에는 포함되지 않았다.
7. **정보원 품질:** Web Searcher URL의 약 절반이 Wikipedia였고, 검색 grounding이 hallucination을 줄였어도 source quality를 보증하지 않는다(PDF pp.5–6).
8. **일반화·인과:** capability demonstration은 6개 task와 특정 GPT-4/tool stack에 국한된다. validator reliability가 closed-loop feasibility를 인과적으로 결정한다거나 AI Scientist 분야 전체가 특정 방향으로 진화한다는 결론을 이 논문 단독으로 도출할 수 없다.

SERVO에 대한 함의는 저자 주장과 분리해야 한다. **감사자의 해석으로서**, Coscientist는 `G`(Planner), `E`(검색·code·hardware), 제한된 `π`(다음 조건 선택), task outcome feedback을 한 pipeline에 넣는 사례다. 그러나 physical execution의 성공, computational feedback의 순환, trustworthy novelty/significance validation은 서로 다르다는 SERVO의 구분을 오히려 필요로 한다. 이 논문은 그 구분에 맞춰 코딩할 사례를 제공하지만 SERVO framework, validator-completeness 가설, POMDP/BED mapping 자체를 검증하지는 않는다.

## Citation Assessments

### `EN-C001:boiko2023emergent`

- **원고 위치:** `main.tex:69`, Introduction.
- **실제 주장:** “AI Scientist systems”를 독립적으로 hypothesis 생성·experiment 실행·knowledge synthesis를 하는 agent로 정의하고, 이들이 빠르게 proliferate했으며 공통 formal vocabulary가 없다고 말한다.
- **Citation role:** `joint`. 여섯 출처 중 하나로 field-level 배경 주장에 결합되어 있다. 이 출처의 기여는 `joint-only`이다.
- **PDF 근거:** PDF p.1/570은 Coscientist가 “designs, plans and performs complex experiments”하고 검색·code·automation tool을 쓴다고 보고하며 6개 task를 열거한다. Discussion은 이를 `(semi-)autonomous` proof of concept로 한정한다(PDF p.8/577).
- **판정:** `PARTIAL`; severity `minor`.
- **이유:** 이 논문은 2023년의 관련 agent 한 사례와 design/execution capability는 직접 지지한다. 그러나 Coscientist가 독립적으로 open-ended hypothesis를 생성하거나 knowledge를 synthesis해 과학적 결론을 갱신했다고 입증하지 않는다. 단일 시스템 논문은 field가 “proliferated rapidly”했다는 추세나 “공통 formal vocabulary가 없다”는 부재 주장도 독립적으로 확립할 수 없다. 후자는 source silence가 아니라 원고의 literature synthesis로 표시해야 한다. 정량 수치는 없어 quantitative mismatch는 없다.
- **권고 수정:** “Recent systems automate different parts of scientific research, including tool-augmented experimental design and execution”처럼 관측 가능한 범위로 낮추고 복수 출처를 붙인 뒤, 공통 vocabulary의 부재는 “we find”라는 원고의 조사 결론으로 분리한다.
- **Korean parity:** `equivalent` with `KO-C001:boiko2023emergent` for the cited field-level claim. 한국어도 같은 과장과 같은 qualification 필요성을 보존한다.

### `EN-C002:boiko2023emergent`

- **원고 위치:** `main.tex:69`, Introduction.
- **실제 주장:** 시스템 범위의 한 끝을 “tool-augmented synthesis agents (Coscientist)”로 예시한다.
- **Citation role:** `example`.
- **PDF 근거:** PDF pp.1–2/570–571은 Coscientist를 GPT-4 Planner가 web/document search, Docker code execution, ECL/OT-2 automation을 호출하는 multi-LLM agent로 정의한다. PDF pp.3–6은 synthesis planning과 실제 cross-coupling 설계·실행을 보인다.
- **판정:** `SUPPORTED`; severity `none`.
- **이유:** “tool-augmented”와 chemical “synthesis agent”라는 요약은 구조와 task에 정확히 부합한다. 이를 general knowledge-synthesis agent라는 뜻으로 읽지만 않으면 scope와 attribution이 정확하다.
- **권고 수정:** 없음. 모호성을 줄이려면 “tool-augmented chemical-synthesis and experimentation agent”라고 쓸 수 있다.
- **Korean parity:** `omitted`. `main_ko.tex:88`은 영어의 Coscientist 구체 예시를 번역하지 않아 이 직접적이고 정확한 source use가 한국어 서론에는 없다.

### `EN-C013:boiko2023emergent`

- **원고 위치:** `main.tex:90`, Related Work.
- **실제 주장:** 네 선행 연구가 개별 시스템의 qualitative characterization은 제공하지만 cross-system comparison을 위한 shared framework는 제공하지 않는다고 말한다.
- **Citation role:** `joint`; 이 출처는 개별-system 부분에 직접 기여하고 부재 결론에는 `joint-only`인 문헌 종합 자료다.
- **PDF 근거:** PDF pp.1–8은 Coscientist 한 시스템의 architecture, task별 experiment, optimization, limitation을 상세히 기술한다. 논문의 목적과 구조에는 여러 AI Scientist system을 공통 축으로 비교하는 framework가 없다.
- **판정:** `PARTIAL`; severity `minor`.
- **이유:** “individual system characterization”은 직접 지지된다. 그러나 해당 논문에 비교 framework가 없다는 관찰은 “분야 전체에 shared framework가 없다”는 universal absence claim을 entail하지 않는다. 그 결론은 네 논문의 침묵이 아니라 원고 저자들의 명시적 review 방법과 범위에 의해 뒷받침되어야 한다.
- **권고 수정:** “These works characterize individual systems. In our review of this set, we did not identify a shared cross-system framework”처럼 source-backed 사실과 manuscript interpretation을 두 문장으로 분리한다.
- **Korean parity:** `equivalent` with `KO-C008:boiko2023emergent`. 의미·강도·부재 주장의 문제까지 동일하다.

### `EN-C026:boiko2023emergent`

- **원고 위치:** `main.tex:166`, Analysis of Core AI Scientist Systems.
- **실제 주장:** Coscientist에서는 measured outcome이 later choice를 알리는 constrained task-level feedback만 있고, loop는 partial이며 novelty/significance validation은 human-mediated라고 SERVO로 분류한다.
- **Citation role:** `interpretive`.
- **PDF 근거:** PDF p.6/575는 “previously collected data to guide future actions”를 reasoning test로 제시한다. PDF pp.7–8/576–577의 최적화 game은 매 iteration의 yield/observation을 다음 condition 선택에 제공하고, normalized advantage 증가를 정보 재사용의 증거로 해석한다. 동시에 20 iterations, 두 fully mapped lookup table, 인간이 설계한 task라는 제약이 있다. 물리 cross-coupling은 plate 이동이 수동이고 결과 GC–MS가 실험 후 분석됐으며(PDF pp.5–6), Discussion은 전체를 `(semi-)autonomous` proof of concept로 부른다(PDF p.8).
- **판정:** `SUPPORTED_WITH_QUALIFICATION`; severity `minor`.
- **이유:** “measured outcomes inform later choices”는 **bounded lookup-table optimization task**에 직접 맞는다. 이를 physical wet-lab feedback loop 일반으로 읽으면 과장이다. `partial loop`는 충실한 SERVO interpretation이지만 source의 용어는 아니다. novelty/significance를 Coscientist가 자동 검증하지 않는 것은 architecture와 task에서 확인되지만, 논문은 그 판단을 “human-mediated validator”로 명시하거나 calibration을 평가하지 않는다. 따라서 부재/인간 의존을 framework coding으로 표시해야지 직접 측정 결과처럼 쓰면 안 된다.
- **권고 수정:** “In a bounded lookup-table optimization task, measured yields informed subsequent choices; physical experiments and novelty/significance assessment did not form an autonomous validated loop”로 feedback의 실험 조건과 interpretive status를 명시한다.
- **Korean parity:** `meaning_shifted` relative to the closest occurrence `KO-C022:boiko2023emergent`. 한국어는 이 Coscientist-specific feedback/partial-loop 근거를 생략하고 cohort-level framework 적용과 validator 공변 관계로 바꾼다.

### `KO-C001:boiko2023emergent`

- **원고 위치:** `main_ko.tex:88`, 서론.
- **실제 주장:** AI 과학자 시스템을 독립적 가설 생성·실험 실행·지식 합성 agent로 정의하고 그 수가 급속히 증가했으나 공통 형식 어휘가 없다고 말한다.
- **Citation role:** `joint`; 이 출처의 기여는 `joint-only`이다.
- **PDF 근거:** PDF p.1/570의 단일 Coscientist 사례는 설계·계획·실행과 tool use를 지지하고, PDF p.8/577은 semi-autonomous proof of concept라고 범위를 제한한다.
- **판정:** `PARTIAL`; severity `minor`.
- **이유:** `EN-C001`과 동일하다. 한 source는 한 사례와 일부 capability만 지지하며 rapid proliferation, 모든 정의 요소, field-level vocabulary 부재를 독립적으로 확립하지 않는다.
- **권고 수정:** 영어 권고와 동일하게 capability 사례와 원고의 literature-synthesis 결론을 분리한다.
- **Korean parity:** `equivalent` with `EN-C001:boiko2023emergent`.

### `KO-C008:boiko2023emergent`

- **원고 위치:** `main_ko.tex:109`, 관련 연구.
- **실제 주장:** 선행 연구가 개별 시스템의 정성적 특성화는 제공하지만 교차 시스템 비교 공통 framework는 없다고 말한다.
- **Citation role:** `joint`.
- **PDF 근거:** PDF pp.1–8은 Coscientist 단일-system characterization을 제공하지만 field-wide framework 부재를 조사하거나 주장하지 않는다.
- **판정:** `PARTIAL`; severity `minor`.
- **이유:** 개별-system 절은 supported이나 universal absence 절은 이 source로 assess할 수 없는 원고 종합이다. source silence를 부재 증거로 사용할 수 없다.
- **권고 수정:** “이 연구들은 개별 시스템을 특성화한다. 본 논문의 검토 범위에서는 공통 비교 framework를 확인하지 못했다”로 분리한다.
- **Korean parity:** `equivalent` with `EN-C013:boiko2023emergent`.

### `KO-C022:boiko2023emergent`

- **원고 위치:** `main_ko.tex:195`, 핵심 AI 과학자 시스템 분석.
- **실제 주장:** SERVO를 Coscientist를 포함한 네 end-to-end system과 한 artifact-infrastructure proposal에 적용하며, 작은 표본에서 closed-loop system은 더 완전한 validator와 함께 `G`·`E`·`π`도 발전시켰다고 요약한다.
- **Citation role:** `joint`. Boiko et al.은 네 system 중 Coscientist 한 사례만 담당하므로 cross-system 결론에는 `joint-only`이다.
- **PDF 근거:** PDF pp.1–6은 자연어 목표에서 검색·계산·protocol 생성·hardware 실행까지 이어지는 task-spanning pipeline을 보인다. 그러나 저자들은 `(semi-)autonomous` proof of concept라고 명시하고(PDF p.8), 수동 plate 이동, guiding prompt, 외부 분석, lookup-table feedback을 보고한다. validator completeness나 네-system 공변 관계는 분석하지 않는다.
- **판정:** `SUPPORTED_WITH_QUALIFICATION`; severity `minor`.
- **이유:** Coscientist를 SERVO 분석 대상인 broad pipeline system으로 포함하는 것은 타당하다. 다만 “end-to-end”는 bounded task execution이라는 뜻으로만 지지되며 autonomous hypothesis-to-novelty-validation loop라는 뜻은 아니다. 뒤의 validator/closed-loop 공변 관계는 원고의 cross-system interpretation이지 Boiko et al.의 결과가 아니다.
- **권고 수정:** “네 task-spanning system에 적용한다. Coscientist의 물리 경로는 semi-autonomous이고 novelty/significance gate는 연구 범위 밖이다”라는 qualifier를 표 또는 본문에 둔다.
- **Korean parity:** `meaning_shifted` relative to `EN-C026:boiko2023emergent`: aggregate 경향은 남지만 영어의 measured-outcome 조건과 Coscientist-specific partial-loop 판정은 사라지고, 영어에 없는 framework-application 문장이 추가되었다.

## Korean Parity

| English occurrence | Korean occurrence | Parity | 감사 결과 |
|---|---|---|---|
| `EN-C001:boiko2023emergent` | `KO-C001:boiko2023emergent` | `equivalent` | field-level proliferation/정의/공통어휘 주장의 강도와 source 한계가 동일하다. |
| `EN-C002:boiko2023emergent` | 없음 | `omitted` | 영어의 정확한 Coscientist tool-augmented synthesis 예시가 한국어 서론에서 삭제됐다. |
| `EN-C013:boiko2023emergent` | `KO-C008:boiko2023emergent` | `equivalent` | 개별-system 지지와 shared-framework 부재의 manuscript synthesis가 동일하게 번역됐다. |
| `EN-C026:boiko2023emergent` | `KO-C022:boiko2023emergent` | `meaning_shifted` | 한국어는 bounded feedback과 partial loop의 구체 근거 대신 framework 적용과 cohort-level validator 관계를 제시한다. |

한국어만의 source key 추가는 없지만 `KO-C022`는 영어 대응문을 단순 번역한 것이 아니다. 두 언어를 동등한 manuscript로 유지하려면 영어의 “bounded lookup-table feedback” qualifier와 한국어의 “semi-autonomous/task-spanning” qualifier를 양쪽에 모두 반영해야 한다.

## Frozen Supplementary Description Assessment

- **“A large-language-model-driven agent that plans and executes chemistry experiments.” — `SUPPORTED_WITH_QUALIFICATION`.** Coscientist는 GPT-4 Planner가 실험을 설계·계획하고 tool command를 호출하는 agent이며(PDF pp.1–2), 실제 Suzuki–Miyaura·Sonogashira protocol을 설계하고 OT-2에서 실행했다(PDF pp.5–6, 12). 다만 저자들은 전체를 `(semi-)autonomous` proof of concept로 한정하고, 물리 plate 이동은 사람이 수행했다고 명시한다(PDF pp.5, 8).
- **문서 검색·code 작성/실행·robotic/analytical platform 조작 — `SUPPORTED_WITH_QUALIFICATION`.** documentation retrieval, Docker code execution, OT-2/ECL API 호출은 architecture와 실험으로 직접 확인된다(PDF pp.2, 4–6, 11–12). 그러나 OT-2에서 수행한 물리 cross-coupling(PDF pp.5–6)과 두 fully mapped historical dataset을 이용한 별도 optimization game(PDF pp.7–8)은 같은 live robotic loop가 아니다. UV–Vis toy task는 agent가 plate-reader output을 분석했지만(PDF pp.5, 11), cross-coupling의 사후 GC–MS characterization은 agent-controlled analytical loop로 제시되지 않는다(PDF pp.5–6, 10).
- **“measured reaction yields to inform subsequent choices” — `SUPPORTED_WITH_QUALIFICATION`.** 이전 iteration의 yield가 다음 조건 선택에 제공되고 normalized advantage의 증가가 정보 재사용을 시사한다(PDF pp.7–8). 그 yield는 새 wet-lab measurement가 아니라, yield가 모든 조합에 대해 이미 알려진 두 dataset에서 조회한 값이며 최대 20회짜리 game에 한정된다.
- **인간의 분석·최종 과학 판단(특히 novelty) — `PARTIAL`.** 저자들은 chemistry experiments를 감독하고, 외부 group의 GC–MS 분석 지원을 받아 결과를 해석했으며, 논문 정보와 결론을 인간 저자들이 검증했다(PDF pp.5–6, 8, 10). 반면 novelty를 별도 기준으로 평가했다거나 인간 validator가 formal novelty decision을 수행했다는 절차는 보고하지 않는다.
- **자율 novelty 인증 부재 — `SUPPORTED_WITH_QUALIFICATION`.** architecture, 여섯 task, 결과에는 autonomous novelty-assessment/certification stage가 기술되거나 평가되지 않는다(PDF pp.1–8). 이는 논문이 직접 선언한 novelty 결과가 아니라 감사자가 연구 범위에서 확인한 부재로 표현해야 한다.

**Frozen description verdict:** `minor_revision`. 시스템의 도구 사용과 bounded feedback이라는 골격은 맞지만, 물리 실행과 offline lookup optimization을 분리하고 novelty에 관한 직접 보고와 감사 해석을 구별해야 한다.

**Corrected description:**

> A GPT-4-driven agent that plans chemistry tasks, searches the web and technical documentation, writes and runs code, and invokes laboratory-automation APIs. In constrained demonstrations, it generated and executed liquid-handler protocols for Suzuki–Miyaura and Sonogashira reactions, with manual plate transfers, and separately used yields retrieved from two fully mapped historical reaction datasets to choose subsequent conditions in a bounded optimization game. Human researchers supervised the physical experiments, obtained or interpreted the subsequent GC–MS characterization, and verified the scientific conclusions. The paper does not describe or evaluate an autonomous novelty-assessment or certification stage.

## Overall Verdict

**Overall verdict: `minor_revision`.**

BibTeX와 PDF identity는 정확하고, Coscientist를 tool-augmented chemical research agent로 드는 핵심 예시는 직접 지지된다. 모든 occurrence가 관련 없는 source를 인용한 것은 아니므로 `citation_invalid`는 아니다. 다만 field-wide proliferation과 shared-framework 부재는 이 단일 source가 직접 entail하지 않으며, Coscientist의 outcome feedback은 두 fully mapped dataset의 bounded lookup game에 한정된다. `partial loop`, human-mediated novelty/significance, validator completeness는 합리적인 SERVO 해석이지만 source 저자의 직접 결과와 구별되어야 한다.

수정 우선순위는 (1) `EN/KO-C001`과 `EN-C013/KO-C008`에서 source fact와 manuscript literature synthesis 분리, (2) `EN-C026`에 lookup-table 조건 명시, (3) `KO-C022`와 영어 사이의 meaning shift 해소이다. 현재 정량 claim의 숫자 오류나 DOI/저자 오귀속은 없다.

## Completion Checklist

- [x] RUBRIC의 필수 heading 11개를 모두 사용했다.
- [x] PDF/BibTeX/manifest로 source identity, SHA-256, DOI, page count, version status를 확인했다.
- [x] 로컬 PDF 13쪽을 p.1부터 p.13까지 순서대로 모두 읽었다.
- [x] 관련 architecture, physical experiment, optimization equation/plots, Extended Data를 시각 확인했다.
- [x] 연구 문제, 맥락, prior work, 구조, methods/data/assumptions, 결과, 한계, SERVO 함의를 구분해 기술했다.
- [x] manifest의 EN link 4개와 KO link 3개를 각각 독립적으로 판정했다.
- [x] multi-key citation의 source-independent support와 `joint-only` 범위를 구분했다.
- [x] 영어·한국어 parity를 `equivalent`, `omitted`, `meaning_shifted`로 대조했다.
- [x] source author claim과 manuscript/SERVO interpretation을 분리했다.
- [x] terminal marker의 page range와 link ID를 manifest와 대조했다.

AUDIT_COMPLETE: yes
PAGES_COVERED: 1-13
EN_LINKS_COVERED: EN-C001:boiko2023emergent, EN-C002:boiko2023emergent, EN-C013:boiko2023emergent, EN-C026:boiko2023emergent
KO_LINKS_COVERED: KO-C001:boiko2023emergent, KO-C008:boiko2023emergent, KO-C022:boiko2023emergent
SYSTEM_DESCRIPTION_ASSESSED: yes
VERDICT: minor_revision
