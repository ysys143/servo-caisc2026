from __future__ import annotations

from conftest import assert_rejected, csv_rows, run_cli, table, write_rows


def test_event_class_must_match_actor_component(package) -> None:
    path = table(package, "events")
    header, rows = csv_rows(path)
    event = next(row for row in rows if row["event_class"] == "execution")
    event["event_class"] = "runtime_validation"
    write_rows(path, header, rows)

    assert_rejected(run_cli(package, "public-regeneration"), "EVENT_COMPONENT_MISMATCH")


def test_edge_type_must_match_component_transition(package) -> None:
    path = table(package, "edges")
    header, rows = csv_rows(path)
    edge = next(row for row in rows if row["edge_type"] == "external_only")
    edge["destination_endpoint_id"] = f"{edge['case_id']}.G"
    write_rows(path, header, rows)

    assert_rejected(run_cli(package, "public-regeneration"), "EDGE_COMPONENT_TRANSITION_INVALID")


def test_experimental_adaptation_requires_later_execution(package) -> None:
    witness_path = table(package, "closure_witnesses")
    witness_header, witnesses = csv_rows(witness_path)
    witness = next(
        row
        for row in witnesses
        if row["case_id"] == "C03" and row["predicate"] == "experimental_adaptation"
    )
    witness["ordered_event_ids"] = "EV11@t;EV41@t+1;EV42@t+1"
    write_rows(witness_path, witness_header, witnesses)
    event_path = table(package, "events")
    event_header, events = csv_rows(event_path)
    execution = next(row for row in events if row["event_id"] == "EV42")
    execution["event_class"] = "generation"
    execution["actor_endpoint_id"] = "C03.G"
    write_rows(event_path, event_header, events)

    assert_rejected(
        run_cli(package, "public-regeneration"),
        "EXPERIMENTAL_ADAPTATION_PATTERN_MISMATCH",
    )


def test_every_established_adaptation_names_a_later_execution(package) -> None:
    witness_path = table(package, "closure_witnesses")
    _, witnesses = csv_rows(witness_path)
    event_path = table(package, "events")
    _, events = csv_rows(event_path)
    classes = {row["event_id"]: row["event_class"] for row in events}

    adaptations = [
        row
        for row in witnesses
        if row["predicate"] == "experimental_adaptation"
        and row["predicate_status"] == "established"
    ]
    assert adaptations
    for witness in adaptations:
        event_ids = [token.split("@")[0] for token in witness["ordered_event_ids"].split(";")]
        assert any(classes[event_id] == "execution" for event_id in event_ids[1:])
