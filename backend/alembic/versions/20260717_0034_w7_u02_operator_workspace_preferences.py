"""W7-U02 operator workspace preferences

Revision ID: 20260717_0034
Revises: 20260717_0033
Create Date: 2026-07-18
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260717_0034"
down_revision: Union[str, None] = "20260717_0033"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "operator_workspace_preferences",
        sa.Column("preference_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("operator_id", sa.String(length=36), nullable=False),
        sa.Column("workspace_key", sa.String(length=96), nullable=False),
        sa.Column("layout_config", sa.JSON(), nullable=False),
        sa.Column("visible_modules", sa.JSON(), nullable=False),
        sa.Column("theme_config", sa.JSON(), nullable=False),
        sa.Column("research_status", sa.String(length=64), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("audit_correlation_id", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["operator_id"], ["operators.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("preference_id"),
        sa.UniqueConstraint(
            "operator_id",
            "workspace_key",
            name="uq_operator_workspace_preferences_operator_workspace",
        ),
    )
    op.create_index(
        "ix_operator_workspace_preferences_operator",
        "operator_workspace_preferences",
        ["operator_id"],
    )
    op.create_index(
        "ix_operator_workspace_preferences_workspace_key",
        "operator_workspace_preferences",
        ["workspace_key"],
    )
    op.create_index(
        "ix_operator_workspace_preferences_correlation_id",
        "operator_workspace_preferences",
        ["audit_correlation_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_operator_workspace_preferences_correlation_id",
        table_name="operator_workspace_preferences",
    )
    op.drop_index(
        "ix_operator_workspace_preferences_workspace_key",
        table_name="operator_workspace_preferences",
    )
    op.drop_index(
        "ix_operator_workspace_preferences_operator",
        table_name="operator_workspace_preferences",
    )
    op.drop_table("operator_workspace_preferences")
