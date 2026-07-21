from __future__ import annotations

import copy

import pytest

from analysis.servo2_graph import validate_graph
from analysis.servo2_io import Servo2Error, read_tables

from conftest import assert_rejected, column, csv_rows, run_cli, table, write_rows


def _discovery_witness(package):
    path = table(package, "closure_witnesses")
    header, rows = csv_rows(path)
    kind = column(rows[0], "closure_kind", "predicate", "witness_kind")
    row = next(item for item in rows if item[kind] == "discovery_cycle_feedback")
    return path, header, rows, row


def test_cross_configuration_or_task_edges_cannot_synthesize_discovery_cycle(package) -> None:
    _, _, _, witness = _discovery_witness(package)
    edges_path = table(package, "edges")
    edge_header, edges = csv_rows(edges_path)
    refs = column(witness, "ordered_edge_ids", "edge_ids", "path_edge_ids", "witness_edge_ids")
    edge_id = witness[refs].split(";")[-1]
    id_field = column(edges[0], "edge_id")
    edge = next(item for item in edges if item[id_field] == edge_id)
    edge[column(edge, "configuration_id", "configuration")] += "-cross-config"
    edge[column(edge, "task_regime_id", "task_regime")] += "-cross-task"
    write_rows(edges_path, edge_header, edges)

    assert_rejected(run_cli(package, "public-regeneration"), "CROSS_CONTEXT_CLOSURE_EDGE")


def test_retry_cannot_be_promoted_to_discovery_feedback(package) -> None:
    path = table(package, "closure_witnesses")
    header, rows = csv_rows(path)
    predicate = column(rows[0], "predicate", "closure_kind", "witness_kind")
    uncertainty = column(rows[0], "uncertainty")
    retry = next(item for item in rows if item[predicate] == "execution_repair" and "retry" in item[uncertainty].lower())
    retry[predicate] = "discovery_cycle_feedback"
    write_rows(path, header, rows)

    assert_rejected(run_cli(package, "public-regeneration"), "RETRY_PROMOTED_TO_DISCOVERY")


def test_append_only_memory_cannot_supply_epistemic_update(package) -> None:
    edge_path = table(package, "edges")
    _, edges = csv_rows(edge_path)
    exclusion = column(edges[0], "exclusion_reason")
    append_edge = next(item for item in edges if item[exclusion] == "append_only_memory")
    witness_path = table(package, "closure_witnesses")
    header, rows = csv_rows(witness_path)
    forged = copy.deepcopy(rows[0])
    forged[column(forged, "witness_id")] += "-append-only"
    forged[column(forged, "case_id")] = append_edge[column(append_edge, "case_id")]
    forged[column(forged, "configuration_id")] = append_edge[column(append_edge, "configuration_id")]
    forged[column(forged, "task_regime_id")] = append_edge[column(append_edge, "task_regime_id")]
    forged[column(forged, "predicate")] = "discovery_cycle_feedback"
    forged[column(forged, "ordered_event_ids", "ordered_event_occurrences")] = append_edge[column(append_edge, "source_event_id")] + "@t"
    forged[column(forged, "ordered_edge_ids")] = append_edge[column(append_edge, "edge_id")]
    forged[column(forged, "ordered_endpoint_ids")] = ";".join(
        (
            append_edge[column(append_edge, "source_endpoint_id")],
            append_edge[column(append_edge, "destination_endpoint_id")],
        )
    )
    forged[column(forged, "evidence_ids")] = append_edge[column(append_edge, "evidence_ids")]
    rows.append(forged)
    write_rows(witness_path, header, rows)

    assert_rejected(run_cli(package, "public-regeneration"), "APPEND_ONLY_MEMORY_NOT_EPISTEMIC_UPDATE")


def test_human_actor_facet_cannot_replace_a_structural_edge_type(package) -> None:
    path = table(package, "edges")
    header, rows = csv_rows(path)
    edge = next(item for item in rows if item["mediation_actor"] == "human")
    edge["edge_type"] = "human_mediation"
    write_rows(path, header, rows)

    assert_rejected(run_cli(package, "public-regeneration"), "SCHEMA_ENUM_INVALID")


def test_human_actor_facet_may_qualify_a_valid_discovery_path(package) -> None:
    tables = read_tables(package)
    discovery = next(
        row
        for row in tables["closure_witnesses"].rows
        if row["predicate"] == "discovery_cycle_feedback"
    )
    edge_ids = discovery["ordered_edge_ids"].split(";")
    edge = next(row for row in tables["edges"].rows if row["edge_id"] == edge_ids[0])
    edge["mediation_actor"] = "human"

    validate_graph(tables)


def test_execution_repair_requires_explicit_later_execution(package) -> None:
    tables = read_tables(package)
    witness = next(
        row
        for row in tables["closure_witnesses"].rows
        if row["predicate"] == "execution_repair" and row["case_id"] == "C04"
    )
    event_ids = {
        occurrence.split("@")[0]
        for occurrence in witness["ordered_event_ids"].split(";")
    }
    for event in tables["events"].rows:
        if event["event_id"] in event_ids and event["event_class"] == "execution":
            event["event_class"] = "runtime_validation"

    with pytest.raises(Servo2Error, match="EXECUTION_REPAIR_PATTERN_MISMATCH"):
        validate_graph(tables)


def test_execution_repair_requires_changed_versioned_artifact(package) -> None:
    tables = read_tables(package)
    witness = next(
        row
        for row in tables["closure_witnesses"].rows
        if row["predicate"] == "execution_repair" and row["case_id"] == "C04"
    )
    event_ids = {
        occurrence.split("@")[0]
        for occurrence in witness["ordered_event_ids"].split(";")
    }
    for event in tables["events"].rows:
        if event["event_id"] in event_ids and event["event_class"] == "runtime_validation":
            event["output_artifact_ids"] = "not_applicable"

    with pytest.raises(Servo2Error, match="EXECUTION_REPAIR_PATTERN_MISMATCH"):
        validate_graph(tables)


def test_adaptation_path_cannot_be_counted_as_artifact_revision(package) -> None:
    path = table(package, "closure_witnesses")
    header, rows = csv_rows(path)
    predicate = column(rows[0], "predicate")
    adaptation = next(item for item in rows if item[predicate] == "experimental_adaptation")
    adaptation[predicate] = "artifact_revision"
    write_rows(path, header, rows)

    assert_rejected(run_cli(package, "public-regeneration"), "ARTIFACT_REVISION_PATTERN_MISMATCH")


@pytest.mark.parametrize(
    ("predicate", "diagnostic"),
    (
        ("experimental_adaptation", "EXPERIMENTAL_ADAPTATION_PATTERN_MISMATCH"),
        ("artifact_revision", "ARTIFACT_REVISION_PATTERN_MISMATCH"),
    ),
)
def test_predicate_witness_requires_evaluation_evidence(
    package, predicate: str, diagnostic: str
) -> None:
    tables = read_tables(package)
    witness = next(
        row
        for row in tables["closure_witnesses"].rows
        if row["predicate"] == predicate
    )
    event_ids = {
        occurrence.split("@")[0]
        for occurrence in witness["ordered_event_ids"].split(";")
    }
    for event in tables["events"].rows:
        if event["event_id"] in event_ids and event["event_class"] in {
            "runtime_validation",
            "artifact_assessment",
            "human_feedback",
            "external_assessment",
        }:
            event["event_class"] = "state_update"

    with pytest.raises(Servo2Error, match=diagnostic):
        validate_graph(tables)


def test_artifact_revision_witness_names_versioned_successor_pair(package) -> None:
    tables = read_tables(package)
    witness = next(
        row
        for row in tables["closure_witnesses"].rows
        if row["predicate"] == "artifact_revision"
    )
    event_ids = {
        occurrence.split("@")[0]
        for occurrence in witness["ordered_event_ids"].split(";")
    }
    for event in tables["events"].rows:
        if event["event_id"] in event_ids:
            event["output_artifact_ids"] = "not_applicable"

    with pytest.raises(Servo2Error, match="ARTIFACT_REVISION_PATTERN_MISMATCH"):
        validate_graph(tables)


def test_human_mediation_is_not_a_closure_predicate(package) -> None:
    path = table(package, "closure_statuses")
    header, rows = csv_rows(path)
    forged = copy.deepcopy(rows[0])
    forged["predicate"] = "human_mediated_feedback"
    rows.append(forged)
    write_rows(path, header, rows)

    assert_rejected(run_cli(package, "public-regeneration"), "SCHEMA_ENUM_INVALID")


def test_terminal_event_has_no_internal_successor(package) -> None:
    events_path = table(package, "events")
    event_header, events = csv_rows(events_path)
    trigger = column(events[0], "trigger_phase", "phase")
    terminal = next(item for item in events if item[trigger] == "terminal")
    edges_path = table(package, "edges")
    edge_header, edges = csv_rows(edges_path)
    source = column(edges[0], "source_event_id", "source_id")
    forged = copy.deepcopy(edges[0])
    forged[column(forged, "edge_id")] += "-terminal-successor"
    forged[source] = terminal[column(terminal, "event_id")]
    terminal_case = terminal[column(terminal, "case_id")]
    forged[column(forged, "destination_endpoint_id", "destination_id")] = f"{terminal_case}.G"
    forged[column(forged, "route_status")] = "implemented"
    forged[column(forged, "closure_eligible")] = "true"
    forged[column(forged, "exclusion_reason")] = "not_applicable"
    edges.append(forged)
    write_rows(edges_path, edge_header, edges)

    assert_rejected(run_cli(package, "public-regeneration"), "TERMINAL_INTERNAL_SUCCESSOR")


def test_target_route_ambiguity_is_rejected(package) -> None:
    edges_path = table(package, "edges")
    header, rows = csv_rows(edges_path)
    destination = column(
        rows[0],
        "destination_endpoint_id",
        "target_endpoint_id",
        "destination_id",
        "routed_destination",
    )
    rows[0][destination] = rows[0][destination] + ";" + rows[0][destination]
    write_rows(edges_path, header, rows)

    assert_rejected(run_cli(package, "public-regeneration"), "AMBIGUOUS_OR_DUPLICATE_ROUTE_TARGET")
