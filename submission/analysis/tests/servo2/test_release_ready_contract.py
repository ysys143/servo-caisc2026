from __future__ import annotations

import hashlib
import json

from conftest import assert_rejected, run_cli


PDF_NAME = "servo_caiscfp2026_post-submit.pdf"


def _write_attestation(package, pdf_hash: str, binding: str) -> None:
    payload = {
        "schema_version": "2.0.0",
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
