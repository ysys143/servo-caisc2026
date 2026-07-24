"""Deterministic builder for ``caisc2026-servo-supplement.zip`` (M8).

The shell ``zip -r`` command records each entry's on-disk mtime, so its
SHA-256 changes on every checkout even when file *contents* are identical.
That makes the archive leaf hash unbindable in a provenance chain.

This builder reproduces the same file set (``analysis/`` recursively plus
``references.bib`` and ``SUPPLEMENT_README.md``, minus the same exclusions
the Makefile uses) but writes every entry with a fixed timestamp, fixed
external attributes, sorted member order, and a fixed DEFLATE level. Given a
fixed zlib build the resulting archive is byte-reproducible, so its leaf
SHA-256 is a stable, bindable value.

Scope note: byte reproducibility of the *compressed container* holds for a
fixed zlib version on one machine; the DEFLATE stream can differ across zlib
builds. The per-file content hashes that the provenance root binds are
content-based and therefore fully portable -- only the container leaf hash
carries the same-zlib caveat.
"""

from __future__ import annotations

import fnmatch
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from .servo_v5_io import sha256

# Members of the supplement archive, expressed relative to the submission root.
ZIP_NAME = "caisc2026-servo-supplement.zip"
TOP_LEVEL_FILES = ("references.bib", "SUPPLEMENT_README.md")
ANALYSIS_DIR_NAME = "analysis"

# Exclusion globs, mirroring the Makefile `zip -x` patterns. Matched against
# the archive member path (posix) with `*` spanning directory separators, as
# Info-ZIP does.
EXCLUDE_GLOBS = (
    "*/.cwf/*",
    "*/.omc/*",
    "*/.git/*",
    "*/.DS_Store",
    ".DS_Store",
    "analysis/texput.log",
    "*/__pycache__/*",
    "*/.pytest_cache/*",
    "*.pyc",
    ZIP_NAME,
)

# Fixed metadata for every entry (byte-stability). 1980-01-01 is the ZIP epoch
# floor; 0o644 regular-file permissions in the high 16 bits of external_attr.
_FIXED_DATE_TIME = (1980, 1, 1, 0, 0, 0)
_FIXED_EXTERNAL_ATTR = 0o644 << 16
_COMPRESSLEVEL = 6


def _excluded(member: str) -> bool:
    return any(fnmatch.fnmatch(member, pat) for pat in EXCLUDE_GLOBS)


def collect_members(submission_root: Path) -> list[str]:
    """Return the sorted archive-relative member paths, exclusions applied."""
    members: list[str] = []
    for name in TOP_LEVEL_FILES:
        if (submission_root / name).is_file() and not _excluded(name):
            members.append(name)
    analysis_root = submission_root / ANALYSIS_DIR_NAME
    for path in analysis_root.rglob("*"):
        if not path.is_file():
            continue
        member = path.relative_to(submission_root).as_posix()
        if _excluded(member):
            continue
        members.append(member)
    return sorted(members)


def build_supplement_zip(submission_root: Path, out_path: Path | None = None) -> str:
    """Write the deterministic supplement zip and return its SHA-256."""
    submission_root = submission_root.resolve()
    if out_path is None:
        out_path = submission_root / ZIP_NAME
    members = collect_members(submission_root)
    # Write to a temporary path first so a failure never leaves a partial zip.
    tmp_path = out_path.with_name(out_path.name + ".tmp")
    with ZipFile(tmp_path, "w", compression=ZIP_DEFLATED, compresslevel=_COMPRESSLEVEL) as archive:
        for member in members:
            info = ZipInfo(filename=member, date_time=_FIXED_DATE_TIME)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = _FIXED_EXTERNAL_ATTR
            info.create_system = 3  # unix, fixed
            data = (submission_root / member).read_bytes()
            archive.writestr(info, data)
    tmp_path.replace(out_path)
    return sha256(out_path)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(prog="servo-v5-supplement-zip")
    parser.add_argument(
        "--submission-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="submission/ directory (default: parent of analysis/)",
    )
    options = parser.parse_args()
    digest = build_supplement_zip(options.submission_root)
    print(f"SERVO_V5_SUPPLEMENT_ZIP_OK: {ZIP_NAME} sha256={digest}")


if __name__ == "__main__":
    main()
