# Retired R24 assets

The following files preserve the stopped baseline-versus-Servo design for auditability. They are not production inputs, are excluded from the protocol hash, and must not be invoked by the R24 Servo-only schedule:

- `baseline_prompt.md` and `baseline.schema.json`
- `statistical_plan.md`
- `scoring.py` and `scoring_contract.json`
- `recommendation_quality.py`, `recommendation_rubric.md`, and `run_quality_evaluation.py`
- sealed probe and action-code files
- stopped run directories `r24-run-002` and `r24-run-003`

Static smoke checks treat distinctive content from these assets as forbidden leakage. Retention does not authorize reuse. Any future comparative experiment requires a new versioned protocol, schedule, smoke contract, and run identifier.
