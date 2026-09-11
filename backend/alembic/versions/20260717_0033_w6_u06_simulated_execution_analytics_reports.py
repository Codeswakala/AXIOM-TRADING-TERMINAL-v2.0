"""W6-U06 simulated execution analytics reports

Revision ID: 20260717_0033
Revises: 20260717_0032
Create Date: 2026-07-17
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260717_0033"
down_revision: Union[str, None] = "20260717_0032"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "simulated_execution_analytics_reports",
        sa.Column("report_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("simulation_mode", sa.String(length=32), nullable=False),
        sa.Column("analytics_type", sa.String(length=96), nullable=False),
        sa.Column("included_scope", sa.JSON(), nullable=False),
        sa.Column("sample_count", sa.Integer(), nullable=False),
        sa.Column("metrics", sa.JSON(), nullable=False),
        sa.Column("uncertainty", sa.JSON(), nullable=False),
        sa.Column("limitations", sa.JSON(), nullable=False),
        sa.Column("economic_usefulness", sa.JSON(), nullable=False),
        sa.Column("report_hash", sa.String(length=128), nullable=False),
        sa.Column("source_artifact_ids", sa.JSON(), nullable=False),
        sa.Column("research_status", sa.String(length=64), nullable=False),
        sa.Column("simulation_disclaimer", sa.Text(), nullable=False),
        sa.Column("audit_correlation_id", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("report_id"),
    )
    op.create_index(
        "ix_simulated_execution_analytics_reports_created_at",
        "simulated_execution_analytics_reports",
        ["created_at"],
    )
    op.create_index(
        "ix_simulated_execution_analytics_reports_type",
        "simulated_execution_analytics_reports",
        ["analytics_type"],
    )
    op.create_index(
        "ix_simulated_execution_analytics_reports_hash",
        "simulated_execution_analytics_reports",
        ["report_hash"],
    )
    op.create_index(
        "ix_simulated_execution_analytics_reports_correlation_id",
        "simulated_execution_analytics_reports",
        ["audit_correlation_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_simulated_execution_analytics_reports_correlation_id",
        table_name="simulated_execution_analytics_reports",
    )
    op.drop_index(
        "ix_simulated_execution_analytics_reports_hash",
        table_name="simulated_execution_analytics_reports",
    )
    op.drop_index(
        "ix_simulated_execution_analytics_reports_type",
        table_name="simulated_execution_analytics_reports",
    )
    op.drop_index(
        "ix_simulated_execution_analytics_reports_created_at",
        table_name="simulated_execution_analytics_reports",
    )
    op.drop_table("simulated_execution_analytics_reports")
