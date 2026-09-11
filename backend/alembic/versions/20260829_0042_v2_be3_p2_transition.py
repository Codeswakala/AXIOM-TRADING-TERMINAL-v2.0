"""V2 BE-3 P2 status transition: architecture_candidate → contract_tested
(Twelve Data) — BO-V2-BE-3-P2-TRANS-001; plan AXIOM-V2-BE-3-P2-TRANS-PLAN-001
v1.1.0 (APPROVED, ITRGA-DET-V2-BE-3-P2-TRANS-PLAN-001).

The SOLE authorized provider-status change. Design summary:
- default-deny precondition chain P-1…P-8 before any mutation;
- durable refusal audit via independent connection (TR-003 fallback:
  ``REFUSAL AUDIT WRITE FAILED: <precondition-name>``);
- P-2 no-op branch: already-applied re-run = clean audited no-op (TR-001);
- guard drop → mutate (provider UPDATE + ONE history append) → recreate →
  verify; history triggers NEVER dropped;
- downgrade = reversal append (history 2→3), state restored; post-reversal
  re-upgrade refused by P-5 by design.

Revision ID: 20260829_0042
Revises: 20260825_0041
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from uuid import uuid4

import sqlalchemy as sa

from alembic import op

revision = "20260829_0042"
down_revision = "20260825_0041"
branch_labels = None
depends_on = None

# --- Embedded constants (BO §2.2 — cited, never re-derived) -----------------
AUTHORITY_REF = "BO-V2-BE-3-P2-TRANS-001"
EVIDENCE_REF = (
    "ITRGA-DET-V2-BE-3-P2-FINAL-001"
    " · run a246607c-f0c5-42e9-8f3b-a1e1bd75fa83"
)
_AUTHORITY_ENV = "AXIOM_TD_TRANSITION_AUTHORITY_REF"

FROM_STATUS = "architecture_candidate"
TO_STATUS = "contract_tested"
PROVIDER_ID = "twelvedata"


# --- Durable refusal audit (independent connection; TR-003 fallback) --------


def _durable_refusal_audit(precondition_name: str) -> None:
    """Write the refusal audit through a dedicated, independently committed
    connection so it survives the migration's rollback. If this write itself
    fails, raise the distinct TR-003 error — never proceed silently, never
    mask the failed precondition (it appears in the error AND the SECURITY
    log line, which fires regardless of the audit-sink state)."""
    import logging

    logging.getLogger("axiom.security").warning(
        "SECURITY provider.status_transition.refused precondition=%s",
        precondition_name,
    )
    try:
        bind = op.get_bind()
        engine = bind.engine
        with engine.connect() as independent:
            independent.execute(
                sa.text(
                    "INSERT INTO v2_audit_event"
                    " (id, correlation_id, actor_id, actor_type, domain,"
                    "  action, mode, classification, details, created_at)"
                    " VALUES (:id, :cid, 'migration', 'operator',"
                    "  'v2.marketdata', 'provider.status_transition.refused',"
                    "  :mode, 'internal', :details, :now)"
                ),
                {
                    "id": str(uuid4()),
                    "cid": str(uuid4()),
                    "mode": os.environ.get("AXIOM_V2_MODE", "RESEARCH"),
                    "details": (
                        '{"failed_precondition": "%s", "authority_ref": "%s"}'
                        % (precondition_name, AUTHORITY_REF)
                    ),
                    "now": datetime.now(timezone.utc),
                },
            )
            independent.commit()
    except Exception as audit_exc:  # TR-003 pinned fallback
        raise RuntimeError(
            f"REFUSAL AUDIT WRITE FAILED: {precondition_name}"
        ) from audit_exc


def _refuse(precondition_name: str) -> None:
    _durable_refusal_audit(precondition_name)
    raise RuntimeError(
        f"P2 status transition refused: precondition {precondition_name} failed"
        " — zero side effects"
    )


# --- Guard handling (0041-proven pattern; provider triggers only) -----------


def _drop_registry_guard(bind) -> None:
    if bind.dialect.name == "postgresql":
        op.execute("DROP TRIGGER IF EXISTS v2_md_provider_immutable ON v2_md_provider")
    elif bind.dialect.name == "sqlite":
        op.execute("DROP TRIGGER IF EXISTS v2_md_provider_immutable_update")
        op.execute("DROP TRIGGER IF EXISTS v2_md_provider_immutable_delete")


def _create_registry_guard(bind) -> None:
    if bind.dialect.name == "postgresql":
        op.execute("""
            CREATE TRIGGER v2_md_provider_immutable
            BEFORE UPDATE OR DELETE ON v2_md_provider
            FOR EACH ROW EXECUTE FUNCTION prevent_v2_md_provider_mutation();
        """)
    elif bind.dialect.name == "sqlite":
        op.execute("""
            CREATE TRIGGER v2_md_provider_immutable_update
            BEFORE UPDATE ON v2_md_provider
            BEGIN
                SELECT RAISE(ABORT, 'V2 provider registry is immutable in P1; UPDATE prohibited');
            END;
        """)
        op.execute("""
            CREATE TRIGGER v2_md_provider_immutable_delete
            BEFORE DELETE ON v2_md_provider
            BEGIN
                SELECT RAISE(ABORT, 'V2 provider registry is immutable in P1; DELETE prohibited');
            END;
        """)


def _verify_guard_present(bind) -> None:
    if bind.dialect.name == "postgresql":
        count = bind.execute(
            sa.text(
                "SELECT COUNT(*) FROM pg_trigger WHERE tgname='v2_md_provider_immutable'"
            )
        ).scalar_one()
        expected = 1
    elif bind.dialect.name == "sqlite":
        count = bind.execute(
            sa.text(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger' AND name IN"
                " ('v2_md_provider_immutable_update','v2_md_provider_immutable_delete')"
            )
        ).scalar_one()
        expected = 2
    else:  # pragma: no cover
        return
    if int(count) != expected:
        raise RuntimeError(
            "P2 transition migration: registry guard NOT restored — manual"
            " recovery required; do not treat this migration as applied"
        )


def _verify_transition_consistent(bind) -> None:
    """SQLite interruption safety: status and history count must agree."""
    status = bind.execute(
        sa.text(
            "SELECT source_status FROM v2_md_provider WHERE provider_id = :p"
        ),
        {"p": PROVIDER_ID},
    ).scalar_one()
    history = int(
        bind.execute(
            sa.text(
                "SELECT COUNT(*) FROM v2_md_provider_status_history"
                " WHERE provider_id = :p"
            ),
            {"p": PROVIDER_ID},
        ).scalar_one()
    )
    consistent = (status == TO_STATUS and history == 2) or (
        status == FROM_STATUS and history in (1, 3)
    )
    if not consistent:
        raise RuntimeError(
            "P2 transition migration: status/history INCONSISTENT"
            f" (status={status}, history={history}) — manual recovery required"
        )


def _in_transaction_audit(bind, action: str, details_json: str) -> None:
    """start/complete/downgraded events ride the migration transaction —
    atomic with the change (if the transition rolls back, so do they)."""
    bind.execute(
        sa.text(
            "INSERT INTO v2_audit_event"
            " (id, correlation_id, actor_id, actor_type, domain, action,"
            "  mode, classification, details, created_at)"
            " VALUES (:id, :cid, 'migration', 'operator', 'v2.marketdata',"
            "  :action, :mode, 'internal', :details, :now)"
        ),
        {
            "id": str(uuid4()),
            "cid": str(uuid4()),
            "action": action,
            "mode": os.environ.get("AXIOM_V2_MODE", "RESEARCH"),
            "details": details_json,
            "now": datetime.now(timezone.utc),
        },
    )


# --- Upgrade ------------------------------------------------------------------


def upgrade() -> None:
    bind = op.get_bind()

    # P-1: authority-ref gate (exact string; BO §2.2)
    if os.environ.get(_AUTHORITY_ENV) != AUTHORITY_REF:
        _refuse("P-1:authority_ref")

    row = bind.execute(
        sa.text(
            "SELECT source_status, entitlement_status, persistence_permitted"
            " FROM v2_md_provider WHERE provider_id = :p"
        ),
        {"p": PROVIDER_ID},
    ).one_or_none()
    if row is None:
        _refuse("P-2:provider_missing")
    source_status, entitlement_status, persistence_permitted = row

    # P-2: status check with the pinned no-op branch (TR-001; BO §2.1 —
    # short-circuits the remaining preconditions)
    if source_status == TO_STATUS:
        note = '{"no_op": "already-applied", "authority_ref": "%s"}' % AUTHORITY_REF
        _in_transaction_audit(bind, "provider.status_transition.start", note)
        _in_transaction_audit(bind, "provider.status_transition.complete", note)
        return  # clean audited no-op: no mutation, exit 0
    if source_status != FROM_STATUS:
        _refuse("P-2:source_status")

    # P-3: verified entitlement
    if entitlement_status != "verified":
        _refuse("P-3:entitlement_status")

    # P-4: persistence flag false (and must remain false)
    if persistence_permitted not in (False, 0):
        _refuse("P-4:persistence_permitted")

    # P-5: history genesis-only
    history_count = int(
        bind.execute(
            sa.text(
                "SELECT COUNT(*) FROM v2_md_provider_status_history"
                " WHERE provider_id = :p"
            ),
            {"p": PROVIDER_ID},
        ).scalar_one()
    )
    if history_count != 1:
        _refuse("P-5:history_count")

    # P-6: basis constants embedded (AUTHORITY_REF / EVIDENCE_REF) — n/a check

    # P-7: mode valid
    mode = os.environ.get("AXIOM_V2_MODE", "RESEARCH")
    if mode not in ("RESEARCH", "SIMULATION"):
        _refuse("P-7:mode")

    # P-8: reserved authority still inactive
    active = bind.execute(
        sa.text("SELECT active FROM v2_md_source WHERE source_id = :p"),
        {"p": PROVIDER_ID},
    ).scalar_one_or_none()
    if active not in (False, 0):
        _refuse("P-8:reserved_authority_active")

    # --- authorized mutation (atomic with start/complete audits) ------------
    now = datetime.now(timezone.utc)
    details = (
        '{"provider_id": "%s", "from": "%s", "to": "%s",'
        ' "authority_ref": "%s", "evidence_ref": "%s"}'
        % (PROVIDER_ID, FROM_STATUS, TO_STATUS, AUTHORITY_REF, EVIDENCE_REF)
    )
    _in_transaction_audit(bind, "provider.status_transition.start", details)

    _drop_registry_guard(bind)
    bind.execute(
        sa.text(
            "UPDATE v2_md_provider SET source_status = :to_status"
            " WHERE provider_id = :p"
        ),
        {"to_status": TO_STATUS, "p": PROVIDER_ID},
    )
    bind.execute(
        sa.text(
            "INSERT INTO v2_md_provider_status_history"
            " (id, provider_id, from_status, to_status, authority_ref,"
            "  evidence_ref, operator_id, created_at)"
            " VALUES (:id, :p, :from_status, :to_status, :aref, :eref,"
            "  NULL, :now)"
        ),
        {
            "id": str(uuid4()),
            "p": PROVIDER_ID,
            "from_status": FROM_STATUS,
            "to_status": TO_STATUS,
            "aref": AUTHORITY_REF,
            "eref": EVIDENCE_REF,
            "now": now,
        },
    )
    _create_registry_guard(bind)
    _verify_guard_present(bind)
    _verify_transition_consistent(bind)

    _in_transaction_audit(
        bind,
        "provider.status_transition.complete",
        '{"history_count": 2, "post_status": "%s",'
        ' "persistence_permitted": false}' % TO_STATUS,
    )


# --- Downgrade (reversal append — never deletion; plan Part 5.2) --------------


def downgrade() -> None:
    bind = op.get_bind()

    # TRD-001: guard presence is verified BEFORE the early return so an
    # interrupted prior downgrade (guard dropped, status reverted, reversal
    # append missing — SQLite per-statement DDL only) raises loudly instead
    # of being masked as a silent exit-0 completion. A clean
    # never-transitioned/no-op database passes this check trivially (the
    # guard exists from 0040/0041) and then takes the early return.
    _verify_guard_present(bind)

    status = bind.execute(
        sa.text("SELECT source_status FROM v2_md_provider WHERE provider_id = :p"),
        {"p": PROVIDER_ID},
    ).scalar_one_or_none()
    if status != TO_STATUS:
        # nothing to reverse (e.g. downgrading a no-op/never-transitioned DB)
        return

    now = datetime.now(timezone.utc)
    _drop_registry_guard(bind)
    bind.execute(
        sa.text(
            "UPDATE v2_md_provider SET source_status = :from_status"
            " WHERE provider_id = :p"
        ),
        {"from_status": FROM_STATUS, "p": PROVIDER_ID},
    )
    bind.execute(
        sa.text(
            "INSERT INTO v2_md_provider_status_history"
            " (id, provider_id, from_status, to_status, authority_ref,"
            "  evidence_ref, operator_id, created_at)"
            " VALUES (:id, :p, :from_status, :to_status, :aref,"
            "  'governed downgrade (reversal append)', NULL, :now)"
        ),
        {
            "id": str(uuid4()),
            "p": PROVIDER_ID,
            "from_status": TO_STATUS,
            "to_status": FROM_STATUS,
            "aref": AUTHORITY_REF + " (downgrade)",
            "now": now,
        },
    )
    _create_registry_guard(bind)
    _verify_guard_present(bind)

    _in_transaction_audit(
        bind,
        "provider.status_transition.downgraded",
        '{"reversal": true, "history_count": 3}',
    )
