"""V2 BE-11 table (BO-V2-BE-11-001 D-2; the DR's one-table ruling).

`v2_paper_bridge_drift_run` is the band's SINGLE table, serving two
declared row kinds under a closed CHECK:

- `drift_run` — C-2 lineage law: every drift computation (clean or
  divergent) lands exactly one evidenced row (both-side figures,
  verdict, tolerances-in-force snapshot);
- `seed` — the BO §0 seed slots: tolerance rows
  (`payload = {name, value, unit, citation}`) and the staleness row
  (`payload = {max_age_hours, citation}`), landed ONLY by a future
  operator overlay migration. The band ships with ZERO seed rows —
  absence is the empty-forced state the engine fail-closes on.

Append-only (guard pair; zero-UPDATE regime).
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    JSON,
    CheckConstraint,
    DateTime,
    Index,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.v2.temporal.validation import utc_now


class V2PaperBridgeDriftRun(Base):
    """Drift-run lineage + seed slots (one table, two declared kinds)."""

    __tablename__ = "v2_paper_bridge_drift_run"
    __table_args__ = (
        Index("ix_v2_pbdrift_created", "created_at"),
        CheckConstraint("run_kind IN ('drift_run','seed')",
                        name="ck_v2_pbdrift_kind"),
        CheckConstraint(
            "verdict IN ('within_tolerance','drift_minor','drift_major',"
            "'uncomputable') OR verdict IS NULL",
            name="ck_v2_pbdrift_verdict"),
        CheckConstraint(
            "(run_kind = 'drift_run') = (verdict IS NOT NULL)",
            name="ck_v2_pbdrift_verdict_iff"),
        CheckConstraint(
            "seed_name IS NULL OR run_kind = 'seed'",
            name="ck_v2_pbdrift_seed_kind"),
        CheckConstraint("data_class IN ('simulated')",
                        name="ck_v2_pbdrift_data_class"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    run_kind: Mapped[str] = mapped_column(String(16), nullable=False)
    # drift_run fields (NULL on seed rows)
    basis_sync_run_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    paper_side: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    broker_side: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    tolerances_in_force: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    verdict: Mapped[str | None] = mapped_column(String(24), nullable=True)
    digest: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # seed fields (NULL on drift rows)
    seed_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    # regime
    actor_id: Mapped[str] = mapped_column(String(128), nullable=False)
    data_class: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    operator_id: Mapped[str] = mapped_column(String(128), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False)
