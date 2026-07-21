from __future__ import annotations

import hashlib
import json

from r24_final.hook_negative import build_report, mutation_cases


def test_adversarial_hook_suite_covers_required_mutations_and_passes() -> None:
    required = {
        "wrong_pdf_sha256",
        "wrong_page",
        "partial_or_wrong_full_quote",
        "wrong_channel_evidence_id",
        "wrong_envelope_evidence_id",
        "wrong_record_id",
        "wrong_vendor",
        "broken_diagnostic_link",
        "duplicate_channel_ids",
        "duplicate_diagnostic_ids",
        "duplicate_priority_ranks",
        "duplicate_json_keys",
        "nan_number",
        "fenced_json",
        "multiple_json_documents",
        "extra_top_level_field",
        "prompt_injection_preamble",
        "prompt_injection_in_quote",
    }

    assert {case_id for case_id, _ in mutation_cases()} == required
    report = build_report()
    assert report["passed"] is True
    assert report["positive_control"]["accepted"] is True
    assert all(case["rejected"] is True for case in report["cases"])


def test_adversarial_hook_report_hash_binds_canonical_report_body() -> None:
    report = build_report()
    claimed = report.pop("report_sha256")
    canonical = json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

    assert claimed == hashlib.sha256(canonical.encode()).hexdigest()
    assert build_report()["report_sha256"] == claimed
