from __future__ import annotations

import json
import shutil
from pathlib import Path

from analysis.servo_v5_schema import validate_file, validate_root

REPOSITORY = Path(__file__).resolve().parents[3]
REAL_ANALYSIS_DIR = REPOSITORY / "analysis"
REAL_C01 = REAL_ANALYSIS_DIR / "servo_v5_source_propositions" / "C01.json"


def _temp_analysis_root(tmp_path: Path, mutate_first_proposition: dict | None = None) -> Path:
    root = tmp_path / "analysis"
    root.mkdir()
    shutil.copyfile(REAL_ANALYSIS_DIR / "servo_v5_schema.yaml", root / "servo_v5_schema.yaml")
    shutil.copyfile(REAL_ANALYSIS_DIR / "servo2_cases.csv", root / "servo2_cases.csv")
    props_dir = root / "servo_v5_source_propositions"
    props_dir.mkdir()
    payload = json.loads(REAL_C01.read_text(encoding="utf-8"))
    if mutate_first_proposition:
        payload["propositions"][0].update(mutate_first_proposition)
    (props_dir / "C01.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return root


def test_real_c01_pilot_validates_with_zero_errors() -> None:
    errors = validate_file(REAL_C01, "source_proposition")
    assert errors == [], f"pilot ledger must validate clean: {[str(e) for e in errors]}"


def test_forbidden_field_yields_source_judgment_leak(tmp_path: Path) -> None:
    root = _temp_analysis_root(tmp_path, mutate_first_proposition={"support_status": "supported"})
    errors = validate_file(root / "servo_v5_source_propositions" / "C01.json", "source_proposition")
    codes = {error.code for error in errors}
    assert codes == {"V5_SOURCE_JUDGMENT_LEAK"}, [str(error) for error in errors]


def test_upward_reference_to_alignment_is_rejected(tmp_path: Path) -> None:
    root = _temp_analysis_root(tmp_path, mutate_first_proposition={"alignment_id": "C01-A01"})
    errors = validate_file(root / "servo_v5_source_propositions" / "C01.json", "source_proposition")
    assert errors, "a proposition carrying an alignment_id must be rejected"
    assert {error.code for error in errors} == {"V5_SOURCE_JUDGMENT_LEAK"}, [str(error) for error in errors]


def test_validate_root_is_fail_closed_on_missing_downstream_families() -> None:
    # Only servo_v5_source_propositions exists in the repository at this
    # stage (T1); author_alignment/derived_claim/policy land in later tasks.
    # validate_root must report that rather than silently skipping it.
    errors = validate_root(REAL_ANALYSIS_DIR)
    codes = {error.code for error in errors}
    assert "V5_FAMILY_DIR_MISSING" in codes
    missing_families = {error.family for error in errors if error.code == "V5_FAMILY_DIR_MISSING"}
    assert missing_families == {"author_alignment", "derived_claim", "policy"}
