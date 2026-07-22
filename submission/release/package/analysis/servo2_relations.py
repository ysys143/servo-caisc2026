from __future__ import annotations

from .servo2_closure import validate_closure_statuses
from .servo2_io import Servo2Error, Table, require, split_values


def validate_relations(tables: dict[str, Table]) -> None:
    cases = _index(tables["cases"], "case_id")
    if len(cases) != 6 or len({row["lineage_id"] for row in cases.values()}) != 5:
        raise Servo2Error(
            "CASE_LINEAGE_CARDINALITY", "expected six cases and five lineages"
        )
    endpoints = _index(tables["endpoints"], "endpoint_id")
    artifacts = _index(tables["artifacts"], "artifact_id")
    events = _index(tables["events"], "event_id")
    edges = _index(tables["edges"], "edge_id")
    reliability = _index(tables["reliability"], "reliability_id")
    witnesses = _index(tables["closure_witnesses"], "witness_id")
    anchors = _index(tables["domain_anchors"], "anchor_id")
    anchor_channels = _index(tables["domain_anchor_channels"], "channel_id")
    _case_owners(tables, cases)
    _event_links(tables["events"], cases, endpoints, artifacts, reliability)
    _edge_links(tables["edges"], cases, events, endpoints)
    _reliability_links(tables["reliability"], events)
    _artifact_links(tables["artifacts"], cases, events, endpoints, artifacts)
    _witness_links(tables["closure_witnesses"], cases, events, edges, endpoints)
    validate_closure_statuses(tables["closure_statuses"], cases, witnesses)
    _anchor_channel_links(tables["domain_anchor_channels"], anchors)
    _selection_links(tables["selection_ledger"], cases, tables["domain_anchors"])
    del anchor_channels


def _index(table: Table, field: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in table.rows:
        identifier = require(row, field, table.name)
        if identifier in result:
            raise Servo2Error("DUPLICATE_PRIMARY_KEY", f"{table.name}:{identifier}")
        result[identifier] = row
    return result


def _case_owners(tables: dict[str, Table], cases: dict[str, dict[str, str]]) -> None:
    for name in (
        "endpoints",
        "artifacts",
        "events",
        "edges",
        "reliability",
        "closure_witnesses",
        "closure_statuses",
    ):
        for row in tables[name].rows:
            if require(row, "case_id", name) not in cases:
                raise Servo2Error("CASE_FOREIGN_KEY_UNKNOWN", f"{name}:{row}")


def _event_links(
    table: Table,
    cases: dict[str, dict[str, str]],
    endpoints: dict[str, dict[str, str]],
    artifacts: dict[str, dict[str, str]],
    reliability: dict[str, dict[str, str]],
) -> None:
    del cases
    for row in table.rows:
        case_id = row["case_id"]
        _same_case(endpoints, row["actor_endpoint_id"], case_id, "EVENT_ENDPOINT")
        for artifact_id in split_values(row["input_artifact_ids"]):
            _same_case(artifacts, artifact_id, case_id, "EVENT_INPUT_ARTIFACT")
        for artifact_id in split_values(row["output_artifact_ids"]):
            _same_case(artifacts, artifact_id, case_id, "EVENT_OUTPUT_ARTIFACT")
        for reliability_id in split_values(row["reliability_ids"]):
            _same_case(reliability, reliability_id, case_id, "EVENT_RELIABILITY")


def _edge_links(
    table: Table,
    cases: dict[str, dict[str, str]],
    events: dict[str, dict[str, str]],
    endpoints: dict[str, dict[str, str]],
) -> None:
    del cases
    for row in table.rows:
        case_id = row["case_id"]
        _same_case(events, row["source_event_id"], case_id, "EDGE_EVENT")
        _same_case(endpoints, row["source_endpoint_id"], case_id, "EDGE_SOURCE")
        _same_case(
            endpoints, row["destination_endpoint_id"], case_id, "EDGE_DESTINATION"
        )


def _artifact_links(
    table: Table,
    cases: dict[str, dict[str, str]],
    events: dict[str, dict[str, str]],
    endpoints: dict[str, dict[str, str]],
    artifacts: dict[str, dict[str, str]],
) -> None:
    del cases
    producers: set[tuple[str, str, str]] = set()
    for row in table.rows:
        case_id = row["case_id"]
        artifact_id = row["artifact_id"]
        lineage_id = require(row, "artifact_lineage_id", table.name)
        _same_case(events, row["producer_event_id"], case_id, "ARTIFACT_PRODUCER")
        _same_case(endpoints, row["producer_endpoint_id"], case_id, "ARTIFACT_ENDPOINT")
        event = events[row["producer_event_id"]]
        if row["producer_endpoint_id"] != event["actor_endpoint_id"]:
            raise Servo2Error("ARTIFACT_PRODUCER_ENDPOINT_MISMATCH", artifact_id)
        if artifact_id not in split_values(event["output_artifact_ids"]):
            raise Servo2Error("ARTIFACT_NOT_IN_PRODUCER_OUTPUT", artifact_id)
        key = (case_id, lineage_id, row["version"])
        if key in producers:
            raise Servo2Error("ARTIFACT_VERSION_MULTIPLE_PRODUCERS", artifact_id)
        producers.add(key)
        predecessor = row["predecessor_artifact_id"]
        if predecessor == "not_applicable":
            if row["version"] != "1":
                raise Servo2Error("ARTIFACT_LINEAGE_ROOT_VERSION_INVALID", artifact_id)
            continue
        _same_case(artifacts, predecessor, case_id, "ARTIFACT_PREDECESSOR")
        prior = artifacts[predecessor]
        if (
            lineage_id != prior["artifact_lineage_id"]
            or row["artifact_type"] != prior["artifact_type"]
            or int(row["version"]) != int(prior["version"]) + 1
        ):
            raise Servo2Error("ARTIFACT_PREDECESSOR_VERSION_INVALID", artifact_id)


def _reliability_links(table: Table, events: dict[str, dict[str, str]]) -> None:
    for row in table.rows:
        _same_case(
            events,
            row["evaluated_event_id"],
            row["case_id"],
            "RELIABILITY_EVALUATED_EVENT",
        )


def _witness_links(
    table: Table,
    cases: dict[str, dict[str, str]],
    events: dict[str, dict[str, str]],
    edges: dict[str, dict[str, str]],
    endpoints: dict[str, dict[str, str]],
) -> None:
    del cases
    for row in table.rows:
        case_id = row["case_id"]
        for occurrence in split_values(row["ordered_event_ids"]):
            _same_case(events, occurrence, case_id, "WITNESS_EVENT")
        for edge_id in split_values(row["ordered_edge_ids"]):
            _same_case(edges, edge_id, case_id, "WITNESS_EDGE")
        for endpoint_id in split_values(row["ordered_endpoint_ids"]):
            _same_case(endpoints, endpoint_id, case_id, "WITNESS_ENDPOINT")


def _selection_links(
    table: Table, cases: dict[str, dict[str, str]], anchors: Table
) -> None:
    anchor_ids = {row["anchor_id"] for row in anchors.rows}
    for row in table.rows:
        kind = row["record_kind"]
        identifier = row["record_id"]
        if (kind == "core_case" and identifier not in cases) or (
            kind == "domain_anchor" and identifier not in anchor_ids
        ):
            raise Servo2Error("SELECTION_FOREIGN_KEY_UNKNOWN", identifier)


def _anchor_channel_links(table: Table, anchors: dict[str, dict[str, str]]) -> None:
    mechanisms: set[tuple[str, str, str, str, str]] = set()
    required = (
        "phase",
        "target",
        "evidence_source",
        "evaluator",
        "decision_role",
        "routed_destination",
        "independence_status",
        "fidelity",
        "pdf_page",
        "exact_quote",
        "evidence_status",
        "uncertainty",
    )
    for row in table.rows:
        anchor_id = require(row, "anchor_id", table.name)
        if anchor_id not in anchors:
            raise Servo2Error("ANCHOR_CHANNEL_FOREIGN_KEY_UNKNOWN", anchor_id)
        if any(require(row, field, table.name).strip() == "" for field in required):
            raise Servo2Error("ANCHOR_CHANNEL_REQUIRED_FIELD_EMPTY", row["channel_id"])
        try:
            page = int(row["pdf_page"])
        except ValueError as error:
            raise Servo2Error(
                "ANCHOR_CHANNEL_PAGE_INVALID", row["channel_id"]
            ) from error
        if page < 1:
            raise Servo2Error("ANCHOR_CHANNEL_PAGE_INVALID", row["channel_id"])
        key = (
            anchor_id,
            row["phase"],
            row["target"],
            row["evaluator"],
            row["decision_role"],
        )
        if key in mechanisms:
            raise Servo2Error("ANCHOR_CHANNEL_NOT_DISTINCT", row["channel_id"])
        mechanisms.add(key)


def _same_case(
    rows: dict[str, dict[str, str]], identifier: str, case_id: str, code: str
) -> None:
    row = rows.get(identifier)
    if row is None or row["case_id"] != case_id:
        raise Servo2Error(f"{code}_FOREIGN_KEY", identifier)
