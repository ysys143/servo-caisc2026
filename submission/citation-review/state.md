# 인용 내용 정합성 리뷰 — 상태 (State)

정본 원고 `submission/main.tex`가 인용 논문 62편에 대해 서술·주장하는 내용이 **실제 논문 전문과 부합하는가**를 논문별 정독으로 검증한다.

## 파일
- `papers.tsv` — 논문 트래커 60행 (read_status: PENDING/READING/READ/TARGETED, n_claims, n_verified). *v2는 crosswalk 등록(TARGETED, 로컬 PDF 없음).*
- `ledger.tsv` — **원자적 주장 원장 129행** (단일 진실원천). status: PENDING→VERIFIED/FLAGGED.
- `findings.md` — FLAGGED 주장 + 권고 수정(사람용 리포트) + 논문별 정독 노트
- `check.py` — 완결성 불변식 3개 검사 (`python3 check.py`)
- `apply.py` — 논문별 리뷰 결과 JSON → 원장 반영 (`python3 apply.py results.json`)
- `seed.py` — 원장 seed 생성기(1회용). `claims-inventory.md`/`paper-catalog.md` — 감사용 seed 사본.

## 원장 상태 요약 (매 논문 후 갱신)
- 진행: `python3 check.py` 로 확인. 현재 기준 = 논문 62/62, 핵심 주장 131/131.
- 검증 단위 유형: NUM 15 · METHOD 17 · CHAR 47 · BG 47 · UNCITED 2.

## verdict 코드
ACCURATE / INACCURATE-NUM(수치 오류) / MISCHARACTERIZATION(메커니즘 오설명) / MISATTRIBUTION(귀속 오류) / OVERCLAIM(과장) / CONTEXT-MISUSE(맥락 오용) / UNSUPPORTED(근거 없음) / IMPRECISE-OK(경미·부정확하나 허용범위).

## 완결성 (완료 판정)
`check.py` 네 불변식 PASS = (1) 62편 read_status READ/TARGETED, (2) 131개 핵심 주장 status≠PENDING + verdict·evidence 有, (3) 원장 키집합 == references.bib cited 62집합, (4) digest/reverse layer 완료. 이후 독립 재추출 diff로 누락 0 확인.

## 처리 방침
리뷰는 **findings 산출까지**. 원고(main.tex/main_ko.tex) 실제 수정은 사용자 승인 후 별도 단계.

## 진행 로그
- (seed) 59 papers / 128 claims 생성, check.py 키커버리지 PASS.
- **완료**: 59/59 논문 전문 정독(블라인드 digest→Layer2 대조→Layer3 역방향), 128/128 주장 검증. check.py **4대 불변식 전부 PASS**. 독립 재추출 감사 COVERAGE OK(누락 0). Tier-2 grep 재확인(aher/sparkes/kim 미귀속 확정).
- verdict: ACCURATE 97·IMPRECISE-OK 17·MISATTRIBUTION 8·MISCHARACTERIZATION 4·CONTEXT-MISUSE 1·OVERCLAIM 1. FLAGGED 14주장(요약: findings.md 상단 표).
- **(2026-07-19 정합성 복구)** `yamada2025aiscientistv2` crosswalk와 `king2004robot` primary source가 원장에 반영되었다. 현재 기준은 62편/131개 핵심 주장이고, `check.py`의 papers=ledger=references 집합은 62=62=62 **ALL PASS**이다.
  - NovelSeek/InternAgent는 같은 arXiv 2505.16938의 후속 명칭 변경으로 확인되었다. citation identity는 `NovelSeek (renamed InternAgent)`로 정규화한다.
- **(2026-07-19 패치 적용 — 사용자 승인)** `patch-plan.md`의 9개 필수 수정을 main.tex/main_ko.tex에 반영 완료:
  - 인용키 교체: +2.3→`schmidgall2025agentlab`(EN L166) · 736→`merchant2023gnome`(EN L230/L444, KO L280) · 능동학습→**신규 `king2004robot`**(EN L85/L92/L94, KO L111/L113) · 순환타당성 `aher2023turing` 제거(EN L200/L448, KO L377).
  - 서술 교정: Aletheia formal→natural-language(EN L69 단독) · SciMuse 생성품질→선택/관심(EN L90, KO L109) · cranmer 결정적→확률적(EN L440, KO L369) · ChemCrow surrogate/beam→ReAct/물리합성(EN L442, KO L371) · park full-factorial 완화(EN L448, KO L377).
  - **선택 항목 처리 완료**: (a) "Bayesian-optimal/베이즈 최적" 완화 → **철회**(King 전문 확증); (b) +2.3 선택 인용 → EN L211·KO L263에 `\citep{schmidgall2025agentlab}` **추가**(parity); (c) 도메인 표 $\pi$ 셀 "Factorial→Factorial/ablation"(EN L192)·"완전 요인→완전 요인/절제"(KO L245) **완화**. 두 PDF 재컴파일(각 19쪽, 미정의 인용 0), PDF 재복사. references.bib 불변→ZIP 재생성 불필요.
  - `king2004robot` 원장 등록 → **(2026-07-19 전문 확보·정독 완료)** Aberystwyth 저자 배포 PDF 확보→vault 추가→전문 정독. **C130 ACCURATE(primary-source 확증)**: 논문이 "active learning" 명시 + "expected cost" 기반 Bayesian 실험선택(entropy 항)·"near-optimal in polynomial time" → 원고 "Bayesian-optimal" **정확히 지지**. 이전 "완화 필요" 주의 **철회**. read_status READ, `results/king2004robot.digest.md`(전문 digest) 참조.
  - 컴파일 검증: main.pdf(19쪽)·main_ko.pdf(19쪽) 오류 0, 미정의 인용 0. check.py 62/62·131/131·**ALL PASS**. PDF 복사 + supplement ZIP 재생성 완료.
  - 원장의 14 FLAGGED verdict는 감사 이력으로 보존(원고는 수정됨; verdict는 당시 발견 기록).
- **(2026-07-19 IMPRECISE-OK + szymanski MED 라운드 — 사용자 승인)** 17개 IMPRECISE-OK와 szymanski MED 3건 전수 검토 후 실질 개선분 적용:
  - **C030**(liu): EN L171에 `\citep{liu2026lasthuman}` 추가 + "papers"→"reproduction requirements"(KO L224는 이미 정확).
  - **C064**(taniguchi): EN L96 "is"→"is modeled as a Metropolis-Hastings acceptance (consensus) process"(KO 해당 절 없음 — EN 단독).
  - **C052/C055**(merchant EIG/BED): "approximates EIG"→"can be read as a coarse EIG surrogate"(EN L219, KO L269); L444 BED 근사 해석을 원고 귀속으로 완화.
  - **C054**(merchant): "2.2M candidate structures (380k stable)"→"structures stable with respect to prior work (380k on updated convex hull)"(EN L444, KO L373).
  - **R014**(szymanski): "36 of 57"의 "36"은 2026 Author Correction 출처 → **신규 bib `szymanski2026correction`**(Nature 650(8100), DOI 10.1038/s41586-025-09992-y, WebSearch 검증) 추가 후 EN L234·KO L282 병기. 원장 **C131 ACCURATE**(web-verified, 전문 미독).
  - **수정 불필요 판정**: R011·R013·C119·C053·C106·C122·C014·C021·C018·C011·C004·C039(정확/의도/외부확증), C059·C088(FIX6/FIX9 기해소).
  - 검증: 두 PDF 각 19쪽·미정의 인용 0, check.py **62/62·131/131·ALL PASS**, PDF 재복사 + ZIP 재생성.
- **전체 감사 반영 상태**: 오류급(FLAGGED 14) + HIGH 역방향 7 + 실질 개선 가능 IMPRECISE-OK/MED = **전부 반영**. 잔여는 "수정 불필요"(정확/의도/기해소) 판정분뿐.
- **(2026-07-19 TARGETED 2편 전문 정독 — 사용자 요청)** `yamada2025aiscientistv2`·`szymanski2026correction`을 전문 확보→vault→블라인드 정독 에이전트(opus, 3층) 실행 후 READ 승격. 이제 **61 READ + ghosal 교과서 1 TARGETED**.
  - **v2 (C129 ACCURATE, 전문 확증)**: 제목/초록이 "agentic tree search"·workshop-level(ICBINB@ICLR2025, 3중 1 채택, avg 6.33) 확증. v2 논문엔 balanced-accuracy 수치 없음 → **Tier-2 확인 결과 원고의 "0.69"·"ICLR workshop"은 `lu2026`(BA 0.69 Table1 p.915)에 올바르게 귀속**, v2 오귀속 아님. **원고 수정 불필요.** (선택 정밀화: 워크숍명 "ICBINB", 1/3·withdrawn 뉘앙스 — 미적용.)
  - **정정본 (C131 → MISCHARACTERIZATION, 전문이 web결론 뒤집음)**: 정정본은 "**36 of 40 reported successes correct, 4 inconclusive**"만 말하고 "**57" 부재**. 지난 라운드의 web기반 "36 of 57"은 분자(36/40 성공)·분모(57 추론) 혼합 재프레이밍 → **오류**. **원고 수정**: EN L234/KO L282 → "초기 41/58 보고(`szymanski2023alab`), 재분석으로 40 성공 중 36 확정·4 미결로 정정(`szymanski2026correction`)". 역방향 R183(신규성 walk-back HIGH, noted-not-applied)·R184(4 미결, 반영)·R185(훈련데이터 누출 1건) 추가.
  - 검증: 두 PDF 각 19쪽·미정의 인용 0, check.py **62/62·131/131·ALL PASS**, PDF 재복사. references.bib 이번 턴 불변→ZIP 현행.
  - **교훈: 전문 정독이 web/crosswalk 검증을 뒤집을 수 있음**(정정본 사례). TARGETED는 역할이 좁을 때만 정당.
