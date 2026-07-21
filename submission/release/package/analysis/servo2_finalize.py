from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from .servo2_build import (
    MANIFEST_NAME,
    find_manifest,
    regenerate,
    verify_canonical_inputs,
    verify_public_allowlist,
)
from .servo2_evidence import validate_evidence
from .servo2_io import Servo2Error, read_tables, sha256
from .servo2_release import (
    ATTESTATION_NAME,
    PDF_NAME,
    manifest_binding,
    verify_release_ready,
)
from .servo2_schema import validate_schema_contract
from .servo2_validate import (
    validate_legacy_headers,
    validate_public_paths,
    validate_public_privacy,
    validate_tables,
)


def finalize(
    package_root: Path, corrected_pdf: Path, github_release: str | None = None
) -> None:
    if corrected_pdf.name != PDF_NAME:
        raise Servo2Error("FINALIZATION_PDF_FILENAME_INVALID", corrected_pdf.name)
    if corrected_pdf.is_symlink():
        raise Servo2Error("FINALIZATION_PDF_SYMLINK_FORBIDDEN", str(corrected_pdf))
    if not corrected_pdf.is_file():
        raise Servo2Error("FINALIZATION_PDF_MISSING", str(corrected_pdf))
    root = package_root.resolve()
    source = corrected_pdf.resolve()
    if source.is_relative_to(root):
        raise Servo2Error("FINALIZATION_SOURCE_INSIDE_PACKAGE", str(corrected_pdf))
    validate_public_paths(root)
    tables = read_tables(root)
    validate_legacy_headers(tables)
    validate_schema_contract(root, tables)
    validate_tables(tables)
    validate_evidence(root, tables)
    manifest_path, manifest = find_manifest(root)
    validate_public_privacy(root, manifest)
    verify_canonical_inputs(root, manifest)
    regenerate(root, tables, manifest)
    verify_public_allowlist(root, manifest)
    target = root / PDF_NAME
    shutil.copyfile(source, target)
    public_hashes = {
        path.relative_to(root).as_posix(): sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.name not in {MANIFEST_NAME, ATTESTATION_NAME}
    }
    manifest["public_file_sha256"] = public_hashes
    attestation = {
        "schema_version": "3.0.0",
        "state": "published_github_release" if github_release else "unpublished_local_candidate",
        "pdf_filename": PDF_NAME,
        "pdf_sha256": sha256(target),
        "manifest_binding_sha256": manifest_binding(manifest),
        "publication_doi": "not_published",
        "github_release": github_release or "not_published",
    }
    attestation_path = root / ATTESTATION_NAME
    attestation_path.write_text(
        json.dumps(attestation, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    public_hashes[ATTESTATION_NAME] = sha256(attestation_path)
    manifest["public_file_sha256"] = public_hashes
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    verify_release_ready(root, manifest)
    verify_public_allowlist(root, manifest)


def main() -> None:
    parser = argparse.ArgumentParser(prog="servo2-finalize")
    parser.add_argument("--package-root", type=Path, required=True)
    parser.add_argument("--corrected-pdf", type=Path, required=True)
    parser.add_argument("--github-release")
    options = parser.parse_args()
    try:
        finalize(options.package_root, options.corrected_pdf, options.github_release)
    except Servo2Error as error:
        raise SystemExit(str(error)) from error
    state = "published_github_release" if options.github_release else "unpublished_local_candidate"
    print(f"SERVO2_FINALIZED: {state}")


if __name__ == "__main__":
    main()
