"""W7-U03 research tags

Revision ID: 20260717_0037
Revises: 20260717_0036
Create Date: 2026-07-18
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260717_0037"
down_revision: Union[str, None] = "20260717_0036"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "research_tags",
        sa.Column("tag_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("operator_id", sa.String(length=36), nullable=False),
        sa.Column("artifact_type", sa.String(length=96), nullable=False),
        sa.Column("artifact_id", sa.String(length=96), nullable=False),
        sa.Column("tag", sa.String(length=96), nullable=False),
        sa.Column("audit_correlation_id", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["operator_id"], ["operators.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("tag_id"),
        sa.UniqueConstraint(
            "operator_id",
            "artifact_type",
            "artifact_id",
            "tag",
            name="uq_research_tags_operator_artifact_tag",
        ),
    )
    op.create_index("ix_research_tags_operator", "research_tags", ["operator_id"])
    op.create_index(
        "ix_research_tags_artifact",
        "research_tags",
        ["artifact_type", "artifact_id"],
    )
    op.create_index("ix_research_tags_tag", "research_tags", ["tag"])
    op.create_index(
        "ix_research_tags_correlation_id",
        "research_tags",
        ["audit_correlation_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_research_tags_correlation_id", table_name="research_tags")
    op.drop_index("ix_research_tags_tag", table_name="research_tags")
    op.drop_index("ix_research_tags_artifact", table_name="research_tags")
    op.drop_index("ix_research_tags_operator", table_name="research_tags")
    op.drop_table("research_tags")
