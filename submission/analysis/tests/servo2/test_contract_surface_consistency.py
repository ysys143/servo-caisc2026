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


def test_public_normative_paths_and_event_semantics_are_current() -> None:
    # Given: the schema and release metadata copied into the public package.
    schema = (ROOT / "analysis" / "servo_schema.yaml").read_text(encoding="utf-8")
    project = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    protected = (ROOT / "release" / "PROTECTED_ARTIFACTS.md").read_text(
        encoding="utf-8"
    )

    # When: current event, evidence-ledger, package, and PDF roles are inspected.
    stale_event_claim = "An event records an evaluation occurrence" in schema
    stale_ledger_path = "analysis/core_servo_evidence_ledger.json" in schema
    stale_package_name = "servo-schema2-reproducibility" in project
    post_submit_declared_immutable = "`main_post-submit.pdf`" in protected
    post_submit_schema_protected = "main_post-submit.pdf:" in schema

    # Then: no public surface revives superseded or false contracts.
    assert not stale_event_claim
    assert not stale_ledger_path
    assert not stale_package_name
    assert not post_submit_declared_immutable
    assert not post_submit_schema_protected


def test_c03_discovery_rationale_matches_current_graph_boundary() -> None:
    # Given: the canonical matrix rationale exposed by the public package.
    statuses = (ROOT / "analysis" / "servo2_closure_statuses.csv").read_text(
        encoding="utf-8"
    )

    # When/Then: it names the missing discovery conditions, not implemented ED15.
    assert "the executor link ED15 is unclear" not in statuses
    assert "explicit epistemic update and a distinct later evidence occurrence" in statuses
