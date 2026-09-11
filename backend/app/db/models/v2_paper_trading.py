"""V2 BE-8 tables (BO-V2-BE-8-001 D-2; design S1.1 — eight tables).

Zero-UPDATE regime (design S1.2): every table guarded UPDATE+DELETE; order
state lives in the append-only event ledger; current state is derived
(max event_index). N4: fill_class CHECK admits exactly 'paper_simulated'.
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    JSON,
    CheckConstraint,
    DateTime,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.v2.temporal.validation import utc_now

_DATA_CLASS_CHECK = (
    "data_class IN ('synthetic','simulated','historical_real','live',"
    "'stale_cached','unavailable')"
)


class V2PaperAccount(Base):
    """Versioned-immutable paper account (S1.1 row 1)."""

    __tablename__ = "v2_paper_account"
    __table_args__ = (
        UniqueConstraint("account_id", "record_seq", name="uq_v2_pacct_id_seq"),
        Index("ix_v2_pacct_account", "account_id"),
        CheckConstraint("base_currency IN ('USD')", name="ck_v2_pacct_ccy"),
        CheckConstraint(
            "lifecycle_state IN ('active','frozen','closed')",
            name="ck_v2_pacct_state"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_pacct_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    account_id: Mapped[str] = mapped_column(String(64), nullable=False)
    record_seq: Mapped[int] = mapped_column(Integer, nullable=False)
    supersedes: Mapped[str | None] = mapped_column(String(36), nullable=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    base_currency: Mapped[str] = mapped_column(String(8), nullable=False)
    initial_balance: Mapped[str] = mapped_column(String(64), nullable=False)
    margin_params: Mapped[dict] = mapped_column(JSON, nullable=False)
    lifecycle_state: Mapped[str] = mapped_column(String(16), nullable=False)
    confirmation_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2PaperOrderIntent(Base):
    """Write-once order intent (S1.1 row 2; N3 anchor)."""

    __tablename__ = "v2_paper_order_intent"
    __table_args__ = (
        UniqueConstraint("account_id", "idempotency_key",
                         name="uq_v2_pintent_idem"),
        Index("ix_v2_pintent_account", "account_id"),
        CheckConstraint("side IN ('buy','sell')", name="ck_v2_pintent_side"),
        CheckConstraint("order_type IN ('market','limit')",
                        name="ck_v2_pintent_type"),
        CheckConstraint("time_in_force IN ('replay_window')",
                        name="ck_v2_pintent_tif"),
        CheckConstraint(
            "(order_type = 'limit') = (limit_price IS NOT NULL)",
            name="ck_v2_pintent_limit_iff"),
        CheckConstraint("CAST(quantity AS REAL) > 0",
                        name="ck_v2_pintent_qty"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_pintent_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    intent_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    account_id: Mapped[str] = mapped_column(String(36), nullable=False)
    instrument_id: Mapped[str] = mapped_column(String(64), nullable=False)
    side: Mapped[str] = mapped_column(String(8), nullable=False)
    order_type: Mapped[str] = mapped_column(String(16), nullable=False)
    quantity: Mapped[str] = mapped_column(String(64), nullable=False)
    limit_price: Mapped[str | None] = mapped_column(String(64), nullable=True)
    time_in_force: Mapped[str] = mapped_column(String(16), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(64), nullable=False)
    snapshot_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    time_basis: Mapped[dict] = mapped_column(JSON, nullable=False)
    confirmation_ref: Mapped[str | None] = mapped_column(String(64), nullable=True)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2PaperRiskDecision(Base):
    """Immutable risk decision — exactly one per intent (S1.1 row 3; S8)."""

    __tablename__ = "v2_paper_risk_decision"
    __table_args__ = (
        UniqueConstraint("intent_id", name="uq_v2_prisk_intent"),
        CheckConstraint("decision IN ('pass','block','hold')",
                        name="ck_v2_prisk_decision"),
        # C-1b: ref NOT NULL iff hold — both directions.
        CheckConstraint(
            "(decision = 'hold') = (confirmation_ref IS NOT NULL)",
            name="ck_v2_prisk_ref_iff"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_prisk_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    intent_id: Mapped[str] = mapped_column(String(36), nullable=False)
    decision: Mapped[str] = mapped_column(String(8), nullable=False)
    evaluated_limits: Mapped[dict] = mapped_column(JSON, nullable=False)
    reasons: Mapped[dict] = mapped_column(JSON, nullable=False)
    risk_config_version: Mapped[str] = mapped_column(String(32), nullable=False)
    decided_at_basis: Mapped[dict] = mapped_column(JSON, nullable=False)
    confirmation_ref: Mapped[str | None] = mapped_column(String(64), nullable=True)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2PaperOrderEvent(Base):
    """Append-only order event ledger (S1.1 row 4; S2.3 derivation law)."""

    __tablename__ = "v2_paper_order_event"
    __table_args__ = (
        UniqueConstraint("intent_id", "event_index", name="uq_v2_pevent_idx"),
        Index("ix_v2_pevent_intent", "intent_id"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_pevent_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    intent_id: Mapped[str] = mapped_column(String(36), nullable=False)
    event_index: Mapped[int] = mapped_column(Integer, nullable=False)
    from_state: Mapped[str] = mapped_column(String(24), nullable=False)
    to_state: Mapped[str] = mapped_column(String(24), nullable=False)
    event_class: Mapped[str] = mapped_column(String(48), nullable=False)
    details: Mapped[dict] = mapped_column(JSON, nullable=False)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2PaperFill(Base):
    """Immutable fill — N4: fill_class single-value CHECK (S1.1 row 5)."""

    __tablename__ = "v2_paper_fill"
    __table_args__ = (
        UniqueConstraint("intent_id", "fill_index", name="uq_v2_pfill_idx"),
        Index("ix_v2_pfill_intent", "intent_id"),
        CheckConstraint("fill_class IN ('paper_simulated')",
                        name="ck_v2_pfill_class"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_pfill_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    fill_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    intent_id: Mapped[str] = mapped_column(String(36), nullable=False)
    fill_index: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[str] = mapped_column(String(64), nullable=False)
    raw_price: Mapped[str] = mapped_column(String(64), nullable=False)
    effective_price: Mapped[str] = mapped_column(String(64), nullable=False)
    cost_model_ref: Mapped[dict] = mapped_column(JSON, nullable=False)
    fill_class: Mapped[str] = mapped_column(String(24), nullable=False)
    simulator_version: Mapped[str] = mapped_column(String(32), nullable=False)
    snapshot_ref: Mapped[str] = mapped_column(String(64), nullable=False)
    time_basis: Mapped[dict] = mapped_column(JSON, nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2PaperPositionSnapshot(Base):
    """Immutable derived positions artifact (S1.1 row 6; anchor law)."""

    __tablename__ = "v2_paper_position_snapshot"
    __table_args__ = (
        UniqueConstraint("account_id", "derivation_inputs_hash",
                         "engine_versions_hash",
                         name="uq_v2_ppos_anchor"),
        Index("ix_v2_ppos_account", "account_id"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_ppos_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), nullable=False)
    as_of_basis: Mapped[dict] = mapped_column(JSON, nullable=False)
    positions: Mapped[dict] = mapped_column(JSON, nullable=False)
    derivation_inputs_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    engine_versions_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2PaperBalanceSnapshot(Base):
    """Immutable derived balances artifact (S1.1 row 7; anchor law)."""

    __tablename__ = "v2_paper_balance_snapshot"
    __table_args__ = (
        UniqueConstraint("account_id", "derivation_inputs_hash",
                         "engine_versions_hash",
                         name="uq_v2_pbal_anchor"),
        Index("ix_v2_pbal_account", "account_id"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_pbal_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), nullable=False)
    as_of_basis: Mapped[dict] = mapped_column(JSON, nullable=False)
    cash: Mapped[str] = mapped_column(String(64), nullable=False)
    equity: Mapped[str] = mapped_column(String(64), nullable=False)
    margin_used: Mapped[str] = mapped_column(String(64), nullable=False)
    margin_available: Mapped[str] = mapped_column(String(64), nullable=False)
    unrealized_pnl: Mapped[str] = mapped_column(String(64), nullable=False)
    realized_pnl: Mapped[str] = mapped_column(String(64), nullable=False)
    derivation_inputs_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    engine_versions_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2PaperReconciliation(Base):
    """Immutable reconciliation record (S1.1 row 8; S5 genesis recompute)."""

    __tablename__ = "v2_paper_reconciliation"
    __table_args__ = (
        Index("ix_v2_precon_account", "account_id"),
        CheckConstraint("outcome IN ('consistent','discrepant')",
                        name="ck_v2_precon_outcome"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_precon_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    account_id: Mapped[str] = mapped_column(String(36), nullable=False)
    run_basis: Mapped[dict] = mapped_column(JSON, nullable=False)
    outcome: Mapped[str] = mapped_column(String(16), nullable=False)
    discrepancies: Mapped[dict] = mapped_column(JSON, nullable=False)
    inputs_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)
