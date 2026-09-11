"""Broker-neutral boundary DTOs for the External Integration System.

These models are anti-corruption DTOs: inner AXIOM systems must see these
neutral types, never native broker/MT5-specific vocabulary.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.time import require_utc


class BrokerBoundaryModel(BaseModel):
    """Strict base for broker boundary DTOs."""

    model_config = ConfigDict(extra="forbid")


class BrokerCapabilities(BrokerBoundaryModel):
    adapter_name: str
    connection_enabled: bool = False
    execution_enabled: bool = False
    market_data_enabled: bool = False
    account_info_enabled: bool = False
    supported_markets: list[str] = Field(default_factory=list)
    reason: str = "Broker integration disabled by constitutional governance gate"


class Instrument(BrokerBoundaryModel):
    symbol: str
    market_class: str
    display_name: str | None = None
    base_currency: str | None = None
    quote_currency: str | None = None
    price_precision: int | None = Field(default=None, ge=0)
    volume_min: Decimal | None = None
    volume_step: Decimal | None = None


class BrokerAccount(BrokerBoundaryModel):
    account_id: str
    broker_name: str
    currency: str | None = None
    balance: Decimal | None = None
    equity: Decimal | None = None
    is_demo: bool | None = None
    descriptor_only: bool = True


class BrokerQuote(BrokerBoundaryModel):
    symbol: str
    bid: Decimal
    ask: Decimal
    timestamp: datetime
    source: str = "broker:disabled"

    @field_validator("timestamp")
    @classmethod
    def _timestamp_utc(cls, value: datetime) -> datetime:
        normalized = require_utc(value, boundary="broker_quote.timestamp")
        assert normalized is not None
        return normalized


class OrderIntent(BrokerBoundaryModel):
    """Inert hypothetical order description; never dispatched in W1-U03."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    symbol: str
    side: Literal["buy", "sell"]
    order_type: Literal["market", "limit", "stop"]
    volume: Decimal = Field(gt=0)
    requested_price: Decimal | None = None
    stop_loss: Decimal | None = None
    take_profit: Decimal | None = None
    created_at: datetime
    rationale: str | None = None

    @field_validator("created_at")
    @classmethod
    def _created_at_utc(cls, value: datetime) -> datetime:
        normalized = require_utc(value, boundary="order_intent.created_at")
        assert normalized is not None
        return normalized
