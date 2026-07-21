from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .servo2_io import Servo2Error, sha256


PDF_NAME = "servo_caiscfp2026_post-submit.pdf"
ATTESTATION_NAME = "release_attestation.json"


def manifest_binding(manifest: dict[str, str | dict[str, str]]) -> str:
    public_files = manifest.get("public_file_sha256")
    if not isinstance(public_files, dict):
        raise Servo2Error("PUBLIC_MANIFEST_INVALID", "public file allowlist is absent")
    bound_public_files = {
        name: digest
        for name, digest in sorted(public_files.items())
        if name != ATTESTATION_NAME
    }
    payload = {
        "schema_version": manifest.get("schema_version"),
        "canonical_input_sha256": manifest.get("canonical_input_sha256"),
        "generated_artifact_sha256": manifest.get("generated_artifact_sha256"),
        "public_file_sha256": bound_public_files,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(canonical).hexdigest()


def verify_release_ready(root: Path, manifest: dict[str, str | dict[str, str]]) -> None:
    pdf = root / PDF_NAME
    attestation_path = root / ATTESTATION_NAME
    if not pdf.is_file():
        raise Servo2Error("RELEASE_PDF_MISSING", PDF_NAME)
    if not attestation_path.is_file():
        raise Servo2Error("RELEASE_ATTESTATION_MISSING", ATTESTATION_NAME)
    try:
        attestation = json.loads(attestation_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, TypeError) as error:
        raise Servo2Error("RELEASE_ATTESTATION_INVALID", ATTESTATION_NAME) from error
    if (
        attestation.get("state") != "unpublished_local_candidate"
        or attestation.get("pdf_filename") != PDF_NAME
        or attestation.get("publication_doi") not in {None, "not_published"}
        or attestation.get("github_release") not in {None, "not_published"}
    ):
        raise Servo2Error("RELEASE_ATTESTATION_INVALID", "publication state")
    actual_pdf_hash = sha256(pdf)
    if attestation.get("pdf_sha256") != actual_pdf_hash:
        raise Servo2Error("RELEASE_PDF_CHECKSUM_MISMATCH", PDF_NAME)
    if attestation.get("manifest_binding_sha256") != manifest_binding(manifest):
        raise Servo2Error("RELEASE_ATTESTATION_MANIFEST_MISMATCH", ATTESTATION_NAME)
    public_files = manifest.get("public_file_sha256")
    if not isinstance(public_files, dict):
        raise Servo2Error("PUBLIC_MANIFEST_INVALID", "public file allowlist is absent")
    for name, path in ((PDF_NAME, pdf), (ATTESTATION_NAME, attestation_path)):
        if public_files.get(name) != sha256(path):
            raise Servo2Error("RELEASE_MANIFEST_INCOMPLETE", name)
