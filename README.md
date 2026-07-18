# Servo (CAISc 2026) — Reproducibility Package

Supplementary material for *Formalizing AI Scientist Systems: A Component Framework and Theoretical Analysis*, CAISc 2026.

## Contents

- `analysis/coding_protocol.md` — the cross-system coding protocol and rubric.
- `analysis/systems.csv`, `analysis/domain_systems.csv` — coding sheets (core systems; the seven-domain map) with a representative source quote and citation per row.
- `analysis/multicoder/` — multi-vendor blind re-coding: exact invocations and per-model outputs from three model-pinned LLM coders.
- `analysis/reliability_report.md` — inter-coder reliability estimates (Fleiss'/Cohen's κ).
- `analysis/build_servo_tables.py`, `analysis/build_domain_tables.py`, `analysis/compute_calib.py` — citation-validating table-regeneration scripts.
- `references.bib` — bibliography.

## Status

The coding is released as **provisional structured annotation**: the scripts verify citation presence and non-empty source quotes but do not validate the semantic entailment of each coded field; independent reproduction of the interpretive coding requires consulting the cited primary sources directly. All analyzed papers are publicly accessible; no separate dataset was generated.
