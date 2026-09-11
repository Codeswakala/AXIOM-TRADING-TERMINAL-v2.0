"""BE-9 read-only adapter contract (design S1.4; BO T-3).

Fetch-unit vocabulary (T-20 N-2, canonical): a "page" is the canonical
fetch unit returned by one adapter call; a "window" is the TIME SPAN a
history page covers (A-8: 24h span, 1h overlap). Pages carry provenance;
windows are declared facts inside history-page provenance.

The V1 `BrokerPort` protocol is NOT reused (it carries `OrderIntent` —
a mutation shape). This Protocol is the closed six-verb vocabulary; the
census test asserts exactly these six members — any seventh fails the
suite. No method named or shaped for mutation exists.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Final, Protocol

# --- Sealed registry + the Q9-successor environment binding (S1.4) -------------
BROKER_READ_PROVIDERS: Final = MappingProxyType(
    {"exness_mt5_demo": "app.v2.broker_read.providers.exness_mt5"})

# Q9 successor: code-pinned binding. Literals delivered by the Operator's
# pre-INT pinning act of 2026-09-05 (D-5 provisioning record; pinned facts,
# not credentials — the investor password never enters code). The
# `environment` value is the governed class 'practice' (schema CHECK law);
# the Operator's account label ("AXIOM") is recorded in the pinning record.
ENVIRONMENT_BINDING: Final = MappingProxyType({
    "provider_id": "exness_mt5_demo",
    "server_hostname": "ExnessKE-MT5Trial9",
    "account_number": "476910140",
    "environment": "practice",
})

BINDING_PENDING_VALUE = "PENDING-OPERATOR-PIN"

# --- Typed refusal taxonomy (S1.3; E-ENV-1) ------------------------------------
REFUSAL_CLASSES = (
    "broker.terminal.unavailable",   # FIRST-CLASS: local MT5 absent/not logged in
    "broker.unavailable",            # terminal up, server-side unreachable
    "broker.auth.refused",
    "broker.auth.misprovisioned",    # master-login detected (T-2)
    "broker.entity.unknown",
    "broker.payload.invalid",
    "broker.timeout",
    "broker.fetch_budget.exceeded",
    "broker.binding.mismatch",       # Q9-successor assertion failure
    "broker.no_data",                # no complete sync has ever landed (Q7)
)

# Sync/reconcile vocabularies (S4/S5/S6)
SYNC_OUTCOMES = ("complete", "partial_refused", "failed")
RECONCILE_OUTCOMES = ("clean", "discrepant")
DISCREPANCY_CLASSES = (
    "amount_mismatch", "missing_on_broker", "missing_in_axiom",
    "currency_mismatch", "timestamp_window", "permission_visibility",
    "set_mismatch",
)
DISCREPANCY_STATES = ("detected", "triaged", "owned", "resolved",
                      "dismissed_with_reason")
DISCREPANCY_TRANSITIONS = (
    ("detected", "triaged"), ("triaged", "owned"),
    ("owned", "resolved"), ("owned", "dismissed_with_reason"),
)

# Fetch-budget + window law (A-7/A-8; per-window limits, terminal envelope)
FETCH_BUDGET_PAGES_PER_MODEL = 200
HISTORY_WINDOW_HOURS = 24
HISTORY_OVERLAP_HOURS = 1

# T-20 N-4: first-sync ORIGIN rule — history windows begin at the
# account-creation basis when the terminal reports it; otherwise the
# BO-declared origin floor below (DA rationale: a demo account created
# 2026-09-05 has no meaningful history before the band's own era; the
# floor bounds the first sync deterministically). The origin fact used is
# recorded on the first sync run row.
ORIGIN_FLOOR_ISO = "2026-09-01T00:00:00+00:00"

_DOMAIN = "v2.broker_read"


@dataclass(frozen=True)
class PageProvenance:
    """Pinned on every page (S1.2): identity, binding echo, time basis."""

    provider_id: str
    server_hostname: str
    account_number: str
    environment: str
    fetch_basis: str          # 'server_time' | 'local_time_secondary'
    fetched_at: str
    window_start: str | None = None
    window_end: str | None = None
    page_index: int = 0


@dataclass(frozen=True)
class BrokerAccountsPage:
    records: tuple = ()
    provenance: PageProvenance | None = None


@dataclass(frozen=True)
class BrokerSummaryPage:
    records: tuple = ()
    provenance: PageProvenance | None = None


@dataclass(frozen=True)
class BrokerPositionsPage:
    records: tuple = ()
    provenance: PageProvenance | None = None


@dataclass(frozen=True)
class BrokerOrdersPage:
    records: tuple = ()
    provenance: PageProvenance | None = None


@dataclass(frozen=True)
class BrokerTransactionsPage:
    records: tuple = ()
    provenance: PageProvenance | None = None


@dataclass(frozen=True)
class BrokerInstrumentsPage:
    records: tuple = ()
    provenance: PageProvenance | None = None


class BrokerReadContract(Protocol):
    """The closed six-verb READ vocabulary (N1 type arm). Census-tested."""

    async def read_accounts(self) -> BrokerAccountsPage: ...

    async def read_account_summary(self) -> BrokerSummaryPage: ...

    async def read_positions(self) -> BrokerPositionsPage: ...

    async def read_orders(self) -> BrokerOrdersPage: ...

    async def read_transactions(
        self, window_start: str, window_end: str,
        page_index: int) -> BrokerTransactionsPage: ...

    async def read_instrument_permissions(self) -> BrokerInstrumentsPage: ...


# The census law: exactly these six verb names, nothing else (T-3).
CONTRACT_VERBS: Final = (
    "read_accounts", "read_account_summary", "read_positions",
    "read_orders", "read_transactions", "read_instrument_permissions",
)


class BrokerRefused(Exception):
    """Typed refusal; class + reasons always carried; never improvised."""

    def __init__(self, refusal_class: str, reasons: list) -> None:
        assert refusal_class in REFUSAL_CLASSES
        self.refusal_class = refusal_class
        self.reasons = reasons
        super().__init__(f"{refusal_class}: {reasons}")


def assert_environment_binding(observed_server: str, observed_account: str,
                               observed_environment: str) -> None:
    """Q9 successor: re-asserted at every vault unlock AND sync start.

    Mismatch (or an unpinned binding) = typed refusal; a config error
    cannot repoint reads because this binding is hash-pinned code.
    """
    b = ENVIRONMENT_BINDING
    if BINDING_PENDING_VALUE in (b["server_hostname"], b["account_number"]):
        raise BrokerRefused("broker.binding.mismatch", [
            {"failing": "binding", "note":
             "binding pins not yet delivered by the Operator pinning act"}])
    mismatches = []
    for name, pinned, observed in (
            ("server_hostname", b["server_hostname"], observed_server),
            ("account_number", b["account_number"], observed_account),
            ("environment", b["environment"], observed_environment)):
        if pinned != observed:
            mismatches.append({"failing": name, "pinned": pinned,
                               "observed": observed})
    if mismatches:
        raise BrokerRefused("broker.binding.mismatch", mismatches)
