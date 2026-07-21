from __future__ import annotations

import json
from pathlib import Path

from .servo2_io import Servo2Error, Table, split_values


EVIDENCE_TABLES = (
    "cases",
    "artifacts",
    "events",
    "edges",
    "reliability",
    "closure_witnesses",
)


def sanitize_ledger(source: Path) -> bytes:
    try:
        value = json.loads(source.read_text(encoding="utf-8"))
        groups = value["components"] + value["channels"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise Servo2Error("EVIDENCE_LEDGER_INVALID", str(source)) from error
    indexed: dict[str, dict[str, str | int]] = {}
    for group in groups:
        for evidence in group["evidence"]:
            entry = {
                "evidence_id": evidence["evidence_id"],
                "owner_record_id": evidence["record_id"],
                "pdf_sha256": evidence["pdf_sha256"],
                "pdf_page": evidence["pdf_page"],
                "exact_quote": evidence["quote"],
            }
            identifier = str(entry["evidence_id"])
            prior = indexed.get(identifier)
            if prior is not None and prior != entry:
                raise Servo2Error("EVIDENCE_ID_CONFLICT", identifier)
            indexed[identifier] = entry
    payload = {
        "schema_version": "3.0.0",
        "evidence": [indexed[key] for key in sorted(indexed)],
    }
    return (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode()


def validate_evidence(root: Path, tables: dict[str, Table]) -> None:
    path = root / "analysis" / "servo2_evidence_ledger.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        entries = value["evidence"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise Servo2Error("EVIDENCE_LEDGER_INVALID", str(path)) from error
    indexed: dict[str, dict[str, str | int]] = {}
    for entry in entries:
        identifier = entry.get("evidence_id")
        if not isinstance(identifier, str) or identifier in indexed:
            raise Servo2Error("EVIDENCE_LEDGER_INVALID", "duplicate or malformed ID")
        if (
            not isinstance(entry.get("owner_record_id"), str)
            or not isinstance(entry.get("pdf_sha256"), str)
            or not isinstance(entry.get("pdf_page"), int)
            or not isinstance(entry.get("exact_quote"), str)
            or entry["pdf_page"] < 1
            or entry["exact_quote"] == ""
        ):
            raise Servo2Error("EVIDENCE_PROVENANCE_INCOMPLETE", identifier)
        indexed[identifier] = entry
    case_owner = {
        row["case_id"]: row["evidence_ids"].split("-")[0]
        for row in tables["cases"].rows
    }
    for table_name in EVIDENCE_TABLES:
        for row in tables[table_name].rows:
            owner = case_owner[row["case_id"]]
            for evidence_id in split_values(row["evidence_ids"]):
                entry = indexed.get(evidence_id)
                if entry is None:
                    raise Servo2Error("EVIDENCE_FOREIGN_KEY_UNKNOWN", evidence_id)
                if entry["owner_record_id"] != owner:
                    raise Servo2Error("EVIDENCE_OWNER_MISMATCH", evidence_id)
    _validate_anchor_channel_evidence(tables)


def _validate_anchor_channel_evidence(tables: dict[str, Table]) -> None:
    anchors = {row["anchor_id"]: row for row in tables["domain_anchors"].rows}
    for row in tables["domain_anchor_channels"].rows:
        anchor = anchors.get(row["anchor_id"])
        if anchor is None:
            continue
        if (
            row["exact_quote"] not in anchor["exact_quote"]
            and row["anchor_id"] != "DA05"
        ):
            raise Servo2Error(
                "ANCHOR_CHANNEL_EVIDENCE_OWNER_MISMATCH", row["channel_id"]
            )
        if row["evidence_status"] not in {
            "directly_stated",
            "structurally_inferred",
            "mixed_direct_and_inferred",
            "not_yet_source_adjudicated",
        }:
            raise Servo2Error(
                "ANCHOR_CHANNEL_EVIDENCE_STATUS_INVALID", row["channel_id"]
            )
