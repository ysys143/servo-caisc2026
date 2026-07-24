"""Evidence layer for SERVO v5: derive the three manuscript evidence tables from
the frozen v5 policy, alignment and claim records, LAST in the D.1 build order
(source proposition -> alignment rubric -> claims -> policy -> [this file:
evidence tables]).

Contract T11 v3 section C is the authoritative column spec. This script emits
three tables that replace the retired closure status matrix (Table 2):

- Table A -- Policy (per case; servo_v5_policy). Columns: Case | Selection
  signal | Follow-up (control) dependence | Selection-purpose facets |
  Candidate-selection rule | Design-selection rule | Candidate-execution rule.
  One row per case, each cell listing the enum values present in the bounded
  source. Candidate-selection rule (which candidate hypotheses h are chosen) and
  Design-selection rule (how the experimental design/assay d is chosen -- the
  BED-central axis added for reviewer Item 2) are SEPARATE columns. generation_scope
  is NOT a column (it is a G/S-level provenance axis) and there is no
  explicit_bed / BED-yes-no column. formal_epistemic_utility_evidence is a
  corpus-level footnote, never a per-case column.

- Table B1 -- Observation-evaluation boundary (case-level; alignments).
  Columns: Case | Observation source | Evaluation target | O-V boundary. Kept
  case-level (not relation-level) to avoid a mostly-n.a. column. The O-V
  boundary is the O_env<->V split carried by evaluation->observation relations
  (rubric v5-rubric-3): separated if the source reports that split in at least
  one relation, boundary_unreported if such relations exist but none reports it.

- Table B2 -- Relation / evidence (per functional relation; alignments +
  claims). Columns: Case | Functional relation (source_role, relation_type,
  target_role, temporal_scope) | Source support | Occurrence resolution |
  Evidence mode. Rendered as a longtable (~70 rows) so it breaks across pages.
  support_status and occurrence_resolution are ALWAYS separate columns (never
  merged); support uses `supported` (not `resolved`). Evidence mode identifies
  the kind of proposition supported by the source and is NOT an ordinal scale
  (see the legend footnote).

Charter references (analysis/servo_v5_charter.md):
- B.2: DerivedDecisionClaim axes (support_status, claim_scope, alignment_kind,
  occurrence_resolution). claim_scope's ascending resolution order is
  architecture < procedure < aggregate_run < occurrence.
- B.4 / contract section B: policy is a schema-v3 BED-lens decomposition, NOT an
  explicit_bed compliance label.
- B.5 / rubric v5-rubric-3: boundary_status reports the E<->O_env and O_env<->V
  splits; Table B1 reads the O_env<->V split from evaluation->observation.
- B.7: the compositional (source_role, relation_type, target_role) schema that
  replaces the retired predicate enum.

This script owns its own JSON/CSV readers (it does not import the servo_v5_*
package modules) and follows the LaTeX-table conventions of
build_servo2_tables.py (tex() escaping, sha256 manifest) so the generators stay
easy to compare, without sharing retired predicate logic.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CLAIMS_DIR = ROOT / "servo_v5_claims"
POLICY_DIR = ROOT / "servo_v5_policy"
ALIGNMENTS_DIR = ROOT / "servo_v5_alignments"

CASE_IDS = ("C01", "C02", "C03", "C04", "C05", "C06")


class TableBuildError(Exception):
    pass


# ---------------------------------------------------------------------------
# Readers
# ---------------------------------------------------------------------------


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise TableBuildError(f"missing input: {path}") from error
    except json.JSONDecodeError as error:
        raise TableBuildError(f"invalid JSON in {path}: {error}") from error


def load_case_family(dirpath: Path, list_key: str) -> dict[str, list[dict]]:
    """Load every C0X.json in a directory into {case_id: [records]}."""
    out: dict[str, list[dict]] = {}
    for case_id in CASE_IDS:
        payload = read_json(dirpath / f"{case_id}.json")
        if payload.get("case_id") != case_id:
            raise TableBuildError(f"{dirpath.name}/{case_id}.json: case_id field does not match filename")
        out[case_id] = payload[list_key]
    return out


def load_policy() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for case_id in CASE_IDS:
        payload = read_json(POLICY_DIR / f"{case_id}.json")
        if payload.get("case_id") != case_id:
            raise TableBuildError(f"servo_v5_policy/{case_id}.json: case_id field does not match filename")
        out[case_id] = payload
    return out


# ---------------------------------------------------------------------------
# LaTeX helpers (matching build_servo2_tables.py conventions)
# ---------------------------------------------------------------------------


def tex(value: str) -> str:
    replacements = (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("_", r"\_"), ("#", r"\#"))
    for source, target in replacements:
        value = value.replace(source, target)
    return value


def mono(value: str) -> str:
    """A single enum token in \\texttt with underscores escaped."""
    return r"\texttt{" + tex(value) + "}"


def mono_list(values: list[str]) -> str:
    """A set of enum tokens stacked with \\newline inside a p{} cell (each token
    kept whole; the vertical stack avoids horizontal overflow of long enums)."""
    if not values:
        return r"\textendash"
    return r"\newline ".join(mono(value) for value in values)


def text_list(values: list[str]) -> str:
    """A set of free-text phrases stacked with \\newline inside a p{} cell."""
    if not values:
        return r"\textendash"
    return r"\newline ".join(tex(value) for value in values)


def legend(lines: list[str]) -> str:
    """A \\footnotesize legend paragraph placed after the tabular, inside the
    generated .tex file so it travels with \\input without touching the
    manuscript."""
    body = [r"\par\vspace{2pt}\noindent\footnotesize"]
    body.append(r"\emph{Legend.} " + " ".join(lines))
    body.append("")
    return "\n".join(body)


def file_header_comment(lines: list[str]) -> str:
    body = ["% " + line if line else "%" for line in lines]
    body.append("")
    return "\n".join(body)


# ---------------------------------------------------------------------------
# Shared enums (mirrors servo_v5_schema.yaml enum_fields; validated below)
# ---------------------------------------------------------------------------

CONTROL_DEPENDENCE = (
    "fixed_or_predefined", "failure", "score", "observation_result",
    "uncertainty", "candidate_disagreement", "not_reported",
)
SELECTION_OBJECTIVE = (
    "local_repair", "performance_improvement", "uncertainty_reduction",
    "hypothesis_model_discrimination", "diversity_directed_selection",
)
GENERATION_SCOPE = ("fixed_space", "search_space_expansion", "candidate_diversification")
CANDIDATE_SELECTION_RULE = (
    "fixed", "threshold", "top_k_ranked", "sampled_subset",
    "sequential_choice", "exhaustive", "not_reported",
)
DESIGN_SELECTION_RULE = (
    "fixed_or_standard_design", "discrimination_directed", "information_directed",
    "cost_directed", "coverage_or_factorial", "not_reported",
)
CANDIDATE_EXECUTION_RULE = (
    "all_selected", "one_at_a_time", "batch", "until_success",
    "until_budget", "source_unreported",
)

# Table A columns, in the contract section-C order. selection_signal is
# free-text; the other five are enum-valued lists. design_selection_rule (how
# the experimental design/assay d is chosen) is the BED-central axis added for
# reviewer Item 2, kept separate from candidate_selection_rule (which candidate
# hypotheses h are chosen). generation_scope and formal_epistemic_utility_evidence
# are deliberately NOT columns.
POLICY_COLUMNS = (
    ("selection_signal", "Selection signal", None),
    ("control_dependence", "Follow-up (control) dependence", CONTROL_DEPENDENCE),
    ("selection_objective", "Selection-purpose facets", SELECTION_OBJECTIVE),
    ("candidate_selection_rule", "Candidate-selection rule", CANDIDATE_SELECTION_RULE),
    ("design_selection_rule", "Design-selection rule", DESIGN_SELECTION_RULE),
    ("candidate_execution_rule", "Candidate-execution rule", CANDIDATE_EXECUTION_RULE),
)


def order_by(values, ordering) -> list[str]:
    """Return the members of `values` present, in the canonical `ordering`."""
    present = set(values)
    ordered = [value for value in ordering if value in present]
    # any value outside the canonical order (should not happen once validated)
    ordered.extend(sorted(present - set(ordering)))
    return ordered


# ---------------------------------------------------------------------------
# Table A -- Policy (per case), contract section C
# ---------------------------------------------------------------------------


def build_policy_table(policy_by_case: dict[str, dict]) -> str:
    # Seven columns hold long unbreakable \texttt enum tokens (e.g.
    # hypothesis_model_discrimination, fixed_or_standard_design). The manuscript
    # wraps this float as a sidewaystable for extra width; on top of that, each
    # p{} column is \raggedright and, inside a scoped \begingroup, `\_` is made a
    # permissible line-break point so the long tokens wrap INSIDE their cell
    # instead of overflowing into (and physically overlapping) the neighbouring
    # column. The added design-selection column (reviewer Item 2) tightens the
    # per-column widths so the six p{} data columns still sum below \linewidth.
    rag = r">{\raggedright\arraybackslash}"
    columns = (
        r"l "
        + rag + r"p{0.19\linewidth} "
        + rag + r"p{0.14\linewidth} "
        + rag + r"p{0.17\linewidth} "
        + rag + r"p{0.13\linewidth} "
        + rag + r"p{0.14\linewidth} "
        + rag + r"p{0.13\linewidth}"
    )
    header = ["Case"] + [label for _key, label, _enum in POLICY_COLUMNS]
    lines = [
        r"\begingroup",
        r"\renewcommand{\arraystretch}{1.15}",
        # save the kernel underscore, then allow a line break after each one so
        # long \texttt enum tokens can wrap within a narrow p{} cell.
        r"\let\origunderscore\_",
        r"\renewcommand{\_}{\origunderscore\allowbreak}",
        r"\begin{tabular}{" + columns + "}",
        r"\toprule",
        " & ".join(header) + r" \\",
        r"\midrule",
    ]
    for case_id in CASE_IDS:
        record = policy_by_case[case_id]
        row = [case_id]
        for key, _label, enum in POLICY_COLUMNS:
            values = record[key]
            if enum is None:
                row.append(text_list(list(values)))
            else:
                row.append(mono_list(order_by(values, enum)))
        lines.append(" & ".join(row) + r" \\")
    lines.extend((r"\bottomrule", r"\end{tabular}", r"\endgroup", ""))
    body = "\n".join(lines)

    body += legend([
        r"Schema-v3 BED-lens decomposition of each case's experiment-selection policy",
        r"(charter B.4 / contract section B); an analytic decomposition, not a compliance label.",
        r"Each cell lists the enum values the bounded source reports for that axis; a multi-valued",
        r"axis is a set, not an ordering. The selection-purpose facets (the objective) are kept",
        r"separate from the candidate-selection, design-selection and candidate-execution rules, so",
        r"no objective is folded into a rule. The \emph{candidate-selection rule} (which candidate",
        r"hypotheses $h$ are chosen) and the \emph{design-selection rule} (how the experimental",
        r"design/assay $d$ is chosen) are separate axes -- the BED-central act of selecting the",
        r"design $d$ that best discriminates hypotheses under a cost is distinct from choosing which",
        r"$h$ to test, so an exhaustive candidate rule (e.g. C05 tests every hypothesis) is not",
        r"evidence about how $d$ is selected. No bounded source reports a \texttt{discrimination\_directed},",
        r"\texttt{information\_directed} or \texttt{cost\_directed} design; the reported designs are",
        r"\texttt{fixed\_or\_standard\_design} or \texttt{coverage\_or\_factorial} (a corpus-level",
        r"observation, not a per-case verdict). Two policy axes are recorded in the source data but",
        r"are not columns here: \emph{generation scope} (\texttt{fixed\_space} /",
        r"\texttt{search\_space\_expansion} / \texttt{candidate\_diversification}) is a G/S-level",
        r"provenance axis, and \emph{formal epistemic-utility evidence} is \texttt{not\_reported} for",
        r"all six cases.",
        # footnote (i), verbatim from contract section C
        r"\emph{Formal epistemic-utility evidence.} None of the bounded sources reports an explicit",
        r"posterior or expected-information-gain criterion; this is a corpus-level reporting",
        r"observation, not evidence of field-wide absence.",
    ])
    return body


SUGGESTED_POLICY_CAPTION = (
    "Policy decomposition (Table A), a schema-v3 BED-lens reading of each case's "
    "experiment-selection policy (charter B.4 / contract section B). Columns are the "
    "selection signal (free text) and five enum axes: the follow-up (control) "
    "dependence, the selection-purpose facets, and the separate candidate-selection, "
    "design-selection and candidate-execution rules. The action is $a=(h,d,P,f)$: the "
    "candidate-selection rule names which candidate hypotheses $h$ are chosen and the "
    "design-selection rule names how the experimental design/assay $d$ is chosen -- two "
    "distinct axes, so that testing every hypothesis is not read as evidence about how "
    "the design is selected. The selection-purpose facet (objective) is kept apart from "
    "all three rules, so no objective is folded into a rule -- e.g. C05 carries "
    "\\texttt{uncertainty\\_reduction} / \\texttt{hypothesis\\_model\\_discrimination} "
    "objectives yet an \\texttt{exhaustive} / \\texttt{all\\_selected} candidate rule (it "
    "tested every hypothesis) and, on the separate design axis, a "
    "\\texttt{fixed\\_or\\_standard\\_design} / \\texttt{coverage\\_or\\_factorial} design "
    "(a model-prescribed assay with a Latin-square layout, not a discrimination-directed "
    "experiment selection), whereas the score-directed cases (C01--C04, C06) are "
    "\\texttt{performance\\_improvement} with \\texttt{top\\_k\\_ranked} / "
    "\\texttt{threshold} / \\texttt{sequential\\_choice} candidate selection. No bounded "
    "source reports a \\texttt{discrimination\\_directed}, \\texttt{information\\_directed} "
    "or \\texttt{cost\\_directed} design (a corpus-level observation). generation\\_scope is "
    "not shown (a provenance axis) and formal epistemic-utility evidence is "
    "\\texttt{not\\_reported} for all six cases (footnote)."
)


# ---------------------------------------------------------------------------
# Table B1 -- Observation-evaluation boundary (case-level), contract section C
# ---------------------------------------------------------------------------

OV_BOUNDARY_VALUES = ("separated", "boundary_unreported", "merged", "n.a.")


def observation_evaluation_boundary(alignments: list[dict]) -> tuple[list[str], list[str], str]:
    """Case-level (observation_source, evaluation_target, O-V boundary).

    - observation source = source_role of (?, produces, observation) relations.
    - evaluation target  = target_role of (evaluation, evaluates, ?) relations.
    - O-V boundary reads the O_env<->V split carried by evaluation->observation
      boundary_status (rubric v5-rubric-3): separated if any such relation reports
      the split, boundary_unreported if such relations exist but none reports it,
      n.a. if the source describes no evaluation-of-observation relation. `merged`
      (observation and evaluation recombined into one step) is a defined category
      that the typed-relation schema forbids by construction, so it never arises.
    """
    obs_source: set[str] = set()
    eval_target: set[str] = set()
    eval_observation_boundaries: list[str] = []
    for alignment in alignments:
        if alignment.get("assertion_kind") != "functional_relation":
            continue
        source_role = alignment["source_role"]
        relation_type = alignment["relation_type"]
        target_role = alignment["target_role"]
        boundary_status = alignment["boundary_status"]
        if target_role == "observation" and relation_type == "produces":
            obs_source.add(source_role)
        if source_role == "evaluation" and relation_type == "evaluates":
            eval_target.add(target_role)
            if target_role == "observation":
                eval_observation_boundaries.append(boundary_status)
    if not eval_observation_boundaries:
        boundary = "n.a."
    elif "reported" in eval_observation_boundaries:
        boundary = "separated"
    else:
        boundary = "boundary_unreported"
    return sorted(obs_source), sorted(eval_target), boundary


def build_boundary_table(alignments_by_case: dict[str, list[dict]]) -> tuple[str, dict[str, str]]:
    columns = r"l p{0.26\linewidth} p{0.30\linewidth} p{0.18\linewidth}"
    header = ["Case", "Observation source", "Evaluation target", "O--V boundary"]
    lines = [r"\begin{tabular}{" + columns + "}", r"\toprule", " & ".join(header) + r" \\", r"\midrule"]
    verdicts: dict[str, str] = {}
    for case_id in CASE_IDS:
        obs_source, eval_target, boundary = observation_evaluation_boundary(alignments_by_case[case_id])
        verdicts[case_id] = boundary
        row = [case_id, mono_list(obs_source), mono_list(eval_target), mono(boundary)]
        lines.append(" & ".join(row) + r" \\")
    lines.extend((r"\bottomrule", r"\end{tabular}", ""))
    body = "\n".join(lines)

    body += legend([
        r"Case-level observation--evaluation boundary (contract section C).",
        r"\emph{Observation source} = the role(s) the bounded source names as producing an observation",
        r"($\cdot\to$\texttt{produces}$\to$\texttt{observation}); \texttt{observation} as a source denotes a",
        r"within-measurement transform whose upstream environment/execution origin the source leaves",
        r"unreported (the E--O\_env boundary is \texttt{boundary\_unreported}).",
        r"\emph{Evaluation target} = the role(s) an \texttt{evaluation}$\to$\texttt{evaluates}$\to\cdot$ relation acts on.",
        r"\emph{O--V boundary} $\in$ \{\texttt{separated}, \texttt{boundary\_unreported}, \texttt{merged}, \texttt{n.a.}\}",
        r"reads the O\_env--V split carried by the \texttt{evaluation}$\to$\texttt{observation} relations",
        r"(rubric v5-rubric-3): \texttt{separated} = the source reports that split (a distinct evaluation of a",
        r"distinct observation) in at least one relation; \texttt{boundary\_unreported} = such relations exist but",
        r"none reports the split; \texttt{merged} = observation and evaluation recombined into one step;",
        r"\texttt{n.a.} = no evaluation-of-observation relation. In this corpus \texttt{merged} and \texttt{n.a.} do not occur.",
    ])
    return body, verdicts


SUGGESTED_BOUNDARY_CAPTION = (
    "Observation--evaluation boundary (Table B1), read at case level to avoid a "
    "mostly-n.a. relation-level column (contract section C). For each case the table "
    "reports where observations originate, what evaluation acts on, and whether the "
    "source separates an observation from its subsequent evaluation. The O--V boundary "
    "is the O\\_env--V split carried by \\texttt{evaluation}$\\to$\\texttt{observation} "
    "relations: all six bounded sources report that split in at least one relation "
    "(\\texttt{separated}), which is the observation/evaluation distinction the "
    "framework turns on, populated from the source rather than assumed."
)


# ---------------------------------------------------------------------------
# Table B2 -- Relation / evidence (per functional relation), contract section C
# ---------------------------------------------------------------------------

# support_status and occurrence_resolution are kept as SEPARATE columns and are
# never merged. `n.a.` renders the schema's not_applicable. Canonical render
# orders (evidence mode is explicitly non-ordinal -- this order is only for
# stable rendering, not a ranking).
SUPPORT_ORDER = ("supported", "unresolved", "contradicted", "n.a.")
OCCURRENCE_ORDER = ("resolved", "unresolved", "n.a.")
EVIDENCE_MODE_ORDER = ("architecture", "capability", "procedure", "aggregate", "occurrence")


def _claim_tuple_sort_key(claim_tuple: tuple[str, str, str]) -> tuple[int, int, int]:
    """Stable render order for a (support, occurrence, mode) claim-tuple using the
    canonical axis orders (rendering only -- evidence mode is not an ordinal)."""
    support, occurrence, mode = claim_tuple

    def rank(value: str, ordering: tuple[str, ...]) -> int:
        return ordering.index(value) if value in ordering else len(ordering)

    return (rank(support, SUPPORT_ORDER), rank(occurrence, OCCURRENCE_ORDER), rank(mode, EVIDENCE_MODE_ORDER))


def na(value: str) -> str:
    return "n.a." if value == "not_applicable" else value


def evidence_mode(claim: dict) -> str:
    """Map a DerivedDecisionClaim to one of the five evidence modes (the kind of
    proposition the source supports). claim_scope carries architecture / procedure
    / aggregate_run / occurrence; the architecture scope splits by support_status
    into `capability` (reported only as a capability -> unresolved) and
    `architecture` (a supported structural claim)."""
    scope = claim["claim_scope"]
    if scope == "occurrence":
        return "occurrence"
    if scope == "aggregate_run":
        return "aggregate"
    if scope == "procedure":
        return "procedure"
    if scope == "architecture":
        return "capability" if claim["support_status"] == "unresolved" else "architecture"
    raise TableBuildError(f"{claim['claim_id']}: unknown claim_scope {scope!r}")


def relation_tuple(alignment: dict) -> tuple[str, str, str, str]:
    return (
        alignment["source_role"],
        alignment["relation_type"],
        alignment["target_role"],
        alignment["temporal_scope"],
    )


def relation_cell(tup: tuple[str, str, str, str]) -> str:
    source_role, relation_type, target_role, temporal_scope = tup
    arrow = r" $\to$ "
    return (
        mono(source_role) + arrow + mono(relation_type) + arrow + mono(target_role)
        + r" (" + mono(temporal_scope) + r")"
    )


def build_relations_table(
    claims_by_case: dict[str, list[dict]],
    alignments_by_case: dict[str, list[dict]],
) -> tuple[str, dict]:
    """One row per distinct (case, functional-relation tuple, support_status,
    occurrence_resolution, evidence_mode) claim-tuple, so the three evidence axes
    ON A ROW correspond to one another. A relation whose claims carry several
    distinct (support, occurrence, mode) combinations gets one row per combination,
    with the relation label repeated on each row (so the correspondence survives a
    page break and no reader has to re-pair three independent set-unions). Rows are
    grouped by case, then relation; within a relation the distinct claim-tuples are
    ordered by the canonical support / occurrence / evidence-mode orders. Emitted as
    a longtable: \\caption and \\label{tab:servo-v5-relations} are embedded in the
    first head, and the column header plus a "continued" notice repeat via
    \\endfirsthead/\\endhead/\\endfoot/\\endlastfoot on every page. The first evidence
    column is headed "Source support" (display only -- the underlying claim field
    stays support_status; OD-5)."""
    columns = r"l p{0.34\linewidth} p{0.15\linewidth} p{0.15\linewidth} p{0.16\linewidth}"
    header = ["Case", "Functional relation", "Source support", "Occurrence resolution", "Evidence mode"]
    header_row = " & ".join(header) + r" \\"
    lines = [
        r"\begin{longtable}{" + columns + "}",
        r"\caption{" + RELATIONS_CAPTION + r"}\label{tab:servo-v5-relations} \\",
        r"\toprule",
        header_row,
        r"\midrule",
        r"\endfirsthead",
        r"\multicolumn{5}{l}{\emph{Table B2 (continued)}} \\",
        r"\toprule",
        header_row,
        r"\midrule",
        r"\endhead",
        r"\midrule",
        r"\multicolumn{5}{r}{\emph{continued on next page}} \\",
        r"\endfoot",
        r"\bottomrule",
        r"\endlastfoot",
    ]

    rows_per_case: dict[str, int] = {}
    mode_counter: Counter = Counter()
    support_counter: Counter = Counter()
    occurrence_counter: Counter = Counter()
    total_rows = 0

    for index, case_id in enumerate(CASE_IDS):
        align_by_id = {a["alignment_id"]: a for a in alignments_by_case[case_id]}
        # group by relation tuple, collecting the DISTINCT (support, occurrence,
        # mode) claim-tuples each relation carries (first-seen order preserved,
        # canonically re-sorted at render time).
        order: list[tuple] = []
        groups: dict[tuple, list[tuple[str, str, str]]] = {}
        seen: dict[tuple, set[tuple[str, str, str]]] = {}
        for claim in claims_by_case[case_id]:
            used = claim["used_alignment_ids"]
            if len(used) != 1:
                raise TableBuildError(f"{claim['claim_id']}: expected exactly one used_alignment_id, found {len(used)}")
            alignment = align_by_id.get(used[0])
            if alignment is None:
                raise TableBuildError(f"{claim['claim_id']}: used_alignment_id {used[0]!r} not in servo_v5_alignments/{case_id}.json")
            if alignment.get("assertion_kind") != "functional_relation":
                raise TableBuildError(f"{claim['claim_id']}: Table B2 expects a functional_relation alignment, got {alignment.get('assertion_kind')!r}")
            tup = relation_tuple(alignment)
            support = na(claim["support_status"])
            occurrence = na(claim["occurrence_resolution"])
            mode = evidence_mode(claim)
            claim_tuple = (support, occurrence, mode)
            if tup not in groups:
                groups[tup] = []
                seen[tup] = set()
                order.append(tup)
            if claim_tuple not in seen[tup]:
                seen[tup].add(claim_tuple)
                groups[tup].append(claim_tuple)
            # counters count EVERY claim (cross_check sums evidence_mode == #claims)
            support_counter[support] += 1
            occurrence_counter[occurrence] += 1
            mode_counter[mode] += 1

        case_rows = 0
        for tup in sorted(order):
            relation_label = relation_cell(tup)
            for support, occurrence, mode in sorted(groups[tup], key=_claim_tuple_sort_key):
                # relation label repeated on every row so the row-level
                # correspondence is unambiguous and survives page breaks.
                row = [case_id, relation_label, mono(support), mono(occurrence), mono(mode)]
                lines.append(" & ".join(row) + r" \\")
                case_rows += 1
        rows_per_case[case_id] = case_rows
        total_rows += case_rows
        if index != len(CASE_IDS) - 1:
            lines.append(r"\midrule")

    lines.extend((r"\end{longtable}", ""))
    body = "\n".join(lines)

    body += legend([
        r"Per functional relation (contract section C): each row is one distinct",
        r"(support status, occurrence resolution, evidence mode) combination carried by the",
        r"DerivedDecisionClaims that use a relation of a given",
        r"(\texttt{source\_role}, \texttt{relation\_type}, \texttt{target\_role}, \texttt{temporal\_scope}) tuple",
        r"within a case, so the three axes on a row correspond; a relation with several combinations",
        r"spans several rows with its label repeated. Support status, occurrence resolution and evidence",
        r"mode are three separate columns and are never merged; support status uses \texttt{supported}",
        r"(not \texttt{resolved}). Domains: support status $\in$ \{\texttt{supported},",
        r"\texttt{unresolved}, \texttt{contradicted}, \texttt{n.a.}\}; occurrence resolution $\in$",
        r"\{\texttt{resolved}, \texttt{unresolved}, \texttt{n.a.}\}; evidence mode $\in$ \{\texttt{architecture},",
        r"\texttt{capability}, \texttt{procedure}, \texttt{aggregate}, \texttt{occurrence}\}.",
        # footnote (ii), verbatim mapping + non-ordinal statement from contract section C
        r"\emph{Evidence mode} maps: \texttt{architecture} $\to$ structural organization;",
        r"\texttt{capability} $\to$ what the system can or is designed to do;",
        r"\texttt{procedure} $\to$ specified operational sequence;",
        r"\texttt{aggregate} $\to$ repetition or result without event identity;",
        r"\texttt{occurrence} $\to$ bounded event-level instance.",
        r"Evidence modes identify the kind of proposition supported by the source and are not treated",
        r"as an ordinal scale of system quality or closure.",
    ])
    counts = {
        "rows_total": total_rows,
        "rows_per_case": rows_per_case,
        "evidence_mode": dict(mode_counter),
        "support_status": dict(support_counter),
        "occurrence_resolution": dict(occurrence_counter),
    }
    return body, counts


RELATIONS_CAPTION = (
    "Relation/evidence table (Table B2): each row is one distinct (source support, "
    "occurrence resolution, evidence mode) combination carried by a typed (source "
    "role, relation type, target role, temporal scope) relation, grouped by case, so "
    "the three axes on a row correspond; a relation with several combinations spans "
    "several rows with its label repeated. Source support, occurrence resolution, and "
    "evidence mode are kept separate. Evidence mode names the kind of proposition the "
    "source supports and is not an ordinal scale of system quality or closure."
)


# ---------------------------------------------------------------------------
# Claims projection CSV (unchanged artifact, still useful for cross-reference)
# ---------------------------------------------------------------------------


def relation_summary(alignment: dict) -> str:
    if alignment["assertion_kind"] == "functional_relation":
        return f"{alignment['source_role']} --{alignment['relation_type']}--> {alignment['target_role']}"
    return f"{alignment['source_term']} => {alignment['component']}"


def build_projection(claims_by_case: dict[str, list[dict]], alignments_by_case: dict[str, list[dict]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for case_id in CASE_IDS:
        align_by_id = {alignment["alignment_id"]: alignment for alignment in alignments_by_case[case_id]}
        for claim in claims_by_case[case_id]:
            used = claim["used_alignment_ids"]
            if len(used) != 1:
                raise TableBuildError(f"{claim['claim_id']}: expected exactly one used_alignment_id, found {len(used)}")
            alignment = align_by_id.get(used[0])
            if alignment is None:
                raise TableBuildError(f"{claim['claim_id']}: used_alignment_id {used[0]!r} not found in servo_v5_alignments/{case_id}.json")
            rows.append(
                {
                    "case_id": case_id,
                    "claim_id": claim["claim_id"],
                    "relation_summary": relation_summary(alignment),
                    "support_status": claim["support_status"],
                    "claim_scope": claim["claim_scope"],
                    "occurrence_resolution": claim["occurrence_resolution"],
                    "evidence_mode": evidence_mode(claim),
                    "alignment_kind": claim["alignment_kind"],
                }
            )
    return rows


PROJECTION_FIELDNAMES = (
    "case_id", "claim_id", "relation_summary", "support_status", "claim_scope",
    "occurrence_resolution", "evidence_mode", "alignment_kind",
)


# ---------------------------------------------------------------------------
# Validation and cross-checks
# ---------------------------------------------------------------------------

POLICY_ENUMS = {
    "control_dependence": CONTROL_DEPENDENCE,
    "selection_objective": SELECTION_OBJECTIVE,
    "generation_scope": GENERATION_SCOPE,
    "candidate_selection_rule": CANDIDATE_SELECTION_RULE,
    "design_selection_rule": DESIGN_SELECTION_RULE,
    "candidate_execution_rule": CANDIDATE_EXECUTION_RULE,
}


def validate(claims_by_case: dict[str, list[dict]], alignments_by_case: dict[str, list[dict]], policy_by_case: dict[str, dict]) -> None:
    seen_claim_ids: set[str] = set()
    for case_id in CASE_IDS:
        claims = claims_by_case[case_id]
        if not claims:
            raise TableBuildError(f"{case_id}: no claims")
        align_ids = {a["alignment_id"] for a in alignments_by_case[case_id]}
        for claim in claims:
            claim_id = claim["claim_id"]
            if claim_id in seen_claim_ids:
                raise TableBuildError(f"duplicate claim_id: {claim_id}")
            seen_claim_ids.add(claim_id)
            for field in ("support_status", "claim_scope", "alignment_kind", "occurrence_resolution", "used_alignment_ids", "used_proposition_ids"):
                if field not in claim:
                    raise TableBuildError(f"{claim_id}: missing field {field}")
            for alignment_id in claim["used_alignment_ids"]:
                if alignment_id not in align_ids:
                    raise TableBuildError(f"{claim_id}: used_alignment_id {alignment_id!r} not in servo_v5_alignments/{case_id}.json")
        record = policy_by_case[case_id]
        for axis_id, values in POLICY_ENUMS.items():
            axis_value = record.get(axis_id)
            if not isinstance(axis_value, list) or not axis_value:
                raise TableBuildError(f"{case_id}: policy axis {axis_id} must be a non-empty list")
            if not set(axis_value) <= set(values):
                raise TableBuildError(f"{case_id}: unknown {axis_id} value in {axis_value}")
        signals = record.get("selection_signal")
        if not isinstance(signals, list) or not signals:
            raise TableBuildError(f"{case_id}: policy selection_signal must be a non-empty list")
        evidence = record.get("formal_epistemic_utility_evidence")
        if not isinstance(evidence, str) or not evidence.strip():
            raise TableBuildError(f"{case_id}: formal_epistemic_utility_evidence must be a non-empty string")


def cross_check(claims_by_case: dict[str, list[dict]], relation_counts: dict) -> dict:
    all_claims = [claim for claims in claims_by_case.values() for claim in claims]
    if len(all_claims) != 240:
        raise TableBuildError(f"expected 240 claims across six cases, found {len(all_claims)}")
    occurrence_established_total = sum(
        1 for claim in all_claims
        if claim["support_status"] == "supported" and claim["claim_scope"] == "occurrence" and claim["occurrence_resolution"] == "resolved"
    )
    if occurrence_established_total != 35:
        raise TableBuildError(f"expected 35 globally (supported, occurrence, resolved) claims, found {occurrence_established_total}")
    mode_total = sum(relation_counts["evidence_mode"].values())
    if mode_total != len(all_claims):
        raise TableBuildError(f"evidence-mode total {mode_total} != {len(all_claims)} claims")
    return {
        "claims_total": len(all_claims),
        "claims_occurrence_established_global": occurrence_established_total,
    }


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    claims_by_case = load_case_family(CLAIMS_DIR, "claims")
    alignments_by_case = load_case_family(ALIGNMENTS_DIR, "alignments")
    policy_by_case = load_policy()

    validate(claims_by_case, alignments_by_case, policy_by_case)

    policy_header = file_header_comment(
        [
            "AUTO-GENERATED by analysis/build_servo_v5_tables.py. Do not edit by hand.",
            "",
            "Table A -- Policy (per case). Suggested manuscript \\caption (T11/G4 to place",
            "in main_post-submit.tex, table* around \\input{analysis/tbl-servo-v5-policy.tex}):",
            "",
        ]
        + [SUGGESTED_POLICY_CAPTION]
    )
    policy_tex = policy_header + build_policy_table(policy_by_case)

    boundary_header = file_header_comment(
        [
            "AUTO-GENERATED by analysis/build_servo_v5_tables.py. Do not edit by hand.",
            "",
            "Table B1 -- Observation-evaluation boundary (case-level). Suggested manuscript",
            "\\caption (T11/G4, table* around \\input{analysis/tbl-servo-v5-boundary.tex}):",
            "",
        ]
        + [SUGGESTED_BOUNDARY_CAPTION]
    )
    boundary_body, boundary_verdicts = build_boundary_table(alignments_by_case)
    boundary_tex = boundary_header + boundary_body

    relations_header = file_header_comment(
        [
            "AUTO-GENERATED by analysis/build_servo_v5_tables.py. Do not edit by hand.",
            "",
            "Table B2 -- Relation / evidence (per functional relation), a longtable so it",
            "breaks across pages. \\caption and \\label{tab:servo-v5-relations} are",
            "embedded in the table itself (T11/G4) -- place directly with",
            "\\input{analysis/tbl-servo-v5-relations.tex}, no table*/tabular wrapper",
            "needed. Caption text:",
            "",
        ]
        + [RELATIONS_CAPTION]
    )
    relations_body, relation_counts = build_relations_table(claims_by_case, alignments_by_case)
    relations_tex = relations_header + relations_body

    claim_counts = cross_check(claims_by_case, relation_counts)

    outputs = {
        "tbl-servo-v5-policy.tex": policy_tex,
        "tbl-servo-v5-boundary.tex": boundary_tex,
        "tbl-servo-v5-relations.tex": relations_tex,
    }
    for name, content in outputs.items():
        (ROOT / name).write_text(content, encoding="utf-8")

    projection_rows = build_projection(claims_by_case, alignments_by_case)
    projection_path = ROOT / "servo_v5_claims_projection.csv"
    # newline="" stops the file layer translating; lineterminator="\n" makes the
    # csv module itself emit LF (not its default CRLF), so the generated CSV passes
    # git's CRLF check on commit.
    with projection_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PROJECTION_FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(projection_rows)

    manifest_inputs = {}
    for dirpath in (CLAIMS_DIR, ALIGNMENTS_DIR, POLICY_DIR):
        for case_id in CASE_IDS:
            path = dirpath / f"{case_id}.json"
            manifest_inputs[f"{dirpath.name}/{path.name}"] = digest(path)

    manifest = {
        "schema": "servo_v5_evidence_layer_manifest",
        "generator": "analysis/build_servo_v5_tables.py",
        "generator_sha256": digest(Path(__file__)),
        "inputs": manifest_inputs,
        "outputs": {
            **{name: digest(ROOT / name) for name in sorted(outputs)},
            "servo_v5_claims_projection.csv": digest(projection_path),
        },
        "counts": {
            "cases": len(CASE_IDS),
            "claims_total": claim_counts["claims_total"],
            "claims_occurrence_established_global": claim_counts["claims_occurrence_established_global"],
            "policy_formal_epistemic_utility_reported_cases": sum(
                1
                for case_id in CASE_IDS
                if policy_by_case[case_id]["formal_epistemic_utility_evidence"].strip().lower() != "not_reported"
            ),
            "boundary_verdicts": boundary_verdicts,
            "boundary_verdict_totals": dict(Counter(boundary_verdicts.values())),
            "relations_rows_total": relation_counts["rows_total"],
            "relations_rows_per_case": relation_counts["rows_per_case"],
            "relations_evidence_mode": relation_counts["evidence_mode"],
            "relations_support_status": relation_counts["support_status"],
            "relations_occurrence_resolution": relation_counts["occurrence_resolution"],
        },
        "notes": [
            "Three tables replace the retired 4-predicate closure status matrix (charter C.1/C.4): "
            "Table A (policy, per case), Table B1 (observation-evaluation boundary, case-level), "
            "Table B2 (relation/evidence, per functional relation). This script does not read or "
            "reconstruct the retired predicate enum.",
            "Table A has no explicit_bed / BED-yes-no column and does not show generation_scope; "
            "formal_epistemic_utility_evidence is a corpus-level footnote (not_reported for all six).",
            "Table B2 keeps support_status and occurrence_resolution as separate columns and uses "
            "`supported` (not `resolved`) for support status; evidence mode is non-ordinal.",
        ],
    }
    (ROOT / "servo_v5_evidence_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("wrote:", ", ".join(sorted(outputs)))
    print("wrote: servo_v5_claims_projection.csv (", len(projection_rows), "rows )")
    print("wrote: servo_v5_evidence_manifest.json")
    print("boundary verdicts:", boundary_verdicts)
    print("relations rows total:", relation_counts["rows_total"], "per case:", relation_counts["rows_per_case"])
    print("evidence-mode distribution:", relation_counts["evidence_mode"])
    print(
        "policy formal-epistemic-utility reported cases:",
        manifest["counts"]["policy_formal_epistemic_utility_reported_cases"],
        "/",
        len(CASE_IDS),
    )


if __name__ == "__main__":
    main()
