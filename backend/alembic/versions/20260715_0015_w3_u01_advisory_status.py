"""W3-U01 advisory status fields

Revision ID: 20260715_0015
Revises: 20260715_0014
Create Date: 2026-07-15
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260715_0015"
down_revision: Union[str, None] = "20260715_0014"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "model_artifacts", sa.Column("advisory_status", sa.String(length=64), nullable=True)
    )
    op.add_column(
        "model_artifacts",
        sa.Column("advisory_approved_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "model_artifacts",
        sa.Column("advisory_approved_by", sa.String(length=128), nullable=True),
    )
    op.create_index("ix_model_artifacts_advisory_status", "model_artifacts", ["advisory_status"])


def downgrade() -> None:
    op.drop_index("ix_model_artifacts_advisory_status", table_name="model_artifacts")
    op.drop_column("model_artifacts", "advisory_approved_by")
    op.drop_column("model_artifacts", "advisory_approved_at")
    op.drop_column("model_artifacts", "advisory_status")
