"""V2 BE-4 — research read models (BO-V2-BE-4-001 D-1).

Creates: v2_computation_version, v2_market_context_report,
v2_chart_intelligence_report; six R-2 guard triggers (exact names and
messages pinned by the Build Order); revision-local seed rows (initial
computation versions with source hashes recorded at seed time; the three
BE-4 permissions — DEL-004 pattern, literal rows).

Touches NOTHING else: no guarded BE-3 table, no BE-1/BE-2 object, no V1
object (BG-3/BG-9). Symmetric downgrade drops only this revision's tables,
triggers, and seed rows.

Revision ID: 20260831_0043
Revises: 20260829_0042
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

import sqlalchemy as sa

from alembic import op

revision = "20260831_0043"
down_revision = "20260829_0042"
branch_labels = None
depends_on = None

# R-2 pins (BO §4 D-1) — exact trigger names and guard messages.
_TRIGGERS = (
    ("v2_computation_version_immutable_update", "v2_computation_version",
     "UPDATE", "V2 computation version registry is immutable; UPDATE prohibited"),
    ("v2_computation_version_immutable_delete", "v2_computation_version",
     "DELETE", "V2 computation version registry is immutable; DELETE prohibited"),
    ("v2_market_context_report_immutable_update", "v2_market_context_report",
     "UPDATE", "V2 market context reports are immutable; UPDATE prohibited"),
    ("v2_market_context_report_immutable_delete", "v2_market_context_report",
     "DELETE", "V2 market context reports are immutable; DELETE prohibited"),
    ("v2_chart_intelligence_report_immutable_update", "v2_chart_intelligence_report",
     "UPDATE", "V2 chart intelligence reports are immutable; UPDATE prohibited"),
    ("v2_chart_intelligence_report_immutable_delete", "v2_chart_intelligence_report",
     "DELETE", "V2 chart intelligence reports are immutable; DELETE prohibited"),
)

# Revision-local permission literals (DEL-004 / R-5 pattern).
_PERMISSIONS = (
    ("admin", "v2.research.market_context.read", "SAL-2"),
    ("admin", "v2.research.chart_intelligence.read", "SAL-2"),
    ("admin", "v2.research.market_context.compute", "SAL-3"),
    ("operator", "v2.research.market_context.read", "SAL-2"),
    ("operator", "v2.research.chart_intelligence.read", "SAL-2"),
)


def _create_guard_triggers(bind) -> None:
    if bind.dialect.name == "sqlite":
        for name, table, event, message in _TRIGGERS:
            op.execute(f"""
                CREATE TRIGGER {name}
                BEFORE {event} ON {table}
                BEGIN
                    SELECT RAISE(ABORT, '{message}');
                END;
            """)
    elif bind.dialect.name == "postgresql":  # deployment dialect
        op.execute("""
            CREATE OR REPLACE FUNCTION prevent_v2_research_mutation()
            RETURNS trigger AS $$
            BEGIN
                IF TG_TABLE_NAME = 'v2_computation_version' THEN
                    RAISE EXCEPTION
                        'V2 computation version registry is immutable; % prohibited', TG_OP;
                ELSIF TG_TABLE_NAME = 'v2_market_context_report' THEN
                    RAISE EXCEPTION
                        'V2 market context reports are immutable; % prohibited', TG_OP;
                ELSE
                    RAISE EXCEPTION
                        'V2 chart intelligence reports are immutable; % prohibited', TG_OP;
                END IF;
            END;
            $$ LANGUAGE plpgsql;
        """)
        for name, table, event, _message in _TRIGGERS:
            op.execute(f"""
                CREATE TRIGGER {name}
                BEFORE {event} ON {table}
                FOR EACH ROW EXECUTE FUNCTION prevent_v2_research_mutation();
            """)


def _drop_guard_triggers(bind) -> None:
    if bind.dialect.name == "sqlite":
        for name, _table, _event, _message in _TRIGGERS:
            op.execute(f"DROP TRIGGER IF EXISTS {name}")
    elif bind.dialect.name == "postgresql":
        for name, table, _event, _message in _TRIGGERS:
            op.execute(f"DROP TRIGGER IF EXISTS {name} ON {table}")
        op.execute("DROP FUNCTION IF EXISTS prevent_v2_research_mutation()")


def upgrade() -> None:
    bind = op.get_bind()
    now = datetime.now(timezone.utc)

    op.create_table(
        "v2_computation_version",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("component", sa.String(64), nullable=False),
        sa.Column("version", sa.String(64), nullable=False),
        sa.Column("source_hash", sa.String(64), nullable=False),
        sa.Column("evidence_ref", sa.String(256), nullable=True),
        sa.Column("registered_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("component", "version",
                            name="uq_v2_compver_component_version"),
    )

    op.create_table(
        "v2_market_context_report",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("instrument_id", sa.String(96), nullable=False),
        sa.Column("timeframe_set", sa.JSON(), nullable=False),
        sa.Column("as_of", sa.DateTime(timezone=True), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("validation_tier", sa.String(32), nullable=False),
        sa.Column("input_snapshot_id", sa.String(256), nullable=False),
        sa.Column("input_content_hash", sa.String(64), nullable=False),
        sa.Column("observations", sa.JSON(), nullable=False),
        sa.Column("engine_versions", sa.JSON(), nullable=False),
        sa.Column("engine_versions_hash", sa.String(64), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("instrument_id", "input_content_hash",
                            "engine_versions_hash",
                            name="uq_v2_mcr_determinism_anchor"),
    )
    op.create_index("ix_v2_mcr_instrument", "v2_market_context_report",
                    ["instrument_id"])
    op.create_index("ix_v2_mcr_mode", "v2_market_context_report", ["mode"])

    op.create_table(
        "v2_chart_intelligence_report",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("market_context_report_id", sa.String(36), nullable=False),
        sa.Column("as_of", sa.DateTime(timezone=True), nullable=False),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("annotations", sa.JSON(), nullable=False),
        sa.Column("interpretations", sa.JSON(), nullable=False),
        sa.Column("engine_versions", sa.JSON(), nullable=False),
        sa.Column("operator_id", sa.String(128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_v2_cir_mcr", "v2_chart_intelligence_report",
                    ["market_context_report_id"])

    # --- Seeds (before triggers so INSERTs are unimpeded; triggers guard
    # UPDATE/DELETE only, but ordering keeps the intent explicit) ---------
    from app.v2.research.versioning import (
        CHART_INTELLIGENCE_ENGINE_VERSION,
        INDICATOR_ENGINE_VERSION,
        MARKET_CONTEXT_ENGINE_VERSION,
        compute_cie_hash,
        compute_indicator_engine_hash,
        compute_mce_hash,
    )

    compver = sa.table(
        "v2_computation_version",
        sa.column("id", sa.String),
        sa.column("component", sa.String),
        sa.column("version", sa.String),
        sa.column("source_hash", sa.String),
        sa.column("evidence_ref", sa.String),
        sa.column("registered_at", sa.DateTime(timezone=True)),
    )
    for component, version, source_hash in (
        ("indicator_engine", INDICATOR_ENGINE_VERSION,
         compute_indicator_engine_hash()),
        ("market_context_engine", MARKET_CONTEXT_ENGINE_VERSION,
         compute_mce_hash()),
        ("chart_intelligence_engine", CHART_INTELLIGENCE_ENGINE_VERSION,
         compute_cie_hash()),
    ):
        op.execute(compver.insert().values(
            id=str(uuid4()), component=component, version=version,
            source_hash=source_hash, evidence_ref="BO-V2-BE-4-001",
            registered_at=now,
        ))

    permission_table = sa.table(
        "v2_permission",
        sa.column("id", sa.String),
        sa.column("role", sa.String),
        sa.column("permission", sa.String),
        sa.column("sal", sa.String),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )
    existing = {
        (row[0], row[1])
        for row in bind.execute(
            sa.text("SELECT role, permission FROM v2_permission")
        )
    }
    for role, permission, sal in _PERMISSIONS:
        if (role, permission) not in existing:
            op.execute(permission_table.insert().values(
                id=str(uuid4()), role=role, permission=permission,
                sal=sal, created_at=now,
            ))

    _create_guard_triggers(bind)
    _verify_guards_present(bind)


def _verify_guards_present(bind) -> None:
    """Fail loudly if any of the six R-2 triggers is missing."""
    if bind.dialect.name == "sqlite":
        names = tuple(t[0] for t in _TRIGGERS)
        placeholders = ",".join(f"'{n}'" for n in names)
        count = bind.execute(sa.text(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'"
            f" AND name IN ({placeholders})"
        )).scalar_one()
        expected = len(names)
    elif bind.dialect.name == "postgresql":
        names = tuple(t[0] for t in _TRIGGERS)
        placeholders = ",".join(f"'{n}'" for n in names)
        count = bind.execute(sa.text(
            f"SELECT COUNT(*) FROM pg_trigger WHERE tgname IN ({placeholders})"
        )).scalar_one()
        expected = len(names)
    else:  # pragma: no cover
        return
    if int(count) != expected:
        raise RuntimeError(
            "BE-4 migration: research guard triggers NOT present — manual"
            " recovery required; do not treat this migration as applied"
        )


def downgrade() -> None:
    bind = op.get_bind()
    _drop_guard_triggers(bind)
    # Revision-local seed removal (permissions are this revision's rows).
    for _role, permission, _sal in _PERMISSIONS:
        op.execute(sa.text(
            "DELETE FROM v2_permission WHERE permission = :p"
        ).bindparams(p=permission))
    op.drop_index("ix_v2_cir_mcr", table_name="v2_chart_intelligence_report")
    op.drop_table("v2_chart_intelligence_report")
    op.drop_index("ix_v2_mcr_mode", table_name="v2_market_context_report")
    op.drop_index("ix_v2_mcr_instrument", table_name="v2_market_context_report")
    op.drop_table("v2_market_context_report")
    op.drop_table("v2_computation_version")
