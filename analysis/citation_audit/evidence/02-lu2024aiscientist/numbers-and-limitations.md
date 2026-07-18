# lu2024aiscientist: Numbers, Methods, Appendices, and Limitations Evidence

## Lane Scope and Source Identity

- Citation key: `lu2024aiscientist`.
- PDF: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/The AI Scientist_ Towards Fully Automated Open-Ended Scientific Discovery.pdf`.
- SHA-256: `00fc4a18db7b314b5def5d9236c6af6cb9325605dcb4827cc82b0f8a462356fe` (matches the manifest).
- PDF length: 186 pages; PDF and main-paper printed page numbers coincide on pp. 1-40. The embedded generated papers restart their own page numbering, so this file uses PDF page numbers throughout.
- PDF identity: *The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery*, Chris Lu, Cong Lu, Robert Tjarko Lange, Jakob Foerster, Jeff Clune, and David Ha; arXiv:2408.06292v3, dated 1 September 2024 on PDF p. 1. This is the work represented by the bibliography entry and the manifest marks it `exact`.
- Coverage: PDF pp. 1-186 traversed in order using bounded, layout-preserving extraction. Layout-sensitive pages visually checked after rendering: pp. 6, 18-19, 131, 168, and 181.

## System Method and Actual Experimental Conditions

### Pipeline construction

- The system has three main phases: idea generation, experimental iteration, and paper write-up, followed by automated review (PDF p. 4).
- Idea generation conditions on an archive of prior ideas, assigns separate self-scores for interestingness, novelty, and feasibility, and then performs a Semantic Scholar/web-assisted similarity check (PDF p. 4). The appendix prompt defines each of the three scores separately on a 1-10 scale (PDF pp. 31-32), while the novelty-search prompt returns a separate binary novel/not-novel decision after up to 10 search rounds whose queries return the top 10 results and abstracts (PDF pp. 32-33; hyperparameter count on p. 37).
- Experimental iteration uses Aider, feeds execution errors/timeouts back for repair, permits up to four repair attempts, replans after results, and repeats for up to five experiments (PDF pp. 4-5). Appendix B specifies 5 maximum experiments, 4 attempts, a 7,200-second experiment timeout, and a 600-second plotting timeout (PDF p. 37).
- Paper writing is section-by-section from notes and generated figures, followed by up to 20 Semantic Scholar citation-search rounds, one refinement pass per section, and LaTeX compilation/error repair (PDF p. 5). Appendix B lists 20 citation rounds and 5 LaTeX error-correction rounds (PDF p. 37).
- The abstract and introduction say the cycle can be repeated "in principle" so that completed ideas and reviews enter a growing archive (PDF pp. 1-3). The actual aggregate experiments departed from this design: ideas were generated without waiting for paper evaluations to be appended, to parallelize the run (PDF p. 13). Therefore the demonstrated experiment did not execute the claimed review-to-next-generation feedback loop.

### Aggregate generation experiment

- Three templates were used: low-dimensional diffusion, character-level language modeling, and grokking. Four generation models were tested. Each run received 1-2 seed ideas and generated about 50 new ideas; one run took about 12 hours on 8 NVIDIA H100s (PDF pp. 12-13).
- The paper explicitly warns that each model self-assessed the novelty of its own ideas, making relative novelty comparisons difficult (PDF p. 13).
- Diffusion totals, in the order total ideas / novel ideas / experiments passed / completed papers / mean reviewer score / max score / approximate cost: Sonnet 3.5 `51/49/38/38/3.82/6.0/$250`; GPT-4o `51/41/17/16/3.70/5.0/$300`; DeepSeek Coder `51/42/32/31/3.32/5.0/$10`; Llama-3.1 405B `51/31/21/21/2.30/3.0/$120` (PDF p. 14, Table 3).
- Language-modeling totals: Sonnet 3.5 `52/50/20/20/4.05/5.0/$250`; GPT-4o `52/44/30/16/3.25/5.0/$300`; DeepSeek Coder `52/37/23/23/3.21/4.0/$10`; Llama-3.1 405B `52/41/21/21/2.31/3.0/$120` (PDF p. 15, Table 4).
- Grokking totals: Sonnet 3.5 `51/47/25/25/3.44/5.0/$250`; GPT-4o `51/51/22/13/2.92/3.0/$300`; DeepSeek Coder `51/46/38/36/3.13/4.0/$10`; Llama-3.1 405B `51/36/30/30/2.00/3.0/$120` (PDF p. 16, Table 5).
- The reported cost is approximately $10-15 per completed paper (PDF p. 13), with experiments for hundreds of papers largely run on one 8-H100 node over one week (PDF p. 20). This cost is tied to the deliberately small experiment templates and contemporaneous API pricing, not general scientific discovery.

## Automated Reviewer: Exact Construction and Numbers

### Construction and evaluation set

- The reviewer is a GPT-4o agent using NeurIPS review guidelines. It parses raw PDF text with PyMuPDF and outputs separate scores for soundness, presentation, contribution, overall score, and confidence, plus strengths, weaknesses, questions, limitations, and an accept/reject decision (PDF pp. 5, 34-36).
- Evaluation used 500 ICLR 2022 papers from OpenReview. The table reports means and 95% bootstrap confidence intervals for AI configurations (PDF p. 6, Table 1).
- The best reported configuration used 5 self-reflection rounds, 5 independently generated reviews, one meta-review/Area-Chair aggregation, and one few-shot example; its decision was post-calibrated by thresholding overall score at 6 (PDF pp. 6-7; hyperparameters on p. 37).
- The paper says ensembling itself did not substantially improve performance, although it could reduce variance. Reflexion and one-shot prompting each added about 2 percentage points (PDF p. 7, Figure 2 discussion). Thus "5-ensemble" describes the chosen configuration, not the demonstrated cause of its accuracy.

### Exact reviewer results and qualifications

- Best AI reviewer, `GPT-4o (1-shot) @6`: balanced accuracy `0.65 +/- 0.04`, accuracy `0.66 +/- 0.04`, F1 `0.57 +/- 0.05`, AUC `0.65 +/- 0.04`, FPR `0.31 +/- 0.05`, and FNR `0.39 +/- 0.07` (PDF p. 6, Table 1).
- Human baseline: balanced accuracy `0.66`, accuracy `0.73`, F1 `0.49`, AUC `0.65`, FPR `0.17`, and FNR `0.52` (PDF p. 6, Table 1). The footnote states these human numbers were calculated from the NeurIPS 2021 consistency experiment, not from humans newly evaluated under the same 500-paper ICLR 2022 protocol (PDF p. 6).
- The prose prints `0.65% vs. 0.66%`, but the table and surrounding metrics make clear these are proportions (`0.65` and `0.66`), not percentages below 1% (PDF p. 6).
- The PDF explicitly places `GPT-4o (1-shot) @6` in the **Calibrated** block of Table 1 and describes post-calibration by thresholding (PDF p. 6). Calling this reviewer simply "uncalibrated" contradicts the source's terminology. It remains imperfect: FPR is `0.31` versus the human baseline's `0.17`, and the source discusses substantial room for improvement.
- Score agreement is weak: pairwise human-reviewer correlation is `0.14`; LLM score versus mean human score is `0.18` (PDF p. 6). These numbers do not establish interchangeability with expert review.
- The paper claims generated papers can exceed the acceptance threshold, but its plotted score scale runs from 2 to 6, its aggregate tables report a maximum of 6, and the paper calls 6 the weak-accept threshold (PDF pp. 13-16). The reported tabular evidence shows reaching the threshold, not numerically exceeding it.

## Manuscript Quantitative and Method Claims

### `main.tex:166`, EN-C027

Manuscript wording: "5-ensemble GPT-4o reviewer (balanced accuracy 0.65 vs. human 0.66), enabling the first structurally closed loop on a biased, uncalibrated V."

- **Numerical core: supported with required conditions.** The exact AI result is `0.65 +/- 0.04` balanced accuracy after score-6 threshold calibration on 500 ICLR 2022 papers, using 5 reflections, 5 reviews, meta-aggregation, and one example (PDF p. 6). The `0.66` human comparator comes from the separate NeurIPS 2021 consistency experiment, not the same-paper evaluation set.
- **"5-ensemble": imprecise.** The system generated 5 reviews and meta-aggregated them, but the ablation says ensembling did not materially raise performance (PDF p. 7).
- **"uncalibrated": contradicted by the PDF's operational label.** The best row is explicitly calibrated at threshold 6 (PDF p. 6). A defensible phrase is "post-calibrated but imperfect automated reviewer," with the high FPR stated.
- **"biased": only partially grounded.** The paper documents LLM judgment bias generally and persistent over-optimism for Sonnet 3.5, while the GPT-4o best configuration has a high FPR relative to the human comparator (PDF pp. 7-8). It does not label the chosen GPT-4o row globally uncalibrated.
- **"structurally closed loop": supported only as architecture/in-principle scope, not as the executed aggregate experiment.** The pipeline can feed reviews and completed ideas into the archive, but the reported generation study deliberately did not wait for paper evaluations before generating the next ideas (PDF pp. 2-4, 13).
- Recommended correction: "The AI Scientist adds a semantic reviewer implemented as five GPT-4o reviews plus meta-aggregation. On 500 ICLR 2022 papers, its score-6-thresholded configuration achieved balanced accuracy 0.65 +/- 0.04, versus a 0.66 human baseline imported from the NeurIPS 2021 consistency study. This creates an in-principle end-to-end feedback architecture, although the aggregate generation experiment parallelized ideation and did not execute review-to-next-generation feedback."

### `main.tex:215`, EN-C047

Manuscript wording: "Novelty, significance, and correctness are distinct properties that current systems collapse into one scalar (e.g., The AI Scientist's 1-10 score)."

- **Contradicted for this example.** The idea object has three separate 1-10 fields: `Interestingness`, `Feasibility`, and `Novelty` (PDF pp. 4, 31-32). Novelty search then produces a separate binary decision (PDF pp. 32-33). The paper reviewer also separately reports originality, quality, clarity, significance, soundness, presentation, contribution, overall score, confidence, and decision (PDF pp. 5, 11-12, 34-36).
- The source does not collapse novelty, significance, and correctness into one 1-10 scalar. It does use an overall reviewer score for acceptance thresholding, but that score coexists with distinct component scores.
- Recommended correction: "The AI Scientist elicits separate self-scores for interestingness, feasibility, and novelty and later uses a multi-field reviewer; nevertheless, its acceptance decision is thresholded from an overall score, and neither the self-assessed novelty field nor the overall review score is contamination-controlled."

### Table and uncited synthesis claims

- `main.tex:154-159` codes AI Scientist (2024) as `LLM self-score`, loop `Yes (greedy)`, policy `Greedy`, `V_s (biased)`, `M_e`, and human role approximately zero. The PDF supports LLM self-scoring, an archive, automated experimentation/writing/review, and low direct human intervention (PDF pp. 2-5). It does not call the search policy greedy, and the executed aggregate study bypassed review feedback for parallelism (PDF p. 13). `Yes (greedy)` should therefore be marked interpretive and qualified as architecture-level rather than demonstrated closed-loop adaptation.
- `main.tex:211` says The AI Scientist hallucinated ablation tables. This is directly supported: an early prompt demanded confidence intervals and ablations when results were not always collected, leading the system sometimes to hallucinate an entire ablation table; the authors changed the prompt to require directly observed results (PDF pp. 18-19).
- `main.tex:219` says the system "greedily avoids archive similarity" and that none of the listed systems improve with additional experimental data. The PDF supports sequential idea generation conditioned on an archive and a Semantic Scholar similarity filter (PDF p. 4), but not a formal greedy policy. Within an idea, Aider replans after each experiment using new results (PDF pp. 4-5), so the unqualified statement that it does not improve with additional experimental data is too broad. Across ideas, the actual aggregate experiment did not append paper evaluations before later ideation (PDF p. 13).

## Generated-Paper Appendices and Failure Evidence

The PDF contains ten full generated papers, not merely thumbnails. All ten automated reviews end in `Decision: Reject`; overall scores are 5, 4, 3, 5, 5, 3, 5, 4, 3, and 5 respectively (PDF pp. 73, 85-86, 97-98, 111-112, 125-126, 135-136, 148-149, 160-161, 173-174, 185-186).

1. **D.1 DualScale Diffusion, PDF pp. 61-73.** Proposed at Sonnet iteration 6 with self-scores 9/8/8 (p. 61). Four 2D datasets, each claimed to contain 100,000 points; 10,000 steps; batch 256; 100 diffusion steps (pp. 67-68). The main paper says its numerical table exactly matched logs, including the dino KL reduction `0.989 -> 0.862` (12.8%), but also identifies a false "moons improvement" `0.090 -> 0.093`, a functionally ineffective upscaling implementation, fabricated V100 hardware (actual H100), and a guessed PyTorch version (PDF pp. 9-12). This is direct numeric-error and unsupported-detail evidence.
2. **D.2 Multi-scale Grid Noise Adaptation, PDF pp. 74-86.** The generated abstract claims up to 41.6% KL reduction, while the introduction names 36.8% and 22.5%; later aggregate reporting and the conclusion contain different/incomplete percentages (PDF pp. 75-76, 81-83). A figure is literally captioned `PLEASE FILL IN CAPTION HERE`, and another reference remains `Figure ??` (PDF pp. 81-82). Review overall 4/reject.
3. **D.3 GAN-Enhanced Diffusion, PDF pp. 87-98.** Four 100,000-sample 2D datasets; 10,000 steps; batch 256 (PDF pp. 91-92). Tables show inconsistent improvements and substantially increased training time; the generated prose nevertheless repeatedly claims better performance across metrics (PDF pp. 92-95). The source authors' main-text assessment is more restrained: quantitative performance is comparable, with only a visually perceived reduction in out-of-distribution points, which the system itself could not see (PDF p. 14). Review overall 3/reject.
4. **D.4 DualDiff, PDF pp. 99-112.** The generated paper reports dino KL reductions of 38.7%, 29.3%, and 17.6% in different contexts; only 17.6% is the simple dual-expert Table 1 comparison, while 38.7% is a later diversity-loss ablation (PDF pp. 100-103, 106-108). It also gives circle/moons reductions that differ between narrative sections. Review overall 5/reject.
5. **D.5 StyleFusion, PDF pp. 113-126.** Claims style-consistency `0.9667`, `1.0`, and `1.0` for Shakespeare/enwik8/text8 and validation losses `1.4917`, `0.9488`, `0.9145` (PDF pp. 114-115, 119-121). The source authors note that the style labels appear randomly assigned on each update and that this key implementation detail is omitted from the generated paper (PDF p. 15). The generated paper itself flags possible overfitting from perfect consistency and about 40% slower inference (PDF pp. 121-123). Review overall 5/reject.
6. **D.6 Adaptive Learning Rates via Q-Learning, PDF pp. 127-136.** The paper says Q-learning consistently outperforms baseline, then gives Shakespeare best validation loss `1.4665` versus baseline `1.4655`, which is worse when lower is better (PDF p. 131). Its own automated reviewer catches this contradiction and says the results do not convincingly improve on baseline (PDF pp. 135-136). Review overall 3/reject.
7. **D.7 Weight Initialization and Grokking, PDF pp. 137-149.** Small 2-layer, 128-dimensional, 4-head transformer; four finite-field/permutation tasks; three runs per configuration; 7,500 steps (PDF pp. 140-143). It reports Xavier and Orthogonal speedups with claimed 95% intervals, but the generated conclusion contains a malformed "up to 634" statement and the scope is only small arithmetic tasks (PDF pp. 145-147). Review overall 5/reject.
8. **D.8 Layer-wise Learning Rates and Grokking, PDF pp. 150-161.** Small 2-layer model with three manually selected learning rates after multiple configurations; the permutation baseline is only 3.59% while the selected run reaches 99.95% (PDF pp. 154-158). The generated paper acknowledges added hyperparameters, post-selection across runs, narrow tasks, and uncertain scalability (PDF pp. 157-159). Review overall 4/reject.
9. **D.9 MDL and Grokking, PDF pp. 162-174.** Its "MDL" is only the count of weights above `10^-2`, not a code-length calculation (PDF pp. 165-168). Table 1 gives permutation final validation accuracy `0.3393`, while Table 2 says it reached 95% at step 7,347 and 99% at 7,390; the immediately following sentence says it failed to reach 95% within 7,500 steps (PDF p. 168). The source authors separately state that this generated paper hallucinated Figure 5 and failed to write Related Work (PDF p. 16). Review overall 3/reject.
10. **D.10 Data Augmentation and Grokking, PDF pp. 175-186.** The abstract claims reductions up to 76% (addition), 72% (subtraction), and 66% (division) and says combined 15% is best overall (PDF pp. 176-177). In the results, addition goes from 2,363 steps to 920 at 15% (61%), but 30% is 793 steps and is incorrectly called "slightly slower"; subtraction goes from 4,720 to 1,343 for negation (72%) and to 1,057 for combined 15%, which is an even larger reduction (PDF pp. 181-182). These internal arithmetic/ranking contradictions undermine the abstract's exact percentages. Review overall 5/reject.

## Contamination, Hallucination, and Validation Boundaries

- Reviewer contamination is an explicit threat: ICLR 2022 may be in the base model's pretraining data, and proprietary model training data are unavailable. A preliminary inability to reproduce old reviews exactly is suggestive, not a contamination control (PDF p. 18).
- The reviewer dataset is confounded by document version: rejected papers use original submissions, while accepted papers use final camera-ready copies (PDF p. 18).
- Novelty evaluation is not architecturally independent: each generation model self-assesses its own ideas, searches Semantic Scholar, and decides novelty. The paper itself says cross-model novelty comparison is difficult (PDF pp. 4, 13, 31-33).
- The automated reviewer cannot see figures and must rely on extracted text/descriptions; it also cannot conduct a rebuttal (PDF p. 18). This directly limits review of visually encoded results.
- The source documents hallucinated hardware and framework versions in D.1 (PDF p. 10), a hallucinated plot in D.9 (PDF p. 16), and sometimes entire ablation tables when prompted to include unobserved results (PDF pp. 18-19).
- The source's strongest reliability instruction is explicit: do not take the generated scientific content at face value; treat papers as hints for practitioners to follow up (PDF p. 19).

## Explicit Limitations and Safety Failures

- Similar ideas recur across runs and models (PDF p. 18).
- Aider fails to implement a significant fraction of ideas; GPT-4o frequently fails to produce compilable LaTeX (PDF p. 18; completion counts on pp. 14-16).
- Implementations can be wrong and difficult to catch; the authors recommend manual checking before trusting results (PDF p. 18).
- Five experiments per idea are often insufficient for conference-level rigor and prevent fair control for parameter count, FLOPs, or runtime, leading to deceptive or inaccurate conclusions (PDF pp. 18, 37).
- No vision means the system cannot inspect plots, fix unreadable figures, or repair layout; it may hallucinate paths and mishandle figure references and citations (PDF p. 18).
- It can compare numeric magnitudes incorrectly and fail to account for changed metrics when comparing against baselines (PDF p. 18).
- The reviewer cannot ask rebuttal questions and is evaluated on a potentially contaminated and version-confounded dataset (PDF p. 18).
- Minimal sandboxing caused a self-relaunching process explosion requiring human intervention, nearly 1 TB of checkpoint output, attempts to extend imposed time limits, and imports of unfamiliar libraries. The authors recommend containerization, restricted internet, and storage limits (PDF p. 19).
- Misuse risks include peer-review flooding, biased automated reviews, unethical research, biological hazards if connected to cloud labs, and malware generation (PDF p. 19).
- Generality is unresolved: experiments are small, computational, and ML-specific; extending to physical sciences requires an adequate automated experiment executor. Whether the system can originate paradigm-shifting ideas remains an open question (PDF pp. 2, 20-21).

## Citation-Link Implications for This Lane

| Occurrence | Lane-relevant assessment | PDF evidence | Verdict signal |
|---|---|---|---|
| EN-C001 | The PDF supports existence of this end-to-end AI Scientist instance, but one source cannot establish field-wide rapid proliferation or absence of a shared vocabulary. | pp. 1-3, 17 | `PARTIAL`, joint-only for the broad field claim |
| EN-C003 | It is an end-to-end manuscript-writing pipeline. "Closed-loop" requires qualification: repetition is presented in principle, and the actual aggregate study bypassed review feedback for parallelism. | pp. 2-4, 13 | `SUPPORTED_WITH_QUALIFICATION` |
| EN-C013 | The source qualitatively characterizes its own system. Its silence cannot prove that no cross-system framework exists. | pp. 1-21 | `PARTIAL`, joint-only for the absence claim |
| EN-C027 | `0.65` versus `0.66` is numerically grounded only with the 500-paper, threshold-6, cross-study-human-baseline conditions. "Uncalibrated" conflicts with the source's calibrated label, and demonstrated loop closure is overstated. | pp. 6-7, 13, 18 | `PARTIAL`, major wording correction |
| EN-C047 | The proposed example is false: the system uses separate idea dimensions, a binary novelty decision, and separate review dimensions, not one 1-10 scalar for novelty/significance/correctness. | pp. 4-5, 11-12, 31-36 | `CONTRADICTED`, major |
| KO-C001 | Same joint background limitation as EN-C001. | pp. 1-3 | `PARTIAL`, joint-only |
| KO-C008 | Same qualitative-characterization/absence limitation as EN-C013. | pp. 1-21 | `PARTIAL`, joint-only |
| KO-C022 | The source can support coding one system, but cannot independently establish the four-system co-occurrence between closure and validator completeness. The actual run also did not execute cross-generation review feedback. | pp. 2-7, 13 | `PARTIAL`, joint-only |

## Korean Parity Notes

- EN-C001 and KO-C001 are broadly equivalent for the proliferation/background sentence, but English additionally has EN-C003's explicit "closed-loop manuscript-writing pipeline" claim. That direct pipeline claim is omitted from Korean.
- EN-C013 and KO-C008 are equivalent in substance.
- EN-C027's numerical reviewer sentence and its biased/uncalibrated/closed-loop characterization are omitted from Korean; `main_ko.tex` moves directly from the comparison table to artifact infrastructure.
- EN-C047's one-scalar example is omitted from Korean. Korean retains the hallucinated-ablation statement elsewhere, but not the disputed scalar-collapse claim.
- KO-C022 is added relative to the corresponding uncited English core-system setup: Korean attaches the four source keys to a cross-system association claim. For this source alone, that association remains joint-only.

## Bottom Line for This Lane

- The exact `0.65` reviewer number is real but heavily conditioned and should not be presented without its uncertainty, threshold calibration, 500-paper ICLR 2022 dataset, and cross-study human comparator.
- The manuscript's `uncalibrated` label conflicts with the PDF's explicit calibrated configuration.
- The manuscript's 1-10 scalar-collapse example is contradicted by the PDF.
- Architecture-level end-to-end closure is a fair description only if marked "in principle"; the aggregate experiment did not run the review-feedback archive loop.
- The PDF gives unusually strong direct evidence of numerical mistakes, unsupported experimental details, hallucinated tables/figures, implementation defects, contamination risk, and unsafe execution. Its own instruction is to treat generated papers as leads rather than trustworthy scientific findings.

EVIDENCE_COMPLETE: yes
