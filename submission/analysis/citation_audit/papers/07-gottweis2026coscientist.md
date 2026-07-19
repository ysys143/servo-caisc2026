# `gottweis2026coscientist` Full-Text Audit

## Source Identity

- **Citation key:** `gottweis2026coscientist`
- **PDF title:** *Towards an AI co-scientist* (PDF p. 1)
- **Authors:** Juraj Gottweis et al.; the title page lists Google Cloud AI Research, Google Research, Google DeepMind, Houston Methodist, Sequome, the Fleming Initiative/Imperial College London, and Stanford University School of Medicine (p. 1).
- **Identifier/version:** `arXiv:2502.18864v1` (PDF p. 1); DOI: not recorded in the frozen evidence.
- **Absolute PDF path:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/Towards an AI Co-Scientist (Google).pdf`
- **SHA-256:** `80730ea110ad450411aa8352a785e996cfcda06afd6e1c60277cb64a65cb676a`
- **PDF properties:** 81 pages. The supplied evidence identifies the PDF as the exact audited artifact.
- **Version status:** `same_work_preprint` in the core14 manifest. This report audits only this 81-page preprint and does not use the v2/Nature paper, a companion report, or any other PDF as evidence.
- **System identity:** A Gemini 2.0-based multi-agent assistant for scientist-specified hypothesis and proposal generation, not an autonomous end-to-end scientist (pp. 1-4, 30-33).

## Full-Text Coverage

PDF pages **1-81** were read sequentially, including main text, figures and captions, appendices, prompts, supplementary experiments, and references. Coverage was: pp. 1-4 abstract/introduction; pp. 5-13 related work and architecture; pp. 14-19 automated, expert, and safety evaluation; pp. 20-27 AML, liver fibrosis, and cf-PICI cases; pp. 28-33 limitations, safety, discussion, and conclusion; pp. 34-38 references; pp. 39-59 appendix prompts and worked pipeline; pp. 60-63 DepMap/AML methods and results; pp. 64-79 Specific Aims evaluation and KIRA6 proposal; pp. 80-81 AlphaFold example and appendix references. The page references below are PDF pages.

## Problem and Context

The paper addresses how AI can assist scientific hypothesis generation and experimental planning while retaining rigorous downstream validation. It frames discovery as a scientist-led process in which a research goal, constraints, and preferences are supplied to a system that searches literature, generates hypotheses and protocols, critiques them, and presents a research overview for human judgment (pp. 2-4, 7-13).

The disciplinary context is multi-agent LLM reasoning, test-time compute scaling, scientific literature grounding, biomedical hypothesis generation, and wet-lab follow-up. The paper distinguishes its scientist-in-the-loop assistant from complete automation and from prior systems that lack broad literature reasoning, iterative debate/evolution, or biological validation (pp. 3-7). Its demonstrated domains are drug repurposing for AML, liver-fibrosis target discovery, and antimicrobial-resistance-related cf-PICI mechanism explanation (pp. 3-4, 20-27).

## Structure and Argument

The document moves from identity and motivation (pp. 1-4), through related work (pp. 5-7), to system architecture (pp. 7-13), quantitative and expert evaluation (pp. 14-19), three biomedical cases (pp. 20-27), limitations and safety (pp. 28-30), and discussion/conclusion (pp. 31-33). The appendix exposes prompts and intermediate artifacts (pp. 39-59), computational and AML details (pp. 60-63), Specific Aims evaluations and a KIRA6 proposal (pp. 64-79), and an AlphaFold tool-use example (pp. 80-81).

The argument establishes an implemented generate-review-rank-evolve loop and then presents preliminary evidence that it can produce highly ranked hypotheses and selected biological signals. It does not establish autonomous science, objective superiority, or causal benefit from any individual agent or test-time-compute component.

## Methods and Evidence

An expert scientist supplies the research goal, constraints, preferences, and optional ideas or feedback (pp. 2, 7-8). A Supervisor assigns work to Generation, Reflection, Ranking, Proximity, Evolution, and Meta-review agents. Persistent memory stores agent/system state; literature search, private-publication retrieval, and auxiliary model/tool use provide grounding (pp. 7-13). The loop uses pairwise Elo tournaments, clustering/de-duplication, critique feedback, and iterative evolution. “Self-improving” is inference-time iteration and context feedback, not reported weight updating (pp. 1, 4, 9-13).

The automated evaluation used GPQA Diamond, reporting 78.4% top-1 accuracy after selecting the highest-Elo answer (p. 14). A 203-goal test-time-compute analysis showed increasing best and top-10 mean Elo over temporal buckets (p. 15). On 15 expert-curated goals, the paper reports comparisons against Gemini, OpenAI, DeepSeek, and expert solutions, but auto-Elo is not ground truth and may reward properties unrelated to scientific quality (pp. 15-16). In the 11-goal expert study, mean preference rank was 2.36, novelty 3.64/5, and impact 3.09/5; these ratings are subjective and small-scale (pp. 17-18). A preliminary unreleased adversarial set of 1,200 goals reportedly passed rejection checks (p. 19).

For AML, experts prioritized candidates from a constrained search over 2,300 approved drugs and 33 cancer types. Cell-line MTS assays used 5,000 cells/well for 48 hours; KIRA6 showed reported IC50 values of 13, 517, and 817 nM in KG-1, MOLM-13, and HL-60, respectively (pp. 20-24, 60-63). For liver fibrosis, experts selected three of 15 hypotheses; four drugs were tested in human hepatic organoids, and drugs based on two of three targets showed significant anti-fibrotic activity without cellular toxicity (p. 25). For cf-PICI, the system generated an in-silico mechanism in two days that matched an independent group's already-known experimental result; the co-scientist did not perform that bacterial wet-lab validation (pp. 26-27).

### Frozen supplementary description clause-by-clause assessment

Frozen clause: “A multi-agent system that, given a human-specified research goal, generates and iteratively refines hypotheses and experimental protocols.” **SUPPORTED** (minor qualification: scientist input is required and the output is a proposal/hypothesis workflow, not complete scientific execution; pp. 1-3, 7-13).

Frozen clause: “Generation, reflection (critique of correctness, quality, and novelty), and evolution agents are ranked by an automatic Elo tournament under a supervisor running an asynchronous task queue.” **PARTIAL, major.** Supervisor, asynchronous task execution, named agents, and automatic pairwise Elo ranking are supported (pp. 7-13). However, the source describes Ranking as the tournament agent; Generation, Reflection, and Evolution are not simply all “ranked by” one Elo tournament, and the full architecture also includes Proximity and Meta-review. Correction: “A Supervisor coordinates asynchronous Generation, Reflection, Ranking, Proximity, Evolution, and Meta-review agents; Ranking uses pairwise Elo tournaments and feedback is iterated through the loop.”

Frozen clause: “A scientist may give natural-language feedback but it is optional.” **CONTRADICTED, major.** The paper repeatedly makes the scientist-specified goal and constraints an entry requirement and defines the system as scientist-in-the-loop (pp. 2-3, 7-8). Ongoing chat feedback may be optional, but scientist input and expert guidance are not. Correction: “A scientist supplies the goal and constraints; additional natural-language feedback can guide iterations.”

Frozen clause: “The system does not execute experiments itself; physical wet-lab validation (cell lines, organoids, antimicrobial resistance) was carried out by independent laboratories.” **PARTIAL, major.** The system does not itself perform physical experiments, and AML/organoid work is human-run; the source says all three validations involved expert guidance/prioritization (pp. 14, 19-25). But the paper does not establish that every validation was carried out by independent laboratories, and the AMR case is an in-silico recapitulation of an independent result rather than a co-scientist wet-lab validation (pp. 26-27). Correction: “The system does not execute physical experiments; human researchers performed expert-guided AML and organoid validation, while the AMR case recapitulated an independent experiment in silico.”

Frozen clause: “Evaluated by domain experts across open research goals.” **SUPPORTED_WITH_QUALIFICATION** (pp. 14-18, 21). Domain experts curated 15 goals and evaluated 11, including 78 Specific Aims proposals assessed by six hematologists/oncologists (p. 21). The evaluation is small-scale, subjective, and supplemented by auto-Elo and LLM judges; it is not objective superiority evidence.

## Findings

- The paper supports a Gemini 2.0, multi-agent, asynchronous hypothesis/proposal assistant with literature/tool grounding, persistent context, tournament ranking, reflection, evolution, and meta-review (pp. 1, 7-13).
- The quantitative results are promising but metric-dependent: GPQA top-1 accuracy was 78.4%, and expert ratings on 11 goals were 2.36 preference rank, 3.64 novelty, and 3.09 impact (pp. 14-18).
- Selected expert-prioritized hypotheses produced AML cell-line activity and liver-organoid signals, not in-vivo or clinical efficacy (pp. 20-25, 60-63).
- The AMR case is a two-day in-silico recapitulation of an independent experimental finding, not system-run wet-lab discovery (pp. 26-27).
- The appendix materially corroborates the named prompts and intermediate loop artifacts, but it is illustrative evidence rather than a complete reproducibility log (pp. 40-59).

## Limitations

The authors describe incomplete open-literature access, missed negative results, weak multimodal and large multi-omics evaluation, inherited LLM factuality/hallucination/bias, and preliminary metrics requiring broader independent evaluation (pp. 27-28). Elo is not ground truth; expert ratings are subjective and small-scale (pp. 15-18). AML cell-line results and organoid activity do not establish in-vivo efficacy, safety, pharmacokinetics, or clinical benefit (pp. 21, 25, 28). The system does not cover delivery, bioavailability, clinical-trial design, or complex drug interactions, and translational experts remain necessary (p. 28).

The workflow retains human selection and oversight: experts curate goals, prioritize experiments and candidates, run biological assays, and make final decisions (pp. 14, 19-25, 30-33). Safety checks, monitoring, logging, red teaming, and trusted testing are described, but the paper treats adversarial robustness, dual use, automation bias, and homogenization as unresolved governance and technical risks (pp. 28-32).

### Implications for SERVO

This is an audit-level mapping, not terminology claimed by the source. `S` maps to scientist-specified goals, constraints, hypotheses, and persistent research state; `G` to Generation, literature search, reflection, and Evolution; `E` to computational proposal/protocol construction and downstream human experiments; `V` to reviews, Elo/GPQA/expert evaluation, safety checks, and wet-lab readouts; `M` to persistent memory, research overviews, reviews, and tournament feedback; and `pi` to Supervisor scheduling, Ranking, Proximity, and Evolution. The mapping must preserve that physical experiments and final scientific decisions remain human-led, and that the AMR result is independent-study recapitulation rather than system-run validation.

## Citation Assessments

### EN-C018:gottweis2026coscientist

- **Manuscript claim/role:** “Co-Scientist, a multi-agent hypothesis-generation system with experimental biomedical validation.” Role: `direct` system identification; the surrounding English paragraph contains separate framework-positioning and diagnostic claims.
- **Evidence:** multi-agent identity and Gemini 2.0 (p. 1; pp. 7-9); wet-lab validation framing and expert prioritization (p. 14); AML and liver-organoid results (pp. 19-25); AMR in-silico recapitulation boundary (pp. 26-27).
- **Verdict:** `SUPPORTED_WITH_QUALIFICATION`; severity `minor` for the narrow clause. The citation is valid, but “experimental biomedical validation” should not imply autonomous system-run wet-lab work or clinical validation. Recommended wording: “a multi-agent hypothesis-generation system with expert-guided biomedical validation, including AML in-vitro and liver-organoid experiments; its AMR example recapitulated an independent experimental finding in silico.”
- **Scope:** The citation does not establish the surrounding manuscript's framework novelty, V-layer decomposition, or comparative diagnostic claims; those require separate support.

### KO-C013:gottweis2026coscientist

- **Manuscript claim/role:** Korean shortened rendering of the same local claim, “다중 에이전트 가설 생성 시스템” with “생물의학 wet-lab 검증.” Role: `direct`.
- **Evidence and parity:** The two predicates are locally equivalent to the English clause and do not add autonomy, clinical, or quantitative claims. Verdict: `SUPPORTED_WITH_QUALIFICATION`; severity `minor`.
- **Parity finding:** `meaning_shifted` risk is limited but real: “wet-lab 검증” narrows the source's mixed evidence, especially because AMR is in-silico recapitulation of independent experimental work. Both EN and KO omit nearby expert guidance/prioritization (p. 14); this is an omitted qualification, not a contradiction. KO also compresses surrounding English claims and is not fully claim-by-claim parallel.
- **Recommended Korean correction:** “전문가가 실험 우선순위를 정한 생물의학 실험 검증을 포함하는 다중 에이전트 가설 생성 시스템(AML 세포 및 인간 간 오가노이드의 in-vitro 검증 포함); AMR 사례는 독립 연구의 실험 결과를 in-silico로 재현했다.”

## Korean Parity

The cited EN and KO clauses are locally semantically aligned and both are appropriate only with the same human-boundary qualification. KO-C013 is a shortened translation of the surrounding English paragraph: it omits English framework-diagnostic material and compresses comparison language. This is not a citation-invalidating discrepancy, but it prevents full paragraph-level parity. The most important parity repair is to distinguish expert-guided AML/organoid experiments from the AMR in-silico recapitulation and independent experiment.

## Overall Verdict

**MINOR_REVISION.** The source identity and full-text evidence are complete, and both citation occurrences are substantively appropriate for the narrow description of a multi-agent hypothesis-generation system with biomedical experimental evidence. The frozen supplementary description contains two major scope defects: it makes scientist feedback sound optional at the input boundary and overstates the common “independent laboratories” characterization of the three validations. The English and Korean manuscript citations should retain an expert-guided, mixed-validation qualifier. This audit does not support autonomous end-to-end science, objective superiority, clinical efficacy, or physical closed-loop experimentation. The v2/Nature relationship is deliberately outside this report's evidentiary scope.

## Completion Checklist

- [x] Source identity, citation key, identifier, absolute PDF path, SHA-256, page count, and version status recorded.
- [x] PDF pages 1-81 covered in order, including appendices and references.
- [x] Research problem, context, prior-work relation, structure, methods, findings, limitations, and SERVO implications assessed.
- [x] Frozen supplementary description evaluated clause by clause.
- [x] EN-C018 and KO-C013 assessed with page-grounded evidence, roles, verdicts, severity, corrections, and parity.
- [x] Human-intervention and AMR independent-validation boundaries recorded.
- [x] No API/model calls made; no other PDF used for this report.
- [x] System description assessed against the full source and appendix.

AUDIT_COMPLETE: yes
PAGES_COVERED: 1-81
EN_LINKS_COVERED: EN-C018:gottweis2026coscientist
KO_LINKS_COVERED: KO-C013:gottweis2026coscientist
SYSTEM_DESCRIPTION_ASSESSED: yes
VERDICT: minor_revision
