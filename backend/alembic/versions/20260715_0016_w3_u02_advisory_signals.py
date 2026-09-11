"""W3-U02 advisory signal contract and persistence

Revision ID: 20260715_0016
Revises: 20260715_0015
Create Date: 2026-07-15
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260715_0016"
down_revision: Union[str, None] = "20260715_0015"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "advisory_signals",
        sa.Column("signal_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("as_of_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("market_class", sa.String(length=64), nullable=False),
        sa.Column("provider", sa.String(length=128), nullable=False),
        sa.Column("symbol", sa.String(length=128), nullable=False),
        sa.Column("timeframe", sa.String(length=32), nullable=False),
        sa.Column("model_artifact_id", sa.String(length=36), nullable=False),
        sa.Column("model_version", sa.String(length=64), nullable=False),
        sa.Column("feature_set_version", sa.String(length=64), nullable=False),
        sa.Column("experiment_id", sa.String(length=96), nullable=False),
        sa.Column("statistical_report_id", sa.String(length=36), nullable=True),
        sa.Column("calibration_report_id", sa.String(length=36), nullable=True),
        sa.Column("economic_report_id", sa.String(length=36), nullable=True),
        sa.Column("generalization_report_id", sa.String(length=36), nullable=True),
        sa.Column("inference_input_hash", sa.String(length=128), nullable=False),
        sa.Column("raw_score", sa.Float(), nullable=True),
        sa.Column("calibrated_confidence", sa.Float(), nullable=True),
        sa.Column("signal_direction", sa.String(length=64), nullable=False),
        sa.Column("signal_state", sa.String(length=32), nullable=False),
        sa.Column("state_reason", sa.String(length=256), nullable=False),
        sa.Column("eligibility_reasons", sa.JSON(), nullable=False),
        sa.Column("operating_domain_status", sa.String(length=64), nullable=False),
        sa.Column("calibration_status", sa.String(length=128), nullable=False),
        sa.Column("economic_verdict", sa.String(length=128), nullable=False),
        sa.Column("risk_notes", sa.Text(), nullable=True),
        sa.Column("rationale", sa.Text(), nullable=False),
        sa.Column("explainability_summary", sa.JSON(), nullable=False),
        sa.Column("state_transition_history", sa.JSON(), nullable=False),
        sa.Column("audit_correlation_id", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(
            ["calibration_report_id"], ["calibration_reports.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["economic_report_id"], ["economic_reports.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["generalization_report_id"], ["generalization_reports.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(["model_artifact_id"], ["model_artifacts.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(
            ["statistical_report_id"], ["validation_reports.id"], ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("signal_id"),
    )
    op.create_index("ix_advisory_signals_created_at", "advisory_signals", ["created_at"])
    op.create_index("ix_advisory_signals_state", "advisory_signals", ["signal_state"])
    op.create_index(
        "ix_advisory_signals_model_artifact", "advisory_signals", ["model_artifact_id"]
    )
    op.create_index(
        "ix_advisory_signals_market_symbol",
        "advisory_signals",
        ["market_class", "symbol", "timeframe"],
    )
    op.create_index(
        "ix_advisory_signals_correlation", "advisory_signals", ["audit_correlation_id"]
    )


def downgrade() -> None:
    op.drop_index("ix_advisory_signals_correlation", table_name="advisory_signals")
    op.drop_index("ix_advisory_signals_market_symbol", table_name="advisory_signals")
    op.drop_index("ix_advisory_signals_model_artifact", table_name="advisory_signals")
    op.drop_index("ix_advisory_signals_state", table_name="advisory_signals")
    op.drop_index("ix_advisory_signals_created_at", table_name="advisory_signals")
    op.drop_table("advisory_signals")
