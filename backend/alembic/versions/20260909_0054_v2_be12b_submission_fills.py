"""V2 BE-12B — submission + fills chapter (BO-V2-BE12B-001 §1.g; AMEND-0054).

+2 tables (`v2_live_exec_submission`, `v2_live_exec_fill_event`) with
their guard pairs (+4 triggers => census 80->84); +3 permission seeds
under the standing AM-1 family (72->75; submit write SAL-4;
submissions/fills reads SAL-2); +1 compver row `live_exec_engine |
lxe-1.0.0` — THE 12A-DEFERRED ENGINE ROW, added exactly once here by BO
citation (13->14; rolled hash from disk at apply time). Exactly ONE
upgrade line. Census re-tattoo: post-apply 84/75/14.

Execution authority: NONE except the practice world under the sealed
practice leg, inside coupons/witnesses only. Funded account: NONE.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import sqlalchemy as sa

from alembic import op

revision = "20260909_0054"
down_revision = "20260909_0053"
branch_labels = None
depends_on = None

_TRIGGERS = (
    ("v2_live_exec_submission_immutable_update",
     "v2_live_exec_submission",
     "UPDATE", "V2 live exec submissions are immutable; UPDATE prohibited"),
    ("v2_live_exec_submission_immutable_delete",
     "v2_live_exec_submission",
     "DELETE", "V2 live exec submissions are immutable; DELETE prohibited"),
    ("v2_live_exec_fill_event_immutable_update",
     "v2_live_exec_fill_event",
     "UPDATE", "V2 live exec fill events are immutable; UPDATE prohibited"),
    ("v2_live_exec_fill_event_immutable_delete",
     "v2_live_exec_fill_event",
     "DELETE", "V2 live exec fill events are immutable; DELETE prohibited"),
)

_PERMISSIONS = (
    ("admin", "v2.live_exec.submit.write", "SAL-4"),
    ("admin", "v2.live_exec.submissions.read", "SAL-2"),
    ("admin", "v2.live_exec.fills.read", "SAL-2"),
)

# The 12A-deferred compver row lands HERE (BO-V2-BE12B-001 SS1.g).
_LXE_FILES = (
    "app/v2/live_exec/intents.py",
    "app/v2/live_exec/eligibility.py",
    "app/v2/live_exec/risk.py",
    "app/v2/live_exec/locks.py",
    "app/v2/live_exec/submissions.py",
    "app/v2/live_exec/ack_fills.py",
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
        "v2_live_exec_submission",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("intent_id", sa.String(36), nullable=False),
        sa.Column("lane", sa.String(16), nullable=False),
        sa.Column("terminal_state", sa.String(24), nullable=False),
        sa.Column("server_ack_ref", sa.String(64), nullable=True),
        sa.Column("raw_note", sa.String(256), nullable=True),
        sa.Column("order_request", sa.JSON(), nullable=False),
        sa.Column("digest", sa.String(64), nullable=False),
        sa.Column("actor_id", sa.String(128), nullable=False),
        sa.Column("data_class", sa.String(32), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "terminal_state IN ('accepted','rejected','requote',"
            "'no_answer','quarantined_unknown')",
            name="ck_v2_lxsub_terminal_state"),
        sa.CheckConstraint("lane IN ('practice')",
                           name="ck_v2_lxsub_lane"),
        sa.CheckConstraint("data_class IN ('simulated')",
                           name="ck_v2_lxsub_data_class"),
    )
    op.create_index("ix_v2_lxsub_created", "v2_live_exec_submission",
                    ["created_at"])
    op.create_index("uq_v2_lxsub_intent", "v2_live_exec_submission",
                    ["intent_id"], unique=True)

    op.create_table(
        "v2_live_exec_fill_event",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("submission_id", sa.String(36), nullable=False),
        sa.Column("fill_event_identity", sa.String(128), nullable=False),
        sa.Column("correlation_basis", sa.String(32), nullable=False),
        sa.Column("correlation_ref", sa.String(64), nullable=False),
        sa.Column("fill_payload", sa.JSON(), nullable=False),
        sa.Column("actor_id", sa.String(128), nullable=False),
        sa.Column("data_class", sa.String(32), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("data_class IN ('simulated')",
                           name="ck_v2_lxfill_data_class"),
        sa.CheckConstraint(
            "correlation_basis IN ('server_ack_ref','terminal_order_id')",
            name="ck_v2_lxfill_corr_basis"),
    )
    op.create_index("ix_v2_lxfill_created", "v2_live_exec_fill_event",
                    ["created_at"])
    op.create_index("uq_v2_lxfill_identity", "v2_live_exec_fill_event",
                    ["fill_event_identity"], unique=True)

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

    # The 12A-deferred compver row, exactly once (existing-set filter).
    compver = sa.table(
        "v2_computation_version",
        sa.column("id", sa.String), sa.column("component", sa.String),
        sa.column("version", sa.String), sa.column("source_hash", sa.String),
        sa.column("evidence_ref", sa.String),
        sa.column("registered_at", sa.DateTime(timezone=True)),
    )
    present = bind.execute(sa.text(
        "SELECT COUNT(*) FROM v2_computation_version"
        " WHERE component = 'live_exec_engine'")).scalar()
    if present == 0:
        op.execute(compver.insert().values(
            id=str(uuid4()), component="live_exec_engine",
            version="lxe-1.0.0", source_hash=_rolling_hash(_LXE_FILES),
            evidence_ref="BO-V2-BE12B-001", registered_at=now))


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
    ).bindparams(c="live_exec_engine", v="lxe-1.0.0"))
    count = bind.execute(sa.text(
        "SELECT COUNT(*) FROM v2_computation_version"
        " WHERE component = :c").bindparams(c="live_exec_engine")).scalar()
    if count != 0:
        raise RuntimeError("compver row not removed cleanly")
    _recreate_compver_delete_guard(bind)
    op.drop_index("uq_v2_lxfill_identity", table_name="v2_live_exec_fill_event")
    op.drop_index("ix_v2_lxfill_created", table_name="v2_live_exec_fill_event")
    op.drop_table("v2_live_exec_fill_event")
    op.drop_index("uq_v2_lxsub_intent", table_name="v2_live_exec_submission")
    op.drop_index("ix_v2_lxsub_created", table_name="v2_live_exec_submission")
    op.drop_table("v2_live_exec_submission")
