from __future__ import annotations

import json
from pathlib import Path
import re
import tomllib
from typing import cast


ROOT = Path(__file__).resolve().parents[3]


def _cff_fields(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if raw_line.startswith(("version:", "url:")):
            key, value = raw_line.split(":", 1)
            fields[key] = value.strip().strip("\"'")
    return fields


def test_external_publication_pointer_matches_current_release() -> None:
    external = cast(
        dict[str, object],
        json.loads(
            (ROOT / "release" / "EXTERNAL_PUBLICATION.json").read_text(encoding="utf-8")
        ),
    )
    attestation = cast(
        dict[str, object],
        json.loads(
            (ROOT / "release" / "package" / "release_attestation.json").read_text(
                encoding="utf-8"
            )
        ),
    )
    project = cast(
        dict[str, object],
        tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8")),
    )
    citation = _cff_fields(ROOT / "release" / "CITATION.cff")

    project_table = cast(dict[str, object], project["project"])
    version = project_table["version"]
    assert isinstance(version, str)
    expected_tag = f"servo-corrected-v{version}"
    assets = cast(dict[str, str], external["assets"])
    pdf_filename = attestation["pdf_filename"]
    pdf_sha256 = attestation["pdf_sha256"]
    assert isinstance(pdf_filename, str)
    assert isinstance(pdf_sha256, str)

    assert external["record_role"] == "current_external_publication"
    assert external["package_version"] == version == citation["version"]
    assert external["tag"] == expected_tag
    assert external["github_release"] == citation["url"]
    assert external["github_release"] == attestation["github_release"]
    assert external["schema_version"] == attestation["schema_version"]
    assert assets[pdf_filename] == pdf_sha256


def test_experimental_adaptation_has_one_evidence_occurrence_contract() -> None:
    # Given: the reader-facing normative predicate table.
    contract = (ROOT / "analysis" / "predicate_contract.md").read_text(encoding="utf-8")
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
    role = (ROOT / "release" / "release-role-manifest.json").read_text(encoding="utf-8")

    # When: their release-state claims are compared with the finalization contract.
    candidate_only_wording = "unpublished local release candidate" in readme
    state_is_attestation_governed = '"status": "attestation-governed"' in role

    # Then: static files cannot contradict the generated release attestation.
    assert not candidate_only_wording
    assert state_is_attestation_governed
    assert "schema version 4.1.0" in readme


def test_reader_facing_audit_documents_name_current_schema_three() -> None:
    # Given: the three audit documents that identify the current contract.
    paths = (
        ROOT / "analysis" / "coding_protocol.md",
        ROOT / "analysis" / "reliability_report.md",
        ROOT / "analysis" / "core_servo_disagreement_adjudication.md",
    )

    # When: their current-schema statements are inspected.
    texts = [path.read_text(encoding="utf-8") for path in paths]

    # Then: none presents Schema 2 as the current Schema 4 contract.
    assert all("current Schema 2" not in text for text in texts)
    assert all(
        "current normative contract is Servo Schema 2" not in text for text in texts
    )


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
    assert (
        "explicit epistemic update and a distinct later evidence occurrence" in statuses
    )


def test_reader_facing_manuscript_excludes_internal_revision_log() -> None:
    manuscript = (ROOT / "main_post-submit.tex").read_text(encoding="utf-8")
    assert r"\section{Post-Submission Revisions}" not in manuscript
    assert "Current-interpretation supersession index" not in manuscript
    assert not re.search(r"\bR(?:[1-9]|[1-6][0-9])\b", manuscript)
    # T11 retired the "four conservative, set-valued predicates" closure surface;
    # the reader-facing manuscript now carries the v5 typed-relation / decomposition
    # contract (Tables A/B1/B2), not the retired closure-predicate phrase.
    assert "four conservative, set-valued predicates" not in manuscript
    assert "typed functional relations" in manuscript
    assert "tab:servo-v5-relations" in manuscript


def test_manuscript_limits_observation_and_predicate_independence_claims() -> None:
    manuscript = (ROOT / "main_post-submit.tex").read_text(encoding="utf-8")
    contract = (ROOT / "analysis" / "predicate_contract.md").read_text(
        encoding="utf-8"
    )

    assert "Columns are independent predicates" not in manuscript
    assert r"\texttt{event\_class} determines actor admissibility" in manuscript
    assert "documentary availability anchor" in manuscript
    assert "does not denote causal observation generation" in manuscript
    assert "not necessarily logically independent" in contract
    assert "execution_repair` established implies `artifact_revision` established" in contract


def test_source_byte_audit_documentation_does_not_claim_locator_validation() -> None:
    readme = (ROOT / "release" / "README.md").read_text(encoding="utf-8")

    assert "expected bytes and locators" not in readme
    assert "expected source-file bytes" in readme


def test_policy_uses_source_reported_information_state_not_mandatory_belief() -> None:
    english = (ROOT / "main_post-submit.tex").read_text(encoding="utf-8")
    korean = (ROOT / "main_ko.tex").read_text(encoding="utf-8")
    schema = (ROOT / "analysis" / "servo_schema.yaml").read_text(encoding="utf-8")
    contract = (ROOT / "analysis" / "predicate_contract.md").read_text(
        encoding="utf-8"
    )

    assert r"\pi: b \times" not in english
    assert r"\pi: b \times" not in korean
    assert r"\pi: I_t \times" in english
    assert r"\pi: I_t \times" in korean
    assert "Servo does not infer an unreported belief state" in english
    assert "보고되지 않은 믿음 상태를 추론하지 않는다" in korean
    assert "belief_specialization: I_t = b_t only when" in schema
    assert "persistent storage and retrieval substrate" in contract
