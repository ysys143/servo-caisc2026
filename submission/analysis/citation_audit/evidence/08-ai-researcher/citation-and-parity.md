# AI-Researcher: citation and parity audit

## Audit boundary

- **Audited source:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/AI-Researcher Autonomous Scientific Innovation.pdf`
- **Source identity:** Jiabin Tang, Lianghao Xia, Zhonghang Li, and Chao Huang, *AI-Researcher: Autonomous Scientific Innovation*, arXiv:2505.18705v1, 24 May 2025. PDF-internal title and authors are on p. 1; the file contains 38 pages.
- **Scope restriction:** This audit directly read this PDF from p. 1 through p. 38. No API/model call was used and no other paper PDF was opened for this audit.
- **Catalog status:** The source is used as a catalog entry for `ai_researcher`; the frozen description is in `submission/analysis/multicoder/systems_desc.json`.

## Frozen-description sentence audit

| Frozen sentence / claim | Direct PDF evidence | Adjudication | English/Korean parity |
|---|---|---|---|
| “An LLM pipeline for machine-learning research across a few domains.” | The paper describes an LLM-agent research pipeline (pp. 5-8). Scientist-Bench covers diffusion models, vector quantization, graph neural networks, and recommender systems (pp. 3, 9). | **CONFIRMED**, with “a few domains” appropriately conservative. | 한국어도 “소수의 머신러닝 연구 영역을 다루는 LLM 파이프라인”으로 동일한 범위여야 함. |
| “A knowledge-acquisition step reads reference papers to scope the problem” | Knowledge Acquisition Agent discovers relevant papers and code repositories; user supplies 10-15 reference papers; Resource Analyst extracts concepts, mathematics, and implementations (pp. 5-7). | **CONFIRMED**, but “scope the problem” is a concise paraphrase, not the paper’s exact wording. | 한국어가 “문제를 정의/해결한다”로 확장되면 과장. “문제 범위를 잡기 위한 문헌·코드 지식 획득”이 parity. |
| “a divergent-convergent step generates several research directions and selects one by novelty, soundness, and transformative-potential criteria” | Idea Generator produces and ranks ideas; the paper explicitly lists novelty, soundness, and transformative potential in the idea-ranking discussion (pp. 6-7). | **CONFIRMED**, subject to the paper’s own description. The phrase “selects one” should mean pipeline selection, not proof that the selected idea is novel. | 한국어는 “여러 방향을 생성·평가해 하나를 선택”으로 유지. “새로운 방향을 보장”은 불일치/과장. |
| “code and advisor agents implement and run experiments in containers with multi-stage refinement.” | Code Agent and Advisor Agent operate in progressive experimental cycles; prototype tests precede full experiments; the secure research environment is Docker-based (pp. 7-8). | **CONFIRMED**. The PDF supports implementation, execution, review, and iterative refinement. | 한국어도 “컨테이너 안에서 코드 작성·실험 실행·다단계 수정”이어야 하며, 물리 실험으로 읽히면 안 됨. |
| “Outputs were compared pairwise against human papers by several LLM judges on a benchmark.” | Scientist-Bench compares generated report `p` with human target `y` using random paper-order swapping and a 7-point rating (p. 4). Experiments use five LLM judges and 16 assessments per paper (p. 10). | **CONFIRMED**, with important qualifier: the comparison is LLM-based evaluation, not human peer review of every output. | 한국어는 “여러 LLM 심사자가 벤치마크의 인간 논문과 쌍대 비교”로 동일하게 써야 함. “전문가가 비교”는 과장. |
| “It uses no external memory beyond the model context” | Discussion 6.2 states the present implementation has no dedicated external memory and relies primarily on the LLM native context window (p. 19); p. 20 says details are compressed into summaries. | **CONFIRMED**. “Beyond the model context” is slightly stronger than “primarily” but is supported by the explicit “without a dedicated external memory management system.” | 한국어는 “전용 외부 메모리 시스템 없이 주로 모델의 context window에 의존”이 가장 정확. “외부 파일을 전혀 읽지 않는다”는 오역. |
| “the pipeline runs forward without feeding results back into ideation.” | The architecture is presented as sequential stages: literature/idea generation, implementation/validation, documentation (pp. 5, 8). The paper does describe Advisor feedback for additional experiments during implementation (p. 8), but it does not describe a result-to-ideation feedback loop. | **CONFIRMED as a bounded architectural reading**, not a verbatim claim. State “the paper does not document feedback from experimental results back into the ideation stage.” | 한국어는 “실험 결과를 아이디어 생성 단계로 되돌리는 루프는 문서화되어 있지 않다”가 parity. “결과 피드백이 전혀 없다”는 과장. |

## Overclaim checks

1. **Do not upgrade evaluation to human validation.** The paper reports LLM judges, random swapping, and alignment experiments on 64 ICLR submissions / 32 pairs (pp. 4-5). This is evidence about an automated reviewer, not independent human confirmation of AI-Researcher’s scientific claims.
2. **Do not call the outputs genuinely novel or human-level as established facts.** The abstract and conclusion use strong language (“approach human-level quality”; pp. 1, 20), but the same paper reports implementation correctness gaps (p. 10), lower correctness on Level-2 tasks (p. 11), failure cases in technical sophistication and theoretical analysis (pp. 16-18), and reviewer limitations (p. 20).
3. **Do not imply broad scientific coverage.** The evaluated benchmark has 22 papers across four listed research domains, with 22 Level-1 tasks and 6 Level-2 tasks (p. 9). “Across a few domains” is safer than “general scientific research.”
4. **Do not imply closed-loop ideation.** The paper documents implementation-stage review/refinement and Advisor recommendations (pp. 7-8), while its memory discussion says the system relies on summaries across stages (pp. 19-20). Neither passage establishes an experimental-results-to-new-idea loop.
5. **Do not imply external-memory persistence.** The paper explicitly identifies the absence of dedicated external memory as a limitation (p. 19), and information loss through summarization as a consequence (p. 20).

## Direct citation occurrence inventory

This inventory is for the audited PDF itself, not for the frozen description. The PDF has a numbered reference list [1]-[27] on pp. 21-22. Direct in-text citation occurrences were checked in the extracted full text and by page-level reading:

| Reference range | Direct occurrence locations and role |
|---|---|
| [1]-[3] | Introduction, p. 1: scientific discovery / LLM reasoning and coding context. |
| [4]-[7] | Introduction, p. 1: comparison with existing agentic task automation; related-work taxonomy, p. 18. |
| [8]-[9] | Introduction, p. 2 and benchmark motivation, p. 3: AgentRxiv and AI Co-Scientist as specialized/related systems. |
| [10]-[11] | Scientist-Bench motivation, p. 3: scientific-discovery benchmark context and comparison with SciBench. |
| [12]-[13] | Framework motivation, p. 5; related work, p. 18: AI Scientist and AI Scientist-v2. |
| [14]-[16] | Idea-generation discussion, p. 6: Chain of Ideas, ResearchAgent, and novelty-study context. |
| [17] | Automated documentation discussion, p. 8: hierarchical writing inspiration. |
| [18] | Evaluation protocol, p. 9: peer-review/LLM-review context. |
| [19]-[24] | Related work, p. 18: LangChain, HuggingGPT, OpenAgents, MetaGPT, AutoGen, and AgentScope. |
| [25]-[27] | Related work, pp. 18-19: CycleResearcher, AI Co-Scientist, and Agent Laboratory. |

**Inventory conclusion:** Each numbered reference [1]-[27] has at least one direct in-text occurrence in the paper’s body, with the reference entries themselves on pp. 21-22. The frozen `ai_researcher` description contains no inline citation marker and is therefore catalog prose, not a citation-bearing claim. Its claims must be kept bounded to this source’s own reported architecture and evaluation.

## Source-supported quantitative anchors

- Scientist-Bench: 22 papers total; 22 Level-1 tasks; 6 Level-2 tasks; four domain rows (p. 9).
- Claude-series completeness: 93.8% across the reported benchmark analysis; average correctness 2.65/5 (p. 10).
- Model comparison subset: Claude-series 87.5% completeness versus 4o-series 50%; correctness 2.75 versus 1.0 (pp. 10-11).
- Level-2 Claude-series result: 100% completeness, with correctness 2.25 versus 2.5 for Level 1 (p. 11).
- The paper reports five LLM judges and 16 independent assessments per paper (p. 10).

These numbers should not be silently generalized beyond the paper’s benchmark, model configurations, and reported evaluation protocol.

EVIDENCE_COMPLETE: yes
