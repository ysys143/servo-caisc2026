#!/usr/bin/env python3
"""Drive independent headless LLM CLIs as blind coders over the SERVO systems.

Each (system, cli) pair receives the SAME fixed rubric + neutral source
description (rubric.txt, systems_desc.json) and must return a JSON coding.
Raw outputs and parsed JSON are saved under raters/; a combined codings.csv is
written for compute_fleiss.py.

Coders are blind to one another and to the author's (Coder A) labels. They are
NOT blind to system identity -- the systems are widely known and the models have
memorized them -- which is a stated limitation in the paper.

Usage: python3 run_coders.py            # all coders, all systems
       python3 run_coders.py claude     # restrict to one coder
This SPENDS external API tokens (codex in particular is token-heavy). No-op-safe
to re-run: each call overwrites its own raters/<coder>__<system>.* files.
"""
import csv, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUBRIC = open(os.path.join(HERE, "rubric.txt"), encoding="utf-8").read()
DESCS = json.load(open(os.path.join(HERE, "systems_desc.json"), encoding="utf-8"))
OUT = os.path.join(HERE, "raters")
os.makedirs(OUT, exist_ok=True)

CODERS = ["claude", "codex", "agy"]   # Anthropic, OpenAI, Google (Antigravity)
TIMEOUT = 300

# Pinned models, recorded to coders.json for reproducibility.
MODELS = {
    "claude": "claude-opus-4-8 (--model flag)",
    "codex":  "gpt-5.5 (-m flag)",
    "agy":    "Gemini 3.1 Pro (High) via ~/.gemini/antigravity-cli/settings.json",
}


def build_cmd(cli, prompt):
    if cli == "claude":
        return ["claude", "--model", "claude-opus-4-8", "-p", prompt]
    if cli == "codex":
        return ["codex", "exec", "--skip-git-repo-check", "-m", "gpt-5.5", prompt]
    if cli == "agy":
        # agy headless: prompt passed to --prompt; flags follow. Invocation
        # pattern taken from multi-ai-delegate council-bridge.sh.
        return ["agy", "--prompt", prompt, "--print-timeout", "280s",
                "--dangerously-skip-permissions"]
    raise ValueError(f"unknown coder: {cli}")
FIELDS = ["loop_status", "Vsyntax", "Vsemantic", "Vempirical",
          "Vhuman", "Vcalibrated", "Vcompleteness", "H"]

PROMPT = """You are an independent coder applying a FIXED rubric to ONE described autonomous-science system. Code ONLY from the description; do not browse the web or use tools. Output ONLY one JSON object and nothing else.

{rubric}

SYSTEM DESCRIPTION:
{desc}

Output a JSON object with EXACTLY these keys:
"loop_status" (string: one of none, partial-task, partial-analysis, closed-comp, closed-wetlab),
"Vsyntax","Vsemantic","Vempirical","Vhuman","Vcalibrated" (each integer 0 or 1),
"Vcompleteness" (integer 0 to 3),
"H" (number between 0 and 1).
Output JSON only, no prose, no code fences."""


def extract_json(s):
    """Return the last balanced {...} object that parses as JSON, else None."""
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
    # stdin=DEVNULL: agy (and some CLIs) otherwise block waiting on stdin EOF.
    p = subprocess.run(build_cmd(cli, prompt), capture_output=True,
                       text=True, timeout=TIMEOUT, stdin=subprocess.DEVNULL)
    return p.stdout + "\n" + p.stderr


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    coders = [only] if only else list(CODERS)
    rows, fails = [], []
    for sysid, desc in DESCS.items():
        prompt = PROMPT.format(rubric=RUBRIC, desc=desc)
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
            if obj and all(f in obj for f in FIELDS):
                row = {"system": sysid, "coder": cli}
                row.update({f: obj[f] for f in FIELDS})
                rows.append(row)
            else:
                fails.append(f"{cli}/{sysid}")
                print(f"  !! no valid JSON for {cli}/{sysid}")
    # Rebuild codings.csv from ALL rater json files on disk -- robust to partial
    # or per-coder runs (e.g., codex run separately later): the CSV always
    # reflects every coding produced so far.
    allrows = []
    for fn in sorted(os.listdir(OUT)):
        if not fn.endswith(".json") or "__" not in fn:
            continue
        cli, sysid = fn[:-len(".json")].split("__", 1)
        try:
            obj = json.load(open(os.path.join(OUT, fn), encoding="utf-8"))
        except Exception:
            obj = None
        if obj and all(f in obj for f in FIELDS):
            row = {"system": sysid, "coder": cli}
            row.update({f: obj[f] for f in FIELDS})
            allrows.append(row)
    with open(os.path.join(HERE, "codings.csv"), "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["system", "coder"] + FIELDS)
        w.writeheader()
        for r in allrows:
            w.writerow(r)
    with open(os.path.join(HERE, "coders.json"), "w", encoding="utf-8") as f:
        json.dump({"coders_run": coders, "models": MODELS,
                   "n_systems": len(DESCS)}, f, indent=2)
    print(f"\nThis run: {len(rows)} ok, {len(fails)} failed"
          + (f" -> {fails}" if fails else "")
          + f"\ncodings.csv now has {len(allrows)} total rows from raters/"
          + "\nwrote coders.json (model pins)")


if __name__ == "__main__":
    main()
