from __future__ import annotations

from pathlib import Path

from .servo2_io import Servo2Error, Table


def validate_schema_contract(root: Path, tables: dict[str, Table]) -> None:
    schema = root / "analysis" / "servo_schema.yaml"
    try:
        lines = schema.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as error:
        raise Servo2Error("SCHEMA_CONTRACT_MISSING", str(schema)) from error
    headers = _mapping(lines, "table_headers")
    enums = _mapping(lines, "enum_fields")
    booleans = _mapping(lines, "boolean_fields")
    if set(headers) != set(tables):
        raise Servo2Error("SCHEMA_TABLE_SET_MISMATCH", _difference(headers, tables))
    for name, table in tables.items():
        expected = headers[name]
        if table.header != expected:
            raise Servo2Error("SCHEMA_HEADER_MISMATCH", name)
    for reference, allowed in enums.items():
        table_name, field = _reference(reference, tables)
        for row in tables[table_name].rows:
            value = row[field]
            values = value.split(";") if ";" in value else [value]
            if any(item not in allowed for item in values):
                raise Servo2Error("SCHEMA_ENUM_INVALID", f"{reference}={value}")
    for table_name, fields in booleans.items():
        if table_name not in tables:
            raise Servo2Error("SCHEMA_BOOLEAN_TABLE_UNKNOWN", table_name)
        for field in fields:
            if field not in tables[table_name].header:
                raise Servo2Error(
                    "SCHEMA_BOOLEAN_FIELD_UNKNOWN", f"{table_name}.{field}"
                )
            for row in tables[table_name].rows:
                if row[field] not in {"true", "false"}:
                    raise Servo2Error(
                        "SCHEMA_BOOLEAN_INVALID", f"{table_name}.{field}={row[field]}"
                    )


def _mapping(lines: list[str], section: str) -> dict[str, tuple[str, ...]]:
    marker = f"{section}:"
    try:
        start = lines.index(marker) + 1
    except ValueError as error:
        raise Servo2Error("SCHEMA_DECLARATION_MISSING", section) from error
    result: dict[str, tuple[str, ...]] = {}
    for line in lines[start:]:
        if line and not line.startswith(" "):
            break
        if not line.startswith("  ") or line.startswith("    "):
            continue
        key, separator, raw = line.strip().partition(":")
        if (
            separator == ""
            or not raw.strip().startswith("[")
            or not raw.strip().endswith("]")
        ):
            raise Servo2Error("SCHEMA_DECLARATION_INVALID", f"{section}:{line}")
        values = tuple(item.strip() for item in raw.strip()[1:-1].split(","))
        if not key or not values or any(not value for value in values):
            raise Servo2Error("SCHEMA_DECLARATION_INVALID", f"{section}:{line}")
        result[key] = values
    if not result:
        raise Servo2Error("SCHEMA_DECLARATION_MISSING", section)
    return result


def _reference(reference: str, tables: dict[str, Table]) -> tuple[str, str]:
    table_name, separator, field = reference.partition(".")
    if (
        separator == ""
        or table_name not in tables
        or field not in tables[table_name].header
    ):
        raise Servo2Error("SCHEMA_ENUM_FIELD_UNKNOWN", reference)
    return table_name, field


def _difference(declared: dict[str, tuple[str, ...]], tables: dict[str, Table]) -> str:
    return f"declared={sorted(declared)} loaded={sorted(tables)}"
