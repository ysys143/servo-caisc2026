from __future__ import annotations

import pytest

from analysis.servo2_io import Servo2Error, Table, read_tables
from analysis.servo2_relations import validate_relations

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
    target = next(row for row in rows if row["status"] == "unknown")
    target["status"] = "not_established"
    target["decision_basis"] = "insufficient_reporting"
    write_rows(table(package, "closure_statuses"), header, rows)

    assert_rejected(
        run_cli(package, "public-regeneration"), "CLOSURE_STATUS_BASIS_MISMATCH"
    )


def test_not_established_rejects_unverified_complete_trace_claim(package) -> None:
    header, rows = _add_decision_basis_contract(package)
    target = next(row for row in rows if row["status"] == "unknown")
    target["status"] = "not_established"
    target["decision_basis"] = "complete_trace_failure"
    write_rows(table(package, "closure_statuses"), header, rows)

    assert_rejected(
        run_cli(package, "public-regeneration"), "SCHEMA_ENUM_INVALID"
    )


def test_not_established_requires_source_grounded_evidence_id(package) -> None:
    # Given: a source-silent unknown row relabelled as explicitly negative.
    tables = read_tables(package)
    rows = tables["closure_statuses"].rows
    for row in rows:
        row["evidence_ids"] = "not_applicable"
    target = next(row for row in rows if row["status"] == "unknown")
    target["status"] = "not_established"
    target["decision_basis"] = "explicit_negative"

    # When/Then: a decision-basis token cannot substitute for source evidence.
    with pytest.raises(Servo2Error, match="NEGATIVE_STATUS_EVIDENCE_MISSING"):
        validate_relations(tables)


def test_not_applicable_requires_explicit_scope_rationale(package) -> None:
    # Given: the sole out-of-scope row with its rationale erased.
    tables = read_tables(package)
    rows = tables["closure_statuses"].rows
    target = next(row for row in rows if row["status"] == "not_applicable")
    target["rationale"] = ""

    # When/Then: not-applicable cannot be asserted without the predeclared reason.
    with pytest.raises(Servo2Error, match="CLOSURE_STATUS_RATIONALE_MISSING"):
        validate_relations(tables)


def test_closure_matrix_rejects_duplicate_case_predicate_cell(package) -> None:
    # Given: a duplicated cell in the frozen case-by-predicate matrix.
    tables = read_tables(package)
    rows = tables["closure_statuses"].rows
    rows[1].update(rows[0])

    # When/Then: the composite key must remain unique.
    with pytest.raises(Servo2Error, match="CLOSURE_STATUS_DUPLICATE"):
        validate_relations(tables)


def test_closure_matrix_rejects_missing_case_predicate_cell(package) -> None:
    # Given: one matrix cell removed without changing the six frozen cases.
    tables = read_tables(package)
    table = tables["closure_statuses"]
    tables["closure_statuses"] = type(table)(table.name, table.header, table.rows[:-1])

    # When/Then: every case must retain all four predicate decisions.
    with pytest.raises(Servo2Error, match="CLOSURE_STATUS_MATRIX_INCOMPLETE"):
        validate_relations(tables)


def test_negative_status_rejects_existing_positive_witness(package) -> None:
    # Given: an established cell relabelled negative while its witness remains canonical.
    tables = read_tables(package)
    target = next(
        row for row in tables["closure_statuses"].rows if row["status"] == "established"
    )
    target["status"] = "not_established"
    target["witness_ids"] = "not_applicable"
    target["decision_basis"] = "explicit_negative"
    target["evidence_ids"] = "R01-E01"

    # When/Then: a positive canonical witness and negative cell cannot coexist.
    with pytest.raises(Servo2Error, match="CLOSURE_STATUS_WITNESS_CONTRADICTION"):
        validate_relations(tables)


def test_execution_repair_requires_established_artifact_revision(package) -> None:
    tables = read_tables(package)
    rows = tables["closure_statuses"].rows
    target = next(
        row
        for row in rows
        if row["case_id"] == "C01" and row["predicate"] == "artifact_revision"
    )
    target["status"] = "unknown"
    target["witness_ids"] = "not_applicable"
    target["decision_basis"] = "insufficient_reporting"
    witness_table = tables["closure_witnesses"]
    tables["closure_witnesses"] = type(witness_table)(
        witness_table.name,
        witness_table.header,
        [row for row in witness_table.rows if row["witness_id"] != "W15"],
    )

    with pytest.raises(Servo2Error, match="CLOSURE_STATUS_IMPLICATION_VIOLATION"):
        validate_relations(tables)


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
    _, witnesses = csv_rows(table(package, "closure_witnesses"))
    referenced_events = {
        occurrence.split("@")[0]
        for witness in witnesses
        for occurrence in witness["ordered_event_ids"].split(";")
    }
    target = next(
        row
        for row in rows
        if row["predecessor_artifact_id"] != "not_applicable"
        and row["producer_event_id"] not in referenced_events
    )
    target["version"] = "99"
    write_rows(path, header, rows)
    assert_rejected(
        run_cli(package, "public-regeneration"),
        "ARTIFACT_PREDECESSOR_VERSION_INVALID",
    )


def test_distinct_artifact_lineages_may_share_version_number(package) -> None:
    tables = read_tables(package)
    source = next(
        row
        for row in tables["artifacts"].rows
        if row["artifact_id"] == "C02.result.v1"
    )
    clone = dict(source)
    clone["artifact_id"] = "C02.result.branch-b.v1"
    clone["artifact_lineage_id"] = "C02.result.branch-b"
    artifacts = tables["artifacts"]
    tables["artifacts"] = Table(
        artifacts.name,
        artifacts.header,
        artifacts.rows + (clone,),
    )
    producer = next(
        row
        for row in tables["events"].rows
        if row["event_id"] == clone["producer_event_id"]
    )
    producer["output_artifact_ids"] += ";" + clone["artifact_id"]
    validate_relations(tables)


def test_successor_cannot_cross_artifact_lineage(package) -> None:
    tables = read_tables(package)
    target = next(
        row
        for row in tables["artifacts"].rows
        if row["artifact_id"] == "C04.code.v2"
    )
    target["artifact_lineage_id"] = "C04.unrelated"
    with pytest.raises(Servo2Error, match="ARTIFACT_PREDECESSOR_VERSION_INVALID"):
        validate_relations(tables)
