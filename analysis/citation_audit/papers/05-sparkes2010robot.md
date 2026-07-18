# `sparkes2010robot` 전문 인용 감사

## Source Identity

- **Citation key:** `sparkes2010robot`
- **BibTeX:** Andrew Sparkes, Wayne Aubrey, Emma Byrne, Amanda Clare, Muhammed N. Khan, Maria Liakata, Magdalena Markham, Jem Rowland, Larisa N. Soldatova, Kenneth E. Whelan, Michael Young, and Ross D. King, "Towards Robot Scientists for autonomous scientific discovery," *Automated Experimentation* 2(1):1 (2010), DOI `10.1186/1759-4499-2-1`.
- **PDF 자체 식별:** 표제, 12인 저자, journal, volume/article number, 2010년, DOI가 `references.bib`와 일치한다(PDF pp.1, 10-11).
- **문서 유형:** 원 논문 제목 위에 `REVIEW`라고 명시된 review article이다(PDF p.1). Adam의 핵심 20개 가설 및 12개 확인 결과는 이 review가 요약하며, 상세 primary result는 이 논문의 reference [24]인 King et al., *Science* 2009에 귀속한다(PDF pp.5-6, 10).
- **절대 PDF 경로:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Reference/Sparkes 2010 - Towards Robot Scientists for Autonomous Scientific Discovery.pdf`
- **SHA-256:** `0838ce55a216d3b5ba46b3bedb5e85194ed056dc98e5909630264f63066692cd`
- **`pdfinfo`:** 11 pages, 595 x 794 pt, 1,776,319 bytes, PDF 1.4, not encrypted.
- **Stable identifier:** DOI `10.1186/1759-4499-2-1`; published 2010-01-04(PDF pp.10-11).
- **Version status:** `exact`. PDF의 bibliographic identity, DOI, 11쪽 구성, hash와 manifest가 모두 일치한다.

## Full-Text Coverage

지정된 로컬 PDF p.1부터 p.11까지 page break를 유지한 layout-preserving text로 순서대로 읽었다. 인쇄 쪽 번호와 PDF 쪽 번호는 일치한다.

| PDF 페이지 | 순차 독해 내용 |
|---|---|
| 1 | 표제, 저자, 초록, Robot Scientist 정의, 자동 과학의 역사적 도입 |
| 2 | DENDRAL부터 data-driven discovery까지의 선행연구, 자동화 장비, 형식 기록, closed-loop learning |
| 3 | Robot Scientist 개념, Adam/Eve의 상태, Adam의 두 수준 가설과 Figure 1 |
| 4 | Figure 2, Adam의 two-factor assay, 실제 robot hardware, OD 595 nm 성장 측정, 통계 분석, human-input 경계 |
| 5 | Figure 3, 가설 생성 절차, Latin-square layout, cubic spline/random forest 분석, 20개 가설과 12개 확인 결과의 시작 |
| 6 | Adam 결과의 나머지, 3개 수동 실험과 6개 문헌 근거, YIL033C 오류, LABORS/EXACT 형식화, 개발 중인 Eve |
| 7 | Figure 4, Eve 장비, 계획된 mass screen, verification, targeted screening software |
| 8 | Figure 5, Eve의 계획된 반복 screening, Adam/Eve 연동의 미래 계획, discussion 시작 |
| 9 | 독립성, 혁신성, database/model error, 측정 오류, hardware fault, 비용 한계, 결론과 appendix 시작 |
| 10 | appendix, competing interests, author contributions, acknowledgements, references 1-32 |
| 11 | references 33-39와 DOI/citation metadata |

PDF pp.1, 3-9를 160 dpi PNG로 렌더링해 시각 확인했다. Figure 1은 system model, hypothesis generation, experiment generation/design, robotic execution, observation, statistical/ML analysis, new knowledge, model update의 closed loop를 보여준다(PDF p.3). Figures 2-3은 Adam의 실제 장비와 세 robot arm, plate reader 등 배치를 보여주고(PDF pp.4-5), Figures 4-5는 Eve의 실제 장비와 배치를 보여준다(PDF pp.7-8). PDF에는 표나 수학식이 없으며, p.3의 두 logical predicate와 p.5의 ORF-to-E.C. mapping은 렌더링에서 정상적으로 확인했다. PDF pp.5-6의 결과 문단과 p.9의 한계/결론도 렌더링과 추출문을 교차 대조했다.

외부 웹사이트와 reference [23], [24]의 원문은 열지 않았다. 이 감사는 지정된 Sparkes et al. PDF가 원고의 각 주장을 직접 뒷받침하는지를 판정한다. 논문이 실험 설계 세부를 웹사이트나 다른 논문으로 넘긴 경우, 그 세부는 이 source의 직접 근거로 간주하지 않았다.

## Problem and Context

논문의 문제의식은 과학 자동화가 주로 물리적 실행이나 일부 계산 단계에 머물고, 가설 생성, 실험 설계, 물리적 실행, 결과 해석과 학습을 하나의 반복 주기로 연결하지 못했다는 데 있다(PDF pp.1-3). 저자들은 이 간극을 메우는 Robot Scientist를 AI, 계산 모델, 자동화 장비, laboratory robotics, closed-loop learning과 과학 기록의 논리적 형식화를 결합한 시스템으로 정의한다.

역사적 맥락에서 논문은 DENDRAL/Meta-DENDRAL, AM/EURISKO, KEKADA, BACON 계열과 natural-law discovery를 검토한다(PDF pp.1-2). 이 선행 시스템들은 구조 추론, 가설 생성 또는 법칙 발견의 일부를 자동화했지만, 대체로 직접 실험을 설계하고 실행한 뒤 결과를 모델로 되돌리는 물리적 loop를 닫지 못했다. Robot Scientist의 차별점은 지능적 추론과 laboratory automation을 같은 주기에 넣는 데 있다(PDF pp.2-3).

이 논문은 동시에 재현성 문제를 핵심 동기로 둔다. 모든 goal, hypothesis, protocol, observation, conclusion과 metadata를 형식 언어로 기록하면 실험의 이유와 절차를 재사용하고 재현할 수 있다고 주장한다(PDF pp.2-3, 6). Adam의 data와 metadata는 MySQL과 LABORS/EXACT/EXPO 계열 ontology, Datalog representation으로 기록되었다(PDF pp.5-6).

Adam과 Eve의 증거 상태는 구분해야 한다. Adam은 2005년 말 물리적으로 commissioned되어 효모 기능유전체학의 실제 실험과 결과를 보고한 prototype이다(PDF pp.3-6). Eve는 2009년 초 물리적으로 commissioned되었지만 software와 biological assays가 아직 개발 중이며, drug-screening loop 대부분은 `will`이라는 미래형으로 기술된다(PDF pp.6-8). 따라서 본 원고의 효모 wet-lab 주장은 Adam으로만 지지되고, Eve의 planned capabilities를 실증 결과로 합쳐서는 안 된다.

## Structure and Argument

문서의 논증은 다음과 같이 전개된다.

1. PDF pp.1-2는 자동 과학의 역사와 기존 partial automation을 검토하고, physical experiment와 intellectual reasoning을 함께 자동화해야 한다고 주장한다.
2. PDF pp.2-3은 closed-loop learning과 Robot Scientist 개념을 정의하고 Figure 1로 model update까지의 이상적 loop를 제시한다.
3. PDF pp.3-6은 Adam의 연구 문제, 가설 표현, 실험 설계, 실제 hardware, 분석 software, 결과와 형식 기록을 설명한다.
4. PDF pp.6-8은 Eve의 hardware와 계획된 drug-screening workflow를 설명하되, software와 assays가 개발 중임을 명시한다.
5. PDF pp.8-9는 두 시스템의 향후 연동, prototype의 독립성, database/model/measurement/hardware/cost 한계를 논의한다.
6. PDF pp.9-11은 결론, appendix, 기여자 역할과 39개 참고문헌으로 마무리한다.

논문의 주장 수준도 분리해야 한다. Adam이 실제 robot으로 growth assay를 수행하고 statistical/ML analysis로 biological hypotheses를 확인 또는 반박했다는 것은 구현 및 결과 주장이다. Figure 1의 완전한 반복 loop와 "all aspects" 자동화는 system concept 및 intended architecture 주장이다. 능동학습, Bayesian-optimal selection, expected information와 cost의 trade-off는 이 PDF의 방법이나 결과에 등장하지 않는다.

## Methods and Evidence

### Adam의 search space와 hypothesis generation

Adam의 연구 대상은 *S. cerevisiae* metabolism에서 효소는 알려져 있지만 대응 gene/ORF가 알려지지 않은 locally orphan enzymes이다(PDF p.3). 첫 수준 가설은 `encodesORFtoEC(ORF, E.C.)`, 둘째 수준은 metabolite가 특정 deletant strain의 성장에 영향을 준다는 `affectsgrowth(compound, deletant)` predicate다(PDF p.3). 이는 원고의 $S$에 대응시킬 수 있는 명시적 후보 공간이다.

가설 생성은 Prolog로 표현한 Forster iFF708 기반 yeast metabolism model, KEGG, PSI-BLAST/FASTA sequence similarity와 abductive inference를 사용한다(PDF pp.3-5). 절차는 locally orphan E.C. number를 찾고, 다른 organism의 알려진 ORF sequence를 모은 뒤, 유사한 yeast ORF를 찾아 ORF-E.C. mapping 후보를 만드는 네 단계다(PDF p.5). 초기 연구에서 C-Progol 5를 사용한 restricted abductive logic programming도 설명한다(PDF p.4). 이 부분은 원고의 $G$에 강하게 대응한다.

### Experiment design과 physical execution

Adam은 각 가설을 시험하기 위해 deletant strain과 wild-type control을 metabolite 유무에 따라 비교하는 two-factor design을 만든다(PDF pp.3-4). Microplate layout은 Latin-square design을 사용해 background noise보다 작은 정량 차이를 더 잘 검출하도록 구성한다(PDF p.5). Layout과 liquid-handler volume file을 robot control software로 보내 실제 실험을 실행한다(PDF pp.4-5).

Figure 2-3과 본문은 Adam이 conventional liquid handler, plate washer, centrifuge, incubator, plate reader와 세 robot arm으로 구성된 실제 laboratory system임을 보여준다(PDF pp.4-5). 하루 최대 1,000개 개별 실험을 만들 수 있고 typical experiment는 4일간 수행된다고 보고한다(PDF p.4). 따라서 physical wet-lab executor $E$는 직접 지지된다.

다만 본 PDF는 어떤 후보 가설을 먼저 또는 다음에 선택하는지를 정하는 목적함수를 제시하지 않는다. 가설에 맞는 assay를 설계하고 suitable metabolite를 고르는 세부는 외부 website로 넘기며(PDF pp.3-4), 보고된 Adam 결과에서는 생성한 20개 가설을 모두 시험했다고 쓴다(PDF p.5). `active learning`, `Bayesian`, `posterior`, `expected information gain`, 또는 정보와 비용을 함께 최적화하는 criterion은 PDF 전 페이지에 없다. Latin-square는 measurement design이지 다음 hypothesis를 고르는 search policy가 아니다.

### Measurement, statistical analysis와 accept/reject

관측값은 두 plate reader가 595 nm에서 측정한 optical density이며, 시간에 따른 growth proxy로 사용된다(PDF p.4). Growth curve는 cubic spline으로 fitting, smoothing, de-noising한 뒤 growth rate와 lag time 같은 parameter를 추출한다(PDF pp.4-5). Multiple replicates의 parameter는 random forests로 분석하여 statistically significant result를 만들고 biological hypothesis를 confirm 또는 refute한다(PDF p.5).

따라서 통계/ML 기반 biological-hypothesis 판정은 직접 지지된다. 그러나 이 review는 conventional null-hypothesis test 이름, null/alternative, test statistic, p-value threshold, false-positive/false-negative rate 또는 random-forest calibration을 제시하지 않는다. `statistical hypothesis test`라는 단수 표현은 source보다 구체적이며, 이 검증은 scientific novelty를 측정하는 test가 아니다.

### Memory와 closed-loop update

Custom MySQL database가 각 단계의 data와 metadata를 저장하고, logical metabolism model은 새 knowledge로 update되며 cycle이 다시 반복될 수 있다고 설명한다(PDF pp.4-5). Figure 1도 observation, statistical/ML analysis, new knowledge, system-model update, hypothesis generation으로 이어지는 loop를 명시한다(PDF p.3). 이를 SERVO에 사후 매핑하면 experimental record $M_e$와 updated model/knowledge $M_s$가 모두 존재한다고 볼 근거가 있다.

다만 논문은 model update 뒤에 수행된 별도의 다음-round 결과나 convergence trajectory를 정량 보고하지 않는다. Adam이 20개 가설을 실제 시험했다는 실증과, 결과가 model에 반영되어 cycle이 반복될 수 있다는 architecture 설명을 구분해야 한다. Physical execution과 result feedback은 명백하지만, 여러 round가 완전히 무인으로 연속 수행됐다는 결과는 이 PDF에 직접 제시되지 않는다.

### Human boundary와 independent confirmation

Adam은 strain stock과 consumables 공급 외에는 인간 개입이 필요 없도록 `intended to be fully automated`되었다(PDF p.4). 그러나 이는 의도된 운용 경계다. 논문은 public database conflict를 발견하면 automated hypothesis generation 전에 humans가 model을 manually update했다고 밝히고(PDF p.9), physical fault나 plate misplacement는 당시 인간이 더 잘 발견하고 수정한다고 인정한다(PDF p.9).

Adam은 13개 locally orphan enzymes에 관한 20개 가설을 만들고 모두 robot에서 시험하여 12개를 높은 confidence로 확인했다고 보고한다(PDF pp.5-6). 이 12개 중 **3개 conclusion만 conventional manual biological experiments로 검증**되었고, **추가 6개는 detailed literature search가 supporting evidence를 찾았다**(PDF pp.5-6). p.9는 Adam의 new knowledge가 independently verified되었다고 요약하지만, 이 review 자체의 구체적 breakdown은 3개 manual verification과 6개 literature support다. 모든 12개가 인간의 독립 wet-lab confirmation을 거쳤다고 확대하면 안 된다.

## Findings

- Adam은 13개 locally orphan enzymes에 대해 20개 gene-function hypotheses를 만들고, 모두 physical robot에서 시험해 12개를 high confidence로 확인했다고 보고한다(PDF pp.5-6).
- 해당 12개 가운데 3개는 conventional manual biological experiments로 검증되었고, 6개는 literature search에서 supporting evidence를 찾았다(PDF pp.5-6). 나머지 3개에 대한 인간 독립 확인 방법은 이 review에 명시되지 않는다.
- Adam은 원래 20개 중 YIL033C를 glutaminase로 잘못 결론 내렸다. 실제 phenotype은 metabolism model에 없던 cAMP-dependent protein kinase role로도 설명될 수 있었고, 저자들은 이를 model weakness로 제시한다(PDF p.6).
- Physical wet-lab closure의 구성 요소는 실제로 존재한다. Adam은 robot으로 yeast growth experiments를 실행하고, OD measurements를 분석해 biological hypotheses를 confirm/refute하며, 결과 knowledge를 metabolism model로 되돌리는 구조를 가진다(PDF pp.3-5, Figures 1-3).
- `S`, `G`, `E`, `V`, `M`은 source 내용에 page-grounded하게 대응시킬 수 있다. `$\pi$`에 해당할 수 있는 automatic assay generation은 있으나, updated belief/memory를 이용해 다음 hypothesis를 선택하는 명시적 decision rule은 없다. 특히 active-learning 또는 Bayesian/EIG policy는 제시되지 않는다.
- 논문이 말하는 statistical validation은 replicate growth phenotype에 대한 cubic-spline/random-forest 분석이다(PDF pp.4-5). 이는 truth-tracking 또는 novelty calibration을 별도로 검증한 결과가 아니다.
- Adam의 최대 1,000 experiments/day와 typical four-day experiment는 hardware throughput 설명이지 discovery rate, cost-optimality 또는 policy efficiency의 비교 결과가 아니다(PDF p.4).
- Eve는 physical hardware가 commissioned되어 있었지만 software와 assays는 개발 중이었다. 10,000 compounds/day, verification, QSAR/ML targeted cycles는 capability/design 목표로 기술되며 completed scientific discovery result가 아니다(PDF pp.6-8).
- 논문의 독자적 기여에는 workflow뿐 아니라 formal recording이 포함된다. Adam 관련 representation은 10-level nested tree와 10,000개 이상의 research elements를 연결하고 Datalog로 공개되었다(PDF p.6).

### SERVO에 대한 제한적 해석

아래는 source 저자의 용어가 아니라 이 감사의 framework mapping이다.

| SERVO component | Source-grounded mapping | 판정 |
|---|---|---|
| $S$ | locally orphan E.C. classes, candidate ORF-E.C. mappings, derived growth hypotheses(PDF pp.3, 5) | `SUPPORTED` |
| $G$ | metabolism model, KEGG, homology search와 abductive inference로 candidate hypothesis 생성(PDF pp.3-5) | `SUPPORTED` |
| $E$ | two-factor/Latin-square growth assay를 physical robotic system에서 실행(PDF pp.3-5) | `SUPPORTED` |
| $V$ | OD growth curves와 replicates를 spline/random forest로 분석해 biological hypothesis를 confirm/refute(PDF pp.4-5) | `SUPPORTED_WITH_QUALIFICATION`; test/calibration 세부 없음 |
| $M$ | MySQL experimental records와 update되는 logical metabolism model(PDF pp.4-6) | `SUPPORTED` |
| $\pi$ | model-based assay generation과 workflow ordering은 있으나 next-hypothesis selection objective는 제시되지 않음 | `PARTIAL`; active-learning/Bayesian-optimal은 `UNSUPPORTED` |

따라서 "여섯 구성요소 전체"는 매우 넓은 사후 매핑으로만 성립할 수 있다. `$\pi$`를 SERVO 정의처럼 belief와 memory에 따라 다음 $h$를 선택하는 policy로 요구하면 이 PDF의 근거는 불완전하다. "including an active-learning policy"를 붙이면 결합 주장은 직접 지지되지 않는다.

## Limitations

- 이 문서는 review article이며 Adam의 핵심 result detail을 primary *Science* 2009 paper [24]와 project website로 넘긴다(PDF pp.5-6, 10). 따라서 이 PDF만으로 test threshold, classifier performance, run-level autonomy와 experiment-selection algorithm을 재구성할 수 없다.
- Adam과 Eve 모두 prototype이다. 저자들은 Robot Scientist가 independent worker는 아니며 향후 hardware/software가 독립성을 높일 것이라고 쓴다(PDF pp.8-9).
- Adam의 metabolism model에는 kinase control mechanism이 없어 YIL033C에 관한 incorrect conclusion을 냈다(PDF p.6). 이것은 physical observation만으로 semantic scientific conclusion이 보장되지 않음을 보여준다.
- Hypothesis generation은 KEGG와 public knowledge에 의존하여 database error에 취약하다. 저자들은 conflict가 있을 때 humans가 model을 manually update한 후 automated generation을 수행했다고 밝힌다(PDF p.9).
- Growth analysis는 noise, contamination과 missing reading을 routine 처리하지만, abnormal pattern 자동 식별은 future refinement로 남아 있다(PDF p.9).
- Plasticware flaw, instrument fault와 plate misplacement 같은 physical problem은 당시 humans가 더 쉽게 발견하고 수정한다(PDF p.9). 따라서 무인 wet-lab reliability는 완전하지 않다.
- Random-forest 판정의 dataset size, split, threshold, Type I/II error, calibration, sensitivity와 specificity가 이 review에 없다. `statistically significant`라는 저자 표현만으로 validator가 calibrated됐다고 결론 내릴 수 없다.
- 20개 가설 전부를 시험했다고 보고하므로(PDF p.5), 실증된 search가 active learning으로 후보 수를 줄였거나 정보/비용 효율을 최적화했다는 증거가 없다.
- Adam은 현재 human scientists보다 cost-effective하지 않다고 저자들이 명시한다(PDF p.9). 본문의 cost 논의는 active-learning selection criterion이 아니라 capital, training, service와 maintenance의 총비용 비교다.
- Manual experiment로 직접 검증된 것은 3개 conclusion이고 literature evidence는 6개다(PDF pp.5-6). "final conclusions were confirmed by humans"를 모든 12개에 대한 독립 wet-lab replication으로 읽을 수 없다.
- 여러 post-update round가 실제로 반복된 횟수, 시간, success rate와 stopping criterion은 보고되지 않는다. Figure 1과 method prose는 closed-loop architecture를 지지하지만 convergence나 trustworthy closure를 입증하지 않는다.
- Eve의 software와 assays는 개발 중이며 대부분 미래형이다(PDF pp.6-8). Adam의 실증 결과와 Eve의 목표 capability를 합산하면 evidence scope가 부풀려진다.

## Citation Assessments

### `EN-C011:sparkes2010robot`

- **원고 위치:** `submission/main.tex:85`, Background.
- **원고 주장:** Domain-specific systems가 active-learning approximation을 이미 사용하며, Robot Scientist의 experiment selection이 그 예라고 말한다. 이 문장은 직전의 EIG 정의와 연결되어 있다.
- **Citation role:** `direct`, `example`, `interpretive`.
- **PDF 근거:** Adam은 model에서 hypotheses를 만들고, two-factor assay와 Latin-square microplate layout을 설계하며, 생성한 20개 hypotheses를 모두 시험한다(PDF pp.3-5). Suitable metabolite 선택 세부는 website로 넘긴다(PDF pp.3-4).
- **부재 근거:** PDF에는 `active learning`, `Bayesian`, posterior, EIG, expected information, 정보-비용 목적함수 또는 next-hypothesis acquisition criterion이 없다. Latin-square는 measurement layout이고 random forest는 result analysis다(PDF p.5).
- **판정:** `MISATTRIBUTED`; severity `major`. 현재 cited source만 놓고 보면 `UNSUPPORTED`다.
- **이유:** Automatic experiment design은 지지되지만, active-learning approximation이라고 부를 selection policy가 이 source에 정의되거나 평가되지 않는다. 이 review가 reference [23]을 Robot Scientist concept의 선행 source로 가리킨다는 사실만으로 [23]의 구체적 policy를 현재 citation에 귀속할 수 없다. EIG 문맥은 source가 제공한 근거보다 강하다.
- **권고 수정:** 이 citation만 유지하려면 "Robot Scientist used model-driven, closed-loop experimental design"으로 낮춘다. Active-learning 또는 information-cost policy를 유지하려면 해당 algorithm을 직접 설명하는 primary source를 별도로 전문 감사하여 인용한다.
- **Korean parity:** `omitted`. 직접 대응 occurrence는 없다. 다만 핵심 active-learning 주장은 뒤의 `KO-C016:sparkes2010robot`에서 Bayesian-optimal claim과 결합되어 별도로 재등장한다.

### `EN-C016:sparkes2010robot`

- **원고 위치:** `submission/main.tex:92`, Related Work.
- **원고 주장:** Robot Scientist가 LLM 시대보다 10년 이상 앞서 yeast functional genomics에서 hypothesis generation, robotic experimentation, statistical validation을 통합했고, active-learning policy를 포함한 SERVO 여섯 구성요소 전체를 physical wet-lab form으로 구체화했다고 말한다.
- **Citation role:** `direct`, `example`, `interpretive`.
- **PDF 근거:** Adam은 yeast gene-enzyme hypotheses를 생성하고(PDF pp.3-5), physical robot에서 growth assays를 실행하며(PDF pp.4-5, Figures 2-3), OD curves와 replicates를 statistical/ML analysis해 confirm/refute하고 model을 update한다(PDF pp.4-5, Figure 1). 2010년 publication은 pre-LLM chronology를 지지한다(PDF pp.1, 10).
- **구성요소 대조:** `$S/G/E/V/M$`은 위 근거로 사후 매핑할 수 있다. `$\pi$`의 최소한의 assay-generation procedure는 있지만, SERVO 정의의 next-hypothesis decision rule이나 active-learning objective는 제시되지 않는다. 통계 분석도 biological hypothesis validation이지 novelty measure가 아니다.
- **판정:** `PARTIAL`; severity `major`.
- **이유:** 문장의 핵심 역사적 wet-lab integration은 강하게 지지된다. 그러나 "all six"의 `$\pi$`와 특히 "including an active-learning policy"가 source를 초과한다. Actual multi-round closure도 architecture와 result를 구분해 표현해야 한다.
- **권고 수정:** "Robot Scientist integrated automated gene-function hypothesis generation, physical robotic growth experiments, statistical/ML analysis, and model updating in yeast functional genomics, providing an early wet-lab closed-loop architecture before LLM systems. This source does not specify an active-learning or Bayesian experiment-selection objective."
- **Korean parity:** `equivalent` with `KO-C011:sparkes2010robot`; 같은 근거와 같은 active-learning/all-six 과장을 유지한다.

### `EN-C021:sparkes2010robot`

- **원고 위치:** `submission/main.tex:94`, Related Work.
- **원고 주장:** Automated science에는 Bayesian-optimal experiment selection의 긴 역사가 있고, 가장 직접적인 예가 Robot Scientist의 active-learning policy라고 말한다.
- **Citation role:** `joint`, `interpretive`, `example`. 일반적 BED history는 인접 BED sources와 함께 서술되지만, Robot Scientist mechanism은 이 source가 독립적으로 입증해야 한다.
- **Joint-only support:** general history clause에 한해 `yes`; 다른 BED citations를 결합해도 Sparkes PDF에 없는 Bayesian/EIG objective의 source 근거가 생기지는 않는다.
- **PDF 근거:** Sparkes et al.은 Adam의 abductive hypothesis generation, two-factor experiment와 Latin-square layout, random-forest analysis를 설명한다(PDF pp.3-5). Robot Scientist concept의 기원으로 reference [23]을 인용하지만(PDF pp.2, 10), 그 reference의 policy를 이 review에서 설명하지 않는다.
- **판정:** `MISATTRIBUTED`; severity `major`. 현재 cited source만 놓고 보면 `UNSUPPORTED`다.
- **이유:** 이 PDF에는 Bayesian inference, optimal design, acquisition objective, active learning 또는 expected-information-versus-cost criterion이 없다. Cost는 p.9에서 system capital/maintenance가 humans보다 비싸다는 별도 한계로만 논의된다. 따라서 이 citation으로 Bayesian-optimal priority/example claim을 뒷받침할 수 없다.
- **권고 수정:** "Automated science has a history of hypothesis-driven closed-loop experiment design, exemplified here by Robot Scientist"로 낮추거나, Bayesian/active-learning policy를 직접 기술하고 평가한 원 논문으로 citation을 교체한다.
- **Korean parity:** `equivalent` with `KO-C016:sparkes2010robot`; 한국어도 `베이즈 최적 실험 선택`과 `능동학습 정책`을 같은 강도로 단정한다.

### `EN-C024:sparkes2010robot`

- **원고 위치:** `submission/main.tex:162`, Analysis of Core AI Scientist Systems, Table `tab:core-comparison` caption. Citation은 표의 Robot Scientist 열을 anchor한다.
- **원고 주장:** Robot Scientist를 pre-LLM core system으로 포함하고, 표에서 `Novelty measure=Stat. test`, `Loop closed?=Yes (wet-lab)`, `$\pi$ type=Active learn.`, `V completeness=V_e`, `M structure=M_e+M_s`, `H=Low`로 coding한다.
- **Citation role:** caption 전체에는 `joint`, Robot Scientist 열에는 `interpretive`, `direct`.
- **Joint-only support:** caption의 cross-system inclusion에는 `yes`; Robot Scientist 열의 각 coding에는 `no`이며 NovelSeek citation이 이 열의 근거를 보완할 수 없다.
- **PDF 근거:** Adam의 physical robot, result-informed model update, statistical/ML biological-hypothesis analysis, MySQL records와 logical model은 각각 wet-lab loop, `$V_e$`의 관측 기반, `$M_e+M_s$` mapping을 지지한다(PDF pp.3-6). Human intervention은 stocks/consumables 공급만 필요하도록 intended되었지만 manual model correction, selected-result verification과 physical fault handling이 남아 있다(PDF pp.4-6, 9).
- **표 항목별 판정:** `pre-LLM`과 physical wet-lab system inclusion은 `SUPPORTED`; loop closure는 architecture와 feedback path 기준 `SUPPORTED_WITH_QUALIFICATION`; `$M_e+M_s$`는 `SUPPORTED`; `$V_e$`는 physical observation과 statistical analysis의 사후 mapping으로 `SUPPORTED_WITH_QUALIFICATION`; `H=Low`는 intended operation 기준 `SUPPORTED_WITH_QUALIFICATION`; `$\pi$=Active learn.`은 `UNSUPPORTED`; `Novelty measure=Stat. test`는 `CONTRADICTED`에 가깝게 잘못 이름 붙인 mapping으로, source의 test는 growth phenotype/gene-function hypothesis를 판정하지 scientific novelty를 측정하지 않는다.
- **판정:** `PARTIAL`; severity `major`.
- **이유:** 표의 절반 이상은 source-grounded interpretation이지만 두 load-bearing labels가 잘못되었다. 특히 statistical validation을 novelty test로 바꾸고, method가 보고하지 않은 active-learning policy를 부여했다.
- **권고 수정:** Robot Scientist 열을 `Hypothesis validation=statistical/ML growth analysis; no autonomous novelty test`, `Loop=physical feedback architecture (reported result; repeated rounds not quantified)`, `$\pi$=model-driven assay generation; active-learning objective not stated`, `$V$=physical measurement plus statistical/ML analysis; calibration not reported`, `$M=M_e+M_s$`, `H=low after setup, with manual support/verification`로 교정한다.
- **Korean parity:** `equivalent` with `KO-C023:sparkes2010robot`; 한국어 표는 `통계 검정`, `능동학습`, `예(습식)`, `낮음`으로 같은 coding과 같은 문제를 재현한다.

### `KO-C011:sparkes2010robot`

- **원고 위치:** `submission/main_ko.tex:111`, 관련 연구.
- **원고 주장:** Robot Scientist가 효모 기능유전체학에서 가설 생성, robot experiment, statistical validation을 통합해 SERVO 여섯 구성요소 전체와 active-learning policy를 physical wet-lab으로 구현했다고 말한다.
- **Citation role:** `direct`, `example`, `interpretive`.
- **PDF 근거:** 실제 Adam의 hypothesis generation, physical experiment, growth measurement, random-forest confirm/refute, model update는 지지된다(PDF pp.3-5). 모든 six-component mapping 중 `$\pi$`의 active-learning criterion은 제시되지 않는다.
- **판정:** `PARTIAL`; severity `major`.
- **이유:** `EN-C016`과 동일하다. Wet-lab integration은 맞지만 active-learning과 all-six의 강한 문구는 source를 넘는다.
- **권고 수정:** 영어 교정안과 동일하게 "모델 기반 가설 생성, 물리적 성장 실험, 통계/ML 분석과 모델 갱신을 연결한 초기 wet-lab closed-loop architecture"로 한정하고 active-learning은 제거하거나 직접 source를 교체한다.
- **Korean parity:** `equivalent` with `EN-C016:sparkes2010robot`.

### `KO-C016:sparkes2010robot`

- **원고 위치:** `submission/main_ko.tex:113`, 관련 연구.
- **원고 주장:** Bayesian-optimal experiment selection의 자동 과학 전통을 Robot Scientist의 active-learning policy가 가장 직접적으로 보여준다고 말한다.
- **Citation role:** `joint`, `interpretive`, `example`.
- **Joint-only support:** general BED history clause에 한해 `yes`; Sparkes-specific policy claim은 이 source가 독립적으로 입증해야 한다.
- **PDF 근거:** Hypothesis-driven closed-loop design과 automatic assay generation은 설명되지만(PDF pp.3-5), Bayesian, optimal, active-learning 또는 information-cost objective는 없다.
- **판정:** `MISATTRIBUTED`; severity `major`. 현재 cited source만 놓고 보면 `UNSUPPORTED`다.
- **이유:** `EN-C021`과 동일하게 cited PDF가 정확한 정책 주장을 뒷받침하지 않는다.
- **권고 수정:** `가설 주도 폐루프 실험 설계`로 낮추거나 Bayesian/active-learning criterion이 명시된 primary source를 인용한다.
- **Korean parity:** `equivalent` with `EN-C021:sparkes2010robot`; `EN-C011`의 broad active-learning example도 이 문장으로 의미상 이동했다.

### `KO-C023:sparkes2010robot`

- **원고 위치:** `submission/main_ko.tex:215`, 핵심 AI 과학자 시스템 분석, Table `tab:core-comparison` caption.
- **원고 주장:** 표의 Robot Scientist 열을 pre-LLM core-system comparison으로 제시하며 `통계 검정`, `예(습식)`, `능동학습`, `$V_e$`, `$M_e+M_s$`, `H 낮음`으로 coding한다.
- **Citation role:** caption 전체에는 `joint`, Robot Scientist 열에는 `interpretive`, `direct`.
- **Joint-only support:** caption의 cross-system inclusion에는 `yes`; Robot Scientist 열에는 `no`.
- **PDF 근거:** Physical wet-lab, statistical/ML biological-hypothesis analysis, records와 model update, intended low-intervention operation은 지지되거나 제한적으로 지지된다(PDF pp.3-6, 9). Novelty test와 active-learning policy는 지지되지 않는다.
- **판정:** `PARTIAL`; severity `major`.
- **이유:** `EN-C024`와 동일한 table-level mapping 오류다. 특히 `신규성 측정=통계 검정`은 biological gene-function validation을 novelty evaluation로 잘못 분류한다.
- **권고 수정:** 영어 표와 같은 열 정의로 동기화하고, `능동학습`을 `모델 기반 실험 설계(선택 목적함수 미보고)`로, `신규성 측정`을 `없음; 생물학적 가설은 통계/ML로 검증`으로 교정한다.
- **Korean parity:** `equivalent` with `EN-C024:sparkes2010robot`.

## Korean Parity

| English occurrence | Korean occurrence | Parity | 감사 결과 |
|---|---|---|---|
| `EN-C011:sparkes2010robot` | 없음 | `omitted` | 한국어 Background에는 EIG 직후의 domain-specific active-learning example가 없다. 다만 Related Work의 별도 occurrence에서는 Bayesian-optimal/active-learning을 더 강하게 단정한다. |
| `EN-C016:sparkes2010robot` | `KO-C011:sparkes2010robot` | `equivalent` | Wet-lab integration, all six components와 active-learning policy를 같은 강도로 서술한다. |
| `EN-C021:sparkes2010robot` | `KO-C016:sparkes2010robot` | `equivalent` | Bayesian-optimal history와 Robot Scientist active-learning policy를 동일하게 단정한다. |
| `EN-C024:sparkes2010robot` | `KO-C023:sparkes2010robot` | `equivalent` | Caption과 표의 Robot Scientist coding이 번역되어 같은 active-learning/novelty-measure 오류를 유지한다. |

언어 간 핵심 의미는 대체로 일치한다. 문제는 번역 비대칭보다 두 언어가 같은 unsupported policy claim을 반복한다는 데 있다. 영어 Background의 별도 `EN-C011`은 한국어에서 빠졌지만, 그보다 강한 Bayesian-optimal 문장이 양쪽 Related Work에 모두 있다. 교정 시 영어와 한국어에서 (1) automatic experiment design, (2) active-learning acquisition policy, (3) Bayesian/EIG optimality를 서로 다른 claim으로 분리하고, 이 PDF가 직접 지지하는 것은 첫째뿐임을 동일하게 표시해야 한다.

## Frozen Supplementary Description Assessment

Frozen description:

> An autonomous laboratory system for yeast functional genomics. It forms hypotheses about gene-enzyme relationships using a model of metabolism, selects which experiments to run via an active-learning criterion weighing expected information against cost, physically executes growth experiments with laboratory robotics, measures cell growth, and applies a statistical hypothesis test to accept or reject before forming the next round. It predates large language models. Final scientific conclusions were confirmed by human scientists.

- **"An autonomous laboratory system for yeast functional genomics" - `SUPPORTED_WITH_QUALIFICATION`.** Adam은 바로 이 목적의 physical prototype이다(PDF pp.3-5). 다만 source 표현은 `intended to be fully automated`이고 stocks/consumables 공급, conflict model의 manual update와 physical-fault handling이 인간에게 남는다(PDF pp.4, 9).
- **"forms hypotheses about gene-enzyme relationships using a model of metabolism" - `SUPPORTED`.** ORF-E.C. mapping과 derived growth hypotheses를 Prolog metabolism model, KEGG와 homology search로 생성한다(PDF pp.3-5).
- **"selects which experiments to run via an active-learning criterion weighing expected information against cost" - `UNSUPPORTED`, severity `major`.** 이 PDF는 suitable metabolite 선택 세부를 website로 넘기고, 20개 hypotheses를 모두 시험했다고만 보고한다(PDF pp.3-5). Active learning, expected information와 cost trade-off는 기술하지 않는다. p.9의 cost discussion은 system economics의 한계이지 selection criterion이 아니다.
- **"physically executes growth experiments with laboratory robotics" - `SUPPORTED`.** Figures 2-3과 hardware/method/result description이 Adam의 actual wet-lab execution을 직접 보여준다(PDF pp.4-5).
- **"measures cell growth" - `SUPPORTED_WITH_QUALIFICATION`.** 직접 측정값은 OD 595 nm이고, 이것을 cellular growth/phenotype proxy로 해석한다(PDF p.4). 직접 cell count가 아니다.
- **"applies a statistical hypothesis test to accept or reject before forming the next round" - `SUPPORTED_WITH_QUALIFICATION`.** Cubic-spline-derived growth parameters와 multiple replicates를 random forests로 분석하여 statistically significant result로 hypothesis를 confirm/refute하고 model을 update한 뒤 cycle이 반복될 수 있다고 설명한다(PDF pp.4-5). 그러나 named statistical test, threshold/calibration, 실제 next round의 결과는 보고하지 않는다.
- **"It predates large language models" - `SUPPORTED`.** Source는 2010년에 출판되었다(PDF pp.1, 10). 이는 temporal description이지 source가 LLM을 비교한 결과는 아니다.
- **"Final scientific conclusions were confirmed by human scientists" - `PARTIAL`, severity `minor`.** Source는 knowledge가 independently verified됐다고 요약하지만(PDF p.9), 구체적으로 manual experiments가 검증한 것은 12개 중 3개이고 literature evidence가 지지한 것은 추가 6개다(PDF pp.5-6). 이 확인은 Figure 1의 machine loop에서 매 round를 결정하는 internal acceptance gate가 아니라 selected conclusions에 대한 post-hoc follow-up이다. 모든 final conclusion이 human wet-lab confirmation을 받았다고 쓸 수 없다.

**Frozen-description verdict:** `major_revision`.

권고 교정문:

> Adam is a pre-LLM physical laboratory system for yeast functional genomics. It uses a logical metabolism model, KEGG, and homology search to generate candidate gene-enzyme and growth hypotheses; designs two-factor, Latin-square growth assays; executes them with laboratory robotics; measures OD 595 nm as a growth proxy; and uses spline processing plus random-forest analysis of replicates to confirm or refute biological hypotheses and update its model. This source describes model-driven closed-loop experiment design but does not specify an active-learning, Bayesian, or expected-information-versus-cost selection criterion. Of twelve conclusions reported as confirmed by Adam, three were manually verified and six more had supporting literature evidence.

## Overall Verdict

**Overall verdict: `major_revision`.**

`sparkes2010robot`은 Robot Scientist/Adam의 정체성, pre-LLM chronology, yeast gene-function hypothesis generation, actual physical wet-lab experiment, statistical/ML analysis, formal record와 model update를 강하게 지지한다. 따라서 citation 자체가 무관하거나 잘못된 문헌인 `citation_invalid`는 아니다. 물리적 discovery loop의 역사적 예로 쓰는 것은 적절하다.

그러나 현재 원고의 load-bearing policy claims는 이 PDF가 지지하지 않는다. `active-learning policy`, `Bayesian-optimal experiment selection`, `expected information against cost`, `$\pi$=Active learn.`은 source에 기술되어 있지 않다. 또한 표의 `Novelty measure=Stat. test`는 growth phenotype을 통해 gene-function hypothesis를 확인/반박하는 validator를 scientific novelty test로 오분류한다. SERVO 여섯 요소 전체를 구현했다는 문장은 `$S/G/E/V/M$`에는 근거가 있으나 `$\pi$`를 source보다 강하게 해석하므로 qualification이 필요하다.

Closed-loop와 human role도 범위를 명시해야 한다. Adam의 physical execution과 feedback architecture는 실제지만, 이 review는 model update 뒤 여러 round의 autonomous trajectory를 정량 보고하지 않는다. 인간은 consumables를 공급하고, conflict가 있는 model을 사전 수정하며, selected conclusions를 검증하고, 일부 physical faults를 처리한다. 12개 확인 결론 전부가 human wet-lab replication을 받은 것이 아니라, 3개는 manual experiment, 6개는 literature support로 구체화된다.

따라서 Robot Scientist를 유지하되, 원고와 frozen description에서 active-learning/Bayesian-optimal 주장을 제거하거나 이를 직접 입증하는 primary source로 교체하고, 표의 novelty, `$\pi$`, validator와 human-boundary labels를 교정해야 한다.

## Completion Checklist

- [x] RUBRIC의 필수 heading 11개를 정확한 이름으로 모두 사용했다.
- [x] PDF, BibTeX와 manifest로 title, 12인 authors, journal, year, DOI, SHA-256, page count와 version status를 확인했다.
- [x] 지정된 local PDF p.1부터 p.11까지 순서대로 모두 읽었다.
- [x] PDF pp.1, 3-9를 렌더링하여 title, Figure 1-5, logical predicates, result와 limitation layout을 시각 확인했다.
- [x] PDF에 표와 수학식이 없음을 확인했고, 표시된 logical predicates와 ORF-E.C. mapping을 렌더링으로 확인했다.
- [x] problem/context, prior work, document structure, Adam/Eve의 evidence status, methods, result, formalization과 limitations를 분석했다.
- [x] 20개 hypotheses, 13개 enzymes, 12개 confirmed conclusions, 3개 manual verification, 6개 literature support를 exact condition과 함께 확인했다.
- [x] active learning, Bayesian/EIG, expected-information-versus-cost criterion이 source에 없음을 full-text와 term search로 확인했다.
- [x] two-factor/Latin-square experiment design과 next-hypothesis search policy를 구분했다.
- [x] physical wet-lab execution, statistical/ML biological validation, model update와 demonstrated multi-round closure를 구분했다.
- [x] random forest의 hypothesis confirm/refute 기능과 scientific novelty test를 구분했다.
- [x] SERVO `$S/G/E/V/M/\pi$` 여섯 요소를 각각 page-grounded하게 대조했다.
- [x] intended low human intervention과 실제 consumable supply, manual model correction, selected-result confirmation, physical-fault handling을 구분했다.
- [x] EN link 4개와 KO link 3개를 각각 독립 판정했다.
- [x] 영어와 한국어 occurrence parity를 `equivalent`, `omitted`로 대조하고, 대응 occurrence가 아닌 뒤 문장의 의미상 재등장을 별도로 기록했다.
- [x] 세 support lane의 identity/system-description, methods/context, claims/parity 근거를 primary report와 대조하고 판정 차이를 해소했다.
- [x] frozen supplementary description의 모든 clause를 page-grounded하게 판정하고 교정문을 제시했다.
- [x] source author claim과 SERVO/framework interpretation을 분리했다.
- [x] 지정된 Sparkes PDF 이외의 source PDF를 열지 않았고 API/model call을 사용하지 않았다.
- [x] status, manifest, manuscript와 evidence file을 수정하지 않았다.

AUDIT_COMPLETE: yes
PAGES_COVERED: 1-11
EN_LINKS_COVERED: EN-C011:sparkes2010robot, EN-C016:sparkes2010robot, EN-C021:sparkes2010robot, EN-C024:sparkes2010robot
KO_LINKS_COVERED: KO-C011:sparkes2010robot, KO-C016:sparkes2010robot, KO-C023:sparkes2010robot
SYSTEM_DESCRIPTION_ASSESSED: yes
VERDICT: major_revision
