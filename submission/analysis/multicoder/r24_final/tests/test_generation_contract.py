from __future__ import annotations

import json
from pathlib import Path

from r24_final.run_experiment import build_prompt
from r24_final.runner import load_schedule


ROOT = Path(__file__).resolve().parents[1]


def test_all_42_servo_prompts_hide_retired_scoring_assets() -> None:
    schedule = load_schedule(ROOT / "schedule.json")
    assert len(schedule) == 42
    action_tokens = tuple(json.loads((ROOT / "action_codes.json").read_text()))

    for trial in schedule:
        prompt = build_prompt(ROOT, trial.record_id, trial.condition, trial.vendor)
        probe_packet = json.loads(
            (ROOT / "probes" / f"{trial.record_id}.json").read_text()
        )
        forbidden_probe_text = {
            probe[key]
            for probe in probe_packet["probes"]
            for key in ("probe_id", "question")
        }

        assert all(text not in prompt for text in forbidden_probe_text)
        assert all(token not in prompt for token in action_tokens)
        assert '"probes"' not in prompt
        assert '"expected_answer"' not in prompt
        assert '"action_code"' not in prompt
