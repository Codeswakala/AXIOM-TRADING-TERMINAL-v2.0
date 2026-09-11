"""V2 BE-3 P1: provider registry + append-only status history, inactive
reserved provider source/mapping rows, BE-3 read permissions
(BO-V2-BE-3-P1-001).

Revision ID: 20260824_0040
Revises: 20260824_0039
"""

from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "20260824_0040"
down_revision = "20260824_0039"
branch_labels = None
depends_on = None

_STATUSES = (
    "'architecture_candidate','contract_tested','integrated',"
    "'authorized','production_certified'"
)


def upgrade() -> None:
    # --- v2_md_provider (read-only seeded registry) -------------------------
    op.create_table(
        "v2_md_provider",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("provider_id", sa.String(64), nullable=False),
        sa.Column("display_name", sa.String(128), nullable=False),
        sa.Column("markets", sa.JSON, nullable=False),
        sa.Column("entitlement", sa.JSON, nullable=True),
        sa.Column("entitlement_status", sa.String(16), nullable=False),
        sa.Column("persistence_permitted", sa.Boolean, nullable=False),
        sa.Column("source_status", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("provider_id", name="uq_v2_md_provider_id"),
        sa.CheckConstraint(f"source_status IN ({_STATUSES})", name="ck_v2_md_provider_status"),
        sa.CheckConstraint(
            "entitlement_status IN ('unverified','verified','expired','revoked')",
            name="ck_v2_md_provider_entitlement",
        ),
    )

    # --- v2_md_provider_status_history (append-only; P1 genesis row only) ---
    op.create_table(
        "v2_md_provider_status_history",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("provider_id", sa.String(64), nullable=False),
        sa.Column("from_status", sa.String(32), nullable=True),
        sa.Column("to_status", sa.String(32), nullable=False),
        sa.Column("authority_ref", sa.String(128), nullable=False),
        sa.Column("evidence_ref", sa.String(256), nullable=True),
        sa.Column("operator_id", sa.String(128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(f"to_status IN ({_STATUSES})", name="ck_v2_md_provider_hist_to"),
    )
    op.create_index(
        "ix_v2_md_provider_hist_provider",
        "v2_md_provider_status_history",
        ["provider_id", "created_at"],
    )

    # --- append-only triggers (BE-2 pattern, both dialects) ------------------
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("""
            CREATE OR REPLACE FUNCTION prevent_v2_md_provider_hist_mutation()
            RETURNS TRIGGER AS $$
            BEGIN
                RAISE EXCEPTION 'V2 provider status history is immutable; UPDATE/DELETE prohibited';
            END;
            $$ LANGUAGE plpgsql;
        """)
        op.execute("""
            CREATE TRIGGER v2_md_provider_hist_immutable
            BEFORE UPDATE OR DELETE ON v2_md_provider_status_history
            FOR EACH ROW EXECUTE FUNCTION prevent_v2_md_provider_hist_mutation();
        """)
    elif bind.dialect.name == "sqlite":
        op.execute("""
            CREATE TRIGGER v2_md_provider_hist_immutable_update
            BEFORE UPDATE ON v2_md_provider_status_history
            BEGIN
                SELECT RAISE(ABORT, 'V2 provider status history is immutable; UPDATE prohibited');
            END;
        """)
        op.execute("""
            CREATE TRIGGER v2_md_provider_hist_immutable_delete
            BEFORE DELETE ON v2_md_provider_status_history
            BEGIN
                SELECT RAISE(ABORT, 'V2 provider status history is immutable; DELETE prohibited');
            END;
        """)

    # --- seeds ---------------------------------------------------------------
    from datetime import datetime, timezone
    from uuid import uuid4

    now = datetime.now(timezone.utc)

    provider_table = sa.table(
        "v2_md_provider",
        sa.column("id", sa.String),
        sa.column("provider_id", sa.String),
        sa.column("display_name", sa.String),
        sa.column("markets", sa.JSON),
        sa.column("entitlement", sa.JSON),
        sa.column("entitlement_status", sa.String),
        sa.column("persistence_permitted", sa.Boolean),
        sa.column("source_status", sa.String),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    op.execute(
        provider_table.insert().values(
            id=str(uuid4()),
            provider_id="twelvedata",
            display_name="Twelve Data (architecture candidate)",
            markets=["forex", "crypto", "metal"],
            entitlement=None,  # unverified — no provider figures (PLAN-003)
            entitlement_status="unverified",
            persistence_permitted=False,
            source_status="architecture_candidate",
            created_at=now,
        )
    )

    history_table = sa.table(
        "v2_md_provider_status_history",
        sa.column("id", sa.String),
        sa.column("provider_id", sa.String),
        sa.column("from_status", sa.String),
        sa.column("to_status", sa.String),
        sa.column("authority_ref", sa.String),
        sa.column("evidence_ref", sa.String),
        sa.column("operator_id", sa.String),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    op.execute(
        history_table.insert().values(
            id=str(uuid4()),
            provider_id="twelvedata",
            from_status=None,
            to_status="architecture_candidate",
            authority_ref="BO-V2-BE-3-P1-001",
            evidence_ref="AXIOM-V2-BE-3-DA-PLAN-001 v3.0.0 / ITRGA-DET-V2-BE-3-PLAN-001",
            operator_id=None,
            created_at=now,
        )
    )

    # Inactive reserved provider source row (authority stays reserved:
    # ck_v2_md_source_active_authority forbids activating it) + mapping rows.
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
    # NOTE: BE-2 CHECK admits only the four BE-2 authority values; the
    # reserved provider row therefore uses 'unknown' authority (honest,
    # unemittable-as-provider) until a future amendment introduces
    # provider vocabulary. kind='reserved' + active=False marks it.
    op.execute(
        source_table.insert().values(
            id=str(uuid4()),
            source_id="twelvedata",
            kind="reserved",
            authority="unknown",
            mode_scope="RESEARCH",
            active=False,
            created_at=now,
        )
    )

    map_table = sa.table(
        "v2_md_symbol_map",
        sa.column("id", sa.String),
        sa.column("source_id", sa.String),
        sa.column("source_symbol", sa.String),
        sa.column("instrument_id", sa.String),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    td_mappings = [
        ("EUR/USD", "forex.eurusd"),
        ("GBP/USD", "forex.gbpusd"),
        ("USD/JPY", "forex.usdjpy"),
        ("AUD/USD", "forex.audusd"),
        ("USD/CAD", "forex.usdcad"),
        ("USD/CHF", "forex.usdchf"),
        ("NZD/USD", "forex.nzdusd"),
        ("EUR/GBP", "forex.eurgbp"),
        ("BTC/USD", "crypto.btcusd"),
        ("ETH/USD", "crypto.ethusd"),
        ("SOL/USD", "crypto.solusd"),
        ("XAU/USD", "metal.xauusd"),
    ]
    for source_symbol, instrument_id in td_mappings:
        op.execute(
            map_table.insert().values(
                id=str(uuid4()),
                source_id="twelvedata",
                source_symbol=source_symbol,
                instrument_id=instrument_id,
                created_at=now,
            )
        )

    # --- BE-3 permissions (idempotent insert, BE-2 pattern) ------------------
    permission_table = sa.table(
        "v2_permission",
        sa.column("id", sa.String),
        sa.column("role", sa.String),
        sa.column("permission", sa.String),
        sa.column("sal", sa.String),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    be3_permissions = [
        ("admin", "v2.marketdata.provider.read", "SAL-2"),
        ("admin", "v2.marketdata.provider.read_history", "SAL-4"),
        ("operator", "v2.marketdata.provider.read", "SAL-2"),
    ]
    connection = op.get_bind()
    existing = {
        (row[0], row[1])
        for row in connection.execute(
            sa.text("SELECT role, permission FROM v2_permission")
        )
    }
    for role, permission, sal in be3_permissions:
        if (role, permission) in existing:
            continue
        op.execute(
            permission_table.insert().values(
                id=str(uuid4()), role=role, permission=permission, sal=sal, created_at=now
            )
        )

    # --- DEL-001: provider registry immutable at database level in P1 -------
    # Added AFTER seeding so the genesis rows insert cleanly. UPDATE/DELETE on
    # the registry is refused on both dialects; status/entitlement/persistence
    # cannot change without a future separately authorized transition design
    # (which would ship its own governed migration altering these guards).
    if bind.dialect.name == "postgresql":
        op.execute("""
            CREATE OR REPLACE FUNCTION prevent_v2_md_provider_mutation()
            RETURNS TRIGGER AS $$
            BEGIN
                RAISE EXCEPTION 'V2 provider registry is immutable in P1; UPDATE/DELETE prohibited';
            END;
            $$ LANGUAGE plpgsql;
        """)
        op.execute("""
            CREATE TRIGGER v2_md_provider_immutable
            BEFORE UPDATE OR DELETE ON v2_md_provider
            FOR EACH ROW EXECUTE FUNCTION prevent_v2_md_provider_mutation();
        """)
    elif bind.dialect.name == "sqlite":
        op.execute("""
            CREATE TRIGGER v2_md_provider_immutable_update
            BEFORE UPDATE ON v2_md_provider
            BEGIN
                SELECT RAISE(ABORT, 'V2 provider registry is immutable in P1; UPDATE prohibited');
            END;
        """)
        op.execute("""
            CREATE TRIGGER v2_md_provider_immutable_delete
            BEFORE DELETE ON v2_md_provider
            BEGIN
                SELECT RAISE(ABORT, 'V2 provider registry is immutable in P1; DELETE prohibited');
            END;
        """)


def downgrade() -> None:
    bind = op.get_bind()

    op.execute(
        "DELETE FROM v2_permission WHERE permission IN ("
        "'v2.marketdata.provider.read','v2.marketdata.provider.read_history')"
    )
    op.execute("DELETE FROM v2_md_symbol_map WHERE source_id = 'twelvedata'")
    op.execute("DELETE FROM v2_md_source WHERE source_id = 'twelvedata'")

    if bind.dialect.name == "postgresql":
        op.execute("DROP TRIGGER IF EXISTS v2_md_provider_immutable ON v2_md_provider")
        op.execute("DROP FUNCTION IF EXISTS prevent_v2_md_provider_mutation()")
        op.execute(
            "DROP TRIGGER IF EXISTS v2_md_provider_hist_immutable"
            " ON v2_md_provider_status_history"
        )
        op.execute("DROP FUNCTION IF EXISTS prevent_v2_md_provider_hist_mutation()")
    elif bind.dialect.name == "sqlite":
        op.execute("DROP TRIGGER IF EXISTS v2_md_provider_immutable_update")
        op.execute("DROP TRIGGER IF EXISTS v2_md_provider_immutable_delete")
        op.execute("DROP TRIGGER IF EXISTS v2_md_provider_hist_immutable_update")
        op.execute("DROP TRIGGER IF EXISTS v2_md_provider_hist_immutable_delete")

    op.drop_index(
        "ix_v2_md_provider_hist_provider", table_name="v2_md_provider_status_history"
    )
    op.drop_table("v2_md_provider_status_history")
    op.drop_table("v2_md_provider")
