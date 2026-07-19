# lu2026aiscientist: Methods, Numbers, and Limitations Evidence

## Lane Scope and Source Identity

- Active source: `lu2026aiscientist` only.
- Local PDF: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/Towards end-to-end automation of AI research.pdf`.
- SHA-256: `a75e0d93447f400179136bf18d909df29e0c8ccaeba076a1dfb1beeef0e0e10d`.
- Length: 9 PDF pages. The six-page Nature article body is followed by three pages of Methods and article metadata.
- Identity: Chris Lu et al., *Towards end-to-end automation of AI research*, Nature 651, DOI `10.1038/s41586-026-10265-5`; received 8 July 2025, accepted 11 February 2026, published online 25 March 2026 (PDF p. 1).
- Coverage: PDF pp. 1-9 read in order with layout-preserving extraction. PDF pp. 2-5 were rendered and visually inspected because they contain Fig. 1, Table 1, Fig. 2, and Fig. 3.
- Scope boundary: the local PDF repeatedly defers prompts, model versions, replication counts, reviewer details, and workshop analyses to Supplementary Information. Those materials are not part of this 9-page file, so claims below distinguish what the article itself establishes from details it merely points elsewhere to.

## Problem, Context, and Intended Contribution

- The paper frames full scientific automation as a longstanding AI ambition. Earlier systems automated isolated tasks such as chemical-structure discovery, theorem proving, materials discovery, protein-shape prediction, or analysis of already collected datasets; the claimed gap is autonomous navigation of the whole cycle from conception to publication (PDF p. 1).
- Machine-learning research is the chosen domain because its experiments can generally be conducted entirely on computers (PDF p. 1). The work therefore demonstrates computational research automation, not a physical laboratory loop.
- The contribution is a pipeline that proposes ideas, searches literature, writes and executes code, analyses and plots results, writes a manuscript, and produces an automated review. It is evaluated in a human-scaffolded template-based mode and a less constrained template-free mode (PDF pp. 1-2, 7-9).
- The evaluation has three distinct goals that should not be conflated: measure an automated reviewer's agreement with conference decisions; compare generated-paper scores across base-model releases and compute budgets; and expose selected generated manuscripts to an external workshop review process (PDF pp. 1-5).

## Document Structure and Argument Flow

1. PDF p. 1 states the end-to-end automation problem, introduces the two operating modes, and motivates automated evaluation.
2. PDF p. 2 presents the workflow, model-release correlation, reviewer comparison, and manuscript-generation procedure.
3. PDF p. 3 gives the complete reviewer benchmark table and the workshop submission outcome.
4. PDF p. 4 shows the selected generated paper and states technical, epistemic, and ethical limitations.
5. PDF p. 5 visualizes the four-stage tree search and compute scaling, then gives the conclusion and online-material pointer.
6. PDF p. 6 contains references and licensing information.
7. PDF pp. 7-9 specify the two system modes, tree-node lifecycle, replication and aggregation nodes, reviewer construction, reviewer-validation caveats, ethics protocol, data, and code availability.

## End-to-End Methods

### Shared high-level workflow

- Figure 1 separates ideation, experimentation, and write-up/review. Ideation produces an LLM proposal, checks novelty against literature, then scores and archives it. Experimentation records an experimental journal; write-up uses plots and notes to create a paper, followed by automated review (PDF p. 2, Fig. 1a).
- Literature retrieval uses Semantic Scholar and web access. The manuscript stage can run up to 20 literature-search rounds; each candidate citation receives a textual inclusion justification (PDF pp. 2, 7).
- The generated LaTeX is compiled automatically with up to five compilation-error correction rounds in the template-based workflow (PDF p. 7).
- The experimental journal is a stated memory mechanism: metrics, plots, observations, and notes inform later planning and writing (PDF pp. 2, 7).

### Template-based mode

- A human provides a code template reproducing a simple training run, such as a small transformer on Shakespeare. The system proposes variations or extensions of archived ideas (PDF p. 7).
- Each idea stores a title, hypothesis summary, experimental plan, and three distinct self-scores: interestingness, novelty, and feasibility, each on a 1-10 scale (PDF p. 7). The source does not collapse these three into one scalar.
- Novelty checking may use up to ten iterative literature-search rounds, with later queries refined from earlier results. Ideas judged too similar to existing work are discarded (PDF p. 7).
- A selected idea receives a sequential plan of up to five experiments. Aider modifies the code, captures failures, and may attempt up to four repair cycles per experiment. The corrected experiment is rerun with a 7,200-second timeout (PDF p. 7).
- The paper is then filled section by section in a conference template from the journal and figures, refined, cited, compiled, and reviewed (PDF pp. 2, 7).

### Template-free mode and model roles

- The template-free mode starts from a high-level research proposal rather than human-provided code. Proposals contain a research problem, method, and expected outcome and are refined against literature (PDF p. 7).
- The reported model allocation is: OpenAI o3 for idea generation and code critique; Claude Sonnet 4 for code generation; GPT-4o for vision-language tasks and best-first node evaluation; o1 for direct LaTeX generation; and o4-mini for the automated reviewer (PDF pp. 7-9).
- The system remains conditioned by human scope. It receives a user-specified ML subfield or, in the workshop experiment, the workshop's broad theme. Humans can also update a ten-example HuggingFace dataset list or manually provide local datasets and instructions (PDF pp. 2-3, 8).
- A complete template-free run takes from several hours to more than 15 hours depending on the problem (PDF p. 8).

## Four-Stage Agentic Tree Search

### Stage manager and stopping conditions

1. **Preliminary investigation:** establish a working prototype; the stage stops after basic viability is successfully demonstrated.
2. **Hyperparameter tuning:** optimize the prototype; the stage stops after training curves converge and execution succeeds on at least two datasets.
3. **Research-agenda execution:** conduct the main research program until its allocated compute budget is exhausted.
4. **Ablation studies:** test component contributions until its allocated compute budget is exhausted.

Each stage runs its own tree search. Every node has a maximum one-hour experiment runtime. At each stage boundary an LLM evaluator selects the most promising leaf as the root of the next stage, pruning the other branches (PDF pp. 5, 7).

### Node lifecycle and search policy

- Claude Sonnet 4 writes a concrete plan and Python code. An execution error ends that node's cycle and marks it buggy. A successful run writes metrics to structured NumPy files, creates plots, and sends those plots to GPT-4o for critique. A VLM-detected plotting problem also marks the node buggy; only an execution and VLM pass produces a non-buggy node (PDF p. 8).
- A node records the experiment script, high-level plan, error trace, runtime, metrics, o3 code critique, plotting script, figure paths, VLM feedback, and buggy/non-buggy state (PDF p. 8).
- At an iteration, several existing nodes are chosen for parallel expansion. A predefined but unreported probability determines whether to prioritize a buggy node for repair or a non-buggy node for improvement. Among non-buggy nodes, GPT-4o conducts best-first selection based on performance metrics, training dynamics, and plot quality. Claude Sonnet 4 generates child code, and new nodes run concurrently (PDF p. 8).
- The policy is therefore a heuristic, evaluator-guided best-first tree search. The paper does not formulate a posterior, expected information gain, or a Bayesian experimental-design objective.

### Specialized nodes and replication

- Hyperparameter nodes explore alternatives in stage 2 and track tested configurations to avoid repetition. Failures spawn debug nodes (PDF p. 8).
- Ablation nodes test components or assumptions in stage 4, likewise tracking tested conditions and spawning debug nodes after errors (PDF p. 8).
- Replication nodes rerun a parent experiment with different random seeds. The source says **typically several** such nodes are created; it does not give a universal fixed replication count in the article. Their purpose is to calculate mean and standard deviation (PDF p. 8).
- Aggregation nodes do not conduct new experiments. They generate a Python script that combines replication results and plots mean and standard deviation (PDF p. 8).
- Consequently, the frozen description's replication-node clause is directly supported, but it should not imply that every experiment is replicated or that a fixed number of seeds is guaranteed.

## Open-Endedness and Memory: Exact Scope

- The paper calls the template-free mode more open-ended because it is not tethered to a starting implementation and can formulate high-level proposals and dynamically integrate public datasets (PDF pp. 1, 7-8).
- A growing archive explicitly conditions iterative idea generation in the described ideation process, and the experimental journal informs later planning and writing (PDF pp. 2, 7). The tree itself carries information through parent-child nodes and by promoting the best leaf between stages (PDF pp. 5, 7-8).
- The article does **not** state that an "open-endedness archive" directly conditions best-first experimental tree expansion. Archive-conditioned ideation, journal memory, and tree-state inheritance are separate mechanisms in the text. A description that merges them needs qualification.
- Open-endedness is bounded by a human-specified subfield or workshop topic, available APIs and datasets, fixed stage structure, finite budgets, model prompts, and human filtering for external submission. It is broader than template extension, not unrestricted autonomous science (PDF pp. 2-3, 7-8).

## Automated Reviewer Construction

- The reviewer uses o4-mini and the NeurIPS reviewer guidelines. It reads a manuscript PDF and outputs a summary, strengths, weaknesses, questions, limitations, ethical concerns, soundness, presentation, contribution, overall score on a 1-10 scale, confidence, and a preliminary accept/reject decision (PDF pp. 8-9).
- Five independent reviews are produced for each paper. A separate LLM meta-review acts as an area chair and aggregates them into one final assessment (PDF pp. 2-3, 9).
- The automated reviewer is used as an evaluation instrument for generated-paper comparisons. The article does not show that its accept/reject output gates tree-node expansion, nor that it was the decisive gate for selecting the three workshop submissions; that selection was manual (PDF pp. 2-3, 8-9).

## Reviewer Benchmark: Complete Quantitative Record

### Evaluation pools and uncertainty

- Automated decisions were compared with public ICLR OpenReview decisions. The prose describes one pool of 1,000 papers from 2017-2024, potentially within training data, and a second "clean" 2025 pool after the model knowledge cutoff; the article does not state the second pool's original size (PDF p. 3).
- Figure 1c reports two-sample z-tests on subsampled accuracy with automated `n = 698/876` (before/after cutoff as printed) and human `n = 412`. It reports 95% bootstrap confidence intervals from 5,000 replicates and uses a five-run ensemble for every automated review (PDF p. 2, Fig. 1 caption).
- The human row is imported from the NeurIPS 2021 consistency experiment, not measured on the same ICLR papers. The Methods explicitly warns that ICLR and NeurIPS contain different submission pools and a distribution shift, so the comparison is "not exact" (PDF pp. 3, 9).

### Table 1 values

| Reviewer and condition | Balanced accuracy | Accuracy | F1 | AUC | FPR | FNR |
|---|---:|---:|---:|---:|---:|---:|
| Human, NeurIPS 2021 consistency experiment | 0.66 | 0.73 | 0.49 | 0.65 | 0.17 | 0.52 |
| Random decision, 2017-2024 | 0.50 | 0.54 | 0.47 | 0.52 | 0.47 | 0.43 |
| Always reject, 2017-2024 | 0.50 | 0.65 | 0.00 | 0.50 | 0.00 | 1.00 |
| Automated Reviewer, 2017-2024 | **0.69 +/- 0.04** | 0.65 +/- 0.10 | 0.62 +/- 0.09 | 0.69 +/- 0.09 | 0.45 +/- 0.10 | 0.17 +/- 0.08 |
| Random decision, 2025 | 0.52 | 0.51 | 0.48 | 0.49 | 0.50 | 0.48 |
| Always reject, 2025 | 0.50 | 0.56 | 0.00 | 0.50 | 0.00 | 1.00 |
| Automated Reviewer, 2025 | **0.66 +/- 0.03** | 0.63 +/- 0.09 | 0.67 +/- 0.09 | 0.65 +/- 0.10 | 0.52 +/- 0.10 | 0.17 +/- 0.07 |

The automated-reviewer margins are 95% bootstrapped confidence intervals (PDF p. 3, Table 1).

### Tests and interpretation

- Two-sample z-tests found no significant balanced-accuracy difference from the human comparator before cutoff (`P = 0.319`) or after cutoff (`P = 0.921`) under the stated subsampling (PDF p. 2).
- Non-parametric bootstrap tests found automated F1 outperformance (`P < 0.001`) (PDF p. 2). This is metric-specific and does not establish superior peer-review quality generally.
- The paper interprets the drop from 69% before cutoff to 66% after cutoff as evidence that contamination may exist, while arguing the effect is at most minimal because post-cutoff performance remains comparable with the human reference (PDF p. 3).

## The 0.69 and Calibration Wording

- `0.69` is specifically the **mean balanced accuracy for the 2017-2024 automated-reviewer pool**, with `+/- 0.04` 95% bootstrap uncertainty, using a five-review ensemble plus meta-review. It is not a condition-free accuracy number (PDF pp. 2-3, 9).
- The same row also has AUC `0.69 +/- 0.09`; wording must name the metric to avoid confusing these two 0.69 values (PDF p. 3).
- The `0.66` human comparator is from a separate NeurIPS consistency experiment, whereas the automated score is on ICLR decisions. The source itself says that the different paper pools make the comparison inexact (PDF p. 9).
- The genuinely post-cutoff automated balanced accuracy is `0.66 +/- 0.03`, not 0.69 (PDF p. 3).
- This 9-page article reports **no calibration procedure**, decision-threshold tuning, calibration curve, expected calibration error, Brier score, or other probability-calibration statistic. Balanced accuracy measures classification agreement, not calibration.
- Accordingly, `automated reviewer, balanced accuracy about 0.69` is supportable only with the pre-cutoff, ensemble, uncertainty, and cross-study-comparator conditions. The stronger manuscript wording that the reviewer's "internal acceptance gate ... stays uncalibrated" is not directly established by this source. The article neither labels it calibrated nor uncalibrated, and it does not demonstrate that the reviewer is the internal gate controlling workshop submission or tree search.
- The paper does document possible training-data contamination, distribution shift, high FPR (`0.45 +/- 0.10` before and `0.52 +/- 0.10` after cutoff), and an inexact human comparison. These are reliability limitations, but they are not interchangeable with a measured calibration failure.

## Generated-Paper Model and Compute Comparisons

- Figure 1b reports a positive association between base-model release date and automated-reviewer paper score: `R^2 = 0.517`, `P < 0.00001`. The caption gives `n = 6` for template-free points and `n = 3` for template-based points and identifies the displayed uncertainty as standard error (PDF p. 2).
- This is an automated-reviewer outcome across model releases, not direct human validation and not a randomized causal estimate that newer models alone cause better science.
- Figure 3c contains four compute-budget points with `n = 30` at each and standard-error bars. The rendered plot visually places the budgets at approximately 3, 8, 16, and 32 experimental nodes, with mean reviewer scores rising from roughly 3.3 to 3.9 (PDF p. 5). Because the article does not print point-value labels and defers exact hyperparameters to Supplementary Information A.2.9, these coordinates are visual readings, not exact tabulated values.
- The supported conclusion is a positive score trend under deeper test-time tree search in the tested setting. It does not establish monotonic scientific-quality gains outside these generated ML papers or under human review.

## External Workshop Outcome

- With IRB approval and cooperation from ICLR 2025 and the I Can't Believe It's Not Better (ICBINB) workshop, the authors submitted three template-free generated manuscripts. It was the only venue used (PDF p. 3).
- The system received the workshop's broad topic as a prompt. Humans manually filtered promising outputs at each stage. Selection checked topic fit, whether code implemented the proposal and ran without errors, and manuscript formatting. The authors say this filtering selected among outputs without modifying the selected papers' scientific workflow or final form (PDF p. 3).
- The three papers were among 43 workshop submissions. Reviewers knew that some submissions were AI-generated but not which ones; the Methods adds that reviewers could opt out (PDF pp. 3, 9).
- One manuscript received scores `6`, `7`, and `6`, averaging `6.33`, and ranked in the top 45% of reviewed papers. It reported a negative result aligned with the workshop theme (PDF pp. 3-4, Fig. 2).
- The organizers said it would in all likelihood have been accepted, but the authors withdrew every AI-generated submission after review under a pre-established protocol. Thus "cleared the peer-review bar" or "passed first-round review" is defensible; "was finally accepted/published" omits the actual withdrawal and should not be stated without qualification (PDF pp. 1, 3-4, 9).
- The other two papers did not meet the acceptance bar. Internal human review concluded that one met workshop quality but none met the main ICLR conference bar (PDF p. 3).
- The workshop acceptance rate was 70%, compared with 32% for the ICLR 2025 main conference. The authors themselves use this difference to limit the strength of the result (PDF pp. 1, 4).

## Explicit Limitations and Threats to Validity

- **Consistency and venue bar:** only one of three submissions cleared the workshop bar, and workshops have a substantially higher acceptance rate than the main conference. The system does not yet consistently meet workshop quality or meet top-tier main-conference quality (PDF p. 4).
- **Output defects:** documented failure modes include naive or underdeveloped ideas, incorrect implementations of the central idea, insufficient methodological rigor, experiment-code errors, duplicate figures, hallucinations, and inaccurate citations (PDF p. 4).
- **Trust and creativity:** the authors say persistent susceptibility to being fooled and confidently wrong prevents reliable trust. They also state that it is unclear whether these systems can produce creative conceptual leaps comparable to major human science (PDF p. 4).
- **Computational-only scope:** all demonstrated experiments are computational. Extension to chemistry or other physical domains is future work requiring an experiment executor or humans to run experiments (PDF p. 4).
- **Human intervention:** the external validation did not involve human edits to the selected papers, but humans supplied scope and manually filtered outputs, checked code implementation and executability, and checked formatting. "Fully autonomous" must therefore be scoped to the generation workflow after selection conditions, not the complete publication decision process (PDF pp. 3, 9).
- **Reviewer benchmark validity:** 0.69 is potentially contaminated pre-cutoff performance; post-cutoff performance is lower. The human comparison comes from another conference and paper distribution, and the evaluation measures agreement with accept/reject decisions rather than correctness, novelty, or significance of generated claims (PDF pp. 3, 9).
- **Reviewer as outcome measure:** model-release and compute-scaling results are scored by the system's own automated reviewer. The article provides external human review for only three selected papers, not for every configuration or tree budget (PDF pp. 2-5).
- **Ethics and governance:** listed risks include overwhelming peer review, credential inflation, taking others' ideas without credit, scientist job displacement, unethical or dangerous experiments, and unsafe open-ended exploration. Protocol H24-02652 required disclosure and withdrawal of all AI-generated papers (PDF pp. 4-5, 9).
- **Reporting completeness:** the article defers many exact prompts, replication counts, model versions, tree hyperparameters, and full paper analyses to the supplement. The 9-page PDF alone cannot verify those deferred details (PDF pp. 2-5, 7-9).

## Frozen System-Description Implications

Frozen description: "A successor LLM system using agentic tree search over experiment plans, with replication nodes that re-run experiments and report results as mean and standard deviation over random seeds. It includes an automated LLM reviewer (about 0.69 balanced accuracy) and an open-endedness archive that conditions later search. One output cleared an external workshop peer-review bar. Experiments are computational only; no physical experiment."

- **Successor system and tree search:** supported for the template-free mode (PDF pp. 1, 5, 7-8).
- **Replication nodes and mean/s.d.:** directly supported, with the qualification that the paper says "typically several" replication nodes and does not promise them for every experiment (PDF p. 8).
- **Reviewer about 0.69:** supported only as `0.69 +/- 0.04` pre-cutoff balanced accuracy under the five-review/meta-review benchmark; post-cutoff is `0.66 +/- 0.03`, and human `0.66` is cross-study (PDF pp. 2-3, 9).
- **Archive conditions later search:** partially supported. The archive conditions ideation, while journal state and parent/leaf nodes condition experimental search. The article does not identify one open-endedness archive as the state directly driving tree-node selection (PDF pp. 2, 7-8).
- **Workshop bar:** supported with required qualification: one of three selected papers scored above the workshop threshold and was likely acceptable, but all were withdrawn and the workshop acceptance rate was 70% (PDF pp. 1, 3-4, 9).
- **Computational only:** directly supported (PDF pp. 1, 4).

## Bottom Line for Synthesis

- The article supports a staged, template-free agentic tree search with explicit debugging, best-first selection, replication nodes over random seeds, and aggregation of mean and standard deviation.
- It supports a 0.69 balanced-accuracy statement only under tightly specified pre-cutoff benchmark conditions. It does not support treating 0.69 as a calibration result or asserting an uncalibrated gating mechanism.
- It supports a qualified workshop peer-review milestone, not an unconditional final acceptance: human filtering preceded submission, one of three papers cleared a relatively permissive workshop bar, and all papers were withdrawn by protocol.
- Its "open-ended" mode remains computational, scoped, budgeted, tool- and dataset-bounded, and partly human-curated.

PAGES_COVERED: 1-9
EVIDENCE_COMPLETE: yes
