# king2004robot — FULL-TEXT blind digest (READ)

**Paper:** King, Whelan, Jones, Reiser, Bryant, Muggleton, Kell, Oliver, "Functional genomic
hypothesis generation and experimentation by a robot scientist," Nature 427:247-252 (2004).
**Source obtained:** author-hosted PDF (Aberystwyth Robot Scientist page),
`~dcswww/Research/bio/robotsci/publications/KingNature2004.pdf`; saved to local vault at
`ai_scientist/1_AI_Scientist_Core/Reference/King 2004 - Functional genomic hypothesis generation and experimentation by a robot scientist.pdf`.
Extraction note: the 6-page Nature-letters PDF also contains the preceding letter
(Koerding-Wolpert Bayesian sensorimotor); King text begins at line 161 of the extract
(title/authors verified verbatim).

## Problem / method
Automates the discovery cycle (hypothesis -> experiment design -> robotic execution ->
interpretation -> repeat) for yeast (S. cerevisiae) gene function via auxotrophic growth
experiments on deletion mutants; builds a logical model of the aromatic-amino-acid (AAA)
synthesis pathway; uses abductive logic programming to generate hypotheses.

## FACTS TABLE (experiment-selection mechanism — the load-bearing content)
- p.249 verbatim: "the branch of machine learning that deals with algorithms that can choose
  experiments is known as **'active learning'**." (paper's OWN term)
- p.249 verbatim: "If we assume that each hypothesis has a **prior probability** of being correct
  and that each experiment has an associated **cost**, then scientific experiment selection can be
  formalized as the task of selecting the **optimal series of experiments (in terms of expected
  cost)** to eliminate all except the one correct hypothesis."
- p.249: problem is NP-hard in general; equivalent to smallest-decision-tree; "**a bayesian
  analysis** of decision-tree learning has shown that **near-optimal solutions can be found in
  polynomial time**."
- p.249: explicit expected-cost recurrence EC(H,T) with prior probabilities p(h) and an entropy
  term J_H = -Sum_h p(h) log2(p(h)) -> an information-theoretic (EIG-like) + cost criterion.
- Strategy named **ASE** (active selection of experiments). p.249: "to achieve an accuracy of
  about 70%, ASE requires ... **a hundredth of the price, of Random**, and ... **a third of the
  price, of Naive** [cheapest]."
- Abstract: "intelligent experiment selection strategy is **competitive with human performance**
  and significantly outperforms, with a cost decrease of 3-fold and 100-fold (respectively), both
  cheapest and random-experiment selection."
- p.249 (human comparison): using nine graduate computer scientists and biologists, "there was
  **no significant difference between the robot and the best human performance**" in iterations to
  reach a given accuracy.

## Scope / limits
Single pathway (AAA) in one organism; noise ~25% in vivo (robot open to air). Authors note most
molecular genetics needs more sophisticated abduction/experiment design than this model.

## Adjudication of manuscript claims attributed to this key
- **C045 (EN L85) / C047 (EN L92, KO L111) / C048 (EN L94, KO L113) / C130** — the Robot
  Scientist's **active-learning / Bayesian-optimal experiment selection**: **ACCURATE and now
  primary-source-verified.** King 2004 (a) uses the exact term "active learning", (b) formalizes
  selection as expected-cost-optimal under Bayesian priors with an entropy criterion, and (c)
  proves near-optimal polynomial-time solutions via Bayesian decision-tree analysis. The
  manuscript's "Bayesian-optimal experiment selection" is faithfully supported (the earlier
  "too strong" caution is **RETRACTED**). This is the correct source; sparkes2010robot (2010
  review) did not describe the mechanism.

## Claim
- **C130 — ACCURATE (full-text verified).** King 2004 is the correct and well-matched source of
  the Robot Scientist's active-learning / Bayesian expected-cost experiment selection. No manuscript
  change needed; "Bayesian-optimal" stands.
