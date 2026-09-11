"""V2 BE-7 tables (BO-V2-BE-7-001 §1 U-1; six physical tables).

Five guarded-immutable + the band's sole mutable row set
(`v2_research_job` — FP-1 accepted model: mutable queue state, immutable
attempt ledger, C1/C2 write-once/mutable-set conditions).
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


class V2BacktestInput(Base):
    """Versioned-immutable input registry (REQ-1.3)."""

    __tablename__ = "v2_backtest_input"
    __table_args__ = (
        UniqueConstraint("input_id", "record_seq", name="uq_v2_btin_id_seq"),
        UniqueConstraint("content_hash", name="uq_v2_btin_content"),
        Index("ix_v2_btin_input", "input_id"),
        CheckConstraint(
            "registration_outcome IN ('registered','reused','refused')",
            name="ck_v2_btin_outcome"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_btin_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    input_id: Mapped[str] = mapped_column(String(64), nullable=False)
    record_seq: Mapped[int] = mapped_column(Integer, nullable=False)
    supersedes: Mapped[str | None] = mapped_column(String(36), nullable=True)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    series_refs: Mapped[dict] = mapped_column(JSON, nullable=False)
    window_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    window_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    registration_outcome: Mapped[str] = mapped_column(String(16), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2CostModel(Base):
    """Versioned-immutable cost-model configuration (REQ-1.4)."""

    __tablename__ = "v2_cost_model"
    __table_args__ = (
        UniqueConstraint("cost_model_id", "record_seq",
                         name="uq_v2_cost_id_seq"),
        Index("ix_v2_cost_model", "cost_model_id"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_cost_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    cost_model_id: Mapped[str] = mapped_column(String(64), nullable=False)
    record_seq: Mapped[int] = mapped_column(Integer, nullable=False)
    supersedes: Mapped[str | None] = mapped_column(String(36), nullable=True)
    spread: Mapped[dict] = mapped_column(JSON, nullable=False)
    commission: Mapped[dict] = mapped_column(JSON, nullable=False)
    slippage: Mapped[dict] = mapped_column(JSON, nullable=False)
    latency_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_limits: Mapped[dict] = mapped_column(JSON, nullable=False)
    citations: Mapped[dict] = mapped_column(JSON, nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2StrategyVersion(Base):
    """Versioned-immutable strategy registry (REQ-1.6). Structurally free
    of credential/adapter/order/account fields (P-9)."""

    __tablename__ = "v2_strategy_version"
    __table_args__ = (
        UniqueConstraint("strategy_id", "record_seq",
                         name="uq_v2_strat_id_seq"),
        Index("ix_v2_strat_strategy", "strategy_id"),
        CheckConstraint(
            "lifecycle_state IN ('draft','registered','retired')",
            name="ck_v2_strat_state"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_strat_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    strategy_id: Mapped[str] = mapped_column(String(64), nullable=False)
    record_seq: Mapped[int] = mapped_column(Integer, nullable=False)
    supersedes: Mapped[str | None] = mapped_column(String(36), nullable=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    parameters: Mapped[dict] = mapped_column(JSON, nullable=False)
    lifecycle_state: Mapped[str] = mapped_column(String(16), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2ResearchJob(Base):
    """The governed queue — the band's SOLE mutable row set (FP-1).
    C1: owner/authorization_ref/inputs/schedule write-once.
    C2: mutable set exactly {job_state, attempt_count, output_ref, failure}."""

    __tablename__ = "v2_research_job"
    __table_args__ = (
        Index("ix_v2_job_state", "job_state"),
        CheckConstraint(
            "job_state IN ('queued','running','succeeded','failed',"
            "'cancelled')",
            name="ck_v2_job_state"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_job_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    owner: Mapped[str] = mapped_column(String(128), nullable=False)
    authorization_ref: Mapped[str] = mapped_column(String(128), nullable=False)
    inputs: Mapped[dict] = mapped_column(JSON, nullable=False)
    schedule: Mapped[dict] = mapped_column(JSON, nullable=False)
    output_ref: Mapped[str | None] = mapped_column(String(36), nullable=True)
    failure: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    job_state: Mapped[str] = mapped_column(String(16), nullable=False)
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2ResearchJobAttempt(Base):
    """Append-only attempt ledger — the P-10 idempotency anchor."""

    __tablename__ = "v2_research_job_attempt"
    __table_args__ = (
        UniqueConstraint("job_id", "attempt_index", name="uq_v2_jobatt_idx"),
        Index("ix_v2_jobatt_job", "job_id"),
        CheckConstraint(
            "outcome IN ('succeeded','failed','cancelled')",
            name="ck_v2_jobatt_outcome"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    job_id: Mapped[str] = mapped_column(String(36), nullable=False)
    attempt_index: Mapped[int] = mapped_column(Integer, nullable=False)
    outcome: Mapped[str] = mapped_column(String(16), nullable=False)
    artifact_ref: Mapped[str | None] = mapped_column(String(36), nullable=True)
    reason: Mapped[dict] = mapped_column(JSON, nullable=False)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)


class V2ResearchResult(Base):
    """Immutable result artifacts. `paper`/`live` absent from the CHECK —
    schema-impossible (P-9)."""

    __tablename__ = "v2_research_result"
    __table_args__ = (
        UniqueConstraint("strategy_version_id", "inputs_hash",
                         "engine_versions_hash",
                         name="uq_v2_result_determinism_anchor"),
        Index("ix_v2_result_job", "job_id"),
        CheckConstraint("result_class IN ('backtest','simulation')",
                        name="ck_v2_result_class"),
        CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_result_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    result_class: Mapped[str] = mapped_column(String(16), nullable=False)
    job_id: Mapped[str] = mapped_column(String(36), nullable=False)
    attempt_index: Mapped[int] = mapped_column(Integer, nullable=False)
    strategy_version_id: Mapped[str] = mapped_column(String(36), nullable=False)
    input_registry_id: Mapped[str] = mapped_column(String(36), nullable=False)
    cost_model_id: Mapped[str] = mapped_column(String(36), nullable=False)
    inputs_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    engine_versions: Mapped[dict] = mapped_column(JSON, nullable=False)
    engine_versions_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    summary: Mapped[dict] = mapped_column(JSON, nullable=False)
    replay_of: Mapped[str | None] = mapped_column(String(36), nullable=True)
    time_basis: Mapped[dict] = mapped_column(JSON, nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)
