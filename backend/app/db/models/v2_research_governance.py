"""V2 BE-5 ML-governance tables (BO-V2-BE-5-001 T-2; P-1/P-2/P-3 applied).

All rows immutable at the DB level (R-2 guards in migration 0044);
governance state changes = new row with incremented ``record_seq``
(P-1 row versioning); current state = greatest ``record_seq``.
PKs uuid4 TEXT(36).
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


class V2MlGovernanceRecord(Base):
    """Versioned governance overlay row for one V1 model artifact (P-1)."""

    __tablename__ = "v2_ml_governance_record"
    __table_args__ = (
        UniqueConstraint("model_artifact_id", "record_seq",
                         name="uq_v2_mlgov_artifact_seq"),
        Index("ix_v2_mlgov_artifact", "model_artifact_id"),
        CheckConstraint(
            "eligibility_status IN ('unevaluated','eligible','ineligible','expired')",
            name="ck_v2_mlgov_eligibility"),
        CheckConstraint(
            "calibration_status IN ('unevaluated','calibrated','miscalibrated','stale')",
            name="ck_v2_mlgov_calibration"),
        CheckConstraint(
            "freshness_status IN ('fresh','stale','expired','unknown')",
            name="ck_v2_mlgov_freshness"),
        CheckConstraint(
            "economic_status IN ('unevaluated','viable','unviable')",
            name="ck_v2_mlgov_economic"),
        CheckConstraint(
            "statistical_status IN ('unevaluated','significant','not_significant')",
            name="ck_v2_mlgov_statistical"),
        CheckConstraint(
            "deployment_class IN ('research','shadow','champion','challenger','retired')",
            name="ck_v2_mlgov_class"),
        CheckConstraint(
            "data_class IN ('synthetic','simulated','historical_real','live',"
            "'stale_cached','unavailable')",
            name="ck_v2_mlgov_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    model_artifact_id: Mapped[str] = mapped_column(String(36), nullable=False)
    record_seq: Mapped[int] = mapped_column(Integer, nullable=False)
    # C-1 (ITRGA-INT-V2-BE-5-DR-001 §2): forward-reading name — this row
    # SUPERSEDES the predecessor row whose id it holds. NULL on genesis.
    supersedes: Mapped[str | None] = mapped_column(String(36), nullable=True)
    registry_version: Mapped[str] = mapped_column(String(64), nullable=False)
    model_type: Mapped[str] = mapped_column(String(64), nullable=False)  # P-3
    instrument_class: Mapped[str] = mapped_column(String(64), nullable=False)  # P-3
    eligibility_status: Mapped[str] = mapped_column(String(32), nullable=False)
    calibration_status: Mapped[str] = mapped_column(String(32), nullable=False)
    freshness_status: Mapped[str] = mapped_column(String(32), nullable=False)
    economic_status: Mapped[str] = mapped_column(String(32), nullable=False)
    statistical_status: Mapped[str] = mapped_column(String(32), nullable=False)
    deployment_class: Mapped[str] = mapped_column(String(32), nullable=False)
    rollback_target_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    evidence_refs: Mapped[dict] = mapped_column(JSON, nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )


class V2MlLifecycleEvent(Base):
    """Append-only governance decision log (immutable — DB guards)."""

    __tablename__ = "v2_ml_lifecycle_event"
    __table_args__ = (
        Index("ix_v2_mlev_record", "governance_record_id"),
        CheckConstraint(
            "event_type IN ('registered','eligibility_evaluated',"
            "'calibration_evaluated','freshness_evaluated',"
            "'economic_evaluated','statistical_evaluated','promoted',"
            "'demoted','refused','rolled_back','retired')",
            name="ck_v2_mlev_type"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    governance_record_id: Mapped[str] = mapped_column(String(36), nullable=False)
    event_type: Mapped[str] = mapped_column(String(48), nullable=False)
    from_value: Mapped[str] = mapped_column(String(64), nullable=False)
    to_value: Mapped[str] = mapped_column(String(64), nullable=False)
    decision_basis: Mapped[dict] = mapped_column(JSON, nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )


class V2MlDiagnosticReport(Base):
    """Immutable ML diagnostic artifact (P-2 — 0043 report-table pattern)."""

    __tablename__ = "v2_ml_diagnostic_report"
    __table_args__ = (
        UniqueConstraint("model_artifact_id", "inputs_hash",
                         "engine_versions_hash",
                         name="uq_v2_mldiag_determinism_anchor"),
        Index("ix_v2_mldiag_artifact", "model_artifact_id"),
        CheckConstraint(
            "data_class IN ('synthetic','simulated','historical_real','live',"
            "'stale_cached','unavailable')",
            name="ck_v2_mldiag_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    model_artifact_id: Mapped[str] = mapped_column(String(36), nullable=False)
    governance_record_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    diagnostics: Mapped[dict] = mapped_column(JSON, nullable=False)
    input_refs: Mapped[dict] = mapped_column(JSON, nullable=False)
    inputs_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    engine_versions: Mapped[dict] = mapped_column(JSON, nullable=False)
    engine_versions_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
