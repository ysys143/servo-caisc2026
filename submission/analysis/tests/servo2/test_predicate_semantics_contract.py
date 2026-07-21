from pathlib import Path

import pytest

from analysis.servo2_graph import validate_graph
from analysis.servo2_io import Servo2Error, read_tables
from analysis.servo2_conformance import validate_component_graph_conformance


def test_execution_repair_requires_failure_semantics(package: Path) -> None:
    # Given: an otherwise valid repair route whose validation reports no failure.
    tables = read_tables(package)
    witness = next(
        row
        for row in tables["closure_witnesses"].rows
        if row["predicate"] == "execution_repair"
    )
    event_ids = {
        occurrence.split("@")[0]
        for occurrence in witness["ordered_event_ids"].split(";")
    }
    validation = next(
        row
        for row in tables["events"].rows
        if row["event_id"] in event_ids and row["event_class"] == "runtime_validation"
    )
    validation["event_kind"] = "evidence_event"
    validation["update_semantics"] = "successful_validation"

    # When/Then: a changed artifact alone cannot establish failure repair.
    with pytest.raises(Servo2Error, match="EXECUTION_REPAIR_PATTERN_MISMATCH"):
        validate_graph(tables)


def test_experimental_adaptation_requires_changed_action_semantics(
    package: Path,
) -> None:
    # Given: a routed evaluation and later execution with no reported action change.
    tables = read_tables(package)
    witness = next(
        row
        for row in tables["closure_witnesses"].rows
        if row["predicate"] == "experimental_adaptation"
    )
    event_ids = {
        occurrence.split("@")[0]
        for occurrence in witness["ordered_event_ids"].split(";")
    }
    evaluation = next(
        row
        for row in tables["events"].rows
        if row["event_id"] in event_ids and row["event_class"] == "runtime_validation"
    )
    evaluation["update_semantics"] = "fixed_schedule_no_action_change"

    # When/Then: topology cannot substitute for evidence of a changed action.
    with pytest.raises(Servo2Error, match="EXPERIMENTAL_ADAPTATION_PATTERN_MISMATCH"):
        validate_graph(tables)


def test_edge_requires_existing_mediator_endpoint(package: Path) -> None:
    # Given: an otherwise typed edge with an unresolved mediator endpoint.
    tables = read_tables(package)
    tables["edges"].rows[0]["mediator_endpoint_id"] = ""

    # When/Then: every routed edge must resolve all required routing fields.
    with pytest.raises(Servo2Error, match="EDGE_MEDIATOR_ENDPOINT_INVALID"):
        validate_component_graph_conformance(tables)
