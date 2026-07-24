"""M8 -- single v5 provenance chain (root manifest + fail-closed verifier).

Two v5 manifests already exist but are disconnected:

* ``servo_v5_source_freeze_manifest.json`` binds the corpus PDFs and each
  ``source_propositions/C0X.json`` ledger.
* ``servo_v5_evidence_manifest.json`` binds the alignment/claim/policy files
  to the generated tables and CSV.

This module adds ``servo_v5_provenance_root.json``, which references and
cross-checks both manifests and extends the chain to the manuscript PDF and
the released supplement contents, plus a verifier that recomputes every leaf
and fails closed on any mismatch.

What the chain guarantees: *artifact-lineage integrity* -- any change to an
upstream artifact makes a downstream verification fail. What it does NOT
guarantee (stated, not hidden):

* the semantic correctness of the draft alignment/claim/policy judgments
  (they remain formative; the charter conditions are unmet);
* LaTeX visual rendering;
* a cryptographic derivation of the PDF from the tables -- the manuscript
  edge binds the ``\\input`` table hashes and records the PDF hash as a leaf,
  so "the PDF was built from these tables" is a *procedural* assurance
  (recorded at build time), not a derivation.

Verification has two scopes. ``verify_root`` (internal) checks the
corpus->source->interpretation->evidence->manuscript->supplement chain
against the working tree and always runs (Makefile / test suite). The
``release=True`` scope additionally binds the released assets recorded in
``release/EXTERNAL_PUBLICATION.json`` to the real files and is a release-cut
gate; it is expected to fail whenever the local tree is ahead of the
published release (unfinalized), which is the intended fail-closed signal.
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

from .servo_v5_io import read_json, sha256
from .servo_v5_supplement_zip import ZIP_NAME, build_supplement_zip, collect_members

SCHEMA = "servo_v5_provenance_root"
SCHEMA_VERSION = "5.1.0"
ROOT_NAME = "servo_v5_provenance_root.json"

CASE_IDS = ("C01", "C02", "C03", "C04", "C05", "C06")
INTERP_FAMILIES = {
    "alignments": "servo_v5_alignments",
    "claims": "servo_v5_claims",
    "policy": "servo_v5_policy",
}
TABLE_FILES = (
    "tbl-servo-v5-policy.tex",
    "tbl-servo-v5-boundary.tex",
    "tbl-servo-v5-relations.tex",
)
PROJECTION_FILE = "servo_v5_claims_projection.csv"
GENERATOR_FILE = "build_servo_v5_tables.py"
FREEZE_MANIFEST = "servo_v5_source_freeze_manifest.json"
EVIDENCE_MANIFEST = "servo_v5_evidence_manifest.json"
CORPUS_MANIFEST = "servo_v5_corpus_manifest.json"
BUILDER_FILE = "servo_v5_supplement_zip.py"
TEX_NAME = "main_post-submit.tex"
PDF_NAME = "servo_caiscfp2026_post-submit.pdf"
EXTERNAL_REL = "release/EXTERNAL_PUBLICATION.json"

SCOPE_NOTE = (
    "Binds artifact-lineage integrity only. Does NOT attest the semantic "
    "correctness of the draft alignment/claim/policy judgments, LaTeX visual "
    "rendering, or a cryptographic derivation of the PDF from the tables (the "
    "manuscript edge binds the input-table hashes and records the PDF hash as "
    "a leaf; PDF<-tables is a procedural, build-time assurance). The "
    "supplement container leaf hash lives in EXTERNAL_PUBLICATION and is "
    "same-zlib reproducible; the per-file supplement hashes here are "
    "content-based and portable."
)
CHAIN_RULE = (
    "each recorded sha256 must equal the recomputed sha of its artifact, and "
    "each cross-checked value must equal the corresponding entry in the "
    "referenced manifest; any mismatch fails verification"
)


def _digests_for_family(analysis_dir: Path, subdir: str) -> dict[str, str]:
    return {case: sha256(analysis_dir / subdir / f"{case}.json") for case in CASE_IDS}


def build_root(submission_root: Path) -> dict:
    """Compute the provenance root manifest from the working tree."""
    submission_root = submission_root.resolve()
    analysis_dir = submission_root / "analysis"

    freeze = read_json(analysis_dir / FREEZE_MANIFEST)

    interpretation = {
        family: _digests_for_family(analysis_dir, subdir)
        for family, subdir in INTERP_FAMILIES.items()
    }
    evidence_outputs = {
        name: sha256(analysis_dir / name) for name in (*TABLE_FILES, PROJECTION_FILE)
    }

    # Supplement content hashes: every shipped member EXCEPT the root manifest
    # itself (self-reference would be circular) and the zip container.
    supplement_files = {
        member: sha256(submission_root / member)
        for member in collect_members(submission_root)
        if member != f"analysis/{ROOT_NAME}"
    }

    external = read_json(submission_root / EXTERNAL_REL)

    root = {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "chain_rule": CHAIN_RULE,
        "scope_note": SCOPE_NOTE,
        "corpus": {
            "source_set_sha256": freeze["source_set_sha256"],
            "corpus_manifest_sha256": sha256(analysis_dir / CORPUS_MANIFEST),
        },
        "source": {
            "freeze_manifest_sha256": sha256(analysis_dir / FREEZE_MANIFEST),
            "propositions": _digests_for_family(analysis_dir, "servo_v5_source_propositions"),
        },
        "interpretation": interpretation,
        "evidence": {
            "evidence_manifest_sha256": sha256(analysis_dir / EVIDENCE_MANIFEST),
            "generator_sha256": sha256(analysis_dir / GENERATOR_FILE),
            "outputs": evidence_outputs,
        },
        "manuscript": {
            "tex": TEX_NAME,
            "tex_sha256": sha256(submission_root / TEX_NAME),
            "input_tables": {name: evidence_outputs[name] for name in TABLE_FILES},
            "pdf": PDF_NAME,
            "pdf_sha256": sha256(submission_root / PDF_NAME),
        },
        "supplement": {
            "zip_name": ZIP_NAME,
            "builder_sha256": sha256(analysis_dir / BUILDER_FILE),
            "files": dict(sorted(supplement_files.items())),
        },
        "release": {
            "tag": external.get("tag"),
            "github_commit": external.get("github_commit"),
            "github_release": external.get("github_release"),
            "published_assets": external.get("assets", {}),
        },
    }
    return root


def write_root(submission_root: Path) -> Path:
    submission_root = submission_root.resolve()
    out_path = submission_root / "analysis" / ROOT_NAME
    root = build_root(submission_root)
    out_path.write_text(
        json.dumps(root, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return out_path


def verify_root(submission_root: Path, *, release: bool = False) -> list[str]:
    """Recompute every leaf and cross-check. Return a list of error strings."""
    submission_root = submission_root.resolve()
    analysis_dir = submission_root / "analysis"
    errors: list[str] = []

    def mism(code: str, detail: str) -> None:
        errors.append(f"{code}: {detail}")

    root_path = analysis_dir / ROOT_NAME
    if not root_path.is_file():
        return [f"V5_PROVENANCE_ROOT_MISSING: {root_path}"]
    root = read_json(root_path)
    freeze = read_json(analysis_dir / FREEZE_MANIFEST)
    evidence = read_json(analysis_dir / EVIDENCE_MANIFEST)

    # -- corpus ------------------------------------------------------------
    if root["corpus"]["source_set_sha256"] != freeze["source_set_sha256"]:
        mism("V5_PROVENANCE_CORPUS_SOURCE_SET_MISMATCH", "root vs freeze source_set_sha256")
    if root["corpus"]["corpus_manifest_sha256"] != sha256(analysis_dir / CORPUS_MANIFEST):
        mism("V5_PROVENANCE_CORPUS_MANIFEST_MISMATCH", CORPUS_MANIFEST)

    # -- source (3-way: root == actual == freeze ledger) -------------------
    if root["source"]["freeze_manifest_sha256"] != sha256(analysis_dir / FREEZE_MANIFEST):
        mism("V5_PROVENANCE_FREEZE_MANIFEST_MISMATCH", FREEZE_MANIFEST)
    for case in CASE_IDS:
        actual = sha256(analysis_dir / "servo_v5_source_propositions" / f"{case}.json")
        ledger = freeze.get("cases", {}).get(case, {}).get("ledger_sha256")
        if root["source"]["propositions"].get(case) != actual:
            mism("V5_PROVENANCE_SOURCE_SHA_MISMATCH", f"{case} root vs actual")
        if ledger is not None and ledger != actual:
            mism("V5_PROVENANCE_SOURCE_LEDGER_MISMATCH", f"{case} freeze ledger vs actual")

    # -- interpretation (3-way: root == actual == evidence.inputs) ---------
    ev_inputs = evidence.get("inputs", {})
    for family, subdir in INTERP_FAMILIES.items():
        for case in CASE_IDS:
            actual = sha256(analysis_dir / subdir / f"{case}.json")
            if root["interpretation"][family].get(case) != actual:
                mism("V5_PROVENANCE_INTERP_SHA_MISMATCH", f"{subdir}/{case}.json root vs actual")
            ev_val = ev_inputs.get(f"{subdir}/{case}.json")
            if ev_val is not None and ev_val != actual:
                mism("V5_PROVENANCE_EVIDENCE_INPUT_MISMATCH", f"{subdir}/{case}.json evidence vs actual")

    # -- evidence (3-way: root == actual == evidence.outputs) --------------
    if root["evidence"]["evidence_manifest_sha256"] != sha256(analysis_dir / EVIDENCE_MANIFEST):
        mism("V5_PROVENANCE_EVIDENCE_MANIFEST_MISMATCH", EVIDENCE_MANIFEST)
    gen_actual = sha256(analysis_dir / GENERATOR_FILE)
    if root["evidence"]["generator_sha256"] != gen_actual:
        mism("V5_PROVENANCE_GENERATOR_MISMATCH", f"{GENERATOR_FILE} root vs actual")
    if evidence.get("generator_sha256") not in (None, gen_actual):
        mism("V5_PROVENANCE_GENERATOR_MANIFEST_MISMATCH", f"{GENERATOR_FILE} evidence vs actual")
    ev_outputs = evidence.get("outputs", {})
    for name in (*TABLE_FILES, PROJECTION_FILE):
        actual = sha256(analysis_dir / name)
        if root["evidence"]["outputs"].get(name) != actual:
            mism("V5_PROVENANCE_EVIDENCE_OUTPUT_MISMATCH", f"{name} root vs actual")
        if ev_outputs.get(name) not in (None, actual):
            mism("V5_PROVENANCE_EVIDENCE_OUTPUT_MANIFEST_MISMATCH", f"{name} evidence vs actual")

    # -- manuscript (tables -> tex -> pdf) ---------------------------------
    if root["manuscript"]["tex_sha256"] != sha256(submission_root / TEX_NAME):
        mism("V5_PROVENANCE_TEX_MISMATCH", TEX_NAME)
    for name in TABLE_FILES:
        table_actual = sha256(analysis_dir / name)
        if root["manuscript"]["input_tables"].get(name) != table_actual:
            mism("V5_PROVENANCE_MANUSCRIPT_TABLE_MISMATCH", f"{name} root input_tables vs actual")
        if root["evidence"]["outputs"].get(name) != root["manuscript"]["input_tables"].get(name):
            mism("V5_PROVENANCE_TABLE_EDGE_MISMATCH", f"{name} evidence.outputs vs manuscript.input_tables")
    if root["manuscript"]["pdf_sha256"] != sha256(submission_root / PDF_NAME):
        mism("V5_PROVENANCE_PDF_MISMATCH", PDF_NAME)

    # -- supplement contents (portable, content-based) ---------------------
    recorded = root["supplement"]["files"]
    current = {
        member: sha256(submission_root / member)
        for member in collect_members(submission_root)
        if member != f"analysis/{ROOT_NAME}"
    }
    if root["supplement"]["builder_sha256"] != sha256(analysis_dir / BUILDER_FILE):
        mism("V5_PROVENANCE_BUILDER_MISMATCH", BUILDER_FILE)
    for member in sorted(set(recorded) | set(current)):
        if member not in recorded:
            mism("V5_PROVENANCE_SUPPLEMENT_ADDED", member)
        elif member not in current:
            mism("V5_PROVENANCE_SUPPLEMENT_REMOVED", member)
        elif recorded[member] != current[member]:
            mism("V5_PROVENANCE_SUPPLEMENT_SHA_MISMATCH", member)

    # -- release binding (gate; expected to fail when local is ahead) ------
    if release:
        external = read_json(submission_root / EXTERNAL_REL)
        assets = external.get("assets", {})
        pdf_actual = sha256(submission_root / PDF_NAME)
        if assets.get(PDF_NAME) != pdf_actual:
            mism("V5_PROVENANCE_RELEASE_PDF_MISMATCH", "EXTERNAL asset vs actual pdf")
        if assets.get(PDF_NAME) != root["manuscript"]["pdf_sha256"]:
            mism("V5_PROVENANCE_RELEASE_PDF_ROOT_MISMATCH", "EXTERNAL asset vs root pdf")
        # Build to a temp path so verification never overwrites the canonical zip.
        with tempfile.TemporaryDirectory() as tmp:
            zip_leaf = build_supplement_zip(submission_root, Path(tmp) / ZIP_NAME)
        if assets.get(ZIP_NAME) != zip_leaf:
            mism("V5_PROVENANCE_RELEASE_ZIP_MISMATCH", "EXTERNAL asset vs rebuilt deterministic zip")
        for field in ("tag", "github_commit", "github_release"):
            if not external.get(field) or root["release"].get(field) != external.get(field):
                mism("V5_PROVENANCE_RELEASE_POINTER_MISMATCH", field)

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(prog="servo-v5-provenance")
    parser.add_argument(
        "--submission-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="submission/ directory (default: parent of analysis/)",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--emit", action="store_true", help="write servo_v5_provenance_root.json")
    group.add_argument("--verify", action="store_true", help="verify the internal chain (fail-closed)")
    group.add_argument(
        "--verify-release",
        action="store_true",
        help="verify the internal chain AND the released-asset binding (release gate)",
    )
    options = parser.parse_args()

    if options.emit:
        out = write_root(options.submission_root)
        print(f"SERVO_V5_PROVENANCE_EMITTED: {out.name}")
        return

    errors = verify_root(options.submission_root, release=options.verify_release)
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        print("SERVO_V5_PROVENANCE_FAILED", file=sys.stderr)
        raise SystemExit(1)
    scope = "internal+release" if options.verify_release else "internal"
    print(f"SERVO_V5_PROVENANCE_OK: {scope} chain verified")


if __name__ == "__main__":
    main()
