"""W4-U06 professional signal validation reports

Revision ID: 20260716_0023
Revises: 20260716_0022
Create Date: 2026-07-16
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260716_0023"
down_revision: Union[str, None] = "20260716_0022"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "signal_validation_reports",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("artifact_type", sa.String(length=96), nullable=False),
        sa.Column("method_version", sa.String(length=96), nullable=False),
        sa.Column("scope_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("scope_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("sample_count", sa.Integer(), nullable=False),
        sa.Column("metrics", sa.JSON(), nullable=False),
        sa.Column("uncertainty", sa.JSON(), nullable=False),
        sa.Column("validation_scope", sa.JSON(), nullable=False),
        sa.Column("outcome_data_status", sa.JSON(), nullable=False),
        sa.Column("economic_usefulness", sa.JSON(), nullable=False),
        sa.Column("config", sa.JSON(), nullable=False),
        sa.Column("input_lineage", sa.JSON(), nullable=False),
        sa.Column("source_signal_ids", sa.JSON(), nullable=False),
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
    op.create_index(
        "ix_signal_validation_reports_created_at",
        "signal_validation_reports",
        ["created_at"],
    )
    op.create_index(
        "ix_signal_validation_reports_scope",
        "signal_validation_reports",
        ["scope_start", "scope_end"],
    )
    op.create_index(
        "ix_signal_validation_reports_report_hash",
        "signal_validation_reports",
        ["report_hash"],
    )
    op.create_index(
        "ix_signal_validation_reports_correlation_id",
        "signal_validation_reports",
        ["audit_correlation_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_signal_validation_reports_correlation_id",
        table_name="signal_validation_reports",
    )
    op.drop_index(
        "ix_signal_validation_reports_report_hash",
        table_name="signal_validation_reports",
    )
    op.drop_index("ix_signal_validation_reports_scope", table_name="signal_validation_reports")
    op.drop_index("ix_signal_validation_reports_created_at", table_name="signal_validation_reports")
    op.drop_table("signal_validation_reports")
