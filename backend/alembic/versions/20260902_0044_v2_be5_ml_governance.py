"""V2 BE-5 U-1 — ML governance overlay (BO-V2-BE-5-001 T-2/T-3/T-4/T-5).

Review Pins applied: P-1 (full immutability + row versioning: record_seq,
supersedes, NO updated_at_event_id, UPDATE guard), P-2 (dedicated
v2_ml_diagnostic_report, 0043 pattern), P-3 (model_type +
instrument_class), P-4 (compver seed mge-1.0.0 co-delivered with U-2).

Creates: 3 tables, 6 guard triggers, 7 permission rows (27→34),
1 computation-version row (3→4). Symmetric downgrade. Touches nothing
else (no V1/BE-1…BE-4 object).

Revision ID: 20260902_0044
Revises: 20260831_0043
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import sqlalchemy as sa

from alembic import op

revision = "20260902_0044"
down_revision = "20260831_0043"
branch_labels = None
depends_on = None

_TRIGGERS = (
    ("v2_ml_governance_record_immutable_update", "v2_ml_governance_record",
     "UPDATE", "V2 ML governance records are immutable; UPDATE prohibited"),
    ("v2_ml_governance_record_immutable_delete", "v2_ml_governance_record",
     "DELETE", "V2 ML governance records are immutable; DELETE prohibited"),
    ("v2_ml_lifecycle_event_immutable_update", "v2_ml_lifecycle_event",
     "UPDATE", "V2 ML lifecycle events are immutable; UPDATE prohibited"),
    ("v2_ml_lifecycle_event_immutable_delete", "v2_ml_lifecycle_event",
     "DELETE", "V2 ML lifecycle events are immutable; DELETE prohibited"),
    ("v2_ml_diagnostic_report_immutable_update", "v2_ml_diagnostic_report",
     "UPDATE", "V2 ML diagnostic reports are immutable; UPDATE prohibited"),
    ("v2_ml_diagnostic_report_immutable_delete", "v2_ml_diagnostic_report",
     "DELETE", "V2 ML diagnostic reports are immutable; DELETE prohibited"),
)

_PERMISSIONS = (
    ("admin", "v2.research.ml_governance.read", "SAL-2"),
    ("admin", "v2.research.ml_governance.decide", "SAL-3"),
    ("admin", "v2.research.signal.read", "SAL-2"),
    ("admin", "v2.research.ml_diagnostics.read", "SAL-2"),
    ("operator", "v2.research.ml_governance.read", "SAL-2"),
    ("operator", "v2.research.signal.read", "SAL-2"),
    ("operator", "v2.research.ml_diagnostics.read", "SAL-2"),
)

# P-4: engine files co-delivered with this migration (U-2, package PG-1).
_MGE_FILES = (
    "app/v2/research_governance/__init__.py",
    "app/v2/research_governance/contracts.py",
    "app/v2/research_governance/decisions.py",
)


def _mge_source_hash() -> str:
    base = Path(__file__).resolve().parents[2]
    digest = hashlib.sha256()
    for rel in _MGE_FILES:
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
            CREATE OR REPLACE FUNCTION prevent_v2_ml_governance_mutation()
            RETURNS trigger AS $$
            BEGIN
                IF TG_TABLE_NAME = 'v2_ml_governance_record' THEN
                    RAISE EXCEPTION
                        'V2 ML governance records are immutable; % prohibited', TG_OP;
                ELSIF TG_TABLE_NAME = 'v2_ml_lifecycle_event' THEN
                    RAISE EXCEPTION
                        'V2 ML lifecycle events are immutable; % prohibited', TG_OP;
                ELSE
                    RAISE EXCEPTION
                        'V2 ML diagnostic reports are immutable; % prohibited', TG_OP;
                END IF;
            END;
            $$ LANGUAGE plpgsql;
        """)
        for name, table, event, _message in _TRIGGERS:
            op.execute(f"""
                CREATE TRIGGER {name}
                BEFORE {event} ON {table}
                FOR EACH ROW EXECUTE FUNCTION prevent_v2_ml_governance_mutation();
            """)


def _drop_triggers(bind) -> None:
    if bind.dialect.name == "sqlite":
        for name, _t, _e, _m in _TRIGGERS:
            op.execute(f"DROP TRIGGER IF EXISTS {name}")
    elif bind.dialect.name == "postgresql":
        for name, table, _e, _m in _TRIGGERS:
            op.execute(f"DROP TRIGGER IF EXISTS {name} ON {table}")
        op.execute("DROP FUNCTION IF EXISTS prevent_v2_ml_governance_mutation()")




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
        "v2_ml_governance_record",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("model_artifact_id", sa.String(36), nullable=False),
        sa.Column("record_seq", sa.Integer(), nullable=False),  # P-1
        sa.Column("supersedes", sa.String(36), nullable=True),  # P-1
        sa.Column("registry_version", sa.String(64), nullable=False),
        sa.Column("model_type", sa.String(64), nullable=False),  # P-3
        sa.Column("instrument_class", sa.String(64), nullable=False),  # P-3
        sa.Column("eligibility_status", sa.String(32), nullable=False),
        sa.Column("calibration_status", sa.String(32), nullable=False),
        sa.Column("freshness_status", sa.String(32), nullable=False),
        sa.Column("economic_status", sa.String(32), nullable=False),
        sa.Column("statistical_status", sa.String(32), nullable=False),
        sa.Column("deployment_class", sa.String(32), nullable=False),
        sa.Column("rollback_target_version", sa.String(64), nullable=True),
        sa.Column("data_class", sa.String(32), nullable=False),
        sa.Column("evidence_refs", sa.JSON(), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("model_artifact_id", "record_seq",
                            name="uq_v2_mlgov_artifact_seq"),  # P-1
        sa.CheckConstraint(
            "eligibility_status IN ('unevaluated','eligible','ineligible','expired')",
            name="ck_v2_mlgov_eligibility"),
        sa.CheckConstraint(
            "calibration_status IN ('unevaluated','calibrated','miscalibrated','stale')",
            name="ck_v2_mlgov_calibration"),
        sa.CheckConstraint(
            "freshness_status IN ('fresh','stale','expired','unknown')",
            name="ck_v2_mlgov_freshness"),
        sa.CheckConstraint(
            "economic_status IN ('unevaluated','viable','unviable')",
            name="ck_v2_mlgov_economic"),
        sa.CheckConstraint(
            "statistical_status IN ('unevaluated','significant','not_significant')",
            name="ck_v2_mlgov_statistical"),
        sa.CheckConstraint(
            "deployment_class IN ('research','shadow','champion','challenger','retired')",
            name="ck_v2_mlgov_class"),
        sa.CheckConstraint(
            "data_class IN ('synthetic','simulated','historical_real','live',"
            "'stale_cached','unavailable')",
            name="ck_v2_mlgov_data_class"),
    )
    op.create_index("ix_v2_mlgov_artifact", "v2_ml_governance_record",
                    ["model_artifact_id"])

    op.create_table(
        "v2_ml_lifecycle_event",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("governance_record_id", sa.String(36), nullable=False),
        sa.Column("event_type", sa.String(48), nullable=False),
        sa.Column("from_value", sa.String(64), nullable=False),
        sa.Column("to_value", sa.String(64), nullable=False),
        sa.Column("decision_basis", sa.JSON(), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("actor_id", sa.String(128), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "event_type IN ('registered','eligibility_evaluated',"
            "'calibration_evaluated','freshness_evaluated',"
            "'economic_evaluated','statistical_evaluated','promoted',"
            "'demoted','refused','rolled_back','retired')",
            name="ck_v2_mlev_type"),
    )
    op.create_index("ix_v2_mlev_record", "v2_ml_lifecycle_event",
                    ["governance_record_id"])

    # P-2: dedicated diagnostic-report artifact table (0043 pattern)
    op.create_table(
        "v2_ml_diagnostic_report",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("model_artifact_id", sa.String(36), nullable=False),
        sa.Column("governance_record_id", sa.String(36), nullable=True),
        sa.Column("diagnostics", sa.JSON(), nullable=False),
        sa.Column("input_refs", sa.JSON(), nullable=False),
        sa.Column("inputs_hash", sa.String(64), nullable=False),
        sa.Column("engine_versions", sa.JSON(), nullable=False),
        sa.Column("engine_versions_hash", sa.String(64), nullable=False),
        sa.Column("data_class", sa.String(32), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("model_artifact_id", "inputs_hash",
                            "engine_versions_hash",
                            name="uq_v2_mldiag_determinism_anchor"),
        sa.CheckConstraint(
            "data_class IN ('synthetic','simulated','historical_real','live',"
            "'stale_cached','unavailable')",
            name="ck_v2_mldiag_data_class"),
    )
    op.create_index("ix_v2_mldiag_artifact", "v2_ml_diagnostic_report",
                    ["model_artifact_id"])

    # --- Seeds (revision-local literals — DEL-004 law) -----------------------
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

    # P-4: compver row for the co-delivered mge engine, hash from disk now.
    compver = sa.table(
        "v2_computation_version",
        sa.column("id", sa.String), sa.column("component", sa.String),
        sa.column("version", sa.String), sa.column("source_hash", sa.String),
        sa.column("evidence_ref", sa.String),
        sa.column("registered_at", sa.DateTime(timezone=True)),
    )
    op.execute(compver.insert().values(
        id=str(uuid4()), component="ml_governance_engine",
        version="mge-1.0.0", source_hash=_mge_source_hash(),
        evidence_ref="BO-V2-BE-5-001", registered_at=now,
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
            "BE-5 0044: governance guard triggers NOT present — manual"
            " recovery required; do not treat this migration as applied"
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
        " WHERE component = 'ml_governance_engine' AND version = 'mge-1.0.0'"
    ))
    _recreate_compver_delete_guard(bind)
    op.drop_index("ix_v2_mldiag_artifact", table_name="v2_ml_diagnostic_report")
    op.drop_table("v2_ml_diagnostic_report")
    op.drop_index("ix_v2_mlev_record", table_name="v2_ml_lifecycle_event")
    op.drop_table("v2_ml_lifecycle_event")
    op.drop_index("ix_v2_mlgov_artifact", table_name="v2_ml_governance_record")
    op.drop_table("v2_ml_governance_record")
