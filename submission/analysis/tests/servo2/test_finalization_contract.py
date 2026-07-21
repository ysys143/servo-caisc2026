from __future__ import annotations

import os
import hashlib
import json
import subprocess
from pathlib import Path

from conftest import REPOSITORY, assert_rejected, run_cli, tree_digest


PDF_NAME = "servo_caiscfp2026_post-submit.pdf"


def _run_finalize(
    package: Path, corrected_pdf: Path
) -> subprocess.CompletedProcess[str]:
    environment = {
        "PATH": os.environ["PATH"],
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "HOME": str(package.parent / "empty-home"),
        "PYTHONHASHSEED": "0",
        "PYTHONDONTWRITEBYTECODE": "1",
        "UV_CACHE_DIR": str(package.parent / "uv-cache"),
        "UV_PROJECT_ENVIRONMENT": str(package.parent / "uv-environment"),
    }
    return subprocess.run(
        [
            "uv",
            "run",
            "--project",
            str(package / "pyproject.toml"),
            "--directory",
            str(package),
            "--no-sync",
            "python",
            "-B",
            "-m",
            "analysis.servo2_finalize",
            "--package-root",
            str(package),
            "--corrected-pdf",
            str(corrected_pdf),
        ],
        cwd=REPOSITORY,
        env=environment,
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )


def _candidate_pdf(tmp_path: Path) -> Path:
    path = tmp_path / "source" / PDF_NAME
    path.parent.mkdir()
    path.write_bytes(b"%PDF-1.4\ncorrected candidate fixture\n%%EOF\n")
    return path


def test_finalization_enables_unpublished_release_ready(
    package: Path, tmp_path: Path
) -> None:
    result = _run_finalize(package, _candidate_pdf(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    ready = run_cli(package, "release-ready")
    assert ready.returncode == 0, ready.stdout + ready.stderr


def test_finalization_is_byte_idempotent(package: Path, tmp_path: Path) -> None:
    source = _candidate_pdf(tmp_path)
    first = _run_finalize(package, source)
    assert first.returncode == 0, first.stdout + first.stderr
    digest = tree_digest(package)
    second = _run_finalize(package, source)
    assert second.returncode == 0, second.stdout + second.stderr
    assert tree_digest(package) == digest


def test_release_ready_rejects_pdf_changed_after_finalization(
    package: Path, tmp_path: Path
) -> None:
    result = _run_finalize(package, _candidate_pdf(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    (package / PDF_NAME).write_bytes(b"%PDF-1.4\nstale replacement\n")
    assert_rejected(run_cli(package, "release-ready"), "RELEASE_PDF_CHECKSUM_MISMATCH")


def test_finalization_rejects_wrong_filename(package: Path, tmp_path: Path) -> None:
    source = tmp_path / "wrong.pdf"
    source.write_bytes(b"%PDF-1.4\n")
    assert_rejected(_run_finalize(package, source), "FINALIZATION_PDF_FILENAME_INVALID")


def test_finalization_rejects_symlink_source(package: Path, tmp_path: Path) -> None:
    target = tmp_path / "actual.pdf"
    target.write_bytes(b"%PDF-1.4\n")
    source = tmp_path / PDF_NAME
    source.symlink_to(target)
    assert_rejected(
        _run_finalize(package, source), "FINALIZATION_PDF_SYMLINK_FORBIDDEN"
    )


def test_finalization_rejects_source_inside_package(package: Path) -> None:
    source = package / "nested" / PDF_NAME
    source.parent.mkdir()
    source.write_bytes(b"%PDF-1.4\n")
    assert_rejected(
        _run_finalize(package, source), "FINALIZATION_SOURCE_INSIDE_PACKAGE"
    )


def test_unchanged_attestation_rejects_rehashed_modified_readme(
    package: Path, tmp_path: Path
) -> None:
    result = _run_finalize(package, _candidate_pdf(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    readme = package / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8") + "\nmodified\n", encoding="utf-8"
    )
    manifest_path = package / "servo2_public_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["public_file_sha256"]["README.md"] = hashlib.sha256(
        readme.read_bytes()
    ).hexdigest()
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    assert_rejected(
        run_cli(package, "release-ready"),
        "RELEASE_ATTESTATION_MANIFEST_MISMATCH",
    )
