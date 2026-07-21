#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REVIEW = ROOT / "submission" / "citation-review"
AUDIT = ROOT / "submission" / "analysis" / "citation_audit"
TEX = ROOT / "submission" / "main.tex"
KO_TEX = ROOT / "submission" / "main_ko.tex"
CURRENT_TEX = ROOT / "submission" / "main_post-submit.tex"
CURRENT_REGISTRY = ROOT / "submission" / "analysis" / "current_claim_registry.json"


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def cited_keys() -> set[str]:
    keys: set[str] = set()
    for path in (TEX,):
        text = path.read_text()
        for match in re.finditer(r"\\cite[a-zA-Z]*\{([^}]+)\}", text):
            keys.update(key.strip() for key in match.group(1).split(","))
    return keys


def keys_in(path: Path) -> set[str]:
    keys: set[str] = set()
    for match in re.finditer(r"\\cite[a-zA-Z]*\{([^}]+)\}", path.read_text()):
        keys.update(key.strip() for key in match.group(1).split(","))
    return keys


def check_current_registry() -> bool:
    registry = json.loads(CURRENT_REGISTRY.read_text())
    current = keys_in(CURRENT_TEX) | keys_in(KO_TEX)
    declared = set(registry["citation_keys"])
    if current != declared:
        print(f"[FAIL] current claim registry drift: added={sorted(current-declared)} removed={sorted(declared-current)}")
        return False
    for name, expected in registry["manuscripts"].items():
        path = ROOT / "submission" / name
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            print(f"[FAIL] current claim registry manuscript drift: {name}")
            return False
    reader = CURRENT_TEX.read_text().split(r"\section{Post-Submission Revisions}", 1)[0]
    korean = KO_TEX.read_text().split(r"\section{제출 후 수정 상태}", 1)[0]
    forbidden = re.compile(r"Schema~?[0-9]|(?<![A-Za-z])R[0-9]{1,2}(?![A-Za-z0-9])")
    if forbidden.search(reader) or forbidden.search(korean):
        print("[FAIL] internal revision identifier leaked into reader-facing text")
        return False
    print(f"[current-claims] {len(current)} citation keys; no reader-facing internal revision tokens")
    return True


def run(label: str, command: list[str], cwd: Path = ROOT) -> bool:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    output = (result.stdout + result.stderr).strip()
    print(f"[{label}] exit={result.returncode}")
    if output:
        print(output)
    return result.returncode == 0


def compile_tex(filename: str) -> bool:
    with tempfile.TemporaryDirectory(prefix="caisc-verify-") as directory:
        result = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", "-halt-on-error", "-output-directory", directory, filename],
            cwd=ROOT / "submission",
            text=True,
            capture_output=True,
        )
        log = Path(directory) / filename.replace(".tex", ".log")
        text = log.read_text(errors="replace") if log.is_file() else result.stdout + result.stderr
        failures = re.findall(r"Undefined (?:citation|references?)|LaTeX Error|Fatal Package Error", text)
        passed = result.returncode == 0 and not failures and (Path(directory) / filename.replace(".tex", ".pdf")).is_file()
        print(f"[xelatex:{filename}] exit={result.returncode} undefined_or_errors={len(failures)}")
        return passed


def check_repaired_claims() -> bool:
    texts = {path.name: path.read_text() for path in (TEX, KO_TEX)}
    forbidden = {
        "AgentLab +2.3 misattribution": r"\+2\.3[^\n]*kim2026aireviewers",
        "GNoME 736 misattribution": r"736 have been independently experimentally realized~\\citep\{cheetham",
        "Aletheia formal label": r"formal-mathematics[^\n]*Aletheia",
        "SciMuse generation-quality claim": r"substantially improve hypothesis-generation quality",
        "Cranmer deterministic search": r"deterministic search~?\\citep\{cranmer2020symbolic",
        "ChemCrow beam claim": r"ChemCrow[^\n]*beam",
        "Circularity misattribution": r"(?:circular validity|self-consistency)[^\n]*aher2023turing",
        "Park full-factorial claim": r"full-factorial designs~?\\citep\{[^}]*park2023generative",
    }
    ok = True
    for label, pattern in forbidden.items():
        for filename, text in texts.items():
            if re.search(pattern, text, re.IGNORECASE):
                print(f"[FAIL] repaired-claim regression: {label} in {filename}")
                ok = False
    if ok:
        print("[repair-regressions] no known corrected-claim pattern found")
    return ok


def main() -> int:
    ok = True
    papers = tsv(REVIEW / "papers.tsv")
    ledger = tsv(REVIEW / "ledger.tsv")
    cited = cited_keys()
    paper_keys = {row["bibkey"] for row in papers}
    ledger_keys = {row["bibkey"] for row in ledger}
    core = [row for row in ledger if not row["claim_id"].startswith("R")]

    counts = {
        "papers": len(papers),
        "ledger_rows": len(ledger),
        "core_claims": len(core),
        "reverse_rows": len(ledger) - len(core),
        "cited_keys": len(cited),
    }
    print(f"[counts] {json.dumps(counts, sort_keys=True)}")
    if paper_keys != cited or ledger_keys != cited:
        print(f"[FAIL] key sets differ: papers-cited={sorted(paper_keys-cited)}, cited-papers={sorted(cited-paper_keys)}")
        ok = False

    unresolved = [row["claim_id"] for row in core if row["status"] == "PENDING"]
    missing_evidence = [row["claim_id"] for row in core if not row["verdict"] or not row["evidence"]]
    if unresolved or missing_evidence:
        print(f"[FAIL] unresolved={unresolved} missing_verdict_or_evidence={missing_evidence}")
        ok = False

    state_text = (REVIEW / "state.md").read_text()
    stale_patterns = ("59편", "128주장", "60=60=60")
    stale = [pattern for pattern in stale_patterns if pattern in state_text]
    if stale:
        print(f"[FAIL] stale state markers: {stale}")
        ok = False

    manifest = json.loads((AUDIT / "core14-manifest.json").read_text())
    novelseek = next(source for source in manifest["sources"] if source["system_id"] == "novelseek")
    if "InternAgent" not in novelseek["name"]:
        print("[FAIL] NovelSeek alias must record renamed InternAgent identity")
        ok = False
    else:
        print("[identity] NovelSeek alias includes renamed InternAgent")

    ok &= run("citation-review/check", [sys.executable, str(REVIEW / "check.py")])
    ok &= run("core14/final", ["uv", "run", "verify_core14.py", "final"], AUDIT)
    ok &= run("pytest", ["uv", "run", "--with", "pytest", "--with", "pydantic", "python", "-m", "pytest", "-q", "tests/test_verify_audit.py", "tests/test_verify_core14.py"], AUDIT)
    ok &= check_repaired_claims()
    ok &= check_current_registry()
    ok &= compile_tex("main.tex")
    ok &= compile_tex("main_ko.tex")
    ok &= compile_tex("main_post-submit.tex")
    ok &= run(
        "servo/release-ready",
        ["uv", "run", "python", "-m", "analysis.validate_servo2", "release-ready", "--package-root", "release/package"],
        ROOT / "submission",
    )
    ok &= run(
        "servo/repository-sync",
        ["uv", "run", "python", "-m", "analysis.validate_servo2", "repository-sync", "--package-root", "release/package", "--reader-pdf", "servo_caiscfp2026_post-submit.pdf"],
        ROOT / "submission",
    )

    print("=== ALL AUTOMATED GATES PASS ===" if ok else "=== AUTOMATED GATES FAILED ===")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
