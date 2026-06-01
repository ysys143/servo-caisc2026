#!/usr/bin/env python3
"""Validate domain_systems.csv and regenerate the cross-domain comparison table (TeX).

Makes the seven-domain Table 2 auditable to the same standard as the core-system
Table 1: every coded domain row must carry a source quote and only citation keys
that resolve in references.bib. Fails (exit 1) otherwise.

Usage: python3 build_domain_tables.py   # validates domain_systems.csv, writes tbl-domain.tex
"""
import csv, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "domain_systems.csv")
# references.bib may sit a level up (repo) or beside / two levels up (bundle layouts).
BIB_PATH = next(
    (p for p in (os.path.join(HERE, "..", "references.bib"),
                 os.path.join(HERE, "references.bib"),
                 os.path.join(HERE, "..", "..", "references.bib"))
     if os.path.exists(p)),
    os.path.join(HERE, "..", "references.bib"))
OUT_PATH = os.path.join(HERE, "tbl-domain.tex")


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
            errs.append(f"{r['domain']}: missing source_quote")
        for k in (r.get("citation_keys") or "").split(";"):
            k = k.strip()
            if k and k not in keys:
                errs.append(f"{r['domain']}: citation_key '{k}' absent from references.bib")
    if errs:
        print("VALIDATION FAILED:")
        for e in errs:
            print("  -", e)
        sys.exit(1)
    print(f"OK: {len(rows)} domains coded; every row has a source quote and resolvable citations.")

    lines = [r"% AUTO-GENERATED from analysis/domain_systems.csv by build_domain_tables.py -- do not edit by hand.",
             r"\begin{tabular}{@{}lccccp{2.6cm}@{}}", r"\toprule",
             r"Domain & $V$ type & $V$ reliability & Loop & $\pi$ & Primary bottleneck \\", r"\midrule"]
    for r in rows:
        lines.append(f"{r['domain']} & {r['V_type']} & {r['V_reliability']} & "
                     f"{r['loop']} & {r['pi']} & {r['bottleneck']} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
