from __future__ import annotations

import csv
import hashlib
import json
import runpy
from pathlib import Path

from .servo2_io import Servo2Error, Table, read_json, sha256

MANIFEST_NAME = "servo2_public_manifest.json"


def find_manifest(root: Path) -> tuple[Path, dict[str, str | dict[str, str]]]:
    path = root / MANIFEST_NAME
    manifest = read_json(path)
    if "generated_artifact_sha256" not in manifest:
        raise Servo2Error("PUBLIC_MANIFEST_INVALID", "generated artifacts are unbound")
    return path, manifest


def regenerate(
    root: Path, tables: dict[str, Table], manifest: dict[str, str | dict[str, str]]
) -> None:
    generated = manifest.get(
        "generated_artifacts", manifest.get("generated_artifact_sha256")
    )
    if not isinstance(generated, dict) or not generated:
        raise Servo2Error("PUBLIC_MANIFEST_INVALID", "generated artifacts are unbound")
    expected_content = _derived_content(tables)
    rebuild_tables = False
    for name, expected_hash in sorted(generated.items()):
        path = _resolve_generated(root, name)
        content = expected_content.get(path.name)
        if content is None:
            if not path.is_file():
                rebuild_tables = True
                continue
            if sha256(path) != expected_hash:
                raise Servo2Error("STALE_GENERATED_ARTIFACT", name)
            continue
        digest = hashlib.sha256(content).hexdigest()
        if digest != expected_hash:
            raise Servo2Error(
                "PUBLIC_MANIFEST_INVALID",
                f"hash does not bind deterministic builder: {name}",
            )
        if path.exists():
            if path.read_bytes() != content:
                raise Servo2Error("STALE_GENERATED_ARTIFACT", name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    if rebuild_tables:
        generator = root / "analysis" / "build_servo2_tables.py"
        if not generator.is_file():
            raise Servo2Error("GENERATED_TABLE_BUILDER_MISSING", str(generator))
        runpy.run_path(str(generator), run_name="__main__")
        for name, expected_hash in sorted(generated.items()):
            path = _resolve_generated(root, name)
            if not path.is_file() or sha256(path) != expected_hash:
                raise Servo2Error("NONDETERMINISTIC_REBUILD", name)


def verify_canonical_inputs(
    root: Path, manifest: dict[str, str | dict[str, str]]
) -> None:
    expected = manifest.get("canonical_input_sha256")
    if not isinstance(expected, dict) or not expected:
        raise Servo2Error("PUBLIC_MANIFEST_INVALID", "canonical inputs are unbound")
    for name, digest in sorted(expected.items()):
        path = _safe_path(root, name)
        if not path.is_file() or sha256(path) != digest:
            raise Servo2Error("CANONICAL_INPUT_MISMATCH", name)


def verify_public_allowlist(
    root: Path, manifest: dict[str, str | dict[str, str]]
) -> None:
    expected = manifest.get("public_file_sha256")
    if not isinstance(expected, dict) or not expected:
        raise Servo2Error("PUBLIC_MANIFEST_INVALID", "public file allowlist is absent")
    generated = manifest.get("generated_artifact_sha256")
    if not isinstance(generated, dict):
        raise Servo2Error("PUBLIC_MANIFEST_INVALID", "generated artifacts are unbound")
    actual: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise Servo2Error(
                "PUBLIC_PACKAGE_SYMLINK_FORBIDDEN", path.relative_to(root).as_posix()
            )
        if path.is_file() and path.name != MANIFEST_NAME:
            relative = path.relative_to(root).as_posix()
            actual[relative] = sha256(path)
    unexpected = set(actual) - set(expected)
    missing = set(expected) - set(actual)
    if unexpected or not missing <= set(generated):
        raise Servo2Error(
            "PUBLIC_PACKAGE_ALLOWLIST_MISMATCH", "unknown or missing public file"
        )
    for name, digest in actual.items():
        if name not in generated and digest != expected[name]:
            raise Servo2Error("PUBLIC_FILE_CHECKSUM_MISMATCH", name)


def _derived_content(tables: dict[str, Table]) -> dict[str, bytes]:
    counts = {name: len(table.rows) for name, table in sorted(tables.items())}
    summary = (
        json.dumps(
            {"schema_version": "3.0.0", "record_counts": counts},
            ensure_ascii=True,
            indent=2,
            sort_keys=True,
        ).encode()
        + b"\n"
    )
    closure = _closure_csv(tables["closure_statuses"])
    return {"servo2_summary.json": summary, "servo2_closure_projection.csv": closure}


def _closure_csv(table: Table) -> bytes:
    lines: list[str] = []
    header = ("case_id", "predicate", "status")
    lines.append(",".join(header))
    for row in sorted(
        table.rows, key=lambda item: (item["case_id"], item["predicate"])
    ):
        values = tuple(row[field] for field in header)
        lines.append(_csv_line(values))
    return ("\n".join(lines) + "\n").encode()


def _csv_line(values: tuple[str, ...]) -> str:
    from io import StringIO

    output = StringIO(newline="")
    csv.writer(output, lineterminator="").writerow(values)
    return output.getvalue()


def _resolve_generated(root: Path, name: str) -> Path:
    relative = Path(name)
    if relative.is_absolute() or ".." in relative.parts:
        raise Servo2Error("PUBLIC_MANIFEST_PATH_ESCAPE", name)
    direct = root / relative
    analysis = root / "analysis" / relative
    if direct.exists() or "/" in name:
        selected = direct
    else:
        selected = analysis
    resolved = selected.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise Servo2Error("PUBLIC_MANIFEST_PATH_ESCAPE", name)
    return selected


def _safe_path(root: Path, name: str) -> Path:
    relative = Path(name)
    if relative.is_absolute() or ".." in relative.parts:
        raise Servo2Error("PUBLIC_MANIFEST_PATH_ESCAPE", name)
    path = root / relative
    if not path.resolve().is_relative_to(root.resolve()):
        raise Servo2Error("PUBLIC_MANIFEST_PATH_ESCAPE", name)
    return path
