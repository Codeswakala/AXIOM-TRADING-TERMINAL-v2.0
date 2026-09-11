"""W2-U05 experiment registry

Revision ID: 20260713_0009
Revises: 20260713_0008
Create Date: 2026-07-13
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260713_0009"
down_revision: Union[str, None] = "20260713_0008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "experiments",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("experiment_id", sa.String(length=96), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("purpose", sa.Text(), nullable=False),
        sa.Column("hypothesis", sa.Text(), nullable=False),
        sa.Column("dataset_snapshot_id", sa.String(length=36), nullable=False),
        sa.Column("dataset_content_hash", sa.String(length=128), nullable=False),
        sa.Column("split_manifest_id", sa.String(length=36), nullable=False),
        sa.Column("split_manifest_hash", sa.String(length=128), nullable=False),
        sa.Column("feature_set_version", sa.String(length=64), nullable=False),
        sa.Column("model_family", sa.String(length=128), nullable=False),
        sa.Column("model_spec", sa.JSON(), nullable=False),
        sa.Column("evaluation_plan", sa.JSON(), nullable=False),
        sa.Column("approval_timestamp", sa.DateTime(timezone=True), nullable=True),
        sa.Column("approver", sa.String(length=128), nullable=True),
        sa.Column("plan_hash", sa.String(length=128), nullable=False),
        sa.Column("previous_experiment_id", sa.String(length=36), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["dataset_snapshot_id"], ["dataset_snapshots.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["split_manifest_id"], ["dataset_split_manifests.id"], ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_experiments")),
        sa.UniqueConstraint("experiment_id", "version", name="uq_experiments_experiment_version"),
    )
    op.create_index("ix_experiments_status", "experiments", ["status"])
    op.create_index("ix_experiments_experiment_id", "experiments", ["experiment_id"])
    op.create_index("ix_experiments_plan_hash", "experiments", ["plan_hash"])


def downgrade() -> None:
    op.drop_index("ix_experiments_plan_hash", table_name="experiments")
    op.drop_index("ix_experiments_experiment_id", table_name="experiments")
    op.drop_index("ix_experiments_status", table_name="experiments")
    op.drop_table("experiments")
