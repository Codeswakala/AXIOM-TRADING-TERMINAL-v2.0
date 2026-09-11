"""W2-U01 dataset snapshots and chronology quarantine tables

Revision ID: 20260713_0005
Revises: 20260711_0004
Create Date: 2026-07-13
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260713_0005"
down_revision: Union[str, None] = "20260711_0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "dataset_snapshots",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("dataset_id", sa.String(length=96), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("market", sa.String(length=64), nullable=False),
        sa.Column("timeframe", sa.String(length=32), nullable=False),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source", sa.String(length=128), nullable=False),
        sa.Column("feature_version", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("quality_score", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("content_hash", sa.String(length=128), nullable=True),
        sa.Column("market_scope", sa.JSON(), nullable=True),
        sa.Column("source_policy", sa.JSON(), nullable=True),
        sa.Column("frozen_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", sa.String(length=128), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_dataset_snapshots")),
        sa.UniqueConstraint("dataset_id", "version", name="uq_dataset_snapshots_dataset_version"),
    )
    op.create_index("ix_dataset_snapshots_dataset_id", "dataset_snapshots", ["dataset_id"])
    op.create_index("ix_dataset_snapshots_status", "dataset_snapshots", ["status"])

    op.create_table(
        "dataset_series_members",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("dataset_snapshot_id", sa.String(length=36), nullable=False),
        sa.Column("market_class", sa.String(length=32), nullable=False),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("symbol", sa.String(length=64), nullable=False),
        sa.Column("timeframe", sa.String(length=16), nullable=False),
        sa.Column("source", sa.String(length=64), nullable=False),
        sa.Column("authoritative", sa.Boolean(), nullable=False),
        sa.Column("record_count", sa.Integer(), nullable=False),
        sa.Column("first_open_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_open_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("series_hash", sa.String(length=128), nullable=False),
        sa.ForeignKeyConstraint(
            ["dataset_snapshot_id"], ["dataset_snapshots.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_dataset_series_members")),
    )
    op.create_index("ix_dataset_series_snapshot", "dataset_series_members", ["dataset_snapshot_id"])
    op.create_index(
        "ix_dataset_series_key",
        "dataset_series_members",
        ["market_class", "provider", "symbol", "timeframe"],
    )

    op.create_table(
        "dataset_lineage_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("dataset_snapshot_id", sa.String(length=36), nullable=False),
        sa.Column("source_candle_id", sa.String(length=36), nullable=False),
        sa.Column("normalized_record_hash", sa.String(length=128), nullable=False),
        sa.Column("feature_record_id", sa.String(length=36), nullable=True),
        sa.Column("lineage_stage", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["dataset_snapshot_id"], ["dataset_snapshots.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_dataset_lineage_records")),
    )
    op.create_index(
        "ix_dataset_lineage_snapshot",
        "dataset_lineage_records",
        ["dataset_snapshot_id"],
    )
    op.create_index(
        "ix_dataset_lineage_source",
        "dataset_lineage_records",
        ["source_candle_id"],
    )

    op.create_table(
        "dataset_quarantine_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("dataset_snapshot_id", sa.String(length=36), nullable=True),
        sa.Column("source_record_id", sa.String(length=64), nullable=True),
        sa.Column("market_class", sa.String(length=32), nullable=False),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("symbol", sa.String(length=64), nullable=False),
        sa.Column("timeframe", sa.String(length=16), nullable=False),
        sa.Column("open_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("source", sa.String(length=64), nullable=False),
        sa.Column("reason_code", sa.String(length=64), nullable=False),
        sa.Column("detected_stage", sa.String(length=64), nullable=False),
        sa.Column("detail", sa.Text(), nullable=False),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["dataset_snapshot_id"], ["dataset_snapshots.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_dataset_quarantine_records")),
    )
    op.create_index("ix_dataset_quarantine_reason", "dataset_quarantine_records", ["reason_code"])
    op.create_index(
        "ix_dataset_quarantine_series",
        "dataset_quarantine_records",
        ["market_class", "provider", "symbol", "timeframe"],
    )


def downgrade() -> None:
    op.drop_index("ix_dataset_quarantine_series", table_name="dataset_quarantine_records")
    op.drop_index("ix_dataset_quarantine_reason", table_name="dataset_quarantine_records")
    op.drop_table("dataset_quarantine_records")
    op.drop_index("ix_dataset_lineage_source", table_name="dataset_lineage_records")
    op.drop_index("ix_dataset_lineage_snapshot", table_name="dataset_lineage_records")
    op.drop_table("dataset_lineage_records")
    op.drop_index("ix_dataset_series_key", table_name="dataset_series_members")
    op.drop_index("ix_dataset_series_snapshot", table_name="dataset_series_members")
    op.drop_table("dataset_series_members")
    op.drop_index("ix_dataset_snapshots_status", table_name="dataset_snapshots")
    op.drop_index("ix_dataset_snapshots_dataset_id", table_name="dataset_snapshots")
    op.drop_table("dataset_snapshots")
