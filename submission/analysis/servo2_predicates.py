from __future__ import annotations

from enum import StrEnum
from typing import assert_never

from .servo2_io import Servo2Error, require, split_values


class Predicate(StrEnum):
    EXECUTION_REPAIR = "execution_repair"
    EXPERIMENTAL_ADAPTATION = "experimental_adaptation"
    ARTIFACT_REVISION = "artifact_revision"
    DISCOVERY_CYCLE_FEEDBACK = "discovery_cycle_feedback"


REPAIR_FAILURE_SEMANTICS = {
    "failure_evidence_changes_code",
    "failure_evidence_changes_protocol",
}
ADAPTATION_CHANGE_SEMANTICS = {
    "evidence_guided_node_selection",
    "evidence_to_epistemic_update_to_new_execution",
    "evidence_to_memory_to_replanned_execution",
    "evidence_to_model_update_to_new_physical_execution",
}


def validate_predicate_pattern(
    witness: dict[str, str],
    event_rows: tuple[dict[str, str], ...],
    edge_rows: tuple[dict[str, str], ...],
    endpoint_refs: tuple[str, ...],
    artifacts: dict[str, dict[str, str]],
) -> None:
    witness_id = require(witness, "witness_id", "closure_witnesses")
    try:
        predicate = Predicate(require(witness, "predicate", "closure_witnesses"))
    except ValueError as error:
        raise Servo2Error("CLOSURE_PREDICATE_UNKNOWN", witness_id) from error

    _validate_common_route(witness_id, edge_rows)
    match predicate:
        case Predicate.EXECUTION_REPAIR:
            _require_execution_repair(
                witness_id, event_rows, edge_rows, endpoint_refs, artifacts
            )
        case Predicate.EXPERIMENTAL_ADAPTATION:
            _require_experimental_adaptation(
                witness_id, event_rows, edge_rows, endpoint_refs
            )
        case Predicate.ARTIFACT_REVISION:
            _require_artifact_revision(
                witness_id, event_rows, edge_rows, endpoint_refs, artifacts
            )
        case Predicate.DISCOVERY_CYCLE_FEEDBACK:
            return
        case unreachable:
            assert_never(unreachable)


def _validate_common_route(
    witness_id: str, edge_rows: tuple[dict[str, str], ...]
) -> None:
    if any(
        edge.get("closure_eligible") != "true"
        or edge.get("feedback_dependent") != "true"
        or edge.get("route_status") != "implemented"
        for edge in edge_rows
    ):
        raise Servo2Error("CLOSURE_ROUTE_INELIGIBLE", witness_id)


def _require_execution_repair(
    witness_id: str,
    event_rows: tuple[dict[str, str], ...],
    edge_rows: tuple[dict[str, str], ...],
    endpoint_refs: tuple[str, ...],
    artifacts: dict[str, dict[str, str]],
) -> None:
    edge_types = {edge["edge_type"] for edge in edge_rows}
    validation_indexes = tuple(
        index
        for index, event in enumerate(event_rows)
        if event["event_class"] == "runtime_validation"
    )
    execution_indexes = tuple(
        index
        for index, event in enumerate(event_rows)
        if event["event_class"] == "execution"
    )
    validation_precedes_execution = any(
        validation < execution
        for validation in validation_indexes
        for execution in execution_indexes
    )
    valid = (
        len(event_rows) >= 2
        and validation_precedes_execution
        and any(
            event["event_class"] == "runtime_validation"
            and event["event_kind"] == "retry_with_revision"
            and event["update_semantics"] in REPAIR_FAILURE_SEMANTICS
            and _event_names_versioned_successor(event, artifacts)
            for event in event_rows
        )
        and {"artifact_revision", "feedback_control"} <= edge_types
        and any(endpoint.endswith(".W_A") for endpoint in endpoint_refs)
        and endpoint_refs[-1].endswith(".E")
    )
    if not valid:
        raise Servo2Error("EXECUTION_REPAIR_PATTERN_MISMATCH", witness_id)


def _require_experimental_adaptation(
    witness_id: str,
    event_rows: tuple[dict[str, str], ...],
    edge_rows: tuple[dict[str, str], ...],
    endpoint_refs: tuple[str, ...],
) -> None:
    edge_types = {edge["edge_type"] for edge in edge_rows}
    evaluation_indexes = tuple(
        index for index, event in enumerate(event_rows) if _is_evaluation(event)
    )
    execution_indexes = tuple(
        index
        for index, event in enumerate(event_rows)
        if event["event_class"] == "execution"
    )
    evaluation_precedes_execution = any(
        evaluation < execution
        for evaluation in evaluation_indexes
        for execution in execution_indexes
    )
    valid = (
        len(event_rows) >= 2
        and "feedback_control" in edge_types
        and any(endpoint.endswith(".E") for endpoint in endpoint_refs)
        and evaluation_precedes_execution
        and any(
            _is_evaluation(event)
            and event["update_semantics"] in ADAPTATION_CHANGE_SEMANTICS
            for event in event_rows
        )
        and _adaptation_route_connects_evaluation_to_execution(
            event_rows, edge_rows, endpoint_refs
        )
    )
    if not valid:
        raise Servo2Error("EXPERIMENTAL_ADAPTATION_PATTERN_MISMATCH", witness_id)


def _adaptation_route_connects_evaluation_to_execution(
    event_rows: tuple[dict[str, str], ...],
    edge_rows: tuple[dict[str, str], ...],
    endpoint_refs: tuple[str, ...],
) -> bool:
    evaluation_endpoints = {
        event["actor_endpoint_id"] for event in event_rows if _is_evaluation(event)
    }
    execution_endpoints = {
        event["actor_endpoint_id"]
        for event in event_rows
        if event["event_class"] == "execution"
    }
    action_components = {"M", "pi", "G", "W_A"}
    for evaluation_index, endpoint in enumerate(endpoint_refs):
        if endpoint not in evaluation_endpoints:
            continue
        for execution_index in range(evaluation_index + 1, len(endpoint_refs)):
            if endpoint_refs[execution_index] not in execution_endpoints:
                continue
            route_edges = edge_rows[evaluation_index:execution_index]
            intermediate_components = {
                item.rsplit(".", 1)[-1]
                for item in endpoint_refs[evaluation_index + 1 : execution_index]
            }
            if (
                action_components & intermediate_components
                and any(edge["edge_type"] == "feedback_control" for edge in route_edges)
            ):
                return True
    return False


def _require_artifact_revision(
    witness_id: str,
    event_rows: tuple[dict[str, str], ...],
    edge_rows: tuple[dict[str, str], ...],
    endpoint_refs: tuple[str, ...],
    artifacts: dict[str, dict[str, str]],
) -> None:
    valid = (
        bool(event_rows)
        and any(
            _is_evaluation(event)
            and _event_names_versioned_successor(event, artifacts)
            for event in event_rows
        )
        and any(edge["edge_type"] == "artifact_revision" for edge in edge_rows)
        and any(endpoint.endswith(".W_A") for endpoint in endpoint_refs)
    )
    if not valid:
        raise Servo2Error("ARTIFACT_REVISION_PATTERN_MISMATCH", witness_id)


def _event_names_versioned_successor(
    event: dict[str, str], artifacts: dict[str, dict[str, str]]
) -> bool:
    inputs = set(split_values(event["input_artifact_ids"])) - {"not_applicable"}
    outputs = set(split_values(event["output_artifact_ids"])) - {"not_applicable"}
    for output_id in outputs:
        output = artifacts.get(output_id)
        if output is None:
            continue
        predecessor_id = output["predecessor_artifact_id"]
        predecessor = artifacts.get(predecessor_id)
        if (
            predecessor_id in inputs
            and predecessor is not None
            and output["artifact_type"] == predecessor["artifact_type"]
            and int(output["version"]) == int(predecessor["version"]) + 1
        ):
            return True
    return False


def _is_evaluation(event: dict[str, str]) -> bool:
    return event["event_class"] in {
        "runtime_validation",
        "artifact_assessment",
        "human_feedback",
        "external_assessment",
    }
