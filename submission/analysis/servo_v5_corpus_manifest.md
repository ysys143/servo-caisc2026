# SERVO v5 corpus acquisition manifest

SERVO v5 codes six AI-scientist systems (C01-C06) against source propositions
extracted from six published PDFs. Those PDFs are third-party copyrighted
works and are **not redistributed** in this package. This manifest lists,
for each case, the exact file Servo is frozen against, its SHA-256, and a
public pointer to acquire it.

A reproducer must:

1. Obtain each PDF from its acquisition pointer below.
2. Compute its SHA-256 (`shasum -a 256 <file>` or `sha256sum <file>`) and
   confirm it matches the value below.
3. Only then run the source-fidelity tests (quote, locator, and hash
   verification) described in [`README.md`](./README.md) — without a
   byte-matching PDF, those tests skip rather than fail, so a green run does
   not by itself confirm source fidelity.

The SHA-256 values here are copied verbatim from
[`servo_v5_source_freeze_manifest.json`](./servo_v5_source_freeze_manifest.json),
the authoritative per-case freeze record; `servo_v5_corpus_manifest.json` in
this directory mirrors this table in machine-readable form.

## Per-case manifest

| Case | Citation | Title | Expected filename | SHA-256 | Acquire |
|---|---|---|---|---|---|
| C01 | `boiko2023emergent` | Autonomous chemical research with large language models | `Boiko 2023 - Autonomous Chemical Research with LLMs.pdf` | `15b340a6fd3cb70ae7f44a96264c051662e4dfd26075604c0c8e94c7c85c959f` | DOI [10.1038/s41586-023-06792-0](https://doi.org/10.1038/s41586-023-06792-0) (Nature 624, 570-578, 2023) |
| C02 | `lu2024aiscientist` | The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery | `The AI Scientist_ Towards Fully Automated Open-Ended Scientific Discovery.pdf` | `00fc4a18db7b314b5def5d9236c6af6cb9325605dcb4827cc82b0f8a462356fe` | arXiv [2408.06292](https://arxiv.org/abs/2408.06292) (2024) |
| C03 | `lu2026aiscientist` | Towards end-to-end automation of AI research | `Towards end-to-end automation of AI research.pdf` | `a75e0d93447f400179136bf18d909df29e0c8ccaeba076a1dfb1beeef0e0e10d` | DOI [10.1038/s41586-026-10265-5](https://doi.org/10.1038/s41586-026-10265-5) (Nature 651, 914-919, 2026) |
| C04 | `schmidgall2025agentlab` | Agent Laboratory: Using LLM Agents as Research Assistants | `Agent Laboratory - Using LLM Agents as Research Assistants.pdf` | `67b9543ae1d8e3ad86a65e2a436ddbd12700d7c8f4a66c5b4c2a6fccc1674d75` | arXiv [2501.04227](https://arxiv.org/abs/2501.04227) (2025) |
| C05 | `sparkes2010robot` | Towards Robot Scientists for autonomous scientific discovery | `Sparkes 2010 - Towards Robot Scientists for Autonomous Scientific Discovery.pdf` | `0838ce55a216d3b5ba46b3bedb5e85194ed056dc98e5909630264f63066692cd` | DOI [10.1186/1759-4499-2-1](https://doi.org/10.1186/1759-4499-2-1) (Automated Experimentation 2(1):1, 2010, open access) |
| C06 | `zhang2025novelseek` | InternAgent: When Agent Becomes the Scientist -- Building a Closed-Loop System from Hypothesis to Verification | `NovelSeek - When Agent Becomes the Scientist.pdf` | `71619a734da64e3b84735fc18417316254fd08c0abeafaf9d8faa08abdd48843` | arXiv [2505.16938](https://arxiv.org/abs/2505.16938) (v3, 2025) |

Notes:

- **C05** is frozen against a single PDF — the Sparkes et al. (2010) review.
  The manuscript separately cites `king2004robot` as related background on
  the same Robot Scientist / Adam lineage, but no second PDF is bound to C05
  in `servo_v5_source_freeze_manifest.json`.
- **C06** circulated as "NovelSeek" in earlier preprint versions; the local
  filename and the `system` label in `servo2_cases.csv` retain that name for
  continuity with prior citations of this work. The current arXiv record is
  titled "InternAgent."
- Filenames are exactly what `servo_v5_source_propositions/C0N.json` records
  in `source_pdf_name` and what the test harness (see
  `analysis/tests/servo_v5/test_verify_contract.py`) expects under a sibling
  corpus directory named `ai_scientist/` (not part of this repository).

## Provenance of the hashes

Every SHA-256 in this table was cross-checked byte-for-byte against two
independent records in this package before publication:
`servo_v5_source_freeze_manifest.json` (`cases.<CASE>.source_pdf_sha256`) and
`servo_v5_source_propositions/<CASE>.json` (`source_pdf_sha256`). Both must
agree; a mismatch between either of them and a locally acquired PDF means the
PDF is the wrong edition/version and should not be used for source-fidelity
verification.
