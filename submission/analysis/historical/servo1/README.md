# Servo Schema 1 migration boundary

Servo Schema 1 is preserved as **historical, non-authoritative migration
material**. Its record-level system and validator-channel tables are
`analysis/servo_core_systems.csv` and `analysis/servo_validator_channels.csv`.
They document the intermediate representation that preceded the portable
event-and-evidence contract.

The current normative contract is Servo Schema 2 in
`analysis/servo_schema.yaml`. Current validation and regeneration use
`python -m analysis.validate_servo2`; they do not read either Schema 1 table.
The legacy `analysis/validate_servo_consistency.py` entry point deliberately
fails closed when presented with the current Schema 2 schema, so an obsolete
record-level projection cannot be mistaken for current validation evidence.

The Schema 1 CSVs and validator remain available to reconstruct the migration
history. They must not be wired into current manuscript tables, manifests, or
release gates.
