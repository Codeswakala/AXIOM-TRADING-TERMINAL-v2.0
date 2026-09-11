"""W5-U02 assistant research responses

Revision ID: 20260717_0024
Revises: 20260716_0023
Create Date: 2026-07-17
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "20260717_0024"
down_revision: Union[str, None] = "20260716_0023"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "assistant_research_responses",
        sa.Column("assistant_response_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("operator_id", sa.String(length=128), nullable=False),
        sa.Column("request_id", sa.String(length=36), nullable=False),
        sa.Column("request_text_hash", sa.String(length=64), nullable=False),
        sa.Column("assistant_policy_version", sa.String(length=96), nullable=False),
        sa.Column("provider_name", sa.String(length=96), nullable=False),
        sa.Column("provider_version", sa.String(length=96), nullable=False),
        sa.Column("model_or_engine_version", sa.String(length=128), nullable=False),
        sa.Column("source_artifact_ids", sa.JSON(), nullable=False),
        sa.Column("grounding_summary", sa.Text(), nullable=False),
        sa.Column("response_text", sa.Text(), nullable=False),
        sa.Column("refused", sa.Boolean(), nullable=False),
        sa.Column("refusal_reason", sa.String(length=96), nullable=True),
        sa.Column("limitations", sa.JSON(), nullable=False),
        sa.Column("disclaimer", sa.Text(), nullable=False),
        sa.Column("research_status", sa.String(length=64), nullable=False),
        sa.Column("audit_correlation_id", sa.String(length=64), nullable=False),
        sa.Column("provenance", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("assistant_response_id"),
    )
    op.create_index(
        "ix_assistant_research_responses_created_at",
        "assistant_research_responses",
        ["created_at"],
    )
    op.create_index(
        "ix_assistant_research_responses_operator",
        "assistant_research_responses",
        ["operator_id"],
    )
    op.create_index(
        "ix_assistant_research_responses_request_hash",
        "assistant_research_responses",
        ["request_text_hash"],
    )
    op.create_index(
        "ix_assistant_research_responses_correlation_id",
        "assistant_research_responses",
        ["audit_correlation_id"],
    )
    op.create_index(
        "ix_assistant_research_responses_refused",
        "assistant_research_responses",
        ["refused"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_assistant_research_responses_refused",
        table_name="assistant_research_responses",
    )
    op.drop_index(
        "ix_assistant_research_responses_correlation_id",
        table_name="assistant_research_responses",
    )
    op.drop_index(
        "ix_assistant_research_responses_request_hash",
        table_name="assistant_research_responses",
    )
    op.drop_index(
        "ix_assistant_research_responses_operator",
        table_name="assistant_research_responses",
    )
    op.drop_index(
        "ix_assistant_research_responses_created_at",
        table_name="assistant_research_responses",
    )
    op.drop_table("assistant_research_responses")
