# Mechanical and trustworthy closure: historical audit only

This artifact reconstructs an abandoned descriptive analysis. It must not be
read as evidence for the direction of an association between validator design
and trustworthy closure.

The historical exercise joined `A_Vcalibrated` from `systems.csv` to an
author-coded `trustworthy_closure.csv`. The join does not supply an independent
outcome: peer review and publication overlap human validation, outcome labels
were visible during later predictor corrections, the six systems were selected
by convenience, and only four were mechanically closed. The predictor also
pooled layer presence, gate identity, reliability, and calibration into a binary
field that the current faceted taxonomy has withdrawn.

Accordingly:

- the contingency is retained only for reconstruction;
- optimistic or pessimistic recoding cannot rescue an association test;
- no confidence interval, p-value, direction claim, or counterexample count is
  substantively interpretable; and
- `association_descriptive.py` now reports provenance and the non-testable status
  instead of calculating a directional contingency.

Mechanical closure remains separately descriptive: implemented observations or
validator signals must alter a later memory state, candidate, policy action, or
stage. Terminal assessment, publication, and external review do not themselves
establish that path.

The final R24 recoding reports validator channel facets and feedback paths. It
does not reuse `A_Vcalibrated` or `trustworthy_closure` as predictor and outcome,
and it does not test their association.
