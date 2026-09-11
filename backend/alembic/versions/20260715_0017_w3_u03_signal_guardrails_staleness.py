"""W3-U03 signal guardrail freshness fields

Revision ID: 20260715_0017
Revises: 20260715_0016
Create Date: 2026-07-15
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260715_0017"
down_revision: Union[str, None] = "20260715_0016"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "advisory_signals",
        sa.Column("input_staleness_seconds", sa.Integer(), nullable=True),
    )
    op.add_column(
        "advisory_signals",
        sa.Column("signal_validity_seconds", sa.Integer(), nullable=True),
    )
    op.add_column(
        "advisory_signals",
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "advisory_signals",
        sa.Column("freshness_status", sa.String(length=64), nullable=True),
    )
    op.create_index("ix_advisory_signals_expires_at", "advisory_signals", ["expires_at"])
    op.create_index(
        "ix_advisory_signals_freshness_status",
        "advisory_signals",
        ["freshness_status"],
    )


def downgrade() -> None:
    op.drop_index("ix_advisory_signals_freshness_status", table_name="advisory_signals")
    op.drop_index("ix_advisory_signals_expires_at", table_name="advisory_signals")
    op.drop_column("advisory_signals", "freshness_status")
    op.drop_column("advisory_signals", "expires_at")
    op.drop_column("advisory_signals", "signal_validity_seconds")
    op.drop_column("advisory_signals", "input_staleness_seconds")
