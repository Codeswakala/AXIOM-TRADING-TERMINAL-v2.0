"""W3-U06 monitoring alert records

Revision ID: 20260715_0018
Revises: 20260715_0017
Create Date: 2026-07-15
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260715_0018"
down_revision: Union[str, None] = "20260715_0017"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "monitoring_alerts",
        sa.Column("alert_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("alert_type", sa.String(length=96), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("subject_type", sa.String(length=64), nullable=False),
        sa.Column("subject_id", sa.String(length=128), nullable=False),
        sa.Column("market_class", sa.String(length=64), nullable=True),
        sa.Column("symbol", sa.String(length=128), nullable=True),
        sa.Column("timeframe", sa.String(length=32), nullable=True),
        sa.Column("model_artifact_id", sa.String(length=36), nullable=True),
        sa.Column("signal_id", sa.String(length=36), nullable=True),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column("lineage", sa.JSON(), nullable=False),
        sa.Column("acknowledged", sa.Boolean(), nullable=False),
        sa.Column("acknowledged_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("acknowledged_by", sa.String(length=128), nullable=True),
        sa.Column("audit_correlation_id", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("alert_id"),
    )
    op.create_index("ix_monitoring_alerts_created_at", "monitoring_alerts", ["created_at"])
    op.create_index("ix_monitoring_alerts_type", "monitoring_alerts", ["alert_type"])
    op.create_index("ix_monitoring_alerts_severity", "monitoring_alerts", ["severity"])
    op.create_index(
        "ix_monitoring_alerts_subject", "monitoring_alerts", ["subject_type", "subject_id"]
    )
    op.create_index("ix_monitoring_alerts_acknowledged", "monitoring_alerts", ["acknowledged"])
    op.create_index(
        "ix_monitoring_alerts_correlation", "monitoring_alerts", ["audit_correlation_id"]
    )


def downgrade() -> None:
    op.drop_index("ix_monitoring_alerts_correlation", table_name="monitoring_alerts")
    op.drop_index("ix_monitoring_alerts_acknowledged", table_name="monitoring_alerts")
    op.drop_index("ix_monitoring_alerts_subject", table_name="monitoring_alerts")
    op.drop_index("ix_monitoring_alerts_severity", table_name="monitoring_alerts")
    op.drop_index("ix_monitoring_alerts_type", table_name="monitoring_alerts")
    op.drop_index("ix_monitoring_alerts_created_at", table_name="monitoring_alerts")
    op.drop_table("monitoring_alerts")
