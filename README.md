# Servo (CAISc 2026) — Reproducibility Package

Supplementary material for *Formalizing AI Scientist Systems: A Component Framework and Theoretical Analysis*, CAISc 2026.

## Contents

- `analysis/coding_protocol.md` — the cross-system coding protocol and rubric.
- `analysis/systems.csv`, `analysis/domain_systems.csv` — coding sheets (core systems; the seven-domain map) with a representative source quote and citation per row.
- `analysis/multicoder/` — multi-vendor blind re-coding: exact invocations and per-model outputs from three model-pinned LLM coders.
- `analysis/reliability_report.md` — inter-coder reliability estimates (Fleiss'/Cohen's κ).
- `analysis/build_servo_tables.py`, `analysis/build_domain_tables.py`, `analysis/association_descriptive.py` — citation-validating table-regeneration and descriptive-association scripts.
- `analysis/citation_audit/` — per-citation verification of the manuscript against the cited primary sources. Contains a coding rubric (`RUBRIC.md`), machine-readable manifests (`manifest.json`, `core14-manifest.json`, `*-status.json`), an audit harness (`audit_models.py`, `tests/`), and per-source evidence reports (`papers/`, `evidence/`) recording, for each in-text citation, the source claim, the supporting passage, a PASS/PARTIAL judgment with severity, and any recommended correction. Both the English and Korean manuscripts are covered.
- `references.bib` — bibliography.

## Status

The coding is released as **provisional structured annotation**: the scripts verify citation presence and non-empty source quotes but do not validate the semantic entailment of each coded field; independent reproduction of the interpretive coding requires consulting the cited primary sources directly. All analyzed papers are publicly accessible; no separate dataset was generated.

The `citation_audit/` reports were produced with model assistance and manual cross-checking against the primary sources; each judgment cites the specific passage it relies on. They are offered as a transparency record of citation-level verification, not as an infallible oracle—readers should consult the cited sources directly for any claim they wish to rely on.
