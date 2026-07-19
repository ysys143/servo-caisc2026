# 인용 내용 정합성 리뷰 — 발견 사항 (Findings)

## 요약 (완료: 59/59 논문 전문 정독, 128/128 원자 주장 검증)

verdict 분포: **ACCURATE 97 · IMPRECISE-OK 17 · MISATTRIBUTION 8 · MISCHARACTERIZATION 4 · CONTEXT-MISUSE 1 · OVERCLAIM 1**. 완결성: check.py 4대 불변식 PASS + 독립 재추출 감사 "COVERAGE OK"(누락 0) + Tier-2 grep 재확인.

**수정 권장 FLAGGED (14주장 / 9논문)** — 원고 주장이 실제 논문과 어긋남:

| 심각도 | 인용 | 주장(claim) | 실제 | 권고 수정 |
|---|---|---|---|---|
| HIGH | cheetham2024gnome C099·C100 | "736 realized"를 cheetham에 인용 | 736은 cheetham에 없음(GNoME 출처) | → `\citep{merchant2023gnome}` |
| HIGH | kim2026aireviewers C102 (+ schmidgall C020) | "+2.3점 과대평가"를 kim에 인용 | +2.3은 Agent Laboratory(schmidgall) | kim→`\citep{schmidgall2025agentlab}` |
| HIGH | sparkes2010robot C045·C048 | "능동학습·베이지안 실험선택" | 이 2010 리뷰에 없음(King 2004) | → King et al. 2004 Nature |
| HIGH | sparkes2010robot C047 (OVERCLAIM) | "6요소 전부 + 능동학습" | 리뷰는 ~5요소, 능동학습 미기재 | 완화 |
| HIGH | google2026aletheia C022 | "formal-mathematics agent" | natural-language(원고 L438과 모순) | "natural-language" |
| HIGH | aher2023turing C087·C089 | "circular validity 실패양식" | aher는 외부검증(circular 0회) | 인용 제거/반례로 |
| HIGH | gu2024scimuse C058 | "KG가 생성 품질 향상" | 생성 무차별, KG는 선택 기여 | "선택/흥미순위"로 |
| HIGH | bran2023chemcrow C076 | "beam search + 계산검증" | ReAct + wet-lab 실행 | ChemReasoner와 분리 |
| MED | cranmer2020symbolic C074 | "deterministic search" | stochastic GA/PySR | AI Feynman과 분리 |
| MED | park2023generative C091 | "full-factorial designs" | 단일요인 ablation | 완화/제외 |

**IMPRECISE-OK(참고, 경미 수정)**: szymanski C119(판본/정정→correction 병기), liu2026lasthuman C030(45.4%/90.2% 인용누락+"papers"→"reproduction requirements"), merchant C052·C055(EIG/BED 윤색 완화), taniguchi C064(MH 인용 추가), leiden C106(수치 사실이나 웹 출처 병기).

_아래는 논문별 상세._

---


FLAGGED 주장(부정확·과장·귀속오류·맥락오용)과 권고 수정안을 논문별로 기록한다. 정확(ACCURATE)한 주장은 원장(`ledger.tsv`)에만 남기고 여기엔 문제 항목만 모은다. 각 논문 정독 노트(문제의식·방법·핵심수치·맥락)도 함께 남긴다.

심각도: HIGH(사실오류·귀속오류로 반드시 수정) / MED(과장·부정확, 수정 권장) / LOW(경미).

---

## HIGH (반드시 수정)

### cheetham2024gnome C099(L230)·C100(L444) — MISATTRIBUTION
"only 736 have been independently experimentally realized"를 `\citep{cheetham2024gnome}`에 인용했으나 **736은 cheetham에 없음**(grep 0회). 출처는 **GNoME 본논문(merchant2023gnome)** — merchant 원문 "we found 736 matches, providing experimental confirmation ... lower bound"으로 삼중 확인(cheetham 에이전트 + merchant 에이전트 + 오케스트레이터 grep). 
**Fix**: 736을 `\citep{merchant2023gnome}`로 귀속; cheetham은 "predicted≠validated materials" 정성 주장에만 유지. (단, 736은 저자 합성이 아니라 ICSD 매칭·lower bound이며 184/736만 신규 — 원고가 "independently experimentally realized"라 쓴 것은 원문 표현과 일치하나 뉘앙스 주의.)

### sparkes2010robot — 능동학습·"6요소" MISATTRIBUTION/OVERCLAIM (L85·L92·L94)
sparkes2010robot은 Robot Scientist **리뷰**로, "active learning"·"Bayesian"·"six" 모두 원문 grep **0회**. 능동학습/베이지안 실험선택 메커니즘은 **King et al. 2004 Nature**("Functional genomic hypothesis generation and experimentation by a robot scientist", 427:247-252)에 있고 이 2010 리뷰엔 없음. 원고가 이 리뷰에 귀속한:
- **C045(L85)** "Robot Scientist's experiment selection [as active-learning approximation]" → MISATTRIBUTION
- **C048(L94)** "Bayesian-optimal experiment selection ... the Robot Scientist's active-learning policy" → MISATTRIBUTION (가장 강함)
- **C047(L92)** "instantiating all six SERVO components including an active-learning policy" → OVERCLAIM(리뷰는 ~5요소 나열, 6요소는 원고 프레임; 능동학습 성분 미기재). "more than a decade before LLM systems"는 연대상 OK.
- C046(L92, yeast+가설생성+로봇실험+RF통계검증) ACCURATE, C049(Table1 라벨) ACCURATE.
**Fix**: 능동학습·실험선택·베이지안 관련 주장은 **King et al. 2004 Nature**를 인용하고, sparkes2010robot은 일반 리뷰 인용으로만 유지.

### kim2026aireviewers / schmidgall2025agentlab — "+2.3점" MISATTRIBUTION (L166)
원고 L166: "Agent Laboratory ... documents +2.3-point systematic over-estimation ... ~\citep{kim2026aireviewers}." **문장 내용은 Agent Laboratory(schmidgall)** 것인데 **인용은 kim에 붙음**. 두 블라인드 정독이 독립 교차 확정: schmidgall 원문에 +2.3 실재(자동 리뷰어 6.1/10 vs 인간 PhD 리뷰어 3.8/10, Intro contribution 3·§4.1.1·Fig 6); kim 원문엔 "+2.3" 0회(7,881줄 grep) + Agent Laboratory 미언급. 
**Fix**: `\citep{kim2026aireviewers}` → `\citep{schmidgall2025agentlab}`. (부수: "relative to human PhD students"는 정확히는 "human PhD-student *reviewers* of the AI-generated papers"로, 자기 논문 대비가 아님.)

### google2026aletheia C022(L69) — MISCHARACTERIZATION
원고 L69가 Aletheia를 "**formal**-mathematics agent"로 분류하나, 논문은 Aletheia가 "operates end-to-end in **natural language**"(AlphaProof/AlphaGeometry 같은 formal 시스템과 대비, p.3 l.154-155)라고 명시. Tier-2 grep 확인("revise solutions end-to-end in natural language"). 게다가 **원고 자체가 L176("NL")·L438("natural-language proofs")에서 모순** — 내부 비일관.
**Fix**: L69에서 "formal-mathematics agents (Aletheia)"를 "natural-language mathematics agent"로 수정. formal 예시가 필요하면 AlphaProof/AlphaGeometry를 인용. (C025 "200 audited ... 13(6.5%)"는 ACCURATE — p.9 Table 6, funnel 700→212→200.)

### aher2023turing C087(L200)·C089(L448) — MISATTRIBUTION
원고가 "circular validity 실패양식"(생성기와 시뮬 피험자가 같은 모델→검증기가 외부사실 아닌 자기일관성 측정)을 aher2023에 귀속. 그러나 aher 원문에 'circular'·'self-consistency'·'validator' **각 0회**(grep). aher는 **정반대** — 외부 인간 데이터와 비교 검증(Milgram 26/40 vs 인간 75/100 등). aher가 명시한 위험은 훈련데이터 오염·저자편향뿐. C089의 "validator measures self-consistency not external fact"는 논문과 직접 모순. G/E·identifying-channel 틀은 **원고 자신의 이론**.
**Fix**: C087/C089에서 `\citep{aher2023turing}` 제거하거나, aher를 *외부검증 안전장치(반례)*로 재서술. (aher의 Milgram TE가 한 LM을 피험자+분류기로 쓰긴 하나 논문이 이를 circularity로 문제삼지 않으므로 지지 근거 안 됨.) C088 "full-factorial"은 aher엔 IMPRECISE(일부는 완전교차, Ultimatum은 샘플링) → "systematically crossed/balanced designs"로 완화.

### gu2024scimuse C058(L90) — MISCHARACTERIZATION
원고: "structuring semantic memory as a relational corpus can **substantially improve hypothesis-generation quality**~\citep{gu2024scimuse,lee2025spacer}." — **논문을 뒤집음**. SciMuse는 생성 모드 간(무작위/고임팩트/개념없음) 흥미도 **유의차 없음**(Supp Fig S1: KG 유무로 생성물 유사). KG의 실증 가치는 흥미로운 아이디어의 **선택/예측**(KG 특징만의 지도학습 NN), 생성 품질 향상 아님. 또 측정 구성개념은 자기보고 **interest(1–5)**이지 "quality"/novelty 아님. lee 공동인용도 약함(선험 proxy 지표 + 키워드-임팩트 그래프이지 의미 KG 아님 — lee 판정 대기).
**Fix**: "생성 품질 향상"→"아이디어 **선택**/흥미도 순위 개선"으로 수정. "without closing the loop"는 정확.

### bran2023chemcrow C076(L442) — MISCHARACTERIZATION
원고 L442 "ChemCrow~\citep{bran2023chemcrow} and ChemReasoner~\citep{sprueill2024chemreasoner} validate computationally with surrogate signals and search by **beam**." — 두 시스템을 뭉뚱그렸는데 **ChemCrow에는 둘 다 틀림**: (1) "beam" 원문 0회 — ChemCrow는 **ReAct+MRKL** 반복 CoT(beam은 제3자 RXN4Chemistry 툴 내부에만); (2) "validate computationally with surrogate signals"는 ChemCrow의 **실제 wet-lab 검증**(IBM RoboRXN 4합성 MS확인 + 발색단 측정)과 전문가/EvaluatorGPT 심사를 누락. beam+계산검증 서술은 **ChemReasoner**엔 정확(C078 ACCURATE, GNN 대리+beam width 6).
**Fix**: 두 시스템을 분리하거나 ChemCrow 서술을 교정 — ChemCrow는 ReAct 검색 + 물리 wet-lab 검증 포함.

## MED (수정 권장)

### park2023generative C091(L448) — CONTEXT-MISUSE
원고 L448: "LLM-simulation studies~\citep{aher2023turing,park2023generative} validate with statistical tests over **full-factorial designs**." — park(Generative Agents)에는 안 맞음: park의 통제 평가는 **단일요인 within-subjects ablation**(5조건: full+3 nested ablation+crowdworker) + Kruskal-Wallis(one-way ANOVA 대체)로, DV는 인간 판정 **believability**. "factorial" 원문 0회. full-factorial은 **manning**엔 정확. 
**Fix**: park를 "full-factorial" 그룹에서 빼거나 "statistical tests (ablation + non-parametric significance tests)"로 완화. ("LLM-simulation study"+"statistical tests" 부분은 정확.)
### cranmer2020symbolic C074(L440) — MISCHARACTERIZATION
원고 L440 "AI Feynman와 symbolic-model discovery~\citep{cranmer2020symbolic} fit equations to data with **deterministic search**." — cranmer에는 틀림: SR 엔진이 eureqa/PySR로 **stochastic genetic algorithm**("genetic algorithm to combine algebraic expressions stochastically", L181-183)이고 논문은 "새 SR 기법 아님"이라 명시. "fits equations to data"는 맞음(훈련된 GNN 내부함수에서 기호식 증류). "deterministic"은 **AI Feynman**(brute-force 열거)엔 정확.
**Fix**: 두 인용 분리 — AI Feynman=결정적 열거, cranmer=확률적 기호회귀(유전 알고리즘).

### taniguchi2024cpc C064(L96) — 인용 누락 (IMPRECISE)
"peer review is a Metropolis-Hastings consensus process"는 논문에 실재(MHNG accept/reject, §2.4·§4.1 명시적 MH ratio)하나 원고가 **\citep 없이** 서술. **Fix**: `\citep{taniguchi2024cpc}` 추가(선택적으로 "is"→"is modeled as").

### leiden2026 C106(L211) — provenance (수치는 사실, 출처 문제)
"signed by over 130 mathematicians": 인용된 Zenodo PDF엔 서명자 수 **미기재**(참가자 ~60 + 워킹그룹 16만). 그러나 **Tier-2 웹검증: ">130 signatories by publication" 외부 사실**(Wikipedia·언론; Scholze·Tao·Aaronson 서명). → 수치는 정확, 오류 아님. **Fix(선택)**: 웹 서명자 수를 access-date와 함께 인용하거나 "a broad group of mathematicians"로 완화(PDF엔 수치 없음).

### 조사 결과 (해소됨)
위 aher·gu·cranmer·leiden 모두 확정. 남은 조사: **tobias2025selfdriving** C122 — digest가 "이 리뷰는 하드웨어 급성숙을 문서화하지 않고 오히려 SW/지적 자율성이 preeminent, 하드웨어는 human에게 쉬움이라 주장"이라 경고 → MISCHARACTERIZATION 후보(adjudication 대기).

### liu2026lasthuman C030(L171) — 인용 누락 + 분모 표현 오류
원고 "only 45.4\% of papers fully specify reproduction requirements and 90.2\% of extension cost is failed exploration"는 **인용(\citep) 없음**. 두 수치는 이 논문 것(PaperBench 45.4%, RE-Bench 90.2%)으로 정확 → **\citep{liu2026lasthuman} 추가**. 또 "45.4% of **papers**"는 실제 논문 분모가 "reproduction **requirements**"(8,921건/23편)이므로 "papers"→"reproduction requirements"로 표현 수정.

### szymanski2023alab C119(L234) — 판본/정정 이슈 (Tier-2로 에이전트 판정 뒤집음)
에이전트는 vault PDF 기준 "41/58 → 36/57은 INACCURATE"로 flag. 그러나 오케스트레이터 웹검증 결과 **원고의 "36 of 57"은 2026 Author Correction 반영 수치**(원본 41/58 → 불확정 4 + 오염 1[Zn2Cr3FeO8] 제거 → 36 확정). 정정본이 현재 VoR이므로 **원고 숫자는 유지**(제 이전 41/58→36/57 수정도 옳았음). 
**Fix(권장)**: 2026 Author Correction(doi:10.1038/s41586-025-09992-y)을 병기해 축소 수치를 추적가능하게. **별도 provenance 이슈**: vault PDF가 정정 이전 41/58 eScholarship 판본 → 정정 Nature VoR로 교체 필요(원고 오류 아님).
- 부수 발견(reverse): 74%/78%는 투영치(실제 자율 71%), 레시피 성공 37%(130/355), 성공 41개 중 35개는 능동학습 아닌 문헌기반 레시피 — 원고의 "fixed rule" 특성화는 *검증-승격 결정* 한정으로는 방어 가능하나 능동학습 강조를 과소평가(에이전트: MISCHARACTERIZATION 아님).

### merchant2023gnome C052(L219)·C055(L444) — IMPRECISE-OK (해석적 윤색)
"deep-ensemble uncertainty sampling approximates EIG / uncertainty sampling approximating the BED ideal"는 **원고의 해석적 gloss**. GNoME 실제 획득함수는 안정성/에너지 임계값(50 meV/atom, recall 최대화)이고 딥앙상블(n=10)은 불확실성 *정량화*이지 정보이득 샘플링 아님. 논문은 EIG/BED/expected information gain을 쓰지 않음. 원고가 "partial exception/approximates"로 강하게 헤지해 IMPRECISE-OK 유지하나, 정확히는 완화 표현 권장(MED).

## LOW / ACCURATE (참고)

- **merchant C053/C054**: "380,000 stable"은 원문 381,000의 2-sig-fig 반올림(IMPRECISE-OK). "2.2 million candidate structures"는 원문상 "stable wrt previous work"라 용어 평탄화 뉘앙스(원 후보풀은 >10^9). 둘 다 원문 수치.
- **merchant C050**: "DFT-in-the-loop active learning" — 정확(ACCURATE).
- **lu2024aiscientist (7주장, C009 고의혹→ACCURATE 확정)**: "balanced accuracy 0.65 vs. human 0.66"는 Table 1의 AI(GPT-4o@6) 0.65 / 인간(NeurIPS, Beygelzimer 2021) 0.66 balanced accuracy에 정확히 매핑(Tier-2 grep 확인). digest의 "인간=73%" 우려는 raw accuracy였고 balanced는 0.66 — 오류 아님. 원고는 논문 본문의 "0.65% vs 0.66%" 오타까지 회피. C008 "5-ensemble"도 정확(@6은 임계값, 앙상블=5). C011 "1-10 score"는 IMPRECISE-OK(1-10 실재하나 리뷰어는 하위차원도 출력, 수용 결정만 스칼라 붕괴 — 선택적 정밀화).
- **liu2026lasthuman (7주장, 6 ACCURATE)**: 82.6%(Table 4, 95/115)·orphan 22%(5/23)·"five injection types"(6 scoring dimensions와 구분)·4계층(/logic,/src,/trace,/evidence) 전부 확인.
- **lu2026aiscientist (6주장 전부 통과)**: C016 "balanced accuracy 0.69" **정확**(Table 1 Automated Reviewer BA 0.69±0.04, pre-cutoff). C015 세 계층(replication nodes mean±sd / automated reviewer / ICLR·ICBINB 2025 워크숍 peer review) 실재 확인. reverse(LOW): 두 66% 혼동 위험(원고는 pre-cutoff 0.69 인용, clean post-cutoff는 0.66); "uncalibrated"는 원고 표현이나 Table 1 FPR 0.45–0.52 vs 인간 0.17로 데이터 지지; "most layers in class"는 단일논문서 미검증 교차비교.

## 정독 노트 (논문별 digest는 results/<bibkey>.digest.md)

- cheetham2024gnome(7p): GNoME 비평. 384,870 stable은 "제안 화합물"이지 기능 입증된 "재료" 아님. 736 없음.
- merchant2023gnome(11p, GNoME): 2.2M(prev work 대비 stable), 381,000 updated hull, 421,000 total stable, 736 ICSD 매칭(184 신규), r2SCAN 재검 84%/86.8% 유지. 736 출처 확인.
- szymanski2023alab(13p, A-Lab, vault=41/58 구판본): 41/58(71%), 레시피 37%, ARROWS3 능동학습. 2026 정정으로 36 확정.
- lu2026aiscientist(9p, Nature): Automated Reviewer BA 0.69(pre)/0.66(post-cutoff), FPR 0.45–0.52, 3계층 검증.
- (대기: lu2024aiscientist, google2026aletheia, liu2026lasthuman)
