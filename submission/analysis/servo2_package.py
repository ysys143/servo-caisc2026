from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from .servo2_build import _derived_content
from .servo2_evidence import sanitize_ledger
from .servo2_io import TABLES, Table, read_tables, sha256


MODULES = (
    "servo2_audit.py",
    "servo2_build.py",
    "servo2_closure.py",
    "servo2_curate.py",
    "servo2_conformance.py",
    "servo2_evidence.py",
    "servo2_finalize.py",
    "servo2_graph.py",
    "servo2_io.py",
    "servo2_package.py",
    "servo2_predicates.py",
    "servo2_relations.py",
    "servo2_release.py",
    "servo2_schema.py",
    "servo2_validate.py",
    "validate_servo2.py",
)
DOCS = (
    "CITATION.cff",
    "LICENSE",
    "LICENSE-CODE",
    "PROTECTED_ARTIFACTS.md",
    "README.md",
    "THIRD_PARTY_NOTICES.md",
    "release-role-manifest.json",
)
SERVO_TABLE_FILES = (
    "tbl-servo2-cases.tex",
    "tbl-servo2-cases-ko.tex",
    "tbl-servo2-closure.tex",
    "tbl-servo2-closure-ko.tex",
    "tbl-servo2-anchors.tex",
    "tbl-servo2-anchors-ko.tex",
    "servo2_generated_manifest.json",
)
ANALYSIS_DOCS = (
    "adversarial_validation.md",
    "current_claim_registry.json",
    "holdout_protocol.md",
    "predicate_contract.md",
    "provenance_crosswalk.md",
)
PUBLIC_LOCATORS = {
    "boiko2023emergent": "https://doi.org/10.1038/s41586-023-06792-0",
    "lu2024aiscientist": "https://arxiv.org/abs/2408.06292",
    "lu2026aiscientist": "https://doi.org/10.1038/s41586-026-10265-5",
    "schmidgall2025agentlab": "https://arxiv.org/abs/2501.04227",
    "sparkes2010robot": "https://doi.org/10.1186/1759-4499-2-1",
    "zhang2025novelseek": "https://arxiv.org/abs/2505.16938",
    "romera2023funsearch": "https://doi.org/10.1038/s41586-023-06924-6",
    "udrescu2020afeynman": "https://doi.org/10.1126/sciadv.aay2631",
    "bran2023chemcrow": "https://arxiv.org/abs/2304.05376",
    "merchant2023gnome": "https://doi.org/10.1038/s41586-023-06735-9",
    "odonoghue2023bioplanner": "https://arxiv.org/abs/2310.10632",
    "manning2024automated": "https://arxiv.org/abs/2404.11794",
    "real2020automlzero": "https://proceedings.mlr.press/v119/real20a.html",
}


def build(repository: Path, package: Path) -> None:
    if package.exists():
        shutil.rmtree(package)
    analysis = package / "analysis"
    analysis.mkdir(parents=True)
    (analysis / "__init__.py").write_bytes(b"")
    shutil.copy2(repository / "pyproject.toml", package / "pyproject.toml")
    shutil.copy2(repository / "uv.lock", package / "uv.lock")
    for name in DOCS:
        shutil.copy2(repository / "release" / name, package / name)
    shutil.copy2(
        repository / "analysis" / "servo_schema.yaml", analysis / "servo_schema.yaml"
    )
    for name in MODULES:
        shutil.copy2(repository / "analysis" / name, analysis / name)
    for stem in TABLES:
        name = f"servo2_{stem}.csv"
        shutil.copy2(repository / "analysis" / name, analysis / name)
    for name in ANALYSIS_DOCS:
        shutil.copy2(repository / "analysis" / name, analysis / name)
    shutil.copy2(
        repository / "analysis" / "build_servo2_tables.py",
        analysis / "build_servo2_tables.py",
    )
    for name in SERVO_TABLE_FILES:
        shutil.copy2(repository / "analysis" / name, analysis / name)
    tables = read_tables(package)
    registry = _source_registry(tables)
    registry_path = analysis / "source_registry.json"
    registry_path.write_bytes(registry)
    evidence_path = analysis / "servo2_evidence_ledger.json"
    evidence_path.write_bytes(
        sanitize_ledger(repository / "analysis" / "core_servo_evidence_ledger.json")
    )
    generated = _derived_content(tables)
    generated_hashes: dict[str, str] = {}
    for name, content in sorted(generated.items()):
        path = analysis / name
        path.write_bytes(content)
        generated_hashes[f"analysis/{name}"] = hashlib.sha256(content).hexdigest()
    for name in SERVO_TABLE_FILES:
        generated_hashes[f"analysis/{name}"] = sha256(analysis / name)
    canonical_names = [
        "analysis/servo_schema.yaml",
        "analysis/source_registry.json",
        "analysis/servo2_evidence_ledger.json",
        "analysis/build_servo2_tables.py",
    ]
    canonical_names.extend(f"analysis/{name}" for name in ANALYSIS_DOCS)
    canonical_names.extend(f"analysis/servo2_{stem}.csv" for stem in TABLES)
    canonical = {name: sha256(package / name) for name in sorted(canonical_names)}
    manifest = {
        "schema_version": "3.0.0",
        "canonical_input_sha256": canonical,
        "generated_artifact_sha256": generated_hashes,
    }
    public_hashes = {
        path.relative_to(package).as_posix(): sha256(path)
        for path in sorted(package.rglob("*"))
        if path.is_file()
    }
    manifest["public_file_sha256"] = public_hashes
    (package / "servo2_public_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _source_registry(tables: dict[str, Table]) -> bytes:
    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for table_name in ("cases", "domain_anchors"):
        table = tables[table_name]
        for row in table.rows:
            identifier = row.get("case_id", row.get("anchor_id", ""))
            digest = row["source_pdf_sha256"]
            key = (identifier, digest)
            if key in seen:
                continue
            seen.add(key)
            citation = row["citation_key"]
            rows.append(
                {
                    "record_id": identifier,
                    "citation_key": citation,
                    "pdf_sha256": digest,
                    "filename_hint": f"{citation}.pdf",
                    "public_locator": PUBLIC_LOCATORS[citation],
                }
            )
    payload = {
        "schema_version": "3.0.0",
        "sources": sorted(rows, key=lambda row: row["record_id"]),
    }
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()


if __name__ == "__main__":
    build(
        Path(__file__).resolve().parents[1],
        Path(__file__).resolve().parents[1] / "release" / "package",
    )
