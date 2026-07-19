# Digest — manning2024automated (BLIND first-pass)

**Paper:** "Automated Social Science: Language Models as Scientist and Subjects"
**Authors / affil:** Benjamin S. Manning (MIT), Kehang Zhu (Harvard), John J. Horton (MIT & NBER). Both first authors contributed equally.
**Venue / ID:** arXiv:2404.11794v2 [econ.GN], dated 25 Apr 2024 (title page: April 26, 2024). Working paper (not a published-journal version in this PDF).
**Length:** 63 pp (main body ~30 pp + Appendices A/B/C).

---

## Thesis / Problem

Social science has good tools for *estimating* econometric models of behavior but little for *automatically generating and testing* the hypotheses/models to estimate. The paper presents a computational system that automatically (a) generates falsifiable social-scientific hypotheses, (b) designs experiments to test them, (c) runs those experiments on independent LLM-powered agents (simulated subjects), and (d) analyzes the results — an end-to-end "in silico" social science pipeline. **The key innovation is the use of structural causal models (SCMs)** to organize the whole process: an SCM simultaneously states a hypothesis, is a blueprint for constructing agents, defines the experimental design, and provides a pre-analysis plan for estimation.

Central empirical claim / motto: **"the LLM knows more than it can (immediately) tell."** Direct elicitation (asking the model to predict outcomes) is inaccurate, but running structured simulations extracts latent information the model cannot report directly.

---

## Method (answers to the flagged questions)

**Q1 — Statistical tests over full-factorial / structured designs? YES.**
- The system fits a linear SCM to simulated data using the **R package `lavaan`** (Rosseel 2012), reporting path estimates, standard errors, p-values, and standardized effect sizes (β̂*).
- **Full-factorial by default:** "By default, the system runs a factorial experimental design for all proposed values of each cause" (§3.3). Designs are the full cross-product of treatment levels (e.g., 9×9×5 = 405, 7×7×7 = 343).
- Available tests: likelihood-ratio, Wald, and Lagrange Multiplier tests for model fit / comparing path estimates; can estimate interactions and non-linear terms; "can do any statistical estimation or test that is built into lavaan" (§A.4).
- Causal identification is by design: exogenous variables are randomized, so estimates are described as unbiased ("All estimates in the fitted SCMs in Section 3 are unbiased … the data comes from an experiment, and we randomized on the causal variables," §5.1).

**Q2 — LLM as BOTH scientist and subject? YES (this is the title).**
- **Scientist role:** GPT-4 generates the relevant agents, outcomes, candidate causes, operationalizations, measurement questions, variable types, aggregation-method selection, interaction-protocol selection, and (implicitly) the analysis plan. "The system is implemented in Python and uses **GPT-4 for all LLM queries**" (§2). Over **50 pre-written scenario-neutral prompts** drive this.
- **Subject role:** independent GPT-4 instances are prompted to *be* the human agents (buyer, seller, judge, bidder, etc.), each endowed with name/role/goal/constraint + proxy attributes; they converse and are then surveyed to measure outcomes.
- The system can mix models (example: GPT-4 to generate hypotheses, Llama-2-70B to power the agents), but the reported experiments use GPT-4 throughout.

**Q3 — Circular-validity discussion (Generator and Experimental-subject sharing one model)? PARTIALLY / IMPLICITLY.**
- The paper does **not** use the term "circular validity," but §4 is essentially built around this concern. It asks: since the same model both proposes and is simulated, are the simulations even necessary — could the LLM just do a "thought experiment" and predict the results directly?
- **Finding:** direct elicitation fails. In the auction, direct predict-yᵢ is "wildly inaccurate" (MSE 8628 vs theory 128); predict-β̂ overestimates path magnitudes ~13.2× on average. Conditioning on the fitted SCM improves predictions sharply (MSE → 1505) but still worse than theory. Conclusion: simulation extracts information not available via introspection → the shared-model setup is argued to be *informative, not merely circular*.
- **External ground truth used to break circularity:** auction theory (Maskin & Riley 1985 — clearing price ≈ second-highest private valuation in an open-ascending auction) and empirical timber-auction evidence (Athey et al. 2011). Validation is against *theory*, not against real human subjects.
- Explicit boundary acknowledged: "There is still, of course, the fundamental jump from simulations to human subjects" (§6.1).

---

## FACTS TABLE (exhaustive) — value | location | context

### System design
| Value | Location | Context |
|---|---|---|
| GPT-4 for all LLM queries | §2 | System implemented in Python; GPT-4 powers scientist + subject roles |
| >50 pre-written scenario-neutral prompts | §2 fn6, §A | To gather all info needed to build SCM, run experiment, analyze |
| 6 interaction / turn-taking protocols | §2, §A.3.1, Fig A.2 | ordered, random, central-ordered, central-random, coordinator-before, coordinator-after |
| 6 aggregation methods | §A.1.1 | min, max, average, mode, median, sum |
| 5 variable types | §A.1.1 | continuous, ordinal, nominal, binary, count |
| 20 statements max per simulation | §2, §A.3.2 fn33 | Hard cap (not incl. coordinator); plus coordinator yes/no continue decision |
| GPT-4 max token limit 8,192 tokens | §A.3.2 fn33 | Given as partial reason for 20-statement cap |
| Two stopping conditions | §2 | (1) external/coordinator LLM decides continue after each turn; (2) 20-statement cap |
| R package `lavaan` (Rosseel 2012) | §A.4 | Used to estimate all SCM paths |
| Procedure exportable as a single JSON | §6.3 | Contains every decision, NL explanations, transcripts |

### Scenario 1 — Bargaining over a mug ("two people bargaining over a mug")
| Value | Location | Context |
|---|---|---|
| 9 × 9 × 5 = 405 simulations | §3.1, Fig 2a | Buyer budget (9) × seller min price (9) × seller love (5) |
| Deal reached in half of simulations; deal outcome µ=0.5, σ²=0.25 | §3.1, Fig 2b | Binary outcome |
| Buyer budget: +3.7 pp per $1; unstd 0.037 (0.003); β̂*=0.51; p<0.001 | §3.1, Fig 2b | Significant |
| Seller min price: −3.5 pp per $1; unstd −0.035 (0.002); β̂*=−0.49; p<0.001 | §3.1 | Significant |
| Seller love (ordinal): −2.5 pp per unit; unstd −0.025 (0.012); β̂*=−0.07; p=0.044 | §3.1 | Significant |
| Budget treatments [3,6,7,8,10,13,18,20,25] | Fig 2a | 9 values (note: text §2 gives illustrative {$5,$10,$20,$40}) |
| Seller-min treatments [3,5,7,8,10,13,18,20,25] | Fig 2a | 9 values |

### Scenario 2 — Bail hearing ("judge setting bail for a defendant who committed $50,000 in tax fraud")
| Value | Location | Context |
|---|---|---|
| "7 × 7 × 5 = 243" simulations | §3.2, Fig 3a | **Internal arithmetic error: 7×7×5 = 245, not 243** |
| 245 simulations | Fig A.5 note | Interaction-term version states 245 — inconsistent with main-text 243 |
| Agents: judge, defendant, defense attorney, prosecutor | §3.2, Fig 3a | Center-ordered protocol (judge = center) |
| Criminal history: +$521.53 per conviction; unstd 521.53 (206.567); β̂*=0.16; p=0.012 | §3.2, Fig 3b | Only significant standalone cause |
| Judge case count: unstd −74.632 (109.263); n.s. | §3.2, Fig 3b | Hypothesized to matter but did NOT affect bail |
| Defendant remorse: unstd −1153.061 (603.325); β̂*=−0.12; p=0.056 | §3.2 | Borderline / "unclear" |
| Bail amount µ=54428.57; σ²=1.9e7 | Fig 3b | Continuous outcome |
| Interaction (judge case count × remorse): β̂*=−0.32; p=0.047 | §3.2, Fig A.5 | In interaction model, criminal history no longer significant |

### Scenario 3 — Job interview ("a person interviewing for a job as a lawyer")
| Value | Location | Context |
|---|---|---|
| n = 80; 2 × 5 × 8 = 80 | §3.3 text | Passed bar (2, binary) × friendliness (5) × height (8) |
| Figure header prints "Simulations Run: 2 × 5 × 8 = 405" | Fig 4a | **Error: should be 80 (405 appears copied from mug figure); text and Fig A.6 both say 80** |
| Passed bar: +75 pp; unstd 0.75 (0.068); β̂*=0.78; p<0.001 | §3.3, Fig 4b | LARGEST standardized effect across all four scenarios |
| Interviewer friendliness: unstd −0.002 (0.005); n.s. | Fig 4b | No effect |
| Applicant height: unstd 0.003 (0.003); n.s. | Fig 4b | No effect |
| Employer decision µ=0.62; σ²=0.24 | Fig 4b | Fig A.6 lists σ²=0.23 (minor inconsistency) |
| Vars manually selected by authors; agents partly edited | §3.3 | Human-in-the-loop demo; system still designed+ran experiment |

### Scenario 4 — Auction ("3 bidders … auction for a piece of art starting at fifty dollars")
| Value | Location | Context |
|---|---|---|
| 7³ = 343 simulations | §3.4, Fig 5a | Each bidder: 7 budget values [$50–$350], private values |
| Bidder 1 budget: +$0.35 per $1; unstd 0.35 (0.015); β̂*=0.57; p<0.001 | §3.4, Fig 5b | Significant |
| Bidder 2 budget: +$0.29; unstd 0.29 (0.015); β̂*=0.47; p<0.001 | §3.4 | Significant |
| Bidder 3 budget: +$0.31; unstd 0.31 (0.015); β̂*=0.5; p<0.001 | §3.4 | Significant |
| Final price µ=186.53; σ²=3879.23 | Fig 5b | Appendix Figs A.7/A.8/A.9 give σ²=3867.92 (inconsistency) |
| Each bidder ~1/3 chance of being marginal | §3.4 | Rationalizes ~0.33 coefficients |
| Clearing price ≈ second-highest reservation | §3.4, abstract | Matches Maskin & Riley (1985) + Athey et al. (2011) |

### Section 4 — LLM predictions (thought-experiment test)
| Value | Location | Context |
|---|---|---|
| ~5 hours to run; cost >$1,000 | §4 | Total cost of the Section-3 experiments |
| MSE_yi = 8628 | §4.1, Fig 6 | Direct predict-yᵢ (auction), no SCM |
| MSE_Theory = 128 | §4.1, Fig 6 | Auction-theory prediction error |
| MSE_yi−Theory = 8915 | §4.1 | LLM predictions further from theory than empirical results are |
| 80/343 auctions hit 20-statement cap; removed | §4.1 fn11 | Theory makes no prediction for partial auctions |
| 12 predictions (4 experiments × 3 causes) | §4.2 | predict-β̂ task |
| Predicted paths avg 13.2× larger than actual | §4.2, Table A.1 | Overestimation |
| 10/12 overestimates; 10/12 sign correct; 10/12 significance correct | §4.2 | At temperature 0 |
| Avg magnitude ratio still 5.3 after removing largest overestimate | §4.2 | Robustness note |
| Predictions once at temp 0; also averaged over 100 prompts at temp 1 | §4 fn10, Table A.2 | "results are similar" |
| MSE_yi\|β̂−i = 1505 | §4.3, Fig 6 | Predict-yᵢ WITH leave-one-out fitted SCM; ~6× lower than 8628 |
| MSE_yi\|β̂−i−Theory = 1761 | §4.3 | Still further from theory than from empirical |
| MSE_Mechanistic:yi\|β̂−i = 725 | §4.3 fn16 | Pure mechanical prediction beats the LLM even with SCM |
| Augmented SCM (2nd-highest reservation as cause): β=0.912, R²=0.977 | §4.3 fn17, Fig A.9 | Matches auction theory when correct exogenous var added |

### Section 5 — Identifying causal structure ex-ante
| Value | Location | Context |
|---|---|---|
| # possible DAGs for n=1,2,3,4 nodes = 1, 3, 25, 543 | §5.2 fn22 | Combinatorial explosion motivating SCM-first approach |
| GES algorithm (Chickering 2002) | §5.2, Fig 8 | Greedy Equivalence Search; gave wrong/undirected causal structure for tax-fraud data |
| Convo-length SCM (correct): buyer budget p<0.001; seller min p=0.026; seller love p=0.147 | §5.1, Fig 7a | Downstream outcome, unbiased |
| Misspecified SCM: deal-made p=0.008; buyer budget p=0.189; seller min p=0.755 | §5.1, Fig 7b | "Bad control" (deal occurs) flips significance |
| GES not perfectly stable across runs | §5.2 fn23 | Noted limitation of the search method |

---

## Scope & Limitations (as stated by the paper)

- Uses **simple linear SCMs "unless stated otherwise"** — acknowledged as "not necessarily correct" but an "unequivocal starting point."
- System **"yet to be optimized for novelty"**; findings are "not counterintuitive" (but empirical, not introspective).
- Transition from one experiment to the next is **not yet automated** (follow-on experiments described but manual, §A.5).
- Many **subjective design choices**; "only one possible implementation of the SCM-based approach."
- Open research problems flagged: which agent attributes to endow; engineering turn-taking; stopping rules (halting-problem analogy, Turing 1937; a Markov model on real conversation data suggested for future work).
- Reproducibility pitch: entire procedure exportable as JSON (§6.3).

## Does NOT claim / boundaries

- Does **NOT** claim simulations replace human subjects — "the fundamental jump from simulations to human subjects" remains.
- Does **NOT** validate against real human-subject data in this paper; external benchmark is auction *theory* + prior empirical auction findings, and only the auction scenario has such a benchmark.
- Does **NOT** claim the LLM can predict *magnitudes* by direct elicitation (only signs/significance reasonably well); "cannot reliably predict the magnitudes."
- Does **NOT** claim full automation of iterated research programs (that is future work).
- Does **NOT** assert SCM search algorithms (GES) recover truth — argues the opposite (they can misidentify direction/structure).

## Section Map

- §1 Introduction — motivation, SCM innovation, summary of findings (incl. 13.2× overestimate, MSE numbers).
- §2 Overview of the system — 6-step social-science analogy; SCM as blueprint; GPT-4; prompts; protocols; stopping rules.
- §3 Results of experiments — 3.1 mug bargaining, 3.2 bail hearing, 3.3 lawyer interview, 3.4 art auction.
- §4 LLM predictions for paths and points — 4.1 predict-yᵢ, 4.2 predict-β̂, 4.3 predict-yᵢ|β̂−i.
- §5 Identifying causal structure ex-ante — 5.1 assuming structure (bad controls), 5.2 searching (GES).
- §6 Conclusion — 6.1 controlled experimentation at scale, 6.2 interactivity, 6.3 replicability, 6.4 future research.
- Appendix A Implementation details (A.1 variables/paths, A.2 agents, A.3 simulation design/execution, A.4 path estimation, A.5 follow-on).
- Appendix B Hypotheses as SCMs (DAG ambiguity, linear SCM equations).
- Appendix C Additional figures/tables (interaction-term SCMs, Table A.1/A.2 GPT-4 predictions, prompt in Fig A.11, Table A.3 variable-info example).

## Audit-relevant flags (internal inconsistencies noticed blind)

1. **Bail sims: "7×7×5 = 243" (Fig 3a) vs correct 245 (arithmetic; Fig A.5 confirms 245).**
2. **Lawyer-interview figure header prints "2 × 5 × 8 = 405" (Fig 4a) — should be 80; text and Fig A.6 say 80.**
3. Auction final-price variance: 3879.23 (main Fig 5b) vs 3867.92 (appendix Figs A.7–A.9).
4. Employer-decision variance: 0.24 (Fig 4b) vs 0.23 (Fig A.6).
5. Illustrative budget values differ between narrative ({$5,$10,$20,$40}, §2) and actual treatments (Fig 2a) — narrative is explicitly an example, not a discrepancy per se.
