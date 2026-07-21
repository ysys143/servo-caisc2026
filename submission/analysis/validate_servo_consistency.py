#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Final

import yaml

HERE: Final = Path(__file__).resolve().parent
ROOT: Final = HERE.parent
SCHEMA_PATH: Final = HERE / "servo_schema.yaml"
LEGACY_SCHEMA_VERSION: Final = "1.0.0"
SYSTEMS_PATH: Final = HERE / "servo_core_systems.csv"
CHANNELS_PATH: Final = HERE / "servo_validator_channels.csv"
LEDGER_PATH: Final = HERE / "core_servo_evidence_ledger.json"
CLAIM_MAP_PATH: Final = HERE / "servo_claim_map.csv"
SOURCE_MANIFEST_PATH: Final = HERE / "citation_audit" / "core14-manifest.json"
REPORT_PATH: Final = HERE / "servo_derived_closure.json"
MANIFEST_PATH: Final = HERE / "servo_validation_manifest.json"

CANONICAL_INPUTS: Final = (SCHEMA_PATH, SYSTEMS_PATH, CHANNELS_PATH, LEDGER_PATH, CLAIM_MAP_PATH)
AUTHORITY_FIELDS: Final = ("H_S", "H_G", "H_E", "H_V", "H_M", "H_pi")
TRUSTED_SOURCE_MANIFEST_SHA256: Final = "db06a01f48314d8cb7ca92bfcba8138e1fce6b9e9a930960d393cc15f93aa2db"
TRUSTED_EVIDENCE_LEDGER_SHA256: Final = "4464213a2c1207ce9a3ea7704889ecf2a28e3fe9d84f3839eb3b5b9ddee5df91"
TRUSTED_PROTECTED_PDF_SHA256: Final = {
    "main.pdf": "7d48eeb1c71ed2cd12e9a677d62587d5f749c5ec19bd8faf0dc9926801bc138d",
    "servo_caiscfp2026.pdf": "7d48eeb1c71ed2cd12e9a677d62587d5f749c5ec19bd8faf0dc9926801bc138d",
}


class ValidationError(Exception):
    pass


def split_values(value: str) -> set[str]:
    return {part.strip() for part in value.split(";") if part.strip()}


def tex_inputs(source: str) -> set[str]:
    uncommented = "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in source.splitlines())
    return set(re.findall(r"\\input\{([^}]+)\}", uncommented))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_inputs() -> tuple[dict[str, Any], list[dict[str, str]], list[dict[str, str]], dict[str, Any]]:
    with SCHEMA_PATH.open(encoding="utf-8") as handle:
        schema = yaml.safe_load(handle)
    schema_version = str(schema.get("schema_version", ""))
    if schema_version != LEGACY_SCHEMA_VERSION:
        raise ValidationError(
            "Servo Schema 1 validator is historical and non-authoritative; "
            f"it cannot consume current Schema {schema_version or 'unknown'} inputs. "
            "Use `python -m analysis.validate_servo2`."
        )
    with LEDGER_PATH.open(encoding="utf-8") as handle:
        ledger = json.load(handle)
    return schema, read_csv(SYSTEMS_PATH), read_csv(CHANNELS_PATH), ledger


def derive_closure(channels: list[dict[str, str]], derivation: dict[str, Any] | None = None) -> tuple[bool, list[str]]:
    if derivation is None:
        derivation = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))["derivations"]["computational_closure"]
    qualifying = set(derivation["qualifying_destinations"])
    excluded = set(derivation["excluded_destinations"])
    required_status = derivation["qualifying_operational_status"]
    witnesses: list[str] = []
    for row in channels:
        destinations = split_values(row["routed_destination"])
        if (
            row["operational_status"] == required_status
            and row["trigger_phase"] != "external"
            and destinations & qualifying
            and not destinations & excluded
        ):
            witnesses.append(row["channel_id"])
    return bool(witnesses), sorted(witnesses)


def validate() -> tuple[list[dict[str, Any]], dict[str, str]]:
    schema, systems, channels, ledger = load_inputs()
    errors: list[str] = []
    if sha256(SOURCE_MANIFEST_PATH) != TRUSTED_SOURCE_MANIFEST_SHA256:
        errors.append("trust root: citation-audit source manifest hash mismatch")
    if sha256(LEDGER_PATH) != TRUSTED_EVIDENCE_LEDGER_SHA256:
        errors.append("trust root: evidence ledger hash mismatch")
    disk_ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    if ledger != disk_ledger:
        errors.append("trust root: loaded evidence ledger differs from the sealed ledger")
    version = str(schema.get("schema_version", ""))
    expected_ids = list(schema.get("scope", {}).get("core_record_ids", []))
    system_required = schema["system_record"]["required_fields"]
    channel_required = schema["channel_record"]["required_fields"]
    authority_enum = set(schema["system_record"]["enums"]["authority"])
    trigger_enum = set(schema["channel_record"]["enums"]["trigger_phase"])
    status_enum = set(schema["channel_record"]["enums"]["operational_status"])
    expected_system_header = list(system_required)
    expected_channel_header = list(channel_required)
    if systems and list(systems[0]) != expected_system_header:
        errors.append(f"servo_core_systems.csv: header must be exactly {expected_system_header!r}")
    if channels and list(channels[0]) != expected_channel_header:
        errors.append(f"servo_validator_channels.csv: header must be exactly {expected_channel_header!r}")
    if schema.get("historical_non_authoritative") != ["analysis/systems.csv#A_*", "analysis/multicoder/r24_final"]:
        errors.append("schema: historical_non_authoritative boundary changed")
    if not str(schema.get("provenance", {}).get("r24_boundary", "")).startswith("R24 is historical development-audit"):
        errors.append("schema: R24 boundary is missing or weakened")

    system_enums = schema["system_record"]["enums"]
    channel_enums = schema["channel_record"]["enums"]
    role_destinations = {
        role: set(destinations)
        for role, destinations in schema["channel_record"]["role_destination_compatibility"].items()
    }

    system_by_id: dict[str, dict[str, str]] = {}
    for line, row in enumerate(systems, start=2):
        rid = row.get("record_id", "")
        if rid in system_by_id:
            errors.append(f"servo_core_systems.csv:{line}: duplicate record_id {rid}")
        system_by_id[rid] = row
        for field in system_required:
            if not row.get(field, "").strip():
                errors.append(f"servo_core_systems.csv:{line}: {rid}: missing {field}")
        if row.get("schema_version") != version:
            errors.append(f"servo_core_systems.csv:{line}: {rid}: schema version mismatch")
        for field in AUTHORITY_FIELDS:
            if row.get(field) not in authority_enum:
                errors.append(f"servo_core_systems.csv:{line}: {rid}: invalid {field}={row.get(field)!r}")
        for field in ("delta_S_status", "O_env_status", "fidelity_choice_status", "cost_function_status", "budget_state_status", "policy_class", "evidential_status"):
            if row.get(field) not in set(system_enums[field]):
                errors.append(f"servo_core_systems.csv:{line}: {rid}: invalid {field}={row.get(field)!r}")
        if any("multicoder/r24_final" in value for value in row.values()):
            errors.append(f"servo_core_systems.csv:{line}: {rid}: historical R24 provenance leaked into current record")

    if list(system_by_id) != expected_ids:
        errors.append(f"servo_core_systems.csv: records must be exactly {expected_ids!r} in order")

    ledger_evidence: dict[str, tuple[str, str, int, str]] = {}
    for section in ("channels", "components"):
        for item in ledger.get(section, []):
            for evidence in item.get("evidence", []):
                eid = evidence["evidence_id"]
                owner = (evidence["record_id"], evidence["pdf_sha256"], evidence["pdf_page"], evidence["quote"])
                previous = ledger_evidence.get(eid)
                if previous is not None and previous != owner:
                    errors.append(f"ledger: evidence {eid} has conflicting owners {previous!r} and {owner!r}")
                ledger_evidence[eid] = owner

    channels_by_record: dict[str, list[dict[str, str]]] = defaultdict(list)
    evidence_channel_targets: dict[str, set[str]] = defaultdict(set)
    keys: set[tuple[str, str]] = set()
    for line, row in enumerate(channels, start=2):
        rid = row.get("record_id", "")
        key = (rid, row.get("channel_id", ""))
        if key in keys:
            errors.append(f"servo_validator_channels.csv:{line}: duplicate channel key {key!r}")
        keys.add(key)
        for field in channel_required:
            if not row.get(field, "").strip():
                errors.append(f"servo_validator_channels.csv:{line}: {key}: missing {field}")
        if rid not in system_by_id:
            errors.append(f"servo_validator_channels.csv:{line}: unknown record_id {rid}")
            continue
        system = system_by_id[rid]
        if row.get("schema_version") != version:
            errors.append(f"servo_validator_channels.csv:{line}: {key}: schema version mismatch")
        if row.get("system") != system.get("system"):
            errors.append(f"servo_validator_channels.csv:{line}: {key}: system identity mismatch")
        if row.get("source_pdf_sha256") != system.get("source_pdf_sha256"):
            errors.append(f"servo_validator_channels.csv:{line}: {key}: source hash mismatch")
        if row.get("trigger_phase") not in trigger_enum:
            errors.append(f"servo_validator_channels.csv:{line}: {key}: invalid trigger phase")
        if row.get("operational_status") not in status_enum:
            errors.append(f"servo_validator_channels.csv:{line}: {key}: invalid operational status")
        for field in ("trigger_phase", "operational_status", "evidential_status", "external_independence", "reliability_finding", "fidelity"):
            if row.get(field) not in set(channel_enums[field]):
                errors.append(f"servo_validator_channels.csv:{line}: {key}: invalid {field}={row.get(field)!r}")
        for field in ("target_property", "evidence_source", "evaluator_substrate", "decision_role", "routed_destination", "reliability_evidence_type"):
            unknown = split_values(row.get(field, "")) - set(channel_enums[field])
            if unknown:
                errors.append(f"servo_validator_channels.csv:{line}: {key}: invalid {field} tokens {sorted(unknown)!r}")
        destinations = split_values(row.get("routed_destination", ""))
        if not destinations:
            errors.append(f"servo_validator_channels.csv:{line}: {key}: no routed destination")
        if row.get("trigger_phase") == "external" and row.get("operational_status") != "external":
            errors.append(f"servo_validator_channels.csv:{line}: {key}: external trigger must have external status")
        if row.get("operational_status") == "external" and row.get("trigger_phase") != "external":
            errors.append(f"servo_validator_channels.csv:{line}: {key}: external status requires external trigger")
        if "terminal_only" in destinations and row.get("trigger_phase") != "terminal":
            errors.append(f"servo_validator_channels.csv:{line}: {key}: terminal_only requires terminal trigger")
        if "external_only" in destinations and row.get("trigger_phase") != "external":
            errors.append(f"servo_validator_channels.csv:{line}: {key}: external_only requires external trigger")
        roles = split_values(row.get("decision_role", ""))
        for role in roles:
            if not destinations & role_destinations[role]:
                errors.append(f"servo_validator_channels.csv:{line}: {key}: role {role} has no compatible routed destination")
        if "terminal_assessment" in roles and row.get("trigger_phase") != "terminal":
            errors.append(f"servo_validator_channels.csv:{line}: {key}: terminal assessment requires terminal trigger")
        if roles & {"external_assessment", "final_acceptance"} and row.get("trigger_phase") != "external":
            errors.append(f"servo_validator_channels.csv:{line}: {key}: external assessment or acceptance requires external trigger")
        if "memory_admission" in roles and "memory_update" not in destinations:
            errors.append(f"servo_validator_channels.csv:{line}: {key}: memory admission requires memory_update route")
        if "stage_transition" in roles and "stage_transition" not in destinations:
            errors.append(f"servo_validator_channels.csv:{line}: {key}: stage-transition role requires stage_transition route")
        for eid in split_values(row.get("evidence_ids", "")):
            evidence_channel_targets[eid] |= split_values(row.get("target_property", ""))
            owner = ledger_evidence.get(eid)
            if owner is None:
                errors.append(f"servo_validator_channels.csv:{line}: {key}: unknown evidence {eid}")
            elif owner[:2] != (rid, row.get("source_pdf_sha256")):
                errors.append(f"servo_validator_channels.csv:{line}: {key}: evidence {eid} belongs to {owner[:2]!r}")
        channels_by_record[rid].append(row)

    ledger_channel_keys = {(item.get("record_id", ""), item.get("channel_id", "")) for item in ledger.get("channels", [])}
    if ledger_channel_keys != keys:
        errors.append(
            "ledger: channel identities must exactly match canonical channel rows; "
            f"missing={sorted(keys - ledger_channel_keys)!r} extra={sorted(ledger_channel_keys - keys)!r}"
        )

    for line, row in enumerate(systems, start=2):
        rid = row["record_id"]
        for eid in split_values(row["evidence_ids"]):
            owner = ledger_evidence.get(eid)
            if owner is None:
                errors.append(f"servo_core_systems.csv:{line}: {rid}: unknown evidence {eid}")
            elif owner[:2] != (rid, row["source_pdf_sha256"]):
                errors.append(f"servo_core_systems.csv:{line}: {rid}: evidence {eid} belongs to {owner[:2]!r}")
        if row["fidelity_choice_status"] == "policy_selects_fidelity":
            if row["cost_function_status"] != "explicit" or row["budget_state_status"] != "explicit_dynamic_state":
                errors.append(f"servo_core_systems.csv:{line}: {rid}: cost-aware fidelity policy lacks explicit cost/budget")

    derived: list[dict[str, Any]] = []
    for rid in expected_ids:
        closed, witnesses = derive_closure(channels_by_record[rid], schema["derivations"]["computational_closure"])
        derived.append(
            {
                "record_id": rid,
                "system": system_by_id[rid]["system"],
                "computational_closure": closed,
                "qualifying_channel_ids": witnesses,
                    "rule": "implemented channel routed to later G/pi/M/stage/S and not terminal-only or external-only",
            }
        )

    claims = read_csv(CLAIM_MAP_PATH)
    expected_claim_header = ["claim_id", "status", "topic", "canonical_fields", "evidence_ids", "en_location", "ko_location", "appendix_d_entry", "note"]
    if claims and list(claims[0]) != expected_claim_header:
        errors.append(f"servo_claim_map.csv: header must be exactly {expected_claim_header!r}")
    en_labels = set(re.findall(r"\\label\{([^}]+)\}", (ROOT / "main_post-submit.tex").read_text(encoding="utf-8")))
    ko_labels = set(re.findall(r"\\label\{([^}]+)\}", (ROOT / "main_ko.tex").read_text(encoding="utf-8")))
    declared_generated_labels = set(schema.get("scope", {}).get("generated_projection_labels", []))
    en_projection = HERE / "tbl-core.tex"
    en_channel_projection = HERE / "tbl-core-channels.tex"
    ko_projection = HERE / "tbl-core-ko.tex"
    ko_channel_projection = HERE / "tbl-core-channels-ko.tex"
    actual_en_generated = set(re.findall(r"\\label\{([^}]+)\}", en_projection.read_text(encoding="utf-8") + en_channel_projection.read_text(encoding="utf-8")))
    actual_ko_generated = set(re.findall(r"\\label\{([^}]+)\}", ko_projection.read_text(encoding="utf-8") + ko_channel_projection.read_text(encoding="utf-8")))
    if actual_en_generated != declared_generated_labels or actual_ko_generated != declared_generated_labels:
        errors.append("generated projection labels do not exactly match schema declarations in both languages")
    en_labels |= actual_en_generated
    ko_labels |= actual_ko_generated
    en_source = (ROOT / "main_post-submit.tex").read_text(encoding="utf-8")
    ko_source = (ROOT / "main_ko.tex").read_text(encoding="utf-8")
    en_inputs = tex_inputs(en_source)
    ko_inputs = tex_inputs(ko_source)
    for required in ("analysis/tbl-core.tex", "analysis/tbl-core-channels.tex", "analysis/tbl-framework-crosswalk.tex"):
        if required not in en_inputs:
            errors.append(f"English manuscript does not input generated projection {required}")
    for required in ("analysis/tbl-core-ko.tex", "analysis/tbl-core-channels-ko.tex", "analysis/tbl-framework-crosswalk-ko.tex"):
        if required not in ko_inputs:
            errors.append(f"Korean manuscript does not input generated projection {required}")
    allowed_canonical_fields = (
        set(system_required)
        | set(channel_required)
        | {
            "scope.components",
            "system_record.required_fields",
            "channel_record.required_fields",
            "channel_record.split_rule",
            "derivations.computational_closure",
            "servo_derived_closure.json",
            "provenance.r24_boundary",
            "historical_non_authoritative",
            "not_applicable",
        }
    )
    claim_ids: set[str] = set()
    for line, claim in enumerate(claims, start=2):
        cid = claim.get("claim_id", "")
        if not cid or cid in claim_ids:
            errors.append(f"servo_claim_map.csv:{line}: missing or duplicate claim_id {cid!r}")
        claim_ids.add(cid)
        if claim.get("status") not in {"current", "historical", "superseded"}:
            errors.append(f"servo_claim_map.csv:{line}: {cid}: invalid status")
        if claim.get("status") == "current":
            if not claim.get("en_location") or not claim.get("ko_location"):
                errors.append(f"servo_claim_map.csv:{line}: {cid}: current claim lacks bilingual locations")
            if any(token in claim.get("canonical_fields", "") for token in ("A_", "V_present", "V_gating", "Vcompleteness")):
                errors.append(f"servo_claim_map.csv:{line}: {cid}: current claim uses a legacy field")
            for label in split_values(claim.get("en_location", "")):
                if label not in en_labels:
                    errors.append(f"servo_claim_map.csv:{line}: {cid}: unknown English label {label}")
            for label in split_values(claim.get("ko_location", "")):
                if label not in ko_labels:
                    errors.append(f"servo_claim_map.csv:{line}: {cid}: unknown Korean label {label}")
        for field in split_values(claim.get("canonical_fields", "")):
            normalized = field.removeprefix("schema.")
            if normalized not in allowed_canonical_fields:
                errors.append(f"servo_claim_map.csv:{line}: {cid}: unknown canonical field {field}")
        if "multicoder/r24_final" in claim.get("canonical_fields", "") and claim.get("status") == "current":
            errors.append(f"servo_claim_map.csv:{line}: {cid}: R24 cannot support a current claim")
        evidence_refs = split_values(claim.get("evidence_ids", ""))
        for eid in evidence_refs - {"not_applicable", "@all_channel_evidence", "@all_system_evidence"}:
            if eid not in ledger_evidence:
                errors.append(f"servo_claim_map.csv:{line}: {cid}: unknown evidence reference {eid}")
        constraint = schema.get("claim_inventory", {}).get("evidence_constraints", {}).get(cid)
        if constraint and evidence_refs:
            required_target = constraint["channel_target_property"]
            for eid in evidence_refs:
                if eid not in {"not_applicable", "@all_channel_evidence", "@all_system_evidence"} and required_target not in evidence_channel_targets.get(eid, set()):
                    errors.append(f"servo_claim_map.csv:{line}: {cid}: evidence {eid} is not bound to a {required_target} channel")

    required_claims = {key: value for key, value in schema["claim_inventory"].items() if key != "evidence_constraints"}
    actual_claims = {claim["claim_id"]: claim["status"] for claim in claims}
    if actual_claims != required_claims:
        errors.append(f"servo_claim_map.csv: exact claim inventory mismatch: expected {required_claims!r}, got {actual_claims!r}")
    appendix_entries = set(re.findall(r"\\item\[(R\d+)\.", en_source))
    for line, claim in enumerate(claims, start=2):
        for entry in split_values(claim.get("appendix_d_entry", "")):
            if entry not in appendix_entries:
                errors.append(f"servo_claim_map.csv:{line}: {claim.get('claim_id')}: unknown Appendix D entry {entry}")

    current_payloads = [systems, channels, claims, ledger]
    if any("multicoder/r24_final" in json.dumps(payload, ensure_ascii=False) for payload in current_payloads):
        errors.append("current canonical inputs contain forbidden R24 provenance")

    with SOURCE_MANIFEST_PATH.open(encoding="utf-8") as handle:
        source_manifest = json.load(handle)
    source_by_citation = {item["citation_key"]: item for item in source_manifest["sources"]}
    for row in systems:
        source = source_by_citation.get(row["citation_key"])
        if source is None:
            errors.append(f"source manifest: no source for {row['record_id']} citation {row['citation_key']}")
            continue
        source_path = Path(source["pdf_path"]).expanduser()
        if not source_path.is_file() or str(source_path).startswith(("http://", "https://")):
            errors.append(f"source manifest: unavailable local PDF for {row['record_id']}")
        elif sha256(source_path) != row["source_pdf_sha256"] or source["pdf_sha256"] != row["source_pdf_sha256"]:
            errors.append(f"source manifest: PDF hash mismatch for {row['record_id']}")

    if schema["provenance"]["protected_pdf_sha256"] != TRUSTED_PROTECTED_PDF_SHA256:
        errors.append("trust root: schema protected-PDF hashes differ from checker constants")
    for name, expected in TRUSTED_PROTECTED_PDF_SHA256.items():
        path = ROOT / name
        if not path.is_file() or sha256(path) != expected:
            errors.append(f"protected artifact: {name} hash mismatch")

    if errors:
        raise ValidationError("\n".join(errors))
    hashes = {path.name: sha256(path) for path in CANONICAL_INPUTS}
    return derived, hashes


def write_reports(derived: list[dict[str, Any]], hashes: dict[str, str]) -> None:
    schema_version = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))["schema_version"]
    REPORT_PATH.write_text(
        json.dumps({"schema_version": schema_version, "systems": derived}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    manifest = {
        "status": "PASS",
        "schema_version": schema_version,
        "canonical_input_sha256": hashes,
        "derived_output_sha256": {REPORT_PATH.name: sha256(REPORT_PATH)},
        "verification_input_sha256": verification_input_hashes(),
        "historical_inputs_used": [],
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def verification_input_hashes() -> dict[str, str]:
    source_manifest = json.loads(SOURCE_MANIFEST_PATH.read_text(encoding="utf-8"))
    values = {
        "main_post-submit.tex": sha256(ROOT / "main_post-submit.tex"),
        "main_ko.tex": sha256(ROOT / "main_ko.tex"),
        "citation_audit/core14-manifest.json": sha256(SOURCE_MANIFEST_PATH),
    }
    for source in source_manifest["sources"]:
        values[f"source:{source['index']:02d}:{Path(source['pdf_path']).name}"] = sha256(Path(source["pdf_path"]).expanduser())
    for name in TRUSTED_PROTECTED_PDF_SHA256:
        values[f"protected:{name}"] = sha256(ROOT / name)
    return values


def verify_generated() -> list[str]:
    errors: list[str] = []
    if not MANIFEST_PATH.is_file():
        return ["validation manifest is missing"]
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    expected_inputs = {path.name: sha256(path) for path in CANONICAL_INPUTS}
    if manifest.get("canonical_input_sha256") != expected_inputs:
        errors.append("validation manifest has stale canonical input hashes")
    if manifest.get("verification_input_sha256") != verification_input_hashes():
        errors.append("validation manifest has stale verification input hashes")
    expected_outputs = {
        "tbl-core.tex", "tbl-core-ko.tex", "tbl-core-channels.tex", "tbl-core-channels-ko.tex",
        "core_servo_channels.csv", "core_servo_channel_timing.csv", "core_servo_components.csv",
    }
    recorded = manifest.get("generated_artifact_sha256", {})
    if set(recorded) != expected_outputs:
        errors.append("validation manifest generated-artifact set is incomplete or has extras")
    for name in expected_outputs:
        path = HERE / name
        if not path.is_file():
            errors.append(f"generated artifact missing: {name}")
        elif recorded.get(name) != sha256(path):
            errors.append(f"generated artifact stale or tampered: {name}")
    if not REPORT_PATH.is_file() or manifest.get("derived_output_sha256", {}).get(REPORT_PATH.name) != sha256(REPORT_PATH):
        errors.append("derived closure report missing or stale")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--verify-generated", action="store_true")
    args = parser.parse_args(argv)
    try:
        derived, hashes = validate()
    except (ValidationError, KeyError, TypeError, yaml.YAMLError) as exc:
        print(f"SERVO VALIDATION FAILED:\n{exc}", file=sys.stderr)
        return 1
    if not args.check_only:
        write_reports(derived, hashes)
    if args.verify_generated:
        stale = verify_generated()
        if stale:
            print("SERVO GENERATED-ARTIFACT VERIFICATION FAILED:\n" + "\n".join(stale), file=sys.stderr)
            return 1
    print(f"SERVO VALIDATION PASS: {len(derived)} systems; schema {yaml.safe_load(SCHEMA_PATH.read_text())['schema_version']}")
    for row in derived:
        print(f"  {row['record_id']}: closure={str(row['computational_closure']).lower()} witnesses={','.join(row['qualifying_channel_ids'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
