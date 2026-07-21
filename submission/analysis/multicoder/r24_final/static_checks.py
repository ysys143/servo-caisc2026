from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Final

from r24_final.adapters import build_command
from r24_final.evidence import EvidencePacket
from r24_final.run_experiment import build_prompt
from r24_final.runner import load_schedule
from r24_final.schedule import Condition
from r24_final.scoring import load_probe_key
from r24_final.smoke_contract import StaticEvidence


CORE_RECORD_IDS: Final = frozenset({"R01", "R02", "R03", "R04", "R05", "R14"})


def build_static_evidence(root: Path, protocol_sha256: str) -> StaticEvidence:
    schedule = load_schedule(root / "schedule.json")
    action_tokens = tuple(json.loads((root / "action_codes.json").read_text()))
    manual = (root / "coding_manual.md").read_text(encoding="utf-8")
    leakage: list[str] = []
    command_failures: list[str] = []
    for trial in schedule:
        prompt = build_prompt(root, trial.record_id, trial.condition, trial.vendor)
        probe_key = load_probe_key(root / "probes" / f"{trial.record_id}.json")
        forbidden = tuple(
            value
            for probe in probe_key.probes
            for value in (probe.probe_id, probe.question)
        ) + action_tokens
        if any(value in prompt for value in forbidden):
            leakage.append(trial.trial_id)
        if trial.condition is Condition.BASELINE and manual in prompt:
            leakage.append(trial.trial_id)
        try:
            build_command(trial, Path(f"{trial.condition.value}.schema.json"), root)
        except (ValueError, OSError) as error:
            command_failures.append(f"{trial.trial_id}:{error}")
    manifest = json.loads((root / "manifest/source_manifest.json").read_text())
    packet_failures: list[str] = []
    scoring_failures: list[str] = []
    for record in manifest["records"]:
        record_id = record["record_id"]
        packet_path = root / record["packet_path"]
        packet = EvidencePacket.model_validate_json(packet_path.read_text())
        pdf_path = Path(record["local_pdf_path"]).expanduser()
        if hashlib.sha256(packet_path.read_bytes()).hexdigest() != record["packet_sha256"]:
            packet_failures.append(f"{record_id}:packet")
        if packet.pdf_id != record["pdf_sha256"] or packet.source.page_count != record["page_count"]:
            packet_failures.append(f"{record_id}:source")
        if not pdf_path.is_file() or hashlib.sha256(pdf_path.read_bytes()).hexdigest() != record["pdf_sha256"]:
            packet_failures.append(f"{record_id}:pdf")
        try:
            load_probe_key(root / record["probes_path"])
        except (ValueError, OSError) as error:
            scoring_failures.append(f"{record_id}:{error}")
    schema_failures = tuple(
        name
        for name in ("servo.schema.json",)
        if not isinstance(json.loads((root / name).read_text()), dict)
    )
    if len(schedule) != 42 or len({trial.trial_id for trial in schedule}) != 42:
        raise ValueError("static schedule does not contain 42 unique trials")
    if len(manifest["records"]) != 14:
        raise ValueError("static source manifest does not contain 14 records")
    core_record_ids = frozenset(
        record["record_id"]
        for record in manifest["records"]
        if record.get("analysis_role") == "core"
    )
    supplementary_record_count = sum(
        record.get("analysis_role") == "supplementary"
        for record in manifest["records"]
    )
    if core_record_ids != CORE_RECORD_IDS:
        raise ValueError("static source manifest has incorrect core record identities")
    if supplementary_record_count != 8:
        raise ValueError("static source manifest must contain eight supplementary records")
    return StaticEvidence(
        evidence_type="static-gate-v1",
        protocol_sha256=protocol_sha256,
        schedule_sha256=hashlib.sha256((root / "schedule.json").read_bytes()).hexdigest(),
        generation_trial_count=42,
        unique_generation_cells=42,
        source_packet_count=14,
        core_record_ids=core_record_ids,
        supplementary_record_count=supplementary_record_count,
        prompt_leakage_findings=tuple(sorted(set(leakage))),
        packet_binding_failures=tuple(packet_failures),
        command_contract_failures=tuple(command_failures),
        schema_failures=schema_failures,
        scoring_key_failures=tuple(scoring_failures),
    )
