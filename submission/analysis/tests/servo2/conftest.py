from __future__ import annotations

import csv
import hashlib
import os
import shutil
import subprocess
from pathlib import Path

import pytest


REPOSITORY = Path(__file__).resolve().parents[3]
PUBLIC_PACKAGE = REPOSITORY / "release" / "package"


def csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames, f"missing CSV header: {path}"
        return list(reader.fieldnames), list(reader)


def write_rows(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def table(package: Path, stem: str) -> Path:
    matches = sorted((package / "analysis").glob(f"servo2_{stem}.*"))
    assert len(matches) == 1, f"expected exactly one servo2_{stem} table, got {matches}"
    assert matches[0].suffix == ".csv", f"mutation contract requires CSV: {matches[0]}"
    return matches[0]


def column(row: dict[str, str], *names: str) -> str:
    for name in names:
        if name in row:
            return name
    raise AssertionError(f"Schema 2 missing required semantic column; expected one of {names}, got {tuple(row)}")


def run_cli(package: Path, *command: str, source_root: Path | None = None) -> subprocess.CompletedProcess[str]:
    arguments = ["uv", "run", "python", "-m", "analysis.validate_servo2", *command, "--package-root", str(package)]
    if source_root is not None:
        arguments.extend(("--source-root", str(source_root)))
    environment = {
        "PATH": os.environ["PATH"],
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "HOME": str(package.parent / ".empty-home"),
        "UV_CACHE_DIR": str(package.parent / ".uv-cache"),
        "PYTHONHASHSEED": "0",
    }
    return subprocess.run(
        arguments,
        cwd=REPOSITORY,
        env=environment,
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )


def assert_rejected(result: subprocess.CompletedProcess[str], code: str) -> None:
    output = f"{result.stdout}\n{result.stderr}"
    assert result.returncode != 0, f"mutation was accepted; expected {code}:\n{output}"
    assert code in output, f"failure did not expose stable diagnostic {code}:\n{output}"


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


@pytest.fixture()
def package(tmp_path: Path) -> Path:
    assert PUBLIC_PACKAGE.is_dir(), (
        "Schema 2 public package is missing; expected release/package. "
        "Do not substitute schema-1 fixtures."
    )
    destination = tmp_path / "package"
    shutil.copytree(PUBLIC_PACKAGE, destination)
    return destination


@pytest.fixture()
def valid_public(package: Path) -> Path:
    result = run_cli(package, "public-regeneration")
    assert result.returncode == 0, f"unmutated public package is invalid:\n{result.stdout}\n{result.stderr}"
    return package
