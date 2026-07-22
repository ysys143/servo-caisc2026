from __future__ import annotations

import copy

from conftest import assert_rejected, column, csv_rows, run_cli, table, write_rows


def test_artifact_must_have_a_producer(package) -> None:
    path = table(package, "artifacts")
    header, rows = csv_rows(path)
    rows[0][column(rows[0], "producer_endpoint_id", "producer_id")] = ""
    rows[0][column(rows[0], "producer_event_id")] = ""
    write_rows(path, header, rows)
    assert_rejected(run_cli(package, "public-regeneration"), "ARTIFACT_PRODUCER_MISSING")


def test_event_cannot_consume_a_future_artifact_version(package) -> None:
    path = table(package, "artifacts")
    header, rows = csv_rows(path)
    produced = column(rows[0], "producer_sequence")
    consumed = column(rows[0], "first_consumed_sequence")
    rows[0][produced] = "999999"
    rows[0][consumed] = "1"
    write_rows(path, header, rows)
    assert_rejected(run_cli(package, "public-regeneration"), "FUTURE_ARTIFACT_CONSUMPTION")


def test_reliability_benchmark_cannot_become_runtime_event(package) -> None:
    reliability_path = table(package, "reliability")
    _, reliability = csv_rows(reliability_path)
    evaluation_id = reliability[0][column(reliability[0], "reliability_id", "evaluation_id")]
    events_path = table(package, "events")
    header, events = csv_rows(events_path)
    forged = copy.deepcopy(events[0])
    forged[column(forged, "event_id")] = evaluation_id
    forged[column(forged, "event_class", "event_kind", "event_type")] = "runtime_validation"
    events.append(forged)
    write_rows(events_path, header, events)
    assert_rejected(run_cli(package, "public-regeneration"), "RELIABILITY_EVALUATION_USED_AS_RUNTIME_EVENT")
