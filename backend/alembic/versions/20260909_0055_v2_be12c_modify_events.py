"""V2 BE-12C — cancel/modify chapter (BO-V2-BE12C-001 §1.g; AMEND-0055).

+1 table `v2_live_exec_modify_event` + guard pair (+2 triggers =>
census 84->86); +2 permission seeds (75->77; modify write SAL-4,
modifies read SAL-2); +1 compver row INSERT-ONLY `live_exec_engine |
lxe-1.1.0` over the EXPANDED file set (the six + the two 12C modify
files; C-2 disclosure in the DR) — `lxe-1.0.0`'s row STANDS (append-
only registry law; the update path is refused by the standing guard,
coupon-witnessed). ONE upgrade line; census re-tattoo 86/77/15;
downgrade exact (restores 84/75/14 via the 0054-proven delete-guard
dance). Drift gate: ITEMIZED law per ERRATUM E-0054-A11.4 (exactly the
9 inherited V1 tokens; zero 12C tokens).
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import sqlalchemy as sa

from alembic import op

revision = "20260909_0055"
down_revision = "20260909_0054"
branch_labels = None
depends_on = None

_TRIGGERS = (
    ("v2_live_exec_modify_event_immutable_update",
     "v2_live_exec_modify_event",
     "UPDATE", "V2 live exec modify events are immutable; UPDATE prohibited"),
    ("v2_live_exec_modify_event_immutable_delete",
     "v2_live_exec_modify_event",
     "DELETE", "V2 live exec modify events are immutable; DELETE prohibited"),
)

_PERMISSIONS = (
    ("admin", "v2.live_exec.modify.write", "SAL-4"),
    ("admin", "v2.live_exec.modifies.read", "SAL-2"),
)

# The EXPANDED lxe file set (BO SS1.g; enumerated at design commit;
# C-2 disclosure carried in the delivery report).
_LXE_FILES_1_1 = (
    "app/v2/live_exec/intents.py",
    "app/v2/live_exec/eligibility.py",
    "app/v2/live_exec/risk.py",
    "app/v2/live_exec/locks.py",
    "app/v2/live_exec/submissions.py",
    "app/v2/live_exec/ack_fills.py",
    "app/v2/live_exec/modify/__init__.py",
    "app/v2/live_exec/modify/engine.py",
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
        "v2_live_exec_modify_event",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("submission_id", sa.String(36), nullable=False),
        sa.Column("intent_id", sa.String(36), nullable=False),
        sa.Column("verb", sa.String(16), nullable=False),
        sa.Column("act_identity", sa.String(128), nullable=False),
        sa.Column("request_payload", sa.JSON(), nullable=False),
        sa.Column("outcome", sa.String(24), nullable=False),
        sa.Column("raw_note", sa.String(256), nullable=True),
        sa.Column("correlation_ref", sa.String(64), nullable=True),
        sa.Column("operator_election", sa.String(24), nullable=False),
        sa.Column("actor_id", sa.String(128), nullable=False),
        sa.Column("data_class", sa.String(32), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("verb IN ('cancel','modify')",
                           name="ck_v2_lxmod_verb"),
        sa.CheckConstraint(
            "outcome IN ('applied','refused_terminal','unknown_outcome',"
            "'unknown_escalate')",
            name="ck_v2_lxmod_outcome"),
        sa.CheckConstraint(
            "operator_election IN ('standard','cancel_on_unknown')",
            name="ck_v2_lxmod_election"),
        sa.CheckConstraint("data_class IN ('simulated')",
                           name="ck_v2_lxmod_data_class"),
    )
    op.create_index("ix_v2_lxmod_created", "v2_live_exec_modify_event",
                    ["created_at"])
    op.create_index("uq_v2_lxmod_identity", "v2_live_exec_modify_event",
                    ["act_identity"], unique=True)

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

    # lxe-1.1.0: INSERT-ONLY (append-only registry law; the 1.0.0 row
    # STANDS; the standing UPDATE guard refuses any update path).
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
        " AND version = 'lxe-1.1.0'")).scalar()
    if present == 0:
        op.execute(compver.insert().values(
            id=str(uuid4()), component="live_exec_engine",
            version="lxe-1.1.0",
            source_hash=_rolling_hash(_LXE_FILES_1_1),
            evidence_ref="BO-V2-BE12C-001", registered_at=now))


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
    ).bindparams(c="live_exec_engine", v="lxe-1.1.0"))
    count = bind.execute(sa.text(
        "SELECT COUNT(*) FROM v2_computation_version"
        " WHERE component = :c AND version = :v"
    ).bindparams(c="live_exec_engine", v="lxe-1.1.0")).scalar()
    if count != 0:
        raise RuntimeError("lxe-1.1.0 compver row not removed cleanly")
    _recreate_compver_delete_guard(bind)
    op.drop_index("uq_v2_lxmod_identity",
                  table_name="v2_live_exec_modify_event")
    op.drop_index("ix_v2_lxmod_created",
                  table_name="v2_live_exec_modify_event")
    op.drop_table("v2_live_exec_modify_event")
