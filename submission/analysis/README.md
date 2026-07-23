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
   selection signal/objective, generation scope, execution rule) derived
   from the claims layer.

Each layer is a strict function of the layer before it; nothing is added at
a later stage that the source layer does not license. This ordering is
SERVO v5's answer to the churn problem of earlier schema versions (see
`servo_v5_charter.md`).

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

Both scope to the v5 test package and pass cleanly independent of the
corpus (114 tests at the time of writing). Running the unscoped
`python -m pytest -q` from the project root also exercises unrelated test
suites elsewhere under `analysis/tests/` (older schema generations); scope
to `analysis/tests/servo_v5` if you only want the v5 checks.

## Corpus

The source-fidelity tests — which verify that a proposition's `exact_quote`
actually appears on its recorded `pdf_page` inside the real source PDF, and
that the PDF's SHA-256 matches the frozen value — require two things this
package does not ship:

1. The six source PDFs, expected at a sibling directory `../ai_scientist/`
   (i.e. next to, not inside, this repository) under the filenames recorded
   in each `servo_v5_source_propositions/C0N.json` (`source_pdf_name`).
2. `pdftotext` on `PATH` (part of `poppler-utils`).

Without both, `analysis/tests/servo_v5/test_verify_contract.py` and
`test_source_freeze_contract.py` **skip** their corpus-dependent tests
(`requires_corpus`) rather than failing — so a fully green run of the
structural test command above does **not** by itself confirm source
fidelity. It confirms only that the four layers are internally consistent
(schema-valid, cross-referenced correctly, deterministic table generation).

To acquire the corpus and run the full verification, including
source-fidelity:

1. See [`servo_v5_corpus_manifest.md`](./servo_v5_corpus_manifest.md) for
   each case's citation, expected filename, expected SHA-256, and a public
   DOI/arXiv pointer to obtain the PDF. The PDFs are third-party copyrighted
   works and are not redistributed here.
2. Place each acquired PDF under `../ai_scientist/` using the expected
   filename, and confirm `shasum -a 256 <file>` matches the manifest before
   relying on it.
3. Re-run the test command above (or the same command without the `-k`/path
   scoping) with the corpus and `pdftotext` present; the `requires_corpus`
   tests then execute instead of skipping.

## Version of record

The version of record for the manuscript is the OpenReview camera-ready
submission. This package accompanies a post-submission revision and is
released under the `servo-corrected-v5.x` tag series (see the repository's
`release/` directory for licensing and release-attestation details).
