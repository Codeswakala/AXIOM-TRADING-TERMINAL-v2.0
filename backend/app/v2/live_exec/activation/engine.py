"""BE-12D activation fact reader (BO-V2-BE12D-001 §1.b.4).

READ-ONLY: the L3 fact is the instrument table's row count, read from
schema truth. No writer exists in this module or anywhere in the band —
the table can only ever be populated by a future register act under a
future build order.
"""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_live_activation import V2LiveActivationInstrument
from app.v2.live_exec.activation.template import (
    ACTIVATION_INSTRUMENT_TEMPLATE,
    TEMPLATE_VERSION,
    template_hash,
)

__all__ = [
    "ACTIVATION_INSTRUMENT_TEMPLATE",
    "TEMPLATE_VERSION",
    "activation_instrument_rows",
    "activation_state_shape",
    "template_hash",
]


async def activation_instrument_rows(session: AsyncSession) -> int:
    """THE L3 FACT READER: the force-row count from schema truth."""
    return (await session.execute(
        select(func.count()).select_from(V2LiveActivationInstrument)
    )).scalar_one()


async def activation_state_shape(session: AsyncSession) -> dict:
    """The read surface's typed shape: zero-row is a STATE, never an
    error (BO §1.b.3)."""
    rows = await activation_instrument_rows(session)
    return {
        "activation_instrument": (
            "not_in_force" if rows == 0 else "row_present"),
        "row_count": rows,
        "template_version": TEMPLATE_VERSION,
        "template_hash": template_hash(),
        "force_note": ("zero-row IS the L3 lock; taking force is a"
                       " future operator register act under a future"
                       " build order (activate-nothing law)"),
    }
