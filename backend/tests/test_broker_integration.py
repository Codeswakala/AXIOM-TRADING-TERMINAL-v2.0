"""W1-U03 broker integration framework tests."""

from __future__ import annotations

import socket
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import pytest

from app.external_integration.broker import (
    BrokerDisabledError,
    BrokerPort,
    GovernanceGateClosedError,
    NullBroker,
    OrderIntent,
)
from app.services.observability_service import get_observability_service


def _order_intent() -> OrderIntent:
    return OrderIntent(
        symbol="EURUSD",
        side="buy",
        order_type="market",
        volume=Decimal("0.01"),
        created_at=datetime(2026, 7, 13, 10, 0, tzinfo=timezone.utc),
        rationale="unit-test inert DTO",
    )


def test_null_broker_implements_port_and_disabled_capabilities() -> None:
    broker = NullBroker()
    assert isinstance(broker, BrokerPort)
    assert broker.is_connected() is False
    capabilities = broker.describe_capabilities()
    assert capabilities.adapter_name == "null-broker"
    assert capabilities.connection_enabled is False
    assert capabilities.execution_enabled is False
    assert capabilities.market_data_enabled is False


@pytest.mark.asyncio
async def test_governance_gate_refuses_connect_and_execute(
    caplog: pytest.LogCaptureFixture,
) -> None:
    broker = NullBroker()
    before = get_observability_service().snapshot()["governance"]["gate_refusals_total"]

    with pytest.raises(GovernanceGateClosedError):
        await broker.connect()
    with pytest.raises(GovernanceGateClosedError):
        await broker.place_order(_order_intent())

    after_snapshot = get_observability_service().snapshot()
    assert after_snapshot["governance"]["gate_refusals_total"] >= before + 2
    assert "broker.connect" in after_snapshot["governance"]["gate_refusals_by_action"]
    assert "broker.place_order" in after_snapshot["governance"]["gate_refusals_by_action"]
    assert "Governance Gate CLOSED" in caplog.text


@pytest.mark.asyncio
async def test_null_broker_read_paths_disabled() -> None:
    broker = NullBroker()
    with pytest.raises(BrokerDisabledError):
        await broker.get_instruments()
    with pytest.raises(BrokerDisabledError):
        await broker.get_account_info()
    with pytest.raises(BrokerDisabledError):
        await broker.get_quote("EURUSD")


@pytest.mark.asyncio
async def test_null_broker_opens_no_socket(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_connection(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("network connection must not be opened by NullBroker")

    monkeypatch.setattr(socket, "create_connection", fail_connection)
    broker = NullBroker()
    assert broker.describe_capabilities().connection_enabled is False
    with pytest.raises(GovernanceGateClosedError):
        await broker.connect()
    await broker.disconnect()


def test_order_intent_rejects_naive_datetime_and_serializes_without_secret() -> None:
    with pytest.raises(ValueError, match="Naive datetime rejected"):
        OrderIntent(
            symbol="EURUSD",
            side="buy",
            order_type="market",
            volume=Decimal("0.01"),
            created_at=datetime(2026, 7, 13, 10, 0),
        )

    payload = _order_intent().model_dump_json()
    assert "password" not in payload.lower()
    assert "token" not in payload.lower()
    assert "secret" not in payload.lower()
    assert "api_key" not in payload.lower()


def test_no_broker_specific_symbols_outside_external_integration() -> None:
    root = Path(__file__).resolve().parents[1] / "app"
    forbidden = ("MetaTrader5", "mt5.", "MqlTrade", "TRADE_ACTION", "ORDER_TYPE")
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        rel = path.relative_to(root).as_posix()
        if rel.startswith("external_integration/"):
            continue
        if rel.startswith("v2/broker_read/providers/"):
            # BO-V2-BE-9-001 D-1: the sanctioned read-only MT5
            # adapter location (containment law extended, not waived)
            continue
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            if needle in text:
                offenders.append(f"{rel}:{needle}")
    assert offenders == []


def test_no_broker_credential_literals_in_external_integration_code() -> None:
    root = Path(__file__).resolve().parents[1] / "app" / "external_integration"
    forbidden = ("broker_password", "api_key=", "server_password", "login_password")
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            if needle in text:
                offenders.append(f"{path.name}:{needle}")
    assert offenders == []
