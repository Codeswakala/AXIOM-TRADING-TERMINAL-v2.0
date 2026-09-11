"""W6-U03 simulated paper ledger entries

Revision ID: 20260717_0030
Revises: 20260717_0029
Create Date: 2026-07-17
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260717_0030"
down_revision: Union[str, None] = "20260717_0029"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "simulated_paper_ledger_entries",
        sa.Column("ledger_entry_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("simulation_mode", sa.String(length=32), nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("simulated_fill_id", sa.String(length=36), nullable=False),
        sa.Column("operator_id", sa.String(length=36), nullable=False),
        sa.Column("ledger_event_type", sa.String(length=64), nullable=False),
        sa.Column("simulated_research_direction", sa.String(length=32), nullable=False),
        sa.Column("simulated_units", sa.Float(), nullable=False),
        sa.Column("simulated_entry_value", sa.Float(), nullable=False),
        sa.Column("simulated_exit_value", sa.Float(), nullable=False),
        sa.Column("simulated_return_estimate", sa.Float(), nullable=False),
        sa.Column("uncertainty", sa.JSON(), nullable=False),
        sa.Column("limitations", sa.JSON(), nullable=False),
        sa.Column("research_status", sa.String(length=64), nullable=False),
        sa.Column("simulation_disclaimer", sa.Text(), nullable=False),
        sa.Column("audit_correlation_id", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(
            ["run_id"], ["simulated_execution_runs.run_id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["simulated_fill_id"],
            ["simulated_fill_events.simulated_fill_id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(["operator_id"], ["operators.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("ledger_entry_id"),
    )
    op.create_index(
        "ix_simulated_paper_ledger_entries_created_at",
        "simulated_paper_ledger_entries",
        ["created_at"],
    )
    op.create_index(
        "ix_simulated_paper_ledger_entries_operator",
        "simulated_paper_ledger_entries",
        ["operator_id"],
    )
    op.create_index(
        "ix_simulated_paper_ledger_entries_run",
        "simulated_paper_ledger_entries",
        ["run_id"],
    )
    op.create_index(
        "ix_simulated_paper_ledger_entries_fill",
        "simulated_paper_ledger_entries",
        ["simulated_fill_id"],
    )
    op.create_index(
        "ix_simulated_paper_ledger_entries_correlation_id",
        "simulated_paper_ledger_entries",
        ["audit_correlation_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_simulated_paper_ledger_entries_correlation_id",
        table_name="simulated_paper_ledger_entries",
    )
    op.drop_index(
        "ix_simulated_paper_ledger_entries_fill",
        table_name="simulated_paper_ledger_entries",
    )
    op.drop_index(
        "ix_simulated_paper_ledger_entries_run",
        table_name="simulated_paper_ledger_entries",
    )
    op.drop_index(
        "ix_simulated_paper_ledger_entries_operator",
        table_name="simulated_paper_ledger_entries",
    )
    op.drop_index(
        "ix_simulated_paper_ledger_entries_created_at",
        table_name="simulated_paper_ledger_entries",
    )
    op.drop_table("simulated_paper_ledger_entries")
