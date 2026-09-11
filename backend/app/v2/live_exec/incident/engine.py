"""BE-12E incident engine (BO-V2-BE12E-001 §1.d).

RECORD SHAPE per DR-1 (§1.d.1): severity CHECK-closed SEV-1..SEV-4;
instruments_pinned non-empty (empty array => typed
`incident_instruments_absent` — an incident names what it touches);
recovery_path non-empty; status open/closed; digest recomputed on open
AND close (R-3.1).

LIFECYCLE LAW (§1.d.2, the valve dance as proven by the kill-switch):
OPEN = INSERT 'open'. CLOSE = 'open' => valve => 'closed' (stamping
closed_at/closed_by) — THE single sanctioned close path. Close of
unknown => `incident_not_open`; close of closed =>
`incident_already_closed`; both NON-FIRING.

NO SELF-ACTIVITY (§1.d.4): this package never opens its own rows; a
parity_break may be QUOTED by an operator, never linked by the machine.
"""

from __future__ import annotations

import hashlib
import json
from typing import Final
from uuid import uuid4

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_live_exec_incident import V2LiveExecIncident
from app.v2.live_exec.intents import LiveExecRefused
from app.v2.temporal.validation import utc_now

# Closed vocabularies (§1.d.1/§1.f.1; schema CHECKs mirror them).
INCIDENT_SEVERITIES: Final = ("SEV-1", "SEV-2", "SEV-3", "SEV-4")
INCIDENT_STATUSES: Final = ("open", "closed")
# CR-1 (V2-BE12E-DEL-001): `incident_severity_invalid` ENUMERATED into
# the closed law — the wire's edge-typed severity refusal is now a
# register-recoverable citizen; the api edge cites THIS constant.
INCIDENT_REFUSALS: Final = ("incident_not_open",
                            "incident_already_closed",
                            "incident_instruments_absent",
                            "incident_severity_invalid")
INCIDENT_SEVERITY_INVALID: Final = "incident_severity_invalid"
INCIDENT_NOT_OPEN: Final = "incident_not_open"

_GUARD_NAME: Final = "v2_live_exec_incident_immutable_update"
# CR-1 §6.4 rider (by election; the file already moves for DEL-001):
# the recreated-guard DDL body aligned to the migration's single-line
# form — full-text byte-equality with the migration trigger, the 12D
# kill-switch precedent restored.
_GUARD_SQL: Final = """
    CREATE TRIGGER v2_live_exec_incident_immutable_update
    BEFORE UPDATE ON v2_live_exec_incident
    BEGIN
        SELECT RAISE(ABORT, 'V2 live exec incidents are immutable; UPDATE prohibited');
    END;
"""


def _canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      default=str)


def incident_digest(facts: dict) -> str:
    """Register-facing digest incl. status lifecycle stamps (recomputed
    on open AND on close — coupon re-derives)."""
    return hashlib.sha256(_canonical(facts).encode("utf-8")).hexdigest()


async def open_incident(
    session: AsyncSession, *, severity: str, instruments_pinned: list,
    recovery_path: str, opened_by: str, actor_id: str, mode: str,
    operator_id: str, step_up_ref: str | None = None,
    correlation_id: str | None = None,
) -> V2LiveExecIncident:
    """OPEN = INSERT 'open' (operator confirm-rank verb)."""
    if not instruments_pinned:
        raise LiveExecRefused("incident_instruments_absent", [
            {"failing": "instruments_pinned",
             "note": "an incident names what it touches (DR-1 shape;"
                     " empty array banned)"}])
    instruments = sorted(str(i) for i in instruments_pinned)
    facts = {"severity": severity, "instruments_pinned": instruments,
             "recovery_path": recovery_path, "status": "open",
             "opened_by": opened_by, "closed_at": None,
             "closed_by": None, "mode": mode}
    row = V2LiveExecIncident(
        id=str(uuid4()), opened_by=opened_by, severity=severity,
        instruments_pinned=instruments, recovery_path=recovery_path,
        status="open", digest=incident_digest(facts),
        step_up_ref=step_up_ref,
        actor_id=actor_id, data_class="evidence", mode=mode,
        operator_id=operator_id, correlation_id=correlation_id)
    session.add(row)
    await session.flush()
    return row


async def close_incident(
    session: AsyncSession, *, incident_id: str, closed_by: str,
    actor_id: str, step_up_ref: str, operator_id: str,
) -> dict:
    """CLOSE — THE single sanctioned close path (valve dance)."""
    row = (await session.execute(
        select(V2LiveExecIncident)
        .where(V2LiveExecIncident.id == incident_id))).scalars().first()
    if row is None:
        raise LiveExecRefused("incident_not_open", [
            {"failing": "incident_id",
             "note": "no incident carries this id (non-firing)"}])
    if row.status == "closed":
        raise LiveExecRefused("incident_already_closed", [
            {"failing": "status", "standing": "closed",
             "standing_closed_by": row.closed_by,
             "note": "an incident closes exactly once (non-firing)"}])
    closed_at = utc_now()
    facts = {"severity": row.severity,
             "instruments_pinned": row.instruments_pinned,
             "recovery_path": row.recovery_path, "status": "closed",
             "opened_by": row.opened_by,
             "closed_at": str(closed_at), "closed_by": closed_by,
             "mode": row.mode}
    new_digest = incident_digest(facts)
    # the valve dance: drop UPDATE guard -> ONE transition -> recreate
    # -> verify-or-die (the kill-switch-proven house pattern)
    await session.execute(text(f"DROP TRIGGER IF EXISTS {_GUARD_NAME}"))
    await session.execute(text(
        "UPDATE v2_live_exec_incident SET status = 'closed',"
        " closed_at = :ca, closed_by = :cb, digest = :d,"
        " actor_id = :a, step_up_ref = :u, operator_id = :o"
        " WHERE id = :i AND status = 'open'"
    ).bindparams(ca=closed_at, cb=closed_by, d=new_digest, a=actor_id,
                 u=step_up_ref, o=operator_id, i=incident_id))
    await session.execute(text(_GUARD_SQL))
    restored = (await session.execute(text(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'"
        " AND name = :n").bindparams(n=_GUARD_NAME))).scalar_one()
    if restored != 1:
        raise RuntimeError(
            "incident valve guard NOT restored - transaction must die")
    return {"incident_id": incident_id, "status": "closed",
            "closed_by": closed_by, "digest": new_digest}
