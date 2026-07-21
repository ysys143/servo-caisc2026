from __future__ import annotations

from .servo2_io import Servo2Error, Table, require, split_values
from .servo2_predicates import validate_predicate_pattern


def validate_graph(tables: dict[str, Table]) -> None:
    events = _index(tables["events"], "event_id")
    endpoints = _index(tables["endpoints"], "endpoint_id")
    edges = _index(tables["edges"], "edge_id")
    _validate_routes(tables["edges"], events)
    reliability_ids = set(_index(tables["reliability"], "reliability_id"))
    if reliability_ids & set(events):
        raise Servo2Error(
            "RELIABILITY_EVALUATION_USED_AS_RUNTIME_EVENT",
            "a reliability evaluation identifier appears in events",
        )
    for witness in tables["closure_witnesses"].rows:
        if require(witness, "predicate_status", "closure_witnesses") != "established":
            continue
        event_refs, event_rows, edge_rows, endpoint_refs = _validate_witness_path(
            witness, events, endpoints, edges
        )
        validate_predicate_pattern(witness, event_rows, edge_rows, endpoint_refs)
        if (
            require(witness, "predicate", "closure_witnesses")
            == "discovery_cycle_feedback"
        ):
            _validate_discovery_witness(
                witness, event_refs, event_rows, edge_rows, endpoint_refs
            )


def _validate_witness_path(
    witness: dict[str, str],
    events: dict[str, dict[str, str]],
    endpoints: dict[str, dict[str, str]],
    edges: dict[str, dict[str, str]],
) -> tuple[
    tuple[str, ...],
    tuple[dict[str, str], ...],
    tuple[dict[str, str], ...],
    tuple[str, ...],
]:
    witness_id = require(witness, "witness_id", "closure_witnesses")
    discovery = witness["predicate"] == "discovery_cycle_feedback"
    event_refs = split_values(
        require(witness, "ordered_event_ids", "closure_witnesses")
    )
    edge_refs = split_values(require(witness, "ordered_edge_ids", "closure_witnesses"))
    endpoint_refs = split_values(
        require(witness, "ordered_endpoint_ids", "closure_witnesses")
    )
    event_rows = tuple(_event(events, ref.split("@")[0]) for ref in event_refs)
    edge_rows = tuple(_edge(edges, ref) for ref in edge_refs)
    _ = tuple(_endpoint(endpoints, ref) for ref in endpoint_refs)
    if not event_rows or not edge_rows or len(endpoint_refs) != len(edge_rows) + 1:
        code = (
            "DISCOVERY_WITNESS_PATH_TRUNCATED"
            if discovery
            else "CLOSURE_WITNESS_PATH_TRUNCATED"
        )
        raise Servo2Error(code, witness_id)
    for index, edge in enumerate(edge_rows):
        if (
            edge["source_endpoint_id"] != endpoint_refs[index]
            or edge["destination_endpoint_id"] != endpoint_refs[index + 1]
        ):
            code = (
                "DISCOVERY_WITNESS_PATH_UNCONNECTED"
                if discovery
                else "CLOSURE_WITNESS_PATH_UNCONNECTED"
            )
            raise Servo2Error(code, witness_id)
    event_ids = {ref.split("@")[0] for ref in event_refs}
    if not discovery and any(
        edge["source_event_id"] not in event_ids for edge in edge_rows
    ):
        raise Servo2Error("CLOSURE_WITNESS_EVENT_EDGE_MISMATCH", witness_id)
    expected = (
        require(witness, "case_id", "closure_witnesses"),
        require(witness, "configuration_id", "closure_witnesses"),
        require(witness, "task_regime_id", "closure_witnesses"),
    )
    for rows in (event_rows, edge_rows):
        contexts = {
            (row["case_id"], row["configuration_id"], row["task_regime_id"])
            for row in rows
        }
        if contexts != {expected}:
            code = (
                "CROSS_CONTEXT_DISCOVERY_EDGE"
                if discovery
                else "CROSS_CONTEXT_CLOSURE_EDGE"
            )
            raise Servo2Error(code, witness_id)
    endpoint_cases = {endpoints[ref]["case_id"] for ref in endpoint_refs}
    if endpoint_cases != {expected[0]}:
        code = (
            "CROSS_CONTEXT_DISCOVERY_EDGE"
            if discovery
            else "CROSS_CONTEXT_CLOSURE_EDGE"
        )
        raise Servo2Error(code, witness_id)
    return event_refs, event_rows, edge_rows, endpoint_refs


def _index(table: Table, field: str) -> dict[str, dict[str, str]]:
    indexed: dict[str, dict[str, str]] = {}
    for row in table.rows:
        identifier = require(row, field, table.name)
        if identifier in indexed:
            raise Servo2Error("DUPLICATE_PRIMARY_KEY", f"{table.name}:{identifier}")
        indexed[identifier] = row
    return indexed


def _validate_routes(table: Table, events: dict[str, dict[str, str]]) -> None:
    for edge in table.rows:
        destination = require(edge, "destination_endpoint_id", table.name)
        values = split_values(destination)
        if len(values) != 1 or len(set(values)) != len(values):
            raise Servo2Error("AMBIGUOUS_OR_DUPLICATE_ROUTE_TARGET", destination)
        source_event = require(edge, "source_event_id", table.name)
        event = events.get(source_event)
        if event is None:
            raise Servo2Error("EDGE_EVENT_UNKNOWN", source_event)
        phase = event.get("phase", event.get("trigger_phase", ""))
        scope = edge.get("edge_scope", edge.get("scope", "internal"))
        if phase == "terminal" and scope in {"internal", "case_internal"}:
            raise Servo2Error("TERMINAL_INTERNAL_SUCCESSOR", source_event)


def _validate_discovery_witness(
    witness: dict[str, str],
    event_refs: tuple[str, ...],
    event_rows: tuple[dict[str, str], ...],
    edge_rows: tuple[dict[str, str], ...],
    endpoint_refs: tuple[str, ...],
) -> None:
    if "retry" in witness.get("uncertainty", "").lower():
        raise Servo2Error(
            "RETRY_PROMOTED_TO_DISCOVERY",
            require(witness, "witness_id", "closure_witnesses"),
        )
    if any(row.get("event_kind") == "retry" for row in event_rows):
        raise Servo2Error(
            "RETRY_PROMOTED_TO_DISCOVERY",
            require(witness, "witness_id", "closure_witnesses"),
        )
    if any(row.get("update_semantics") == "append_only" for row in event_rows):
        raise Servo2Error(
            "APPEND_ONLY_MEMORY_NOT_EPISTEMIC_UPDATE",
            require(witness, "witness_id", "closure_witnesses"),
        )
    if any(row.get("exclusion_reason") == "append_only_memory" for row in edge_rows):
        raise Servo2Error(
            "APPEND_ONLY_MEMORY_NOT_EPISTEMIC_UPDATE",
            require(witness, "witness_id", "closure_witnesses"),
        )
    _validate_discovery_sequence(
        witness, event_refs, event_rows, edge_rows, endpoint_refs
    )
    event_ids = {ref.split("@")[0] for ref in event_refs}
    if any(edge["source_event_id"] not in event_ids for edge in edge_rows):
        raise Servo2Error(
            "CLOSURE_WITNESS_EVENT_EDGE_MISMATCH",
            require(witness, "witness_id", "closure_witnesses"),
        )


def _validate_discovery_sequence(
    witness: dict[str, str],
    event_refs: tuple[str, ...],
    event_rows: tuple[dict[str, str], ...],
    edge_rows: tuple[dict[str, str], ...],
    endpoint_refs: tuple[str, ...],
) -> None:
    witness_id = require(witness, "witness_id", "closure_witnesses")
    if len(event_refs) < 3 or len(set(event_refs)) != len(event_refs):
        raise Servo2Error("DISCOVERY_WITNESS_EVENT_SEQUENCE_INVALID", witness_id)
    evidence_indexes = tuple(
        index for index, event in enumerate(event_rows) if _is_evidence(event)
    )
    execution_indexes = tuple(
        index for index, event in enumerate(event_rows) if _is_execution(event)
    )
    if len(evidence_indexes) < 2 or not execution_indexes:
        raise Servo2Error("DISCOVERY_WITNESS_EVENT_SEQUENCE_INVALID", witness_id)
    first_evidence = evidence_indexes[0]
    final_evidence = evidence_indexes[-1]
    eligible_execution = tuple(
        index for index in execution_indexes if first_evidence < index < final_evidence
    )
    if not eligible_execution:
        raise Servo2Error("DISCOVERY_WITNESS_EVENT_SEQUENCE_INVALID", witness_id)
    execution = event_rows[eligible_execution[-1]]
    if len(endpoint_refs) != len(edge_rows) + 1:
        raise Servo2Error("DISCOVERY_WITNESS_PATH_TRUNCATED", witness_id)
    for index, edge in enumerate(edge_rows):
        if (
            edge["source_endpoint_id"] != endpoint_refs[index]
            or edge["destination_endpoint_id"] != endpoint_refs[index + 1]
        ):
            raise Servo2Error("DISCOVERY_WITNESS_PATH_UNCONNECTED", witness_id)
    edge_types = tuple(edge["edge_type"] for edge in edge_rows)
    if "epistemic_update" not in edge_types:
        raise Servo2Error("DISCOVERY_WITNESS_EPISTEMIC_UPDATE_MISSING", witness_id)
    update_index = edge_types.index("epistemic_update")
    if (
        edge_rows[update_index]["source_endpoint_id"]
        != event_rows[first_evidence]["actor_endpoint_id"]
    ):
        raise Servo2Error("DISCOVERY_WITNESS_PATH_REORDERED", witness_id)
    action_edges = tuple(
        edge
        for edge in edge_rows[update_index + 1 :]
        if edge["edge_type"] == "feedback_control"
        and edge["feedback_dependent"] == "true"
    )
    if (
        not action_edges
        or execution["actor_endpoint_id"] != endpoint_refs[-2]
        or event_rows[first_evidence]["actor_endpoint_id"] not in endpoint_refs
        or event_rows[final_evidence]["actor_endpoint_id"] != endpoint_refs[-1]
        or edge_rows[-1]["edge_type"] != "observation"
    ):
        raise Servo2Error("DISCOVERY_WITNESS_ACTION_EXECUTION_MISSING", witness_id)


def _is_evidence(event: dict[str, str]) -> bool:
    return (
        event["event_kind"] in {"evidence_event", "repeated_evidence_cycle"}
        or event["phase"] == "post_observation"
    )


def _is_execution(event: dict[str, str]) -> bool:
    return event["event_class"] == "execution" or event["event_kind"] == "execution"


def _event(rows: dict[str, dict[str, str]], identifier: str) -> dict[str, str]:
    if identifier not in rows:
        raise Servo2Error("WITNESS_EVENT_UNKNOWN", identifier)
    return rows[identifier]


def _edge(rows: dict[str, dict[str, str]], identifier: str) -> dict[str, str]:
    if identifier not in rows:
        raise Servo2Error("WITNESS_EDGE_UNKNOWN", identifier)
    return rows[identifier]


def _endpoint(rows: dict[str, dict[str, str]], identifier: str) -> dict[str, str]:
    if identifier not in rows:
        raise Servo2Error("WITNESS_ENDPOINT_UNKNOWN", identifier)
    return rows[identifier]
