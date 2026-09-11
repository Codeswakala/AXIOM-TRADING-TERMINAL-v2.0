"""BE-12A eligibility engine (BO-V2-BE12A-001 §1.c).

Account + instrument + session checks with typed refusals
(`account_ineligible`, `instrument_ineligible`, `session_ineligible`,
`basis_stale` — BOP law: the basis must be PRESENT, not stale).
Pre-trade risk: money-units sizing inherited from the BE-11
flat-account law; decline verbs typed. This act carries NO live
submission (12B).

Basis facts arrive as ONE read from the BE-9 projection (read-only
wall law) — the BE-11 consistency-ARM pattern; this module never
touches a provider.
"""

from __future__ import annotations

from typing import Final

from app.v2.live_exec.intents import LiveExecRefused

# Closed refusal vocabularies (wording law; CWS-recoverable ids).
ELIGIBILITY_REFUSALS: Final = (
    "account_ineligible", "instrument_ineligible",
    "session_ineligible", "basis_stale",
)
# Closed eligibility answer states.
ELIGIBILITY_STATES: Final = ("eligible", "refused")


def require_eligibility(
    *, account_present: bool, account_posture_class: str | None,
    instrument_mapped: bool, session_open: bool,
    basis_present: bool, basis_age_hours: float | None,
    max_age_hours: float,
) -> dict:
    """All checks or first typed refusal; answer is a record of state."""
    if not account_present or account_posture_class is None:
        raise LiveExecRefused("account_ineligible", [
            {"failing": "account",
             "note": "no synced account posture on the lineage"}])
    if not instrument_mapped:
        raise LiveExecRefused("instrument_ineligible", [
            {"failing": "instrument",
             "note": "instrument absent from the sealed symbol map"}])
    if not session_open:
        raise LiveExecRefused("session_ineligible", [
            {"failing": "session",
             "note": "market session closed for the mapped venue"}])
    if not basis_present or basis_age_hours is None:
        raise LiveExecRefused("basis_stale", [
            {"failing": "basis",
             "note": "BOP law: basis must be PRESENT — absence refuses"
                     " on the staleness arm, never silently proceeds"}])
    if basis_age_hours > max_age_hours:
        raise LiveExecRefused("basis_stale", [
            {"failing": "basis_age_hours", "observed": basis_age_hours,
             "seeded_max": max_age_hours}])
    return {"eligibility_state": "eligible"}
