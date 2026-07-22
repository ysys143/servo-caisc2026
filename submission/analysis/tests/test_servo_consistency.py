from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from analysis import validate_servo_consistency as schema1


ROOT = Path(__file__).resolve().parents[2]
ANALYSIS = ROOT / "analysis"


def schema_version(path: Path) -> str:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return str(payload["schema_version"])


def csv_versions(path: Path) -> set[str]:
    with path.open(encoding="utf-8", newline="") as handle:
        return {row["schema_version"] for row in csv.DictReader(handle)}


def test_schema1_validator_rejects_current_schema2_inputs() -> None:
    with pytest.raises(schema1.ValidationError, match="historical and non-authoritative"):
        schema1.load_inputs()


def test_schema1_cli_fails_closed_on_current_schema2_inputs() -> None:
    result = subprocess.run(
        [sys.executable, str(ANALYSIS / "validate_servo_consistency.py"), "--check-only"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "cannot consume current Schema 4.0.0 inputs" in result.stderr
    assert "validate_servo2" in result.stderr


def test_schema_versions_are_separated_at_migration_boundary() -> None:
    assert schema_version(ANALYSIS / "servo_schema.yaml") == "4.0.0"
    assert csv_versions(ANALYSIS / "servo_core_systems.csv") == {"1.0.0"}
    assert csv_versions(ANALYSIS / "servo_validator_channels.csv") == {"1.0.0"}


def test_schema2_registry_excludes_schema1_tables() -> None:
    payload = yaml.safe_load((ANALYSIS / "servo_schema.yaml").read_text(encoding="utf-8"))
    registered = {record["file"] for record in payload["records"].values()}
    assert "analysis/servo_core_systems.csv" not in registered
    assert "analysis/servo_validator_channels.csv" not in registered
    assert all(path.startswith("analysis/servo2_") for path in registered)


def test_schema1_is_preserved_as_historical_migration_material() -> None:
    note = (ANALYSIS / "historical" / "servo1" / "README.md").read_text(encoding="utf-8")
    assert "historical" in note.lower()
    assert "non-authoritative" in note.lower()
    assert "validate_servo2" in note


def test_current_manuscripts_do_not_wire_schema1_generated_tables() -> None:
    english = (ROOT / "main_post-submit.tex").read_text(encoding="utf-8")
    korean = (ROOT / "main_ko.tex").read_text(encoding="utf-8")
    for source in (english, korean):
        inputs = schema1.tex_inputs(source)
        assert "analysis/tbl-core.tex" not in inputs
        assert "analysis/tbl-core-ko.tex" not in inputs
        assert "analysis/tbl-core-channels.tex" not in inputs
        assert "analysis/tbl-core-channels-ko.tex" not in inputs

