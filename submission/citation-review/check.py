#!/usr/bin/env python3
"""Completeness checker for the 3-layer citation-content-review.
Verifies four invariants and prints progress. Exit 0 iff all PASS."""
import os, csv, sys, re

HERE=os.path.dirname(os.path.abspath(__file__))
BIB="/Users/jaesolshin/Documents/GitHub/CAISc_2026/submission/references.bib"
TEX="/Users/jaesolshin/Documents/GitHub/CAISc_2026/submission/main.tex"

def load(p):
    with open(p) as f: return list(csv.DictReader(f,delimiter="\t"))
def cited_keys():
    tex=open(TEX).read(); ks=set()
    for m in re.finditer(r'\\cite[a-zA-Z]*\{([^}]+)\}',tex):
        for k in m.group(1).split(','): ks.add(k.strip())
    return ks

def main():
    papers=load(os.path.join(HERE,"papers.tsv"))
    ledger=load(os.path.join(HERE,"ledger.tsv"))
    cited=cited_keys(); ok=True

    unread=[p["bibkey"] for p in papers if p["read_status"] not in ("READ","TARGETED")]
    print(f"[1] Papers read: {len(papers)-len(unread)}/{len(papers)}"+(f"  PENDING:{len(unread)}" if unread else "  -> PASS"))
    ok&=not unread

    core=[c for c in ledger if not c["claim_id"].startswith("R")]
    pend=[c["claim_id"] for c in core if c["status"]=="PENDING"]
    noverd=[c["claim_id"] for c in core if c["status"]!="PENDING" and (not c["verdict"] or not c["evidence"])]
    print(f"[2] Atomic claims resolved: {len(core)-len(pend)}/{len(core)}"
          +(f"  PENDING:{len(pend)}" if pend else "")+(f"  MISSING verdict/evidence:{noverd}" if noverd else "")
          +("  -> PASS" if not pend and not noverd else ""))
    ok&=not pend and not noverd

    lk={c["bibkey"] for c in ledger}; pk={p["bibkey"] for p in papers}
    m1=cited-lk; m2=lk-cited
    print(f"[3] Key coverage: cited={len(cited)} ledger={len(lk)} papers={len(pk)}"+("  -> PASS" if not m1 and not m2 and pk==cited else ""))
    if m1: print("    !!! cited but no claim row:",sorted(m1)); ok=False
    if m2: print("    !!! claim key not cited:",sorted(m2)); ok=False
    if pk!=cited: print("    !!! paper set != cited"); ok=False

    nod=[p["bibkey"] for p in papers if p.get("digest")!="YES"]
    nor=[p["bibkey"] for p in papers if p.get("reverse_done")!="YES"]
    print(f"[4] 3-layer done: digest {len(papers)-len(nod)}/{len(papers)}, reverse {len(papers)-len(nor)}/{len(papers)}"
          +("  -> PASS" if not nod and not nor else ""))
    ok&=not nod and not nor

    vd={}
    for c in core:
        if c["status"]!="PENDING": vd[c["verdict"]]=vd.get(c["verdict"],0)+1
    if vd: print("[i] Verdicts:",dict(sorted(vd.items())))
    fl=[c["claim_id"] for c in core if c["status"]=="FLAGGED"]
    rv=[c["claim_id"] for c in ledger if c["claim_id"].startswith("R")]
    if fl: print(f"[i] FLAGGED claims ({len(fl)}):",fl)
    if rv: print(f"[i] REVERSE findings ({len(rv)})")
    print("\n===","ALL INVARIANTS PASS" if ok else "INCOMPLETE / ISSUES","===")
    sys.exit(0 if ok else 1)

if __name__=="__main__": main()
