"""V2 BE-8 — paper trading (BO-V2-BE-8-001 D-4; design S1/S10).

Eight tables, ALL guarded (zero-UPDATE regime): 16 triggers (42->58);
8 permission rows (49->57; D-1 scoped-exemption vocabulary); 2 compver
seeds (8->10: paper_execution_simulator=pxs-1.0.0 over {simulator,
ledger}.py, paper_risk_gateway=prg-1.0.0 over {risk,contracts}.py —
rolling-hash recipe identical to 0047; RPE/RJE untouched, append-only
law). Symmetric content-based downgrade.

Revision ID: 20260904_0048
Revises: 20260903_0047
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import sqlalchemy as sa

from alembic import op

revision = "20260904_0048"
down_revision = "20260903_0047"
branch_labels = None
depends_on = None

_TRIGGERS = (
    ("v2_paper_account_immutable_update", "v2_paper_account",
     "UPDATE", "V2 paper accounts are immutable; UPDATE prohibited"),
    ("v2_paper_account_immutable_delete", "v2_paper_account",
     "DELETE", "V2 paper accounts are immutable; DELETE prohibited"),
    ("v2_paper_order_intent_immutable_update", "v2_paper_order_intent",
     "UPDATE", "V2 paper order intents are immutable; UPDATE prohibited"),
    ("v2_paper_order_intent_immutable_delete", "v2_paper_order_intent",
     "DELETE", "V2 paper order intents are immutable; DELETE prohibited"),
    ("v2_paper_risk_decision_immutable_update", "v2_paper_risk_decision",
     "UPDATE", "V2 paper risk decisions are immutable; UPDATE prohibited"),
    ("v2_paper_risk_decision_immutable_delete", "v2_paper_risk_decision",
     "DELETE", "V2 paper risk decisions are immutable; DELETE prohibited"),
    ("v2_paper_order_event_immutable_update", "v2_paper_order_event",
     "UPDATE", "V2 paper order events are immutable; UPDATE prohibited"),
    ("v2_paper_order_event_immutable_delete", "v2_paper_order_event",
     "DELETE", "V2 paper order events are immutable; DELETE prohibited"),
    ("v2_paper_fill_immutable_update", "v2_paper_fill",
     "UPDATE", "V2 paper fills are immutable; UPDATE prohibited"),
    ("v2_paper_fill_immutable_delete", "v2_paper_fill",
     "DELETE", "V2 paper fills are immutable; DELETE prohibited"),
    ("v2_paper_position_snapshot_immutable_update",
     "v2_paper_position_snapshot",
     "UPDATE", "V2 paper position snapshots are immutable; UPDATE prohibited"),
    ("v2_paper_position_snapshot_immutable_delete",
     "v2_paper_position_snapshot",
     "DELETE", "V2 paper position snapshots are immutable; DELETE prohibited"),
    ("v2_paper_balance_snapshot_immutable_update",
     "v2_paper_balance_snapshot",
     "UPDATE", "V2 paper balance snapshots are immutable; UPDATE prohibited"),
    ("v2_paper_balance_snapshot_immutable_delete",
     "v2_paper_balance_snapshot",
     "DELETE", "V2 paper balance snapshots are immutable; DELETE prohibited"),
    ("v2_paper_reconciliation_immutable_update", "v2_paper_reconciliation",
     "UPDATE", "V2 paper reconciliations are immutable; UPDATE prohibited"),
    ("v2_paper_reconciliation_immutable_delete", "v2_paper_reconciliation",
     "DELETE", "V2 paper reconciliations are immutable; DELETE prohibited"),
)

_PERMISSIONS = (
    ("admin", "v2.paper.accounts.read", "SAL-2"),
    ("admin", "v2.paper.accounts.manage", "SAL-3"),
    ("admin", "v2.paper.orders.read", "SAL-2"),
    ("admin", "v2.paper.orders.place", "SAL-3"),
    ("admin", "v2.paper.orders.cancel", "SAL-3"),
    ("admin", "v2.paper.orders.confirm", "SAL-3"),
    ("admin", "v2.paper.fills.read", "SAL-2"),
    ("admin", "v2.paper.risk.read", "SAL-2"),
)

_PXS_FILES = (
    "app/v2/paper_trading/simulator.py",
    "app/v2/paper_trading/ledger.py",
)
_PRG_FILES = (
    "app/v2/paper_trading/risk.py",
    "app/v2/paper_trading/contracts.py",
)

_DATA_CLASS_CHECK = (
    "data_class IN ('synthetic','simulated','historical_real','live',"
    "'stale_cached','unavailable')"
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
            CREATE OR REPLACE FUNCTION prevent_v2_paper_trading_mutation()
            RETURNS trigger AS $$
            BEGIN
                RAISE EXCEPTION
                    'V2 paper-trading artifact is immutable; % prohibited on %',
                    TG_OP, TG_TABLE_NAME;
            END;
            $$ LANGUAGE plpgsql;
        """)
        for name, table, event, _message in _TRIGGERS:
            op.execute(f"""
                CREATE TRIGGER {name}
                BEFORE {event} ON {table}
                FOR EACH ROW EXECUTE FUNCTION prevent_v2_paper_trading_mutation();
            """)


def _drop_triggers(bind) -> None:
    if bind.dialect.name == "sqlite":
        for name, _t, _e, _m in _TRIGGERS:
            op.execute(f"DROP TRIGGER IF EXISTS {name}")
    elif bind.dialect.name == "postgresql":
        for name, table, _e, _m in _TRIGGERS:
            op.execute(f"DROP TRIGGER IF EXISTS {name} ON {table}")
        op.execute(
            "DROP FUNCTION IF EXISTS prevent_v2_paper_trading_mutation()")


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


def _be1_columns() -> list:
    return [
        sa.Column("data_class", sa.String(32), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    ]


def upgrade() -> None:
    bind = op.get_bind()
    now = datetime.now(timezone.utc)

    op.create_table(
        "v2_paper_account",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("account_id", sa.String(64), nullable=False),
        sa.Column("record_seq", sa.Integer(), nullable=False),
        sa.Column("supersedes", sa.String(36), nullable=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("base_currency", sa.String(8), nullable=False),
        sa.Column("initial_balance", sa.String(64), nullable=False),
        sa.Column("margin_params", sa.JSON(), nullable=False),
        sa.Column("lifecycle_state", sa.String(16), nullable=False),
        sa.Column("confirmation_ref", sa.String(64), nullable=False),
        *_be1_columns(),
        sa.UniqueConstraint("account_id", "record_seq",
                            name="uq_v2_pacct_id_seq"),
        sa.CheckConstraint("base_currency IN ('USD')",
                           name="ck_v2_pacct_ccy"),
        sa.CheckConstraint(
            "lifecycle_state IN ('active','frozen','closed')",
            name="ck_v2_pacct_state"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_pacct_data_class"),
    )
    op.create_index("ix_v2_pacct_account", "v2_paper_account",
                    ["account_id"])

    op.create_table(
        "v2_paper_order_intent",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("intent_id", sa.String(64), nullable=False, unique=True),
        sa.Column("account_id", sa.String(36), nullable=False),
        sa.Column("instrument_id", sa.String(64), nullable=False),
        sa.Column("side", sa.String(8), nullable=False),
        sa.Column("order_type", sa.String(16), nullable=False),
        sa.Column("quantity", sa.String(64), nullable=False),
        sa.Column("limit_price", sa.String(64), nullable=True),
        sa.Column("time_in_force", sa.String(16), nullable=False),
        sa.Column("idempotency_key", sa.String(64), nullable=False),
        sa.Column("snapshot_ref", sa.String(64), nullable=False),
        sa.Column("time_basis", sa.JSON(), nullable=False),
        sa.Column("confirmation_ref", sa.String(64), nullable=True),
        sa.Column("actor_id", sa.String(128), nullable=False),
        *_be1_columns(),
        sa.UniqueConstraint("account_id", "idempotency_key",
                            name="uq_v2_pintent_idem"),
        sa.CheckConstraint("side IN ('buy','sell')",
                           name="ck_v2_pintent_side"),
        sa.CheckConstraint("order_type IN ('market','limit')",
                           name="ck_v2_pintent_type"),
        sa.CheckConstraint("time_in_force IN ('replay_window')",
                           name="ck_v2_pintent_tif"),
        sa.CheckConstraint(
            "(order_type = 'limit') = (limit_price IS NOT NULL)",
            name="ck_v2_pintent_limit_iff"),
        sa.CheckConstraint("CAST(quantity AS REAL) > 0",
                           name="ck_v2_pintent_qty"),
        sa.CheckConstraint(_DATA_CLASS_CHECK,
                           name="ck_v2_pintent_data_class"),
    )
    op.create_index("ix_v2_pintent_account", "v2_paper_order_intent",
                    ["account_id"])

    op.create_table(
        "v2_paper_risk_decision",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("intent_id", sa.String(36), nullable=False),
        sa.Column("decision", sa.String(8), nullable=False),
        sa.Column("evaluated_limits", sa.JSON(), nullable=False),
        sa.Column("reasons", sa.JSON(), nullable=False),
        sa.Column("risk_config_version", sa.String(32), nullable=False),
        sa.Column("decided_at_basis", sa.JSON(), nullable=False),
        sa.Column("confirmation_ref", sa.String(64), nullable=True),
        *_be1_columns(),
        sa.UniqueConstraint("intent_id", name="uq_v2_prisk_intent"),
        sa.CheckConstraint("decision IN ('pass','block','hold')",
                           name="ck_v2_prisk_decision"),
        sa.CheckConstraint(
            "(decision = 'hold') = (confirmation_ref IS NOT NULL)",
            name="ck_v2_prisk_ref_iff"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_prisk_data_class"),
    )

    op.create_table(
        "v2_paper_order_event",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("intent_id", sa.String(36), nullable=False),
        sa.Column("event_index", sa.Integer(), nullable=False),
        sa.Column("from_state", sa.String(24), nullable=False),
        sa.Column("to_state", sa.String(24), nullable=False),
        sa.Column("event_class", sa.String(48), nullable=False),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.Column("actor_id", sa.String(128), nullable=False),
        *_be1_columns(),
        sa.UniqueConstraint("intent_id", "event_index",
                            name="uq_v2_pevent_idx"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_pevent_data_class"),
    )
    op.create_index("ix_v2_pevent_intent", "v2_paper_order_event",
                    ["intent_id"])

    op.create_table(
        "v2_paper_fill",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("fill_id", sa.String(64), nullable=False, unique=True),
        sa.Column("intent_id", sa.String(36), nullable=False),
        sa.Column("fill_index", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.String(64), nullable=False),
        sa.Column("raw_price", sa.String(64), nullable=False),
        sa.Column("effective_price", sa.String(64), nullable=False),
        sa.Column("cost_model_ref", sa.JSON(), nullable=False),
        sa.Column("fill_class", sa.String(24), nullable=False),
        sa.Column("simulator_version", sa.String(32), nullable=False),
        sa.Column("snapshot_ref", sa.String(64), nullable=False),
        sa.Column("time_basis", sa.JSON(), nullable=False),
        *_be1_columns(),
        sa.UniqueConstraint("intent_id", "fill_index",
                            name="uq_v2_pfill_idx"),
        sa.CheckConstraint("fill_class IN ('paper_simulated')",
                           name="ck_v2_pfill_class"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_pfill_data_class"),
    )
    op.create_index("ix_v2_pfill_intent", "v2_paper_fill", ["intent_id"])

    op.create_table(
        "v2_paper_position_snapshot",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("account_id", sa.String(36), nullable=False),
        sa.Column("as_of_basis", sa.JSON(), nullable=False),
        sa.Column("positions", sa.JSON(), nullable=False),
        sa.Column("derivation_inputs_hash", sa.String(64), nullable=False),
        sa.Column("engine_versions_hash", sa.String(64), nullable=False),
        *_be1_columns(),
        sa.UniqueConstraint("account_id", "derivation_inputs_hash",
                            "engine_versions_hash",
                            name="uq_v2_ppos_anchor"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_ppos_data_class"),
    )
    op.create_index("ix_v2_ppos_account", "v2_paper_position_snapshot",
                    ["account_id"])

    op.create_table(
        "v2_paper_balance_snapshot",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("account_id", sa.String(36), nullable=False),
        sa.Column("as_of_basis", sa.JSON(), nullable=False),
        sa.Column("cash", sa.String(64), nullable=False),
        sa.Column("equity", sa.String(64), nullable=False),
        sa.Column("margin_used", sa.String(64), nullable=False),
        sa.Column("margin_available", sa.String(64), nullable=False),
        sa.Column("unrealized_pnl", sa.String(64), nullable=False),
        sa.Column("realized_pnl", sa.String(64), nullable=False),
        sa.Column("derivation_inputs_hash", sa.String(64), nullable=False),
        sa.Column("engine_versions_hash", sa.String(64), nullable=False),
        *_be1_columns(),
        sa.UniqueConstraint("account_id", "derivation_inputs_hash",
                            "engine_versions_hash",
                            name="uq_v2_pbal_anchor"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_pbal_data_class"),
    )
    op.create_index("ix_v2_pbal_account", "v2_paper_balance_snapshot",
                    ["account_id"])

    op.create_table(
        "v2_paper_reconciliation",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("account_id", sa.String(36), nullable=False),
        sa.Column("run_basis", sa.JSON(), nullable=False),
        sa.Column("outcome", sa.String(16), nullable=False),
        sa.Column("discrepancies", sa.JSON(), nullable=False),
        sa.Column("inputs_hash", sa.String(64), nullable=False),
        *_be1_columns(),
        sa.CheckConstraint("outcome IN ('consistent','discrepant')",
                           name="ck_v2_precon_outcome"),
        sa.CheckConstraint(_DATA_CLASS_CHECK,
                           name="ck_v2_precon_data_class"),
    )
    op.create_index("ix_v2_precon_account", "v2_paper_reconciliation",
                    ["account_id"])

    # --- Seeds (revision-local literals; DEL-004 law) ---------------------
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
    for component, version, files in (
        ("paper_execution_simulator", "pxs-1.0.0", _PXS_FILES),
        ("paper_risk_gateway", "prg-1.0.0", _PRG_FILES),
    ):
        op.execute(compver.insert().values(
            id=str(uuid4()), component=component, version=version,
            source_hash=_rolling_hash(files), evidence_ref="BO-V2-BE-8-001",
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
            f" AND name IN ({placeholders})")).scalar_one()
    elif bind.dialect.name == "postgresql":
        count = bind.execute(sa.text(
            f"SELECT COUNT(*) FROM pg_trigger WHERE tgname IN ({placeholders})"
        )).scalar_one()
    else:  # pragma: no cover
        return
    if int(count) != len(names):
        raise RuntimeError(
            "BE-8 0048: guard triggers NOT present - manual recovery"
            " required; do not treat this migration as applied")


def downgrade() -> None:
    bind = op.get_bind()
    _drop_triggers(bind)
    for _role, permission, _sal in _PERMISSIONS:
        op.execute(sa.text(
            "DELETE FROM v2_permission WHERE permission = :p"
        ).bindparams(p=permission))
    _drop_compver_delete_guard(bind)
    for component, version in (
            ("paper_execution_simulator", "pxs-1.0.0"),
            ("paper_risk_gateway", "prg-1.0.0")):
        op.execute(sa.text(
            "DELETE FROM v2_computation_version"
            " WHERE component = :c AND version = :v"
        ).bindparams(c=component, v=version))
    _recreate_compver_delete_guard(bind)
    for index, table in (
        ("ix_v2_precon_account", "v2_paper_reconciliation"),
        ("ix_v2_pbal_account", "v2_paper_balance_snapshot"),
        ("ix_v2_ppos_account", "v2_paper_position_snapshot"),
        ("ix_v2_pfill_intent", "v2_paper_fill"),
        ("ix_v2_pevent_intent", "v2_paper_order_event"),
        ("ix_v2_pintent_account", "v2_paper_order_intent"),
        ("ix_v2_pacct_account", "v2_paper_account"),
    ):
        op.drop_index(index, table_name=table)
    for table in ("v2_paper_reconciliation", "v2_paper_balance_snapshot",
                  "v2_paper_position_snapshot", "v2_paper_fill",
                  "v2_paper_order_event", "v2_paper_risk_decision",
                  "v2_paper_order_intent", "v2_paper_account"):
        op.drop_table(table)
