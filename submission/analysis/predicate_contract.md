# Servo predicate and evidential-status contract

This document is the human-readable normative companion to
`servo_schema.yaml`. The validator enforces the machine-checkable portions. A
source graph is a bounded documentary reconstruction, not a complete execution
log; no missing source statement is converted into an absent real-world event.

## Common witness requirements

Every established witness stays within one case, version, configuration, and
task regime. Its event occurrences, connected endpoint path, and edges are
ordered. Every edge is implemented, feedback-dependent, closure-eligible, and
source-grounded. A terminal assessment, fixed schedule, pre-action filter,
formatting/copying step, or append-only memory update cannot establish a
predicate by itself.

| Predicate | Start and required route | Required destination or recurrence | Exclusions |
|---|---|---|---|
| `execution_repair` | Runtime-validation evidence followed by an `artifact_revision` edge and a `feedback_control` edge through `W_A` | A later execution occurrence in the same bounded context | A retry without a changed executable/protocol artifact; terminal review |
| `experimental_adaptation` | Execution/evaluation evidence followed by `epistemic_update` and `feedback_control` | A later evidence-generating execution; the path contains `E` | Code repair alone; fixed schedules; selection without successor execution |
| `artifact_revision` | An evaluation occurrence followed by an `artifact_revision` edge | A successor versioned artifact through `W_A` | Formatting, copying, or an unlinked terminal assessment |
| `discovery_cycle_feedback` | Evidence event, epistemic update, feedback-dependent epistemic action, new execution, and new evidence event | At least two distinct evidence occurrences with an intervening execution | Retry-only, append-only memory, human-mediated edge counted as automated, or a terminal-only path |
| `human_mediated_feedback` | Human-feedback event followed by a `human_mediation` edge | A routed destination inside the bounded workflow | Initial task specification or external terminal review without a return edge |

A path may establish more than one predicate only when it independently
satisfies every predicate-specific pattern. Sharing event or edge identifiers is
not itself evidence of inclusion between predicates.

## Status decision table

| Status | Required `decision_basis` | Decision rule |
|---|---|---|
| `established` | `positive_witness` | At least one fully conforming, source-grounded witness exists. |
| `not_established` | `explicit_negative` or `complete_trace_failure` | The bounded source explicitly places the route outside the case, or a fully reported eligible trace violates a required transition. |
| `unknown` | `insufficient_reporting` | A required event, edge, order, artifact identity, or source link is missing or ambiguous. Source silence is classified here. |
| `not_applicable` | `out_of_scope` | The predicate is excluded by the predeclared case boundary, with a reason. |

## Alignment and mismatch handling

- Explicit source ordering is used when available. Structurally inferred order
  must be marked in the evidence status and cannot repair a missing semantic
  edge.
- Alternative paths are evaluated independently. One conforming path is enough
  for `established`; a nonconforming path does not cancel it.
- Missing events, ambiguous ordering, ambiguous artifact identity, and source
  silence yield `unknown`.
- An explicitly external-only route or a complete trace missing a required
  transition may yield `not_established`.
- Any contract change after holdout coding makes that case formative and
  requires a new untouched holdout.
