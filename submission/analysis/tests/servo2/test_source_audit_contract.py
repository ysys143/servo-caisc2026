from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from conftest import REPOSITORY, assert_rejected, run_cli


def _one_sealed_source(package: Path) -> tuple[Path, dict[str, str]]:
    registry = json.loads(
        (package / "analysis" / "source_registry.json").read_text(encoding="utf-8")
    )
    entry = registry["sources"][0]
    manifest = json.loads(
        (REPOSITORY / "analysis" / "citation_audit" / "core14-manifest.json").read_text(
            encoding="utf-8"
        )
    )
    source = next(
        item
        for item in manifest["sources"]
        if item["citation_key"] == entry["citation_key"]
    )
    path = Path(source["pdf_path"]).expanduser().resolve()
    assert path.is_file(), f"local source-audit fixture is unavailable: {path}"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["pdf_sha256"]
    return path, entry


def test_source_audit_rejects_symlink_escape_outside_source_root(
    package: Path, tmp_path: Path
) -> None:
    source, entry = _one_sealed_source(package)
    source_root = tmp_path / "source-root"
    source_root.mkdir()
    outside = tmp_path / "outside" / entry["filename_hint"]
    outside.parent.mkdir()
    shutil.copyfile(source, outside)
    (source_root / entry["filename_hint"]).symlink_to(outside)

    assert_rejected(
        run_cli(package, "source-byte-audit", source_root=source_root),
        "SOURCE_BYTE_AUDIT_SYMLINK_ESCAPE",
    )


def test_source_audit_rejects_duplicate_files_with_one_expected_hash(
    package: Path, tmp_path: Path
) -> None:
    source, entry = _one_sealed_source(package)
    source_root = tmp_path / "source-root"
    source_root.mkdir()
    shutil.copyfile(source, source_root / entry["filename_hint"])
    shutil.copyfile(source, source_root / f"duplicate-{entry['filename_hint']}")

    assert_rejected(
        run_cli(package, "source-byte-audit", source_root=source_root),
        "SOURCE_BYTE_AUDIT_DUPLICATE",
    )


def test_source_audit_distinguishes_partial_corpus_from_wrong_bytes(
    package: Path, tmp_path: Path
) -> None:
    source, entry = _one_sealed_source(package)
    source_root = tmp_path / "source-root"
    source_root.mkdir()
    shutil.copyfile(source, source_root / entry["filename_hint"])

    result = run_cli(package, "source-byte-audit", source_root=source_root)
    assert_rejected(result, "SOURCE_BYTE_AUDIT_MISMATCH")
    assert "missing 12 sealed source files" in result.stderr
