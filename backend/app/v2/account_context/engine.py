"""BE-10 join engine (BO B-1.3; laws L4/L6/L7).

Basis law: the newest COMPLETE sync run is the sole basis; none ever =
typed `account_context.no_basis` (fail-closed, never synthesized).
Mapping law: explicit seeded `v2_md_symbol_map` rows ONLY (source
`exness_mt5_demo`); a miss is a VISIBLE `unmapped` verdict, never a
filter and never a guess. Digest (L7): SHA-256 over (sync_run_id, the
mapping rowset, the signal pins, engine version) — canonical JSON,
deterministic x3.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_broker_read import V2BrokerPosition, V2BrokerSyncRun
from app.db.models.v2_marketdata import V2MdSymbolMap
from app.db.models.v2_signal import V2SignalRecord
from app.v2.account_context.contract import (
    ENGINE_VERSION,
    LIVE_SIGNAL_STATES,
    AccountContextRefused,
    AlignmentMatrix,
    AlignmentRow,
)

BROKER_SOURCE_ID = "exness_mt5_demo"
STALE_AFTER_HOURS = 24  # the BE-9 staleness law carried (L8)


def _canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      default=str)


async def _basis(session: AsyncSession) -> V2BrokerSyncRun:
    """L4: newest complete sync run, or typed refusal."""
    run = (await session.execute(
        select(V2BrokerSyncRun)
        .where(V2BrokerSyncRun.outcome == "complete")
        .order_by(V2BrokerSyncRun.created_at.desc()))).scalars().first()
    if run is None:
        raise AccountContextRefused("account_context.no_basis", [
            {"failing": "basis",
             "note": "no complete sync has ever landed (L4 fail-closed)"}])
    return run


async def _mapping(session: AsyncSession) -> dict[str, str]:
    """The seeded broker->canonical rowset; absent artifact = typed."""
    rows = list((await session.execute(
        select(V2MdSymbolMap)
        .where(V2MdSymbolMap.source_id == BROKER_SOURCE_ID))).scalars().all())
    if not rows:
        raise AccountContextRefused(
            "account_context.mapping_artifact_absent", [
                {"failing": "v2_md_symbol_map",
                 "source_id": BROKER_SOURCE_ID,
                 "note": "0050 seed rows not present on this lineage"}])
    return {r.source_symbol: r.instrument_id for r in rows}


def _signal_facts(record: V2SignalRecord | None,
                  now: datetime) -> tuple[str, str | None]:
    """(signal_state, direction). States: live/none/expired/indeterminate."""
    if record is None:
        return "none", None
    expires = record.expires_at
    if expires is not None:
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        if expires <= now:
            return "expired", None
    payload = record.payload or {}
    direction = payload.get("direction")
    if direction not in ("up", "down"):
        return "indeterminate", None
    return "live", direction


def _posture(units_long: Decimal, units_short: Decimal) -> str:
    if units_long > 0 and units_short > 0:
        return "mixed"
    if units_long > 0:
        return "long"
    if units_short > 0:
        return "short"
    return "flat"


def _verdict(posture: str, signal_state: str,
             direction: str | None, mapped: bool) -> str:
    if not mapped:
        return "unmapped"
    if signal_state in ("indeterminate",):
        return "indeterminate"
    live = signal_state == "live"
    held = posture in ("long", "short", "mixed")
    if held and live:
        if posture == "mixed":
            return "indeterminate"
        agrees = (posture == "long" and direction == "up") or \
                 (posture == "short" and direction == "down")
        return "aligned" if agrees else "opposed"
    if held and not live:
        return "unsignalled_holding"
    if not held and live:
        return "signal_without_holding"
    return "flat_no_signal"


async def compute_alignment(session: AsyncSession) -> AlignmentMatrix:
    now = datetime.now(timezone.utc)
    run = await _basis(session)
    mapping = await _mapping(session)

    created = run.created_at
    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)
    age_hours = round((now - created).total_seconds() / 3600, 3)
    stale = age_hours > STALE_AFTER_HOURS

    positions = list((await session.execute(
        select(V2BrokerPosition)
        .where(V2BrokerPosition.sync_run_id == run.id))).scalars().all())

    # The instrument universe = held instruments UNION live-signal
    # instruments whose canonical id reverse-maps into the broker book.
    held: dict[str, dict] = {}
    for p in positions:
        held[p.instrument_ext_id] = {
            "units_long": Decimal(p.units_long),
            "units_short": Decimal(p.units_short)}

    signal_rows = list((await session.execute(
        select(V2SignalRecord)
        .where(V2SignalRecord.state.in_(LIVE_SIGNAL_STATES))
        .order_by(V2SignalRecord.created_at.desc()))).scalars().all())
    newest_by_instrument: dict[str, V2SignalRecord] = {}
    for s in signal_rows:
        newest_by_instrument.setdefault(s.instrument_id, s)
    reverse_map = {v: k for k, v in mapping.items()}

    universe: list[str] = sorted(
        set(held)
        | {reverse_map[iid] for iid in newest_by_instrument
           if iid in reverse_map})

    rows: list[AlignmentRow] = []
    signal_pins: list = []
    unmapped = 0
    for ext_id in universe:
        canonical_id = mapping.get(ext_id)
        mapped = canonical_id is not None
        h = held.get(ext_id, {"units_long": Decimal(0),
                              "units_short": Decimal(0)})
        posture = _posture(h["units_long"], h["units_short"])
        record = (newest_by_instrument.get(canonical_id)
                  if mapped else None)
        signal_state, direction = _signal_facts(record, now)
        verdict = _verdict(posture, signal_state, direction, mapped)
        if verdict == "unmapped":
            unmapped += 1
        if record is not None:
            signal_pins.append({"id": record.id,
                                "instrument_id": record.instrument_id,
                                "state": record.state,
                                "direction": direction})
        rows.append(AlignmentRow(
            instrument_ext_id=ext_id, instrument_id=canonical_id,
            posture=posture, units_long=str(h["units_long"]),
            units_short=str(h["units_short"]),
            signal_state=signal_state, signal_direction=direction,
            verdict=verdict, basis_sync_run_id=run.id,
            basis_age_hours=age_hours))

    digest = hashlib.sha256(_canonical({
        "sync_run_id": run.id,
        "mapping": sorted(mapping.items()),
        "signal_pins": sorted(signal_pins, key=lambda p: p["id"]),
        "engine_version": ENGINE_VERSION,
    }).encode("utf-8")).hexdigest()

    return AlignmentMatrix(
        rows=tuple(rows), basis_sync_run_id=run.id,
        basis_age_hours=age_hours,
        staleness="stale" if stale else "fresh",
        banner=("last-good basis; broker not re-contacted since the shown"
                " basis" if stale else None),
        digest=digest, engine_version=ENGINE_VERSION,
        unmapped_count=unmapped)
