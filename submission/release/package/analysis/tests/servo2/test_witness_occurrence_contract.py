from __future__ import annotations

import pytest

from analysis.servo2_graph import validate_graph
from analysis.servo2_io import Servo2Error, read_tables


def test_witness_rejects_malformed_occurrence_labels(package) -> None:
    tables = read_tables(package)
    witness = next(
        row
        for row in tables["closure_witnesses"].rows
        if row["predicate"] == "discovery_cycle_feedback"
    )
    witness["ordered_event_ids"] = witness["ordered_event_ids"].replace(
        "EV34", "EV34@garbage", 1
    )

    with pytest.raises(Servo2Error, match="OCCURRENCE_TOKEN_INVALID"):
        validate_graph(tables)


def test_witness_rejects_edge_spliced_to_later_event(package) -> None:
    tables = read_tables(package)
    edge = next(row for row in tables["edges"].rows if row["edge_id"] == "ED13")
    edge["source_event_id"] = "EV43"

    with pytest.raises(
        Servo2Error, match="CLOSURE_WITNESS_EVENT_EDGE_ORDER_MISMATCH"
    ):
        validate_graph(tables)


def test_witness_rejects_occurrence_offset_beyond_next_iteration(package) -> None:
    tables = read_tables(package)
    witness = next(
        row
        for row in tables["closure_witnesses"].rows
        if row["predicate"] == "experimental_adaptation" and row["case_id"] == "C03"
    )
    witness["ordered_event_ids"] = witness["ordered_event_ids"].replace(
        "EV43", "EV43+2"
    )

    with pytest.raises(Servo2Error, match="OCCURRENCE_TOKEN_INVALID"):
        validate_graph(tables)


def test_witness_rejects_reused_event_identity(package) -> None:
    tables = read_tables(package)
    witness = next(
        row
        for row in tables["closure_witnesses"].rows
        if row["predicate"] == "discovery_cycle_feedback"
    )
    event_ids = witness["ordered_event_ids"].split(";")
    event_ids[-1] = event_ids[1]
    witness["ordered_event_ids"] = ";".join(event_ids)

    with pytest.raises(Servo2Error, match="OCCURRENCE_ID_REUSED"):
        validate_graph(tables)
