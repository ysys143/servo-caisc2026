# Digest: liu2024aigs (AIGS)

**Full title:** AIGS: Generating Science from AI-Powered Automated Falsification
**Authors:** Zijun Liu, Kaiming Liu, Yiqi Zhu, Xuanyu Lei, Zonghan Yang (equal contribution); Zhenhe Zhang, Peng Li, Yang Liu. Tsinghua University (Dept. of CS&T) + Institute for AI Industry Research (AIR).
**Venue/ID:** arXiv:2411.11910v2 [cs.LG], 24 Nov 2024. 36 pages. Code: github.com/AgentForceTeamOfficial/Baby-AIGS.
**Read basis:** Full paper only (extracted text, all 36 pages / 2760 lines).

---

## Thesis / Problem

The paper studies **AI-Generated Science (AIGS)**: agents that autonomously complete the *entire* research process. Revisiting Popper (1935), the authors argue **falsification is the essence** of both human research and any AIGS system design. They claim prior end-to-end systems (notably AI Scientist, Lu et al. 2024) *lack an explicit falsification component*, while domain-specialized systems (e.g., AlphaGeometry) rely on *external verification engines* rather than autonomous falsification. Their contribution is **BABY-AIGS**, a "baby-step" LLM multi-agent system whose distinguishing feature is a **FALSIFICATIONAGENT** performing explicit falsification via automated ablation studies. Three AIGS design principles: **falsification, creativity, executability**.

## Method — Selection mechanism (CRITICAL for audit)

BABY-AIGS has **two phases**:

1. **Pre-Falsification phase** (M iterations): ProposalAgent → ExpAgent → ReviewAgent loop refines idea/methodology (expressed in a Domain-Specific Language, DSL). Uses a **multi-sampling strategy**: N parallel threads, then **reranking by average benchmark performance score**; top-Ns threads retained for next iteration. Selection here is **performance-based (benchmark scores)**, NOT falsification.

2. **Falsification phase** (the FALSIFICATIONAGENT):
   - **Significance Screening**: identifies adjacent pre-falsification turns with the **greatest performance discrepancies** (largest increase/decrease in benchmark results) — candidates are selected by *magnitude of result change*.
   - Generates **scientific discovery candidates** (hypothesized "key factors") from those turns.
   - For each candidate, designs **at most T ablation experiments**, each isolating **a single factor**; selects a pre-falsification iteration as the ablation baseline; modifies methodology by ablating the factor.
   - Both baseline and ablation experiments are **repeated multiple times**.
   - **Acceptance rule (quote, ~lines 1189–1191):** "If a particular discovery withstands this process and consistently produces results similar to those in the main experiment, it is regarded as a verified and valuable Scientific Discovery. And it is falsified otherwise."

### IMPORTANT — Does AIGS select hypotheses by SURVIVAL OF AUTOMATED REFUTATION/FALSIFICATION?
**YES — at the verification stage.** A discovery candidate (hypothesized key factor) is **accepted only if it withstands (survives) the automated ablation experiments** and consistently reproduces the main-experiment result; otherwise it is falsified/discarded. The falsification is operationalized as **automated single-factor ablation studies**. Note the two-part structure: *which* candidates enter falsification is chosen by **significance screening (magnitude of performance change)**, and *acceptance* is by **survival of ablation**. In the pre-falsification phase, the intermediate selection among proposals is instead by **benchmark performance reranking** (not falsification).

### IMPORTANT — Does it compute/maximize EIG (Expected Information Gain)?
**NO. Explicitly not.** The paper contains **no mention** of expected information gain, information gain, mutual information, entropy-based objectives, Bayesian experimental design, active learning, acquisition functions, or posterior/surprisal (verified by full-text grep — only incidental matches like "weight_decay"/"informative"). The selection/acceptance signals are entirely: (a) **average benchmark performance scores** (multi-sampling reranking), (b) **magnitude of adjacent-turn performance discrepancy** (significance screening), and (c) **consistency/reproducibility of ablation results** (verification). Candidate/experiment selection is **heuristic and performance-driven**, not information-theoretic. The authors even contrast their reranking signal with reward-model-based or self-verification methods, favoring "large-scale validation benchmarks indicating generalization performance" as process supervision — still no EIG.

---

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| arXiv:2411.11910v2 [cs.LG], 24 Nov 2024 | line 10 | Version/date |
| 8 authors, Tsinghua CS&T + AIR; 5 equal-contribution | lines 3–8, 90–92 | Authorship |
| 3 research topics: data engineering, self-instruct alignment, language modeling | lines 357, 1278 | Experimental scope |
| gpt-4o-2024-05-13 | line 2291 | Underlying model for all agents |
| temperature 0.7 (agents); ProposalAgent generates **3** proposal sets @ temp 0.7 | lines 2291–2294 | Agent LLM config |
| Jaccard similarity (Jaccard 1901) of **bigram sets**; proposal with **lowest** similarity selected (for diversity) | lines 2294–2297 | ProposalAgent selection = diversity, not falsification |
| ReviewAgent & FalsificationAgent invoke GPT-4o **once** per generation | lines 2297–2298 | Agent config |
| Significance-screening thresholds: adjacent-benchmark diff > **1.5** on Vicuna-Bench (validation) OR > **0.5** on MT-Bench (test), ICL-aligned Llama-3-8B | lines 2312–2315 | Data-eng candidate selection thresholds |
| Data engineering: **M=5, N=32** | lines 2315–2316 | Iterations / multi-sample threads |
| Self-Instruct: **M=15, N=1** | lines 2334–2335 | N=1 due to limited compute |
| Language modeling: **M=10, N=1** | lines 2342–2344 | N=1 due to limited compute |
| Human eval: **20** agent-generated falsification logs/samples | lines 1433, 2355 | Falsification human eval |
| Left-tailed **Welch's t-test**, significant when **p<0.05** | lines 1433–1434 | Statistical test |
| Table 2 Importance Score (0–2): BABY-AIGS AVG **1.80**, STD 0.41, **P=0.02**, MIN 0.00, MAX 2.00; Top Conf AVG 2.00, STD 0.00 | Table 2, ~lines 1340–1355 | Human eval, data eng |
| Table 2 Consistency Score: BABY-AIGS AVG **1.00**, STD 0.86, P=0.00, MIN 0.00, MAX 2.00; Top Conf 2.00 | Table 2 | Human eval |
| Table 2 Correctness Score: BABY-AIGS AVG **0.95**, STD 0.94, P=0.00, MIN 0.00, MAX 2.00; Top Conf 2.00 | Table 2 | Human eval |
| Table 2 Overall Score: BABY-AIGS AVG **1.25**, STD 0.47, P=0.00, MIN 0.67, MAX 2.00; Top Conf 2.00 | Table 2 | Human eval |
| Table 3 Data-eng MT-Bench (15-shot ICL / SFT): Baseline(Turn0) **4.18 / 4.53**; AI Scientist **4.36 / 4.67**; BABY-AIGS **4.51 / 4.77**; Top Conf **4.45 / 5.01** | Table 3, ~lines 1459–1475 | Creativity/perf; BABY-AIGS > AI Scientist, < Top Conf on SFT |
| Table 4 Self-Instruct MT-Bench: Baseline(Turn0) **2.45**; BABY-AIGS **3.26** | Table 4, ~lines 1490–1496 | Creativity/perf |
| Table 5 Language-modeling Perplexity ↓ (shakespeare_char / enwik8 / text8): Baseline **1.473 / 1.003 / 0.974**; BABY-AIGS **1.499 / 0.984 / 0.966** | Table 5, ~lines 1542–1555 | BABY-AIGS worse on shakespeare_char, better on other two |
| Table 6 Success rates: AI Scientist Exp.SR **44.8%**, Overall SR **29.2%**; Baby-AIGS **Almost 100% / Almost 100%** | Table 6, ~lines 1568–1578 | Executability |
| Table 7 Multi-Sampling@1 MT-Bench (15-shot ICL): Baseline 4.18; T1–T5 = 3.68, 4.01, 4.05, 3.88, 3.90 | Table 7, ~lines 1630–1642 | Ablation: N=1 does not improve |
| Table 7 Multi-Sampling@32: Baseline 4.18; T1–T5 = 4.02, 4.05, 4.50, 4.51, 4.42 | Table 7 | Ablation: N=32 steadily improves |
| Table 8 API cost: Pre-Falsification/iter — Input **6,616.2** tok, Gen **761.5**, **$0.045**; Falsification/disc.cand — Input **43,375.5**, Gen **1,120.3**, **$0.234** | Table 8, ~lines 2373–2388 | Cost |
| Hardware: 8× RTX 3090 24GB (ICL data-eng + LM); 8× A100 80GB (SFT data-eng + self-instruct) | lines 2288–2291 | Compute |
| Data-eng dataset: Alpaca-GPT4 (Peng et al. 2023); rater = Llama-3-8B-Instruct (vLLM, temp 0.05); align model = Llama-3-8B; max 1024 tokens; FastChat | lines 2303–2308 | Data-eng setup |
| DSL data-eng instance (Fig 7): Number **27**, Threshold **15**, Ratio **0.7** | Fig 7, ~lines 2441–2444 | DSL parameters |
| DSL LM instance (Fig 9): n_layer 6, n_embd 384, dropout 0.2, lr 0.001, max_iters 5000, weight_decay 0.1 | Fig 9, ~lines 2483–2500 | DSL parameters |
| Self-Instruct fine-tuning: **LoRA** (Hu et al. 2022) via LLaMA-Factory, default hyperparams | line 2334 | Method |
| 15-shot / many-shot ICL (Jiang et al. 2024) | lines 1439–1440 | Data-eng eval |
| Turn 0 = trivial methodology (no-op / identity mapping); nanoGPT default = LM baseline | lines 689–691, 1502–1504 | Baselines |
| Benchmarks: Vicuna-Bench (validation), MT-Bench (Zheng et al. 2023, test) | lines 1440–1443 | Data-eng & self-instruct |
| LM training corpora: Karpathy 2015 (shakespeare_char), Hutter 2006 (enwik8), Mahoney 2011 (text8) | lines 1502–1503 | LM datasets |
| Baselines: AI Scientist (Lu et al. 2024) = automated baseline; top-conf literature = human baseline; **Deita** (Liu et al. 2024a) = human research for data-eng | lines 1321–1323, 1444–1445 | Baselines |
| Reranking uses **average performance score of all benchmarks** | lines 1118–1119 | Multi-sampling reranking signal |
| Multi-sampling related to **inference-cost scaling** (Snell et al. 2024; Brown et al. 2024) | lines 1668–1669 | Positioning |

---

## Scope & Limitations (as stated by the paper)

- **Empirical/ML-only scope:** focuses on subjects requiring actual implementation to get empirical results (machine learning); explicitly leaves physics, biology, chemistry, mathematics, humanities for future work (lines 661–663, 1721–1724).
- **Below human researchers:** BABY-AIGS performance "still lags behind experienced researchers"; data-eng SFT result inferior to Deita (lines 360–361, 1584–1586).
- **FalsificationAgent is weak:** Importance (1.80) > Consistency (1.00) > Correctness (0.95) — it can *identify* important factors but *fails to design concrete experiment plans and verify hypotheses*; "current LLMs are far from desired" in this workflow (lines 1518–1523, 1601–1606).
- **Statistically worse than humans:** p-values show falsification process "significantly less satisfactory" than top-conference literature (lines 1520–1522).
- **Small scale:** only 20 samples, "small compared to Si et al. 2024" (lines 1523–1524).
- **DSL requires human effort** and may constrain idea diversity/creativity (lines 891–893, 1691–1695).
- **FalsificationAgent seldom proposes plans beyond provided templates** (lines 1603–1604).
- **Simplified agents:** LiteratureAgent "was not put into practical use"; ExpAgent reduced to fixed code (lines 2283–2285).

## Does NOT claim / boundaries

- Does **NOT** claim to match or surpass human researchers (repeatedly positioned as a "baby step").
- Does **NOT** use or maximize **EIG / information gain / Bayesian experimental design / active learning** — no such objective anywhere.
- Does **NOT** rely on external verification engines (contrasts itself with AlphaGeometry precisely on this).
- Does **NOT** claim general cross-domain capability — empirical ML only.
- The falsification is **ablation-based single-factor verification**, not active experiment design to reduce uncertainty.
- Novelty claim (bounded, "to our knowledge"): FALSIFICATIONAGENT is "the first agent within AI-accelerated scientific discovery systems capable of autonomously completing the falsification process" — proposing candidates, designing+executing ablations, and verifying (lines 1270–1271).

## Section Map

- §1 Introduction (p.3) — motivation, falsification as foundation, three lines of prior work.
- §2 Development of AI-Accelerated Scientific Discovery (p.4) — four paradigms: (I) Performance Optimizer, (II) Research Assistant, (III) Automated Scientist, (IV) Research Community.
- §3 BABY-AIGS (p.6) — §3.1 design principles; §3.2 system design (two phases); §3.3 implementation (§3.3.1 DSL, §3.3.2 ProposalAgent, §3.3.3 ReviewAgent, §3.3.4 Multi-Sampling, §3.3.5 FalsificationAgent); §3.4 experiments (topics, eval settings); §3.5 quantitative/qualitative analysis; §3.6 Discussions (Q1–Q4).
- §4 Limitations and Actionable Insights (p.19).
- §5 Ethics and Impact Statement (p.20).
- §6 Conclusion (p.22).
- Appendix A (implementation), B (experiment details incl. human-eval guidelines, API costs, DSL demos), C (prompting structure).
