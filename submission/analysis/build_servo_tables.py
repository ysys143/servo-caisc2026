#!/usr/bin/env python3
"""Validate systems.csv and regenerate the SERVO core-comparison table (TeX).

Fails (exit 1) if any coded row lacks a source quote or cites a key absent from
references.bib. This makes the cross-system coding behind Table 1 auditable and
the manuscript table a build product rather than hand-written prose.

Usage: python3 build_servo_tables.py   # validates systems.csv, writes tbl-core.tex
"""
import csv, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "systems.csv")
BIB_PATH = os.path.join(HERE, "..", "references.bib")
OUT_PATH = os.path.join(HERE, "tbl-core.tex")


def bib_keys(path):
    keys = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"\s*@\w+\{([^,]+),", line)
            if m:
                keys.add(m.group(1).strip())
    return keys


def main():
    keys = bib_keys(BIB_PATH)
    rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
    errs = []
    for r in rows:
        if not (r.get("source_quote") or "").strip():
            errs.append(f"{r['system']}: missing source_quote")
        if r["citation_key"] not in keys:
            errs.append(f"{r['system']}: citation_key '{r['citation_key']}' absent from references.bib")
    if errs:
        print("VALIDATION FAILED:")
        for e in errs:
            print("  -", e)
        sys.exit(1)
    print(f"OK: {len(rows)} systems coded; every cell has a source quote and a resolvable citation.")

    # Regenerate a compact TeX table from the coded rows.
    lines = [r"% AUTO-GENERATED from analysis/systems.csv by build_servo_tables.py -- do not edit by hand.",
             r"\begin{tabular}{@{}lccc@{}}", r"\toprule",
             r"System & Loop & $V$ completeness & $H$ \\", r"\midrule"]
    for r in rows:
        lines.append(f"{r['system']} & {r['A_loop_status']} & {r['A_Vcompleteness']} & {r['A_H']} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
