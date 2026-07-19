# NovelSeek occurrence audit: citation and parity

## Audit boundary and method

- Audited source: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Reference/NovelSeek - When Agent Becomes the Scientist.pdf` only.
- The requested file is a 34-page PDF. `pdfinfo` reports the title `InternAgent: When Agent Becomes the Scientist -- Building Closed-Loop System from Hypothesis to Verification`, 34 pages, and letter page size. The first page identifies `InternAgent Team`, Shanghai Artificial Intelligence Laboratory, and arXiv:2505.16938v3 (22 Jul 2025).
- I read the extracted PDF text in page order from PDF page 1 through page 34, including references and appendices. Key pages were also rendered and visually checked for text placement and figure/caption context.
- No API call, model call, or other PDF opening was performed. Page references below are PDF page numbers.

## Source identity finding

The four manuscript records cite `zhang2025novelseek` and label the cited system **NovelSeek**, but the supplied PDF consistently presents **InternAgent**, not NovelSeek (title and author block, p. 1; system name throughout pp. 2-34). The PDF does support several of the factual propositions attributed to the occurrence, but it does not establish that the cited work is a NovelSeek paper. This is a source-identity/citation-key blocker independent of sentence-level entailment.

## Occurrence findings

### EN-C017

**Manuscript sentence/context** (`submission/main.tex`, Related Work, line 92):

> More recent unified frameworks include NovelSeek, a closed-loop multi-agent system spanning idea generation to verification across twelve scientific tasks, and Co-Scientist, a multi-agent hypothesis-generation system with experimental biomedical validation.

**PDF evidence:**

- p. 2 abstract: InternAgent is described as a “unified closed-loop multi-agent framework”; it is demonstrated across “12 scientific research tasks” and provides human-expert feedback and multi-agent interaction.
- p. 2 introduction: the proposed pipeline has self-evolving idea generation, human-interactive feedback, idea-to-methodology construction, and multi-round experiment planning/execution.
- p. 3: the authors say the framework was validated across 12 tasks and describe the research cycle as idea generation, idea-to-methodology transformation, experiment execution, and result feedback.
- p. 22 conclusion: the framework is described as completing a closed-loop process “from hypothesis generation to verification.”

**Judgment:** **PARTIALLY SUPPORTED / BLOCKED BY IDENTITY.** The predicate “closed-loop multi-agent,” “12 scientific research tasks,” and the broad idea-generation-to-verification scope are directly supported, although the exact phrase “spanning” is a reasonable compression of the pipeline. The claim is not supported as written because the supplied PDF is InternAgent, not NovelSeek. The citation also scopes the same sentence over the adjacent Co-Scientist claim; that latter claim is not evidence supplied by this PDF and needs its own source.

**Overclaim risk:** “across twelve scientific tasks” is acceptable only as the paper’s reported validation scope, not as a universal capability guarantee. “Verification” is computational experiment/result validation in this paper; it should not be read as physical wet-lab or scientific-truth verification. The paper’s p. 2 introduction explicitly identifies real-world experimental validation as a challenge.

### EN-C025

**Manuscript caption** (`submission/main.tex`, Analysis of Core AI Scientist Systems, line 162):

> Comparative framework analysis of core AI Scientist systems, including the pre-LLM Robot Scientist and the recent unified framework NovelSeek.

**PDF evidence:**

- p. 2 abstract: InternAgent is called a unified closed-loop multi-agent framework.
- p. 3 contribution statement: it is called a unified closed-loop scientific research framework that automates idea generation, idea-to-methodology transformation, experiment execution, and result feedback.
- p. 22 conclusion: it is called a closed-loop multi-agent framework and is said to support 12 types of scientific research tasks.

**Judgment:** **PARTIALLY SUPPORTED / BLOCKED BY IDENTITY.** The supplied PDF supports the generic characterization “recent unified [closed-loop] framework,” but not the name NovelSeek. The PDF does not support the comparative analysis itself, the Robot Scientist portion, or any framework labels in the table; those require the other cited sources and the authors’ own analysis. Citation scope is therefore too broad if `zhang2025novelseek` is intended to support the whole caption or the comparison.

**Overclaim risk:** “recent” is time-relative but consistent with the 22 Jul 2025 version date. “Unified” is source language. “Comparative framework analysis” is an analytical claim by the manuscript, not a result reported by this PDF.

### KO-C012

**Manuscript sentence/context** (`submission/main_ko.tex`, 관련 연구, line 111):

> 보다 최근의 통합 프레임워크로는 아이디어 생성에서 검증까지 12개 과학 과제에 걸친 폐루프 다중 에이전트 시스템 NovelSeek와 ... Co-Scientist ... 가 있다. ... 첫째, 표준 POMDP 분류와 NovelSeek의 다중 에이전트 프레임워크는 루프 폐쇄/개방을 구분하지만 ... 둘째, ...

**PDF evidence:** same direct evidence as EN-C017: pp. 2-3 and p. 22 support InternAgent’s unified closed-loop multi-agent design, 12 tasks, idea-generation pipeline, and hypothesis-to-verification endpoint.

**Judgment:** **PARTIALLY SUPPORTED / BLOCKED BY IDENTITY.** The factual architecture is supported only after replacing NovelSeek with InternAgent and narrowing “검증” to the paper’s computational/result-validation workflow. The citation scope is also too broad for the sentence’s Co-Scientist claim and for the later POMDP comparison: this PDF does not discuss the manuscript’s `V_present`, `V_gating`, POMDP classification, or the three-way diagnostic separation.

**EN/KO parity:** **INCOMPLETE.** The English context explicitly says the framework’s diagnostic value is “illustrated, not independently tested,” states that both AI Scientist systems are coded as closed-loop, and identifies two diagnostic points. The Korean context omits the English AI Scientist/gating sentence and compresses the qualification. The remaining two-point structure is present, but the omission changes the qualification and leaves the Korean version less explicit about what is source fact versus the manuscript’s own analysis.

### KO-C024

**Manuscript caption** (`submission/main_ko.tex`, 핵심 AI 과학자 시스템 분석, line 215):

> 핵심 AI 과학자 시스템의 비교 framework 분석(LLM 이전 Robot Scientist와 최근 통합 프레임워크 NovelSeek 포함).

**PDF evidence:** pp. 2-3 and p. 22 support the generic “recent unified closed-loop multi-agent framework” description, but identify it as InternAgent. No page in the PDF identifies NovelSeek or supports the Robot Scientist comparison.

**Judgment:** **PARTIALLY SUPPORTED / BLOCKED BY IDENTITY.** The citation can support only a generic system-description clause after correcting the source identity. It cannot, alone, support the comparison, Robot Scientist clause, or the table’s `V_s`, `V_e`, and `V_h` coding. Those are outside this PDF’s reported content.

**EN/KO parity:** **PASS for the cited caption content, conditional on identity correction.** EN-C025 and KO-C024 preserve the same two system references and the same “recent unified framework” relation. The Korean caption does not introduce an additional factual claim. Both nevertheless share the same source-identity and citation-scope blocker.

## Consolidated verdict

| occurrence | direct proposition support | citation scope | parity | verdict |
|---|---|---|---|---|
| EN-C017 | Partial: InternAgent’s closed-loop, 12-task, idea-to-verification description is supported | Too broad for adjacent Co-Scientist claim; identity mismatch | N/A | **BLOCKED** |
| EN-C025 | Partial: generic unified-framework description supported | Too broad for comparison/caption analysis | N/A | **BLOCKED** |
| KO-C012 | Partial: same bounded InternAgent description supported | Too broad for Co-Scientist and POMDP/framework analysis | Incomplete versus EN-C017 | **BLOCKED** |
| KO-C024 | Partial: generic unified-framework description supported | Too broad for Robot Scientist/comparative coding | Pass versus EN-C025, conditional | **BLOCKED** |

Required correction before publication: resolve the bibliographic identity/key so the citation points to the actual work being described. If this supplied PDF is intended, replace “NovelSeek” with “InternAgent” and cite the matching reference. Keep the citation attached only to the InternAgent proposition; cite Co-Scientist, Robot Scientist, and any POMDP/V-layer analysis separately. Align KO-C012 with EN-C017’s explicit qualification that the diagnostic analysis is manuscript analysis and not independently tested.

EVIDENCE_COMPLETE: yes
