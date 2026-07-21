from __future__ import annotations

from r24_final.schedule import Condition, build_schedule


def test_schedule_has_42_unique_servo_trials() -> None:
    # Given
    records = tuple(f"R{i:02d}" for i in range(1, 15))

    # When
    schedule = build_schedule(records, seed=20260720)

    # Then
    assert len(schedule) == 42
    assert len({trial.trial_id for trial in schedule}) == 42
    assert {trial.condition for trial in schedule} == {Condition.SERVO}
    for vendor in {trial.vendor for trial in schedule}:
        vendor_trials = [trial for trial in schedule if trial.vendor == vendor]
        assert len(vendor_trials) == 14
        assert {trial.record_id for trial in vendor_trials} == set(records)
