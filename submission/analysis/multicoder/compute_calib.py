#!/usr/bin/env python3
"""Agreement on the sharpened calibration constructs vs the old single Vcalibrated.

Demonstrates that the AI Scientist (Nature 2026) author-vs-coder dispute on the
old `Vcalibrated` (author=1, all three coders=0) was a CONSTRUCT CONFLATION:
once split into V_present and V_gating, the coders agree with each other and with
the author on each sharpened construct. Counts only; N is small by design (this is
the key-case demonstration, not the full study).
"""
import csv, os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, "codings_calib.csv"), encoding="utf-8")))
author = {r["system"]: r for r in
          csv.DictReader(open(os.path.join(HERE, "author_calib.csv"), encoding="utf-8"))}
FIELDS = ["V_present", "V_gating", "novelty_gate"]
coders = sorted(set(r["coder"] for r in rows))
systems = sorted(set(r["system"] for r in rows))
data = defaultdict(lambda: defaultdict(dict))
for r in rows:
    for f in FIELDS:
        data[f][r["system"]][r["coder"]] = str(r[f])


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


print(f"Coders: {coders}   Systems: {len(systems)}\n")
print("=== Per-system: coders[a/c/...] | author ===")
for s in systems:
    parts = []
    for f in FIELDS:
        vals = "/".join(data[f][s].get(c, "?") for c in coders)
        a = author.get(s, {}).get(f, "?")
        parts.append(f"{f}=[{vals}|A:{a}]")
    print(f"  {s:<20} " + "  ".join(parts))

print("\n=== Fleiss kappa (3 coders) on the sharpened constructs ===")
for f in FIELDS:
    r = fleiss(f)
    if r:
        print(f"  {f:<14} N={r[0]} raw_agreement={r[1]:.2f} fleiss_kappa={r[2]:.2f}")

print("\n=== Author vs coder-majority match per field ===")
for f in FIELDS:
    match = 0
    tot = 0
    for s in systems:
        vals = [data[f][s][c] for c in coders if c in data[f][s]]
        if not vals or s not in author:
            continue
        maj = max(set(vals), key=vals.count)
        tot += 1
        match += (maj == author[s].get(f))
    print(f"  {f:<14} author==coder-majority on {match}/{tot} systems")

print("\n=== The AI Scientist Nature 2026 case (old Vcalibrated: author=1 vs all coders=0) ===")
s = "ai_scientist_2026"
for f in FIELDS:
    print(f"  {f:<14} coders={[data[f][s].get(c) for c in coders]}  author={author.get(s, {}).get(f)}")
print("  -> if coders now agree (V_present=1, V_gating=0), the old dispute was the")
print("     conflation of 'has a calibrated layer' with 'the deciding layer is calibrated'.")
