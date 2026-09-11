"""W6-U01 execution research safety foundation tests."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy import select

from app.db.models.audit import AuditEvent
from app.execution_research import (
    RESEARCH_STATUS,
    SIMULATED_EXECUTION_RESEARCH_DISCLAIMER,
    SIMULATION_MODE,
    ExecutionResearchSafetyContract,
)
from app.external_integration.broker import (
    GovernanceGateClosedError,
    NullBroker,
    OrderIntent,
    governance_gate,
)
from app.external_integration.broker.null_broker import (
    BROKER_REFUSAL_RESOURCE_TYPE,
    GATE_CLOSED_CONNECT_REFUSED,
    GATE_CLOSED_EXECUTE_REFUSED,
)


def _order_intent() -> OrderIntent:
    return OrderIntent(
        symbol="EURUSD",
        side="buy",
        order_type="market",
        volume=Decimal("0.01"),
        created_at=datetime(2026, 7, 17, 10, 0, tzinfo=timezone.utc),
        rationale="W6-U01 closed-gate refusal fixture",
    )


def test_governance_gate_remains_closed_for_wave6() -> None:
    assert governance_gate.broker_integration_authorized is False
    assert governance_gate.execution_authorized is False
    contract = ExecutionResearchSafetyContract()
    contract.assert_simulation_only()
    assert contract.simulation_mode == SIMULATION_MODE
    assert contract.research_status == RESEARCH_STATUS
    assert contract.disclaimer == SIMULATED_EXECUTION_RESEARCH_DISCLAIMER


@pytest.mark.asyncio
async def test_null_or_simulated_broker_refuses_connect_when_gate_closed(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        broker = NullBroker(audit_session=session)
        with pytest.raises(GovernanceGateClosedError):
            await broker.connect()
        event = (
            await session.scalars(
                select(AuditEvent).where(
                    AuditEvent.action == "broker.connect.refused",
                    AuditEvent.resource_type == BROKER_REFUSAL_RESOURCE_TYPE,
                    AuditEvent.details["reason_code"].as_string() == GATE_CLOSED_CONNECT_REFUSED,
                )
            )
        ).one()
        assert event.details is not None
        assert event.details["gate_state"] == "CLOSED"
        assert event.details["simulation_only"] is True
        assert event.details["live_broker_connection_attempted"] is False
        assert event.details["live_order_attempted"] is False


@pytest.mark.asyncio
async def test_null_or_simulated_broker_refuses_execute_when_gate_closed(
    prepared_db: None,
) -> None:
    from app.db.session import session_scope

    async with session_scope() as session:
        broker = NullBroker(audit_session=session)
        with pytest.raises(GovernanceGateClosedError):
            await broker.place_order(_order_intent())
        event = (
            await session.scalars(
                select(AuditEvent).where(
                    AuditEvent.action == "broker.execute.refused",
                    AuditEvent.resource_type == BROKER_REFUSAL_RESOURCE_TYPE,
                    AuditEvent.details["reason_code"].as_string() == GATE_CLOSED_EXECUTE_REFUSED,
                )
            )
        ).one()
        assert event.details is not None
        assert event.details["gate_state"] == "CLOSED"
        assert event.details["simulation_only"] is True
        assert event.details["live_broker_connection_attempted"] is False
        assert event.details["live_order_attempted"] is False


def test_broker_logic_contained_in_external_integration() -> None:
    root = Path(__file__).resolve().parents[1] / "app"
    broker_specific = (
        "MetaTrader5",
        "mt5",
        "MqlTrade",
        "TRADE_ACTION",
        "ORDER_TYPE",
        "broker_endpoint",
        "broker_credentials",
        "BrokerClient",
    )
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        for needle in broker_specific:
            if (
                re.search(rf"\b{re.escape(needle)}\b", text)
                and not rel.startswith("external_integration/")
                # BO-V2-BE-9-001 D-1 sanctioned adapter location:
                and not rel.startswith("v2/broker_read/providers/")
            ):
                offenders.append(f"{rel}:{needle}")
    assert offenders == []


def test_execution_research_has_no_live_broker_sdk_or_credentials() -> None:
    root = Path(__file__).resolve().parents[2]
    files = [root / "backend" / "requirements.txt", root / "backend" / "pyproject.toml"]
    package_text = "\n".join(path.read_text(encoding="utf-8").lower() for path in files)
    forbidden_packages = (
        "metatrader",
        "mt5",
        "ccxt",
        "ib_insync",
        "oandapy",
        "alpaca",
        "binance",
        "openai",
        "anthropic",
        "transformers",
        "langchain",
        "llama",
    )
    assert all(package not in package_text for package in forbidden_packages)

    execution_root = root / "backend" / "app" / "execution_research"
    text = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in execution_root.rglob("*.py")
    )
    forbidden_runtime = ("api_key", "secret_key", "password", "token", "credential")
    assert all(item not in text for item in forbidden_runtime)


def test_wave6_bright_line_grep_no_live_execution_path() -> None:
    root = Path(__file__).resolve().parents[1] / "app" / "execution_research"
    forbidden = (
        "place_order",
        "cancel_order",
        "go_live",
        "live_order",
        "real_account",
        "account_balance",
        "margin",
        "broker.connect",
        "broker.execute",
    )
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            if needle in text:
                offenders.append(f"{path.name}:{needle}")
    assert offenders == []


def test_execution_research_ui_module_has_no_live_execution_controls() -> None:
    """SURF-P01 M1 — frontend T-1 guard over the execution research stage view.

    The CONV-phase guards pin frontend files with non-vacuity assertions; this
    suite previously pinned none. The execution research surface is the most
    execution-adjacent surface in the platform, so the guard pins the module
    that actually renders it, and the positive assertions fail loudly if the
    path is ever re-pointed at a wrapper or barrel that does not contain the
    surface.
    """
    root = Path(__file__).resolve().parents[2]
    ui = (
        root
        / "frontend"
        / "src"
        / "components"
        / "terminal"
        / "execution"
        / "ExecutionResearchView.tsx"
    )
    text = ui.read_text(encoding="utf-8").lower()
    # Non-vacuity anchors: the module genuinely renders the simulated surface
    # and its per-group SIMULATED · NON-ACTUATING labelling (M2).
    assert "execution research workspace" in text
    assert "simulated" in text
    assert "non-actuating" in text
    forbidden = (
        "place_order",
        "submit order",
        "go live",
        "connect broker",
        "broker_account",
        "order_ticket",
        "account_id",
        "execute_order",
        "live_trade",
    )
    assert all(item not in text for item in forbidden)
