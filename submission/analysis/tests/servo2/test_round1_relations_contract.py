from __future__ import annotations

from conftest import assert_rejected, csv_rows, run_cli, table, write_rows


def _add_decision_basis_contract(package) -> tuple[list[str], list[dict[str, str]]]:
    path = table(package, "closure_statuses")
    header, rows = csv_rows(path)
    if "decision_basis" not in header:
        header.append("decision_basis")
    defaults = {
        "established": "positive_witness",
        "not_established": "explicit_negative",
        "unknown": "insufficient_reporting",
        "not_applicable": "out_of_scope",
    }
    for row in rows:
        row["decision_basis"] = defaults[row["status"]]
    schema_path = package / "analysis" / "servo_schema.yaml"
    schema = schema_path.read_text(encoding="utf-8")
    schema = schema.replace(
        "closure_statuses: [schema_version, case_id, predicate, status, witness_ids, rationale]",
        "closure_statuses: [schema_version, case_id, predicate, status, witness_ids, rationale, decision_basis]",
    )
    schema_path.write_text(schema, encoding="utf-8")
    return header, rows


def test_exact_case_and_lineage_cardinality_is_enforced(package) -> None:
    path = table(package, "cases")
    header, rows = csv_rows(path)
    write_rows(path, header, rows[:-1])
    assert_rejected(run_cli(package, "public-regeneration"), "CASE_LINEAGE_CARDINALITY")


def test_established_closure_requires_same_predicate_witness(package) -> None:
    path = table(package, "closure_statuses")
    header, rows = csv_rows(path)
    target = next(row for row in rows if row["predicate"] == "artifact_revision")
    target["witness_ids"] = "W09"
    write_rows(path, header, rows)
    assert_rejected(
        run_cli(package, "public-regeneration"), "CLOSURE_WITNESS_STATUS_MISMATCH"
    )


def test_not_established_rejects_insufficient_reporting_basis(package) -> None:
    header, rows = _add_decision_basis_contract(package)
    target = next(row for row in rows if row["status"] == "not_established")
    target["decision_basis"] = "insufficient_reporting"
    write_rows(table(package, "closure_statuses"), header, rows)

    assert_rejected(
        run_cli(package, "public-regeneration"), "CLOSURE_STATUS_BASIS_MISMATCH"
    )


def test_unknown_rejects_explicit_negative_basis(package) -> None:
    header, rows = _add_decision_basis_contract(package)
    target = next(row for row in rows if row["status"] == "unknown")
    target["decision_basis"] = "explicit_negative"
    write_rows(table(package, "closure_statuses"), header, rows)

    assert_rejected(
        run_cli(package, "public-regeneration"), "CLOSURE_STATUS_BASIS_MISMATCH"
    )


def test_discovery_witness_rejects_truncated_event_sequence(package) -> None:
    path = table(package, "closure_witnesses")
    header, rows = csv_rows(path)
    target = next(row for row in rows if row["predicate"] == "discovery_cycle_feedback")
    target["ordered_event_ids"] = target["ordered_event_ids"].split(";")[0]
    write_rows(path, header, rows)
    assert_rejected(
        run_cli(package, "public-regeneration"),
        "DISCOVERY_WITNESS_EVENT_SEQUENCE_INVALID",
    )


def test_discovery_witness_rejects_reordered_edges(package) -> None:
    path = table(package, "closure_witnesses")
    header, rows = csv_rows(path)
    target = next(row for row in rows if row["predicate"] == "discovery_cycle_feedback")
    edges = target["ordered_edge_ids"].split(";")
    edges[1], edges[2] = edges[2], edges[1]
    target["ordered_edge_ids"] = ";".join(edges)
    write_rows(path, header, rows)
    assert_rejected(
        run_cli(package, "public-regeneration"), "DISCOVERY_WITNESS_PATH_UNCONNECTED"
    )


def test_artifact_must_appear_in_producer_event_output(package) -> None:
    artifact_path = table(package, "artifacts")
    _, artifacts = csv_rows(artifact_path)
    artifact = artifacts[0]
    event_path = table(package, "events")
    header, events = csv_rows(event_path)
    producer = next(
        row for row in events if row["event_id"] == artifact["producer_event_id"]
    )
    producer["output_artifact_ids"] = "not_applicable"
    write_rows(event_path, header, events)
    assert_rejected(
        run_cli(package, "public-regeneration"), "ARTIFACT_NOT_IN_PRODUCER_OUTPUT"
    )


def test_artifact_predecessor_version_must_increment(package) -> None:
    path = table(package, "artifacts")
    header, rows = csv_rows(path)
    target = next(
        row for row in rows if row["predecessor_artifact_id"] != "not_applicable"
    )
    target["version"] = "99"
    write_rows(path, header, rows)
    assert_rejected(
        run_cli(package, "public-regeneration"),
        "ARTIFACT_PREDECESSOR_VERSION_INVALID",
    )
