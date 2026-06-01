#!/usr/bin/env python3
"""Cohen's kappa between Coder A and Coder B over systems.csv.

Reads systems.csv, which must contain A_* and B_* columns for each coded field.
Reports per-field Cohen's kappa and raw agreement. With a small N (~6 systems)
kappa is noisy and reported as a transparency measure, not a precision estimate.

Usage: python3 compute_kappa.py
"""
import csv, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "systems.csv")

FIELDS = ["loop_status", "Vcompleteness", "Vsyntax", "Vsemantic",
          "Vempirical", "Vhuman", "Vcalibrated"]


def cohen_kappa(a, b):
    """a, b: equal-length lists of categorical labels."""
    n = len(a)
    if n == 0:
        return float("nan"), float("nan")
    cats = sorted(set(a) | set(b))
    # raw agreement
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    # expected agreement
    pa = {c: a.count(c) / n for c in cats}
    pb = {c: b.count(c) / n for c in cats}
    pe = sum(pa[c] * pb[c] for c in cats)
    kappa = (po - pe) / (1 - pe) if pe != 1 else 1.0
    return po, kappa


def main():
    rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
    have_b = all((f"B_{FIELDS[0]}") in r for r in rows) if rows else False
    if not have_b:
        print("No B_* columns found in systems.csv -- merge Coder B first.")
        sys.exit(2)
    print(f"Inter-coder reliability over N={len(rows)} systems (Coder A vs Coder B):\n")
    print(f"{'field':<16}{'raw agree':>10}{'kappa':>9}")
    kappas = []
    for f in FIELDS:
        a = [r[f"A_{f}"].strip() for r in rows]
        b = [r[f"B_{f}"].strip() for r in rows]
        po, k = cohen_kappa(a, b)
        kappas.append(k)
        print(f"{f:<16}{po:>10.2f}{k:>9.2f}")
    mean_k = sum(kk for kk in kappas if kk == kk) / len(kappas)
    print(f"\nmean kappa across fields: {mean_k:.2f}")


if __name__ == "__main__":
    main()
