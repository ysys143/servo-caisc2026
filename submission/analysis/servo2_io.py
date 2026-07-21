from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


TABLES = (
    "cases",
    "endpoints",
    "artifacts",
    "events",
    "edges",
    "reliability",
    "closure_witnesses",
    "closure_statuses",
    "domain_anchors",
    "domain_anchor_channels",
    "selection_ledger",
)
SCHEMA_VERSION = "3.0.0"


@dataclass(frozen=True, slots=True)
class Table:
    name: str
    header: tuple[str, ...]
    rows: tuple[dict[str, str], ...]


class Servo2Error(Exception):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code


def read_table(root: Path, name: str) -> Table:
    path = root / "analysis" / f"servo2_{name}.csv"
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise Servo2Error("CSV_HEADER_MISSING", name)
            rows = tuple(dict(row) for row in reader)
            return Table(name, tuple(reader.fieldnames), rows)
    except FileNotFoundError as error:
        raise Servo2Error("CANONICAL_TABLE_MISSING", name) from error


def read_tables(root: Path) -> dict[str, Table]:
    return {name: read_table(root, name) for name in TABLES}


def require(row: dict[str, str], field: str, table: str) -> str:
    value = row.get(field)
    if value is None:
        raise Servo2Error("SCHEMA_FIELD_MISSING", f"{table}.{field}")
    return value


def split_values(value: str) -> tuple[str, ...]:
    if value in {"", "not_applicable", "none"}:
        return ()
    return tuple(part for part in value.split(";") if part)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict[str, str | dict[str, str]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as error:
        raise Servo2Error("PUBLIC_MANIFEST_INVALID", str(path)) from error
    if not isinstance(value, dict):
        raise Servo2Error("PUBLIC_MANIFEST_INVALID", str(path))
    result: dict[str, str | dict[str, str]] = {}
    for key, item in value.items():
        if isinstance(item, str):
            result[str(key)] = item
        elif isinstance(item, dict) and all(
            isinstance(name, str) and isinstance(digest, str)
            for name, digest in item.items()
        ):
            result[str(key)] = {str(name): str(digest) for name, digest in item.items()}
    return result
