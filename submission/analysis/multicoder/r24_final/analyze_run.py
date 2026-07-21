# /// script
# requires-python = ">=3.12"
# dependencies = ["pydantic>=2.12,<3", "typer>=0.21,<1"]
# ///

from __future__ import annotations

import csv
import json
import math
from collections import Counter
from pathlib import Path
from typing import Annotated, Final

import typer

from r24_final.agreement import krippendorff_alpha_masi, mean_pairwise_jaccard
from r24_final.generation_snapshot import verify_generation_snapshot
from r24_final.models import ServoCoding, derive_closure


ROOT: Final = Path(__file__).resolve().parent
FACETS: Final = (
    "target_property",
    "evidence_source",
    "evaluator_substrate",
    "decision_role",
    "feedback_path",
    "reliability_evidence_type",
    "experimental_fidelity",
)
app = typer.Typer(add_completion=False)


def _load(run_dir: Path) -> dict[str, dict[str, ServoCoding]]:
    verify_generation_snapshot(ROOT, run_dir)
    grouped: dict[str, dict[str, ServoCoding]] = {}
    for path in sorted((run_dir / "accepted").glob("*.json")):
        coding = ServoCoding.model_validate_json(path.read_text(encoding="utf-8"))
        grouped.setdefault(coding.record_id, {})[coding.vendor] = coding
    if len(grouped) != 14 or any(len(values) != 3 for values in grouped.values()):
        raise ValueError("analysis requires fourteen records with three vendors each")
    return grouped


def _sets(coding: ServoCoding, facet: str) -> frozenset[str]:
    return frozenset(
        str(value)
        for channel in coding.channels
        for value in getattr(channel, facet)
    )


def _majority(values: list[frozenset[str]]) -> list[str]:
    counts = Counter(item for value in values for item in value)
    return sorted(item for item, count in counts.items() if count >= 2)


def _manifest() -> dict[str, dict[str, str]]:
    payload = json.loads((ROOT / "manifest/source_manifest.json").read_text())
    return {item["record_id"]: item for item in payload["records"]}


def _write_matrix(
    destination: Path,
    records: list[str],
    grouped: dict[str, dict[str, ServoCoding]],
    metadata: dict[str, dict[str, str]],
) -> None:
    fields = ["record_id", "system_id", "source_name", "analysis_role", *FACETS, "closure"]
    with destination.open("x", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record_id in records:
            codings = list(grouped[record_id].values())
            row: dict[str, str] = {
                key: metadata[record_id][key]
                for key in ("record_id", "system_id", "source_name", "analysis_role")
            }
            for facet in FACETS:
                row[facet] = "|".join(_majority([_sets(coding, facet) for coding in codings]))
            closures = [
                derive_closure(frozenset(path for channel in coding.channels for path in channel.feedback_path)).value
                for coding in codings
            ]
            row["closure"] = Counter(closures).most_common(1)[0][0]
            writer.writerow(row)


def _write_channels(destination: Path, grouped: dict[str, dict[str, ServoCoding]]) -> None:
    fields = ["record_id", "vendor", "channel_id", *FACETS, "external_independence", "reliability_finding"]
    with destination.open("x", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record_id, vendors in sorted(grouped.items()):
            for vendor, coding in sorted(vendors.items()):
                for channel in coding.channels:
                    row = {"record_id": record_id, "vendor": vendor, "channel_id": channel.channel_id}
                    row.update({facet: "|".join(sorted(map(str, getattr(channel, facet)))) for facet in FACETS})
                    row["external_independence"] = channel.external_independence.value
                    row["reliability_finding"] = channel.reliability_finding.value
                    writer.writerow(row)


def _write_disagreements(
    destination: Path, grouped: dict[str, dict[str, ServoCoding]], metadata: dict[str, dict[str, str]]
) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    for record_id, vendors in sorted(grouped.items()):
        for facet in FACETS:
            values = {vendor: sorted(_sets(coding, facet)) for vendor, coding in sorted(vendors.items())}
            if len({tuple(value) for value in values.values()}) == 1:
                continue
            flattened = {item for value in values.values() for item in value}
            classification = "source_absence" if "not_reported" in flattened else (
                "source_ambiguity" if "unclear" in flattened else "rubric_or_system_boundary_ambiguity"
            )
            items.append({
                "record_id": record_id,
                "analysis_role": metadata[record_id]["analysis_role"],
                "facet": facet,
                "values": values,
                "provisional_classification": classification,
                "adjudication_status": "not_adjudicated",
            })
    destination.write_text(json.dumps(items, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return items


def _write_agreement(
    destination: Path, grouped: dict[str, dict[str, ServoCoding]], disagreements: list[dict[str, object]]
) -> None:
    lines = [
        "# Descriptive agreement audit",
        "",
        "The source record is the analytical unit (n=14). These coefficients describe coding behavior; they are not inferential tests, pass thresholds, or evidence that Servo is superior to another framework.",
        "",
        "| Facet | Mean pairwise Jaccard | Krippendorff alpha (MASI) |",
        "|---|---:|---:|",
    ]
    for facet in FACETS:
        units = [
            [_sets(coding, facet) for coding in vendors.values()]
            for vendors in grouped.values()
        ]
        pairwise = [mean_pairwise_jaccard(unit) for unit in units]
        finite = [value for value in pairwise if not math.isnan(value)]
        mean_value = sum(finite) / len(finite) if finite else math.nan
        alpha = krippendorff_alpha_masi(units)
        lines.append(f"| `{facet}` | {mean_value:.3f} | {alpha:.3f} |")
    lines.extend(("", f"Disagreement entries retained without editorial adjudication: {len(disagreements)}.", ""))
    destination.write_text("\n".join(lines), encoding="utf-8")


@app.command()
def main(
    run_dir: Annotated[Path, typer.Option("--run-dir")],
    output_dir: Annotated[Path, typer.Option("--output-dir")],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=False)
    grouped = _load(run_dir)
    metadata = _manifest()
    core = [record for record, item in metadata.items() if item["analysis_role"] == "core"]
    supplementary = [record for record, item in metadata.items() if item["analysis_role"] == "supplementary"]
    _write_matrix(output_dir / "core_case_matrix.csv", core, grouped, metadata)
    _write_matrix(output_dir / "supplementary_scope_audit.csv", supplementary, grouped, metadata)
    _write_channels(output_dir / "validator_channels.csv", grouped)
    disagreements = _write_disagreements(output_dir / "disagreement_log.json", grouped, metadata)
    _write_agreement(output_dir / "agreement_report.md", grouped, disagreements)
    consensus = {
        record: {facet: _majority([_sets(coding, facet) for coding in vendors.values()]) for facet in FACETS}
        for record, vendors in sorted(grouped.items())
    }
    (output_dir / "consensus.json").write_text(
        json.dumps(consensus, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    typer.echo(f"analysis artifacts written: {output_dir}")


if __name__ == "__main__":
    app()
