#!/usr/bin/env python3
"""Inter-rater reliability over codings.csv (long format: system, coder, fields).

Reports Fleiss' kappa (>=3 raters) and pairwise Cohen's kappa for the categorical
fields, and mean pairwise |difference| for the continuous H. Optionally compares
each LLM coder against the author column A_<field> in ../systems.csv.

With N=6 systems these statistics are noisy and reported as transparency measures
for automated raters, not as a claim of human-level inter-rater reliability.
"""
import csv, itertools, os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, "codings.csv"), encoding="utf-8")))
CAT = ["loop_status", "Vsyntax", "Vsemantic", "Vempirical",
       "Vcalibrated", "Vhuman", "Vcompleteness"]
coders = sorted(set(r["coder"] for r in rows))
systems = sorted(set(r["system"] for r in rows))

data = defaultdict(lambda: defaultdict(dict))     # data[field][system][coder] = value
for r in rows:
    for f in CAT + ["H"]:
        data[f][r["system"]][r["coder"]] = r[f]


def fleiss(field):
    items = [s for s in systems if len(data[field][s]) == len(coders)]
    if len(items) < 1 or len(coders) < 3:
        return None
    cats = sorted({data[field][s][c] for s in items for c in coders})
    n = len(coders)
    P, tot = [], {c: 0 for c in cats}
    for s in items:
        cnt = {c: 0 for c in cats}
        for c in coders:
            cnt[data[field][s][c]] += 1
        P.append((sum(v * v for v in cnt.values()) - n) / (n * (n - 1)))
        for c in cats:
            tot[c] += cnt[c]
    Pbar = sum(P) / len(P)
    N = len(items) * n
    Pe = sum((tot[c] / N) ** 2 for c in cats)
    return len(items), Pbar, (1.0 if Pe == 1 else (Pbar - Pe) / (1 - Pe))


def cohen(field, c1, c2, src=None):
    if src is None:
        items = [s for s in systems if c1 in data[field][s] and c2 in data[field][s]]
        a = [data[field][s][c1] for s in items]
        b = [data[field][s][c2] for s in items]
    else:                                          # c2 is the author column in systems.csv
        items = [s for s in systems if c1 in data[field][s] and s in src]
        a = [data[field][s][c1] for s in items]
        b = [src[s] for s in items]
    n = len(a)
    if n == 0:
        return None
    cats = set(a) | set(b)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    return po, (1.0 if pe == 1 else (po - pe) / (1 - pe))


print(f"Coders ({len(coders)}): {coders}   Systems: {len(systems)}\n")
print("== Fleiss' kappa (>=3 raters) ==")
for f in CAT:
    r = fleiss(f)
    if r:
        print(f"  {f:<14} N={r[0]} Pbar={r[1]:.2f} fleiss_kappa={r[2]:.2f}")

print("\n== Pairwise Cohen's kappa (between LLM coders) ==")
for f in CAT:
    parts = []
    for c1, c2 in itertools.combinations(coders, 2):
        r = cohen(f, c1, c2)
        if r:
            parts.append(f"{c1[:3]}-{c2[:3]}={r[1]:.2f}")
    print(f"  {f:<14} " + "  ".join(parts))

print("\n== H (continuous): mean pairwise |difference| ==")
diffs = []
for s in systems:
    vals = [float(data["H"][s][c]) for c in coders if c in data["H"][s]]
    for a, b in itertools.combinations(vals, 2):
        diffs.append(abs(a - b))
print(f"  mean pairwise |H diff| = {sum(diffs) / len(diffs):.3f}" if diffs else "  (insufficient)")

# Optional: each LLM coder vs the author (Coder A) in ../systems.csv
apath = os.path.join(HERE, "..", "systems.csv")
if os.path.exists(apath):
    arows = list(csv.DictReader(open(apath, encoding="utf-8")))
    NAME = {"robot_scientist": "Robot Scientist", "coscientist": "Coscientist",
            "ai_scientist_2024": "AI Scientist (2024)",
            "ai_scientist_2026": "AI Scientist (Nature 2026)",
            "agent_laboratory": "Agent Laboratory", "novelseek": "NovelSeek"}
    byname = {r["system"]: r for r in arows}
    print("\n== Each LLM coder vs author (Coder A) -- Cohen's kappa ==")
    for f in CAT:
        src = {sid: byname[NAME[sid]][f"A_{f}"] for sid in systems
               if NAME.get(sid) in byname}
        parts = []
        for c in coders:
            r = cohen(f, c, None, src=src)
            if r:
                parts.append(f"{c[:3]}={r[1]:.2f}")
        print(f"  {f:<14} " + "  ".join(parts))
