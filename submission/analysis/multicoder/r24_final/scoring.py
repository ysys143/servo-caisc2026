from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter

from r24_final.models import BaselineCoding, ServoCoding


class FrozenModel(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid", frozen=True)


class Probe(FrozenModel):
    probe_id: str = Field(pattern=r"^R\d{2}-P\d{2}$")
    question: str = Field(min_length=1)
    expected_answer: str = Field(pattern=r"^(yes|no|not_reported)$")
    evidence_ids: tuple[str, ...]


class ProbeKey(FrozenModel):
    schema_version: int
    record_id: str = Field(pattern=r"^R\d{2}$")
    completeness_boundary: str = Field(min_length=1)
    audit_boundary: str | None = None
    answer_options: tuple[str, ...]
    probes: tuple[Probe, ...]


class ChecklistScore(FrozenModel):
    record_id: str
    condition: str
    cited_reference_items: int
    reference_items: int
    evidence_recall: float = Field(ge=0, le=1)
    unsupported_evidence_ids: tuple[str, ...]
    scoring_key_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    output_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")


def load_probe_key(path: Path) -> ProbeKey:
    key = ProbeKey.model_validate_json(path.read_text(encoding="utf-8"))
    if key.record_id != path.stem:
        raise ValueError("probe record_id does not match filename")
    if len(key.probes) != 12 or len({probe.probe_id for probe in key.probes}) != 12:
        raise ValueError("each scoring key must contain twelve unique probes")
    for probe in key.probes:
        if probe.expected_answer == "not_reported" and probe.evidence_ids:
            raise ValueError("not_reported probes must not carry positive evidence")
        if probe.expected_answer != "not_reported" and not probe.evidence_ids:
            raise ValueError("reported probes require reference evidence")
    return key


def score_checklist(output_path: Path, probe_path: Path) -> ChecklistScore:
    output_bytes = output_path.read_bytes()
    raw = json.loads(output_bytes)
    condition = "servo" if "channels" in raw else "baseline"
    coding = (
        ServoCoding.model_validate(raw)
        if condition == "servo"
        else BaselineCoding.model_validate(raw)
    )
    key = load_probe_key(probe_path)
    if coding.record_id != key.record_id:
        raise ValueError("output and scoring-key record_id mismatch")
    cited = {
        evidence_id
        for item in (*coding.envelope.diagnostics, *coding.envelope.recommendations)
        for evidence_id in item.evidence_ids
    }
    reference = {
        evidence_id for probe in key.probes for evidence_id in probe.evidence_ids
    }
    recovered = cited & reference
    return ChecklistScore(
        record_id=key.record_id,
        condition=condition,
        cited_reference_items=len(recovered),
        reference_items=len(reference),
        evidence_recall=len(recovered) / len(reference) if reference else 0.0,
        unsupported_evidence_ids=tuple(sorted(cited - reference)),
        scoring_key_sha256=hashlib.sha256(probe_path.read_bytes()).hexdigest(),
        output_sha256=hashlib.sha256(output_bytes).hexdigest(),
    )


def scoring_assets_manifest(root: Path) -> dict[str, object]:
    paths = sorted((root / "probes").glob("R*.json"))
    for path in paths:
        load_probe_key(path)
    hashes = {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in paths
    }
    canonical = json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()
    return {
        "scoring_assets_sha256": hashlib.sha256(canonical).hexdigest(),
        "files": hashes,
    }


def score_many(output_paths: tuple[Path, ...], probes_dir: Path) -> tuple[ChecklistScore, ...]:
    scores = tuple(
        score_checklist(path, probes_dir / f"{json.loads(path.read_text())['record_id']}.json")
        for path in output_paths
    )
    return TypeAdapter(tuple[ChecklistScore, ...]).validate_python(scores)


def score_completed_generation(root: Path, run_dir: Path, output_path: Path) -> None:
    from r24_final.generation_snapshot import verify_generation_snapshot
    from r24_final.lifecycle import verify_smoke_gate

    verify_smoke_gate(root)
    if output_path.exists():
        raise FileExistsError(f"refusing to overwrite scoring output: {output_path}")
    completed = verify_generation_snapshot(root, run_dir)
    sealed = completed["accepted_outputs"]
    if not isinstance(sealed, dict) or len(sealed) != 84:
        raise ValueError("scoring requires a sealed 84-output generation run")
    accepted = tuple(run_dir / item["path"] for item in sealed.values())
    scores = score_many(accepted, root / "probes")
    payload = {
        "scoring_assets": scoring_assets_manifest(root),
        "scores": TypeAdapter(tuple[ChecklistScore, ...]).dump_python(
            scores, mode="json"
        ),
    }
    with output_path.open("x", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        _ = handle.write("\n")
