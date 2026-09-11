"""W2-U03 feature definitions and feature store metadata

Revision ID: 20260713_0007
Revises: 20260713_0006
Create Date: 2026-07-13
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260713_0007"
down_revision: Union[str, None] = "20260713_0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "feature_definitions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("feature_name", sa.String(length=128), nullable=False),
        sa.Column("feature_version", sa.String(length=64), nullable=False),
        sa.Column("formula_spec", sa.JSON(), nullable=False),
        sa.Column("input_requirements", sa.JSON(), nullable=False),
        sa.Column("lookback_window", sa.Integer(), nullable=False),
        sa.Column("causal", sa.Boolean(), nullable=False),
        sa.Column("market_compatibility_notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_feature_definitions")),
        sa.UniqueConstraint(
            "feature_name",
            "feature_version",
            name="uq_feature_definition_name_version",
        ),
    )
    op.create_index("ix_feature_definitions_name", "feature_definitions", ["feature_name"])

    op.create_table(
        "feature_quality_reports",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("feature_set_version", sa.String(length=64), nullable=False),
        sa.Column("source_dataset_hash", sa.String(length=128), nullable=False),
        sa.Column("missing_rate", sa.Float(), nullable=False),
        sa.Column("drift_summary", sa.JSON(), nullable=False),
        sa.Column("leakage_checks", sa.JSON(), nullable=False),
        sa.Column("stationarity_notes", sa.Text(), nullable=True),
        sa.Column("cross_market_compatibility", sa.Text(), nullable=True),
        sa.Column("content_hash", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_feature_quality_reports")),
    )
    op.create_index(
        "ix_feature_quality_reports_version",
        "feature_quality_reports",
        ["feature_set_version"],
    )
    op.create_index(
        "ix_feature_quality_reports_hash",
        "feature_quality_reports",
        ["content_hash"],
    )

    op.add_column(
        "feature_records",
        sa.Column("provider", sa.String(length=64), nullable=False, server_default="internal"),
    )
    op.add_column(
        "feature_records",
        sa.Column("source_dataset_hash", sa.String(length=128), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("feature_records", "source_dataset_hash")
    op.drop_column("feature_records", "provider")
    op.drop_index("ix_feature_quality_reports_hash", table_name="feature_quality_reports")
    op.drop_index("ix_feature_quality_reports_version", table_name="feature_quality_reports")
    op.drop_table("feature_quality_reports")
    op.drop_index("ix_feature_definitions_name", table_name="feature_definitions")
    op.drop_table("feature_definitions")
