"""V2 BE-12E — reconciliation + incident (BO-V2-BE12E-001 §1.g; FINAL BAND).

+2 tables (`v2_live_exec_reconciliation`, `v2_live_exec_incident`) with
guard pairs (+4 triggers => census 90->94); indexes (disclosed:
`ix_v2_lxrecon_created`, `ix_v2_lxinc_created` — created_at functional
indexes only; uuid surrogate pks); closed CHECKs per §c.5/§d.1;
+5 permission seeds (83->88: reconcile.run SAL-4, reconcile.read SAL-2,
incident.open SAL-4, incident.close SAL-4, incident.read SAL-2);
+1 compver row INSERT-ONLY `live_exec_engine|lxe-1.3.0` over the
EXPANDED set (the 13 12D-set files — ALL BYTE-UNMOVED, disk re-proof
law stands — + the five 12E files: reconcile/{__init__,money,engine}.py
+ incident/{__init__,engine}.py; C-2 disclosure in the DR). Append-only
registry law: lxe-1.0.0/1.1.0/1.2.0 STAND AND STILL DISK-RE-PROVE; the
registry's last row names the last build's order (BO-V2-BE12E-001) —
the "compver rows with last build" carry item closes here. ONE upgrade
line; census re-tattoo 94/88/17; downgrade exact (restores 90/83/16;
delete-guard dance; all three prior rows preserved). Drift: ITEMIZED
(E-0054-A11.4). CHECK pins in cards carry RENDERED form (E-0055-A10.3).

ZERO seed rows in either table: evidence ledgers are born empty; the
first row of each arrives only by an operator-initiated verb.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import sqlalchemy as sa

from alembic import op

revision = "20260909_0057"
down_revision = "20260909_0056"
branch_labels = None
depends_on = None

_TRIGGERS = (
    ("v2_live_exec_reconciliation_immutable_update",
     "v2_live_exec_reconciliation",
     "UPDATE", "V2 live exec reconciliation is immutable; UPDATE prohibited"),
    ("v2_live_exec_reconciliation_immutable_delete",
     "v2_live_exec_reconciliation",
     "DELETE", "V2 live exec reconciliation is immutable; DELETE prohibited"),
    ("v2_live_exec_incident_immutable_update",
     "v2_live_exec_incident",
     "UPDATE", "V2 live exec incidents are immutable; UPDATE prohibited"),
    ("v2_live_exec_incident_immutable_delete",
     "v2_live_exec_incident",
     "DELETE", "V2 live exec incidents are immutable; DELETE prohibited"),
)

_PERMISSIONS = (
    ("admin", "v2.live_exec.reconcile.run", "SAL-4"),
    ("admin", "v2.live_exec.reconcile.read", "SAL-2"),
    ("admin", "v2.live_exec.incident.open", "SAL-4"),
    ("admin", "v2.live_exec.incident.close", "SAL-4"),
    ("admin", "v2.live_exec.incident.read", "SAL-2"),
)

# The EXPANDED lxe set (BO SS1.g; C-2 disclosure in the DR).
_LXE_FILES_1_3 = (
    "app/v2/live_exec/intents.py",
    "app/v2/live_exec/eligibility.py",
    "app/v2/live_exec/risk.py",
    "app/v2/live_exec/locks.py",
    "app/v2/live_exec/submissions.py",
    "app/v2/live_exec/ack_fills.py",
    "app/v2/live_exec/modify/__init__.py",
    "app/v2/live_exec/modify/engine.py",
    "app/v2/live_exec/activation/__init__.py",
    "app/v2/live_exec/activation/engine.py",
    "app/v2/live_exec/activation/template.py",
    "app/v2/live_exec/killswitch/__init__.py",
    "app/v2/live_exec/killswitch/engine.py",
    "app/v2/live_exec/reconcile/__init__.py",
    "app/v2/live_exec/reconcile/money.py",
    "app/v2/live_exec/reconcile/engine.py",
    "app/v2/live_exec/incident/__init__.py",
    "app/v2/live_exec/incident/engine.py",
)


def _rolling_hash(files: tuple[str, ...]) -> str:
    base = Path(__file__).resolve().parents[2]
    digest = hashlib.sha256()
    for ref in files:
        digest.update(ref.encode("utf-8"))
        digest.update(b"\x00")
        digest.update((base / ref).read_bytes())
        digest.update(b"\x00")
    return digest.hexdigest()


def _drop_compver_delete_guard(bind) -> None:
    if bind.dialect.name == "sqlite":
        op.execute("DROP TRIGGER IF EXISTS"
                   " v2_computation_version_immutable_delete")


def _recreate_compver_delete_guard(bind) -> None:
    if bind.dialect.name == "sqlite":
        op.execute("""
            CREATE TRIGGER v2_computation_version_immutable_delete
            BEFORE DELETE ON v2_computation_version
            BEGIN
                SELECT RAISE(ABORT,
                    'V2 computation versions are immutable; DELETE prohibited');
            END;
        """)
        restored = bind.execute(sa.text(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'"
            " AND name = 'v2_computation_version_immutable_delete'"
        )).scalar()
        if restored != 1:
            raise RuntimeError(
                "compver delete guard NOT restored - manual recovery required")


def _make_triggers(bind) -> None:
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
        for name, table, event, _message in _TRIGGERS:
            op.execute(f"""
                CREATE TRIGGER {name}
                BEFORE {event} ON {table}
                FOR EACH ROW EXECUTE FUNCTION
                    prevent_v2_live_exec_mutation();
            """)


def _drop_triggers(bind) -> None:
    if bind.dialect.name == "sqlite":
        for name, _t, _e, _m in _TRIGGERS:
            op.execute(f"DROP TRIGGER IF EXISTS {name}")
    elif bind.dialect.name == "postgresql":
        for name, table, _e, _m in _TRIGGERS:
            op.execute(f"DROP TRIGGER IF EXISTS {name} ON {table}")


def upgrade() -> None:
    bind = op.get_bind()
    now = datetime.now(timezone.utc)

    op.create_table(
        "v2_live_exec_reconciliation",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("scope", sa.JSON(), nullable=False),
        sa.Column("outcome", sa.String(16), nullable=False),
        sa.Column("drift_facts", sa.JSON(), nullable=True),
        sa.Column("digest", sa.String(64), nullable=False),
        sa.Column("actor_id", sa.String(128), nullable=False),
        sa.Column("data_class", sa.String(32), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("outcome IN ('clean','parity_break')",
                           name="ck_v2_lxrecon_outcome"),
        sa.CheckConstraint("data_class IN ('evidence')",
                           name="ck_v2_lxrecon_data_class"),
    )
    op.create_index("ix_v2_lxrecon_created", "v2_live_exec_reconciliation",
                    ["created_at"])

    op.create_table(
        "v2_live_exec_incident",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("opened_by", sa.String(128), nullable=False),
        sa.Column("severity", sa.String(8), nullable=False),
        sa.Column("instruments_pinned", sa.JSON(), nullable=False),
        sa.Column("recovery_path", sa.Text(), nullable=False),
        sa.Column("status", sa.String(8), nullable=False),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("closed_by", sa.String(128), nullable=True),
        sa.Column("digest", sa.String(64), nullable=False),
        sa.Column("step_up_ref", sa.String(128), nullable=True),
        sa.Column("actor_id", sa.String(128), nullable=False),
        sa.Column("data_class", sa.String(32), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "severity IN ('SEV-1','SEV-2','SEV-3','SEV-4')",
            name="ck_v2_lxinc_severity"),
        sa.CheckConstraint("status IN ('open','closed')",
                           name="ck_v2_lxinc_status"),
        sa.CheckConstraint("data_class IN ('evidence')",
                           name="ck_v2_lxinc_data_class"),
    )
    op.create_index("ix_v2_lxinc_created", "v2_live_exec_incident",
                    ["created_at"])

    _make_triggers(bind)

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

    # lxe-1.3.0: INSERT-ONLY (append-only registry; the last row names
    # the last build's order — the carry item closes here).
    compver = sa.table(
        "v2_computation_version",
        sa.column("id", sa.String), sa.column("component", sa.String),
        sa.column("version", sa.String), sa.column("source_hash", sa.String),
        sa.column("evidence_ref", sa.String),
        sa.column("registered_at", sa.DateTime(timezone=True)),
    )
    present = bind.execute(sa.text(
        "SELECT COUNT(*) FROM v2_computation_version"
        " WHERE component = 'live_exec_engine'"
        " AND version = 'lxe-1.3.0'")).scalar()
    if present == 0:
        op.execute(compver.insert().values(
            id=str(uuid4()), component="live_exec_engine",
            version="lxe-1.3.0",
            source_hash=_rolling_hash(_LXE_FILES_1_3),
            evidence_ref="BO-V2-BE12E-001", registered_at=now))

    # ZERO seed rows in either table (evidence ledgers are born empty).


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
    ).bindparams(c="live_exec_engine", v="lxe-1.3.0"))
    count = bind.execute(sa.text(
        "SELECT COUNT(*) FROM v2_computation_version"
        " WHERE component = :c AND version = :v"
    ).bindparams(c="live_exec_engine", v="lxe-1.3.0")).scalar()
    if count != 0:
        raise RuntimeError("lxe-1.3.0 compver row not removed cleanly")
    _recreate_compver_delete_guard(bind)
    op.drop_index("ix_v2_lxinc_created", table_name="v2_live_exec_incident")
    op.drop_table("v2_live_exec_incident")
    op.drop_index("ix_v2_lxrecon_created",
                  table_name="v2_live_exec_reconciliation")
    op.drop_table("v2_live_exec_reconciliation")
