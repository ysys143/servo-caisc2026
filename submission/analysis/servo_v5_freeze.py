from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Mapping, Sequence, TypedDict

from .servo_v5_io import V5_SCHEMA_VERSION, ServoV5Error, read_json, sha256
from .servo_v5_verify import verify_root

MANIFEST_NAME: Final = "servo_v5_source_freeze_manifest.json"
WARNING_AUDIT_NAME: Final = "servo_v5_warning_dispositions.json"
SOURCE_DIRNAME: Final = "servo_v5_source_propositions"
EXPECTED_CASES: Final = frozenset({"C01", "C02", "C03", "C04", "C05", "C06"})
T5_CONSUMABLE_FIELDS: Final = (
    "proposition_id",
    "locator",
    "exact_quote",
    "modality",
    "named_actors",
    "named_inputs",
    "named_outputs",
)
_COVERAGE_STATUSES: Final = frozenset(
    {
        "body_complete",
        "body_complete_appendix_partial",
        "config_bounded_complete",
        "review_bounded_complete",
    }
)
_SEMANTIC_LEAK_MARKERS: Final = (
    "memory update",
    "memory-update",
    "repair channel",
    "candidate conditioning",
    "human-authority boundary",
    "observation-to-state",
    "evaluation-to-artifact",
    "policy adaptation",
    "bed-like",
    "score-directed",
    "outcome-conditioned",
    "closure status",
    "servo component",
    "functional relation",
    "closed-loop recurrence",
)
_WARNING_PATTERN: Final = re.compile(r"case=(C[0-9]{2}) proposition=(C[0-9]{2}-P[0-9]{2})")


class SourceProjection(TypedDict):
    proposition_id: str
    locator: dict[str, int | str]
    exact_quote: str
    modality: str
    named_actors: list[str]
    named_inputs: list[str]
    named_outputs: list[str]


class CaseFreezeRecord(TypedDict):
    status: str
    coverage_status: str
    ledger_sha256: str
    source_pdf_sha256: str
    proposition_count: int
    proposition_ids: list[str]


class SourceFreezeManifest(TypedDict):
    schema: str
    schema_version: str
    rules_version: str
    source_set_sha256: str
    rule_file_sha256: dict[str, str]
    warning_audit_sha256: str
    current_warning_ids: list[str]
    t5_consumable_fields: list[str]
    downstream_invalidation: dict[str, str | list[str]]
    cases: dict[str, CaseFreezeRecord]


@dataclass(frozen=True, slots=True)
class FreezeIssue:
    code: str
    message: str
    case_id: str = ""
    record_id: str = ""

    def __str__(self) -> str:
        return f"{self.code} case={self.case_id} record={self.record_id}: {self.message}"


def _string(value: object, field: str) -> str:
    if not isinstance(value, str):
        raise ServoV5Error("V5_FREEZE_FIELD_INVALID", field)
    return value


def _string_list(value: object, field: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ServoV5Error("V5_FREEZE_FIELD_INVALID", field)
    return list(value)


def _locator(value: object) -> dict[str, int | str]:
    if not isinstance(value, dict):
        raise ServoV5Error("V5_FREEZE_FIELD_INVALID", "locator")
    if not all(isinstance(key, str) and isinstance(item, (int, str)) for key, item in value.items()):
        raise ServoV5Error("V5_FREEZE_FIELD_INVALID", "locator")
    return dict(value)


def project_source_proposition(proposition: Mapping[str, object]) -> SourceProjection:
    return SourceProjection(
        proposition_id=_string(proposition.get("proposition_id"), "proposition_id"),
        locator=_locator(proposition.get("locator")),
        exact_quote=_string(proposition.get("exact_quote"), "exact_quote"),
        modality=_string(proposition.get("modality"), "modality"),
        named_actors=_string_list(proposition.get("named_actors"), "named_actors"),
        named_inputs=_string_list(proposition.get("named_inputs"), "named_inputs"),
        named_outputs=_string_list(proposition.get("named_outputs"), "named_outputs"),
    )


def validate_context_note(case_id: str, proposition_id: str, note: str) -> list[FreezeIssue]:
    lowered = note.casefold()
    markers = [marker for marker in _SEMANTIC_LEAK_MARKERS if marker in lowered]
    if not markers:
        return []
    return [
        FreezeIssue(
            "V5_SOURCE_SEMANTIC_LEAK",
            f"source_context_note contains T5 semantics: {', '.join(markers)}",
            case_id,
            proposition_id,
        )
    ]


def _warning_ids(warnings: Sequence[str]) -> set[str]:
    result: set[str] = set()
    for warning in warnings:
        match = _WARNING_PATTERN.search(warning)
        if match is None:
            continue
        result.add(f"W-{match.group(2)}")
    return result


def validate_warning_dispositions(analysis_dir: Path, warnings: Sequence[str]) -> list[FreezeIssue]:
    payload = read_json(analysis_dir / WARNING_AUDIT_NAME)
    dispositions = payload.get("dispositions")
    if not isinstance(dispositions, list):
        return [FreezeIssue("V5_WARNING_AUDIT_INVALID", "dispositions must be a list")]
    active: set[str] = set()
    issues: list[FreezeIssue] = []
    for record in dispositions:
        if not isinstance(record, dict):
            issues.append(FreezeIssue("V5_WARNING_AUDIT_INVALID", "disposition must be an object"))
            continue
        warning_id = record.get("warning_id")
        status = record.get("status")
        if not isinstance(warning_id, str) or status not in {"active", "resolved_by_split"}:
            issues.append(FreezeIssue("V5_WARNING_AUDIT_INVALID", f"invalid warning_id/status: {warning_id}"))
            continue
        if status == "active":
            active.add(warning_id)
    current = _warning_ids(warnings)
    for warning_id in sorted(current - active):
        issues.append(FreezeIssue("V5_WARNING_DISPOSITION_MISSING", warning_id))
    for warning_id in sorted(active - current):
        issues.append(FreezeIssue("V5_WARNING_DISPOSITION_STALE", warning_id))
    return issues


def _canonical_sha(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def build_manifest(analysis_dir: Path, warnings: Sequence[str]) -> SourceFreezeManifest:
    cases: dict[str, CaseFreezeRecord] = {}
    for path in sorted((analysis_dir / SOURCE_DIRNAME).glob("C*.json")):
        payload = read_json(path)
        propositions = payload.get("propositions")
        if not isinstance(propositions, list):
            raise ServoV5Error("V5_FREEZE_FIELD_INVALID", f"{path}: propositions")
        proposition_ids = [
            _string(item.get("proposition_id"), "proposition_id")
            for item in propositions
            if isinstance(item, dict)
        ]
        cases[path.stem] = CaseFreezeRecord(
            status=_string(payload.get("status"), "status"),
            coverage_status=_string(payload.get("coverage_status"), "coverage_status"),
            ledger_sha256=sha256(path),
            source_pdf_sha256=_string(payload.get("source_pdf_sha256"), "source_pdf_sha256"),
            proposition_count=len(propositions),
            proposition_ids=proposition_ids,
        )
    rules = {
        name: sha256(analysis_dir / name)
        for name in ("servo_v5_charter.md", "servo_v5_schema.yaml", "servo_v5_source_proposition_schema.md")
    }
    warning_ids = sorted(_warning_ids(warnings))
    material = {"rules": rules, "warnings": warning_ids, "cases": cases}
    return SourceFreezeManifest(
        schema="servo_v5_source_freeze_manifest",
        schema_version=V5_SCHEMA_VERSION,
        rules_version="v5.0-rules/B.8",
        source_set_sha256=_canonical_sha(material),
        rule_file_sha256=rules,
        warning_audit_sha256=sha256(analysis_dir / WARNING_AUDIT_NAME),
        current_warning_ids=warning_ids,
        t5_consumable_fields=list(T5_CONSUMABLE_FIELDS),
        downstream_invalidation={
            "rule": "any_bound_sha256_change_invalidates_all_downstream_v5_artifacts",
            "families": ["author_alignment", "derived_claim", "policy", "evidence_projection"],
        },
        cases=cases,
    )


def _validate_sources(analysis_dir: Path) -> list[FreezeIssue]:
    paths = sorted((analysis_dir / SOURCE_DIRNAME).glob("C*.json"))
    issues: list[FreezeIssue] = []
    if {path.stem for path in paths} != EXPECTED_CASES:
        issues.append(FreezeIssue("V5_SOURCE_CASE_SET_INVALID", "expected exactly C01-C06"))
    for path in paths:
        payload = read_json(path)
        if payload.get("status") != "frozen":
            issues.append(FreezeIssue("V5_SOURCE_NOT_FROZEN", "status must be frozen", path.stem))
        if payload.get("coverage_status") not in _COVERAGE_STATUSES:
            issues.append(FreezeIssue("V5_SOURCE_COVERAGE_INCOMPLETE", "coverage_status is not freeze-ready", path.stem))
        propositions = payload.get("propositions")
        if not isinstance(propositions, list):
            continue
        for proposition in propositions:
            if not isinstance(proposition, dict):
                continue
            note = proposition.get("source_context_note")
            if isinstance(note, str):
                issues.extend(validate_context_note(path.stem, str(proposition.get("proposition_id", "")), note))
    return issues


def validate_manifest(analysis_dir: Path, warnings: Sequence[str]) -> list[FreezeIssue]:
    path = analysis_dir / MANIFEST_NAME
    if not path.is_file():
        return [FreezeIssue("V5_SOURCE_FREEZE_MANIFEST_MISSING", str(path))]
    expected = build_manifest(analysis_dir, warnings)
    if read_json(path) == expected:
        return []
    return [FreezeIssue("V5_SOURCE_FREEZE_STALE", "manifest does not match canonical source inputs")]


def validate_readiness(analysis_dir: Path, warnings: Sequence[str]) -> list[FreezeIssue]:
    return (
        _validate_sources(analysis_dir)
        + validate_warning_dispositions(analysis_dir, warnings)
        + validate_manifest(analysis_dir, warnings)
    )


def run(arguments: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="servo-v5-freeze")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    options = parser.parse_args(arguments)
    analysis_dir = options.root.resolve() / "analysis"
    pdf_errors, warnings = verify_root(analysis_dir, options.source_root.resolve())
    issues = _validate_sources(analysis_dir) + validate_warning_dispositions(analysis_dir, warnings)
    if not pdf_errors and not issues and options.write:
        manifest = build_manifest(analysis_dir, warnings)
        (analysis_dir / MANIFEST_NAME).write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    issues += validate_manifest(analysis_dir, warnings)
    for error in pdf_errors:
        print(str(error), file=sys.stderr)
    for issue in issues:
        print(str(issue), file=sys.stderr)
    if pdf_errors or issues:
        print("SERVO_V5_SOURCE_FREEZE_FAILED", file=sys.stderr)
        return 1
    print(f"SERVO_V5_SOURCE_FREEZE_OK: {len(build_manifest(analysis_dir, warnings)['cases'])} cases")
    return 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
