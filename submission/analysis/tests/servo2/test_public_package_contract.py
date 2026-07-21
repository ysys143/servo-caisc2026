from __future__ import annotations

import json
import re
from pathlib import Path

from conftest import assert_rejected, run_cli, tree_digest


SECRET_MARKERS = ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY")
SECRET_TOKEN = re.compile(r"(?<![A-Za-z0-9])sk-(?:proj|ant)-[A-Za-z0-9_-]{24,}(?![A-Za-z0-9])")
ALLOWED_RELEASE_PDFS = {"servo_caiscfp2026_post-submit.pdf"}
NORMATIVE_ANALYSIS_DOCS = {
    "holdout_protocol.md",
    "predicate_contract.md",
    "provenance_crosswalk.md",
}


def _manifest(package: Path) -> Path:
    paths = sorted(package.rglob("*manifest*.json"))
    for path in reversed(paths):
        value = json.loads(path.read_text(encoding="utf-8"))
        if "generated_artifacts" in value or "generated_artifact_sha256" in value:
            return path
    raise AssertionError("Schema 2 package lacks a generated-artifact manifest")


def _generated_paths(package: Path) -> list[Path]:
    manifest = json.loads(_manifest(package).read_text(encoding="utf-8"))
    generated = manifest.get("generated_artifacts") or manifest.get("generated_artifact_sha256")
    assert isinstance(generated, dict) and generated, "manifest does not bind generated artifacts"
    paths: list[Path] = []
    for name in generated:
        candidate = package / name
        if not candidate.is_file():
            candidate = package / "analysis" / name
        assert candidate.is_file(), f"manifest target not found: {name}"
        paths.append(candidate)
    return paths


def test_public_package_contains_normative_analysis_documents(package: Path) -> None:
    present = {path.name for path in (package / "analysis").glob("*.md")}
    assert NORMATIVE_ANALYSIS_DOCS <= present
    manifest = json.loads(_manifest(package).read_text(encoding="utf-8"))
    canonical = manifest["canonical_input_sha256"]
    assert {f"analysis/{name}" for name in NORMATIVE_ANALYSIS_DOCS} <= set(canonical)


def test_public_package_contains_no_absolute_paths_secrets_or_source_pdfs(valid_public: Path) -> None:
    forbidden: list[str] = []
    for path in valid_public.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() == ".pdf" and path.name not in ALLOWED_RELEASE_PDFS:
            forbidden.append(f"source PDF: {path.relative_to(valid_public)}")
            continue
        raw = path.read_bytes()
        text = raw.decode("utf-8", errors="ignore")
        if "/Users/" in text or "C:\\Users\\" in text:
            forbidden.append(f"absolute path: {path.relative_to(valid_public)}")
        if any(marker in text for marker in SECRET_MARKERS) or SECRET_TOKEN.search(text):
            forbidden.append(f"secret marker: {path.relative_to(valid_public)}")
    assert not forbidden, "PUBLIC_PACKAGE_PRIVACY_LEAK:\n" + "\n".join(forbidden)


def test_stale_generated_artifact_is_rejected(valid_public: Path) -> None:
    target = _generated_paths(valid_public)[0]
    target.write_bytes(target.read_bytes() + b"\nSTALE")
    assert_rejected(run_cli(valid_public, "public-regeneration"), "STALE_GENERATED_ARTIFACT")


def test_public_regeneration_rejects_manifest_schema_drift(package: Path) -> None:
    manifest_path = _manifest(package)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["schema_version"] = "2.0.0"
    manifest_path.write_text(json.dumps(manifest, sort_keys=True) + "\n", encoding="utf-8")

    assert_rejected(
        run_cli(package, "public-regeneration"),
        "RELEASE_SCHEMA_IDENTITY_MISMATCH",
    )


def test_public_regeneration_rejects_normative_schema_version_drift(package: Path) -> None:
    schema = package / "analysis" / "servo_schema.yaml"
    schema.write_text(
        schema.read_text(encoding="utf-8").replace(
            'schema_version: "3.0.0"', 'schema_version: "2.0.0"', 1
        ),
        encoding="utf-8",
    )

    assert_rejected(
        run_cli(package, "public-regeneration"), "SCHEMA_VERSION_MISMATCH"
    )


def test_public_regeneration_rejects_evidence_ledger_schema_drift(package: Path) -> None:
    ledger_path = package / "analysis" / "servo2_evidence_ledger.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    ledger["schema_version"] = "2.0.0"
    ledger_path.write_text(json.dumps(ledger, sort_keys=True) + "\n", encoding="utf-8")

    assert_rejected(
        run_cli(package, "public-regeneration"), "SCHEMA_VERSION_MISMATCH"
    )


def test_public_mode_does_not_read_external_source_root(package: Path, tmp_path: Path) -> None:
    canary = tmp_path / "outside-source" / "secret.txt"
    canary.parent.mkdir()
    canary.write_text("PUBLIC-MODE-MUST-NOT-READ-THIS", encoding="utf-8")
    canary.chmod(0)
    manifest_path = _manifest(package)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["source_root"] = str(canary.parent.resolve())
    manifest_path.write_text(json.dumps(manifest, sort_keys=True) + "\n", encoding="utf-8")
    result = run_cli(package, "public-regeneration")
    canary.chmod(0o600)
    combined = result.stdout + result.stderr
    assert "PUBLIC-MODE-MUST-NOT-READ-THIS" not in combined
    assert_rejected(result, "PUBLIC_EXTERNAL_READ_FORBIDDEN")


def test_public_validator_rejects_injected_secret_absolute_path_and_pdf(package: Path) -> None:
    leak = package / "analysis" / "leaked-source.pdf"
    leak.write_bytes(
        b"%PDF-1.4\n/Users/private/source.pdf\n"
        b"OPENAI_API_KEY=sk-proj-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    )

    assert_rejected(run_cli(package, "public-regeneration"), "PUBLIC_PACKAGE_PRIVACY_LEAK")


def test_delete_and_rebuild_is_byte_deterministic(package: Path) -> None:
    for path in _generated_paths(package):
        path.unlink()
    first = run_cli(package, "public-regeneration")
    assert first.returncode == 0, first.stdout + first.stderr
    first_digest = tree_digest(package)
    for path in _generated_paths(package):
        path.unlink()
    second = run_cli(package, "public-regeneration")
    assert second.returncode == 0, second.stdout + second.stderr
    assert tree_digest(package) == first_digest, "NONDETERMINISTIC_REBUILD"


def test_source_byte_audit_fails_closed_without_matching_local_corpus(package: Path, tmp_path: Path) -> None:
    source_root = tmp_path / "source-root"
    source_root.mkdir()
    (source_root / "wrong.pdf").write_bytes(b"not the sealed source bytes")

    assert_rejected(
        run_cli(package, "source-byte-audit", source_root=source_root),
        "SOURCE_BYTE_AUDIT_MISMATCH",
    )
