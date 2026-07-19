# Digest: google2026aletheia

**Paper**: "Towards Autonomous Mathematics Research" (Feng, Trinh, Bingham, et al.), Google DeepMind. arXiv:2602.10177v3 [cs.LG], dated 2026-3-9. 42 pages.

---

## Thesis / Problem

The paper documents the transition from AI competition-level math problem solving (IMO gold) to professional research-level mathematics. It introduces **Aletheia**, a math-research agent that iteratively generates, verifies, and revises solutions **end-to-end in natural language** (not formal/proof-checker language), built on top of Gemini Deep Think. The paper presents an initial wave of AI-assisted results (several papers, an Erdos-problem case study, and FirstProof performance), and — because of a public "evaluation gap" that lets AI-math misinformation spread — proposes a taxonomy of "Autonomous Mathematics Research Levels" (analogous to SAE vehicle-autonomy levels) plus "Human-AI Interaction (HAI) Cards" for transparent documentation.

---

## Method: What Aletheia actually does

- **Natural-language, not formal.** Explicitly contrasted with AlphaGeometry (Chervonyi 2025; Trinh 2024) and AlphaProof (Hubert 2025), which use formal language. Aletheia operates **end-to-end in natural language** (§2, p.3). Verification is **informal natural-language verification by human experts and/or an AI verifier subagent** — NOT a formal proof checker.
- **Three subagents:** a (solution) Generator, a Verifier, and a Reviser, which interact continuously until the Verifier approves a solution or a preset attempt limit is reached (§2, p.3, Fig 1). Each subagent internally orchestrates calls to a Gemini base model.
- **Three power sources** (§1, p.2): (i) advanced Gemini Deep Think; (ii) a novel inference-time scaling law extending from Olympiad to PhD-level; (iii) intensive tool use — Google Search and web browsing.
- **Design rationale** (§2.2): decoupling the model's final output from its intermediate thinking tokens + prompt scaffolding lets the model catch flaws it overlooked during generation; explicitly separating the verification step is effective in practice.
- **Human role in the papers:** Final versions of ALL research papers were **written by human authors starting from Aletheia's outputs** (principle that math papers should be human-authored for accountability) (§3, p.6).
- **Proof correctness scoring:** graded by **human experts** (natural-language verification), with acknowledged subjectivity. AI grading was used only as an initial filter in the Erdos study, then human experts vetted.

---

## FACTS TABLE (exhaustive)

Note on notation: `[O]` = correct/success, `[X]` = failure, in place of the check/cross marks used in the paper's tables.

### Benchmarks / scaling (§2.1–2.2)

| Value / finding | Exact location | Context |
|---|---|---|
| Gold-medal at IMO, **5 of 6 problems perfectly solved** | §2.1 p.4 (Luong & Lockhart 2025) | Advanced Gemini Deep Think, July 2025 IMO |
| IMO-Proof Bench Advanced = **30 problems** | §2.1 p.4 | Advanced subset, IMO-difficulty; benchmark used for IMO 2025 prep |
| Compute for equivalent IMO-Proof Bench performance reduced by **~2 orders of magnitude (100x)** | §2.1 p.4 | Jan 2026 advanced Deep Think vs prior |
| IMO 2025 Problem 6 solved (Appendix C); prior IMO-gold model had failed | §2.1 p.4 | Jan 2026 model, no internet |
| IMO 2024 Problem 3 solved with a minor mistake at **2^7 scale**; Problem 5 solved at **2^8 scale** | §2.1 p.5, Appendix D | Jan 2026 model |
| **Aletheia 93% overall score on IMO-Proof Bench Advanced, no tool usage** | §2.2 p.5 | Surpassing Deep Think across all tested compute scales, same base model |
| On the **29 of 30** problems where Aletheia returned a solution, **conditional accuracy 96%** | §2.2 p.5 | IMO-Proof Bench Advanced |
| On FutureMath Basic, Aletheia returned solutions for **fewer than 60%** of problems; conditional accuracy on answered subset **exceeded 82%** | §2.2 p.5 | PhD-level internal benchmark |
| Footnote 6: With **Feb 2026 Gemini 3 base model, Aletheia achieved SOTA 95%** on IMO-Proof Bench Advanced, no tool usage | §2.2 fn 6 p.5 | later model |
| Python-as-tool gave **only marginal** improvement in mitigating computational hallucinations | §2.3 p.6 | tool-use ablation observation |

### Erdos problems case study (§3.3, §5.1, §5.2) — CRITICAL AUDIT NUMBERS

| Value / finding | Exact location | Context |
|---|---|---|
| ErdosProblems.com database tracks **1,179 problems, 483 (41%) classified as solved** | §3.3 p.8 | "at the time of this writing"; Bloom launched site 2023 |
| Deployed Aletheia on **700 Erdos problems** then marked "Open" | §3.3 p.8 | Dec 2–9 2025, **November 2025 base model of Gemini 3** |
| Of the 700 prompts, model returned **212 responses as potentially correct** | §3.3 p.8 | Aletheia's informal verifier filtered the pool |
| **63 solutions technically correct**, but **only 13 correctly addressed the intended problem statement** | §3.3 p.8–9 | after human expert vetting |
| Remaining **50** of the correct solutions were technically valid but **"mathematically vacuous"** (interpreted problem in a way that missed Erdos's intent) | §3.3 p.9 | |
| **12 responses marked ambiguous** (e.g., open-endedness of question) | §3.3 p.9 | |
| Of **200** candidates definitively markable correct/incorrect: **137 (68.5%) fundamentally flawed; 63 (31.5%) technically correct; of which only 13 (6.5%) meaningfully correct** | §3.3 p.9 AND Table 6 §5.2 p.14 | 200 = 212 minus 12 ambiguous |
| The **13 meaningfully correct** cluster into **4 categories** (Table 2) | §3.3 p.9, Table 2 | |
| **Autonomous Resolution: Erdos-652\*, 1051** | Table 2 p.9 | "Autonomous novel solution" |
| **Partial AI Solution: Erdos-654, 1040** | Table 2 p.9 | solved part of a multi-part problem |
| **Independent Rediscovery: Erdos-397\*, 659\*, 935, 1089** | Table 2 p.9 | correct but solution already in literature |
| **Literature Identification: Erdos-333\*, 591, 705, 992, 1105** | Table 2 p.9 | problem already solved in literature |
| The **"4" autonomous solutions = Erdos-652, 654, 1040, 1051** | §3.3 p.9 | "none of the four individually rises to the level of a research paper" |
| Erdos-1051 solution was **generalized further** (Aletheia + humans + Gemini Deep Think) -> research paper **(BKKKZ26)** | §3.3 p.9 | |
| Table 2 footnote: `*` = independently obtained by other parties after initial evaluations but before this work published (marks 652, 397, 659, 333) | Table 2 note p.9 | |
| Erdos-1089 answered by an offhand remark in a **1981 paper (Bannai & Bannai)** whose authors seemed unaware they'd resolved it | §3.3 p.9 | argues problems open "out of obscurity rather than difficulty" |

### Ablation: Gemini Deep Think (IMO scale) vs Aletheia (§5.1)

| Value / finding | Exact location | Context |
|---|---|---|
| Gemini Deep Think (IMO scale) correctly solved **8 of the 13** Erdos problems Aletheia solved | §5.1 p.13, Table 4 | at **~2x the average compute per problem** vs Aletheia; same base model |
| Table 4 per-problem (333,397,591,652,654,659,705,935,992,1040,1051,1089,1105): [O][O][X][O][O][O][X][O][X][X][O][O][X] | Table 4 p.13 | Deep Think results |
| Table 5 — Deep Think reproducing research-paper prompts: (FYZ26)[O] (Feng26)[X] (LeeSeo26)[X] (BKKKZ26)[O] (ACGKMP26)[O] | §5.1 p.13, Table 5 | text: failed all 3 prompts for Feng26; solved 1st but not the crucial 2nd LeeSeo26 prompt; BKKKZ26 "essentially succeeded"; ACGKMP26 upper bound less sharp than Aletheia's; comparable total compute |

### FirstProof (§4, §5.2)

| Value / finding | Exact location | Context |
|---|---|---|
| FirstProof = **ten research-level problems** (Abouzaid et al., 2026), curated by academics with no AI-company ties | §4 p.11 | problems described as "Lemmas"; all already solved by mathematicians, solutions not online |
| Released **Feb 5 2026**, deadline **11:59pm PST Feb 13 2026** | §4 p.11 | official human solutions then published |
| **Two runs** of Aletheia (two base models: Gemini 3 Deep Think Feb 2026, and Jan 2026 base) | §4.1 p.11 | prompts copy-pasted unmodified from LaTeX |
| Both runs produced solution candidates to **exactly 6 problems (P2, P5, P7, P8, P9, P10)** | §5.2 p.14 | |
| Best-of-2, majority expert opinion: **all 6 rated correct** (publishable after minor revisions) | §5.2 p.14, Table 3 | |
| **P8 not unanimous: only 5 of 7 experts rated Correct** | §5.2 p.14, Table 3, Table 7 | only non-unanimous assessment |
| Table 3 expert (correct/total): P2 4/4, P5 4/4, P7 3/3, P8 5/7, P9 4/4, P10 2/2 | Table 3 p.12 | P1,P3,P4,P6 = No Output |
| For P1, P3, P4, P6 **both agents returned no solution** | §5.2 p.14 | "No solution found" or no output in time limit |
| **One** Aletheia FirstProof solution is publication-grade: **Problem 7** -> success rate **1/10** for publication-grade | §5.2 p.14 | most FirstProof problems are technical Lemmas |
| Problem 7 was an open problem in book (Weinberger 2023); resolved by Cappell–Weinberger–Yan (unpublished until FirstProof solutions); Aletheia's solution distinct enough for separate ArXiv paper **(FK26)** | §4.1 p.11 | |
| For P7 the inference cost exceeded previous scales **by an order of magnitude** | §4.3 p.12, Fig 5 | costs shown as multiples of the Erdos-1051 solution cost |
| Table 7 (Run A / Run B): P2 Correct/Correct; P5 Correct/Misinterpreted; P7 Critically Flawed/Correct; P8 Inadequate/Correct?; P9 Correct/Correct; P10 Correct/Correct; P1,P3,P4,P6 No output/No output | Table 7 p.15 | per-run detail |

### FirstProof — other systems' comparisons (§4.2)

| Value / finding | Exact location | Context |
|---|---|---|
| **GPT 5.2 Pro** solved Problems 9 and 10 "out of the box" (FirstProof authors' internal tests) | §4.2 p.11 | baseline for publicly available models |
| **Gemini 3 Deep Think** could solve Problem 10 "out of the box" (observed by D. Woodruff & A. Mokhtari) | §4.2 p.11 | |
| **OpenAI** claimed "highly likely" solutions to Problems **2, 4, 5, 6, 9, 10** (internal model); solution to **Problem 2 quickly found flawed**; experts regard the other five correct; produced with **undisclosed human guidance** | §4.2 p.11–12 | |
| **Cursor researchers (Zhang & Lin)** exhibited an autonomously generated solution to **Problem 6**; experts regard it correct | §4.2 p.12 | |
| Authors unaware of any credible autonomous solutions beyond baseline (P9, P10) besides these | §4.2 p.12 | |

### Autonomy/Significance taxonomy classification (§6.1)

| Value / finding | Exact location | Context |
|---|---|---|
| Autonomy levels: **H** (Primarily Human), **C** (Human-AI Collaboration), **A** (Essentially Autonomous) | Table 8 p.16 | |
| Significance levels: **0** Negligible, **1** Minor, **2** Publication Grade, **3** Major Advance, **4** Landmark Breakthrough | Table 9 p.17 | Level 3 = top-5 journals; no autonomous result close to Level 3 |
| Classification: **Feng26 = A2**; **BKKKZ26, LeeSeo26 = C2**; **ACGKMP26, FYZ26 = H2** | §6.1.2 p.17 | |
| Erdos-652, 654, 935, 1040 = **Level A0**; Erdos-1051 = **Level A1** | §6.1.2 p.17 | (note: 935 appears here though it was "Independent Rediscovery" in Table 2) |
| Table 1 (front page) places all results on a 2-axis grid (Primarily Human / Human-AI Collaboration / Essentially Autonomous) x (Levels 0–4) | Table 1 p.2 | organizes Erdos-652/654/1040, Erdos-1051, ACGKMP26, BKKKZ26, FYZ26, LeeSeo26, Feng26 |

---

## Scope & explicit limitations (heavily caveated)

- **Reliability of validation.** "Natural language verification by human experts inherently involves some subjectivity" (fn 15, p.13). Human expert grading is the primary correctness measure; there is no formal proof verification.
- **Novelty is an upper bound.** "our initial classification into categories is, at best, an upper bound on novelty. It is subject to revision" (§3.3 p.10). Authors note they may have missed earlier human solutions.
- **Prior AI Erdos claims were wrong.** Previous AI-assisted work on Erdos **1026, 397, 333, 281** was found, after initial novelty announcements, to be **redundant with the literature** (§3.3 p.10). (Exception noted: Erdos-281 AI solution distinct from literature.)
- **"Subconscious plagiarism" danger** (fn 10, p.9): AI may reproduce knowledge acquired during pretraining without attribution; even scanning reasoning logs cannot rule out indirect ingestion.
- **Hallucination still common** (§5.3 p.15): even with internet search, the model tends to "fabricate or misrepresent results from legitimate references in order to assert a solution" (Fig 4 example). Figure 3 shows a fully fabricated citation (Livingston–Naik pretzel-knot paper) from a model without search.
- **Specification gaming / reward hacking** (§5.3): model tends to misinterpret ambiguous questions in the easiest-to-answer way.
- **November 2025 base model was substantially weaker** than the January 2026 model (the Erdos study used the Nov 2025 model) (§5.2 p.14).
- **Success is rare** (§5.2 p.14): "success cases are rare"; the §3 papers "grew out of spontaneous positive outcomes in a wider benchmarking effort … for most of these problems, no autonomous progress was made."
- **Autonomous results are brief/elementary** (§5.3): relatively brief and elementary vs typical human papers; success from "clever technical manipulations or vast knowledge retrieval, rather than … genuine creativity."
- **Data contamination caveats** on IMO 2024/2025 (fn 5, p.5; Appendix D): model's knowledge cutoff falls between IMO 2024 and 2025.

## Does NOT claim / boundaries

- Does **NOT** claim AI has matched, or will match, human mathematicians (§7 p.19: "they do not indicate that artificial intelligence has matched, or will match, the capabilities of human mathematicians").
- Does **NOT** claim the autonomous results are "major advances" for mathematics (§1 p.3): the solved Erdos problems, "despite being open for several decades — turned out … to be quite elementary."
- Does **NOT** claim novelty for the "Independent Rediscovery" or "Literature Identification" categories (§3.3 p.9).
- Does **NOT** claim reliable/consistent solving of research math (§5.2).
- Aletheia is a Google DeepMind system; the FirstProof comparisons of GPT-5.2 Pro / OpenAI / Cursor are reported second-hand with hedges ("our understanding is …").

## Section map

1. Introduction (milestones A–D listed; Table 1 taxonomy; Erdos results context)
2. The Aletheia agent (§2.1 scaling laws & Deep Think evolution; §2.2 agentic harness, 93%/96% numbers; §2.3 tool use, hallucination figures 3–4)
3. Summary of research results (§3.1 Milestone A Eigenweights/Feng26; §3.2 Milestone B independence polynomials/LeeSeo26; §3.3 Milestone C Erdos problems — the audit numbers; §3.4 Robust MDPs/ACGKMP26)
4. FirstProof (§4.1 Aletheia results/Table 3; §4.2 comparisons to GPT-5.2 Pro/OpenAI/Cursor; §4.3 inference cost)
5. Analysis & Discussion (§5.1 ablations Tables 4–5; §5.2 accuracy Table 6–7; §5.3 weaknesses of AI)
6. Representing AI contributions (§6.1 Autonomy Levels Tables 8–9; §6.2 HAI Cards for Feng26/LeeSeo26/BKKKZ26)
7. Reflections on impact
8. Related Work
9. Conclusion
Appendices: A & B FutureMath Basic (Potts model example), C IMO 2025 P6, D IMO 2024 P3 & P5 case studies
