from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from .servo_v5_io import (
    ID_FIELD,
    ID_LETTER,
    ID_MAX_DIGITS,
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
    conditional_discriminator_fields: dict[str, str]
    conditional_record_fields: dict[str, dict[str, tuple[str, ...]]]
    optional_conditional_record_fields: dict[str, dict[str, tuple[str, ...]]]
    nested_record_fields: dict[str, dict[str, tuple[str, ...]]]


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
        conditional_discriminator_fields=_scalar_mapping(lines, "conditional_discriminator_fields"),
        conditional_record_fields=_nested_list_mapping(lines, "conditional_record_fields"),
        optional_conditional_record_fields=_nested_list_mapping(lines, "optional_conditional_record_fields"),
        nested_record_fields=_nested_list_mapping(lines, "nested_record_fields"),
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


def _nested_list_mapping(lines: list[str], section: str) -> dict[str, dict[str, tuple[str, ...]]]:
    # Two-level grammar (charter B.7 conditional-fields mechanism):
    #   section:
    #     family:
    #       kind: [field, field]
    #       kind: [field]
    # A 2-space-indented, colon-terminated line opens a family block; the
    # 4-space-indented "kind: [...]" lines under it become that family's
    # kind -> field-list mapping.
    result: dict[str, dict[str, tuple[str, ...]]] = {}
    current_family: str | None = None
    for line in _section_lines(lines, section):
        if not line.strip():
            continue
        if line.startswith("    "):
            if current_family is None:
                raise ServoV5Error("V5_SCHEMA_DECLARATION_INVALID", f"{section}:{line}")
            key, separator, raw = line.strip().partition(":")
            raw = raw.strip()
            if separator == "" or not key or not raw.startswith("[") or not raw.endswith("]"):
                raise ServoV5Error("V5_SCHEMA_DECLARATION_INVALID", f"{section}:{line}")
            values = tuple(item.strip() for item in raw[1:-1].split(",") if item.strip())
            result[current_family][key] = values
        elif line.startswith("  "):
            key, separator, raw = line.strip().partition(":")
            if separator == "" or not key or raw.strip():
                raise ServoV5Error("V5_SCHEMA_DECLARATION_INVALID", f"{section}:{line}")
            current_family = key
            result[current_family] = {}
        else:
            raise ServoV5Error("V5_SCHEMA_DECLARATION_INVALID", f"{section}:{line}")
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
    pattern = id_pattern_for(case_id, ID_LETTER[family], ID_MAX_DIGITS[family])
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
        errors = _check_enum(entry, "assertion_kind", family, case_id, record_id, contract)
        errors += _check_enum(entry, "basis", family, case_id, record_id, contract)
        errors += _check_enum(entry, "boundary_status", family, case_id, record_id, contract)
        errors += _check_string_list(entry, "proposition_ids", family, case_id, record_id, allow_empty=False)
        errors += _check_alignment_kind_fields(entry, family, case_id, record_id, contract)
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


def _check_alignment_kind_fields(
    entry: dict, family: str, case_id: str, record_id: str, contract: SchemaContract
) -> list[ValidationError]:
    # charter B.7: assertion_kind (named by conditional_discriminator_fields)
    # selects one group of extra fields from conditional_record_fields; the
    # other kind's fields are disallowed and the selected kind's fields are
    # mandatory. charter B.8 adds optional_conditional_record_fields: fields
    # (e.g. proposition_tags on functional_relation, polarity on
    # component_mapping) that are likewise restricted to one kind but,
    # unlike conditional_record_fields, are never mandatory on it.
    kind_groups = contract.conditional_record_fields.get(family)
    discriminator = contract.conditional_discriminator_fields.get(family)
    if not kind_groups or discriminator is None:
        return []
    optional_kind_groups = contract.optional_conditional_record_fields.get(family, {})
    kind = entry.get(discriminator)
    errors: list[ValidationError] = []
    for other_kind in set(kind_groups) | set(optional_kind_groups):
        if other_kind == kind:
            continue
        for field in kind_groups.get(other_kind, ()) + optional_kind_groups.get(other_kind, ()):
            if field in entry:
                errors.append(
                    ValidationError(
                        "V5_ALIGNMENT_KIND_FIELD_MISMATCH",
                        family,
                        case_id,
                        record_id,
                        f"{field} not allowed when {discriminator}={kind!r}",
                    )
                )
    fields_for_kind = kind_groups.get(kind)
    if fields_for_kind is not None:
        for field in fields_for_kind:
            if field not in entry:
                errors.append(
                    ValidationError(
                        "V5_ALIGNMENT_MISSING_FIELD",
                        family,
                        case_id,
                        record_id,
                        f"{field} required when {discriminator}={kind!r}",
                    )
                )
            elif field == "source_term":
                errors += _check_nonempty_string(entry, field, family, case_id, record_id)
            else:
                errors += _check_enum(entry, field, family, case_id, record_id, contract)
    for field in optional_kind_groups.get(kind, ()):
        if field not in entry:
            continue
        if field == "proposition_tags":
            errors += _check_proposition_tags(entry, family, case_id, record_id, contract)
        else:
            # charter B.8 / v5-rubric-4: other optional-conditional fields
            # (e.g. polarity on component_mapping) are plain enum-valued.
            errors += _check_enum(entry, field, family, case_id, record_id, contract)
    return errors


def _check_proposition_tags(
    entry: dict, family: str, case_id: str, record_id: str, contract: SchemaContract
) -> list[ValidationError]:
    # rubric section 3 / charter B.8: proposition_tags is a list of
    # per-proposition tag entries feeding T6 derive_claim, not a judgment
    # stored here. Each entry's proposition_id must resolve within the
    # record's own proposition_ids (cross-check), and unlisted keys are
    # rejected via nested_record_fields' allowlist.
    tags = entry.get("proposition_tags")
    if not isinstance(tags, list):
        return [
            ValidationError(
                "V5_FIELD_TYPE_INVALID", family, case_id, record_id, "proposition_tags must be a list"
            )
        ]
    allowed_keys = set(contract.nested_record_fields.get(family, {}).get("proposition_tags", ()))
    proposition_ids = entry.get("proposition_ids")
    known_propositions = set(proposition_ids) if isinstance(proposition_ids, list) else set()

    errors: list[ValidationError] = []
    for tag in tags:
        if not isinstance(tag, dict):
            errors.append(ValidationError("V5_RECORD_NOT_OBJECT", family, case_id, record_id, repr(tag)))
            continue
        for key in tag:
            if key not in allowed_keys:
                errors.append(ValidationError("V5_ALIGNMENT_TAG_FIELD_UNKNOWN", family, case_id, record_id, key))
        prop_id = tag.get("proposition_id")
        if not isinstance(prop_id, str) or not prop_id.strip():
            errors.append(
                ValidationError(
                    "V5_FIELD_TYPE_INVALID",
                    family,
                    case_id,
                    record_id,
                    "proposition_tags[].proposition_id must be a non-empty string",
                )
            )
        elif prop_id not in known_propositions:
            errors.append(
                ValidationError("V5_ALIGNMENT_TAG_UNKNOWN_PROPOSITION", family, case_id, record_id, prop_id)
            )
        if "structurally_inferred" in tag and not isinstance(tag["structurally_inferred"], bool):
            errors.append(
                ValidationError(
                    "V5_FIELD_TYPE_INVALID",
                    family,
                    case_id,
                    record_id,
                    "proposition_tags.structurally_inferred must be a bool",
                )
            )
        for enum_field in ("occurrence_class", "polarity"):
            if enum_field not in tag:
                continue
            allowed = contract.enum_fields.get(f"{family}.proposition_tags.{enum_field}")
            if allowed is not None and tag[enum_field] not in allowed:
                errors.append(
                    ValidationError(
                        "V5_ENUM_INVALID",
                        family,
                        case_id,
                        record_id,
                        f"{enum_field}={tag[enum_field]!r} allowed={allowed}",
                    )
                )
    return errors


# The eight BED-lens policy axes (charter B.4 / contract section B). Used both
# as the enum-list axis set validated above and as the key allowlist for the
# optional axis_provenance map (reviewer Item 4/B2).
POLICY_AXES = (
    "control_dependence",
    "selection_signal",
    "selection_objective",
    "generation_scope",
    "candidate_selection_rule",
    "design_selection_rule",
    "candidate_execution_rule",
    "formal_epistemic_utility_evidence",
)


def _check_axis_provenance(
    payload: dict, case_id: str, contract: SchemaContract
) -> list[ValidationError]:
    # reviewer Item 4/B2: axis_provenance is an OPTIONAL per-axis provenance map
    # that attaches, to each of the eight policy axes, the source-proposition ids
    # that GROUND that axis value (faithful to the rationale). This checks shape
    # only -- a dict keyed by the eight axes, each value a list of strings that
    # match the case's proposition-id pattern (C0N-Pnn). Whether each id resolves
    # to a real proposition in servo_v5_source_propositions/C0N.json is a
    # cross-family check performed in _check_downward_references (validate_root),
    # mirroring how author_alignment/derived_claim proposition_ids are resolved.
    if "axis_provenance" not in payload:
        return []
    provenance = payload["axis_provenance"]
    if not isinstance(provenance, dict):
        return [
            ValidationError(
                "V5_POLICY_AXIS_PROVENANCE_NOT_OBJECT", "policy", case_id, "", "axis_provenance must be an object"
            )
        ]
    pattern = id_pattern_for(case_id, ID_LETTER["source_proposition"], ID_MAX_DIGITS["source_proposition"])
    errors: list[ValidationError] = []
    for axis, ids in provenance.items():
        if axis not in POLICY_AXES:
            errors.append(
                ValidationError("V5_POLICY_AXIS_PROVENANCE_AXIS_UNKNOWN", "policy", case_id, "", axis)
            )
            continue
        if not isinstance(ids, list) or not all(isinstance(item, str) for item in ids):
            errors.append(
                ValidationError(
                    "V5_POLICY_AXIS_PROVENANCE_TYPE_INVALID",
                    "policy",
                    case_id,
                    "",
                    f"{axis} must be a list of strings",
                )
            )
            continue
        for prop_id in ids:
            if not pattern.match(prop_id):
                errors.append(
                    ValidationError(
                        "V5_POLICY_AXIS_PROVENANCE_ID_INVALID",
                        "policy",
                        case_id,
                        "",
                        f"{axis} -> {prop_id} (expected {pattern.pattern})",
                    )
                )
    return errors


def _check_policy_record(
    payload: dict, case_id: str, contract: SchemaContract
) -> list[ValidationError]:
    # charter B.4 (schema-v3 re-derivation, contract section B, 2026-07-23): the
    # policy record is an eight-axis BED-lens decomposition of the case's
    # experiment-selection policy, not an explicit_bed compliance score. Six
    # axes are enum-valued non-empty lists -- control_dependence,
    # selection_objective, generation_scope, candidate_selection_rule,
    # design_selection_rule and candidate_execution_rule. The action is
    # a=(h,d,P,f): candidate_selection_rule (which candidate hypotheses h are
    # chosen), design_selection_rule (how the experimental design/assay d is
    # chosen -- the BED-central axis added for reviewer Item 2) and
    # candidate_execution_rule (how the chosen candidates are run) are kept as
    # separate axes on purpose, with no objective in any of them. The
    # selection_objective enum (declared in servo_v5_schema.yaml and read here via
    # load_contract) admits the literal not_reported when the bounded source
    # establishes no uncertainty- or discrimination-DIRECTED objective -- exhaustive
    # testing of all candidates is no experiment SELECTION, so no directed objective
    # is licensed (e.g. C05). selection_signal
    # is a non-empty free-string list (concrete signal names);
    # formal_epistemic_utility_evidence is a non-empty string (an evidence citation
    # or the literal "not_reported"). The retired
    # V5_POLICY_EXPLICIT_BED_EVIDENCE_MISSING conditional rule is gone with the
    # compliance model.
    errors = _check_enum_list(payload, "control_dependence", "policy", case_id, "", contract)
    errors += _check_string_list(payload, "selection_signal", "policy", case_id, "", allow_empty=False)
    errors += _check_enum_list(payload, "selection_objective", "policy", case_id, "", contract)
    errors += _check_enum_list(payload, "generation_scope", "policy", case_id, "", contract)
    errors += _check_enum_list(payload, "candidate_selection_rule", "policy", case_id, "", contract)
    errors += _check_enum_list(payload, "design_selection_rule", "policy", case_id, "", contract)
    errors += _check_enum_list(payload, "candidate_execution_rule", "policy", case_id, "", contract)
    errors += _check_nonempty_string(payload, "formal_epistemic_utility_evidence", "policy", case_id, "")
    errors += _check_axis_provenance(payload, case_id, contract)
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

    # reviewer Item 4/B2: resolve every axis_provenance proposition id against the
    # case's source_propositions, the same cross-family gate applied above to
    # author_alignment.proposition_ids and derived_claim.used_proposition_ids.
    for case_id, payload in loaded.get("policy", {}).items():
        allowed_props = proposition_ids_by_case.get(case_id, set())
        provenance = payload.get("axis_provenance")
        if not isinstance(provenance, dict):
            continue
        for axis, ids in provenance.items():
            if not isinstance(ids, list):
                continue
            for prop_id in ids:
                if prop_id not in allowed_props:
                    errors.append(
                        ValidationError("V5_REFERENCE_UNKNOWN", "policy", case_id, "", f"axis_provenance[{axis}] -> {prop_id}")
                    )
    return errors
