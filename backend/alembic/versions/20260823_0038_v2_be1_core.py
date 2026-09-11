"""V2 BE-1 Core: audit, lineage, capability, permission tables with dialect-aware immutability triggers.

Revision ID: 20260823_0038
Revises: 20260717_0037
Create Date: 2026-08-23
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers
revision = "20260823_0038"
down_revision = "20260717_0037"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create v2_audit_event table
    op.create_table(
        "v2_audit_event",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("correlation_id", sa.String(64), nullable=False),
        sa.Column("causation_id", sa.String(64), nullable=True),
        sa.Column("actor_id", sa.String(128), nullable=False),
        sa.Column("actor_type", sa.String(32), nullable=False),
        sa.Column("domain", sa.String(64), nullable=False),
        sa.Column("action", sa.String(128), nullable=False),
        sa.Column("resource_type", sa.String(64), nullable=True),
        sa.Column("resource_id", sa.String(128), nullable=True),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("details", sa.JSON, nullable=True),
        sa.Column("classification", sa.String(32), nullable=False, server_default="internal"),
        sa.Column("operator_id", sa.String(128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_v2_audit_domain_created", "v2_audit_event", ["domain", "created_at"])
    op.create_index("ix_v2_audit_actor", "v2_audit_event", ["actor_id"])
    op.create_index("ix_v2_audit_correlation", "v2_audit_event", ["correlation_id"])
    op.create_index("ix_v2_audit_mode", "v2_audit_event", ["mode"])
    op.create_index("ix_v2_audit_operator", "v2_audit_event", ["operator_id"])

    # Create v2_lineage_record table
    op.create_table(
        "v2_lineage_record",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("artifact_type", sa.String(64), nullable=False),
        sa.Column("artifact_id", sa.String(128), nullable=False),
        sa.Column("source_artifact_ids", sa.JSON, nullable=True),
        sa.Column("computation_version", sa.String(64), nullable=True),
        sa.Column("input_snapshot_id", sa.String(128), nullable=True),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_v2_lineage_artifact", "v2_lineage_record", ["artifact_type", "artifact_id"])
    op.create_index("ix_v2_lineage_operator", "v2_lineage_record", ["operator_id"])
    op.create_index("ix_v2_lineage_mode", "v2_lineage_record", ["mode"])

    # Create v2_capability_record table
    op.create_table(
        "v2_capability_record",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("capability_id", sa.String(128), nullable=False, unique=True),
        sa.Column("domain", sa.String(64), nullable=False),
        sa.Column("band", sa.String(16), nullable=False),
        sa.Column("maturity", sa.String(32), nullable=False),
        sa.Column("artifact_status", sa.String(32), nullable=False),
        sa.Column("version", sa.String(16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_v2_capability_id", "v2_capability_record", ["capability_id"], unique=True)
    op.create_index("ix_v2_capability_domain", "v2_capability_record", ["domain"])
    op.create_index("ix_v2_capability_band", "v2_capability_record", ["band"])

    # Create v2_permission table
    op.create_table(
        "v2_permission",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("role", sa.String(32), nullable=False),
        sa.Column("permission", sa.String(128), nullable=False),
        sa.Column("sal", sa.String(16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_v2_permission_role_permission", "v2_permission", ["role", "permission"], unique=True)

    # Dialect-aware immutability triggers
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        # PostgreSQL: function + trigger
        op.execute("""
            CREATE OR REPLACE FUNCTION prevent_v2_audit_mutation()
            RETURNS TRIGGER AS $$
            BEGIN
                RAISE EXCEPTION 'V2 audit events are immutable; UPDATE/DELETE prohibited';
            END;
            $$ LANGUAGE plpgsql;
        """)
        op.execute("""
            CREATE TRIGGER v2_audit_immutable
            BEFORE UPDATE OR DELETE ON v2_audit_event
            FOR EACH ROW EXECUTE FUNCTION prevent_v2_audit_mutation();
        """)

        op.execute("""
            CREATE OR REPLACE FUNCTION prevent_v2_lineage_mutation()
            RETURNS TRIGGER AS $$
            BEGIN
                RAISE EXCEPTION 'V2 lineage records are immutable; UPDATE/DELETE prohibited';
            END;
            $$ LANGUAGE plpgsql;
        """)
        op.execute("""
            CREATE TRIGGER v2_lineage_immutable
            BEFORE UPDATE OR DELETE ON v2_lineage_record
            FOR EACH ROW EXECUTE FUNCTION prevent_v2_lineage_mutation();
        """)
    elif bind.dialect.name == "sqlite":
        # SQLite: triggers
        op.execute("""
            CREATE TRIGGER v2_audit_immutable_update
            BEFORE UPDATE ON v2_audit_event
            BEGIN
                SELECT RAISE(ABORT, 'V2 audit events are immutable; UPDATE prohibited');
            END;
        """)
        op.execute("""
            CREATE TRIGGER v2_audit_immutable_delete
            BEFORE DELETE ON v2_audit_event
            BEGIN
                SELECT RAISE(ABORT, 'V2 audit events are immutable; DELETE prohibited');
            END;
        """)
        op.execute("""
            CREATE TRIGGER v2_lineage_immutable_update
            BEFORE UPDATE ON v2_lineage_record
            BEGIN
                SELECT RAISE(ABORT, 'V2 lineage records are immutable; UPDATE prohibited');
            END;
        """)
        op.execute("""
            CREATE TRIGGER v2_lineage_immutable_delete
            BEFORE DELETE ON v2_lineage_record
            BEGIN
                SELECT RAISE(ABORT, 'V2 lineage records are immutable; DELETE prohibited');
            END;
        """)

    # Seed capability records
    from datetime import datetime, timezone
    from uuid import uuid4

    from app.v2.capability.seed import V2_CAPABILITY_SEED

    capability_table = sa.table(
        "v2_capability_record",
        sa.column("id", sa.String),
        sa.column("capability_id", sa.String),
        sa.column("domain", sa.String),
        sa.column("band", sa.String),
        sa.column("maturity", sa.String),
        sa.column("artifact_status", sa.String),
        sa.column("version", sa.String),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    for cap in V2_CAPABILITY_SEED:
        op.execute(
            capability_table.insert().values(
                id=str(uuid4()),
                capability_id=cap["capability_id"],
                domain=cap["domain"],
                band=cap["band"],
                maturity=cap["maturity"],
                artifact_status=cap["artifact_status"],
                version=cap["version"],
                created_at=datetime.now(timezone.utc),
            )
        )

    # Seed permission records — REVISION-LOCAL IMMUTABLE seed data
    # (DEL-004 correction, ITRGA-REV-V2-BE-3-P2-DELIVERY-001: historical
    # migrations must not read the mutable runtime permission structure;
    # this literal list is the BE-1-era inventory and never changes).
    V2_PERMISSION_SEED = [
        {"role": "admin", "permission": "v2.mode.read", "sal": "SAL-2"},
        {"role": "admin", "permission": "v2.capability.read", "sal": "SAL-2"},
        {"role": "admin", "permission": "v2.audit.read", "sal": "SAL-3"},
        {"role": "admin", "permission": "v2.audit.read_all", "sal": "SAL-4"},
        {"role": "admin", "permission": "v2.lineage.read", "sal": "SAL-3"},
        {"role": "admin", "permission": "v2.lineage.read_all", "sal": "SAL-4"},
        {"role": "admin", "permission": "v2.error.read", "sal": "SAL-2"},
        {"role": "operator", "permission": "v2.mode.read", "sal": "SAL-2"},
        {"role": "operator", "permission": "v2.capability.read", "sal": "SAL-2"},
        {"role": "operator", "permission": "v2.audit.read", "sal": "SAL-3"},
        {"role": "operator", "permission": "v2.lineage.read", "sal": "SAL-3"},
        {"role": "operator", "permission": "v2.error.read", "sal": "SAL-2"},
    ]

    permission_table = sa.table(
        "v2_permission",
        sa.column("id", sa.String),
        sa.column("role", sa.String),
        sa.column("permission", sa.String),
        sa.column("sal", sa.String),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    for perm in V2_PERMISSION_SEED:
        op.execute(
            permission_table.insert().values(
                id=str(uuid4()),
                role=perm["role"],
                permission=perm["permission"],
                sal=perm["sal"],
                created_at=datetime.now(timezone.utc),
            )
        )


def downgrade() -> None:
    bind = op.get_bind()

    # Remove triggers first
    if bind.dialect.name == "postgresql":
        op.execute("DROP TRIGGER IF EXISTS v2_audit_immutable ON v2_audit_event")
        op.execute("DROP FUNCTION IF EXISTS prevent_v2_audit_mutation()")
        op.execute("DROP TRIGGER IF EXISTS v2_lineage_immutable ON v2_lineage_record")
        op.execute("DROP FUNCTION IF EXISTS prevent_v2_lineage_mutation()")
    elif bind.dialect.name == "sqlite":
        op.execute("DROP TRIGGER IF EXISTS v2_audit_immutable_update")
        op.execute("DROP TRIGGER IF EXISTS v2_audit_immutable_delete")
        op.execute("DROP TRIGGER IF EXISTS v2_lineage_immutable_update")
        op.execute("DROP TRIGGER IF EXISTS v2_lineage_immutable_delete")

    # Drop tables
    op.drop_table("v2_permission")
    op.drop_table("v2_capability_record")
    op.drop_table("v2_lineage_record")
    op.drop_table("v2_audit_event")
