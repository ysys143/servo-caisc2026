from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tomllib

from .servo2_io import Servo2Error, sha256


PDF_NAME = "servo_caiscfp2026_post-submit.pdf"
ATTESTATION_NAME = "release_attestation.json"


def _cff_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if raw_line.startswith(("version:", "date-released:", "url:")):
            key, value = raw_line.split(":", 1)
            fields[key] = value.strip().strip("\"'")
    return fields


def _verify_release_identity(root: Path, state: object, release: object) -> None:
    try:
        project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
        project_name = project["project"]["name"]
        project_version = project["project"]["version"]
        citation = _cff_fields(root / "CITATION.cff")
    except (FileNotFoundError, KeyError, tomllib.TOMLDecodeError) as error:
        raise Servo2Error("RELEASE_IDENTITY_MISMATCH", "release metadata") from error

    citation_version = citation.get("version", "")
    if (
        project_name != "servo-schema3-reproducibility"
        or not isinstance(project_version, str)
        or citation_version != project_version
        or "unreleased" in citation_version.lower()
    ):
        raise Servo2Error("RELEASE_IDENTITY_MISMATCH", "project and citation version")

    if state == "published_github_release":
        expected_suffix = f"/servo-corrected-v{project_version}"
        if (
            not isinstance(release, str)
            or not release.endswith(expected_suffix)
            or citation.get("url") != release
            or not citation.get("date-released")
        ):
            raise Servo2Error("RELEASE_IDENTITY_MISMATCH", "published release citation")


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
    state = attestation.get("state")
    release = attestation.get("github_release")
    publication_valid = (state == "unpublished_local_candidate" and release in {None, "not_published"}) or (
        state == "published_github_release"
        and isinstance(release, str)
        and release.startswith("https://github.com/")
    )
    if (
        not publication_valid
        or attestation.get("pdf_filename") != PDF_NAME
        or attestation.get("publication_doi") not in {None, "not_published"}
    ):
        raise Servo2Error("RELEASE_ATTESTATION_INVALID", "publication state")
    _verify_release_identity(root, state, release)
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


def verify_repository_pdf_sync(reader_pdf: Path, package_root: Path) -> None:
    packaged_pdf = package_root / PDF_NAME
    if not reader_pdf.is_file() or not packaged_pdf.is_file():
        raise Servo2Error("RELEASE_SOURCE_PDF_MISSING", PDF_NAME)
    if sha256(reader_pdf) != sha256(packaged_pdf):
        raise Servo2Error("RELEASE_SOURCE_PDF_MISMATCH", PDF_NAME)
