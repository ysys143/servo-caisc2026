# SERVO Cross-System Coding Protocol

This protocol operationalizes the component extraction behind the cross-system
tables so the V-completeness pattern is auditable. It addresses the
reproducibility critique (no rubric / no inter-coder reliability / convenience
sample) raised in review.

## Inclusion / exclusion criteria

**Include** a system if it automates at least one full hypothesis -> experiment
-> validation cycle (a generation step G, an execution step E, and a validation
step V that produces a signal used by the system).

**Exclude** specialized predictors with no generation-and-search loop
(e.g., AlphaFold), pure benchmarks, and tool libraries without an internal loop.

**Search log.** Candidate systems were drawn from (a) the AI Scientist survey
literature, (b) the venues NeurIPS/ICLR/Nature 2023-2026, and (c) backward/
forward citation from the core systems. This is a convenience sample of
widely-cited representatives, not an exhaustive enumeration; the selection bias
this introduces is stated in the paper's Limitations. The candidate universe and
the include/exclude decision per system are recorded in
`multicoder/target_systems.md`.

## Operational rubric (each cell answerable from an explicit source quote)

For every system we record, for each of S, G, E, V, M, pi, a short label, and we
attach at least one direct source quote with a citation as the evidentiary
anchor. (The released `systems.csv` carries one representative source quote per
system for the existence/citation check enforced by `build_servo_tables.py`; the
per-component values are the coded fields, not one quote per component.) The
decisive constructs are coded as discrete indicators so coders can agree or
disagree unambiguously:

### V layers (binary presence; each requires a source quote)
- `V_syntax`  {0,1}: a deterministic automated pass/fail check exists.
- `V_semantic`{0,1}: an LLM/rubric-based score of outputs is used.
- `V_empirical`{0,1}: measured experimental/benchmark outcomes feed the loop.
- `V_human`   {0,1}: human judgment is required for the validity/novelty signal.
- `V_calibrated`{0,1}: the highest automated layer present is reliably calibrated
  (e.g., DFT, formal kernel) rather than systematically biased (e.g., LLM judge).

Three further columns were added to `systems.csv` after the first coding pass, when the
single `V_calibrated` flag proved to conflate two questions. They were defined in
`multicoder/rubric_calib.txt` for the recoding round and are restated here, because the
paper's central claim rests on the second of them:

- `V_present`  {0,1}: a calibrated automated layer exists anywhere in the system.
- `V_gating`   {0,1}: the layer that *decides acceptance* is itself calibrated. This is a
  property of calibration, not of who performs the gating; a biased automated reviewer and
  a social review process both yield 0.
- `novelty_gate` {`none`|`human`|`predefined`|`biased_auto`|`calibrated_auto`}: what, if
  anything, gates on novelty.

Note also that this protocol describes two things the released sheets do not carry as
columns. The per-component S/G/E/V/M/pi labels of §"Unit of coding" are given in the
manuscript's comparison table rather than in `systems.csv`, and the three loop boundaries
`L_task`/`L_measurement`/`L_discovery` are collapsed into the single `A_loop_status`
field. Anyone reconciling this document against the CSV should expect those two gaps.

### V_completeness (ordinal 0-3, holistic judgment --- NOT mechanically derived)
A 0-3 ordinal summarizing how much of the validity burden is carried by reliable
automated layers: 0 = V_human only; 1 = one reliable automated layer; 2 = two;
3 = three automated layers AND the top automated layer is calibrated. This
ordinal is an interpreted summary, NOT a deterministic function of the binary
indicators above: coders may legitimately differ on whether V_human counts
toward the total and whether an accessible-but-biased layer (e.g., an LLM judge)
is discounted. It is therefore the lowest-agreement field; the paper rests its
claim on the calibration sub-construct, not on this ordinal.

### loop_status (3-boundary, resolves the Coscientist ambiguity)
- `L_task` {0,1}: results inform later choices within a predefined task.
- `L_measurement` {0,1}: the measurement->analysis step is automated (not human).
- `L_discovery` {0,1}: an autonomous hypothesis->experiment->new-hypothesis cycle
  exists that certifies new knowledge (novelty).
Label (as recorded in systems.csv): none / partial-task / partial-analysis /
closed-comp / closed-wetlab, derived from which boundaries are crossed.

### H (human intervention, continuous in [0,1])
Approximate fraction of the loop's decision burden a human carries, judged from
which of G / pi / V_human a human performs. Reported on a continuous [0,1] scale
(values such as 0.1 or 0.8 denote "almost none" / "almost all" of that burden);
the quartile points {0,.25,.5,.75,1} are reference anchors, not the only allowed
values.

## Multi-coder reliability
- **Coder A (reference):** the manuscript authors (labels in `systems.csv`,
  columns `A_*`), re-verified against the cited primary source.
- **Independent coders:** three model-pinned, blind LLM-based coder agents from
  different vendors -- Claude Code (`claude-opus-4-8`, Anthropic), Codex CLI
  (`gpt-5.5`, OpenAI), and Antigravity `agy` (Gemini 3.1 Pro High, Google) --
  each given ONLY this protocol and the neutral source descriptions in
  `multicoder/systems_desc.json`, blind to the author's labels and to one
  another (but NOT blind to system identity -- the systems are widely known and
  may be memorized, which the paper states as a limitation). Per-coder outputs
  are in `multicoder/codings.csv` and
  `multicoder/raters/`.
- **Agreement:** Fleiss' kappa across the three coders plus pairwise Cohen's
  kappa, per categorical field, reported in `reliability_report.md`. Because the
  coders are LLMs scoring structural indicators (not human raters), kappa is a
  transparency measure, not a claim of human-level inter-rater reliability.
- The published per-system labels remain Coder A (`systems.csv`); the
  multi-coder matrix (`multicoder/codings.csv`) is the reliability evidence.

## Counterexample search
We explicitly seek systems that (a) are V-incomplete yet loop-closed, or
(b) V-complete yet loop-open. A confirmed case of (a) would refute the claim that
V-completeness is necessary for closure. Result reported in
`reliability_report.md`.

## Regeneration
`build_servo_tables.py` regenerates the core table (TeX) from `systems.csv` and
fails if any cell lacks a source quote or any cited source key is absent.
`multicoder/run_coders.py` re-runs the blind multi-vendor coding and
`multicoder/compute_fleiss.py` recomputes the reliability statistics.
