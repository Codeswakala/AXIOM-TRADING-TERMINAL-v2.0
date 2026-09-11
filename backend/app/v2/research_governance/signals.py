"""BE-5 U-4 signal writer service (BO-V2-BE-5-001 T-8).

The ONLY signal creation path. Structural vs predictive separately typed;
withheld/expired/refused are permanent typed records (never silent drops);
predictive without an eligible current governance record => refused;
`historical_real`/`live` data classes refused at first landing (data
honesty); RESEARCH mode enforced by the API layer, re-checked here.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_research_governance import V2MlGovernanceRecord
from app.db.models.v2_signal import V2SignalRecord, V2SignalStateEvent
from app.v2.research_governance.contracts import (
    FIRST_LANDING_DATA_CLASSES,
    SIGNAL_FAMILIES,
)

_ALLOWED_MODES = ("RESEARCH",)


@dataclass(frozen=True)
class SignalRequest:
    family: str
    signal_type: str
    instrument_id: str
    timeframe: str
    payload: dict | None
    uncertainty: dict | None
    limitations: dict
    source_family_refs: dict
    governance_record_id: str | None
    data_class: str
    as_of: datetime
    expires_at: datetime | None
    mode: str
    operator_id: str
    correlation_id: str | None


@dataclass(frozen=True)
class SignalResult:
    record: V2SignalRecord
    state: str
    reasons: list


async def _current_governance(
    session: AsyncSession, governance_record_id: str | None
) -> tuple[V2MlGovernanceRecord | None, bool]:
    """Resolve the record and whether it is CURRENT (greatest record_seq
    for its artifact — the P-1/C-1 currency projection)."""
    if governance_record_id is None:
        return None, False
    result = await session.execute(
        select(V2MlGovernanceRecord).where(
            V2MlGovernanceRecord.id == governance_record_id
        )
    )
    record = result.scalar_one_or_none()
    if record is None:
        return None, False
    newest = (await session.execute(
        select(V2MlGovernanceRecord)
        .where(V2MlGovernanceRecord.model_artifact_id
               == record.model_artifact_id)
        .order_by(V2MlGovernanceRecord.record_seq.desc())
    )).scalars().first()
    return record, newest is not None and newest.id == record.id


def _refusal_reasons(req: SignalRequest,
                     governance: V2MlGovernanceRecord | None,
                     governance_is_current: bool) -> list:
    reasons: list = []
    if req.family not in SIGNAL_FAMILIES:
        reasons.append({"failing": "family", "value": req.family})
    if req.mode not in _ALLOWED_MODES:
        reasons.append({"failing": "mode", "value": req.mode,
                        "required": "RESEARCH"})
    # Data honesty: first-landing restriction (typed refusal, never relabel)
    if req.data_class not in FIRST_LANDING_DATA_CLASSES:
        reasons.append({
            "failing": "data_class", "value": req.data_class,
            "required": list(FIRST_LANDING_DATA_CLASSES),
            "note": "historical_real/live unreachable until the corpus"
                    " track lands (plan Part 6.7)",
        })
    if not req.source_family_refs:
        reasons.append({"failing": "source_family_refs", "value": "empty"})
    if req.family == "predictive":
        if req.uncertainty is None or not req.uncertainty:
            reasons.append({"failing": "uncertainty",
                            "required": "mandatory for predictive"})
        if governance is None:
            reasons.append({"failing": "governance_record_id",
                            "required": "resolvable current record"})
        else:
            if not governance_is_current:
                # C-1 currency projection: a row with a greater
                # record_seq exists — this generation is superseded
                reasons.append({"failing": "governance_record",
                                "value": "superseded generation — not current"})
            if governance.eligibility_status != "eligible":
                reasons.append({"failing": "governance.eligibility_status",
                                "value": governance.eligibility_status,
                                "required": "eligible"})
    return reasons


async def emit_signal(session: AsyncSession, req: SignalRequest) -> SignalResult:
    """Create the signal record: `emitted` on a clean pass, otherwise a
    PERMANENT `refused` record with typed reasons. Nothing is dropped."""
    governance, is_current = await _current_governance(
        session, req.governance_record_id)
    reasons = _refusal_reasons(req, governance, is_current)
    state = "emitted" if not reasons else "refused"

    uncertainty = req.uncertainty
    if req.family == "structural" and not uncertainty:
        uncertainty = {"basis": "deterministic"}

    record = V2SignalRecord(
        family=req.family if req.family in SIGNAL_FAMILIES else "predictive",
        signal_type=req.signal_type,
        instrument_id=req.instrument_id,
        timeframe=req.timeframe,
        state=state,
        state_reason={"reasons": reasons} if reasons else None,
        payload=req.payload if state == "emitted" else None,  # nothing fabricated
        uncertainty=uncertainty or {"basis": "unspecified"},
        limitations=req.limitations,
        source_family_refs=req.source_family_refs,
        governance_record_id=req.governance_record_id,
        data_class=req.data_class,
        as_of=req.as_of,
        expires_at=req.expires_at,
        mode=req.mode,
        operator_id=req.operator_id,
        correlation_id=req.correlation_id,
    )
    session.add(record)
    await session.flush()

    session.add(V2SignalStateEvent(
        signal_record_id=record.id,
        event_type=state,
        from_state="none",
        to_state=state,
        reason={"reasons": reasons} if reasons else {"clean": True},
        mode=req.mode,
        actor_id=req.operator_id,
        operator_id=req.operator_id,
        correlation_id=req.correlation_id,
    ))
    await session.flush()
    return SignalResult(record=record, state=state, reasons=reasons)


async def expire_signal(
    session: AsyncSession, *, signal: V2SignalRecord, as_of: datetime,
    actor_id: str, correlation_id: str | None,
) -> V2SignalStateEvent | None:
    """Expiry = appended state event (the record row is immutable; the
    projected state is the latest event). Only emitted signals expire."""
    if signal.state != "emitted":
        return None
    if signal.expires_at is None or as_of <= signal.expires_at.replace(
            tzinfo=signal.expires_at.tzinfo or as_of.tzinfo):
        return None
    event = V2SignalStateEvent(
        signal_record_id=signal.id,
        event_type="expired",
        from_state="emitted",
        to_state="expired",
        reason={"expired_at": as_of.isoformat(),
                "expires_at": signal.expires_at.isoformat()},
        mode=signal.mode,
        actor_id=actor_id,
        operator_id=signal.operator_id,
        correlation_id=correlation_id,
    )
    session.add(event)
    await session.flush()
    return event


async def projected_state(session: AsyncSession, signal_id: str) -> str | None:
    """Current state = the latest state event for the signal."""
    result = await session.execute(
        select(V2SignalStateEvent)
        .where(V2SignalStateEvent.signal_record_id == signal_id)
        .order_by(V2SignalStateEvent.created_at.desc(),
                  V2SignalStateEvent.id.desc())
    )
    latest = result.scalars().first()
    return latest.to_state if latest else None
