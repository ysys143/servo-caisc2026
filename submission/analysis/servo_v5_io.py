from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


# Single source of truth for the v5 schema version string (charter lesson:
# "4.1.0" was hardcoded in 4 places in the v4.1 track and drifted).
V5_SCHEMA_VERSION = "5.0.0"

# The three list-based data families each key their records with
# "<case_id>-<LETTER><nn>". `policy` is case-level (one flat record per
# case file, no id, no record list) and is intentionally absent below.
ID_LETTER = {
    "source_proposition": "P",
    "author_alignment": "A",
    "derived_claim": "D",
}
ID_FIELD = {
    "source_proposition": "proposition_id",
    "author_alignment": "alignment_id",
    "derived_claim": "claim_id",
}
RECORD_LIST_FIELD = {
    "source_proposition": "propositions",
    "author_alignment": "alignments",
    "derived_claim": "claims",
}


class ServoV5Error(Exception):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise ServoV5Error("V5_JSON_MISSING", str(path)) from error
    try:
        value = json.loads(text)
    except json.JSONDecodeError as error:
        raise ServoV5Error("V5_JSON_INVALID", f"{path}: {error}") from error
    if not isinstance(value, dict):
        raise ServoV5Error("V5_JSON_NOT_OBJECT", str(path))
    return value


def load_family(dirpath: Path) -> dict[str, dict]:
    if not dirpath.is_dir():
        raise ServoV5Error("V5_FAMILY_DIR_MISSING", str(dirpath))
    return {path.stem: read_json(path) for path in sorted(dirpath.glob("*.json"))}


def id_pattern_for(case_id: str, letter: str) -> re.Pattern[str]:
    return re.compile(rf"^{re.escape(case_id)}-{letter}[0-9]{{2}}$")
