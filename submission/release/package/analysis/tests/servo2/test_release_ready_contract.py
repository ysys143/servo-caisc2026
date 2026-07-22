from __future__ import annotations

import hashlib
import json
from pathlib import Path

from conftest import assert_rejected, run_cli
from analysis.servo2_build import find_manifest
from analysis.servo2_release import (
    manifest_binding,
    verify_release_ready,
    verify_repository_pdf_sync,
)
from analysis.servo2_io import Servo2Error
import pytest


PDF_NAME = "servo_caiscfp2026_post-submit.pdf"


def _write_attestation(package, pdf_hash: str, binding: str) -> None:
    payload = {
        "schema_version": "4.1.0",
        "state": "unpublished_local_candidate",
        "pdf_filename": PDF_NAME,
        "pdf_sha256": pdf_hash,
        "manifest_binding_sha256": binding,
        "publication_doi": "not_published",
        "github_release": "not_published",
    }
    (package / "release_attestation.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def test_release_ready_rejects_missing_corrected_pdf(package) -> None:
    (package / PDF_NAME).unlink(missing_ok=True)
    assert_rejected(run_cli(package, "release-ready"), "RELEASE_PDF_MISSING")


def test_release_ready_rejects_stale_pdf(package) -> None:
    (package / PDF_NAME).write_bytes(b"stale corrected manuscript")
    _write_attestation(package, "0" * 64, "0" * 64)
    assert_rejected(run_cli(package, "release-ready"), "RELEASE_PDF_CHECKSUM_MISMATCH")


def test_release_ready_rejects_attestation_manifest_mismatch(package) -> None:
    raw = b"candidate corrected manuscript"
    (package / PDF_NAME).write_bytes(raw)
    _write_attestation(package, hashlib.sha256(raw).hexdigest(), "0" * 64)
    assert_rejected(
        run_cli(package, "release-ready"),
        "RELEASE_ATTESTATION_MANIFEST_MISMATCH",
    )


def test_repository_sync_rejects_different_reader_and_packaged_pdf(
    package: Path, tmp_path: Path
) -> None:
    reader_pdf = tmp_path / PDF_NAME
    reader_pdf.write_bytes(b"new reader-facing manuscript")
    (package / PDF_NAME).write_bytes(b"stale packaged manuscript")

    with pytest.raises(Servo2Error, match="RELEASE_SOURCE_PDF_MISMATCH"):
        verify_repository_pdf_sync(reader_pdf, package)


def test_release_ready_rejects_unreleased_citation_identity(package: Path) -> None:
    # Given: a published attestation paired with candidate-only citation metadata.
    raw = b"candidate corrected manuscript"
    (package / PDF_NAME).write_bytes(raw)
    _, manifest = find_manifest(package)
    _write_attestation(
        package,
        hashlib.sha256(raw).hexdigest(),
        manifest_binding(manifest),
    )
    citation = package / "CITATION.cff"
    citation_text = citation.read_text(encoding="utf-8")
    citation_version = next(
        line for line in citation_text.splitlines() if line.startswith("version:")
    )
    citation.write_text(
        citation_text.replace(citation_version, "version: 0.0.0-unreleased"),
        encoding="utf-8",
    )
    # When/Then: release readiness checks the public citation surface itself.
    with pytest.raises(Servo2Error, match="RELEASE_IDENTITY_MISMATCH"):
        verify_release_ready(package, manifest)


def test_release_ready_rejects_attestation_schema_drift(package: Path) -> None:
    _, manifest = find_manifest(package)
    attestation_path = package / "release_attestation.json"
    attestation = json.loads(attestation_path.read_text(encoding="utf-8"))
    attestation["schema_version"] = "2.0.0"
    attestation["manifest_binding_sha256"] = manifest_binding(manifest)
    attestation_path.write_text(
        json.dumps(attestation, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    with pytest.raises(Servo2Error, match="RELEASE_SCHEMA_IDENTITY_MISMATCH"):
        verify_release_ready(package, manifest)


def test_release_ready_rejects_manifest_schema_drift(package: Path) -> None:
    _, manifest = find_manifest(package)
    manifest["schema_version"] = "2.0.0"
    attestation_path = package / "release_attestation.json"
    attestation = json.loads(attestation_path.read_text(encoding="utf-8"))
    attestation["schema_version"] = "2.0.0"
    attestation["manifest_binding_sha256"] = manifest_binding(manifest)
    attestation_path.write_text(
        json.dumps(attestation, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    with pytest.raises(Servo2Error, match="RELEASE_SCHEMA_IDENTITY_MISMATCH"):
        verify_release_ready(package, manifest)
