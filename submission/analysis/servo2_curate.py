from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from .servo2_io import SCHEMA_VERSION, Servo2Error, sha256


def curate(package_root: Path, source_root: Path, destination: Path) -> None:
    if not source_root.is_dir():
        raise Servo2Error("SOURCE_BYTE_AUDIT_MISMATCH", "source root is absent")
    if destination.exists() and any(destination.iterdir()):
        raise Servo2Error("CURATED_SOURCE_DESTINATION_NOT_EMPTY", str(destination))
    destination.mkdir(parents=True, exist_ok=True)
    registry_path = package_root / "analysis" / "source_registry.json"
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))["sources"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise Servo2Error("SOURCE_REGISTRY_INVALID", str(registry_path)) from error
    candidates: dict[str, list[Path]] = {}
    for path in sorted(source_root.rglob("*")):
        if path.is_symlink():
            raise Servo2Error(
                "SOURCE_BYTE_AUDIT_SYMLINK_ESCAPE",
                path.relative_to(source_root).as_posix(),
            )
        if path.is_file() and path.suffix.lower() == ".pdf":
            digest = sha256(path)
            candidates.setdefault(digest, []).append(path)
    copied: list[dict[str, str]] = []
    for entry in registry:
        digest = entry["pdf_sha256"]
        matches = candidates.get(digest, [])
        if not matches:
            raise Servo2Error("SOURCE_BYTE_AUDIT_MISMATCH", entry["record_id"])
        filename = entry["filename_hint"]
        target = destination / filename
        if target.parent != destination or target.exists():
            raise Servo2Error("CURATED_SOURCE_FILENAME_INVALID", filename)
        shutil.copyfile(matches[0], target)
        copied.append(
            {
                "record_id": entry["record_id"],
                "filename": filename,
                "pdf_sha256": digest,
            }
        )
    manifest = {"schema_version": SCHEMA_VERSION, "sources": copied}
    (destination / "curated_source_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser(prog="servo2-curate")
    parser.add_argument("--package-root", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    options = parser.parse_args()
    try:
        curate(options.package_root, options.source_root, options.destination)
    except Servo2Error as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
