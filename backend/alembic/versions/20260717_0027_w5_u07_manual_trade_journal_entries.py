"""W5-U07 manual trade journal entries

Revision ID: 20260717_0027
Revises: 20260717_0026
Create Date: 2026-07-17
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260717_0027"
down_revision: Union[str, None] = "20260717_0026"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "manual_trade_journal_entries",
        sa.Column("journal_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("operator_id", sa.String(length=128), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("reflection_text", sa.Text(), nullable=False),
        sa.Column("linked_plan_id", sa.String(length=36), nullable=True),
        sa.Column("linked_signal_ids", sa.JSON(), nullable=False),
        sa.Column("linked_report_ids", sa.JSON(), nullable=False),
        sa.Column("emotion_tags", sa.JSON(), nullable=False),
        sa.Column("process_tags", sa.JSON(), nullable=False),
        sa.Column("lesson_notes", sa.Text(), nullable=True),
        sa.Column("research_disclaimer", sa.Text(), nullable=False),
        sa.Column("research_status", sa.String(length=64), nullable=False),
        sa.Column("audit_correlation_id", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("journal_id"),
    )
    op.create_index(
        "ix_manual_trade_journal_entries_created_at",
        "manual_trade_journal_entries",
        ["created_at"],
    )
    op.create_index(
        "ix_manual_trade_journal_entries_operator",
        "manual_trade_journal_entries",
        ["operator_id"],
    )
    op.create_index(
        "ix_manual_trade_journal_entries_linked_plan",
        "manual_trade_journal_entries",
        ["linked_plan_id"],
    )
    op.create_index(
        "ix_manual_trade_journal_entries_correlation_id",
        "manual_trade_journal_entries",
        ["audit_correlation_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_manual_trade_journal_entries_correlation_id",
        table_name="manual_trade_journal_entries",
    )
    op.drop_index(
        "ix_manual_trade_journal_entries_linked_plan",
        table_name="manual_trade_journal_entries",
    )
    op.drop_index(
        "ix_manual_trade_journal_entries_operator",
        table_name="manual_trade_journal_entries",
    )
    op.drop_index(
        "ix_manual_trade_journal_entries_created_at",
        table_name="manual_trade_journal_entries",
    )
    op.drop_table("manual_trade_journal_entries")
