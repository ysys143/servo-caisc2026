# Full-Text Citation Audit Rubric

## Unit of Work

One cited source is active at a time. A source is complete only after its full
PDF and every linked English and Korean manuscript occurrence have been
reviewed. Completion describes audit coverage, not citation correctness.

Codex agents perform all reading and semantic judgment. Automation is limited
to inventory, identity, hash, page-range, required-field, citation-link, and
state-consistency checks; it must not generate or infer a verdict.

## Source Identity Gate

Record all of the following before reading:

- citation key and bibliography metadata;
- absolute PDF path, SHA-256, and `pdfinfo` page count;
- title, authors, year, DOI, arXiv identifier, or other stable identifier from
  the PDF itself;
- version status: `exact`, `same_work_preprint`, or `mismatch`;
- evidence that a permitted preprint is the same work.

`mismatch`, a corrupt/partial PDF, or unavailable material required to evaluate
the manuscript claim blocks completion.

## Full-Text Coverage Gate

- Traverse all PDF pages in order, including appendices and references.
- Read substantive sections closely; inspect bibliography/index pages for
  completeness and contextual dependencies.
- Use layout-preserving text extraction for navigation and notes.
- Render and visually inspect pages containing relevant figures, tables,
  equations, extraction failures, or ambiguous layout.
- Record the covered PDF-page range. When printed and PDF page numbers differ,
  cite both where possible.

## Required Source Analysis

Every report must explain:

1. research problem and motivating concern;
2. historical and disciplinary context;
3. relationship to prior work;
4. document structure and argument flow;
5. methods, data, experiments, and assumptions;
6. principal findings and quantitative results;
7. limitations, threats to validity, and intended scope;
8. implications relevant to SERVO, separated from the source authors' claims.

## Citation-Link Analysis

For every manifest link associated with the source, record:

- occurrence ID, source line, section, and manuscript sentence/claim;
- citation role: `direct`, `background`, `example`, `interpretive`, or `joint`;
- evidence location in the PDF and a short supporting excerpt or precise
  paraphrase;
- entailment verdict and severity;
- reasoning about scope, context, attribution, and wording strength;
- a proposed correction when the verdict is not fully supported;
- Korean parity: `equivalent`, `omitted`, `added`, or `meaning_shifted`.

## Verdicts

| Verdict | Meaning |
|---|---|
| `SUPPORTED` | The source directly and accurately supports the claim. |
| `SUPPORTED_WITH_QUALIFICATION` | Correct only with an explicit limitation. |
| `PARTIAL` | The source supports only part of the cited claim. |
| `UNSUPPORTED` | The cited source does not establish the claim. |
| `CONTRADICTED` | The source conflicts with the manuscript claim. |
| `MISATTRIBUTED` | The claim belongs to another source or is attributed incorrectly. |
| `NOT_ASSESSABLE` | This source cannot establish the claim type or required evidence. |

Severity is `none`, `minor`, `major`, or `critical`.

## Claim-Type Checks

- Quantitative claims require exact values, denominator/sample, metric, and
  experimental condition.
- Causal wording requires causal evidence, not association or author opinion.
- Priority wording requires explicit priority evidence and appropriate scope.
- Universal or absence claims cannot be supported merely because one source is
  silent; classify the manuscript's synthesis separately.
- Framework mappings are judged as faithful interpretations, not quotations.
- In a multi-key citation, assess each source independently and mark
  `joint-only` when the full claim requires combined support.

## Required Report Headings

1. `Source Identity`
2. `Full-Text Coverage`
3. `Problem and Context`
4. `Structure and Argument`
5. `Methods and Evidence`
6. `Findings`
7. `Limitations`
8. `Citation Assessments`
9. `Korean Parity`
10. `Overall Verdict`
11. `Completion Checklist`

Each report ends with machine-readable markers:

```text
AUDIT_COMPLETE: yes
PAGES_COVERED: 1-N
EN_LINKS_COVERED: comma-separated occurrence IDs or none
KO_LINKS_COVERED: comma-separated occurrence IDs or none
VERDICT: clean | minor_revision | major_revision | citation_invalid
```

## Final Closure

After all individual reports pass, reconcile every multi-source citation and
every English/Korean occurrence mapping. Final completion requires no pending,
active, or blocked source; no unaccounted citation link; no report placeholder;
and no manuscript/PDF drift that has not been re-audited.
