# DeepScientist: results and limitations

## Audit scope and source

- Audited source: `DeepScientist Advancing Frontier-Pushing Scientific Findings.pdf`.
- Source location: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Core_Systems/DeepScientist Advancing Frontier-Pushing Scientific Findings.pdf`.
- The source reports 19 pages. This note records direct page-grounded observations from all 19 pages; no other PDF was opened and no API or model call was made during this audit.
- The paper is identified on p. 1 as arXiv:2509.26603v1, dated 30 Sep 2025.

## Page coverage

- **p. 1:** Abstract and Figure 1. The paper claims a goal-oriented autonomous system, more than 20,000 GPU hours, about 5,000 ideas, approximately 1,100 experimentally validated ideas, and improvements over human SOTA of 183.7%, 1.9%, and 7.9% across three tasks. Figure 1 frames two weeks of AI progress against several years of human progress on RAID AI-text detection and states the generated zero-shot methods use Falcon-7B.
- **p. 2:** Motivation and contributions. The authors position the system against unguided AI Scientist exploration, define goal-driven optimization, name the three tasks, state use of 16 H800 GPUs over a month-long cycle, and report 21 eventual scientific innovations plus a near-linear resource/output relationship.
- **p. 3:** Related work and the optimization formulation. Scientific value is modeled as an expensive black-box function `f(I)` over candidate methods, with the objective `arg max f(I)`. The page distinguishes engineering optimization from discovery targeting core SOTA limitations.
- **p. 4:** Figure 2 and framework setup. The closed loop is `Strategize & Hypothesize -> Implement & Verify -> Analyze & Report`; Findings Memory combines human findings with system findings, and Bayesian Optimization is motivated by costly evaluations.
- **p. 5:** Table 1 and operational details. Baselines are All at Once (ICML 2025 Spotlight, Who&When), TokenRecycling (ACL 2025 Outstanding, MBPP), and FastDetectGPT (ICLR 2024, RAID). The page specifies surrogate scoring, UCB selection, sandboxed implementation, and promotion to Progress Finding after successful validation. It also states two servers with eight H800 GPUs each, Gemini-2.5-Pro for core logic, Claude-4-Opus for code, and three human supervisors.
- **p. 6:** Table 1-style result summary, Figure 3, and the first two domain narratives. A2P is presented as causal Abduction-Action-Prediction for agent failure attribution; ACRA is presented as a stable-suffix, long-term-memory mechanism for inference acceleration.
- **p. 7:** AI Text Detection trajectory, Tables 2 and 3, and review setup. T-Detect, TDT, and PA-Detect are described as progressively changing the detector from robust statistics to wavelet and phase-congruency analysis. The page reports automated comparison against 28 public papers and introduces three human reviewers.
- **p. 8:** Figure 4, human-review summary, and post-hoc analysis setup. The paper reports full operational logs and Findings Memory, a one-week parallel scaling experiment, and causal attribution of 300 failed implementations. It states over 5,000 ideas, about 1,100 validated, 21 progress findings, 1-3% selected success, near-zero random-baseline success, and approximately 60% implementation-error failures.
- **p. 9:** Figures 5 and 6 plus trajectory/scaling analysis. The AI-text search-space plot covers 2,472 ideas and labels T-Detect, TDT, and PA-Detect as progress ideas. Scaling shows 1 progress finding at 4 GPUs, 4 at 8 GPUs, and 11 at 16 GPUs in the one-week experiment; the paper contrasts 20,000 GPU hours with over 100,000 GPU hours for testing all 5,000 candidates.
- **p. 10:** Interpretation, discussion, conclusion, and ethics start. The paper characterizes the progress rate as 1-5%, limits the current strategy to rapid-feedback domains, and says high-cost pretraining or pharmaceutical synthesis is currently impractical. It presents human-AI collaboration as the intended operating model.
- **p. 11:** Ethics continuation and references. The authors describe red-team tests for harmful computer-virus research, selective open-sourcing, withholding the Analyze & Report module, and a requirement for human supervision and final responsibility.
- **p. 12:** References only. No additional experimental result or limitation is introduced.
- **p. 13:** References only. No additional experimental result or limitation is introduced.
- **p. 14:** References only. No additional experimental result or limitation is introduced.
- **p. 15:** Human Expert Review protocol and feedback. Five papers were independently reviewed by three researchers, including two ICLR 2025 reviewers and one invited ICLR Area Chair; the review averaged 55 minutes per paper and omitted a rebuttal phase. Reviewers praised novelty but identified weak validation, missing ablations/motivation studies, and incomplete baseline/related-work context.
- **p. 16:** Bottleneck analysis. The paper states that progress-producing ideas are typically below 3% and proposes improving hypothesis quality, filtering, and implementation quality. It warns that data-driven hypothesis generation can lack theory and hallucinate.
- **p. 17:** Findings Memory and verification limitations, followed by implementation details. The paper says up to 60% of exploratory failures are implementation-level errors, calls reliable automated verification the critical defense, and emphasizes human goal-setting and oversight. It states Gemini-2.5-Pro powers reasoning, Claude-4-Opus/Claude Code v1.0.53 handles implementation, containers communicate via a port API, an independent CLI rerun counters false positives, approximately 50% of initial implementation attempts failed from internal timeouts, results were manually inspected, and fixed settings were `K=15`, `wu=1`, `wq=1`, `kappa=1`.
- **p. 18:** Cost and compute details plus short method summaries. Per-idea ideation cost is about $5, implementation averages $20 plus about 1 GPU hour, and a successful Analyze & Report finding costs about $150; total reported cost is about $100,000. The page gives an H800 estimate of about 2 TFLOPS FP16 and about `1 x 10^16` FLOPs for 70 minutes, and summarizes A2P, ACRA, T-Detect, TDT, and PA-Detect.
- **p. 19:** Appendix C links to three generated papers. No new result or limitation is stated.

## Experimental design and selection loop

The paper defines discovery as optimization over a conceptual method space, where the true scientific value is expensive and black-box (pp. 3-4). The proposed surrogate is an LLM Reviewer that scores each new idea on utility, quality, and exploration, each from 0 to 100 (p. 5). The acquisition step uses UCB:

`wu * vu + wq * vq + kappa * ve`

The top candidate is implemented in the baseline repository inside a sandbox; experimental logs update its Findings Memory record. A successful implementation is promoted to a Progress Finding, which triggers ablations, new-dataset evaluations, synthesis, and paper generation (p. 5). Retrieval is top-`K` from a structured memory because of context limits (p. 4-5), with fixed `K=15` and unit UCB weights in Appendix C (p. 17).

The experiment starts from manually reproduced, logged SOTA baselines and uses two 8xH800 servers, one system instance per GPU, with three human experts supervising outputs (p. 5). The design therefore is not a blind free-form generation test: it is a goal-conditioned, staged, filtered, memory-updated search with human-supervised baselines and a secondary command-line rerun for implementation verification (p. 17).

## Three-domain results and SOTA comparison

| Domain | Human baseline | DeepScientist method | Reported result | Reported change |
|---|---|---|---:|---:|
| Agent Failure Attribution, Who&When, handcraft | All at Once: 12.07% | A2P: 29.31% | Accuracy | `+142.8%` relative, `+17.24` points |
| Agent Failure Attribution, Who&When, algorithm-generated | All at Once: 16.67% | A2P: 47.46% | Accuracy | `+183.7%` relative, `+30.79` points |
| LLM Inference Acceleration, MBPP | Token Recycling: 190.25 tokens/s | ACRA: 193.90 tokens/s | Throughput | `+1.9%`, `+3.65` tokens/s |
| AI Text Detection, RAID | Binoculars: 0.800 AUROC, 117 ms | PA-Detect: 0.863 AUROC, 60 ms | AUROC and latency | `+7.9%`, `+0.063`; latency `-57 ms` and described as roughly 2x faster |

These figures are the table and Figure 3 values on p. 6. The abstract's 183.7%, 1.9%, and 7.9% correspond to the algorithm-generated attribution setting, acceleration throughput, and detection AUROC. For attribution, the paper explains A2P as counterfactual causal reasoning rather than pattern matching (p. 6). For acceleration, ACRA uses stable suffix patterns to add contextual memory, and the authors explicitly distinguish this from merely combining known layer-skipping or PageAttention techniques (p. 6). For detection, the progression is T-Detect -> TDT -> PA-Detect: robust t-distribution, wavelet localization, then phase congruency for temporal alignment (p. 7).

Figure 4 gives the per-domain funnel counts (p. 8): AI Text Detection has 2,472 total ideas, 600 implemented ideas, and 7 progress ideas; Agent Failure Attribution has 1,077 total, 196 implemented, and 12 progress ideas; LLM Inference Acceleration has 1,330 total, 312 implemented, and 2 progress ideas. These sum to 4,879 ideas and 1,108 implemented ideas, which is consistent with the paper's rounded prose claims of over 5,000 and about 1,100, but not numerically identical to them.

## Human final validation

The paper reports two evaluation tracks. DeepReviewer-14B compares five DeepScientist papers with 28 publicly available papers from other AI Scientist systems; Table 2 reports DeepScientist at rating 5.90 and 60% acceptance, while the authors warn that public papers may be curated (p. 7). Separately, a three-person program committee reviewed all five papers independently. Table 3 reports DeepScientist average confidence 4.07, soundness 2.27, presentation 2.53, contribution 2.40, and holistic rating 5.00, versus ICLR 2025 human average rating 5.08; Krippendorff's alpha for rating is 0.739 (p. 7).

The protocol is more specific in Appendix A: three reviewers, two ICLR 2025 reviewers and one prior Area Chair, approximately 55 minutes per paper, blind initial assessments on a custom site, confidence 1-5, soundness/presentation/contribution each 1-4, holistic rating 1-10, and a final Area Chair decision after reading the reviews (p. 15). The same appendix records the important negative result: reviewers praised ideation and novelty but repeatedly found insufficient standard-benchmark coverage, ablations, motivation studies, baseline comparisons, and related-work context (p. 15).

## Limitations, costs, and audit cautions

1. **Very low yield.** The funnel is over 5,000 ideas -> about 1,100 implemented/validated candidates -> 21 progress findings, with selected success around 1-3% and effectively zero for the stated random 100-idea baseline (pp. 2, 8). The paper itself characterizes the broader rate as 1-5% (p. 10), so the exact denominator and scope must be kept attached to each percentage.
2. **Implementation is a dominant failure mode.** Human attribution of 300 failed implementations assigns approximately 60% to premature termination from implementation errors; Appendix C separately reports approximately 50% of initial attempts failing to complete due to Claude Code internal timeouts (pp. 8, 17). These are different analyses and should not be conflated.
3. **Scientific execution remains weak.** Human reviewers found insufficient validation plans, missing ablations and motivation studies, and incomplete baseline/related-work comparisons despite praising novelty (p. 15). Thus SOTA-surpassing headline metrics do not establish uniformly rigorous scientific validation.
4. **Domain and cost boundary.** The strategy is presented as suitable for rapid-feedback tasks, but currently impractical for foundation-model pretraining or pharmaceutical synthesis because low success rates make high-cost search prohibitive (p. 8). Reported total cost is about $100,000, with per-idea and per-stage estimates on p. 18.
5. **Scaling evidence is limited.** The near-linear claim comes from a dedicated one-week experiment in which parallel paths solve assigned baseline limitations and synchronize to shared memory every five cycles (pp. 8-10). The observed points are 1 progress finding at 4 GPUs, 4 at 8 GPUs, and 11 at 16 GPUs; this is a small resource range, not a general scaling law.
6. **Human dependence is explicit.** Baselines were manually reproduced, three experts supervised the process, experimental results were manually inspected, and the authors require human supervision and final responsibility (pp. 5, 11, 17). The paper's intended system is therefore autonomous in execution loops but not independent of human goal selection, oversight, or final verification.
7. **Reproducibility and attribution caveats.** The implementation depends on named proprietary/API-backed agents and a distributed container setup (p. 17), while the Analyze & Report module is intentionally not open-sourced (p. 11). The public-paper comparison may also be affected by curation (p. 7). These constraints limit independent replication of the complete pipeline.

## Evidence boundary

The source supports the existence of a staged Bayesian/UCB-guided, Findings-Memory-based search; the reported three-domain measurements; the human-review protocol and its criticisms; and the stated cost, failure, and applicability limitations. It does **not** by itself establish that every claimed discovery is independently reproducible, that the small scaling experiment proves a universal law, or that the generated papers meet the rigor of ordinary peer-reviewed scientific publication. Those stronger interpretations would exceed the 19-page evidence.

EVIDENCE_COMPLETE: yes
