"""W4-U02 correlation intelligence reports

Revision ID: 20260716_0019
Revises: 20260715_0018
Create Date: 2026-07-16
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260716_0019"
down_revision: Union[str, None] = "20260715_0018"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "correlation_reports",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("artifact_type", sa.String(length=96), nullable=False),
        sa.Column("method_version", sa.String(length=96), nullable=False),
        sa.Column("left_market_class", sa.String(length=64), nullable=False),
        sa.Column("left_symbol", sa.String(length=128), nullable=False),
        sa.Column("right_market_class", sa.String(length=64), nullable=False),
        sa.Column("right_symbol", sa.String(length=128), nullable=False),
        sa.Column("timeframe", sa.String(length=32), nullable=False),
        sa.Column("as_of_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("as_of_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("sample_count", sa.Integer(), nullable=False),
        sa.Column("correlation_value", sa.Float(), nullable=False),
        sa.Column("uncertainty", sa.JSON(), nullable=False),
        sa.Column("significance", sa.JSON(), nullable=False),
        sa.Column("economic_usefulness", sa.JSON(), nullable=False),
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
    op.create_index("ix_correlation_reports_created_at", "correlation_reports", ["created_at"])
    op.create_index(
        "ix_correlation_reports_pair",
        "correlation_reports",
        ["left_symbol", "right_symbol", "timeframe"],
    )
    op.create_index("ix_correlation_reports_report_hash", "correlation_reports", ["report_hash"])
    op.create_index(
        "ix_correlation_reports_correlation_id", "correlation_reports", ["audit_correlation_id"]
    )


def downgrade() -> None:
    op.drop_index("ix_correlation_reports_correlation_id", table_name="correlation_reports")
    op.drop_index("ix_correlation_reports_report_hash", table_name="correlation_reports")
    op.drop_index("ix_correlation_reports_pair", table_name="correlation_reports")
    op.drop_index("ix_correlation_reports_created_at", table_name="correlation_reports")
    op.drop_table("correlation_reports")
