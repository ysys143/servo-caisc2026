#!/usr/bin/env python3
"""Descriptive (NOT inferential) separation of mechanical vs trustworthy closure.

Reviewers noted a circularity: if "trustworthy closure" is judged by the same
validator fields used as predictors, the V-completeness/trustworthiness link cannot
be tested, only restated. To break this, `trustworthy_closure` is coded in
`trustworthy_closure.csv` from signals EXTERNAL to each system's validator design --
independent replication, post-hoc human audit, documented hallucination, real human
peer review -- with a source per system. This script joins that external outcome to
the validator labels in `systems.csv` and prints a contingency of COUNTS ONLY.

With six core systems (four mechanically closed) the data are far too small for
inference: we deliberately report NO confidence intervals and NO p-values. The table
is a transparency check on the direction of the pattern, not a hypothesis test.
"""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
sys_rows = {r["system"]: r for r in
            csv.DictReader(open(os.path.join(HERE, "systems.csv"), encoding="utf-8"))}
tc_rows = {r["system"]: r for r in
           csv.DictReader(open(os.path.join(HERE, "trustworthy_closure.csv"), encoding="utf-8"))}

CLOSED = {"closed-comp", "closed-wetlab"}   # "mechanical" discovery-loop closure


def tc(system):
    return tc_rows.get(system, {}).get("trustworthy_closure", "?")


print("Per-system (validator labels from systems.csv; outcome from trustworthy_closure.csv):\n")
print(f"  {'system':<28}{'mechanical_loop':<16}{'Vcalibrated':<13}{'trustworthy(external)'}")
for s, r in sys_rows.items():
    loop = "closed" if r["A_loop_status"] in CLOSED else "partial/open"
    print(f"  {s:<28}{loop:<16}{r['A_Vcalibrated']:<13}{tc(s)}")

print("\nContingency over MECHANICALLY-CLOSED systems "
      "(counts only; N far too small for inference):\n")
cells = {}
for s, r in sys_rows.items():
    if r["A_loop_status"] not in CLOSED:
        continue
    cal = "Vcal=1" if r["A_Vcalibrated"] == "1" else "Vcal=0"
    cells.setdefault((cal, tc(s)), []).append(s)
for (cal, t), names in sorted(cells.items()):
    print(f"  {cal} x trustworthy={t:<9}: {len(names)}  ({', '.join(names)})")

n_closed = sum(1 for r in sys_rows.values() if r["A_loop_status"] in CLOSED)
print(f"\nN = {len(sys_rows)} core systems; {n_closed} mechanically closed.")
print("Descriptive only: trustworthy_closure is coded from signals external to the")
print("validator (see trustworthy_closure.csv / trustworthy_closure.md). No CIs, no p-values.")
