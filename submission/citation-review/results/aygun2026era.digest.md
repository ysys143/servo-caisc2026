# Digest: aygun2026era

**Full title:** An AI system to help scientists write expert-level empirical software
**Venue:** arXiv preprint arXiv:2509.06503v2 [cs.AI], 15 May 2026 (header date 2026-05-19). 78 pages.
**Lead authors:** Eser Aygün, Anastasiya Belyaeva, Gheorghe Comanici, Marc Coram, Hao Cui, Jake Garrison, et al. (Google DeepMind, Google Research, Google Platforms & Devices; with MIT, Harvard SEAS, McGill, Caltech). Equal contribution in alphabetical order. Corresponding: Shibl Mourad (shibl@google.com), Michael P. Brenner (mbrenner@google.com).
**System name:** ERA = **Empirical Research Assistance**.

---

## Thesis / problem
Scientific discovery is bottlenecked by the slow, manual creation of software for computational experiments (abstract, lines 30–31; Intro lines 62–67). The paper presents **ERA**, an AI system that **automatically creates expert-level scientific software whose goal is to maximize a quality metric** (abstract lines 32–34). ERA pairs a **Large Language Model (LLM) with Tree Search (TS)** to systematically improve a quality score and navigate the large solution space. The central object is **"empirical software" — software designed to maximize a measurable quality score** (Intro line 55). Claimed contribution: first system to beat human performance across a wide range of well-studied scientific problems (Discussion lines 639–642).

## Method — does ERA generate expert-level EMPIRICAL SOFTWARE judged by a FIXED COMPUTATIONAL EVALUATOR / held-out QUALITY METRIC? **YES. Is there any PHYSICAL escalation? NO — purely computational.**
- ERA converts "software creation into a scorable task" — it searches for a **program whose output maximizes a quality score** (Discussion lines 583–586). Every task is scored by a **fixed computational evaluator / held-out quality metric**, never a physical/wet-lab experiment.
- Pipeline (Fig. 1a; Methods lines 679–726): LLM is prompted with a task description, the **evaluation metric**, and data → produces Python code → code is **executed and scored in a sandbox** (CPU/GPU) → score + logs used to hill-climb. No laboratory, no robotics, no physical measurement anywhere.
- **Search algorithm:** PUCT/UCB tree search inspired by AlphaZero (ref 47), but because children cannot be exhaustively enumerated every node is a candidate for expansion; sampling is from the whole node set, making it **closer to Flat UCB than MCTS/AlphaZero** (lines 683–689). No random rollouts; randomness comes from LLM sampling (lines 690–693). PUCT formula uses rank-normalized scores; **c_puct = 1** tuned on Kaggle (line 712). Mutations occur at the **code level**; ideas are injected via prompts (line 718). Score **saturates after 300–1000 nodes** (line 720).
- **Core model:** all experiments used **Gemini 2.5 Flash**; improvement with Gemini 2.5 Pro was "modest" (lines 725–726).
- **Research-idea injection** (Fig. 1c; Methods lines 772–787): instructions from highly-cited papers, textbooks, search engines, or LLM research agents (**Gemini Deep Research**, **AI co-scientist**) are injected into the prompt; PDFs summarized by Gemini 2.5 Pro. ERA then writes code implementing the idea, which is scored.
- **Held-out evaluation is explicit** throughout: holdout OpenProblems datasets (batch integration), rolling validation window / three-week holdout (COVID), official train/val/**test** splits (GIFT-Eval, ZAPBench), held-out test images (geospatial), held-out integrals (numerics).

## Key headline claims (abstract / Discussion)
- **40 novel methods** for single-cell (scRNA-seq) analysis that outperformed the top human-developed methods on a public leaderboard (abstract lines 36–38; Discussion line 664).
- **14 models** that outperformed the CDC (CovidHub) ensemble and all other individual models for forecasting COVID-19 hospitalizations (abstract lines 38–40; Discussion line 665).
- Also expert-level software for geospatial analysis, neural-activity prediction in zebrafish, numerical solution of integrals, and a novel rule-based time-series forecasting construction (abstract lines 39–41).

---

## FACTS TABLE (exhaustive)

### System / algorithm / cost
| Value | Location | Context |
|---|---|---|
| Core model = Gemini 2.5 Flash (all experiments) | Methods lines 725–726 | Gemini 2.5 Pro improvement "modest" |
| c_puct = 1 | line 712 | PUCT exploration constant, tuned on Kaggle |
| Score saturates after 300–1000 nodes | line 720 | Breakthrough plots |
| Search = Flat-UCB-like PUCT, no rollouts | lines 683–693 | Inspired by AlphaZero (ref 47) |
| Gemini text embedding = 3,072-dim vectors | lines 831–834 | Used for cosine-similarity clustering of generated code |
| Per-node cost table (S1) | lines 19268–19320 | Request/Response tokens, duration (min), sandbox type |
| Batch Integration: 16,171 req / 4,183 resp tok / 8.0 min / GPU (T4) | S1 | |
| Covid Forecasting: 9,607 / 3,392 / 1.2 min / CPU | S1 | |
| GIFT-Eval: 15,828 / 9,308 / 53.3 min / CPU | S1 | |
| Integrals: 224,415 / 6,074 / 1.5 min / CPU | S1 | Req tokens inflated by image tokenization |
| Geospatial: 7,186 / 3,172 / 16.4 min / GPU | S1 | |
| ZAPBench: 16,809 / 8,036 / 192.2 min / GPU | S1 | |

### Kaggle Playground benchmark (development benchmark)
| Value | Location | Context |
|---|---|---|
| 16 playground competitions, 2023 season (Season 3) | lines 166–167; Table S2 | Regression + classification; scored by direct Kaggle submission (public percentile rank) |
| ERA beats single LLM call, best-of-1000, and AIDE (ref 13) | lines 173–175; Fig. 1b | Metric = average public leaderboard percentile over 16 tasks |
| TS + expert advice; TS + Boosted Decision Tree (BDT) from scratch | lines 178–182; Tables S4, S5 | Problem-specific advice substantially improves performance; adherence manually verified |

### scRNA-seq batch integration (Genomics)
| Value | Location | Context |
|---|---|---|
| OpenProblems v2.0.0 benchmark; 15 SOTA + 8 control methods, 13 metrics, 6 datasets (human & mouse) | lines 194–198 | As of July 2025 |
| Holdout n = 1,747,937 total cells | line 205 | Reported performance on holdout OpenProblems datasets |
| No advice (TS) ≈ ComBat conceptually, beats leaderboard | lines 208–209 | ERA with no research idea |
| ERA beat published result for 8 of 9 methods (overall score) | lines 213–214; Fig. 2b | 9 methods selected incl. 6 highest-performing |
| BBKNN (TS) = top method: **14% overall improvement over best published method (ComBat)** | lines 214–217 | Equaled/outperformed published BBKNN in every dataset, 11/13 metrics |
| ComBat-corrected PCA embedding introduced at implementation attempt 429 | line 320; Fig. 2c | Recombination of ComBat + BBKNN drove the boost |
| 55 recombinations of all pairs of 11 base methods | lines 238–241 | Programmatically generated |
| 24 of 55 (44%) beat BOTH base methods; 22 of remaining 31 beat one | lines 244–246 | Recombination outperformance |
| 21 additional ideas from Gemini Deep Research + AI co-scientist | lines 247–248 | |
| **40 of 87** methods beat all current OpenProblems leaderboard methods | lines 248–250; Fig. 2d | Breakdown: 6/11 base, 29/55 recombination, 4/9 Deep Research, 1/12 AI co-scientist |
| Overall score = arithmetic mean of 78 measurements (13 metrics × 6 datasets), NaN→0 | lines 864–868 | Control-scaled, clamped [0,1] |
| 500 nodes per tree search; ~7 h each | lines 841–842 | 3 replicates per method |
| Training data: CZ CELLxGENE Discover; 22 candidate datasets → 1 selected; two disjoint N=20,000 subsets | lines 843–858 | Separate from test to avoid overfitting |
| Replication universe: 19 methods (July 11 2025) → 16 research ideas → 9 optimized | lines 869–880 | Excluded 6 foundation models (UCE, SCimilarity, scGPT zero-shot, scGPT fine-tuned, Geneformer, scPRINT) + scANVI (data leakage) |
| Hyperparameter opt = Optuna TPE, 5× #params trials | lines 898–905 | Shows ERA gain exceeds hyperparameter tuning |

### COVID-19 hospitalization forecasting (Public Health)
| Value | Location | Context |
|---|---|---|
| CovidHub (COVID-19 Forecast Hub), CDC-coordinated | lines 338–340 | Primary US benchmark |
| 52 US states/territories, current + 3 weeks, 23 quantiles | lines 341–343 | Scored by **Weighted Interval Score (WIS)** |
| Retrospective; data as of May 1 2025; 6-week rolling validation window over 2024–25 season | lines 350–352 | |
| **'Google Retrospective' avg WIS = 26 vs CovidHub Ensemble avg WIS = 29** | lines 358–359; Fig. 3b | Lower is better; ERA best overall |
| 2000 nodes per run | line 915 | |
| Replication: 8 models from brief public descriptions; ERA exceeded original in 6 of 8 | lines 363–366; 918–928 | 2 worse (JHU_CSSE-CSSE_Ensemble, OHT_JHU-nbxd) used external data ERA lacked |
| Recombination: 26 hybrids; 11 beat BOTH parents (WIS) | lines 454–455 | |
| **14 total strategies beat CovidHub-ensemble**: 10 recombination + 2 Deep Research + 1 AI co-scientist + 1 replicated baseline | lines 458–460; Fig. 3e | 3-week eval: 3 ref dates × 4 horizons × 52 jurisdictions |
| Most frequent winning parents: CMU-climate_baseline + UMass-ar6_pooled | lines 467–470 | Synergistic hybridization pattern |
| Data source = NHSN HRD (CDC); missing → 0; only extra input = static population | lines 907–913 | Minimal preprocessing |

### Best-of-N ablation (Table 1, lines 479–545)
N = 128 ERA search nodes vs BoN = best-of-N=1000. Batch integration higher-better; Epidemiology (flu forecasting) lower-better. Validation set.
| Model | BoN (batch / epi) | ERA (batch / epi) |
|---|---|---|
| Gemini 2.5 Flash | 0.6306 / 106.55 | 0.6552 / 93.07 |
| Mistral Medium | 0.6129 / 95.73 | 0.6332 / 87.98 |
| Claude Sonnet 4.6 | 0.6502 / 85.03 | 0.6575 / 84.56 |
| GPT-5 | 0.6740 / 78.04 | 0.6671 / 74.55 |
| Gemini 3.1 Pro | 0.6461 / 92.39 | 0.6641 / 72.70 |
ERA beats BoN for all models/problems **except GPT-5 on batch integration** (lines 808–811).

### GIFT-Eval time-series forecasting
| Value | Location | Context |
|---|---|---|
| GIFT-Eval = 28 datasets, 7 domains (main body) / 97 datasets (Methods) | lines 549; 959–966 | Normalized MASE vs seasonal naive; snapshot 5/18/2025 |
| Per-dataset: 92 of 97 tree searches, 300 nodes each, full ML libs | lines 959–964 | 5 largest excluded (compute); ERA beat entire May 18 2025 leaderboard incl. foundation models |
| Unified solution: >1000 nodes, basic libs only (numpy, pandas, holidays), geometric-mean normalized MASE | lines 965–969 | Novel rule-based decomposition construction |
| MASE trajectory: 0.82 → 0.77 → **final 0.734** | lines 974–983 | 8 preset configs after 500-node refinement |
| Deliberately did NOT submit to live leaderboard | lines 948–954 | Avoid unsound comparison after protocol changes (7/24/2025 scoring fix, 8/5 Agentic category, 8/25 Zero-shot redefinition) |

### Geospatial segmentation (Supplementary Note A.1)
| Value | Location | Context |
|---|---|---|
| DLRSD dataset (dense-labeled UC Merced), 17 class labels | lines 9833–9837 | Semantic segmentation |
| 80/20 train/test split; held-out test = 420 images; metric = mIoU | lines 9838–9840 | |
| 3 top ERA solutions all mIoU > 0.80, beat recent academic papers | lines 9841–9843; Table S14 | UNet++ (efficientnet-b7), U-Net (se-resnext101), SegFormer; all use Test-Time Augmentation |

### ZAPBench (Neuroscience)
| Value | Location | Context |
|---|---|---|
| Larval zebrafish, light-sheet microscopy; 71,721 neurons × 7,879 time steps | lines 9854–9861 | Whole-brain cellular-resolution activity |
| Predict up to 32 steps ahead given past 4 steps; splits 70/10/20 per stimulus; metric = MAE | lines 9872–9877 | |
| ERA beat all baselines incl. best video Unet, EXCEPT 1-step-ahead | lines 9886–9888 | Separate model built for 1-step; achieved leading 1-step performance |
| ERA model: <2 h on single T4 GPU vs 36 h on 16 A100 GPUs for Unet | lines 9895–9896 | Orders of magnitude cheaper |
| Jaxley biophysical exploration: single-compartment Hodgkin-Huxley + latent autoencoder | lines 9902–9911 | Competitive with time-series baselines, did not beat top video model |

### Numerical integration (Supplementary Note A.3)
| Value | Location | Context |
|---|---|---|
| 38 oscillatory integrals, infinite upper limits, where scipy quad() fails; from Gradshteyn & Ryzhik | lines 9925–9930 | Analytic solution known; converted via SymPy |
| Split n=19 train / n=19 eval; 1000 nodes; score = −log(1+|resp−ans|/|ans|) | lines 9942–9946 | |
| Best solution: partition infinite domain + Euler's series-acceleration transformation | lines 9956–9963 | Drop-in replacement for quad() |
| **Correctly evaluated 17 of 19 held-out integrals to <3% fractional error** | lines 9968–9969; Fig. S20 | |

### "Towards Genuine Discovery" (Supplementary Note A.4)
| Value | Location | Context |
|---|---|---|
| Derived exact analytical power spectrum of gravitational radiation from cosmic strings; 6 novel analytical derivations | lines 9977–9981 (ref 84) | Symbolic-math search, no empirical data — closed-form solution to a previously unsolved integral |
| In-silico larval zebrafish: structural priors (wiring diagrams) → recovered causal effective connectivity | lines 9982–9986 (ref 85) | Distinguished from statistical-shortcut predictive models |

---

## Scope & limitations (explicit)
- **Critical distinction** drawn between "optimizing empirical predictive models" and "genuine scientific discovery, the latter of which requires reasoning about underlying theories, causal mechanisms, and mathematical frameworks" (lines 648–653). The core benchmarks "primarily emphasize advanced empirical software engineering to allow for rigorous, automated scoring."
- Requires a **scorable task with a quality metric**. For open-ended domains, "inventing an appropriate scoring metric requires significant domain expertise and scientific creativity," and **the user must iterate the scoring function** (lines 9987–9999).
- **More resource-intensive** than single/zero-shot prompting; cost scales linearly with node count (lines 10000–10004; Table S1).
- Snapshotting benchmarks to fixed dates for stability; deliberately avoided live GIFT-Eval submission (lines 948–954).
- **Safety risk stated:** lowers the barrier to deploying advanced models in "sensitive or potentially dangerous domains"; systemic risk from large-scale inference-time compute + rising foundation-model quality (lines 654–659).

## Does NOT claim / boundaries
- **No physical / wet-lab escalation of any kind.** All scoring is done by a fixed computational evaluator on held-out data in a code sandbox. No robotics, no laboratory experiments, no physical measurement.
- Does **not** claim genuine scientific discovery for the core benchmarks — those are framed as empirical software engineering; discovery is only "towards" in Supplementary Notes (mathematical + in-silico neuroscience), still computational.
- Does **not** use large pre-training data the way foundation-model baselines do (explicitly noted for GIFT-Eval, lines 950–952; and foundation models excluded from scRNA-seq comparison).
- Numeric methods used as drop-in replacements only when the standard method fails; otherwise defer to quad() (lines 9970–9973).

## Section map
- **Abstract** (lines 30–48) — ERA = LLM + Tree Search creating expert-level empirical software to maximize a quality metric; 40 scRNA-seq methods, 14 COVID models, plus geospatial/ZAPBench/integrals/time-series.
- **Introduction** (54–81) — empirical software bottleneck; ERA overview; developed on Kaggle; research-idea injection.
- **Results** (83–580) — Overview of scorable tasks; Kaggle benchmark; scRNA-seq batch integration (Fig. 2); COVID-19 (Fig. 3); Best-of-N (Table 1); GIFT-Eval; brief geospatial/neuro/numerics.
- **Discussion** (582–672) — related fields (Genetic Programming, Generative Programming, LLMs-for-code, AutoML, LLM+Search incl. FunSearch/AlphaEvolve, science agents); empirical-vs-genuine-discovery distinction; safety.
- **Methods** (678–1014) — code-mutation system + PUCT (Algorithm 1); research-idea injection; ERA-vs-BoN; recombination; Gemini embeddings; per-task methods (scRNA-seq, COVID, GIFT-Eval).
- **References** (1020–); Author Contributions (1244); Acknowledgements (1252).
- **Extended Data** Figs. 1–8, Tables 1–2 (adherence inspection, breakthrough plots/trees, recombination performance).
- **Supplementary Notes A.1–A.5** (9823–10009) — geospatial, ZAPBench, numerical integrals, "towards genuine discovery," computational cost.
- **Supplementary Figures S1–S20; Tables S1–S19** (10010–20618) — experimental designs, prompts, leaderboard snapshot (S12), configs.
