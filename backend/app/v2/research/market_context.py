"""BE-4 Market Context Engine (MCE) — spec §14 synthesis (plan §3).

Families 1–9 computed per timeframe from the REUSED V1 deterministic
surface (imported, never modified); family 10 (timeframe_relationships)
composed under the plan §2 / R-4 rules. Deterministic: pure function of
(bars, as_of, versions) — no wall clock, no randomness, no I/O.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.services import indicators as _ind
from app.services import market_structure as _ms
from app.services.indicator_registry import INDICATOR_REGISTRY
from app.v2.research.typing import (
    Observation,
    TypedOutcomes,
    validate_observation,
)
from app.v2.research.versioning import (
    INDICATOR_ENGINE_VERSION,
)

# V1 liquidity-structure disclosure (CHART-P03 M8) — propagated verbatim
# (plan §3 family 5: structural outputs do not imply institutional order
# flow or execution readiness).
_LIQUIDITY_DISCLOSURE = (
    INDICATOR_REGISTRY["OBPATTERN"].disclosure
    or "Pattern-based observation; implies no institutional order flow."
)


def canonical_json(value) -> str:
    """Canonical serialization (BO D-1 pin): keys sorted lexicographically,
    no whitespace. Used for input hashing and the engine_versions hash."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def input_content_hash(bars_by_timeframe: dict[str, list[dict]]) -> str:
    """SHA-256 over the canonical serialization of the consumed bars
    (plan §1.3 input snapshot identity)."""
    payload = {
        tf: [
            {
                "open_time": b["open_time"].isoformat()
                if isinstance(b["open_time"], datetime)
                else str(b["open_time"]),
                "open": str(b["open"]),
                "high": str(b["high"]),
                "low": str(b["low"]),
                "close": str(b["close"]),
                "volume": str(b.get("volume", "0")),
            }
            for b in bars
        ]
        for tf, bars in bars_by_timeframe.items()
    }
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


class _IdGen:
    """Deterministic per-report id sequence — computation order is
    deterministic, so ids (and therefore the whole report body) are
    byte-identically reproducible (plan §11.1)."""

    def __init__(self, prefix: str) -> None:
        self._prefix = prefix
        self._n = 0

    def next(self) -> str:
        self._n += 1
        return f"{self._prefix}-{self._n:04d}"


def _dec_str(value) -> str | None:
    if value is None:
        return None
    return str(Decimal(str(value)).normalize())


def _last_line_value(series, line_name: str) -> tuple[str | None, str | None]:
    """(value, iso_time) of the last non-None point on a named line."""
    if series.kind != "computed" or not series.lines:
        return None, None
    for point in reversed(series.lines.get(line_name, [])):
        if getattr(point, "value", None) is not None:
            return _dec_str(point.value), point.time.isoformat()
    return None, None


def _last_value(series) -> str | None:
    """Last non-None point value of a single-line IndicatorSeries."""
    if series.kind != "computed":
        return None
    for point in reversed(series.points):
        if getattr(point, "value", None) is not None:
            return _dec_str(point.value)
    return None


@dataclass(frozen=True)
class FamilyResult:
    observations: list[Observation]
    outcomes: TypedOutcomes


def _observed(idgen: _IdGen, family: str, timeframe: str, indicator_id: str,
              params: dict, statement: dict) -> Observation:
    return Observation(
        observation_id=idgen.next(),
        family=family,
        timeframe=timeframe,
        layer="observed",
        claim_type="fact",
        statement=statement,
        indicator_basis={
            "indicator_id": indicator_id,
            "parameters": params,
            "engine": INDICATOR_ENGINE_VERSION,
        },
    )


def _derived(idgen: _IdGen, family: str, timeframe: str, statement: dict,
             contributing: tuple[str, ...]) -> Observation:
    return Observation(
        observation_id=idgen.next(),
        family=family,
        timeframe=timeframe,
        layer="derived",
        claim_type="derived_observation",
        statement=statement,
        contributing_observation_ids=contributing,
    )


def _contextual(idgen: _IdGen, family: str, timeframe: str, statement: dict,
                contributing: tuple[str, ...],
                relationship_class: str | None = None) -> Observation:
    return Observation(
        observation_id=idgen.next(),
        family=family,
        timeframe=timeframe,
        layer="contextual",
        claim_type="contextual_interpretation",
        statement=statement,
        contributing_observation_ids=contributing,
        relationship_class=relationship_class,
    )


# --- Per-timeframe family computation (families 1–9) -------------------------


_TF_MINUTES = {
    "M1": 1, "M5": 5, "M15": 15, "M30": 30,
    "H1": 60, "H4": 240, "D1": 1440,
}


def _tf_minutes(timeframe: str) -> int:
    return _TF_MINUTES.get(timeframe.upper(), 60)


def compute_timeframe_families(timeframe: str, bars: list[dict],
                               idgen: _IdGen) -> FamilyResult:
    """Families 1–9 for one timeframe. Insufficient data per family is a
    typed outcome, never an exception (plan §6)."""
    observations: list[Observation] = []
    outcomes = TypedOutcomes()
    n = len(bars)

    def short(family: str, required: int) -> bool:
        if n < required:
            outcomes.record(family, timeframe, required, n)
            return True
        return False

    # 1 — prevailing_trend (sma/ema/supertrend/adx basis → derived state)
    if not short("prevailing_trend", 50):
        sma20 = _ind.sma(bars, 20)
        sma50 = _ind.sma(bars, 50)
        adx = _ind.adx_dmi(bars, 14)
        o_fast = _observed(idgen, "prevailing_trend", timeframe, "SMA20", {"n": 20},
                           {"metric": "sma", "value": _last_value(sma20)})
        o_slow = _observed(idgen, "prevailing_trend", timeframe, "SMA50", {"n": 50},
                           {"metric": "sma", "value": _last_value(sma50)})
        observations += [o_fast, o_slow]
        fast, slow = _last_value(sma20), _last_value(sma50)
        if fast is not None and slow is not None:
            state = ("up" if Decimal(fast) > Decimal(slow)
                     else "down" if Decimal(fast) < Decimal(slow) else "flat")
            adx_line = (adx.lines or {}).get("adx", []) if adx.kind == "computed" else []
            adx_last = next(
                (_dec_str(p.value) for p in reversed(adx_line) if p.value is not None),
                None,
            )
            observations.append(_derived(idgen,
                "prevailing_trend", timeframe,
                {"trend": state, "basis": "sma20-vs-sma50", "adx": adx_last},
                (o_fast.observation_id, o_slow.observation_id),
            ))

    # 2 — structural_state + 3 — protected_swing (swings/struct)
    if not short("structural_state", 11):
        swings = _ms.swings(bars, k=5)
        struct = _ms.struct(bars, k=5)
        hi_val, hi_time = _last_line_value(swings, "swing_high")
        lo_val, lo_time = _last_line_value(swings, "swing_low")
        swing_count = sum(
            1
            for name in ("swing_high", "swing_low")
            for pt in (swings.lines or {}).get(name, [])
            if getattr(pt, "value", None) is not None
        ) if swings.kind == "computed" else 0
        o_swings = _observed(idgen, "structural_state", timeframe, "SWINGS55", {"k": 5},
                             {"metric": "swing_count", "value": str(swing_count)})
        observations.append(o_swings)
        observations.append(_derived(idgen,
            "structural_state", timeframe,
            {"structural_state": "structured" if swing_count > 0 else "unstructured",
             "struct_computed": struct.kind == "computed"},
            (o_swings.observation_id,),
        ))
        if hi_val is not None or lo_val is not None:
            observations.append(_derived(idgen,
                "protected_swing", timeframe,
                {"swing_high": hi_val, "swing_high_time": hi_time,
                 "swing_low": lo_val, "swing_low_time": lo_time},
                (o_swings.observation_id,),
            ))
        else:
            outcomes.record("protected_swing", timeframe, 11, n)

    # 4 — structural_break (bos/choch)
    if not short("structural_break", 11):
        bos = _ms.bos(bars, k=5)
        choch = _ms.choch(bars, k=5)

        def _marker_count(series) -> int:
            if series.kind != "computed":
                return 0
            total = sum(
                1 for pt in series.points if getattr(pt, "value", None) is not None
            )
            for line in (series.lines or {}).values():
                total += sum(1 for pt in line if getattr(pt, "value", None) is not None)
            return total

        bos_count, choch_count = _marker_count(bos), _marker_count(choch)
        o_bos = _observed(idgen, "structural_break", timeframe, "BOS55", {"k": 5},
                          {"metric": "bos_count", "value": str(bos_count)})
        observations.append(o_bos)
        observations.append(_derived(idgen,
            "structural_break", timeframe,
            {"breaks_detected": bos_count > 0,
             "choch_detected": choch_count > 0},
            (o_bos.observation_id,),
        ))

    # 5 — liquidity_context (fvg/order_block_pattern; disclosure verbatim)
    if not short("liquidity_context", 3):
        fvg = _ms.fvg(bars)
        obp = _ms.order_block_pattern(bars)

        def _zone_count(series) -> int:
            if series.kind != "computed":
                return 0
            total = sum(
                1 for pt in series.points if getattr(pt, "value", None) is not None
            )
            for line in (series.lines or {}).values():
                total += sum(1 for pt in line if getattr(pt, "value", None) is not None)
            return total

        fvg_count, obp_count = _zone_count(fvg), _zone_count(obp)
        o_fvg = _observed(idgen, "liquidity_context", timeframe, "FVG3", {},
                          {"metric": "fvg_count", "value": str(fvg_count)})
        observations.append(o_fvg)
        observations.append(_contextual(idgen,
            "liquidity_context", timeframe,
            {"gaps_present": fvg_count > 0,
             "pattern_zones": obp_count,
             "disclosure": _LIQUIDITY_DISCLOSURE},
            (o_fvg.observation_id,),
        ))

    # 6 — key_levels (pivots/donchian)
    if not short("key_levels", 20):
        piv = _ind.pivot_points(bars, _tf_minutes(timeframe))
        don = _ind.donchian(bars, 20)
        pivot_last, _ = _last_line_value(piv, "P")
        o_piv = _observed(idgen, "key_levels", timeframe, "PIVOTCL", {},
                          {"metric": "pivot", "value": pivot_last})
        observations.append(o_piv)
        if don.kind == "computed" and don.points:
            last_band = don.points[-1]
            observations.append(_derived(idgen,
                "key_levels", timeframe,
                {"channel_upper": _dec_str(last_band.upper),
                 "channel_lower": _dec_str(last_band.lower)},
                (o_piv.observation_id,),
            ))

    # 7 — session_context (session_levels; label-only on synthetic 24×7 data)
    if not short("session_context", 2):
        sess = _ind.session_levels(bars, _tf_minutes(timeframe))
        o_sess = _observed(idgen,
            "session_context", timeframe, "SESSLVL", {},
            {"metric": "session_series", "computed": sess.kind == "computed",
             "disclosure": "Synthetic 24x7 simulator grid; session labels are"
                           " label-only and imply no venue claim."},
        )
        observations.append(o_sess)

    # 8 — volatility_state (atr/bollinger)
    if not short("volatility_state", 20):
        atr = _ind.atr(bars, 14)
        bb = _ind.bollinger(bars, 20, 2.0)
        o_atr = _observed(idgen, "volatility_state", timeframe, "ATR14", {"n": 14},
                          {"metric": "atr", "value": _last_value(atr)})
        observations.append(o_atr)
        if bb.kind == "computed" and bb.points:
            last_bb = bb.points[-1]
            width = (
                _dec_str(Decimal(str(last_bb.upper)) - Decimal(str(last_bb.lower)))
                if last_bb.upper is not None and last_bb.lower is not None
                else None
            )
            observations.append(_derived(idgen,
                "volatility_state", timeframe,
                {"band_width": width},
                (o_atr.observation_id,),
            ))

    # 9 — momentum_state (rsi/macd)
    if not short("momentum_state", 34):
        rsi = _ind.rsi(bars, 14)
        macd = _ind.macd(bars)
        o_rsi = _observed(idgen, "momentum_state", timeframe, "RSI14", {"n": 14},
                          {"metric": "rsi", "value": _last_value(rsi)})
        observations.append(o_rsi)
        rsi_last = _last_value(rsi)
        if rsi_last is not None:
            macd_hist = None
            if macd.kind == "computed" and macd.points:
                macd_hist = _dec_str(macd.points[-1].histogram)
            state = ("overbought" if Decimal(rsi_last) >= 70
                     else "oversold" if Decimal(rsi_last) <= 30 else "neutral")
            observations.append(_derived(idgen,
                "momentum_state", timeframe,
                {"momentum": state, "macd_histogram": macd_hist},
                (o_rsi.observation_id,),
            ))

    return FamilyResult(observations=observations, outcomes=outcomes)


# --- Family 10: timeframe_relationships (plan §2 / R-4) -----------------------


def compute_timeframe_relationships(
    per_tf: dict[str, list[Observation]], idgen: _IdGen,
) -> list[Observation]:
    """Compose cross-timeframe relationship observations under the R-4 rule
    table. Only produced when both contributing sides exist; an incomplete
    contributing set is refused by validation (typed outcome upstream)."""
    relationships: list[Observation] = []
    timeframes = sorted(per_tf)
    if len(timeframes) < 2:
        return relationships

    def derived_of(tf: str, family: str) -> Observation | None:
        for obs in per_tf[tf]:
            if obs.family == family and obs.layer == "derived":
                return obs
        return None

    for i in range(len(timeframes) - 1):
        lower_tf, higher_tf = timeframes[i], timeframes[i + 1]
        for family, rel_class in (
            ("prevailing_trend", "trend_alignment"),
            ("momentum_state", "momentum_alignment"),
            ("volatility_state", "volatility_alignment"),
        ):
            lo, hi = derived_of(lower_tf, family), derived_of(higher_tf, family)
            if lo is None or hi is None:
                continue  # incomplete set — no relationship emitted
            relationships.append(_derived(idgen,
                "timeframe_relationships", f"{lower_tf}+{higher_tf}",
                {"relationship_class": rel_class,
                 "lower": {"timeframe": lower_tf, **lo.statement},
                 "higher": {"timeframe": higher_tf, **hi.statement}},
                (lo.observation_id, hi.observation_id),
            ))
            # _derived() has no relationship_class parameter; rebuild frozen
            rel = relationships.pop()
            relationships.append(Observation(
                observation_id=rel.observation_id,
                family=rel.family,
                timeframe=rel.timeframe,
                layer="derived",
                claim_type="derived_observation",
                statement=rel.statement,
                contributing_observation_ids=rel.contributing_observation_ids,
                relationship_class=rel_class,
            ))
        # higher_tf_context — contextual by construction (R-4 table)
        hi_trend = derived_of(higher_tf, "prevailing_trend")
        lo_struct = derived_of(lower_tf, "structural_state")
        if hi_trend is not None and lo_struct is not None:
            relationships.append(Observation(
                observation_id=idgen.next(),
                family="timeframe_relationships",
                timeframe=f"{lower_tf}+{higher_tf}",
                layer="contextual",
                claim_type="contextual_interpretation",
                statement={"relationship_class": "higher_tf_context",
                           "higher_trend": hi_trend.statement,
                           "lower_structure": lo_struct.statement},
                contributing_observation_ids=(
                    hi_trend.observation_id, lo_struct.observation_id
                ),
                relationship_class="higher_tf_context",
            ))
    return relationships


# --- Report assembly ----------------------------------------------------------


@dataclass(frozen=True)
class MarketContextResult:
    status: str  # BE-1 status model
    observations: list[Observation]
    insufficient: list[dict]
    families_computed: int
    families_requested: int


def compute_market_context(
    bars_by_timeframe: dict[str, list[dict]],
) -> MarketContextResult:
    """Full MCE computation. Deterministic; validates every element through
    the single typing gate before acceptance (plan §2/§3)."""
    all_obs: list[Observation] = []
    all_insufficient: list[dict] = []
    per_tf: dict[str, list[Observation]] = {}

    idgen = _IdGen("obs")
    for timeframe, bars in sorted(bars_by_timeframe.items()):
        result = compute_timeframe_families(timeframe, bars, idgen)
        per_tf[timeframe] = result.observations
        all_obs.extend(result.observations)
        all_insufficient.extend(result.outcomes.insufficient)

    all_obs.extend(compute_timeframe_relationships(per_tf, idgen))

    # Single typing gate: every element validated; violation = typed refusal.
    known_ids: set[str] = set()
    known_tfs: dict[str, str] = {}
    for obs in all_obs:
        validate_observation(
            obs,
            known_ids=frozenset(known_ids),
            known_timeframes=dict(known_tfs),
        )
        known_ids.add(obs.observation_id)
        # relationships span "tfA+tfB"; contributing sides carry real tfs
        known_tfs[obs.observation_id] = obs.timeframe

    families_present = {o.family for o in all_obs}
    requested = 10 if len(bars_by_timeframe) >= 2 else 9
    computed = len(families_present)

    if not all_obs:
        status = "unavailable"
    elif all_insufficient or computed < requested:
        status = "degraded"
    else:
        status = "available"

    return MarketContextResult(
        status=status,
        observations=all_obs,
        insufficient=all_insufficient,
        families_computed=computed,
        families_requested=requested,
    )


def observations_to_json(observations: list[Observation],
                         insufficient: list[dict]) -> dict:
    """Canonical, deterministic report body (ids included; determinism tests
    compare bodies computed with pinned ids)."""
    return {
        "observations": [
            {
                "observation_id": o.observation_id,
                "family": o.family,
                "timeframe": o.timeframe,
                "layer": o.layer,
                "claim_type": o.claim_type,
                "statement": o.statement,
                "contributing_observation_ids": list(o.contributing_observation_ids),
                "indicator_basis": o.indicator_basis,
                "relationship_class": o.relationship_class,
            }
            for o in observations
        ],
        "insufficient_data": insufficient,
    }
