# Fail-closed production smoke criteria

No production run may start unless every criterion below is independently verified and bound to the current protocol hash. Model self-report is never evidence of isolation.

## Static and deterministic gates

- All 42 Servo prompts contain no retired probe ID, expected answer, action-code token, prior coder output, or adjudication.
- Every packet has unique evidence IDs; its PDF SHA-256, page count, record identity, and frozen analysis role match the source manifest and local PDF. The exact role split is six core records (`R01`--`R05`, `R14`) and eight supplementary records.
- Commands match exact provider allowlists. Duplicate, unknown, continuation, plugin, extra-directory, fallback, dangerous, or network-enabling flags fail.
- Every staged schema resolves all `$ref` values and passes Draft 2020-12 validation before invocation.
- The production post-response hook rejects wrong record/vendor, source SHA, page, quotation, evidence ID, diagnostic link, duplicate ID/rank, extra field, duplicate JSON key, NaN, fenced output, and multiple JSON documents.
- Runtime-owned provenance records executable realpath and digest, CLI version, argv digest, requested model, environment-policy digest, prompt/schema/packet digests, and protocol digest. Generated provenance is ignored.

## Task-specific isolation gates

This is a frozen-packet coding audit, not an OS-security certification. Isolation exists to prevent retired-asset leakage, reuse of prior coder outputs, and cross-trial contamination. Every invocation uses a fresh trial root and session. The harness scans the rendered prompt, stdout, stderr, and retained files for retired scoring assets, prior outputs, and cross-trial canaries. A Servo trial may not contain probe answers, action codes, author adjudications, or another trial's output.

Filesystem and tool restrictions are supporting controls. A runtime with model-accessible tools must either disable them or demonstrate that the forbidden study assets are absent and the canary attack produces no tool event or leakage. Provider authentication and configuration reads by the trusted CLI control plane are not experimental leakage and are recorded as exceptions.

## Live functional matrix

Claude, Codex, and `agy` must each pass one Servo cell in a fresh session. Functional smoke and isolation attack are separate: the functional cell requires exit code zero, exactly one unfenced JSON object, runtime-owned provenance, and exact packet evidence; the attack cell may terminate nonzero but must produce no forbidden study-asset or cross-trial leakage. Smoke start, every invocation boundary, and completion retain one protocol digest.

## Four independent reports

The smoke gate consists of exactly four reports under `smoke_reports/`.

- `STATIC_GATE_REPORT.json` covers exact 42-trial Servo scheduling, the frozen 6/8 analysis-role split, prompt non-leakage, 14 packet-to-PDF bindings, command contracts, schema, and retired-asset non-leakage.
- `HOOK_NEGATIVE_REPORT.json` covers every required malformed-output and provenance mutation against the production acceptance hook.
- `ISOLATION_REPORT.json` contains exactly three Servo vendor cells with distinct roots and zero scoring-key, prior-output, cross-trial, or forbidden-tool canary hits.
- `FUNCTIONAL_REPORT.json` covers the three Servo vendor cells, runtime provenance, and the frozen latency boundary. Functional and attack invocations remain separate.

Each report has one typed raw-evidence artifact whose schema is specific to that report. The verifier parses and recomputes the required cardinalities and identities; arbitrary text plus `result: pass` is invalid. Every evidence artifact is inside `smoke_reports/`, uses a relative non-escaping path, and is SHA-256 bound by its report. Each report is bound to the same protocol and runtime command contract.

## Decision rule

All gates are conjunctive. Missing, ambiguous, untyped, stale, or partial execution evidence is failure. No agreement coefficient or threshold is a smoke criterion; low agreement is an audit result rather than a harness failure. A failed smoke writes append-only evidence but never `SMOKE_PASSED.json`. `sandbox_smoke finalize` rereads all four reports, validates their typed observations, recomputes every raw-evidence hash and binding, and writes only report paths and hashes plus the common binding. Production independently repeats that derivation and requires byte-equivalent manifest content.
