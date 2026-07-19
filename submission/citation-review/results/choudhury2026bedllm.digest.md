# Digest: choudhury2026bedllm (BED-LLM)

BLIND first-pass reading. Base ONLY on the paper itself. Locations are line numbers
in the pdftotext dump (`bedllm.txt`) plus section labels from the PDF.

## Bibliographic header
- Title: "BED-LLM: Intelligent Information Gathering with LLMs and Bayesian Experimental Design" (p.1, lines 3-4).
- Venue: "Published as a conference paper at ICLR 2026" (running header on every page, line 1).
- Preprint id: arXiv:2508.21184v3 [cs.CL] 20 Apr 2026 (line 19).
- Authors: Deepro Choudhury, Sinead Williamson, Adam Goliński, Ning Miao, Freddie Bickford Smith, Michael Kirchhof, Yizhe Zhang, Tom Rainforth (lines 5-6).
- Affiliations: University of Oxford (∗), Apple (†), City University of Hong Kong (‡) (lines 9-17).
- Code: https://github.com/DeeproChoudhury/BED-LLM (§J, line 2860).

## Thesis / problem
Intelligent information gathering — asking the right questions at the right time — is
fundamental to AI, but LLMs "currently fall short on proactively seeking out information
from a user or external environment in an adaptive manner" (§1, lines 42-43). They can
generate good single-turn questions but "struggle to appropriately tailor their questions
to previously gathered responses on interactive tasks" (§1, lines 47-49). The paper
proposes a general-purpose, deployment-time method to make LLMs adaptively gather
information, framed as **sequential Bayesian experimental design (BED)** (§1, lines 61-64).

## Method — direct answers to the two audit questions

**Q1: Does BED-LLM derive a usable EIG from the LLM's PREDICTIVE DISTRIBUTIONS? YES.**
- Abstract states the EIG "can be formulated (and then estimated) in a principled way
  using a probabilistic model derived from the LLM's predictive distributions" (lines 30-32).
- The joint model is built directly from the LLM: initial joint `p(θ,y;x) = p(θ) pLLM(y;[θ,x])`
  (prior-likelihood pairing) (§3, line 190).
- The EIG estimator (Eq. 3, §3.3, lines 368-373) is an explicit **Rao-Blackwellized estimator
  based on the LLM's predictive distribution**: it sums LLM answer-likelihoods
  `pLLM(yt;[θn,xt])` over the (small, enumerable) answer space Y, using the LLM's logits
  "whenever possible" (line 382). So the EIG is computed from the LLM's per-answer predictive
  probabilities, not from an external simulator or trained surrogate.
- The belief state `pf(θ;ht−1)` over the target θ is likewise derived from the LLM's
  in-context predictive distribution `pLLM(θ;ht−1)`, then filtered for history-consistency
  and made uniform over survivors (§3.1, lines 240-255).

**Q2: Is the application CONVERSATIONAL / INFORMATION-GATHERING (20-questions, preference
inference), NOT physical experiment design? YES — conversational/interactive queries.**
- Two and only two experimental domains (§6, lines 490-493):
  1. **20 Questions** — a game where the questioner LLM guesses a hidden target entity by
     asking up to 20 yes/no questions (§6.1).
  2. **Preference elicitation** — inferring a user's film/movie preference profile by asking
     five multiple-choice questions, then producing film recommendations (§6.2).
- Queries `x` are "explicit questions asked to the user" (§2, line 109). The framework is
  said to generalize to "retrieving documents or calling external functions" / "external
  function calling, document retrieval, web search" (§2 line 110-111; §3 line 210), but the
  paper does NOT run any such experiment and does NOT do any physical/lab experiment design.
- "AI-driven scientific inquiries (Lu et al., 2024; Mandal et al., 2025)" appear only as one
  item in a motivating list of downstream domains in the intro (§1, line 58) — not as a
  task BED-LLM performs. The method is about conversational/interactive information gathering.

**Application domain, stated precisely:** deployment-time (no fine-tuning) adaptive
*conversational query selection* for LLMs — multi-turn information gathering where the LLM
picks the next question to a user/external source by maximizing EIG about a target of
interest θ. Demonstrated on the 20 Questions guessing game and LLM-driven user-preference
(film) elicitation. It is emphatically NOT physical/scientific experiment design.

### The BED-LLM loop (§3, lines 208-222; Fig. 1)
Per turn t: (A) Extract beliefs — build hypothesis set Θcand by sampling `θ ∼ pLLM(θ;ht−1)`
and rejecting inconsistent ones, giving `pf(θ;ht−1)` uniform over survivors; (B) Generate M
diverse multiple-choice candidate questions Xcand; (C) Estimate EIGθ(xt;ht−1) for each
candidate via Eq. 3; (D) Select/ask the arg-max-EIG question; (E) Observe response, update
history ht.

### Three core algorithmic components (Table 2, lines 885-934)
1. Joint model: **prior-likelihood pairing** `p(θ)pLLM(y;[θ,x])` (vs. data-estimation pairing).
2. Objective: **full EIG (Eq. 3)** with a *non-deterministic* likelihood (vs. predictive
   entropy under a deterministic-likelihood assumption).
3. Belief updates: **filtered** `pf` (sample-then-filter-then-uniform), between naive
   in-context updating and full Bayesian updating (§3.1).

### Key modeling stances
- Uses the LLM's uncertainty "in the space of answers rather than the more complicated
  underlying hypothesis space" (§1, lines 76-77) — favor prior-likelihood when θ is more
  complex than y (§4, lines 457-462).
- **Static likelihood**: does NOT update `pLLM(yt;[θ,xt])` with history; §A.1/§F.3 show
  updating it hurts (Table 4).
- Central novelty claim (Conclusion, lines 1090-1092): "BED-LLM is notably the first work
  that uses both this prior-likelihood pairing without making a deterministic likelihood
  assumption that causes the EIG to [collapse] to just marginal predictive entropy."

## FACTS TABLE (exhaustive)

| Value | Location | Context |
|---|---|---|
| ICLR 2026 conference paper | header, line 1 | Publication venue |
| arXiv:2508.21184v3, 20 Apr 2026 | line 19 | Preprint version/date |
| 8 authors; Oxford / Apple / City U. Hong Kong | lines 5-17 | Authorship & affiliations |
| **+37.4 percentage points** avg improvement over direct prompting on 20 Questions | Abstract line 82; §1 | Headline result |
| Success rate "more than doubling in over half of the setups... and never decreasing" | Abstract lines 83; §1 line 83 | 20Q success-rate claim |
| EIG maximization w.r.t. variable of interest θ given prior responses | Abstract lines 28-30 | Core objective |
| Method name = "Bayesian experimental design with large language models" | Abstract line 27 | Acronym expansion |
| Eq. 1: EIGθ(x)=H[p(θ)]−E_{p(y;x)}[H[p(θ\|y;x)]] | §2.2, line 146 | EIG form (a): info gain in θ |
| Eq. 2: =H[p(y;x)]−E_{p(θ)}[H[p(y\|θ;x)]] | §2.2, line 150 | EIG form (b): predictive-entropy form |
| Eq. 3: Rao-Blackwellized EIG estimator from LLM predictive dist. | §3.3, lines 368-373 | Estimator actually used |
| `p̂(yt;[ht−1,xt]) = (1/N)Σ pLLM(yt;[θn,xt])`, θn∼pf(θ;ht−1) | §3.3, lines 378-379 | Marginal predictive term |
| Rao-Blackwell ⇒ always lower variance than sample-based estimators | §3.3, lines 383-384 | vs. Hu et al. 2024, Kobalczyk et al. 2025 |
| Initial joint model `p(θ,y;x)=p(θ)pLLM(y;[θ,x])` (prior-likelihood) | §3, line 190 | Chosen factorization |
| Data-estimation pairing `p(yt;[ht−1,xt])p(θ;[ht−1,xt,yt])` | §4, line 409 | Alternative factorization (an ablation) |
| Filtering threshold = 0.2 (reject sample if answer prob below it) | §E, lines 2029-2030 | Hypothesis-filtering hyperparameter |
| Hypothesis-generation temperature T=1.3 (20Q), T=1 (preference) | §E, lines 2025-2026 | Sampling temperatures |
| Multiple-choice question format (to simplify uncertainty quantification) | §3.2 line 363; §4 | Design restriction |
| Models: GPT-4o-mini, GPT-4o, Llama-3.1-8B, Llama-3.3-70B, Mistral-Large, Qwen2.5-72B | Table 1, lines 706-711 | Backbone LLMs |
| 3 problem sets (Animals, Celebrities, Things), 100 targets each | §6.1, lines 674-675 | 20Q datasets |
| Up to 20 yes/no questions per 20Q game; turns t∈(0..20) | §6 line 491; §6.1 line 680 | 20Q budget |
| Preference elicitation: 5 multiple-choice questions; turns t∈(0..5) | §6 line 493; §6.2 line 1073 | Preference budget |
| 200 ground-truth user profiles | §6.2, line 1068 | Preference dataset size |
| 10 film recommendations rated per turn, scale 1-5 in 0.5 increments | §6.2, lines 1073-1076 | Preference evaluation metric |
| Preference θ = user profile = paragraph of text describing film tastes | §6.2, lines 1065-1067 | Target definition |
| MovieLens-100K (Harper & Konstan 2015) → 200 real ratings → o3 writes profiles | §I.1, lines 2786-2789 | Profile generation source |
| Animals set generated by OpenAI o3 (o3-2025-04-16); Celebrities & Things from Zhang et al. 2024 | §H.1, lines 2620-2624 | Dataset provenance |
| Baselines: Prompt-Only, CoT (ReAct-style), Split | §6 lines 654-665 | Comparison methods |
| Split = previous SOTA for 20 Questions (marginal-predictive-entropy under deterministic likelihood) | §6, lines 660-665 | Prior best baseline |
| Ablations: Entropy, Data-Estimation, ICL Beliefs, Implicit Maximization | §6.1, lines 691-942; Table 2 | One-component-changed variants |
| Prior works assuming deterministic likelihoods: Cooper 2025, Kobalczyk 2025, Hu 2024, Mazzaccara 2024, Piriyakulkij 2023 | §3.3 lines 386-387; §5; §C | Related-work grouping |
| Implicit Maximization = collapsed Tree-of-Thoughts (ToT) lookahead in one LLM call | §6.1 lines 938-942; §G lines 2589-2601 | Ablation description |
| 20Q hyperparams: N=15 hypotheses, M=15 candidate questions | §H.3, lines 2771-2775 | Algorithmic settings |
| Preference hyperparams: M=8 candidate questions, N=5 hypotheses | §I.3, lines 2821-2822 | Algorithmic settings |
| Answerer is a separate LLM given θ*, no access to questioner context | §6, lines 494-496 | Experimental protocol |
| Two questioner-answerer setups: same LLM vs. different LLMs (model misspecification) | §6, lines 496-497 | Robustness test design |
| Q=GPT-4o-mini/A=Qwen2.5-72B and reverse used as cross-model pairs | Fig. 2 lines 532-636 | Mismatch experiments |
| Runtime (Qwen2.5-72B, Animals): Data-Est. 1d17h13m; ICL Beliefs 3h10m; Entropy 2h46m; Split 2h30m; BED-LLM 2h28m; Impl.Max. 45m; CoT 35m; Prompt-Only 26m | Table 3, lines 2438-2457 | Wall-clock cost |
| Table 1 (20Q final success %) e.g. GPT-4o Animals: BED-LLM 93±2.6 vs Prompt-Only 45±5.0 vs Split 62±4.9 | Table 1, lines 706-720 | Representative numbers |
| Static vs updated likelihood: static wins on most cells (Table 4) | §F.3, lines 2469-2536 | Ablation result |
| Std-error estimator sqrt(p(1−p)/(n−1)), positively biased/conservative | Table 1 caption, lines 882-884 | Statistics method |
| EIG estimator convergence: ranking of 5 candidates stable by \|Θ\|=10 (matches \|Θ\|=85) | §F.1, Fig. 10, lines 2132-2139 | Sample-budget justification |
| Extended to 50 turns: BED-LLM best at every turn; gap narrows as task saturates | §F.1, Fig. 9, lines 2104-2107 | Long-horizon result |
| pLLM(θ) is "heavily overconfident on a small number of hypotheses" | §3.1, lines 231-233; Fig. 5 | Motivation for filtering |
| Fig. 5: N=200 samples → 93 van Gogh, mode collapse | §D.3, lines 1919-1937 | Diagnostic of overconfidence |

## Scope & limitations
- **Deployment-time only**: focuses on how the model is *used*, not fine-tuning; "improvements
  at the model level... would be complementary" (§2, lines 91-96).
- **Myopic / greedy**: optimizes only the next-step (incremental) EIG; acknowledges traditional
  sequential BED can be suboptimal vs. policy-based lookahead, and positions BED-LLM as a
  *complementary building block* for policy-based methods, not a replacement (§C, lines 1790-1799).
- **Two task families only**: 20 Questions and film-preference elicitation. No physical/lab
  experiments, no tool-use/retrieval experiments (those are aspirational generalizations).
- **Data-estimation pairing unviable for large θ**: for preference elicitation, entropy over
  the free-form profile space θ "is not only infeasible to estimate, but also is not a
  meaningful measure of uncertainty" (§I.3, lines 2825-2827); Split baseline also inapplicable
  there (§6.2, lines 1070-1071).
- **Answer space assumed enumerable/multiple-choice** so entropies are computable from logits
  (§4 line 363; §I.1 lines 2791-2797).

## Does NOT claim / boundaries
- Does NOT claim to fine-tune or modify the LLM (no training/data required — explicitly
  contrasted with Wang et al. 2025 which meta-trains, §C lines 1701-1705).
- Does NOT do full Bayesian posterior inference; uses a sample-filter-uniform approximation
  `pf` that sits "somewhere between the two" extremes (§3, lines 203-206; §3.1).
- Does NOT assume deterministic answer likelihoods — this is the stated differentiator from all
  cited prior EIG-for-LLM works, whose objectives collapse to marginal predictive entropy
  (§3.3 lines 385-400; §5; Conclusion lines 1090-1092).
- Does NOT restrict the hypothesis space of θ: the target list is never revealed to the
  questioner, so θ is "bounded only by what the LLM can generate" — contrasted with prior works
  that use restricted/closed-world θ (Chan 2025, Hu 2024, Piriyakulkij 2023, Wang 2025)
  (§6.1, lines 676-679).
- Does NOT perform physical experiment design or automated scientific experimentation; those
  are cited only as motivating downstream domains (§1, line 58).

## Section map
- §1 Introduction — problem, BED framing, headline results (lines 38-85).
- §2 Problem formulation & background — target θ, history ht, in-context updating (§2.1),
  information-theoretic experimental design / EIG Eqs. 1-2 (§2.2) (lines 87-167).
- §3 Sequential BED with LLMs — model construction/updating, the BED-LLM loop (A)-(E);
  §3.1 prior construction & belief updating (filtering, pf); §3.2 generating candidate
  questions (unconstrained vs conditional); §3.3 EIG estimator Eq. 3, avoiding deterministic
  likelihoods (lines 169-400).
- §4 On the specification of the joint p(θ,yt;ht−1,xt) — prior-likelihood vs data-estimation:
  modeling flexibility, faithfulness of conditionals, complexity of θ vs y, belief-state
  extraction (lines 402-467).
- §5 Related work (brief) — prior EIG-for-LLM works, deterministic-likelihood grouping
  (lines 469-484).
- §6 Experiments — answerer setup, baselines; §6.1 20 Questions (results, ablations,
  prior-likelihood>data-estimation, misspecification robustness); §6.2 Preference elicitation
  (lines 486-1081).
- §7 Conclusion — summary + "first work" novelty claim (lines 1083-1094).
- Appendices: §A discussion re §3 (likelihood updating, predictive-entropy≠EIG, EIG estimator,
  prior/belief); §B discussion re §4 (conditional faithfulness, choice of θ, EIG/update
  alignment); §C extended related work; §D data-estimation method + Algorithm 1; §E generating
  candidate hypotheses for BED-LLM; §F additional results (50-turn, wall-clock Table 3,
  static-vs-updated likelihood Table 4); §G method/ablation descriptions + prompts; §H 20Q
  experiment details (problem sets, evaluation, hyperparams); §I preference-elicitation details;
  §J code link (lines 1310-2860).
