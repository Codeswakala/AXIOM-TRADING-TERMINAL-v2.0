"""W4-U03 regime detection reports

Revision ID: 20260716_0020
Revises: 20260716_0019
Create Date: 2026-07-16
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260716_0020"
down_revision: Union[str, None] = "20260716_0019"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "regime_reports",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("artifact_type", sa.String(length=96), nullable=False),
        sa.Column("method_version", sa.String(length=96), nullable=False),
        sa.Column("market_class", sa.String(length=64), nullable=False),
        sa.Column("symbol", sa.String(length=128), nullable=False),
        sa.Column("timeframe", sa.String(length=32), nullable=False),
        sa.Column("as_of_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("as_of_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("sample_count", sa.Integer(), nullable=False),
        sa.Column("regime_label", sa.String(length=64), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("uncertainty", sa.JSON(), nullable=False),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column("economic_meaning", sa.JSON(), nullable=False),
        sa.Column("config", sa.JSON(), nullable=False),
        sa.Column("input_lineage", sa.JSON(), nullable=False),
        sa.Column("source_artifact_ids", sa.JSON(), nullable=False),
        sa.Column("market_scope", sa.JSON(), nullable=False),
        sa.Column("results", sa.JSON(), nullable=False),
        sa.Column("limitations", sa.JSON(), nullable=False),
        sa.Column("report_hash", sa.String(length=128), nullable=False),
        sa.Column("research_status", sa.String(length=64), nullable=False),
        sa.Column("created_by", sa.String(length=128), nullable=False),
        sa.Column("audit_correlation_id", sa.String(length=64), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_regime_reports_created_at", "regime_reports", ["created_at"])
    op.create_index(
        "ix_regime_reports_series",
        "regime_reports",
        ["market_class", "symbol", "timeframe"],
    )
    op.create_index("ix_regime_reports_label", "regime_reports", ["regime_label"])
    op.create_index("ix_regime_reports_report_hash", "regime_reports", ["report_hash"])
    op.create_index("ix_regime_reports_correlation_id", "regime_reports", ["audit_correlation_id"])


def downgrade() -> None:
    op.drop_index("ix_regime_reports_correlation_id", table_name="regime_reports")
    op.drop_index("ix_regime_reports_report_hash", table_name="regime_reports")
    op.drop_index("ix_regime_reports_label", table_name="regime_reports")
    op.drop_index("ix_regime_reports_series", table_name="regime_reports")
    op.drop_index("ix_regime_reports_created_at", table_name="regime_reports")
    op.drop_table("regime_reports")
