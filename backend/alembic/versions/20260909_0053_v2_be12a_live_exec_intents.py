"""V2 BE-12A — live_exec intents chapter (BO-V2-BE12A-001 §1.g; AMEND-0053).

+1 table `v2_live_exec_intent` (zero-UPDATE regime; guard-pair triggers
=> census 78->80); +3 permission seeds under the AM-1 exemption family
`v2.live_exec.*` (69->72; writes SAL-4, reads SAL-2); NO compver row
this act (12A carries no engine compver by order); NO exception-table
entries. Exactly ONE upgrade line. Census re-tattoo law: counts
re-enumerated fresh per sub-BO — post-apply tattoo 80/72/13.

Execution authority: NONE. This migration creates a LEDGER for
capability-posture intents; no submission surface exists anywhere in
the 12A chapter (12B scope).
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

import sqlalchemy as sa

from alembic import op

revision = "20260909_0053"
down_revision = "20260909_0052"
branch_labels = None
depends_on = None

_TRIGGERS = (
    ("v2_live_exec_intent_immutable_update",
     "v2_live_exec_intent",
     "UPDATE", "V2 live exec intents are immutable; UPDATE prohibited"),
    ("v2_live_exec_intent_immutable_delete",
     "v2_live_exec_intent",
     "DELETE", "V2 live exec intents are immutable; DELETE prohibited"),
)

_PERMISSIONS = (
    ("admin", "v2.live_exec.intent.write", "SAL-4"),
    ("admin", "v2.live_exec.evaluate.write", "SAL-4"),
    ("admin", "v2.live_exec.intents.read", "SAL-2"),
)


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
        op.execute("""
            CREATE OR REPLACE FUNCTION prevent_v2_live_exec_mutation()
            RETURNS trigger AS $$
            BEGIN
                RAISE EXCEPTION
                    'V2 live-exec artifact is immutable; % prohibited on %',
                    TG_OP, TG_TABLE_NAME;
            END;
            $$ LANGUAGE plpgsql;
        """)
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
        op.execute(
            "DROP FUNCTION IF EXISTS prevent_v2_live_exec_mutation()")


def upgrade() -> None:
    bind = op.get_bind()
    now = datetime.now(timezone.utc)

    op.create_table(
        "v2_live_exec_intent",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("idempotency_key", sa.String(128), nullable=False),
        sa.Column("requested_basis_id", sa.String(64), nullable=False),
        sa.Column("posture", sa.String(16), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("digest", sa.String(64), nullable=False),
        sa.Column("record_state", sa.String(16), nullable=False),
        sa.Column("step_up_ref", sa.String(128), nullable=True),
        sa.Column("actor_id", sa.String(128), nullable=False),
        sa.Column("data_class", sa.String(32), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("record_state IN ('registered')",
                           name="ck_v2_lxintent_state"),
        sa.CheckConstraint("data_class IN ('simulated')",
                           name="ck_v2_lxintent_data_class"),
        sa.CheckConstraint(
            "posture IN ('capability','practice','activation')",
            name="ck_v2_lxintent_posture"),
    )
    op.create_index("ix_v2_lxintent_created", "v2_live_exec_intent",
                    ["created_at"])
    op.create_index("uq_v2_lxintent_idem", "v2_live_exec_intent",
                    ["idempotency_key"], unique=True)

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
    # NO compver row (BO SS1.g); NO exception-table entries.


def downgrade() -> None:
    bind = op.get_bind()
    _drop_triggers(bind)
    for _role, permission, _sal in _PERMISSIONS:
        op.execute(sa.text(
            "DELETE FROM v2_permission WHERE permission = :p"
        ).bindparams(p=permission))
    op.drop_index("uq_v2_lxintent_idem", table_name="v2_live_exec_intent")
    op.drop_index("ix_v2_lxintent_created", table_name="v2_live_exec_intent")
    op.drop_table("v2_live_exec_intent")
