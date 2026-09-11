"""W2-U07 statistical validation reports

Revision ID: 20260714_0011
Revises: 20260714_0010
Create Date: 2026-07-14
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260714_0011"
down_revision: Union[str, None] = "20260714_0010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "validation_reports",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("experiment_id", sa.String(length=96), nullable=False),
        sa.Column("model_artifact_id", sa.String(length=36), nullable=False),
        sa.Column("validation_kind", sa.String(length=64), nullable=False),
        sa.Column("metrics", sa.JSON(), nullable=False),
        sa.Column("uncertainty", sa.JSON(), nullable=False),
        sa.Column("fold_results", sa.JSON(), nullable=False),
        sa.Column("effect_size", sa.JSON(), nullable=False),
        sa.Column("significance", sa.JSON(), nullable=False),
        sa.Column("config", sa.JSON(), nullable=False),
        sa.Column("report_hash", sa.String(length=128), nullable=False),
        sa.Column("research_status", sa.String(length=64), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["model_artifact_id"], ["model_artifacts.id"], ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_validation_reports")),
    )
    op.create_index("ix_validation_reports_experiment_id", "validation_reports", ["experiment_id"])
    op.create_index(
        "ix_validation_reports_model_artifact_id",
        "validation_reports",
        ["model_artifact_id"],
    )
    op.create_index("ix_validation_reports_report_hash", "validation_reports", ["report_hash"])


def downgrade() -> None:
    op.drop_index("ix_validation_reports_report_hash", table_name="validation_reports")
    op.drop_index("ix_validation_reports_model_artifact_id", table_name="validation_reports")
    op.drop_index("ix_validation_reports_experiment_id", table_name="validation_reports")
    op.drop_table("validation_reports")
