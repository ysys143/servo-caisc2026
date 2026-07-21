from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .servo2_audit import audit_source_bytes
from .servo2_build import (
    find_manifest,
    regenerate,
    verify_canonical_inputs,
    verify_public_allowlist,
)
from .servo2_evidence import validate_evidence
from .servo2_io import Servo2Error, read_tables
from .servo2_release import (
    verify_manifest_schema,
    verify_release_ready,
    verify_repository_pdf_sync,
)
from .servo2_schema import validate_schema_contract
from .servo2_validate import (
    validate_legacy_headers,
    validate_public_paths,
    validate_public_privacy,
    validate_tables,
)


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(prog="validate-servo2")
    commands = value.add_subparsers(dest="mode", required=True)
    public = commands.add_parser("public-regeneration")
    public.add_argument("--package-root", type=Path, required=True)
    audit = commands.add_parser("source-byte-audit")
    audit.add_argument("--package-root", type=Path, required=True)
    audit.add_argument("--source-root", type=Path, required=True)
    ready = commands.add_parser("release-ready")
    ready.add_argument("--package-root", type=Path, required=True)
    sync = commands.add_parser("repository-sync")
    sync.add_argument("--package-root", type=Path, required=True)
    sync.add_argument("--reader-pdf", type=Path, required=True)
    return value


def run(arguments: list[str]) -> int:
    options = parser().parse_args(arguments)
    package_root: Path = options.package_root.resolve()
    try:
        if options.mode == "repository-sync":
            verify_repository_pdf_sync(options.reader_pdf.resolve(), package_root)
            print(f"SERVO2_OK: {options.mode}")
            return 0
        if options.mode in {"public-regeneration", "release-ready"}:
            validate_public_paths(package_root)
        tables = read_tables(package_root)
        validate_legacy_headers(tables)
        validate_schema_contract(package_root, tables)
        validate_tables(tables)
        validate_evidence(package_root, tables)
        if options.mode in {"public-regeneration", "release-ready"}:
            _, manifest = find_manifest(package_root)
            verify_manifest_schema(manifest)
            validate_public_privacy(package_root, manifest)
            verify_canonical_inputs(package_root, manifest)
            regenerate(package_root, tables, manifest)
            if options.mode == "release-ready":
                verify_release_ready(package_root, manifest)
            verify_public_allowlist(package_root, manifest)
        elif options.mode == "source-byte-audit":
            source_root: Path = options.source_root.resolve()
            audit_source_bytes(source_root, tables)
        else:
            raise Servo2Error("MODE_INVALID", str(options.mode))
    except Servo2Error as error:
        print(str(error), file=sys.stderr)
        return 1
    print(f"SERVO2_OK: {options.mode}")
    return 0


def main() -> None:
    raise SystemExit(run(sys.argv[1:]))


if __name__ == "__main__":
    main()
