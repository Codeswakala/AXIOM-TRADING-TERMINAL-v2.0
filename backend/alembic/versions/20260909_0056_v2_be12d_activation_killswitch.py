"""V2 BE-12D — activation instrument + kill-switch (BO-V2-BE12D-001 §1.g).

+2 tables (`v2_live_activation_instrument`, `v2_live_kill_switch`) with
guard pairs (+4 triggers => census 86->90) + singleton/discriminator
indexes + closed CHECKs; +6 permission seeds (77->83: killswitch
arm/pull/clear SAL-4, killswitch read SAL-2, activation read SAL-2,
activation template read SAL-3); +1 compver row INSERT-ONLY
`live_exec_engine|lxe-1.2.0` over the EXPANDED set (the eight 12C-set
files + activation/{__init__,engine,template}.py +
killswitch/{__init__,engine}.py — template.py rides the hash so the
instrument artifact is compver-scoped; C-2 disclosure in the DR).
Append-only registry law: lxe-1.0.0 AND lxe-1.1.0 STAND. ONE upgrade
line; census re-tattoo 90/83/16; downgrade exact (restores 86/77/15;
delete-guard dance; both prior rows preserved). Drift: ITEMIZED law
(E-0054-A11.4). CHECK-name pins carry the RENDERED form per
E-0055-A10.3.

ZERO seed rows in either new table: the activation instrument's
zero-row state IS the L3 lock; the kill-switch's zero-row state is the
intact resting posture. Nothing arms at migration.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import sqlalchemy as sa

from alembic import op

revision = "20260909_0056"
down_revision = "20260909_0055"
branch_labels = None
depends_on = None

_TRIGGERS = (
    ("v2_live_activation_instrument_immutable_update",
     "v2_live_activation_instrument",
     "UPDATE", "V2 live activation instrument is immutable; UPDATE prohibited"),
    ("v2_live_activation_instrument_immutable_delete",
     "v2_live_activation_instrument",
     "DELETE", "V2 live activation instrument is immutable; DELETE prohibited"),
    ("v2_live_kill_switch_immutable_update",
     "v2_live_kill_switch",
     "UPDATE", "V2 live kill switch is immutable; UPDATE prohibited"),
    ("v2_live_kill_switch_immutable_delete",
     "v2_live_kill_switch",
     "DELETE", "V2 live kill switch is immutable; DELETE prohibited"),
)

_PERMISSIONS = (
    ("admin", "v2.live_exec.killswitch.arm", "SAL-4"),
    ("admin", "v2.live_exec.killswitch.pull", "SAL-4"),
    ("admin", "v2.live_exec.killswitch.clear", "SAL-4"),
    ("admin", "v2.live_exec.killswitch.read", "SAL-2"),
    ("admin", "v2.live_exec.activation.read", "SAL-2"),
    ("admin", "v2.live_exec.activation.template.read", "SAL-3"),
)

# The EXPANDED lxe set (BO SS1.g; C-2 disclosure in the DR).
_LXE_FILES_1_2 = (
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
        "v2_live_activation_instrument",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("sole", sa.String(4), nullable=False),
        sa.Column("version", sa.String(16), nullable=False),
        sa.Column("template_hash", sa.String(64), nullable=False),
        sa.Column("funded_posture_ref", sa.String(128), nullable=False),
        sa.Column("step_up_ref", sa.String(128), nullable=False),
        sa.Column("operator_ref", sa.String(128), nullable=False),
        sa.Column("correlation_ref", sa.String(64), nullable=True),
        sa.Column("actor_id", sa.String(128), nullable=False),
        sa.Column("data_class", sa.String(32), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("sole IN ('SOLE')", name="ck_v2_lai_sole"),
        sa.CheckConstraint("version IN ('lai-1.0.0')",
                           name="ck_v2_lai_version"),
        sa.CheckConstraint("data_class IN ('live_marker')",
                           name="ck_v2_lai_data_class"),
    )
    op.create_index("uq_v2_lai_sole", "v2_live_activation_instrument",
                    ["sole"], unique=True)

    op.create_table(
        "v2_live_kill_switch",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("sole", sa.String(4), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("step_up_ref", sa.String(128), nullable=False),
        sa.Column("actor_id", sa.String(128), nullable=False),
        sa.Column("data_class", sa.String(32), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("sole IN ('SOLE')", name="ck_v2_lks_sole"),
        sa.CheckConstraint("status IN ('armed','pulled','cleared')",
                           name="ck_v2_lks_status"),
        sa.CheckConstraint("data_class IN ('evidence')",
                           name="ck_v2_lks_data_class"),
    )
    op.create_index("uq_v2_lks_sole", "v2_live_kill_switch",
                    ["sole"], unique=True)

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

    # lxe-1.2.0: INSERT-ONLY (append-only registry law).
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
        " AND version = 'lxe-1.2.0'")).scalar()
    if present == 0:
        op.execute(compver.insert().values(
            id=str(uuid4()), component="live_exec_engine",
            version="lxe-1.2.0",
            source_hash=_rolling_hash(_LXE_FILES_1_2),
            evidence_ref="BO-V2-BE12D-001", registered_at=now))

    # ZERO seed rows in either new table (zero-row IS the law).


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
    ).bindparams(c="live_exec_engine", v="lxe-1.2.0"))
    count = bind.execute(sa.text(
        "SELECT COUNT(*) FROM v2_computation_version"
        " WHERE component = :c AND version = :v"
    ).bindparams(c="live_exec_engine", v="lxe-1.2.0")).scalar()
    if count != 0:
        raise RuntimeError("lxe-1.2.0 compver row not removed cleanly")
    _recreate_compver_delete_guard(bind)
    op.drop_index("uq_v2_lks_sole", table_name="v2_live_kill_switch")
    op.drop_table("v2_live_kill_switch")
    op.drop_index("uq_v2_lai_sole",
                  table_name="v2_live_activation_instrument")
    op.drop_table("v2_live_activation_instrument")
