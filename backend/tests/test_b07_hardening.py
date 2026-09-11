"""BO-B-07 — cross-cutting hardening tests (fail-first).

Pre-fix expectations (b07_probe_prefix.log): no rate limiter (no 429s), no
security headers, no pipeline/resource metrics, the rate-guard disposition is
`formally_deferred`, and the Doc-11 evidence inventory does not exist.
Post-fix: all pinned.
"""

from __future__ import annotations

import pytest
from httpx import AsyncClient

from app.core.config import clear_settings_cache


async def _auth(client: AsyncClient) -> dict[str, str]:
    login = await client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}


def test_b07_rate_limiter_unit_burst_and_failsafe() -> None:
    from app.core.rate_limit import SlidingWindowRateLimiter

    limiter = SlidingWindowRateLimiter(window_seconds=60, ceiling=3)
    assert limiter.config_valid() is True
    for _ in range(3):
        assert limiter.allow("operator-a") is True
    assert limiter.allow("operator-a") is False  # burst beyond ceiling denied
    assert limiter.allow("operator-b") is True  # other operators unaffected

    bad = SlidingWindowRateLimiter(window_seconds=0, ceiling=3)
    assert bad.config_valid() is False
    assert bad.allow("anyone") is False  # fail-safe deny on misconfiguration


def test_b07_rate_limit_write_surface_scope_matches_build_order() -> None:
    from app.core.rate_limit import RATE_LIMITED_PREFIXES

    families = (
        "/api/v1/ingestion/",
        "/api/v1/intelligence/",
        "/api/v1/collaboration/",
        "/api/v1/alerts/",
    )
    assert set(RATE_LIMITED_PREFIXES) == set(families)
    assert "/api/v1/auth/" not in RATE_LIMITED_PREFIXES


@pytest.mark.asyncio
async def test_b07_burst_beyond_ceiling_returns_429(
    async_client: AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("AXIOM_RATE_LIMIT_ENABLED", "true")
    monkeypatch.setenv("AXIOM_RATE_LIMIT_GLOBAL_CEILING", "3")
    monkeypatch.setenv("AXIOM_RATE_LIMIT_PER_ROUTE_CEILING", "3")
    monkeypatch.setenv("AXIOM_RATE_LIMIT_ADMIN_ALLOWLIST", "")
    clear_settings_cache()
    headers = await _auth(async_client)
    payload = {
        "series": {"market_class": "crypto", "symbol": "BTCUSDT", "timeframe": "H1"},
        "as_of_start": "2025-01-01T00:00:00Z",
        "as_of_end": "2025-01-02T00:00:00Z",
    }
    statuses = []
    for _ in range(5):
        response = await async_client.post(
            "/api/v1/intelligence/regime-reports", json=payload, headers=headers
        )
        statuses.append(response.status_code)
    assert 429 in statuses, f"expected a 429 on burst, got {statuses}"
    # The first requests may be 201/422 depending on data — only the burst
    # behavior matters; the 429 body must be minimal (no operator identity).
    burst = [s for s in statuses if s == 429]
    assert len(burst) >= 1
    for _ in range(3):
        response = await async_client.post(
            "/api/v1/intelligence/regime-reports", json=payload, headers=headers
        )
        assert response.status_code == 429
        assert "operator" not in response.text.lower()
    # Read surfaces are NOT rate-limited.
    for _ in range(5):
        listed = await async_client.get(
            "/api/v1/intelligence/regime-reports", headers=headers
        )
        assert listed.status_code == 200
    # The 429 responses carry the security headers too (the headers layer
    # wraps the rate-limit layer).
    throttled = await async_client.post(
        "/api/v1/intelligence/regime-reports", json=payload, headers=headers
    )
    assert throttled.status_code == 429
    assert throttled.headers.get("x-frame-options") == "DENY"
    assert throttled.headers.get("x-content-type-options") == "nosniff"


@pytest.mark.asyncio
async def test_b07_admin_allowlist_honored(
    async_client: AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("AXIOM_RATE_LIMIT_ENABLED", "true")
    monkeypatch.setenv("AXIOM_RATE_LIMIT_GLOBAL_CEILING", "2")
    monkeypatch.setenv("AXIOM_RATE_LIMIT_PER_ROUTE_CEILING", "2")
    monkeypatch.setenv("AXIOM_RATE_LIMIT_ADMIN_ALLOWLIST", "admin")
    clear_settings_cache()
    headers = await _auth(async_client)
    payload = {
        "series": {"market_class": "crypto", "symbol": "BTCUSDT", "timeframe": "H1"},
        "as_of_start": "2025-01-01T00:00:00Z",
        "as_of_end": "2025-01-02T00:00:00Z",
    }
    statuses = []
    for _ in range(5):
        response = await async_client.post(
            "/api/v1/intelligence/regime-reports", json=payload, headers=headers
        )
        statuses.append(response.status_code)
    assert 429 not in statuses, f"allowlisted admin must bypass, got {statuses}"


@pytest.mark.asyncio
async def test_b07_security_headers_present(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.headers.get("x-content-type-options") == "nosniff"
    assert response.headers.get("x-frame-options") == "DENY"
    assert response.headers.get("referrer-policy") == "strict-origin-when-cross-origin"
    csp = response.headers.get("content-security-policy")
    assert csp and "default-src 'none'" in csp


@pytest.mark.asyncio
async def test_b07_metrics_include_pipelines_and_resources(
    async_client: AsyncClient,
) -> None:
    headers = await _auth(async_client)
    response = await async_client.get("/api/v1/metrics", headers=headers)
    assert response.status_code == 200
    body = response.json()
    observability = body["observability"]
    assert "pipelines" in observability
    assert "resources" in observability
    resources = observability["resources"]
    assert "process_cpu_user_seconds" in resources or "process_cpu_time_seconds" in resources


def test_b07_rate_guard_disposition_implemented() -> None:
    from app.institutional_platform.readiness import RATE_GUARD_DISPOSITION

    assert RATE_GUARD_DISPOSITION.status == "implemented"
    assert RATE_GUARD_DISPOSITION.technical_debt_id == "TD-W7-U07-RATE-GUARD"


def test_b07_doc11_evidence_inventory_exists_and_disclaims_certification() -> None:
    from pathlib import Path

    doc = (
        Path(__file__).resolve().parents[1]
        / "docs"
        / "DOC11_EVIDENCE_INVENTORY.md"
    )
    assert doc.is_file(), "Doc 11 evidence inventory missing"
    text = doc.read_text(encoding="utf-8")
    categories = (
        "security",
        "secrets",
        "state management",
        "error management",
        "deployment",
        "performance",
        "accessibility",
        "operational",
    )
    lowered = text.lower()
    for category in categories:
        assert category in lowered, f"category {category!r} not mapped"
    assert "not certified" in lowered or "no certification claim" in lowered
    # No affirmative certification claim anywhere: "is certified" never
    # appears, and the un-negated "production certified" phrase never does
    # (the posture phrase always carries the negation between the words).
    assert "is certified" not in lowered
    assert "production certified" not in lowered


def test_b07_rate_limit_module_has_no_actuation_surface() -> None:
    from pathlib import Path

    module = (
        Path(__file__).resolve().parents[1] / "app" / "core" / "rate_limit.py"
    ).read_text(encoding="utf-8")
    forbidden = (
        "place_order",
        "cancel_order",
        "OrderIntent",
        "BrokerRepository",
        "ExecutionService",
    )
    assert all(term not in module for term in forbidden)
    assert "time.monotonic" in module  # sliding-window clock discipline
