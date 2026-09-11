"""BE-9 Exness/MT5 provider leg — the ONLY real adapter (design S1.2/S1.3).

Maps the closed six-verb contract onto the official `MetaTrader5` Python
integration (Windows-native, A-2 posture). The import is DEFERRED and
guarded: on the DA/test station the package is absent and every verb
refuses typed `broker.terminal.unavailable` — E-ENV-1's first-class
fact, never an improvised error. The suite exercises the contract via
the fixture provider; THIS leg's live contact happens only inside the
separately-authorized E1 evidence act on the operator console (plain
wifi, witnessed transcript).

Terminal-courtesy law: sequential calls only, no parallel fan-out (v1).
Fetch unit vocabulary: page = one adapter call's return; window = the
time span a history page covers (24h span, 1h overlap — A-8).
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.v2.broker_read.contract import (
    ENVIRONMENT_BINDING,
    FETCH_BUDGET_PAGES_PER_MODEL,
    HISTORY_OVERLAP_HOURS,
    HISTORY_WINDOW_HOURS,
    BrokerAccountsPage,
    BrokerInstrumentsPage,
    BrokerOrdersPage,
    BrokerPositionsPage,
    BrokerRefused,
    BrokerSummaryPage,
    BrokerTransactionsPage,
    PageProvenance,
    assert_environment_binding,
)

PROVIDER_ID = "exness_mt5_demo"


def _terminal():
    """Deferred import; absence or init failure = the E-ENV-1 typed fact."""
    try:
        import MetaTrader5 as mt5  # noqa: N813 - provider package name
    except ImportError as exc:
        raise BrokerRefused("broker.terminal.unavailable", [
            {"failing": "terminal", "note": "MetaTrader5 package not"
             " importable on this station", "detail": str(exc)}]) from exc
    if not mt5.initialize():
        raise BrokerRefused("broker.terminal.unavailable", [
            {"failing": "terminal", "note": "MT5 initialize() False -"
             " terminal absent/not logged in (E-ENV-1)"}])
    return mt5


def _provenance(mt5, window_start: str | None = None,
                window_end: str | None = None,
                page_index: int = 0) -> PageProvenance:
    info = mt5.account_info()
    if info is None:
        raise BrokerRefused("broker.unavailable", [
            {"failing": "account_info", "note": "terminal up, no account"
             " session (server-side or login failure)"}])
    observed_server = str(getattr(info, "server", ""))
    observed_account = str(getattr(info, "login", ""))
    # Q9 successor: re-asserted here on every page build.
    assert_environment_binding(observed_server, observed_account,
                               ENVIRONMENT_BINDING["environment"])
    return PageProvenance(
        provider_id=PROVIDER_ID, server_hostname=observed_server,
        account_number=observed_account,
        environment=ENVIRONMENT_BINDING["environment"],
        fetch_basis="server_time",
        fetched_at=datetime.now(timezone.utc).isoformat(),
        window_start=window_start, window_end=window_end,
        page_index=page_index)


def read_only_login_asserted(mt5) -> bool:
    """T-2 scope probe: FACT read only — no mutation attempt ever.

    MT5 exposes `trade_allowed`-class flags on account/terminal info; an
    investor login reports trading disallowed. Master-login detection is
    the caller's typed refusal (`broker.auth.misprovisioned`)."""
    info = mt5.account_info()
    if info is None:
        raise BrokerRefused("broker.unavailable", [
            {"failing": "account_info"}])
    return not bool(getattr(info, "trade_allowed", True))


class ExnessMt5ReadProvider:
    """The six read verbs; sequential; every page provenance-pinned."""

    async def read_accounts(self) -> BrokerAccountsPage:
        mt5 = _terminal()
        prov = _provenance(mt5)
        info = mt5.account_info()
        record = {
            "broker_account_ext_id": str(info.login),
            "alias": str(getattr(info, "name", "")),
            "currency": str(getattr(info, "currency", "")),
            "environment": ENVIRONMENT_BINDING["environment"],
            "read_only_login": read_only_login_asserted(mt5),
        }
        return BrokerAccountsPage(records=(record,), provenance=prov)

    async def read_account_summary(self) -> BrokerSummaryPage:
        mt5 = _terminal()
        prov = _provenance(mt5)
        info = mt5.account_info()
        record = {
            "broker_account_ext_id": str(info.login),
            "balance": str(info.balance),
            "margin_used": str(getattr(info, "margin", "0")),
            "margin_available": str(getattr(info, "margin_free", "0")),
            "unrealized_pl": str(getattr(info, "profit", "0")),
            "currency": str(getattr(info, "currency", "")),
        }
        return BrokerSummaryPage(records=(record,), provenance=prov)

    async def read_positions(self) -> BrokerPositionsPage:
        mt5 = _terminal()
        prov = _provenance(mt5)
        rows = mt5.positions_get() or ()
        records = tuple({
            "broker_account_ext_id": prov.account_number,
            "instrument_ext_id": str(p.symbol),
            "units_long": str(p.volume) if p.type == 0 else "0",
            "units_short": str(p.volume) if p.type == 1 else "0",
            "avg_price_long": str(p.price_open) if p.type == 0 else "0",
            "avg_price_short": str(p.price_open) if p.type == 1 else "0",
            "position_ext_id": str(p.ticket),
        } for p in rows)
        return BrokerPositionsPage(records=records, provenance=prov)

    async def read_orders(self) -> BrokerOrdersPage:
        mt5 = _terminal()
        prov = _provenance(mt5)
        rows = mt5.orders_get() or ()
        records = tuple({
            "order_ext_id": str(o.ticket),
            "broker_account_ext_id": prov.account_number,
            "order_state_ext": str(getattr(o, "state", "")),
            "payload": {"type": str(getattr(o, "type", "")),
                        "volume": str(getattr(o, "volume_current", "")),
                        "price": str(getattr(o, "price_open", "")),
                        "symbol": str(getattr(o, "symbol", ""))},
        } for o in rows)
        return BrokerOrdersPage(records=records, provenance=prov)

    async def read_transactions(self, window_start: str, window_end: str,
                                page_index: int) -> BrokerTransactionsPage:
        if page_index >= FETCH_BUDGET_PAGES_PER_MODEL:
            raise BrokerRefused("broker.fetch_budget.exceeded", [
                {"failing": "page_index", "value": page_index,
                 "ceiling": FETCH_BUDGET_PAGES_PER_MODEL}])
        mt5 = _terminal()
        prov = _provenance(mt5, window_start=window_start,
                           window_end=window_end, page_index=page_index)
        start = datetime.fromisoformat(window_start)
        end = datetime.fromisoformat(window_end)
        deals = mt5.history_deals_get(start, end) or ()
        records = tuple({
            "transaction_ext_id": str(d.ticket),
            "broker_account_ext_id": prov.account_number,
            "tx_type_ext": str(getattr(d, "type", "")),
            "instrument_ext_id": str(getattr(d, "symbol", "")),
            "units": str(getattr(d, "volume", "")),
            "price": str(getattr(d, "price", "")),
            "tx_time_ext": str(getattr(d, "time", "")),
        } for d in deals)
        return BrokerTransactionsPage(records=records, provenance=prov)

    async def read_instrument_permissions(self) -> BrokerInstrumentsPage:
        mt5 = _terminal()
        prov = _provenance(mt5)
        symbols = mt5.symbols_get() or ()
        records = tuple({
            "broker_account_ext_id": prov.account_number,
            "instrument_ext_id": str(s.name),
            "visibility": {"visible": bool(getattr(s, "visible", False)),
                           "trade_mode": str(getattr(s, "trade_mode", ""))},
            "display_name": str(getattr(s, "description", "")),
        } for s in symbols)
        return BrokerInstrumentsPage(records=records, provenance=prov)


def history_windows(origin_iso: str, until_iso: str) -> list[tuple[str, str]]:
    """A-8 window law: 24h spans, 1h overlap, origin-floored (T-20 N-4)."""
    start = datetime.fromisoformat(origin_iso)
    until = datetime.fromisoformat(until_iso)
    windows: list[tuple[str, str]] = []
    cursor = start
    while cursor < until:
        w_end = min(cursor + timedelta(hours=HISTORY_WINDOW_HOURS), until)
        windows.append((cursor.isoformat(), w_end.isoformat()))
        if w_end >= until:
            break
        cursor = w_end - timedelta(hours=HISTORY_OVERLAP_HOURS)
    return windows
