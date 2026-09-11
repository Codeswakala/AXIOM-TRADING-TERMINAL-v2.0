"""W5-U03 chart research annotations

Revision ID: 20260717_0025
Revises: 20260717_0024
Create Date: 2026-07-17
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260717_0025"
down_revision: Union[str, None] = "20260717_0024"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "chart_research_annotations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("operator_id", sa.String(length=128), nullable=False),
        sa.Column("artifact_type", sa.String(length=96), nullable=False),
        sa.Column("chart_context", sa.JSON(), nullable=False),
        sa.Column("content", sa.JSON(), nullable=False),
        sa.Column("source_artifact_ids", sa.JSON(), nullable=False),
        sa.Column("provenance", sa.JSON(), nullable=False),
        sa.Column("uncertainty", sa.JSON(), nullable=False),
        sa.Column("disclaimer", sa.Text(), nullable=False),
        sa.Column("research_status", sa.String(length=64), nullable=False),
        sa.Column("audit_correlation_id", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_chart_research_annotations_created_at",
        "chart_research_annotations",
        ["created_at"],
    )
    op.create_index(
        "ix_chart_research_annotations_operator",
        "chart_research_annotations",
        ["operator_id"],
    )
    op.create_index(
        "ix_chart_research_annotations_artifact_type",
        "chart_research_annotations",
        ["artifact_type"],
    )
    op.create_index(
        "ix_chart_research_annotations_research_status",
        "chart_research_annotations",
        ["research_status"],
    )
    op.create_index(
        "ix_chart_research_annotations_correlation_id",
        "chart_research_annotations",
        ["audit_correlation_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_chart_research_annotations_correlation_id",
        table_name="chart_research_annotations",
    )
    op.drop_index(
        "ix_chart_research_annotations_research_status",
        table_name="chart_research_annotations",
    )
    op.drop_index(
        "ix_chart_research_annotations_artifact_type",
        table_name="chart_research_annotations",
    )
    op.drop_index(
        "ix_chart_research_annotations_operator",
        table_name="chart_research_annotations",
    )
    op.drop_index(
        "ix_chart_research_annotations_created_at",
        table_name="chart_research_annotations",
    )
    op.drop_table("chart_research_annotations")
