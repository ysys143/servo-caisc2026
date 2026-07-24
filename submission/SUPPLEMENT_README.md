# SERVO v5 supplement — top-level README

This is `caisc2026-servo-supplement.zip`, the supplementary-material package
for the SERVO analysis of six AI-scientist systems (C01-C06). It contains
the source-first v5 pipeline (machine-readable per-case records, generated
tables, and tests) plus the manuscript's bibliography.

This file is intentionally short. The full package documentation —
directory-by-directory contents, the four coding layers, and the corpus
verification procedure in detail — lives in [`analysis/README.md`](./analysis/README.md).
Read this file first to run the tests; read `analysis/README.md` for
everything else.

## Layout at a glance

```
.
├── SUPPLEMENT_README.md      (this file)
├── references.bib            manuscript bibliography
└── analysis/
    ├── README.md              full package documentation
    ├── servo_v5_corpus_manifest.md   how to acquire/verify the 6 source PDFs
    ├── servo_v5_source_propositions/ layer 1: verbatim propositions, quotes, locators
    ├── servo_v5_alignments/          layer 2: propositions mapped to Servo schema
    ├── servo_v5_claims/              layer 3: derived decision-semantic claims
    ├── servo_v5_policy/              layer 4: case-level policy classification
    ├── tbl-servo-v5-*.tex            LaTeX tables generated from the layers above
    └── tests/servo_v5/               the structural test suite (see below)
```

## Running the tests

From the unzipped root, run:

```sh
python -m pytest analysis/tests/servo_v5 -q
```

Do **not** run a bare `pytest -q` from the root — that scope-crawls into
older schema generations and unrelated test suites under `analysis/tests/`
and `analysis/citation_audit/tests/` that this package does not need for the
v5 regression check. The command above is the official one.

Requirements: Python 3.12+ and `pytest` (`pip install pytest`, or
`pip install "pytest>=8.4,<10"` to match `analysis/pyproject.toml`). Nothing
else — the v5 test suite itself does not import PyYAML or pydantic; those
are only pulled in by legacy (`servo2_*`, `validate_servo_consistency.py`)
and `citation_audit` modules outside this test path. If reproducing from the
full `CAISc_2026` repository rather than this standalone zip, `uv run
--extra test python -m pytest analysis/tests/servo_v5 -q` works the same
way and matches the project's locked environment. `pdftotext` (part of
`poppler-utils`) is needed only for the corpus-dependent checks described
next, not for this command.

The suite has 114 tests. Run from a bare unzip (no corpus present, the
default case — see below), it reports **111 passed, 3 skipped**. With a
byte-matching corpus in place it reports **114 passed, 0 skipped**.

## The corpus caveat

The command above passing does **not** by itself confirm source fidelity.
It confirms only that the four coding layers are internally consistent
(schema-valid, cross-referenced correctly, deterministic table generation).

A subset of tests — `test_verify_contract.py` and
`test_source_freeze_contract.py` — additionally check that each recorded
`exact_quote` really appears on its stated `pdf_page` inside the real source
PDF, and that the PDF's SHA-256 matches the frozen value. These
corpus-dependent checks require the six source PDFs at a sibling directory
`../ai_scientist/` (i.e., next to, not inside, the unzipped package) plus
`pdftotext` on `PATH`. Without both, they **skip** rather than fail or
error, so "114 passed" alone does not mean source fidelity was checked.

To run the corpus-dependent checks, see
[`analysis/servo_v5_corpus_manifest.md`](./analysis/servo_v5_corpus_manifest.md)
for each case's citation, expected filename, expected SHA-256, and a public
DOI/arXiv pointer — the PDFs are third-party copyrighted works and are not
redistributed here.

## Version of record

The version of record for the manuscript is the OpenReview camera-ready
submission. This package accompanies a post-submission revision and is
released under the `servo-corrected-v5.x` tag series.
