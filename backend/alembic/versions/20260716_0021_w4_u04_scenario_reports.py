"""W4-U04 scenario simulation research reports

Revision ID: 20260716_0021
Revises: 20260716_0020
Create Date: 2026-07-16
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260716_0021"
down_revision: Union[str, None] = "20260716_0020"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "scenario_reports",
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
        sa.Column("scenario_name", sa.String(length=128), nullable=False),
        sa.Column("hypothetical_return", sa.Float(), nullable=False),
        sa.Column("scenario_result", sa.JSON(), nullable=False),
        sa.Column("assumptions", sa.JSON(), nullable=False),
        sa.Column("inputs", sa.JSON(), nullable=False),
        sa.Column("uncertainty", sa.JSON(), nullable=False),
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
    op.create_index("ix_scenario_reports_created_at", "scenario_reports", ["created_at"])
    op.create_index(
        "ix_scenario_reports_series",
        "scenario_reports",
        ["market_class", "symbol", "timeframe"],
    )
    op.create_index("ix_scenario_reports_name", "scenario_reports", ["scenario_name"])
    op.create_index("ix_scenario_reports_report_hash", "scenario_reports", ["report_hash"])
    op.create_index(
        "ix_scenario_reports_correlation_id", "scenario_reports", ["audit_correlation_id"]
    )


def downgrade() -> None:
    op.drop_index("ix_scenario_reports_correlation_id", table_name="scenario_reports")
    op.drop_index("ix_scenario_reports_report_hash", table_name="scenario_reports")
    op.drop_index("ix_scenario_reports_name", table_name="scenario_reports")
    op.drop_index("ix_scenario_reports_series", table_name="scenario_reports")
    op.drop_index("ix_scenario_reports_created_at", table_name="scenario_reports")
    op.drop_table("scenario_reports")
