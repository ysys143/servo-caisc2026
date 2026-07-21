from __future__ import annotations

from pathlib import Path

from .servo2_graph import validate_graph
from .servo2_io import Servo2Error, Table, require, split_values
from .servo2_relations import validate_relations


FORBIDDEN_FIELDS = {
    "A_Vcompleteness",
    "V_completeness",
    "novelty_gate",
    "loop_closed",
    "H",
}
FROZEN_ANCHORS = {
    "FunSearch",
    "AI Feynman",
    "ChemCrow",
    "GNoME",
    "BioPlanner",
    "Manning automated social science",
    "AutoML-Zero",
}


def validate_public_paths(root: Path) -> None:
    forbidden_names = {".cache", ".env", ".git", ".venv", "__pycache__"}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise Servo2Error("PUBLIC_PACKAGE_SYMLINK_FORBIDDEN", relative)
        if (
            path.name in forbidden_names
            or "raw-log" in path.name
            or "cache" in path.parts
            or path.suffix in {".pyc", ".pyo"}
        ):
            raise Servo2Error("PUBLIC_PACKAGE_FORBIDDEN_PATH", relative)


def validate_tables(tables: dict[str, Table]) -> None:
    _validate_versions(tables)
    _validate_legacy_fields(tables)
    _validate_anchors(tables["domain_anchors"])
    _validate_artifacts(tables["artifacts"], tables["events"])
    validate_graph(tables)
    validate_relations(tables)


def validate_legacy_headers(tables: dict[str, Table]) -> None:
    _validate_legacy_fields(tables)


def _validate_versions(tables: dict[str, Table]) -> None:
    for table in tables.values():
        for row in table.rows:
            if require(row, "schema_version", table.name) != "3.0.0":
                raise Servo2Error("SCHEMA_VERSION_MISMATCH", table.name)


def _validate_legacy_fields(tables: dict[str, Table]) -> None:
    for table in tables.values():
        leaked = FORBIDDEN_FIELDS & set(table.header)
        if leaked:
            raise Servo2Error(
                "LEGACY_FIELD_FORBIDDEN", f"{table.name}:{sorted(leaked)}"
            )


def _validate_anchors(table: Table) -> None:
    if len(table.rows) != 7:
        raise Servo2Error("DOMAIN_ANCHOR_COUNT_MISMATCH", str(len(table.rows)))
    systems: list[str] = []
    for row in table.rows:
        system = require(row, "system", table.name)
        if len(split_values(system)) != 1:
            raise Servo2Error("DOMAIN_ANCHOR_MULTI_SYSTEM", system)
        systems.append(system)
    math_count = sum(
        "math" in require(row, "domain", table.name).lower()
        or "formal" in require(row, "domain", table.name).lower()
        for row in table.rows
    )
    if math_count != 1:
        raise Servo2Error("DOMAIN_ANCHOR_MATH_DOUBLE_COUNT", str(math_count))
    if set(systems) != FROZEN_ANCHORS:
        raise Servo2Error("DOMAIN_ANCHOR_SET_MISMATCH", ";".join(systems))


def _validate_artifacts(table: Table, event_table: Table) -> None:
    events = {
        require(row, "event_id", event_table.name): row for row in event_table.rows
    }
    for row in table.rows:
        producer = require(row, "producer_event_id", table.name)
        event = events.get(producer)
        if event is None:
            raise Servo2Error(
                "ARTIFACT_PRODUCER_MISSING", require(row, "artifact_id", table.name)
            )
        if require(event, "case_id", event_table.name) != require(
            row, "case_id", table.name
        ):
            raise Servo2Error(
                "ARTIFACT_PRODUCER_CASE_MISMATCH",
                require(row, "artifact_id", table.name),
            )
        produced = _sequence(row, "producer_sequence", table.name)
        consumed = _sequence(row, "first_consumed_sequence", table.name)
        if consumed is not None and produced is not None and consumed < produced:
            raise Servo2Error(
                "FUTURE_ARTIFACT_CONSUMPTION", require(row, "artifact_id", table.name)
            )


def _sequence(row: dict[str, str], field: str, table: str) -> int | None:
    value = require(row, field, table)
    if value in {"", "not_applicable", "not_reported"}:
        return None
    try:
        return int(value)
    except ValueError as error:
        raise Servo2Error("SEQUENCE_INVALID", f"{table}.{field}={value}") from error


def validate_public_privacy(
    root: Path, manifest: dict[str, str | dict[str, str]]
) -> None:
    if "source_root" in manifest or "undeclared_input" in manifest:
        raise Servo2Error(
            "PUBLIC_EXTERNAL_READ_FORBIDDEN", "manifest declares an external input"
        )
    allowed_pdf = "servo_caiscfp2026_post-submit.pdf"
    markers = (
        b"/" + b"Users/",
        b"C:\\" + b"Users\\",
        b"OPENAI" + b"_API_KEY",
        b"ANTHROPIC" + b"_API_KEY",
        b"GEMINI" + b"_API_KEY",
        b"sk" + b"-proj-",
        b"sk" + b"-live-",
    )
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise Servo2Error(
                "PUBLIC_PACKAGE_SYMLINK_FORBIDDEN", path.relative_to(root).as_posix()
            )
        if not path.is_file():
            continue
        if path.suffix.lower() == ".pdf" and path.name != allowed_pdf:
            raise Servo2Error(
                "PUBLIC_PACKAGE_PRIVACY_LEAK", path.relative_to(root).as_posix()
            )
        raw = path.read_bytes()
        if any(marker in raw for marker in markers):
            raise Servo2Error(
                "PUBLIC_PACKAGE_PRIVACY_LEAK", path.relative_to(root).as_posix()
            )
