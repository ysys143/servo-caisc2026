from __future__ import annotations

from conftest import assert_rejected, column, csv_rows, run_cli, table, write_rows


def test_domain_anchor_row_cannot_merge_multiple_systems(package) -> None:
    path = table(package, "domain_anchors")
    header, rows = csv_rows(path)
    system = column(rows[0], "system_id", "record_id", "system")
    rows[0][system] = rows[0][system] + ";another-system"
    write_rows(path, header, rows)
    assert_rejected(run_cli(package, "public-regeneration"), "DOMAIN_ANCHOR_MULTI_SYSTEM")


def test_exactly_seven_domain_anchors_are_required(package) -> None:
    path = table(package, "domain_anchors")
    header, rows = csv_rows(path)
    assert len(rows) == 7, "positive Schema 2 package must freeze exactly seven anchors"
    write_rows(path, header, rows[:-1])
    assert_rejected(run_cli(package, "public-regeneration"), "DOMAIN_ANCHOR_COUNT_MISMATCH")


def test_formal_math_anchor_cannot_be_double_counted(package) -> None:
    path = table(package, "domain_anchors")
    header, rows = csv_rows(path)
    domain = column(rows[0], "domain", "domain_id")
    math_row = next(row for row in rows if "math" in row[domain].lower() or "formal" in row[domain].lower())
    other = next(row for row in rows if row is not math_row)
    other[domain] = math_row[domain]
    write_rows(path, header, rows)
    assert_rejected(run_cli(package, "public-regeneration"), "DOMAIN_ANCHOR_MATH_DOUBLE_COUNT")


def test_legacy_fields_cannot_leak_into_schema2(package) -> None:
    path = table(package, "cases")
    header, rows = csv_rows(path)
    header.append("A_Vcompleteness")
    for row in rows:
        row["A_Vcompleteness"] = "3"
    write_rows(path, header, rows)
    assert_rejected(run_cli(package, "public-regeneration"), "LEGACY_FIELD_FORBIDDEN")
