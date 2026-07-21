from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def test_experimental_adaptation_has_one_evidence_occurrence_contract() -> None:
    # Given: the reader-facing normative predicate table.
    contract = (ROOT / "analysis" / "predicate_contract.md").read_text(
        encoding="utf-8"
    )
    adaptation_row = next(
        line
        for line in contract.splitlines()
        if line.startswith("| `experimental_adaptation`")
    )

    # When: its minimum recurrence semantics are inspected.
    requires_second_evidence = "resulting evidence" in adaptation_row
    requires_return_to_validator = "returns to `V`" in adaptation_row

    # Then: adaptation ends at later execution; only discovery requires new evidence.
    assert not requires_second_evidence
    assert not requires_return_to_validator


def test_public_release_documentation_defers_state_to_attestation() -> None:
    # Given: the documentation and role manifest copied into every public package.
    readme = (ROOT / "release" / "README.md").read_text(encoding="utf-8")
    role = (ROOT / "release" / "release-role-manifest.json").read_text(
        encoding="utf-8"
    )

    # When: their release-state claims are compared with the finalization contract.
    candidate_only_wording = "unpublished local release candidate" in readme
    state_is_attestation_governed = '"status": "attestation-governed"' in role

    # Then: static files cannot contradict the generated release attestation.
    assert not candidate_only_wording
    assert state_is_attestation_governed
    assert "Schema 3" in readme


def test_reader_facing_audit_documents_name_current_schema_three() -> None:
    # Given: the three audit documents that identify the current contract.
    paths = (
        ROOT / "analysis" / "coding_protocol.md",
        ROOT / "analysis" / "reliability_report.md",
        ROOT / "analysis" / "core_servo_disagreement_adjudication.md",
    )

    # When: their current-schema statements are inspected.
    texts = [path.read_text(encoding="utf-8") for path in paths]

    # Then: none presents Schema 2 as the current Schema 3 contract.
    assert all("current Schema 2" not in text for text in texts)
    assert all("current normative contract is Servo Schema 2" not in text for text in texts)
