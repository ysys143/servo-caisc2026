from __future__ import annotations

import copy

from conftest import assert_rejected, csv_rows, run_cli, table, write_rows


def test_non_discovery_witness_rejects_cross_context(package) -> None:
    path = table(package, "closure_witnesses")
    header, rows = csv_rows(path)
    target = next(row for row in rows if row["predicate"] == "execution_repair")
    target["configuration_id"] += "-forged"
    write_rows(path, header, rows)
    assert_rejected(run_cli(package, "public-regeneration"), "CROSS_CONTEXT_CLOSURE_EDGE")


def test_non_discovery_witness_rejects_disconnected_path(package) -> None:
    path = table(package, "closure_witnesses")
    header, rows = csv_rows(path)
    target = next(row for row in rows if row["predicate"] == "execution_repair")
    endpoints = target["ordered_endpoint_ids"].split(";")
    endpoints[1], endpoints[2] = endpoints[2], endpoints[1]
    target["ordered_endpoint_ids"] = ";".join(endpoints)
    write_rows(path, header, rows)
    assert_rejected(
        run_cli(package, "public-regeneration"), "CLOSURE_WITNESS_PATH_UNCONNECTED"
    )


def test_non_discovery_witness_rejects_unlisted_source_event(package) -> None:
    witness_path = table(package, "closure_witnesses")
    _, witnesses = csv_rows(witness_path)
    target = next(row for row in witnesses if row["predicate"] == "execution_repair")
    edge_id = target["ordered_edge_ids"].split(";")[0]
    edge_path = table(package, "edges")
    header, edges = csv_rows(edge_path)
    edge = next(row for row in edges if row["edge_id"] == edge_id)
    events_path = table(package, "events")
    _, events = csv_rows(events_path)
    replacement = next(
        row
        for row in events
        if row["case_id"] == edge["case_id"]
        and row["configuration_id"] == edge["configuration_id"]
        and row["task_regime_id"] == edge["task_regime_id"]
        and row["event_id"] not in target["ordered_event_ids"]
    )
    edge["source_event_id"] = replacement["event_id"]
    write_rows(edge_path, header, edges)
    assert_rejected(
        run_cli(package, "public-regeneration"), "CLOSURE_WITNESS_EVENT_EDGE_MISMATCH"
    )


def test_artifact_endpoint_must_match_producer_event(package) -> None:
    artifact_path = table(package, "artifacts")
    header, artifacts = csv_rows(artifact_path)
    target = artifacts[0]
    endpoint_path = table(package, "endpoints")
    _, endpoints = csv_rows(endpoint_path)
    target["producer_endpoint_id"] = next(
        row["endpoint_id"]
        for row in endpoints
        if row["case_id"] == target["case_id"]
        and row["endpoint_id"] != target["producer_endpoint_id"]
    )
    write_rows(artifact_path, header, artifacts)
    assert_rejected(
        run_cli(package, "public-regeneration"), "ARTIFACT_PRODUCER_ENDPOINT_MISMATCH"
    )


def test_domain_channel_anchor_foreign_key_is_enforced(package) -> None:
    path = table(package, "domain_anchor_channels")
    header, rows = csv_rows(path)
    rows[0]["anchor_id"] = "DA99"
    write_rows(path, header, rows)
    assert_rejected(
        run_cli(package, "public-regeneration"), "ANCHOR_CHANNEL_FOREIGN_KEY_UNKNOWN"
    )


def test_domain_channel_mechanisms_must_be_distinct(package) -> None:
    path = table(package, "domain_anchor_channels")
    header, rows = csv_rows(path)
    duplicate = copy.deepcopy(rows[0])
    duplicate["channel_id"] = "DA05-C99"
    rows.append(duplicate)
    write_rows(path, header, rows)
    assert_rejected(
        run_cli(package, "public-regeneration"), "ANCHOR_CHANNEL_NOT_DISTINCT"
    )


def test_domain_channel_provenance_fields_are_required(package) -> None:
    path = table(package, "domain_anchor_channels")
    header, rows = csv_rows(path)
    rows[0]["exact_quote"] = ""
    write_rows(path, header, rows)
    assert_rejected(
        run_cli(package, "public-regeneration"), "ANCHOR_CHANNEL_REQUIRED_FIELD_EMPTY"
    )


def test_yaml_declared_header_is_exact(package) -> None:
    path = table(package, "cases")
    header, rows = csv_rows(path)
    header.append("undeclared")
    for row in rows:
        row["undeclared"] = "value"
    write_rows(path, header, rows)
    assert_rejected(run_cli(package, "public-regeneration"), "SCHEMA_HEADER_MISMATCH")


def test_yaml_declared_enum_rejects_unknown_status(package) -> None:
    path = table(package, "closure_statuses")
    header, rows = csv_rows(path)
    rows[0]["status"] = "probably"
    write_rows(path, header, rows)
    assert_rejected(run_cli(package, "public-regeneration"), "SCHEMA_ENUM_INVALID")


def test_yaml_declared_boolean_rejects_noncanonical_value(package) -> None:
    path = table(package, "edges")
    header, rows = csv_rows(path)
    rows[0]["feedback_dependent"] = "yes"
    write_rows(path, header, rows)
    assert_rejected(run_cli(package, "public-regeneration"), "SCHEMA_BOOLEAN_INVALID")
