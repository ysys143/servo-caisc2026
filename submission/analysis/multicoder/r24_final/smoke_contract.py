from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter

from r24_final.hook_negative import build_report


HashValue = str


class FrozenModel(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid", frozen=True)


class StaticEvidence(FrozenModel):
    evidence_type: Literal["static-gate-v1"]
    protocol_sha256: HashValue = Field(pattern=r"^[0-9a-f]{64}$")
    schedule_sha256: HashValue = Field(pattern=r"^[0-9a-f]{64}$")
    generation_trial_count: Literal[42]
    unique_generation_cells: Literal[42]
    source_packet_count: Literal[14]
    core_record_ids: frozenset[str] = Field(min_length=6, max_length=6)
    supplementary_record_count: Literal[8]
    prompt_leakage_findings: tuple[str, ...] = Field(max_length=0)
    packet_binding_failures: tuple[str, ...] = Field(max_length=0)
    command_contract_failures: tuple[str, ...] = Field(max_length=0)
    schema_failures: tuple[str, ...] = Field(max_length=0)
    scoring_key_failures: tuple[str, ...] = Field(max_length=0)


class IsolationCell(FrozenModel):
    cell_id: str
    trial_root: str = Field(min_length=1)
    artifact_root: str = Field(min_length=1)
    artifact_tree_sha256: HashValue = Field(pattern=r"^[0-9a-f]{64}$")
    attack_invocation_id: str = Field(min_length=1)
    attack_prompt_sha256: HashValue = Field(pattern=r"^[0-9a-f]{64}$")
    canary_sha256: HashValue = Field(pattern=r"^[0-9a-f]{64}$")
    stdout_sha256: HashValue = Field(pattern=r"^[0-9a-f]{64}$")
    stderr_sha256: HashValue = Field(pattern=r"^[0-9a-f]{64}$")
    process_policy_sha256: HashValue = Field(pattern=r"^[0-9a-f]{64}$")
    forbidden_tool_events: Literal[0]
    outside_canary_hits: Literal[0]
    scoring_asset_hits: Literal[0]
    cross_trial_hits: Literal[0]


class IsolationEvidence(FrozenModel):
    evidence_type: Literal["task-isolation-v1"]
    protocol_sha256: HashValue = Field(pattern=r"^[0-9a-f]{64}$")
    cells: tuple[IsolationCell, ...] = Field(min_length=3, max_length=3)


class FunctionalCell(FrozenModel):
    cell_id: str
    invocation_id: str = Field(min_length=1)
    trial_root: str = Field(min_length=1)
    artifact_root: str = Field(min_length=1)
    artifact_tree_sha256: HashValue = Field(pattern=r"^[0-9a-f]{64}$")
    returncode: Literal[0]
    accepted: Literal[True]
    prompt_sha256: HashValue = Field(pattern=r"^[0-9a-f]{64}$")
    packet_sha256: HashValue = Field(pattern=r"^[0-9a-f]{64}$")
    schema_sha256: HashValue = Field(pattern=r"^[0-9a-f]{64}$")
    stdout_sha256: HashValue = Field(pattern=r"^[0-9a-f]{64}$")
    stderr_sha256: HashValue = Field(pattern=r"^[0-9a-f]{64}$")


class FunctionalEvidence(FrozenModel):
    evidence_type: Literal["functional-matrix-v1"]
    protocol_sha256: HashValue = Field(pattern=r"^[0-9a-f]{64}$")
    cells: tuple[FunctionalCell, ...] = Field(min_length=3, max_length=3)
    latency_boundary_passed: Literal[True]


def verify_typed_evidence(
    report_name: str, path: Path, protocol_sha256: str, root: Path
) -> None:
    raw = path.read_text(encoding="utf-8")
    match report_name:
        case "STATIC_GATE_REPORT":
            evidence = StaticEvidence.model_validate_json(raw)
            if evidence.protocol_sha256 != protocol_sha256:
                raise ValueError("static evidence protocol mismatch")
            schedule_sha256 = hashlib.sha256(
                (root / "schedule.json").read_bytes()
            ).hexdigest()
            if evidence.schedule_sha256 != schedule_sha256:
                raise ValueError("static evidence schedule mismatch")
        case "HOOK_NEGATIVE_REPORT":
            if json.loads(raw) != build_report():
                raise ValueError("hook evidence does not match a fresh production-hook run")
        case "ISOLATION_REPORT":
            evidence = IsolationEvidence.model_validate_json(raw)
            _verify_cells(evidence.cells, protocol_sha256, evidence.protocol_sha256)
            _verify_artifacts(evidence.cells, root)
        case "FUNCTIONAL_REPORT":
            evidence = FunctionalEvidence.model_validate_json(raw)
            _verify_cells(evidence.cells, protocol_sha256, evidence.protocol_sha256)
            _verify_artifacts(evidence.cells, root)
        case _:
            raise ValueError(f"unknown typed smoke report: {report_name}")




def _verify_cells(
    cells: tuple[IsolationCell, ...] | tuple[FunctionalCell, ...],
    expected_protocol: str,
    observed_protocol: str,
) -> None:
    expected_cells = {
        f"{vendor}:{condition}"
        for vendor in ("claude", "codex", "gemini")
        for condition in ("servo",)
    }
    if observed_protocol != expected_protocol:
        raise ValueError("smoke evidence protocol mismatch")
    if {cell.cell_id for cell in cells} != expected_cells:
        raise ValueError("smoke evidence must contain the exact three Servo vendor cells")
    if len({cell.trial_root for cell in cells}) != 3:
        raise ValueError("each smoke cell must use a fresh trial root")


def artifact_tree_sha256(path: Path) -> str:
    entries = {
        str(item.relative_to(path)): hashlib.sha256(item.read_bytes()).hexdigest()
        for item in sorted(path.rglob("*"))
        if item.is_file()
    }
    canonical = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(canonical).hexdigest()


def _verify_artifacts(
    cells: tuple[IsolationCell, ...] | tuple[FunctionalCell, ...], root: Path
) -> None:
    smoke_root = (root / "smoke_reports").resolve()
    for cell in cells:
        artifact = (root / cell.artifact_root).resolve()
        if smoke_root not in artifact.parents or not artifact.is_dir():
            raise ValueError(f"observer artifact escapes or is absent: {cell.artifact_root}")
        if artifact_tree_sha256(artifact) != cell.artifact_tree_sha256:
            raise ValueError(f"observer artifact tree hash mismatch: {cell.cell_id}")


SMOKE_EVIDENCE_ADAPTER = TypeAdapter(
    StaticEvidence | IsolationEvidence | FunctionalEvidence
)
