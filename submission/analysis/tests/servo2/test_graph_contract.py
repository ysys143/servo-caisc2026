from __future__ import annotations

import copy

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


def test_human_mediated_edge_cannot_be_counted_as_automated_discovery(package) -> None:
    path = table(package, "closure_witnesses")
    header, rows = csv_rows(path)
    predicate = column(rows[0], "predicate")
    human = next(item for item in rows if item[predicate] == "human_mediated_feedback")
    human[predicate] = "discovery_cycle_feedback"
    write_rows(path, header, rows)

    assert_rejected(run_cli(package, "public-regeneration"), "HUMAN_EDGE_MISCLASSIFIED_AUTOMATED")


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
