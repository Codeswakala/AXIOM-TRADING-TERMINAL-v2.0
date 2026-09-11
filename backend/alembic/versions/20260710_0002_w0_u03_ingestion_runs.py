"""W0-U03 ingestion_runs metadata table

Revision ID: 20260710_0002
Revises: 20260710_0001
Create Date: 2026-07-10

"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260710_0002"
down_revision: Union[str, None] = "20260710_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ingestion_runs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("source_type", sa.String(length=32), nullable=False),
        sa.Column("source_name", sa.String(length=512), nullable=False),
        sa.Column("market_class", sa.String(length=32), nullable=False),
        sa.Column("symbol", sa.String(length=64), nullable=False),
        sa.Column("timeframe", sa.String(length=16), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("rows_read", sa.Integer(), nullable=False),
        sa.Column("rows_valid", sa.Integer(), nullable=False),
        sa.Column("rows_invalid", sa.Integer(), nullable=False),
        sa.Column("rows_inserted", sa.Integer(), nullable=False),
        sa.Column("rows_updated", sa.Integer(), nullable=False),
        sa.Column("rows_unchanged", sa.Integer(), nullable=False),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("error_summary", sa.Text(), nullable=True),
        sa.Column("details", sa.JSON(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_ingestion_runs")),
    )
    op.create_index(
        "ix_ingestion_runs_symbol_started",
        "ingestion_runs",
        ["symbol", "started_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_ingestion_runs_symbol_started", table_name="ingestion_runs")
    op.drop_table("ingestion_runs")
