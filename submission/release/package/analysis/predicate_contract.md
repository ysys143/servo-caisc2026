# Servo predicate and evidential-status contract

This document is the human-readable normative companion to
`servo_schema.yaml`. The validator enforces the machine-checkable portions. A
source graph is a bounded documentary reconstruction, not a complete execution
log; no missing source statement is converted into an absent real-world event.

## Policy information state

The policy input $I_t$ contains only information that the bounded source reports
as available at decision time. It may include observation history, retrieved
memory, validator outputs, or a reported controller, predictive, or recurrent
state. $M$ is the persistent storage and retrieval substrate; $I_t$ may use
retrieved content from $M$ but is not identical to $M$. Servo does not infer an
unreported latent or belief state or require a particular update function. When
the source explicitly defines a Bayesian or POMDP belief or posterior, the
interface may be specialized as $I_t=b_t$.

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
| `experimental_adaptation` | Evaluation evidence followed by feedback-dependent control of a changed experimental action | A later execution in the same bounded context; the path reaches `E` | Code repair alone; fixed schedules; selection without successor execution |
| `artifact_revision` | An evaluation occurrence followed by an `artifact_revision` edge | A successor versioned authored research artifact produced through `W_A` | Formatting, copying, an unlinked terminal assessment, or a model/memory-state update confined to `M` |
| `discovery_cycle_feedback` | Evidence event, epistemic update, an explicit `epistemic_action` event on the feedback-controlled route, new execution, and new evidence event | At least two distinct evidence occurrences with the action and execution between them | Retry-only, append-only memory, endpoint-only action inference, or a terminal-only path |

Human mediation is recorded separately as a coarse actor facet
(`mediation_actor`) on the routed edge and by the component-level authority
vector. The vector does not distinguish initiation, advice, approval, veto,
direct execution, and final authority within one component. A single mediator
endpoint records one represented locus and does not enumerate every human and
system participant in a `mixed` route. Human mediation can qualify any of the
four topological predicates and is not itself a fifth closure type.

The predicates are separately reported and are not levels of one closure scale,
but they are not necessarily logically independent. Under the current contracts,
`execution_repair` established implies `artifact_revision` established because
the repair witness subsumes the required evaluated, versioned successor route.
No unconditional implication is declared between `discovery_cycle_feedback`
and `experimental_adaptation`; an epistemic action need not satisfy the latter's
changed-experimental-action semantics.

## Component--graph integrity

Every event class has an allowed actor component, and every structural edge type
has allowed source--destination component pairs. The validator rejects, for
example, an execution event attributed to `V`, an observation routed from `E`
to `G`, or external human feedback labelled as system mediation. These are
endpoint-level admissibility constraints. They do not type edge payloads, prove
direct composition of the component function signatures, or make the
uninstantiated environment or measurement process graph-identifiable.

The graph edges record source-reported dependency or control, not a typed call
graph. In particular, `V-to-G` and `pi-to-G` mean that evaluation or policy
context conditions a later generation occurrence; they do not add formal
arguments to the schematic signature of `G`. `G-to-E` records delivery of a
generated candidate into a source-reported execution route after the bounded
selection context; it does not grant `G` the action-selection authority assigned
to `pi`. Servo does not currently validate payload-level function composition.

`event_class` determines actor admissibility, whereas `event_kind` records a
predicate-relevant semantic role. Thus `epistemic_action` is an event kind, not
an additional event class; its occurrence must still carry an admissible class
such as `generation`, `runtime_validation`, or `state_update`.

The current graph is an operational documentary projection, not a causal
decomposition of observation generation. Its `observation` edge from `E` to `V`
does not denote causal observation generation; it records that evidence
associated with a documented execution became available to a validator.
`producer_event_id` for a result or measurement artifact is likewise a
documentary availability anchor within the bounded trace, not necessarily the
ultimate physical, environmental, simulator, or measurement producer. The
current contract does not instantiate `O_env`, simulator response, or
measurement apparatus as graph endpoints and cannot localize failure among
those omitted processes.

A path may establish more than one predicate only when it independently
satisfies every predicate-specific pattern. Sharing event or edge identifiers is
not itself evidence of inclusion between predicates.

## Status decision table

| Status | Required `decision_basis` | Decision rule |
|---|---|---|
| `established` | `positive_witness` | At least one fully conforming, source-grounded witness exists. |
| `not_established` | `explicit_negative` | The bounded source explicitly states that the required route is absent, external-only, terminated, or otherwise fails the predicate. |
| `unknown` | `insufficient_reporting` | A required event, edge, order, artifact identity, or source link is missing or ambiguous. Source silence is classified here. |
| `not_applicable` | `out_of_scope` | The predicate is excluded by the predeclared case boundary, with a reason. |

## Alignment and mismatch handling

- Explicit source ordering is used when available. Structurally inferred order
  must be marked in the evidence status and cannot repair a missing semantic
  edge or manufacture a required successor occurrence. The later execution
  required by experimental adaptation, and the successor execution and evidence
  required by discovery-cycle feedback, must each have a directly stated event
  anchor in the bounded source.
- Alternative paths are evaluated independently. One conforming path is enough
  for `established`; a nonconforming path does not cancel it.
- Missing events, ambiguous ordering, ambiguous artifact identity, and source
  silence yield `unknown`.
- Only explicit source-grounded contrary evidence may yield `not_established`;
  an incomplete trace or an unverified claim of trace completeness yields `unknown`.
- Any contract change after holdout coding makes that case formative and
  requires a new untouched holdout.
