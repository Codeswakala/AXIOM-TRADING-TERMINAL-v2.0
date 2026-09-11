"""V2 BE-10 — account context (BO-V2-BE-10-001 B-1.5; seed-only).

INSERT-only; zero UPDATE/DELETE; zero new tables (B-0 D-4 ruling).
Seeds: (a) compver row `account_context_engine|ace-1.0.0` (engine body
hashed from disk at apply time — household recipe); (b) permission
`v2.account_context.read` (admin per ROLE-ROW convention);
(c) `v2_md_source` row `exness_mt5_demo` (the FOURTH source);
(d) exactly the 12 SEALED `v2_md_symbol_map` pairs (suffixed forms —
build may not invent others). Downgrade reverses exactly those inserts.

Revision ID: 20260908_0050
Revises: 20260905_0049
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import sqlalchemy as sa

from alembic import op

revision = "20260908_0050"
down_revision = "20260905_0049"
branch_labels = None
depends_on = None

_PERMISSIONS = (
    ("admin", "v2.account_context.read", "SAL-2"),
)

_ACE_FILES = (
    "app/v2/account_context/engine.py",
)

# The fourth source row, fitted INSIDE the closed BE-2 vocabulary
# (ck_v2_md_source_kind/authority/active_authority CHECKs bind; a seed-only
# migration may not amend CHECKs). Honest classification: this row is a
# symbol-mapping ANCHOR for the BE-9/BE-10 read seam, not an authoritative
# market-data source — kind='import' (broker-imported symbols),
# authority='unknown' (non-authoritative by construction; lawful with
# active=true under ck_v2_md_source_active_authority). Disclosed in the
# delivery note.
_BROKER_SOURCE = {
    "source_id": "exness_mt5_demo",
    "kind": "import",
    "authority": "unknown",
    "mode_scope": "RESEARCH",
    "active": True,
}

# The 12 SEALED map pairs (BO commission text — exactly these, no others).
_SYMBOL_MAP = (
    ("EURUSDm", "forex.eurusd"),
    ("GBPUSDm", "forex.gbpusd"),
    ("USDJPYm", "forex.usdjpy"),
    ("AUDUSDm", "forex.audusd"),
    ("USDCADm", "forex.usdcad"),
    ("USDCHFm", "forex.usdchf"),
    ("NZDUSDm", "forex.nzdusd"),
    ("EURGBPm", "forex.eurgbp"),
    ("BTCUSDm", "crypto.btcusd"),
    ("ETHUSDm", "crypto.ethusd"),
    ("SOLUSDm", "crypto.solusd"),
    ("XAUUSDm", "metal.xauusd"),
)


def _rolling_hash(files: tuple[str, ...]) -> str:
    base = Path(__file__).resolve().parents[2]
    digest = hashlib.sha256()
    for rel in files:
        digest.update(rel.encode("utf-8"))
        digest.update(b"\x00")
        digest.update((base / rel).read_bytes())
        digest.update(b"\x00")
    return digest.hexdigest()


def upgrade() -> None:
    bind = op.get_bind()
    now = datetime.now(timezone.utc)

    # (a) compver row
    compver = sa.table(
        "v2_computation_version",
        sa.column("id", sa.String), sa.column("component", sa.String),
        sa.column("version", sa.String), sa.column("source_hash", sa.String),
        sa.column("evidence_ref", sa.String),
        sa.column("registered_at", sa.DateTime(timezone=True)),
    )
    op.execute(compver.insert().values(
        id=str(uuid4()), component="account_context_engine",
        version="ace-1.0.0", source_hash=_rolling_hash(_ACE_FILES),
        evidence_ref="BO-V2-BE-10-001", registered_at=now,
    ))

    # (b) permission (existing-set filter; DEL-004 law)
    permission_table = sa.table(
        "v2_permission",
        sa.column("id", sa.String), sa.column("role", sa.String),
        sa.column("permission", sa.String), sa.column("sal", sa.String),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    existing = {
        (row[0], row[1])
        for row in bind.execute(
            sa.text("SELECT role, permission FROM v2_permission"))
    }
    for role, permission, sal in _PERMISSIONS:
        if (role, permission) not in existing:
            op.execute(permission_table.insert().values(
                id=str(uuid4()), role=role, permission=permission,
                sal=sal, created_at=now,
            ))

    # (c) the fourth source (refuse-if-present idempotency)
    source_table = sa.table(
        "v2_md_source",
        sa.column("id", sa.String), sa.column("source_id", sa.String),
        sa.column("kind", sa.String), sa.column("authority", sa.String),
        sa.column("mode_scope", sa.String), sa.column("active", sa.Boolean),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    present = bind.execute(sa.text(
        "SELECT COUNT(*) FROM v2_md_source WHERE source_id = :s"
    ).bindparams(s=_BROKER_SOURCE["source_id"])).scalar_one()
    if int(present) == 0:
        op.execute(source_table.insert().values(
            id=str(uuid4()), created_at=now, **_BROKER_SOURCE))

    # (d) exactly the 12 sealed map rows (existing-set filter)
    map_table = sa.table(
        "v2_md_symbol_map",
        sa.column("id", sa.String), sa.column("source_id", sa.String),
        sa.column("source_symbol", sa.String),
        sa.column("instrument_id", sa.String),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    existing_maps = {
        row[0] for row in bind.execute(sa.text(
            "SELECT source_symbol FROM v2_md_symbol_map"
            " WHERE source_id = :s"
        ).bindparams(s=_BROKER_SOURCE["source_id"]))
    }
    for source_symbol, instrument_id in _SYMBOL_MAP:
        if source_symbol not in existing_maps:
            op.execute(map_table.insert().values(
                id=str(uuid4()), source_id=_BROKER_SOURCE["source_id"],
                source_symbol=source_symbol, instrument_id=instrument_id,
                created_at=now))


def _drop_compver_delete_guard(bind) -> None:
    if bind.dialect.name == "sqlite":
        op.execute(
            "DROP TRIGGER IF EXISTS v2_computation_version_immutable_delete")
    elif bind.dialect.name == "postgresql":
        op.execute(
            "DROP TRIGGER IF EXISTS v2_computation_version_immutable_delete"
            " ON v2_computation_version")


def _recreate_compver_delete_guard(bind) -> None:
    if bind.dialect.name == "sqlite":
        op.execute("""
            CREATE TRIGGER v2_computation_version_immutable_delete
            BEFORE DELETE ON v2_computation_version
            BEGIN
                SELECT RAISE(ABORT,
                    'V2 computation version registry is immutable; DELETE prohibited');
            END;
        """)
        count = bind.execute(sa.text(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'"
            " AND name='v2_computation_version_immutable_delete'")).scalar_one()
    elif bind.dialect.name == "postgresql":
        op.execute("""
            CREATE TRIGGER v2_computation_version_immutable_delete
            BEFORE DELETE ON v2_computation_version
            FOR EACH ROW EXECUTE FUNCTION prevent_v2_research_mutation();
        """)
        count = bind.execute(sa.text(
            "SELECT COUNT(*) FROM pg_trigger"
            " WHERE tgname='v2_computation_version_immutable_delete'")).scalar_one()
    else:  # pragma: no cover
        return
    if int(count) != 1:
        raise RuntimeError(
            "compver delete guard NOT restored - manual recovery required")


def downgrade() -> None:
    bind = op.get_bind()
    for source_symbol, _instrument_id in _SYMBOL_MAP:
        op.execute(sa.text(
            "DELETE FROM v2_md_symbol_map WHERE source_id = :s"
            " AND source_symbol = :y"
        ).bindparams(s=_BROKER_SOURCE["source_id"], y=source_symbol))
    op.execute(sa.text(
        "DELETE FROM v2_md_source WHERE source_id = :s"
    ).bindparams(s=_BROKER_SOURCE["source_id"]))
    for _role, permission, _sal in _PERMISSIONS:
        op.execute(sa.text(
            "DELETE FROM v2_permission WHERE permission = :p"
        ).bindparams(p=permission))
    _drop_compver_delete_guard(bind)
    op.execute(sa.text(
        "DELETE FROM v2_computation_version"
        " WHERE component = :c AND version = :v"
    ).bindparams(c="account_context_engine", v="ace-1.0.0"))
    _recreate_compver_delete_guard(bind)
