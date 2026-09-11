"""W5-U06 trade plan notes

Revision ID: 20260717_0026
Revises: 20260717_0025
Create Date: 2026-07-17
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260717_0026"
down_revision: Union[str, None] = "20260717_0025"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "trade_plan_notes",
        sa.Column("plan_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("operator_id", sa.String(length=128), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("market_context", sa.Text(), nullable=False),
        sa.Column("hypothesis", sa.Text(), nullable=False),
        sa.Column("linked_signal_ids", sa.JSON(), nullable=False),
        sa.Column("linked_report_ids", sa.JSON(), nullable=False),
        sa.Column("scenario_notes", sa.Text(), nullable=True),
        sa.Column("risk_notes", sa.Text(), nullable=True),
        sa.Column("invalidating_conditions_text", sa.Text(), nullable=True),
        sa.Column("decision_status", sa.String(length=32), nullable=False),
        sa.Column("research_disclaimer", sa.Text(), nullable=False),
        sa.Column("research_status", sa.String(length=64), nullable=False),
        sa.Column("audit_correlation_id", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("plan_id"),
    )
    op.create_index("ix_trade_plan_notes_created_at", "trade_plan_notes", ["created_at"])
    op.create_index("ix_trade_plan_notes_updated_at", "trade_plan_notes", ["updated_at"])
    op.create_index("ix_trade_plan_notes_operator", "trade_plan_notes", ["operator_id"])
    op.create_index(
        "ix_trade_plan_notes_decision_status",
        "trade_plan_notes",
        ["decision_status"],
    )
    op.create_index(
        "ix_trade_plan_notes_correlation_id",
        "trade_plan_notes",
        ["audit_correlation_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_trade_plan_notes_correlation_id", table_name="trade_plan_notes")
    op.drop_index("ix_trade_plan_notes_decision_status", table_name="trade_plan_notes")
    op.drop_index("ix_trade_plan_notes_operator", table_name="trade_plan_notes")
    op.drop_index("ix_trade_plan_notes_updated_at", table_name="trade_plan_notes")
    op.drop_index("ix_trade_plan_notes_created_at", table_name="trade_plan_notes")
    op.drop_table("trade_plan_notes")
