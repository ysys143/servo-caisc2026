# Identity and architecture audit: Towards an AI co-scientist (Google)

## Audit boundary

- Source read: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/Towards an AI Co-Scientist (Google).pdf`.
- The PDF has 81 pages. Page numbers below are PDF page numbers, including the reference pages and the appendix.
- This note uses the target PDF only. No API/model call was made and no other paper was read for this lane.
- The PDF is an article plus its own appendix, not a separate frozen implementation specification. The appendix is therefore treated as the paper's frozen supplementary description and checked against the main-text identity and architecture.

## Identity

The paper is titled **Towards an AI co-scientist** (p. 1). The author list is led by Juraj Gottweis and Wei-Hung Weng, with affiliations spanning Google Cloud AI Research, Google Research, Google DeepMind, Houston Methodist, Sequome, the Fleming Initiative/Imperial College London, and Stanford University School of Medicine (p. 1). The system is explicitly a **multi-agent system built on Gemini 2.0**, intended to help scientists formulate original, testable hypotheses and proposals from scientist-provided objectives and guidance (p. 1).

The identity is not “an autonomous scientist that completes the scientific process.” The paper defines an assistant/collaborator: a scientist supplies the research goal, preferences, constraints, ideas, reviews, and chat feedback; the system generates, reviews, debates, evolves, and summarizes hypotheses for the scientist (pp. 2-3). The paper says the work does not aim to completely automate the scientific process and emphasizes downstream validation and scientist oversight (pp. 3-4, 30-33).

The central design claim is a generate-debate-evolve loop accelerated by test-time compute scaling (pp. 1, 4). The demonstrated scope is primarily biomedical and scientific hypothesis generation, proposal formulation, literature-grounded reasoning, and experimental planning. The main validation cases are: drug repurposing for acute myeloid leukemia (AML), target discovery for liver fibrosis, and recapitulation of a mechanism in antimicrobial-resistance-related bacterial evolution (pp. 2-4, 20-27).

## Whole-paper structure and problem framing

| PDF pages | Structure and evidentiary role |
|---|---|
| 1 | Title, authors/affiliations, abstract, contribution framing. Establishes Gemini 2.0 multi-agent identity and generate/debate/evolve idea. |
| 2 | Figure 1 system overview. Shows scientist inputs, agents, tool use, research overview, and the AML/liver-fibrosis/cf-PICI narrative. |
| 3-4 | Introduction. Frames scientific discovery as hypothesis generation followed by rigorous experimental validation; motivates assistance across disciplines and gives the three validation directions. |
| 5-7 | Related work: reasoning/test-time compute, scientific hypothesis generation, AI for biomedicine, and comparison to prior LLM-agent systems. This is context, not evidence that the present system itself has those prior systems' capabilities. |
| 7-13 | Section 3, technical system description: criteria, plan configuration, supervisor/worker architecture, persistent memory, specialized agents, iteration, ranking/evolution, and research overview. |
| 14-19 | Section 4.1-4.3: evaluation setup, Elo/GPQA calibration, test-time-compute scaling, expert and LLM preference evaluations, and adversarial research-goal rejection. |
| 20-25 | Section 4.4-4.6: computational/DepMap-assisted drug repurposing, expert evaluation, AML in-vitro validation, and liver-fibrosis target discovery with human hepatic organoids. |
| 26-27 | Section 4.7: cf-PICI antimicrobial-resistance mechanism recapitulation and its temporal/knowledge-access qualification. |
| 28-30 | Limitations, safety, adversarial robustness, human oversight, and future work. |
| 31-33 | Discussion and conclusion. Reasserts evidence-grounded novelty, experimental validation, augmentation rather than replacement, and unresolved limitations. |
| 34-38 | References. |
| 39 | Appendix map and glossary start. |
| 40-46 | Appendix A.2: frozen prompts for Generation, Reflection, Ranking, Evolution, and Meta-review agents. |
| 47-59 | Appendix A.3: example input, intermediate outputs, novelty/full/deep/observation reviews, tournament debate, meta-review, research overview, and contact identification. |
| 60-63 | Appendix A.4: 33-cancer dataset, DepMap analysis, in-vitro validation protocol, and additional wet-lab results. |
| 64-71 | Appendix A.5: Specific Aims count distribution, expert rubric, and example proposals/evaluations. |
| 72-79 | Appendix A.5.4: detailed AI-generated KIRA6-for-AML proposal, including rationale, mechanisms, risks, and proposed validation. |
| 80-81 | Appendix A.6 AlphaFold tool-use example, followed by appendix references. |

## Architecture, as stated in the main text

### Input and configuration boundary

The entry point is a research goal specified by an expert scientist in natural language. The goal may contain preferences, experimental constraints, laboratory context, and other attributes; the system parses it into a research-plan configuration (pp. 7-8). The claimed context capacity includes extensive documents and hundreds of prior publication PDFs (p. 8), but the paper does not turn that capacity claim into an independent factuality guarantee.

The default output criteria are alignment with the goal, plausibility, novelty, usefulness, and testability/feasibility as described in the criteria list (p. 7). The scientist can add an idea, review an idea, discuss the research, and provide constraints or feedback through the interface shown in Figure 1 (p. 2).

### Supervisor and workers

The system uses a Supervisor agent to assign subtasks to specialized worker agents (pp. 7-9). The foundational LLM for all agents is Gemini 2.0 (p. 8). Persistent context memory stores and retrieves agent/system states over long computations (p. 8). The authors say the framework is model-agnostic and portable to other models or combinations, but the reported implementation and experiments use Gemini 2.0 and named comparison systems (p. 10).

The specialized agents and their actual functions are:

| Agent | Function in paper | PDF evidence |
|---|---|---|
| Generation | Literature web search, simulated scientific debate/self-critique, assumptions identification, out-of-the-box generation, and hypothesis/research-plan generation. | pp. 9-10; prompt examples pp. 40-41, 47-48 |
| Reflection | Full review, literature/novelty review, simulation review, deep verification of assumptions, observation review, and critique. | pp. 10-11; examples pp. 49-53 |
| Ranking | Pairwise hypothesis comparison in tournament matches; uses simulated scientific debate and produces win/loss patterns and limitations. | pp. 2, 9, 12; example p. 54 |
| Proximity | Computes a proximity graph for clustering, de-duplication, and exploration of similar hypotheses. | p. 9 |
| Evolution | Improves top-ranked hypotheses by synthesis, analogy, extension, simplification, feasibility improvement, and unconventional reasoning. | pp. 9, 12; prompts pp. 45-46 |
| Meta-review | Synthesizes review/tournament patterns, feeds recurring critiques back to subsequent iterations, and prepares the research overview for the scientist. | pp. 9, 13; examples pp. 55-59 |

### Loop and test-time compute

Generated hypotheses are iteratively explored and exploited. Ranking tournaments compare hypotheses pairwise; similar, newer, and highly ranked hypotheses receive priority. Tournament results and review limitations are fed back to other agents. Evolution refines the top-ranked hypotheses, while Meta-review aggregates recurring critique patterns and supplies feedback in later iterations (pp. 9-13). The paper characterizes this as a self-improving loop, but the improvement is inference-time iteration and prompt/context feedback, not a reported update to Gemini weights (pp. 1, 4, 10).

The evaluation section reports increasing performance with more test-time compute, using the co-scientist's Elo rating and comparisons to baselines (pp. 14-18). The paper explicitly warns that Elo is auto-evaluated and not ground-truth based; it may favor attributes not aligned with scientific quality, accuracy, or expert preference (pp. 15-18).

### Tools and grounding

The Generation agent searches the web and retrieves relevant articles; the system cites literature and explains reasoning in its recommendations (pp. 2-3, 10). The system can index/search a private publication repository, and can incorporate feedback from specialized AI models such as AlphaFold; the AlphaFold case is qualitative and placed in Appendix A.6 (p. 13; p. 80). These are tool-use/grounding surfaces, not proof that every generated citation or claim is correct.

## Frozen supplementary description cross-check

The appendix is consistent with the main identity and architecture in several concrete ways:

1. **Agent prompts match the named agents.** Appendix A.2 supplies separate prompts for Generation (pp. 40-41), Reflection (pp. 42-43), Ranking (pp. 43-44), Evolution (pp. 45-46), and Meta-review (p. 46). The prompts contain goal/preferences/instructions/reviews inputs and structured response/termination expectations, matching the worker-agent description on pp. 7-13.
2. **The loop is visible in intermediate artifacts.** Appendix A.3 gives a research-plan configuration and generated hypothesis (pp. 47-48), novelty/full/deep/observation reviews (pp. 49-53), a Ranking tournament debate (p. 54), Meta-review critiques (pp. 55-56), and a research overview (pp. 57-58). This supports the stated generate-review-rank-evolve-meta-review pipeline, while remaining examples rather than a complete reproducibility log.
3. **The supplementary evaluation is biomedical and downstream-facing.** A.4 specifies 33 cancer types and DepMap-based analysis (pp. 60-61), then gives the in-vitro procedure and additional wet-lab results (pp. 62-63). A.5 records the cancer-count distribution, an adapted expert Specific Aims rubric, examples, and expert assessments (pp. 64-71). This is consistent with proposal generation plus biological viability checks, not autonomous clinical deployment.
4. **KIRA6 output preserves the human-validation boundary.** The detailed proposal calls for IC50, ER-stress, IRE1-alpha/XBP1, apoptosis, pathway, combination, cell-cycle, normal-cell, xenograft, and pharmacokinetic studies (pp. 72-79). It explicitly presents limited human safety data and the need for further in-vivo/toxicity work (pp. 75-79). The appendix therefore does not convert the in-vitro result into clinical efficacy.
5. **AlphaFold is an auxiliary tool example, not the system identity.** A.6 describes a protein-sequence suggestion task and qualitative use of AlphaFold feedback (p. 80). It supports the paper's general-purpose/tool-augmented claim, but is not an independent benchmark or wet-lab validation.

## Human intervention boundary

- **Required at input:** an expert scientist specifies the research goal, constraints/preferences, and optionally ideas/reviews (pp. 2, 7-8).
- **In the loop:** scientists can discuss research and review outputs; seven biomedical experts curate the challenging research goals used in the 15-goal evaluation, and domain experts select candidates for laboratory testing (pp. 2, 16, 23).
- **Evaluation:** Elo and LLM judges are automated/AI-based, but expert ratings are subjective and not ground truth (pp. 15-18). Six hematologists/oncologists evaluate 78 Specific Aims proposals using an adapted NIH rubric (p. 21).
- **Biological validation:** human researchers select candidates and run the AML cell experiments and human hepatic organoid experiments (pp. 20-25). The AML wet-lab work is described as a viability checkpoint, not replacement for preclinical/clinical assessment (p. 21).
- **Final decision:** the paper states that continuous human expert oversight is intended and final decisions are made by scientists exercising expert judgment (p. 30). Positive in-vitro results are preliminary and do not establish in-vivo efficacy or clinical success (pp. 21, 25).

## Claims, limitations, and citation-appropriateness implications

The paper's strongest defensible identity claim is “Gemini 2.0-based, asynchronous, multi-agent hypothesis/proposal assistant with test-time iterative debate, ranking, evolution, tool use, and human-directed downstream validation” (pp. 1-13). It is not accurate to cite this PDF as evidence for a fully autonomous end-to-end scientific laboratory or clinical system: the reported demonstrations stop at computational evaluation, cell/organoid experiments, and proposal/recapitulation evidence, while the paper repeatedly reserves final validation and decisions for scientists (pp. 20-33).

The principal limitations are explicit: the evaluation is preliminary and needs broader metrics and independent validation (p. 28); Elo is not ground truth and may misalign with scientific quality (pp. 15-18); expert ratings are subjective (pp. 17-18); in-vitro and organoid findings do not establish in-vivo or clinical efficacy (pp. 21, 25); literature search/citation recall, factuality, coherence, and cross-checking need improvement (p. 30); automation bias, homogenization, human over-reliance, adversarial prompting, unsafe queries, and dual-use risks require safeguards and monitoring (pp. 28-32).

Safety controls are described as input-goal safety review, generated-hypothesis safety review, exclusion of unsafe hypotheses from tournaments, monitoring through Meta-review, and continuous human oversight (pp. 29-30). These controls should not be inflated into a guarantee: the same section calls safeguards an ongoing technical and governance problem and discusses adversarial robustness and dual-use risk (pp. 28-30).

For citation auditing, claims about the following are supported by this PDF only when qualified as reported by the authors: Gemini 2.0 foundation (pp. 1, 7-8), asynchronous test-time compute scaling (pp. 1, 4, 7), named multi-agent roles (pp. 2, 8-13), literature/tool grounding (pp. 3, 10, 13), subjective/auto evaluation boundaries (pp. 15-18), AML and liver-fibrosis biological checks (pp. 20-25), cf-PICI recapitulation (pp. 26-27), and human final oversight (pp. 29-33). Unqualified claims of autonomous discovery, clinical efficacy, objective superiority, complete novelty, or closed-loop physical experimentation exceed the PDF's own evidence and caveats.

## Verdict

**Identity: CONFIRMED.** The document is a Google-affiliated research paper introducing a Gemini 2.0-based AI co-scientist multi-agent assistant.

**Architecture: CONFIRMED WITH QUALIFIERS.** The main text and appendix agree on the Supervisor/worker, Generation/Reflection/Ranking/Proximity/Evolution/Meta-review, tournament, persistent-memory, tool-use, and research-overview structure. “Self-improving” means iterative inference/context feedback in the reported system, not demonstrated weight learning.

**Human boundary: CONFIRMED.** Scientist-defined goals, expert review/candidate selection, wet-lab validation, and scientist final decisions remain part of the workflow.

**Citation use: APPROPRIATE ONLY WITH SCOPE QUALIFIERS.** The PDF supports an assistant and hypothesis/proposal generation architecture plus preliminary biomedical validations. It does not support claims that the system independently completes scientific discovery, establishes clinical efficacy, or provides objective ground-truth superiority.

EVIDENCE_COMPLETE: yes
