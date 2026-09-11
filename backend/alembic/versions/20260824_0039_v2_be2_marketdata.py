"""V2 BE-2: market-data abstraction — six additive tables, dialect-aware
append-only triggers on integrity-exception and as-of-verification tables,
versioned reference-data seed (BO-V2-BE-2-001).

Revision ID: 20260824_0039
Revises: 20260823_0038
"""

from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "20260824_0039"
down_revision = "20260823_0038"
branch_labels = None
depends_on = None

_MARKET_CLASSES = "'forex','crypto','index','equity','commodity','metal','future','etf','synthetic'"


def upgrade() -> None:
    # --- v2_md_instrument -----------------------------------------------
    op.create_table(
        "v2_md_instrument",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("instrument_id", sa.String(96), nullable=False),
        sa.Column("market_class", sa.String(32), nullable=False),
        sa.Column("display_symbol", sa.String(64), nullable=False),
        sa.Column("precision", sa.Integer, nullable=False),
        sa.Column("meta", sa.JSON, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("instrument_id", name="uq_v2_md_instrument_id"),
        sa.CheckConstraint(
            f"market_class IN ({_MARKET_CLASSES})", name="ck_v2_md_instrument_class"
        ),
    )
    op.create_index("ix_v2_md_instrument_class", "v2_md_instrument", ["market_class"])

    # --- v2_md_symbol_map -------------------------------------------------
    op.create_table(
        "v2_md_symbol_map",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("source_id", sa.String(64), nullable=False),
        sa.Column("source_symbol", sa.String(64), nullable=False),
        sa.Column("instrument_id", sa.String(96), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("source_id", "source_symbol", name="uq_v2_md_symbol_map"),
    )
    op.create_index("ix_v2_md_symbol_map_instrument", "v2_md_symbol_map", ["instrument_id"])

    # --- v2_md_source -----------------------------------------------------
    op.create_table(
        "v2_md_source",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("source_id", sa.String(64), nullable=False),
        sa.Column("kind", sa.String(16), nullable=False),
        sa.Column("authority", sa.String(32), nullable=False),
        sa.Column("mode_scope", sa.String(16), nullable=False),
        sa.Column("active", sa.Boolean, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("source_id", name="uq_v2_md_source_id"),
        sa.CheckConstraint(
            "kind IN ('simulator','seed','import','reserved')", name="ck_v2_md_source_kind"
        ),
        sa.CheckConstraint(
            "authority IN ('seed:synthetic','live:simulated','historical:imported','unknown')",
            name="ck_v2_md_source_authority",
        ),
        sa.CheckConstraint(
            "active = false OR authority IN ('seed:synthetic','live:simulated','unknown')",
            name="ck_v2_md_source_active_authority",
        ),
        sa.CheckConstraint(
            "mode_scope IN ('RESEARCH','SIMULATION')", name="ck_v2_md_source_mode"
        ),
    )

    # --- v2_md_series -----------------------------------------------------
    op.create_table(
        "v2_md_series",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("instrument_id", sa.String(96), nullable=False),
        sa.Column("timeframe", sa.String(16), nullable=False),
        sa.Column("source_id", sa.String(64), nullable=False),
        sa.Column("first_open_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_open_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("bar_count", sa.Integer, nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "instrument_id", "timeframe", "source_id", name="uq_v2_md_series_triple"
        ),
    )
    op.create_index("ix_v2_md_series_instrument", "v2_md_series", ["instrument_id"])

    # --- v2_md_integrity_exception (append-only) ---------------------------
    op.create_table(
        "v2_md_integrity_exception",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("series_ref", sa.String(192), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("exception_type", sa.String(32), nullable=False),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("detail", sa.JSON, nullable=True),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("fingerprint", name="uq_v2_md_integrity_fingerprint"),
        sa.CheckConstraint(
            "exception_type IN ('out_of_order','duplicate','future_data',"
            "'unmapped_symbol','gap','stale','verification_mismatch')",
            name="ck_v2_md_integrity_type",
        ),
    )
    op.create_index(
        "ix_v2_md_integrity_series", "v2_md_integrity_exception", ["series_ref", "observed_at"]
    )
    op.create_index(
        "ix_v2_md_integrity_operator", "v2_md_integrity_exception", ["operator_id"]
    )

    # --- v2_md_asof_verification (append-only; verification-only) ----------
    op.create_table(
        "v2_md_asof_verification",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("verification_id", sa.String(64), nullable=False),
        sa.Column("scope", sa.JSON, nullable=False),
        sa.Column("as_of", sa.DateTime(timezone=True), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("row_count", sa.Integer, nullable=False),
        sa.Column("source_ids", sa.JSON, nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("created_by_operator_id", sa.String(128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("verification_id", name="uq_v2_md_asof_verification_id"),
    )
    op.create_index(
        "ix_v2_md_asof_verification_operator",
        "v2_md_asof_verification",
        ["created_by_operator_id"],
    )

    # --- dialect-aware append-only triggers (BE-1 pattern) ------------------
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("""
            CREATE OR REPLACE FUNCTION prevent_v2_md_integrity_mutation()
            RETURNS TRIGGER AS $$
            BEGIN
                RAISE EXCEPTION 'V2 integrity exceptions are immutable; UPDATE/DELETE prohibited';
            END;
            $$ LANGUAGE plpgsql;
        """)
        op.execute("""
            CREATE TRIGGER v2_md_integrity_immutable
            BEFORE UPDATE OR DELETE ON v2_md_integrity_exception
            FOR EACH ROW EXECUTE FUNCTION prevent_v2_md_integrity_mutation();
        """)
        op.execute("""
            CREATE OR REPLACE FUNCTION prevent_v2_md_verification_mutation()
            RETURNS TRIGGER AS $$
            BEGIN
                RAISE EXCEPTION 'V2 as-of verification records are immutable; UPDATE/DELETE prohibited';
            END;
            $$ LANGUAGE plpgsql;
        """)
        op.execute("""
            CREATE TRIGGER v2_md_verification_immutable
            BEFORE UPDATE OR DELETE ON v2_md_asof_verification
            FOR EACH ROW EXECUTE FUNCTION prevent_v2_md_verification_mutation();
        """)
    elif bind.dialect.name == "sqlite":
        op.execute("""
            CREATE TRIGGER v2_md_integrity_immutable_update
            BEFORE UPDATE ON v2_md_integrity_exception
            BEGIN
                SELECT RAISE(ABORT, 'V2 integrity exceptions are immutable; UPDATE prohibited');
            END;
        """)
        op.execute("""
            CREATE TRIGGER v2_md_integrity_immutable_delete
            BEFORE DELETE ON v2_md_integrity_exception
            BEGIN
                SELECT RAISE(ABORT, 'V2 integrity exceptions are immutable; DELETE prohibited');
            END;
        """)
        op.execute("""
            CREATE TRIGGER v2_md_verification_immutable_update
            BEFORE UPDATE ON v2_md_asof_verification
            BEGIN
                SELECT RAISE(ABORT, 'V2 as-of verification records are immutable; UPDATE prohibited');
            END;
        """)
        op.execute("""
            CREATE TRIGGER v2_md_verification_immutable_delete
            BEFORE DELETE ON v2_md_asof_verification
            BEGIN
                SELECT RAISE(ABORT, 'V2 as-of verification records are immutable; DELETE prohibited');
            END;
        """)

    # --- reference-data seed from the versioned manifest module -------------
    from datetime import datetime, timezone
    from uuid import uuid4

    from app.v2.marketdata.seed import (
        V2_MD_INSTRUMENT_SEED,
        V2_MD_SOURCE_SEED,
        V2_MD_SYMBOL_MAP_SEED,
    )

    now = datetime.now(timezone.utc)

    source_table = sa.table(
        "v2_md_source",
        sa.column("id", sa.String),
        sa.column("source_id", sa.String),
        sa.column("kind", sa.String),
        sa.column("authority", sa.String),
        sa.column("mode_scope", sa.String),
        sa.column("active", sa.Boolean),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    for row in V2_MD_SOURCE_SEED:
        op.execute(source_table.insert().values(id=str(uuid4()), created_at=now, **row))

    instrument_table = sa.table(
        "v2_md_instrument",
        sa.column("id", sa.String),
        sa.column("instrument_id", sa.String),
        sa.column("market_class", sa.String),
        sa.column("display_symbol", sa.String),
        sa.column("precision", sa.Integer),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    for row in V2_MD_INSTRUMENT_SEED:
        op.execute(instrument_table.insert().values(id=str(uuid4()), created_at=now, **row))

    map_table = sa.table(
        "v2_md_symbol_map",
        sa.column("id", sa.String),
        sa.column("source_id", sa.String),
        sa.column("source_symbol", sa.String),
        sa.column("instrument_id", sa.String),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    for row in V2_MD_SYMBOL_MAP_SEED:
        op.execute(map_table.insert().values(id=str(uuid4()), created_at=now, **row))

    # --- BE-2 permission seed into existing v2_permission table -------------
    permission_table = sa.table(
        "v2_permission",
        sa.column("id", sa.String),
        sa.column("role", sa.String),
        sa.column("permission", sa.String),
        sa.column("sal", sa.String),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    be2_permissions = [
        ("admin", "v2.marketdata.read", "SAL-2"),
        ("admin", "v2.marketdata.read_all", "SAL-4"),
        ("admin", "v2.marketdata.verify", "SAL-3"),
        ("admin", "v2.marketdata.catalog.refresh", "SAL-3"),
        ("operator", "v2.marketdata.read", "SAL-2"),
        ("operator", "v2.marketdata.verify", "SAL-3"),
    ]
    from uuid import uuid4 as _uuid4

    # Idempotent insert: the BE-1 migration seeds v2_permission dynamically
    # from V2_PERMISSION_SEED, so a fresh chain already contains these rows;
    # an existing BE-1 database does not. Insert only the missing rows.
    connection = op.get_bind()
    existing = {
        (row[0], row[1])
        for row in connection.execute(
            sa.text("SELECT role, permission FROM v2_permission")
        )
    }
    for role, permission, sal in be2_permissions:
        if (role, permission) in existing:
            continue
        op.execute(
            permission_table.insert().values(
                id=str(_uuid4()), role=role, permission=permission, sal=sal, created_at=now
            )
        )


def downgrade() -> None:
    bind = op.get_bind()

    # Remove BE-2 permission rows from the shared v2_permission table
    op.execute(
        "DELETE FROM v2_permission WHERE permission IN ("
        "'v2.marketdata.read','v2.marketdata.read_all',"
        "'v2.marketdata.verify','v2.marketdata.catalog.refresh')"
    )

    # Remove triggers first
    if bind.dialect.name == "postgresql":
        op.execute("DROP TRIGGER IF EXISTS v2_md_integrity_immutable ON v2_md_integrity_exception")
        op.execute("DROP FUNCTION IF EXISTS prevent_v2_md_integrity_mutation()")
        op.execute("DROP TRIGGER IF EXISTS v2_md_verification_immutable ON v2_md_asof_verification")
        op.execute("DROP FUNCTION IF EXISTS prevent_v2_md_verification_mutation()")
    elif bind.dialect.name == "sqlite":
        op.execute("DROP TRIGGER IF EXISTS v2_md_integrity_immutable_update")
        op.execute("DROP TRIGGER IF EXISTS v2_md_integrity_immutable_delete")
        op.execute("DROP TRIGGER IF EXISTS v2_md_verification_immutable_update")
        op.execute("DROP TRIGGER IF EXISTS v2_md_verification_immutable_delete")

    op.drop_index("ix_v2_md_asof_verification_operator", table_name="v2_md_asof_verification")
    op.drop_table("v2_md_asof_verification")
    op.drop_index("ix_v2_md_integrity_operator", table_name="v2_md_integrity_exception")
    op.drop_index("ix_v2_md_integrity_series", table_name="v2_md_integrity_exception")
    op.drop_table("v2_md_integrity_exception")
    op.drop_index("ix_v2_md_series_instrument", table_name="v2_md_series")
    op.drop_table("v2_md_series")
    op.drop_table("v2_md_source")
    op.drop_index("ix_v2_md_symbol_map_instrument", table_name="v2_md_symbol_map")
    op.drop_table("v2_md_symbol_map")
    op.drop_index("ix_v2_md_instrument_class", table_name="v2_md_instrument")
    op.drop_table("v2_md_instrument")
