"""W2-U08 calibration reports

Revision ID: 20260714_0012
Revises: 20260714_0011
Create Date: 2026-07-14
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260714_0012"
down_revision: Union[str, None] = "20260714_0011"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "calibration_reports",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("experiment_id", sa.String(length=96), nullable=False),
        sa.Column("model_artifact_id", sa.String(length=36), nullable=False),
        sa.Column("validation_report_id", sa.String(length=36), nullable=False),
        sa.Column("brier_score", sa.String(length=64), nullable=False),
        sa.Column("expected_calibration_error", sa.String(length=64), nullable=False),
        sa.Column("bin_scheme", sa.JSON(), nullable=False),
        sa.Column("bins", sa.JSON(), nullable=False),
        sa.Column("per_slice", sa.JSON(), nullable=False),
        sa.Column("warnings", sa.JSON(), nullable=False),
        sa.Column("base_rate", sa.String(length=64), nullable=False),
        sa.Column("base_rate_significance", sa.JSON(), nullable=False),
        sa.Column("config", sa.JSON(), nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_calibration_reports")),
    )
    op.create_index(
        "ix_calibration_reports_experiment_id",
        "calibration_reports",
        ["experiment_id"],
    )
    op.create_index(
        "ix_calibration_reports_model_artifact_id",
        "calibration_reports",
        ["model_artifact_id"],
    )
    op.create_index(
        "ix_calibration_reports_validation_report_id",
        "calibration_reports",
        ["validation_report_id"],
    )
    op.create_index("ix_calibration_reports_report_hash", "calibration_reports", ["report_hash"])


def downgrade() -> None:
    op.drop_index("ix_calibration_reports_report_hash", table_name="calibration_reports")
    op.drop_index("ix_calibration_reports_validation_report_id", table_name="calibration_reports")
    op.drop_index("ix_calibration_reports_model_artifact_id", table_name="calibration_reports")
    op.drop_index("ix_calibration_reports_experiment_id", table_name="calibration_reports")
    op.drop_table("calibration_reports")
