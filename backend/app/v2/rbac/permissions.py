"""V2 RBAC Permissions — read-only seeded permission definitions.

Per 17_INSTITUTIONAL_SECURITY_STANDARD.md Part VI:
- Default Deny
- Explicit Permission Grant
- Least Privilege
- Complete Auditability

Permissions are seeded during migration. No runtime mutation.
"""

from __future__ import annotations

from enum import Enum


class V2Permission(str, Enum):
    """V2 permission strings."""

    MODE_READ = "v2.mode.read"
    CAPABILITY_READ = "v2.capability.read"
    AUDIT_READ = "v2.audit.read"
    AUDIT_READ_ALL = "v2.audit.read_all"
    LINEAGE_READ = "v2.lineage.read"
    LINEAGE_READ_ALL = "v2.lineage.read_all"
    ERROR_READ = "v2.error.read"
    # BE-2 market data (BO-V2-BE-2-001)
    MARKETDATA_READ = "v2.marketdata.read"
    MARKETDATA_READ_ALL = "v2.marketdata.read_all"
    MARKETDATA_VERIFY = "v2.marketdata.verify"
    MARKETDATA_CATALOG_REFRESH = "v2.marketdata.catalog.refresh"
    # BE-3 P1 provider (BO-V2-BE-3-P1-001) — read-only
    PROVIDER_READ = "v2.marketdata.provider.read"
    PROVIDER_READ_HISTORY = "v2.marketdata.provider.read_history"
    # BE-3 P2 (BO-V2-BE-3-P2-001) — admin-only contract test
    PROVIDER_CONTRACT_TEST = "v2.marketdata.provider.contract_test"
    # BE-4 research read models (BO-V2-BE-4-001; R-1)
    RESEARCH_MC_READ = "v2.research.market_context.read"
    RESEARCH_CI_READ = "v2.research.chart_intelligence.read"
    RESEARCH_MC_COMPUTE = "v2.research.market_context.compute"
    # BE-5 research governance (BO-V2-BE-5-001)
    RESEARCH_MLGOV_READ = "v2.research.ml_governance.read"
    RESEARCH_MLGOV_DECIDE = "v2.research.ml_governance.decide"
    RESEARCH_SIGNAL_READ = "v2.research.signal.read"
    RESEARCH_SIGNAL_EMIT = "v2.research.signal.emit"
    RESEARCH_MLDIAG_READ = "v2.research.ml_diagnostics.read"
    # BE-6 portfolio research (BO-V2-BE-6-001)
    RESEARCH_PF_READ = "v2.research.portfolio.read"
    RESEARCH_PF_DEFINE = "v2.research.portfolio.define"
    RESEARCH_PFRISK_READ = "v2.research.portfolio_risk.read"
    RESEARCH_PFRISK_COMPUTE = "v2.research.portfolio_risk.compute"
    # BE-7 research jobs (BO-V2-BE-7-001)
    RESEARCH_JOBS_READ = "v2.research.jobs.read"
    RESEARCH_JOBS_SUBMIT = "v2.research.jobs.submit"
    RESEARCH_JOBS_CANCEL = "v2.research.jobs.cancel"
    RESEARCH_REGISTRY_READ = "v2.research.registry.read"
    RESEARCH_REGISTRY_WRITE = "v2.research.registry.write"
    RESEARCH_RESULTS_READ = "v2.research.results.read"
    # BE-8 paper trading (BO-V2-BE-8-001 D-3; D-1 scoped marker exemption)
    PAPER_ACCOUNTS_READ = "v2.paper.accounts.read"
    PAPER_ACCOUNTS_MANAGE = "v2.paper.accounts.manage"
    PAPER_ORDERS_READ = "v2.paper.orders.read"
    PAPER_ORDERS_PLACE = "v2.paper.orders.place"
    PAPER_ORDERS_CANCEL = "v2.paper.orders.cancel"
    PAPER_ORDERS_CONFIRM = "v2.paper.orders.confirm"
    PAPER_FILLS_READ = "v2.paper.fills.read"
    PAPER_RISK_READ = "v2.paper.risk.read"
    # BE-9 broker read (BO-V2-BE-9-001 D-3; DECISION-1 scoped marker exemption)
    BROKER_ACCOUNTS_READ = "v2.broker.accounts.read"
    BROKER_BALANCES_READ = "v2.broker.balances.read"
    BROKER_POSITIONS_READ = "v2.broker.positions.read"
    BROKER_ORDERS_FILLS_READ = "v2.broker.orders_fills.read"
    BROKER_SYNC_RUN = "v2.broker.sync.run"
    BROKER_DISCREPANCY_MANAGE = "v2.broker.discrepancy.manage"
    BROKER_VAULT_MANAGE = "v2.broker.vault.manage"
    # BE-10 account context (BO-V2-BE-10-001; third literal-prefix exemption)
    ACCOUNT_CONTEXT_READ = "v2.account_context.read"
    # BE-11 paper bridge (BO-V2-BE-11-001 SS0 proposed enum; no marker
    # collision - no exemption needed; 'v2.paper_bridge.' is NOT
    # 'v2.paper.' under the trailing-dot law and carries no banned token)
    PAPER_BRIDGE_INTENT_WRITE = "v2.paper_bridge.intent.write"
    PAPER_BRIDGE_EVALUATE_WRITE = "v2.paper_bridge.evaluate.write"
    PAPER_BRIDGE_LEDGER_READ = "v2.paper_bridge.ledger.read"
    PAPER_BRIDGE_DRIFT_READ = "v2.paper_bridge.drift.read"
    # BE-12A live exec (BO-V2-BE12A-001 AM-1: fourth literal-prefix
    # exemption 'v2.live_exec.' — the 'live' marker is crossed
    # DELIBERATELY under the adopted REQ S-1/AM-1; trailing-dot law;
    # 'v2.live.*' and 'v2.live_execution.*' are NOT exempt)
    LIVE_EXEC_INTENT_WRITE = "v2.live_exec.intent.write"
    LIVE_EXEC_EVALUATE_WRITE = "v2.live_exec.evaluate.write"
    LIVE_EXEC_INTENTS_READ = "v2.live_exec.intents.read"
    # BE-12B (BO-V2-BE12B-001 SS1.g; same AM-1 exemption family)
    LIVE_EXEC_SUBMIT_WRITE = "v2.live_exec.submit.write"
    LIVE_EXEC_SUBMISSIONS_READ = "v2.live_exec.submissions.read"
    LIVE_EXEC_FILLS_READ = "v2.live_exec.fills.read"
    # BE-12C (BO-V2-BE12C-001 SS1.g; same AM-1 exemption family)
    LIVE_EXEC_MODIFY_WRITE = "v2.live_exec.modify.write"
    LIVE_EXEC_MODIFIES_READ = "v2.live_exec.modifies.read"
    # BE-12D (BO-V2-BE12D-001 SS1.g; same AM-1 exemption family)
    LIVE_EXEC_KILLSWITCH_ARM = "v2.live_exec.killswitch.arm"
    LIVE_EXEC_KILLSWITCH_PULL = "v2.live_exec.killswitch.pull"
    LIVE_EXEC_KILLSWITCH_CLEAR = "v2.live_exec.killswitch.clear"
    LIVE_EXEC_KILLSWITCH_READ = "v2.live_exec.killswitch.read"
    LIVE_EXEC_ACTIVATION_READ = "v2.live_exec.activation.read"
    LIVE_EXEC_ACTIVATION_TEMPLATE_READ = (
        "v2.live_exec.activation.template.read")
    # BE-12E (BO-V2-BE12E-001 SS1.g; same AM-1 exemption family)
    LIVE_EXEC_RECONCILE_RUN = "v2.live_exec.reconcile.run"
    LIVE_EXEC_RECONCILE_READ = "v2.live_exec.reconcile.read"
    LIVE_EXEC_INCIDENT_OPEN = "v2.live_exec.incident.open"
    LIVE_EXEC_INCIDENT_CLOSE = "v2.live_exec.incident.close"
    LIVE_EXEC_INCIDENT_READ = "v2.live_exec.incident.read"


# Role → permissions mapping
V2_ROLE_PERMISSIONS: dict[str, frozenset[str]] = {
    "admin": frozenset({
        V2Permission.MODE_READ.value,
        V2Permission.CAPABILITY_READ.value,
        V2Permission.AUDIT_READ.value,
        V2Permission.AUDIT_READ_ALL.value,
        V2Permission.LINEAGE_READ.value,
        V2Permission.LINEAGE_READ_ALL.value,
        V2Permission.ERROR_READ.value,
        V2Permission.MARKETDATA_READ.value,
        V2Permission.MARKETDATA_READ_ALL.value,
        V2Permission.MARKETDATA_VERIFY.value,
        V2Permission.MARKETDATA_CATALOG_REFRESH.value,
        V2Permission.PROVIDER_READ.value,
        V2Permission.PROVIDER_READ_HISTORY.value,
        V2Permission.PROVIDER_CONTRACT_TEST.value,
        V2Permission.RESEARCH_MC_READ.value,
        V2Permission.RESEARCH_CI_READ.value,
        V2Permission.RESEARCH_MC_COMPUTE.value,
        V2Permission.RESEARCH_MLGOV_READ.value,
        V2Permission.RESEARCH_MLGOV_DECIDE.value,
        V2Permission.RESEARCH_SIGNAL_READ.value,
        V2Permission.RESEARCH_SIGNAL_EMIT.value,
        V2Permission.RESEARCH_MLDIAG_READ.value,
        V2Permission.RESEARCH_PF_READ.value,
        V2Permission.RESEARCH_PF_DEFINE.value,
        V2Permission.RESEARCH_PFRISK_READ.value,
        V2Permission.RESEARCH_PFRISK_COMPUTE.value,
        V2Permission.RESEARCH_JOBS_READ.value,
        V2Permission.RESEARCH_JOBS_SUBMIT.value,
        V2Permission.RESEARCH_JOBS_CANCEL.value,
        V2Permission.RESEARCH_REGISTRY_READ.value,
        V2Permission.RESEARCH_REGISTRY_WRITE.value,
        V2Permission.RESEARCH_RESULTS_READ.value,
        V2Permission.PAPER_ACCOUNTS_READ.value,
        V2Permission.PAPER_ACCOUNTS_MANAGE.value,
        V2Permission.PAPER_ORDERS_READ.value,
        V2Permission.PAPER_ORDERS_PLACE.value,
        V2Permission.PAPER_ORDERS_CANCEL.value,
        V2Permission.PAPER_ORDERS_CONFIRM.value,
        V2Permission.PAPER_FILLS_READ.value,
        V2Permission.PAPER_RISK_READ.value,
        V2Permission.BROKER_ACCOUNTS_READ.value,
        V2Permission.BROKER_BALANCES_READ.value,
        V2Permission.BROKER_POSITIONS_READ.value,
        V2Permission.BROKER_ORDERS_FILLS_READ.value,
        V2Permission.BROKER_SYNC_RUN.value,
        V2Permission.BROKER_DISCREPANCY_MANAGE.value,
        V2Permission.BROKER_VAULT_MANAGE.value,
        V2Permission.ACCOUNT_CONTEXT_READ.value,
        V2Permission.PAPER_BRIDGE_INTENT_WRITE.value,
        V2Permission.PAPER_BRIDGE_EVALUATE_WRITE.value,
        V2Permission.PAPER_BRIDGE_LEDGER_READ.value,
        V2Permission.PAPER_BRIDGE_DRIFT_READ.value,
        V2Permission.LIVE_EXEC_INTENT_WRITE.value,
        V2Permission.LIVE_EXEC_EVALUATE_WRITE.value,
        V2Permission.LIVE_EXEC_INTENTS_READ.value,
        V2Permission.LIVE_EXEC_SUBMIT_WRITE.value,
        V2Permission.LIVE_EXEC_SUBMISSIONS_READ.value,
        V2Permission.LIVE_EXEC_FILLS_READ.value,
        V2Permission.LIVE_EXEC_MODIFY_WRITE.value,
        V2Permission.LIVE_EXEC_MODIFIES_READ.value,
        V2Permission.LIVE_EXEC_KILLSWITCH_ARM.value,
        V2Permission.LIVE_EXEC_KILLSWITCH_PULL.value,
        V2Permission.LIVE_EXEC_KILLSWITCH_CLEAR.value,
        V2Permission.LIVE_EXEC_KILLSWITCH_READ.value,
        V2Permission.LIVE_EXEC_ACTIVATION_READ.value,
        V2Permission.LIVE_EXEC_ACTIVATION_TEMPLATE_READ.value,
        V2Permission.LIVE_EXEC_RECONCILE_RUN.value,
        V2Permission.LIVE_EXEC_RECONCILE_READ.value,
        V2Permission.LIVE_EXEC_INCIDENT_OPEN.value,
        V2Permission.LIVE_EXEC_INCIDENT_CLOSE.value,
        V2Permission.LIVE_EXEC_INCIDENT_READ.value,
    }),
    "operator": frozenset({
        V2Permission.MODE_READ.value,
        V2Permission.CAPABILITY_READ.value,
        V2Permission.AUDIT_READ.value,
        V2Permission.LINEAGE_READ.value,
        V2Permission.ERROR_READ.value,
        V2Permission.MARKETDATA_READ.value,
        V2Permission.MARKETDATA_VERIFY.value,
        V2Permission.PROVIDER_READ.value,
        V2Permission.RESEARCH_MC_READ.value,
        V2Permission.RESEARCH_CI_READ.value,
        V2Permission.RESEARCH_MLGOV_READ.value,
        V2Permission.RESEARCH_SIGNAL_READ.value,
        V2Permission.RESEARCH_MLDIAG_READ.value,
        V2Permission.RESEARCH_PF_READ.value,
        V2Permission.RESEARCH_PFRISK_READ.value,
        V2Permission.RESEARCH_JOBS_READ.value,
        V2Permission.RESEARCH_RESULTS_READ.value,
        # BE-8 note: operator paper grants deferred — the BO-V2-BE-8-001
        # T-13 census pin (57 = 49 + exactly 8 rows) binds; the S7.1
        # roles column's operator reads would make 12. Disclosed in the
        # delivery report; admin-only v1 surface.
    }),
}

# Forbidden permission markers — any V2 permission containing these is rejected
V2_FORBIDDEN_PERMISSION_MARKERS = (
    "gate",
    "execution",
    "execute",
    "order",
    "broker",
    "account",
    "position",
    "live",
    "capital",
    "margin",
)

# SAL classification for each permission
V2_PERMISSION_SAL: dict[str, str] = {
    V2Permission.MODE_READ.value: "SAL-2",
    V2Permission.CAPABILITY_READ.value: "SAL-2",
    V2Permission.AUDIT_READ.value: "SAL-3",
    V2Permission.AUDIT_READ_ALL.value: "SAL-4",
    V2Permission.LINEAGE_READ.value: "SAL-3",
    V2Permission.LINEAGE_READ_ALL.value: "SAL-4",
    V2Permission.ERROR_READ.value: "SAL-2",
    V2Permission.MARKETDATA_READ.value: "SAL-2",
    V2Permission.MARKETDATA_READ_ALL.value: "SAL-4",
    V2Permission.MARKETDATA_VERIFY.value: "SAL-3",
    V2Permission.MARKETDATA_CATALOG_REFRESH.value: "SAL-3",
    V2Permission.PROVIDER_READ.value: "SAL-2",
    V2Permission.PROVIDER_READ_HISTORY.value: "SAL-4",
    V2Permission.PROVIDER_CONTRACT_TEST.value: "SAL-4",
    V2Permission.RESEARCH_MC_READ.value: "SAL-2",
    V2Permission.RESEARCH_CI_READ.value: "SAL-2",
    V2Permission.RESEARCH_MC_COMPUTE.value: "SAL-3",
    V2Permission.RESEARCH_MLGOV_READ.value: "SAL-2",
    V2Permission.RESEARCH_MLGOV_DECIDE.value: "SAL-3",
    V2Permission.RESEARCH_SIGNAL_READ.value: "SAL-2",
    V2Permission.RESEARCH_SIGNAL_EMIT.value: "SAL-3",
    V2Permission.RESEARCH_MLDIAG_READ.value: "SAL-2",
    V2Permission.RESEARCH_PF_READ.value: "SAL-2",
    V2Permission.RESEARCH_PF_DEFINE.value: "SAL-3",
    V2Permission.RESEARCH_PFRISK_READ.value: "SAL-2",
    V2Permission.RESEARCH_PFRISK_COMPUTE.value: "SAL-3",
    V2Permission.RESEARCH_JOBS_READ.value: "SAL-2",
    V2Permission.RESEARCH_JOBS_SUBMIT.value: "SAL-3",
    V2Permission.RESEARCH_JOBS_CANCEL.value: "SAL-3",
    V2Permission.RESEARCH_REGISTRY_READ.value: "SAL-2",
    V2Permission.RESEARCH_REGISTRY_WRITE.value: "SAL-3",
    V2Permission.RESEARCH_RESULTS_READ.value: "SAL-2",
    V2Permission.PAPER_ACCOUNTS_READ.value: "SAL-2",
    V2Permission.PAPER_ACCOUNTS_MANAGE.value: "SAL-3",
    V2Permission.PAPER_ORDERS_READ.value: "SAL-2",
    V2Permission.PAPER_ORDERS_PLACE.value: "SAL-3",
    V2Permission.PAPER_ORDERS_CANCEL.value: "SAL-3",
    V2Permission.PAPER_ORDERS_CONFIRM.value: "SAL-3",
    V2Permission.PAPER_FILLS_READ.value: "SAL-2",
    V2Permission.PAPER_RISK_READ.value: "SAL-2",
    V2Permission.BROKER_ACCOUNTS_READ.value: "SAL-2",
    V2Permission.BROKER_BALANCES_READ.value: "SAL-2",
    V2Permission.BROKER_POSITIONS_READ.value: "SAL-2",
    V2Permission.BROKER_ORDERS_FILLS_READ.value: "SAL-2",
    V2Permission.BROKER_SYNC_RUN.value: "SAL-3",
    V2Permission.BROKER_DISCREPANCY_MANAGE.value: "SAL-3",
    V2Permission.BROKER_VAULT_MANAGE.value: "SAL-4",
    V2Permission.ACCOUNT_CONTEXT_READ.value: "SAL-2",
    V2Permission.PAPER_BRIDGE_INTENT_WRITE.value: "SAL-3",
    V2Permission.PAPER_BRIDGE_EVALUATE_WRITE.value: "SAL-3",
    V2Permission.PAPER_BRIDGE_LEDGER_READ.value: "SAL-2",
    V2Permission.PAPER_BRIDGE_DRIFT_READ.value: "SAL-2",
    V2Permission.LIVE_EXEC_INTENT_WRITE.value: "SAL-4",
    V2Permission.LIVE_EXEC_EVALUATE_WRITE.value: "SAL-4",
    V2Permission.LIVE_EXEC_INTENTS_READ.value: "SAL-2",
    V2Permission.LIVE_EXEC_SUBMIT_WRITE.value: "SAL-4",
    V2Permission.LIVE_EXEC_SUBMISSIONS_READ.value: "SAL-2",
    V2Permission.LIVE_EXEC_FILLS_READ.value: "SAL-2",
    V2Permission.LIVE_EXEC_MODIFY_WRITE.value: "SAL-4",
    V2Permission.LIVE_EXEC_MODIFIES_READ.value: "SAL-2",
    V2Permission.LIVE_EXEC_KILLSWITCH_ARM.value: "SAL-4",
    V2Permission.LIVE_EXEC_KILLSWITCH_PULL.value: "SAL-4",
    V2Permission.LIVE_EXEC_KILLSWITCH_CLEAR.value: "SAL-4",
    V2Permission.LIVE_EXEC_KILLSWITCH_READ.value: "SAL-2",
    V2Permission.LIVE_EXEC_ACTIVATION_READ.value: "SAL-2",
    V2Permission.LIVE_EXEC_ACTIVATION_TEMPLATE_READ.value: "SAL-3",
    V2Permission.LIVE_EXEC_RECONCILE_RUN.value: "SAL-4",
    V2Permission.LIVE_EXEC_RECONCILE_READ.value: "SAL-2",
    V2Permission.LIVE_EXEC_INCIDENT_OPEN.value: "SAL-4",
    V2Permission.LIVE_EXEC_INCIDENT_CLOSE.value: "SAL-4",
    V2Permission.LIVE_EXEC_INCIDENT_READ.value: "SAL-2",
}


def permissions_for_role(role: str) -> frozenset[str]:
    """Return permissions for a role. Unknown roles default-deny."""
    return V2_ROLE_PERMISSIONS.get(role, frozenset())


def has_permission(role: str, permission: str) -> bool:
    """Check if a role has a specific permission."""
    return permission in permissions_for_role(role)


def assert_permission_vocabulary_safe() -> None:
    """Refuse permission vocabularies that encode forbidden execution powers.

    D-1 scoped exemption (ITRGA-REV-V2-BE-8-DESIGN-001 §5, binding
    conditions honored): permissions with EXACTLY the literal prefix
    'v2.paper.' are exempt from the marker scan — the sealed paper domain
    legitimately names account/order/margin/position. The markers remain
    rejected in every other namespace ('v2.paperwork.*' is NOT exempt:
    the test is a literal prefix including the trailing dot). Live
    vocabulary still cannot exist to be named.
    """
    for permission_set in V2_ROLE_PERMISSIONS.values():
        for permission in permission_set:
            lower = permission.lower()
            if lower.startswith("v2.paper."):
                continue  # D-1: single literal prefix test, nothing broader
            if lower.startswith("v2.broker."):
                # DECISION-1 (BE-9): identical mechanism, second literal
                # prefix. 'v2.brokerage.*' is NOT exempt (trailing dot law).
                continue
            if lower.startswith("v2.account_context."):
                # BE-10 (BO-V2-BE-10-001): third literal prefix, same
                # mechanism. 'v2.account.*' and 'v2.account_contexts.*'
                # are NOT exempt (trailing dot + exact-token law).
                continue
            if lower.startswith("v2.live_exec."):
                # BE-12A AM-1 (BO-V2-BE12A-001 SS1.e; adopted REQ S-1):
                # fourth literal prefix — the 'live' marker crossed
                # DELIBERATELY for the capability-before-activation
                # band. 'v2.live.*' and 'v2.live_execution.*' are NOT
                # exempt (trailing dot law). Live BEHAVIOR remains
                # locked at the actuation chokepoint (mode_locked).
                continue
            if any(marker in lower for marker in V2_FORBIDDEN_PERMISSION_MARKERS):
                raise ValueError(f"V2_PERMISSION_FORBIDDEN: {permission}")


# Seed data for v2_permission table
V2_PERMISSION_SEED: list[dict[str, str]] = []
for role, perms in V2_ROLE_PERMISSIONS.items():
    for perm in perms:
        V2_PERMISSION_SEED.append({
            "role": role,
            "permission": perm,
            "sal": V2_PERMISSION_SAL.get(perm, "SAL-2"),
        })
