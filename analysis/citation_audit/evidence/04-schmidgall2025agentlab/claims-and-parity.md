# Agent Laboratory: Claim and Bilingual-Parity Evidence

## Assignment Boundary

- Active source: `agent_laboratory` / `schmidgall2025agentlab`
- Citation key: `schmidgall2025agentlab`
- PDF: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/Agent Laboratory - Using LLM Agents as Research Assistants.pdf`
- PDF SHA-256: `67b9543ae1d8e3ad86a65e2a436ddbd12700d7c8f4a66c5b4c2a6fccc1674d75`
- PDF pages: 84
- Stable identifier in PDF: arXiv `2501.04227v2` (`cs.HC`, 17 June 2025)
- Version status: `exact`
- API/model calls: none

The title, author list, arXiv identifier, page count, and hash agree with the
frozen inventory. No other source PDF was opened for this lane.

## Full-Text and Visual Coverage

I read PDF pages 1-84 in order. Coverage included:

- pp. 1-4: abstract, motivation, contributions, and related work;
- pp. 5-10: the complete literature-review, experimentation, `mle-solver`,
  `paper-solver`, report-refinement, and operating-mode descriptions;
- pp. 10-19: autonomous/co-pilot evaluation, automated-versus-human review,
  runtime/cost, and MLE-Bench experiments;
- pp. 19-22: limitations, failure modes, ethics, discussion, and conclusion;
- pp. 22-30: all references;
- p. 31: configuration, hyperparameters, and hardware;
- pp. 32-56: all base, context, role, command, solver, and reviewer prompts;
- pp. 57-84: all autonomous and co-pilot survey instruments.

I rendered and visually inspected PDF pp. 1, 5, 7, 8, 13, 17, 18, and 31.
These cover the human-input overview (Fig. 1), human-agent workflow (Fig. 2),
iterative code and paper loops (Figs. 3-4), automated-versus-human reviewer
results (Fig. 6), runtime/cost and MLE-Bench tables (Figs. 8-9), and the full
hyperparameter table (Table 1). The rendered layouts agree with the extracted
text and expose no table-column or caption ambiguity relevant to this audit.

## Source-Grounded System Characterization

Agent Laboratory is an end-to-end *research-assistance pipeline after a human
has supplied the research idea*, not an independent hypothesis generator.
This distinction is explicit and repeated:

- The abstract and Fig. 1 say that the framework accepts a human-provided
  research idea and notes (p. 1).
- The introduction contrasts Agent Laboratory with systems that perform
  research ideation "independent of human input" and says its purpose is to
  help scientists execute "their own research ideas" (p. 2).
- The workflow contains literature review, planning, data preparation, code
  generation/execution, result interpretation, writing, and refinement, but no
  upstream idea- or hypothesis-generation stage (pp. 5-10; Figs. 2-4).
- In autonomous mode, the only human involvement *after initiation* is absent,
  but a human still provides the initial research idea (p. 10). Calling this
  mode autonomous therefore does not license the stronger claim that the
  system independently originates hypotheses.
- The discussion again distinguishes the system from pipelines that conceive
  their own research directions and calls Agent Laboratory a co-pilot (p. 21).

The system does contain computational feedback loops. `mle-solver` edits and
executes code, uses an LLM reward model to score alignment with the supplied
plan/code/output, retains top programs, and self-reflects (pp. 6-7). The paper
refinement phase uses three LLM reviewers and can send work back to planning,
experimentation, or interpretation (p. 10; Table 1 on p. 31). These loops refine
execution of the supplied idea; they do not create an independent scientific
hypothesis or certify its novelty.

The reviewer includes an `Originality` score (pp. 9-10 and 50-56), but this is
not a reliable novelty gate. On the 15 autonomous papers, automated overall
scores averaged 6.1/10 while human PhD-student scores averaged 3.8/10, a
2.3-point overestimate, and the paper says human scores were not predicted by
automated scores (pp. 12-14; Fig. 6). The limitations further state that LLM
self-evaluation is unreliable for subjective tasks including research-idea
evaluation (p. 19). Literature retrieval is not a novelty certification
mechanism, and the paper reports no independent automated novelty test.

## Occurrence Assessments

### EN-C001:schmidgall2025agentlab

- Manuscript line/section: `submission/main.tex:69`, Introduction.
- Claim as applied to this source: Agent Laboratory is among rapidly
  proliferating "AI Scientist systems" defined as agents that *independently*
  generate hypotheses, execute experiments, and synthesize knowledge; the
  field lacks a shared formal vocabulary.
- Citation role: `joint` (background and class-membership claim).
- Joint-only support: `yes` for the plural proliferation trend. This one paper
  cannot establish a field-wide trend or the universal absence of a shared
  vocabulary. Joint citation cannot rescue the incorrect independent-ideation
  attribution for Agent Laboratory itself.
- Source evidence: pp. 1-2 require a human-provided idea; p. 2 expressly
  contrasts the system with agents that ideate independently; p. 10 defines
  autonomous mode as no human involvement *other than* the initial idea; p. 21
  calls the system a human-centric co-pilot. It does execute experiments and
  synthesize a report after that input (pp. 5-10).
- Entailment: `CONTRADICTED`.
- Severity: `major`.
- Scope/attribution reasoning: The sentence's appositive is a class definition,
  not a loose description. Agent Laboratory does not satisfy its independent
  hypothesis-generation component. Inferring otherwise from the paper's use of
  "autonomous" strips away the explicit initial-human-idea condition. The
  source also does not itself prove a field-wide absence of formal vocabulary.
- Proposed correction: "AI Scientist and research-assistant systems - ranging
  from human-directed pipelines that execute supplied ideas to agents that
  generate hypotheses independently - have proliferated rapidly, while this
  paper identifies the lack of a shared comparison vocabulary."
- Korean parity: `equivalent` to `KO-C001`; both versions preserve the same
  independent-generation overclaim.

### EN-C013:schmidgall2025agentlab

- Manuscript line/section: `submission/main.tex:90`, Related Work.
- Claim as applied to this source: prior work provides qualitative
  characterizations of individual systems but no shared framework for
  cross-system comparison.
- Citation role: `joint` (background characterization).
- Joint-only support: `yes` for the plural statement that the cited papers are
  individual-system studies. The field-wide absence claim is the manuscript's
  survey synthesis and is not established merely because this paper is silent
  about a shared framework.
- Source evidence: the paper is a detailed characterization and evaluation of
  Agent Laboratory alone (pp. 1-22), with comparisons to selected prior systems
  in related work and discussion (pp. 4-5, 21-22). It proposes no formal
  cross-system taxonomy.
- Entailment: `PARTIAL`.
- Severity: `minor`.
- Scope/attribution reasoning: This source directly supports the
  individual-system-characterization half. It can illustrate that *this paper*
  does not supply a common taxonomy, but cannot prove the universal negative
  that no shared framework exists anywhere in the field.
- Proposed correction: "These studies characterize individual systems; we use
  them as source material for the cross-system vocabulary introduced here."
  Treat the broader absence statement as the present survey's conclusion rather
  than as a fact directly entailed by each citation.
- Korean parity: `equivalent` to `KO-C008`; the two sentences carry the same
  supported first clause and the same over-broad absence attribution.

### KO-C001:schmidgall2025agentlab

- Manuscript line/section: `submission/main_ko.tex:88`, 서론.
- Claim as applied to this source: Agent Laboratory belongs to a class defined
  as agents that independently generate hypotheses, execute experiments, and
  synthesize knowledge, and that class is rapidly expanding while lacking a
  common formal vocabulary.
- Citation role: `joint` (background and class-membership claim).
- Joint-only support: `yes` only for a plural trend; `no` for attributing
  independent hypothesis generation to this source.
- Source evidence: human-provided idea and notes (p. 1); explicit contrast with
  independent ideation (p. 2); initial idea still supplied by a human in
  autonomous mode (p. 10); co-pilot positioning (p. 21).
- Entailment: `CONTRADICTED`.
- Severity: `major`.
- Scope/attribution reasoning: `독립적으로 생성` is as strong as the English
  wording and conflicts with the documented system boundary. Planning an
  implementation inside a supplied topic is not independent hypothesis
  generation.
- Proposed correction: "AI 과학자 및 연구 보조 시스템 - 인간이 제시한
  아이디어를 실행하는 파이프라인부터 가설을 독립적으로 생성하는
  에이전트까지 - 은 빠르게 증가하고 있으며, 본 논문은 이들을 비교할 공통
  형식 어휘의 필요성을 제기한다."
- Korean parity: `equivalent` to `EN-C001`; no translation-only repair is
  available because both versions require the same substantive correction.

### KO-C008:schmidgall2025agentlab

- Manuscript line/section: `submission/main_ko.tex:109`, 관련 연구.
- Claim as applied to this source: the cited prior work qualitatively
  characterizes individual systems but supplies no common cross-system
  framework.
- Citation role: `joint` (background characterization).
- Joint-only support: `yes` for identifying a set of individual-system papers;
  the universal absence claim remains author synthesis.
- Source evidence: Agent Laboratory alone is the object of the method,
  evaluation, limitations, and discussion (pp. 1-22); no cross-system formal
  framework is proposed.
- Entailment: `PARTIAL`.
- Severity: `minor`.
- Scope/attribution reasoning: The individual-characterization clause is
  accurate. Silence in one paper cannot establish that the entire field lacks a
  common framework.
- Proposed correction: "이 연구들은 개별 시스템을 정성적으로 특성화하며,
  본 논문은 이를 교차 시스템 어휘를 구성하기 위한 자료로 사용한다."
- Korean parity: `equivalent` to `EN-C013`.

### KO-C022:schmidgall2025agentlab

- Manuscript line/section: `submission/main_ko.tex:195`, 핵심 AI 과학자 시스템
  분석.
- Claim as applied to this source: Agent Laboratory is one of four end-to-end
  systems to which the manuscript applies SERVO; across the small sample,
  closed-loop operation co-occurs with more complete validators while `G`, `E`,
  and `pi` also advance.
- Citation role: `joint` (system identification plus interpretive synthesis).
- Joint-only support: `yes`. This source can supply only the Agent Laboratory
  datum. The four-system association and SERVO mapping require the other
  sources and the manuscript's coding; they are not findings of Schmidgall et
  al.
- Source evidence: the paper calls its process an entire/end-to-end workflow
  from a supplied idea to code and report (pp. 1, 10), and documents iterative
  code and report-refinement loops (pp. 6-10). It also shows that the reviewer
  channel is unreliable (`+2.3` overall-score overestimate, pp. 12-14) and that
  human input improves output (pp. 14-16, 21). The source never claims an
  independent hypothesis-generation loop or a trustworthy acceptance gate.
- Entailment: `SUPPORTED_WITH_QUALIFICATION`.
- Severity: `minor`.
- Scope/attribution reasoning: "End-to-end" is defensible only with the
  starting boundary stated: human-supplied idea to generated code/report. The
  cross-system correlation is a SERVO interpretation, not a result that this
  paper independently entails. Its computational refinement loop should not be
  conflated with autonomous scientific ideation or reliable closure.
- Proposed correction: "본 프레임워크를 인간이 제시한 아이디어에서
  출발하는 Agent Laboratory를 포함한 네 개의 엔드투엔드 실행
  파이프라인에 적용한다. 이어지는 폐루프-검증기 관계는 이 논문들의 직접
  결론이 아니라 본 조사의 잠정적 교차 시스템 코딩이다."
- Korean parity: `added`. There is no `schmidgall2025agentlab` occurrence paired
  with this Korean citation in the English manifest. The English manuscript has
  related uncited cross-system synthesis, but not an equivalent keyed occurrence,
  so citation-layer parity is asymmetric.

## Bilingual Reconciliation

| English occurrence | Korean occurrence | Parity | Result |
|---|---|---|---|
| `EN-C001` | `KO-C001` | `equivalent` | Same class definition and same major misclassification of Agent Laboratory as independently ideating. |
| `EN-C013` | `KO-C008` | `equivalent` | Same supported individual-study clause and same unsupported universal absence attribution. |
| none | `KO-C022` | `added` | Korean adds an explicit Agent Laboratory citation to a cross-system SERVO synthesis; English has no paired keyed occurrence. |

There is no case where the Korean translation alone creates or repairs the
human-directed-versus-independent-ideation distinction. The major issue is
shared by both language versions at `C001`.

## Lane Verdict

Overall verdict for the five occurrences: `major_revision`.

The source is valid evidence for a recent human-directed research assistant
that automates literature review, experiment implementation/execution, result
interpretation, and report drafting after receiving a human idea. It is not
valid evidence that Agent Laboratory independently generates hypotheses. The
related-work occurrences remain usable after narrowing universal absence
language, and the Korean-only core-system occurrence is usable if its
human-supplied starting point and manuscript-level interpretive status are made
explicit.

PAGES_COVERED: 1-84
EN_LINKS_COVERED: EN-C001, EN-C013
KO_LINKS_COVERED: KO-C001, KO-C008, KO-C022
EVIDENCE_COMPLETE: yes
