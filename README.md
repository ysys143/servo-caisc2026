# Servo (CAISc 2026) — Reproducibility Package

Supplementary material for *Formalizing AI Scientist Systems: A Component Framework and Theoretical Analysis*, CAISc 2026.

## Contents

- `analysis/coding_protocol.md` — the cross-system coding protocol and rubric.
- `analysis/systems.csv`, `analysis/domain_systems.csv` — coding sheets (core systems; the seven-domain map) with a representative source quote and citation per row.
- `analysis/multicoder/` — multi-vendor blind re-coding: exact invocations and per-model outputs from three model-pinned LLM coders.
- `analysis/reliability_report.md` — inter-coder reliability estimates (Fleiss'/Cohen's κ).
- `analysis/build_servo_tables.py`, `analysis/build_domain_tables.py`, `analysis/multicoder/compute_calib.py` — the citation-validating table-regeneration and calibration scripts named in the paper's reproducibility statement. `analysis/association_descriptive.py` additionally reports the descriptive association between gating calibration and trustworthy closure.
- `analysis/citation_audit/` — citation verification against the cited primary sources, released at **two scopes**. `core14-status.json` carries the machine-readable state of the completed one.
  - **Complete — the 14 Tier-1 core systems** (`core14-manifest.json`, `core14-status.json`, `papers/`, `evidence/`, `final-reconciliation.md`). Each source was read as one complete PDF, recording per in-text citation the source claim, the supporting passage, and a PASS/PARTIAL judgment with severity plus any recommended correction. All 14 are `complete`; English–Korean manuscript parity and manual QA are reconciled.
  - **Retired — a 59-source sweep that duplicated work already done.** A second harness
    once aimed the same per-source procedure at the whole bibliography. It was stopped at
    5 of 59 and its ledger has been deleted, because `citation-review/` (in the paper's
    own repository, summarised below) had already read all 59 sources in full and
    adjudicated 128 of 128 atomic claims. `manifest.json` is kept: it is not sweep state
    but the citation-link inventory that `verify_core14.py` reads to check each Tier-1
    report against its assigned links.
  - Supporting files: the audit rubric (`RUBRIC.md`) and the harness (`audit_models.py`, `verify_audit.py`, `verify_core14.py`, `tests/`). The verifiers check structural gates (PDF hash, page count, manifest freeze, manuscript-link inventory, report headings); they do not infer semantic entailment, which is recorded in the reports themselves.
- Citation verification of the **full bibliography** was carried out separately from the
  audit above: all 59 cited sources were read in full and 128 atomic claims adjudicated
  (ACCURATE 97, IMPRECISE-OK 17, MISATTRIBUTION 8, MISCHARACTERIZATION 4, CONTEXT-MISUSE 1,
  OVERCLAIM 1). Fourteen claims were flagged for correction and all fourteen have been
  applied to the manuscript. That working set lives in the paper's repository rather than
  here; the corrections it produced are recorded in Appendix D of the post-submission
  manuscript.
- `references.bib` — bibliography.

## Status

The coding is released as **provisional structured annotation**: the scripts verify citation presence and non-empty source quotes but do not validate the semantic entailment of each coded field; independent reproduction of the interpretive coding requires consulting the cited primary sources directly. All analyzed papers are publicly accessible; no separate dataset was generated.

The completed `citation_audit/` reports (the 14 Tier-1 systems) were produced with model assistance and manual cross-checking against the primary sources; each judgment cites the specific passage it relies on. They are offered as a transparency record of citation-level verification, not as an infallible oracle—readers should consult the cited sources directly for any claim they wish to rely on.
