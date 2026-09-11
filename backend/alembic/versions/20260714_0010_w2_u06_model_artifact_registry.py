"""W2-U06 model artifact registry fields

Revision ID: 20260714_0010
Revises: 20260713_0009
Create Date: 2026-07-14
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260714_0010"
down_revision: Union[str, None] = "20260713_0009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "model_artifacts",
        sa.Column("experiment_id", sa.String(length=96), nullable=True),
    )
    op.add_column(
        "model_artifacts",
        sa.Column("dataset_snapshot_id", sa.String(length=36), nullable=True),
    )
    op.add_column(
        "model_artifacts",
        sa.Column("dataset_content_hash", sa.String(length=128), nullable=True),
    )
    op.add_column(
        "model_artifacts",
        sa.Column("split_manifest_hash", sa.String(length=128), nullable=True),
    )
    op.add_column("model_artifacts", sa.Column("hyperparameters", sa.JSON(), nullable=True))
    op.add_column(
        "model_artifacts",
        sa.Column("artifact_hash", sa.String(length=128), nullable=True),
    )
    op.add_column(
        "model_artifacts",
        sa.Column("research_status", sa.String(length=64), nullable=True),
    )
    op.create_index("ix_model_artifacts_experiment_id", "model_artifacts", ["experiment_id"])
    op.create_index("ix_model_artifacts_artifact_hash", "model_artifacts", ["artifact_hash"])


def downgrade() -> None:
    op.drop_index("ix_model_artifacts_artifact_hash", table_name="model_artifacts")
    op.drop_index("ix_model_artifacts_experiment_id", table_name="model_artifacts")
    op.drop_column("model_artifacts", "research_status")
    op.drop_column("model_artifacts", "artifact_hash")
    op.drop_column("model_artifacts", "hyperparameters")
    op.drop_column("model_artifacts", "split_manifest_hash")
    op.drop_column("model_artifacts", "dataset_content_hash")
    op.drop_column("model_artifacts", "dataset_snapshot_id")
    op.drop_column("model_artifacts", "experiment_id")
