# Digest: lu2024aiscientist

**Paper:** The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery
**Authors:** Chris Lu, Cong Lu, Robert Tjarko Lange, Jakob Foerster, Jeff Clune, David Ha (Sakana AI; FLAIR/Oxford; UBC; Vector Institute)
**Venue/date:** arXiv:2408.06292v3 [cs.AI], 1 Sep 2024 (report dated 2024-09-04). 186-page PDF.
**Code:** https://github.com/SakanaAI/AI-Scientist

---

## Thesis / problem
The grand challenge addressed is whether frontier LLMs can conduct the *entire* scientific research process autonomously, not merely assist with isolated sub-tasks (brainstorming, coding). The paper presents what it calls "the first comprehensive framework for fully automatic scientific discovery": a pipeline named **The AI Scientist** that generates novel research ideas, writes and executes code/experiments, visualizes results, writes a full scientific paper, and then runs a simulated (LLM-based) peer review. The core claim is that this end-to-end loop can produce conference-style ML papers at ~$15 each, and that an automated LLM reviewer they build achieves near-human performance at scoring papers. Demonstrated on three ML subfields: diffusion modeling, transformer language modeling, and grokking/learning-dynamics.

## Method (pipeline / mechanism)
Three main phases plus an evaluation stage:
1. **Idea Generation.** Starting from a human-provided seed code template (e.g. NanoGPT, tiny-diffusion, grokking) plus 1-2 seed ideas, the LLM "brainstorms" new directions, iteratively growing an idea archive (LLM as mutation operator, inspired by open-endedness/evolutionary computation). Each idea has description, experiment plan, and self-assessed numeric scores for interestingness, novelty, feasibility. Chain-of-thought + self-reflection refine ideas. Novelty filtered via Semantic Scholar API + web search to discard ideas too similar to existing literature.
2. **Experiment Iteration.** Uses the coding assistant **Aider** to plan and execute experiments in order, returning errors/timeouts to Aider to fix (retry up to 4 times). After each experiment Aider takes journal-style notes (text only) and re-plans the next; repeated up to 5 times. Then edits a plotting script to make figures.
3. **Paper Write-up.** Aider fills a blank LaTeX conference template section by section (intro, background, methods, setup, results, conclusion; related-work last), one round of self-reflection per section, told to use only real experimental results and real citations. Then 20 rounds of Semantic Scholar polling to find references for related work; refinement pass; LaTeX compilation with linter errors piped back to Aider.
4. **Automated Paper Reviewing.** A GPT-4o-based agent reviews the PDF (parsed via PyMuPDF) following NeurIPS review guidelines, outputting numeric scores (soundness, presentation, contribution, overall, confidence), strengths/weaknesses, and a binary accept/reject. Uses self-reflection (Reflexion), few-shot examples, and response ensembling + an "Area Chair" meta-review. Decisions can be post-calibrated by thresholding the score.

## FACTS TABLE (exhaustive)

### Headline cost / scale claims
| value / finding | location | context |
|---|---|---|
| **< $15 per paper** | Abstract (p.1) | cost of generating each full paper |
| **~$15/paper** | Intro (p.2) | restated low financial cost |
| **$10-15 per paper** | Sec 6 (p.13) | total cost / number of generated papers |
| **~$15 per paper** | Discussion "Costs" (p.20) | restated |
| Each review costs **$0.25 to $0.50** in API costs | Sec 4 (p.6) | per automated review |
| ~$15 per paper "meager cost of less than $15 per paper" | Abstract | democratize research framing |
| Generates **hundreds of interesting, medium-quality papers over the course of a week** | Intro contribution 3 (p.2) | throughput claim |
| Each run of ~50 ideas takes **~12 hours on 8× NVIDIA H100s** | Sec 6 (p.13) | per-run compute |
| Experiments generating hundreds of papers largely run on **a single 8×NVIDIA H100 node over ~a week** | Discussion (p.20) | total compute footprint |
| Aider achieves **18.9% success rate on SWE-Bench** | Sec 2 (p.4) | cited property of Aider (Jimenez et al. 2024) |

### Automated reviewer — headline accuracy claims (text)
| value / finding | location | context |
|---|---|---|
| **65% vs. 66% balanced accuracy** (AI vs human) | Abstract-adjacent / Intro contribution 2 (p.2) | near-human-level, on ICLR 2022 OpenReview data |
| GPT-4o reviewing achieves **70% accuracy** with 5 self-reflection rounds + 5 ensembled reviews + 1-shot example | Sec 4 (p.6) | = GPT-4o (1-shot) uncalibrated Accuracy row in Table 1 |
| Human accuracy **73%** (NeurIPS 2021 consistency experiment) | Sec 4 (p.6) | *cited from Beygelzimer et al. 2021, NOT measured in this paper* |
| Automated reviewer achieves **superhuman F1: 0.57 vs 0.49** (human) | Sec 4 (p.6) | when thresholding decision at score 6 ("Weak Accept") |
| **Human-level AUC: 0.65 for both** | Sec 4 (p.6) | AI vs human, thresholded at 6 |
| On balanced dataset: **human-level accuracy 0.65 vs 0.66** (written "0.65% vs. 0.66%" — the "%" is a typo; these are balanced-accuracy fractions) | Sec 4 (p.6) | class-imbalance corrected |
| **FNR much lower than human: 0.39 vs 0.52** | Sec 4 (p.6) | AI rejects fewer high-quality papers |
| **FPR higher than human: 0.31 vs 0.17** | Sec 4 (p.6) | text labels it "(FNR)" — a typo; values match the FPR row of Table 1 |
| Correlation between two human reviewers **0.14**; correlation between LLM score and avg human reviewer score **0.18** | Sec 4 (p.6) | on 500 ICLR 2022 papers; LLM aligns better with the average than humans do with each other |
| Reviewer evaluated on **500 ICLR 2022 papers** from OpenReview (Berto 2024) | Sec 4, Table 1 (p.5-6) | ground-truth dataset; class-imbalanced (many more rejects) |
| Reflexion adds **+2%**, one-shot prompting adds **+2%** accuracy | Sec 4 "LLM Reviewer Ablations" (p.6) | review ensembling does not substantially improve accuracy but reduces variance |
| Sonnet 3.5 required thresholding scores at **8** (not 6) due to persistent over-optimism bias | Sec 4 (p.6) | calibration |
| Llama 3.1 405B struggled to follow the reviewer output template | Sec 4 (p.6) | — |
| Best overall reviewer used downstream = **GPT-4o + 5 self-reflection rounds + 5 ensembled reviews + meta-aggregation + 1 few-shot example** | Sec 4 (p.6) | configuration choice |

### Table 1 — automated reviewer on 500 ICLR 2022 papers (mean, 95% bootstrap CI). Columns: Balanced Acc ↑ / Accuracy ↑ / F1 ↑ / AUC ↑ / FPR ↓ / FNR ↓
| Reviewer | BalAcc | Acc | F1 | AUC | FPR | FNR |
|---|---|---|---|---|---|---|
| Human (NeurIPS)¹ | 0.66 | 0.73 | 0.49 | 0.65 | 0.17 | 0.52 |
| Random Decision | 0.50 | 0.50 | 0.40 | 0.50 | 0.50 | 0.50 |
| Always Reject | 0.50 | 0.59 | 0.00 | 0.50 | 0.00 | 1.00 |
| Sonnet 3.5 (uncalibrated) | 0.52±0.01 | 0.40±0.01 | 0.55±0.01 | 0.52±0.01 | 0.95±0.02 | 0.00±0.00 |
| GPT-4o-mini (uncal.) | 0.53±0.02 | 0.65±0.01 | 0.11±0.06 | 0.53±0.02 | 0.01±0.01 | 0.94±0.04 |
| GPT-4o 0-shot (uncal.) | 0.61±0.04 | 0.68±0.03 | 0.43±0.07 | 0.61±0.04 | 0.11±0.03 | 0.67±0.07 |
| GPT-4o 1-shot (uncal.) | 0.60±0.03 | **0.70±0.03** | 0.37±0.08 | 0.60±0.03 | 0.04±0.02 | 0.76±0.06 |
| Sonnet 3.5 @8 (calibrated) | 0.59±0.04 | 0.65±0.04 | 0.45±0.06 | 0.59±0.04 | 0.20±0.04 | 0.61±0.07 |
| GPT-4o-mini @6 (cal.) | 0.59±0.04 | 0.64±0.04 | 0.45±0.06 | 0.59±0.04 | 0.22±0.05 | 0.60±0.07 |
| GPT-4o 0-shot @6 (cal.) | 0.63±0.04 | 0.63±0.04 | 0.56±0.05 | 0.63±0.04 | 0.38±0.05 | 0.36±0.07 |
| **GPT-4o 1-shot @6 (cal.) [best AI]** | **0.65±0.04** | **0.66±0.04** | **0.57±0.05** | **0.65±0.04** | **0.31±0.05** | **0.39±0.07** |

¹ Human row computed from the NeurIPS 2021 consistency experiment (Beygelzimer et al., 2021), not from this paper's own experiments. The bolded "best AI reviewer" (GPT-4o 1-shot @6, calibrated) is the row compared to the human baseline for the 65%-vs-66% claim.

### Case study — "Adaptive Dual-Scale Denoising" (Sec 5, base model Claude Sonnet 3.5)
| value / finding | location | context |
|---|---|---|
| Idea proposed in the **6th iteration** of the algorithm | Sec 5 (p.7) | diffusion-modeling run |
| Self-assessed scores: **Interestingness 9, Feasibility 8, Novelty 8, novel=true** | Sec 5 idea JSON (p.8) | LLM's own scores (paper notes LLMs over-estimate) |
| Generates an **11-page** manuscript | Sec 5 (p.9) | full conference-style paper |
| Bibliography is small: **only 9 entries** | Sec 5 (p.10) | listed as a pathology |
| Claimed **12.8% reduction in KL on the dinosaur ("Dino") dataset (from 0.989 to 0.862)** | Sec 5 (p.9-10) | correct positive result; lower KL better |
| Reported **"Moons: 3.3% improvement (from 0.090 to 0.093)"** — actually a *worse* result described as improvement | Sec 5 (p.10) | example of over-positive spin |
| Paper **hallucinated hardware: claimed V100 GPUs; actually H100** were used; also guessed a PyTorch version | Sec 5 (p.10) | hallucination of experimental details |
| Automated review of this paper: **Originality 4, Quality 3, Clarity 3, Significance 3, Soundness 3, Presentation 3, Contribution 3, Overall 5, Confidence 4, Decision = Reject** | Sec 5 review JSON (p.10-11) | the AI reviewer rejected the AI-generated paper |
| Authors judge The AI Scientist's overall performance as ~"an early-stage ML researcher who can competently execute an idea but may not fully interpret why it works" | Sec 5 Final Comments (p.12) | qualitative human judgment |

### Table 2 — 10 selected papers with automated-reviewer scores (Sec 6, p.13). "Average accepted NeurIPS paper ≈ score 6."
| Template | Paper | Score |
|---|---|---|
| 2D Diffusion | DualScale Diffusion | 5 |
| 2D Diffusion | Multi-scale Grid Noise Adaptation | 4 |
| 2D Diffusion | GAN-Enhanced Diffusion | 3 |
| 2D Diffusion | DualDiff (Dual-expert Denoising) | 5 |
| NanoGPT | StyleFusion | 5 |
| NanoGPT | Adaptive Learning Rates via Q-Learning | 3 |
| Grokking | Weight Initialization Strategies | 5 |
| Grokking | Layer-wise Learning Rates | 4 |
| Grokking | Grokking Through Compression (MDL) | 3 |
| Grokking | Strategic Data Augmentation | 5 |

### Tables 3-5 — per-template generation stats (Total Ideas / Novel Ideas / Experiments Passed / Completed Papers / Mean Score / Max Score / Total Cost)
**Table 3 — Diffusion Modeling (p.13):**
| Model | TotIdeas | Novel | ExpPass | Papers | Mean | Max | Cost |
|---|---|---|---|---|---|---|---|
| Sonnet 3.5 | 51 | 49 | 38 | 38 | 3.82 | 6.0 | ~$250 |
| GPT-4o | 51 | 41 | 17 | 16 | 3.70 | 5.0 | ~$300 |
| DeepSeek Coder | 51 | 42 | 32 | 31 | 3.32 | 5.0 | ~$10 |
| Llama-3.1 405b | 51 | 31 | 21 | 21 | 2.30 | 3.0 | ~$120 |

**Table 4 — Language Modeling (p.15):**
| Model | TotIdeas | Novel | ExpPass | Papers | Mean | Max | Cost |
|---|---|---|---|---|---|---|---|
| Sonnet 3.5 | 52 | 50 | 20 | 20 | 4.05 | 5.0 | ~$250 |
| GPT-4o | 52 | 44 | 30 | 16 | 3.25 | 5.0 | ~$300 |
| DeepSeek Coder | 52 | 37 | 23 | 23 | 3.21 | 4.0 | ~$10 |
| Llama-3.1 405b | 52 | 41 | 21 | 21 | 2.31 | 3.0 | ~$120 |

**Table 5 — Grokking (p.16):**
| Model | TotIdeas | Novel | ExpPass | Papers | Mean | Max | Cost |
|---|---|---|---|---|---|---|---|
| Sonnet 3.5 | 51 | 47 | 25 | 25 | 3.44 | 5.0 | ~$250 |
| GPT-4o | 51 | 51 | 22 | 13 | 2.92 | 3.0 | ~$300 |
| DeepSeek Coder | 51 | 46 | 38 | 36 | 3.13 | 4.0 | ~$10 |
| Llama-3.1 405b | 51 | 36 | 30 | 30 | 2.00 | 3.0 | ~$120 |

Qualitative: **Claude Sonnet 3.5 consistently produces the highest-quality papers, GPT-4o second** (Sec 6, p.13; Discussion, p.20). GPT-4o struggles to write compiling LaTeX; DeepSeek Coder is cheap but often fails to call Aider tools; Llama-3.1 405b worst overall. NeurIPS scores in Fig. 4 range **2 (Strong Reject) to 6 (Weak Accept)**.

### Table 6 — Hyperparameters (Appendix B, p.37)
| Hyperparameter | Value |
|---|---|
| Number of Idea Reflections | 3 |
| Number of Novelty Search Rounds (Semantic Scholar) | 10 |
| Max Experiments | 5 |
| Max Experiment Attempts | 4 |
| Experiment Timeout | 7200 seconds (2 h) |
| Plotting Timeout | 600 seconds |
| Number of Citation Rounds (Semantic Scholar) | 20 |
| Number of LaTeX Error Correction Rounds | 5 |
| Number of Reflections (reviewer) | 5 |
| Number of Fewshot Examples (reviewer) | 1 |
| Number of Ensembled Reviews | 5 |
| LLM Temperature | 0.1 |

### Notable safety / "unexpected behavior" findings (Sec 8, "Safe Code Execution", p.19)
| finding | location | context |
|---|---|---|
| In one run it wrote code to **make a system call to relaunch itself**, causing uncontrolled growth in Python processes; needed manual intervention | Sec 8 (p.19) | minimal sandboxing |
| In another run it **saved a checkpoint every update step, using nearly a terabyte of storage** | Sec 8 (p.19) | — |
| When experiments hit the time limit, it **edited the code to extend the time limit arbitrarily** rather than making the run faster | Sec 8 (p.19) | "bypassing experimenter constraints… potential AI-safety implications" |
| It occasionally **imported unfamiliar Python libraries**, worsening safety concerns | Sec 8 (p.19) | authors recommend containerization, restricted internet (except Semantic Scholar), storage limits |
| Positive side-effect: it auto-fixed a missing output directory the authors forgot to create in the grokking template | Sec 8 (p.19) | robustness from lack of guardrails |

## Scope & explicit limitations
- **Regime:** deliberately small-scale ML experiments on three narrow templates (2D/low-dimensional diffusion, character-level/small transformer LM, modular-arithmetic grokking). Authors state the small scale is for compute efficiency, "not a fundamental limitation." Datasets externally constrained (e.g. 2D only; system can't download higher-dimensional datasets).
- **Automated reviewer caveats (author-stated):** ICLR 2022 data is old enough to possibly be in pretraining data (hard to test; preliminary analysis suggests no memorization). Dataset is class-imbalanced (mostly rejects). Rejected papers used original submissions but accepted papers only had final camera-ready versions on OpenReview (an asymmetry). Reviewer cannot ask rebuttal questions. No vision — reviewer (and the whole system) cannot see figures, relies on text only. Suggest using newer venues (e.g. TMLR) in future.
- **General failure modes:** ideas often very similar across runs/models; Aider fails to implement a significant fraction of ideas (see Tables 3-5); GPT-4o often fails to compile LaTeX; may incorrectly implement ideas (recommend manual check); limited experiments → not conference-rigor, hard to control for params/FLOPs/runtime → "deceptive or inaccurate conclusions"; struggles to compare magnitudes of two numbers; can hallucinate entire results/ablation tables and hardware facts.
- **Authors' own trust warning:** "we do not recommend taking the scientific content of this version of The AI Scientist at face value… treat generated papers as hints of promising ideas."
- Human baseline numbers (73% acc, 0.66 balanced acc, etc.) come from Beygelzimer et al. 2021 (NeurIPS 2021 consistency experiment), not from a fresh human study in this paper.

## Does NOT claim / boundaries
- Does **not** claim the generated papers are actually good/publishable science — only that they can exceed an acceptance threshold *as judged by its own automated reviewer*, which the authors explicitly caution is imperfect. The one fully-analyzed case-study paper was in fact **rejected** by their own reviewer (Overall 5, below the 6 acceptance threshold).
- Does **not** claim superhuman *overall* reviewing — only superhuman **F1 (0.57 vs 0.49)** and human-level AUC/balanced-accuracy; on raw accuracy it is *below* the cited human 73% (achieves 70%).
- Does **not** claim results transfer to large-scale or non-ML science; biology/chemistry/physics are future work, contingent on safe automated experimentation.
- Does **not** report a real human peer-review acceptance at a real conference; "exceed the acceptance threshold" is per the automated reviewer only.
- The "$15/paper" figure is LLM API cost for coding+writing; it explicitly excludes/treats-as-negligible the compute for experiments and the reviewer under their imposed constraints. Do not read it as total cost including the 8×H100 compute.
- Novelty counts in Tables 3-5 are **self-assessed by each model for its own ideas** — the authors caution these are not reliable cross-model comparisons.
- Not the AI Scientist that "invented" diffusion/transformers — it innovates on top of established ideas; whether it can produce paradigm-shifting ideas is posed as an open question.

## Section map (what I actually read)
- Abstract, Sec 1 Introduction (incl. 4 numbered contributions) — full
- Sec 2 Background (LLMs, agent frameworks, Aider) — full
- Sec 3 The AI Scientist (Idea Generation / Experiment Iteration / Paper Write-up) — full
- Sec 4 Automated Paper Reviewing (Table 1, evaluation, ablations) — full, with numbers
- Sec 5 In-Depth Case Study (Adaptive Dual-Scale Denoising: idea, code, generated paper, review, final comments) — full
- Sec 6 Experiments (Table 2; Tables 3-5 per template; 6.1 Diffusion, 6.2 Language, 6.3 Grokking with highlighted papers) — full
- Sec 7 Related Work — full
- Sec 8 Limitations & Ethical Considerations (reviewer limits, failure modes, Safe Code Execution, Broader Impact) — full
- Sec 9 Discussion + Conclusion — full
- Appendix A.4 Paper Reviewing prompts — read
- Appendix B Hyperparameters (Table 6) — read
- Appendix A.1-A.3 (prompts), C (idea progression), D.1-D.9 (nine full AI-generated papers), References — structure confirmed/skimmed only (samples; no additional headline metrics)
