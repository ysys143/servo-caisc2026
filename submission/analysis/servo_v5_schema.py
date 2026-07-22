from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from .servo_v5_io import (
    ID_FIELD,
    ID_LETTER,
    RECORD_LIST_FIELD,
    V5_SCHEMA_VERSION,
    ServoV5Error,
    id_pattern_for,
    read_json,
)

SCHEMA_FILE_NAME = "servo_v5_schema.yaml"
CASE_REGISTRY_FILE_NAME = "servo2_cases.csv"


@dataclass(frozen=True, slots=True)
class ValidationError:
    code: str
    family: str
    case_id: str
    record_id: str
    message: str

    def __str__(self) -> str:
        return (
            f"{self.code} family={self.family} case={self.case_id} "
            f"record={self.record_id}: {self.message}"
        )


@dataclass(frozen=True, slots=True)
class SchemaContract:
    directories: dict[str, str]
    envelope_fields: dict[str, tuple[str, ...]]
    required_envelope_fields: dict[str, tuple[str, ...]]
    record_fields: dict[str, tuple[str, ...]]
    required_record_fields: dict[str, tuple[str, ...]]
    forbidden_record_fields: dict[str, tuple[str, ...]]
    enum_fields: dict[str, tuple[str, ...]]
    locator_required: tuple[str, ...]
    locator_optional: tuple[str, ...]


def load_contract(analysis_dir: Path) -> SchemaContract:
    path = analysis_dir / SCHEMA_FILE_NAME
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as error:
        raise ServoV5Error("V5_SCHEMA_CONTRACT_MISSING", str(path)) from error
    if not lines or lines[0] != f'schema_version: "{V5_SCHEMA_VERSION}"':
        raise ServoV5Error("V5_SCHEMA_VERSION_MISMATCH", str(path))
    locator = _list_mapping(lines, "locator_fields")
    return SchemaContract(
        directories=_scalar_mapping(lines, "directories"),
        envelope_fields=_list_mapping(lines, "envelope_fields"),
        required_envelope_fields=_list_mapping(lines, "required_envelope_fields"),
        record_fields=_list_mapping(lines, "record_fields"),
        required_record_fields=_list_mapping(lines, "required_record_fields"),
        forbidden_record_fields=_list_mapping(lines, "forbidden_record_fields"),
        enum_fields=_list_mapping(lines, "enum_fields"),
        locator_required=locator.get("required", ()),
        locator_optional=locator.get("optional", ()),
    )


def _section_lines(lines: list[str], section: str) -> list[str]:
    marker = f"{section}:"
    try:
        start = lines.index(marker) + 1
    except ValueError as error:
        raise ServoV5Error("V5_SCHEMA_DECLARATION_MISSING", section) from error
    body: list[str] = []
    for line in lines[start:]:
        if line and not line.startswith(" "):
            break
        body.append(line)
    return body


def _list_mapping(lines: list[str], section: str) -> dict[str, tuple[str, ...]]:
    result: dict[str, tuple[str, ...]] = {}
    for line in _section_lines(lines, section):
        if not line.startswith("  ") or line.startswith("    "):
            continue
        key, separator, raw = line.strip().partition(":")
        raw = raw.strip()
        if separator == "" or not raw.startswith("[") or not raw.endswith("]"):
            raise ServoV5Error("V5_SCHEMA_DECLARATION_INVALID", f"{section}:{line}")
        values = tuple(item.strip() for item in raw[1:-1].split(",") if item.strip())
        if not key:
            raise ServoV5Error("V5_SCHEMA_DECLARATION_INVALID", f"{section}:{line}")
        result[key] = values
    if not result:
        raise ServoV5Error("V5_SCHEMA_DECLARATION_MISSING", section)
    return result


def _scalar_mapping(lines: list[str], section: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in _section_lines(lines, section):
        if not line.startswith("  ") or line.startswith("    "):
            continue
        key, separator, raw = line.strip().partition(":")
        if separator == "" or not key:
            raise ServoV5Error("V5_SCHEMA_DECLARATION_INVALID", f"{section}:{line}")
        result[key] = raw.strip()
    if not result:
        raise ServoV5Error("V5_SCHEMA_DECLARATION_MISSING", section)
    return result


def validate_file(path: Path, family: str) -> list[ValidationError]:
    analysis_dir = path.parents[1]
    case_id = path.stem
    try:
        contract = load_contract(analysis_dir)
    except ServoV5Error as error:
        return [ValidationError(error.code, family, case_id, "", str(error))]
    try:
        payload = read_json(path)
    except ServoV5Error as error:
        return [ValidationError(error.code, family, case_id, "", str(error))]

    errors = _check_envelope(payload, family, case_id, contract)
    if family == "policy":
        errors.extend(_check_policy_record(payload, case_id, contract))
    else:
        errors.extend(_check_record_list(payload, family, case_id, contract))
    if family == "source_proposition":
        try:
            errors.extend(_check_sha256_gate(payload, case_id, analysis_dir))
        except ServoV5Error as error:
            errors.append(ValidationError(error.code, family, case_id, "", str(error)))
    return errors


def validate_root(analysis_dir: Path) -> list[ValidationError]:
    contract = load_contract(analysis_dir)
    errors: list[ValidationError] = []
    loaded: dict[str, dict[str, dict]] = {}
    for family, dirname in contract.directories.items():
        dirpath = analysis_dir / dirname
        if not dirpath.is_dir():
            errors.append(ValidationError("V5_FAMILY_DIR_MISSING", family, "", "", str(dirpath)))
            loaded[family] = {}
            continue
        payloads: dict[str, dict] = {}
        for path in sorted(dirpath.glob("*.json")):
            errors.extend(validate_file(path, family))
            try:
                payloads[path.stem] = read_json(path)
            except ServoV5Error:
                continue
        loaded[family] = payloads
    errors.extend(_check_downward_references(loaded))
    return errors


def _check_envelope(
    payload: dict, family: str, case_id: str, contract: SchemaContract
) -> list[ValidationError]:
    errors: list[ValidationError] = []
    allowed = set(contract.envelope_fields.get(family, ()))
    required = set(contract.required_envelope_fields.get(family, ()))
    for field in payload:
        if field not in allowed:
            errors.append(ValidationError("V5_ENVELOPE_FIELD_UNKNOWN", family, case_id, "", field))
    for field in required:
        if field not in payload:
            errors.append(ValidationError("V5_ENVELOPE_FIELD_MISSING", family, case_id, "", field))
    envelope_case_id = payload.get("case_id")
    if envelope_case_id is not None and envelope_case_id != case_id:
        errors.append(
            ValidationError(
                "V5_CASE_ID_MISMATCH",
                family,
                case_id,
                "",
                f"filename={case_id} envelope.case_id={envelope_case_id}",
            )
        )
    return errors


def _check_record_list(
    payload: dict, family: str, case_id: str, contract: SchemaContract
) -> list[ValidationError]:
    list_field = RECORD_LIST_FIELD[family]
    records = payload.get(list_field)
    if not isinstance(records, list):
        return [ValidationError("V5_RECORD_LIST_MISSING", family, case_id, "", list_field)]

    id_field = ID_FIELD[family]
    pattern = id_pattern_for(case_id, ID_LETTER[family])
    allowed = set(contract.record_fields.get(family, ()))
    required = set(contract.required_record_fields.get(family, ()))
    forbidden = set(contract.forbidden_record_fields.get(family, ()))
    leak_code = "V5_SOURCE_JUDGMENT_LEAK" if family == "source_proposition" else "V5_RECORD_FIELD_FORBIDDEN"

    errors: list[ValidationError] = []
    seen_ids: set[str] = set()
    for entry in records:
        if not isinstance(entry, dict):
            errors.append(ValidationError("V5_RECORD_NOT_OBJECT", family, case_id, "", repr(entry)))
            continue
        record_id = str(entry.get(id_field, ""))
        for field in entry:
            if field in forbidden:
                errors.append(ValidationError(leak_code, family, case_id, record_id, field))
            elif field not in allowed:
                errors.append(ValidationError("V5_RECORD_FIELD_UNKNOWN", family, case_id, record_id, field))
        for field in required:
            if field not in entry:
                errors.append(ValidationError("V5_RECORD_FIELD_MISSING", family, case_id, record_id, field))
        if not record_id or not pattern.match(record_id):
            errors.append(
                ValidationError("V5_ID_PATTERN_INVALID", family, case_id, record_id, f"expected {pattern.pattern}")
            )
        elif record_id in seen_ids:
            errors.append(ValidationError("V5_ID_DUPLICATE", family, case_id, record_id, "reused within file"))
        else:
            seen_ids.add(record_id)
        errors.extend(_check_record_fields(entry, family, case_id, record_id, contract))
    return errors


def _check_record_fields(
    entry: dict, family: str, case_id: str, record_id: str, contract: SchemaContract
) -> list[ValidationError]:
    if family == "source_proposition":
        errors = _check_enum(entry, "modality", family, case_id, record_id, contract)
        errors += _check_string_list(entry, "named_actors", family, case_id, record_id)
        errors += _check_string_list(entry, "named_inputs", family, case_id, record_id)
        errors += _check_string_list(entry, "named_outputs", family, case_id, record_id)
        errors += _check_nonempty_string(entry, "exact_quote", family, case_id, record_id)
        errors += _check_locator(entry.get("locator"), family, case_id, record_id, contract)
        return errors
    if family == "author_alignment":
        errors = _check_enum(entry, "component", family, case_id, record_id, contract)
        errors += _check_enum(entry, "basis", family, case_id, record_id, contract)
        errors += _check_enum(entry, "boundary_status", family, case_id, record_id, contract)
        errors += _check_enum(entry, "relation_asserted", family, case_id, record_id, contract)
        errors += _check_string_list(entry, "proposition_ids", family, case_id, record_id, allow_empty=False)
        errors += _check_nonempty_string(entry, "source_term", family, case_id, record_id)
        return errors
    if family == "derived_claim":
        errors = _check_enum(entry, "support_status", family, case_id, record_id, contract)
        errors += _check_enum(entry, "claim_scope", family, case_id, record_id, contract)
        errors += _check_enum(entry, "alignment_kind", family, case_id, record_id, contract)
        errors += _check_enum(entry, "occurrence_resolution", family, case_id, record_id, contract)
        errors += _check_string_list(entry, "used_alignment_ids", family, case_id, record_id, allow_empty=True)
        errors += _check_string_list(entry, "used_proposition_ids", family, case_id, record_id, allow_empty=False)
        errors += _check_nonempty_string(entry, "rationale", family, case_id, record_id)
        return errors
    return []


def _check_policy_record(
    payload: dict, case_id: str, contract: SchemaContract
) -> list[ValidationError]:
    errors = _check_enum_list(payload, "mechanism_labels", "policy", case_id, "", contract)
    errors += _check_enum_list(payload, "purpose_facets", "policy", case_id, "", contract)
    labels = payload.get("mechanism_labels")
    if isinstance(labels, list) and "explicit_bed" in labels:
        evidence = payload.get("explicit_bed_evidence")
        if not isinstance(evidence, str) or not evidence.strip():
            errors.append(
                ValidationError(
                    "V5_POLICY_EXPLICIT_BED_EVIDENCE_MISSING",
                    "policy",
                    case_id,
                    "",
                    "explicit_bed requires non-empty explicit_bed_evidence (charter B.4)",
                )
            )
    return errors


def _check_enum(
    entry: dict, field: str, family: str, case_id: str, record_id: str, contract: SchemaContract
) -> list[ValidationError]:
    if field not in entry:
        return []
    allowed = contract.enum_fields.get(f"{family}.{field}")
    if allowed is None:
        return []
    value = entry[field]
    if value not in allowed:
        return [ValidationError("V5_ENUM_INVALID", family, case_id, record_id, f"{field}={value!r} allowed={allowed}")]
    return []


def _check_enum_list(
    entry: dict, field: str, family: str, case_id: str, record_id: str, contract: SchemaContract
) -> list[ValidationError]:
    if field not in entry:
        return []
    value = entry[field]
    if not isinstance(value, list) or not value or not all(isinstance(item, str) for item in value):
        return [ValidationError("V5_FIELD_TYPE_INVALID", family, case_id, record_id, f"{field} must be a non-empty list of strings")]
    allowed = contract.enum_fields.get(f"{family}.{field}")
    if allowed is None:
        return []
    return [
        ValidationError("V5_ENUM_INVALID", family, case_id, record_id, f"{field} item={item!r} allowed={allowed}")
        for item in value
        if item not in allowed
    ]


def _check_string_list(
    entry: dict, field: str, family: str, case_id: str, record_id: str, allow_empty: bool = True
) -> list[ValidationError]:
    if field not in entry:
        return []
    value = entry[field]
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        return [ValidationError("V5_FIELD_TYPE_INVALID", family, case_id, record_id, f"{field} must be a list of strings")]
    if not allow_empty and not value:
        return [ValidationError("V5_FIELD_EMPTY", family, case_id, record_id, field)]
    return []


def _check_nonempty_string(
    entry: dict, field: str, family: str, case_id: str, record_id: str
) -> list[ValidationError]:
    if field not in entry:
        return []
    value = entry[field]
    if not isinstance(value, str) or not value.strip():
        return [ValidationError("V5_FIELD_TYPE_INVALID", family, case_id, record_id, f"{field} must be a non-empty string")]
    return []


def _check_locator(
    locator: object, family: str, case_id: str, record_id: str, contract: SchemaContract
) -> list[ValidationError]:
    if locator is None:
        return [ValidationError("V5_RECORD_FIELD_MISSING", family, case_id, record_id, "locator")]
    if not isinstance(locator, dict):
        return [ValidationError("V5_FIELD_TYPE_INVALID", family, case_id, record_id, "locator must be an object")]
    allowed = set(contract.locator_required) | set(contract.locator_optional)
    errors: list[ValidationError] = []
    for key in locator:
        if key not in allowed:
            errors.append(ValidationError("V5_LOCATOR_FIELD_UNKNOWN", family, case_id, record_id, key))
    for key in contract.locator_required:
        if key not in locator:
            errors.append(ValidationError("V5_LOCATOR_FIELD_MISSING", family, case_id, record_id, key))
    if "pdf_page" in locator and not isinstance(locator["pdf_page"], int):
        errors.append(ValidationError("V5_FIELD_TYPE_INVALID", family, case_id, record_id, "locator.pdf_page must be an integer"))
    return errors


def _check_sha256_gate(payload: dict, case_id: str, analysis_dir: Path) -> list[ValidationError]:
    registry = _case_sha_registry(analysis_dir)
    expected = registry.get(case_id)
    if expected is None:
        return []
    actual = payload.get("source_pdf_sha256")
    if actual != expected:
        return [
            ValidationError(
                "V5_SOURCE_PDF_SHA_MISMATCH",
                "source_proposition",
                case_id,
                "",
                f"expected={expected} actual={actual}",
            )
        ]
    return []


def _case_sha_registry(analysis_dir: Path) -> dict[str, str]:
    path = analysis_dir / CASE_REGISTRY_FILE_NAME
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            return {row["case_id"]: row["source_pdf_sha256"] for row in reader}
    except FileNotFoundError as error:
        raise ServoV5Error("V5_CASE_REGISTRY_MISSING", str(path)) from error


def _check_downward_references(loaded: dict[str, dict[str, dict]]) -> list[ValidationError]:
    proposition_ids_by_case = {
        case_id: {
            item.get("proposition_id")
            for item in payload.get("propositions", [])
            if isinstance(item, dict)
        }
        for case_id, payload in loaded.get("source_proposition", {}).items()
    }
    alignment_ids_by_case = {
        case_id: {
            item.get("alignment_id")
            for item in payload.get("alignments", [])
            if isinstance(item, dict)
        }
        for case_id, payload in loaded.get("author_alignment", {}).items()
    }

    errors: list[ValidationError] = []
    for case_id, payload in loaded.get("author_alignment", {}).items():
        allowed_props = proposition_ids_by_case.get(case_id, set())
        for entry in payload.get("alignments", []):
            if not isinstance(entry, dict):
                continue
            record_id = str(entry.get("alignment_id", ""))
            proposition_ids = entry.get("proposition_ids")
            if not isinstance(proposition_ids, list):
                continue
            for prop_id in proposition_ids:
                if prop_id not in allowed_props:
                    errors.append(
                        ValidationError("V5_REFERENCE_UNKNOWN", "author_alignment", case_id, record_id, f"proposition_ids -> {prop_id}")
                    )

    for case_id, payload in loaded.get("derived_claim", {}).items():
        allowed_props = proposition_ids_by_case.get(case_id, set())
        allowed_aligns = alignment_ids_by_case.get(case_id, set())
        for entry in payload.get("claims", []):
            if not isinstance(entry, dict):
                continue
            record_id = str(entry.get("claim_id", ""))
            used_alignment_ids = entry.get("used_alignment_ids")
            if isinstance(used_alignment_ids, list):
                for align_id in used_alignment_ids:
                    if align_id not in allowed_aligns:
                        errors.append(
                            ValidationError("V5_REFERENCE_UNKNOWN", "derived_claim", case_id, record_id, f"used_alignment_ids -> {align_id}")
                        )
            used_proposition_ids = entry.get("used_proposition_ids")
            if isinstance(used_proposition_ids, list):
                for prop_id in used_proposition_ids:
                    if prop_id not in allowed_props:
                        errors.append(
                            ValidationError("V5_REFERENCE_UNKNOWN", "derived_claim", case_id, record_id, f"used_proposition_ids -> {prop_id}")
                        )
    return errors
