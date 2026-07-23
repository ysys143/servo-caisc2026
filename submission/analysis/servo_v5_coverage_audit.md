# SERVO v5 source coverage audit (T4.5-D)

- 목적: charter B.8 / T4.5. 핵심 감사 질문 = **"SERVO 판정에 유용해 보이는 문장만 골라 추출했는가?"** (선택 편향). proposition을 다시 읽는 게 아니라 커버리지 경계·미커버 영역·누락 리스크를 기록한다.
- **공통 inclusion rule(6사례):** 각 사례의 bounded configuration 안에서 decision-structure 관련 문장(setup, actor/component naming, task regime, candidate/artifact 정의, generation/selection/execution/evaluation/memory/update, human/external boundary, fixed procedure, capability, 부정·모호 결과)을 판정 없이 추출. figure caption/legend, 사례 무관 배경, 인접 proposition과 중복 문장은 제외.

## Coverage matrix

| case | system | 총p | covered pages | 미커버 | 제외/미커버 이유 | potential omissions (확인 필요) |
|---|---|---|---|---|---|---|
| C01 | Coscientist (boiko2023emergent) | 13 | 1-5,8 -> **1-8 (보완중)** | 9-13 | 9-13 = Methods/refs/extended data | **pages 6-7 보완 진행(T45aC01gap)** — pilot이 web-search/RDKit tool, reasoning-capabilities 섹션, optimization game(score-directed policy) 누락. 9-13(Methods) 미확인 |
| C02 | AI Scientist 2024 (lu2024aiscientist) | 186 | 2-6,11-13,18,19 | 1,7-10,14-17,20-186 | 본문 핵심 커버; 20-186은 방대한 appendix(생성 논문 예시·프롬프트·리뷰 덤프) | appendix 프롬프트/템플릿에 procedure 문장 잔존 가능(미확인) |
| C03 | AI Scientist 2026 (lu2026aiscientist) | 9 | 1-4,7-9 | 5-6 | 5-6 = template-BASED 3단계 워크플로(bounded config가 template-FREE라 명시 제외) | 낮음 — config 경계상 정당 제외 |
| C04 | Agent Laboratory (schmidgall2025agentlab) | 84 | 1,5-10,18-22,42-43 | 2-4,11-17,23-41,44-84 | 본문 워크플로·평가·discussion + appendix B 프롬프트 일부 커버; 2-4 Related Work, 10-18 survey/cost 표, 나머지 appendix grading | 23-41,44-84 appendix에 procedure/프롬프트 문장 잔존 가능(미확인) |
| C05 | Adam (sparkes2010robot) | 11 | 1,3-6,8,9 | 2,7,10,11 | Adam material 집중; Eve(6-8)·references(9-11)는 out of scope | **스팟체크 완료(2026-07-23):** page 2=generic Robot Scientist 배경/역사(DENDRAL/AM/EURISKO/closed-loop 개념, Adam-특정 없음, C05-P01이 개념 커버), page 7=Eve-특정(out of scope), page 10-11=references. **Adam 누락 없음** |
| C06 | NovelSeek (zhang2025novelseek) | 34 | 2-9,13,20,22 | 1,10-12,14-19,21,23-34 | 본문 아키텍처·평가 커버; 10-12 per-task 데이터/베이스라인, 나머지 결과표·Related Works·appendix | 10-12,23-34 appendix에 procedure 문장 잔존 가능(미확인) |

## 선택 편향 평가 (핵심 감사 질문)

**방향 1 — 정(正) cherry-picking("유용한 것만 골랐다"):** 낮음. 근거: 각 사례 modality 분포에 procedure/capability가 다수이고(C03 41 procedure, C06 24 procedure, capability 다수), **부정·한계 문장을 명시 포함**했다 — C01 Falcon-40B 실패·GPT-3.5 Web Searcher 실패·air-bubble 오염, C04 failure modes·repository-limitation, C05 하나의 hypothesis가 incorrect conclusion(kinase gap). "유용한 established 근거만" 골랐다면 이런 부정 문장은 없어야 한다. 포함됐으므로 정-cherry-picking 리스크는 낮다.

**방향 2 — 역(逆) cherry-picking("결정적 문장을 놓쳤다"):** C01에서 실측됨 — pages 6-7의 optimization game("maximizing the reaction yield" = score-directed policy 직접 근거)과 tool 사용(web search/code execution)이 pilot에서 누락. **T45aC01gap로 보완 중.** 이것이 coverage audit가 실제로 잡아낸 결함이다.

**커버리지 불균형:** C01만 full 본문(1-8), 타 사례는 본문 핵심 + appendix 미커버. appendix 미커버는 대부분 정당(생성물 예시·결과표·코드)이나, C02/C04/C06 appendix의 프롬프트/템플릿에 procedure 문장이 잔존할 수 있어 potential omission으로 기록. 이는 T5 판정을 **왜곡하지 않는다**(procedure 문장은 이미 충분히 포집됐고, 누락 시 occurrence가 아닌 procedure/architecture claim의 근거만 소폭 감소). 단, freeze manifest에 coverage_status를 사례별로 기록해 후속 확장 가능성을 남긴다.

## Disposition
- **C01:** pages 6-7 보완 필수(진행 중). 완료 후 이 표의 C01 행을 확정.
- **C05:** page 2,7 스팟체크 완료(2026-07-23) — page 2 generic 배경, page 7 Eve(out of scope), page 10-11 references. Adam 누락 없음. coverage_status=review_bounded_complete 정당.
- **C02/C04/C06:** appendix 미커버는 coverage_status="body_complete_appendix_partial"로 freeze manifest에 기록. 후속 확장은 별도 issue.
- **C03:** coverage_status="config_bounded_complete"(template-free 경계 내 완전).
