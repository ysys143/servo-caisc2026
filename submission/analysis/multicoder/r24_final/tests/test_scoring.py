from __future__ import annotations

import json
from pathlib import Path

from r24_final.scoring import load_probe_key, score_checklist, scoring_assets_manifest


ROOT = Path(__file__).resolve().parents[1]


def test_all_probe_keys_validate_and_are_hash_bound() -> None:
    paths = tuple(sorted((ROOT / "probes").glob("R*.json")))
    assert len(paths) == 14
    assert all(len(load_probe_key(path).probes) == 12 for path in paths)
    manifest = scoring_assets_manifest(ROOT)
    assert len(manifest["files"]) == 14
    assert len(manifest["scoring_assets_sha256"]) == 64


def test_checklist_score_binds_key_and_output_hashes(tmp_path: Path) -> None:
    output = tmp_path / "current-output.json"
    output.write_text(
        json.dumps(
            {
                "record_id": "R01",
                "vendor": "codex",
                "model_id": "snapshot",
                "memo": "memo",
                "envelope": {
                    "diagnostics": [
                        {
                            "id": "D1",
                            "statement": "statement",
                            "kind": "risk",
                            "evidence_ids": ["R01-E01"],
                            "exact_quotes": [
                                {
                                    "evidence_id": "R01-E01",
                                    "exact_quote": "quote",
                                }
                            ],
                            "consequence": "consequence",
                        }
                    ],
                    "recommendations": [
                        {
                            "id": "A1",
                            "priority_rank": 1,
                            "proposed_action": "action",
                            "linked_diagnostic_ids": ["D1"],
                            "evidence_ids": ["R01-E01"],
                            "exact_quotes": [
                                {
                                    "evidence_id": "R01-E01",
                                    "exact_quote": "quote",
                                }
                            ],
                            "success_check": {
                                "observable": "observable",
                                "comparator_or_threshold": "threshold",
                                "evidence_needed": "evidence",
                            },
                        }
                    ],
                },
            }
        ),
        encoding="utf-8",
    )
    score = score_checklist(output, ROOT / "probes" / "R01.json")
    assert score.record_id == "R01"
    assert score.condition == "baseline"
    assert score.reference_items > 0
    assert len(score.scoring_key_sha256) == 64
    assert len(score.output_sha256) == 64
