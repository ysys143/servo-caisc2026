#!/usr/bin/env python3
"""Blind multi-vendor re-coding of validator DECISION ARCHITECTURE (calibration split).

Splits the old conflated `Vcalibrated` into mechanically-codeable sub-constructs
(V_present, V_gating, novelty_gate; see rubric_calib.txt) and re-runs the three
model-pinned blind coders on the key disputed core systems, so we can compare
agreement on the sharpened constructs against the old single label (on which the
author and all three coders split for AI Scientist Nature 2026).

Usage: python3 run_calib.py [claude|codex|agy]   (default: all three)
"""
import csv, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DESCS = json.load(open(os.path.join(HERE, "systems_desc.json"), encoding="utf-8"))
RUBRIC = open(os.path.join(HERE, "rubric_calib.txt"), encoding="utf-8").read()
OUT = os.path.join(HERE, "raters_calib")
os.makedirs(OUT, exist_ok=True)

KEY = list(DESCS.keys())   # all 14 Tier-1 systems
CODERS = ["claude", "codex"]   # agy excluded: empty output in headless re-coding
TIMEOUT = 200
FIELDS = ["V_present", "V_gating", "novelty_gate"]

PROMPT = """You are an independent coder applying a FIXED rubric to ONE described autonomous-science system. Code ONLY from the description; do not browse the web or use tools. Output ONLY one JSON object and nothing else.

{rubric}

Output a JSON object with EXACTLY these keys:
"V_present" (integer 0 or 1),
"V_gating" (integer 0 or 1),
"novelty_gate" (one of: "calibrated_auto","biased_auto","human","predefined","none").

SYSTEM DESCRIPTION:
{desc}

Output JSON only, no prose, no code fences."""


def build_cmd(cli, prompt):
    if cli == "claude":
        return ["claude", "--model", "claude-opus-4-8", "-p", prompt]
    if cli == "codex":
        return ["codex", "exec", "--skip-git-repo-check", "-m", "gpt-5.5", prompt]
    if cli == "agy":
        return ["agy", "--prompt", prompt, "--print-timeout", "180s",
                "--dangerously-skip-permissions"]
    raise ValueError(cli)


def extract_json(s):
    end = s.rfind("}")
    while end != -1:
        depth = 0
        for i in range(end, -1, -1):
            if s[i] == "}":
                depth += 1
            elif s[i] == "{":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(s[i:end + 1])
                    except Exception:
                        break
        end = s.rfind("}", 0, end)
    return None


def call(cli, prompt):
    p = subprocess.run(build_cmd(cli, prompt), capture_output=True, text=True,
                       timeout=TIMEOUT, stdin=subprocess.DEVNULL)
    return p.stdout + "\n" + p.stderr


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    coders = [only] if only else list(CODERS)
    for sysid in KEY:
        prompt = PROMPT.format(rubric=RUBRIC, desc=DESCS[sysid])
        for cli in coders:
            print(f"[{cli}] {sysid} ...", flush=True)
            try:
                raw = call(cli, prompt)
            except subprocess.TimeoutExpired:
                raw = "TIMEOUT"
            open(os.path.join(OUT, f"{cli}__{sysid}.raw.txt"), "w",
                 encoding="utf-8").write(raw)
            obj = extract_json(raw)
            open(os.path.join(OUT, f"{cli}__{sysid}.json"), "w",
                 encoding="utf-8").write(json.dumps(obj, indent=2) if obj else "null")
    rows = []
    for fn in sorted(os.listdir(OUT)):
        if not fn.endswith(".json") or "__" not in fn:
            continue
        cli, sysid = fn[:-len(".json")].split("__", 1)
        try:
            obj = json.load(open(os.path.join(OUT, fn), encoding="utf-8"))
        except Exception:
            obj = None
        if obj and all(f in obj for f in FIELDS):
            rows.append({"system": sysid, "coder": cli,
                         **{f: obj[f] for f in FIELDS}})
    with open(os.path.join(HERE, "codings_calib.csv"), "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["system", "coder"] + FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"\nwrote codings_calib.csv ({len(rows)} rows)")


if __name__ == "__main__":
    main()
