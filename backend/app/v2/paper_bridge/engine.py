"""BE-11 bridge engine (BO D-1; DR Q2/Q3 laws; pure computation).

Consistency ARM: the basis is pinned by sync_run_id in ONE read at
entry; no re-reads mid-computation. Money-units-only sizing while
positions are absent (instrument-exposure checks answer `deferred` with
notes — honest degradation, not failure). The cited reference price is
consumed as INPUT (D-B11-CITE). Digest (per-world law N-O13): SHA-256
over (basis_sync_run_id, intent payload, pxs/prg/pbr versions).

Seed reads (BO §0): tolerances and max_age_hours come from `seed`-kind
rows in v2_paper_bridge_drift_run. Zero rows shipped; absence
fail-closes every dependent arm.
"""

from __future__ import annotations

import hashlib
import json
from datetime import timezone
from decimal import ROUND_HALF_EVEN, Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_broker_read import (
    V2BrokerBalance,
    V2BrokerPosition,
    V2BrokerSyncRun,
)
from app.db.models.v2_paper_bridge import V2PaperBridgeDriftRun
from app.v2.paper_bridge.contract import (
    CITATION_KEYS,
    ENGINE_VERSION,
    BridgeBasis,
    BridgeRefused,
    CitedReferencePrice,
    GatewayRecord,
)

# pxs/prg consumed AS-IS (compver-pinned; R-2 reuse law) — versions only;
# the bodies are the standing BE-8 engines, un-reimplemented.
PXS_VERSION = "pxs-1.0.0"
PRG_VERSION = "prg-1.0.0"

# L-1 coupon target: the pinned engine tuple (order law: pxs, prg, pbr).
PBR_ENGINE_TUPLE = (PXS_VERSION, PRG_VERSION, ENGINE_VERSION)

_DOMAIN = "v2.paper_bridge"


def _canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      default=str)


def quantize_2dp(value: Decimal) -> str:
    """D-B10-2DP mirror: presentation-boundary rounding only."""
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN))


# --- seed reads (BO §0 slots; absence = the shipped state) ----------------------


async def read_tolerance_seeds(session: AsyncSession) -> list[dict]:
    rows = list((await session.execute(
        select(V2PaperBridgeDriftRun)
        .where(V2PaperBridgeDriftRun.run_kind == "seed",
               V2PaperBridgeDriftRun.seed_name == "drift_tolerance")
    )).scalars().all())
    return [r.payload for r in rows if r.payload]


async def read_staleness_seed(session: AsyncSession) -> float | None:
    row = (await session.execute(
        select(V2PaperBridgeDriftRun)
        .where(V2PaperBridgeDriftRun.run_kind == "seed",
               V2PaperBridgeDriftRun.seed_name == "generation_staleness")
        .order_by(V2PaperBridgeDriftRun.created_at.desc())
    )).scalars().first()
    if row is None or not row.payload:
        return None
    try:
        return float(row.payload["max_age_hours"])
    except (KeyError, TypeError, ValueError):
        return None


# --- basis (consistency ARM: one read at entry) ---------------------------------


async def pin_basis(session: AsyncSession) -> BridgeBasis:
    from datetime import datetime

    run = (await session.execute(
        select(V2BrokerSyncRun)
        .where(V2BrokerSyncRun.outcome == "complete")
        .order_by(V2BrokerSyncRun.created_at.desc()))).scalars().first()
    if run is None:
        raise BridgeRefused("basis_unavailable", [
            {"failing": "basis", "note": "no complete sync has ever landed"}])
    balance = (await session.execute(
        select(V2BrokerBalance)
        .where(V2BrokerBalance.sync_run_id == run.id))).scalars().first()
    if balance is None:
        raise BridgeRefused("basis_unavailable", [
            {"failing": "balance", "note": "basis run carries no balance row"}])
    positions = list((await session.execute(
        select(V2BrokerPosition)
        .where(V2BrokerPosition.sync_run_id == run.id))).scalars().all())

    created = run.created_at
    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)
    age = round((datetime.now(timezone.utc) - created)
                .total_seconds() / 3600, 3)
    return BridgeBasis(
        sync_run_id=run.id, balance=balance.balance,
        margin_used=balance.margin_used,
        margin_available=balance.margin_available,
        unrealized_pl=balance.unrealized_pl, currency=balance.currency,
        basis_age_hours=age,
        staleness="stale" if age > 24 else "fresh",
        positions_present=bool(positions))


# --- citation law (D-B11-CITE) ---------------------------------------------------


def require_citation(raw: dict | None) -> CitedReferencePrice:
    if not raw or any(k not in raw or raw[k] in (None, "")
                      for k in CITATION_KEYS):
        raise BridgeRefused("reference_price_uncited", [
            {"failing": "reference_price",
             "required": list(CITATION_KEYS),
             "note": "operator citation mandatory (D-B11-CITE);"
                     " the platform holds no price basis (E-B11-1)"}])
    return CitedReferencePrice(
        value=str(raw["value"]), currency_unit=str(raw["currency_unit"]),
        cited_source=str(raw["cited_source"]),
        cited_at=str(raw["cited_at"]))


# --- the gateway evaluation (pure; state record out) ------------------------------


def bridge_digest(basis_sync_run_id: str, intent_payload: dict) -> str:
    return hashlib.sha256(_canonical({
        "basis_sync_run_id": basis_sync_run_id,
        "intent_payload": intent_payload,
        "versions": {"pxs": PXS_VERSION, "prg": PRG_VERSION,
                     "pbr": ENGINE_VERSION},
    }).encode("utf-8")).hexdigest()


def evaluate_intent(basis: BridgeBasis, intent_payload: dict,
                    citation: CitedReferencePrice,
                    max_age_hours: float | None) -> GatewayRecord:
    """Money-units-only sizing today; decisions are RECORDS OF STATE."""
    if max_age_hours is None:
        raise BridgeRefused("basis_staleness_threshold_unseeded", [
            {"failing": "max_age_hours",
             "note": "generation refuses until the operator seeds the"
                     " staleness threshold (BO SS0 empty-forced law)"}])
    if basis.basis_age_hours > max_age_hours:
        raise BridgeRefused("basis_stale", [
            {"failing": "basis_age_hours",
             "observed": basis.basis_age_hours,
             "seeded_max": max_age_hours,
             "note": "stale basis may READ with banner, never spawn"
                     " ledger entries"}])

    notes: list[str] = []
    reasons: list[str] = []
    quantity = Decimal(str(intent_payload.get("quantity", "0")))
    price = Decimal(citation.value)
    notional = quantity * price
    available = Decimal(basis.margin_available)

    if citation.currency_unit != basis.currency:
        reasons.append("citation_currency_differs_from_basis")
    if notional > available:
        reasons.append("notional_exceeds_available_margin")
    if not basis.positions_present:
        notes.append("instrument_exposure_check_deferred:"
                     " no positions in basis (money-units-only sizing)")
    if basis.staleness == "stale":
        notes.append("basis_stale_banner_carried")

    if reasons:
        decision = "refused_under_policy"
    elif notes and any("deferred" in n for n in notes):
        decision = "deferred" if quantity == 0 else "accept_with_notes"
    else:
        decision = "accept_with_notes"

    return GatewayRecord(
        decision=decision, reasons=tuple(reasons), notes=tuple(notes),
        digest=bridge_digest(basis.sync_run_id, intent_payload),
        basis_sync_run_id=basis.sync_run_id,
        engine_versions={"pxs": PXS_VERSION, "prg": PRG_VERSION,
                         "pbr": ENGINE_VERSION})


# --- drift computation (R-3.4; refuse-to-compare until seeded) ---------------------


def compute_drift(paper_side: dict, broker_side: dict,
                  tolerance_seeds: list[dict]) -> tuple[str, list]:
    """Verdict + per-field findings. No seeds => uncomputable, always."""
    if not tolerance_seeds:
        return "uncomputable", [
            {"field": "*", "note": "refuse-to-compare: no tolerance seeds"
             " on the lineage (BO SS0 empty-forced law)"}]
    by_name = {t["name"]: t for t in tolerance_seeds
               if all(k in t for k in ("name", "value", "unit",
                                       "citation"))}
    if not by_name:
        return "uncomputable", [
            {"field": "*", "note": "seed rows malformed (citation chassis"
             " incomplete) - refuse-to-compare"}]
    findings: list = []
    worst = "within_tolerance"
    order = {"within_tolerance": 0, "drift_minor": 1, "drift_major": 2}
    for fld in sorted(set(paper_side) | set(broker_side)):
        if fld not in by_name:
            findings.append({"field": fld, "verdict": "uncomputable",
                             "note": "no seeded tolerance for this field"})
            return "uncomputable", findings
        try:
            p = Decimal(str(paper_side.get(fld, "0")))
            b = Decimal(str(broker_side.get(fld, "0")))
        except Exception:
            return "uncomputable", [{"field": fld,
                                     "note": "non-decimal input"}]
        delta = abs(p - b)
        tol = Decimal(str(by_name[fld]["value"]))
        if delta <= tol:
            v = "within_tolerance"
        elif delta <= tol * 2:
            v = "drift_minor"
        else:
            v = "drift_major"
        findings.append({"field": fld, "paper": str(p), "broker": str(b),
                         "delta": quantize_2dp(delta),
                         "tolerance": str(tol), "verdict": v})
        if order[v] > order[worst]:
            worst = v
    return worst, findings
