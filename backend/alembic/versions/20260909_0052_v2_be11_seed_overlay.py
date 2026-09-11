"""V2 BE-11 seed overlay — OV-V2-BE-11-002 (Exit (a); data rows only).

Five INSERTs into v2_paper_bridge_drift_run, kind `seed`:
four `drift_tolerance` rows (balance / margin_used / margin_available /
unrealized_pl, each 125.00 USD absolute — declared intent map: minor
boundary 125.00, major boundary 250.00 under the structural 2x law) and
one `generation_staleness` row (max_age_hours 48). Zero DDL, zero model
edits, zero engine bytes, compver untouched, triggers untouched.

Chassis sourced from the ENUMERATED ENGINE CONTRACT (OV-002 §0; N-O19
law: seed specs enumerate engine-read contracts from engine source) and
build-gate-probed against accepted pbr-1.0.0
(4c243435103a149830fd448d4f84a931af7543aa08b901299ebb5d1a27ff178b)
before this migration was authored.

Downgrade: deletes exactly the five rows content-keyed by
(seed_name, payload name), count-asserted; the immutable guard pair is
dropped and recreated around the delete (compver delete-guard dance
precedent) and its restoration is verified.
"""

from __future__ import annotations

import json
import uuid

import sqlalchemy as sa

from alembic import op

revision = "20260909_0052"
down_revision = "20260909_0051"
branch_labels = None
depends_on = None

# The guard pair of 0051, quoted verbatim (drop/recreate dance only —
# the overlay neither adds nor removes triggers on net).
_TRIGGERS = (
    ("v2_paper_bridge_drift_run_immutable_update",
     "v2_paper_bridge_drift_run",
     "UPDATE", "V2 paper bridge drift runs are immutable; UPDATE prohibited"),
    ("v2_paper_bridge_drift_run_immutable_delete",
     "v2_paper_bridge_drift_run",
     "DELETE", "V2 paper bridge drift runs are immutable; DELETE prohibited"),
)

_ACT_REF = "OV-V2-BE-11-002"
_CREATED_AT = "2026-09-07 00:00:00.000000+00:00"

# OV-V2-BE-11-002 §1 payload, verbatim (values quoted, not retyped).
_SEED_ROWS = (
    ("drift_tolerance",
     {"name": "balance", "value": "125.00", "unit": "USD",
      "citation": "operator seed"}),
    ("drift_tolerance",
     {"name": "margin_used", "value": "125.00", "unit": "USD",
      "citation": "operator seed"}),
    ("drift_tolerance",
     {"name": "margin_available", "value": "125.00", "unit": "USD",
      "citation": "operator seed"}),
    ("drift_tolerance",
     {"name": "unrealized_pl", "value": "125.00", "unit": "USD",
      "citation": "operator seed"}),
    ("generation_staleness",
     {"max_age_hours": 48, "citation": "operator seed"}),
)


def _drop_guard_pair(bind) -> None:
    if bind.dialect.name == "sqlite":
        for name, _t, _e, _m in _TRIGGERS:
            op.execute(f"DROP TRIGGER IF EXISTS {name}")
    elif bind.dialect.name == "postgresql":
        for name, table, _e, _m in _TRIGGERS:
            op.execute(f"DROP TRIGGER IF EXISTS {name} ON {table}")


def _recreate_guard_pair(bind) -> None:
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
                    prevent_v2_paper_bridge_mutation();
            """)
    restored = bind.execute(sa.text(
        "SELECT COUNT(*) FROM sqlite_master WHERE type = 'trigger'"
        " AND name LIKE 'v2_paper_bridge_drift_run_immutable_%'"
    )).scalar() if bind.dialect.name == "sqlite" else len(_TRIGGERS)
    if restored != len(_TRIGGERS):
        raise RuntimeError(
            "paper-bridge guard pair NOT restored - manual recovery required")


def _seed_identity(payload: dict) -> str:
    return payload.get("name", "generation_staleness")


def upgrade() -> None:
    bind = op.get_bind()
    # DEL-004 existing-set filter (content-keyed on seed_name + bound name)
    existing = {
        (row[0], _seed_identity(json.loads(row[1])))
        for row in bind.execute(sa.text(
            "SELECT seed_name, payload FROM v2_paper_bridge_drift_run"
            " WHERE run_kind = 'seed' AND seed_name IS NOT NULL"))
    }
    for seed_name, payload in _SEED_ROWS:
        if (seed_name, _seed_identity(payload)) in existing:
            continue
        bind.execute(sa.text(
            "INSERT INTO v2_paper_bridge_drift_run"
            " (id, run_kind, seed_name, payload, actor_id, data_class,"
            "  mode, operator_id, correlation_id, created_at)"
            " VALUES (:id, 'seed', :seed_name, :payload, :act, 'simulated',"
            "  'PAPER', :act, NULL, :created_at)"
        ).bindparams(
            id=str(uuid.uuid4()), seed_name=seed_name,
            payload=json.dumps(payload), act=_ACT_REF,
            created_at=_CREATED_AT))


def downgrade() -> None:
    bind = op.get_bind()
    pre = bind.execute(sa.text(
        "SELECT COUNT(*) FROM v2_paper_bridge_drift_run"
        " WHERE run_kind = 'seed' AND actor_id = :act"
    ).bindparams(act=_ACT_REF)).scalar()
    _drop_guard_pair(bind)
    for seed_name, payload in _SEED_ROWS:
        if seed_name == "drift_tolerance":
            bind.execute(sa.text(
                "DELETE FROM v2_paper_bridge_drift_run"
                " WHERE run_kind = 'seed' AND seed_name = :sn"
                " AND actor_id = :act"
                " AND json_extract(payload, '$.name') = :fname"
            ).bindparams(sn=seed_name, act=_ACT_REF,
                         fname=payload["name"]))
        else:
            bind.execute(sa.text(
                "DELETE FROM v2_paper_bridge_drift_run"
                " WHERE run_kind = 'seed' AND seed_name = :sn"
                " AND actor_id = :act"
            ).bindparams(sn=seed_name, act=_ACT_REF))
    post = bind.execute(sa.text(
        "SELECT COUNT(*) FROM v2_paper_bridge_drift_run"
        " WHERE run_kind = 'seed' AND actor_id = :act"
    ).bindparams(act=_ACT_REF)).scalar()
    if post != 0 or (pre - post) > len(_SEED_ROWS):
        raise RuntimeError(
            f"overlay downgrade count law violated: pre={pre} post={post}")
    _recreate_guard_pair(bind)
