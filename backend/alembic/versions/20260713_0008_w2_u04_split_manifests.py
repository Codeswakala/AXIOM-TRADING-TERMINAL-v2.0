"""W2-U04 dataset split manifests

Revision ID: 20260713_0008
Revises: 20260713_0007
Create Date: 2026-07-13
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260713_0008"
down_revision: Union[str, None] = "20260713_0007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "dataset_split_manifests",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("dataset_snapshot_id", sa.String(length=36), nullable=False),
        sa.Column("split_id", sa.String(length=96), nullable=False),
        sa.Column("split_strategy", sa.String(length=32), nullable=False),
        sa.Column("label_horizon_bars", sa.Integer(), nullable=False),
        sa.Column("embargo_bars", sa.Integer(), nullable=False),
        sa.Column("train_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("train_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("validation_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("validation_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("test_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("test_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("train_count", sa.Integer(), nullable=False),
        sa.Column("validation_count", sa.Integer(), nullable=False),
        sa.Column("test_count", sa.Integer(), nullable=False),
        sa.Column("split_hash", sa.String(length=128), nullable=False),
        sa.Column("manifest", sa.JSON(), nullable=False),
        sa.Column("quality_summary", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["dataset_snapshot_id"], ["dataset_snapshots.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_dataset_split_manifests")),
        sa.UniqueConstraint(
            "dataset_snapshot_id",
            "split_id",
            name="uq_dataset_split_snapshot_split_id",
        ),
    )
    op.create_index(
        "ix_dataset_split_snapshot",
        "dataset_split_manifests",
        ["dataset_snapshot_id"],
    )
    op.create_index("ix_dataset_split_hash", "dataset_split_manifests", ["split_hash"])


def downgrade() -> None:
    op.drop_index("ix_dataset_split_hash", table_name="dataset_split_manifests")
    op.drop_index("ix_dataset_split_snapshot", table_name="dataset_split_manifests")
    op.drop_table("dataset_split_manifests")
