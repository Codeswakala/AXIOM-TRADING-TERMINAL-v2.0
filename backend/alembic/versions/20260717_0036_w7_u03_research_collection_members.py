"""W7-U03 research collection members

Revision ID: 20260717_0036
Revises: 20260717_0035
Create Date: 2026-07-18
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260717_0036"
down_revision: Union[str, None] = "20260717_0035"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "research_collection_members",
        sa.Column("member_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("operator_id", sa.String(length=36), nullable=False),
        sa.Column("collection_id", sa.String(length=36), nullable=False),
        sa.Column("artifact_type", sa.String(length=96), nullable=False),
        sa.Column("artifact_id", sa.String(length=96), nullable=False),
        sa.Column("audit_correlation_id", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["operator_id"], ["operators.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(
            ["collection_id"],
            ["research_collections.collection_id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("member_id"),
        sa.UniqueConstraint(
            "collection_id",
            "artifact_type",
            "artifact_id",
            name="uq_research_collection_members_collection_artifact",
        ),
    )
    op.create_index(
        "ix_research_collection_members_operator",
        "research_collection_members",
        ["operator_id"],
    )
    op.create_index(
        "ix_research_collection_members_collection",
        "research_collection_members",
        ["collection_id"],
    )
    op.create_index(
        "ix_research_collection_members_artifact",
        "research_collection_members",
        ["artifact_type", "artifact_id"],
    )
    op.create_index(
        "ix_research_collection_members_correlation_id",
        "research_collection_members",
        ["audit_correlation_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_research_collection_members_correlation_id",
        table_name="research_collection_members",
    )
    op.drop_index(
        "ix_research_collection_members_artifact",
        table_name="research_collection_members",
    )
    op.drop_index(
        "ix_research_collection_members_collection",
        table_name="research_collection_members",
    )
    op.drop_index(
        "ix_research_collection_members_operator",
        table_name="research_collection_members",
    )
    op.drop_table("research_collection_members")
