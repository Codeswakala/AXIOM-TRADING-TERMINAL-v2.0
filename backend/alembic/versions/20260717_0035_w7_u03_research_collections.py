"""W7-U03 research collections

Revision ID: 20260717_0035
Revises: 20260717_0034
Create Date: 2026-07-18
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260717_0035"
down_revision: Union[str, None] = "20260717_0034"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "research_collections",
        sa.Column("collection_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("operator_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("research_status", sa.String(length=64), nullable=False),
        sa.Column("audit_correlation_id", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["operator_id"], ["operators.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("collection_id"),
        sa.UniqueConstraint(
            "operator_id",
            "name",
            name="uq_research_collections_operator_name",
        ),
    )
    op.create_index(
        "ix_research_collections_operator",
        "research_collections",
        ["operator_id"],
    )
    op.create_index(
        "ix_research_collections_correlation_id",
        "research_collections",
        ["audit_correlation_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_research_collections_correlation_id", table_name="research_collections")
    op.drop_index("ix_research_collections_operator", table_name="research_collections")
    op.drop_table("research_collections")
