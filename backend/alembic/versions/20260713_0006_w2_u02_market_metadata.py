"""W2-U02 market series metadata table

Revision ID: 20260713_0006
Revises: 20260713_0005
Create Date: 2026-07-13
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260713_0006"
down_revision: Union[str, None] = "20260713_0005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "market_series_metadata",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("market_class", sa.String(length=32), nullable=False),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("symbol", sa.String(length=64), nullable=False),
        sa.Column("timeframe", sa.String(length=16), nullable=False),
        sa.Column("session_calendar", sa.String(length=128), nullable=True),
        sa.Column("tick_size", sa.Numeric(precision=24, scale=10), nullable=True),
        sa.Column("price_precision", sa.Integer(), nullable=True),
        sa.Column("timezone_assumption", sa.String(length=64), nullable=False),
        sa.Column("source_authority", sa.String(length=32), nullable=False),
        sa.Column("known_limitations", sa.Text(), nullable=True),
        sa.Column("metadata_role", sa.String(length=64), nullable=False),
        sa.Column("extra", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_market_series_metadata")),
        sa.UniqueConstraint(
            "market_class",
            "provider",
            "symbol",
            "timeframe",
            name="uq_market_series_metadata_key",
        ),
    )
    op.create_index(
        "ix_market_series_metadata_key",
        "market_series_metadata",
        ["market_class", "provider", "symbol", "timeframe"],
    )
    op.create_index(
        "ix_market_series_metadata_market_provider",
        "market_series_metadata",
        ["market_class", "provider"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_market_series_metadata_market_provider",
        table_name="market_series_metadata",
    )
    op.drop_index("ix_market_series_metadata_key", table_name="market_series_metadata")
    op.drop_table("market_series_metadata")
