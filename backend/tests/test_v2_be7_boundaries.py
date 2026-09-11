"""V2 BE-7 boundary + regression completion — BO-V2-BE-7-001 T-8/T-11/T-12
(budget completion to 60; API-surface scan; no-touch regression pair).
"""

from __future__ import annotations

import socket
from datetime import datetime, timedelta, timezone

import pytest

from app.v2.research_jobs.contracts import (
    JOB_STATES,
    JOB_TERMINAL_STATES,
    LIFECYCLE_STATES,
    REGISTRATION_OUTCOMES,
    SCHEDULE_KINDS_V1,
)
from app.v2.research_jobs.leakage import (
    LeakageRefused,
    ReplayWindow,
    validate_horizon_g3,
)
from app.v2.research_jobs.replay import STRATEGY_RULES, CursorSlice, crossover_rule

UTC = timezone.utc
T0 = datetime(2026, 9, 1, tzinfo=UTC)


@pytest.fixture(autouse=True)
def _socket_guard(monkeypatch):
    def _deny(*_a, **_k):
        raise AssertionError("network attempt during BE-7 boundary test")

    monkeypatch.setattr(socket, "getaddrinfo", _deny)
    monkeypatch.setattr(socket, "create_connection", _deny)


# --- vocabulary integrity (1) ---------------------------------------------------


def test_vocabulary_integrity():
    assert JOB_STATES == ("queued", "running", "succeeded", "failed",
                          "cancelled")
    assert set(JOB_TERMINAL_STATES) < set(JOB_STATES)
    assert LIFECYCLE_STATES == ("draft", "registered", "retired")
    assert REGISTRATION_OUTCOMES == ("registered", "reused", "refused")
    assert SCHEDULE_KINDS_V1 == ("manual",)
    assert set(STRATEGY_RULES) == {"threshold", "crossover"}


# --- crossover rule determinism (1) ------------------------------------------------


def test_crossover_rule_deterministic_and_sliced():
    def bars(closes):
        return tuple(
            {"open_time": T0 + timedelta(minutes=15 * i), "close": c}
            for i, c in enumerate(closes))

    params = {"fast": 2, "slow": 4}
    up = bars(["100", "100", "100", "100", "99", "103", "108"])
    slice_ = CursorSlice(bars=up, cursor=up[-1]["open_time"])
    first = crossover_rule(slice_, params)
    second = crossover_rule(slice_, params)
    assert first == second  # deterministic
    short = CursorSlice(bars=up[:2], cursor=up[1]["open_time"])
    assert crossover_rule(short, params) is None  # insufficient = typed None


# --- G-3 boundary values (1) ---------------------------------------------------------


def test_g3_boundary_exactness():
    window = ReplayWindow(window_start=T0,
                          window_end=T0 + timedelta(hours=4),
                          as_of=T0 + timedelta(hours=4))
    # zero horizon always legal
    validate_horizon_g3(label_horizon=timedelta(0),
                        embargo=timedelta(hours=1), window=window)
    # horizon+embargo exactly consuming the window: refused
    with pytest.raises(LeakageRefused):
        validate_horizon_g3(label_horizon=timedelta(hours=3),
                            embargo=timedelta(hours=1), window=window)


# --- window validation edges (1) -------------------------------------------------------


def test_window_degenerate_refused():
    with pytest.raises(LeakageRefused):
        ReplayWindow(window_start=T0, window_end=T0, as_of=T0).validate()


# --- API-surface enumeration scan (1) — exit item v (c) ----------------------------------


def test_api_surface_enumeration_no_execution_vocabulary():
    from fastapi.routing import APIRoute

    from app.v2.research_jobs.api import router

    writer_paths = {
        "/research-jobs/registry/inputs",
        "/research-jobs/registry/cost-models",
        "/research-jobs/registry/strategies",
        "/research-jobs/jobs/submit",
        "/research-jobs/jobs/run",
        "/research-jobs/jobs/cancel",
    }
    banned = ("order", "execute", "broker", "position", "account",
              "paper", "live")
    for route in router.routes:
        if not isinstance(route, APIRoute):
            continue
        for token in banned:
            assert token not in route.path.lower(), route.path
        if "POST" in route.methods:
            assert route.path in writer_paths
        else:
            assert route.methods == {"GET"} or "GET" in route.methods


# --- regression pair (2): protected-band modules untouched by BE-7 ------------------------


def test_regression_prior_band_contracts_untouched():
    """BE-4/BE-5/BE-6 contract vocabularies unchanged by the BE-7 package
    (content assertions, not imports-only)."""
    from app.v2.portfolio_research.contracts import BASIS_LABELS, PORTFOLIO_BASES
    from app.v2.research.typing import FAMILIES
    from app.v2.research_governance.contracts import (
        DEPLOYMENT_CLASSES,
        SIGNAL_FAMILIES,
        SIGNAL_STATES,
    )

    assert PORTFOLIO_BASES == ("hypothetical",)
    assert BASIS_LABELS == ("hypothetical-research",)
    assert SIGNAL_FAMILIES == ("structural", "predictive")
    assert SIGNAL_STATES == ("emitted", "withheld", "expired", "refused")
    assert DEPLOYMENT_CLASSES == ("research", "shadow", "champion",
                                  "challenger", "retired")
    assert len(FAMILIES) == 10


def test_regression_v1_reuse_pins_unchanged():
    """The six §1.0-pinned V1 files re-hash unchanged (T-7 tail)."""
    import hashlib
    from pathlib import Path

    backend = Path(__file__).resolve().parents[1]
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
            (backend / rel).read_bytes()).hexdigest()[:16]
        assert actual == pin, f"{rel}: {actual} != {pin}"
