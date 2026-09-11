"""V2 BE-9 tables (BO-V2-BE-9-001 D-2; design S3 — nine tables).

Six projections + sync_run + reconcile_run + discrepancy. Zero-UPDATE
regime; provenance pins NOT NULL on every projection row (N3);
`data_class` CHECK single value 'simulated' (demo money); account
`environment` CHECK 'practice'. The broker is the authority; these rows
are projections, never state (V2-R-10).
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

_DATA_CLASS_CHECK = "data_class IN ('simulated')"




class V2BrokerAccount(Base):
    """Append-only account snapshot generations (S3 row 1)."""

    __tablename__ = "v2_broker_account"
    __table_args__ = (
        UniqueConstraint("provider_id", "broker_account_ext_id",
                         "record_seq", name="uq_v2_bracct_gen"),
        Index("ix_v2_bracct_ext", "broker_account_ext_id"),
        CheckConstraint("environment IN ('practice')",
                        name="ck_v2_bracct_env"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_bracct_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    provider_id: Mapped[str] = mapped_column(String(64), nullable=False)
    broker_account_ext_id: Mapped[str] = mapped_column(String(64), nullable=False)
    record_seq: Mapped[int] = mapped_column(Integer, nullable=False)
    supersedes: Mapped[str | None] = mapped_column(String(36), nullable=True)
    alias: Mapped[str] = mapped_column(String(128), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False)
    environment: Mapped[str] = mapped_column(String(16), nullable=False)
    read_only_login: Mapped[bool] = mapped_column(nullable=False)
    sync_run_id: Mapped[str] = mapped_column(String(36), nullable=False)
    server_hostname: Mapped[str] = mapped_column(String(128), nullable=False)
    fetched_at_basis: Mapped[str] = mapped_column(String(64), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2BrokerBalance(Base):
    """Append-only per-sync balance snapshot (S3 row 2; money law)."""

    __tablename__ = "v2_broker_balance"
    __table_args__ = (
        UniqueConstraint("sync_run_id", "broker_account_ext_id",
                         name="uq_v2_brbal_run"),
        Index("ix_v2_brbal_ext", "broker_account_ext_id"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_brbal_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    provider_id: Mapped[str] = mapped_column(String(64), nullable=False)
    broker_account_ext_id: Mapped[str] = mapped_column(String(64), nullable=False)
    balance: Mapped[str] = mapped_column(String(64), nullable=False)
    margin_used: Mapped[str] = mapped_column(String(64), nullable=False)
    margin_available: Mapped[str] = mapped_column(String(64), nullable=False)
    unrealized_pl: Mapped[str] = mapped_column(String(64), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False)
    sync_run_id: Mapped[str] = mapped_column(String(36), nullable=False)
    server_hostname: Mapped[str] = mapped_column(String(128), nullable=False)
    fetched_at_basis: Mapped[str] = mapped_column(String(64), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2BrokerPosition(Base):
    """Append-only per-sync position snapshot set (S3 row 3)."""

    __tablename__ = "v2_broker_position"
    __table_args__ = (
        UniqueConstraint("sync_run_id", "broker_account_ext_id",
                         "instrument_ext_id", name="uq_v2_brpos_run"),
        Index("ix_v2_brpos_ext", "broker_account_ext_id"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_brpos_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    provider_id: Mapped[str] = mapped_column(String(64), nullable=False)
    broker_account_ext_id: Mapped[str] = mapped_column(String(64), nullable=False)
    instrument_ext_id: Mapped[str] = mapped_column(String(64), nullable=False)
    units_long: Mapped[str] = mapped_column(String(64), nullable=False)
    units_short: Mapped[str] = mapped_column(String(64), nullable=False)
    avg_price_long: Mapped[str] = mapped_column(String(64), nullable=False)
    avg_price_short: Mapped[str] = mapped_column(String(64), nullable=False)
    sync_run_id: Mapped[str] = mapped_column(String(36), nullable=False)
    server_hostname: Mapped[str] = mapped_column(String(128), nullable=False)
    fetched_at_basis: Mapped[str] = mapped_column(String(64), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2BrokerOrder(Base):
    """Append-only per-sync OPEN-order snapshot (S3 row 4; broker state)."""

    __tablename__ = "v2_broker_order"
    __table_args__ = (
        UniqueConstraint("sync_run_id", "order_ext_id",
                         name="uq_v2_brord_run"),
        Index("ix_v2_brord_ext", "order_ext_id"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_brord_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    provider_id: Mapped[str] = mapped_column(String(64), nullable=False)
    order_ext_id: Mapped[str] = mapped_column(String(64), nullable=False)
    broker_account_ext_id: Mapped[str] = mapped_column(String(64), nullable=False)
    order_state_ext: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    sync_run_id: Mapped[str] = mapped_column(String(36), nullable=False)
    server_hostname: Mapped[str] = mapped_column(String(128), nullable=False)
    fetched_at_basis: Mapped[str] = mapped_column(String(64), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2BrokerFill(Base):
    """Append-only fill/transaction ledger (S3 row 5; idempotency anchor)."""

    __tablename__ = "v2_broker_fill"
    __table_args__ = (
        UniqueConstraint("provider_id", "broker_account_ext_id",
                         "transaction_ext_id", name="uq_v2_brfill_anchor"),
        Index("ix_v2_brfill_ext", "broker_account_ext_id"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_brfill_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    provider_id: Mapped[str] = mapped_column(String(64), nullable=False)
    broker_account_ext_id: Mapped[str] = mapped_column(String(64), nullable=False)
    transaction_ext_id: Mapped[str] = mapped_column(String(64), nullable=False)
    tx_type_ext: Mapped[str] = mapped_column(String(64), nullable=False)
    instrument_ext_id: Mapped[str] = mapped_column(String(64), nullable=False)
    units: Mapped[str] = mapped_column(String(64), nullable=False)
    price: Mapped[str] = mapped_column(String(64), nullable=False)
    tx_time_ext: Mapped[str] = mapped_column(String(64), nullable=False)
    sync_run_id: Mapped[str] = mapped_column(String(36), nullable=False)
    server_hostname: Mapped[str] = mapped_column(String(128), nullable=False)
    fetched_at_basis: Mapped[str] = mapped_column(String(64), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2BrokerInstrumentPermission(Base):
    """Append-only per-sync instrument-visibility facts (S3 row 6)."""

    __tablename__ = "v2_broker_instrument_permission"
    __table_args__ = (
        UniqueConstraint("sync_run_id", "broker_account_ext_id",
                         "instrument_ext_id", name="uq_v2_brinst_run"),
        Index("ix_v2_brinst_ext", "instrument_ext_id"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_brinst_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    provider_id: Mapped[str] = mapped_column(String(64), nullable=False)
    broker_account_ext_id: Mapped[str] = mapped_column(String(64), nullable=False)
    instrument_ext_id: Mapped[str] = mapped_column(String(64), nullable=False)
    visibility: Mapped[dict] = mapped_column(JSON, nullable=False)
    display_name: Mapped[str] = mapped_column(String(256), nullable=False)
    sync_run_id: Mapped[str] = mapped_column(String(36), nullable=False)
    server_hostname: Mapped[str] = mapped_column(String(128), nullable=False)
    fetched_at_basis: Mapped[str] = mapped_column(String(64), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2BrokerSyncRun(Base):
    """Sync-run lineage — written ONCE at completion (S4)."""

    __tablename__ = "v2_broker_sync_run"
    __table_args__ = (
        Index("ix_v2_brsync_created", "created_at"),
        CheckConstraint(
            "outcome IN ('complete','partial_refused','failed')",
            name="ck_v2_brsync_outcome"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_brsync_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    provider_id: Mapped[str] = mapped_column(String(64), nullable=False)
    scope: Mapped[dict] = mapped_column(JSON, nullable=False)
    outcome: Mapped[str] = mapped_column(String(24), nullable=False)
    page_counts: Mapped[dict] = mapped_column(JSON, nullable=False)
    origin_basis: Mapped[str] = mapped_column(String(64), nullable=False)
    inputs_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    result_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    refusal: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2BrokerReconcileRun(Base):
    """Reconcile-run lineage — the clean run is evidenced (S5.1/C-2)."""

    __tablename__ = "v2_broker_reconcile_run"
    __table_args__ = (
        Index("ix_v2_brrec_created", "created_at"),
        CheckConstraint("outcome IN ('clean','discrepant')",
                        name="ck_v2_brrec_outcome"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_brrec_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    provider_id: Mapped[str] = mapped_column(String(64), nullable=False)
    sync_run_id: Mapped[str] = mapped_column(String(36), nullable=False)
    compare_scope: Mapped[dict] = mapped_column(JSON, nullable=False)
    broker_side_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    projection_side_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    compared_counts: Mapped[dict] = mapped_column(JSON, nullable=False)
    discrepancy_count: Mapped[int] = mapped_column(Integer, nullable=False)
    outcome: Mapped[str] = mapped_column(String(16), nullable=False)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2BrokerDiscrepancy(Base):
    """Immutable discrepancy generations (S6; zero UPDATE)."""

    __tablename__ = "v2_broker_discrepancy"
    __table_args__ = (
        UniqueConstraint("discrepancy_id", "record_seq",
                         name="uq_v2_brdisc_gen"),
        Index("ix_v2_brdisc_id", "discrepancy_id"),
        CheckConstraint(
            "discrepancy_class IN ('amount_mismatch','missing_on_broker',"
            "'missing_in_axiom','currency_mismatch','timestamp_window',"
            "'permission_visibility','set_mismatch')",
            name="ck_v2_brdisc_class"),
        CheckConstraint(
            "state IN ('detected','triaged','owned','resolved',"
            "'dismissed_with_reason')",
            name="ck_v2_brdisc_state"),
        CheckConstraint(
            "(state = 'dismissed_with_reason') = (dismiss_reason IS NOT NULL)",
            name="ck_v2_brdisc_reason_iff"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_brdisc_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    discrepancy_id: Mapped[str] = mapped_column(String(64), nullable=False)
    record_seq: Mapped[int] = mapped_column(Integer, nullable=False)
    supersedes: Mapped[str | None] = mapped_column(String(36), nullable=True)
    reconcile_run_id: Mapped[str] = mapped_column(String(36), nullable=False)
    discrepancy_class: Mapped[str] = mapped_column(String(32), nullable=False)
    state: Mapped[str] = mapped_column(String(32), nullable=False)
    broker_side: Mapped[dict] = mapped_column(JSON, nullable=False)
    projection_side: Mapped[dict] = mapped_column(JSON, nullable=False)
    owned_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    dismiss_reason: Mapped[str | None] = mapped_column(String(512), nullable=True)
    provider_id: Mapped[str] = mapped_column(String(64), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)
