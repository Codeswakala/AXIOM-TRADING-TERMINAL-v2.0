"""BE-12D kill-switch engine (BO-V2-BE12D-001 §1.c).

THE VALVE LAW (§1.c.1): the guard pair prohibits UPDATE/DELETE at
schema; the ONLY legal transitions run through `_valve()` — the house
dance proven by the compver delete-guard: drop the UPDATE guard →
perform exactly ONE transition → recreate the guard → verify restored,
hard-fail otherwise. Any transition outside the valve dies on the
guard (coupon-witnessed inversion).

LIFECYCLE LAW (§1.c.2), every cell typed:
  arm   : no row ⇒ INSERT 'armed' · 'cleared' ⇒ valve ⇒ 'armed'
          · 'armed'|'pulled' ⇒ typed `killswitch_armed`, NON-FIRING
  pull  : 'armed' ⇒ valve ⇒ 'pulled' · anything else ⇒
          `killswitch_state_invalid` typed
  clear : 'armed'|'pulled' ⇒ valve ⇒ 'cleared' (THE single sanctioned
          clear path — no other clear exists anywhere)
          · no row ⇒ the `intact` no-op shape (a state, never invented)
Each transition stamps actor/step_up/operator refs (R-3.4 carriage;
second FACTOR, never second actor).

L5 (§1.c.3): `killswitch_engaged()` — no row or 'cleared' ⇒ NOT armed;
'armed'|'pulled' ⇒ armed.
"""

from __future__ import annotations

from typing import Final
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_live_killswitch import V2LiveKillSwitch
from app.v2.live_exec.intents import LiveExecRefused

# Closed lifecycle vocabulary (state nouns; schema CHECK mirrors it).
KILLSWITCH_STATES: Final = ("armed", "pulled", "cleared")

# 12D governor refusal ids (closed; `killswitch_armed` is BY DESIGN the
# SAME token as the L5 lock — the arm-while-engaged refusal).
GOVERNOR_REFUSALS: Final = ("killswitch_armed", "killswitch_state_invalid")

_GUARD_NAME: Final = "v2_live_kill_switch_immutable_update"
_GUARD_SQL: Final = """
    CREATE TRIGGER v2_live_kill_switch_immutable_update
    BEFORE UPDATE ON v2_live_kill_switch
    BEGIN
        SELECT RAISE(ABORT,
            'V2 live kill switch is immutable; UPDATE prohibited');
    END;
"""


async def _sole_row(session: AsyncSession) -> V2LiveKillSwitch | None:
    from sqlalchemy import select
    return (await session.execute(
        select(V2LiveKillSwitch)
        .where(V2LiveKillSwitch.sole == "SOLE"))).scalars().first()


async def killswitch_state(session: AsyncSession) -> str | None:
    """The sole-row status; None = no row (the intact resting state)."""
    row = await _sole_row(session)
    return None if row is None else row.status


async def killswitch_engaged(session: AsyncSession) -> bool:
    """THE L5 FACT READER: 'armed'|'pulled' => engaged."""
    status = await killswitch_state(session)
    return status in ("armed", "pulled")


async def _valve(session: AsyncSession, new_status: str,
                 actor_id: str, step_up_ref: str,
                 operator_id: str) -> None:
    """THE single sanctioned valve: drop guard -> ONE transition ->
    recreate guard -> verify restored, hard-fail otherwise."""
    await session.execute(text(f"DROP TRIGGER IF EXISTS {_GUARD_NAME}"))
    await session.execute(text(
        "UPDATE v2_live_kill_switch SET status = :s, actor_id = :a,"
        " step_up_ref = :u, operator_id = :o WHERE sole = 'SOLE'"
    ).bindparams(s=new_status, a=actor_id, u=step_up_ref, o=operator_id))
    await session.execute(text(_GUARD_SQL))
    restored = (await session.execute(text(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'"
        " AND name = :n").bindparams(n=_GUARD_NAME))).scalar_one()
    if restored != 1:
        raise RuntimeError(
            "kill-switch valve guard NOT restored - transaction must die")


async def governor_arm(session: AsyncSession, *, actor_id: str,
                       step_up_ref: str, operator_id: str,
                       correlation_id: str | None = None) -> str:
    status = await killswitch_state(session)
    if status in ("armed", "pulled"):
        raise LiveExecRefused("killswitch_armed", [
            {"failing": "status", "standing": status,
             "note": "re-arm blocked until cleared (DR-1 law;"
                     " BO-V2-BE12D-001 SS1.c.2) - non-firing"}])
    if status is None:
        session.add(V2LiveKillSwitch(
            id=str(uuid4()), sole="SOLE", status="armed",
            step_up_ref=step_up_ref, actor_id=actor_id,
            data_class="evidence", mode="RESEARCH",
            operator_id=operator_id, correlation_id=correlation_id))
        await session.flush()
        return "armed"
    # status == 'cleared': re-arm through the valve
    await _valve(session, "armed", actor_id, step_up_ref, operator_id)
    return "armed"


async def governor_pull(session: AsyncSession, *, actor_id: str,
                        step_up_ref: str, operator_id: str) -> str:
    status = await killswitch_state(session)
    if status != "armed":
        raise LiveExecRefused("killswitch_state_invalid", [
            {"failing": "status", "standing": status,
             "asked": "pull",
             "note": "pull applies to the 'armed' state only"}])
    await _valve(session, "pulled", actor_id, step_up_ref, operator_id)
    return "pulled"


async def governor_clear(session: AsyncSession, *, actor_id: str,
                         step_up_ref: str, operator_id: str) -> str:
    """THE single sanctioned clear path (no other clear exists)."""
    status = await killswitch_state(session)
    if status is None:
        return "intact"  # the standing state, never invented
    if status == "cleared":
        return "cleared"
    await _valve(session, "cleared", actor_id, step_up_ref, operator_id)
    return "cleared"
