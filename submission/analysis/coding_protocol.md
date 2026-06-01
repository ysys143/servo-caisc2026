# SERVO Cross-System Coding Protocol

This protocol operationalizes the component extraction behind Tables 1-2 so the
V-completeness pattern is auditable. It addresses the reproducibility critique
(no rubric / no inter-coder reliability / convenience sample) raised in review.

## Inclusion / exclusion criteria

**Include** a system if it automates at least one full hypothesis -> experiment
-> validation cycle (a generation step G, an execution step E, and a validation
step V that produces a signal used by the system).

**Exclude** specialized predictors with no generation-and-search loop
(e.g., AlphaFold), pure benchmarks, and tool libraries without an internal loop.

**Search log.** Candidate systems were drawn from (a) the AI Scientist survey
literature (Tie et al. 2025), (b) the venues NeurIPS/ICLR/Nature 2023-2026, and
(c) backward/forward citation from the four core systems. This is a convenience
sample of widely-cited representatives, not an exhaustive enumeration; the
selection bias this introduces is stated in the paper's Limitations.

## Operational rubric (each cell answerable from an explicit source quote)

For every system we record, for each of S, G, E, M, pi, a short label plus a
direct source quote and citation. The decisive constructs are coded as discrete
indicators so two coders can agree or disagree unambiguously:

### V layers (binary presence; each requires a source quote)
- `V_syntax`  {0,1}: a deterministic automated pass/fail check exists.
- `V_semantic`{0,1}: an LLM/rubric-based score of outputs is used.
- `V_empirical`{0,1}: measured experimental/benchmark outcomes feed the loop.
- `V_human`   {0,1}: human judgment is required for the validity/novelty signal.
- `V_calibrated`{0,1}: the highest automated layer present is reliably calibrated
  (e.g., DFT, formal kernel) rather than systematically biased (e.g., LLM judge).

### V_completeness (ordinal 0--3, holistic judgment --- NOT mechanically derived)
A 0--3 ordinal summarizing how much of the validity burden is carried by reliable
automated layers: 0 = V_human only (no automated validity layer); 1 = one reliable
automated layer; 2 = two reliable automated layers; 3 = three automated layers AND
the top automated layer is calibrated. This ordinal is an interpreted summary, NOT
a deterministic function of the binary indicators above. Two coders may legitimately
differ on (i) whether V_human counts toward the layer total, and (ii) whether an
accessible-but-biased layer (e.g., an LLM judge) is discounted ("accessibility
without calibration does not count"). Under the strict automated-layer reading,
4 of 12 coded ordinals reflect these two latitudes (Coder A counts V_human for
Robot Scientist and AI Scientist Nature 2026; Coder B discounts biased/auxiliary
layers for Coscientist and Agent Laboratory). This is why V_completeness shows the
lowest inter-coder agreement of any field (Cohen's kappa = 0.14; see
reliability_report.md), while the calibration sub-construct it depends on is coded
identically (kappa = 1.0). The paper therefore rests its claim on the robust
calibration construct, not on this noisy ordinal.

### loop_status (3-boundary, resolves the Coscientist ambiguity)
- `L_task` {0,1}: results inform later choices within a predefined task.
- `L_measurement` {0,1}: the measurement->analysis step is automated (not human).
- `L_discovery` {0,1}: an autonomous hypothesis->experiment->new-hypothesis cycle
  exists that certifies new knowledge (novelty).
Label (as recorded in systems.csv): none / partial-task / partial-analysis / closed-comp / closed-wetlab,
derived from which boundaries are crossed.

### H (human intervention, continuous in [0,1])
Approximate fraction of the loop's decision burden a human carries, judged from which
of G / pi / V_human a human performs. Reported on a continuous [0,1] scale (values
such as 0.1 or 0.8 denote "almost none" / "almost all" of that burden); the quartile
points {0,.25,.5,.75,1} are reference anchors, not the only allowed values.

## Double coding and reliability
- Coder A: the manuscript authors (labels in `systems.csv`, columns `A_*`),
  re-verified against the cited primary source.
- Coder B: an independent pass given ONLY this protocol and the primary-source
  description, blind to Coder A's labels (columns `B_*`).
- Agreement: Cohen's kappa per categorical field, reported in
  `reliability_report.md`. Because Coder B is an LLM pass on structural
  indicators (not a human rater), kappa is reported as a transparency measure,
  not as a claim of human-level inter-rater reliability.
- Disagreements are adjudicated against the source quote; the adjudicated value
  is the published one.

## Counterexample search
We explicitly seek systems that (a) are V-incomplete yet loop-closed, or
(b) V-complete yet loop-open. A confirmed case of (a) would refute the claim
that V-completeness is necessary for closure. Result reported in
`reliability_report.md`.

## Regeneration
`build_servo_tables.py` regenerates Tables 1-2 (TeX) from `systems.csv` and fails
if any cell lacks a source quote or any cited source key is absent.
