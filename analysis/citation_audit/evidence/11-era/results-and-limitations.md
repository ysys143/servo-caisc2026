# ERA: results and limitations

## Audit scope and source

- Audited source: `ERA - An AI System to Help Scientists Write Expert-Level Empirical Software.pdf`.
- Source location: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/ERA - An AI System to Help Scientists Write Expert-Level Empirical Software.pdf`.
- The source reports 78 pages. Pages 1-78 were read directly, including the abstract, main text, Methods, References, Extended Data legends, Supplementary Figures, Supplementary Notes, and Supplementary Tables.
- No other PDF was opened. No API call or model call was made during this audit. The paper itself describes use of LLMs and external research agents; those are reported as part of the paper's experiment, not used as audit evidence.

## Page coverage

- **pp. 1-4:** Identity, abstract, motivation, scorable-task framing, Figure 1, Kaggle benchmark, and the six scientific task areas.
- **pp. 5-10:** Main results for scRNA-seq batch integration, COVID forecasting, GIFT-Eval, and discussion of geospatial, neuroscience, and numerical-analysis tasks; Table 1 compares ERA with Best-of-N.
- **pp. 11-15:** Related work, explicit empirical-optimization versus genuine-discovery distinction, safety discussion, code mutation system, PUCT/UCB algorithm, research-idea injection, recombination, and model comparison design.
- **pp. 16-19:** Dataset construction, train/validation/test procedures, existing-method replication, COVID and GIFT-Eval protocols, unified forecasting method, and discussion of computational limits.
- **pp. 20-25:** References, code availability, author contributions, acknowledgements, and competing-interest declaration.
- **pp. 26-34:** Extended Data Figures 1-4 and Supplementary Tables S3-S7, including replicate behavior, score progression, embeddings, method adherence, prompts, and recombination setup.
- **pp. 35-38:** Supplementary Notes for geospatial segmentation, ZAPBench, numerical integration, genuine discovery, and computational cost.
- **pp. 39-56:** Supplementary Figures S1-S20 covering data splits, replicate/embedding analyses, COVID forecasts, GIFT-Eval solution categories, geospatial/ZAPBench/integration breakthrough plots, and held-out integral scores.
- **pp. 57-78:** Supplementary Tables S1-S19 covering budgets, Kaggle tasks, prompts, COVID method descriptions and adherence judgments, GIFT-Eval leaderboard/configurations, DLRSD scores, research-idea prompts, recombination prompts, and the BBKNN example.

## Experimental design

ERA defines a **scorable task** as a problem in which generated software is executed in a sandbox and ranked by a quality metric (pp. 1-4, 13). The prompt supplies a task description, evaluation metric, relevant data/code, and optionally a research idea. The LLM writes Python code, the sandbox executes it, and the resulting score plus logs guide later search (p. 13).

The paper's main tasks are: Kaggle Playground tabular regression/classification; OpenProblems v2.0.0 scRNA-seq batch integration; CDC CovidHub hospitalization forecasting; GIFT-Eval time-series forecasting; DLRSD remote-sensing segmentation; ZAPBench whole-brain neural activity prediction; and difficult numerical integrals (pp. 2-4, 35-38). The abstract groups these into six scientific problems while the Kaggle benchmark is the development/calibration benchmark.

For scRNA-seq, ERA is optimized on a distinct CELLxGENE dataset, with disjoint 20,000-cell train and validation subsets, then evaluated on six OpenProblems holdout datasets totaling 1,747,937 cells (pp. 5, 16, 39). For each of nine existing methods, three tree-search replicates are run; the best node from training and then the best replicate from validation are selected before holdout evaluation (pp. 16-17, 39). Base-method hyperparameters are separately optimized with Optuna on the training dataset (p. 17).

For COVID, retrospective searches use rolling six-week validation windows through the 2024-2025 season, with data available as of 2025-05-01, and compare against CovidHub submissions and the official ensemble (p. 7, 17). The reported recombination test uses three held-out reference dates, 2025-04-05 through 2025-04-19, four horizons, and 52 jurisdictions (p. 8). Existing model replications are restricted to methods reproducible from historical hospitalization data and meeting coverage/duration criteria (p. 17).

For GIFT-Eval, the paper fixes a 2025-05-18 snapshot because the benchmark later changed its dataset, scoring, and categories. Separate searches cover 92 of 97 datasets; the five largest use the naive baseline in the aggregate. Each per-dataset search uses 300 nodes, while the unified solution uses over 1,000 nodes and basic libraries only (pp. 10, 18, 71).

## Mutation, search, and UCB/PUCT

ERA's mutation occurs at the **code level**: the LLM rewrites a parent candidate rather than applying random syntax edits (pp. 11, 13). The search is a globally flat tree. Every executed candidate can be expanded; selection does not recurse from the root as in AlphaZero, and the authors characterize it as closer to Flat UCB than conventional MCTS (p. 13).

The implemented selection score is PUCT-inspired:

`PUCT_i = r_i + c_puct * E(i)`

where `r_i` is a rank-normalized task score and `E(i)` depends on the node's visit count relative to total visits across the tree (p. 13). The prior is flat, `P_T(u) = 1/|T|`; visit counts are backpropagated to ancestors after a child is generated and executed (pp. 13-14). The algorithm returns the candidate with maximum task score, not the most visited node (p. 14). `c_puct = 1` was tuned on the Kaggle benchmark (p. 13).

This is not beam search: historical nodes are retained so the algorithm can backtrack and branch when a current path plateaus (pp. 4, 14). It is also not a standard rollout-based game tree: scores come from empirical execution, with randomness mainly from LLM sampling (p. 13). The authors report score saturation after roughly 300-1,000 nodes, depending on the task (p. 13).

## Research ideas, recombination, and feedback

Research ideas are injected as prompt instructions derived from highly cited papers, textbooks, search results, or LLM-driven research systems (pp. 2, 14). For the single-cell experiments, method PDFs were summarized into short descriptions before being supplied to ERA; the authors manually filtered proposals and removed one proposed method before formatting the remaining ideas (pp. 5, 14, 17, 74-78).

The main feedback signal is the executed quality score, supplemented by output logs and code information during hill climbing (p. 13). There is also human inspection: experts checked whether generated code followed requested algorithms and whether recombination outputs contained relevant aspects of both parent codes (pp. 5, 7, 17, 26, 34, 67-70). The system itself does not receive a general scientific peer-review feedback loop; its operational feedback is task scoring, execution status, and prompt-level research guidance.

Recombination is performed in conceptual space. The authors use an LLM to compare two parent methods and place the comparison in a prompt directing ERA to combine their strengths, rather than crossing only distilled model parameters (p. 15, 76). In scRNA-seq, 55 pairwise recombinations were generated; 24/55 (44%) beat both parents, and 22 of the remaining 31 beat one parent (p. 5). In COVID, 26 hybrid models were generated and 11 beat both parents (p. 9).

## Results and benchmark numbers

### Kaggle Playground

The development benchmark contains 16 2023 Kaggle Playground competitions spanning regression and classification (pp. 3-4, 57). Performance is average public leaderboard percentile across the 16 tasks. ERA tree search substantially outperformed a single LLM call, Best-of-1000 LLM calls, and AIDE; expert advice and an instruction to implement a boosted decision tree from scratch improved performance further (p. 4). The paper reports standard deviations across competitions, but the extracted main text does not provide the individual percentile values in prose; the comparison is shown in Figure 1b (p. 3).

### scRNA-seq batch integration

- OpenProblems v2.0.0 evaluates 15 state-of-the-art methods plus eight controls across 13 metrics, six datasets, and 78 dataset-metric measurements (p. 4; Methods p. 16).
- ERA beat the corresponding published result for 8 of 9 replicated methods (p. 5).
- BBKNN (TS) produced a 14% overall improvement over the best published method, ComBat, and equaled or outperformed published BBKNN on every dataset and 11/13 metrics (p. 5).
- The key discovered implementation combines ComBat-corrected PCA embeddings with BBKNN's cross-batch neighbor graph; manual modification experiments identify the ComBat-corrected embedding as critical (p. 5).
- Across 87 methods, 40 beat all methods currently on the OpenProblems leaderboard: 6/11 base methods, 29/55 recombinations, 4/9 Deep Research methods, and 1/12 AI co-scientist methods (pp. 5-6).
- Metrics that fail to compute are assigned zero in the overall score, and some low-performing replicates computed only 30, 57, or 45 of the 78 metrics. The authors state that out-of-memory or time failures were not explicitly selected against because optimization ran on 20k-cell datasets (pp. 6, 16, 26).

### COVID hospitalization forecasting

- CovidHub forecasts cover 52 states/territories, the current week plus three subsequent weeks, and 23 quantiles; scoring uses Weighted Interval Score (WIS) (p. 7).
- The Google Retrospective model achieved average WIS 26 versus 29 for the official CovidHub Ensemble over the retrospective season (p. 7).
- Fourteen strategies beat the official ensemble on the three-week held-out evaluation: 10 recombinations, two Deep Research ideas, one AI co-scientist idea, and one replicated baseline (pp. 8-9).
- In the 26 recombination experiment, 11 beat both parent models (p. 9).
- For the explicit held-out dates, the best recombination had average WIS 11.63, the CovidHub ensemble 12.85, and Google Retrospective 14.39 (Supplementary Fig. S12, p. 49). This is a narrower comparison than the full retrospective-season result and should not be conflated with it.

### GIFT-Eval

- The per-dataset ERA solution scored MASE 0.671 on the 2025-05-18 snapshot, versus 0.679 for TTM-R2-Finetuned and 0.680 for TimesFM 2.0 500m (Supplementary Table S12, p. 71).
- The unified solution scored MASE 0.734 (p. 71). Lower MASE is better.
- The unified model uses up to eight validation-selected configurations, including level, trend, seasonality, residual correction, transforms, and date/holiday features (pp. 10, 19, 72).
- The paper explicitly does not claim a live leaderboard result because GIFT-Eval changed after the experiment; it restricts comparison to the fixed May 18 snapshot (p. 18).

### Geospatial, neuroscience, and numerical analysis

- On DLRSD, the top three tree-search solutions achieved mIoU 0.80, 0.81, and 0.82, versus reported prior results from 0.580 to 0.762 (pp. 35, 73). The solutions use standard architectures, pretrained ImageNet encoders, augmentation, and extensive test-time augmentation (p. 35).
- On ZAPBench, the general tree-search model outperformed listed baselines including the best video model except for one-step-ahead prediction; a separately optimized one-step model led that condition (p. 36). ERA models trained in under two hours on one T4 GPU, versus 36 hours on 16 A100 GPUs for the best video model (p. 36).
- For numerical integration, the task uses 38 oscillatory integrals where `scipy.integrate.quad()` failed and the analytic answer was known; 19 are training and 19 held out (p. 37). The best evolved routine correctly solved 17/19 held-out integrals within 3% (pp. 38, 56). It first calls `quad()` and falls back to geometrically partitioned intervals plus Euler acceleration only when error/NaN/Inf/exception conditions trigger (p. 38).

### Best-of-N comparison

With `N=128` search nodes, ERA outperformed Best-of-N for all tested model/task combinations except GPT-5 on batch integration (p. 15). Table 1 reports, for example, Gemini 2.5 Flash batch integration 0.6306 (BoN) versus 0.6552 (ERA), and epidemiology 106.55 versus 93.07; GPT-5 gives 0.6740 versus 0.6671 on batch integration and 78.04 versus 74.55 on epidemiology (p. 9). The authors note typical experiment variation around 0.01 for batch integration and order 1 for epidemiology, with model-dependent variability (p. 15).

## Computational-only boundary and genuine discovery

The paper explicitly distinguishes optimizing empirical predictive models from genuine scientific discovery. Its evaluated core tasks primarily test advanced empirical software engineering under a machine-defined score, not causal or theoretical understanding (p. 12). High leaderboard performance therefore establishes performance on a scored computational task, not by itself a new scientific explanation.

The paper's “Towards Genuine Discovery” section cites two separate deployments of the core tree-search algorithm (p. 38):

1. **Mathematical discovery:** a system allegedly derived six novel analytical derivations and a closed-form exact solution for an open cosmic-string radiation-spectrum problem, without empirical data or predictive modeling. The score compared proposed formulas against high-precision numerical integration at random physical parameter values.
2. **Neural mechanisms:** in an in-silico zebrafish setting, unconstrained search found statistical shortcuts, while adding wiring-diagram structural priors enabled recovery of causal effective connectivity.

These are cited as demonstrations of potential and are outside the main ERA benchmark results in this PDF. The paper also says that creating a valid scoring metric for open-ended scientific domains requires domain expertise and scientific creativity, and that users must iteratively design the scoring function (p. 38). The evidence therefore supports a conditional claim: ERA can search for software or formulas under a specified computational objective, and structural priors may move a task toward mechanism discovery. It does not support treating every benchmark winner as a genuine discovery.

## Limitations and evidence cautions

1. **Metric and benchmark dependence.** ERA optimizes whatever score is supplied. The paper itself says metric design is a major scientific input for open-ended problems (p. 38). A better score can reward an implementation artifact, and a poor score can omit the scientific property of interest.
2. **Selection and validation scope.** ScRNA-seq model selection uses a separate development dataset and validation split, which is a strength, but final claims remain benchmark-specific and depend on the OpenProblems scoring convention, including zero for failed metrics (pp. 5-6, 16, 39).
3. **Compute failures were not fully penalized during search.** Search was optimized on 20,000-cell datasets, while holdout datasets are much larger; some replicates failed many metrics, and the authors explicitly say OOM/time failures were not selected against (pp. 6, 26).
4. **Snapshot and live-leaderboard limitation.** GIFT-Eval results are tied to the 2025-05-18 snapshot. Later structural and scoring changes make direct live-leaderboard comparisons unsound, so the paper deliberately did not submit to the live leaderboard (p. 18).
5. **Small or task-specific generalization evidence.** The headline results span several tasks, but each has a specialized dataset, metric, node budget, and prompt. The scRNA-seq method uses 500 nodes per experiment and about seven hours; COVID runs use 2,000 nodes; GIFT-Eval uses 300 nodes per dataset or over 1,000 for the unified search (pp. 16-19).
6. **High resource cost.** Per-node averages are 8.0 minutes/GPU for batch integration, 1.2 minutes/CPU for COVID, 53.3 minutes/CPU for GIFT-Eval, 16.4 minutes/GPU for geospatial, and 192.2 minutes/GPU for ZAPBench. Request/response token counts and Tesla T4 requirements are listed in Table S1 (p. 57). Cost scales linearly with explored nodes (p. 57).
7. **External idea and model dependence.** Several experiments use paper summaries, Gemini Deep Research, AI co-scientist, Gemini embeddings, and other external model-generated guidance (pp. 5, 14-17, 21-24, 41-42, 74-78). The paper's strongest results therefore test the combined pipeline of LLM generation, prompt engineering, external ideas, and scoring, not an isolated search algorithm alone.
8. **Manual checks remain part of the evidence.** Authors manually verified algorithm adherence, recombination content, method conversion, and some data preparation (pp. 5, 9, 17, 26, 34, 37). This supports quality control but limits a claim that the workflow is fully autonomous.
9. **Benchmark overfitting and comparator caveats.** The Kaggle benchmark is useful for calibration against thousands of humans but is not itself a sophisticated scientific task (p. 4). DLRSD comparisons use reported results from prior papers, while ZAPBench comparisons involve different computational regimes and specialized runs (pp. 35-36, 53, 73).
10. **Reproducibility is bounded.** A reference implementation and representative search data are linked, but the paper's claims rely on changing external datasets, leaderboard snapshots, LLM behavior, model versions, and infrastructure. The authors note that Gemini models evolved since the experiments (p. 18).
11. **Safety boundary.** The system lowers the technical barrier for sophisticated computational work. The authors explicitly warn about use in sensitive or dangerous domains and frame the work as carrying systemic risk as inference-time compute and foundation-model capability increase (p. 12).
12. **Genuine-discovery claim is conditional.** The paper distinguishes the benchmark results from genuine discovery and states that causal/theoretical interpretation requires appropriate priors and scoring functions. The two cited discovery examples are not independently established by the benchmark tables in this PDF (p. 38).

## Evidence boundary

This PDF supports the existence and design of a code-level LLM mutation loop with flat PUCT/UCB selection, empirical execution feedback, research-idea injection, and conceptual recombination; it supports the reported benchmark results and the stated resource, snapshot, failure, and manual-validation caveats. It does not establish that leaderboard superiority is equivalent to scientific novelty, that the fixed-snapshot numbers remain current, that all generated methods are robust outside the evaluated datasets, or that the cited genuine-discovery deployments are independently reproducible from this PDF alone.

EVIDENCE_COMPLETE: yes
