"""W0-U02 core persistence foundation tables

Revision ID: 20260710_0001
Revises:
Create Date: 2026-07-10

"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260710_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "candles",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("market_class", sa.String(length=32), nullable=False),
        sa.Column("symbol", sa.String(length=64), nullable=False),
        sa.Column("timeframe", sa.String(length=16), nullable=False),
        sa.Column("open_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("open", sa.Numeric(precision=24, scale=10), nullable=False),
        sa.Column("high", sa.Numeric(precision=24, scale=10), nullable=False),
        sa.Column("low", sa.Numeric(precision=24, scale=10), nullable=False),
        sa.Column("close", sa.Numeric(precision=24, scale=10), nullable=False),
        sa.Column("volume", sa.Numeric(precision=24, scale=10), nullable=True),
        sa.Column("source", sa.String(length=64), nullable=True),
        sa.Column("extra", sa.JSON(), nullable=True),
        sa.Column("ingested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_candles")),
        sa.UniqueConstraint(
            "market_class",
            "symbol",
            "timeframe",
            "open_time",
            name="uq_candles_market_symbol_tf_time",
        ),
    )
    op.create_index(
        "ix_candles_market_class_symbol",
        "candles",
        ["market_class", "symbol"],
        unique=False,
    )
    op.create_index(
        "ix_candles_symbol_timeframe_open_time",
        "candles",
        ["symbol", "timeframe", "open_time"],
        unique=False,
    )

    op.create_table(
        "feature_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("feature_set_version", sa.String(length=64), nullable=False),
        sa.Column("market_class", sa.String(length=32), nullable=False),
        sa.Column("symbol", sa.String(length=64), nullable=False),
        sa.Column("timeframe", sa.String(length=16), nullable=False),
        sa.Column("as_of", sa.DateTime(timezone=True), nullable=False),
        sa.Column("features", sa.JSON(), nullable=False),
        sa.Column("quality_score", sa.String(length=32), nullable=True),
        sa.Column("source", sa.String(length=64), nullable=True),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_feature_records")),
        sa.UniqueConstraint(
            "feature_set_version",
            "market_class",
            "symbol",
            "timeframe",
            "as_of",
            name="uq_feature_records_version_context_asof",
        ),
    )
    op.create_index(
        "ix_feature_records_symbol_as_of",
        "feature_records",
        ["symbol", "as_of"],
        unique=False,
    )

    op.create_table(
        "model_artifacts",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("version", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("framework", sa.String(length=64), nullable=True),
        sa.Column("feature_set_version", sa.String(length=64), nullable=True),
        sa.Column("supported_markets", sa.JSON(), nullable=True),
        sa.Column("metrics", sa.JSON(), nullable=True),
        sa.Column("artifact_uri", sa.String(length=512), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("registered_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_model_artifacts")),
    )
    op.create_index(
        "ix_model_artifacts_name_version",
        "model_artifacts",
        ["name", "version"],
        unique=False,
    )
    op.create_index("ix_model_artifacts_status", "model_artifacts", ["status"], unique=False)

    op.create_table(
        "audit_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("action", sa.String(length=128), nullable=False),
        sa.Column("actor", sa.String(length=128), nullable=False),
        sa.Column("resource_type", sa.String(length=64), nullable=True),
        sa.Column("resource_id", sa.String(length=64), nullable=True),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("details", sa.JSON(), nullable=True),
        sa.Column("correlation_id", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_audit_events")),
    )
    op.create_index("ix_audit_events_actor", "audit_events", ["actor"], unique=False)
    op.create_index(
        "ix_audit_events_category_created",
        "audit_events",
        ["category", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_audit_events_category_created", table_name="audit_events")
    op.drop_index("ix_audit_events_actor", table_name="audit_events")
    op.drop_table("audit_events")
    op.drop_index("ix_model_artifacts_status", table_name="model_artifacts")
    op.drop_index("ix_model_artifacts_name_version", table_name="model_artifacts")
    op.drop_table("model_artifacts")
    op.drop_index("ix_feature_records_symbol_as_of", table_name="feature_records")
    op.drop_table("feature_records")
    op.drop_index("ix_candles_symbol_timeframe_open_time", table_name="candles")
    op.drop_index("ix_candles_market_class_symbol", table_name="candles")
    op.drop_table("candles")
