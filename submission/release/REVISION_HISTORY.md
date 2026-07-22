# Post-submission revision history

This repository record preserves the detailed chronological revision log removed from the reader-facing manuscript. Internal R-numbers are archival process identifiers, not scientific concepts or reader-facing schema terms. The normative current state is the checksum-bound release and its canonical records.

Current-state note: Schema 4.1 supersedes the historical occurrence-token and artifact-production descriptions below. Event identity is occurrence identity, artifact versions are lineage-local, and an established artifact revision requires a distinct `W_A` production event. The earlier C01 experimental-adaptation recoding recorded as R68 is withdrawn because the bounded source does not directly link reuse evidence to a distinct later evidence-generating execution. C05 experimental adaptation and discovery-cycle feedback are likewise `unknown`: a source-described repeatable architecture does not establish a distinct post-update execution and evidence occurrence. Graph transitions are endpoint-level dependency/control constraints, not typed function composition, and the human-authority vector is explicitly coarse. These corrections intentionally leave the chronological entries unchanged as an audit record.

```latex
\section{Post-Submission Revisions}
\label{app:postsubmit}

This manuscript continues to be refined after the CAISc~2026 submission deadline. This
appendix is the running record of every difference between it and the archival version of
record, so that the two can be reconciled entry by entry. Each entry states what changed,
why, and whether the version of record is thereby wrong or merely less precise.

\begin{description}
  \item[R1. Leiden Declaration signatory count (Section~\ref{sec:openproblems}).]
  \emph{Status in the version of record: unsupported by the source cited for it.} The version
  of record states that the Leiden Declaration was ``signed by over 130 mathematicians,''
  attributing that figure to the declaration document. The document states no signatory count
  at all: its only numerals are section numbers and the year of the meeting that produced it.
  The count is maintained on the separate signature site, which recorded 3{,}071 signatories
  when checked on 20~July~2026. The defect is therefore not that the figure was understated
  but that it was attributed to a text that does not contain it. This revision cites the
  signature site for the count, marks it as of a date because it grows over time, and notes
  that the declaration itself gives none. The substantive claim the sentence supports---that
  AI-produced proofs may carry errors that resist detection without expert scrutiny---is
  stated in the declaration and is unaffected.

  \item[R2. Formal validators and RL stability (Section~\ref{sec:domains}).]
  \emph{Status in the version of record: overclaim; the sentence asserts more than the
  evidence supports.} The version of record states that formal mathematics has ``a binary
  $V_\text{formal}$ that makes RL stable and the loop fully closed.'' A deterministic
  pass/fail oracle settles whether a candidate proof or program is acceptable, but the
  stability of policy learning also depends on reward density, the state space, the policy
  update rule, the exploration strategy, and function approximation; the surveyed formal
  systems do not isolate the validator as the cause of stable training (DeepSeek-Prover-V1.5
  additionally uses supervised fine-tuning and an MCTS variant with intrinsic rewards, and
  FunSearch couples the evaluator to an LLM and an evolutionary procedure). The clause is
  replaced here with ``enables mechanically closed evaluation within the formalized task,''
  matching the wording already used for the same systems in
  Appendix~\ref{app:domains}. No other claim depends on the removed clause.

  \item[R3. Scoring of novelty, significance and correctness (Section~\ref{sec:openproblems}).]
  \emph{Status in the version of record: contradicted by the cited source.} The version of
  record cited ``The AI Scientist's 1--10 score'' as an instance of collapsing the three
  properties into one scalar. The cited system in fact rates ideas on \emph{separate}
  interestingness, feasibility and novelty scales, and its reviewer emits several axes; the
  collapse occurs not in scoring but at the accept/reject decision, which thresholds a single
  aggregate. The sentence now locates the collapse where it happens. The open problem is
  unchanged.

  \item[R4. ``Greedy'' as a coding, not a source claim (Section~\ref{sec:openproblems}).]
  \emph{Status in the version of record: unsupported interpretation.} The cited source
  describes archive-conditioned idea generation but defines no argmax, best-score or greedy
  selection rule; ``greedy'' is this paper's own coding. The sentence now says so.

  \item[R5. Two different quantities compared (Section~\ref{sec:core}).]
  \emph{Status in the version of record: contradicted in metric meaning.} The version of
  record read ``balanced accuracy 0.65 vs.\ human 0.66,'' which invites reading 0.65 as
  agreement with human reviewers. It is the balanced accuracy of predicting ICLR~2022
  accept/reject labels; 0.66 is human inter-reviewer consistency measured on a different
  pool. The two are now distinguished.

  \item[R6. Class definition and Agent Laboratory (Introduction).]
  \emph{Status in the version of record: contradicted by the cited source.} The opening
  sentence defines the class as agents that \emph{independently} generate hypotheses and
  cited Agent Laboratory among them; in that system the research idea is supplied by a human.
  The citation has been removed from the class-defining list. Agent Laboratory remains
  analysed throughout the paper.

  \item[R7. Robot Scientist table cells (Table~\ref{tab:core-comparison}).]
  \emph{Status in the version of record: one unsupported, one mislabelled.} The novelty-measure
  cell read ``Stat.\ test''; the statistical test in the cited source adjudicates growth
  phenotypes and gene-function hypotheses, not scientific novelty, so the cell now reads
  ``None (corr.).'' The policy cell ``Active learn.'' is not supported by the 2010 review used
  for that column; the caption now attributes the active-learning policy to the primary source
  that documents it.

  \item[R8. What ``calibration'' denotes (Section~\ref{sec:framework}).]
  \emph{Status in the version of record: a term used in a weaker sense than the word normally
  carries, without saying so.} The version of record calls a validator ``uncalibrated'' on the
  strength of discrimination statistics. Calibration and discrimination are independent
  properties: balanced accuracy, F1 and AUC measure how well a scorer separates classes, while
  calibration---whether stated confidence matches empirical frequency---is measured by
  reliability curves, expected calibration error or Brier score. No surveyed source reports the
  latter, so neither ``calibrated'' nor ``uncalibrated'' is established in the strong sense.
  The paper's own coding protocol already defines the field operationally as \emph{not
  systematically biased} rather than as probabilistically calibrated. This revision states that
  definition in the body where the term is first made operative. The construct, its coding, and
  the reported inter-coder agreement are unchanged; only the term's scope is now explicit.

  \item[R9. The automated reviewer is not a gate (Section~\ref{sec:core}).]
  \emph{Status in the version of record: contradicted by the cited source.} The version of
  record described the automated reviewer as the system's ``internal acceptance gate.'' In the
  cited source the reviewer scores finished manuscripts and configurations; what advances the
  search is a stage evaluator, a best-first policy and a compute budget, and the manuscripts
  sent for external review were chosen by hand. The reviewer is an evaluation instrument, not
  a gate. The sentence now says so, and the acceptance bias it does exhibit is stated with the
  figure that supports it (false-positive rate 0.45 against 0.17 for human reviewers).

  \item[R10. Coding corrections and their effect on reported agreement (Appendix~\ref{app:coding}).]
  \emph{Status in the version of record: reference labels contained demonstrable errors, and one
  reported statistic depended on them.} An audit of the released coding sheet against the
  paper's own protocol found eleven cells that the protocol, the primary sources, or the
  manuscript itself contradict. \texttt{Vsyntax} was coded 0 for every system, including five
  that execute code, against a rubric whose example of the field is ``code compiles/executes'';
  the blind coders assigned 1 unanimously on four of them. \texttt{Vhuman} was coded 1 for
  AI~Scientist (Nature~2026) on the strength of an external post-hoc workshop review, which the
  protocol's ``required for the validity/novelty signal'' test does not cover, and 0 for Agent
  Laboratory, contradicting this paper's own table, which records that system's novelty measure
  as human-delegated. \texttt{Vcompleteness} was 3 for AI~Scientist (Nature~2026), a value the
  scale licenses only when the top automated layer is calibrated; that flag had been corrected
  to 0 earlier without propagating to the ordinal. The remaining ordinals were re-derived from
  the scale anchor after the \texttt{Vsyntax} correction rather than copied from the coders;
  that derivation independently reproduces the coder consensus in every case.
  \emph{Effect on reported statistics:} the Fleiss agreements among the three blind coders,
  which are the figures this paper quotes, are identical before and after the correction, as
  are the pairwise coder agreements. What moves is agreement between the coders and the
  author's reference labels---necessarily, because those labels were revised. The released
  reliability report now states both the original and the corrected values and warns that the
  rise is an artefact of the revision rather than evidence of reliability.

  \item[R11. InternAgent / InternAgent citation identity (Table~\ref{tab:core-comparison}).]
  \emph{Status in the version of record: bibliographic entry does not match the work as it
  now stands.} The entry keyed \texttt{zhang2025novelseek} gave the title and individual
  author list under which arXiv:2505.16938 first circulated. Later versions of the same
  preprint (v3, the one audited here) retitle the work \emph{InternAgent} and place it
  under a laboratory team byline. The citation is to the right work---the identifier is
  unchanged---but a reader retrieving 2505.16938 today finds a different title and author
  line than the bibliography gives. The entry now carries the current title and byline,
  records the former name, and keeps the key so that earlier citations of this work still
  resolve. The manuscript continues to call the system InternAgent, which is how it is named
  in the analysis released with this paper, and notes the retitling in the caption of
  Table~\ref{tab:core-comparison}, where the system is introduced.

  \item[R12. What the 736 GNoME matches are (Section~\ref{sec:openproblems}).]
  \emph{Status in the version of record: the phrase is the source's own, but it invites a
  reading the source does not support.} The version of record wrote that of 380{,}000
  predicted stable compounds ``only 736 have been independently experimentally realized,''
  which is verbatim from the cited abstract. The cited Methods make the mechanism explicit:
  the 736 are matches between GNoME's predicted structures and entries already present in,
  or added to, the ICSD when it was queried in January 2023, and 184 of them are new since
  the project began. They are therefore structures other groups made independently or
  concurrently, not syntheses the system prompted. Used as the numerator of a realization
  rate, the original phrasing suggests a predict-then-synthesize pipeline that did not
  operate. The sentence now states the mechanism. This strengthens rather than weakens the
  point it supports---that escalation to physical work is decided outside the system---since
  the matches were not triggered by any escalation criterion at all.

  \item[R13. Epistemic status of the formal claims (Abstract; Section~\ref{sec:framework}; Appendix~\ref{app:vformal}).]
  \emph{Status in the version of record: less precise and materially overstates the scope of
  the mathematical contribution.} The version of record presents three numbered propositions,
  a bundled assumption, and proof sketches as if they established results for a tractable AI
  Scientist loop. The paper's purpose is a diagnostic framework, however, and the cited
  statistical results do not supply a new theorem for adaptive, non-stationary, open-ended
  search. This revision replaces that theorem-and-proof posture with three explicitly bounded
  analytical observations, removes the unused theorem environments and their cross-references,
  and states in the abstract, background, checklist, conclusion, and domain discussion that the
  appendix imports standard fixed-setting distinctions rather than proving the framework. The
  six-component framework, three-way closure distinction, and provisional survey claims are
  unchanged; their evidential status is made
  explicit rather than upgraded by mathematical presentation.

  \item[R14. Posterior consistency and cumulative EIG (Appendix~\ref{app:vformal}).]
  \emph{Status in the version of record: partly incorrect.} The version of record treats
  compactness, identification, prior support, and a bespoke design-separation clause as a
  standard sufficient condition for posterior consistency under~\citet{ghosal2017fundamentals},
  without stating the Kullback--Leibler prior-mass and testing conditions used by the relevant
  classical results or proving an adaptive-design analogue. Its proof sketch also says that
  positive but summable one-step EIG leaves the posterior short of a point mass. That claim is
  false in general: for a discrete parameter with finite entropy, the conditional-information
  chain rule bounds total expected EIG by initial entropy even when the posterior concentrates.
  The revision states the fixed-i.i.d. conditions only schematically and with their scope,
  removes the unsupported adaptive conclusion, and describes Equation~\ref{eq:eid} as a
  one-step myopic criterion rather than a globally optimal scientific policy. This narrows the
  theoretical rhetoric without weakening the observation-versus-reward distinction, the
  empirical BED--practice gap, or its falsification test.

  \item[R15. Misspecified validator coupling and KL projection (Appendix~\ref{app:vformal}).]
  \emph{Status in the version of record: mathematically under-specified and broader than the
  cited result.} The version of record writes the coupled update only up to proportionality,
  invokes~\citet{berk1966} without restricting the claim to its fixed-i.i.d. misspecification
  setting, assumes a unique KL projection, and gives ``outcome dependence'' as if it were a
  sufficient drift condition. The revision defines the finite normalizer
  $Z_\theta(d)$, fixes the design and data-generating distribution, states the needed
  regularity and prior-mass qualifications, and uses the KL-minimizer set
  $\Theta^\dagger$ unless uniqueness is separately available. Drift now means that this set
  differs from the projection under the original likelihood; an additive constant cancels and
  an outcome-dependent validator need not change the target. Policy-only effects are separated
  as adaptive design selection, not attributed to Berk's theorem. The correction preserves the
  paper's diagnostic warning about coupling while withdrawing any claim that the surveyed
  systems instantiate this asymptotic result.

  \item[R16. Novelty non-identification and the human channel (Section~\ref{sec:openproblems}; Appendix~\ref{app:vformal}).]
  \emph{Status in the version of record: the non-identification premise is correct, but its
  human-only conclusion exceeds that premise.} If every observed likelihood is independent of
  an a priori independent novelty component, its posterior marginal remains the prior; those
  channels cannot identify it. What follows is the need for an additional informative channel,
  not a theorem that this channel must always be human or that human validation is
  irreplaceable in principle. The revision makes that logical boundary explicit and limits the
  empirical conclusion to the surveyed systems: their novelty and significance judgments are
  human-mediated or lack a validated automated gate. This leaves the novelty open problem and
  its falsification criterion unchanged while removing a universal impossibility claim.

  \item[R17. Table~\ref{tab:core-comparison} reconciled with the coding sheet.]
  \emph{Status in the version of record: two rows disagreed with the released coding they
  summarise.} The novelty row read ``None'' for Coscientist, where the sheet codes a human
  gate, and ``Human-deleg.'' for Agent Laboratory, where the sheet codes a biased automated
  gate---the latter also contradicting Section~\ref{sec:core}, which describes that system's
  reviewer as biased. The $H$ row rendered Coscientist's 0.75 as ``${\approx}1$'' while giving
  Agent Laboratory's 0.8 exactly, so one table rounded two neighbouring values by different
  rules. Both rows now reproduce \texttt{novelty\_gate} and \texttt{A\_H} verbatim and the row
  is renamed to name what it reports. This also settles the Robot Scientist cell left open by
  R7: the sheet codes a predefined novelty criterion, which is what the cell now reads.

  \item[R18. Residual claim boundaries and analytical premises (Sections~\ref{sec:framework} and~\ref{sec:openproblems}; Appendix~\ref{app:vformal}).]
  \emph{Status in the version of record: partly incorrect, and the R13--R16 revision remained
  incomplete.} The version of record identifies a sequential policy with a one-step EIG
  maximizer, treats validator reliability and human review too categorically, and states the
  novelty posterior-invariance argument without excluding prior coupling through other
  likelihood-relevant latent variables. The first mathematical revision narrowed these claims
  but left several stronger English sentences in place and retained the insufficient
  independence premise. This revision makes the EIG rule explicitly myopic, factorizes the
  novelty prior from every likelihood-relevant latent component, limits human mediation to a
  finding about the surveyed workflows, and recasts cross-domain validator patterns as
  provisional associations rather than necessity or causality. The Korean source is narrowed
  to the same scope. These changes repair the logical propagation of R13--R16 without changing
  the six-component framework, the three open problems, or their proposed falsification tests.

  \item[R19. Correction status and gate semantics (Abstract; Table~\ref{tab:core-comparison}; Appendix~\ref{app:coding}).]
  \emph{Status in the version of record: materially inaccurate in several claims, while the
  earlier post-submission citation and coding language remained insufficiently precise.}
  Appendix~\ref{app:postsubmit} records corrections to factual, coding, statistical, and
  mathematical statements, so readers should not be directed to the archival text alone when
  relying on a corrected claim. The notice now asks readers to pair the version-of-record
  citation with this dated correction and states that the correction should be linked from the
  official record when possible. Table~\ref{tab:core-comparison} also called a biased automated
  score a ``novelty gate'' for AI Scientist (Nature~2026), although the paper and released
  coding set \texttt{V\_gating=0}: the reviewer scores completed outputs but does not advance
  search or select external submissions. The row is therefore renamed ``Novelty assessment,''
  the non-gating status is explicit, and the caption distinguishes the legacy
  \texttt{novelty\_gate} field from operational gating. Finally, the abstract withdraws the
  claim of direction consistency: because the six-system outcome coding partly overlaps $V$,
  even the direction of association remains untested. These corrections preserve the framework
  and hypotheses while removing unsupported evidential status.

  \item[R20. Validator roles, closure scope, and novelty validation (Sections~\ref{sec:related}--\ref{sec:discussion}; Table~\ref{tab:domain-comparison}).]
  \emph{Status in the version of record: partly incorrect and conceptually under-specified.}
  Related Work described AI Scientist (Nature~2026)'s biased automated reviewer as the gating
  layer even though the system description and R19 establish that it is a non-gating assessment
  instrument. The text now treats $V_\text{gating}=0$ only as failure to establish a calibrated
  decisive gate and states that the binary field does not distinguish absence, non-gating,
  unidentified, and identified-but-uncalibrated cases. The manuscript also withdraws the proposed
  reliability partial order and any substantive use of the low-agreement holistic
  $V$-completeness ordinal, replacing it with a vector of gate identity, target property,
  bias/calibration evidence, experimental fidelity, and external independence. The introductory
  servo analogy is restricted to trustworthy acceptance feedback, and formal mathematics in
  Table~\ref{tab:domain-comparison} is described as exact and mechanically closed only for formal
  validity, not as a perfect scientific oracle or a fully closed discovery process. Finally, the
  novelty ``falsification test'' is recast as a prospective validation design requiring independent
  expert labels, human--human agreement, prior-art adjudication, separate endpoints, held-out
  evaluation, uncertainty reporting, and later priority checks. These changes preserve the
  six-component vocabulary and the open problems but remove a scalar validator hierarchy,
  overbroad closure language, and an inadequate novelty ground-truth claim.

  \item[R21. Interfaces and loop evidence (Sections~\ref{sec:framework},~\ref{sec:core}, and~\ref{sec:openproblems}).]
  \emph{Status in the version of record: partly incorrect and materially under-specified.}
  The version of record assigned both $G$ and $\pi$ the output type $h$ and then placed them in
  an operational sequence that was not a function composition. The revision makes $G$ generate
  a candidate set, makes $\pi$ select a typed action $(h,d,P)$, and states the resulting update
  loop explicitly. It also replaces unsupported decimal human-intervention scores with a
  categorical component-wise authority vector. For AI Scientist (2024), the earlier table's
  computational-closure label is retained but its rationale is corrected: the primary system
  description returns execution failures and metrics to the experiment agent for conditional
  replanning, whereas the terminal simulated reviewer is a separate assessment layer and is not
  what closes that internal loop. The table and released coding now record this internal
  empirical-feedback channel without treating the reviewer as an operational gate. The Nature
  2026 system is analyzed separately: its performance, training-dynamics, plot-quality, and
  stage-evaluator signals control best-first expansion and stage transitions, whereas its paper
  reviewer is terminal assessment; calibration of the search-controlling signals is not
  established. Finally,
  the BED criterion now admits exact, variational, ensemble, and other documented probabilistic
  surrogates, while direct Bayesian representation of natural-language hypotheses is identified
  as a stronger separate problem; the former experiment-fidelity problem is narrowed to a
  multi-fidelity integration gap in light of existing cost--information acquisition criteria.
  These corrections preserve the six-component vocabulary and the AI Scientist (2024)
  computational-loop classification, but repair the component interfaces, the evidence for that
  classification, the human-authority coding, and the claimed novelty and success criteria of two
  open problems.

  \item[R22. Validator context and scope (Sections~\ref{sec:framework} and~\ref{sec:discussion}).]
  \emph{Status in the version of record: partly incorrect and materially under-specified.}
  The version of record typed the validator as $V:o\rightarrow r$, which can represent
  observation scoring but not novelty, significance, reproducibility, or acceptance judgments
  that depend on a candidate claim, protocol, memory, external prior art, and an evaluation-time
  cutoff. The revised interface is $V:z\rightarrow r$, where $z$ exposes those contextual inputs
  and $r$ may contain separate property-specific outputs; the operational loop now constructs
  $z_t$ explicitly. The restricted $V(o)$ used in Appendix~\ref{app:vformal} is identified as a
  special fixed-context case rather than a general novelty model. The manuscript also no longer
  claims a complete POMDP grounding: it distinguishes the candidate search space $S$ from a
  POMDP world-state space $\mathcal X$, lists the kernels a full instantiation would require, and
  describes POMDP belief and policy concepts as organizing terminology because those kernels and
  a reward model are not specified here. The novelty open problem is narrowed from a performance
  conclusion to the documented absence of independently validated novelty-specific gates; paper
  quality, hallucination, correctness, and review agreement are retained only as adjacent general
  assessment failures, not novelty-discrimination measurements. Finally, cross-domain relation
  language is removed, and the multi-agent limitation now states that systems such as InternAgent
  are multi-agent but are collapsed into one system-level tuple. These changes preserve the
  component taxonomy and open research questions while correcting their formal expressiveness,
  evidential status, and abstraction boundary.

  \item[R23. Observation kernel and final coding facets (Sections~\ref{sec:framework} and~\ref{app:coding}).]
  \emph{Status in the version of record: partly incorrect and materially under-specified.}
  The version of record made $E$ a deterministic map from hypothesis and protocol to one
  observation even though its likelihood--reward distinction and BED discussion require the
  selected design to alter an observation distribution. The revised executor is the
  design-conditioned kernel $E(\mathrm{d}o\mid h,d,P,x)$, with deterministic execution as a
  Dirac special case, and the operational loop now samples from that kernel. This locates the
  observation model inside the six-component tuple without adding a seventh component and
  states explicitly that EIG and belief updates are not computable when a system does not expose
  the required probability law. The former syntax/semantic/empirical/human/formal layer labels
  also mixed target property, evidence source, evaluator substrate, decision role, and external
  independence. They are replaced in substantive analysis and Table~\ref{tab:core-comparison}
  by those separate facets; legacy layer columns remain only for audit reconstruction.
  Likewise, absence of documented bias is no longer called calibration. Gate reliability
  evidence is reported by evidence type, and probabilistic calibration is reserved for an
  evaluated confidence--outcome correspondence. Finally, all reported $\kappa$ values are
  explicitly limited to the earlier rubric: they do not validate the R20--R23 facets,
  contextual validator, human-authority vector, or diagnostic utility. A frozen-manual,
  prospective independent recoding remained future evaluation at R23 and is now reported in
  R24 without the abandoned free-form baseline comparison.
  These changes preserve the six component names while repairing the observation path,
  validator taxonomy, statistical terminology, and reproducibility claim.

  \item[R24. Frozen faceted recoding audit (Limitations and Appendix~\ref{app:coding}).]
  \emph{Status in the version of record: materially under-specified and not applicable to
  the revised taxonomy.} The version of record reported agreement for an earlier mixed-field
  rubric and therefore supplied no reproducibility evidence for the final validator facets.
  The revision freezes hash-bound local-source packets, the final coding manual and schema,
  a 42-cell schedule, strict provenance validation, isolated host-login CLI execution, and
  four adversarial smoke gates. Three vendors then produced one accepted fresh-session coding
  for each of 14 source records: six manuscript core cases and eight supplementary scope cases.
  All 42 accepted outputs and their hashes are sealed before analysis. Facet-wise mean pairwise
  Jaccard values are 0.567--0.706 and MASI-based Krippendorff $\alpha$ values are 0.165--0.338;
  90 record--facet disagreements are retained without overwriting raw outputs. These small-$n$
  quantities compare record-level unions of facet tokens, not alignment among complete
  validator channels. They are descriptive audit results, not pass thresholds, inferential validation, a
  human reference standard, or evidence that Servo outperforms a free-form or competing
  framework. The change strengthens traceability and demonstrates application of the final
  schema while leaving diagnostic superiority and downstream utility untested.

  \item[R25. Channel-aware core cases and construct crosswalk (Sections~\ref{sec:related},
  \ref{sec:core}, and Appendix~\ref{app:coding}).]
  \emph{Status in the version of record: materially under-specified and partly conflates
  validator presence with operational feedback.} The version of record compressed each
  system's heterogeneous assessment mechanisms into layer and loop labels, did not preserve
  which target, evidence source, evaluator, decision role, and feedback path belonged to the
  same channel, and offered no construct-level comparison with adjacent frameworks. After the
  R24 outputs were frozen, the six core cases were therefore adjudicated against the same
  hash-bound local-source packets. The released channel ledger resolves every evidence ID to
  an exact quote, page, and PDF hash; the separate component sheet records $S$, $G$, $E$, $M$,
  $\pi$, component-specific human authority, and experimental fidelity. The resulting table
  distinguishes operational feedback from terminal and external assessment and supersedes the
  record-level majority projection for substantive case reading. A framework-native crosswalk
  and three contrastive readings identify Servo's selected system-level resolution while
  acknowledging InternAgent's advantage for agent organization and the Robot Scientist as a
  negative case where the central closed loop was already explicit. The change improves
  traceability and construct clarity but does not establish population reliability, universal
  superiority, exhaustiveness, causal utility, or improved system design.

  \item[R26. Framework boundary corrections
  (Sections~\ref{sec:related},~\ref{sec:framework},~\ref{sec:domains}, and
  Appendix~\ref{app:coding}).]
  \emph{Status in the version of record: partly incorrect and materially under-specified.}
  The version of record claimed that no shared cross-system framework existed, although direct
  AI-Scientist surveys already organize autonomous discovery by capabilities, mechanisms, and
  workflow stages. The revision therefore compares Servo first with the unified frameworks of
  Wei et al. and Tie et al.; POMDP, InternAgent, CPC-MS, and ARA remain complementary adjacent
  formalisms rather than selected direct baselines. Servo's contribution is narrowed to making
  selected system-level distinctions explicit and comparable, not supplying the first shared
  vocabulary or a universally superior taxonomy. The substantive domain table and appendix also
  replace residual syntax/semantic/empirical/human/formal layer shorthand and common reliability
  rankings with target property, evidence and evaluator, decision role and feedback, fidelity
  boundary, and local bottleneck fields. The six-case validator table is now explicitly an
  author-interpreted source synthesis: channel split/merge and bounded ``None identified'' rules
  are disclosed, and neither R24's record-level token agreement nor the later adjudication is
  presented as independent channel-level reproducibility. Finally, R23's single stochastic $E$
  mixed a system-controlled executor with the environment's observation law. The present
  formulation keeps $E_{\mathrm{exec}}$ as the system component and introduces
  $O_{\mathrm{env}}$ as an auxiliary environment/measurement model outside the six-component
  tuple. These corrections leave the six component names and the three open problems intact,
  while narrowing the originality and reproducibility claims and clarifying the framework's
  system--environment boundary.

  \item[R27. Event channels and open-ended policy interfaces
  (Sections~\ref{sec:background},~\ref{sec:framework},~\ref{sec:openproblems}, and
  Appendix~\ref{app:coding}).]
  \emph{Status in the version of record: partly incorrect and materially under-specified.}
  The version of record, and revisions through R26, represented validation as one
  post-observation call even though the substantive cases distinguish pre-action filters,
  in-execution evaluators, terminal review, and external assessment. The revised $V$ is a
  family of event-indexed channels with a trigger phase and routed destination; the operational
  loop preserves pre-action and later events instead of collapsing them into one reward vector.
  The coding manual now uses trigger phase as a split criterion, but this is an author-specified
  refinement of the frozen R24 material, not a new independent recoding. The earlier
  gate-reliability/``trustworthy closure'' association is withdrawn rather than merely called
  untested because its outcome definition contained gate reliability; future studies require
  gate-independent, property-specific endpoints. The generator now returns an explicit
  search-space expansion, and the policy selects fidelity under a cost function and remaining
  budget. Finally, the novelty-gate proposal is relabeled as necessary design requirements and
  requires prospective power or precision calculations, prespecified prevalence and
  discrimination targets, confidence-interval precision, and follow-up/censoring rules. These
  changes make the six-component vocabulary capable of locating the stated open problems but
  do not establish open-endedness, cost-aware optimization, external outcome validity, or a
  sufficient novelty-validation protocol in any surveyed system.

  \item[R28. Closure coding, audit status, and search-space authority
  (Sections~\ref{sec:framework},~\ref{sec:core},~\ref{sec:openproblems}, and
  Appendix~\ref{app:coding}).]
  \emph{Status in the version of record: partly incorrect and materially under-specified.}
  The version of record and subsequent tables coded Coscientist and Agent Laboratory as
  ``partial'' even after the operational criterion defined any implemented feedback edge to
  later generation, policy, memory, stage, or represented search space as computational
  closure. Source-grounded channels show such edges in both systems, so the current table codes
  them computationally closed within their demonstrated task or revision workflows. Human
  problem selection, manual execution, terminal authority, and incomplete novelty or physical
  validation remain separate authority, fidelity, and evidential limitations. R24 is also
  reclassified as a historical development audit: its three-vendor record-level facets preceded
  the final trigger, routed channel, space-expansion, fidelity, cost, budget, and $H_S$ fields
  and therefore do not establish reproducibility of the current framework. The final six-case
  channel table remains the author's source-grounded synthesis. The novelty discussion now
  distinguishes functional generator/reviewer separation, which several systems implement,
  from independently validated and contamination-controlled novelty discrimination, which the
  surveyed reports do not establish. Finally, the authority vector adds $H_S$ so human control
  of the initial problem and represented search space is not silently folded into $G$. These
  changes preserve the diagnostic framework and open problems while correcting two case labels
  and narrowing its reproducibility and architecture claims.

  \item[R29. Canonical schema, derived closure, and projection integrity
  (Sections~\ref{sec:framework} and~\ref{sec:core}, Tables~\ref{tab:core-comparison}
  and~\ref{tab:core-channels}, and Appendix~\ref{app:coding}).]
  \emph{Status in the version of record: materially under-specified, with later revisions
  internally inconsistent.}
  The version of record did not provide a machine-checkable source of truth for the framework,
  and revisions through R28 still distributed current judgments among legacy fields, free-text
  component sheets, split channel/timing files, manually stored bilingual display strings, and
  prose. This allowed corrected closure definitions to coexist with stale loop labels and let
  Appendix~\ref{app:coding} restate a hypothesis already withdrawn as definitionally circular.
  The current revision freezes Servo schema~1.0, joins each event channel's trigger, destination,
  facets, evidence and source hash in one canonical row, records all six authority fields and
  system-level expansion/fidelity/cost/budget states, and derives computational closure from
  implemented routed edges rather than a stored label. A fail-closed validator checks evidence
  ownership, channel compatibility, historical/current separation, claim mapping and bilingual
  projections before generating both tables. The mixed \texttt{systems.csv}, compatibility
  exports, and R24 outputs remain available for reconstruction but are not current semantic
  inputs. This consolidation improves internal consistency and auditability; it is not a new
  independent recoding, source-entailment study, construct-validity result, or test of Servo's
  superiority or scientific-outcome prediction.

  \item[R30. Portable event--evidence contract and bounded case identity
  (Abstract; Sections~\ref{sec:framework},~\ref{sec:core}, and~\ref{sec:domains};
  Appendix~\ref{app:coding}).]
  \emph{Status in the version of record: materially under-specified; the post-submission
  Schema~1 interpretation was also too coarse.}
  The version of record and revisions through R29 treated a system record and a routed
  validator channel as sufficient current units and collapsed heterogeneous feedback into one
  computational-closure judgment. They did not require version, configuration, and task-regime
  identity along a witness; distinguish runtime events from reliability studies; or represent
  versioned artifacts and artifact revision explicitly. Schema~2.0 preserves the six-component
  core while placing $O_{\mathrm{env}}$, artifact state $A$, and optional artifact synthesis or
  revision $W_A$ at its boundary. It defines an event--artifact graph and five set-valued
  predicates---execution repair, experimental adaptation, artifact revision, discovery-cycle
  feedback, and human-mediated feedback---with conservative source-traceable witnesses. The
  application is restated as six versioned cases from five lineages and seven selected frozen
  source anchors. This change improves identity, provenance, and falsifiability of the
  diagnostic descriptions; it does not validate the schema, establish scientific outcomes,
  estimate a population, infer causes, or show comparative superiority.

  \item[R31. Local reproducibility-package status
  (Reproducibility and Responsibility Checklist; Appendix~\ref{app:coding}).]
  \emph{Status in the version of record: absent, and later post-submission wording overstated
  public availability.}
  The archival record did not contain Schema~2.0. A complete working-tree package now exists
  locally, including the normative schema and case, endpoint, artifact, event, edge,
  reliability, closure-witness, closure-status, domain-anchor, and selection-ledger records.
  No public repository snapshot or DOI for that complete package has yet been verified, and it
  is neither published nor part of the official record. The reproducibility and open-access
  checklist answers are therefore changed to ``No---not yet.'' This correction separates local
  preparation from public availability; it does not change the paper's diagnostic argument or
  supply external reproduction, peer validation, or official erratum linkage.

  \item[R32. Predicate conformance and provenance.]
  \textbf{Scope:} Related Work; \S\ref{sec:framework}, \S\ref{sec:core},
  \S\ref{sec:discussion}; reproducibility checklist.
  \emph{Status in the version of record: absent; the earlier post-submission contract specified
  a full pattern only for discovery-cycle feedback and did not separate source silence from
  negative evidence.}
  This revision defines minimum graph patterns for all five predicates, adds machine-readable
  decision bases for established, unknown, not-established, and not-applicable statuses, and
  reclassifies source-silent negatives as unknown. It maps base objects and relations to PROV-DM
  and Workflow Run RO-Crate while limiting Servo's increment to scientific diagnostic semantics.
  It also withdraws demonstrated portability: the six complete cases were formative and the seven
  anchors are partial, so no prospective held-out full instantiation has yet been reported. The
  public 2.0.0 snapshot predates these changes; the checklist remains ``No---not yet'' for the
  current analysis until a synchronized successor release is published.
  \item[R33. Closure-axis correction and cross-representation conformance.]
  \textbf{Scope:} Abstract; \S\ref{sec:framework}; \S\ref{sec:core}; Appendix~\ref{app:coding}; public analysis package.
  \emph{Status before this correction: the actor providing feedback was mixed with path topology, and the AI Scientist 2026 adaptation cell omitted a source-stated execution transition.}
  Human mediation is now an actor facet rather than a fifth closure predicate. The four remaining predicates describe path topology. Event classes and edge types are constrained to compatible six-component actors and source--destination pairs. The AI Scientist 2026 experimental-adaptation status is corrected to established because metric- and plot-guided node selection is followed by child-code generation and reported parallel execution. This does not promote that path to discovery-cycle feedback, which still requires an explicit epistemic update and a second evidence occurrence.
  \item[R34. Explicit execution occurrences in adaptation witnesses.]
  \textbf{Scope:} Predicate contract and public analysis package.
  The experimental-adaptation validator now requires a later event whose class is explicitly \texttt{execution}; reaching endpoint $E$ or repeating an evaluation event is insufficient. The AI Scientist 2024 and InternAgent witnesses now name their already source-grounded execution events directly. This tightens conformance without changing their established statuses.
  \item[R35. Portability-claim boundary.]
  \textbf{Scope:} Related Work; \S\ref{sec:framework}; normative contract and provenance crosswalk.
  The manuscript no longer labels the current contract or event--artifact graph portable. The evidence establishes an operational, machine-readable representation and a construct-level mapping to PROV-DM and Workflow Run RO-Crate. It does not establish executable serialization, standards conformance, or out-of-sample portability; those require a tested serializer and a prospectively frozen holdout application.
  \item[R36. Explicit tuple--graph admissibility maps.]
  \textbf{Scope:} \S\ref{sec:framework}; normative contract and validator.
  The manuscript now states the complete event-class--actor map $\eta$ and edge-type--component-transition map $\tau$ enforced by the validator. This makes instantiated system-component assignments and represented graph transitions jointly checkable while preserving the distinction between an invalid mapping and a source that does not report one; it does not make the auxiliary environment or measurement process graph-identifiable.
  \item[R37. Actor--topology independence and explicit predicate patterns.]
  \textbf{Scope:} \S\ref{sec:framework}; normative contract, validator, and regression suite.
  Human mediation may now qualify a structurally valid discovery-cycle path without being mistaken for a closure type or an automation claim. Table~\ref{tab:predicate-patterns} states the required evidence condition, ordered route, endpoint or recurrence, and exclusions for all four predicates; the validator continues to reject retry-only, append-only, disconnected, and otherwise nonconforming paths.
  \item[R38. Explicit execution-repair occurrences.]
  \textbf{Scope:} Table~\ref{tab:predicate-patterns}; execution-repair witnesses, validator, and regression suite.
  An execution-repair witness must now name a later event whose class is explicitly \texttt{execution}; reaching endpoint $E$ or repeating a runtime-validation event is insufficient. The three established repair witnesses now identify the reported post-repair execution occurrence, so the released records and the reader-facing graph pattern enforce the same rule.
  \item[R39. Witness-level artifact successor linkage.]
  \textbf{Scope:} Table~\ref{tab:predicate-patterns}; execution-repair and artifact-revision validators; regression suite.
  A qualifying evaluation event must now name both the predecessor artifact and a same-type output artifact whose version is exactly one greater and whose \texttt{predecessor\_artifact\_id} points to that input. A routed edge to $W_A$ or an unrelated valid successor elsewhere in the case is insufficient. This enforces the changed-artifact and distinct-successor conditions stated in Table~\ref{tab:predicate-patterns}.
  \item[R40. Evaluation-to-action connectivity for adaptation.]
  \textbf{Scope:} Table~\ref{tab:predicate-patterns}; experimental-adaptation validator and regression suite.
  An adaptation witness must now connect an evaluation endpoint through at least one intervening action component in $\{M,\pi,G,W_A\}$ and feedback control before reaching the endpoint of a later explicit execution. An unrelated $G\!\to\!E$ edge cannot be paired with otherwise ordered evaluation and execution events to establish adaptation.
  \item[R41. Explicit epistemic-action occurrence in discovery feedback.]
  \textbf{Scope:} Table~\ref{tab:predicate-patterns}; discovery-cycle witness, normative contract, validator, and regression suite.
  Discovery-cycle feedback must now name an event whose \texttt{event\_kind} is \texttt{epistemic\_action} between the first evidence occurrence and the later execution, and that event's actor endpoint must lie on the routed action segment after the epistemic update. The Robot Scientist witness now records the source-stated hypothesis-generation and experiment-design action explicitly; endpoints and control edges alone are insufficient.
  \item[R42. Negative-status evidence boundary.]
  \textbf{Scope:} \S\ref{sec:framework}; Table~\ref{tab:status-matrix}; normative contract, status records, validator, and regression suite.
  \texttt{not\_established} now requires explicit source-grounded contrary evidence; an incomplete trace or an unverified claim that a trace is complete is classified as \texttt{unknown}. The three discovery-cycle rows formerly labelled \texttt{not\_established} are corrected to \texttt{unknown}: their graphs already contain epistemic-update edges, contrary to the former rationales, while a distinct later evidence occurrence and, in two cases, an explicit scientific action event remain insufficiently reported.
  \item[R43. Cross-surface adaptation contract and release mutability.]
  \textbf{Scope:} Predicate contract; reproducibility checklist; regression suite.
  The human-readable normative table now matches the manuscript and validator: experimental adaptation ends at a later explicit execution and does not require the second evidence occurrence reserved for discovery-cycle feedback. A regression test guards that recurrence boundary. Static package documentation now defers publication state to the generated attestation and names the current Schema~3 contract instead of the superseded Schema~2 contract. The checklist also replaces ``immutable release'' with ``versioned, checksum-bound release'': the checksums make replacement detectable, but the hosting platform reports that the release itself is not immutable.
  \item[R44. Closure-route and release-identity consistency.]
  \textbf{Scope:} Normative contract; closure records and validator; public release metadata and artifact policy; regression suite.
  Every predicate, including discovery-cycle feedback, now passes the same common-route checks for implemented, case-internal, closure-eligible edges. A \texttt{not\_established} status must cite source-grounded evidence, while every status retains a nonempty rationale; this prevents missing reporting from being converted into a negative finding. The public package now aligns its Schema~3 project identity, citation version, release URL, event semantics, and evidence-ledger path. The artifact policy also distinguishes immutable submitted PDFs from rebuildable post-submission products and requires the released corrected PDF to remain byte-identical to its reader-facing counterpart.
  \item[R45. Predicate semantics and matrix totality.]
  \textbf{Scope:} Predicate contract; closure matrix; tuple--graph conformance; canonical C03 rationale; regression suite.
  Execution repair now requires an explicit retry-with-revision event whose update semantics record failure-driven artifact change. Experimental adaptation requires one of the enumerated evidence-to-changed-action update semantics in addition to its routed later execution. The validator also enforces exactly one status for every case--predicate pair, rejects missing or duplicate cells and negative cells that contradict an established canonical witness, and resolves every edge's mediator endpoint. The AI Scientist 2026 discovery-cycle rationale now states the actual missing conditions---an explicit epistemic update and a distinct later evidence occurrence---rather than calling its implemented executor edge unclear.
  \item[R46. Ordered-witness and release-schema integrity.]
  \textbf{Scope:} Witness grammar and validator; release identity; source-audit documentation; current-interpretation index.
  Event occurrences now use only \texttt{@t} or monotone \texttt{@t+1} labels, and each routed edge must remain bound to a source event in witness order; malformed recurrence labels and later-event splicing fail closed. Release readiness now requires both the public manifest and attestation to identify normative Schema~3.0.0. The source-byte audit is described only as a byte, uniqueness, and containment check, not as passage- or page-locator verification. The supersession index below now points to the four-predicate Schema~3 contract rather than leaving Schema~2 as the apparent current state.
  \item[R47. Cross-entry-point schema identity.]
  \textbf{Scope:} Public regeneration; normative schema and evidence ledger; occurrence grammar; regression suite.
  The public-regeneration path now rejects a manifest that does not identify Schema~3.0.0, matching release-ready behavior. The normative YAML and evidence ledger must carry the same schema identity before hash verification. The executable occurrence grammar now matches the normative contract exactly: only \texttt{@t} and \texttt{@t+1} are accepted, so arbitrary offsets cannot manufacture unreported iterations.
  \item[R48. Manifest, adaptation-route, and mediation binding.]
  \textbf{Scope:} Public manifest; experimental-adaptation validator; mediator conformance; regression suite.
  The validator now rejects the obsolete \texttt{generated\_artifacts} alias so only the attestation-bound \texttt{generated\_artifact\_sha256} map controls regeneration and allowlisting. An established adaptation must bind an evaluation event itself to the first edge of its routed action segment; merely listing a disconnected evaluation occurrence is insufficient. Every mediator endpoint must belong to the edge's case, and human versus system mediation must agree with whether that endpoint is external.
  \item[R49. Documentary observation projection and predicate implication.]
  \textbf{Scope:} Abstract; Related Work; \S\ref{sec:framework}; Table~\ref{tab:predicate-patterns}; Table~\ref{tab:status-matrix}; limitations; provenance crosswalk; normative contract and validator.
  The tuple-level environment law is now identified as a conceptual boundary rather than an instantiated graph endpoint. The graph-level \texttt{observation} edge and result-artifact producer fields are delimited as execution-anchored documentary availability records, not causal representations of environment or measurement production. The manuscript also distinguishes event class from event kind, replaces the claim that closure predicates are independent with separate reporting plus declared implications, and the validator enforces that established execution repair entails established artifact revision.
  \item[R50. Public regression-suite completeness.]
  \textbf{Scope:} Public package builder, manifest, regression tests, and reproducibility checklist.
  The public package now includes the package-applicable mutation and conformance tests cited as regression evidence, declares their pytest dependency as a locked test extra, and disables in-package pytest caches so their execution does not invalidate the public allowlist. Repository-only manuscript, external-publication, source-vault, and finalization tests remain repository gates rather than being represented as executable public-package tests.
  \item[R51. Source-reported policy information state.]
  \textbf{Scope:} Background; six-component interface; POMDP and BED boundary; normative schema and contract; bilingual regression gate.
  The policy interface now takes a source-reported decision-time information state $I_t$ rather than requiring a POMDP belief $b$ in every case. Servo neither reconstructs an unreported latent state nor assumes a state-update function. An explicit belief or posterior is represented only by the specialization $I_t=b_t$. Persistent memory $M$ remains a distinct storage and retrieval substrate that may supply information to $I_t$ but is not identical to it.

  \item[R52. GNoME's acquisition rule (Section~\ref{sec:domains}; Section~\ref{sec:openproblems}; Table~\ref{tab:domain-comparison}).]
  \emph{Status in the version of record: contradicted by the cited source.} The version of
  record presents GNoME as the closest surveyed approximation to an information-gain-optimal
  policy: its domain-table policy cell reads ``uncertainty sampling,'' and the body describes
  ``deep-ensemble uncertainty estimates \dots{} read as a coarse EIG surrogate'' and
  ``uncertainty estimates that the manuscript reads as a coarse approximation to the BED
  ideal.'' The cited Methods describe the opposite selection principle: candidates are filtered
  by predicted formation energy under a fixed stability threshold ($50\,\mathrm{meV\,atom^{-1}}$),
  and for active learning only the minimum-energy structure per composition is sent for DFT
  verification---greedy exploitation of predicted stability, not information-gain sampling. The
  deep ensemble ($n{=}10$) quantifies predictive uncertainty for generalization and confidence
  bounds, not to select experiments; expected information gain selects the \emph{most uncertain}
  design, whereas GNoME selects the \emph{most stable} predicted candidate---opposite criteria.
  The revision recodes the policy as stability-threshold filtering and removes the EIG/BED-surrogate
  framing. This strengthens rather than weakens the BED--practice gap, since it makes GNoME another
  system that does not implement an information objective rather than a partial exception to it. The
  DFT-in-the-loop active-learning \emph{loop} is unaffected; only the mischaracterized \emph{selection
  criterion} is corrected.

  \item[R53. Self-driving-laboratory review characterization (Section~\ref{sec:openproblems}).]
  \emph{Status in the version of record: contradicted by the cited source.} The version of record
  cites the self-driving-laboratory review for ``the rapid maturation of the underlying hardware.''
  The review's stated emphasis is the reverse: it argues that software autonomy is preeminent for
  scientific progress and treats physical automation as the comparatively tractable part (laboratory
  robots ``almost never perform tasks that would be outright impossible for a human''). The revision
  attributes to the review only its actual claim---that intelligent, not physical, autonomy is the
  binding constraint---which in fact aligns with this paper's own point that the escalation
  bottleneck is orthogonal to hardware automation.

  \item[R54. Analytical-technique attribution in chemistry (Section~\ref{sec:openproblems}).]
  \emph{Status in the version of record: unsupported by the cited source.} The version of record
  cites the Anthropic ``chemist'' technical report for ``physical characterization (NMR, MS).'' That
  report addresses NMR prediction and structure elucidation only; it contains no mass-spectrometry
  content. The revision drops the MS example from this citation.

  \item[R55. Escalation-timing claim in chemistry (Section~\ref{sec:openproblems}).]
  \emph{Status in the version of record: attributed to a source that does not make the claim.} The
  version of record cites a 2019 chemical-space-exploration review for the statement that ``NMR and
  MS characterization require physical execution that no current system knows when to invoke.'' That
  review is optimistic about automation and raises no escalation-timing (when-to-invoke) problem; it
  also predates the 2023--2024 systems the sentence calls ``current'' and so cannot speak to them.
  The revision states the escalation-timing point as this paper's own observation and cites the
  review only for the general background that physical characterization lies outside the automated
  search.

  \item[R56. Leiden signatory composition (Section~\ref{sec:openproblems}).]
  \emph{Status in the version of record: characterization narrower than the signatory pool.} Beyond
  the count-provenance issue recorded in R1, the sentence describes the signatories as
  ``mathematicians.'' The declaration's drafters and signatories are a mixed group of mathematicians,
  computer scientists, philosophers, and historians. The revision describes them as mathematicians
  and allied scholars.

  \item[R57. Knowledge-graph ideation outcome (Section~\ref{sec:related}).]
  \emph{Status in the version of record: partly contradicted by one cited source.} The version of
  record groups two knowledge-graph ideation systems and states that both help ``surface and rank
  higher-interest research ideas.'' Only the first (SciMuse) measures self-reported \emph{interest};
  the second (Spacer) ranks candidates by predicted \emph{impact/novelty} (a reported AUROC of 0.737
  for high-impact ideas), not interest. The revision states each system's actual ranking target.

  \item[R58. Reverse-engineering finding (Section~\ref{sec:openproblems}).]
  \emph{Status in the version of record: understates the cited source's finding.} The version of
  record cites the reverse-engineering study for LLMs that ``fail to do so reliably even with
  systematic query access,'' which reads as though querying does not help. The study's finding is
  that active querying---intervening on the black box rather than only observing it---\emph{substantially
  improves} performance while still falling short of reliable Bayesian inference. The revision states
  that active querying improves on passive observation yet remains below reliable performance.

  \item[R59. BioPlanner's function (Section~\ref{sec:domains}).]
  \emph{Status in the version of record: mischaracterizes the system's role.} The version of record
  states that ``BioPlanner generates experimental protocols.'' BioPlanner is an automatic-evaluation
  benchmark (BioProt): protocols are LLM-generated and BioPlanner scores their planning against a
  reference, rather than being a protocol generator itself. The revision describes it as evaluating
  LLM-generated protocols.

  \item[R60. Kandasamy author list (References).]
  \emph{Status in the version of record: bibliographic error.} The entry for the 2017 ICML paper
  ``Multi-fidelity Bayesian optimisation with continuous approximations'' listed five authors,
  inserting Junier B.\ Oliva; the paper has four (Kandasamy, Dasarathy, Schneider, P\'oczos). Oliva
  is an author of a separate 2016 multi-fidelity paper. The entry now lists the four correct authors.

  \item[R61. Aletheia author order (References).]
  \emph{Status in the version of record: bibliographic error.} The entry for arXiv:2602.10177 promoted
  Quoc V.\ Le and Thang Luong to the 2nd and 3rd author positions; on the source they are the last two
  authors, and the actual 2nd/3rd authors (Trinh, Bingham) were correspondingly demoted. The entry now
  follows the source order and renders ``Feng et al.'' unchanged.

  \item[R62. Workflow Run RO-Crate version and year (References).]
  \emph{Status in the version of record: bibliographic error.} The entry dated version~0.5 of the
  Workflow Run RO-Crate profile to 2023; version~0.5 was published 19~June 2024 (Zenodo record
  12159311). The year is corrected and the deposit is noted, while the citation key is retained for
  continuity.

  \item[R63. What the ARA 90.2\% measures (Section~\ref{sec:core}).]
  \emph{Status in the version of record: mislabels the population and inverts the source caveat.} The
  version of record wrote ``90.2\% of extension cost is failed exploration.'' In the source, 90.2\% is
  the share of \emph{total dollar cost}---across 24,008 agent runs over 228 tasks in the METR MALT
  corpus---spent in runs that did not reach the task's reference score. The source explicitly states
  ``this is not wasted research effort'': the cost becomes waste only when a later agent cannot reuse
  the exploration and must rediscover the same dead ends. The revision restates the figure as
  below-reference agent-run cost carrying that conditional.

  \item[R64. ARA memory mapping, \texttt{/trace} versus \texttt{/logic} (Section~\ref{sec:core}).]
  \emph{Status in the version of record: contradicted by the cited source.} The version of record wrote
  that ``\texttt{/trace} externalizes $M_e/M_s$'' (episodic and semantic). In ARA the semantic content
  (falsifiable claims, convergence-critical heuristics, design reasoning) is held in \texttt{/logic}
  (the Cognitive Layer); \texttt{/trace} (the Exploration Graph) holds the branching trajectory and
  session history (episodic). The revision maps \texttt{/trace} to $M_e$ and locates $M_s$ in
  \texttt{/logic}.

  \item[R65. ResearchBench temporal cutoff (Section~\ref{sec:openproblems}).]
  \emph{Status in the version of record: off by one year.} The version of record wrote ``post-2024
  findings,'' which in normal usage excludes 2024. The source restricts ``to publications from 2024
  onward,'' with 2024 included. The revision uses ``from 2024 onward.''

  \item[R66. AI Scientist scoring example (Section~\ref{sec:openproblems}).]
  \emph{Status in the version of record: conflates two separate scoring stages.} An earlier
  post-submission sentence illustrated score collapse with ``The AI Scientist rates ideas on separate
  interestingness, feasibility and novelty scales, yet uses an aggregate \texttt{Overall} paper
  score.'' Those three are the generator's self-ratings of its own \emph{ideas}; \texttt{Overall} is a
  separate reviewer score on the finished \emph{paper}, and no documented mechanism aggregates the
  former into the latter. The revision re-grounds the example on the reviewer's own separate axes
  (originality, quality, clarity, significance) collapsing into \texttt{Overall} and the accept/reject
  decision---the actual within-reviewer collapse. The open-problem claim is unchanged.

  \item[R67. What the ARA 82.6\% measures (Section~\ref{sec:core}).]
  \emph{Status in the version of record: the label understates the estimand.} The version of record
  wrote ``Rigor Auditor (82.6\% detection).'' The figure is recall on a seeded-mutation benchmark: 23
  already-valid ARAs each receive one of five predefined defect injections (115 mutations, 95 caught
  $=82.6\%$), each injection serving as its own oracle with no expert gold standard; per-type detection
  ranges $100/100/100/91/22\%$. The revision labels it recall on the seeded rigor-defect benchmark. The
  number itself and the 22\% orphan-experiment figure were already correct.

  \item[R68. Coscientist experimental-adaptation coding (released \texttt{servo2} closure sheet).]
  \emph{Status in the version of record: coding more conservative than the source supports.} The
  released \texttt{servo2} coding marks C01 (Coscientist) \texttt{experimental\_adaptation} ``unknown,''
  on the rationale that reuse of prior-iteration outcomes for guidance is inferred while a downstream
  evidence-generating execution is not separately witnessed. The source in fact states the mechanism:
  each action selects reaction conditions ``listing the player's observations about the outcome of the
  previous iteration,'' and the system ``reuse[s] the information obtained to provide more specific
  guidance'' over up to 20 iterations, with normalized advantage rising across rounds. This is direct,
  not inferred, evidence of experimental adaptation. The rationale is corrected to record the source
  mechanism, and the cell is now recoded to ``established'': a source-grounded witness (\texttt{W17}) traces
  the reused reactivity evidence through the memory and policy path ($C01.V\!\to\!C01.M\!\to\!C01.\pi\!\to\!C01.E$)
  to a later guided execution (ordered occurrences \texttt{EV46@t;EV47@t+1}), grounded in the same Boiko
  reactivity quote already in the evidence ledger (\texttt{R01-E04}). The closure matrix
  (Table~\ref{tab:core-comparison}) and the released closure sheet are regenerated accordingly. The new
  evaluation and execution occurrences are marked structurally inferred, consistent with the source's
  aggregate ``advantage increases over time'' phrasing and with the existing treatment of that evidence.

  \item[R69. BioPlanner anchor coding (Table~\ref{tab:domain-comparison}; released \texttt{servo2} anchor sheet).]
  \emph{Status in the version of record: overstates the evaluator and decision role.} The released
  anchor codes BioPlanner's analysis target as ``protocol planning and executability,'' its evaluator
  as ``generator, evaluator, laboratory,'' and its decision role as ``diagnosis and external
  execution.'' The source's systematic benchmark measures pseudocode reconstruction (effectively
  multiple-choice selection over admissible pseudofunctions); its ``Feedback'' is a code-error loop,
  not laboratory feedback; and the wet-lab component is a single one-off \emph{E.\ coli} run, not a
  general executability validator. This revision restricts the anchor: the domain-anchor table now reads
  ``protocol-planning pseudocode reconstruction,'' ``generator; pseudocode evaluator; one-off lab check,''
  and ``diagnostic benchmark; single validation,'' matching the already-correct channel records
  (DA05-C1, DA05-C2, DA05-C3), and the table is regenerated accordingly.
\end{description}

\noindent\textbf{Scope of revision.} The entries above are the complete set of changes
made since the archival deposit, R1--R69. Entries R3--R12 narrow or correct statements
that the citation audit judged unsupported by, contradicted by, or less precise than their
cited sources. Entries R13--R16 record the subsequent adversarial mathematical review: they
replace the proposition/assumption/proof-sketch presentation with bounded analytical
observations, correct the EIG statement, delimit the conditions under which the
Ghosal--van~der~Vaart and Berk references may be invoked, and distinguish mathematical
non-identification from the surveyed use of human judgment. R17 reconciles two table rows with
the released coding sheet. R18 records the adversarial recheck that completed the propagation
of the earlier mathematical corrections, including the stronger prior-factorization premise
and the removal of residual universal, causal, and human-only wording. R19 corrects the
citation guidance, distinguishes novelty assessment from operational gating, and withdraws
the untestable direction-consistency statement. R20 makes gate-zero semantics explicit,
withdraws the holistic validator order from substantive analysis, narrows closure and formal-oracle
language, and replaces the novelty majority-agreement threshold with a prospective validation
design. R21 types the generator--policy interface, identifies the internal experimental
feedback that supports the AI Scientist (2024) computational-loop coding, replaces scalar
human-intervention scores, and reframes the BED and proxy-to-physical criteria around accepted
surrogate BED and multi-fidelity integration methods. R22 makes validation context-dependent,
limits the POMDP relation to organizing concepts rather than a complete instantiation, separates
the absence of reported novelty validation from adjacent assessment failures, removes residual
cross-domain association language, and states the system-level abstraction of multi-agent cases.
R23 places a stochastic, design-conditioned observation kernel inside $E$, replaces mixed
validator layers with explicit facets, reserves calibration for measured probability--outcome
correspondence, and limits the old agreement statistics to their pre-revision rubric.
R24 replaces the abandoned free-form baseline comparison with an evidence-bound audit of six
core and eight supplementary records, freezes 42 independent three-vendor codings, and reports
facet disagreements and agreement coefficients only as descriptive development-audit diagnostics.
R25 replaces the record-level majority projection as substantive evidence with a
source-adjudicated channel ledger, restores the complete component and authority fields for the
six cases, and adds a framework-native construct crosswalk with contrastive and negative cases.
R26 adds the closest AI-Scientist survey frameworks to the direct comparison, propagates the
final validator facets through the domain analysis, marks the six-case channel table as an
author interpretation rather than an independently reproduced result, and separates the
system executor from the auxiliary environment observation law.
R27 replaces the single post-observation validator call with routed event channels, withdraws
the circular gate-reliability/closure hypothesis, makes search-space expansion and budgeted
fidelity explicit, and turns the novelty benchmark checklist into precision-driven design
requirements.
R28 applies the closure rule consistently to Coscientist and Agent Laboratory, demotes R24 to
a pre-final-schema development audit, separates functional reviewer architecture from validated
novelty discrimination, and adds authority over the search space to the human-authority vector.
R29 consolidates the current six-case semantics in a versioned schema, derives closure and
bilingual tables from canonical records, rejects legacy/R24 inputs from current projections,
and corrects the residual Appendix-B restatement of the withdrawn closure hypothesis.
R30 superseded Schema~1 as the then-current interpretation: it introduced bounded versioned case
identity, explicit artifact state and revision, typed event and edge records, and five
predicate-specific closure judgments with ordered witnesses; it also replaces domain
aggregation with seven selected frozen source anchors.
R31 records the then-local package state; R32 records the later public 2.0.0 snapshot, clarifies
all predicate and evidential-status contracts, adds the provenance mapping, and marks the revised
working tree as awaiting a synchronized successor release.
The six component labels persist, as do the three prospective design questions, but their
interfaces and operationalization have changed materially: Schema~2 adds bounded identity,
versioned artifacts, $W_A$, typed event and edge records, and predicate-specific witnesses in
place of Schema~1's channel and single-closure interpretation. The application remains
non-representative source annotation. In addition to the entry corrected in R11, R21 adds
Parasuraman et al. on function-specific human--automation authority and Kandasamy et al. and
Song et al. on multi-fidelity Bayesian optimization; R26 adds Wei et al. and Tie et al. as
the closest direct AI-Scientist survey frameworks.

Entries R52--R59 record a second citation audit. R52 recodes GNoME's policy as
stability-threshold filtering rather than uncertainty sampling or an EIG surrogate, correcting
the domain table and the BED--practice-gap discussion. R53 corrects the self-driving-laboratory
review's emphasis (software rather than hardware autonomy). R54 drops an unsupported
mass-spectrometry attribution; R55 detaches an escalation-timing claim from a review that does
not make it; R56 widens the Leiden signatory description beyond mathematicians; R57 separates
interest from impact ranking in two knowledge-graph ideation systems; R58 corrects an
understatement of the reverse-engineering study's querying result; and R59 recasts BioPlanner as
an evaluation benchmark rather than a protocol generator. None of these entries changes the
framework, the three open problems, or their proposed evaluations.

Entries R60--R69 record a third citation audit against primary metadata and source text. R60--R62
correct bibliographic identity errors (an inserted Kandasamy co-author, a reordered Aletheia author
list, and a Workflow Run RO-Crate version/year mismatch). R63 and R67 correct the labelling of two
ARA statistics---the 90.2\% below-reference cost, restated with the source's ``not wasted'' caveat,
and the 82.6\% seeded-mutation recall. R64 restores ARA's \texttt{/trace}-versus-\texttt{/logic}
memory separation, R65 fixes a one-year cutoff error for ResearchBench, and R66 re-grounds an AI
Scientist scoring example on the reviewer's own axes. R68 records that the Coscientist
experimental-adaptation cell is recoded to \texttt{established} with a source-grounded witness; R69
restricts the BioPlanner anchor from an overstated laboratory/executability channel to its actual
pseudocode-reconstruction benchmark. Both regenerate the affected \texttt{servo2} tables so the
result matrices match the corrected interpretation. None of these entries changes the
framework, the three open problems, or their proposed evaluations.

\noindent\textbf{Current-interpretation supersession index.}
R23's stochastic executor formulation is read with R26's executor/environment separation;
R24's agreement results are read only as the development audit delimited by R28 and R29; in
particular, R24's contemporaneous phrases ``final coding manual and schema'' and ``application
of the final schema'' are superseded and do not describe schema~1.0;
R25's six-case synthesis is read through the canonical event records introduced in R29; and
R27's event-channel interface and R29's Schema~1 closure derivation are superseded by the
Schema~3 event--artifact graph, bounded case identity, and four predicate-specific witness
contracts finalized through R33--R51. References in earlier entries to ``final'' Schema~1 tables or current
six-case closure labels are historical statements, not present semantics. This index does not
alter the historical text or chronology of those entries.
```
