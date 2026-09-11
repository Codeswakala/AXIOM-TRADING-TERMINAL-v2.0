"""W2-U09 economic validation reports

Revision ID: 20260715_0013
Revises: 20260714_0012
Create Date: 2026-07-15
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260715_0013"
down_revision: Union[str, None] = "20260714_0012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "economic_reports",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("experiment_id", sa.String(length=96), nullable=False),
        sa.Column("model_artifact_id", sa.String(length=36), nullable=False),
        sa.Column("validation_report_id", sa.String(length=36), nullable=True),
        sa.Column("calibration_report_id", sa.String(length=36), nullable=True),
        sa.Column("cost_model", sa.JSON(), nullable=False),
        sa.Column("scenario_results", sa.JSON(), nullable=False),
        sa.Column("statistical_conclusion", sa.JSON(), nullable=False),
        sa.Column("economic_conclusion", sa.JSON(), nullable=False),
        sa.Column("sensitivity_summary", sa.JSON(), nullable=False),
        sa.Column("per_slice", sa.JSON(), nullable=False),
        sa.Column("report_hash", sa.String(length=128), nullable=False),
        sa.Column("research_status", sa.String(length=64), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["model_artifact_id"], ["model_artifacts.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["validation_report_id"], ["validation_reports.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["calibration_report_id"], ["calibration_reports.id"], ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_economic_reports")),
    )
    op.create_index("ix_economic_reports_experiment_id", "economic_reports", ["experiment_id"])
    op.create_index(
        "ix_economic_reports_model_artifact_id",
        "economic_reports",
        ["model_artifact_id"],
    )
    op.create_index("ix_economic_reports_report_hash", "economic_reports", ["report_hash"])


def downgrade() -> None:
    op.drop_index("ix_economic_reports_report_hash", table_name="economic_reports")
    op.drop_index("ix_economic_reports_model_artifact_id", table_name="economic_reports")
    op.drop_index("ix_economic_reports_experiment_id", table_name="economic_reports")
    op.drop_table("economic_reports")
