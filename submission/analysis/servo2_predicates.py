from __future__ import annotations

from enum import StrEnum
from typing import assert_never

from .servo2_io import Servo2Error, require


class Predicate(StrEnum):
    EXECUTION_REPAIR = "execution_repair"
    EXPERIMENTAL_ADAPTATION = "experimental_adaptation"
    ARTIFACT_REVISION = "artifact_revision"
    DISCOVERY_CYCLE_FEEDBACK = "discovery_cycle_feedback"


def validate_predicate_pattern(
    witness: dict[str, str],
    event_rows: tuple[dict[str, str], ...],
    edge_rows: tuple[dict[str, str], ...],
    endpoint_refs: tuple[str, ...],
) -> None:
    witness_id = require(witness, "witness_id", "closure_witnesses")
    try:
        predicate = Predicate(require(witness, "predicate", "closure_witnesses"))
    except ValueError as error:
        raise Servo2Error("CLOSURE_PREDICATE_UNKNOWN", witness_id) from error

    match predicate:
        case Predicate.EXECUTION_REPAIR:
            _validate_common_route(witness_id, edge_rows)
            _require_execution_repair(witness_id, event_rows, edge_rows, endpoint_refs)
        case Predicate.EXPERIMENTAL_ADAPTATION:
            _validate_common_route(witness_id, edge_rows)
            _require_experimental_adaptation(
                witness_id, event_rows, edge_rows, endpoint_refs
            )
        case Predicate.ARTIFACT_REVISION:
            _validate_common_route(witness_id, edge_rows)
            _require_artifact_revision(witness_id, edge_rows, endpoint_refs)
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
) -> None:
    edge_types = {edge["edge_type"] for edge in edge_rows}
    valid = (
        len(event_rows) >= 2
        and all(event["event_class"] == "runtime_validation" for event in event_rows)
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
    event_ids = {event["event_id"] for event in event_rows}
    execution_supported = any(
        event["event_class"] == "execution" for event in event_rows
    ) or len(event_ids) == 1
    valid = (
        len(event_rows) >= 2
        and "feedback_control" in edge_types
        and any(endpoint.endswith(".E") for endpoint in endpoint_refs)
        and execution_supported
    )
    if not valid:
        raise Servo2Error("EXPERIMENTAL_ADAPTATION_PATTERN_MISMATCH", witness_id)


def _require_artifact_revision(
    witness_id: str,
    edge_rows: tuple[dict[str, str], ...],
    endpoint_refs: tuple[str, ...],
) -> None:
    valid = any(edge["edge_type"] == "artifact_revision" for edge in edge_rows) and any(
        endpoint.endswith(".W_A") for endpoint in endpoint_refs
    )
    if not valid:
        raise Servo2Error("ARTIFACT_REVISION_PATTERN_MISMATCH", witness_id)
