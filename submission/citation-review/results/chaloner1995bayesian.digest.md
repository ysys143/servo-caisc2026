# Digest — chaloner1995bayesian (BLIND first-pass read)

**Source read:** JSTOR scan, body pages OCR'd (pdftotext returned only the JSTOR
cover; the 33-page body is scanned images). Rendered pg-02..pg-33 @300 DPI →
tesseract. OCR file: `/Users/jaesolshin/.claude-3/jobs/e6b73762/tmp/chaloner_ocr.txt`.
Page map: OCR label `pg-NN` = journal page (NN + 271), e.g. pg-02 = p.273.

**Citation:** Kathryn Chaloner & Isabella Verdinelli, "Bayesian Experimental
Design: A Review," *Statistical Science* **10**(3), Aug. 1995, pp. 273–304
(Institute of Mathematical Statistics; JSTOR 2246015). Chaloner: School of
Statistics, Univ. of Minnesota. Verdinelli: Univ. di Roma "La Sapienza" &
Carnegie Mellon. (pg-02)

---

## Thesis / problem

A **review of the literature on Bayesian experimental design (BED)**, presenting
a **unified view based on a decision-theoretic approach**. The framework "casts
criteria from the Bayesian literature of design as part of a single coherent
approach," incorporates both **linear and nonlinear** design problems, and gives
"a mathematical justification for selecting the appropriate optimality
criterion." Core organizing idea (Abstract, pg-02): the experimenter specifies a
**utility function** reflecting the purpose of the experiment and chooses the
design that **maximizes expected utility**. Different utilities/criteria yield
different optimal designs.

## Method — IS this the classical BED review with a normative EIG / expected-utility criterion? YES.

**Normative criterion = maximize expected utility (Lindley's decision-theoretic
argument).** Following Raiffa & Schlaifer (1961) and Lindley (1972, pp. 19–20),
the paper states the general utility U(d, θ, η, y) and defines (pg-04, p.275):

- Eq. (1): **U(η) = ∫∫ U(d, θ, η, y) p(θ|y, η) p(y|η) dθ dy** — expected utility
  of the best decision for design η.
- Eq. (2): "**The Bayesian solution to the experimental design problem is
  provided by the design η\* maximizing (1).**" i.e. "specify a utility function
  reflecting the purpose of the experiment ... regard the design choice as a
  decision problem and ... select a design that **maximizes the expected
  utility**." This is the normative design criterion.

**Expected Information Gain / Shannon information IS covered as the canonical
information utility (= EIG).** Pg-06 (p.277): "Following Lindley's (1956)
suggestion, several authors (Stone, 1959a,b; DeGroot, 1962, 1986; Bernardo,
1979) considered the **expected gain in Shannon information** given by an
experiment as a utility function (Shannon, 1948). These authors proposed
choosing a design that **maximizes the expected gain in Shannon information** or,
equivalently, **maximizes the expected Kullback–Leibler distance between the
posterior and the prior distributions**":

- Eq. (3): ∫∫ log[ p(θ|y,η) / p(θ) ] p(y,θ|η) dθ dy  (expected posterior-to-prior
  KL — this is exactly EIG / mutual information I(θ; y | η)).
- Eq. (4): **U₁(η) = ∫∫ log{p(θ|y,η)} p(y,θ|η) dθ dy** — "the expected Shannon
  information of the posterior distribution," used when the experiment is for
  inference on θ.
- Pg-04 (p.275): "a utility function based on **Shannon information leads to
  Bayesian D-optimality** in the normal linear model (see Bernardo, 1979)."

So the manuscript's EIG objective d\* = argmax E[H(θ) − H(θ|y,d)] is precisely
this paper's "expected gain in Shannon information = expected KL(posterior‖prior)"
utility (Eqs. 3–4), and the general normative criterion (Eqs. 1–2) is expected-
utility maximization of which EIG is the information-based special case.

**Alphabetical criteria as special cases.** Bayesian A-, c-, D-, E-, G-optimality
are derived from utility/loss functions (D-opt from Shannon info or proper
scoring rules; A-opt/c-opt from quadratic/squared-error loss). Note: **not all**
alphabetical criteria have a utility-based Bayesian version — Bayes E-optimality
and G-optimality "do not correspond to maximizing a utility function" and their
decision-theoretic justification is "unclear" (pg-07).

**Nonlinear design.** For nonlinear models exact expected utility has no closed
form; approximations (normal approx. to posterior; expected Fisher information
matrix 𝓕(θ,η)) are required. Bayesian nonlinear design criteria = **expectation
over the prior of a local-optimality criterion** (Chaloner & Larntz 1986/1989);
an **equivalence theorem** (Whittle 1973) certifies optimality; **local
optimality** (Chernoff 1953) = crude one-point-prior approximation, "approximately
Bayesian." Key qualitative result: the **number of support points in an optimal
Bayesian nonlinear design increases as the prior becomes more dispersed** (pg-18).

## FACTS TABLE (exhaustive of load-bearing content)

| value / statement | location | context |
|---|---|---|
| Statistical Science 10(3):273–304, Aug 1995 | pg-02 (p.273) | Publication record (JSTOR 2246015) |
| Kathryn Chaloner (Univ. Minnesota); Isabella Verdinelli (Roma La Sapienza / CMU) | pg-02 (p.273) | Authors/affiliations |
| "This paper reviews the literature on Bayesian experimental design. A unified view ... based on a decision-theoretic approach." | pg-02 (p.273), Abstract | Thesis; it is a REVIEW |
| Key words: decision theory, hierarchical linear models, logistic regression, nonlinear design, optimal design, optimality criteria, utility functions | pg-02 (p.273) | Scope keywords |
| Eq (1) U(η)=∫∫U(d,θ,η,y)p(θ|y,η)p(y|η)dθdy; Eq (2) design η\* maximizes (1) | pg-04 (p.275) | **Normative criterion = max expected utility** (Lindley 1972; Raiffa & Schlaifer 1961) |
| "select a design that maximizes the expected utility" | pg-04 (p.275) | Statement of the normative rule |
| Shannon-information utility → Bayesian D-optimality in normal linear model (Bernardo 1979) | pg-04 (p.275) | Info utility ↔ D-optimality |
| "expected gain in Shannon information ... equivalently ... expected Kullback–Leibler distance between the posterior and the prior" (Lindley 1956; Stone 1959; DeGroot 1962,1986; Bernardo 1979; Shannon 1948) | pg-06 (p.277) | **EIG defined as utility** |
| Eq (3) ∫∫ log[p(θ|y,η)/p(θ)] p(y,θ|η) dθdy | pg-06 (p.277) | Expected posterior-to-prior KL = EIG |
| Eq (4) U₁(η)=∫∫ log{p(θ|y,η)} p(y,θ|η) dθdy = "expected Shannon information of the posterior" | pg-06 (p.277) | EIG design objective for inference on θ |
| Bayes A-optimality: maximize φ₂(η)=−tr{A D(η)}; from quadratic loss U₂ (Eq 7) | pg-07 (p.278) | Alphabetical criterion from utility |
| Bayes c-optimality (rank-1 A); Elfving-type geometry (Chaloner 1984) | pg-07 (p.278) | Special case |
| Bayes E-optimality & G-optimality "do not correspond to maximizing a utility function"; Bayesian justification "unclear" | pg-07 (p.278) | Boundary: not every criterion is utility-based |
| Utility functions catalogued: U₁ (Shannon/D-opt), U₂ (quadratic/A-opt), U₃ (predictive Shannon info), U₄ (Verdinelli & Kadane 1992: info + total output, weights ρ,β), U₅ (Verdinelli 1992: inference + prediction) | pg-06..pg-09 (p.277–280) | Menu of utilities → "different designs from different utilities" |
| Large-n limit: D(n)=n⁻¹(M(η)+n⁻¹R)⁻¹ → Bayesian ≈ non-Bayesian design when n large or prior diffuse; "when a noninformative prior ... there is no advantage to using the Bayesian approach for design" (linear) | pg-08 (p.279) | Boundary: Bayesian advantage is at small n / informative prior |
| Nonlinear: exact expected utility has no closed form; use normal approx + expected Fisher info 𝓕(θ,η); criteria φ (15),(16),(18),(19),(20) | pg-13..pg-15 (p.284–286) | Approximation methods |
| Local optimality (Chernoff 1953,1962; Box & Lucas 1959): one-point prior, "crude approximation," "approximately Bayesian" | pg-16 (p.287) | Non-Bayesian special case |
| Bayesian nonlinear criterion = ∫ (local criterion) p(θ)dθ; equivalence theorem (Whittle 1973); directional-derivative check | pg-17..pg-18 (p.288–289) | Optimality certification |
| Number of support points **increases as prior becomes more dispersed** (Chaloner & Larntz 1986,1989) | pg-18 (p.289) | Signature qualitative BED result |
| Example 1: one-way ANOVA, allocate n obs across t groups (control vs treatments; "square root rule") | pg-03, pg-10..pg-13 | Linear illustration |
| Example 2: logistic regression LD50; 54 experiments, 6 equally-spaced doses × 10 mice = 60 animals; Beta(4,4) prior; used design ≈ Bayes-optimal | pg-03, pg-20..pg-21 (p.291–292) | Nonlinear illustration; "experimenters may already be ~optimal" |
| Example 3: nonlinear pharmacokinetic compartmental model (Atkinson et al. 1993); 18-point design; ϕ₂-optimal designs for AUC, t_max, c_max | pg-04, pg-22 (p.293) | Nonlinear regression illustration |
| Sequential design: for most LINEAR problems (σ² known) no gain over fixed design; for nonlinear, sequential can gain | pg-19 (p.290) | Boundary on sequential value |
| Software: Clyde (1993b) XLISP-STAT object-oriented system; Chaloner & Larntz (1988) FORTRAN for logistic regression (needs NPSOL) | pg-19 (p.290) | Practical tooling of the era |
| "Bayesian design is an exciting and fast-developing area of research." | pg-27 (p.298) | Concluding remark |
| "it does remain regrettable ... that so few real case studies appear in the ... literature of Bayesian optimal design" | pg-27 (p.298) | Self-stated limitation |

## Scope & limitations / boundaries (does NOT claim)

- It is a **theory/methodology REVIEW** of classical statistical design (linear
  & nonlinear regression, ANOVA, clinical-trial sample size, reliability/QC,
  computer experiments). Explicitly notes **applications lag theory**: "Apart
  from Flournoy (1993), there are no true 'case studies' ... where Bayesian ideas
  have been formally applied to the design of an actual scientific experiment
  before it is done." (pg-02, p.273)
- The **general normative criterion is expected-UTILITY maximization**; EIG
  (expected Shannon-information gain / expected posterior-to-prior KL) is the
  canonical *information* utility (Eqs 3–4), but the bulk of the paper treats
  "alphabetical" criteria (A/c/D/E/G) — some of which (E, G) are **not**
  utility-based. So the paper is broader than, and grounds, the pure-EIG framing.
- **No modern computational machinery**: nested/multi-level Monte Carlo,
  variational EIG bounds, amortized/policy-based design (DAD/iDAD), or
  reinforcement learning are **absent** (those are the modern additions, e.g.
  Rainforth et al. 2024). Chaloner uses analytic results, numerical optimization,
  normal approximations, and local optimality.
- **No LLMs / ML / neural nets / agents / POMDPs.** No "policy π," no RL, no
  amortization. Terms "expected information gain," "EIG," and "mutual
  information" as such are not the paper's vocabulary — it says "expected gain in
  Shannon information" / "expected Kullback–Leibler distance." (Semantically
  identical to EIG.)
- Bayesian advantage in **linear** design is real only at **small n / informative
  prior**; with diffuse prior or large n it collapses to non-Bayesian design
  (pg-08). (For nonlinear design, prior information is always needed.)

## Section map

1. Introduction (1.1 design; 1.2 three examples; 1.3 overview of Bayesian
   approach incl. Lindley's Eqs 1–2; 1.4 structure; 1.5 notation; 1.6 related
   reviews)
2. Bayesian designs for the normal linear model (2.2 alphabetical optimality +
   Shannon-info/EIG Eqs 3–4; 2.3 related work; 2.4 other utility functions
   U₃–U₅; 2.5 unknown variance)
3. Design for analysis of variance models (incl. 3.4 hierarchical prior)
4. Nonlinear design problems (4.2 approximations to expected utility; 4.3
   Bayesian criteria; 4.4 local optimality; 4.5 comparison)
5. Optimal nonlinear Bayesian design (5.2 number of support points; 5.3 exact
   results; 5.4 software; 5.5 sequential design)
6. Specific nonlinear design problems (6.1 binary response; 6.5 clinical-trial
   sample size; 6.7 reliability/QC; 6.8 large computer experiments)
7. Nonlinear estimation within a linear model (7.2 turning-point example)
8. Other design problems (variance components; mixtures; model discrimination;
   8.4 constrained/weighted criteria; 8.5 robustness to prior; 8.6 model unknown)
9. Concluding remarks

## Two-line verdict

YES — this is the **classical review of Bayesian Experimental Design**, giving
the **normative decision-theoretic criterion = maximize expected utility** (Eqs
1–2, after Lindley 1972), with **Expected Information Gain** explicitly present as
the "expected gain in Shannon information = expected KL(posterior‖prior)" utility
(Eqs 3–4, after Lindley 1956 / Bernardo 1979 / Shannon 1948). It is
theory-focused, pre-dates all modern (MC/variational/amortized/RL) EIG machinery,
and treats EIG as the information-based special case of a broader utility menu.
