from __future__ import annotations

from .servo2_io import Servo2Error, Table, split_values


CLOSURE_PREDICATES = {
    "execution_repair",
    "experimental_adaptation",
    "artifact_revision",
    "discovery_cycle_feedback",
}
ALLOWED_BASES = {
    "established": {"positive_witness"},
    "not_established": {"explicit_negative"},
    "unknown": {"insufficient_reporting"},
    "not_applicable": {"out_of_scope"},
}


def validate_closure_statuses(
    table: Table,
    cases: dict[str, dict[str, str]],
    witnesses: dict[str, dict[str, str]],
) -> None:
    expected = {
        (case_id, predicate)
        for case_id in cases
        for predicate in CLOSURE_PREDICATES
    }
    observed: set[tuple[str, str]] = set()
    positive_witnesses = {
        (row["case_id"], row["predicate"])
        for row in witnesses.values()
        if row["predicate_status"] == "established"
    }
    for row in table.rows:
        _validate_status_row(row, witnesses, positive_witnesses, observed)
    if observed != expected:
        missing = sorted(expected - observed)
        extras = sorted(observed - expected)
        raise Servo2Error(
            "CLOSURE_STATUS_MATRIX_INCOMPLETE",
            f"missing={missing};extras={extras}",
        )
    statuses = {
        (row["case_id"], row["predicate"]): row["status"] for row in table.rows
    }
    for case_id in cases:
        if (
            statuses[(case_id, "execution_repair")] == "established"
            and statuses[(case_id, "artifact_revision")] != "established"
        ):
            raise Servo2Error(
                "CLOSURE_STATUS_IMPLICATION_VIOLATION",
                f"{case_id}:execution_repair=>artifact_revision",
            )


def _validate_status_row(
    row: dict[str, str],
    witnesses: dict[str, dict[str, str]],
    positive_witnesses: set[tuple[str, str]],
    observed: set[tuple[str, str]],
) -> None:
    identity = f"{row['case_id']}:{row['predicate']}"
    key = (row["case_id"], row["predicate"])
    if key in observed:
        raise Servo2Error("CLOSURE_STATUS_DUPLICATE", identity)
    observed.add(key)
    if row["rationale"].strip() == "":
        raise Servo2Error("CLOSURE_STATUS_RATIONALE_MISSING", identity)
    if row["decision_basis"] not in ALLOWED_BASES[row["status"]]:
        raise Servo2Error("CLOSURE_STATUS_BASIS_MISMATCH", identity)
    if row["status"] == "not_established" and not split_values(row["evidence_ids"]):
        raise Servo2Error("NEGATIVE_STATUS_EVIDENCE_MISSING", identity)
    if row["status"] != "established" and key in positive_witnesses:
        raise Servo2Error("CLOSURE_STATUS_WITNESS_CONTRADICTION", identity)
    refs = split_values(row["witness_ids"])
    if row["status"] == "established" and not refs:
        raise Servo2Error("ESTABLISHED_CLOSURE_WITNESS_MISSING", identity)
    for witness_id in refs:
        witness = witnesses.get(witness_id)
        if witness is None:
            raise Servo2Error("CLOSURE_WITNESS_UNKNOWN", witness_id)
        if (
            witness["case_id"] != row["case_id"]
            or witness["predicate"] != row["predicate"]
            or witness["predicate_status"] != "established"
        ):
            raise Servo2Error("CLOSURE_WITNESS_STATUS_MISMATCH", witness_id)
