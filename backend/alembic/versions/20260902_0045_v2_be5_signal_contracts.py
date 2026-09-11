"""V2 BE-5 U-3 — signal contracts (BO-V2-BE-5-001 T-6).

Tables: v2_signal_record (family CHECK exactly structural|predictive;
state CHECK exactly emitted|withheld|expired|refused) +
v2_signal_state_event (append-only). 4 guard triggers (24→28);
+1 permission (34→35); +1 compver row sge-1.0.0 co-delivered with U-4
(P-4). Symmetric downgrade.

Revision ID: 20260902_0045
Revises: 20260902_0044
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import sqlalchemy as sa

from alembic import op

revision = "20260902_0045"
down_revision = "20260902_0044"
branch_labels = None
depends_on = None

_TRIGGERS = (
    ("v2_signal_record_immutable_update", "v2_signal_record",
     "UPDATE", "V2 signal records are immutable; UPDATE prohibited"),
    ("v2_signal_record_immutable_delete", "v2_signal_record",
     "DELETE", "V2 signal records are immutable; DELETE prohibited"),
    ("v2_signal_state_event_immutable_update", "v2_signal_state_event",
     "UPDATE", "V2 signal state events are immutable; UPDATE prohibited"),
    ("v2_signal_state_event_immutable_delete", "v2_signal_state_event",
     "DELETE", "V2 signal state events are immutable; DELETE prohibited"),
)

_PERMISSIONS = (
    ("admin", "v2.research.signal.emit", "SAL-3"),
)

# P-4: signal-engine files co-delivered with this migration (U-4, PG-2).
_SGE_FILES = (
    "app/v2/research_governance/signals.py",
    "app/v2/research_governance/api.py",
)


def _sge_source_hash() -> str:
    base = Path(__file__).resolve().parents[2]
    digest = hashlib.sha256()
    for rel in _SGE_FILES:
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
            CREATE OR REPLACE FUNCTION prevent_v2_signal_mutation()
            RETURNS trigger AS $$
            BEGIN
                IF TG_TABLE_NAME = 'v2_signal_record' THEN
                    RAISE EXCEPTION
                        'V2 signal records are immutable; % prohibited', TG_OP;
                ELSE
                    RAISE EXCEPTION
                        'V2 signal state events are immutable; % prohibited', TG_OP;
                END IF;
            END;
            $$ LANGUAGE plpgsql;
        """)
        for name, table, event, _message in _TRIGGERS:
            op.execute(f"""
                CREATE TRIGGER {name}
                BEFORE {event} ON {table}
                FOR EACH ROW EXECUTE FUNCTION prevent_v2_signal_mutation();
            """)


def _drop_triggers(bind) -> None:
    if bind.dialect.name == "sqlite":
        for name, _t, _e, _m in _TRIGGERS:
            op.execute(f"DROP TRIGGER IF EXISTS {name}")
    elif bind.dialect.name == "postgresql":
        for name, table, _e, _m in _TRIGGERS:
            op.execute(f"DROP TRIGGER IF EXISTS {name} ON {table}")
        op.execute("DROP FUNCTION IF EXISTS prevent_v2_signal_mutation()")




def _drop_compver_delete_guard(bind) -> None:
    """0043's v2_computation_version delete guard blocks this revision's
    own seed-row removal on downgrade. Established pattern (0041/0042):
    drop -> mutate -> recreate -> verify. UPDATE guard stays in place."""
    if bind.dialect.name == "sqlite":
        op.execute("DROP TRIGGER IF EXISTS v2_computation_version_immutable_delete")
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
        "v2_signal_record",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("family", sa.String(16), nullable=False),
        sa.Column("signal_type", sa.String(64), nullable=False),
        sa.Column("instrument_id", sa.String(96), nullable=False),
        sa.Column("timeframe", sa.String(16), nullable=False),
        sa.Column("state", sa.String(16), nullable=False),
        sa.Column("state_reason", sa.JSON(), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.Column("uncertainty", sa.JSON(), nullable=False),
        sa.Column("limitations", sa.JSON(), nullable=False),
        sa.Column("source_family_refs", sa.JSON(), nullable=False),
        sa.Column("governance_record_id", sa.String(36), nullable=True),
        sa.Column("data_class", sa.String(32), nullable=False),
        sa.Column("as_of", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("family IN ('structural','predictive')",
                           name="ck_v2_signal_family"),
        sa.CheckConstraint(
            "state IN ('emitted','withheld','expired','refused')",
            name="ck_v2_signal_state"),
        sa.CheckConstraint(
            "data_class IN ('synthetic','simulated','historical_real','live',"
            "'stale_cached','unavailable')",
            name="ck_v2_signal_data_class"),
    )
    op.create_index("ix_v2_signal_instrument", "v2_signal_record",
                    ["instrument_id"])
    op.create_index("ix_v2_signal_family_state", "v2_signal_record",
                    ["family", "state"])

    op.create_table(
        "v2_signal_state_event",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("signal_record_id", sa.String(36), nullable=False),
        sa.Column("event_type", sa.String(16), nullable=False),
        sa.Column("from_state", sa.String(16), nullable=False),
        sa.Column("to_state", sa.String(16), nullable=False),
        sa.Column("reason", sa.JSON(), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("actor_id", sa.String(128), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "event_type IN ('emitted','withheld','refused','expired')",
            name="ck_v2_sigev_type"),
    )
    op.create_index("ix_v2_sigev_signal", "v2_signal_state_event",
                    ["signal_record_id"])

    permission_table = sa.table(
        "v2_permission",
        sa.column("id", sa.String), sa.column("role", sa.String),
        sa.column("permission", sa.String), sa.column("sal", sa.String),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    existing = {
        (row[0], row[1])
        for row in bind.execute(sa.text("SELECT role, permission FROM v2_permission"))
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
        id=str(uuid4()), component="signal_engine", version="sge-1.0.0",
        source_hash=_sge_source_hash(), evidence_ref="BO-V2-BE-5-001",
        registered_at=now,
    ))

    _create_triggers(bind)
    _verify_triggers_present(bind)


def _verify_triggers_present(bind) -> None:
    names = tuple(t[0] for t in _TRIGGERS)
    placeholders = ",".join(f"'{n}'" for n in names)
    if bind.dialect.name == "sqlite":
        count = bind.execute(sa.text(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'"
            f" AND name IN ({placeholders})"
        )).scalar_one()
    elif bind.dialect.name == "postgresql":
        count = bind.execute(sa.text(
            f"SELECT COUNT(*) FROM pg_trigger WHERE tgname IN ({placeholders})"
        )).scalar_one()
    else:  # pragma: no cover
        return
    if int(count) != len(names):
        raise RuntimeError(
            "BE-5 0045: signal guard triggers NOT present — manual recovery"
            " required; do not treat this migration as applied"
        )


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
        " WHERE component = 'signal_engine' AND version = 'sge-1.0.0'"
    ))
    _recreate_compver_delete_guard(bind)
    op.drop_index("ix_v2_sigev_signal", table_name="v2_signal_state_event")
    op.drop_table("v2_signal_state_event")
    op.drop_index("ix_v2_signal_family_state", table_name="v2_signal_record")
    op.drop_index("ix_v2_signal_instrument", table_name="v2_signal_record")
    op.drop_table("v2_signal_record")
