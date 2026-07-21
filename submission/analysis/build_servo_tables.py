#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Final

try:
    import validate_servo_consistency as validator
except ModuleNotFoundError:
    from analysis import validate_servo_consistency as validator

HERE: Final = Path(__file__).resolve().parent
OUT_EN: Final = HERE / "tbl-core.tex"
OUT_KO: Final = HERE / "tbl-core-ko.tex"
CHANNEL_EN: Final = HERE / "tbl-core-channels.tex"
CHANNEL_KO: Final = HERE / "tbl-core-channels-ko.tex"
COMPAT_CHANNELS: Final = HERE / "core_servo_channels.csv"
COMPAT_TIMING: Final = HERE / "core_servo_channel_timing.csv"
COMPAT_COMPONENTS: Final = HERE / "core_servo_components.csv"

HEADERS: Final = (
    "Robot Sci.",
    "Coscientist",
    r"AI Sci.\ (2024)",
    r"AI Sci.\ (2026)",
    "AgentLab",
    "NovelSeek",
)
DISPLAY_RECORD_ORDER: Final = ("R05", "R01", "R02", "R03", "R04", "R14")


def tex(value: str) -> str:
    return value.replace("_", r"\_").replace("&", r"\&").replace("%", r"\%")


def display(value: str) -> str:
    return tex(value.replace("_", " ").replace(";", "; ")).replace("-", r"-\allowbreak{}")


def values(value: str) -> list[str]:
    return sorted(validator.split_values(value))


def compact_system_rows(
    systems: list[dict[str, str]], channels: list[dict[str, str]], derived: list[dict[str, object]], language: str
) -> list[tuple[str, list[str]]]:
    channel_map: dict[str, list[dict[str, str]]] = defaultdict(list)
    for channel in channels:
        channel_map[channel["record_id"]].append(channel)
    closure = {row["record_id"]: row for row in derived}
    labels = {
        "en": ("Novelty channels", "Computational closure", r"$\pi$ class", r"$V$ channels", r"$\Delta S$", "Fidelity choice", "Human authority"),
        "ko": ("신규성 채널", "계산적 폐쇄", r"$\pi$ 분류", r"$V$ 채널", r"$\Delta S$", "충실도 선택", "인간 권한"),
    }[language]
    columns: list[list[str]] = [[] for _ in labels]
    system_by_id = {row["record_id"]: row for row in systems}
    for rid in DISPLAY_RECORD_ORDER:
        system = system_by_id[rid]
        current = channel_map[rid]
        novelty = [row for row in current if "novelty" in values(row["target_property"])]
        witnesses = closure[rid]["qualifying_channel_ids"]
        closed_word = "Yes" if language == "en" else "예"
        open_word = "No" if language == "en" else "아니오"
        novelty_roles = sorted({item for row in novelty for item in values(row["decision_role"])})
        columns[0].append(f"{len(novelty)} ({'/'.join(novelty_roles)})" if novelty else "0")
        columns[1].append(f"{closed_word} ({len(witnesses)} routed channels)" if witnesses else open_word)
        columns[2].append(system["policy_class"])
        operational = sum(1 for row in current if row["channel_id"] in witnesses)
        terminal = sum(1 for row in current if "terminal_only" in values(row["routed_destination"]))
        external = sum(1 for row in current if "external_only" in values(row["routed_destination"]))
        columns[3].append(f"{len(current)} ({operational} routed; {terminal} terminal-only; {external} external-only)")
        columns[4].append(system["delta_S_status"])
        columns[5].append(system["fidelity_choice_status"])
        authority = [field[2:] for field in validator.AUTHORITY_FIELDS if system[field] in {"human_controls", "human_participates", "shared"}]
        columns[6].append(", ".join(authority) if authority else "none reported")
    return list(zip(labels, columns, strict=True))


def system_table(rows: list[tuple[str, list[str]]], language: str) -> str:
    source = "% AUTO-GENERATED from validated Servo v1 canonical records; do not edit by hand."
    headings = {
        "en": ("System", "Closure / channels", "Search", "Human authority", "Fidelity"),
        "ko": ("시스템", "폐쇄 / 채널", "탐색", "인간 권한", "충실도"),
    }[language]
    caption = {
        "en": "Compact projection of the schema-validated canonical six-system records. Closure witnesses, terminal and external events, search-space change, fidelity, policy, and human authority remain separate non-ordered fields. Complete event alignment and evidence appear in Table~\\ref{tab:core-channels} and the canonical CSVs.",
        "ko": "Schema consistency를 통과한 여섯 시스템 정본의 compact 투영. Closure witness, terminal·external event, 탐색공간 변화, fidelity, policy, 인간 권한은 서로 다른 비순서형 필드다. 완전한 event 정렬과 근거는 표~\\ref{tab:core-channels}와 정본 CSV에 있다.",
    }[language]
    by_label = {label: cells for label, cells in rows}
    novelty_label, closure_label, policy_label, channels_label, delta_label, fidelity_label, authority_label = by_label
    column_spec = (
        r"@{}>{\raggedright\arraybackslash}p{1.95cm}"
        r">{\raggedright\arraybackslash}p{3.35cm}"
        r">{\raggedright\arraybackslash}p{3.35cm}"
        r">{\raggedright\arraybackslash}p{1.85cm}"
        r">{\raggedright\arraybackslash}p{2.15cm}@{}"
    )
    lines = [source, rf"\begin{{longtable}}{{{column_spec}}}", rf"\caption{{{caption}}}\label{{tab:core-comparison}} \\", r"\toprule", " & ".join(rf"\textbf{{{item}}}" for item in headings) + " \\\\", r"\midrule", r"\endfirsthead", r"\toprule", " & ".join(rf"\textbf{{{item}}}" for item in headings) + " \\\\", r"\midrule", r"\endhead"]
    for index, system in enumerate(HEADERS):
        closure = f"{by_label[closure_label][index]}; {by_label[channels_label][index]}; novelty {by_label[novelty_label][index]}"
        search = f"policy: {by_label[policy_label][index]}; delta S: {by_label[delta_label][index]}"
        cells = (system, closure, search, by_label[authority_label][index], by_label[fidelity_label][index])
        lines.append(" & ".join(display(cell) for cell in cells) + " \\\\")
    lines.extend((r"\bottomrule", r"\end{longtable}"))
    return "\n".join(lines) + "\n"


def channel_table(channels: list[dict[str, str]], language: str) -> str:
    headers = {
        "en": ("System/channel", "Phase", "Target", "Role / route", "Evidence status"),
        "ko": ("시스템/channel", "시점", "평가대상", "역할 / 경로", "근거 상태"),
    }[language]
    caption = {
        "en": "Author-interpreted source-grounded channels for the six cases. Routed, terminal-only, and external-only events remain distinct; evidence IDs resolve to the released ledger. This is not an independent channel-level reproducibility study.",
        "ko": "저자가 해석한 여섯 사례의 source-grounded channel. Routed, terminal-only, external-only event를 구분하며 근거 ID는 공개 ledger로 해소된다. 독립 channel-level 재현성 연구가 아니다.",
    }[language]
    lines = [
        "% AUTO-GENERATED from validated Servo v1 canonical records; do not edit by hand.",
        r"\begin{longtable}{@{}>{\raggedright\arraybackslash}p{2.25cm}>{\raggedright\arraybackslash}p{2.05cm}>{\raggedright\arraybackslash}p{2.45cm}>{\raggedright\arraybackslash}p{3.10cm}>{\raggedright\arraybackslash}p{2.75cm}@{}}",
        rf"\caption{{{caption}}}\label{{tab:core-channels}} \\",
        r"\toprule",
        " & ".join(rf"\textbf{{{tex(item)}}}" for item in headers) + " \\\\",
        r"\midrule",
        r"\endfirsthead",
        r"\toprule",
        " & ".join(rf"\textbf{{{tex(item)}}}" for item in headers) + " \\\\",
        r"\midrule",
        r"\endhead",
    ]
    for row in channels:
        evidence_status = f"{row['reliability_evidence_type']}; {row['reliability_finding']}"
        cells = (
            f"{row['system']}: {row['channel_id']}",
            row["trigger_phase"],
            row["target_property"],
            f"{row['decision_role']} / {row['routed_destination']}",
            evidence_status,
        )
        lines.append(" & ".join(display(cell) for cell in cells) + " \\\\")
    lines.extend((r"\bottomrule", r"\end{longtable}"))
    return "\n".join(lines) + "\n"


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_compatibility(systems: list[dict[str, str]], channels: list[dict[str, str]]) -> None:
    channel_fields = [
        "record_id", "system", "channel_id", "target_property", "evidence_source", "evaluator_substrate",
        "decision_role", "routed_destination", "operational_status", "evidential_status", "evidence_ids", "adjudication",
    ]
    write_csv(COMPAT_CHANNELS, channel_fields, channels)
    timing_rows = [{key: row[key] for key in ("record_id", "channel_id", "trigger_phase", "evidence_ids")} for row in channels]
    write_csv(COMPAT_TIMING, ["record_id", "channel_id", "trigger_phase", "evidence_ids"], timing_rows)
    component_fields = [
        "record_id", "system", "S_0", "represented_S_t", "delta_S_status", "delta_S_operator", "G", "E_exec", "M", "pi", "policy_class",
        "H_S", "H_G", "H_E", "H_V", "H_M", "H_pi", "fidelity_choice_status", "fidelity_levels", "cost_function_status",
        "budget_state_status", "evidential_status", "evidence_ids", "adjudication",
    ]
    write_csv(COMPAT_COMPONENTS, component_fields, systems)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    try:
        derived, hashes = validator.validate()
        _, systems, channels, _ = validator.load_inputs()
    except validator.ValidationError as exc:
        print(f"TABLE GENERATION BLOCKED:\n{exc}", file=sys.stderr)
        return 1
    OUT_EN.write_text(system_table(compact_system_rows(systems, channels, derived, "en"), "en"), encoding="utf-8")
    OUT_KO.write_text(system_table(compact_system_rows(systems, channels, derived, "ko"), "ko"), encoding="utf-8")
    CHANNEL_EN.write_text(channel_table(channels, "en"), encoding="utf-8")
    CHANNEL_KO.write_text(channel_table(channels, "ko"), encoding="utf-8")
    write_compatibility(systems, channels)
    validator.write_reports(derived, hashes)
    generated = (OUT_EN, OUT_KO, CHANNEL_EN, CHANNEL_KO, COMPAT_CHANNELS, COMPAT_TIMING, COMPAT_COMPONENTS)
    manifest = json.loads(validator.MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest["generated_artifact_sha256"] = {path.name: digest(path) for path in generated}
    validator.MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"SERVO TABLE BUILD PASS: {len(systems)} systems, {len(channels)} channels")
    return 0


if __name__ == "__main__":
    sys.exit(main())
