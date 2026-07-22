from __future__ import annotations

from analysis.servo2_io import Table


def add_directly_stated_discovery_witness(
    tables: dict[str, Table],
) -> dict[str, str]:
    events = {row["event_id"]: row for row in tables["events"].rows}
    later_execution = dict(events["EV34"])
    later_execution.update(
        event_id="EV_TEST_LATER_EXECUTION",
        output_artifact_ids="not_applicable",
        evidence_status="directly_stated",
    )
    later_evidence = dict(events["EV17"])
    later_evidence.update(
        event_id="EV_TEST_LATER_EVIDENCE",
        input_artifact_ids="not_applicable",
        output_artifact_ids="not_applicable",
        event_kind="evidence_event",
        evidence_status="directly_stated",
    )
    tables["events"] = Table(
        tables["events"].name,
        tables["events"].header,
        (*tables["events"].rows, later_execution, later_evidence),
    )

    edge = next(row for row in tables["edges"].rows if row["edge_id"] == "ED37")
    later_observation = dict(edge)
    later_observation.update(
        edge_id="ED_TEST_LATER_OBSERVATION",
        source_event_id=later_execution["event_id"],
    )
    tables["edges"] = Table(
        tables["edges"].name,
        tables["edges"].header,
        (*tables["edges"].rows, later_observation),
    )

    witness = dict(tables["closure_witnesses"].rows[0])
    witness.update(
        witness_id="W_TEST_DISCOVERY",
        case_id="C05",
        configuration_id="adam-yeast",
        task_regime_id="yeast-functional-genomics",
        predicate="discovery_cycle_feedback",
        ordered_event_ids=(
            "EV34;EV17;EV45;EV_TEST_LATER_EXECUTION;EV_TEST_LATER_EVIDENCE"
        ),
        ordered_edge_ids="ED37;ED22;ED40;ED41;ED_TEST_LATER_OBSERVATION",
        ordered_endpoint_ids="C05.E;C05.V;C05.M;C05.G;C05.E;C05.V",
        predicate_status="established",
        execution_status="trace_demonstrated",
        uncertainty="synthetic directly stated recurrence for contract testing",
    )
    tables["closure_witnesses"] = Table(
        tables["closure_witnesses"].name,
        tables["closure_witnesses"].header,
        (*tables["closure_witnesses"].rows, witness),
    )
    return witness
