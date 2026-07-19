# `zhang2025novelseek` 전문 인용 감사

## Source Identity

**최우선 blocker: manifest/system identity와 실제 PDF identity가 불일치한다.** Manifest와 citation key는 `novelseek` / `zhang2025novelseek`이고 파일명도 `NovelSeek - When Agent Becomes the Scientist.pdf`이지만, 공급된 PDF의 표제와 본문은 **InternAgent: When Agent Becomes the Scientist -- Building Closed-Loop System from Hypothesis to Verification**로 일관된다. 첫 페이지는 `InternAgent Team`, Shanghai Artificial Intelligence Laboratory, `arXiv:2505.16938v3 [cs.AI] 22 Jul 2025`를 식별한다. 따라서 이 감사에서 실제 source는 InternAgent로 기록하며, NovelSeek라는 frozen audit alias가 같은 작업의 이전 명칭인지 여부와 무관하게 현재 manifest/key가 실제 PDF bibliographic identity를 정확히 가리키는지는 해결되지 않았다.

- **Citation key:** `zhang2025novelseek`
- **Manifest system ID/name:** `novelseek` / `InternAgent / NovelSeek`
- **PDF path:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Reference/NovelSeek - When Agent Becomes the Scientist.pdf`
- **SHA-256:** `71619a734da64e3b84735fc18417316254fd08c0abeafaf9d8faa08abdd48843`
- **PDF page count:** 34
- **PDF identity:** InternAgent Team, Shanghai Artificial Intelligence Laboratory; `arXiv:2505.16938v3`; 2025
- **Version status:** `mismatch` for the frozen manifest/name versus the supplied PDF title/system identity. Bibliographic correction is required before publication.

이 blocker는 두 판단을 분리한다. (1) **citation occurrence의 오귀속/문장 entailment:** 실제 PDF가 InternAgent의 좁은 proposition을 지지하는가. (2) **frozen supplementary description의 적용 범위:** 그 description이 실제 PDF의 InternAgent system에 어느 범위까지 적용되는가. 후자는 대체로 지지되더라도, 그것이 NovelSeek라는 현재 citation identity를 치료하지 않는다.

## Full-Text Coverage

PDF p.1부터 p.34까지 본문, 표, 그림, 참고문헌, 부록과 software/application material을 페이지 순서로 검토했다. 주요 figure/table과 title/caption layout을 시각 확인했다. 본 감사는 지정된 단일 PDF만 사용했으며, 다른 PDF를 열지 않았고 API 호출이나 model 호출을 하지 않았다. 모든 page reference는 PDF page number다.

구조 범위는 p.1 title/overview, pp.2-3 abstract/introduction/contributions, pp.4-9 architecture and loop, pp.9-17 experiments/results/ablations, pp.18-22 case studies/human evaluation/related work/conclusion, pp.23-26 references, pp.27-30 appendices/software interface, pp.31-34 additional generated artifacts and interface material이다.

## Problem and Context

InternAgent는 autonomous scientific research에서 data analysis, hypothesis generation, experiment design, result interpretation을 연결하는 문제를 다룬다(pp.2-3). 저자들이 제시하는 핵심 어려움은 novel하면서도 valid하고 feasible한 idea를 생성하는 일과, 실행·분석·수정이 반복되는 closed-loop validation을 cross-domain task에서 수행하는 일이다. 시스템은 이를 self-evolving idea generation, human-interactive feedback, idea-to-methodology construction, multi-round experiment planning/execution의 결합으로 해결하려 한다.

이 source의 실험 맥락은 물리 실험실이 아니라 public dataset, baseline repository, generated code, GPU training, benchmark metric을 사용하는 computational AI/science task다(pp.1, 9-17, 22). 따라서 “verification”은 이 PDF에서 computational execution/result feedback의 범위로 읽어야 하며, physical wet-lab validation이나 일반적 scientific-truth verification으로 확장할 수 없다.

## Structure and Argument

논증은 다음 순서다.

1. pp.1-3에서 InternAgent를 12개 scientific research task에 적용하는 unified closed-loop multi-agent framework로 소개한다.
2. pp.4-7에서 Survey, Code Review, Idea Innovation, Assessment, Orchestration agent를 통한 self-evolving idea generation과 human/agent feedback을 설명한다.
3. p.8에서 idea를 executable methodology로 초기화·정제하는 Method Development Agent를 설명한다.
4. pp.8-9에서 planning, code generation, traceback-based debugging, execution log와 performance reflection을 연결한다.
5. pp.9-17에서 12개 computational benchmark의 task, baseline, metrics, results, ablations와 비교를 보고한다.
6. pp.18-22에서 case studies, human idea evaluation, limitations, future work와 conclusion을 제시한다.
7. pp.27-34에서 evaluation details와 software/application material을 제공한다.

저자 주장의 closed-loop는 idea -> methodology -> code/experiment -> result/performance feedback -> next plan의 computational loop다. 다만 문서가 physical laboratory loop를 시연하는 것은 아니다.

## Methods and Evidence

Architecture evidence는 pp.2-9에 있다. Survey Agent는 literature review, Code Review Agent는 repository context, Idea Innovation/Assessment Agent는 generation/evaluation, Orchestration Agent는 workflow와 feedback timing, Method Development Agent는 idea-to-methodology transformation을 담당한다. Human feedback과 agent-generated feedback이 별도 source로 설명되며(pp.6-7), human interaction은 capability/control point로 제시된다. “optional rather than required”는 agent feedback도 가능하다는 근거에서 도출되는 해석이지, full operation에 human이 절대 필요 없다는 명시적 operational guarantee는 아니다.

실험 setup은 survey 50 papers, initial 15 ideas, idea evolution과 top-5 selection, 최대 four evolution rounds, method initialization/refinement, code/debug run limits를 보고한다(p.12). 12개 task의 datasets, baselines, metrics는 pp.9-11에 있다. Main comparison은 task당 10 ideas와 improved/successful/tested counts를 사용한다(pp.13-14). DOLPHIN은 project-level multi-file baseline 일부를 수정하지 못해 비교가 불완전하며(Table 2, p.13), AutoVLM metric은 GPT-4o answer extraction에 의존한다(p.11).

## Findings

InternAgent가 보고한 maximum baseline comparison은 AutoRYP R2 35.4 대 27.6, AutoEAP HK-PCC 0.79 대 0.65, Auto2DCls accuracy 83.3 대 81.2, Auto2DSeg mIoU 81.0 대 78.8 등이다(Tables 1-2, p.13). 개선은 보편적이지 않다. 예를 들어 AutoPCDet은 2/5/10, AutoVLM은 1/5/10 improved/successful/tested다(Table 4, p.14). 따라서 source가 지지하는 것은 paper-reported computational benchmark improvement이지, 모든 idea의 실행·개선이나 일반화된 autonomous discovery가 아니다.

Adaptive Evolution ablation은 일부 task에서 result reflection과 replanning이 성능에 기여했다고 보고한다(Table 8, p.16). Human study는 네 task, task당 20 ideas, 다섯 qualified reviewers, 네 scoring dimension으로 idea quality를 평가한다(pp.20-21, 27-29). 이는 human-vs-agent scientific discovery나 physical-world confirmation의 증거가 아니다.

고정 supplementary description의 clause별 판정은 다음과 같다.

| Clause | 판정 | 범위 |
|---|---|---|
| unified multi-agent framework | `SUPPORTED` | InternAgent의 source language와 architecture(pp.2, 4-7) |
| idea generation | `SUPPORTED` | self-evolving idea generation(pp.4-7) |
| idea-to-methodology conversion | `SUPPORTED` | Section 2.2, p.8 |
| computational experiment execution | `SUPPORTED_WITH_QUALIFICATION` | 12개 computational task로 한정(pp.9-17) |
| result feedback in a loop | `SUPPORTED_WITH_QUALIFICATION` | performance/log feedback과 adaptive planning은 지지되나 physical loop는 아님(pp.3-4, 8-9) |
| across many tasks | `SUPPORTED` | 정확히 12 scientific research tasks(pp.1, 9-12) |
| improvements relative to baselines | `SUPPORTED_WITH_QUALIFICATION` | paper-reported results이며 성공/개선률은 task별로 불균등(pp.13-17) |
| human interaction optional rather than required | `PARTIAL` | human feedback와 agent feedback의 병존은 지지되나 categorical optionality는 명시되지 않음(pp.6-7, 34) |
| experiments are computational | `SUPPORTED` | physical/wet-lab experiment는 보고되지 않음(pp.9-17, 22) |

Frozen description verdict: **`major_revision` for identity and wording**. InternAgent에 적용하면 substantive architecture description은 대체로 맞지만, “optional rather than required”는 qualification이 필요하다. NovelSeek라는 manifest/key identity를 유지한 채 적용하는 것은 source-identity blocker 때문에 publication-ready가 아니다.

## Limitations

저자들은 retrieval/knowledge representation, agent feedback adaptation, discovery benchmark와 generalization을 future work로 남긴다(p.22). 이 감사상 중요한 제한은 computational-only validation, task별 uneven execution/improvement, DOLPHIN과 AI-Scientist-V2 비교의 missing/unavailable cells, GPU/API/model dependence, AutoVLM의 model-based answer extraction, controlled human comparison 부재다(pp.11, 13-17, 20-22, 29). “12 tasks”는 breadth를 보이지만 physical-world autonomy, universal generalization, calibrated novelty gate를 입증하지 않는다.

## Citation Assessments

### Source-identity rule

네 occurrence 모두에서 먼저 identity를 판정한다. 실제 PDF가 InternAgent proposition을 지지하는지와, 원고가 이를 NovelSeek로 귀속한 것이 맞는지는 별도다. 따라서 아래 `BLOCKED`는 단순 sentence entailment 실패가 아니라 **mismatch identity가 해결되지 않은 publication blocker**를 포함한다.

### EN-C017: `PARTIAL`, severity `critical`, `BLOCKED`

`submission/main.tex:92`의 문장은 NovelSeek가 idea generation부터 verification까지 12개 task를 아우르는 closed-loop multi-agent system이고, 같은 citation scope에 Co-Scientist claim도 포함한다. InternAgent의 unified closed-loop framework, 12 tasks, idea-to-methodology, execution/result feedback은 pp.2-3, 22가 지지한다. 그러나 PDF는 NovelSeek가 아니라 InternAgent다. 또한 이 PDF는 인접한 Co-Scientist biomedical claim을 지지하지 않는다. “verification”은 computational/result validation으로 좁혀야 한다.

**Correction:** bibliography/key를 실제 InternAgent identity로 수정하고, citation을 InternAgent proposition에만 붙인다. Co-Scientist는 별도 source를 인용하며, “12 computational/scientific research tasks”와 computational verification 범위를 명시한다.

### EN-C025: `PARTIAL`, severity `critical`, `BLOCKED`

`submission/main.tex:162` caption은 pre-LLM Robot Scientist와 recent unified framework NovelSeek를 comparative framework analysis에 포함한다고 말한다. PDF pp.2-3, 22는 generic unified closed-loop framework description만 지지하고 InternAgent identity를 제시한다. Robot Scientist inclusion, comparison, table의 SERVO labels는 이 source가 단독으로 지지하지 않는다.

**Correction:** identity를 수정한 citation을 generic InternAgent description에만 anchor한다. Robot Scientist와 comparative coding은 해당 source와 manuscript authors' analysis로 분리한다.

### KO-C012: `PARTIAL`, severity `critical`, `BLOCKED`; parity `INCOMPLETE`

`submission/main_ko.tex:111`은 EN-C017과 같은 12-task closed-loop description을 포함하고, 뒤에서 POMDP, `V_present`, `V_gating` 및 diagnostic separation을 NovelSeek framework와 연결한다. pp.2-3, 22는 InternAgent의 bounded architecture만 지지하며 POMDP/V-layer analysis는 지지하지 않는다. 또한 Co-Scientist claim과 citation scope가 섞여 있다.

영어에는 diagnostic value가 “illustrated, not independently tested”라는 qualification과 AI Scientist/gating 설명이 있으나 한국어는 이를 압축·생략한다. 따라서 parity는 완전한 equivalent가 아니다.

**Correction:** InternAgent proposition, Co-Scientist proposition, manuscript-level POMDP/V-layer interpretation을 문장과 citation으로 분리하고, 한국어에도 “본 논문의 분석이며 독립 검증되지 않음”을 명시한다.

### KO-C024: `PARTIAL`, severity `critical`, `BLOCKED`; parity `PASS conditional`

`submission/main_ko.tex:215` caption은 EN-C025와 동일하게 Robot Scientist와 recent unified framework NovelSeek를 comparative analysis에 넣는다. InternAgent의 generic framework description은 pp.2-3, 22가 지지하지만 NovelSeek identity와 Robot Scientist comparison/table coding은 지지하지 않는다. EN-C025와 cited caption content의 관계는 의미상 equivalent이며, identity correction을 조건으로 parity는 `PASS`다.

**Correction:** EN-C025와 동일하게 source identity와 citation scope를 고친다.

### Consolidated occurrence table

| ID | Direct proposition | Scope/identity | Korean parity | Verdict |
|---|---|---|---|---|
| EN-C017 | InternAgent의 bounded architecture는 partial support | Co-Scientist scope 혼합 + identity mismatch | N/A | `BLOCKED` |
| EN-C025 | generic unified-framework clause만 partial support | comparison/Robot Scientist/table 전체로 과도함 + mismatch | N/A | `BLOCKED` |
| KO-C012 | EN-C017과 같은 bounded support | POMDP/V-layer와 Co-Scientist까지 확장 + mismatch | `INCOMPLETE` | `BLOCKED` |
| KO-C024 | generic clause만 partial support | comparison/Robot Scientist/table 전체로 과도함 + mismatch | `PASS conditional` | `BLOCKED` |

## Korean Parity

EN-C017/KO-C012는 핵심 InternAgent description은 대응하지만, KO-C012가 영어의 explicit qualification과 gating-context를 생략하므로 `INCOMPLETE`다. EN-C025/KO-C024는 “Robot Scientist와 recent unified framework를 비교한다”는 caption 구조와 두 system reference를 유지하므로 `PASS conditional on identity correction`이다. 한국어 occurrence가 source identity mismatch를 완화하지는 않는다. 양 언어 모두 Co-Scientist, Robot Scientist, POMDP/V-layer/framework coding의 joint or manuscript-level claims를 이 PDF 하나에 과도하게 걸고 있다.

## Overall Verdict

**Overall verdict: `citation_invalid` as currently keyed/attributed; `major_revision` after identity correction.**

source-identity blocker가 최우선이다. 현재 manifest/system_id/citation key가 NovelSeek를 가리키지만 공급된 PDF는 InternAgent이며, 이 mismatch가 해결되기 전에는 네 citation occurrence를 publication-ready로 승인할 수 없다. 그렇다고 source content가 전부 무관한 것은 아니다. 실제 PDF는 InternAgent의 unified closed-loop multi-agent computational framework, idea-to-methodology transformation, result feedback, 12-task benchmark scope와 paper-reported improvements를 지지한다. 따라서 identity/key를 실제 work와 일치시키고 citation scope를 좁히면 source-specific proposition은 `SUPPORTED` 또는 `SUPPORTED_WITH_QUALIFICATION`으로 회복될 수 있다.

오귀속과 frozen-description 적용 범위는 분리해서 판정해야 한다. Frozen description은 InternAgent에 대해 architecture-level로 대체로 맞지만 human optionality는 partial이고 computational scope를 명시해야 한다. 이 substantive fit은 NovelSeek라는 현재 source identity를 승인하는 근거가 아니다. Co-Scientist, Robot Scientist, POMDP/V-layer interpretation, comparative table coding은 별도 citation 또는 manuscript-level analysis로 분리해야 한다.

## Completion Checklist

- [x] RUBRIC의 필수 heading 11개를 정확한 이름으로 사용했다.
- [x] manifest의 system ID, citation key, PDF path, SHA-256, page count와 PDF 자체 identity를 대조했다.
- [x] source-identity mismatch를 citation entailment 및 frozen-description 적용 범위와 분리 판정했다.
- [x] PDF p.1부터 p.34까지 본문, 참고문헌, 부록과 software/application material을 페이지 순서로 검토했다.
- [x] 지정된 단일 PDF만 사용했으며 API/model call과 다른 PDF 열람을 하지 않았다.
- [x] problem/context, historical/disciplinary context, prior-work relation, structure, methods, evidence, findings와 limitations를 분석했다.
- [x] 12 task 범위, benchmark comparison, improved/successful/tested counts, human idea study와 computational-only limitation을 기록했다.
- [x] frozen supplementary description의 모든 핵심 clause를 별도 판정했다.
- [x] EN-C017, EN-C025, KO-C012, KO-C024를 각각 line/context, evidence, scope, severity, correction과 함께 판정했다.
- [x] EN/KO parity를 `INCOMPLETE` 및 conditional `PASS`로 분리 기록했다.
- [x] source author claims와 manuscript-level POMDP/V-layer/comparative interpretation을 분리했다.
- [x] terminal markers의 page range와 네 manifest link ID를 기록했다.

AUDIT_COMPLETE: yes
PAGES_COVERED: 1-34
EN_LINKS_COVERED: EN-C017:zhang2025novelseek, EN-C025:zhang2025novelseek
KO_LINKS_COVERED: KO-C012:zhang2025novelseek, KO-C024:zhang2025novelseek
SYSTEM_DESCRIPTION_ASSESSED: yes
VERDICT: citation_invalid
