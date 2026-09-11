"""W5-U05 scenario comparison workspace safety tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import func, select

from app.core.time import utc_now
from app.db.models.scenario_report import ScenarioReport
from app.db.session import session_scope
from app.institutional_intelligence import (
    ScenarioAssumptions,
    ScenarioReportService,
    ScenarioSeriesSpec,
)
from tests.test_scenario_reports import _seed_path


async def _auth_headers(async_client: AsyncClient) -> dict[str, str]:
    login = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login.status_code == 200, login.text
    return {"Authorization": f"Bearer {login.json()['tokens']['access_token']}"}


async def _seed_two_scenarios() -> tuple[str, str]:
    async with session_scope() as session:
        start, end, _ = await _seed_path(session)
        service = ScenarioReportService(session)
        first = (
            await service.create_report(
                series=ScenarioSeriesSpec("forex", "EURUSD", "M1"),
                assumptions=ScenarioAssumptions(
                    scenario_name="hypothetical_minus_two_percent",
                    shock_return=-0.02,
                    horizon_bars=3,
                    volatility_multiplier=1.0,
                ),
                as_of_start=start,
                as_of_end=end,
                actor="pytest",
            )
        ).report
        second = (
            await service.create_report(
                series=ScenarioSeriesSpec("forex", "EURUSD", "M1"),
                assumptions=ScenarioAssumptions(
                    scenario_name="hypothetical_plus_one_percent",
                    shock_return=0.01,
                    horizon_bars=3,
                    volatility_multiplier=1.0,
                ),
                as_of_start=start,
                as_of_end=end,
                actor="pytest",
            )
        ).report
        return first.id, second.id


async def _scenario_count() -> int:
    async with session_scope() as session:
        return int(
            (await session.execute(select(func.count()).select_from(ScenarioReport))).scalar_one()
        )


@pytest.mark.asyncio
async def test_scenario_comparison_reads_existing_reports_and_creates_no_rows(
    async_client: AsyncClient,
) -> None:
    first_id, second_id = await _seed_two_scenarios()
    before_count = await _scenario_count()
    headers = await _auth_headers(async_client)

    for _ in range(3):
        listed = await async_client.get("/api/v1/intelligence/scenario-reports", headers=headers)
        assert listed.status_code == 200, listed.text
        rows = listed.json()
        assert {first_id, second_id}.issubset({row["id"] for row in rows})
        for report_id in (first_id, second_id):
            detail = await async_client.get(
                f"/api/v1/intelligence/scenario-reports/{report_id}", headers=headers
            )
            assert detail.status_code == 200, detail.text
            payload = detail.json()
            assert payload["research_status"] == "research_only"
            assert payload["uncertainty"]["method"] == "historical_volatility_band"
            assert payload["source_artifact_ids"]
            assert "not_a_prediction" in payload["limitations"]

    after_count = await _scenario_count()
    assert after_count == before_count


@pytest.mark.asyncio
async def test_scenario_comparison_api_auth_read_only_and_generate_requires_valid_body(
    async_client: AsyncClient,
) -> None:
    first_id, _ = await _seed_two_scenarios()

    unauth = await async_client.get("/api/v1/intelligence/scenario-reports")
    assert unauth.status_code == 401

    headers = await _auth_headers(async_client)
    list_response = await async_client.get("/api/v1/intelligence/scenario-reports", headers=headers)
    assert list_response.status_code == 200, list_response.text
    detail_response = await async_client.get(
        f"/api/v1/intelligence/scenario-reports/{first_id}", headers=headers
    )
    assert detail_response.status_code == 200, detail_response.text

    # BO-B-04 supersession: POST /intelligence/scenario-reports is now the
    # governed GENERATION endpoint (422 on an invalid body — it exists, it is
    # not a mutation bypass); the other three paths remain nonexistent.
    response = await async_client.post(
        "/api/v1/intelligence/scenario-reports", headers=headers, json={"blocked": True}
    )
    assert response.status_code == 422
    for path in (
        f"/api/v1/intelligence/scenario-reports/{first_id}",
        "/api/v1/intelligence/scenario-reports/generate",
        "/api/v1/intelligence/scenario-reports/compare",
    ):
        response = await async_client.post(path, headers=headers, json={"blocked": True})
        assert response.status_code in {404, 405}


def test_scenario_comparison_workspace_has_no_generation_or_execution_path() -> None:
    root = Path(__file__).resolve().parents[2]
    frontend_path = (
        root
        / "frontend"
        / "src"
        / "components"
        / "terminal"
        / "docks"
        / "ScenarioComparisonPanel.tsx"
    )
    text = frontend_path.read_text(encoding="utf-8")
    forbidden = (
        "ScenarioReportService",
        "create_report",
        "createScenario",
        "computeScenario",
        "generateScenario",
        "scenario generation endpoint",
        "place_order",
        "emit_signal",
        "broker.",
        "allow_execution",
        "gate_open",
        "raw_score",
    )
    for needle in forbidden:
        assert needle not in text


def test_scenario_comparison_workspace_no_new_migration_file() -> None:
    root = Path(__file__).resolve().parents[2]
    versions = root / "backend" / "alembic" / "versions"
    migration_names = {path.name for path in versions.glob("*.py")}
    assert not any("w5_u05" in name or "scenario_comparison" in name for name in migration_names)
    assert "20260717_0025_w5_u03_chart_research_annotations.py" in migration_names


def test_scenario_comparison_uses_current_time_only_for_test_fixture() -> None:
    # Guard against accidental import cleanup removing the UTC fixture dependency.
    assert utc_now().tzinfo is not None
