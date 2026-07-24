# SERVO v5 supplementary analysis package

This directory is the supplementary material for the SERVO analysis of six
AI-scientist systems (C01-C06). It accompanies the manuscript's post-submission
revision and contains the source-first v5 pipeline: machine-readable
per-case records, the tables generated from them, and the tests that check
the pipeline's internal and external consistency.

## What SERVO v5 does

Each case is coded through four ordered, non-collapsing layers:

1. **`source_proposition`** — sentences extracted verbatim from the source
   PDF, with an exact quote, page locator, and grammatical modality
   (`directly_reported` / `reported_as_procedure` /
   `reported_only_as_capability`). No judgment, no inference — only what the
   source states.
2. **`author_alignment`** — each proposition mapped onto the Servo schema's
   component/relation vocabulary, still without asserting an occurrence
   verdict.
3. **`derived_claim`** — the decision-semantic claims (e.g. component
   presence, relation occurrence) that the aligned propositions support,
   together with their evidence basis.
4. **`policy`** — case-level policy classification (control dependence,
   selection signal/objective, generation scope, execution rule), coded by
   the author directly from the source material with a written rationale.
   Unlike layers 1-3 below, this is not a machine-validated derivation from
   the claims layer -- see the note that follows.

Layers 1-3 form a validated downward chain: each `author_alignment` record
references the `source_proposition` it maps, and each `derived_claim`
references the `author_alignment` records that support it; the schema
validator checks that these references resolve and that no field asserts
more than the layer before it licenses (no judgment leaks upstream into the
source layer). The **`policy` layer does not carry this kind of validated
reference** -- its schema has no claim/alignment/proposition pointer field,
and the validator checks only that its enum values are well-formed and
non-empty (see `servo_v5_schema.yaml`). Policy is grounded in the source via
the author's rationale, but that rationale is not machine-checked against
the claims layer; read it as informed judgment, not a validated function of
the claims below it. This ordering -- verbatim source before interpretation,
wherever validation is possible -- is SERVO v5's answer to the churn problem
of earlier schema versions (see `servo_v5_charter.md`).

## Status of the judgments in this package

The `author_alignment`, `derived_claim`, and `policy` records are all
marked `status: draft` in their files, and the schema validator does
**not** gate on that value -- a `draft` record passes the same checks a
`frozen` or `pilot` one would (only `source_proposition.status` has a
meaningful `draft`/`pilot`/`frozen` progression enforced elsewhere in the
pipeline; see `servo_v5_source_freeze_manifest.json`). Concretely, this
means the interpretive judgments in this package have **not** yet gone
through the verification conditions the project's own charter sets for
them (`servo_v5_charter.md`): an independent blind-human second review of
boundary cases, a third adversarial verification pass, and the FunSearch
deterministic-replay worked case. Those remain future work. Treat the
alignment/claim/policy judgments released here as formative -- they may
change -- and do not read "the tests pass" as "the judgments are final."

## Directory layout

| Path | Contents |
|---|---|
| `servo_v5_source_propositions/C0N.json` | Layer 1: per-case verbatim propositions, quotes, locators, modality. `source_pdf_name` / `source_pdf_sha256` record which PDF each case is bound to. |
| `servo_v5_alignments/C0N.json` | Layer 2: per-case alignment of propositions to Servo schema components/relations. |
| `servo_v5_claims/C0N.json` | Layer 3: per-case derived decision-semantic claims and their evidence basis. |
| `servo_v5_policy/C0N.json` | Layer 4: per-case policy classification (control dependence, selection signal, generation scope, execution rule). |
| `tbl-servo-v5-*.tex` | LaTeX tables generated from the four layers above (e.g. `tbl-servo-v5-policy.tex`, `tbl-servo-v5-relations.tex`, `tbl-servo-v5-boundary.tex`), consumed by the manuscript build. |
| `tests/servo_v5/` | Structural and (where the corpus is present) source-fidelity tests over the four layers — see below. |
| `servo_v5_charter.md` | The frozen rules the v5 reconstruction follows. |
| `servo_v5_schema.yaml`, `servo_v5_source_proposition_schema.md` | Schema definitions for the objects above. |
| `servo_v5_source_freeze_manifest.json` | Authoritative freeze record: per-case `source_pdf_sha256`, proposition IDs/count, coverage status. Any change to a bound hash invalidates all downstream v5 artifacts (alignment, claim, policy). |
| `servo_v5_coverage_audit.md` | Per-case audit of which document pages/ranges were read and why (selection-bias review). |
| `servo_v5_corpus_manifest.md` / `.json` | How to acquire and verify the six source PDFs — see [Corpus](#corpus) below. |

Older `servo2_*` / `servo_*` (non-`v5`) files in this directory are prior
schema generations (v3/v4.1), retained for provenance; they are not part of
the v5 pipeline described here.

## Running the structural tests

From the `submission/` root:

```sh
uv run --extra test --with pyyaml --with pydantic python -m pytest analysis/tests/servo_v5 -q
```

or, if a local virtual environment is already set up:

```sh
.venv/bin/python -m pytest analysis/tests/servo_v5 -q
```

Both scope to the v5 test package. As observed on 2026-07-24: with the
corpus present and resolvable (see [Corpus](#corpus) below), this reports
**119 passed, 0 skipped**; without a resolvable corpus it reports **116
passed, 3 skipped**. These counts are corpus- and version-sensitive -- the
underlying `C0N.json` records are still under revision -- so treat them as
an observed snapshot, not a pinned contract, and check the pass/skip split
yourself rather than assuming a specific total.

Running the unscoped `python -m pytest -q` (the `testpaths` configured in
`pyproject.toml` also pull in `analysis/citation_audit/tests`) additionally
exercises unrelated suites elsewhere under `analysis/tests/` (older schema
generations); those require `pyyaml` and `pydantic`, which the v5 test
package itself does not import. Scope to `analysis/tests/servo_v5` if you
only want the v5 checks and want to avoid those extra dependencies.

The repository's `Makefile` automates the full build (`make revision`), but
it hardcodes an author-specific environment: a `.venv/bin/python`
interpreter, a fixed TeX Live install path
(`/usr/local/texlive/2026basic/...`), and a default corpus `SOURCE_ROOT`
under one author's home directory. It is not a portable build for an
arbitrary machine -- use the `uv run` / `.venv` commands above directly, or
pass `SOURCE_ROOT=/path/to/ai_scientist` to `make verify`, and expect to
adjust the TeX paths for your own toolchain.

## Provenance chain

`servo_v5_provenance_root.json` binds the whole v5 lineage into one chain --
the corpus set, the source propositions, the alignment/claim/policy records,
the generated tables, the manuscript's input-table hashes and PDF, and the
supplement contents. It references and cross-checks the two existing
manifests (`servo_v5_source_freeze_manifest.json` for the source layer and
`servo_v5_evidence_manifest.json` for the tables layer) rather than
duplicating them. Verify the internal chain (fail-closed on any upstream
change):

```sh
python -m analysis.servo_v5_provenance --verify
```

The root manifest is regenerated with `--emit` (the `Makefile` does this
after `tables` and `pdf`), and the supplement zip is built deterministically
by `python -m analysis.servo_v5_supplement_zip` so its leaf hash is
reproducible. A release-cut gate, `--verify-release`, additionally binds the
distributed assets recorded in `release/EXTERNAL_PUBLICATION.json`; it fails
by design whenever the working tree is ahead of the published release.

Scope: the chain establishes **artifact-lineage integrity** (each recorded
hash must equal its recomputed value), not the semantic correctness of the
draft judgments, and the tables-to-PDF edge is a procedural build-time
binding rather than a cryptographic derivation.

## Corpus

The source-fidelity tests — which verify that a proposition's `exact_quote`
actually appears on its recorded `pdf_page` inside the real source PDF, and
that the PDF's SHA-256 matches the frozen value — require two things this
package does not ship:

1. The six source PDFs under the filenames recorded in each
   `servo_v5_source_propositions/C0N.json` (`source_pdf_name`), located in a
   directory you point at with the **`SERVO_V5_CORPUS_ROOT`** environment
   variable (set it to the corpus root -- the directory containing
   `1_AI_Scientist_Core/...`). Without `SERVO_V5_CORPUS_ROOT` set, the tests
   fall back to `../ai_scientist/` resolved relative to this repository's
   root, i.e. two directories above `analysis/`; that fallback only resolves
   correctly inside a full `CAISc_2026` git checkout. It does **not**
   resolve correctly for a standalone unzipped supplement, because the
   directory depth from the test file to the unzip root is different there
   -- see `SUPPLEMENT_README.md`. Set the environment variable explicitly
   rather than relying on relative placement.
2. `pdftotext` on `PATH` (part of `poppler-utils`).

Without both, `analysis/tests/servo_v5/test_verify_contract.py` and
`test_source_freeze_contract.py` **skip** their corpus-dependent tests
(`requires_corpus`) rather than failing — so a fully green run of the
structural test command above does **not** by itself confirm source
fidelity; **a skip is not a pass**. It confirms only that the four layers
are internally consistent (schema-valid, cross-referenced correctly,
deterministic table generation). Always check that the run reports 0
skipped before treating it as a source-fidelity check.

To acquire the corpus and run the full verification, including
source-fidelity:

1. See [`servo_v5_corpus_manifest.md`](./servo_v5_corpus_manifest.md) for
   each case's citation, expected filename, expected SHA-256, and a public
   DOI/arXiv pointer to obtain the PDF. The PDFs are third-party copyrighted
   works and are not redistributed here.
2. Place each acquired PDF under a directory of your choosing and set
   `SERVO_V5_CORPUS_ROOT` to that directory, e.g.
   `export SERVO_V5_CORPUS_ROOT=/path/to/ai_scientist`. Confirm
   `shasum -a 256 <file>` matches the manifest before relying on it.
3. Re-run the test command above with `SERVO_V5_CORPUS_ROOT` set and
   `pdftotext` present; the `requires_corpus` tests then execute instead of
   skipping. Confirm the run reports 0 skipped.

## Version of record

The version of record for the manuscript is the OpenReview camera-ready
submission. This package accompanies a post-submission revision and is
released under the `servo-corrected-v5.x` tag series (see the repository's
`release/` directory for licensing and release-attestation details).
