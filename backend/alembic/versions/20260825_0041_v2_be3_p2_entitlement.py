"""V2 BE-3 P2: entitlement verification migration (BO-V2-BE-3-P2-001 §3.8).

The SOLE P2 registry mutation. Records the ITRGA-reviewed Operator
entitlement evidence (ITRGA-DET-V2-BE-3-P2-ENT-001):

    Plan: Basic — 8 API credits/minute, 8 WebSocket credits, 800/day
    entitlement_status: verified
    source_status: UNCHANGED (architecture_candidate)
    persistence_permitted: UNCHANGED (false)

Dialect-aware registry-guard handling: drop trigger(s) → update entitlement
fields only → recreate trigger(s), ordered so the guard is absent only
inside this migration run. Interruption safety: the upgrade verifies guard
presence at the end; the standalone verify helper (scripts side) and the
BE-3 P2 tests re-prove refusal post-migration on both dialects.

Revision ID: 20260825_0041
Revises: 20260824_0040
"""

from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "20260825_0041"
down_revision = "20260824_0040"
branch_labels = None
depends_on = None

#: Verified entitlement values — sourced ONLY from the evidence reviewed in
#: ITRGA-DET-V2-BE-3-P2-ENT-001. The displayed allowance does NOT amend the
#: hard 35-attempt cap.
VERIFIED_ENTITLEMENT = {
    "plan": "Basic",
    "api_credits_per_minute": 8,
    "websocket_credits": 8,
    "api_credits_per_day": 800,
    "evidence_ref": "ITRGA-DET-V2-BE-3-P2-ENT-001",
    "operator_decision": "AXIOM-V2-OD-BE-3-P2-002",
    "note": "Bounded P2 evaluation only; does not amend the 35-attempt cap;"
    " no persistence/redistribution rights evidenced",
}


def _drop_registry_guard(bind) -> None:
    if bind.dialect.name == "postgresql":
        op.execute("DROP TRIGGER IF EXISTS v2_md_provider_immutable ON v2_md_provider")
    elif bind.dialect.name == "sqlite":
        op.execute("DROP TRIGGER IF EXISTS v2_md_provider_immutable_update")
        op.execute("DROP TRIGGER IF EXISTS v2_md_provider_immutable_delete")


def _create_registry_guard(bind) -> None:
    if bind.dialect.name == "postgresql":
        # Function retained from 0040; recreate the trigger only.
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


def _verify_guard_present(bind) -> None:
    """Interruption-safety check: fail the migration loudly if the guard did
    not come back — a failed/interrupted run must never be presented as safe."""
    if bind.dialect.name == "postgresql":
        count = bind.execute(
            sa.text("SELECT COUNT(*) FROM pg_trigger WHERE tgname='v2_md_provider_immutable'")
        ).scalar_one()
        expected = 1
    elif bind.dialect.name == "sqlite":
        count = bind.execute(
            sa.text(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'"
                " AND name IN ('v2_md_provider_immutable_update','v2_md_provider_immutable_delete')"
            )
        ).scalar_one()
        expected = 2
    else:  # pragma: no cover
        return
    if int(count) != expected:
        raise RuntimeError(
            "P2 entitlement migration: registry guard NOT restored — manual"
            " recovery required; do not treat this migration as applied"
        )


def upgrade() -> None:
    from datetime import datetime, timezone
    from uuid import uuid4

    bind = op.get_bind()

    # BE-3 P2 permission — introduced ONLY by this revision (DEL-004:
    # the 0038 seed is revision-local; no earlier revision can contain it).
    # Idempotence guard retained for defensive re-run safety only.
    existing = {
        (row[0], row[1])
        for row in bind.execute(sa.text("SELECT role, permission FROM v2_permission"))
    }
    if ("admin", "v2.marketdata.provider.contract_test") not in existing:
        permission_table = sa.table(
            "v2_permission",
            sa.column("id", sa.String),
            sa.column("role", sa.String),
            sa.column("permission", sa.String),
            sa.column("sal", sa.String),
            sa.column("created_at", sa.DateTime(timezone=True)),
        )
        op.execute(
            permission_table.insert().values(
                id=str(uuid4()),
                role="admin",
                permission="v2.marketdata.provider.contract_test",
                sal="SAL-4",
                created_at=datetime.now(timezone.utc),
            )
        )

    _drop_registry_guard(bind)
    # PG-001 correction: bind the entitlement through a typed JSON parameter
    # so PostgreSQL receives a json-typed expression (asyncpg rejected the
    # previous untyped VARCHAR bind) while SQLite keeps its JSON-serialized
    # storage. Table construct + typed column = dialect-correct binds; no
    # string-concatenated SQL.
    provider_table = sa.table(
        "v2_md_provider",
        sa.column("provider_id", sa.String),
        sa.column("entitlement", sa.JSON),
        sa.column("entitlement_status", sa.String),
    )
    op.execute(
        provider_table.update()
        .where(provider_table.c.provider_id == "twelvedata")
        .values(entitlement=VERIFIED_ENTITLEMENT, entitlement_status="verified")
    )
    _create_registry_guard(bind)
    _verify_guard_present(bind)


def downgrade() -> None:
    bind = op.get_bind()
    op.execute(
        "DELETE FROM v2_permission"
        " WHERE permission = 'v2.marketdata.provider.contract_test'"
    )
    _drop_registry_guard(bind)
    provider_table = sa.table(
        "v2_md_provider",
        sa.column("provider_id", sa.String),
        sa.column("entitlement", sa.JSON),
        sa.column("entitlement_status", sa.String),
    )
    op.execute(
        provider_table.update()
        .where(provider_table.c.provider_id == "twelvedata")
        .values(entitlement=sa.null(), entitlement_status="unverified")
    )
    _create_registry_guard(bind)
    _verify_guard_present(bind)
