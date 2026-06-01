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

# Sensitivity: how the mechanically-closed contingency moves when the ambiguous
# outcomes (weak / unknown) are recoded to the optimistic (yes) or pessimistic (no) pole.
print("\n=== Sensitivity: recode weak/unknown (mechanically-closed systems) ===")
closed = [(s, r) for s, r in sys_rows.items() if r["A_loop_status"] in CLOSED]


def summarize(recode):
    cells = {}
    for s, r in closed:
        cal = "Vcal=1" if r["A_Vcalibrated"] == "1" else "Vcal=0"
        t = recode.get(tc(s), tc(s))
        cells[(cal, t)] = cells.get((cal, t), 0) + 1
    return ", ".join(f"{k[0]}/{k[1]}:{v}" for k, v in sorted(cells.items()))


print(f"  as-coded                   : {summarize({})}")
print(f"  weak/unknown -> yes (optim) : {summarize({'weak': 'yes', 'unknown': 'yes'})}")
print(f"  weak/unknown -> no  (pessim): {summarize({'weak': 'no', 'unknown': 'no'})}")
print("  Robust direction: no Vcal=0 closed system is trustworthy under any recoding")
print("  (AI Scientist v1 stays untrustworthy); but N=4 is far too small for inference,")
print("  and under the pessimistic recoding calibrated systems no longer cleanly separate.")
