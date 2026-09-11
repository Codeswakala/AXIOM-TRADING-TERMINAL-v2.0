"""V2 BE-9 boundary tests — BO-V2-BE-9-001 T-5/T-6/T-8/T-16/T-20.

N2 frontend scan; N3 wall from the PAPER side; PGF-021; V1 pins;
prior-band regression; T-16 provision-pin compliance; T-20 N-2/N-3
vocabulary laws.
"""

from __future__ import annotations

import ast
import hashlib
import socket
from pathlib import Path

import pytest

BACKEND = Path(__file__).resolve().parents[1]
REPO = BACKEND.parent
BROKER_DIR = BACKEND / "app/v2/broker_read"
PAPER_DIR = BACKEND / "app/v2/paper_trading"


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-9 test")

    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)


# --- T-5: N2 — no provider hostname outside the sealed binding ---------------------


def test_n2_no_provider_hostname_in_frontend():
    frontend = REPO / "frontend"
    if not frontend.exists():
        return  # no frontend tree on this station: vacuously holds
    for ext in ("*.ts", "*.tsx", "*.js", "*.jsx", "*.html"):
        for f in frontend.rglob(ext):
            if "node_modules" in str(f):
                continue
            text = f.read_text(errors="ignore").lower()
            for token in ("exness", "metatrader", "mt5", "broker_read"):
                assert token not in text, f"{token} in {f}"


def test_n2_hostname_only_in_binding():
    """The server-hostname concept lives only in contract.py (the sealed
    binding) and the provider leg's provenance echo."""
    allowed = {"contract.py", "exness_mt5.py"}
    for f in BROKER_DIR.rglob("*.py"):
        if f.name in allowed:
            continue
        text = f.read_text()
        assert "Exness-MT5" not in text, f.name
        assert "ExnessKE" not in text, f.name  # the pinned real hostname
        assert "476910140" not in text, f.name  # the pinned account
        assert "PENDING-OPERATOR-PIN" not in text, f.name


# --- T-6: N3 wall from the PAPER side (both-sides law) -----------------------------


def test_n3_paper_wall_from_paper_side():
    for f in PAPER_DIR.rglob("*.py"):
        tree = ast.parse(f.read_text())
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            for name in names:
                assert "broker" not in name.lower(), f"{f.name}: {name}"


def test_n3_no_cross_fk_between_domains():
    """No paper model column references broker tables and vice versa."""
    broker_model = (BACKEND / "app/db/models/v2_broker_read.py").read_text()
    paper_model = (BACKEND / "app/db/models/v2_paper_trading.py").read_text()
    assert "v2_paper" not in broker_model
    assert "v2_broker" not in paper_model


# --- T-18/PGF-021: no filesystem-conditional behavior -------------------------------


def test_pgf021_no_filesystem_conditionals():
    """Domain modules: no Path.exists/is_dir branching; env reads only in
    vault.py (the unlock act) — never behavioral branching."""
    for f in BROKER_DIR.rglob("*.py"):
        text = f.read_text()
        for marker in (".exists()", ".is_dir()"):
            assert marker not in text, f"{marker} in {f.name}"
        if f.name != "vault.py":
            assert "os.environ" not in text, f.name
            assert "os.getenv" not in text, f.name


# --- T-16: provision-pin compliance + money law -------------------------------------


def test_t16_cent_environment_refused_at_binding():
    """Provision pin: a cent-denominated environment (Standard Cent) is
    structurally refused — the binding admits 'practice' only, and the
    account currency law is USD whole-unit (USC is the cent marker)."""
    from app.v2.broker_read.contract import ENVIRONMENT_BINDING
    assert ENVIRONMENT_BINDING["environment"] == "practice"
    # currency law: the reconcile comparison is exact-decimal; a USC
    # currency string would surface as currency_mismatch, never silently
    from app.v2.broker_read.reconcile import _detect
    broker = {"balances": [{"broker_account_ext_id": "1",
                            "balance": "1000000", "margin_used": "0",
                            "margin_available": "1000000",
                            "unrealized_pl": "0", "currency": "USC"}]}
    projection = {"balances": [{"broker_account_ext_id": "1",
                                "balance": "10000", "margin_used": "0",
                                "margin_available": "10000",
                                "unrealized_pl": "0", "currency": "USD"}]}
    found = _detect(broker, projection, {})
    assert any(d["class"] == "currency_mismatch" for d in found)


def test_t16_exact_decimal_no_tolerance():
    from app.v2.broker_read.reconcile import _dec_eq
    assert _dec_eq("10000.00", "10000.0000")   # numeric equality
    assert not _dec_eq("10000.00", "10000.01")  # any diff = discrepancy


# --- T-20: N-2 vocabulary / N-3 REST-era terms absent --------------------------------


def test_t20_n2_page_window_vocabulary_declared():
    text = (BROKER_DIR / "contract.py").read_text()
    assert 'a "page" is the canonical' in text
    assert "TIME SPAN" in text


def test_t20_n3_no_rest_era_vocabulary():
    """The 429/token-bucket line must NOT appear (terminal-courtesy only)."""
    for f in BROKER_DIR.rglob("*.py"):
        text = f.read_text().lower()
        assert "token bucket" not in text, f.name
        assert "token-bucket" not in text, f.name
        assert "rate_limited" not in text, f.name
        assert "retry-after" not in text, f.name


def test_t20_n4_origin_rule_pinned():
    from app.v2.broker_read.contract import ORIGIN_FLOOR_ISO
    assert ORIGIN_FLOOR_ISO == "2026-09-01T00:00:00+00:00"
    from app.v2.broker_read.providers.exness_mt5 import history_windows
    windows = history_windows(ORIGIN_FLOOR_ISO,
                              "2026-09-03T00:00:00+00:00")
    assert windows[0][0] == "2026-09-01T00:00:00+00:00"  # floored
    # A-8: 24h span, 1h overlap
    assert windows[0][1] == "2026-09-02T00:00:00+00:00"
    assert windows[1][0] == "2026-09-01T23:00:00+00:00"


# --- regression: V1 pins + prior bands ------------------------------------------------


def test_regression_v1_reuse_pins_unchanged():
    pins = {
        "app/ml/dataset/chronology_guard.py": "7dbc665dc4b43f31",
        "app/ml/dataset/split_engine.py": "e893b92c6ccce188",
        "app/ml/dataset/snapshot_builder.py": "b08ef4b1dec07567",
        "app/ml/dataset/service.py": "6c5d72a8942050b4",
        "app/execution_research/simulation.py": "f163e610ba1a6215",
        "app/ml/economic/service.py": "c49527ed12f4d2ca",
    }
    for rel, pin in pins.items():
        actual = hashlib.sha256(
            (BACKEND / rel).read_bytes()).hexdigest()[:16]
        assert actual == pin, f"{rel}: {actual} != {pin}"


def test_regression_prior_band_contracts_untouched():
    from app.v2.paper_trading.contracts import (
        FILL_CLASSES,
        INTENT_SIDES,
        INTENT_TYPES,
    )
    from app.v2.research_jobs.contracts import (
        CONSTRUCTIBLE_RESULT_CLASSES,
        COST_UNITS_V1,
        RESULT_CLASS_TAXONOMY,
    )

    assert FILL_CLASSES == ("paper_simulated",)
    assert INTENT_SIDES == ("buy", "sell")
    assert INTENT_TYPES == ("market", "limit")
    assert RESULT_CLASS_TAXONOMY == ("backtest", "simulation", "paper",
                                     "live")
    assert CONSTRUCTIBLE_RESULT_CLASSES == ("backtest", "simulation")
    assert COST_UNITS_V1 == ("price", "fraction")
    from app.v2.mode.contract import DEFERRED_MODES, VALID_MODES
    assert VALID_MODES == ("RESEARCH", "SIMULATION", "PAPER")
    assert DEFERRED_MODES == ("LIVE",)
