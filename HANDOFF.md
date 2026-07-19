# CAISc 2026 제출 작업 핸드오프

작성일: 2026-05-29  
다음 세션 목표: paper_1에 시뮬레이션 섹션 통합 + 8페이지 압축 + PDF 제출

---

## 1. 제출 정보

| 항목 | 내용 |
|------|------|
| 학회 | CAISc 2026 (Conference for AI Scientists) |
| 마감 | 2026-05-31 23:59 AoE |
| 트랙 | Track 2: Open-Ended Problems |
| 플랫폼 | OpenReview (계정 있음 — JAESOL SHIN) |
| 분량 제한 | 최대 8페이지 (참고문헌·체크리스트 제외) |
| 제출 유형 | Archival |

---

## 2. 디렉토리 구조

```
/Users/jaesolshin/Documents/Github/CAISc_2026/
├── HANDOFF.md                        ← 이 파일
├── submission/
│   ├── main.tex                      ← 제출 대상 논문 (현재 18페이지, 8로 압축 필요)
│   ├── references.bib
│   └── neurips_2024.sty
└── simulation/
    ├── CONTEXT.md                    ← 실험 컨텍스트 문서
    ├── main.tex                      ← 미완성 스켈레톤 (이번 제출에 사용 안 함)
    ├── references.bib
    ├── neurips_2024.sty
    └── src/
        └── simulation.py             ← 작동하는 시뮬레이션 코드
```

**원본 논문 위치:**
- 한국어본: `/Users/jaesolshin/Documents/GitHub/ai_scientist/paper/main_ko.tex`
- 영문본(동일): `/Users/jaesolshin/Documents/GitHub/ai_scientist/paper/main.tex`
- xelatex: `/usr/local/texlive/2026basic/bin/universal-darwin/xelatex`
- bibtex: `/usr/local/texlive/2026basic/bin/universal-darwin/bibtex`

---

## 3. 논문 정보

**제목:** Formalizing AI Scientist Systems: A Unified Framework for Automated Scientific Discovery  
**저자:** Jaesol Shin (WeDataLab, ysys143@wedatalab.com)  
**프레임워크:** SciAgent — (S, G, E, V, M, π)  
**핵심 주장:** V(검증기) 완결성이 AI Scientist 시스템의 가장 중요한 설계 변수

**현재 논문 섹션 구조 (18페이지):**
```
1. Introduction
2. Background (POMDP + BED)
3. Related Work
4. The SciAgent Framework        ← 핵심 기여, 유지
5. Analysis of Core AI Scientist Systems (5 서브섹션)
6. Domain Analysis (7 서브섹션 + Cross-Domain 표)
7. Open Problems (3 서브섹션)
8. Discussion
9. Conclusion
+ AI Involvement Checklist
+ Reproducibility Checklist
```

---

## 4. 해야 할 작업

### 4-A. 시뮬레이션 섹션 추가 (신규)

**목표:** paper_1의 §6(Open Problems) 앞에 새 섹션 삽입

**섹션 제목:** `\section{Illustrative Simulation: Validator Coverage and False Novelty}`

**프레이밍 (매우 중요 — Codex 검토 결과):**
- topology를 독립 주제로 제시하면 안 됨
- topology = V 완결성의 서로 다른 operationalization으로 정의
  - `isolated` = 로컬 메모리만 가진 불완전 V
  - `lattice` = 국소 지식 공유 가능한 부분 완결 V
  - `small_world` = 장거리 연결로 coverage 개선된 V
  - `shared` = 공통 문헌 접근 가능한 더 완결적 V
- FNR = "V 불완전성의 최소 실패 모드"로 정의
- 반드시 써야 할 표현: "illustrates one minimal mechanism by which V incompleteness produces systematic failure in autonomous scientific loops"
- 절대 쓰면 안 될 표현: "Our simulation validates/proves the central claim"

**시뮬레이션 실행 방법:**
```bash
cd /Users/jaesolshin/Documents/Github/CAISc_2026/simulation
uv run python src/simulation.py
```

**파일럿 결과 (n_seeds=3 기준):**
| 토폴로지 | FNR (평균) | True Recall |
|---------|-----------|-------------|
| isolated | ~0.96 | ~0.98 |
| lattice | ~0.27 | ~0.43 |
| small_world | ~0.04 | ~0.12 |
| shared | ~0.003 | ~0.007 |

**classifier_accuracy(0.6→0.9) 효과 < topology 효과 → V 구조가 개별 정확도보다 중요**

**논문에 넣을 내용:**
1. 에이전트 정의 (2-3문장)
2. 실험 조건 표
3. 결과 표 or 그림 1개 (FNR by topology)
4. 해석 + 한계 명시

### 4-B. 8페이지 압축

**주요 삭감 대상:**

| 섹션 | 현재 | 목표 | 방법 |
|------|------|------|------|
| §5 Domain Analysis | ~4p | ~0.4p | §5.1-5.7 서브섹션 전부 삭제, Cross-Domain 표만 유지 |
| §4 System Analysis | ~4p | ~1.0p | 2개 시스템 심층 유지, 나머지 표로 압축 |
| §2 Background | ~1p | ~0.5p | 핵심 수식만 유지 |
| §3 Related Work | ~1p | ~0.4p | 단락 압축 |

**삭감 금지:** Framework 섹션 (핵심 기여), Open Problems 섹션 (논문의 논점)

**목표 구조 (8페이지):**
```
1. Introduction          0.5p
2. Background            0.5p
3. Related Work          0.4p
4. Framework             1.5p  ← 유지
5. System Analysis       1.0p
6. Domain Analysis       0.4p  (표만)
7. Illustrative Sim.     1.0p  ← 신규
8. Open Problems         1.5p
9. Conclusion            0.3p
────────────────────────────
합계                     ~7.1p
```

### 4-C. 컴파일 확인

```bash
cd /Users/jaesolshin/Documents/Github/CAISc_2026/submission
/usr/local/texlive/2026basic/bin/universal-darwin/xelatex -interaction=nonstopmode main.tex
/usr/local/texlive/2026basic/bin/universal-darwin/bibtex main
/usr/local/texlive/2026basic/bin/universal-darwin/xelatex -interaction=nonstopmode main.tex
/usr/local/texlive/2026basic/bin/universal-darwin/xelatex -interaction=nonstopmode main.tex
grep "^!" main.log  # 오류 없어야 함
pdfinfo main.pdf | grep Pages  # 8 이하여야 함
```

---

## 5. 확정된 결정들

- **제출 트랙:** Track 2 (Open-Ended)
- **제출 유형:** Archival
- **언어:** 영어 (main.tex)
- **paper_2는 이번에 제출 안 함** — 별도 연구로 발전
- **시뮬레이션은 paper_1에 illustrative 섹션으로 통합**
- **새 논제("2부 리그, 지식 붕괴, 중간 게이트")는 별도 연구**

---

## 6. OpenReview 제출 폼 정보

> **[폐기됨 — 2026-07-19]** 아래 표는 2026-05-29 최초 제출 준비 시점의 것으로 **더 이상 유효하지 않다**.
> 제목이 카메라레디와 다르고("A Unified Framework…" vs 실제 "A Component Framework and Theoretical
> Analysis"), TL;DR은 카메라레디가 명시적으로 철회한 인과 주장을 담고 있다.
> **현재 유효한 메타데이터는 [`submission/OPENREVIEW_METADATA.md`](./submission/OPENREVIEW_METADATA.md)를 쓸 것.**

| 필드 | 내용 |
|------|------|
| Title | Formalizing AI Scientist Systems: A Unified Framework for Automated Scientific Discovery |
| Keywords | AI scientist, automated scientific discovery, POMDP, Bayesian experimental design, hypothesis generation, scientific automation, multi-agent systems, formal framework |
| TL;DR | A 6-component formal framework (S,G,E,V,M,π) for characterizing AI Scientist systems, revealing that validator completeness is the single most critical design variable for closed-loop autonomy. |
| Track | Track 2: Open-Ended Problems |
| Archival | Archival |
| Checklist | 두 체크리스트 모두 main.tex에 포함됨 (확인 완료) |

---

## 7. 시뮬레이션 시각화 (선택)

논문에 그림을 넣으려면:
```bash
cd /Users/jaesolshin/Documents/Github/CAISc_2026/simulation
uv add matplotlib  # 아직 설치 안 됨
uv run python src/plot_results.py  # 작성 필요
```

그림 내용: topology별 FNR 막대 그래프 (4개 토폴로지 × 3개 classifier_accuracy)

---

## 8. 주의사항

- 분량 삭제 전에 반드시 git commit으로 현재 상태 저장
- Domain Analysis 삭제 시 `\label{tab:domain-comparison}` 참조가 본문에 남아있는지 확인
- 시뮬레이션 섹션은 `\section*` 아닌 `\section`으로 — 체크리스트와 구분
- Codex 권고: claim을 낮추고 V completeness proxy로 재프레이밍하는 것이 핵심
