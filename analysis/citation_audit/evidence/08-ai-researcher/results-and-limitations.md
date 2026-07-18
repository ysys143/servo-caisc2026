# AI-Researcher: Results and Limitations Evidence

## Audit scope and reading record

- **Single audited source:** `AI-Researcher Autonomous Scientific Innovation.pdf`
- **Source path:** `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/AI-Researcher Autonomous Scientific Innovation.pdf`
- **PDF length:** 38 pages, verified from PDF metadata and page-by-page extraction/rendering.
- **Reading scope:** pages 1-38, including the appendix and all tables, figures, system prompts, and reference pages.
- **Evidence rule:** The statements below are transcribed or conservatively paraphrased from this PDF only. No API/model call, external paper PDF, or external source was used for this audit.

## System and experimental design

### Claimed end-to-end workflow

The paper describes AI-Researcher as a multi-agent system covering literature exploration, idea generation, algorithm implementation, experimental validation, and scholarly documentation (pp. 1-2, Fig. 1). The stated design goal is minimal human intervention, not an explicitly human-free deployment. The architecture uses specialized agents with structured knowledge exchange and recursive refinement; the paper specifically claims bidirectional feedback between theoretical concepts and implementations (p. 2).

The implementation workflow is described as follows (pp. 5-8, Figs. 2-3):

1. Knowledge acquisition and literature/codebase selection.
2. Resource analysis by Paper Analyst, Code Analyst, and Plan Agent, including mappings between academic concepts and code.
3. Code Agent implementation.
4. Advisor Agent review, including Judge Agent and Code Review Agent.
5. Experiment Analysis Agent review after initial results, with proposed code changes and further experiments.
6. Automated Documentation Agent synthesis and iterative revision into a manuscript.

The documentation workflow has three phases: research-artifact synthesis, template-guided structure/content elaboration, and checklist-based verification/revision (pp. 8, 32-35).

### Scientist-Bench task construction

Scientist-Bench takes a human target paper `y`, 15-20 relevant references `R`, a research instruction `I`, and datasets `D` as input. The agent output is code `C` plus a technical report `p` covering background, motivation, method, experiments, and results (p. 3).

- **Level 1 / guided innovation:** explicit research instructions extracted from the target paper are provided with references; intended to test execution of a specified idea.
- **Level 2 / autonomous exploration:** the explicit instruction is omitted; the agent receives references and datasets and must identify a gap, formulate a direction, implement it, and document it (pp. 3, 9).
- Domains include diffusion models, vector quantization, graph neural networks, and recommender systems (pp. 3, 9).
- Benchmark-paper selection used 2022-2024 papers, LLM-generated keywords over 16 research areas, top-cited arXiv retrieval, and citation filtering; 22 representative papers were selected (p. 3).
- Reference selection itself uses a five-step LLM process: citation-pattern analysis, context analysis, evidence collection, impact scoring, and final selection (p. 4).
- Anonymization masks method/model names, abstracts technical details, standardizes datasets, and removes citation/time/institutional markers (p. 4; pp. 37-38).

### Evaluation design

The evaluation has two stages (pp. 4, 9-10):

1. **Technical execution validation:** a code-review agent checks algorithm correctness, computational efficiency, and constraint adherence. Completion is a ratio of required functionality implemented.
2. **Scientific contribution evaluation:** an automated review compares generated report `p` with the human target paper `y` on innovation/novelty, theoretical/methodological rigor, and empirical validation/experimental design. The pairwise rating is on a -3 to +3 scale: negative means below the human paper, zero parity, and positive above it (p. 10).

The primary judge setup uses five LLMs (GPT-4, o1-mini, o3-mini, Claude-sonnet-3.5, Claude-sonnet-3.7), 16 independent assessments per paper, and temperature 1.0. Reported aggregate metrics are mean rating and the percentage with rating >= -1.0, called Comparable (p. 10). The validation section separately includes Gemini-2.0-flash, but the paper says it was excluded from primary experiments due to inferior reliability (pp. 14-15).

## Results and benchmark numbers

### Dataset counts

Table 1 (p. 9) reports:

| Domain | Papers | Level 1 | Level 2 | Rejected |
|---|---:|---:|---:|---:|
| Diffusion Models | 4 | 4 | 1 | 0 |
| Vector Quantization | 6 | 6 | 1 | 0 |
| Graph Neural Networks | 7 | 7 | 1 | 1 |
| Recommender Systems | 5 | 5 | 3 | 1 |
| **Total** | **22** | **22** | **6** | **2** |

The prose says Level 2 used 5 representative papers (p. 9; also p. 13), while Table 1 totals 6 Level-2 tasks. This is an internal reporting inconsistency and should not be silently resolved in downstream claims.

### Implementation quality (RQ1)

- Claude-series models over the full benchmark: **93.8% completeness**, with failures attributed to persistent tensor-dimension conflicts and datatype mismatches after debugging; mean correctness **2.65/5** (p. 10).
- Domain correctness: **VQ 3.22** highest; **Recommendation 2.20** lowest (p. 10).
- Controlled backbone subset: Claude-series **87.5% completeness** versus 4o-series **50%**; correctness **2.75** versus **1.0** (pp. 10-11).
- Level comparison with Claude-series: Level 1 completeness not stated as a percentage in the prose/figure text, while Level 2 is reported as **100% completeness**; correctness falls from **2.5** (Level 1) to **2.25** (Level 2) (p. 11).
- A concrete failure is GPT-4o claiming a Diffusion Transformer implementation that inspection found to be only a standard ViT with diffusion components absent (pp. 11, 19).

### Guided paper comparison (RQ2)

Table 2 (p. 12) reports overall AI-versus-human results:

| Judge | Mean rating | Comparable |
|---|---:|---:|
| GPT-4o | -0.53 +/- 1.00 | 81.82% |
| o1-mini | -1.09 +/- 1.60 | 54.55% |
| o3-mini | -1.51 +/- 0.78 | 13.64% |
| Claude-3.5 | -1.58 +/- 1.28 | 13.64% |
| Claude-3.7 | -1.70 +/- 1.54 | 22.73% |

The surrounding prose gives a broader range of **-0.58 to -1.76** and **15.79% to 78.95%**, which does not exactly match Table 2's overall values. It also emphasizes judge divergence: GPT-4o is most favorable, while Claude-3.7 is most unfavorable. Domain-level values vary substantially, especially for recommender systems, where GPT-4o and o1-mini rate all generated papers as comparable but o3-mini rates none as comparable (p. 12).

### Open-ended autonomous exploration (RQ3)

Table 3 (p. 13) reports overall Level-2 results:

| Judge | Mean rating | Comparable |
|---|---:|---:|
| GPT-4o | -0.23 +/- 0.99 | 100.00% |
| o1-mini | -0.85 +/- 1.32 | 66.67% |
| o3-mini | -1.22 +/- 1.07 | 66.67% |
| Claude-3.5 | -0.65 +/- 1.66 | 66.67% |
| Claude-3.7 | -0.95 +/- 1.54 | 50.00% |

The paper summarizes the guided-to-open-ended shift as mean ratings improving from **-0.58 to -1.76** to **-0.20 to -1.01**, and comparable rates increasing from **15.79%-78.95%** to **40%-100%** (p. 13). The claimed interpretation is that open-ended internal synthesis/ideation outperforms prescriptive instructions. The paper also attributes weaker diffusion results relative to recommender systems to computational resource demands, not necessarily conceptual inability (p. 13). This is an interpretation offered by the authors, not an independently established causal result.

### Backbone ablation (RQ4)

Using 7 research problems with identical architecture/tasks/protocols, Table 4 (p. 14) compares the research-agent backbone:

- GPT-4o agent: comparable rates range from **0%** (o3-mini, Claude-3.5 judges) to **71.43%** (GPT-4o judge).
- Claude-3.5 agent: comparable rates range from **0%** (Claude-3.5 judge) to **85.71%** (GPT-4o judge).
- Claude-3.5 generally receives higher mean ratings than GPT-4o, except under the o1-mini judge where the comparable rate is lower (**28.57% vs 42.86%**).

The result supports strong model-dependence, but the evaluation is only 7 problems and remains highly judge-dependent.

### Paper-review-agent validation (RQ5)

The review agent was tested on **32** high-TF-IDF-similarity ICLR accept/reject pairs from 2021-2023 (pp. 14-15). Overall selection accuracy was:

- Gemini-2.0-flash: **65.62%**, comparable **93.75%**.
- GPT-4o: **81.25%**, comparable **100%**.
- o3-mini: **90.62%**, comparable **100%**.
- Claude-3.5: **90.62%**, comparable **100%**.
- Claude-3.7: **81.25%**, comparable **100%**.

The paper says five of six evaluators exceeded 81%, but Table 5 displays five evaluator columns total. The validation therefore has another presentation/count ambiguity. The authors note Gemini's lower reliability and exclude it from primary experiments; they also note Claude-3.7's extra system-2 reasoning did not improve review performance (p. 15).

### Qualitative case study (RQ6)

The case study focuses on the `rotation_vq` task, using Claude-series models for experimentation/implementation and 4o for manuscript generation (p. 15). The described output has modular code structure, documentation, and separate model/training/evaluation entry points (pp. 15-16). The authors claim that agent interaction produced experiments without explicit experimental requirements: overall benchmarking, controlled ablations, training-dynamics visualization, and latent-space embedding analysis (p. 16). This is a qualitative case, not a separate quantified benchmark.

## Failures and limitations

### Scientific capability failures

- **Technical sophistication:** the system defaults to common methods and missed Gumbel reparameterization for intelligent subgraph sampling in a knowledge-graph recommendation task, while the human paper used it (p. 17).
- **Theoretical depth:** human analysis addressed alignment-uniformity tradeoffs; the AI output defaulted to superficial computational-complexity analysis (p. 17).
- **Mathematical formalism:** outputs favor standard GCN and InfoNCE forms instead of task-specific formalizations (p. 17).
- **Sequential reasoning:** extended derivations and multi-step theoretical deductions degrade toward descriptive, established principles; the paper attributes this to hallucination vulnerability and limited reasoning depth (pp. 17-18).
- **Extended implementation fidelity:** GPT-4o repeatedly omitted diffusion components in multi-turn work despite succeeding on the same task with a single-turn prompt, suggesting knowledge-application degradation rather than simple lack of knowledge (p. 19).
- **Persistent execution failures:** tensor dimension conflicts, datatype mismatches, NaN losses, and training instability are explicitly reported failure modes (pp. 10-11).

### Evaluation limitations

The paper explicitly states that current evaluation inadequately captures idea novelty, feasibility, and impact; code review needs stronger measures of algorithmic efficiency and implementation elegance; and LLM reviewers can overweight presentation/style over substantive methodological innovation (p. 20). Judge divergence in Tables 2-4 is a direct empirical warning against treating one judge's score as ground truth.

### Human intervention boundary

The system is advertised as requiring minimal human intervention (pp. 1-2), and the workflow is designed to proceed autonomously through implementation, review, experiments, and writing. However, the PDF does not establish that humans are absent from benchmark construction, target-paper/reference selection, prompt construction, or final scientific validation. Benchmark inputs are prepared through LLM-assisted curation and anonymization, while human expert judgments are used as validation data from ICLR (pp. 3-4, 14-15). The defensible boundary is therefore **minimal intervention in an execution workflow**, not demonstrated elimination of human involvement across the research/evaluation lifecycle.

### Memory boundary

The current implementation has **no dedicated external memory management system**. It relies primarily on the LLM's native context window and summarized outputs from earlier stages (pp. 19-20). Fine-grained experimental parameters, literature findings, and implementation details can be compressed into abstract summaries and become difficult to retrieve. The authors identify structured semantic repositories, hierarchical memory, attention-guided compression, KV-cache improvements, and long-context training as future directions (p. 20).

### Feedback boundary

Feedback is explicit and multi-stage, but bounded by the agents' available context/tools:

- Resource analysts map papers and code into notes and a plan (pp. 5-7, 26-28).
- Judge and Code Review agents inspect atomic concepts and implementation fidelity after coding (pp. 7, 30).
- Experiment Analysis Agent inspects results and proposes modifications/further experiments (pp. 7-8, 31).
- Documentation Agent performs iterative structure/content/checklist revision (pp. 8, 32-35).

The PDF does not show a durable external research memory, an independently verified human sign-off gate, or a formal mechanism guaranteeing that feedback changes the underlying hypothesis rather than only code/report artifacts. In fact, the memory limitation means later feedback can operate on summaries that have already lost detail (pp. 19-20).

## Bottom-line interpretation

The PDF provides evidence of a broad autonomous workflow and strong implementation completion under some Claude configurations, with open-ended paper-comparison scores often higher than guided scores. It does **not** establish stable human-level scientific discovery: correctness is materially below perfect, results vary sharply by judge/model/domain, the Level-2 sample count is inconsistently reported, and the authors document gaps in advanced methods, theory, long-horizon reasoning, memory, implementation fidelity, and evaluation validity. The strongest supported claim is that AI-Researcher can produce end-to-end research artifacts with substantial automation and sometimes near-human comparative ratings under the paper's automated judging protocol.

EVIDENCE_COMPLETE: yes
