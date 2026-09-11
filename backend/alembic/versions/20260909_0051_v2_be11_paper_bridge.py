"""V2 BE-11 — paper bridge (BO-V2-BE-11-001 D-2; exactly ONE upgrade line).

+1 table `v2_paper_bridge_drift_run` with guard pair (triggers 76->78);
+4 permission seeds (65->69, SS0 proposed enum); +1 compver row
`paper_bridge_engine|pbr-1.0.0` (12->13, rolled hash from disk).
Tolerance/staleness seed SLOTS stand EMPTY-FORCED: this migration lands
ZERO seed rows — absence is the shipped state; operator values arrive by
a future seeded overlay migration (no model/DDL edits). Symmetric
content-based downgrade.

Revision ID: 20260909_0051
Revises: 20260908_0050
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import sqlalchemy as sa

from alembic import op

revision = "20260909_0051"
down_revision = "20260908_0050"
branch_labels = None
depends_on = None

_TRIGGERS = (
    ("v2_paper_bridge_drift_run_immutable_update",
     "v2_paper_bridge_drift_run",
     "UPDATE", "V2 paper bridge drift runs are immutable; UPDATE prohibited"),
    ("v2_paper_bridge_drift_run_immutable_delete",
     "v2_paper_bridge_drift_run",
     "DELETE", "V2 paper bridge drift runs are immutable; DELETE prohibited"),
)

_PERMISSIONS = (
    ("admin", "v2.paper_bridge.intent.write", "SAL-3"),
    ("admin", "v2.paper_bridge.evaluate.write", "SAL-3"),
    ("admin", "v2.paper_bridge.ledger.read", "SAL-2"),
    ("admin", "v2.paper_bridge.drift.read", "SAL-2"),
)

_PBR_FILES = (
    "app/v2/paper_bridge/engine.py",
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


def _create_triggers(bind) -> None:
    if bind.dialect.name == "sqlite":
        for name, table, event, message in _TRIGGERS:
            op.execute(f"""
                CREATE TRIGGER {name}
                BEFORE {event} ON {table}
                BEGIN
                    SELECT RAISE(ABORT, '{message}');
                END;
            """)
    elif bind.dialect.name == "postgresql":
        op.execute("""
            CREATE OR REPLACE FUNCTION prevent_v2_paper_bridge_mutation()
            RETURNS trigger AS $$
            BEGIN
                RAISE EXCEPTION
                    'V2 paper-bridge artifact is immutable; % prohibited on %',
                    TG_OP, TG_TABLE_NAME;
            END;
            $$ LANGUAGE plpgsql;
        """)
        for name, table, event, _message in _TRIGGERS:
            op.execute(f"""
                CREATE TRIGGER {name}
                BEFORE {event} ON {table}
                FOR EACH ROW EXECUTE FUNCTION prevent_v2_paper_bridge_mutation();
            """)


def _drop_triggers(bind) -> None:
    if bind.dialect.name == "sqlite":
        for name, _t, _e, _m in _TRIGGERS:
            op.execute(f"DROP TRIGGER IF EXISTS {name}")
    elif bind.dialect.name == "postgresql":
        for name, table, _e, _m in _TRIGGERS:
            op.execute(f"DROP TRIGGER IF EXISTS {name} ON {table}")
        op.execute(
            "DROP FUNCTION IF EXISTS prevent_v2_paper_bridge_mutation()")


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


def upgrade() -> None:
    bind = op.get_bind()
    now = datetime.now(timezone.utc)

    op.create_table(
        "v2_paper_bridge_drift_run",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("run_kind", sa.String(16), nullable=False),
        sa.Column("basis_sync_run_id", sa.String(36), nullable=True),
        sa.Column("paper_side", sa.JSON(), nullable=True),
        sa.Column("broker_side", sa.JSON(), nullable=True),
        sa.Column("tolerances_in_force", sa.JSON(), nullable=True),
        sa.Column("verdict", sa.String(24), nullable=True),
        sa.Column("digest", sa.String(64), nullable=True),
        sa.Column("seed_name", sa.String(64), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.Column("actor_id", sa.String(128), nullable=False),
        sa.Column("data_class", sa.String(32), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("run_kind IN ('drift_run','seed')",
                           name="ck_v2_pbdrift_kind"),
        sa.CheckConstraint(
            "verdict IN ('within_tolerance','drift_minor','drift_major',"
            "'uncomputable') OR verdict IS NULL",
            name="ck_v2_pbdrift_verdict"),
        sa.CheckConstraint(
            "(run_kind = 'drift_run') = (verdict IS NOT NULL)",
            name="ck_v2_pbdrift_verdict_iff"),
        sa.CheckConstraint("seed_name IS NULL OR run_kind = 'seed'",
                           name="ck_v2_pbdrift_seed_kind"),
        sa.CheckConstraint("data_class IN ('simulated')",
                           name="ck_v2_pbdrift_data_class"),
    )
    op.create_index("ix_v2_pbdrift_created", "v2_paper_bridge_drift_run",
                    ["created_at"])

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

    compver = sa.table(
        "v2_computation_version",
        sa.column("id", sa.String), sa.column("component", sa.String),
        sa.column("version", sa.String), sa.column("source_hash", sa.String),
        sa.column("evidence_ref", sa.String),
        sa.column("registered_at", sa.DateTime(timezone=True)),
    )
    op.execute(compver.insert().values(
        id=str(uuid4()), component="paper_bridge_engine",
        version="pbr-1.0.0", source_hash=_rolling_hash(_PBR_FILES),
        evidence_ref="BO-V2-BE-11-001", registered_at=now,
    ))

    # Seed slots: ZERO rows landed - EMPTY-FORCED is the shipped state.

    _create_triggers(bind)
    _verify_triggers_present(bind)


def _verify_triggers_present(bind) -> None:
    names = tuple(t[0] for t in _TRIGGERS)
    placeholders = ",".join(f"'{n}'" for n in names)
    if bind.dialect.name == "sqlite":
        count = bind.execute(sa.text(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'"
            f" AND name IN ({placeholders})")).scalar_one()
    elif bind.dialect.name == "postgresql":
        count = bind.execute(sa.text(
            f"SELECT COUNT(*) FROM pg_trigger WHERE tgname IN ({placeholders})"
        )).scalar_one()
    else:  # pragma: no cover
        return
    if int(count) != len(names):
        raise RuntimeError(
            "BE-11 0051: guard triggers NOT present - manual recovery"
            " required; do not treat this migration as applied")


def downgrade() -> None:
    bind = op.get_bind()
    _drop_triggers(bind)
    for _role, permission, _sal in _PERMISSIONS:
        op.execute(sa.text(
            "DELETE FROM v2_permission WHERE permission = :p"
        ).bindparams(p=permission))
    _drop_compver_delete_guard(bind)
    op.execute(sa.text(
        "DELETE FROM v2_computation_version"
        " WHERE component = :c AND version = :v"
    ).bindparams(c="paper_bridge_engine", v="pbr-1.0.0"))
    _recreate_compver_delete_guard(bind)
    op.drop_index("ix_v2_pbdrift_created",
                  table_name="v2_paper_bridge_drift_run")
    op.drop_table("v2_paper_bridge_drift_run")
