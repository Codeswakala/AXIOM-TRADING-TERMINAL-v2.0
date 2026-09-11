"""BE-7 U-3 registration writers (REQ-1.3/1.4/1.6).

Input registration with content-addressed dedupe; cost-model and strategy
generation writers. All refusals typed + durably audited (C-1 law:
commit-before-return on refusal paths so the audit survives)."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_research_jobs import (
    V2BacktestInput,
    V2CostModel,
    V2StrategyVersion,
)
from app.v2.audit.contract import V2AuditEventCreate
from app.v2.audit.repository import V2AuditRepository
from app.v2.research_jobs.contracts import (
    COST_UNITS_V1,
    LIFECYCLE_STATES,
    RJ_FIRST_LANDING_DATA_CLASSES,
    TypedOutcome,
)
from app.v2.research_jobs.leakage import LeakageRefused, ReplayWindow

_DOMAIN = "v2.research_jobs"


async def _audit(session: AsyncSession, action: str, *, details: dict,
                 mode: str, operator_id: str,
                 correlation_id: str | None,
                 resource_type: str, resource_id: str | None = None) -> None:
    await V2AuditRepository(session).append(V2AuditEventCreate(
        domain=_DOMAIN, action=action, actor_id=operator_id,
        actor_type="operator", mode=mode, resource_type=resource_type,
        resource_id=resource_id, details=details, operator_id=operator_id,
        correlation_id=correlation_id))


async def register_input(
    session: AsyncSession, *, input_id: str, content_hash: str,
    series_refs: dict, window_start: datetime, window_end: datetime,
    data_class: str, mode: str, operator_id: str,
    correlation_id: str | None,
) -> TypedOutcome:
    reasons: list = []
    if data_class not in RJ_FIRST_LANDING_DATA_CLASSES:
        reasons.append({"failing": "data_class", "value": data_class,
                        "note": "corpus-gated (V2-TD-18)"})
    try:
        ReplayWindow(window_start=window_start, window_end=window_end,
                     as_of=window_end).validate()
    except LeakageRefused as exc:
        reasons.extend(exc.reasons)
    if not series_refs:
        reasons.append({"failing": "series_refs", "value": "empty"})

    if reasons:
        await _audit(session, "input.refused",
                     details={"input_id": input_id, "reasons": reasons[:8]},
                     mode=mode, operator_id=operator_id,
                     correlation_id=correlation_id,
                     resource_type="backtest_input")
        await session.commit()
        return TypedOutcome(outcome="refused", reasons=reasons)

    # content-addressed dedupe: identical content ⇒ idempotent reuse
    existing = (await session.execute(
        select(V2BacktestInput).where(
            V2BacktestInput.content_hash == content_hash)
    )).scalar_one_or_none()
    if existing is not None:
        await _audit(session, "input.reused",
                     details={"input_id": existing.input_id,
                              "content_hash": content_hash},
                     mode=mode, operator_id=operator_id,
                     correlation_id=correlation_id,
                     resource_type="backtest_input",
                     resource_id=existing.id)
        return TypedOutcome(outcome="reused", record_id=existing.id)

    newest = (await session.execute(
        select(V2BacktestInput)
        .where(V2BacktestInput.input_id == input_id)
        .order_by(V2BacktestInput.record_seq.desc())
    )).scalars().first()
    row = V2BacktestInput(
        input_id=input_id,
        record_seq=1 if newest is None else newest.record_seq + 1,
        supersedes=newest.id if newest is not None else None,
        content_hash=content_hash,
        series_refs=series_refs,
        window_start=window_start, window_end=window_end,
        registration_outcome="registered",
        data_class=data_class, mode=mode, operator_id=operator_id,
        correlation_id=correlation_id)
    session.add(row)
    await session.flush()
    await _audit(session, "input.registered",
                 details={"input_id": input_id, "record_seq": row.record_seq,
                          "content_hash": content_hash},
                 mode=mode, operator_id=operator_id,
                 correlation_id=correlation_id,
                 resource_type="backtest_input", resource_id=row.id)
    return TypedOutcome(outcome="registered", record_id=row.id)


async def register_cost_model(
    session: AsyncSession, *, cost_model_id: str, spread: dict,
    commission: dict, slippage: dict, latency_ms: int, risk_limits: dict,
    data_class: str, mode: str, operator_id: str,
    correlation_id: str | None,
) -> TypedOutcome:
    reasons: list = []
    citations: dict = {}
    for key, entry in (("spread", spread), ("commission", commission),
                       ("slippage", slippage)):
        for field in ("value", "unit", "citation"):
            if field not in entry:
                reasons.append({"failing": f"{key}.{field}",
                                "required": "value+unit+citation"
                                            " (REQ-1.4 — no invented"
                                            " numbers as spec values)"})
        # F-1 (CR-V2-BE-7-001): unit vocabulary gate at registration —
        # apply_costs knows exactly COST_UNITS_V1; anything else must be a
        # typed refusal HERE, never an untyped engine failure downstream.
        if "unit" in entry and entry["unit"] not in COST_UNITS_V1:
            reasons.append({"failing": f"{key}.unit",
                            "value": entry["unit"],
                            "allowed": list(COST_UNITS_V1)})
        citations[key] = entry.get("citation")
    if data_class not in RJ_FIRST_LANDING_DATA_CLASSES:
        reasons.append({"failing": "data_class", "value": data_class})
    if reasons:
        await _audit(session, "cost_model.refused",
                     details={"cost_model_id": cost_model_id,
                              "reasons": reasons[:8]},
                     mode=mode, operator_id=operator_id,
                     correlation_id=correlation_id, resource_type="cost_model")
        await session.commit()
        return TypedOutcome(outcome="refused", reasons=reasons)

    newest = (await session.execute(
        select(V2CostModel)
        .where(V2CostModel.cost_model_id == cost_model_id)
        .order_by(V2CostModel.record_seq.desc())
    )).scalars().first()
    row = V2CostModel(
        cost_model_id=cost_model_id,
        record_seq=1 if newest is None else newest.record_seq + 1,
        supersedes=newest.id if newest is not None else None,
        spread=spread, commission=commission, slippage=slippage,
        latency_ms=latency_ms, risk_limits=risk_limits,
        citations=citations, data_class=data_class, mode=mode,
        operator_id=operator_id, correlation_id=correlation_id)
    session.add(row)
    await session.flush()
    await _audit(session, "cost_model.registered",
                 details={"cost_model_id": cost_model_id,
                          "record_seq": row.record_seq},
                 mode=mode, operator_id=operator_id,
                 correlation_id=correlation_id,
                 resource_type="cost_model", resource_id=row.id)
    return TypedOutcome(outcome="registered", record_id=row.id)


async def register_strategy(
    session: AsyncSession, *, strategy_id: str, name: str, parameters: dict,
    lifecycle_state: str, data_class: str, mode: str, operator_id: str,
    correlation_id: str | None,
) -> TypedOutcome:
    from app.v2.research_jobs.replay import STRATEGY_RULES

    reasons: list = []
    if lifecycle_state not in LIFECYCLE_STATES:
        reasons.append({"failing": "lifecycle_state",
                        "value": lifecycle_state})
    rule = parameters.get("rule")
    if rule not in STRATEGY_RULES:
        reasons.append({"failing": "parameters.rule", "value": rule,
                        "required": sorted(STRATEGY_RULES),
                        "note": "v1 scope: registered deterministic rule"
                                " functions only (plan Part 15)"})
    for banned in ("credential", "api_key", "broker", "account", "adapter"):
        if banned in {k.lower() for k in parameters}:
            reasons.append({"failing": "parameters",
                            "value": f"forbidden key class: {banned}"})
    if data_class not in RJ_FIRST_LANDING_DATA_CLASSES:
        reasons.append({"failing": "data_class", "value": data_class})
    if reasons:
        await _audit(session, "strategy.refused",
                     details={"strategy_id": strategy_id,
                              "reasons": reasons[:8]},
                     mode=mode, operator_id=operator_id,
                     correlation_id=correlation_id,
                     resource_type="strategy_version")
        await session.commit()
        return TypedOutcome(outcome="refused", reasons=reasons)

    newest = (await session.execute(
        select(V2StrategyVersion)
        .where(V2StrategyVersion.strategy_id == strategy_id)
        .order_by(V2StrategyVersion.record_seq.desc())
    )).scalars().first()
    row = V2StrategyVersion(
        strategy_id=strategy_id,
        record_seq=1 if newest is None else newest.record_seq + 1,
        supersedes=newest.id if newest is not None else None,
        name=name, parameters=parameters, lifecycle_state=lifecycle_state,
        data_class=data_class, mode=mode, operator_id=operator_id,
        correlation_id=correlation_id)
    session.add(row)
    await session.flush()
    action = ("strategy.registered" if newest is None
              else "strategy.superseded")
    await _audit(session, action,
                 details={"strategy_id": strategy_id,
                          "record_seq": row.record_seq,
                          "lifecycle_state": lifecycle_state},
                 mode=mode, operator_id=operator_id,
                 correlation_id=correlation_id,
                 resource_type="strategy_version", resource_id=row.id)
    return TypedOutcome(outcome="registered", record_id=row.id)
