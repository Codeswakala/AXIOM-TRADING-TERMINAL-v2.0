"""W6-U02 simulated execution runs

Revision ID: 20260717_0028
Revises: 20260717_0027
Create Date: 2026-07-17
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260717_0028"
down_revision: Union[str, None] = "20260717_0027"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "simulated_execution_runs",
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("operator_id", sa.String(length=36), nullable=False),
        sa.Column("simulation_mode", sa.String(length=32), nullable=False),
        sa.Column("simulation_policy_version", sa.String(length=96), nullable=False),
        sa.Column("input_artifact_ids", sa.JSON(), nullable=False),
        sa.Column("replay_scope", sa.JSON(), nullable=False),
        sa.Column("fill_model_name", sa.String(length=96), nullable=False),
        sa.Column("fill_model_version", sa.String(length=96), nullable=False),
        sa.Column("assumptions", sa.JSON(), nullable=False),
        sa.Column("limitations", sa.JSON(), nullable=False),
        sa.Column("research_status", sa.String(length=64), nullable=False),
        sa.Column("simulation_disclaimer", sa.Text(), nullable=False),
        sa.Column("audit_correlation_id", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["operator_id"], ["operators.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("run_id"),
    )
    op.create_index(
        "ix_simulated_execution_runs_created_at",
        "simulated_execution_runs",
        ["created_at"],
    )
    op.create_index(
        "ix_simulated_execution_runs_operator",
        "simulated_execution_runs",
        ["operator_id"],
    )
    op.create_index(
        "ix_simulated_execution_runs_policy",
        "simulated_execution_runs",
        ["simulation_policy_version"],
    )
    op.create_index(
        "ix_simulated_execution_runs_fill_model",
        "simulated_execution_runs",
        ["fill_model_name", "fill_model_version"],
    )
    op.create_index(
        "ix_simulated_execution_runs_correlation_id",
        "simulated_execution_runs",
        ["audit_correlation_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_simulated_execution_runs_correlation_id",
        table_name="simulated_execution_runs",
    )
    op.drop_index(
        "ix_simulated_execution_runs_fill_model",
        table_name="simulated_execution_runs",
    )
    op.drop_index("ix_simulated_execution_runs_policy", table_name="simulated_execution_runs")
    op.drop_index("ix_simulated_execution_runs_operator", table_name="simulated_execution_runs")
    op.drop_index("ix_simulated_execution_runs_created_at", table_name="simulated_execution_runs")
    op.drop_table("simulated_execution_runs")
