from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Final



PROTOCOL_FILES: Final = (
    "adapters.py",
    "assets.py",
    "action_codes.json",
    "coding_manual.md",
    "evidence.py",
    "hook_negative.py",
    "generation_snapshot.py",
    "lifecycle.py",
    "live_smoke.py",
    "manifest/source_manifest.json",
    "models.py",
    "output_validation.py",
    "process_sandbox.py",
    "execution_metrics_contract.json",
    "run_experiment.py",
    "runner.py",
    "sandbox_smoke.py",
    "smoke_contract.py",
    "static_checks.py",
    "SMOKE_CRITERIA.md",
    "schedule.py",
    "schedule.json",
    "servo_prompt.md",
    "servo.schema.json",
    "servo_analysis_plan.md",
)

SMOKE_MANIFEST: Final = "SMOKE_PASSED.json"
SMOKE_REPORT_DIRECTORY: Final = "smoke_reports"
REQUIRED_SMOKE_REPORTS: Final = {
    "STATIC_GATE_REPORT": frozenset({
        "prompt_nonleakage", "packet_pdf_binding", "command_allowlist",
        "schema_resolution", "schedule_contract", "retired_asset_nonleakage",
    }),
    "HOOK_NEGATIVE_REPORT": frozenset({
        "wrong_pdf_sha256", "wrong_page", "partial_or_wrong_full_quote",
        "wrong_channel_evidence_id", "wrong_envelope_evidence_id",
        "wrong_record_id", "wrong_vendor", "broken_diagnostic_link",
        "duplicate_channel_ids", "duplicate_diagnostic_ids",
        "duplicate_priority_ranks", "duplicate_json_keys", "nan_number",
        "fenced_json", "multiple_json_documents", "extra_top_level_field",
        "prompt_injection_preamble", "prompt_injection_in_quote",
    }),
    "ISOLATION_REPORT": frozenset({
        "fresh_trial_roots", "model_tools_disabled", "filesystem_denied",
        "network_policy", "canary_scan", "control_plane_exceptions",
    }),
    "FUNCTIONAL_REPORT": frozenset({
        "servo_generation_matrix", "runtime_provenance", "latency_boundary",
    }),
}
REQUIRED_SMOKE_CELLS: Final = tuple(
    f"{vendor}:servo"
    for vendor in ("claude", "codex", "gemini")
)


def protocol_manifest(root: Path) -> dict[str, object]:
    paths = [root / name for name in PROTOCOL_FILES]
    paths.extend(sorted((root / "packets").glob("R*.json")))
    paths.extend(sorted((root / "probes").glob("R*.json")))
    hashes = {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in paths
    }
    canonical = json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()
    return {"protocol_sha256": hashlib.sha256(canonical).hexdigest(), "files": hashes}


def smoke_binding(root: Path) -> dict[str, str]:
    from r24_final.adapters import Vendor, build_command
    from r24_final.process_sandbox import build_execution_command
    from r24_final.schedule import Condition, Trial

    protocol = protocol_manifest(root)["protocol_sha256"]
    assert isinstance(protocol, str)
    runtime_payload: dict[str, object] = {
        "python_executable": str(Path(sys.executable).resolve()),
        "python_version": sys.version,
    }
    command_payload: dict[str, object] = {}
    for vendor in Vendor:
        executable = shutil.which({Vendor.CLAUDE: "claude", Vendor.CODEX: "codex", Vendor.GEMINI: "agy"}[vendor])
        executable_path = Path(executable).resolve() if executable else None
        runtime_payload[vendor.value] = {
            "executable": str(executable_path) if executable_path else None,
            "sha256": _sha256_file(executable_path) if executable_path and executable_path.is_file() else None,
        }
        for condition in Condition:
            trial = Trial("binding", vendor.value, "R10", condition, 1, 0)
            command = build_command(trial, Path(f"{condition.value}.schema.json"), root)
            command_payload[f"{vendor.value}:{condition.value}"] = {
                "arguments": command.arguments,
                "execution_arguments": build_execution_command(command.arguments),
                "requested_model": command.requested_model,
            }
    environment_policy = {
        "allowed": sorted({
            "PATH", "HOME", "TMPDIR", "LANG", "LC_ALL", "USER", "LOGNAME", "SHELL",
            "__CF_USER_TEXT_ENCODING", "SSL_CERT_FILE", "SSL_CERT_DIR",
            "ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY",
        }),
        "present": sorted(name for name in os.environ if name.endswith("_API_KEY")),
        "values_recorded": False,
    }
    sandbox_files = {
        name: _sha256_file(root / name)
        for name in ("adapters.py", "process_sandbox.py", "runner.py", "sandbox_smoke.py")
    }
    return {
        "protocol_sha256": protocol,
        "runtime_sha256": _canonical_sha256({"runtime": runtime_payload, "commands": command_payload}),
        "environment_policy_sha256": _canonical_sha256(environment_policy),
        "sandbox_profile_sha256": _canonical_sha256(sandbox_files),
    }


def verify_smoke_report(root: Path, report_name: str) -> dict[str, object]:
    from r24_final.smoke_contract import verify_typed_evidence

    if report_name not in REQUIRED_SMOKE_REPORTS:
        raise ValueError(f"unknown smoke report: {report_name}")
    path = root / SMOKE_REPORT_DIRECTORY / f"{report_name}.json"
    report = _read_object(path, f"{report_name} is absent or invalid")
    if report.get("report_type") != report_name:
        raise ValueError(f"{report_name} has the wrong report_type")
    if report.get("binding") != smoke_binding(root):
        raise ValueError(f"{report_name} has stale or mismatched bindings")
    evidence = report.get("evidence")
    if not isinstance(evidence, list) or len(evidence) != 1:
        raise ValueError(f"{report_name} has no raw evidence")
    evidence_ids: set[str] = set()
    for item in evidence:
        if not isinstance(item, dict) or set(item) != {"id", "path", "sha256"}:
            raise ValueError(f"{report_name} has malformed evidence")
        evidence_id, relative, expected = item["id"], item["path"], item["sha256"]
        if not all(isinstance(value, str) and value for value in (evidence_id, relative, expected)):
            raise ValueError(f"{report_name} has malformed evidence values")
        evidence_path = (root / SMOKE_REPORT_DIRECTORY / relative).resolve()
        report_root = (root / SMOKE_REPORT_DIRECTORY).resolve()
        if report_root not in evidence_path.parents or not evidence_path.is_file():
            raise ValueError(f"{report_name} evidence escapes or is absent: {relative}")
        if _sha256_file(evidence_path) != expected:
            raise ValueError(f"{report_name} raw evidence hash mismatch: {relative}")
        if evidence_id in evidence_ids:
            raise ValueError(f"{report_name} has duplicate evidence ids")
        evidence_ids.add(evidence_id)
        try:
            protocol_sha256 = smoke_binding(root)["protocol_sha256"]
            verify_typed_evidence(report_name, evidence_path, protocol_sha256, root)
        except (ValueError, json.JSONDecodeError) as error:
            raise ValueError(f"{report_name} typed evidence is invalid: {error}") from error
    checks = report.get("checks")
    expected_checks = REQUIRED_SMOKE_REPORTS[report_name]
    if not isinstance(checks, list) or {item.get("id") for item in checks if isinstance(item, dict)} != expected_checks:
        raise ValueError(f"{report_name} does not contain its exact required checks")
    for check in checks:
        if not isinstance(check, dict) or set(check) != {"id", "result", "evidence_ids"}:
            raise ValueError(f"{report_name} has malformed checks")
        refs = check["evidence_ids"]
        if check["result"] != "pass" or not isinstance(refs, list) or not refs or not set(refs) <= evidence_ids:
            raise ValueError(f"{report_name} check is failed or unsupported: {check.get('id')}")
    return report


def assemble_smoke_manifest(root: Path) -> dict[str, object]:
    reports: dict[str, object] = {}
    for name in REQUIRED_SMOKE_REPORTS:
        verify_smoke_report(root, name)
        path = root / SMOKE_REPORT_DIRECTORY / f"{name}.json"
        reports[name] = {"path": str(path.relative_to(root)), "sha256": _sha256_file(path)}
    return {
        "format": "r24-four-report-smoke-v1",
        "binding": smoke_binding(root),
        "reports": reports,
    }


def start_run(root: Path, output_dir: Path) -> None:
    if output_dir.exists():
        raise FileExistsError(f"fresh run directory already exists: {output_dir}")
    output_dir.mkdir(parents=True)
    payload = {
        "status": "running",
        "started_utc": datetime.now(UTC).isoformat(),
        **protocol_manifest(root),
    }
    _write_new(output_dir / "RUN_STARTED.json", payload)


def verify_protocol(root: Path, output_dir: Path) -> None:
    started_path = output_dir / "RUN_STARTED.json"
    if not started_path.is_file():
        raise ValueError("run has no RUN_STARTED.json")
    started = json.loads(started_path.read_text(encoding="utf-8"))
    current = protocol_manifest(root)
    if started.get("protocol_sha256") != current["protocol_sha256"]:
        raise ValueError("protocol drift detected after run start")


def verify_smoke_gate(root: Path) -> None:
    path = root / SMOKE_MANIFEST
    if not path.is_file():
        raise ValueError(f"production smoke gate is absent: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError("production smoke gate is not valid JSON") from error
    expected = assemble_smoke_manifest(root)
    if payload != expected:
        raise ValueError("production smoke manifest is stale, incomplete, or not derived from reports")


def finish_run(output_dir: Path, status: str, **details: object) -> None:
    if status not in {"completed", "failed", "stopped", "invalidated"}:
        raise ValueError(f"unsupported terminal status: {status}")
    if not (output_dir / "RUN_STARTED.json").is_file():
        raise ValueError("run has no RUN_STARTED.json")
    terminal = tuple(output_dir.glob("RUN_*.json"))
    if any(path.name != "RUN_STARTED.json" for path in terminal):
        raise FileExistsError("run already has a terminal event")
    payload = {
        "status": status,
        "finished_utc": datetime.now(UTC).isoformat(),
        **details,
    }
    _write_new(output_dir / f"RUN_{status.upper()}.json", payload)


def _write_new(path: Path, payload: dict[str, object]) -> None:
    with path.open("x", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        _ = handle.write("\n")


def _read_object(path: Path, message: str) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(message) from error
    if not isinstance(value, dict):
        raise ValueError(message)
    return value


def _canonical_sha256(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
