"""W6-U04 execution risk research reports

Revision ID: 20260717_0031
Revises: 20260717_0030
Create Date: 2026-07-17
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260717_0031"
down_revision: Union[str, None] = "20260717_0030"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "execution_risk_research_reports",
        sa.Column("report_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("simulation_mode", sa.String(length=32), nullable=False),
        sa.Column("input_artifact_ids", sa.JSON(), nullable=False),
        sa.Column("simulated_request_summary", sa.JSON(), nullable=False),
        sa.Column("risk_metrics", sa.JSON(), nullable=False),
        sa.Column("uncertainty", sa.JSON(), nullable=False),
        sa.Column("limitations", sa.JSON(), nullable=False),
        sa.Column("economic_usefulness", sa.JSON(), nullable=False),
        sa.Column("research_status", sa.String(length=64), nullable=False),
        sa.Column("simulation_disclaimer", sa.Text(), nullable=False),
        sa.Column("audit_correlation_id", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("report_id"),
    )
    op.create_index(
        "ix_execution_risk_reports_created_at",
        "execution_risk_research_reports",
        ["created_at"],
    )
    op.create_index(
        "ix_execution_risk_reports_correlation_id",
        "execution_risk_research_reports",
        ["audit_correlation_id"],
    )
    op.create_index(
        "ix_execution_risk_reports_simulation_mode",
        "execution_risk_research_reports",
        ["simulation_mode"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_execution_risk_reports_simulation_mode",
        table_name="execution_risk_research_reports",
    )
    op.drop_index(
        "ix_execution_risk_reports_correlation_id",
        table_name="execution_risk_research_reports",
    )
    op.drop_index(
        "ix_execution_risk_reports_created_at",
        table_name="execution_risk_research_reports",
    )
    op.drop_table("execution_risk_research_reports")
