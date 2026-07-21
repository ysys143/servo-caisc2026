# /// script
# requires-python = ">=3.12"
# ///

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Final


ROOT: Final = Path(__file__).resolve().parents[2]
R24: Final = Path(__file__).resolve().parent
CORE_IDS: Final = ("R01", "R02", "R03", "R04", "R05", "R14")


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _evidence() -> dict[str, dict[str, object]]:
    indexed: dict[str, dict[str, object]] = {}
    for record_id in CORE_IDS:
        packet = json.loads((R24 / f"packets/{record_id}.json").read_text(encoding="utf-8"))
        source = packet["source"]
        for item in packet["evidence"]:
            indexed[item["evidence_id"]] = {
                "record_id": record_id,
                "pdf_sha256": source["pdf_sha256"],
                "pdf_page": item["pdf_page"],
                "quote": item["quote"],
            }
    return indexed


def _attach(rows: list[dict[str, str]], indexed: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    enriched: list[dict[str, object]] = []
    for row in rows:
        identifiers = [value for value in row["evidence_ids"].split(";") if value]
        if not identifiers or any(value not in indexed for value in identifiers):
            raise ValueError(f"unresolved evidence in {row}")
        if any(indexed[value]["record_id"] != row["record_id"] for value in identifiers):
            raise ValueError(f"cross-record evidence in {row}")
        enriched.append({**row, "evidence": [indexed[value] | {"evidence_id": value} for value in identifiers]})
    return enriched


def _tex_escape(value: str) -> str:
    return value.replace("&", r"\&").replace("_", r"\_")


def _channel_summary(rows: list[dict[str, str]], record_id: str, korean: bool) -> tuple[str, str, str]:
    selected = [row for row in rows if row["record_id"] == record_id]
    labels = {
        "protocol_execution_correction": "프로토콜 실행 교정", "reactivity_guidance": "반응성 안내",
        "subjective_labeling": "주관적 라벨링", "ideation_prior_art_filter": "아이디어 선행연구 필터",
        "experiment_result_replanner": "실험결과 재계획", "automated_paper_reviewer": "자동 논문 reviewer",
        "archive_admission": "아카이브 수용", "literature_refinement": "문헌 기반 개선",
        "stage_evaluator": "단계 평가기", "plot_critique": "플롯 비평",
        "best_first_node_evaluator": "최선우선 노드 평가기", "workshop_review": "워크숍 심사",
        "mle_execution_feedback": "MLE 실행 피드백", "phd_revision_evaluator": "PhD 수정 평가기",
        "human_research_authority": "인간 연구 권한", "physical_hypothesis_test": "물리 가설 검정",
        "knowledge_admission": "지식 수용", "idea_assessment": "아이디어 평가",
        "human_feedback": "인간 피드백", "debugging_loop": "디버깅 루프",
        "adaptive_evolution": "적응적 진화",
    }
    def label(row: dict[str, str]) -> str:
        return labels[row["channel_id"]] if korean else row["channel_id"].replace("_", " ")
    operational = [label(row) for row in selected if row["feedback_path"] != "terminal_only" and row["operational_status"] == "implemented"]
    terminal = [label(row) for row in selected if row["feedback_path"] in {"terminal_only", "external_only"}]
    evidence = sorted({item for row in selected for item in row["evidence_ids"].split(";")})
    absent = "식별되지 않음" if korean else "None identified"
    return "; ".join(operational) or absent, "; ".join(terminal) or absent, ", ".join(evidence)


def _write_tex(rows: list[dict[str, str]], destination: Path, korean: bool) -> None:
    headers = ("시스템", "운영 채널", "종결/외부 평가", "근거") if korean else ("System", "Operational channels", "Terminal/external assessment", "Evidence")
    names = {
        "R01": "Coscientist",
        "R02": "AI Scientist 2024",
        "R03": "AI Scientist 2026",
        "R04": "Agent Laboratory",
        "R05": "Robot Scientist",
        "R14": "NovelSeek",
    }
    lines = [
        r"\begin{tabular}{p{0.15\textwidth}p{0.31\textwidth}p{0.29\textwidth}p{0.17\textwidth}}",
        r"\toprule",
        " & ".join(headers) + r" \\",
        r"\midrule",
    ]
    for record_id in CORE_IDS:
        operational, terminal, evidence = _channel_summary(rows, record_id, korean)
        lines.append(" & ".join(map(_tex_escape, (names[record_id], operational, terminal, evidence))) + r" \\")
    lines.extend((r"\bottomrule", r"\end{tabular}"))
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    indexed = _evidence()
    channels = _attach(_rows(ROOT / "core_servo_channels.csv"), indexed)
    components = _attach(_rows(ROOT / "core_servo_components.csv"), indexed)
    payload = {
        "schema_version": 1,
        "unit": "source-defined system record with channel-level validators",
        "adjudication_policy": "author interpretation of bounded primary-source packet; split distinct trigger phase, evaluator, target, decision role, or destination; merge only the same reported mechanism; none identified means not found in packet; no majority vote or independent channel-level reproducibility claim",
        "channels": channels,
        "components": components,
    }
    (ROOT / "core_servo_evidence_ledger.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    _write_tex(_rows(ROOT / "core_servo_channels.csv"), ROOT / "tbl-core-channels.tex", False)
    _write_tex(_rows(ROOT / "core_servo_channels.csv"), ROOT / "tbl-core-channels-ko.tex", True)


if __name__ == "__main__":
    main()
