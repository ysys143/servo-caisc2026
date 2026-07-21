from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CASE_PATH = ROOT / "servo2_cases.csv"
CLOSURE_PATH = ROOT / "servo2_closure_statuses.csv"
ANCHOR_PATH = ROOT / "servo2_domain_anchors.csv"
WITNESS_PATH = ROOT / "servo2_closure_witnesses.csv"
LEDGER_PATH = ROOT / "servo2_selection_ledger.csv"
PREDICATES = (
    "execution_repair",
    "experimental_adaptation",
    "artifact_revision",
    "discovery_cycle_feedback",
    "human_mediated_feedback",
)
PREDICATE_LABELS = {
    "execution_repair": ("Execution repair", "실행 복구"),
    "experimental_adaptation": ("Experimental adaptation", "실험 적응"),
    "artifact_revision": ("Artifact revision", "산출물 수정"),
    "discovery_cycle_feedback": ("Discovery-cycle feedback", "발견 주기 피드백"),
    "human_mediated_feedback": ("Human-mediated feedback", "인간 매개 피드백"),
}
STATUS_LABELS = {
    "established": (r"\{established\}", r"\{확립\}"),
    "not_established": (r"\{not established\}", r"\{미확립\}"),
    "unknown": (r"\{unknown\}", r"\{불명\}"),
    "not_applicable": (r"\{not applicable\}", r"\{해당 없음\}"),
}


class TableBuildError(Exception):
    pass


CASE_LABELS = {
    "C01": {
        "system": ("Coscientist", "Coscientist"),
        "version": ("2023 paper", "2023년 논문"),
        "configuration": ("Reported demonstration", "보고된 시연"),
        "regime": ("Six chemistry tasks", "화학 과제 6개"),
    },
    "C02": {
        "system": ("AI Scientist 2024", "AI Scientist 2024"),
        "version": ("2024 paper", "2024년 논문"),
        "configuration": ("Reported default", "보고된 기본 설정"),
        "regime": ("At most five computational experiments", "계산 실험 최대 5회"),
    },
    "C03": {
        "system": ("AI Scientist 2026", "AI Scientist 2026"),
        "version": ("2026 Nature", "2026년 Nature"),
        "configuration": ("Template-free tree", "템플릿 없는 트리"),
        "regime": ("Computational tree search", "계산 트리 탐색"),
    },
    "C04": {
        "system": ("Agent Laboratory", "Agent Laboratory"),
        "version": ("2025 paper", "2025년 논문"),
        "configuration": ("Autonomous mode", "자율 모드"),
        "regime": ("Human-provided ML idea", "인간 제공 ML 아이디어"),
    },
    "C05": {
        "system": ("Robot Scientist", "Robot Scientist"),
        "version": ("2010 review of Adam", "2010년 Adam 리뷰"),
        "configuration": ("Adam yeast", "Adam 효모"),
        "regime": ("Yeast functional genomics", "효모 기능유전체학"),
    },
    "C06": {
        "system": ("NovelSeek/InternAgent", "NovelSeek/InternAgent"),
        "version": ("2025 InternAgent", "2025년 InternAgent"),
        "configuration": ("Reported multi-agent", "보고된 다중 에이전트"),
        "regime": ("Twelve computational tasks", "계산 과제 12개"),
    },
}
ANCHOR_LABELS = {
    "DA01": (("FunSearch", "FunSearch"), ("Formal mathematics", "형식수학"), ("Program quality and task performance", "프로그램 품질과 과제 성능"), ("Executable evaluator", "실행 가능 평가기"), ("Ranking and search control", "순위화와 탐색 제어"), ("Computational oracle", "계산 오라클")),
    "DA02": (("AI Feynman", "AI Feynman"), ("Physics", "물리학"), ("Symbolic fit to data", "데이터에 대한 기호 적합"), ("Symbolic-regression algorithm", "기호회귀 알고리즘"), ("Model search and fit", "모형 탐색과 적합"), ("Computational data fit", "계산 데이터 적합")),
    "DA03": (("ChemCrow", "ChemCrow"), ("Chemistry", "화학"), ("Task performance and synthesis", "과제 성능과 합성"), ("Tools, execution, and assessment", "도구·실행·평가"), ("Planning, execution, assessment", "계획·실행·평가"), ("Computational and physical", "계산·물리 혼합")),
    "DA04": (("GNoME", "GNoME"), ("Materials science", "재료과학"), ("Phase stability and energy", "상 안정성과 에너지"), ("Graph networks plus DFT", "그래프 신경망과 DFT"), ("Filtering and active-learning update", "필터링과 능동학습 갱신"), ("Surrogate; separate experiment", "대리모형; 실험은 별도")),
    "DA05": (("BioPlanner", "BioPlanner"), ("Biology", "생물학"), ("Protocol planning and executability", "프로토콜 계획과 실행 가능성"), ("Generator, evaluator, laboratory", "생성기·평가기·실험실"), ("Diagnosis and external execution", "진단과 외부 실행"), ("Protocol to physical laboratory", "프로토콜에서 물리 실험실로")),
    "DA06": (("Manning automated social science", "Manning 자동화 사회과학"), ("Social science", "사회과학"), ("Causal hypotheses and simulated effects", "인과 가설과 모의 효과"), ("Causal model and LLM agents", "인과모형과 LLM 에이전트"), ("Design and model update", "설계와 모형 갱신"), ("Simulated subjects", "모의 피험자")),
    "DA07": (("AutoML-Zero", "AutoML-Zero"), ("Computer science", "컴퓨터과학"), ("Evolved-algorithm benchmark performance", "진화 알고리즘의 벤치마크 성능"), ("Executable benchmark", "실행 가능 벤치마크"), ("Selection and evolutionary update", "선택과 진화 갱신"), ("Computational benchmark", "계산 벤치마크")),
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def tex(value: str) -> str:
    replacements = (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("_", r"\_"), ("#", r"\#"))
    for source, target in replacements:
        value = value.replace(source, target)
    return value


def table(columns: str, header: list[str], rows: list[list[str]]) -> str:
    body = [r"\begin{tabular}{" + columns + "}", r"\toprule", " & ".join(header) + " \\\\", r"\midrule"]
    body.extend(" & ".join(row) + r" \\" for row in rows)
    body.extend((r"\bottomrule", r"\end{tabular}", ""))
    return "\n".join(body)


def validate(cases: list[dict[str, str]], closure: list[dict[str, str]], anchors: list[dict[str, str]], witnesses: list[dict[str, str]], ledger: list[dict[str, str]]) -> None:
    case_ids = {row["case_id"] for row in cases}
    if len(cases) != 6 or case_ids != set(CASE_LABELS) or len({row["lineage_id"] for row in cases}) != 5:
        raise TableBuildError("expected exactly six cases, five lineages, and IDs C01--C06")
    pairs = {(row["case_id"], row["predicate"]) for row in closure}
    expected_pairs = {(case_id, predicate) for case_id in case_ids for predicate in PREDICATES}
    if len(closure) != 30 or pairs != expected_pairs:
        raise TableBuildError("closure matrix must contain every case-predicate pair exactly once")
    if any(row["status"] not in STATUS_LABELS for row in closure):
        raise TableBuildError("unknown closure status")
    if len(anchors) != 7 or {row["anchor_id"] for row in anchors} != set(ANCHOR_LABELS):
        raise TableBuildError("expected exactly seven individual domain anchors")
    witness_index = {row["witness_id"]: row for row in witnesses}
    if len(witness_index) != len(witnesses):
        raise TableBuildError("duplicate closure witness ID")
    for row in closure:
        witness_ids = () if row["witness_ids"] == "not_applicable" else tuple(row["witness_ids"].split(";"))
        for witness_id in witness_ids:
            witness = witness_index.get(witness_id)
            if witness is None or witness["case_id"] != row["case_id"] or witness["predicate_status"] != row["status"]:
                raise TableBuildError(f"closure witness reference mismatch: {row['case_id']}/{row['predicate']}/{witness_id}")
    selected = {(row["record_kind"], row["record_id"]) for row in ledger if row["selection_status"] == "included"}
    expected_selected = {("core_case", case_id) for case_id in case_ids} | {("domain_anchor", anchor_id) for anchor_id in ANCHOR_LABELS}
    if selected != expected_selected:
        raise TableBuildError("selection ledger does not exactly reference generated cases and anchors")
    if any(row["schema_version"] != "3.0.0" for row in cases + closure + anchors + witnesses + ledger):
        raise TableBuildError("mixed schema versions")


def build_cases(cases: list[dict[str, str]], language: int) -> str:
    header = (["ID", "Lineage", "System/version", "Configuration", "Task regime"] if language == 0 else ["ID", "계보", "시스템/버전", "구성", "과제 범위"])
    rows = []
    for source in sorted(cases, key=lambda row: row["case_id"]):
        labels = CASE_LABELS[source["case_id"]]
        rows.append([source["case_id"], tex(source["lineage_id"]), tex(labels["system"][language] + " (" + labels["version"][language] + ")"), tex(labels["configuration"][language]), tex(labels["regime"][language])])
    return table("llllp{.25\\linewidth}", header, rows)


def build_closure(cases: list[dict[str, str]], closure: list[dict[str, str]], language: int) -> str:
    indexed = {(row["case_id"], row["predicate"]): row["status"] for row in closure}
    header = ["ID"] + [PREDICATE_LABELS[predicate][language] for predicate in PREDICATES]
    rows = [[case["case_id"]] + [STATUS_LABELS[indexed[(case["case_id"], predicate)]][language] for predicate in PREDICATES] for case in sorted(cases, key=lambda row: row["case_id"])]
    return table("l" + "p{.16\\linewidth}" * 5, header, rows)


def build_anchors(anchors: list[dict[str, str]], language: int) -> str:
    header = (["ID", "System/domain", "Analysis target", "Evaluator/evidence", "Decision role", "Fidelity boundary"] if language == 0 else ["ID", "시스템/분야", "분석 대상", "평가기/근거", "의사결정 역할", "충실도 경계"])
    rows = []
    for source in sorted(anchors, key=lambda row: row["anchor_id"]):
        labels = ANCHOR_LABELS[source["anchor_id"]]
        if source["system"] != labels[0][0]:
            raise TableBuildError(f"anchor label mismatch: {source['anchor_id']}")
        rows.append([source["anchor_id"], tex(labels[0][language] + " / " + labels[1][language]), tex(labels[2][language]), tex(labels[3][language]), tex(labels[4][language]), tex(labels[5][language])])
    return table("llp{.18\\linewidth}p{.18\\linewidth}p{.18\\linewidth}p{.16\\linewidth}", header, rows)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    cases = read_rows(CASE_PATH)
    closure = read_rows(CLOSURE_PATH)
    anchors = read_rows(ANCHOR_PATH)
    witnesses = read_rows(WITNESS_PATH)
    ledger = read_rows(LEDGER_PATH)
    validate(cases, closure, anchors, witnesses, ledger)
    outputs = {
        "tbl-servo2-cases.tex": build_cases(cases, 0),
        "tbl-servo2-cases-ko.tex": build_cases(cases, 1),
        "tbl-servo2-closure.tex": build_closure(cases, closure, 0),
        "tbl-servo2-closure-ko.tex": build_closure(cases, closure, 1),
        "tbl-servo2-anchors.tex": build_anchors(anchors, 0),
        "tbl-servo2-anchors-ko.tex": build_anchors(anchors, 1),
    }
    for name, content in outputs.items():
        (ROOT / name).write_bytes(content.encode("utf-8"))
    manifest = {
        "schema_version": "3.0.0",
        "generator_sha256": digest(Path(__file__)),
        "inputs": {path.name: digest(path) for path in (CASE_PATH, CLOSURE_PATH, WITNESS_PATH, ANCHOR_PATH, LEDGER_PATH)},
        "outputs": {name: digest(ROOT / name) for name in sorted(outputs)},
        "counts": {"cases": 6, "lineages": 5, "closure_cells": 30, "anchors": 7},
    }
    (ROOT / "servo2_generated_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
