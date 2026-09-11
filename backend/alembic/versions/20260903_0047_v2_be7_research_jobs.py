"""V2 BE-7 U-1 — research jobs (BO-V2-BE-7-001 §1/T-1…T-6).

Six physical tables (five guarded + the sole-mutable job queue, FP-1);
10 guard triggers (32→42); 8 permission rows (41→49); 2 compver seeds
(6→8, P-4 co-delivery, C-2 disclosure: the 0047 application-act
instrument re-pins both engine file sets). Symmetric downgrade.

Revision ID: 20260903_0047
Revises: 20260903_0046
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import sqlalchemy as sa

from alembic import op

revision = "20260903_0047"
down_revision = "20260903_0046"
branch_labels = None
depends_on = None

_TRIGGERS = (
    ("v2_backtest_input_immutable_update", "v2_backtest_input",
     "UPDATE", "V2 backtest inputs are immutable; UPDATE prohibited"),
    ("v2_backtest_input_immutable_delete", "v2_backtest_input",
     "DELETE", "V2 backtest inputs are immutable; DELETE prohibited"),
    ("v2_cost_model_immutable_update", "v2_cost_model",
     "UPDATE", "V2 cost models are immutable; UPDATE prohibited"),
    ("v2_cost_model_immutable_delete", "v2_cost_model",
     "DELETE", "V2 cost models are immutable; DELETE prohibited"),
    ("v2_strategy_version_immutable_update", "v2_strategy_version",
     "UPDATE", "V2 strategy versions are immutable; UPDATE prohibited"),
    ("v2_strategy_version_immutable_delete", "v2_strategy_version",
     "DELETE", "V2 strategy versions are immutable; DELETE prohibited"),
    ("v2_research_job_attempt_immutable_update", "v2_research_job_attempt",
     "UPDATE", "V2 research job attempts are immutable; UPDATE prohibited"),
    ("v2_research_job_attempt_immutable_delete", "v2_research_job_attempt",
     "DELETE", "V2 research job attempts are immutable; DELETE prohibited"),
    ("v2_research_result_immutable_update", "v2_research_result",
     "UPDATE", "V2 research results are immutable; UPDATE prohibited"),
    ("v2_research_result_immutable_delete", "v2_research_result",
     "DELETE", "V2 research results are immutable; DELETE prohibited"),
)

_PERMISSIONS = (
    ("admin", "v2.research.jobs.read", "SAL-2"),
    ("admin", "v2.research.jobs.submit", "SAL-3"),
    ("admin", "v2.research.jobs.cancel", "SAL-3"),
    ("admin", "v2.research.registry.read", "SAL-2"),
    ("admin", "v2.research.registry.write", "SAL-3"),
    ("admin", "v2.research.results.read", "SAL-2"),
    ("operator", "v2.research.jobs.read", "SAL-2"),
    ("operator", "v2.research.results.read", "SAL-2"),
)

_RPE_FILES = (
    "app/v2/research_jobs/__init__.py",
    "app/v2/research_jobs/leakage.py",
    "app/v2/research_jobs/replay.py",
)
_RJE_FILES = (
    "app/v2/research_jobs/queue.py",
    "app/v2/research_jobs/runner.py",
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
            CREATE OR REPLACE FUNCTION prevent_v2_research_jobs_mutation()
            RETURNS trigger AS $$
            BEGIN
                RAISE EXCEPTION
                    'V2 research-jobs artifact is immutable; % prohibited on %',
                    TG_OP, TG_TABLE_NAME;
            END;
            $$ LANGUAGE plpgsql;
        """)
        for name, table, event, _message in _TRIGGERS:
            op.execute(f"""
                CREATE TRIGGER {name}
                BEFORE {event} ON {table}
                FOR EACH ROW EXECUTE FUNCTION prevent_v2_research_jobs_mutation();
            """)


def _drop_triggers(bind) -> None:
    if bind.dialect.name == "sqlite":
        for name, _t, _e, _m in _TRIGGERS:
            op.execute(f"DROP TRIGGER IF EXISTS {name}")
    elif bind.dialect.name == "postgresql":
        for name, table, _e, _m in _TRIGGERS:
            op.execute(f"DROP TRIGGER IF EXISTS {name} ON {table}")
        op.execute("DROP FUNCTION IF EXISTS prevent_v2_research_jobs_mutation()")


def _drop_compver_delete_guard(bind) -> None:
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
        "v2_backtest_input",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("input_id", sa.String(64), nullable=False),
        sa.Column("record_seq", sa.Integer(), nullable=False),
        sa.Column("supersedes", sa.String(36), nullable=True),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("series_refs", sa.JSON(), nullable=False),
        sa.Column("window_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("window_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("registration_outcome", sa.String(16), nullable=False),
        *_be1_columns(),
        sa.UniqueConstraint("input_id", "record_seq", name="uq_v2_btin_id_seq"),
        sa.UniqueConstraint("content_hash", name="uq_v2_btin_content"),
        sa.CheckConstraint(
            "registration_outcome IN ('registered','reused','refused')",
            name="ck_v2_btin_outcome"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_btin_data_class"),
    )
    op.create_index("ix_v2_btin_input", "v2_backtest_input", ["input_id"])

    op.create_table(
        "v2_cost_model",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("cost_model_id", sa.String(64), nullable=False),
        sa.Column("record_seq", sa.Integer(), nullable=False),
        sa.Column("supersedes", sa.String(36), nullable=True),
        sa.Column("spread", sa.JSON(), nullable=False),
        sa.Column("commission", sa.JSON(), nullable=False),
        sa.Column("slippage", sa.JSON(), nullable=False),
        sa.Column("latency_ms", sa.Integer(), nullable=False),
        sa.Column("risk_limits", sa.JSON(), nullable=False),
        sa.Column("citations", sa.JSON(), nullable=False),
        *_be1_columns(),
        sa.UniqueConstraint("cost_model_id", "record_seq",
                            name="uq_v2_cost_id_seq"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_cost_data_class"),
    )
    op.create_index("ix_v2_cost_model", "v2_cost_model", ["cost_model_id"])

    op.create_table(
        "v2_strategy_version",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("strategy_id", sa.String(64), nullable=False),
        sa.Column("record_seq", sa.Integer(), nullable=False),
        sa.Column("supersedes", sa.String(36), nullable=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("parameters", sa.JSON(), nullable=False),
        sa.Column("lifecycle_state", sa.String(16), nullable=False),
        *_be1_columns(),
        sa.UniqueConstraint("strategy_id", "record_seq",
                            name="uq_v2_strat_id_seq"),
        sa.CheckConstraint(
            "lifecycle_state IN ('draft','registered','retired')",
            name="ck_v2_strat_state"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_strat_data_class"),
    )
    op.create_index("ix_v2_strat_strategy", "v2_strategy_version",
                    ["strategy_id"])

    op.create_table(
        "v2_research_job",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("owner", sa.String(128), nullable=False),
        sa.Column("authorization_ref", sa.String(128), nullable=False),
        sa.Column("inputs", sa.JSON(), nullable=False),
        sa.Column("schedule", sa.JSON(), nullable=False),
        sa.Column("output_ref", sa.String(36), nullable=True),
        sa.Column("failure", sa.JSON(), nullable=True),
        sa.Column("job_state", sa.String(16), nullable=False),
        sa.Column("attempt_count", sa.Integer(), nullable=False),
        *_be1_columns(),
        sa.CheckConstraint(
            "job_state IN ('queued','running','succeeded','failed',"
            "'cancelled')",
            name="ck_v2_job_state"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_job_data_class"),
    )
    op.create_index("ix_v2_job_state", "v2_research_job", ["job_state"])

    op.create_table(
        "v2_research_job_attempt",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("job_id", sa.String(36), nullable=False),
        sa.Column("attempt_index", sa.Integer(), nullable=False),
        sa.Column("outcome", sa.String(16), nullable=False),
        sa.Column("artifact_ref", sa.String(36), nullable=True),
        sa.Column("reason", sa.JSON(), nullable=False),
        sa.Column("actor_id", sa.String(128), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("job_id", "attempt_index", name="uq_v2_jobatt_idx"),
        sa.CheckConstraint(
            "outcome IN ('succeeded','failed','cancelled')",
            name="ck_v2_jobatt_outcome"),
    )
    op.create_index("ix_v2_jobatt_job", "v2_research_job_attempt", ["job_id"])

    op.create_table(
        "v2_research_result",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("result_class", sa.String(16), nullable=False),
        sa.Column("job_id", sa.String(36), nullable=False),
        sa.Column("attempt_index", sa.Integer(), nullable=False),
        sa.Column("strategy_version_id", sa.String(36), nullable=False),
        sa.Column("input_registry_id", sa.String(36), nullable=False),
        sa.Column("cost_model_id", sa.String(36), nullable=False),
        sa.Column("inputs_hash", sa.String(64), nullable=False),
        sa.Column("engine_versions", sa.JSON(), nullable=False),
        sa.Column("engine_versions_hash", sa.String(64), nullable=False),
        sa.Column("summary", sa.JSON(), nullable=False),
        sa.Column("replay_of", sa.String(36), nullable=True),
        sa.Column("time_basis", sa.JSON(), nullable=False),
        *_be1_columns(),
        sa.UniqueConstraint("strategy_version_id", "inputs_hash",
                            "engine_versions_hash",
                            name="uq_v2_result_determinism_anchor"),
        sa.CheckConstraint("result_class IN ('backtest','simulation')",
                           name="ck_v2_result_class"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_result_data_class"),
    )
    op.create_index("ix_v2_result_job", "v2_research_result", ["job_id"])

    # --- Seeds (revision-local literals; DEL-004 law) ---------------------
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
    for component, version, files in (
        ("replay_engine", "rpe-1.0.0", _RPE_FILES),
        ("research_job_engine", "rje-1.0.0", _RJE_FILES),
    ):
        op.execute(compver.insert().values(
            id=str(uuid4()), component=component, version=version,
            source_hash=_rolling_hash(files), evidence_ref="BO-V2-BE-7-001",
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
            "BE-7 0047: guard triggers NOT present — manual recovery"
            " required; do not treat this migration as applied")


def downgrade() -> None:
    bind = op.get_bind()
    _drop_triggers(bind)
    for _role, permission, _sal in _PERMISSIONS:
        op.execute(sa.text(
            "DELETE FROM v2_permission WHERE permission = :p"
        ).bindparams(p=permission))
    _drop_compver_delete_guard(bind)
    for component, version in (("replay_engine", "rpe-1.0.0"),
                               ("research_job_engine", "rje-1.0.0")):
        op.execute(sa.text(
            "DELETE FROM v2_computation_version"
            " WHERE component = :c AND version = :v"
        ).bindparams(c=component, v=version))
    _recreate_compver_delete_guard(bind)
    for index, table in (
        ("ix_v2_result_job", "v2_research_result"),
        ("ix_v2_jobatt_job", "v2_research_job_attempt"),
        ("ix_v2_job_state", "v2_research_job"),
        ("ix_v2_strat_strategy", "v2_strategy_version"),
        ("ix_v2_cost_model", "v2_cost_model"),
        ("ix_v2_btin_input", "v2_backtest_input"),
    ):
        op.drop_index(index, table_name=table)
    for table in ("v2_research_result", "v2_research_job_attempt",
                  "v2_research_job", "v2_strategy_version",
                  "v2_cost_model", "v2_backtest_input"):
        op.drop_table(table)
