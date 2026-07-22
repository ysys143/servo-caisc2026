from pathlib import Path

import pytest

from analysis.servo2_io import Servo2Error, read_tables
from analysis.servo2_predicates import validate_predicate_pattern
from discovery_test_support import add_directly_stated_discovery_witness


def test_discovery_witness_requires_every_edge_to_be_closure_eligible(
    package: Path,
) -> None:
    # Given: the released discovery witness with one independently mutated route edge.
    tables = read_tables(package)
    witness = add_directly_stated_discovery_witness(tables)
    events = {row["event_id"]: row for row in tables["events"].rows}
    edges = {row["edge_id"]: row for row in tables["edges"].rows}
    artifacts = {row["artifact_id"]: row for row in tables["artifacts"].rows}
    event_rows = tuple(
        events[token.split("@")[0]] for token in witness["ordered_event_ids"].split(";")
    )
    edge_rows = tuple(
        dict(edges[edge_id]) for edge_id in witness["ordered_edge_ids"].split(";")
    )
    edge_rows[0]["closure_eligible"] = "false"

    # When/Then: discovery cannot bypass the common all-edge contract.
    with pytest.raises(Servo2Error, match="CLOSURE_ROUTE_INELIGIBLE"):
        validate_predicate_pattern(
            witness,
            event_rows,
            edge_rows,
            tuple(witness["ordered_endpoint_ids"].split(";")),
            artifacts,
        )
