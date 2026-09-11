"""W6-U05 execution research experiments

Revision ID: 20260717_0032
Revises: 20260717_0031
Create Date: 2026-07-17
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260717_0032"
down_revision: Union[str, None] = "20260717_0031"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "execution_research_experiments",
        sa.Column("experiment_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("simulation_mode", sa.String(length=32), nullable=False),
        sa.Column("operator_id", sa.String(length=36), nullable=False),
        sa.Column("experiment_title", sa.String(length=200), nullable=False),
        sa.Column("pre_registration_plan", sa.JSON(), nullable=False),
        sa.Column("plan_hash", sa.String(length=128), nullable=False),
        sa.Column("as_of_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("as_of_window", sa.JSON(), nullable=False),
        sa.Column("replay_input_lineage", sa.JSON(), nullable=False),
        sa.Column("included_scope_summary", sa.JSON(), nullable=False),
        sa.Column("uncertainty", sa.JSON(), nullable=False),
        sa.Column("limitations", sa.JSON(), nullable=False),
        sa.Column("research_status", sa.String(length=64), nullable=False),
        sa.Column("simulation_disclaimer", sa.Text(), nullable=False),
        sa.Column("audit_correlation_id", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["operator_id"], ["operators.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("experiment_id"),
    )
    op.create_index(
        "ix_execution_research_experiments_created_at",
        "execution_research_experiments",
        ["created_at"],
    )
    op.create_index(
        "ix_execution_research_experiments_operator",
        "execution_research_experiments",
        ["operator_id"],
    )
    op.create_index(
        "ix_execution_research_experiments_plan_hash",
        "execution_research_experiments",
        ["plan_hash"],
    )
    op.create_index(
        "ix_execution_research_experiments_as_of_time",
        "execution_research_experiments",
        ["as_of_time"],
    )
    op.create_index(
        "ix_execution_research_experiments_correlation_id",
        "execution_research_experiments",
        ["audit_correlation_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_execution_research_experiments_correlation_id",
        table_name="execution_research_experiments",
    )
    op.drop_index(
        "ix_execution_research_experiments_as_of_time",
        table_name="execution_research_experiments",
    )
    op.drop_index(
        "ix_execution_research_experiments_plan_hash",
        table_name="execution_research_experiments",
    )
    op.drop_index(
        "ix_execution_research_experiments_operator",
        table_name="execution_research_experiments",
    )
    op.drop_index(
        "ix_execution_research_experiments_created_at",
        table_name="execution_research_experiments",
    )
    op.drop_table("execution_research_experiments")
