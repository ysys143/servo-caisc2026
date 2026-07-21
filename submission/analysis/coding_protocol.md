# SERVO cross-system coding protocol

## Status and unit of analysis

This document preserves the Servo Schema 1 author coding protocol and the frozen
multicoder audit performed against it. Schema 1's
`servo_core_systems.csv` and `servo_validator_channels.csv` are historical,
non-authoritative migration material; they are not current substantive inputs.
The current normative contract is Servo Schema 3 in `servo_schema.yaml`, whose
case, endpoint, artifact, event, edge, reliability, closure-witness,
closure-status, domain-anchor, and selection-ledger records are validated and
projected by `python -m analysis.validate_servo2`. The frozen artifacts under
`multicoder/r24_final/` preserve the instructions actually shown to the three
vendors and are a development audit, not an independent recoding of the current
event--evidence contract. Schema 3 supersedes the historical layer,
scalar-human-intervention, `V_present`, `V_gating`, and `V_completeness` rubrics
for substantive analysis. Those columns remain in `systems.csv` only to
reconstruct earlier revisions and must not be used to rank systems.

The Schema 1 unit was a source-defined system version plus a validator channel. The
14 records comprise 13 lineages because AI Scientist-v2 and the Nature 2026 AI
Scientist describe the same agentic-tree method family at different publication
stages. AI Scientist 2024 and Nature 2026 remain separate system versions. The
Nature record covers only its template-free agentic-tree configuration.

The sample is a convenience sample, not an estimate of the population of AI
Scientist systems. Domain Table 2 is a separate single-coder illustration and is
not part of the R24 recoding.

The manuscript's substantive comparison uses six core records: Coscientist,
AI Scientist 2024, AI Scientist Nature 2026, Agent Laboratory, Robot Scientist,
and NovelSeek. The remaining eight records are supplementary applications for
scope, boundary-case, and counterexample inspection. This role split is frozen
in the R24 source manifest before generation.

## Frozen source inputs

Each coder receives a fresh, identity-minimized source packet built only from the
local primary-source PDFs. A packet contains a record identifier, PDF hash, page
anchors, paragraph identifiers, and source text. It does not contain the
manuscript, historical coder output, author labels, citation-audit verdicts, or
other coders' results. No web retrieval is allowed during coding.

The manual, JSON schema, packet manifest, prompts, model identifiers, run order,
and statistical plan are hashed before the first run. A substantive change after
coding begins creates a new protocol version and requires a complete rerun; cells
are never selectively rerun.

## Historical Schema 1 channel synthesis

For each implemented, proposed, external, unreported, or unclear validator
channel, the development-era author synthesis recorded:

- `trigger_phase`: pre-action, in-execution, post-observation, terminal, or
  external; this locates the validation event rather than assuming one
  post-observation call;
- `target_property`: executability, specification compliance, task performance,
  correctness or formal validity, empirical adequacy, reproducibility, novelty,
  significance, or aggregate quality;
- `evidence_source`: execution trace, benchmark metric, statistical test,
  physical measurement, replication, prior-art corpus, artifact review, or human
  judgment;
- `evaluator_substrate`: deterministic program, statistical model, formal
  kernel, LLM, human, or hybrid;
- `decision_role`: diagnostic, ranking, search control, stage transition, memory
  admission, terminal assessment, final acceptance, or external assessment;
- `feedback_path`: terminal only, memory update, candidate revision, policy
  control, stage transition, external only, or unclear;
- `external_independence`: internal self-evaluation, internal separate component,
  external non-independent, external independent, or not reported;
- `reliability_evidence_type`: none reported, discrimination study, agreement
  study, systematic-error or bias test, property-specific external validation,
  or probabilistic calibration analysis;
- `reliability_finding`: not evaluated, not established, evidence of error or
  bias, positive property-specific evidence, mixed, or unclear; and
- `experimental_fidelity`: simulation or proxy, computational experiment,
  computational oracle or benchmark, robotic experiment, physical assay, not
  applicable, or not reported.

Multiple values may apply within a facet. `not_reported`, explicit absence,
`unclear`, and `not_applicable` are distinct. Every value carries the PDF record,
page, paragraph identifier, exact source excerpt, and rationale.

System-level fields record policy type, memory structure, search-space expansion,
fidelity choice, cost or budget state when reported, and component-specific human
authority over `S`, `G`, `E`, `V`, `M`, and `pi`. `H_S` distinguishes authority
over the initial problem or represented search space from candidate generation. Human authority is categorical, not a
percentage. Computational closure is derived from an implemented feedback edge
that changes later memory, candidates, represented search space, policy, or
stage. A channel routed only to terminal or external assessment does not close
the loop; an evaluation occurring after manuscript generation can qualify only
when the source reports an explicit route back to a later stage or component.

## AI Scientist channel boundary

AI Scientist 2024 contains three distinct channels: a literature-similarity
filter that can discard ideas during ideation; execution status and metrics that
can trigger bounded revision and replanning; and a terminal simulated paper
reviewer. The reviewer error study does not establish bias in the ideation filter.

In the Nature 2026 paper, the common idea-generation phase connects to Semantic
Scholar and can discard ideas that closely resemble existing work. The
template-free prompts also use literature-grounded reflection and refinement.
The Schema 1 record therefore coded one pre-action prior-art gate and kept it
separate from the later metrics, training dynamics, plot checks, and stage evaluators that
control tree expansion and stage transitions. Its paper reviewer is terminal.
Workshop review is external to the computational loop after manual submission
selection. False-positive-rate results are reviewer-error evidence, not
probabilistic calibration and not a head-to-head comparison with the separately
sampled human-review figure.

## Servo recoding

Claude, Codex, and Gemini each coded all 14 packets in isolated stateless sessions
using the then-frozen R24 record-level facet schema, with fresh processes and a
fixed randomized record order. They did not code post-R24 trigger phase, routed
channel alignment, search-space expansion, fidelity choice, cost, budget, or
`H_S`. The stopped paired free-form baseline design is retained only as audit
history and is not part of the R24 production protocol.

Transport or strict output-validation failure permits one identical fresh-session
retry; both attempts remain in the run ledger. Model substitution is prohibited. Author adjudication begins only after
all raw outputs are frozen and is excluded from inter-coder agreement.

## Interpretation boundary

The frozen model run supplies record-level facet proposals, a supplementary
scope audit, and explicit disagreement diagnostics. Because a record-level
union does not preserve which facet values belong to the same validator
channel, it is not the current substantive representation. After all responses were frozen,
the six core cases were author-interpreted and editorially reconciled against the source packets in
`servo_validator_channels.csv`, with complete evidence provenance in
`core_servo_evidence_ledger.json` and resolutions in
`core_servo_disagreement_adjudication.md`. These Schema 1 artifacts are now
historical and non-authoritative; the current Schema 3 records are named in
`servo_schema.yaml`. This author adjudication is disclosed
as source-grounded case analysis rather than treated as a coder or reference
standard. A channel is split when the source reports a distinct trigger phase,
evaluator, target, decision role, or downstream destination. Channels are merged only
when one reported mechanism supplies those roles. `None identified` means that
the bounded evidence packet reports no separate terminal or external channel;
it is not evidence of ontological absence. Trigger phase and destination are
retained together so a pre-action novelty filter, an in-execution evaluator,
and a terminal reviewer cannot collapse into one vector reward. These rules have not been tested in
an independent channel-level reproducibility study. Agreement
statistics, when defined, are descriptive summaries for the fixed 14-record
convenience set. They are not success thresholds and do not establish source
entailment, population reliability, construct validity, human reliability,
probabilistic calibration, prevalence, or diagnostic superiority. The former
gate-reliability/``trustworthy closure'' association is withdrawn as
definitionally entangled rather than retained as an untested hypothesis.
