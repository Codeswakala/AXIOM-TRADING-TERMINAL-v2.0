"""BE-7 typed contracts — vocabularies and the P-9 result-class law.

The four-class taxonomy exists here; ONLY backtest/simulation are
constructible in this band. `paper`/`live` are typed refusals at every
construction point AND absent from the DDL CHECK (schema-impossible).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.v2.research_governance.contracts import DATA_CLASSES

# Single taxonomy — shared lineage, no fork (REQ-1.12).
RJ_DATA_CLASSES = DATA_CLASSES
RJ_FIRST_LANDING_DATA_CLASSES = ("synthetic", "simulated")

# P-9: the full taxonomy vs the constructible set.
RESULT_CLASS_TAXONOMY = ("backtest", "simulation", "paper", "live")
CONSTRUCTIBLE_RESULT_CLASSES = ("backtest", "simulation")

REGISTRATION_OUTCOMES = ("registered", "reused", "refused")
# CR-V2-BE-7-001 F-1: the v1 cost-unit vocabulary. The replay engine's
# `apply_costs` accepts exactly these two units; registration refuses
# anything else (typed + durably audited) so no lawfully registered cost
# model can reach the engine's unknown-unit branch.
COST_UNITS_V1 = ("price", "fraction")
LIFECYCLE_STATES = ("draft", "registered", "retired")
JOB_STATES = ("queued", "running", "succeeded", "failed", "cancelled")
JOB_TERMINAL_STATES = ("succeeded", "failed", "cancelled")
ATTEMPT_OUTCOMES = ("succeeded", "failed", "cancelled")
SCHEDULE_KINDS_V1 = ("manual",)  # C4: anything else is a typed refusal

# C2: the exact mutable column set on v2_research_job (allow-list constant;
# asserted by test — Part 10.1).
JOB_MUTABLE_COLUMNS = frozenset(
    {"job_state", "attempt_count", "output_ref", "failure"})
# Part 10.1: the runner's writable-table allow-list.
RUNNER_INSERT_TABLES = frozenset(
    {"v2_research_result", "v2_research_job_attempt",
     "v2_audit_event", "v2_lineage_record"})
RUNNER_UPDATE_TABLES = frozenset({"v2_research_job"})


class ResultClassRefused(Exception):
    """P-9 typed refusal: paper/live are not constructible in BE-7."""

    def __init__(self, requested: str) -> None:
        self.requested = requested
        super().__init__(
            f"result class '{requested}' is not constructible in band BE-7"
            f" — constructible set: {CONSTRUCTIBLE_RESULT_CLASSES}"
        )


def require_constructible_result_class(result_class: str) -> str:
    """Every construction point calls this BEFORE touching the DB."""
    if result_class not in RESULT_CLASS_TAXONOMY:
        raise ResultClassRefused(result_class)
    if result_class not in CONSTRUCTIBLE_RESULT_CLASSES:
        raise ResultClassRefused(result_class)
    return result_class


@dataclass(frozen=True)
class TypedOutcome:
    """Uniform typed outcome for registration/submission writers."""

    outcome: str
    reasons: list = field(default_factory=list)
    record_id: str | None = None

    @property
    def refused(self) -> bool:
        return self.outcome == "refused"
