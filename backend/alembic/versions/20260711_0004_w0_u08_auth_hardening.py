"""W0-U08 refresh tokens + ws tickets

Revision ID: 20260711_0004
Revises: 20260710_0003
Create Date: 2026-07-11
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260711_0004"
down_revision: Union[str, None] = "20260710_0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("jti", sa.String(length=64), nullable=False),
        sa.Column("operator_id", sa.String(length=36), nullable=False),
        sa.Column("token_hash", sa.String(length=128), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked", sa.Boolean(), nullable=False),
        sa.Column("replaced_by_jti", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["operator_id"],
            ["operators.id"],
            name=op.f("fk_refresh_tokens_operator_id_operators"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_refresh_tokens")),
        sa.UniqueConstraint("jti", name="uq_refresh_tokens_jti"),
    )
    op.create_index("ix_refresh_tokens_jti", "refresh_tokens", ["jti"], unique=False)
    op.create_index(
        "ix_refresh_tokens_operator_id",
        "refresh_tokens",
        ["operator_id"],
        unique=False,
    )

    op.create_table(
        "ws_tickets",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("ticket", sa.String(length=64), nullable=False),
        sa.Column("operator_id", sa.String(length=36), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["operator_id"],
            ["operators.id"],
            name=op.f("fk_ws_tickets_operator_id_operators"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_ws_tickets")),
        sa.UniqueConstraint("ticket", name="uq_ws_tickets_ticket"),
    )
    op.create_index("ix_ws_tickets_ticket", "ws_tickets", ["ticket"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_ws_tickets_ticket", table_name="ws_tickets")
    op.drop_table("ws_tickets")
    op.drop_index("ix_refresh_tokens_operator_id", table_name="refresh_tokens")
    op.drop_index("ix_refresh_tokens_jti", table_name="refresh_tokens")
    op.drop_table("refresh_tokens")
