# Servo (CAISc 2026) — Reproducibility Package

Supplementary material for *Formalizing AI Scientist Systems: A Component Framework and Theoretical Analysis*, CAISc 2026.

## Contents

- `analysis/coding_protocol.md` — the cross-system coding protocol and rubric.
- `analysis/systems.csv`, `analysis/domain_systems.csv` — coding sheets (core systems; the seven-domain map) with a representative source quote and citation per row.
- `analysis/multicoder/` — multi-vendor blind re-coding: exact invocations and per-model outputs from three model-pinned LLM coders.
- `analysis/reliability_report.md` — inter-coder reliability estimates (Fleiss'/Cohen's κ).
- `analysis/build_servo_tables.py`, `analysis/build_domain_tables.py`, `analysis/multicoder/compute_calib.py` — the citation-validating table-regeneration and calibration scripts named in the paper's reproducibility statement. `analysis/association_descriptive.py` additionally reports the descriptive association between gating calibration and trustworthy closure.
- `analysis/citation_audit/` — citation verification against the cited primary sources, released at **two scopes with different completion states**. Read `core14-status.json` and `status.json` for the machine-readable state of each.
  - **Complete — the 14 Tier-1 core systems** (`core14-manifest.json`, `core14-status.json`, `papers/`, `evidence/`, `final-reconciliation.md`). Each source was read as one complete PDF, recording per in-text citation the source claim, the supporting passage, and a PASS/PARTIAL judgment with severity plus any recommended correction. All 14 are `complete`; English–Korean manuscript parity and manual QA are reconciled.
  - **Incomplete — a wider 59-source bibliography sweep** (`manifest.json`, `status.json`). This scope was declared but not carried out: **5 of 59 sources are complete, 54 remain `pending`, and none of its reconciliation gates are met.** It is shipped so that readers can see exactly which sources were and were not checked, and it must not be read as a verification record.
  - Supporting files: the audit rubric (`RUBRIC.md`) and the harness (`audit_models.py`, `verify_audit.py`, `verify_core14.py`, `tests/`). The verifiers check structural gates (PDF hash, page count, manifest freeze, manuscript-link inventory, report headings); they do not infer semantic entailment, which is recorded in the reports themselves.
- `references.bib` — bibliography.

## Status

The coding is released as **provisional structured annotation**: the scripts verify citation presence and non-empty source quotes but do not validate the semantic entailment of each coded field; independent reproduction of the interpretive coding requires consulting the cited primary sources directly. All analyzed papers are publicly accessible; no separate dataset was generated.

The completed `citation_audit/` reports (the 14 Tier-1 systems) were produced with model assistance and manual cross-checking against the primary sources; each judgment cites the specific passage it relies on. They are offered as a transparency record of citation-level verification, not as an infallible oracle—readers should consult the cited sources directly for any claim they wish to rely on.
