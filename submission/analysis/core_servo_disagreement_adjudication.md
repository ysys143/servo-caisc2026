# Core-case channel adjudication

This note records the author's development-era adjudication for the six core Servo cases. It does not convert the 90 token-level mismatches in the frozen R24 run into a semantic error rate. Those diagnostics cannot determine which facets belong to one event channel. The current substantive representation is `servo_validator_channels.csv`; `core_servo_channels.csv` is a generated compatibility projection. Quotes and source hashes resolve in `core_servo_evidence_ledger.json`.

## R01 Coscientist

- The protocol-correction channel is operational because execution feedback changes a later procedure (`R01-E07`, `R01-E11`).
- The natural-language labeling or interpretation channel is terminal assessment, not the mechanism that closes the execution loop (`R01-E06`).
- Any stronger claim that reactive replanning is itself a calibrated gate remains unsupported; the policy interpretation is structurally inferred from the reported feedback path.

## R02 AI Scientist 2024

- The prior-art checker is an ideation-stage novelty filter (`R02-E07`); its novelty discrimination is not independently validated.
- Execution status and metrics return to the coding agent and can trigger replanning, which establishes computational closure (`R02-E11`, `R02-E12`).
- The simulated paper reviewer is a separate terminal assessment (`R02-E06`, `R02-E15`). Reviewer accuracy does not measure the reliability of the earlier novelty filter.
- Archive admission or external submission is not treated as an automatically controlled operational gate unless the source reports that control path.

## R03 AI Scientist 2026

- The common idea-generation phase filters ideas through Semantic Scholar and can discard close prior-art matches; later template-free prompts also use literature-grounded reflection. The canonical ledger records both functions in the pre-action prior-art channel (`R03-E01`, `R03-E13`).
- Stage evaluators, metric/training feedback, plot critique, and best-first node evaluation affect tree expansion or stage transition and are operational channels (`R03-E08`, `R03-E10`, `R03-E11`, `R03-E12`).
- The paper reviewer is terminal assessment (`R03-E06`, `R03-E13`), and workshop review follows manual submission selection outside the search loop (`R03-E14`). Neither channel establishes reliability of the internal operational evaluators.

## R04 Agent Laboratory

- Execution metrics and the reported revision dialogue supply internal computational feedback (`R04-E07`, `R04-E11`).
- Humans supply the initial research direction and retain consequential research authority (`R04-E12`). Pipeline completion is therefore not equated with fully autonomous trustworthy closure.
- The LLM paper-quality score is terminal assessment with documented mean overestimation, not calibration of the internal revision channel (`R04-E06`).

## R05 Robot Scientist

- Physical assays and statistical hypothesis testing feed the model and experiment-selection cycle, establishing a directly reported operational wet-lab loop (`R05-E06`, `R05-E07`, `R05-E10`).
- No separate terminal paper-quality or novelty assessor is identified in the coded source. The system is a negative case against claims that Servo always reveals a previously hidden loop distinction: here the source architecture already exposes the central feedback cycle.
- Human provision of consumables does not by itself negate computational closure, but it marks a physical-resource authority boundary (`R05-E13`).

## R14 NovelSeek / InternAgent

- Idea assessment, debugging, human feedback, and adaptive evolution are kept as distinct channels because they change different later actions (`R14-E06`, `R14-E07`, `R14-E11`, `R14-E12`).
- Reported idea scoring is not treated as independently validated novelty or significance discrimination.
- The Servo system tuple makes this system comparable with the other cases but compresses agent-to-agent communication. NovelSeek's native multi-agent description remains more informative for internal role organization.

## Evidential rule

`directly_stated` means that the source explicitly reports the component, assessment, or feedback transition. `structurally_inferred` means that the classification follows from an explicitly reported sequence but the Servo label is editorial. `unclear` or `not_reported` is retained when the source does not identify the channel or authority. These statuses are not confidence scores and are not collapsed by coder majority vote.

A channel is split when the bounded source packet reports a distinct evaluator,
target property, decision role, or downstream destination. Channels are merged
only when the same reported mechanism supplies those roles. `None identified`
means that no separate terminal or external channel was found in the bounded
packet; it is not evidence that such a mechanism is absent from the wider
system. These decisions have not been independently reproduced.
