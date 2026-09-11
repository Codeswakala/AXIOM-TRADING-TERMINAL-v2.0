"""W2-U10 generalization reports, drift records, model registry links

Revision ID: 20260715_0014
Revises: 20260715_0013
Create Date: 2026-07-15
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260715_0014"
down_revision: Union[str, None] = "20260715_0013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "generalization_reports",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("experiment_id", sa.String(length=96), nullable=False),
        sa.Column("model_artifact_id", sa.String(length=36), nullable=False),
        sa.Column("trained_on", sa.JSON(), nullable=False),
        sa.Column("evaluated_on", sa.JSON(), nullable=False),
        sa.Column("holdout_results", sa.JSON(), nullable=False),
        sa.Column("operating_domain", sa.JSON(), nullable=False),
        sa.Column("unsupported_domain_warnings", sa.JSON(), nullable=False),
        sa.Column("report_hash", sa.String(length=128), nullable=False),
        sa.Column("research_status", sa.String(length=64), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["model_artifact_id"], ["model_artifacts.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_generalization_reports")),
    )
    op.create_index(
        "ix_generalization_reports_experiment_id", "generalization_reports", ["experiment_id"]
    )
    op.create_index(
        "ix_generalization_reports_model_artifact_id",
        "generalization_reports",
        ["model_artifact_id"],
    )
    op.create_index(
        "ix_generalization_reports_report_hash", "generalization_reports", ["report_hash"]
    )

    op.create_table(
        "drift_monitoring_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("model_artifact_id", sa.String(length=36), nullable=False),
        sa.Column("drift_kind", sa.String(length=64), nullable=False),
        sa.Column("window_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("window_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("signals", sa.JSON(), nullable=False),
        sa.Column("drift_detected", sa.Boolean(), nullable=False),
        sa.Column("auto_retrain_requested", sa.Boolean(), nullable=False),
        sa.Column("retrain_triggered", sa.Boolean(), nullable=False),
        sa.Column("governance_required", sa.Boolean(), nullable=False),
        sa.Column("evidence_summary", sa.Text(), nullable=False),
        sa.Column("record_hash", sa.String(length=128), nullable=False),
        sa.Column("research_status", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["model_artifact_id"], ["model_artifacts.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_drift_monitoring_records")),
    )
    op.create_index(
        "ix_drift_records_model_artifact_id", "drift_monitoring_records", ["model_artifact_id"]
    )
    op.create_index("ix_drift_records_drift_kind", "drift_monitoring_records", ["drift_kind"])
    op.create_index("ix_drift_records_record_hash", "drift_monitoring_records", ["record_hash"])

    op.add_column(
        "model_artifacts", sa.Column("statistical_report_id", sa.String(length=36), nullable=True)
    )
    op.add_column(
        "model_artifacts", sa.Column("calibration_report_id", sa.String(length=36), nullable=True)
    )
    op.add_column(
        "model_artifacts", sa.Column("economic_report_id", sa.String(length=36), nullable=True)
    )
    op.add_column("model_artifacts", sa.Column("operating_domain", sa.JSON(), nullable=True))
    op.add_column("model_artifacts", sa.Column("unsupported_domains", sa.JSON(), nullable=True))
    op.add_column("model_artifacts", sa.Column("approval_history", sa.JSON(), nullable=True))
    op.add_column(
        "model_artifacts", sa.Column("rollback_version", sa.String(length=64), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("model_artifacts", "rollback_version")
    op.drop_column("model_artifacts", "approval_history")
    op.drop_column("model_artifacts", "unsupported_domains")
    op.drop_column("model_artifacts", "operating_domain")
    op.drop_column("model_artifacts", "economic_report_id")
    op.drop_column("model_artifacts", "calibration_report_id")
    op.drop_column("model_artifacts", "statistical_report_id")
    op.drop_index("ix_drift_records_record_hash", table_name="drift_monitoring_records")
    op.drop_index("ix_drift_records_drift_kind", table_name="drift_monitoring_records")
    op.drop_index("ix_drift_records_model_artifact_id", table_name="drift_monitoring_records")
    op.drop_table("drift_monitoring_records")
    op.drop_index("ix_generalization_reports_report_hash", table_name="generalization_reports")
    op.drop_index(
        "ix_generalization_reports_model_artifact_id", table_name="generalization_reports"
    )
    op.drop_index("ix_generalization_reports_experiment_id", table_name="generalization_reports")
    op.drop_table("generalization_reports")
