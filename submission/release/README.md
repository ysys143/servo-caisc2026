# Servo corrected package

Package release 3.0.16 implements the normative Servo schema version 3.0.0.
The package release number identifies this synchronized manuscript and audit
snapshot; it does not change the schema contract version.

Package state is recorded in `release_attestation.json`, which is written during
finalization. Cite a DOI or release tag only when that attestation names it.

Licensing is split by artifact type: documentation and structured data use
CC BY 4.0 (`LICENSE`), while executable source code uses the MIT License
(`LICENSE-CODE`). Third-party materials remain excluded as described in the
notices.

This package separates two assurances:

1. `public-regeneration` validates redistributable Schema 3 records and rebuilds
   derived tables using package files only. It does not authenticate primary
   sources or establish semantic entailment.
2. `source-byte-audit --source-root PATH` is an optional local audit against
   lawfully obtained user-supplied PDFs. It checks expected source-file bytes,
   uniqueness, and containment; it does not verify quoted passages or page
   locators. It never redistributes PDFs or serializes local paths.

The release allowlist forbids source PDFs, absolute personal paths, credentials,
caches, local source maps, and raw model-provider logs. The only manuscript PDF
eligible for the corrected release is `servo_caiscfp2026_post-submit.pdf`.

Set `PACKAGE` to the package's absolute path.  The explicit temporary cache and
environment keep runtime state outside the release tree and `--directory`
makes the commands independent of the caller's working directory:

```sh
PACKAGE=/absolute/path/to/package
UV_CACHE_DIR="$(mktemp -d)" UV_PROJECT_ENVIRONMENT="$(mktemp -d)" \
  uv run --project "$PACKAGE/pyproject.toml" --directory "$PACKAGE" --no-sync \
  python -B -m analysis.validate_servo2 public-regeneration --package-root "$PACKAGE"

UV_CACHE_DIR="$(mktemp -d)" UV_PROJECT_ENVIRONMENT="$(mktemp -d)" \
  uv run --project "$PACKAGE/pyproject.toml" --directory "$PACKAGE" --no-sync \
  python -B -m analysis.servo2_curate --package-root "$PACKAGE" \
  --source-root /path/to/local/corpus --destination /path/to/curated-corpus

UV_CACHE_DIR="$(mktemp -d)" UV_PROJECT_ENVIRONMENT="$(mktemp -d)" \
  uv run --project "$PACKAGE/pyproject.toml" --directory "$PACKAGE" --no-sync \
  python -B -m analysis.validate_servo2 source-byte-audit --package-root "$PACKAGE" \
  --source-root /path/to/curated-corpus

UV_CACHE_DIR="$(mktemp -d)" UV_PROJECT_ENVIRONMENT="$(mktemp -d)" \
  uv run --project "$PACKAGE/pyproject.toml" --directory "$PACKAGE" --no-sync \
  python -B -m analysis.servo2_finalize --package-root "$PACKAGE" \
  --corrected-pdf /path/to/servo_caiscfp2026_post-submit.pdf

UV_CACHE_DIR="$(mktemp -d)" UV_PROJECT_ENVIRONMENT="$(mktemp -d)" \
  uv run --project "$PACKAGE/pyproject.toml" --directory "$PACKAGE" --no-sync \
  python -B -m analysis.validate_servo2 release-ready --package-root "$PACKAGE"
```

The first command must work with an empty HOME, no credentials, no network, and
an arbitrary working directory. The second command intentionally fails closed
when the source root or required source bytes are absent.  The audit requires
exactly one regular PDF for every sealed hash; it rejects symlinks and duplicate
matching PDFs.  The deterministic curation helper copies one lexicographically
first matching regular file per hash and writes `curated_source_manifest.json`.
Finalization is a separate, explicit operation: it accepts only the corrected
PDF's fixed filename, records either an unpublished candidate or the supplied
GitHub release URL in the attestation, rebinds the complete public-file
allowlist, and enables `release-ready`. It does not itself publish or claim a
DOI.
The attestation is an unsigned consistency record binding the PDF, code, data,
documentation, and generated artifacts.  It is not a provenance signature or
publisher authentication. Publication status must be read from the attestation,
not inferred from this static README.

## Evidential limits

The six core entries are source-grounded author interpretations of six
versioned cases from five lineages. The seven domain entries are frozen,
selected anchors, not a representative sample. Historical R24 agreement data
document schema development; they do not validate the final event-channel unit.
