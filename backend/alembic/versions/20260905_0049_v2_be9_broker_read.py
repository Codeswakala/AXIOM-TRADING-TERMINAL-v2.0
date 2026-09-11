"""V2 BE-9 — broker read (BO-V2-BE-9-001 D-4; design S3/S10).

Nine tables, ALL guarded (zero-UPDATE regime): 18 triggers (58->76);
7 permission rows (57->64); 1 compver seed (10->11:
broker_read_engine=bre-1.0.0 over {providers/exness_mt5,sync,
reconcile}.py — the adapter/sync/reconcile set per design S3, rolling-
hash recipe identical to 0047/0048). Symmetric content-based downgrade.

Revision ID: 20260905_0049
Revises: 20260904_0048
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import sqlalchemy as sa

from alembic import op

revision = "20260905_0049"
down_revision = "20260904_0048"
branch_labels = None
depends_on = None

_TRIGGERS = (
    ("v2_broker_account_immutable_update", "v2_broker_account",
     "UPDATE", "V2 broker accounts are immutable; UPDATE prohibited"),
    ("v2_broker_account_immutable_delete", "v2_broker_account",
     "DELETE", "V2 broker accounts are immutable; DELETE prohibited"),
    ("v2_broker_balance_immutable_update", "v2_broker_balance",
     "UPDATE", "V2 broker balances are immutable; UPDATE prohibited"),
    ("v2_broker_balance_immutable_delete", "v2_broker_balance",
     "DELETE", "V2 broker balances are immutable; DELETE prohibited"),
    ("v2_broker_position_immutable_update", "v2_broker_position",
     "UPDATE", "V2 broker positions are immutable; UPDATE prohibited"),
    ("v2_broker_position_immutable_delete", "v2_broker_position",
     "DELETE", "V2 broker positions are immutable; DELETE prohibited"),
    ("v2_broker_order_immutable_update", "v2_broker_order",
     "UPDATE", "V2 broker orders are immutable; UPDATE prohibited"),
    ("v2_broker_order_immutable_delete", "v2_broker_order",
     "DELETE", "V2 broker orders are immutable; DELETE prohibited"),
    ("v2_broker_fill_immutable_update", "v2_broker_fill",
     "UPDATE", "V2 broker fills are immutable; UPDATE prohibited"),
    ("v2_broker_fill_immutable_delete", "v2_broker_fill",
     "DELETE", "V2 broker fills are immutable; DELETE prohibited"),
    ("v2_broker_instrument_permission_immutable_update",
     "v2_broker_instrument_permission",
     "UPDATE",
     "V2 broker instrument permissions are immutable; UPDATE prohibited"),
    ("v2_broker_instrument_permission_immutable_delete",
     "v2_broker_instrument_permission",
     "DELETE",
     "V2 broker instrument permissions are immutable; DELETE prohibited"),
    ("v2_broker_sync_run_immutable_update", "v2_broker_sync_run",
     "UPDATE", "V2 broker sync runs are immutable; UPDATE prohibited"),
    ("v2_broker_sync_run_immutable_delete", "v2_broker_sync_run",
     "DELETE", "V2 broker sync runs are immutable; DELETE prohibited"),
    ("v2_broker_reconcile_run_immutable_update", "v2_broker_reconcile_run",
     "UPDATE", "V2 broker reconcile runs are immutable; UPDATE prohibited"),
    ("v2_broker_reconcile_run_immutable_delete", "v2_broker_reconcile_run",
     "DELETE", "V2 broker reconcile runs are immutable; DELETE prohibited"),
    ("v2_broker_discrepancy_immutable_update", "v2_broker_discrepancy",
     "UPDATE", "V2 broker discrepancies are immutable; UPDATE prohibited"),
    ("v2_broker_discrepancy_immutable_delete", "v2_broker_discrepancy",
     "DELETE", "V2 broker discrepancies are immutable; DELETE prohibited"),
)

_PERMISSIONS = (
    ("admin", "v2.broker.accounts.read", "SAL-2"),
    ("admin", "v2.broker.balances.read", "SAL-2"),
    ("admin", "v2.broker.positions.read", "SAL-2"),
    ("admin", "v2.broker.orders_fills.read", "SAL-2"),
    ("admin", "v2.broker.sync.run", "SAL-3"),
    ("admin", "v2.broker.discrepancy.manage", "SAL-3"),
    ("admin", "v2.broker.vault.manage", "SAL-4"),
)

_BRE_FILES = (
    "app/v2/broker_read/providers/exness_mt5.py",
    "app/v2/broker_read/sync.py",
    "app/v2/broker_read/reconcile.py",
)

_DATA_CLASS_CHECK = "data_class IN ('simulated')"


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
            CREATE OR REPLACE FUNCTION prevent_v2_broker_read_mutation()
            RETURNS trigger AS $$
            BEGIN
                RAISE EXCEPTION
                    'V2 broker-read artifact is immutable; % prohibited on %',
                    TG_OP, TG_TABLE_NAME;
            END;
            $$ LANGUAGE plpgsql;
        """)
        for name, table, event, _message in _TRIGGERS:
            op.execute(f"""
                CREATE TRIGGER {name}
                BEFORE {event} ON {table}
                FOR EACH ROW EXECUTE FUNCTION prevent_v2_broker_read_mutation();
            """)


def _drop_triggers(bind) -> None:
    if bind.dialect.name == "sqlite":
        for name, _t, _e, _m in _TRIGGERS:
            op.execute(f"DROP TRIGGER IF EXISTS {name}")
    elif bind.dialect.name == "postgresql":
        for name, table, _e, _m in _TRIGGERS:
            op.execute(f"DROP TRIGGER IF EXISTS {name} ON {table}")
        op.execute(
            "DROP FUNCTION IF EXISTS prevent_v2_broker_read_mutation()")


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


def _regime_columns() -> list:
    return [
        sa.Column("data_class", sa.String(32), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    ]


def _provenance_columns() -> list:
    return [
        sa.Column("sync_run_id", sa.String(36), nullable=False),
        sa.Column("server_hostname", sa.String(128), nullable=False),
        sa.Column("fetched_at_basis", sa.String(64), nullable=False),
    ]


def upgrade() -> None:
    bind = op.get_bind()
    now = datetime.now(timezone.utc)

    op.create_table(
        "v2_broker_account",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("provider_id", sa.String(64), nullable=False),
        sa.Column("broker_account_ext_id", sa.String(64), nullable=False),
        sa.Column("record_seq", sa.Integer(), nullable=False),
        sa.Column("supersedes", sa.String(36), nullable=True),
        sa.Column("alias", sa.String(128), nullable=False),
        sa.Column("currency", sa.String(8), nullable=False),
        sa.Column("environment", sa.String(16), nullable=False),
        sa.Column("read_only_login", sa.Boolean(), nullable=False),
        *_provenance_columns(),
        *_regime_columns(),
        sa.UniqueConstraint("provider_id", "broker_account_ext_id",
                            "record_seq", name="uq_v2_bracct_gen"),
        sa.CheckConstraint("environment IN ('practice')",
                           name="ck_v2_bracct_env"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_bracct_data_class"),
    )
    op.create_index("ix_v2_bracct_ext", "v2_broker_account",
                    ["broker_account_ext_id"])

    op.create_table(
        "v2_broker_balance",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("provider_id", sa.String(64), nullable=False),
        sa.Column("broker_account_ext_id", sa.String(64), nullable=False),
        sa.Column("balance", sa.String(64), nullable=False),
        sa.Column("margin_used", sa.String(64), nullable=False),
        sa.Column("margin_available", sa.String(64), nullable=False),
        sa.Column("unrealized_pl", sa.String(64), nullable=False),
        sa.Column("currency", sa.String(8), nullable=False),
        *_provenance_columns(),
        *_regime_columns(),
        sa.UniqueConstraint("sync_run_id", "broker_account_ext_id",
                            name="uq_v2_brbal_run"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_brbal_data_class"),
    )
    op.create_index("ix_v2_brbal_ext", "v2_broker_balance",
                    ["broker_account_ext_id"])

    op.create_table(
        "v2_broker_position",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("provider_id", sa.String(64), nullable=False),
        sa.Column("broker_account_ext_id", sa.String(64), nullable=False),
        sa.Column("instrument_ext_id", sa.String(64), nullable=False),
        sa.Column("units_long", sa.String(64), nullable=False),
        sa.Column("units_short", sa.String(64), nullable=False),
        sa.Column("avg_price_long", sa.String(64), nullable=False),
        sa.Column("avg_price_short", sa.String(64), nullable=False),
        *_provenance_columns(),
        *_regime_columns(),
        sa.UniqueConstraint("sync_run_id", "broker_account_ext_id",
                            "instrument_ext_id", name="uq_v2_brpos_run"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_brpos_data_class"),
    )
    op.create_index("ix_v2_brpos_ext", "v2_broker_position",
                    ["broker_account_ext_id"])

    op.create_table(
        "v2_broker_order",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("provider_id", sa.String(64), nullable=False),
        sa.Column("order_ext_id", sa.String(64), nullable=False),
        sa.Column("broker_account_ext_id", sa.String(64), nullable=False),
        sa.Column("order_state_ext", sa.String(64), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        *_provenance_columns(),
        *_regime_columns(),
        sa.UniqueConstraint("sync_run_id", "order_ext_id",
                            name="uq_v2_brord_run"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_brord_data_class"),
    )
    op.create_index("ix_v2_brord_ext", "v2_broker_order", ["order_ext_id"])

    op.create_table(
        "v2_broker_fill",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("provider_id", sa.String(64), nullable=False),
        sa.Column("broker_account_ext_id", sa.String(64), nullable=False),
        sa.Column("transaction_ext_id", sa.String(64), nullable=False),
        sa.Column("tx_type_ext", sa.String(64), nullable=False),
        sa.Column("instrument_ext_id", sa.String(64), nullable=False),
        sa.Column("units", sa.String(64), nullable=False),
        sa.Column("price", sa.String(64), nullable=False),
        sa.Column("tx_time_ext", sa.String(64), nullable=False),
        *_provenance_columns(),
        *_regime_columns(),
        sa.UniqueConstraint("provider_id", "broker_account_ext_id",
                            "transaction_ext_id",
                            name="uq_v2_brfill_anchor"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_brfill_data_class"),
    )
    op.create_index("ix_v2_brfill_ext", "v2_broker_fill",
                    ["broker_account_ext_id"])

    op.create_table(
        "v2_broker_instrument_permission",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("provider_id", sa.String(64), nullable=False),
        sa.Column("broker_account_ext_id", sa.String(64), nullable=False),
        sa.Column("instrument_ext_id", sa.String(64), nullable=False),
        sa.Column("visibility", sa.JSON(), nullable=False),
        sa.Column("display_name", sa.String(256), nullable=False),
        *_provenance_columns(),
        *_regime_columns(),
        sa.UniqueConstraint("sync_run_id", "broker_account_ext_id",
                            "instrument_ext_id", name="uq_v2_brinst_run"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_brinst_data_class"),
    )
    op.create_index("ix_v2_brinst_ext", "v2_broker_instrument_permission",
                    ["instrument_ext_id"])

    op.create_table(
        "v2_broker_sync_run",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("provider_id", sa.String(64), nullable=False),
        sa.Column("scope", sa.JSON(), nullable=False),
        sa.Column("outcome", sa.String(24), nullable=False),
        sa.Column("page_counts", sa.JSON(), nullable=False),
        sa.Column("origin_basis", sa.String(64), nullable=False),
        sa.Column("inputs_hash", sa.String(64), nullable=False),
        sa.Column("result_digest", sa.String(64), nullable=False),
        sa.Column("refusal", sa.JSON(), nullable=True),
        sa.Column("actor_id", sa.String(128), nullable=False),
        *_regime_columns(),
        sa.CheckConstraint(
            "outcome IN ('complete','partial_refused','failed')",
            name="ck_v2_brsync_outcome"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_brsync_data_class"),
    )
    op.create_index("ix_v2_brsync_created", "v2_broker_sync_run",
                    ["created_at"])

    op.create_table(
        "v2_broker_reconcile_run",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("provider_id", sa.String(64), nullable=False),
        sa.Column("sync_run_id", sa.String(36), nullable=False),
        sa.Column("compare_scope", sa.JSON(), nullable=False),
        sa.Column("broker_side_digest", sa.String(64), nullable=False),
        sa.Column("projection_side_digest", sa.String(64), nullable=False),
        sa.Column("compared_counts", sa.JSON(), nullable=False),
        sa.Column("discrepancy_count", sa.Integer(), nullable=False),
        sa.Column("outcome", sa.String(16), nullable=False),
        sa.Column("actor_id", sa.String(128), nullable=False),
        *_regime_columns(),
        sa.CheckConstraint("outcome IN ('clean','discrepant')",
                           name="ck_v2_brrec_outcome"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_brrec_data_class"),
    )
    op.create_index("ix_v2_brrec_created", "v2_broker_reconcile_run",
                    ["created_at"])

    op.create_table(
        "v2_broker_discrepancy",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("discrepancy_id", sa.String(64), nullable=False),
        sa.Column("record_seq", sa.Integer(), nullable=False),
        sa.Column("supersedes", sa.String(36), nullable=True),
        sa.Column("reconcile_run_id", sa.String(36), nullable=False),
        sa.Column("discrepancy_class", sa.String(32), nullable=False),
        sa.Column("state", sa.String(32), nullable=False),
        sa.Column("broker_side", sa.JSON(), nullable=False),
        sa.Column("projection_side", sa.JSON(), nullable=False),
        sa.Column("owned_by", sa.String(128), nullable=True),
        sa.Column("dismiss_reason", sa.String(512), nullable=True),
        sa.Column("provider_id", sa.String(64), nullable=False),
        *_regime_columns(),
        sa.UniqueConstraint("discrepancy_id", "record_seq",
                            name="uq_v2_brdisc_gen"),
        sa.CheckConstraint(
            "discrepancy_class IN ('amount_mismatch','missing_on_broker',"
            "'missing_in_axiom','currency_mismatch','timestamp_window',"
            "'permission_visibility','set_mismatch')",
            name="ck_v2_brdisc_class"),
        sa.CheckConstraint(
            "state IN ('detected','triaged','owned','resolved',"
            "'dismissed_with_reason')",
            name="ck_v2_brdisc_state"),
        sa.CheckConstraint(
            "(state = 'dismissed_with_reason') = (dismiss_reason IS NOT NULL)",
            name="ck_v2_brdisc_reason_iff"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_brdisc_data_class"),
    )
    op.create_index("ix_v2_brdisc_id", "v2_broker_discrepancy",
                    ["discrepancy_id"])

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
    op.execute(compver.insert().values(
        id=str(uuid4()), component="broker_read_engine",
        version="bre-1.0.0", source_hash=_rolling_hash(_BRE_FILES),
        evidence_ref="BO-V2-BE-9-001", registered_at=now,
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
            "BE-9 0049: guard triggers NOT present - manual recovery"
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
    ).bindparams(c="broker_read_engine", v="bre-1.0.0"))
    _recreate_compver_delete_guard(bind)
    for index, table in (
        ("ix_v2_brdisc_id", "v2_broker_discrepancy"),
        ("ix_v2_brrec_created", "v2_broker_reconcile_run"),
        ("ix_v2_brsync_created", "v2_broker_sync_run"),
        ("ix_v2_brinst_ext", "v2_broker_instrument_permission"),
        ("ix_v2_brfill_ext", "v2_broker_fill"),
        ("ix_v2_brord_ext", "v2_broker_order"),
        ("ix_v2_brpos_ext", "v2_broker_position"),
        ("ix_v2_brbal_ext", "v2_broker_balance"),
        ("ix_v2_bracct_ext", "v2_broker_account"),
    ):
        op.drop_index(index, table_name=table)
    for table in ("v2_broker_discrepancy", "v2_broker_reconcile_run",
                  "v2_broker_sync_run", "v2_broker_instrument_permission",
                  "v2_broker_fill", "v2_broker_order", "v2_broker_position",
                  "v2_broker_balance", "v2_broker_account"):
        op.drop_table(table)
