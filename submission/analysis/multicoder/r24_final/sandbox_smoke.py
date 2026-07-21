from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import Annotated, Final

import typer

from r24_final.lifecycle import (
    SMOKE_MANIFEST,
    REQUIRED_SMOKE_REPORTS,
    SMOKE_REPORT_DIRECTORY,
    assemble_smoke_manifest,
    smoke_binding,
    verify_smoke_report,
)
from r24_final.hook_negative import build_report
from r24_final.smoke_contract import verify_typed_evidence
from r24_final.static_checks import build_static_evidence


ROOT: Final = Path(__file__).resolve().parent
app = typer.Typer(add_completion=False)


@app.command()
def verify(report_name: str) -> None:
    verify_smoke_report(ROOT, report_name)
    typer.echo(f"{report_name}: verified")


@app.command("generate-static")
def generate_static() -> None:
    binding = smoke_binding(ROOT)
    evidence = build_static_evidence(
        ROOT, binding["protocol_sha256"]
    ).model_dump(mode="json")
    _write_report("STATIC_GATE_REPORT", evidence, binding)


@app.command("generate-hook-negative")
def generate_hook_negative() -> None:
    _write_report("HOOK_NEGATIVE_REPORT", build_report(), smoke_binding(ROOT))


@app.command("register-observer-evidence")
def register_observer_evidence(
    report_name: str,
    evidence_path: Annotated[Path, typer.Option("--evidence-path")],
) -> None:
    if report_name not in {"ISOLATION_REPORT", "FUNCTIONAL_REPORT"}:
        raise typer.BadParameter("observer evidence is only valid for isolation or functional reports")
    binding = smoke_binding(ROOT)
    try:
        verify_typed_evidence(
            report_name, evidence_path, binding["protocol_sha256"], ROOT
        )
        evidence_body = json.loads(evidence_path.read_text(encoding="utf-8"))
    except (ValueError, OSError, json.JSONDecodeError) as error:
        raise typer.BadParameter(str(error)) from error
    _write_report(report_name, evidence_body, binding)


@app.command()
def finalize(
    manifest_path: Annotated[Path | None, typer.Option()] = None,
) -> None:
    destination = manifest_path or ROOT / SMOKE_MANIFEST
    if destination.exists():
        raise typer.BadParameter(f"refusing to overwrite smoke manifest: {destination}")
    try:
        payload = assemble_smoke_manifest(ROOT)
    except ValueError as error:
        raise typer.BadParameter(str(error)) from error
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    typer.echo(f"four-report smoke manifest written: {destination}")


def _write_report(
    report_name: str, evidence_body: dict[str, object], binding: dict[str, str]
) -> None:
    directory = ROOT / SMOKE_REPORT_DIRECTORY
    raw = directory / "raw" / f"{report_name}.json"
    report_path = directory / f"{report_name}.json"
    raw.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(evidence_body, indent=2, sort_keys=True).encode()
    if raw.exists() or report_path.exists():
        raise typer.BadParameter(f"refusing to overwrite smoke evidence: {report_name}")
    raw.write_bytes(encoded + b"\n")
    evidence_id = f"{report_name.lower()}-evidence"
    report = {
        "report_type": report_name,
        "binding": binding,
        "evidence": [{
            "id": evidence_id,
            "path": str(raw.relative_to(directory)),
            "sha256": hashlib.sha256(raw.read_bytes()).hexdigest(),
        }],
        "checks": [
            {"id": check_id, "result": "pass", "evidence_ids": [evidence_id]}
            for check_id in sorted(REQUIRED_SMOKE_REPORTS[report_name])
        ],
    }
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    verify_smoke_report(ROOT, report_name)
    typer.echo(f"{report_name}: generated and verified")


if __name__ == "__main__":
    app()
