# Digest — bran2023chemcrow (BLIND first-pass)

**Paper:** "Augmenting large language models with chemistry tools" (ChemCrow)
**Authors:** Andres M. Bran, Sam Cox, Oliver Schilter, Carlo Baldassari, Andrew D. White, Philippe Schwaller (EPFL LIAC / NCCR Catalysis; Univ. of Rochester; IBM Research – Europe). Bran & Cox contributed equally.
**Venue/ID:** arXiv:2304.05376v5 [physics.chem-ph], 2 Oct 2023. "Preprint. Under review." Code: github.com/ur-whitelab/chemcrow-public ; runs: github.com/ur-whitelab/chemcrow-runs.

---

## Thesis / Problem
Excellent computational chemistry tools exist but have steep learning curves and poor interoperability; LLMs are strong at NL tasks but struggle with chemistry (e.g., cannot reliably multiply 12345*98765 or convert IUPAC→molecular graph) and lack external-knowledge access. **ChemCrow** augments an LLM (GPT-4) with 18 expert-designed chemistry tools to autonomously plan/execute tasks across organic synthesis, drug discovery, and materials design. Claims it is "one of the first chemistry-related LLM agent interactions with the physical world."

## Method — reasoning/search paradigm (KEY)
- **Search = ReAct, NOT beam search.** The agent operates via the **ReAct** framework (Thought → Action → Action Input → Observation), explicitly combined with **MRKL** (neuro-symbolic modular architecture). It is an "automatic, iterative chain-of-thought process" that loops until a final answer. The paper cites ReAct [43] and MRKL [53] as the workflow. No beam search is used for the agent's own reasoning/tool-planning.
  - Caveat: beam/"search algorithms" appear *inside a tool* — the `ReactionPlanner` tool uses RXN4Chemistry's Transformer + "search algorithms to handle multi-step synthesis." That is internal to the third-party tool, not the agent's control loop.
- **LLM:** OpenAI GPT-4, temperature 0.1. Framework: **LangChain** (external tools integrated as LangChain tools). LLM is given tool names + descriptions + expected I/O.

## Method — how ChemCrow VALIDATES outputs (KEY)
Three distinct validation channels — and it **DOES do physical/wet-lab execution, not only computational + tool calls**:
1. **Physical / wet-lab execution (real).** Via the cloud-connected, proprietary **RoboRXN** robotic synthesis platform (IBM Research). ChemCrow autonomously planned AND ran syntheses of **DEET** (insect repellent) and **three thiourea organocatalysts** (Schreiner's, Ricci's, Takemoto's) — 4 syntheses, all yielded the anticipated compounds (MS-confirmed, Appendix A). Separately, the human-AI chromophore was physically synthesized and measured. So ChemCrow reaches beyond computation into robotic wet-lab execution. `ReactionExecute` requests user permission before launching; the `ActionCleaner` loop auto-fixes invalid robot actions (e.g., "not enough solvent") without human intervention.
2. **Computational-tool grounding (surrogate signals).** Answers are grounded in expert tools rather than LLM memory: RXN4Chemistry/Molecular-Transformer reaction prediction, RDKit molecular weight, molbloom/ZINC purchasability & patent checks, PubChem safety, Tanimoto/ECFP similarity, RF ML model (chromophore). These give "exact answers" that mitigate hallucination.
3. **Evaluation of quality (not physical).** Dual assessment on 14 tasks: an LLM judge **EvaluatorGPT** (grades whether task is addressed + thought process correct; role = teacher grading students) AND a **panel of 4 expert chemists** scoring 3 dimensions. Key finding: EvaluatorGPT (GPT-4-as-judge) CANNOT distinguish wrong GPT-4 answers from ChemCrow's — it prefers GPT-4's fluent-but-wrong answers, while humans prefer ChemCrow.

---

## FACTS TABLE (exhaustive)
| Value | Location | Context |
|---|---|---|
| **18** expert-designed tools | Abstract, Intro (p2) | Core claim of tool count integrated into ChemCrow |
| **19** tools actually described in §5.3 (my count) | §5.3.1–5.3.4 | 4 general + 8 molecule + 3 safety + 4 reaction = 19; paper states 18. Discrepancy to flag. |
| **12** tools | Data/Code availability (p11) | Open-source public version includes a *subset of 12* of the original tools |
| GPT-4, temperature **0.1** | §5.1 Methods | LLM used in all experiments |
| **14** tasks / use cases | Intro (p2); Appendix G | Evaluation set (G.1–G.14) |
| **4** expert chemists | Appendix B | Human evaluation panel |
| **3** evaluation dimensions | §2.3 (p5) | 1. Correctness of chemistry; 2. Quality of reasoning; 3. Degree of task completion |
| **3** task categories | Fig 4a | Synthesis, Molecular design, Chemical logic |
| **95%** confidence interval | Fig 4c | Error bars on aggregate scores |
| **4** physically executed syntheses | §2.1 | DEET + Schreiner's + Ricci's + Takemoto's organocatalysts on RoboRXN |
| **3** thiourea organocatalysts | §2.1, Abstract | Schreiner's [56,57], Ricci's [58], Takemoto's [59] |
| Chromophore target absorption max = **369 nm** | §2.2, Fig 3 | Human-AI collaboration target property |
| Chromophore *measured* absorption max = **336 nm** | §2.2 (p3) | "approximately the desired property" |
| RF model RMSE = **37 nm** | Fig 3 | Random Forest predicting absorption max wavelength |
| Chromophore = **(E)-3-methyl-4-(2-(3'-(methylsulfonamido)-[1,1'-biphenyl]-4-yl)vinyl)benzoate** | Fig 3 | Novel chromophore discovered; solvent = acetonitrile |
| **5** independent executions of task 6 | Appendix E | Reproducibility test |
| **2 of 5** executions wrong | Appendix E | LLM mislabels SMILES "CCc1ccc(Cl)cc1" as trans-alkene → wrong mechanism conclusion |
| **50** robust medchem reactions | §5.3.2 ModifyMol | SynSpace package; retro/forward rules; blocks from Purchasable Mcule |
| OPCW Schedules **1–3** + Australia Group list | §5.3.3 ControlledChemicalCheck | Controlled-chemical/CW-precursor screening |
| GHS "Explosive" rating | §5.3.3 ExplosiveCheck | Queries PubChem via name/IUPAC/CAS |
| DEET MS: m/z 192 [M+H] calc, found 192.14 | Appendix A.1 | Experimental confirmation |
| Schreiner's MS: m/z 501, found 501.02 | Appendix A.2 | " |
| Takemoto MS: m/z 413, found 413.14 | Appendix A.2 | " |
| Ricci's MS: m/z 421, found 421.08 | Appendix A.2 | " |
| GitHub Copilot introduced **2021** | Intro | Motivating example |
| NSF grant 1751471; NIH R35GM137966; NCCR Catalysis grant 180544 | Acknowledgements | Funding |

### Tool inventory (by group)
- **General (4):** WebSearch (SerpAPI, Google first page); LitSearch (paper-qa + OpenAI Embeddings + FAISS; LitSearch preferred over WebSearch by default); Python REPL; Human (asks user).
- **Molecule (8):** Name2SMILES (chem-space→PubChem→OPSIN); SMILES2Price (molbloom/ZINC20 + chem-space API, cheapest price); Name2CAS (PubChem); Similarity (Tanimoto on ECFP2); ModifyMol (SynSpace, 50 robust reactions, PostEra Manifold optional); PatentCheck (molbloom bloom-filter vs ZINC); FuncGroups (SMARTS patterns); SMILES2Weight (RDKit).
- **Safety (3):** ControlledChemicalCheck (CAS vs OPCW + Australia Group; auto-invoked, stops execution on hit); ExplosiveCheck (GHS via PubChem; auto-invoked on synthesis request); SafetySummary (PubChem; operational safety, GHS, environmental, societal impact; GPT-4 may fill gaps but must state so).
- **Reaction (4):** NameRXN (NextMove proprietary; classifies via Carey-Laffan-Thomson-Williams hierarchy); ReactionPredict (RXN4Chemistry API / Molecular Transformer; reactants→product); ReactionPlanner (RXN4Chemistry + search algs for multi-step + action prediction→machine-readable steps, then LLM→NL); ReactionExecute (RoboRXN robotic platform; plan+adapt+execute; ActionCleaner auto-fix; requests user permission).

---

## Scope & Limitations (Appendix F; §4)
- Bound by **quality and quantity of tools**; "unreasonable to anticipate ChemCrow could outperform the retrosynthetic tools it uses."
- Three named limitations (cites [105–108]): **hallucination, difficulty of evaluating results, reproducibility**.
- **External tools cannot fully rectify the LLM's flawed reasoning** — occasional errors from faulty logic remain.
- **LLM-based evaluation (EvaluatorGPT) is insufficient/unreliable** — lacks knowledge to detect errors, favors verbose/fluent answers; forces reliance on human evaluation → limits pace/scale.
- Reproducibility hindered by closed-source API LLMs; open-source models [76–78] a possible fix but with reasoning trade-off.
- Robot procedures not always directly executable (solvent/purify issues); needs adaptation.

## Does NOT claim / boundaries
- Does NOT claim an exhaustive/complete tool set ("not exhaustive," "limited set").
- Does NOT claim to beat its underlying retrosynthesis tools.
- Does NOT claim LLM-as-judge is trustworthy for factual chemistry — explicitly argues the opposite.
- Physical execution is NOT fully hands-off end-to-end: user permission requested before robotic launch (though invalid-action cleanup is automated).
- GPT-4 outperforms ChemCrow only on easy/memorization tasks (e.g., DEET, paracetamol, aspirin); ChemCrow wins on novel/complex tasks.

## Section map
1 Introduction · 2 Results & Discussion (2.1 Autonomous chemical synthesis, 2.2 Human-AI collaboration [chromophore], 2.3 Evaluation across diverse chemical use cases) · 3 Risk Mitigation Strategies · 4 Conclusion · 5 Methods (5.1 LLMs, 5.2 LangChain, 5.3 Tools [5.3.1 General / 5.3.2 Molecule / 5.3.3 Safety / 5.3.4 Reaction]) · Data & Code availability · Appendices A Experimental procedures, B Human evaluation (4 chemists), C GPT-4 vs ChemCrow synthesis example, D Safety Workflow, E Reproducibility (task 6, 5 runs), F Limitations, G 14 Tasks & Evaluation (G.1–G.14).

## Contemporaneous-work note
Paper distinguishes itself from ref [54] Boiko et al. ("Emergent autonomous scientific research…"): that work focuses on cloud labs; ChemCrow investigates a broader task/tool range including connection to a cloud-connected robotic synthesis platform.
