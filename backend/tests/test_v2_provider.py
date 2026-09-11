"""V2 BE-3 P1 unit tests — network deny, credential non-access, normalizer,
symbols, resilience (synthetic policies), inert URL builder.
"""

from __future__ import annotations

import os
import socket
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from app.v2.errors.contract import V2Error
from app.v2.marketdata.providers.contract import (
    ALLOWED_PROVIDER_HOST,
    P1_NETWORK_ENABLED,
    CredentialState,
    FixtureCredentialResolver,
    FixtureTransport,
    PlannedRequest,
    ProviderAdapter,
    plan_request,
)
from app.v2.marketdata.providers.resilience import (
    CircuitBreaker,
    SyntheticPolicy,
    TokenBucket,
    backoff_schedule,
    should_retry,
)
from app.v2.marketdata.providers.twelvedata.adapter import FIXTURES_ROOT, TwelveDataAdapter
from app.v2.marketdata.providers.twelvedata.symbols import to_canonical, to_td

UTC = timezone.utc
PROVIDERS_DIR = Path(__file__).resolve().parents[1] / "app" / "v2" / "marketdata" / "providers"


def _policy(**overrides) -> SyntheticPolicy:
    base = dict(
        label="synthetic:test-policy",
        max_requests_per_window=3,
        window_seconds=60,
        max_retries=3,
        backoff_base_seconds=1.0,
        breaker_failure_threshold=3,
        breaker_cooldown_seconds=60,
    )
    base.update(overrides)
    return SyntheticPolicy(**base)


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    """Fail the test on ANY outbound network attempt (BO §4)."""

    def _deny(*_a, **_k):  # pragma: no cover — must never fire
        raise AssertionError("P1 outbound network attempt detected")

    monkeypatch.setattr(socket, "socket", _deny)
    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)
    yield


class TestNetworkDeny:
    def test_network_flag_is_hard_false(self):
        assert P1_NETWORK_ENABLED is False

    def test_non_fixture_transport_refused_and_security_logged(self, caplog):
        """DEL-002 control: refusal emits a structured SECURITY log line."""
        import logging

        class RogueTransport:
            kind = "http"

        with caplog.at_level(logging.WARNING):
            with pytest.raises(V2Error) as excinfo:
                ProviderAdapter(transport=RogueTransport())  # type: ignore[arg-type]
        assert "fixture transport only" in excinfo.value.detail
        assert any(
            "provider.network_refused" in r.message for r in caplog.records
        ), "refusal was not security-logged"

    def test_live_entry_points_refuse_and_security_logged(self, caplog):
        import logging

        adapter = TwelveDataAdapter()
        with caplog.at_level(logging.WARNING):
            with pytest.raises(V2Error):
                adapter.fetch_live("forex.eurusd")
            with pytest.raises(V2Error):
                adapter.connect()
        refusals = [r for r in caplog.records if "provider.live_refused" in r.message]
        assert len(refusals) == 2, "live refusals were not security-logged"

    def test_no_forbidden_transport_imports_in_providers_package(self):
        """Static assertion: no transport lib import anywhere in providers/
        EXCEPT transport.py — the sole authorized P2 network module
        (BO-V2-BE-3-P2-001 §3.2), whose construction is token-gated to the
        authenticated endpoint chain and covered by its own boundary tests."""
        forbidden = ("import httpx", "import aiohttp", "import websockets",
                     "from httpx", "from aiohttp", "from websockets",
                     "import socket", "from socket")
        offenders = []
        for py in PROVIDERS_DIR.rglob("*.py"):
            if py.name == "transport.py":
                continue
            text = py.read_text()
            for marker in forbidden:
                if marker in text:
                    offenders.append(f"{py.name}: {marker}")
        assert offenders == [], offenders

    def test_planned_request_is_inert_and_redacted(self):
        planned = plan_request("/time_series", {"symbol": "EUR/USD", "apikey": "WOULD-BE-SECRET"})
        assert isinstance(planned, PlannedRequest)
        assert planned.host == ALLOWED_PROVIDER_HOST
        assert "WOULD-BE-SECRET" not in planned.redacted()
        assert "apikey=[REDACTED]" in planned.redacted()
        # inert: no execute/send/perform surface
        assert not any(hasattr(planned, m) for m in ("execute", "send", "perform", "run"))


class TestCredentialNonAccess:
    def test_resolver_always_absent(self):
        resolver = FixtureCredentialResolver()
        assert resolver.get("twelvedata") == CredentialState.ABSENT
        assert resolver.get("anything") == CredentialState.ABSENT

    def test_env_variable_present_but_never_read(self, monkeypatch):
        """PLAN-005 proof: placeholder set; P1 code never queries it."""
        monkeypatch.setenv("AXIOM_TD_API_KEY", "TD_TEST_KEY_PLACEHOLDER")
        queried: list[str] = []
        real_getenv = os.getenv
        real_getitem = os.environ.__class__.__getitem__

        def spy_getenv(key, default=None):
            queried.append(key)
            return real_getenv(key, default)

        def spy_getitem(self_, key):
            queried.append(key)
            return real_getitem(self_, key)

        monkeypatch.setattr(os, "getenv", spy_getenv)
        monkeypatch.setattr(os.environ.__class__, "__getitem__", spy_getitem)

        adapter = TwelveDataAdapter()
        adapter.descriptor()
        adapter.supported_symbol("forex.eurusd")
        bars = adapter.fetch_bars_fixture(
            "forex.eurusd", "M1", fixture_name="time_series_eurusd_ok.json"
        )
        assert bars
        resolver = FixtureCredentialResolver()
        resolver.get("twelvedata")

        secretish = [k for k in queried if "TD_API" in k or "APIKEY" in k.upper()]
        assert secretish == [], f"P1 code queried provider-secret env vars: {secretish}"

    def test_descriptor_is_truthful(self):
        d = TwelveDataAdapter().descriptor()
        assert d.source_status == "architecture_candidate"
        assert d.entitlement_status == "unverified"
        assert d.transport_kind == "fixture"
        assert d.network_enabled is False


class TestSymbols:
    def test_exact_universe(self):
        assert to_canonical("EUR/USD") == "forex.eurusd"
        assert to_td("crypto.btcusd") == "BTC/USD"
        assert to_canonical("DOGE/USD") is None
        assert to_td("forex.zzz") is None


class TestNormalizer:
    def test_ok_fixture_normalizes_ascending_utc(self):
        bars = TwelveDataAdapter().fetch_bars_fixture(
            "forex.eurusd", "M1", fixture_name="time_series_eurusd_ok.json"
        )
        assert len(bars) == 5
        times = [b.open_time for b in bars]
        assert times == sorted(times)
        assert all(t.tzinfo is not None for t in times)
        assert all(b.low <= b.open <= b.high and b.low <= b.close <= b.high for b in bars)

    def test_volume_fixture(self):
        bars = TwelveDataAdapter().fetch_bars_fixture(
            "crypto.btcusd", "M1", fixture_name="time_series_btcusd_ok.json"
        )
        assert all(b.volume is not None and b.volume > 0 for b in bars)

    def test_quote_fixture(self):
        q = TwelveDataAdapter().fetch_quote_fixture(
            "forex.eurusd", fixture_name="quote_eurusd_ok.json"
        )
        assert q["instrument_id"] == "forex.eurusd"
        assert q["as_of"].endswith("+00:00")

    def test_error_shape_refused(self):
        with pytest.raises(V2Error) as excinfo:
            TwelveDataAdapter().fetch_bars_fixture(
                "forex.eurusd", "M1", fixture_name="error_invalid_key.json"
            )
        assert excinfo.value.status_code == 502

    def test_rate_limit_shape_refused(self):
        with pytest.raises(V2Error):
            TwelveDataAdapter().fetch_bars_fixture(
                "forex.eurusd", "M1", fixture_name="error_rate_limit.json"
            )

    def test_symbol_echo_mismatch_refused(self):
        with pytest.raises(V2Error) as excinfo:
            TwelveDataAdapter().fetch_bars_fixture(
                "forex.eurusd", "M1", fixture_name="time_series_mismatched_symbol.json"
            )
        assert "misdelivered" in excinfo.value.detail

    def test_malformed_numeric_refused(self):
        with pytest.raises(V2Error):
            TwelveDataAdapter().fetch_bars_fixture(
                "forex.eurusd", "M1", fixture_name="time_series_malformed.json"
            )

    def test_ohlc_insanity_refused(self):
        with pytest.raises(V2Error):
            TwelveDataAdapter().fetch_bars_fixture(
                "forex.eurusd", "M1", fixture_name="time_series_ohlc_insane.json"
            )

    def test_missing_fixture_is_honest_unavailable(self):
        with pytest.raises(V2Error) as excinfo:
            TwelveDataAdapter().fetch_bars_fixture(
                "forex.eurusd", "M1", fixture_name="does_not_exist.json"
            )
        assert excinfo.value.status_code == 404

    def test_fixture_path_traversal_refused(self):
        with pytest.raises(V2Error):
            FixtureTransport(FIXTURES_ROOT).load("../secrets.json")

    def test_determinism(self):
        a = TwelveDataAdapter().fetch_bars_fixture(
            "forex.eurusd", "M1", fixture_name="time_series_eurusd_ok.json"
        )
        b = TwelveDataAdapter().fetch_bars_fixture(
            "forex.eurusd", "M1", fixture_name="time_series_eurusd_ok.json"
        )
        assert a == b


class TestResilienceSyntheticOnly:
    def test_policy_label_enforced(self):
        with pytest.raises(ValueError, match="synthetic test policies only"):
            SyntheticPolicy(
                label="twelvedata:free-tier",
                max_requests_per_window=8,
                window_seconds=60,
                max_retries=3,
                backoff_base_seconds=1.0,
                breaker_failure_threshold=5,
                breaker_cooldown_seconds=60,
            )

    def test_token_bucket_refuses_on_exhaustion(self):
        bucket = TokenBucket(_policy(max_requests_per_window=2))
        now = datetime(2026, 8, 24, 12, 0, tzinfo=UTC)
        assert bucket.try_acquire(now=now) is True
        assert bucket.try_acquire(now=now) is True
        assert bucket.try_acquire(now=now) is False  # honest refusal
        later = now + timedelta(seconds=61)
        assert bucket.try_acquire(now=later) is True  # window reset

    def test_backoff_schedule_deterministic(self):
        assert backoff_schedule(_policy(backoff_base_seconds=1.0, max_retries=3)) == [1.0, 2.0, 4.0]

    def test_retry_matrix(self):
        p = _policy()
        assert should_retry("transport", 0, p) is True
        assert should_retry("5xx", 1, p) is True
        assert should_retry("429", 2, p) is True
        assert should_retry("4xx", 0, p) is False  # never retry auth/entitlement
        assert should_retry("transport", 3, p) is False  # exhausted

    def test_breaker_full_cycle_in_memory(self):
        breaker = CircuitBreaker(_policy(breaker_failure_threshold=3, breaker_cooldown_seconds=60))
        now = datetime(2026, 8, 24, 12, 0, tzinfo=UTC)
        assert breaker.state == CircuitBreaker.CLOSED
        for _ in range(3):
            breaker.record_failure(now=now)
        assert breaker.state == CircuitBreaker.OPEN
        assert breaker.allow(now=now) is False  # no hammering
        assert breaker.degraded_view() == {"availability": "unavailable", "freshness": "unknown"}
        probe_time = now + timedelta(seconds=61)
        assert breaker.allow(now=probe_time) is True  # HALF_OPEN probe
        assert breaker.state == CircuitBreaker.HALF_OPEN
        breaker.record_failure(now=probe_time)
        assert breaker.state == CircuitBreaker.OPEN  # failed probe reopens
        recovered = probe_time + timedelta(seconds=61)
        assert breaker.allow(now=recovered) is True
        breaker.record_success()
        assert breaker.state == CircuitBreaker.CLOSED

    def test_breaker_transitions_not_persisted(self):
        """PLAN-006: the breaker has no session, repo, or audit dependency."""
        import ast
        import inspect

        import app.v2.marketdata.providers.resilience as resilience

        src = inspect.getsource(resilience)
        tree = ast.parse(src)
        # Check actual imports, not docstring prose
        imported: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.extend(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.append(node.module)
        forbidden_modules = [
            m for m in imported
            if any(t in m for t in ("db.", "audit", "repositor", "sqlalchemy"))
        ]
        assert forbidden_modules == [], (
            f"resilience module imports persistence/audit modules: {forbidden_modules}"
        )


class TestFixtureHygiene:
    def test_fixtures_marked_and_secret_free(self):
        """OBS 1: every fixture is marked static/candidate; leak-hunt clean."""
        fixture_files = list(FIXTURES_ROOT.glob("*.json"))
        assert fixture_files, "no fixtures found"
        for f in fixture_files:
            text = f.read_text()
            assert "_fixture_note" in text, f"{f.name} missing static-candidate marker"
            assert "TD_TEST_KEY_PLACEHOLDER" not in text
            # no live-data claim markers
            assert "live:provider" not in text
        readme = (FIXTURES_ROOT / "README.md").read_text()
        assert "unverified" in readme.lower()
