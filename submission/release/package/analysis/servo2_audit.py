from __future__ import annotations

from pathlib import Path

from .servo2_io import Servo2Error, Table, sha256


def audit_source_bytes(source_root: Path, tables: dict[str, Table]) -> None:
    if not source_root.is_dir():
        raise Servo2Error("SOURCE_BYTE_AUDIT_MISMATCH", "source root is absent")
    expected = {
        row["source_pdf_sha256"]
        for table_name in ("cases", "domain_anchors")
        for row in tables[table_name].rows
        if row.get("source_pdf_sha256")
    }
    observed: dict[str, int] = {}
    root = source_root.resolve()
    try:
        for path in sorted(source_root.rglob("*")):
            if path.is_symlink():
                raise Servo2Error(
                    "SOURCE_BYTE_AUDIT_SYMLINK_ESCAPE",
                    path.relative_to(source_root).as_posix(),
                )
            if path.is_file() and path.suffix.lower() == ".pdf":
                resolved = path.resolve()
                if not resolved.is_relative_to(root):
                    raise Servo2Error(
                        "SOURCE_BYTE_AUDIT_SYMLINK_ESCAPE",
                        path.relative_to(source_root).as_posix(),
                    )
                digest = sha256(path)
                observed[digest] = observed.get(digest, 0) + 1
    except PermissionError as error:
        raise Servo2Error(
            "SOURCE_BYTE_AUDIT_MISMATCH", "source corpus is unreadable"
        ) from error
    duplicates = {digest for digest in expected if observed.get(digest, 0) > 1}
    if duplicates:
        raise Servo2Error(
            "SOURCE_BYTE_AUDIT_DUPLICATE",
            f"{len(duplicates)} sealed hashes occur more than once",
        )
    missing = {digest for digest in expected if observed.get(digest, 0) != 1}
    if missing:
        raise Servo2Error(
            "SOURCE_BYTE_AUDIT_MISMATCH", f"missing {len(missing)} sealed source files"
        )
