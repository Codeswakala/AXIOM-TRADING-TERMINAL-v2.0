"""V2 BE-6 U-1 — portfolio research (BO-V2-BE-6-001 T-1…T-6).

Creates: v2_portfolio_definition (versioned-immutable, P-1/C-1),
v2_portfolio_risk_report (immutable artifact, P-2), 4 guard triggers
(28→32), 6 permission rows (35→41), 1 compver row pre-1.0.0 (5→6, P-4;
C-2 re-pin obligation recorded for the application act). Symmetric
downgrade. Touches nothing else (no V1/BE-1…BE-5 object).

Revision ID: 20260903_0046
Revises: 20260902_0045
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import sqlalchemy as sa

from alembic import op

revision = "20260903_0046"
down_revision = "20260902_0045"
branch_labels = None
depends_on = None

_TRIGGERS = (
    ("v2_portfolio_definition_immutable_update", "v2_portfolio_definition",
     "UPDATE", "V2 portfolio definitions are immutable; UPDATE prohibited"),
    ("v2_portfolio_definition_immutable_delete", "v2_portfolio_definition",
     "DELETE", "V2 portfolio definitions are immutable; DELETE prohibited"),
    ("v2_portfolio_risk_report_immutable_update", "v2_portfolio_risk_report",
     "UPDATE", "V2 portfolio risk reports are immutable; UPDATE prohibited"),
    ("v2_portfolio_risk_report_immutable_delete", "v2_portfolio_risk_report",
     "DELETE", "V2 portfolio risk reports are immutable; DELETE prohibited"),
)

_PERMISSIONS = (
    ("admin", "v2.research.portfolio.read", "SAL-2"),
    ("admin", "v2.research.portfolio.define", "SAL-3"),
    ("admin", "v2.research.portfolio_risk.read", "SAL-2"),
    ("admin", "v2.research.portfolio_risk.compute", "SAL-3"),
    ("operator", "v2.research.portfolio.read", "SAL-2"),
    ("operator", "v2.research.portfolio_risk.read", "SAL-2"),
)

# P-4: engine files co-delivered with this migration (U-2/U-3, one package).
_PRE_FILES = (
    "app/v2/portfolio_research/__init__.py",
    "app/v2/portfolio_research/contracts.py",
    "app/v2/portfolio_research/metrics.py",
    "app/v2/portfolio_research/scenarios.py",
)

_DATA_CLASS_CHECK = (
    "data_class IN ('synthetic','simulated','historical_real','live',"
    "'stale_cached','unavailable')"
)


def _pre_source_hash() -> str:
    base = Path(__file__).resolve().parents[2]
    digest = hashlib.sha256()
    for rel in _PRE_FILES:
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
            CREATE OR REPLACE FUNCTION prevent_v2_portfolio_mutation()
            RETURNS trigger AS $$
            BEGIN
                IF TG_TABLE_NAME = 'v2_portfolio_definition' THEN
                    RAISE EXCEPTION
                        'V2 portfolio definitions are immutable; % prohibited', TG_OP;
                ELSE
                    RAISE EXCEPTION
                        'V2 portfolio risk reports are immutable; % prohibited', TG_OP;
                END IF;
            END;
            $$ LANGUAGE plpgsql;
        """)
        for name, table, event, _message in _TRIGGERS:
            op.execute(f"""
                CREATE TRIGGER {name}
                BEFORE {event} ON {table}
                FOR EACH ROW EXECUTE FUNCTION prevent_v2_portfolio_mutation();
            """)


def _drop_triggers(bind) -> None:
    if bind.dialect.name == "sqlite":
        for name, _t, _e, _m in _TRIGGERS:
            op.execute(f"DROP TRIGGER IF EXISTS {name}")
    elif bind.dialect.name == "postgresql":
        for name, table, _e, _m in _TRIGGERS:
            op.execute(f"DROP TRIGGER IF EXISTS {name} ON {table}")
        op.execute("DROP FUNCTION IF EXISTS prevent_v2_portfolio_mutation()")


def _drop_compver_delete_guard(bind) -> None:
    """Established pattern (0044/0045): drop -> delete own seed -> recreate
    -> verify. UPDATE guard stays in place."""
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
        "v2_portfolio_definition",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("portfolio_id", sa.String(64), nullable=False),
        sa.Column("record_seq", sa.Integer(), nullable=False),
        sa.Column("supersedes", sa.String(36), nullable=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("basis", sa.String(16), nullable=False),
        sa.Column("allocations", sa.JSON(), nullable=False),
        sa.Column("base_currency", sa.String(8), nullable=False),
        sa.Column("data_class", sa.String(32), nullable=False),
        sa.Column("assumptions", sa.JSON(), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("portfolio_id", "record_seq",
                            name="uq_v2_pfdef_id_seq"),
        sa.CheckConstraint("basis IN ('hypothetical')",
                           name="ck_v2_pfdef_basis"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_pfdef_data_class"),
    )
    op.create_index("ix_v2_pfdef_portfolio", "v2_portfolio_definition",
                    ["portfolio_id"])

    op.create_table(
        "v2_portfolio_risk_report",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("portfolio_definition_id", sa.String(36), nullable=False),
        sa.Column("as_of", sa.DateTime(timezone=True), nullable=False),
        sa.Column("time_basis", sa.JSON(), nullable=False),
        sa.Column("input_refs", sa.JSON(), nullable=False),
        sa.Column("inputs_hash", sa.String(64), nullable=False),
        sa.Column("metrics", sa.JSON(), nullable=False),
        sa.Column("scenarios", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("basis_label", sa.String(32), nullable=False),
        sa.Column("data_class", sa.String(32), nullable=False),
        sa.Column("engine_versions", sa.JSON(), nullable=False),
        sa.Column("engine_versions_hash", sa.String(64), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("correlation_id", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("portfolio_definition_id", "inputs_hash",
                            "engine_versions_hash",
                            name="uq_v2_pfrisk_determinism_anchor"),
        sa.CheckConstraint(
            "status IN ('available','degraded','unavailable','stale',"
            "'unknown','denied')",
            name="ck_v2_pfrisk_status"),
        sa.CheckConstraint("basis_label IN ('hypothetical-research')",
                           name="ck_v2_pfrisk_basis_label"),
        sa.CheckConstraint(_DATA_CLASS_CHECK, name="ck_v2_pfrisk_data_class"),
    )
    op.create_index("ix_v2_pfrisk_def", "v2_portfolio_risk_report",
                    ["portfolio_definition_id"])

    # --- Seeds (revision-local literals — DEL-004 law) -------------------
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
        id=str(uuid4()), component="portfolio_risk_engine",
        version="pre-1.0.0", source_hash=_pre_source_hash(),
        evidence_ref="BO-V2-BE-6-001", registered_at=now,
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
            "BE-6 0046: portfolio guard triggers NOT present — manual"
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
        " WHERE component = 'portfolio_risk_engine' AND version = 'pre-1.0.0'"
    ))
    _recreate_compver_delete_guard(bind)
    op.drop_index("ix_v2_pfrisk_def", table_name="v2_portfolio_risk_report")
    op.drop_table("v2_portfolio_risk_report")
    op.drop_index("ix_v2_pfdef_portfolio", table_name="v2_portfolio_definition")
    op.drop_table("v2_portfolio_definition")
