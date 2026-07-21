# R24 frozen-schema recoding

This directory is the versioned contract for the R24 automated recoding study. Historical multicoder outputs outside this directory are audit material and are not inputs.

Inputs are `manifest/source_manifest.json` and anonymous `packets/R01.json` through `packets/R14.json`. Every packet is built from a locally held primary-source PDF and pins its PDF hash. No network retrieval, earlier coding, manuscript conclusion, or citation-audit verdict is available to a trial.

Generation prompts contain neither the retired probe checklist nor its answers, and the response envelope contains no probe field. Recommendations use free-text `proposed_action`; no action-code list is disclosed. Retired probe, baseline, and recommendation-judging files are leakage canaries and audit history only; they are not generation, scoring, or inferential assets for the production run.

The production audit contains 42 fresh-session Servo codings: three vendors by fourteen frozen source records. Records R01--R05 and R14 are the six manuscript core cases; the other eight are supplementary scope and boundary cases. The source record is the analytical unit. The earlier baseline comparison and paired recommendation-judging design are retained only as audit history and are excluded from the production schedule and protocol hash.

After generation, the primary analysis is the source-grounded core case matrix and the documented disagreement audit. The supplementary records probe application scope and counterexamples. Agreement coefficients are optional descriptive summaries of this fixed convenience set, never pass criteria or estimates of general taxonomy reliability. Framework comparison is a separate qualitative crosswalk; the harness does not generate competing-framework codings or estimate comparative superiority.

Generation requires exactly 42 accepted, source-grounded Servo outputs and a matching completed protocol. Each scheduled cell receives at most two fresh-session attempts under the identical frozen prompt: one bounded retry is allowed after a transport or output-validation failure, and every attempt is retained. Any invalid or missing final artifact blocks agreement and adjudication; it is never silently imputed or repaired in place. Latency, token, retry, and failure metadata are retained for reproducibility rather than comparative utility claims.

Generation completion seals the exact 42 scheduled trial identities and every accepted-output SHA-256. Downstream agreement and editorial adjudication must read that unchanged snapshot. The harness authorizes execution integrity only; low agreement is a substantive result rather than a harness failure.

Smoke preparation is executable rather than manually asserted:

```bash
PYTHONPATH=analysis/multicoder uv run --with 'pydantic>=2.12,<3' --with 'typer>=0.21,<1' python -m r24_final.sandbox_smoke generate-static
PYTHONPATH=analysis/multicoder uv run --with 'pydantic>=2.12,<3' --with 'typer>=0.21,<1' python -m r24_final.sandbox_smoke generate-hook-negative
```

The live observer supplies typed three-cell Servo `ISOLATION_REPORT` and `FUNCTIONAL_REPORT` evidence through `register-observer-evidence`; the registrar rejects a missing vendor, reused trial roots, leakage/tool canary hits, or failed acceptance. `finalize` remains blocked until all four typed reports verify against one protocol binding.

Authoritative post-run artifacts are:

- `consensus.json`
- `core_case_matrix.csv`
- `supplementary_scope_audit.csv`
- `validator_channels.csv`
- `agreement_report.md`
- `disagreement_log.json`

The record-level matrices and agreement summaries above deliberately preserve
the frozen automated output. They union facet values within a source record and
therefore do not preserve cross-facet channel alignment. The later six-case
editorial products live at the analysis root:

- `core_servo_channels.csv`
- `core_servo_components.csv`
- `core_servo_evidence_ledger.json`
- `core_servo_disagreement_adjudication.md`

Those files are source-adjudicated case analysis, not additional model outputs
or inputs to the reported agreement coefficients.

Adjudication occurs only after all raw responses are frozen. It is editorial reconciliation, not a fourth coder or a gold standard.

`runs/r24-run-002/` and `runs/r24-run-003/` are invalidated stopped pilots. Their files are audit-only and must not be reused. A production run needs a new run ID after every gate and its adversarial smoke tests pass.

See `AUDIT_ONLY.md` for the retired experimental machinery that must remain outside the production protocol.

Run the isolated tests from `submission/`:

```sh
PYTHONPATH=analysis/multicoder uv run --with pydantic --with pytest pytest -q analysis/multicoder/r24_final/tests
```
