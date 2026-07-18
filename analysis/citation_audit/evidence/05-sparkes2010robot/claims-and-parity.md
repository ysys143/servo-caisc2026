# Robot Scientist: Claim and Bilingual-Parity Evidence

## Assignment Boundary

- Active source: `robot_scientist` / `sparkes2010robot`
- Citation key: `sparkes2010robot`
- PDF: `~/Documents/GitHub/ai_scientist/1_AI_Scientist_Core/Reference/Sparkes 2010 - Towards Robot Scientists for Autonomous Scientific Discovery.pdf`
- PDF SHA-256: `0838ce55a216d3b5ba46b3bedb5e85194ed056dc98e5909630264f63066692cd`
- PDF pages: 11
- Bibliographic identity: Andrew Sparkes et al., *Towards Robot Scientists for autonomous scientific discovery*, *Automated Experimentation* 2:1 (2010), DOI `10.1186/1759-4499-2-1`
- Version status: `exact`
- API/model calls: none

The PDF title, authors, venue, year, DOI, page count, and hash agree with the
frozen inventory and bibliography. This is a review and system-description
article. It summarizes Adam's reported results and cites the primary Nature
2004 and Science 2009 papers; it does not itself report an active-learning
selection rule, and the cited primary papers were outside this lane. No other
source PDF was opened for this lane.

## Full-Text and Visual Coverage

I read PDF pages 1-11 in order:

- pp. 1-2: abstract, automation history, prior discovery systems, formal
  recording, closed-loop learning, and the Robot Scientist concept;
- pp. 3-6: Adam's yeast-functional-genomics problem, logical hypotheses,
  assay design, robotic execution, analysis, results, and formalization;
- pp. 6-8: Eve's planned drug-screening workflow, hardware, software, and
  future work;
- pp. 8-9: discussion, human dependence, model and measurement failure modes,
  costs, and conclusion;
- pp. 9-11: appendix notes, author contributions, acknowledgements, and all
  references.

I rendered and visually inspected PDF pp. 3-8, covering every figure in the
paper. Figure 1 (p. 3) depicts the actual closed loop: system model and
knowledge base, hypothesis generation, experiment generation and design,
robotic execution, observation collection, statistical/machine-learning
analysis, new knowledge, and model update. Figures 2-3 (pp. 4-5) show Adam's
physical system and instrument layout. Figures 4-5 (pp. 7-8) show Eve's
physical system and layout. The paper contains no table and no Bayesian/EIG
equation. Its displayed logical predicates on p. 3 encode gene-enzyme and
metabolite-growth hypotheses, not an experiment-selection objective.

## Source-Grounded Mechanism and Evidentiary Boundary

### What the source directly supports

- Adam is an autonomous physical laboratory prototype for yeast functional
  genomics, especially identifying genes for locally orphan enzymes (pp. 3-5).
- It forms abductive candidate gene-enzyme hypotheses from a logical yeast
  metabolism model, KEGG, and sequence-similarity searches (pp. 3-5).
- Its experiment-design code constructs two-factor assays comparing deletant
  and wild-type strains with and without metabolites. It uses Latin-square
  microplate layouts to improve detection of small differences above noise
  (pp. 3-5).
- The robotic system physically executes these assays and measures optical
  density at 595 nm as a proxy for cellular growth (p. 4).
- Curve fitting and smoothing extract growth parameters; random forests over
  replicated experiments produce statistically significant results used to
  confirm or refute hypotheses and update the metabolism model (pp. 4-5).
- Adam generated 20 hypotheses for 13 orphan enzymes and experimentally
  confirmed 12 with high confidence. Conventional manual experiments checked
  3 conclusions, and literature searches supported 6 more (pp. 5-6).
- The paper reports one incorrect conclusion caused by an incomplete system
  model that omitted kinase regulation (p. 6). It also notes manual correction
  of model conflicts before automated hypothesis generation and several
  laboratory faults that humans handled more readily (p. 9).
- A relational database stores data and metadata, while accepted knowledge can
  update the logical domain model (pp. 4-6). This supports a SERVO
  interpretation of episodic and semantic memory, with qualifications.
- Eve is described as commissioned hardware whose software and biological
  assays were still under development. Its iterative QSAR-guided targeted
  screening is prospective in this source, not a completed empirical result
  (pp. 6-8).

### What the source does not support

The PDF contains no occurrence of `active learning` or `active-learning` and
does not define a policy that maximizes posterior entropy reduction, expected
information gain, or any Bayesian objective. It gives no prior, posterior,
entropy, EIG, utility equation, or optimization proof. It also gives no
criterion that weighs expected information against experimental cost. The
cost discussion on p. 9 concerns whether the robot platform is cost-effective
relative to human labor; it is not an experiment-selection reward.

Accordingly, this source supports neither a Bayesian-optimal/EIG policy nor an
explicit heuristic active-learning criterion. The strongest source-grounded
description is `model-driven closed-loop hypothesis generation and fixed
assay design`. Calling it an active-learning approximation is an external
retrospective interpretation. If the intended evidence is the selection
mechanism in King et al. (2004), that primary source must be cited and audited
separately. Even then, `heuristic active learning` must not be upgraded to
`Bayesian-optimal` or `EIG-maximizing` without direct objective-level evidence.

The source also does not treat its statistical test as a novelty measure.
Statistics evaluate whether growth observations confirm a biological
hypothesis. Novelty is instead a broader scientific judgment: the discussion
acknowledges that the AI did not meet human expectations for innovative
thought (p. 9), and the reported conclusions received limited manual and
literature follow-up (pp. 5-6). Thus `Stat. test` in the manuscript table is a
validation mechanism, not a source-supported novelty metric.

## Occurrence Assessments

### EN-C011:sparkes2010robot

- Manuscript line/section: `submission/main.tex:85`, Background.
- Claim as applied to this source: Robot Scientist experiment selection is a
  domain-specific active-learning approximation in the paragraph immediately
  following the manuscript's EIG equation.
- Citation role: `example` with an interpretive decision-theoretic bridge.
- Source evidence: the review documents abductive hypothesis generation,
  two-factor assay design, Latin-square layouts, physical execution, replicated
  statistical analysis, and model update (pp. 3-5). It says Adam tested all 20
  generated hypotheses (p. 5). It does not describe active learning, candidate
  ranking by informativeness, Bayesian updating, EIG, or a cost-information
  objective.
- Entailment: `MISATTRIBUTED`.
- Severity: `major`.
- Source-vs-SERVO reasoning: `closed-loop experiment design` is a direct source
  fact. `Active-learning approximation` is the manuscript's interpretation,
  and the placement after the EIG equation invites a stronger EIG analogy that
  this source cannot support. The paper's reference [23] identifies the 2004
  Robot Scientist paper but does not reproduce its selection rule.
- Proposed correction: "Domain-specific systems already use model-driven
  closed-loop experiment design, as illustrated by Robot Scientist." If an
  active-learning claim is essential, cite and audit the primary source for
  that policy and state its actual heuristic objective without implying EIG.
- Korean parity: `omitted`. The Korean manuscript has no counterpart to this
  Background occurrence, although active-learning claims recur later in both
  languages.

### EN-C016:sparkes2010robot

- Manuscript line/section: `submission/main.tex:92`, Related Work.
- Claim as applied to this source: Robot Scientist integrated hypothesis
  generation, robotic experimentation, and statistical validation in yeast
  functional genomics; in SERVO terms it instantiated all six components,
  including an active-learning policy, in a physical wet lab more than a decade
  before LLM systems.
- Citation role: `direct` for the system facts and `interpretive` for the SERVO
  mapping.
- Source evidence: pp. 3-5 directly support the yeast domain, abductive
  hypotheses, physical assays, statistical analysis, database/model memory,
  and iterative model update. Publication in 2010 and Adam's earlier operation
  support the pre-LLM chronology. No page documents an active-learning policy.
- Entailment: `PARTIAL`.
- Severity: `major`.
- Source-vs-SERVO reasoning: The integrated physical loop is accurately
  attributed. Mapping the source into `S/G/E/V/M/pi` can be a defensible SERVO
  interpretation if labeled as such: candidates form `S`; abduction and
  bioinformatics form `G`; robotics form `E`; statistical analysis forms `V`;
  database plus metabolism model form `M`; and assay design supplies a limited
  `pi`. But the source's `pi` is model-driven assay construction, not a
  documented active-learning or EIG policy. "All six" is therefore a framework
  coding, not the source authors' claim, and its active-learning qualifier is
  unsupported by this citation.
- Proposed correction: "Robot Scientist integrated model-based hypothesis
  generation, robotic experimentation, statistical hypothesis assessment, and
  model update in yeast functional genomics. In our SERVO mapping it supplies
  all six slots in physical wet-lab form, but this review documents
  model-driven assay design rather than an explicit EIG policy."
- Korean parity: `equivalent` to `KO-C011`; both versions retain the same valid
  integrated-loop claim and the same unsupported active-learning clause.

### EN-C021:sparkes2010robot

- Manuscript line/section: `submission/main.tex:94`, Related Work.
- Claim as applied to this source: Bayesian-optimal experiment selection has a
  long history in automated science, most directly in Robot Scientist's
  active-learning policy.
- Citation role: `joint` and `interpretive`. The adjacent POMDP/BED sources
  ground the general theory; Sparkes is asked to ground the Robot Scientist
  example.
- Joint-only support: `yes` for the broad history sentence, but no combination
  with the BED citations can make Sparkes evidence for a Bayesian/EIG objective
  it never states.
- Source evidence: pp. 3-5 provide fixed domain-specific hypothesis and assay
  design; p. 5 reports that all 20 hypotheses were tested. The complete PDF has
  no Bayesian, posterior, entropy, information-gain, or active-learning policy.
- Entailment: `MISATTRIBUTED`.
- Severity: `major`.
- Source-vs-SERVO reasoning: The manuscript collapses three distinct levels:
  closed-loop experimental choice, heuristic active learning, and normative
  Bayesian-optimal/EIG selection. This review establishes only the first. Its
  citations to earlier Robot Scientist work cannot substitute for citing the
  primary mechanism, and a heuristic rule would still not establish Bayesian
  optimality.
- Proposed correction: "Decision-theoretic experiment selection has a long
  history in automated science. Robot Scientist provides an early example of
  model-driven closed-loop experiment design; this review does not establish
  that its policy is Bayesian-optimal or EIG-maximizing." Add a separately
  audited primary citation for any stronger active-learning claim.
- Korean parity: `equivalent` to `KO-C016`; both make the same unsupported
  Bayesian-optimal/active-learning attribution.

### EN-C024:sparkes2010robot

- Manuscript line/section: `submission/main.tex:162`, core-systems table
  caption; the cited Robot Scientist column is at lines 152-159.
- Claim as applied to this source: Robot Scientist is a pre-LLM core system and
  is coded as novelty measure `Stat. test`, wet-lab closed loop, policy type
  `Active learn.`, validator completeness `V_e`, memory `M_e+M_s`, and low human
  involvement.
- Citation role: `joint` in the caption and `interpretive` for the Robot
  Scientist SERVO column.
- Joint-only support: `no` for the Robot Scientist column, which must stand on
  this source independently; `yes` only for the caption's cross-system
  comparison with NovelSeek.
- Source evidence: pre-LLM status and wet-lab closure are direct (pp. 1-5).
  Empirical validation, relational records, and model update support `V_e` and
  `M_e+M_s` as qualified framework mappings (pp. 4-6). Adam was intended to
  require human input mainly for stocks and consumables (p. 4), but humans also
  performed manual verification, corrected model conflicts, and handled some
  physical failures (pp. 5, 9). No active-learning policy appears. Statistical
  analysis confirms or refutes gene-function hypotheses; it does not measure
  novelty (pp. 4-5, 9).
- Entailment: `PARTIAL`.
- Severity: `major`.
- Source-vs-SERVO reasoning: The caption's literal identification of a pre-LLM
  Robot Scientist is supported. The table mixes direct facts with SERVO coding.
  `Yes (wet-lab)` is supported. `V_e`, `M_e+M_s`, and `Low` are plausible only
  as explicitly labeled interpretations with the above caveats. `Stat. test`
  under novelty is a category error, and `Active learn.` is not supported by
  this source. The paper's one wrong conclusion due to an incomplete model
  also prevents treating empirical validation as automatically calibrated.
- Proposed correction: change the Robot Scientist cells to `Novelty: not
  independently automated / statistical hypothesis test only` and `pi:
  model-driven assay design`. Retain `wet-lab`, `V_e`, `M_e+M_s`, and `Low` only
  with a table note that these are SERVO interpretations and that human model
  maintenance and follow-up verification remained material.
- Korean parity: `equivalent` to `KO-C023` for every Robot Scientist cell. The
  English caption's additional Nature-2026 note has no bearing on this source.

### KO-C011:sparkes2010robot

- Manuscript line/section: `submission/main_ko.tex:111`, Related Work.
- Claim as applied to this source: the Korean counterpart of `EN-C016`, stating
  that Robot Scientist integrated hypothesis generation, robot experiments,
  and statistical validation and instantiated all six SERVO elements,
  including an active-learning policy, in a physical wet lab.
- Citation role: `direct` plus `interpretive`.
- Source evidence: integrated loop on pp. 3-5; database/model memory on pp. 4-6;
  no active-learning or EIG policy anywhere in pp. 1-11.
- Entailment: `PARTIAL`.
- Severity: `major`.
- Source-vs-SERVO reasoning: `능동학습 정책 포함` is not softened relative to
  English and remains unsupported. The six-component mapping must be attributed
  to the present manuscript, while the physical loop can be attributed to
  Sparkes et al.
- Proposed correction: mirror the corrected English wording and replace
  `능동학습 정책` with `모델 기반 실험 설계 메커니즘`; state that the six-slot
  classification is this paper's SERVO mapping.
- Korean parity: `equivalent` to `EN-C016`.

### KO-C016:sparkes2010robot

- Manuscript line/section: `submission/main_ko.tex:113`, Related Work.
- Claim as applied to this source: the Korean counterpart of `EN-C021`, calling
  Robot Scientist's active-learning policy the most direct early example of
  Bayesian-optimal experiment selection.
- Citation role: `joint` and `interpretive`.
- Joint-only support: `yes` only for the general BED history; Sparkes does not
  supply the missing objective-level evidence.
- Source evidence: model-driven two-factor and Latin-square assay design on
  pp. 3-5; no Bayesian, EIG, posterior, entropy, or explicit active-learning
  criterion on any page.
- Entailment: `MISATTRIBUTED`.
- Severity: `major`.
- Source-vs-SERVO reasoning: `베이즈 최적` is stronger than the source, and
  `능동학습 정책` is itself absent from this PDF. The Korean sentence reproduces
  rather than repairs the English conceptual collapse.
- Proposed correction: describe this source as early model-driven closed-loop
  experiment design. Reserve `베이즈 최적` or `EIG 최대화` for a source that
  explicitly defines and evaluates that objective.
- Korean parity: `equivalent` to `EN-C021`.

### KO-C023:sparkes2010robot

- Manuscript line/section: `submission/main_ko.tex:215`, core-systems table
  caption; Robot Scientist cells are at lines 205-212.
- Claim as applied to this source: the Korean table counterpart of `EN-C024`,
  including `통계 검정` as novelty measure and `능동학습` as policy type.
- Citation role: `joint` in the caption and `interpretive` for the table coding.
- Joint-only support: `no` for the Robot Scientist column; the NovelSeek source
  cannot repair unsupported Robot Scientist cells.
- Source evidence: the same page-grounded evidence as `EN-C024`. Wet-lab loop,
  empirical assessment, database, and model update are supported; novelty
  measurement and active learning are not.
- Entailment: `PARTIAL`.
- Severity: `major`.
- Source-vs-SERVO reasoning: `통계 검정` tests the biological claim, not
  scientific novelty. `능동학습` lacks support in this review. The other cells
  are framework interpretations and require notes about model error, human
  maintenance, and partial manual follow-up.
- Proposed correction: use `신규성: 자동 측정 없음(통계적 가설 검증만)` and
  `pi 유형: 모델 기반 실험 설계`, with a note separating source facts from SERVO
  coding.
- Korean parity: `equivalent` to `EN-C024` for the source-specific content.

## Bilingual Reconciliation

| English occurrence | Korean occurrence | Parity | Result |
|---|---|---|---|
| `EN-C011` | none | `omitted` | The English-only Background sentence introduces the active-learning approximation immediately after EIG. Korean omits this occurrence, but not the later active-learning claims. |
| `EN-C016` | `KO-C011` | `equivalent` | Both support the physical closed loop but over-attribute an active-learning policy and fail to label the six-slot mapping as SERVO interpretation. |
| `EN-C021` | `KO-C016` | `equivalent` | Both incorrectly use this source as direct evidence for Bayesian-optimal/active-learning experiment selection. |
| `EN-C024` | `KO-C023` | `equivalent` | Both table columns misclassify statistical hypothesis testing as novelty measurement and code the policy as active learning without source support. |

There is no translation-only correction. Korean removes one English
occurrence, but its three retained Robot Scientist occurrences preserve the
same substantive problems.

## Lane Verdict

Overall verdict for the seven occurrences: `major_revision`.

Sparkes et al. is strong direct evidence for a pre-LLM physical closed loop in
yeast functional genomics: logical hypothesis generation, model-driven assay
design, robotic wet-lab execution, statistical/ML hypothesis assessment,
structured records, and model update. It is not evidence for a
Bayesian-optimal or EIG-maximizing policy. More strictly, this PDF does not
even specify an active-learning selection criterion; it documents fixed
domain-specific assay design and reports that Adam tested all 20 generated
hypotheses. The manuscript must either narrow its wording to that mechanism or
cite and audit the primary active-learning source. It must also separate
statistical hypothesis validation from scientific novelty assessment in both
table versions.

EVIDENCE_COMPLETE: yes
