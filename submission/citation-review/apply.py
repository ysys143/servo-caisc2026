#!/usr/bin/env python3
"""Apply one paper's 3-layer review results to ledger.tsv + papers.tsv.
Usage: python3 apply.py results/<bibkey>.json
Schema:
{
  "bibkey": "...",
  "read_status": "READ"|"TARGETED",
  "note": "...",                                  # blind-digest / reading note
  "claims": { "C008": {"status":"VERIFIED"|"FLAGGED","verdict":..,"evidence":..,"fix":..}, ... },
  "reverse_findings": [ {"fact":..,"loc":..,"mismatch":..,"severity":"HIGH|MED|LOW"}, ... ]
}
- Claims (Layer 2) update existing C### rows.
- reverse_findings (Layer 3) are appended as new R### rows (type=REVERSE, status=FLAGGED, verdict=REVERSE).
- Sets paper.read_status, n_verified, reverse_done=YES; digest=YES if results/<bibkey>.digest.md exists.
Fields with tabs/newlines are sanitized. Re-applying a paper first removes its prior R### rows (idempotent)."""
import os, csv, sys, json

HERE=os.path.dirname(os.path.abspath(__file__))
def san(s): return " ".join(str(s).replace("\t"," ").split())
def rf(p):
    with open(p) as f:
        rr=csv.reader(f,delimiter="\t"); h=next(rr); return h,[dict(zip(h,x)) for x in rr]
def wf(p,h,rows):
    with open(p,"w",newline="") as f:
        w=csv.writer(f,delimiter="\t"); w.writerow(h)
        for r in rows: w.writerow([r[c] for c in h])

def main():
    res=json.load(open(sys.argv[1])); bk=res["bibkey"]
    lh,ledger=rf(os.path.join(HERE,"ledger.tsv"))
    ph,papers=rf(os.path.join(HERE,"papers.tsv"))
    VALID={"ACCURATE","INACCURATE-NUM","MISCHARACTERIZATION","MISATTRIBUTION",
           "OVERCLAIM","CONTEXT-MISUSE","UNSUPPORTED","IMPRECISE-OK","REVERSE",""}
    by_id={r["claim_id"]:r for r in ledger}
    updated=0; unknown=[]
    for cid,u in res.get("claims",{}).items():
        if cid not in by_id: unknown.append(cid); continue
        r=by_id[cid]
        if r["bibkey"]!=bk: print(f"WARN {cid} belongs to {r['bibkey']} not {bk}")
        vd=u.get("verdict","")
        if vd not in VALID: print(f"WARN {cid} invalid verdict '{vd}'")
        PROB={"INACCURATE-NUM","MISCHARACTERIZATION","MISATTRIBUTION","OVERCLAIM","CONTEXT-MISUSE","UNSUPPORTED"}
        # canonical status derived from verdict (ignore agent's free-form status string)
        r["status"]="FLAGGED" if vd in PROB else "VERIFIED"; r["verdict"]=vd
        r["evidence"]=san(u.get("evidence","")); r["fix"]=san(u.get("fix",""))
        updated+=1
    if unknown: print("UNKNOWN claim_ids (skipped):",unknown)
    # drop prior R### rows for this bibkey (idempotent re-apply), then append fresh
    ledger=[r for r in ledger if not (r["claim_id"].startswith("R") and r["bibkey"]==bk)]
    rmax=max([int(r["claim_id"][1:]) for r in ledger if r["claim_id"].startswith("R")]+[0])
    nrev=0
    for i,rfd in enumerate(res.get("reverse_findings",[]),1):
        rid=f"R{rmax+i:03d}"
        if isinstance(rfd,str): rfd={"fact":rfd,"loc":"","mismatch":"","severity":""}
        ledger.append({"claim_id":rid,"bibkey":bk,"loc":san(rfd.get("loc","")),
            "type":"REVERSE","status":"FLAGGED","verdict":"REVERSE",
            "claim_text":san("[reverse] "+rfd.get("fact","")+" | mismatch: "+rfd.get("mismatch","")+" ["+rfd.get("severity","")+"]"),
            "evidence":san(rfd.get("loc","")),"fix":san(rfd.get("mismatch",""))})
        nrev+=1
    # paper flags
    digest_exists=os.path.exists(os.path.join(HERE,"results",f"{bk}.digest.md"))
    for p in papers:
        if p["bibkey"]==bk:
            p["read_status"]=res.get("read_status",p["read_status"])
            p["n_verified"]=str(sum(1 for r in ledger if r["bibkey"]==bk and not r["claim_id"].startswith("R") and r["status"]!="PENDING"))
            p["reverse_done"]="YES" if "reverse_findings" in res else p.get("reverse_done","")
            p["digest"]="YES" if digest_exists else p.get("digest","")
    wf(os.path.join(HERE,"ledger.tsv"),lh,ledger)
    wf(os.path.join(HERE,"papers.tsv"),ph,papers)
    print(f"{bk}: claims updated={updated}, reverse appended={nrev}, digest={'YES' if digest_exists else 'no'}, read={res.get('read_status')}")

if __name__=="__main__": main()
