# SERVO coding audit report

## Current schema and two historical audits

The current normative contract is Servo Schema 3, defined in
`servo_schema.yaml`. Its case, endpoint, artifact, event, edge, reliability,
closure-witness, closure-status, domain-anchor, and selection-ledger records are
author-interpreted source annotations, not a new independent coding study.
`python -m analysis.validate_servo2` checks their structural and provenance
contracts and generates the bilingual projections. Its PASS does not establish
semantic entailment or construct validity. Schema 1 and its
`validate_servo_consistency.py` entry point are retained only as historical,
non-authoritative migration material.

The repository contains historical agreement results and the R24 frozen-schema
audit. They use different constructs and must not be combined.

### Historical audit

Three vendor LLMs coded an earlier 14-record rubric; 13 records had all three
usable outputs. The historical Fleiss statistics were `Vsemantic` 1.00,
`Vcalibrated` 0.79, loop status 0.74, `Vsyntax` 0.69, `Vhuman` 0.59,
`Vempirical` 0.54, and `Vcompleteness` 0.39. A later two-vendor recode reported
raw agreement and Cohen's kappa for `V_present`, `V_gating`, and
`novelty_gate`.

These figures are audit history only. Their source descriptions predate the
citation audit; several reference labels and rules changed after outputs were
visible; the holistic ordinal and scalar human-intervention field were later
withdrawn; and the present/gating binary pooled heterogeneous states. The
figures therefore do not validate the final facets, current Table 1, contextual
validator interface, component-wise human authority, or channel-specific
feedback paths. They also do not establish source entailment, construct
validity, human reliability, diagnostic utility, or statistical calibration.

The historical scripts are preserved to reconstruct those numbers. A
constant-category chance-adjusted coefficient must be reported as undefined,
not as perfect agreement.

## R24 frozen development audit

R24 creates a separate versioned dataset rather than overwriting the historical
outputs. It codes 14 source-defined records from 13 lineages with the record-level
facets frozen at that stage. Trigger phase, routed channel alignment, search-space
expansion, fidelity choice, cost, budget, and `H_S` were added or made substantive
after those outputs were frozen and were not independently recoded. Six records are
the core cases used for the manuscript's substantive comparison: Coscientist,
AI Scientist 2024, AI Scientist Nature 2026, Agent Laboratory, Robot Scientist,
and NovelSeek. The other eight are supplementary applications for inspecting
scope, boundary cases, and possible counterexamples. These roles are frozen in
the source manifest before generation.

Claude, Codex, and Gemini each received the same local-PDF evidence packets in
fresh stateless sessions, yielding 42 accepted Servo codings. Models, packets, prompts,
ordering, hashes, errors, and exact retries are recorded. No web source,
historical label, manuscript text, other coder output, or human coder is exposed
during annotation. Author adjudication occurs only after raw outputs are frozen
and is not counted as a coder.

The stopped free-form baseline, probe-recall comparison, and automated
recommendation-judging designs remain audit history only. They are not R24
generation, scoring, or inferential assets.

## Descriptive agreement

The frozen automated outputs are the six-case record-level matrix, the eight-record
supplementary scope audit, and the disagreement log. Facet-wise mean pairwise
Jaccard values range from 0.567 to 0.706; MASI-based Krippendorff alpha values
range from 0.165 to 0.338. The audit retains 90 record-facet disagreements
from the frozen model outputs. These figures compare the union of tokens used
within each facet for a record; they do not align validator channels and cannot
show whether a target, evidence source, evaluator, decision role, and feedback
path describe the same mechanism. A coefficient is omitted when validator
channels cannot be aligned without editorial judgment or when sparse category
use makes the summary misleading. Constant categories have undefined kappa,
reported as `NA`. Coefficients from heterogeneous facets are not pooled into one reliability score.

For substantive interpretation of the six cases, the author subsequently
adjudicated channel boundaries against the frozen local-source packets. A
channel is split for a distinct evaluator, target, decision role, or downstream
destination and merged only when the same reported mechanism supplies those
roles. `None identified` means that the bounded packet reports no separate
terminal or external channel, not that one is known to be absent. That
development-era result is preserved in `servo_validator_channels.csv`;
`core_servo_channels.csv` is its generated compatibility projection. Neither is
a current semantic input. The current representation is the set of Schema 3
case, endpoint, artifact, event, edge, reliability, and predicate-witness
records named in `servo_schema.yaml`. `core_servo_evidence_ledger.json` resolves
every cited evidence ID to an exact quote, page, and PDF hash, and
`core_servo_disagreement_adjudication.md` records the principal historical
editorial resolutions. This is author-interpreted source-grounded case analysis,
not a fourth coder, a gold standard, a channel-level reproducibility study, or a
post-hoc improvement to the agreement coefficients.

The 42 model calls and individual facets are not independent scientific systems.
The sample is a fixed convenience set, not a probability sample, so agreement
coefficients are not population reliability estimates. No coefficient,
confidence interval, p-value, or arbitrary threshold determines protocol success
or validates the taxonomy.

## Interpretation

R24 can document how automated readers applied the then-frozen record-level facet labels under fixed inputs.
The later channel adjudication can illustrate how the Servo vocabulary separates validator targets,
operational roles, feedback paths, evidence, and system boundaries in the cited
cases. It can also expose where automated readers disagree under fixed inputs.
It cannot show that the taxonomy is correct, generally reliable, superior to
other frameworks, useful in real system design, representative of the field, or
predictive of independently measured scientific outcomes. Cross-framework comparison remains a separate
qualitative crosswalk using each framework's native definitions.

The cross-domain table remains outside this coding audit. No reported
agreement result may be transferred to its single-coder domain labels or used to
claim a gate--outcome relationship.
