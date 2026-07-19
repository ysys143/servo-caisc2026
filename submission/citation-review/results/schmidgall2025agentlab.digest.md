# Digest — schmidgall2025agentlab (Agent Laboratory)

**Full title:** Agent Laboratory: Using LLM Agents as Research Assistants
**Authors:** Samuel Schmidgall, Yusheng Su, Ze Wang, Ximeng Sun, Jialian Wu, Xiaodong Yu, Jiang Liu, Michael Moor, Zicheng Liu, Emad Barsoum
**Affiliations:** AMD (1), Johns Hopkins University (2), ETH Zurich (3)
**Venue/version:** arXiv:2501.04227v2 [cs.HC], 17 Jun 2025 (dated 2025-06-18)
**Project page:** https://AgentLaboratory.github.io
**Source read:** full main body (Abstract through References + Discussion/Conclusion), pages ~1–21; appendices A (config), B (prompts), C (survey questions) inspected and confirmed to contain no additional headline statistics.

---

## Thesis / Problem

Scientific discovery is slow and costly. The paper introduces **Agent Laboratory**, an autonomous LLM-based framework that completes the *entire* research process from a **human-provided research idea** through three stages — (1) Literature Review, (2) Experimentation, (3) Report Writing — producing a code repository and a research report, while allowing human feedback/guidance at each stage. Explicitly positioned NOT as a replacement for human scientists but as a **co-pilot / research assistant** that lets researchers focus on ideation rather than low-level coding/writing. Contrasts itself with fully-autonomous idea-generating pipelines (The AI Scientist, Lu et al.) by keeping the human in the loop with their own research idea.

## Method (what Agent Laboratory is)

- **Input:** a human research idea + notes. **Output:** research report + code repository, produced by a pipeline of specialized LLM-driven agents (PhD agent, Postdoc agent, ML Engineer agent, SW Engineer agent, Professor agent).
- **Three phases:**
  1. **Literature Review** — PhD agent uses arXiv API with three actions (summary [top-20 abstracts], full text, add paper); iterative until N=max relevant texts curated.
  2. **Experimentation** — Plan Formulation (PhD + Postdoc dialogue → `plan` command); Data Preparation (ML Engineer runs Python, HuggingFace datasets via `search HF`, SW Engineer submits code after compiler check); Running Experiments via **mle-solver**; Results Interpretation (PhD+Postdoc → `interpretation` command).
  3. **Report Writing** — PhD + Professor agent via **paper-solver** (scaffold of 8 fixed sections → arXiv research → EDIT-based LaTeX editing → Paper Review → Paper Refinement).
- **mle-solver** submodule: Command Execution (EDIT/REPLACE operations), Code Execution (compile, repair up to N_rep=3 tries), Program Scoring (LLM reward model scores program 0–1), Self-Reflection, Performance Stabilization (top-program sampling + batch-parallelization). Compared to AIDE's Solution Space Search.
- **paper-solver** Paper Review step uses an **adapted version of the automated reviewer from Lu et al. (2024b)** (The AI Scientist), simulating NeurIPS review; three reviewer agents mimic NeurIPS peer reviewers.
- **Two operating modes:** autonomous (idea only, no human in loop) and co-pilot (human checkpoint reviews at end of each subtask).

### Evaluation design (incl. human/LLM reviewer comparison)
- **Autonomous-mode human eval:** 5 research-question templates × 3 LLM backends (gpt-4o, o1-mini, o1-preview) = **15 papers** written autonomously. **10 volunteer PhD students** each reviewed 3 randomly-assigned papers, rating experimental quality, report quality, usefulness on **1–5** scale, plus **NeurIPS-style criteria** (quality, significance, clarity, soundness, presentation, contribution) and an overall NeurIPS-style score.
- **Automated vs. human reviewer comparison:** the **automated (LLM) reviewer** scores the same generated papers and is compared against the **human PhD-student reviewers'** scores on the NeurIPS-style overall scale — this is the source of the over-estimation figure (see FACTS TABLE).
- **Co-pilot eval:** researchers co-pilot on custom + preselected topics; self-eval + external-eval on NeurIPS criteria; tool-utility survey (utility/continuation/satisfaction/usability). o1-mini backbone used (except literature review).
- **Runtime eval:** cost (USD) + time (s) + success rate per phase per backend.
- **mle-solver isolated eval:** subset of 10 low-complexity text/tabular MLE-Bench Kaggle challenges vs MLAB, OpenHands, AIDE.

---

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| **Automated reviewer 6.1/10 vs. human reviewer 3.8/10 overall = –2.3 points** | §Intro contribution 3 (p.2, lines 76–81); §4.1.1 "Automated Reviews vs Human Reviews" (p.12, lines 511–513); Fig 6 caption (lines 519–524) | **THE OVER-ESTIMATION FIGURE.** Automated (LLM) reviewer scores generated papers at avg **6.1/10** overall on a NeurIPS-style 1–10 scale; **human reviewers** (the 10 PhD students) score the SAME papers at **3.8/10** — automated **over-estimates by 2.3 points**. Verbatim: "While the automated reviewers gave an average overall above average NeurIPS paper score of 6.1/10, human reviewers provided a much lower average of 3.8/10 (-2.3 points)." Fig 6 caption: "Human scores are not predictive of automated reviewer scores, demonstrating an average of -2.3 points lower." Intro: "automated scores significantly overestimating quality (6.1/10 vs. 3.8/10 overall)." **NOTE for audit:** the 2.3-point over-estimation is the AUTOMATED LLM REVIEWER over-estimating relative to HUMAN reviewers on AI-generated papers — it is NOT a claim that the system's papers exceed human PhD students' papers by 2.3. Sign in text is "-2.3" (human relative to automated); equivalently automated is "+2.3" over human. |
| Clarity: automated 3.6/4 vs human 2.4/4 | §4.1.1 (p.13, line 530) | Example of same over-estimation pattern across specific criteria; pattern "holds for all criterion." |
| $2.33 USD per paper (gpt-4o backend) | Abstract (line 25 implies 84% cut); Intro contribution 6 (line 97); §4.3 (line 667) | Full-workflow monetary cost with gpt-4o backend. "only $2.33 USD per paper with a gpt-4o backend." |
| 84% decrease in research expenses vs previous autonomous methods | Abstract finding (4) (line 25) | Headline cost reduction claim. |
| ~$15 (6.4x more) for prior autonomous workflow (Lu et al. 2024b) using gpt-4o | §4.3 (line 668) | Baseline The AI Scientist cost comparison; $2.33 is 6.4x cheaper. |
| o1-mini $7.51; o1-preview $13.10 per workflow | §4.3 (lines 669–670) | o1-preview is >5.6x more expensive than gpt-4o. |
| gpt-4o total workflow time 1165.4 s; o1-mini 3616.8 s; o1-preview 6201.3 s | §4.3 (lines 658–660) | gpt-4o ~3.2x faster than o1-mini, ~5.3x faster than o1-preview. |
| Running Experiments: gpt-4o 417.8 s, o1-mini 2082.5 s, o1-preview 4036.2 s | §4.3 (lines 662–664) | Per-phase timing. |
| Report Writing: gpt-4o 572.5 s, o1-mini 827.7 s, o1-preview 1854.2 s | §4.3 (lines 664–665) | Per-phase timing. |
| Data Prep cost gpt-4o $0.09 vs o1-mini $3.03 vs o1-preview $0.30; Report Writing $1.73 / $2.58 / $9.58 | §4.3 (lines 671–673) | Per-phase cost breakdown. |
| Lit Review: gpt-4o 92.9 s / $0.12; o1-mini 56.8 s / $0.16 | §4.3 (lines 682–683) | Phase-level detail. |
| Plan Formulation: gpt-4o 23.3 s / $0.03; o1-preview 33.1 s / $0.04 | §4.3 (lines 684–685) | Phase-level detail. |
| Subtask success rates: o1-preview 95.7%, gpt-4o 94.3%, o1-mini 92.8% (avg) | §4.3 (lines 689–691) | Overall reliability. |
| Literature review phase success only 60%/70%/80% (gpt-4o/o1-mini/o1-preview) | §4.3 (lines 691–693) | High failure phase. |
| Data Prep: o1-mini 80%, gpt-4o 100%, o1-preview 90% | §4.3 (lines 693–695) | Phase success. |
| **Autonomous human eval (1–5):** gpt-4o exp 2.6, report 3.0, useful 4.0 | §4.1 (lines 455–456) | Per-backend quality (PhD-student ratings). |
| o1-mini exp 3.2 (+0.6), report 3.2 (+0.2), useful 4.3 (+0.3) | §4.1 (lines 457–458) | o1-mini highest experimental quality. |
| o1-preview useful 4.4, report 3.4, exp 2.9 | §4.1 (lines 459–461) | o1-preview most useful + highest report quality. |
| Highest report quality 3.8/5 & usefulness 4.5/5 (word-order topic); highest exp quality 3.2/5 (cognitive bias) | §4.1 (lines 470–472) | Topic-level maxima. |
| Image-noise exp quality 1.5/5 (gpt-4o) vs 4.0/5 (o1-mini) = +2.5 pt; usefulness 2.5 vs 4.5 = +2.0 pt | §4.1 (lines 474–476) | High variance by backend on one topic. (Distinct +2.5/+2.0 numbers — NOT the reviewer over-estimation figure.) |
| **Autonomous NeurIPS-style overall (human):** gpt-4o 3.5/10, o1-mini 3.8/10, o1-preview 4.0/10 | §4.1.1 (lines 488–490) | Human reviewer overall scores by backend. |
| Quality(/4): gpt-4o 1.8, o1-mini 2.3 (highest) | §4.1.1 (lines 491–492) | Human NeurIPS criterion. |
| Significance 2.2–2.5/4 across backends | §4.1.1 (line 493) | Human NeurIPS criterion. |
| Clarity: gpt-4o 2.6/4, o1-mini 2.1/4 (-0.5) | §4.1.1 (lines 494–495) | Human NeurIPS criterion. |
| Soundness: o1-preview 2.2/4 highest; o1-mini 1.8, gpt-4o 1.7 | §4.1.1 (lines 496–497) | Human NeurIPS criterion. |
| Contribution avg 2.1/4 across models | §4.1.1 (lines 498–499) | Human NeurIPS criterion. |
| Avg accepted NeurIPS paper = 5.9 (general); autonomous papers below acceptance threshold | §4.1.1 (line 503) | Benchmark reference. |
| NeurIPS 2024 accepted-paper avg = 5.85* (footnote papercopilot); autonomous scores –2.05 below | §4.1.1 (lines 534–535); footnote (line 571) | Autonomous overall (3.8) is 2.05 below 5.85. |
| **Adapted automated reviewer (from Lu et al. 2024b) validation:** 65% accuracy vs 66% human; F1 0.57 vs 0.49 (after calibration) on 500 ICLR 2022 OpenReview papers | §3.3 D Paper Review (lines 351–353) | Validation claim carried over from The AI Scientist's reviewer; "human-level accuracy." |
| **Co-pilot tool survey (1–5):** utility 3.5, continuation 3.75, satisfaction 3.63, usability 4.0 (overall) | §4.2.1 (lines 561–562) | Tool-quality ratings. |
| Custom: utility 3.75, cont 4.0, sat 3.75, usability 3.75 | §4.2.1 (lines 563–564) | Co-pilot custom topics. |
| Preselected: utility 3.25, cont 3.5, sat 3.5, usability 4.25 | §4.2.1 (lines 565–566) | Co-pilot preselected topics. |
| Co-pilot quality (1–5): exp 2.38, report 3.13, useful 3.75 | §4.2.1 (line 570) | Co-pilot vs autonomous comparison; all lower than o1-mini autonomous. |
| Co-pilot self-eval overall 4.13/10 vs autonomous 3.8/10 (+0.33); o1-preview autonomous 4.0/10 | §4.2.2 (lines 605–608) | Human involvement improves scores. |
| Co-pilot external eval overall 4.38/10 (up from 4.13 self) | §4.2.2 (lines 614–616) | External > self evaluation. |
| Co-pilot external 4.38 is –1.45 below NeurIPS 2024 accepted avg 5.85 | §4.2.2 (lines 637–638) | Still below acceptance. |
| 75% response rate on optional feedback question | §4.2.1 (line 585) | Survey participation. |
| **MLE-Bench:** mle-solver 4 medals (2 gold, 1 silver, 1 bronze); OpenHands 2 (2 gold); AIDE 2 (1 gold, 1 bronze); MLAB 0 | §4.4 (lines 721–724) | mle-solver best. |
| Above-median human performance: mle-solver 6/10, AIDE 5/10, OpenHands 2/10, MLAB 0/10 | §4.4 (lines 724–726) | Benchmark subset. |
| MLE-Bench: 10 challenges (low-complexity text/tabular subset); dev = 20% of train, train = 80% | §4.4 (lines 698–707) | Eval protocol. mle-solver submitted valid solutions for all within 2 hours; others often failed to submit. |
| Self-eval LLM agreement 53.3% vs human 56.1% | §5.1 (lines 745–747) | Limitation: LLMs less reliable for self-eval (contrasts with Lu et al. 2024b). |
| N_rep = 3 (code repair tries); reward model scores 0–1 | §3.2 B/C (lines 249, 255) | mle-solver internals. |
| MLE-Bench/DS-bench/MLAgentBench use 75/74/6 Kaggle challenges | §2 (lines 138–140) | Related-work benchmark sizes. |

---

## Scope & explicit limitations (§5)

- **Self-evaluation limitation:** paper-solver quality judged by LLM-emulated NeurIPS reviewers; reports are qualitatively *less satisfying* than The AI Scientist's (lower-quality figures) **despite scoring higher overall**. Reports are meant as a human-readable summary of what was accomplished, NOT a replacement for human paper-writing.
- **Automated structure:** fixed 8-section paper layout disallows unique organizations; mle-solver + paper-solver limited to **only two figures**; cannot manage repository-level code autonomously.
- **Hallucination:** lower-performing models (esp. gpt-4o) sometimes hallucinated experimental results that never occurred (verbatim fabricated hyperparameter example given).
- **Common failure modes:** repeated summarize command until termination in lit review; token-limit overflows; 0% accuracy runs uncorrected; mle-solver edits line 0 excessively; `exit()` command terminating process; running host `subprocess.run()` system commands (no safeguards yet); paper-solver arXiv search taking up to 100 tries (limit of 5 imposed).
- **Ethics:** risk of substandard/misleading outputs overwhelming peer review; amplifying dataset biases; misuse for malware/harmful tech; need for transparent disclosure of AI involvement.

## Does NOT claim / boundaries

- Does **NOT** claim to replace human scientists or the human paper-writing process — explicitly a co-pilot/assistant that summarizes accomplished work.
- Does **NOT** claim the generated papers meet NeurIPS acceptance standards — autonomous (3.8) and co-pilot (4.38) overall scores are **below** the ~5.85–5.9 accepted-paper threshold.
- Does **NOT** claim its automated reviewer is accurate for its own papers — the central finding is the OPPOSITE: automated reviewers over-estimate quality by 2.3 points vs humans, and "automated reviewer scores do not predict human reviewer scores."
- Does **NOT** generate its own research ideas (unlike The AI Scientist) — it takes a human-provided idea.
- Does **NOT** claim the +2.3 gap means the system's papers are better than PhD-student papers — the 2.3 gap is strictly LLM-reviewer vs human-reviewer scoring of the SAME AI-generated papers.

## Section map

1. Introduction (7 numbered contributions) — p.2
2. Background & Related Work (LLMs, LLM Agents, AutoML, AI in Scientific Discovery, LLMs for research tasks, LLMs for autonomous research) — p.3–4
3. Agent Laboratory (3.1 Literature Review; 3.2 Experimentation incl. mle-solver A–E; 3.3 Report Writing incl. paper-solver A–D + Paper Refinement; 3.3.1 Autonomous vs Co-Pilot) — p.5–10
4. Results (4.1 quality by LM; 4.1.1 human reviewer scores + Automated vs Human; 4.2 co-pilot quality; 4.2.1 quality as tool; 4.2.2 co-pilot papers; 4.3 runtime stats; 4.4 mle-solver on MLE-Bench) — p.10–19
5. Limitations (5.1 workflow; 5.2 failure modes; 5.3 ethics) — p.19–20
6. Discussion + Conclusion — p.21
References — p.22–27
Appendix A (config/hyperparameters, Table 1), B (prompts), C (survey questions) — p.28+
