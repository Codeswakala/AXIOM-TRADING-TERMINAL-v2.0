"""W6-U02 simulated fill events

Revision ID: 20260717_0029
Revises: 20260717_0028
Create Date: 2026-07-17
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260717_0029"
down_revision: Union[str, None] = "20260717_0028"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "simulated_fill_events",
        sa.Column("simulated_fill_id", sa.String(length=36), nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("simulation_mode", sa.String(length=32), nullable=False),
        sa.Column("market_class", sa.String(length=64), nullable=False),
        sa.Column("symbol", sa.String(length=128), nullable=False),
        sa.Column("timeframe", sa.String(length=32), nullable=False),
        sa.Column("as_of_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("simulated_research_direction", sa.String(length=32), nullable=False),
        sa.Column("simulated_units", sa.Float(), nullable=False),
        sa.Column("requested_reference_price", sa.Float(), nullable=False),
        sa.Column("simulated_fill_price", sa.Float(), nullable=False),
        sa.Column("simulated_slippage_bps", sa.Float(), nullable=False),
        sa.Column("source_candle_ids", sa.JSON(), nullable=False),
        sa.Column("fill_model_name", sa.String(length=96), nullable=False),
        sa.Column("fill_model_version", sa.String(length=96), nullable=False),
        sa.Column("research_status", sa.String(length=64), nullable=False),
        sa.Column("simulation_disclaimer", sa.Text(), nullable=False),
        sa.Column("audit_correlation_id", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(
            ["run_id"], ["simulated_execution_runs.run_id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("simulated_fill_id"),
    )
    op.create_index("ix_simulated_fill_events_created_at", "simulated_fill_events", ["created_at"])
    op.create_index("ix_simulated_fill_events_run", "simulated_fill_events", ["run_id"])
    op.create_index(
        "ix_simulated_fill_events_series",
        "simulated_fill_events",
        ["market_class", "symbol", "timeframe"],
    )
    op.create_index("ix_simulated_fill_events_as_of", "simulated_fill_events", ["as_of_time"])
    op.create_index(
        "ix_simulated_fill_events_fill_model",
        "simulated_fill_events",
        ["fill_model_name", "fill_model_version"],
    )
    op.create_index(
        "ix_simulated_fill_events_correlation_id",
        "simulated_fill_events",
        ["audit_correlation_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_simulated_fill_events_correlation_id", table_name="simulated_fill_events")
    op.drop_index("ix_simulated_fill_events_fill_model", table_name="simulated_fill_events")
    op.drop_index("ix_simulated_fill_events_as_of", table_name="simulated_fill_events")
    op.drop_index("ix_simulated_fill_events_series", table_name="simulated_fill_events")
    op.drop_index("ix_simulated_fill_events_run", table_name="simulated_fill_events")
    op.drop_index("ix_simulated_fill_events_created_at", table_name="simulated_fill_events")
    op.drop_table("simulated_fill_events")
